#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Юнит-тесты ORACLE-2 CLI печи (unittest, stdlib-only).

Лочат паритет python-зеркала (tools/oracle.py) с каноническим движком
(src/lib/t5/oracle-engine.ts) через ЗОЛОТЫЕ ВЕКТОРЫ tests/fixtures/
oracle_vectors.json — тот же файл читает bun-тест tests/unit/oracle.test.ts:
паритет прилавок ↔ печь ↔ сервис держится с обоих берегов.

Регрессы этого файла:
  - parse_for: «T5-27» → 27 (не 527! — жребий сеялся не тем номером и
    расходился с сервисом; поймано живой сверкой органов 2026-11-20);
  - окно ротации: только прошлое, depth=0 = выключено;
  - mulberry32: беззнаковая 32-бит арифметика побитово;
  - жребий: расклады/seed/окно/shortfall по векторам;
  - selftest CLI: тот же прогон, что в CI печи.

Прогон: python3 -m unittest discover -s tests/python -v
"""

import json
import tempfile
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO / "tools"))

import oracle  # noqa: E402

VECTORS_PATH = REPO / "tests" / "fixtures" / "oracle_vectors.json"


def vectors():
    return json.loads(VECTORS_PATH.read_text(encoding="utf-8"))


class Mulberry32GoldenTest(unittest.TestCase):
    """mulberry32 против золотой последовательности (побитово)."""

    def test_golden_sequences(self):
        for seed_str, expected in vectors()["mulberry32"].items():
            rng = oracle.mulberry32(int(seed_str))
            got = [next(rng) for _ in range(len(expected))]
            self.assertEqual(
                [round(x, 15) for x in got],
                [round(x, 15) for x in expected],
                f"mulberry32(seed={seed_str}) разошёлся с каноном",
            )

    def test_same_seed_same_stream(self):
        a = oracle.mulberry32(31337)
        b = oracle.mulberry32(31337)
        self.assertEqual([next(a) for _ in range(16)], [next(b) for _ in range(16)])

    def test_range_unit(self):
        rng = oracle.mulberry32(7)
        for _ in range(2000):
            v = next(rng)
            self.assertGreaterEqual(v, 0.0)
            self.assertLess(v, 1.0)


class ParseForRegressionTest(unittest.TestCase):
    """Регресс parse_for: «T5-27» когда-то парсился в 527."""

    def test_t5_prefix(self):
        self.assertEqual(oracle.parse_for("T5-27"), 27)

    def test_lowercase_and_bare(self):
        self.assertEqual(oracle.parse_for("t5-27"), 27)
        self.assertEqual(oracle.parse_for("27"), 27)
        self.assertEqual(oracle.parse_for("T5-100"), 100)

    def test_garbage(self):
        self.assertEqual(oracle.parse_for("жребий"), 0)
        self.assertEqual(oracle.parse_for(""), 0)


class DrawParityTest(unittest.TestCase):
    """Жребий-зеркало против золотых раскладов."""

    @classmethod
    def setUpClass(cls):
        v = vectors()
        cls.cards = v["fixture"]["cards"]
        cls.usage = v["fixture"]["usage"]

    def _draw(self, batch_no):
        return oracle.draw_constellation(
            batch_no, self.cards, self.usage,
            oc_target=3, main_target=9, exp_target=4, window_depth=3,
        )

    def test_golden_draws(self):
        for batch_str, expected in vectors()["draws"].items():
            draw = self._draw(int(batch_str))
            self.assertEqual(draw["seed"], expected["seed"], "seed разошёлся")
            self.assertEqual([c["id"] for c in draw["oc"]], expected["oc"], f"draw({batch_str}).oc")
            self.assertEqual([c["id"] for c in draw["main"]], expected["main"], f"draw({batch_str}).main")
            self.assertEqual([c["id"] for c in draw["exp"]], expected["exp"], f"draw({batch_str}).exp")
            self.assertEqual(draw["windowExcluded"], expected["windowExcluded"])
            self.assertEqual(draw["shortfall"], expected["shortfall"])

    def test_determinism(self):
        a = self._draw(27)
        b = self._draw(27)
        self.assertEqual(json.dumps(a, sort_keys=True), json.dumps(b, sort_keys=True))

    def test_window_cards_never_drawn(self):
        draw = self._draw(27)
        hot_tail = {"Y3", "Y7", "Y11", "Y19"}  # партии 24–26 фикстуры
        drawn = {c["id"] for c in draw["oc"] + draw["main"] + draw["exp"]}
        self.assertEqual(drawn & hot_tail, set(), "жребий выдал карту из окна ротации")

    def test_oc_from_a_side(self):
        draw = self._draw(27)
        for c in draw["oc"]:
            self.assertIn(c["corridor"], ("A", "A+B"))

    def test_exp_only_never_used(self):
        draw = self._draw(27)
        for c in draw["exp"]:
            self.assertNotIn(c["id"], self.usage)

    def test_no_duplicates(self):
        draw = self._draw(31)
        ids = [c["id"] for c in draw["oc"] + draw["main"] + draw["exp"]]
        self.assertEqual(len(ids), len(set(ids)), "карта раздалась дважды")

    def test_shortfall_on_empty_pool(self):
        draw = oracle.draw_constellation(27, [self.cards[0]], self.usage)
        total = len(draw["oc"]) + len(draw["main"]) + len(draw["exp"])
        self.assertEqual(total, 1)
        self.assertGreater(draw["shortfall"], 0)


class WindowTest(unittest.TestCase):
    """Окно ротации: только прошлое, дубль карты считается один раз."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        tmp = Path(self._tmp.name)
        self.batch_dir = tmp / "batches"
        self.batch_dir.mkdir()

    def tearDown(self):
        self._tmp.cleanup()

    def _batch(self, name, y_cards):
        """Мини-батч как в test_gates.synth_batch (карта в шапке слота)."""
        lines = [f"# Batch {name.replace('.md', '')} «synthetic»", ""]
        for i, y in enumerate(y_cards, start=1):
            lines.append(f"P{i:02d} — synth-{i} (VOLT · human · R+ · PL1 · {y})")
            lines.append("POS: synthetic pos line")
            lines.append("NEG: synthetic neg")
        p = self.batch_dir / name
        p.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return p

    def test_window_golden(self):
        corpus = [
            (24, self._batch("T5-24.md", ["Y11"])),
            (25, self._batch("T5-25.md", ["Y7", "Y7"])),
            (26, self._batch("T5-26.md", ["Y3", "Y19"])),
            (23, self._batch("T5-23.md", ["Y23"])),
        ]
        w = oracle.build_window(27, 3, corpus=corpus)
        v = vectors()["window"]
        self.assertEqual([b["no"] for b in w["batches"]], [b["no"] for b in v["batches"]])
        self.assertEqual(w["usedInWindow"], v["usedInWindow"])

    def test_no_future(self):
        # синтетика: окно партии 25 не видит 26-ю
        corpus = [
            (23, self._batch("T5-23.md", ["Y1"])),
            (24, self._batch("T5-24.md", ["Y2"])),
            (26, self._batch("T5-26.md", ["Y3"])),
        ]
        w = oracle.build_window(25, 3, corpus=corpus)
        for b in w["batches"]:
            self.assertLess(b["no"], 25)
        self.assertNotIn("Y3", w["usedInWindow"])

    def test_depth_zero_disables(self):
        corpus = [(24, self._batch("T5-24.md", ["Y11"]))]
        w = oracle.build_window(27, 0, corpus=corpus)
        self.assertEqual(w["batches"], [])
        self.assertEqual(w["usedInWindow"], {})

    def test_live_corpus_window_only_past(self):
        """Живой корпус: окно всегда строго в прошлом (интеграция, не векторы)."""
        w = oracle.build_window(25, 3)
        for b in w["batches"]:
            self.assertLess(b["no"], 25)


class CardNumTest(unittest.TestCase):
    def test_keys(self):
        self.assertEqual(oracle.card_num("Y1"), 1)
        self.assertEqual(oracle.card_num("Y513"), 513)
        self.assertEqual(oracle.card_num("мусор"), -1)


class SelftestCliTest(unittest.TestCase):
    """CLI selftest — тот же прогон, что в CI (паритет против векторов)."""

    def test_selftest_passes(self):
        rc = oracle.cmd_selftest(None)
        self.assertEqual(rc, 0, "selftest зеркала FAIL — зеркало разошлось с каноном")


if __name__ == "__main__":
    unittest.main()
