"""Юнит-тесты гейта carrierTruth (gates.json 1.30.0) — В61 DANBOORU-FIRST
CARRIER LAW, тикет #7 (остаток) + приказ автора «редактировать Т5-36,
чтобы она точно соответствовала рейтингу».

Диагноз аудита #7 (матрица словарей по всем 30 POS T5-35): фраз-носителей
МАШИНЫ 7.80 на R+ слот, данбоору-токенов РЕНДЕРЕРА 0.05 — 19/20 R+ слотов
без единого носителя, который рендерер умеет рисовать. Гейты подтверждали
поэзию писца против словаря писца — самоссылка.

В61: каждый R+ слот несёт ≥2 РАЗЛИЧНЫХ каноничных данбоору-носителя
(≥1 класса тела/прикрытия hard/see/body; бельё-импакт только вторым+);
носитель в NEG своего слота мёртв (В58-класс); приватный диалект
(«breast shape», «soft crests», «reading through», «imprint») носителем
не считается. Канон-решение автора по просвету: see-through = R+ носитель.

Эра: applyFrom 36, failFrom 36 — T5-36 пересобрана danbooru-first приказом
автора (контроль отменён), FAIL сразу. Ретро T5-35: 20/20 R+ тонкие
(единичные данбоору-токены P13 wet shirt / P14 camera-between / P05 bare
shoulders не дотягивают до ≥2) — партия на мёртвом диалекте, история не
переписывается.
"""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

import gates  # noqa: E402


def _slot(num, pos, neg="", genre="VOLT", rating="R+"):
    s = gates.Slot(f"{num:02d}", "slug",
                   f"({genre} · human · {rating} · test)", "")
    s.pos = pos
    s.pos_lines = pos.splitlines() or [pos]
    s.neg = neg
    s.neg_lines = neg.splitlines() or [neg]
    assert s.rating == rating, s.rating
    return s


class TestCarrierTruthGate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cfg = gates.GATES["carrierTruth"]
        cls.tokens = [c["token"] for c in cls.cfg["carriers"]]

    def run_gate(self, slots, batch_no=36, retro=False):
        warns, fails = [], []
        stats = gates.check_carrier_truth(slots, warns, fails, batch_no, retro)
        return stats, warns, fails

    def test_spec_pin(self):
        self.assertEqual(gates.GATES.get("version"), "1.30.0")
        self.assertEqual(self.cfg["applyFrom"], 36)
        self.assertEqual(self.cfg["failFrom"], 36)
        self.assertEqual(self.cfg["minCarriers"], 2)
        # словарь — рендер-улика у каждого токена (приёмка тикета #7)
        for c in self.cfg["carriers"]:
            self.assertTrue(c.get("evidence"),
                            f"токен «{c.get('token')}» без рендер-улики")
            self.assertIn(c.get("class"), ("hard", "see", "body", "lingerie"))
            self.assertIn(c.get("zone"), ("chest", "bottom"))

    def test_carrier_dictionary_covers_ticket7(self):
        """Приёмка #7: весь R+ словарь живёт токенами рендерера."""
        for tok in ("see-through", "wet clothes", "underboob", "sideboob",
                    "no bra", "handbra", "cameltoe", "visible pantyline",
                    "covered nipples", "clothed nipples", "pasties",
                    "nipple tape"):
            self.assertIn(tok, self.tokens,
                          f"«{tok}» нет в словаре carrierTruth (приёмка #7)")

    def test_see_through_canon_is_rplus(self):
        """Канон-решение автора: see-through = R+ носитель (see-класс)."""
        c = next(c for c in self.cfg["carriers"] if c["token"] == "see-through")
        self.assertEqual(c["class"], "see")
        self.assertIn("КАНОН-РЕШЕНИЕ АВТОРА", c["evidence"])

    # ── живые слои ────────────────────────────────────────────────────

    def test_nude_first_pair_passes(self):
        """P01-паттерн: bare breasts + covered nipples — тело + прикрытие."""
        s = _slot(1, "1girl, solo, silk ribbon crossing bare breasts in a "
                     "bow, covered nipples, the knot held between her lips")
        stats, warns, fails = self.run_gate([s])
        self.assertEqual(stats["thin"], [])
        self.assertEqual(fails, [])

    def test_see_through_pair_passes(self):
        """canon-просвет: no bra + see-through (тело + просвет)."""
        s = _slot(2, "1girl, solo, no bra under the sheer gown, the gown "
                     "gone see-through at the chest where the lamp backs it")
        stats, warns, fails = self.run_gate([s])
        self.assertEqual(stats["thin"], [])

    def test_wet_channel_passes(self):
        """Мокрый канал: wet clothes + see-through + clothed nipples."""
        s = _slot(3, "1girl, solo, wet clothes gone see-through at the "
                     "chest, clothed nipples reading through the soaked "
                     "weave")
        stats, warns, fails = self.run_gate([s])
        self.assertEqual(stats["thin"], [])

    def test_hard_anchor_pair_passes(self):
        """Закон 2: cameltoe + crotch-фрейминг — пара hard-носителей."""
        s = _slot(4, "1girl, solo, the camera between her knees into the "
                     "crotch line, a faint cameltoe hint at the skintight "
                     "seam")
        stats, warns, fails = self.run_gate([s])
        self.assertEqual(stats["thin"], [])

    # ── мёртвые слои ──────────────────────────────────────────────────

    def test_private_dialect_alone_fails(self):
        """Приватный диалект — НЕ носитель: «breast shape» + «soft crests»
        без данбоору-токенов = FAIL в T5-36+ (диалект отмечен)."""
        s = _slot(5, "1girl, solo, breast shape honest under the ribbed "
                     "count, two soft crests reading through the weave, "
                     "nothing underneath the tank but the wait")
        stats, warns, fails = self.run_gate([s])
        self.assertEqual(stats["thin"], ["P05"])
        self.assertEqual(stats["dialect_only"], 1)
        self.assertEqual(len(fails), 1)
        self.assertEqual(fails[0][1], "carrier-truth")

    def test_single_carrier_fails(self):
        """Один носитель < minCarriers — FAIL (пара мёртвых = мёртвый слот)."""
        s = _slot(6, "1girl, solo, the wet shirt clinging, everything else "
                     "dry and honest, breast shape given to the lean")
        stats, warns, fails = self.run_gate([s])
        self.assertEqual(stats["thin"], ["P06"])

    def test_lingerie_only_fails(self):
        """Бельё-импакт в одиночку не несёт R+ (В60: от голого тела):
        lingerie + garter belt без тела/прикрытия = FAIL."""
        s = _slot(7, "1girl, solo, lingerie set with garter belt and "
                     "garter straps under the coat, everything buttoned")
        stats, warns, fails = self.run_gate([s])
        self.assertEqual(stats["thin"], ["P07"])

    def test_lingerie_as_second_carrier_passes(self):
        """Бельё-импакт ВТОРЫМ носителем — легален (см. P27/P28)."""
        s = _slot(8, "1girl, solo, no bra under the sheer organza gone "
                     "see-through at the lean, satin panties named in the "
                     "frame")
        stats, warns, fails = self.run_gate([s])
        self.assertEqual(stats["thin"], [])

    def test_carrier_killed_by_own_neg(self):
        """В58-класс: носитель в NEG своего слота — мёртв, слот тонкий."""
        s = _slot(
            9,
            "no bra under the sheer gown, the gown gone see-through at "
            "the chest",
            "young girl, loli, signature, watermark, areola, pink nipples, "
            "see-through, no bra",
        )
        stats, warns, fails = self.run_gate([s])
        self.assertEqual(stats["thin"], ["P09"])
        self.assertEqual(stats["neg_killed"], 2)
        self.assertIn("NEG", fails[0][2])

    def test_non_rplus_untouched(self):
        """R и PG-13 слоты гейтом не бьются (их этаж — В43/В60)."""
        r_slot = gates.Slot(10, "slug", "", "(VOLT · human · R)")
        r_slot.pos = "breast shape printing through thin cotton"
        r_slot.rating = "R"
        pg_slot = gates.Slot(11, "slug", "", "(NICHE · human · PG-13)")
        pg_slot.pos = "everything covered, midriff honest"
        pg_slot.rating = "PG-13"
        stats, warns, fails = self.run_gate([r_slot, pg_slot])
        self.assertEqual(stats["rplus_slots"], 0)
        self.assertEqual(fails, [])

    # ── эры и ретро ───────────────────────────────────────────────────

    def test_silent_before_apply_from(self):
        """T5-35 и старше в живом прогоне — гейт молчит (эра 36)."""
        s = _slot(12, "breast shape honest, nothing underneath the ribbon")
        stats, warns, fails = self.run_gate([s], batch_no=35)
        self.assertEqual(stats, {"mode": "silent"})
        self.assertEqual(warns, [])
        self.assertEqual(fails, [])

    def test_retro_shows_warns_not_fails(self):
        """--retro на T5-35: урок виден WARN-ами, история не переписывается."""
        s = _slot(13, "breast shape honest, nothing underneath the slip")
        stats, warns, fails = self.run_gate([s], batch_no=35, retro=True)
        self.assertEqual(stats["mode"], "RETRO-WARN")
        self.assertEqual(len(warns), 1)
        self.assertEqual(fails, [])


