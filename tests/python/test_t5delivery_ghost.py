#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Страж призраков + hotfix-KPI tools/t5delivery.py (аудит 5.3, волна 0).

Классы, которые ловит страж (оба живые прецеденты, не теория):
  T5-28 — ready висит 4 дня: номер занят, окно/жребий не видят, статус
          печатается неотличимо от свежего;
  T5-30 — delivered без формального вердикта 2 дня (AUDIT-5.4 §1.1):
          вердикт существовал в чате, но формально не существовал нигде.

Все фикстуры изолированы (tmp-каталоги, инъекция путей) — тесты не трогают
рабочее дерево и не зависят от реального календаря.

Прогон: python3 -m unittest discover -s tests/python -v
"""

import json
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO / "tools"))

import t5delivery  # noqa: E402


class Fixture(unittest.TestCase):
    """tmp-квитанции и tmp-вердикты — только имена файлов несут даты."""

    def receipts(self, tmp, names):
        d = tmp / "gate-receipts"
        d.mkdir()
        for n in names:
            (d / n).write_text("{}", encoding="utf-8")
        return d

    def verdicts(self, tmp, rows):
        d = tmp / "verdicts"
        d.mkdir()
        for stem, date in rows:
            (d / f"{stem}.json").write_text(
                json.dumps({"schema": "t5-verdict/1", "batch": stem, "date": date},
                           ensure_ascii=False),
                encoding="utf-8")
        return d

    def empty_verdicts(self, tmp):
        """Пустой tmp-verdicts: тесты ОБЯЗАНЫ передавать verdicts_dir явно —
        дефолт ведёт в реальное verdicts/ дерева (урок первых прогонов:
        фикстура T5-30/T5-27 подхватывала настоящие вердикты)."""
        d = tmp / "verdicts"
        d.mkdir(exist_ok=True)
        return d


class GhostAlarmsTest(Fixture):
    def test_ready_stale_alarms_class_t528(self):
        with tempfile.TemporaryDirectory() as td:
            rec = self.receipts(Path(td), ["2026-11-21-T5-28-v1.json"])
            alarms = t5delivery.ghost_alarms(
                now="2026-11-25", index_rows={"T5-28": "ready"},
                receipts_dir=rec)
            self.assertTrue(
                any("ПРИЗРАК ready" in a and "T5-28" in a for a in alarms),
                alarms)

    def test_ready_fresh_is_silent(self):
        with tempfile.TemporaryDirectory() as td:
            rec = self.receipts(Path(td), ["2026-11-24-T5-32-v2.json"])
            alarms = t5delivery.ghost_alarms(
                now="2026-11-25", index_rows={"T5-32": "ready"},
                receipts_dir=rec)
            self.assertEqual(alarms, [])

    def test_ready_on_boundary_is_silent(self):
        # ровно 3 дня — ещё не призрак (строго БОЛЬШЕ READY_STALE_DAYS)
        with tempfile.TemporaryDirectory() as td:
            rec = self.receipts(Path(td), ["2026-11-22-T5-32-v1.json"])
            alarms = t5delivery.ghost_alarms(
                now="2026-11-25", index_rows={"T5-32": "ready"},
                receipts_dir=rec)
            self.assertEqual(alarms, [])

    def test_verdict_ghost_alarms_class_t530(self):
        with tempfile.TemporaryDirectory() as td:
            rec = self.receipts(Path(td), ["2026-11-22-T5-30-v1.json"])
            ver = self.empty_verdicts(Path(td))
            alarms = t5delivery.ghost_alarms(
                now="2026-11-25", index_rows={"T5-30": "delivered"},
                receipts_dir=rec, verdicts_dir=ver)
            self.assertTrue(
                any("ВЕРДИКТ-ПРИЗРАК" in a and "T5-30" in a for a in alarms),
                alarms)

    def test_delivered_with_verdict_is_silent(self):
        with tempfile.TemporaryDirectory() as td:
            rec = self.receipts(Path(td), ["2026-11-22-T5-30-v1.json"])
            ver = self.verdicts(Path(td), [("T5-30", "2026-11-24")])
            alarms = t5delivery.ghost_alarms(
                now="2026-11-25", index_rows={"T5-30": "delivered"},
                receipts_dir=rec, verdicts_dir=ver)
            self.assertEqual(alarms, [])

    def test_legacy_era_without_verdict_is_silent(self):
        # до JSON-канона (T5-27 — первый) вердикты жили в MD/LIVING-NOTES:
        # отсутствие verdicts/*.json у легаси — не тревога
        with tempfile.TemporaryDirectory() as td:
            rec = self.receipts(Path(td), ["2026-11-17-T5-24-v2.json"])
            alarms = t5delivery.ghost_alarms(
                now="2026-11-25", index_rows={"T5-24": "delivered"},
                receipts_dir=rec)
            self.assertEqual(alarms, [])

    def test_archived_never_alarms(self):
        with tempfile.TemporaryDirectory() as td:
            rec = self.receipts(Path(td), ["2026-11-21-T5-28-v1.json"])
            alarms = t5delivery.ghost_alarms(
                now="2026-11-25", index_rows={"T5-28": "archived"},
                receipts_dir=rec)
            self.assertEqual(alarms, [])

    def test_pre_receipt_era_is_silent(self):
        # партии без квитанций (до 2026-10-28) — нечем мерить, молчание честно
        with tempfile.TemporaryDirectory() as td:
            rec = self.receipts(Path(td), [])
            alarms = t5delivery.ghost_alarms(
                now="2026-11-25", index_rows={"T5-03": "ready"},
                receipts_dir=rec)
            self.assertEqual(alarms, [])


class HotfixKpiTest(Fixture):
    def test_t531_shape_two_hotfixes(self):
        # эталон: v1 до вердикта (11-24), хирургия v2 + хотфикс v3 после (11-25)
        with tempfile.TemporaryDirectory() as td:
            rec = self.receipts(Path(td), [
                "2026-11-24-T5-31-v1.json",
                "2026-11-25-T5-31-v2.json",
                "2026-11-25-T5-31-v3.json",
            ])
            ver = self.verdicts(Path(td), [("T5-31", "2026-11-25")])
            kpi = t5delivery.hotfix_kpi(
                index_rows={"T5-31": "delivered"},
                receipts_dir=rec, verdicts_dir=ver)
            self.assertEqual(kpi, [("T5-31", 2)])

    def test_same_day_assembly_is_not_a_hotfix(self):
        # прецедент T5-29: сборка и вердикт в один день без правок после —
        # квитанция дня вердикта без квитанций ДО него не хотфикс
        with tempfile.TemporaryDirectory() as td:
            rec = self.receipts(Path(td), ["2026-11-22-T5-29-v1.json"])
            ver = self.verdicts(Path(td), [("T5-29", "2026-11-22")])
            kpi = t5delivery.hotfix_kpi(
                index_rows={"T5-29": "delivered"},
                receipts_dir=rec, verdicts_dir=ver)
            self.assertEqual(kpi, [])

    def test_same_day_only_receipts_are_ambiguous_not_counted(self):
        # квитанции только ДНЯ вердикта (v1 и v2 в один день с вердиктом):
        # из имён файлов нельзя отличить сборочный прогон от правки после
        # вердикта — честное «недостаточно данных», не счёт (машина не
        # угадывает время суток из имени файла)
        with tempfile.TemporaryDirectory() as td:
            rec = self.receipts(Path(td), [
                "2026-11-25-T5-32-v1.json",
                "2026-11-25-T5-32-v2.json",
            ])
            ver = self.verdicts(Path(td), [("T5-32", "2026-11-25")])
            kpi = t5delivery.hotfix_kpi(
                index_rows={"T5-32": "delivered"},
                receipts_dir=rec, verdicts_dir=ver)
            self.assertEqual(kpi, [])

    def test_no_verdict_means_insufficient_data_not_zero(self):
        with tempfile.TemporaryDirectory() as td:
            rec = self.receipts(Path(td), [
                "2026-11-20-T5-27-v1.json",
                "2026-11-21-T5-27-v2.json",
            ])
            ver = self.empty_verdicts(Path(td))
            kpi = t5delivery.hotfix_kpi(
                index_rows={"T5-27": "delivered"},
                receipts_dir=rec, verdicts_dir=ver)  # вердикта нет
            self.assertEqual(kpi, [])

    def test_ready_batch_not_counted(self):
        with tempfile.TemporaryDirectory() as td:
            rec = self.receipts(Path(td), ["2026-11-25-T5-32-v2.json"])
            kpi = t5delivery.hotfix_kpi(
                index_rows={"T5-32": "ready"}, receipts_dir=rec)
            self.assertEqual(kpi, [])


class ReceiptDatesTest(Fixture):
    def test_versions_and_diagnostics_parsed(self):
        with tempfile.TemporaryDirectory() as td:
            rec = self.receipts(Path(td), [
                "2026-11-18-T5-24-v1.json",
                "2026-11-18-T5-24-v2-act2.json",      # суффикс после -vN легален
                "2026-11-18-T5-25-ystamp-broken.json",  # диагностическая v0
                "2026-11-19-T5-24-v3.json",           # другая дата
            ])
            rows = t5delivery.receipt_dates("T5-24", receipts_dir=rec)
            self.assertEqual(
                rows, [("2026-11-18", 1), ("2026-11-18", 2), ("2026-11-19", 3)])
            self.assertEqual(
                t5delivery.receipt_dates("T5-25", receipts_dir=rec),
                [("2026-11-18", 0)])


class ArchivedStatusTest(unittest.TestCase):
    def test_statuses_include_archived(self):
        self.assertIn("archived", t5delivery.STATUSES)

    def test_validate_tolerates_archived_without_file(self):
        # прецедент T5-28: файлы в archive/, запись в индексе остаётся —
        # validate не требует batches/*.md для archived
        with tempfile.TemporaryDirectory() as td:
            tmp = Path(td)
            idx = {"batches": [{"batch": "T5-28", "status": "archived"}]}
            (tmp / "delivery-index.json").write_text(
                json.dumps(idx), encoding="utf-8")
            (tmp / "batches").mkdir()
            old_idx, old_batch = t5delivery.INDEX_PATH, t5delivery.BATCH_DIR
            t5delivery.INDEX_PATH = tmp / "delivery-index.json"
            t5delivery.BATCH_DIR = tmp / "batches"
            try:
                rc = t5delivery._cmd(["validate"])
            finally:
                t5delivery.INDEX_PATH, t5delivery.BATCH_DIR = old_idx, old_batch
            self.assertEqual(rc, 0)

    def test_validate_still_fails_on_non_archived_ghost(self):
        # не-archived запись без файла по-прежнему FAIL (инвариант №12 цел)
        with tempfile.TemporaryDirectory() as td:
            tmp = Path(td)
            idx = {"batches": [{"batch": "T5-29", "status": "delivered"}]}
            (tmp / "delivery-index.json").write_text(
                json.dumps(idx), encoding="utf-8")
            (tmp / "batches").mkdir()
            old_idx, old_batch = t5delivery.INDEX_PATH, t5delivery.BATCH_DIR
            t5delivery.INDEX_PATH = tmp / "delivery-index.json"
            t5delivery.BATCH_DIR = tmp / "batches"
            try:
                rc = t5delivery._cmd(["validate"])
            finally:
                t5delivery.INDEX_PATH, t5delivery.BATCH_DIR = old_idx, old_batch
            self.assertEqual(rc, 1)

    def test_real_tree_validate_passes(self):
        # живое дерево: T5-28 archived без файла, остальные согласованы
        self.assertEqual(t5delivery._cmd(["validate"]), 0)


if __name__ == "__main__":
    unittest.main()
