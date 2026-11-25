#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Калибровочный мост rating_truth_delta (аудит 5.3 §3.1, волна 1; решения
автора №2/№3 2026-11-25: «послотовые метки сразу», «как только — так сразу»).

Мост — LAB-отчёт: машинный тир слота (slot_table квитанции) против
послотовых меток автора (verdicts/T5-NN.json → rating_truth_delta). Он
НИЧЕГО не правит; правка словарей ratingTruth — по слову автора
«калибровка принята», после — калибровка В43 (test_t529_lessons.py).

Классификация, которую держат тесты:
  сошлось · ЛОЖНЫЙ R+ (машина R+, автор ниже) · ПРОПУЩЕННЫЙ R+ (автор R+,
  машина ниже) · дрейф (R↔PG-13) · слот не найден · нелегальный тир.

Прогон: python3 -m unittest discover -s tests/python -v
"""

import argparse
import json
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO / "tools"))

import oracle  # noqa: E402


def ns(**kw):
    return argparse.Namespace(**kw)


class RatingDeltaTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.rec_dir = self.root / "gate-receipts"
        self.rec_dir.mkdir()
        self.ver_dir = self.root / "verdicts"
        self.ver_dir.mkdir()

    def tearDown(self):
        self.tmp.cleanup()

    def receipt(self, name, ratings, channels=None):
        """Квитанция с slot_table: id → rating (+ channel)."""
        table = [{"id": s, "rating": r,
                  "channel": (channels or {}).get(s, "")}
                 for s, r in ratings.items()]
        p = self.rec_dir / name
        p.write_text(json.dumps({"slot_table": table}), encoding="utf-8")
        return p

    def verdict(self, stem, marks):
        p = self.ver_dir / f"{stem}.json"
        p.write_text(json.dumps(
            {"schema": "t5-verdict/1", "batch": stem,
             "date": "2026-11-25", "rating_truth_delta": marks},
            ensure_ascii=False), encoding="utf-8")
        return p

    def run_delta(self, stem, receipt=None, verdict=None):
        import io
        import contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = oracle.cmd_rating_delta(ns(
                batch=stem,
                receipt=str(receipt) if receipt else "",
                verdict=str(verdict) if verdict else ""))
        return rc, buf.getvalue()

    def test_find_latest_receipt_by_date_and_version(self):
        self.receipt("2026-11-25-T5-32-v1.json", {"P01": "R"})
        self.receipt("2026-11-24-T5-32-v9.json", {"P01": "R"})  # дата старше
        got = oracle.find_latest_receipt("T5-32", receipts_dir=self.rec_dir)
        self.assertEqual(got.name, "2026-11-25-T5-32-v1.json")
        self.receipt("2026-11-25-T5-32-v2.json", {"P01": "R"})
        got = oracle.find_latest_receipt("T5-32", receipts_dir=self.rec_dir)
        self.assertEqual(got.name, "2026-11-25-T5-32-v2.json")

    def test_no_receipt_is_loud(self):
        rc, out = self.run_delta("T5-99")
        self.assertEqual(rc, 1)
        self.assertIn("не найдена", out)

    def test_no_verdict_is_soft_zero(self):
        # метки приходят с рендером — их отсутствие НЕ FAIL.
        # Т5-32 вердиктирован 2026-11-25 (verdicts/T5-32.json есть) —
        # пример «вердикта нет» переехал на следующий батч.
        rec = self.receipt("2026-11-25-T5-33-v1.json", {"P01": "R"})
        rc, out = self.run_delta("T5-33", receipt=rec)
        self.assertEqual(rc, 0)
        self.assertIn("вердикта нет", out)

    def test_no_marks_prints_schema_hint(self):
        rec = self.receipt("2026-11-25-T5-32-v1.json", {"P01": "R"})
        v = self.ver_dir / "T5-32.json"
        v.write_text(json.dumps({"schema": "t5-verdict/1", "batch": "T5-32",
                                 "date": "2026-11-25"}), encoding="utf-8")
        rc, out = self.run_delta("T5-32", receipt=rec, verdict=v)
        self.assertEqual(rc, 0)
        self.assertIn("rating_truth_delta", out)
        self.assertIn("сравнивать не с чем", out)

    def test_classification_counts(self):
        rec = self.receipt("2026-11-25-T5-31-v3.json", {
            "P07": "R",     # сошлось (автор R)
            "P30": "R+",    # ложный R+ (автор R) — канал декантера
            "P28": "R",     # пропущенный R+ (автор R+, эталон В44)
            "P10": "R",     # дрейф (автор PG-13)
        }, channels={"P30": "wet-sheer-delivery", "P28": "contact-physics",
                     "P10": ""})
        v = self.verdict("T5-31", [
            {"slot": "P07", "truth": "R"},
            {"slot": "P30", "truth": "R", "note": "крупный объект-панель"},
            {"slot": "P28", "truth": "R+", "note": "эталон В44"},
            {"slot": "P10", "truth": "PG-13"},
            {"slot": "P99", "truth": "R"},       # слота в квитанции нет
            {"slot": "P07", "truth": "X"},       # нелегальный тир
        ])
        rc, out = self.run_delta("T5-31", receipt=rec, verdict=v)
        self.assertEqual(rc, 0)
        self.assertIn("меток автора 6", out)
        self.assertIn("сошлось 1", out)
        self.assertIn("ложных R+ 1", out)
        self.assertIn("пропущенных R+ 1", out)
        self.assertIn("дрейф 1", out)
        self.assertIn("P99", out)                 # неизвестный слот виден
        self.assertIn("нелегальный тир 1", out)
        self.assertIn("ЛОЖНЫЕ R+", out)
        self.assertIn("P30: машина R+ → автор R", out)
        self.assertIn("крупный объект-панель", out)   # note доезжает
        self.assertIn("wet-sheer-delivery×1", out)    # группировка каналов
        self.assertIn("LAB: словари не тронуты", out)

    def test_clean_batch_all_agree(self):
        rec = self.receipt("2026-11-25-T5-32-v1.json",
                           {"P01": "R+", "P02": "R"})
        v = self.verdict("T5-32", [
            {"slot": "P01", "truth": "R+"},
            {"slot": "P02", "truth": "R"},
        ])
        rc, out = self.run_delta("T5-32", receipt=rec, verdict=v)
        self.assertEqual(rc, 0)
        self.assertIn("сошлось 2", out)
        self.assertIn("ложных R+ 0", out)
        self.assertIn("пропущенных R+ 0", out)

    def test_real_tree_t531_soft_zero(self):
        # живое дерево: вердикт T5-31 есть, меток ещё нет — мягкий ноль
        rc, out = self.run_delta("T5-31")
        self.assertEqual(rc, 0)


if __name__ == "__main__":
    unittest.main()
