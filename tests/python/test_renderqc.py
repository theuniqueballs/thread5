#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Тесты renderqc.py (ПЛАН 5.5 T2.1, В56 «гейты мерили бумагу»).

Продукт-изация сеанса t534-render-qc: инбокс-рендеры → VLM-разбор →
таблица «слот/заявка/канон-локи/эхо» → автодрафт rating_truth_delta.
Автор арбитрирует (truth: null — тир решает автор, LAWS §9).

Проверяется:
1. Парсер QC-файлов: VLM-ответ → секции (оба формата t534:
   CHARACTER/CLOTHING STATE и HAIR/EYES/MARKERS/GARMENT).
2. Пин: P-номер из имени файла; канон-локи (≥3 стемов, единственный
   слот); спорный пин не ставится — unknown (урок T5-17/T5-33).
3. Канонический промпт: 9 секций, имена канонов партии.
4. Живой прогон на t534-render-qc (34 файла в git): таблица + драфт
   собираются, truth везде null, неизвестные видны списком автору.
"""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO / "tools"))

import renderqc  # noqa: E402

QC_DIR = REPO / "tools" / "out" / "t534-render-qc"


class TestParsers(unittest.TestCase):
    def test_parse_qc_file_both_formats(self):
        f1 = QC_DIR / "P01-OS-Miyu-Tendencies.json"
        secs = renderqc.parse_qc_file(f1)
        self.assertIsNotNone(secs)
        self.assertTrue(any("CHARACTER" in k or "HAIR" in k for k in secs))

    def test_parse_qc_file_rejects_non_vlm(self):
        self.assertIsNone(renderqc.parse_qc_file(
            QC_DIR / "id-batch-1.json"))

    def test_pin_by_filename(self):
        rows = [{"slot": "P07", "claim": "R+", "genre": "VOLT", "name": None}]
        sid, why = renderqc.pin_to_slot(
            {}, "P07-MAIN-strapfall-Rplus.json", rows, {})
        self.assertEqual(sid, "P07")
        self.assertIn("имя файла", why)

    def test_pin_by_canon_locks(self):
        srcs = {"Miyu": "straight bangs heterochromia light"}
        rows = [{"slot": "P01", "claim": "R+", "genre": "EXQ", "name": "Miyu"}]
        secs = {"HAIR": "straight long bangs", "EYES": "heterochromia"}
        sid, why = renderqc.pin_to_slot(secs, "single-abc.json", rows, srcs)
        self.assertEqual(sid, "P01")
        self.assertIn("канон-локи Miyu", why)

    def test_weak_pin_goes_unknown(self):
        srcs = {"Miyu": "straight bangs heterochromia"}
        rows = [{"slot": "P01", "claim": "R+", "genre": "EXQ", "name": "Miyu"}]
        sid, why = renderqc.pin_to_slot(
            {"HAIR": "something entirely different"}, "single-x.json",
            rows, srcs)
        self.assertEqual(sid, "unknown")

    def test_prompt_contract(self):
        import io
        import contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            renderqc.cmd_prompt("T5-34")
        out = buf.getvalue()
        for sec in renderqc.SECTIONS:
            self.assertIn(sec, out)
        self.assertIn("Miyu", out)  # имена канонов партии видны VLM


class TestLiveT534Run(unittest.TestCase):
    """Живой прогон на наследии сеанса (34 файла в git) — квитанция
    продукт-изации: таблица и драфт собираются теми же данными."""

    @classmethod
    def setUpClass(cls):
        import tempfile
        cls._tmp = tempfile.TemporaryDirectory()
        cls.out = Path(cls._tmp.name)
        rc = renderqc.cmd_table(str(QC_DIR), "T5-34", str(cls.out))
        assert rc == 0

    @classmethod
    def tearDownClass(cls):
        cls._tmp.cleanup()

    def test_table_and_draft_exist(self):
        self.assertTrue((self.out / "table.md").exists())
        d = json.loads((self.out / "delta-draft.json").read_text(encoding="utf-8"))
        self.assertEqual(d["batch"], "T5-34")
        self.assertGreaterEqual(len(d["rows"]), 9)
        self.assertGreaterEqual(len(d["unknown"]), 20)

    def test_truth_is_always_null(self):
        """Машина не вердиктит (LAWS §9): тир решает автор."""
        d = json.loads((self.out / "delta-draft.json").read_text(encoding="utf-8"))
        for r in d["rows"]:
            self.assertIsNone(r["truth"])

    def test_os_slots_pinned_with_canon(self):
        d = json.loads((self.out / "delta-draft.json").read_text(encoding="utf-8"))
        by_slot = {r["slot"]: r for r in d["rows"]}
        self.assertIn("P01", by_slot)  # Miyu — имя файла
        self.assertIn("P02", by_slot)  # Rue
        self.assertIn("P03", by_slot)  # Yui
        self.assertEqual(by_slot["P01"]["claim"], "R+")

    def test_unknown_listed_for_author(self):
        t = (self.out / "table.md").read_text(encoding="utf-8")
        self.assertIn("Не припинены", t)
        self.assertIn("id-batch-1.json", t)  # манифесты видны, не карантин


if __name__ == "__main__":
    unittest.main()
