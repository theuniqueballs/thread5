#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Тесты negCanonGuard (gates.json 1.23.0, ПЛАН 5.5 T6.2, В55).

Основание: вердикт T5-34, finding named_feature_in_neg — розовые очки
SO-20 (инвариант заказа SO-09) посажены в NEG гард-формой («glasses
covering eyes, glasses removed») и потеряны на рендере; тем же классом
потеряны канон-локи SO-19 катка-2. Закон В55 (ОС-протокол): именные
фишки заказа и канон-локи НИКОГДА не в NEG — держать фишку позитивной
строкой POS; гейт = FAIL с T5-35 (класс оплачен), special/SO-файлы —
живые заказы, проверяются всегда, --retro — WARN.

Проверяется:
1. Спеки: gates.json 1.23.0 (negCanonGuard: applyFrom/failFrom 35,
   genericStop/colorStop); special-roster.json 1.5.0 (order_invariants
   Эрешкигаль: SO-09 «pink glasses» — структурированная декларация из
   SO-20); gate-registry 1.3.0 — 35 секций, impl и тест на месте.
2. Мейн-слоты (мини-канон, эра 40): канон-лок именного OC в NEG →
   FAIL; чистый OC-слот → тихо; не-OC слот → не проверяется; до эры
   (34) — молчит; ретро — WARN.
3. Special-файлы (мини-ростер): инвариант заказа в NEG → FAIL; чистый
   заказ → тихо; ретро → WARN; не-special путь → special: False.
4. Живой тампер: special/SO-20.md — очки («glasse») + гард-локи
   («ribbon», «twintail») ловятся (история не переписывается — файл
   не трогаем, проверяем чтением).
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


class TestNegCanonSpec(unittest.TestCase):
    """Спеки: конфиг гейта, инварианты ростера, реестр."""

    @classmethod
    def setUpClass(cls):
        cls.gt = load("gates.json")
        cls.roster = load("special-roster.json")
        cls.reg = load("gate-registry.json")

    def test_gate_config(self):
        self.assertEqual(self.gt["version"], "1.26.0")  # 1.26.0 — k1Sense (тикет #2)
        g = self.gt["negCanonGuard"]
        self.assertEqual(g["applyFrom"], 35)
        self.assertEqual(g["failFrom"], 35)
        self.assertTrue(g["genericStop"])
        self.assertTrue(g["colorStop"])
        self.assertIn("В55", g["law"])
        self.assertIn("v1.23.0", (REPO / "tools/gates.py").read_text(encoding="utf-8"))

    def test_roster_invariants(self):
        self.assertEqual(self.roster["version"], "1.5.0")
        er = next(g for g in self.roster["guests"] if g["name"] == "Ereshkigal")
        self.assertEqual(er["order_invariants"], {"SO-09": ["pink glasses"]})

    def test_registry_chain(self):
        self.assertEqual(self.reg["version"], "1.6.0")
        self.assertEqual(len(self.reg["gates"]), 38)
        row = next(g for g in self.reg["gates"]
                   if g["section"] == "negCanonGuard")
        self.assertEqual(row["impl"],
                         ["check_neg_canon_guard", "check_special_neg_canon"])
        self.assertEqual(row["receiptField"], "neg_canon_guard")
        self.assertTrue((REPO / row["test"]).exists())

    def test_validator_knows_section(self):
        v = (REPO / "tools/validate.py").read_text(encoding="utf-8")
        self.assertIn('"negCanonGuard"', v)


