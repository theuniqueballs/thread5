#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Юнит-тесты ЗАКОНОВ PROTO-2 тест-горна (unittest, stdlib-only) — протокол
«пробы и ошибки» 2026-11-22 (после вердикта T5-29, уроки В39–В43).

Страховки:
1. ЗОЛОТЫЕ РОЛЛЫ: живые болванки PROTO-2 (777/31337/999/424242) — check
   PASS; жанровый скелет Закона 24 (вольт ≥ 13, ниша 5–8, EXQUISITE 1–4,
   бег ≤ 3), кин-каст ≤ 10, EXP-клетки с H-XX, предикт ≡ состав (В43).
2. ТАМПЕРЫ (законы РЕАЛЬНО стреляют): изъятый жанр → ошибка; кин-каст 11 →
   ошибка; EXP без H-XX → ошибка; дубль карты → ошибка; канон-раса →
   ошибка; NEG без candle/lamp → ошибка; предикт ≠ состав → ошибка;
   жанровый бег 14 → ошибка.
3. ЭРА: проба PROTO-1 (TB-20261122-20261122, битая, 25 причин) — SKIP,
   история не переписывается; genre_plan держит законы на 40 сидах.

Прогон: python3 -m unittest discover -s tests/python -v
"""

import copy
import json
import random
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO / "tools"))
import testforge as tf  # noqa: E402

CORPUS = REPO / "tests" / "test-corpus"
GOLD = ["TB-20261122-777", "TB-20261122-31337",
        "TB-20261122-999", "TB-20261122-424242"]
TRIAL_PROBE = "TB-20261122-20261122"


def load_tb(name: str) -> dict:
    return json.loads((CORPUS / f"{name}.json").read_text(encoding="utf-8"))


class TestGoldenRolls(unittest.TestCase):
    """Живые болванки PROTO-2 — законы В39–В43 держатся на них все."""

    @classmethod
    def setUpClass(cls):
        cls.forge = tf.Forge()

    def test_gold_rolls_exist_and_pass(self):
        for name in GOLD:
            doc = load_tb(name)
            self.assertEqual(doc.get("proto"), 2, f"{name} не PROTO-2")
            errs = tf.check_batch(doc, self.forge)
            self.assertEqual(errs, [], f"{name}: {errs[:4]}")

    def test_genre_skeleton_law24(self):
        for name in GOLD:
            doc = load_tb(name)
            mains = [s for s in doc["slots"] if s["genre"] != "EXP"]
            volt = sum(1 for s in mains if s["genre"] in ("VOLT", "EXQUISITE"))
            niche = sum(1 for s in mains if s["genre"] == "NICHE")
            exq = sum(1 for s in mains if s["genre"] == "EXQUISITE")
            self.assertGreaterEqual(volt, tf.VOLT_MIN, f"{name}: вольт {volt}")
            self.assertTrue(tf.NICHE_MIN <= niche <= tf.NICHE_MAX,
                            f"{name}: ниша {niche}")
            self.assertTrue(tf.EXQ_MIN <= exq <= tf.EXQ_MAX, f"{name}: exq {exq}")

    def test_kin_cap_v40(self):
        for name in GOLD:
            doc = load_tb(name)
            mains = [s for s in doc["slots"] if s["genre"] != "EXP"]
            kin = sum(1 for s in mains if s["race"] != "R01")
            self.assertLessEqual(kin, tf.KIN_CAP, f"{name}: кин {kin}/21")

    def test_exp_cells_hypotheses_v42(self):
        shelf = {h["id"] for h in json.loads(
            (REPO / "specs" / "open-hypotheses.json").read_text(
                encoding="utf-8"))["hypotheses"]}
        for name in GOLD:
            doc = load_tb(name)
            exps = [s for s in doc["slots"] if s["genre"] == "EXP"]
            self.assertEqual(len(exps), doc.get("n_exp", 9), f"{name}: клеток")
            counts: dict = {}
            for s in exps:
                self.assertIn(s.get("hypothesis"), shelf,
                              f"{name} P{s['n']:02d}: H-XX вне полки")
                counts[s["hypothesis"]] = counts.get(s["hypothesis"], 0) + 1
                self.assertFalse(s.get("oc_hook"),
                                 f"{name} P{s['n']:02d}: oc_hook в EXP")
            for h, c in counts.items():
                self.assertLessEqual(c, tf.EXP_MAX_PER_HYP,
                                     f"{name}: {h} на {c} клетках")

    def test_predict_is_composition_v43(self):
        for name in GOLD:
            doc = load_tb(name)
            for s in doc["slots"]:
                implied = self.forge.rating_implied(
                    " ".join(s["pos"]), self.forge.rating_cfg)
                self.assertEqual(
                    implied, s["predicted"]["tier"],
                    f"{name} P{s['n']:02d}: предикт {s['predicted']['tier']} "
                    f"≠ состав {implied} — болванка обязана предсказывать "
                    f"то, что проверяет печь")

    def test_neg_hard_floors(self):
        for name in GOLD:
            doc = load_tb(name)
            for s in doc["slots"]:
                neg = " ".join(s["neg"])
                self.assertIn("candle", neg, f"{name} P{s['n']:02d}: света-флор")
                self.assertNotIn("nude", neg, f"{name} P{s['n']:02d}: вне реестра")

    def test_no_window_hits_no_dupes(self):
        for name in GOLD:
            doc = load_tb(name)
            cards = [s["y_card"] for s in doc["slots"]]
            self.assertEqual(len(cards), len(set(cards)), f"{name}: дубли карт")
            if self.forge.window_cards:
                hit = set(cards) & self.forge.window_cards
                self.assertFalse(hit, f"{name}: окно пробито {sorted(hit)}")


class TestTamperFires(unittest.TestCase):
    """Тамперы: законы PROTO-2 стреляют, а не декорированы."""

    @classmethod
    def setUpClass(cls):
        cls.forge = tf.Forge()
        cls.doc = load_tb("TB-20261122-777")

    def _errs(self, mutate):
        doc = copy.deepcopy(self.doc)
        mutate(doc)
        return tf.check_batch(doc, self.forge)

    def test_genre_removed(self):
        def m(doc):
            doc["slots"][0]["genre"] = None
        errs = self._errs(m)
        self.assertTrue(any("жанров" in e for e in errs), errs[:3])

    def test_kin_over_cap(self):
        def m(doc):
            # 11 кинов: перекрашиваем 5 human-мейнов в один кин
            kined = 0
            for s in doc["slots"]:
                if s["genre"] != "EXP" and s["race"] == "R01" and kined < 5:
                    s["race"] = "R02"
                    kined += 1
        errs = self._errs(m)
        self.assertTrue(any("кины опция" in e for e in errs), errs[:3])

    def test_exp_without_hypothesis(self):
        def m(doc):
            for s in doc["slots"]:
                if s["genre"] == "EXP":
                    s["hypothesis"] = None
                    break
        errs = self._errs(m)
        self.assertTrue(any("H-XX" in e for e in errs), errs[:3])

    def test_duplicate_card(self):
        def m(doc):
            doc["slots"][1]["y_card"] = doc["slots"][0]["y_card"]
        errs = self._errs(m)
        self.assertTrue(any("дубль" in e for e in errs), errs[:3])

    def test_canon_race_assigned(self):
        def m(doc):
            doc["slots"][2]["race"] = "R50"  # Nier (Nine-tails)
        errs = self._errs(m)
        self.assertTrue(any("канон-лок" in e for e in errs), errs[:3])

    def test_neg_without_candle(self):
        def m(doc):
            s = doc["slots"][3]
            s["neg"] = [n.replace(", candle, lamp", "") for n in s["neg"]]
        errs = self._errs(m)
        self.assertTrue(any("candle" in e for e in errs), errs[:3])

    def test_predict_drift(self):
        def m(doc):
            doc["slots"][4]["predicted"]["tier"] = "PG-13"
        errs = self._errs(m)
        self.assertTrue(any("состав" in e for e in errs), errs[:3])

    def test_genre_run_block(self):
        def m(doc):
            # паттерн T5-29: вольт-блок, потом ниша-блок (бег 14 подряд)
            mains = [s for s in doc["slots"] if s["genre"] != "EXP"]
            for i, s in enumerate(mains):
                s["genre"] = "VOLT" if i < 14 else "NICHE"
        errs = self._errs(m)
        self.assertTrue(any("жанровый бег" in e for e in errs), errs[:3])


class TestEraSkip(unittest.TestCase):
    """Проба PROTO-1 — эра-скип: история не переписывается."""

    def test_trial_probe_skipped(self):
        forge = tf.Forge()
        doc = load_tb(TRIAL_PROBE)
        self.assertEqual(doc.get("proto"), 1)
        self.assertIn("trial_probe", doc, "проба обязана нести пометку эвиденса")
        self.assertEqual(tf.check_batch(doc, forge), [],
                         "proto 1 — SKIP, законы В39–В43 назад не бьют")


class TestGenrePlan(unittest.TestCase):
    """genre_plan держит законы на 40 сидах (мультивселенная роллов)."""

    def test_forty_seeds_law24(self):
        for seed in range(40):
            rng = random.Random(seed)
            plan = tf.Forge().genre_plan(rng, 21)
            volt = sum(1 for g in plan if g in ("VOLT", "EXQUISITE"))
            niche = sum(1 for g in plan if g == "NICHE")
            exq = sum(1 for g in plan if g == "EXQUISITE")
            run, cur, prev = 0, 0, None
            for g in plan:
                cur = cur + 1 if g == prev else 1
                run = max(run, cur)
                prev = g
            self.assertGreaterEqual(volt, tf.VOLT_MIN, f"seed {seed}")
            self.assertTrue(tf.NICHE_MIN <= niche <= tf.NICHE_MAX, f"seed {seed}")
            self.assertTrue(tf.EXQ_MIN <= exq <= tf.EXQ_MAX, f"seed {seed}")
            self.assertLessEqual(run, tf.GENRE_MAX_RUN, f"seed {seed}: бег {run}")

    def test_small_roll_mono_not_choked(self):
        """Малый ролл без ниши не душится бегом (смешивать нечем)."""
        plan = tf.Forge().genre_plan(random.Random(1), 8)
        self.assertEqual(len(plan), 8)
        self.assertTrue(all(g in ("VOLT", "EXQUISITE", "NICHE") for g in plan))


class TestRollReproducibility(unittest.TestCase):
    """Воспроизводимость: один сид — один батч (цель В)."""

    def test_same_seed_same_batch(self):
        with tempfile.TemporaryDirectory(prefix="tb-repro-") as d:
            doc1 = tf.roll(12, 555, Path(d) / "A.json", n_exp=0)
            doc2 = tf.roll(12, 555, Path(d) / "B.json", n_exp=0)
            self.assertEqual(
                [s["y_card"] for s in doc1["slots"]],
                [s["y_card"] for s in doc2["slots"]],
                "один сид обязан давать один батч")


if __name__ == "__main__":
    unittest.main()
