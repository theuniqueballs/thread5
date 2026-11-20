#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Юнит-тесты инструментов печи (unittest, stdlib-only).

Проверяют регрессии инженерного апгрейда 2026-11-20 (gates.py v1.16.0):
  - SLOT_RE: 3-значные слоты P100+;
  - окно ротации Y-карт смотрит НАЗАД (правка старого батча не видит
    «будущие» партии — раньше бралось глобально новейшее);
  - depth=0 выключает окно (раньше «-0:» отдавало ВСЕ батчи);
  - Corridor: «A + B»/дефисы нормализуются, мусор не матчится;
  - нулевой слот-парсинг виден (guard живёт в main, parse_batch честно
    возвращает [] — фиксируется контрактом теста);
  - y_range из живого реестра.

Прогон: python3 -m unittest discover -s tests/python -v
"""

import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO / "tools"))

import gates  # noqa: E402


def synth_batch(y_cards):
    """Мини-батч с заданными Y-картами (в шапке слота, как T5-25/26)."""
    lines = ["# Batch T5-00 «synthetic»", ""]
    for i, y in enumerate(y_cards, start=1):
        lines.append(f"P{i:02d} — synth-{i} (VOLT · human · R+ · PL1 · {y})")
        lines.append("POS: synthetic pos line")
        lines.append("NEG: synthetic neg")
    return "\n".join(lines) + "\n"


class TempBatchesMixin:
    """Подменяет ROOT/batches на временную папку с синтетикой."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        tmp = Path(self._tmp.name)
        (tmp / "batches").mkdir()
        (tmp / "specs").mkdir()
        # валидный gates.json не нужен — работаем с чистыми функциями
        self._old_root = gates.ROOT
        gates.ROOT = tmp
        self.batch_dir = tmp / "batches"

    def tearDown(self):
        gates.ROOT = self._old_root
        self._tmp.cleanup()

    def write_batch(self, name, y_cards):
        p = self.batch_dir / name
        p.write_text(synth_batch(y_cards), encoding="utf-8")
        return p


class TestSlotRe(unittest.TestCase):
    def test_slot_re_two_and_three_digits(self):
        for sid in ("P01", "P99", "P100", "P999"):
            m = gates.SLOT_RE.match(f"{sid} — slug (VOLT · human · R · PL1)")
            self.assertIsNotNone(m, f"SLOT_RE не берёт {sid}")
        self.assertIsNone(gates.SLOT_RE.match("P1 — slug (…), обрезанный"))

    def test_slot_re_rejects_wrapped_header(self):
        # перенос строки внутри скобок = дрейф формата (SO-06): парсер
        # обязан вернуть 0 слотов — guard в main() превращает это в FAIL
        self.assertIsNone(gates.SLOT_RE.match("P01 — sue (SPECIAL · Sue · PG-13 · свободная"))
        self.assertIsNone(gates.SLOT_RE.match("роевая компоновка · P067_PEARL_VOID)"))


class TestBatchNumber(unittest.TestCase):
    def test_numbers(self):
        self.assertEqual(gates.batch_number("batches/T5-26.md"), 26)
        self.assertEqual(gates.batch_number("T5-100.md"), 100)
        self.assertEqual(gates.batch_number("special/SO-06.md"), -1)


class TestCorridor(unittest.TestCase):
    def _corridor(self, line):
        m = __import__("re").match(r"^Corridor:\s*(A\s*\+\s*B|A\+B|A|B|—|–|-)\s*$", line)
        if not m:
            return None
        v = m.group(1).replace(" ", "")
        return "—" if v in ("—", "–", "-") else v

    def test_forms(self):
        self.assertEqual(self._corridor("Corridor: A"), "A")
        self.assertEqual(self._corridor("Corridor: A+B"), "A+B")
        self.assertEqual(self._corridor("Corridor: A + B"), "A+B")
        self.assertEqual(self._corridor("Corridor: —"), "—")
        self.assertIsNone(self._corridor("Corridor: AB"))       # мусор не матчится
        self.assertIsNone(self._corridor("Corridor: A B"))      # мусор не матчится

    def test_parse_batch_corridor(self):
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as f:
            f.write(
                "P01 — slug (VOLT · human · R+ · PL1)\n"
                "Corridor: A + B\n"
                "POS: p\nNEG: n\n"
            )
            path = f.name
        try:
            _, _, slots = gates.parse_batch(path)
            self.assertEqual(len(slots), 1)
            self.assertEqual(slots[0].corridor, "A+B")
        finally:
            Path(path).unlink(missing_ok=True)


class TestYRange(unittest.TestCase):
    def test_range_from_live_registry(self):
        ycards = gates.load_y_cards()  # живой camera.json (521 карта)
        self.assertGreaterEqual(len(ycards), 500)
        r = gates.y_range(ycards)
        self.assertTrue(r.startswith("Y1–Y"), r)
        self.assertIn("Y5", r)  # серия дошла хотя бы до Y5xx

    def test_empty_registry_is_loud(self):
        self.assertIn("не читается", gates.y_range({}))


