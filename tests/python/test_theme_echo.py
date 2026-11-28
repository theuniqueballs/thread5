#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Тесты themeEcho (gates.json 1.25.0, ПЛАН 5.5 T4.1/T4.2, В54).

Основание: вердикт T5-34 «худший по раскрытию темы» — тема читалась в
1/31 рендера: лексемы темы запрещены в POS, волна-18 несла тему именами
палитр, а не содержимым. В54: тема = визуальная система — ≥3 рендеримых
акссиомы (поведение света · насыщение · мотив-предмет), осмеченные в
≥60% мейнов; THEME-ECHO машинострока в брифе, по ней гейт WARN «тема —
гарнир» при доле < 60%.

Проверяется:
1. Спеки: gates.json 1.25.0 (themeEcho: WARN, applyFrom 35, share 0.6);
   gate-registry 1.5.0 — 37 секций; шаблон брифа несёт THEME-SPEC +
   машиностроку; 01-SOL чек-лист требует THEME-SPEC.
2. Функционально: бриф без THEME-ECHO → WARN «тема не специфицирована»;
   словарь есть, эхо < 60% мейнов → WARN «тема — гарнир»; эхо ≥ 60% →
   чисто; до эры (34) — молчит; ретро — WARN-режим.
3. Живой T5-34 (retro): бриф есть, THEME-ECHO нет → WARN виден
   (тема партии не была специфицирована — факт вердикта).
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

SPEC = REPO / "specs"


def load(name):
    return json.loads((SPEC / name).read_text(encoding="utf-8"))


class TestThemeEchoSpec(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.gt = load("gates.json")
        cls.reg = load("gate-registry.json")

    def test_gate_config(self):
        self.assertEqual(self.gt["version"], "1.30.0")  # 1.30.0 — carrierTruth (тикет #7/В61); 1.29.0 — nudeTruth (вердикт T5-35)
        g = self.gt["themeEcho"]
        self.assertEqual(g["applyFrom"], 35)
        self.assertEqual(g["mode"], "WARN")
        self.assertEqual(g["mainsShareMin"], 0.6)
        self.assertIn("В54", g["born"])

    def test_registry(self):
        self.assertEqual(self.reg["version"], "1.9.0")  # 1.9.0 — секция carrierTruth (тикет #7/В61); 1.8.0 — nudeTruth
        self.assertEqual(len(self.reg["gates"]), 41)  # 41 — +carrierTruth (тикет #7/В61); 40 — +nudeTruth
        row = next(g for g in self.reg["gates"] if g["section"] == "themeEcho")
        self.assertEqual(row["impl"], ["check_theme_echo"])
        self.assertEqual(row["receiptField"], "theme_echo")
        self.assertIn('"themeEcho"',
                      (REPO / "tools/validate.py").read_text(encoding="utf-8"))

    def test_brief_template_carries_theme_spec(self):
        t = (REPO / "batches" / "_BRIEF-TEMPLATE.md").read_text(encoding="utf-8")
        self.assertIn("THEME-SPEC", t)
        self.assertIn("THEME-ECHO (словарь эха)", t)
        self.assertIn("РЕНДЕРИМЫХ аксиомы", t)
        sol = (REPO / "docs" / "ars" / "01-SOL.md").read_text(encoding="utf-8")
        self.assertIn("THEME-SPEC", sol)


class ThemeEchoFunctional(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        tmp = Path(self._tmp.name)
        (tmp / "batches" / "T5-40").mkdir(parents=True)
        self._old_root = gates.ROOT
        gates.ROOT = tmp
        self.batch = tmp / "batches" / "T5-40.md"

    def tearDown(self):
        gates.ROOT = self._old_root
        self._tmp.cleanup()

    @staticmethod
    def make_slot(n, pos):
        s = gates.Slot(n, f"synth-{n}", f"VOLT · human · R+ · PL1",
                       f"P{n:02d} — synth-{n} (VOLT · human · R+ · PL1)")
        s.pos = pos
        return s

    def write_brief(self, echo_line=None):
        d = self.batch.parent / "T5-40"
        (d / "00-brief.md").write_text(
            "# БРИФ\n\n## Исследование темы\n\n"
            + (echo_line or "- суть темы: …\n"),
            encoding="utf-8")

    def run_gate(self, slots, batch_no, retro=False):
        warns, fails = [], []
        st = gates.check_theme_echo(str(self.batch), slots, warns, fails,
                                    batch_no, oc_names=[], retro=retro)
        return st, warns, fails

    def test_no_theme_spec_warns(self):
        self.write_brief()  # без THEME-ECHO
        s = self.make_slot(1, "some prose")
        st, warns, fails = self.run_gate([s], batch_no=40)
        self.assertTrue(any("тема не специфицирована" in w[2] for w in warns))
        self.assertEqual(st["dict_size"], 0)

    def test_theme_garnish_warns(self):
        self.write_brief("- THEME-ECHO (словарь эха): candlelight, "
                         "amber glow, brass\n")
        # 1 из 2 мейнов несёт эхо = 50% < 60%
        s1 = self.make_slot(1, "warm candlelight on amber skin")
        s2 = self.make_slot(2, "cold office neon hum")
        st, warns, fails = self.run_gate([s1, s2], batch_no=40)
        self.assertTrue(any("тема — гарнир" in w[2] for w in warns))
        self.assertEqual(st["with_echo"], 1)
        self.assertEqual(st["mains"], 2)

    def test_theme_present_clean(self):
        self.write_brief("- THEME-ECHO (словарь эха): candlelight, "
                         "amber glow, brass\n")
        s1 = self.make_slot(1, "warm candlelight on amber skin")
        s2 = self.make_slot(2, "brass rail in candlelight")
        st, warns, fails = self.run_gate([s1, s2], batch_no=40)
        self.assertFalse([w for w in warns if w[1] == "theme-echo"])
        self.assertEqual(st["share"], 1.0)

    def test_pre_era_silent(self):
        self.write_brief()
        s = self.make_slot(1, "some prose")
        st, warns, fails = self.run_gate([s], batch_no=34)
        self.assertEqual(st["mode"], "silent")

    def test_retro_mode(self):
        self.write_brief()
        s = self.make_slot(1, "some prose")
        st, warns, fails = self.run_gate([s], batch_no=34, retro=True)
        self.assertEqual(st["mode"], "RETRO-WARN")
        self.assertTrue(any("тема не специфицирована" in w[2] for w in warns))

    def test_live_t534_no_theme_spec(self):
        """Живой факт: бриф T5-34 без THEME-ECHO — тема партии не была
        специфицирована (вердикт: 1/31 рендера)."""
        _, _, slots = gates.parse_batch(str(REPO / "batches" / "T5-34.md"))
        warns, fails = [], []
        st = gates.check_theme_echo(str(REPO / "batches" / "T5-34.md"),
                                    slots, warns, fails, 34, oc_names=[],
                                    retro=True)
        self.assertEqual(st["dict_size"], 0)
        self.assertTrue(any("тема не специфицирована" in w[2] for w in warns))


if __name__ == "__main__":
    unittest.main()
