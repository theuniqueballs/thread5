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
            self.assertIn(c.get("class"),
                          ("hard", "see", "body", "wet", "edge", "lingerie"))
            self.assertIn(c.get("zone"), ("chest", "bottom"))

    def test_wet_is_support_class(self):
        """Урок золотого ролла TB-20261122-777 P16: мокрая непрозрачная
        ткань — support-класс (вторым+), сама не несёт тело/прикрытие:
        пара «wet clothes + lingerie» в одиночку не поднимает R+ (В60:
        мокрая ткань без просвета/голой кожи = R-этаж, T5-35 P13)."""
        wet = [c for c in self.cfg["carriers"] if c["class"] == "wet"]
        self.assertEqual({c["token"] for c in wet},
                         {"wet clothes", "wet shirt", "wet body"})

    def test_edge_is_support_class(self):
        """Урок золотого ролла TB-20261122-999 P11: граничные токены без
        состояния груди (bare shoulders/back, through shirt/clothes) —
        support-класс (вторым+): bare shoulders + lingerie ≠ R+."""
        edge = [c for c in self.cfg["carriers"] if c["class"] == "edge"]
        self.assertEqual({c["token"] for c in edge},
                         {"bare shoulder", "bare back",
                          "through shirt", "through clothes"})

    def test_edge_with_lingerie_only_fails(self):
        """Ролл-999-P11-класс: bare shoulders + lingerie + panties — не R+.
        (ИИН в тексте нет — «the linen pinafore dress» держит панель.)"""
        s = _slot(7, "1girl, solo, bare shoulders above, nothing "
                     "underneath, lingerie; panties — the linen pinafore "
                     "dress buttoned over the chest")
        stats, warns, fails = self.run_gate([s])
        self.assertEqual(stats["thin"], ["P07"])

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

    def test_wet_with_lingerie_only_fails(self):
        """Урок ролла TB-20261122-777 P16: wet clothes + lingerie + panties
        в одиночку — НЕ R+ (класс wet не несёт тело/прикрытия)."""
        s = _slot(7, "1girl, solo, wet clothes under the coat, lingerie set "
                     "with garter belt, the panties' line at the cut")
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


class TestRatingImpliedCarrierBranch(unittest.TestCase):
    """В43-согласованность (1.30.0): rating_implied признаёт В61-носители.

    Машина В43 по приватным словарям звала пересобранные слоты «ложным
    R+ бейджем» (панель ткани), пока nudeTruth/carrierTruth пропускали
    их же по В57/В61 — два гейта противоречили друг другу. Ветка
    аддитивная: приватные списки В43 не тронуты (калибровка T5-29 33/33
    заперта), на старых слотах ветка молчит."""

    def setUp(self):
        self.cfg = gates.GATES["ratingTruth"]

    def test_carrier_pair_implies_rplus(self):
        """P01-паттерн: bare breasts + covered nipples — implied R+."""
        implied = gates.rating_implied(
            "1girl, solo, silk ribbon crossing bare breasts in a bow, "
            "covered nipples, the knot held between her lips",
            self.cfg,
        )
        self.assertEqual(implied, "R+")

    def test_wet_channel_implies_rplus(self):
        """Мокрый канал: no bra + wet clothes + see-through — implied R+."""
        implied = gates.rating_implied(
            "1girl, solo, no bra under the soaked silk slip, wet clothes "
            "gone see-through across the chest, clothed nipples reading "
            "through ruined silk",
            self.cfg,
        )
        self.assertEqual(implied, "R+")

    def test_single_carrier_does_not_imply_rplus(self):
        """Один носитель — ветка молчит (модель В43 судит как раньше)."""
        implied = gates.rating_implied(
            "1girl, solo, the wet shirt clinging, everything else dry",
            self.cfg,
        )
        self.assertNotEqual(implied, "R+")

    def test_lingerie_only_does_not_imply_rplus(self):
        """Бельё-импакт в одиночку — не R+ (В60: от голого тела)."""
        implied = gates.rating_implied(
            "1girl, solo, lingerie set with garter belt under the coat, "
            "everything buttoned",
            self.cfg,
        )
        self.assertNotEqual(implied, "R+")

    def test_wet_with_lingerie_does_not_imply_rplus(self):
        """Урок ролла TB-20261122-777 P16: wet clothes + lingerie + panties
        — не R+ (мокрая непрозрачная ткань = R-этаж, В60)."""
        implied = gates.rating_implied(
            "1girl, solo, wet clothes under the coat, lingerie set with "
            "garter belt, the panties' line at the cut",
            self.cfg,
        )
        self.assertNotEqual(implied, "R+")

    def test_edge_with_lingerie_does_not_imply_rplus(self):
        """Урок ролла TB-20261122-999 P11: bare shoulders + lingerie —
        не R+ (граничные токены не несут состояния груди)."""
        implied = gates.rating_implied(
            "1girl, solo, bare shoulders above, nothing underneath, "
            "lingerie; panties — the linen pinafore dress buttoned over "
            "the chest",
            self.cfg,
        )
        self.assertNotEqual(implied, "R+")

    def test_t535_retro_unaffected(self):
        """Калибровка заперта: В61-ветка аддитивна — на T5-35 ни один
        R/PG-13 слот не поднят до R+ (ложная инфляция исключена), а все
        R+ слоты модель согласует с бейджем (как и при В43 — бумага
        всегда соглашалась с бейджем, урок «гейты меряют бумагу")."""
        _, _, slots = gates.parse_batch(ROOT / "batches" / "T5-35.md")
        for s in slots:
            if s.rating not in ("R", "PG-13"):
                continue
            implied = gates.rating_implied(s.pos, self.cfg)
            self.assertNotEqual(
                implied, "R+",
                f"{s.sid} ({s.rating}): В61-ветка подняла слот — ложная "
                "инфляция, пересчитай пин")


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
