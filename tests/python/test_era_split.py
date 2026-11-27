#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Тесты ERA-СПЛИТА Y-карт + yStamp eraGuard (camera.json 1.23.0 /
gates.json 1.22.0, ПЛАН 5.5 «ПРАВДА В КАДРЕ» T3.1/T3.2).

Основание: вердикт T5-34 (В52 «старые Y = материал не слот») — 24 слота
партии собрались на старых 512 Y вербатимом («клеймо 1:1»), процесс-
носители старой концепции рендером как эротика не читаются: 15 ложных
R+ из 17. Era-сплит разводит концепции: legacy (Y1–Y512) = материал
(скелет: поза/мех-группы/камера, джус пишется заново), modern (Y513+) =
вплетение 1:1 обязательно, как было (В34/В35).

Проверяется:
1. Спека: все 559 карт несут era; legacy ⇔ Y1–Y512 ⇔ combo-блок;
   modern ⇔ Y513–Y559; версия camera 1.23.0, закон и changelog вшили
   era-сплит.
2. Конфиг: gates.json 1.22.0, yStamp.eraGuard (applyFrom/failFrom 35,
   skeletonFloor 2, legacyVerbatim fail_rplus).
3. Штамп: tools/stamp_era.py --check проходит на живом реестре.
4. Функционально (мини-реестр, живая эра T5-40):
   - вербатим legacy под R+ → FAIL (класс оплачен T5-34);
   - вербатим legacy под R → WARN, не FAIL;
   - legacy без вербатима, скелет читается (≥2 стемов) → чисто,
     квитанция считает legacy_material;
   - legacy без вербатима, скелет не читается → WARN «скелет не читается»;
   - modern без вплетения → FAIL «не вплетён» (прежний режим В34/В35
     не тронут);
   - до эры (T5-34, без --retro) поведение прежнее: вербатим legacy
     легален, счётчики era молчат;
   - ретро (T5-34, --retro) → вербатим legacy виден WARN-ом, не FAIL.