class TestPrevYUsageWindow(TempBatchesMixin, unittest.TestCase):
    def test_window_looks_backward(self):
        """Окно для T5-24 = T5-23, T5-22, T5-21 — НИКОГДА T5-25/T5-26."""
        self.write_batch("T5-21.md", ["Y1"])
        self.write_batch("T5-22.md", ["Y2"])
        self.write_batch("T5-23.md", ["Y3"])
        self.write_batch("T5-24.md", ["Y4"])
        self.write_batch("T5-25.md", ["Y5"])
        self.write_batch("T5-26.md", ["Y6"])
        used = gates.load_prev_y_usage(depth=3, exclude=str(self.batch_dir / "T5-24.md"), batch_no=24)
        self.assertEqual(sorted(used), ["Y1", "Y2", "Y3"], "окно обязано смотреть назад")

    def test_depth_zero_disables_window(self):
        self.write_batch("T5-01.md", ["Y1"])
        self.write_batch("T5-02.md", ["Y2"])
        used = gates.load_prev_y_usage(depth=0, batch_no=3)
        self.assertEqual(used, {}, "depth=0 — окно выключено, а не «все батчи»")

    def test_so_batch_number_sees_all(self):
        """batch_no=-1 (SO-комета): фильтр по номеру не режет — все партии."""
        self.write_batch("T5-01.md", ["Y1"])
        self.write_batch("T5-02.md", ["Y2"])
        used = gates.load_prev_y_usage(depth=2, batch_no=-1)
        self.assertEqual(sorted(used), ["Y1", "Y2"])


class TestStoryCardsSoExempt(unittest.TestCase):
    def test_so_does_not_warn(self):
        warns = []
        ok = gates.check_story_cards("special/SO-06.md", warns, batch_no=-1)
        self.assertTrue(ok)
        self.assertEqual(warns, [], "SO-кометы вне цикла story-cards — WARN не шумит")


class TestPaletteSkin(unittest.TestCase):
    """v1.16.0 paletteSkin — В36 «палитра ≠ кожа» (вердикт T5-27 P01 Vae:
    «blood-moon red deep over obsidian skin» = красная кожа на рендере)."""

    def _slot_with_pos(self, pos):
        s = gates.Slot(1, "synth", "VOLT · human · R+ · PL1", "P01 — synth (VOLT · human · R+ · PL1)")
        s.pos = pos
        return [s]

    def test_bleed_caught(self):
        # живой урок T5-27: цвет палитры мостом over утекает в кожу
        warns = []
        n = gates.check_palette_skin(
            self._slot_with_pos("sheer red gown, blood-moon red deep over obsidian skin"),
            warns, batch_no=28,
        )
        self.assertEqual(n, 1)
        self.assertEqual(warns[0][1], "palette-skin")

    def test_clean_skin_no_color(self):
        # канон-цвет вида без цветового токена палитры рядом — чисто
        warns = []
        n = gates.check_palette_skin(
            self._slot_with_pos("obsidian skin, crimson ribbon in her hands"),
            warns, batch_no=28,
        )
        # «crimson ribbon in her hands» — моста к коже нет; skin без цвета в окне
        self.assertEqual(n, 0)
        self.assertEqual(warns, [])

    def test_color_far_from_skin_is_clean(self):
        # цвет в начале кадра, кожа далеко — окно 5 не дотягивается
        warns = []
        n = gates.check_palette_skin(
            self._slot_with_pos("red neon signs far behind her, long corridor, "
                                "deep shadows, quiet hall, obsidian skin"),
            warns, batch_no=28,
        )
        self.assertEqual(n, 0)

    def test_apply_from_28(self):
        # 8.6: WARN с T5-28 — T5-27 не ретроактивен
        warns = []
        n = gates.check_palette_skin(
            self._slot_with_pos("blood red over pale skin"), warns, batch_no=27
        )
        self.assertEqual(n, 0, "T5-27 вне зоны действия гейта (applyFrom 28)")

    def test_no_config_no_crash(self):
        # gates.json без paletteSkin — гейт молчит, не валит печь
        old = gates.GATES.pop("paletteSkin", None)
        try:
            warns = []
            n = gates.check_palette_skin(
                self._slot_with_pos("red over skin"), warns, batch_no=28
            )
            self.assertEqual(n, 0)
        finally:
            if old is not None:
                gates.GATES["paletteSkin"] = old

    def test_hyphen_compound_is_one_token(self):
        # живой ретро-прогон T5-27: P22 «stage-crimson-deep over amp-black,
        # skin-spotlit warm» — кожа в СЛОЖНОМ слове, цвет её не трогает;
        # ложняк дефис-сплита (words() рвал «skin-spotlit» на два) закрыт
        warns = []
        n = gates.check_palette_skin(
            self._slot_with_pos(
                "stage-crimson-deep over amp-black, skin-spotlit warm at the throat"
            ),
            warns, batch_no=28,
        )
        self.assertEqual(n, 0, "skin-spotlit — сложное слово, не модификатор кожи")

    def test_retro_mode_fires_on_old_batches(self):
        # --retro: гейт показывает, что поймал бы в старой партии
        warns = []
        n = gates.check_palette_skin(
            self._slot_with_pos("blood red over pale skin"), warns,
            batch_no=27, retro=True,
        )
        self.assertEqual(n, 1, "ретро-режим не смотрит на applyFrom")


if __name__ == "__main__":
    unittest.main()
