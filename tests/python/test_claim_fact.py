#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Юнит-тесты гейта claimFact (тикет #5 → #6, gates.json 1.28.0) — FACT-СЛОЙ ЗАЯВКИ
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
        # тикет #6: новые словари правки
        for key in ("openModifiers", "geometryClaims", "panelSynonymGroups",
                    "shoulderAnchors"):
            self.assertTrue(cfg.get(key), f"словарь {key} пуст")
        for noun in ("shirt", "knit", "ribbed knit", "cloth", "dress-front"):
            self.assertIn(noun, cfg["objectNouns"], f"тикет #6: {noun} забыт")
        self.assertIn("tight", cfg["materialStates"], "тикет #6: tight забыт")
        self.assertNotIn("bib", cfg["chestPanels"],
                         "тикет #6: номер-нагрудник не глушит чтение")
        self.assertEqual(gates.GATES.get("version"), "1.28.0")

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


class TestTicket6Fixes(unittest.TestCase):
    """Приёмка тикета #6: живой прогон T5-35 вскрыл ложные WARN — чинится."""

    def _run(self, slots, batch_no=35):
        warns, fails = [], []
        st = gates.check_claim_fact(slots, warns, fails, batch_no=batch_no)
        return st, warns, fails

    def test_shirt_and_knit_are_objects(self):
        """Корень 1: plain shirt/knit — носители (P11/P13/P04 T5-35),
        nightshirt был, shirt забыли; knit — вязание P04/P14."""
        for word in ("thin opened shirt", "rain-wet ribbed knit"):
            s = make_slot("P01", "R+", "VOLT", [
                f"two soft points reading against the {word} at the chest, "
                "nothing underneath the wet cloth but steam,",
            ])
            st, warns, _ = self._run([s])
            self.assertEqual(st["caught"], [], f"{word} — named object")

    def test_hyphen_state_compounds_match(self):
        """Корень 2: rain-wet / sheer-lined — состояния-компаунды PROSE
        PLUS матчатся стемом (левая граница слова, не дефис)."""
        s = make_slot("P01", "R+", "VOLT", [
            "breast shape held high in the corset's tight weave at the chest,",
            "two soft crests across the sheer-lined corset's weave under the lamp,",
        ])
        st, _, _ = self._run([s])
        self.assertEqual(st["caught"], [], "sheer-lined на соседней строке — носитель")

    def test_carrier_window_plus_minus_one_line(self):
        """Корень 3: окно носителя ±1 строка вокруг claim-строки (PROSE
        PLUS: строка = кадр-аспект — P10-паттерн T5-35)."""
        s = make_slot("P01", "R+", "VOLT", [
            "breast shape held high in the corset's tight weave, nothing underneath,",
            "mid-flip of wet hair, arms up, the room's steam rising,",
        ])
        st, warns, _ = self._run([s])
        self.assertEqual(st["caught"], [], "wet на ±1 строке — носитель")

    def test_open_modifier_voids_panel(self):
        """Корень 4: worn open / zipper ride / fallen off — раскрытая
        панель не глушит заявку (P15-паттерн T5-35)."""
        s = make_slot("P01", "R+", "VOLT", [
            "post-comp jacket zipper ride + leotard leg-line, breast shape riding "
            "the zipper's track, nothing underneath the leotard but the race's heat,",
            "two soft crests through the leotard's tight weave at the chest,",
        ])
        st, warns, _ = self._run([s])
        self.assertEqual(st["caught"], [], "раскрытая панель не считается")

    def test_geometry_claim_carries_itself(self):
        """Корень 5: H-15/В53 — геометрия-заявка (camera between / под-
        подолом) токенизирована и несёт себя сама, как холд."""
        s = make_slot("P01", "R+", "VOLT", [
            "staircase under-hem shot, the camera between her knees one flight "
            "below her climb, the skirt's hem living its own polygon,",
        ])
        st, warns, _ = self._run([s])
        self.assertEqual(st["caught"], [], "геометрия = носитель (X-слип 0/6)")

    def test_shoulder_incident_not_parking(self):
        """Плечо-инцидент позы («chin over shoulder») не паркует заявку
        груди (P10 T5-35); якорь-фраза («at the shoulder line») паркует
        (P17 T5-34 — живой урок разводки)."""
        incident = make_slot("P01", "R+", "VOLT", [
            "chair straddle, chin over shoulder, breast shape held high in the "
            "corset's tight weave at the chest, nothing underneath the sheer corset,",
        ])
        st, _, _ = self._run([incident])
        self.assertEqual(st["caught"], [], "инцидент позы ≠ парковка")
        anchor = make_slot("P02", "R+", "VOLT", [
            "a sheer organza blouse, see-through at the shoulder line with "
            "nothing underneath the film but the room's held breath, "
            "two soft crests across the film's pale field,",
        ])
        st, warns, _ = self._run([anchor])
        self.assertEqual(st["caught"], ["P02"], "якорь-фраза = PG-13-парковка")

    def test_top_heavy_not_a_panel(self):
        """Живой урок правки: правый дефис-страж noun удержан — «top-heavy
        build» не панель груди (P04/P11/P27 T5-35 чуть не поймались)."""
        s = make_slot("P01", "R+", "VOLT", [
            "two soft points reading against the thin opened shirt at the chest, "
            "nothing underneath the wet cloth but steam,",
            "full top-heavy build settled into the saddle,",
        ])
        st, _, _ = self._run([s])
        self.assertEqual(st["caught"], [], "top-heavy — телосложение, не вещь")


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

    def test_t5_35_rerun_caught_empty(self):
        """Тикет #6, приёмка: перегон живой T5-35 исправленным гейтом —
        ложные WARN схлопнулись (v1: 8 пойманных из 20, 5+ ложных по
        разбору Чарли; v2: заявки на физике кадра у всех 20 R+)."""
        _, _, slots = gates.parse_batch(REPO / "batches" / "T5-35.md")
        warns, fails = [], []
        st = gates.check_claim_fact(slots, warns, fails, batch_no=35)
        self.assertEqual(st["caught"], [],
                         f"ложные WARN живы: {st['caught']}")
        self.assertEqual(st["passing"], 20)
        self.assertEqual(fails, [])

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
