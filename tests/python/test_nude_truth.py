"""Юнит-тесты гейта nudeTruth (gates.json 1.29.0) — В57/В58, вердикт T5-35.

Разбор автора 2026-11-28 (послотовый вердикт 30/30): fact-hit R+ 1 чистый +
1 грань из 17 — «всё обучение по эччи почему-то не особо сработало». Корень:
ню-состояние всех R+ слотов написано поэтическим отрицанием «nothing
underneath X but Y» — рендерер Tsubaki.2 Pro читает literal-токены и молчит
на прозе; P01 доехал геометрией ленты и всё равно дрейфовал одеждой (приказ:
«уточняй, что она под лентами — голая», «не стесняйся — мы в рамках эччи»).

В57: R+ обязан нести ню-состояние literal-токеном (nude/naked/topless/bare
chest/bare underneath/covered only by), hard-якорем автора (tapeEvidence —
Закон 1, crotchFocus — Закон 2, handbra-холд) или wet-sheer-на-коже (P06).
В58: bare-зона POS не глушится bare-зоной той же группы в NEG (P08:
«bare thigh-strip» × «bare legs»).

Эра: applyFrom 37, failFrom 37 — T5-36 (контрольная, сдана до вердикта)
не бьётся; T5-37+ FAIL. Ретро-калибровка T5-35: 17 no-state (P06/P14/P17
проходят: wet-sheer / crotchFocus-якорь / «only cover»), poetic_only 17,
коллизий 1 (P08).
"""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

import gates  # noqa: E402


def _slot(num, pos, neg="", genre="VOLT", rating="R+"):
    """Слот-болванка (реальный конструктор Slot: sid, slug, paren, header)."""
    s = gates.Slot(f"{num:02d}", "slug",
                   f"({genre} · human · {rating} · test)", "")
    s.pos = pos
    s.pos_lines = pos.splitlines() or [pos]
    s.neg = neg
    s.neg_lines = neg.splitlines() or [neg]
    assert s.rating == rating, s.rating
    return s


class TestNudeTruthGate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cfg = gates.GATES["nudeTruth"]

    def run_gate(self, slots, batch_no=37, retro=False):
        warns, fails = [], []
        stats = gates.check_nude_truth(slots, warns, fails, batch_no, (), retro)
        return stats, warns, fails

    def test_spec_pin(self):
        self.assertEqual(gates.GATES.get("version"), "1.29.0")
        self.assertEqual(self.cfg["applyFrom"], 37)
        self.assertEqual(self.cfg["failFrom"], 37)

    # ── В57: живые ню-слои ────────────────────────────────────────────

    def test_direct_token_passes(self):
        """Прямой токен «nude underneath» проходит."""
        s = _slot(1, "1girl, solo, nude underneath the single silk ribbon "
                     "crossing her chest, the knot pinned by her lips")
        stats, warns, fails = self.run_gate([s])
        self.assertEqual(stats["no_nude_state"], [])
        self.assertEqual(fails, [])

    def test_topless_tape_passes(self):
        """Закон 1 автора: топлесс + тейп — hard-якорь, проходит в любой позе."""
        s = _slot(2, "1girl, solo, sitting calm, topless with tape, taped "
                     "nipples, jeans, hands in lap")
        stats, warns, fails = self.run_gate([s])
        self.assertEqual(stats["no_nude_state"], [])

    def test_crotch_focus_passes(self):
        """Закон 2 автора: crotch-фокус с намёком cameltoe — hard-якорь."""
        s = _slot(3, "1girl, solo, shorts and tee, camera between her knees "
                     "into the crotch line, a faint cameltoe hint")
        stats, warns, fails = self.run_gate([s])
        self.assertEqual(stats["no_nude_state"], [])

    def test_wet_sheer_on_skin_passes(self):
        """P06-класс: мокрый sheer, ткань запечатана на голой коже."""
        s = _slot(4, "1girl, solo, leaning over the table, the soaked cloth "
                     "sealed to the breast's underside where the tea ran")
        stats, warns, fails = self.run_gate([s])
        self.assertEqual(stats["no_nude_state"], [])

    def test_handbra_hold_passes(self):
        """handbra-холд (В43 семья) — проходит."""
        s = _slot(5, "1girl, solo, both fists hauling the towel back flat "
                     "against the chest, the only cover in the frame")
        stats, warns, fails = self.run_gate([s])
        self.assertEqual(stats["no_nude_state"], [])

    # ── В57: мёртвые носители ─────────────────────────────────────────

    def test_poetic_negation_fails(self):
        """«nothing underneath X but Y» — НЕ ню-состояние: FAIL в T5-37+."""
        s = _slot(6, "1girl, solo, breast shape held under a single silk "
                     "ribbon, nothing underneath the sheer ribbon but the "
                     "library's hush, soft crests reading through")
        stats, warns, fails = self.run_gate([s])
        self.assertEqual(stats["no_nude_state"], ["P06"])
        self.assertEqual(stats["poetic_only"], 1)
        self.assertEqual(len(fails), 1)
        self.assertEqual(fails[0][1], "nude-truth")

    def test_opaque_print_fails(self):
        """Печать по плотной ткани (риб-трикотаж P04-класс) — FAIL."""
        s = _slot(7, "1girl, solo, breast shape printing through the rain-wet "
                     "ribbed knit in bands, nothing underneath the wet knit "
                     "but the laundromat's steam")
        stats, warns, fails = self.run_gate([s])
        self.assertEqual(stats["no_nude_state"], ["P07"])

    def test_only_cover_short_token_passes(self):
        """«only cover» без «in the frame» — тоже hard-якорь холда."""
        s = _slot(8, "1girl, solo, arms crossed over her chest, the towel "
                     "the only cover, steam everywhere")
        stats, warns, fails = self.run_gate([s])
        self.assertEqual(stats["no_nude_state"], [])

    # ── В58: коллизия POS/NEG ─────────────────────────────────────────

    def test_collision_p08_class(self):
        """P08-класс: «bare thigh-strip» в POS против «bare legs» в NEG.

        Прямой ню-токен добавлен, чтобы ловился ТОЛЬКО В58 (изолированно)."""
        s = _slot(
            8,
            "nude underneath the knit top, zettai ryouiki band, the bare "
            "thigh-strip between stocking and skirt carrying the garter's dent",
            "young girl, loli, signature, watermark, areola, pink nipples, "
            "bare legs",
        )
        stats, warns, fails = self.run_gate([s])
        self.assertEqual(stats["no_nude_state"], [])
        self.assertEqual(stats["collisions"], 1)
        self.assertEqual(len(fails), 1)

    def test_x_guards_do_not_collide(self):
        """X-гварды NEG (areola/nipples) без bare-слов — коллизии нет."""
        s = _slot(
            9,
            "nude underneath the sheer gown, bare chest visible in the "
            "candlelight",
            "young girl, loli, signature, watermark, areola, pink nipples",
        )
        stats, warns, fails = self.run_gate([s])
        self.assertEqual(stats["collisions"], 0)
        self.assertEqual(fails, [])

    def test_collision_fails_in_hard_era(self):
        stats, warns, fails = self.run_gate(
            [_slot(
                10,
                "nude underneath the slip, the bare thigh-strip between "
                "stocking and skirt",
                "areola, pink nipples, bare legs",
            )],
            batch_no=37,
        )
        self.assertEqual(len(fails), 1)
        self.assertIn("В58", fails[0][2])

    # ── эры и ретро ───────────────────────────────────────────────────

    def test_silent_before_apply_from(self):
        """T5-36 (контрольная, сдана до вердикта) — гейт молчит."""
        s = _slot(11, "nothing underneath the ribbon but the hush")
        stats, warns, fails = self.run_gate([s], batch_no=36)
        self.assertEqual(stats, {"mode": "silent"})
        self.assertEqual(warns, [])
        self.assertEqual(fails, [])

    def test_retro_shows_warns_not_fails(self):
        """--retro на T5-35: урок виден WARN-ами, история не переписывается."""
        s = _slot(12, "nothing underneath the sheer slip but held air")
        stats, warns, fails = self.run_gate([s], batch_no=35, retro=True)
        self.assertEqual(len(warns), 1)
        self.assertEqual(fails, [])

    def test_non_rplus_untouched(self):
        """R и PG-13 слоты гейтом не бьются (этаж В43 — их машина)."""
        r_slot = gates.Slot(13, "slug", "", "(VOLT · human · R)")
        r_slot.pos = "nothing underneath the hem but honest weave"
        r_slot.rating = "R"
        pg_slot = gates.Slot(14, "slug", "", "(NICHE · human · PG-13)")
        pg_slot.pos = "everything covered, the geometry counting the border"
        pg_slot.rating = "PG-13"
        stats, warns, fails = self.run_gate([r_slot, pg_slot])
        self.assertEqual(stats["rplus_slots"], 0)
        self.assertEqual(fails, [])