class TestCarrierTruthCalibration(unittest.TestCase):
    """Ретро-калибровка на живом T5-35 (матрица аудита #7)."""

    @classmethod
    def setUpClass(cls):
        _, _, cls.slots = gates.parse_batch(
            ROOT / "batches" / "T5-35.md")

    def test_t535_all_thin(self):
        """T5-35 на мёртвом диалекте: 20/20 R+ тонкие, диалект везде."""
        warns, fails = [], []
        stats = gates.check_carrier_truth(
            self.slots, warns, fails, batch_no=35, retro=True)
        self.assertEqual(stats["rplus_slots"], 20)
        self.assertEqual(stats["passing"], 0)
        self.assertEqual(len(stats["thin"]), 20)
        self.assertEqual(stats["dialect_only"], 20)
        self.assertEqual(stats["neg_killed"], 0)
        self.assertEqual(len(warns), 20)
        self.assertEqual(fails, [])

    def test_t535_single_tokens_not_enough(self):
        """Единственные данбоору-токены батча (P13 wet shirt и др.) не
        дотягивают до ≥2 — матрица «19/20 без носителя» подтверждена
        словарём В61 (3 слота с ровно одним токеном — тоже тонкие)."""
        warns, fails = [], []
        stats = gates.check_carrier_truth(
            self.slots, warns, fails, batch_no=35, retro=True)
        self.assertIn("P13", stats["thin"], "wet shirt в одиночку — тонко")
        cfg = gates.GATES["carrierTruth"]
        for s in self.slots:
            if s.rating != "R+":
                continue
            found = [c["token"] for c in cfg["carriers"]
                     if c["token"] in (s.pos or "").lower()]
            self.assertLess(len(found), 2,
                            f"{s.sid}: нашлось ≥2 носителя — калибровка "
                            "«20/20 тонкие» протухла, пересчитай пин")


if __name__ == "__main__":
    unittest.main()