class NegCanonMainSlots(unittest.TestCase):
    """Мейн-слоты: канон-локи именного OC против NEG (мини-канон)."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        tmp = Path(self._tmp.name)
        (tmp / "specs").mkdir()
        (tmp / "batches").mkdir()
        self._old_root = gates.ROOT
        gates.ROOT = tmp
        (tmp / "specs" / "oc-canon.json").write_text(json.dumps({
            "ocs": {"Sue": {
                "hair": "platinum twin ponytails",
                "eyes": "soft purple right eye",
                "skin": "pale ivory",
                "signature_marks": ["square white medical eyepatch",
                                    "neck tattoo"],
            }}}), encoding="utf-8")
        self.batch = tmp / "batches" / "T5-40.md"

    def tearDown(self):
        gates.ROOT = self._old_root
        self._tmp.cleanup()

    @staticmethod
    def make_slot(n, paren, neg):
        s = gates.Slot(n, f"synth-{n}", paren,
                       f"P{n:02d} — synth-{n} ({paren})")
        s.neg = neg
        s.pos = "positive prose with her identity locks"
        return s

    def run_guard(self, slots, batch_no, retro=False):
        warns, fails = [], []
        st = gates.check_neg_canon_guard(slots, warns, fails, batch_no,
                                         oc_names=["Sue"], retro=retro)
        return st, warns, fails

    def test_canon_lock_in_neg_fails(self):
        s = self.make_slot(1, "EXQUISITE · Sue · R+ · PL1",
                           "signature, watermark, eyepatch, bad hands")
        st, warns, fails = self.run_guard([s], batch_no=40)
        self.assertTrue(any("eyepatch" in f[2] for f in fails))
        self.assertEqual(st["canon_hits"], 1)
        self.assertEqual(st["oc_slots"], 1)

    def test_clean_oc_slot_is_silent(self):
        s = self.make_slot(1, "EXQUISITE · Sue · R+ · PL1",
                           "signature, watermark, bad hands, extra fingers")
        st, warns, fails = self.run_guard([s], batch_no=40)
        self.assertFalse(fails)
        self.assertEqual(st["canon_hits"], 0)

    def test_non_oc_slot_ignored(self):
        s = self.make_slot(1, "VOLT · human · R+ · PL1",
                           "signature, eyepatch, watermark")
        st, warns, fails = self.run_guard([s], batch_no=40)
        self.assertFalse(fails)
        self.assertEqual(st["oc_slots"], 0)

    def test_pre_era_silent(self):
        s = self.make_slot(1, "EXQUISITE · Sue · R+ · PL1",
                           "signature, eyepatch, watermark")
        st, warns, fails = self.run_guard([s], batch_no=34)
        self.assertFalse(fails)
        self.assertEqual(st["mode"], "silent")

    def test_retro_warns_not_fails(self):
        s = self.make_slot(1, "EXQUISITE · Sue · R+ · PL1",
                           "signature, eyepatch, watermark")
        st, warns, fails = self.run_guard([s], batch_no=34, retro=True)
        self.assertFalse(fails)
        self.assertTrue(any("eyepatch" in w[2] for w in warns))
        self.assertEqual(st["mode"], "RETRO-WARN")


class NegCanonSpecial(unittest.TestCase):
    """Special/SO-файлы: живые заказы, эры нет (мини-ростер)."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        tmp = Path(self._tmp.name)
        (tmp / "specs").mkdir()
        (tmp / "special").mkdir()
        self._old_root = gates.ROOT
        gates.ROOT = tmp
        (tmp / "specs" / "special-roster.json").write_text(json.dumps({
            "guests": [{
                "name": "Ereshkigal",
                "orders": ["SO-09"],
                "canon_run": "blonde twintails tied with black ribbons, "
                             "gold hair ornament",
                "order_invariants": {"SO-09": ["pink glasses"]},
            }]}), encoding="utf-8")

    def tearDown(self):
        gates.ROOT = self._old_root
        self._tmp.cleanup()

    def write_so(self, neg_line):
        p = Path(self._tmp.name) / "special" / "SO-99.md"
        p.write_text(
            "# SO-99 «synthetic»\n\nCanon: Ereshkigal — тест.\n\n"
            "POS:\n\nanime style, pink glasses on her nose, twintails\n\n"
            f"NEG:\n\n{neg_line}\n\n════════════\nПЕЧЬ\n",
            encoding="utf-8")
        return p

    def run_guard(self, path, retro=False):
        warns, fails = [], []
        st = gates.check_special_neg_canon(str(path), warns, fails,
                                           retro=retro)
        return st, warns, fails

    def test_invariant_in_neg_fails(self):
        """Оплаченный кейс SO-20: «glasses removed» в NEG = FAIL."""
        p = self.write_so("signature, glasses covering eyes, glasses removed")
        st, warns, fails = self.run_guard(p)
        self.assertTrue(any("glasse" in f[2] for f in fails))
        self.assertEqual(st["invariant_hits"], 1)
        self.assertEqual(st["guest"], "Ereshkigal")
        self.assertTrue(st["special"])

    def test_canon_gards_in_neg_fail_too(self):
        """Гард-формы канон-локов («twintails down») — тот же класс."""
        p = self.write_so("signature, twintails down, ribbons missing")
        st, warns, fails = self.run_guard(p)
        self.assertTrue(any("twintail" in f[2] for f in fails))
        self.assertEqual(st["canon_hits"], 2)  # ribbon + twintail

    def test_clean_special_is_silent(self):
        p = self.write_so("signature, watermark, bad hands, black background")
        st, warns, fails = self.run_guard(p)
        self.assertFalse(fails)
        self.assertEqual(st["invariant_hits"], 0)
        self.assertEqual(st["canon_hits"], 0)

    def test_retro_warns(self):
        p = self.write_so("signature, glasses removed")
        st, warns, fails = self.run_guard(p, retro=True)
        self.assertFalse(fails)
        self.assertTrue(any("glasse" in w[2] for w in warns))

    def test_non_special_path_ignored(self):
        p = Path(self._tmp.name) / "batches" / "T5-40.md"
        p.parent.mkdir(exist_ok=True)
        p.write_text("# T5-40\n", encoding="utf-8")
        st, warns, fails = self.run_guard(p)
        self.assertFalse(st["special"])


class TestLiveSO20Tamper(unittest.TestCase):
    """Живой SO-20 (чтение, не правка): оплаченный кейс виден гейтом."""

    def test_so20_glasses_caught(self):
        warns, fails = [], []
        st = gates.check_special_neg_canon(
            str(REPO / "special" / "SO-20.md"), warns, fails, retro=True)
        self.assertEqual(st["guest"], "Ereshkigal")
        self.assertEqual(st["invariant_hits"], 1)   # glasse — розовые очки
        self.assertGreaterEqual(st["canon_hits"], 2)  # ribbon, twintail
        self.assertTrue(any("glasse" in w[2] for w in warns))


if __name__ == "__main__":
    unittest.main()
