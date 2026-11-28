#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Тесты voltRun (gates.json 1.24.0 / rating-techniques 1.7.0, ПЛАН 5.5 T1.2).

Основание: В45 «машина горячее глаза» (постмортем T5-34 §2.1/§2.3) — 15
ложных R+ из 17: R+-бейдж при плоском рендере. Второй тег-ран R+-слота:
грудь (форма+состояние) · руки (что ДЕЛАЮТ) · бёдра/попа/кожа — ≥2 стемов
одной группы и ≥3 суммарно, иначе WARN (закон 8.6: WARN-старт с T5-35).

Калибровка на живом T5-34 (retro): 11 R+-мейнов все с раном (тоталы 4–11,
P17 лучший 11) — лексика в T5-34 была, плоскими были носители (В52,
территория eraGuard); гейт бережёт будущее от сухих POS.

Проверяется:
1. Спеки: rating-techniques 1.7.0 (volt_run группы breast/hands/
   hips_ass_skin), gates.json 1.24.0 (voltRun: WARN, applyFrom 35,
   minStems 3, groupMin 2), gate-registry 1.4.0 — 36 секций.
2. Функционально: богатый второй ран → чисто; сухой POS (бойлерплейт
   «large breasts» + «pale skin») → WARN «машина горячее глаза»; R-слот
   не проверяется; до эры (34) молчит; ретро — WARN-режим.
"""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO / "tools"))

import gates  # noqa: E402

SPEC = REPO / "specs"


def load(name):
    return json.loads((SPEC / name).read_text(encoding="utf-8"))


RICH_POS = (
    "masterpiece, upper body, 1girl, solo, large soft natural-set build, "
    "pale skin, long hair, "
    "breast shape held honest by the wet silk's surface tension, both soft "
    "crests reading through, cleavage deepening as she leans, "
    "one palm pressing the wall, fingers tugging the towel's edge, "
    "the sarong's knot gone slack at the hip, thighs closing the frame"
)
THIN_POS = (
    "masterpiece, upper body, 1girl, solo, large breasts, pale skin, "
    "long black hair, standing in a garden, looking at viewer, "
    "a dress, some flowers, nice weather, beautiful scenery"
)


class TestVoltRunSpec(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rt = load("rating-techniques.json")
        cls.gt = load("gates.json")
        cls.reg = load("gate-registry.json")

    def test_dictionary(self):
        self.assertEqual(self.rt["version"], "1.9.0")  # 1.9.0 — volt_run.groups + carriers (тикет #7/В61); 1.8.0 — nude_truth
        vr = self.rt["volt_run"]
        self.assertEqual(set(vr["groups"]),
                         {"breast", "hands", "hips_ass_skin", "carriers"})
        for g, ws in vr["groups"].items():
            self.assertGreaterEqual(len(ws), 10, f"группа {g} тонка")
        self.assertIn("В45", vr["born"])

    def test_gate_config(self):
        self.assertEqual(self.gt["version"], "1.30.0")  # 1.30.0 — carrierTruth (тикет #7/В61); 1.29.0 — nudeTruth (вердикт T5-35)
        g = self.gt["voltRun"]
        self.assertEqual(g["applyFrom"], 35)
        self.assertEqual(g["mode"], "WARN")
        self.assertEqual(g["minStems"], 3)
        self.assertEqual(g["groupMin"], 2)

    def test_registry(self):
        self.assertEqual(self.reg["version"], "1.9.0")  # 1.9.0 — секция carrierTruth (тикет #7/В61); 1.8.0 — nudeTruth
        self.assertEqual(len(self.reg["gates"]), 41)  # 41 — +carrierTruth (тикет #7/В61); 40 — +nudeTruth
        row = next(g for g in self.reg["gates"] if g["section"] == "voltRun")
        self.assertEqual(row["impl"], ["check_volt_run"])
        self.assertEqual(row["receiptField"], "volt_run")
        self.assertTrue((REPO / row["test"]).exists())
        self.assertIn('"voltRun"',
                      (REPO / "tools/validate.py").read_text(encoding="utf-8"))


class TestVoltRunFunctional(unittest.TestCase):
    def make_slot(self, n, rating, pos):
        s = gates.Slot(n, f"synth-{n}",
                       f"VOLT · human · {rating} · PL1",
                       f"P{n:02d} — synth-{n} (VOLT · human · {rating} · PL1)")
        s.pos = pos
        s.pos_lines = [l.strip() for l in pos.split(",") if l.strip()]
        return s

    def run_gate(self, slots, batch_no, retro=False):
        warns, fails = [], []
        st = gates.check_volt_run(slots, warns, fails, batch_no,
                                  oc_names=[], retro=retro)
        return st, warns, fails

    def test_rich_second_run_clean(self):
        s = self.make_slot(1, "R+", RICH_POS)
        st, warns, fails = self.run_gate([s], batch_no=40)
        self.assertEqual(st["with_run"], 1)
        self.assertEqual(st["thin"], 0)
        self.assertFalse([w for w in warns if w[1] == "volt-run"])

    def test_thin_pos_warns(self):
        """Сухой POS: бойлерплейт «large breasts» + «pale skin» — ран
        одиночный, WARN «машина горячее глаза» (В45)."""
        s = self.make_slot(1, "R+", THIN_POS)
        st, warns, fails = self.run_gate([s], batch_no=40)
        self.assertEqual(st["thin"], 1)
        self.assertTrue(any("машина горячее глаза" in w[2] for w in warns))
        self.assertFalse(fails)  # WARN-эра, не FAIL

    def test_r_slot_not_checked(self):
        s = self.make_slot(1, "R", THIN_POS)
        st, warns, fails = self.run_gate([s], batch_no=40)
        self.assertEqual(st["rplus_mains"], 0)
        self.assertFalse([w for w in warns if w[1] == "volt-run"])

    def test_pre_era_silent(self):
        s = self.make_slot(1, "R+", THIN_POS)
        st, warns, fails = self.run_guard = self.run_gate([s], batch_no=34)
        self.assertEqual(st["mode"], "silent")
        self.assertFalse([w for w in warns if w[1] == "volt-run"])

    def test_retro_mode(self):
        s = self.make_slot(1, "R+", THIN_POS)
        st, warns, fails = self.run_gate([s], batch_no=34, retro=True)
        self.assertEqual(st["mode"], "RETRO-WARN")
        self.assertTrue(any("машина горячее глаза" in w[2] for w in warns))

    def test_live_t534_all_rich(self):
        """Калибровка: живой T5-34 (retro) — 11 R+-мейнов, сухих 0
        (лексика была; плоскость — носители В52, не слова)."""
        _, _, slots = gates.parse_batch(str(REPO / "batches" / "T5-34.md"))
        warns, fails = [], []
        st = gates.check_volt_run(slots, warns, fails, 34,
                                  oc_names=gates.load_oc_names(), retro=True)
        self.assertEqual(st["rplus_mains"], 11)
        self.assertEqual(st["thin"], 0)
        self.assertGreaterEqual(st["with_run"], 11)


if __name__ == "__main__":
    unittest.main()
