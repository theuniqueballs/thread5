#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Юнит-тесты гейта k1Sense (тикет #2, gates.json 1.26.0) — смысл-поле К-1
в каждой карточке stories.md обязательно с T5-35.

Класс «объявлено ≠ исполнено» (аудит 5.4 §2.5 обещал «без оправданий»):
AGENTS:137 объявил К-1 волной 1д без формы, гейта, реестра и теста.
Вариант А тикета — исполнить: форма в _BRIEF-TEMPLATE + гейт + секция
реестра + эти тесты. Приёмка тикета: «нет поля → WARN с T5-35 /
ретро молчит».

Прогон: python3 -m unittest discover -s tests/python -v
"""

import json
import re
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
sys_path_tool = str(REPO / "tools")

import sys  # noqa: E402

sys.path.insert(0, sys_path_tool)

import gates  # noqa: E402


def _make_batch(tmp: Path, name: str, stories: str | None) -> Path:
    """Мини-батч: файл + соседняя папка со stories.md (или без неё)."""
    d = Path(tmp)
    batch = d / name
    batch.write_text(f"# Batch {name[:-3]}: «тест»\n\nP01 — dummy (VOLT · R+)\n", encoding="utf-8")
    if stories is not None:
        cards = d / name[:-3]
        cards.mkdir(exist_ok=True)
        (cards / "stories.md").write_text(stories, encoding="utf-8")
    return batch


STORIES_TWO_CARDS = (
    "# T5-35 — карточки историй\n\n"
    "## Мейн-сегмент (P04–P24)\n"
    "- SOL: сборка от геометрии и темы\n"
    "- К-1: её мир отвечает теплом на каждое движение\n"
    "- Отвергнуто: (1) … — почему нет: …\n\n"
    "## EXP-сегмент (P25–P30)\n"
    "- SOL: грань-X по квоте\n"
    "- Отвергнуто: (2) … — почему нет: …\n"
)

STORIES_ALL_K1 = STORIES_TWO_CARDS.replace(
    "## EXP-сегмент (P25–P30)\n- SOL: грань-X по квоте\n",
    "## EXP-сегмент (P25–P30)\n- SOL: грань-X по квоте\n- К-1: граница дышит, но не переходит\n",
)


class TestK1Specs(unittest.TestCase):
    """Цепочка «объявлено → исполнено → доказано» не разорвана (закон №2)."""

    def test_gates_json_section(self):
        cfg = gates.GATES.get("k1Sense")
        self.assertIsNotNone(cfg, "секции k1Sense нет в gates.json")
        self.assertEqual(cfg.get("applyFrom"), 35, "К-1 обязателен с T5-35 (AGENTS:137)")
        self.assertEqual(cfg.get("mode"), "WARN", "закон 8.6: WARN-старт")
        re.compile(cfg.get("pattern", ""))
        self.assertEqual(gates.GATES.get("version"), "1.30.0")  # 1.30.0 — carrierTruth (тикет #7/В61); 1.29.0 — nudeTruth (вердикт T5-35)

    def test_registry_row(self):
        reg = json.loads((REPO / "specs" / "gate-registry.json").read_text(encoding="utf-8"))
        row = next((g for g in reg["gates"] if g["section"] == "k1Sense"), None)
        self.assertIsNotNone(row, "секции k1Sense нет в реестре")
        self.assertIn("check_k1_sense", row.get("impl") or [])
        self.assertEqual(row.get("receiptField"), "k1_sense")
        self.assertTrue((REPO / str(row.get("test"))).exists(), "тест из реестра не существует")

    def test_validator_required_list(self):
        vsrc = (REPO / "tools" / "validate.py").read_text(encoding="utf-8")
        self.assertIn('"k1Sense"', vsrc, "k1Sense нет в REQUIRED_GATES_KEYS — валидатор слеп к секции")

    def test_template_carries_the_field(self):
        t = (REPO / "batches" / "_BRIEF-TEMPLATE.md").read_text(encoding="utf-8")
        self.assertIn("К-1", t, "форма К-1 отсутствует в _BRIEF-TEMPLATE.md — «AGENTS говорит, цех не умеет»")


class TestK1Behavior(unittest.TestCase):
    """Приёмка тикета: нет поля → WARN с T5-35; до эры/ретро — молчит."""

    def test_card_without_k1_warns_at_35(self):
        warns = []
        with tempfile.TemporaryDirectory(prefix="t5-k1-") as tmp:
            p = _make_batch(Path(tmp), "T5-35.md", STORIES_TWO_CARDS)
            st = gates.check_k1_sense(p, warns, batch_no=35)
        self.assertEqual(st["cards"], 2)
        self.assertEqual(st["with_k1"], 1)
        self.assertEqual(st["without"], ["EXP-сегмент (P25–P30)"])
        self.assertEqual(len(warns), 1)
        self.assertEqual(warns[0][1], "k1-sense")
        self.assertIn("EXP-сегмент", warns[0][2], "WARN обязан назвать карточку")

    def test_all_cards_with_k1_clean(self):
        warns = []
        with tempfile.TemporaryDirectory(prefix="t5-k1-") as tmp:
            p = _make_batch(Path(tmp), "T5-35.md", STORIES_ALL_K1)
            st = gates.check_k1_sense(p, warns, batch_no=35)
        self.assertEqual(st["with_k1"], 2)
        self.assertEqual(st["without"], [])
        self.assertEqual(warns, [])

    def test_before_era_silent(self):
        """До T5-35 — молчит (форма новая, история не переписывается)."""
        warns = []
        with tempfile.TemporaryDirectory(prefix="t5-k1-") as tmp:
            p = _make_batch(Path(tmp), "T5-34.md", STORIES_TWO_CARDS)
            st = gates.check_k1_sense(p, warns, batch_no=34)
        self.assertEqual(st["mode"], "silent")
        self.assertEqual(warns, [])

    def test_no_stories_silent(self):
        """Нет stories.md — карточек не видит, не шумит: за отсутствие
        карточек отвечает storyCardsGate (не дублируем)."""
        warns = []
        with tempfile.TemporaryDirectory(prefix="t5-k1-") as tmp:
            p = _make_batch(Path(tmp), "T5-35.md", None)
            st = gates.check_k1_sense(p, warns, batch_no=35)
        self.assertEqual(st["cards"], 0)
        self.assertEqual(st["with_k1"], 0)
        self.assertEqual(warns, [], "k1Sense не дублирует storyCardsGate")

    def test_live_t5_34_stays_silent(self):
        """Живой T5-34 (карточки-сегменты без К-1, форма тогда не существовала)
        не получает новых WARN — ретро-инвариант приёмки тикета."""
        warns = []
        st = gates.check_k1_sense(REPO / "batches" / "T5-34.md", warns, batch_no=34)
        self.assertEqual(st["mode"], "silent")
        self.assertEqual(warns, [])

    def test_live_t5_34_would_catch_at_35(self):
        """Калибровка на живом материале: те же карточки T5-34, номер 35 —
        гейт видит все три карточки без К-1 (сегменты ОС/мейн/EXP)."""
        warns = []
        st = gates.check_k1_sense(REPO / "batches" / "T5-34.md", warns, batch_no=35)
        self.assertEqual(st["cards"], 3, "T5-34: три карточки-сегмента")
        self.assertEqual(len(warns), 1)
        self.assertIn("3 из 3", warns[0][2])


if __name__ == "__main__":
    unittest.main()