class TestNudeTruthCalibration(unittest.TestCase):
    """Ретро-калибровка на живом T5-35 (ground truth автора 30/30)."""

    @classmethod
    def setUpClass(cls):
        sys.path.insert(0, str(ROOT / "tools"))
        _, _, cls.slots = gates.parse_batch(
            ROOT / "batches" / "T5-35.md")

    def test_t535_caught(self):
        warns, fails = [], []
        stats = gates.check_nude_truth(
            self.slots, warns, fails, batch_no=35, retro=True)
        # 20 R+ слотов: 17 без literal-ню (P06/P14/P17 проходят: wet-sheer /
        # crotchFocus-якорь / «only cover»), 17 poetic_only, 1 коллизия (P08)
        self.assertEqual(stats["rplus_slots"], 20)
        self.assertEqual(stats["passing"], 3)
        self.assertEqual(len(stats["no_nude_state"]), 17)
        self.assertEqual(stats["poetic_only"], 17)
        self.assertEqual(stats["collisions"], 1)
        self.assertIn("P01", stats["no_nude_state"])
        self.assertIn("P08", stats["no_nude_state"])
        self.assertEqual(len(warns), 18, "17 ню-флагов + 1 коллизия в retro")
        self.assertEqual(fails, [])

    def test_passing_slots(self):
        warns, fails = [], []
        stats = gates.check_nude_truth(
            self.slots, warns, fails, batch_no=35, retro=True)
        flagged = set(stats["no_nude_state"])
        self.assertNotIn("P06", flagged, "мокрый sheer на коже — живой слой")
        self.assertNotIn("P14", flagged, "camera-between-knees — hard-якорь")
        self.assertNotIn("P17", flagged, "полотенце-холд «only cover» — живой")

    def test_t536_silent_live(self):
        """T5-36 в живом прогоне (не retro) молчит: applyFrom 37."""
        _, _, slots36 = gates.parse_batch(ROOT / "batches" / "T5-36.md")
        warns, fails = [], []
        stats = gates.check_nude_truth(slots36, warns, fails, batch_no=36)
        self.assertEqual(stats, {"mode": "silent"})
        self.assertEqual(warns, [])
        self.assertEqual(fails, [])


if __name__ == "__main__":
    unittest.main()