"""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO / "tools"))

import gates  # noqa: E402
import stamp_era  # noqa: E402

SPEC = REPO / "specs"

LEGACY_POSE = ("arched over the sill with the weight on the wrists and "
               "the knees drawn together")
MODERN_POSE = ("leaning into the doorframe with the towel barely holding "
               "and one heel against the sill")


def load(name):
    return json.loads((SPEC / name).read_text(encoding="utf-8"))


class TestEraSplitSpec(unittest.TestCase):
    """Спека camera.json 1.23.0: поле era на всех картах, сплит согласован."""

    @classmethod
    def setUpClass(cls):
        cls.cam = load("camera.json")
        cls.cards = {c["id"]: c for c in cls.cam["y_cards"]["cards"]}

    def test_versions_and_law(self):
        self.assertEqual(self.cam["version"], "1.23.0")
        self.assertIn("1.23.0", self.cam["y_cards"]["law"])
        self.assertIn("ERA-СПЛИТ", self.cam["y_cards"]["law"])
        self.assertIn("В52", self.cam["y_cards"]["law"])
        self.assertIn("1.23.0", json.dumps(self.cam["changelog"][0]))

    def test_every_card_has_era(self):
        for c in self.cam["y_cards"]["cards"]:
            self.assertIn(c.get("era"), ("legacy", "modern"),
                          f"{c['id']}: era={c.get('era')!r}")

    def test_legacy_is_exactly_old_512(self):
        """legacy ⇔ Y1–Y512 ⇔ combo-блок: сплит по диапазону и по разбору
        1.22.0 сходятся, без пропусков и лишних."""
        legacy = {c["id"] for c in self.cam["y_cards"]["cards"]
                  if c.get("era") == "legacy"}
        expected = {f"Y{i}" for i in range(1, 513)}
        self.assertEqual(legacy, expected)
        self.assertEqual(len(legacy), 512)
        for yid in legacy:
            self.assertIsNotNone(self.cards[yid].get("combo"),
                                 f"{yid}: legacy без combo-блока 1.22.0")

    def test_modern_is_y513_plus(self):
        modern = {c["id"] for c in self.cam["y_cards"]["cards"]
                  if c.get("era") == "modern"}
        self.assertEqual(len(modern), 47)  # 559 − 512
        for yid in modern:
            self.assertGreater(int(yid[1:]), 512, f"{yid}: modern вне диапазона")

    def test_era_field_position(self):
        """era — паспорт концепции, читается сразу после id."""
        for c in self.cam["y_cards"]["cards"][:20]:
            self.assertEqual(list(c.keys())[:2], ["id", "era"],
                             f"{c['id']}: era не на втором месте")

    def test_stamp_era_check_passes(self):
        """tools/stamp_era.py --check: согласованность живого реестра."""
        self.assertEqual(stamp_era.check(self.cam), 0)


class TestEraGuardConfig(unittest.TestCase):
    """gates.json 1.22.0: yStamp.eraGuard с эрой и порогами."""

    @classmethod
    def setUpClass(cls):
        cls.gt = load("gates.json")

    def test_version(self):
        self.assertEqual(self.gt["version"], "1.22.0")
        self.assertIn("v1.22.0", (REPO / "tools/gates.py").read_text(encoding="utf-8"))

    def test_era_guard_config(self):
        g = self.gt["yStamp"]["eraGuard"]
        self.assertEqual(g["applyFrom"], 35)
        self.assertEqual(g["failFrom"], 35)
        self.assertEqual(g["legacyVerbatim"], "fail_rplus")
        self.assertEqual(g["skeletonFloor"], 2)
        self.assertIn("В52", g["born"])


class EraGuardFunctional(unittest.TestCase):
    """Функциональные кейсы check_ystamp на мини-реестре (живая эра T5-40)."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        tmp = Path(self._tmp.name)
        (tmp / "specs").mkdir()
        (tmp / "batches").mkdir()
        self._old_root = gates.ROOT
        gates.ROOT = tmp
        cards = {
            "y_cards": {"cards": [
                {"id": "Y100", "era": "legacy", "pattern": "old process",
                 "corridor": "A", "trust": "t", "verdict": "v",
                 "components": {"pose": LEGACY_POSE,
                                "exposure": {"class": "PROCESS"}},
                 "combo": {"carriers": [], "mech_groups": [],
                           "camera": "CAM05_close", "juice": ""}},
                {"id": "Y600", "era": "modern", "pattern": "new wave",
                 "corridor": "A", "trust": "t", "verdict": "v",
                 "components": {"pose": MODERN_POSE,
                                "exposure": {"class": "LINGERIE"}}},
            ]}
        }
        (tmp / "specs" / "camera.json").write_text(
            json.dumps(cards), encoding="utf-8")
        self.batch = tmp / "batches" / "T5-40.md"
        self.batch.write_text("# T5-40 synth\n", encoding="utf-8")

    def tearDown(self):
        gates.ROOT = self._old_root
        self._tmp.cleanup()

    @staticmethod
    def make_slot(n, rating, y_card, pos_lines):
        s = gates.Slot(n, f"synth-{n}",
                       f"VOLT · human · {rating} · PL1",
                       f"P{n:02d} — synth-{n} (VOLT · human · {rating} · PL1)")
        s.y_card = y_card
        s.pos_lines = list(pos_lines)
        return s

    def run_ystamp(self, slots, batch_no, retro=False):
        warns, fails = [], []
        st = gates.check_ystamp(str(self.batch), slots, warns, fails,
                                batch_no=batch_no, retro=retro)
        return st, warns, fails

    def test_legacy_verbatim_under_rplus_fails(self):
        """24 слота T5-34, повторение запрещено: вербатим legacy под R+ — FAIL."""
        s = self.make_slot(1, "R+", "Y100", [
            "claim line with corridor physics",
            LEGACY_POSE,  # клеймо 1:1 на legacy — отменено (В52)
            "detail lines of the fresh juice",
        ])
        st, warns, fails = self.run_ystamp([s], batch_no=40)
        self.assertTrue(any("В52" in f[2] for f in fails),
                        f"FAIL не пойман: fails={fails}")
        self.assertEqual(st["legacy_verbatim"], 1)
        self.assertEqual(st["legacy_used"], 1)

    def test_legacy_verbatim_under_r_is_warn(self):
        s = self.make_slot(1, "R", "Y100", [
            "claim line", LEGACY_POSE, "fresh juice line",
        ])
        st, warns, fails = self.run_ystamp([s], batch_no=40)
        self.assertFalse(fails)
        self.assertTrue(any("В52" in w[2] for w in warns))
        self.assertEqual(st["legacy_verbatim"], 1)

    def test_legacy_skeleton_present_is_clean_material(self):
        """legacy = материал: скелет читается (≥2 стемов), вербатима нет —
        чисто, квитанция считает legacy_material (джус написан заново)."""
        s = self.make_slot(1, "R+", "Y100", [
            "claim line with corridor physics and object",
            "she arches back, the weight shifting onto the sill edge, "
            "fabric state telegraphed by the strain lines",
        ])
        st, warns, fails = self.run_ystamp([s], batch_no=40)
        self.assertFalse(fails)
        self.assertFalse([w for w in warns if "скелет" in w[2]])
        self.assertEqual(st["legacy_material"], 1)
        self.assertEqual(st["legacy_verbatim"], 0)

    def test_legacy_skeleton_missing_warns(self):
        s = self.make_slot(1, "R+", "Y100", [
            "claim line with corridor physics and object",
            "she stands tall in the garden among the roses",
        ])
        st, warns, fails = self.run_ystamp([s], batch_no=40)
        self.assertFalse(fails)
        self.assertTrue(any("скелет не читается" in w[2] for w in warns))
        self.assertEqual(st["legacy_skeleton_miss"], 1)

    def test_modern_unwoven_still_fails(self):
        """Modern-режим В34/В35 не тронут: без вплетения — FAIL."""
        s = self.make_slot(1, "R+", "Y600", [
            "claim line", "completely different prose about the scene",
            "more fresh prose lines here",
        ])
        st, warns, fails = self.run_ystamp([s], batch_no=40)
        self.assertTrue(any("не вплетён" in f[2] for f in fails))
        self.assertEqual(st["no_weave"], 1)

    def test_modern_woven_executed_is_clean(self):
        s = self.make_slot(1, "R+", "Y600", [
            "claim line", MODERN_POSE,
            "the doorframe leans with her, the towel barely holding",
        ])
        st, warns, fails = self.run_ystamp([s], batch_no=40)
        self.assertFalse(fails)
        self.assertEqual(st["weaved"], 1)

    def test_pre_era_behavior_unchanged(self):
        """До эры eraGuard (T5-34, без --retro) — прежний режим: вербатим
        legacy легален (клеймо 1:1 было законом), счётчики era молчат."""
        s = self.make_slot(1, "R+", "Y100", [
            "claim line", LEGACY_POSE,
            # тело несёт стемы паттерна вне вплетения (закон §17.3 прежнего
            # режима: исполнение ≥ minExecStems)
            "the weight on her wrists tells the doorframe everything",
        ])
        st, warns, fails = self.run_ystamp([s], batch_no=34)
        self.assertFalse(fails)
        self.assertEqual(st["legacy_verbatim"], 0)
        self.assertEqual(st["weaved"], 1)  # засчитан прежним режимом

    def test_retro_shows_legacy_verbatim_as_warn(self):
        """Ретро: находки WARN-ами, история не переписывается."""
        s = self.make_slot(1, "R+", "Y100", [
            "claim line", LEGACY_POSE, "fresh juice line",
        ])
        st, warns, fails = self.run_ystamp([s], batch_no=34, retro=True)
        self.assertFalse(fails)
        self.assertTrue(any("В52" in w[2] for w in warns))
        self.assertEqual(st["legacy_verbatim"], 1)


if __name__ == "__main__":
    unittest.main()
