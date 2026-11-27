"""В51 ratingMass — R+-масса мейнов (вердикт T5-34, «ты нигде рейтингом
не попал»; закон 2026-11-27).

1. КАНОН: R+-заявок в мейнах ≥ 14, PG-13 в мейнах = 0 (спред Закона 24
   / В39: R+×14 · R×7). voltCore меряет ЖАНРОВЫЕ метки (VOLT+EXQUISITE) и
   спред-дрейф не видит: T5-34 собрал «вольт-ядро 13» из R-слотов с жанром
   VOLT при R+×11 · PG-13×3 — худший батч конвейера по рейтингу.
2. ЭРА: applyFrom/failFrom 35 — FAIL без WARN-эры (класс оплачен дважды:
   В39 T5-29 + вердикт T5-34); T5-34 и старше бьются только в --retro
   (WARN, история не переписывается — урок F2).
3. ТАМПЕР: живой T5-34 (R+×11 · PG-13×3 мейнов) ловится в retro WARN-ом;
   синтетический канон 14/7/0 проходит чисто; синтетический дрейф — FAIL.
"""
import unittest
from pathlib import Path

from tools.gates import parse_batch, check_rating_mass, GATES, load_oc_names

REPO = Path(__file__).resolve().parents[2]
T534 = REPO / "batches" / "T5-34.md"


def _synth(tmpdir, rplus=14, r=7, pg13=0):
    """Синтетический батч: 21 мейн R+×N · R×N · PG-13×N (спред в шапке
    не нужен — гейт считает парснутые тиры слотов, не строку шапки)."""
    tiers = ["R+"] * rplus + ["R"] * r + ["PG-13"] * pg13
    lines = ["# SYNTH", ""]
    for i, t in enumerate(tiers, start=4):
        lines.append(f"P{i:02d} — synth-main-{i} (VOLT · {t} · Y1)")
        lines.append("POS:")
        lines.append(f"synthetic main {i}, the claim is the body, Y-made")
        lines.append("")
    p = Path(tmpdir) / "T5-99.md"
    p.write_text("\n".join(lines), encoding="utf-8")
    return p


class TestRatingMass(unittest.TestCase):

    def test_config(self):
        cfg = GATES.get("ratingMass")
        self.assertIsNotNone(cfg, "секция ratingMass обязана жить в gates.json")
        self.assertEqual(int(cfg["applyFrom"]), 35)
        self.assertEqual(int(cfg["failFrom"]), 35)
        self.assertEqual(int(cfg["rplusMin"]), 14)
        self.assertEqual(int(cfg["pg13Max"]), 0)

    def test_canon_passes(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            _, _, slots = parse_batch(_synth(td, 14, 7, 0))
            warns, fails = [], []
            stats = check_rating_mass(slots, warns, fails, batch_no=35)
            self.assertEqual(stats["rplus"], 14)
            self.assertEqual(stats["r"], 7)
            self.assertEqual(stats["pg13"], 0)
            self.assertEqual(fails, [], "канон R+×14 · R×7 · PG-13×0 — чисто")
            self.assertEqual(warns, [])

    def test_drift_fails_hard(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            # спред T5-34: R+×11 · R×7 · PG-13×3 — дрейф, убитый В39
            _, _, slots = parse_batch(_synth(td, 11, 7, 3))
            warns, fails = [], []
            stats = check_rating_mass(slots, warns, fails, batch_no=35)
            self.assertEqual(stats["rplus"], 11)
            self.assertEqual(stats["pg13"], 3)
            self.assertEqual(len(fails), 1, "один BATCH-entry с обеими проблемами (стиль voltCore)")
            self.assertEqual(fails[0][1], "rating-mass")
            self.assertIn("R+-масса", fails[0][2])
            self.assertIn("PG-13", fails[0][2])

    def test_era_below_applyfrom_silent(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            _, _, slots = parse_batch(_synth(td, 11, 7, 3))
            warns, fails = [], []
            stats = check_rating_mass(slots, warns, fails, batch_no=34)
            self.assertEqual(stats, {}, "T5-34 и старше — эра молчит (урок F2)")
            self.assertEqual(fails, [])
            self.assertEqual(warns, [])

    def test_retro_shows_warn_not_fail(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            _, _, slots = parse_batch(_synth(td, 11, 7, 3))
            warns, fails = [], []
            check_rating_mass(slots, warns, fails, batch_no=34, retro=True)
            self.assertEqual(fails, [], "retro — WARN-эра, история не бьётся FAIL-ом")
            self.assertEqual(len(warns), 1)
            self.assertEqual(warns[0][1], "rating-mass")

    def test_tamper_live_t534_retro(self):
        """Живой тампер: T5-34 (худший спред конвейера) ловится retro-WARN-ом."""
        if not T534.is_file():
            self.skipTest("batches/T5-34.md недоступен")
        oc_names = load_oc_names()  # как в живом прогоне gates.py — ОС не мейны
        _, _, slots = parse_batch(T534)
        warns, fails = [], []
        stats = check_rating_mass(slots, warns, fails, batch_no=34, retro=True,
                                   oc_names=oc_names)
        self.assertEqual(stats["rplus"], 11, "T5-34 сдал R+×11 (канон ≥ 14)")
        self.assertEqual(stats["pg13"], 3, "T5-34 сдал PG-13×3 (канон = 0)")
        self.assertEqual(fails, [])
        self.assertTrue(
            any(w[1] == "rating-mass" for w in warns),
            "ретро-прогон обязан показать спред-дрейф T5-34")


if __name__ == "__main__":
    unittest.main()
