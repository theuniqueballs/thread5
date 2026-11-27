"""ЗАКОНЫ АВТОРА 2026-11-26 — калибровка T5-32 принята (В45/В47).

Разбор автора: «Они не то чтобы были ложные, ошибка лишь в том, что комбо Y
оказалось недостаточно эротичным для такой одежды. Типа, дрессер не понимает,
что в любой позе, даже если она будет просто сидеть, топлесс с заклееными
сосками - уже будет R+. И наоборот, если девчонка будет даже в шортиках, но
фокус будет на её crotch где будет лишь намёк на camel toe - это уже будет R+».
Плюс: «батчи переделывать - хуйня идея... Снижаешь тиры того что увидел».

Гейты:
1. rating_implied() (specs/gates.json 1.22.0): tapeEvidence/crotchFocus —
   HARD R+ независимо от остального состава; bareClaim+pointRead — R+;
   bareLineRead («chest's bare line» как декор, P06-класс T5-32) больше НЕ
   даёт R+.
2. T5-29 ground truth В43 не сдвинулся: matched {P04,P11,P18,P27},
   17 ложных R+, 12 дрейфов (test_t529_lessons.py — дубль-страховка здесь).
3. Словари: rating-techniques 1.7.0 (hard_carriers + volt_run В45 + импорт «копай оракла» + ЗАКОН 3 покрытия-в-позе),
   dresser 1.10.0 (carrier_first + two_carrier В52/В53 + yuri_quota В49 + carrier_matrix + combo_book), gates.json 1.25.0
   (negBase += yellow skin/sallow skin, skinCast В48 — вердикт T5-33; yStamp eraGuard В52 + negCanonGuard В55 + voltRun В45 + themeEcho В54 — вердикт T5-34).
"""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

import gates  # noqa: E402


def _slot(num, pos, genre="VOLT"):
    """Слот-болванка для skinCast-тестов (реальный конструктор Slot)."""
    s = gates.Slot(num, "slug", "", "(VOLT · human · R+)")
    s.pos = pos
    s.genre = genre
    return s


