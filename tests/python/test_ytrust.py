#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Траст-слой Y (заказ автора 2026-11-23 «Сделай траст-слой Y», Коул §7
«ACTIVE POOLS И TRUST — обязательный следующий шаг»):

  specs/y-trust.json  — HIGH (hit) / MID (нет улик или ok) / LOW (miss),
                        генерируется: python3 tools/oracle.py trust --rebuild
  oracle.py pool      — active_trust_count / window_eligible_count (Коул §7.3–7.4)
  oracle.py draw --trust — CLOCK-жребий только по HIGH+MID ≤ потолка 80

Прогон: python3 -m unittest discover -s tests/python -v
"""

import json
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO / "tools"))

import gates  # noqa: E402
import oracle  # noqa: E402


def load(name):
    return json.loads((REPO / "specs" / name).read_text(encoding="utf-8"))


def verdict_slot_map(batch):
    """слот → Y-карта каноническим парсером печи (тот же маппер, что в oracle)."""
    _, _, slots = gates.parse_batch(REPO / "batches" / f"{batch}.md")
    return {s.sid: s.y_card for s in slots if s.y_card}


class TestTrustRegistry(unittest.TestCase):
    """Реестр specs/y-trust.json: улики из JSON-вердиктов (Коул §7.1)."""

    @classmethod
    def setUpClass(cls):
        cls.reg = load("y-trust.json")
        cls.cards = cls.reg["cards"]

    def test_registry_shape(self):
        self.assertEqual(self.reg["id"], "y-trust")
        self.assertEqual(self.reg["version"], "1.0.0")
        self.assertIn("ceiling", self.reg["policy"])
        self.assertLessEqual(self.reg["policy"]["ceiling"], 80)
        self.assertIn("regenerate", self.reg["policy"])
        for cid, c in self.cards.items():
            self.assertIn(c["trust"], ("HIGH", "MID", "LOW"), cid)
            self.assertIsInstance(c["hits"], int)
            self.assertIsInstance(c["misses"], int)
            for ev in c["evidence"]:
                self.assertIn(ev["kind"], ("loved", "hypothesis", "ok_with_issues", "miss"))
                self.assertTrue(ev["slot"].startswith("P"), ev)

    def test_sources_cover_json_verdicts(self):
        """Каждый t5-verdict/1 в verdicts/ обязан быть в sources реестра
        (валидатор — проверка №15; здесь — тот же инвариант)."""
        vfiles = []
        for vf in sorted((REPO / "verdicts").glob("*.json")):
            d = json.loads(vf.read_text(encoding="utf-8"))
            if d.get("schema") == "t5-verdict/1":
                vfiles.append(vf.name)
        self.assertEqual([s["file"] for s in self.reg["sources"]], vfiles,
                         "y-trust.json отстаёт от verdicts/*.json — oracle.py trust --rebuild")

    def test_high_from_loved_and_hypothesis(self):
        """Коул §7.1: hit (loved или подтверждённая гипотеза) → HIGH."""
        for vf in sorted((REPO / "verdicts").glob("*.json")):
            d = json.loads(vf.read_text(encoding="utf-8"))
            if d.get("schema") != "t5-verdict/1":
                continue
            smap = verdict_slot_map(d["batch"])
            hit_slots = ({e.get("slot") for e in d.get("loved") or []}
                         | {e.get("slot") for e in d.get("hypothesis_hits") or []})
            for sid in hit_slots:
                cid = smap.get(sid)
                if cid:
                    self.assertEqual(self.cards[cid]["trust"], "HIGH",
                                     f"{d['batch']} {sid} loved/гипотеза, но {cid} не HIGH")
                    self.assertGreaterEqual(self.cards[cid]["hits"], 1)

    def test_misses_are_low(self):
        """Катана в вердиктной партии мимо loved/ok → LOW (если не искуплена хитом)."""
        lows = 0
        for vf in sorted((REPO / "verdicts").glob("*.json")):
            d = json.loads(vf.read_text(encoding="utf-8"))
            if d.get("schema") != "t5-verdict/1":
                continue
            smap = verdict_slot_map(d["batch"])
            ok = {e.get("slot") for e in d.get("ok_with_issues") or []}
            hit = ({e.get("slot") for e in d.get("loved") or []}
                   | {e.get("slot") for e in d.get("hypothesis_hits") or []})
            for sid, cid in smap.items():
                if sid not in hit and sid not in ok and self.cards[cid]["hits"] == 0:
                    self.assertEqual(self.cards[cid]["trust"], "LOW",
                                     f"{d['batch']} {sid}: промах {cid} обязан быть LOW")
                    lows += 1
        self.assertGreater(lows, 0, "в двух вердиктных партиях обязаны быть промахи")

    def test_stats_consistent(self):
        st = self.reg["stats"]
        self.assertEqual(st["high"], sum(1 for c in self.cards.values() if c["trust"] == "HIGH"))
        self.assertEqual(st["mid"], sum(1 for c in self.cards.values() if c["trust"] == "MID"))
        self.assertEqual(st["low"], sum(1 for c in self.cards.values() if c["trust"] == "LOW"))
        self.assertEqual(st["judged_batches"], len(self.reg["sources"]))
        self.assertGreaterEqual(st["high"], 1, "T5-27/29 loved дают хотя бы один HIGH")

    def test_cards_exist_in_camera(self):
        cam = load("camera.json")
        ids = {c["id"] for c in cam["y_cards"]["cards"]}
        for cid in self.cards:
            self.assertIn(cid, ids, f"y-trust знает карту {cid}, которой нет в camera.json")

    def test_rebuild_deterministic(self):
        a = oracle.build_trust()
        b = oracle.build_trust()
        self.assertEqual(a, b, "rebuild недетерминирован")


class TestTrustPool(unittest.TestCase):
    """Пул CLOCK (Коул §7.2): HIGH+MID ≤ потолка, LOW исключены,
    MID-приоритет — никогда не катаны раньше."""

    def _cards(self, n=10):
        return [{"id": f"Y{i}", "corridor": "A", "exposureClass": "—",
                 "pattern": f"p{i}", "builtFrom": ""} for i in range(1, n + 1)]

    def test_low_excluded_high_first_ceiling(self):
        cards = self._cards(10)
        usage = {f"Y{i}": {"id": f"Y{i}", "usedCount": 0, "lastBatch": None,
                           "lastBatchFile": None} for i in range(1, 11)}
        trust_cards = {
            "Y1": {"trust": "HIGH"}, "Y2": {"trust": "LOW"}, "Y3": {"trust": "LOW"},
            "Y4": {"trust": "HIGH"},
        }
        pool, st = oracle.trust_pool(cards, usage, 99, 0, None,
                                     trust_cards=trust_cards, ceiling=4)
        ids = [c["id"] for c in pool]
        self.assertNotIn("Y2", ids)
        self.assertNotIn("Y3", ids, "LOW — вне жребия CLOCK")
        self.assertLessEqual("Y1", ids[0])  # HIGH первыми
        self.assertEqual(ids[0], "Y1")
        self.assertIn("Y4", ids[:2])
        self.assertEqual(len(pool), 4, "потолок 4 — пул не больше потолка")
        self.assertEqual(st["ceiling"], 4)

    def test_mid_priority_never_used_first(self):
        cards = self._cards(6)
        usage = {
            "Y1": {"id": "Y1", "usedCount": 5, "lastBatch": 9, "lastBatchFile": "x"},
            "Y2": {"id": "Y2", "usedCount": 1, "lastBatch": 8, "lastBatchFile": "x"},
            "Y3": {"id": "Y3", "usedCount": 0, "lastBatch": None, "lastBatchFile": None},
            "Y4": {"id": "Y4", "usedCount": 0, "lastBatch": None, "lastBatchFile": None},
        }
        pool, st = oracle.trust_pool(cards, usage, 99, 0, None,
                                     trust_cards={}, ceiling=2)
        ids = [c["id"] for c in pool]
        # никогда не катана Y3 (номер меньше Y4) идёт первой среди MID
        self.assertEqual(ids, ["Y3", "Y4"],
                         "MID-приоритет: никогда не катаны → по номеру; катаные позже")

    def test_no_trust_data_all_mid(self):
        """Нет улик по карте → MID (годна по умолчанию, Коул §7.1)."""
        reg = load("y-trust.json")
        lvl = oracle.trust_pool  # smoke: функция доступна
        self.assertTrue(callable(lvl))
        # карты вне реестра ведут себя как MID: в пуле, не LOW.
        # Предусловие честное: живой реестр траста учит вердикты и может
        # содержать Y1–Y4 (урок T5-31: Y2 ушёл в LOW после промаха P01) —
        # поэтому тестируем строго «вне реестра», отфильтровав id тестовых карт.
        cards = self._cards(4)
        usage = {}
        trust_cards = {
            k: v
            for k, v in reg.get("cards", {}).items()
            if k not in {c["id"] for c in cards}
        }
        pool, st = oracle.trust_pool(cards, usage, 99, 0, None,
                                     trust_cards=trust_cards, ceiling=10)
        self.assertEqual(len(pool), 4)


class TrustCliSmoke(unittest.TestCase):
    """CLI-дым: trust/pool/draw печатают числа Коула §7.3."""

    def test_pool_prints_both_counts(self):
        import io
        import contextlib
        buf = io.StringIO()
        import argparse
        args = argparse.Namespace(for_batch="T5-31", depth=3, ids=False)
        with contextlib.redirect_stdout(buf):
            rc = oracle.cmd_pool(args)
        out = buf.getvalue()
        self.assertEqual(rc, 0)
        self.assertIn("window_eligible_count", out, "квитанция обязана нести window_eligible_count")
        self.assertIn("active_trust_count", out, "квитанция обязана нести active_trust_count")
        self.assertIn("window-eligible", out)


if __name__ == "__main__":
    unittest.main()
