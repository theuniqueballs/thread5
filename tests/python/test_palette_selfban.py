#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Юнит-тесты №17 «палитра не запрещает собственную суть» (тикет #3,
palettes.json 1.21.1).

Решение автора 2026-11-27 (вербатим из тикета): «неон не виноват — тему
хуёво раскрыл писец». Наказание словаря = лечение не того органа:
enforcement темы — THEME-SPEC/themeEcho (В54), не баны слов в палитрах.
Класс «тематическая волна не наследует forbidden из словаря мёртвой
темы» не должен вернуться в волну 19.

Прогон: python3 -m unittest discover -s tests/python -v
"""

import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO / "tools"))

import validate  # noqa: E402  (модуль-скрипт: main() под __main__ — импорт безопасен)


class TestSelfbanClass(unittest.TestCase):
    """Класс: кислотная семья ≠ самозапрет неона — ловится и не возвращается."""

    def test_live_palettes_zero_selfbans(self):
        """Живое дерево: 0 самозапретов — 30 правок тикета #3 реальны."""
        import json
        pal = json.loads((REPO / "specs" / "palettes.json").read_text(encoding="utf-8"))
        self.assertEqual(pal.get("version"), "1.21.1")
        bans = validate.palette_selfbans(pal.get("palettes"))
        self.assertEqual(bans, [], f"самозапреты вернулись: {bans[:3]}")

    def test_lsd_wave_keeps_antidrift_guards(self):
        """muddy colors / photo color остались — это защита палитры, не бан темы."""
        import json
        pal = json.loads((REPO / "specs" / "palettes.json").read_text(encoding="utf-8"))
        lsd = [p for p in pal["palettes"] if p.get("family") == "lsd_wave_18"]
        self.assertEqual(len(lsd), 30, "семья lsd_wave_18 обязана быть целой (30)")
        for p in lsd:
            forb = " ".join(p.get("forbidden") or []).lower()
            self.assertNotIn("neon", forb, f"{p['id']}: самозапрет неона жив")
            self.assertIn("muddy colors", forb,
                          f"{p['id']}: анти-дрейф 'muddy colors' изъят — не по тикету")

    def test_tamper_acid_family_with_neon_is_caught(self):
        """Тампер: кислотная палитра с 'neon' в forbidden → класс ловится
        (волна 19 не унаследует forbidden из словаря мёртвой темы молча)."""
        palettes = [
            {"id": "P400_ACID_TEST", "family": "lsd_wave_19",
             "forbidden": ["neon", "muddy colors"]},
        ]
        bans = validate.palette_selfbans(palettes)
        self.assertEqual(len(bans), 1)
        self.assertEqual(bans[0][0], "P400_ACID_TEST")
        self.assertEqual(bans[0][1], "neon")

    def test_tamper_by_id_without_family_is_caught(self):
        """Кислотность читается и из id без family — «ACID» в имени достаточен."""
        bans = validate.palette_selfbans([
            {"id": "P401_NEON_DREAM", "forbidden": ["neon"]},
        ])
        self.assertEqual(len(bans), 1)

    def test_non_acid_family_may_forbid_neon(self):
        """Не-кислотная семья банит неон законно (анти-дрейф: noir против
        кислоты) — класс не расширяется на любые цвета."""
        bans = validate.palette_selfbans([
            {"id": "P01_NOIR_VELVET", "family": "noir",
             "forbidden": ["neon", "muddy colors"]},
            {"id": "P02_DAWN_AMBER", "family": "warm_dawn", "forbidden": ["neon"]},
        ])
        self.assertEqual(bans, [], "не-кислотная семья законно держит 'neon' в forbidden")

    def test_saturated_variants_also_selfban(self):
        """Семья ловит и 'vivid colors'/'saturated colors' — суть волны
        шире одного слова."""
        bans = validate.palette_selfbans([
            {"id": "P402_LSD_POOL", "family": "lsd_wave_19",
             "forbidden": ["saturated colors"]},
            {"id": "P403_ACID_RAIN", "family": "acid", "forbidden": ["vivid colors"]},
        ])
        self.assertEqual(len(bans), 2)


if __name__ == "__main__":
    unittest.main()