class TestAuthorRatingLaws(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cfg = gates.GATES["ratingTruth"]

    def implied(self, pos):
        return gates.rating_implied(pos, self.cfg)

    def test_law1_tape_any_pose(self):
        """Закон 1: топлесс с заклееными сосками — R+ В ЛЮБОЙ ПОЗЕ (даже сидя)."""
        pos = ("anime style, original character, 1girl, solo, sitting on a stool, calm posture, "
               "topless with tape, taped nipples, jeans, hands in lap, warm light")
        self.assertEqual(self.implied(pos), "R+")

    def test_law2_crotch_focus_any_clothes(self):
        """Закон 2: шорты + фокус на crotch с намёком cameltoe — R+."""
        pos = ("anime style, original character, 1girl, solo, standing, shorts and tee, "
               "low camera, the lens on the crotch line, a faint cameltoe hint through the shorts, "
               "nothing else bare, daylight")
        self.assertEqual(self.implied(pos), "R+")

    def test_law2_pantyline_hard(self):
        """Закон 2-родственный: visible pantyline через обычную одежду — R+."""
        pos = ("anime style, original character, 1girl, solo, walking, skirt and blouse, "
               "visible pantyline reading through the skirt's cloth, street")
        self.assertEqual(self.implied(pos), "R+")

    def test_point_read_with_bare_claim(self):
        """P07-класс: bareClaim + бугорки читаются сквозь мокрый слой — R+."""
        pos = ("the soaked shirt committed to the skin, worn open at the front, "
               "nothing underneath the rain's verdict, two soft points reading against the wet weave")
        self.assertEqual(self.implied(pos), "R+")

    def test_bare_line_alone_is_not_rplus(self):
        """T5-32 P06-класс: «chest's bare line framed by the hem» — декор, R не R+."""
        pos = ("kneeling at the bench's edge, the apron worn open at the sides over the jersey, "
               "nothing underneath the apron's word but the cellar's cold, "
               "the chest's bare line framed by the hem's straight edge at the lean")
        self.assertEqual(self.implied(pos), "R")

    def test_pair_contact_is_carrier_v47(self):
        """В47: юри-пара — контакт-геометрия = носитель R+ (2girls + pairContact)."""
        pos = ("anime style, original character, 2girls, yuri, upper body, "
               "deep kiss at the bench's edge, both in open shirts worn loose off the shoulders")
        self.assertEqual(self.implied(pos), "R+")

    def test_pair_contact_requires_pair_tag(self):
        """pairContact-токен без 2girls/yuri не делает соло R+."""
        pos = ("anime style, original character, 1girl, solo, a deep kiss printed on a poster "
               "she hangs on the wall, casual clothes")
        self.assertNotEqual(self.implied(pos), "R+")

    def test_ethalon_ribbon_hold_still_rplus(self):
        """В44-эталон жив: bareClaim + handHold при панелях off — R+ (T5-31 P28)."""
        pos = ("bare underneath a single silk ribbon crossing her chest in a bow, "
               "her fingers gripping the ribbon's offered end, "
               "the shirt dress worn open off both shoulders, its panels off the claim, "
               "nothing underneath the ribbon's bow but the morning's jam")
        self.assertEqual(self.implied(pos), "R+")

    def test_honest_straps_still_rplus(self):
        """T5-29 P27-класс: честные стрэпы на голой груди — R+."""
        pos = ("nothing underneath the shirt, the suspenders' straps covering the chest, "
               "the glove coming off finger by finger")
        self.assertEqual(self.implied(pos), "R+")


class TestCalibrationRegistryPins(unittest.TestCase):
    """Реестры калибровки: версии и носитель-первый закон на месте."""

    def setUp(self):
        self.rt = json.loads((ROOT / "specs" / "rating-techniques.json").read_text(encoding="utf-8"))
        self.dr = json.loads((ROOT / "specs" / "dresser.json").read_text(encoding="utf-8"))
        self.gt = json.loads((ROOT / "specs" / "gates.json").read_text(encoding="utf-8"))

    def test_versions(self):
        self.assertEqual(self.rt["version"], "1.7.0")
        self.assertEqual(self.dr["version"], "1.10.0")
        self.assertEqual(self.gt["version"], "1.27.0")  # 1.27.0 — claimFact (тикет #5)

    def test_hard_carriers_present(self):
        hc = self.rt["sum_rules"]["hard_carriers"]
        self.assertIn("taped nipples", hc["law"])
        self.assertIn("cameltoe", hc["law"])
        self.assertIn("between-knees", hc["law"])

    def test_author_laws_recorded(self):
        laws = " ".join(self.rt["principle"]["laws_author"])
        self.assertIn("заклееными сосками", laws)
        self.assertIn("camel toe", laws)
        self.assertIn("разнообразия", laws)

    def test_dresser_carrier_first(self):
        cf = self.dr["y_stack"]["carrier_first"]
        self.assertIn("НОСИТЕЛЬ-ПЕРВЫЙ", cf["law"])
        self.assertIn("21 промах T5-32", cf["law"])
        self.assertIn("очги" if False else "очки у Doe", cf["pair_slots"])

    def test_base_taxonomy_import_count(self):
        """Импорт из базового таксонома эччи-оракла: 161 (1.4.0) → 166 (1.5.0,
        «копай оракла на приёмы… больше эротики в волт», вердикт T5-33)."""
        self.assertEqual(len(self.rt["techniques"]), 166)
        tags = " ".join(t["tag"] for t in self.rt["techniques"])
        for frag in ("shape telegraph", "weight contact-geometry",
                     "fanservice framing", "dead fabrics", "catalog-calm"):
            self.assertIn(frag, tags)

    def test_dresser_yuri_quota_v49(self):
        """В49: юри-квота — мейн ≤2, ОС/EXP по прямому заказу (вердикт T5-33)."""
        yq = self.dr["y_stack"]["yuri_quota"]
        self.assertIn("≤ 2", yq["law"])
        self.assertIn("по прямому заказу", yq["law"])
        self.assertIn("НЕ ВСЁ ЗАБИВАЙ ЮРИ СЛОТАМИ", yq["law"])

    def test_gates_yellow_guard_v48(self):
        """В48: против-жёлтые токены в NEG-базе всегда + гейт skinCast на месте."""
        for tok in ("yellow skin", "sallow skin"):
            self.assertIn(tok, self.gt["negBase"]["always"])
        sc = self.gt["skinCast"]
        self.assertEqual(sc["mode"], "WARN")
        self.assertEqual(sc["applyFrom"], 34)
        self.assertTrue(sc["warmSkin"] and sc["warmPalette"])

    def test_skin_cast_catches_warm_skin_x_warm_palette(self):
        """skinCast ловит совместность тёплая кожа × тёплая палитра (В48)."""
        slots = [_slot(1, "warm ivory skin, honey hair, "
                      "Dawn Amber palette, deep amber light")]
        warns = []
        caught = gates.check_skin_cast(slots, warns, batch_no=34)
        self.assertEqual(caught, 1)
        self.assertEqual(warns[0][1], "skin-cast")

    def test_skin_cast_silent_on_cool_skin(self):
        """Холодная кожа при тёплой палитре — правило сборки В48, без WARN."""
        slots = [_slot(2, "cool fair skin, pale porcelain, "
                      "Dawn Amber palette")]
        warns = []
        caught = gates.check_skin_cast(slots, warns, batch_no=34)
        self.assertEqual(caught, 0)

    def test_skin_cast_silent_on_amber_eyes_cool_palette(self):
        """«amber eyes» при холодной палитре не шумит: палитра ищется только
        в строке палитры POS."""
        slots = [_slot(3, "warm ivory skin, amber eyes, "
                      "Arctic White palette, pale blue snow")]
        warns = []
        caught = gates.check_skin_cast(slots, warns, batch_no=34)
        self.assertEqual(caught, 0)

    def test_gates_rating_truth_groups(self):
        rt = self.gt["ratingTruth"]
        for grp in ("tapeEvidence", "crotchFocus", "pointRead", "bareLineRead"):
            self.assertTrue(rt.get(grp), f"нет группы {grp}")
        self.assertIn("КАЛИБРОВКА T5-32 ПРИНЯТА", rt["law"])


class TestT529GroundTruthUnmoved(unittest.TestCase):
    """В43-эталон не сдвинулся новой калибровкой (страховка к
    test_t529_lessons.TestRatingTruthCalibration)."""

    def test_ethalon_slots(self):
        text, header, slots = gates.parse_batch(str(ROOT / "batches" / "T5-29.md"))
        cfg = gates.GATES["ratingTruth"]
        imp = {s.sid: gates.rating_implied(s.pos, cfg) for s in slots}
        self.assertEqual(imp["P04"], "R+")
        self.assertEqual(imp["P27"], "R+")
        self.assertEqual(imp["P11"], "R")
        self.assertEqual(imp["P18"], "R")
        matched = {s.sid for s in slots
                   if s.rating in ("R+", "R", "PG-13") and imp[s.sid] == s.rating}
        self.assertEqual(matched, {"P04", "P11", "P18", "P27"})


if __name__ == "__main__":
    unittest.main()
