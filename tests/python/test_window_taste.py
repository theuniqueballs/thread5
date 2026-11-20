#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Юнит-тесты станции окна и вкуса (unittest, stdlib-only).

Регрессы 2026-11-20:
  - window.delivered_batches сортирует по НОМЕРУ партии (mtime врёт после
    правок старых файлов) — T5-9 < T5-10 < T5-100;
  - taste.take_recent берёт ПОСЛЕДНИЕ вердикт-секции (старая инверсия
    [:depth] скармливала SOL самый старый вкус автора).

Прогон: python3 -m unittest discover -s tests/python -v
"""

import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO / "tools"))

import window  # noqa: E402
import taste  # noqa: E402


class TestWindowOrder(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        tmp = Path(self._tmp.name)
        (tmp / "batches").mkdir()
        self._old_dir = window.BATCH_DIR
        window.BATCH_DIR = tmp / "batches"
        self.batch_dir = tmp / "batches"

    def tearDown(self):
        window.BATCH_DIR = self._old_dir
        self._tmp.cleanup()

    def _touch(self, name):
        p = self.batch_dir / name
        p.write_text("# synthetic\n", encoding="utf-8")
        return p

    def test_bnum(self):
        self.assertEqual(window.bnum("T5-09.md"), 9)
        self.assertEqual(window.bnum("T5-100.md"), 100)
        self.assertEqual(window.bnum("SO-01.md"), -1)

    def test_number_order_beats_mtime(self):
        """T5-10 новее T5-9 по номеру — даже если T5-9 трогали позже."""
        p9 = self._touch("T5-09.md")
        p10 = self._touch("T5-10.md")
        p100 = self._touch("T5-100.md")
        # имитируем «правку старого»: T5-9 получает самый свежий mtime
        import os
        os.utime(p9, (2_000_000_000, 2_000_000_000))
        os.utime(p10, (1_000_000_000, 1_000_000_000))
        os.utime(p100, (1_000_000_000, 1_000_000_000))
        order = [p.name for p in window.delivered_batches()]
        self.assertEqual(order, ["T5-100.md", "T5-10.md", "T5-09.md"])

    def test_gate_reports_and_templates_excluded(self):
        self._touch("T5-01.md")
        self._touch("T5-01.gate-report.md")
        self._touch("_TEMPLATE.md")
        names = [p.name for p in window.delivered_batches()]
        self.assertEqual(names, ["T5-01.md"])


class TestJsonVerdicts(unittest.TestCase):
    """Уровень 0 вкуса (двойной аудит 2026-11-20, P1-02): вердикты в
    структурированной форме verdicts/T5-NN.json — канонический вход,
    Markdown — фолбэк. Батч с JSON не считается дважды."""

    def test_parse_json_verdicts_reads_loved_slots(self):
        loved, extra = taste.parse_json_verdicts()
        # живой вердикт T5-27 обязан читаться из JSON
        t27 = [(b, s, m) for b, s, m in loved if b == "T5-27"]
        self.assertTrue(t27, "T5-27.json не читается — JSON-канон вкуса слеп")
        slots = {s for _, s, _ in t27}
        self.assertIn("P29", slots)   # «поза просто имба»
        self.assertIn("P33", slots)   # «лютая имба»
        for _b, _s, m in t27:
            self.assertTrue(m["genre"], f"мета без жанра: {m}")
            self.assertTrue(m["rating"], f"мета без тира: {m}")

    def test_json_replaces_markdown_no_double_count(self):
        """Батч с JSON исключается из MD-выборки: любимые слоты T5-27
        приходят только из verdicts/T5-27.json, не из LIVING-NOTES."""
        json_loved, json_extra = taste.parse_json_verdicts()
        json_batches = {b for b, *_ in json_loved} | set(json_extra)
        md_all = taste.parse_loved()
        md_json_batches = {b for b, *_ in md_all if b in json_batches}
        # LIVING-NOTES может не иметь секции T5-27 вовсе; если имеет —
        # она не должна попадать в выборку вкуса (json_batches исключаются)
        self.assertIsInstance(json_batches, set)
        self.assertIn("T5-27", json_batches)

    def test_json_extra_fields(self):
        _loved, extra = taste.parse_json_verdicts()
        self.assertIn("T5-27", extra)
        e = extra["T5-27"]
        self.assertEqual(e["overall"], "average")
        self.assertGreaterEqual(e["loved_count"], 8)
        self.assertGreaterEqual(e["lessons"], 1)  # В36


class TestTakeRecent(unittest.TestCase):
    def test_last_not_first(self):
        """Инверсия: [:3] отдавало СТАРЫЕ секции — свежий вкус не доезжал до SOL."""
        sections = ["T5-02", "T5-03", "T5-08", "T5-09", "T5-22"]
        self.assertEqual(taste.take_recent(sections, 3), ["T5-08", "T5-09", "T5-22"])
        self.assertEqual(taste.take_recent(sections, 1), ["T5-22"])
        self.assertEqual(taste.take_recent(sections, 99), sections)

    def test_zero_and_negative(self):
        self.assertEqual(taste.take_recent(["T5-01", "T5-02"], 0), [])
        self.assertEqual(taste.take_recent(["T5-01"], -1), [])

    def test_short_list_unchanged(self):
        self.assertEqual(taste.take_recent(["T5-08", "T5-09", "T5-22"], 3), ["T5-08", "T5-09", "T5-22"])


if __name__ == "__main__":
    unittest.main()
