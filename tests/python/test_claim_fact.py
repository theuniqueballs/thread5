#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Юнит-тесты гейта claimFact (тикет #5, gates.json 1.27.0) — FACT-СЛОЙ ЗАЯВКИ
R+ (В56 «гейты мерили бумагу»): named object в тег-ране + зона грудь/низ +
нет второй панели + носитель состояния (материал/холд); процесс — только
второй носитель (two-carrier В52/В53).

Калибровка тикета (живой материал):
  - ретро T5-34 ловит ≥13 из 15 ложных R+ (сейчас ловит 0 по В56-факту);
  - золотой T5-27 не дрейфует (PASS · ровно 2 WARN);
  - T5-33/T5-32 ретро — WARN без FAIL;
  - P04/P13 (материальные попадания T5-34) — чисто; P25/P26 (честные грани
    с thin cotton / thinned tank) — пропущены: это грани, не ложь.

Прогон: python3 -m unittest discover -s tests/python -v
"""

import json
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO / "tools"))

import gates  # noqa: E402


def make_slot(sid, rating, genre, pos_lines):
    """Мини-слот для fact-проверки: только то, что читает гейт."""
    s = gates.Slot(sid.replace("P", ""), f"slot-{sid.lower()}", f"{genre} · {rating}",
                   f"{sid} — slot-{sid.lower()} ({genre} · {rating})")
    s.pos_lines = list(pos_lines)
    s.pos = " ".join(pos_lines)
    return s


class TestClaimFactSpecs(unittest.TestCase):
    """Цепочка «объявлено → исполнено → доказано» (закон AGENTS №2)."""

    def test_gates_json_section(self):
        cfg = gates.GATES.get("claimFact")
        self.assertIsNotNone(cfg, "секции claimFact нет в gates.json")
        self.assertEqual(cfg.get("applyFrom"), 35, "WARN с T5-35 (закон 8.6)")
        self.assertEqual(cfg.get("mode"), "WARN")
        self.assertEqual(cfg.get("maxPanelsOnZone"), 2)
        for key in ("tokenZones", "objectNouns", "zoneChest", "zoneBottom",
                    "zoneShoulder", "chestPanels", "bottomPanels",
                    "materialStates", "holdTokens"):
            self.assertTrue(cfg.get(key), f"словарь {key} пуст")
        self.assertEqual(gates.GATES.get("version"), "1.27.0")

    def test_registry_row(self):
        reg = json.loads((REPO / "specs" / "gate-registry.json").read_text(encoding="utf-8"))
        row = next((g for g in reg["gates"] if g["section"] == "claimFact"), None)
        self.assertIsNotNone(row)
        self.assertIn("check_claim_fact", row.get("impl") or [])
        self.assertEqual(row.get("receiptField"), "claim_fact")
        self.assertTrue((REPO / str(row.get("test"))).exists())

    def test_validator_required_list(self):
        vsrc = (REPO / "tools" / "validate.py").read_text(encoding="utf-8")
        self.assertIn('"claimFact"', vsrc, "claimFact нет в REQUIRED_GATES_KEYS")


class TestClaimFactBehavior(unittest.TestCase):
    """Слои fact-проверки: каждый класс ловится своей причиной."""

    def _run(self, slots, batch_no=35):
        warns, fails = [], []
        st = gates.check_claim_fact(slots, warns, fails, batch_no=batch_no)
        return st, warns, fails

    def test_rich_material_frame_passes(self):
        """Богатый кадр (P13-класс): named object + материал + зона — PASS."""
        s = make_slot("P01", "R+", "VOLT", [
            "a wine-dark lace set worn as the only layer,",
            "two soft crests through that wine-dark lace where the light pools,",
        ])
        st, warns, fails = self._run([s])
        self.assertEqual(st["passing"], 1)
        self.assertEqual((warns, fails), ([], []))

    def test_transient_hold_passes(self):
        """Транзиентный холд (В43): руки/тейп — легальный носитель R+."""
        s = make_slot("P01", "R+", "VOLT", [
            "topless with tape cross over each nipple, palms flat on the rail,",
        ])
        st, warns, fails = self._run([s])
        self.assertEqual(st["passing"], 1, "тейп-холд — рендер-доказанный класс")

    def test_process_only_carrier_warns(self):
        """Процесс-одиночка (P28-класс): leotard crotch-line, состояние —
        «taut by the split» (процесс), материала нет → WARN."""
        s = make_slot("P01", "R+", "EXP", [
            "the leotard's crotch-line printed taut by the split, toes pointed,",
        ])
        st, warns, fails = self._run([s])
        self.assertEqual(st["caught"], ["P01"])
        self.assertIn("процесс-носитель", warns[0][2])

    def test_no_named_object_warns(self):
        """Заявка на процесс-геометрии («мост из ткани»), не на вещи → WARN."""
        s = make_slot("P01", "R+", "VOLT", [
            "two soft crests across the taut bridges of fabric at the lean,",
        ])
        st, warns, _ = self._run([s])
        self.assertEqual(st["caught"], ["P01"])
        self.assertIn("named object", warns[0][2])

    def test_shoulder_parking_warns(self):
        """PG-13-парковка (P05-класс): заявка R+ на плече → WARN."""
        s = make_slot("P01", "R+", "VOLT", [
            "nothing underneath the slip's bared shoulder but the attic's cool,",
        ])
        st, warns, _ = self._run([s])
        self.assertEqual(st["caught"], ["P01"])
        self.assertIn("PG-13-зоне", warns[0][2])

    def test_second_panel_blocks(self):
        """Вторая панель на зоне (P08-класс): shirt поверх wrap → WARN."""
        s = make_slot("P01", "R+", "VOLT", [
            "a linen shirt hung open, the bandage top's wrap reading the wind,",
            "nothing underneath the wind-pressed wrap but salt air, "
            "two soft points reading against the wrap,",
        ])
        st, warns, _ = self._run([s])
        self.assertEqual(st["caught"], ["P01"])
        self.assertIn("панел", warns[0][2])

    def test_no_claim_token_warns(self):
        """Нет claim-токена рендер-доказанного класса (P27-класс) → WARN."""
        s = make_slot("P01", "R+", "EXP", [
            "the fold's weight employed full-time covering the chest, inverted,",
        ])
        st, warns, _ = self._run([s])
        self.assertEqual(st["caught"], ["P01"])
        self.assertIn("claim-токен", warns[0][2])

    def test_before_era_silent(self):
        """До T5-35 — молчит (эра WARN стартует с 35)."""
        s = make_slot("P01", "R+", "VOLT", ["nothing underneath the dress,"])
        st, warns, fails = self._run([s], batch_no=34)
        self.assertEqual(st["mode"], "silent")
        self.assertEqual((warns, fails), ([], []))

    def test_material_word_boundary(self):
        """«thin» ≠ «nothing»: материал-стем с границей слова — живой урок
        калибровки (подстрока чуть не легализовала ложный R+)."""
        s = make_slot("P01", "R+", "VOLT", [
            "nothing underneath the ribbed tank, both soft crests printing through the tank,",
        ])
        st, warns, _ = self._run([s])
        self.assertEqual(st["caught"], ["P01"],
                         "«nothing» не считается материалом thin — носителя нет")


class TestLiveCalibration(unittest.TestCase):
    """Приёмка тикета на живом дереве: числа, не обещания."""

    FALSE_15 = {"P05", "P07", "P08", "P10", "P12", "P15", "P17", "P19",
                "P20", "P25", "P26", "P27", "P28", "P29", "P30"}

    def test_t5_34_retro_catches_at_least_13_of_15(self):
        """Ретро T5-34: ≥13 из 15 ложных R+; P04/P13 (материальные
        попадания) — чисто; P25/P26 (честные грани) — пропущены."""
        _, _, slots = gates.parse_batch(REPO / "batches" / "T5-34.md")
        warns, fails = [], []
        st = gates.check_claim_fact(slots, warns, fails, batch_no=34, retro=True)
        caught = set(st["caught"])
        hit = caught & self.FALSE_15
        self.assertGreaterEqual(len(hit), 13,
                                f"калибровка тикета: поймано {len(hit)}/15 — {sorted(hit)}")
        self.assertNotIn("P04", caught, "P04 (translucent gel) — материальное попадание, не ложь")
        self.assertNotIn("P13", caught, "P13 (wine-dark lace) — материальное попадание, не ложь")
        self.assertEqual(fails, [], "ретро — WARN, история не переписывается")

    def test_golden_t5_27_untouched(self):
        """Золотой T5-27: гейт молчит до эры — вердикт PASS 0F/2W не
        дрейфует (приёмка тикета)."""
        _, _, slots = gates.parse_batch(REPO / "batches" / "T5-27.md")
        warns, fails = [], []
        st = gates.check_claim_fact(slots, warns, fails, batch_no=27)
        self.assertEqual(st["mode"], "silent")
        self.assertEqual((warns, fails), ([], []))

    def test_t5_32_33_retro_no_new_fails(self):
        """T5-33/T5-32 ретро: WARN-видимость без FAIL (приёмка тикета)."""
        for name, no in (("T5-33", 33), ("T5-32", 32)):
            _, _, slots = gates.parse_batch(REPO / "batches" / f"{name}.md")
            warns, fails = [], []
            gates.check_claim_fact(slots, warns, fails, batch_no=no, retro=True)
            self.assertEqual(fails, [], f"{name}: ретро не рождает FAIL")


if __name__ == "__main__":
    unittest.main()
