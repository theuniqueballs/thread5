#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Юнит-тесты СЛОЖНОСТЬ-БЮДЖЕТА ПАРТИИ (ПЛАН 5.5 T9.3, gates.py v1.27.0).

Боль: T4-деградация — «машина научилась проходить собственные гейты».
Рост сложности обязан быть виден ЧИСЛОМ в квитанции каждой партии, а не
ощущением. Счётчик — не новый реестр и не новая доктрина (план §5, риск
«сложность-бюджет сам станет сложностью»): active/total + эры на подходе.

Прогон: python3 -m unittest discover -s tests/python -v
"""

import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO / "tools"))

import gates  # noqa: E402


class TestComplexityBudget(unittest.TestCase):
    """Счётчик: активные секции по эре партии, рост виден числом."""

    def test_growth_is_visible(self):
        """Эра 35 активирует больше секций, чем эра 27 — T4-тренд измерим."""
        b27 = gates.complexity_budget(27)
        b35 = gates.complexity_budget(35)
        self.assertGreater(b35["active"], b27["active"],
                           "между T5-27 и T5-35 эры включались — счётчик обязан это видеть")
        self.assertEqual(b35["total"], b27["total"])

    def test_counts_match_registry(self):
        """total = числу секций gates.json (дикт-секции, не метаданные)."""
        reg = gates.complexity_budget(35)
        dict_sections = sum(1 for v in gates.GATES.values() if isinstance(v, dict))
        self.assertEqual(reg["total"], dict_sections)

    def test_pending_eras_listed(self):
        """Секции, чья эра ещё не наступила, перечислены с номером партии."""
        b30 = gates.complexity_budget(30)
        pending_now = {p.split("·")[0] for p in b30["pending"]}
        #claimFact/k1Sense/voltRun/themeEcho стартуют с 35 — в эре 30 они на подходе
        self.assertIn("claimFact", pending_now)
        b35 = gates.complexity_budget(35)
        pending_35 = {p.split("·")[0] for p in b35["pending"]}
        self.assertNotIn("claimFact", pending_35)

    def test_receipt_carries_budget(self):
        """Живая квитанция несёт complexity_budget (T4-тревога числом)."""
        import json
        import subprocess
        import tempfile
        out = Path(tempfile.mkdtemp(prefix="t5-cb-")) / "r.json"
        subprocess.run(
            [sys.executable, str(REPO / "tools" / "gates.py"),
             str(REPO / "batches" / "T5-27.md"), "--json", str(out)],
            capture_output=True, cwd=REPO, timeout=180,
        )
        receipt = json.loads(out.read_text(encoding="utf-8"))
        cb = receipt.get("complexity_budget")
        self.assertIsNotNone(cb, "квитанция без complexity_budget — рост сложности невидим")
        self.assertIn("active", cb)
        self.assertIn("total", cb)


if __name__ == "__main__":
    unittest.main()
