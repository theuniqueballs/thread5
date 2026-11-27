#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Юнит-тесты OC-FIDELITY дрифт-таблицы (ПЛАН 5.5 T6.3, renderqc.py).

Боль (вердикт T5-34): OC-fidelity 1/3 — катка SO-19 потеряна, очки SO-20
посажены в NEG. Дрифт по девицам обязан быть виден ТРЕНДОМ партия за
партией, а не «лучший/худший батч». Источник — delta-draft.json всех
RENDER-QC прогонов; спорные файлы (unknown) не карантинятся (урок
T5-17/T5-33) — просто не входят.

Прогон: python3 -m unittest discover -s tests/python -v
"""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
RENDERQC = REPO / "tools" / "renderqc.py"


class TestOcFidelity(unittest.TestCase):
    """Живая калибровка на T5-34 (единственная RENDER-QC дельта на сегодня)."""

    def _run(self, out_dir):
        proc = subprocess.run(
            [sys.executable, str(RENDERQC), "oc-fidelity", "--out", str(out_dir)],
            capture_output=True, text=True, cwd=REPO, timeout=120,
        )
        return proc

    def test_live_table_written_and_shaped(self):
        with tempfile.TemporaryDirectory(prefix="t5-ocfid-") as tmp:
            proc = self._run(tmp)
            self.assertEqual(proc.returncode, 0, proc.stderr[-300:])
            table = Path(tmp) / "oc-fidelity.md"
            self.assertTrue(table.is_file())
            text = table.read_text(encoding="utf-8")
        # шапка таблицы на месте
        for col in ("Девица", "Партий", "Рендеров", "Верность",
                    "Топ потерянных локов"):
            self.assertIn(col, text)
        # живой факт T5-34: три ОС-девицы партии разобраны по канон-локам
        for name in ("Miyu", "Yui", "Rue"):
            self.assertIn(name, text, f"{name} отсутствует в дрифт-таблице")

    def test_live_fidelity_numbers_honest(self):
        """Верность — доля доехавших локов: T5-34 (OC-fidelity 1/3 по
        вердикту) обязан показывать низкие проценты, не 100%."""
        with tempfile.TemporaryDirectory(prefix="t5-ocfid-") as tmp:
            self._run(tmp)
            text = (Path(tmp) / "oc-fidelity.md").read_text(encoding="utf-8")
        import re
        pcts = [int(p) for p in re.findall(r"(\d+)%", text)]
        self.assertTrue(pcts, "проценты верности не найдены")
        self.assertLess(min(pcts), 50,
                        "T5-34: OC-fidelity был 1/3 — таблица не может показывать сплошные 100%")
        for p in pcts:
            self.assertLessEqual(p, 100)
            self.assertGreaterEqual(p, 0)

    def test_unknown_files_do_not_quarantine(self):
        """Спорные файлы не входят в таблицу молча — но и не роняют её
        (25 unknown в живой T5-34 дельте, таблица всё равно построена)."""
        draft = REPO / "tools" / "out" / "renderqc-T5-34" / "delta-draft.json"
        if not draft.exists():
            self.skipTest("живая дельта T5-34 недоступна")
        import json
        d = json.loads(draft.read_text(encoding="utf-8"))
        self.assertTrue(d.get("unknown"), "в T5-34 дельте обязаны быть unknown-файлы")
        with tempfile.TemporaryDirectory(prefix="t5-ocfid-") as tmp:
            proc = self._run(tmp)
            self.assertEqual(proc.returncode, 0,
                             "unknown-файлы роняют дрифт-таблицу — карантин запрещён (T5-33)")


if __name__ == "__main__":
    unittest.main()
