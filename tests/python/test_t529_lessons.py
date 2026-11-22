#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Юнит-тесты УРОКА T5-29 (unittest, stdlib-only) — вердикт автора 2026-11-22:

«Несоответствие рейтингу присутствует. Делай отладку системы которая за это
отвечает. […] Но сделай так, чтобы ты никогда нахуй больше таких ошибок
не повторял.»

Пять страховок:

1. КАЛИБРОВКА ratingTruth (В43): модель состава на живом T5-29 обязана
   воспроизвести ground truth автора ТОЧНО — совпали только P04/P11/P18/P27,
   помечены остальные 29 (17 ложных R+ + 12 мягких дрейфов). Дрейф любого
   словаря gates.json ratingTruth роняет этот тест.

2. ЗУБЫ РЕАЛЬНО СТРЕЛЯЮТ (эра 30, задним числом не бьют): на слотах T5-29
   с batch_no=30 гейты урока обязаны выдать FAIL — voltCore (вольт 7/14,
   бег 14), raceCast v2.0 (кины 13 > 10), exquisiteMain (0), expHypothesis
   (9 клеток без H-XX), ratingTruth (17 ложных R+).

3. ЭРА ЧЕСТНА: batch_no=29 без --retro — ни одного вхождения урока
   (квитанция T5-29 заперта, история не переписывается).

4. NOXX: пакет ОС-канона выдан по приказу («Забираем в ОС, даём ей имя -
   Noxx. Выдашь ей пакет ос-канона.») — запись в oc-canon.json 2.14.0,
   реестры (Two of Swords / SEAM / Libra), PH-промпт автора VERBATIM,
   P32 в oc-candidates.json promoted.

5. ВЕРДИКТ: verdicts/T5-29.json — схема t5-verdict/1, уроки В39–В43,
   вербатим автора не потерян.

Прогон: python3 -m unittest discover -s tests/python -v
"""

import json
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO / "tools"))

import gates  # noqa: E402

T5_29 = REPO / "batches" / "T5-29.md"
ERA = 30  # FAIL-эра урока T5-29 (applyFrom/failFrom)

# ground truth автора, вербатим: «Не соответствуют рейтингу: почти все
# слоты, кроме: 4, 11, 18, 27»
RATING_MATCH = {"P04", "P11", "P18", "P27"}


def parse_t5_29():
    text, header, slots = gates.parse_batch(T5_29)
    return text, header, slots


class TestRatingTruthCalibration(unittest.TestCase):
    """В43: модель состава обязана воспроизводить глаз автора на T5-29."""

    @classmethod
    def setUpClass(cls):
        cfg = gates.GATES["ratingTruth"]
        cls.cfg = cfg
        _, _, cls.slots = parse_t5_29()
        cls.by_id = {s.sid: s for s in cls.slots}
        cls.implied = {
            s.sid: gates.rating_implied(s.pos, cfg) for s in cls.slots
        }

    def test_ground_truth_exact(self):
        """Совпали ТОЛЬКО P04/P11/P18/P27 — 33/33 калибровки."""
        matched = {
            sid for sid, s in self.by_id.items()
            if s.rating in ("R+", "R", "PG-13")
            and self.implied[sid] == s.rating
        }
        self.assertEqual(
            matched, RATING_MATCH,
            f"модель дрейфнула от ground truth автора: лишние "
            f"{sorted(matched - RATING_MATCH)}, потеряны "
            f"{sorted(RATING_MATCH - matched)} — словари ratingTruth в "
            f"gates.json калибровались на T5-29 (docs/POSTMORTEM-T5-29.md)")

    def test_false_rplus_seventeen(self):
        """17 ложных R+ бейджей: OS×3 + мейн R+×6 + EXP×8."""
        false_rplus = [
            sid for sid, s in self.by_id.items()
            if s.rating == "R+" and self.implied[sid] != "R+"
        ]
        self.assertEqual(len(false_rplus), 17, f"{false_rplus}")
        self.assertNotIn("P04", false_rplus)
        self.assertNotIn("P27", false_rplus)

    def test_soft_drift_twelve(self):
        """12 мягких дрейфов R↔PG-13 (10 R→PG-13 + 2 PG-13→R)."""
        drift = [
            (sid, self.by_id[sid].rating, self.implied[sid])
            for sid in self.by_id
            if (self.by_id[sid].rating == "R" and self.implied[sid] == "PG-13")
            or (self.by_id[sid].rating == "PG-13" and self.implied[sid] != "PG-13")
        ]
        self.assertEqual(len(drift), 12, f"{drift}")

    def test_reference_slots(self):
        """Эталоны урока: P04/P27 — состав R+, P11/P18 — состав R."""
        self.assertEqual(self.implied["P04"], "R+")
        self.assertEqual(self.implied["P27"], "R+")
        self.assertEqual(self.implied["P11"], "R")
        self.assertEqual(self.implied["P18"], "R")
        # панель ткани держит потолок R: дресс-мостик P05, биб P10,
        # органза P33, узел-футболка Noxx P32
        for sid in ("P05", "P10", "P32", "P33"):
            self.assertEqual(self.implied[sid], "R", f"{sid} должен нести R")
        # мейн-быт без R-токенов: P12/P13 — PG-13 при бейдже R
        for sid in ("P12", "P13"):
            self.assertEqual(self.implied[sid], "PG-13", f"{sid}")


class TestLessonGatesFire(unittest.TestCase):
    """Зубы урока реально стреляют на дефектах T5-29 (эра 30)."""

    @classmethod
    def setUpClass(cls):
        _, header, cls.slots = parse_t5_29()
        cls.header = header
        cls.oc_names = gates.load_oc_names()
        cls.statuses = gates.load_race_statuses()

    def test_volt_core_fails(self):
        warns, fails = [], []
        stats = gates.check_volt_core(
            self.slots, warns, fails, batch_no=ERA, oc_names=self.oc_names)
        self.assertTrue(fails, "voltCore обязан FAIL на 7/14 с бегом 14")
        self.assertEqual(stats["volt"], 7)
        self.assertEqual(stats["niche"], 14)
        self.assertEqual(stats["max_run"], 14)
        self.assertIn("ВОЛЬТ-ЯДРО", fails[0][2])

    def test_race_cast_v2_fails(self):
        warns, fails = [], []
        stats = gates.check_race_cast(
            self.header, self.slots, self.statuses, warns, fails,
            batch_no=ERA, oc_names=self.oc_names)
        self.assertTrue(fails, "raceCast v2.0 обязан FAIL на 13 кинах")
        self.assertEqual(stats["kin"], 13)
        self.assertEqual(stats["human"], 8)
        self.assertIn("В40", fails[0][2])

    def test_exquisite_main_fails(self):
        warns, fails = [], []
        stats = gates.check_exquisite_main(
            self.slots, warns, fails, batch_no=ERA, oc_names=self.oc_names)
        self.assertTrue(fails, "exquisiteMain обязан FAIL на нуле EXQUISITE")
        self.assertEqual(stats["exquisite"], 0)

    def test_exp_hypothesis_fails(self):
        warns, fails = [], []
        stats = gates.check_exp_hypothesis(
            self.slots, warns, fails, batch_no=ERA)
        self.assertEqual(len(fails), 9, "все 9 клеток T5-29 без H-XX")
        self.assertEqual(stats["cells"], 9)
        self.assertEqual(stats["with_h"], 0)

    def test_rating_truth_fails(self):
        warns, fails = [], []
        stats = gates.check_rating_truth(self.slots, warns, fails, batch_no=ERA)
        self.assertEqual(len(fails), 17, "17 ложных R+ = FAIL")
        self.assertEqual(stats["false_rplus"], 17)
        self.assertEqual(stats["soft_drift"], 12)
        self.assertEqual(stats["implied_rplus"], 2)


class TestEraHonesty(unittest.TestCase):
    """Эра applyFrom 30: T5-29 задним числом не бьётся (квитанция заперта)."""

    def test_batch_29_silent(self):
        _, _, slots = parse_t5_29()
        oc_names = gates.load_oc_names()
        for check, args in (
            (gates.check_volt_core, (slots, [], [], 29, oc_names, False)),
            (gates.check_exquisite_main, (slots, [], [], 29, oc_names, False)),
            (gates.check_exp_hypothesis, (slots, [], [], 29, False)),
            (gates.check_rating_truth, (slots, [], [], 29, False)),
        ):
            warns, fails = [], []
            args = list(args)
            args[1], args[2] = warns, fails
            check(*args)
            self.assertEqual((warns, fails), ([], []),
                             f"{check.__name__} молчал в эре < 30")

    def test_retro_shows_warns_not_fails(self):
        """--retro на T5-29: урок виден WARN-ами, история не переписывается."""
        _, _, slots = parse_t5_29()
        warns, fails = [], []
        gates.check_rating_truth(slots, warns, fails, batch_no=29, retro=True)
        self.assertEqual(len(warns), 29, "29 WARN-ов ground truth в retro")
        self.assertEqual(fails, [])


class TestNoxxCanon(unittest.TestCase):
    """Noxx: пакет ОС-канона по прямому приказу (T5-29 P32 → canon 2.14.0)."""

    @classmethod
    def setUpClass(cls):
        cls.canon = json.loads(
            (REPO / "specs" / "oc-canon.json").read_text(encoding="utf-8"))
        cls.candidates = json.loads(
            (REPO / "specs" / "oc-candidates.json").read_text(encoding="utf-8"))

    def test_noxx_entry(self):
        noxx = self.canon["ocs"].get("Noxx")
        self.assertIsNotNone(noxx, "Noxx обязана быть в oc-canon.json")
        self.assertTrue(noxx.get("active"))
        self.assertEqual(noxx["id"], "noxx")
        self.assertTrue(noxx["body_type"].startswith("BT-12"))

    def test_registries(self):
        self.assertIn("Noxx — Two of Swords", self.canon["registries"]["tarot"])
        self.assertIn("Noxx — SEAM", self.canon["registries"]["element"])
        self.assertIn("Noxx — Libra", self.canon["registries"]["zodiac"])

    def test_ph_prompt_verbatim(self):
        """PH-промпт автора сохранён дословно — канон-лок Noxx."""
        ph = self.canon["ocs"]["Noxx"]["ph_prompt_verbatim"]
        for fragment in (
            "depth-black hair in a ghost-layer shag",
            "black skin with soft star-glow flecks",
            "nothing underneath the negotiation but the light she argued in",
            "the negotiated light is the claim, diplomacy-made",
            "Dusk Binding palette, dusk-bind-violet over corridor-stone",
        ):
            self.assertIn(fragment, ph, f"вербатим потерян: {fragment!r}")

    def test_birth_cites_verdict(self):
        birth = self.canon["ocs"]["Noxx"]["birth"]
        self.assertIn("T5-29 P32", birth)
        self.assertIn("Noxx", birth)

    def test_candidate_promoted(self):
        p32 = [c for c in self.candidates["candidates"] if c["slot"] == "P32"]
        self.assertEqual(len(p32), 1)
        self.assertEqual(p32[0]["status"], "promoted")
        self.assertIn("Noxx", p32[0].get("promoted_to", ""))
        self.assertEqual(self.candidates["stats"]["promoted"], 1)

    def test_oracle_sees_noxx(self):
        """Окно/жребий знают новую ОС: load_oc_names отдаёт 30 имён."""
        names = gates.load_oc_names()
        self.assertIn("Noxx", names)


class TestVerdictT529(unittest.TestCase):
    """Вердикт T5-29: схема, уроки, вербатим без потерь."""

    @classmethod
    def setUpClass(cls):
        cls.v = json.loads(
            (REPO / "verdicts" / "T5-29.json").read_text(encoding="utf-8"))

    def test_schema(self):
        self.assertEqual(self.v["schema"], "t5-verdict/1")
        self.assertEqual(self.v["batch"], "T5-29")
        self.assertEqual(self.v["overall"]["score"], "below average")

    def test_lessons_v39_v43(self):
        ids = {l["id"] for l in self.v["lessons"]}
        self.assertEqual(ids, {"В39", "В40", "В41", "В42", "В43"})
        for l in self.v["lessons"]:
            self.assertTrue(l["machine"].startswith("gates.json"),
                            f"{l['id']}: машинная ссылка обязана вести в гейты")

    def test_verbatim_preserved(self):
        full = self.v["verbatim_full"]
        for fragment in (
            "Какой перевес в Niche, если основная масса должна быть - волт",
            "почему у нас везде кины, если кины - опция, а не основа",
            "почему волт и ниша идут подряд, хотя должно быть вперемешку",
            "где Exquisite в основной теме",
            "Почему EXP слоты следуют теме, если они должны проверять штуки",
            "почти все слоты, кроме: 4, 11, 18, 27",
            "Забираем в ОС, даём ей имя - Noxx",
            "Но сделай так, чтобы ты никогда нахуй больше таких ошибок не повторял",
        ):
            self.assertIn(fragment, full, f"вербатим потерян: {fragment!r}")

    def test_noxx_promotion_logged(self):
        loved = self.v["loved"]
        self.assertEqual(loved[0]["slot"], "P32")
        self.assertIn("Noxx", loved[0]["note"])


if __name__ == "__main__":
    unittest.main()
