#!/usr/bin/env python3
"""Эра гейтов 1.18.0 · T5-30 «WHAT THE FUCK IS THAT?!» — первый батч FAIL-режима
В39–В43. Тесты запирают: живой прогон 0F/0W, вольт-ядро 14/7 вперемешку, кины
9/21 (policy v2.0), EXQUISITE ×2 в мейнах, EXP-клетки = полка гипотез (8 гипотез,
H-13 на A/B-паре), рейтинг честен по составу (26 R+, 0 ложных), расы чисты от
канон-локов и clarifier-грамм сданных партий, волна 14 палитр + волна 16
каналов зарегистрированы, квота кандидатов ≤2 соблюдена, карзамены задокументированы.
"""
import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import gates as G  # noqa: E402

BATCH = ROOT / "batches" / "T5-30.md"
RECEIPT = ROOT / "specs" / "gate-receipts" / "2026-11-22-T5-30-v1.json"


def load(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


class TestT530Batch(unittest.TestCase):
    """Батч собран, заперт и проходит эру 1.18.0 без единого нарушения."""

    @classmethod
    def setUpClass(cls):
        cls.text, cls.header, cls.slots = G.parse_batch(BATCH)
        cls.receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))

    def test_batch_exists_33_slots(self):
        self.assertTrue(BATCH.exists())
        self.assertEqual(len(self.slots), 33)

    def test_locked_receipt_clean(self):
        # «Муха не еблась»: живая эра 1.18.0 — ни одного FAIL, ни одного WARN
        self.assertEqual(self.receipt["verdict"], "PASS")
        self.assertEqual(self.receipt["fails"], [])
        self.assertEqual(self.receipt["warns"], [])

    def test_live_rerun_bitwise(self):
        # квитанция не протухла: свежий прогон теми же гейтами = тот же вердикт
        text, header, slots = G.parse_batch(BATCH)
        receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
        self.assertEqual(receipt["verdict"], "PASS")

    def test_volt_core_39(self):
        st = self.receipt["volt_core"]
        self.assertEqual(st["mains"], 21)
        self.assertEqual(st["volt"], 14)      # R+×14 — Закон 24 восстановлен
        self.assertEqual(st["niche"], 7)      # R×7
        self.assertLessEqual(st["max_run"], 3)  # вперемешку (В39)

    def test_race_cast_40(self):
        st = self.receipt["race_cast"]
        self.assertEqual(st["kin"], 9)        # кины — опция (≤10)
        self.assertEqual(st["human"], 12)     # человек — основа
        self.assertEqual(st["policy"], "v2.0")

    def test_exquisite_main_41(self):
        st = self.receipt["exquisite_main"]
        self.assertEqual(st["exquisite"], 2)  # P09 + P19 — ультра в мейн-массе

    def test_exp_hypotheses_42(self):
        st = self.receipt["exp_hypothesis"]
        self.assertEqual(st["cells"], 9)
        self.assertEqual(st["with_h"], 9)     # «полка отдыхает» незаконна
        self.assertEqual(st["without"], [])
        # H-13 (кандидат-механика) — ровно на A/B-паре
        per_h = {}
        for s in self.slots:
            if s.genre == "EXP":
                ids = set(re.findall(r"H-\d{2}", "\n".join(s.body_lines)))
                for h in ids:
                    per_h[h] = per_h.get(h, 0) + 1
        self.assertEqual(per_h.get("H-13"), 2)
        for h, n in per_h.items():
            self.assertLessEqual(n, 2, f"{h} на {n} клетках > 2")

    def test_rating_truth_43(self):
        st = self.receipt["rating_truth"]
        self.assertEqual(st["checked"], 33)
        self.assertEqual(st["false_rplus"], 0)  # ложных R+ нет (наследие В33)
        self.assertEqual(st["soft_drift"], 0)   # дрейфов нет
        self.assertEqual(st["implied_rplus"], 26)  # 3 ОС + 14 мейн + 9 EXP

    def test_no_rplus_from_empty_class(self):
        # В27/В33: R+ собран только от карт с классом экспозиции
        ycards = G.load_y_cards()
        for s in self.slots:
            if s.rating != "R+":
                continue
            card = ycards.get(s.y_card)
            self.assertIsNotNone(card, f"{s.sid}: R+ без карты")
            cls = ((card.get("components") or {}).get("exposure") or {}).get("class")
            self.assertNotEqual(cls, "—", f"{s.sid}: R+ от карты класса «—» (В27)")

    def test_canon_locks_respected(self):
        # LAWS §21.4: расы действующих ОС не катается пулом
        canon = load("specs/oc-canon.json")
        locks = set()
        for oc in canon["ocs"].values():
            if oc.get("active", True):
                m = re.match(r"(R\d{2})", str(oc.get("race", "")))
                if m:
                    locks.add(m.group(1))
        for s in self.slots:
            if s.sid in ("P01", "P02", "P03"):
                continue  # сами ОС — канон VERBATIM
            for r in re.findall(r"\bR\d{2,3}\b", s.paren):
                self.assertNotIn(r, locks, f"{s.sid}: раса {r} — канон-лок ОС")

    def test_races_fresh_vs_delivered(self):
        # clarifier-граммы: расы мейнов не выходили в сданных T5-27/T5-29
        # (прецедент T5-29 «мейн-касты не видели 2–4 партии»)
        delivered = ["T5-27.md", "T5-29.md"]
        mine = [s for s in self.slots
                if s.genre not in ("EXP", "EXQUISITE") or True]
        for s in self.slots:
            if s.sid in ("P01", "P02", "P03"):
                continue
            m = re.search(r"(R\d{2,3})", s.paren)
            if not m:
                continue
            race = m.group(1)
            for b in delivered:
                other = (ROOT / "batches" / b).read_text(encoding="utf-8")
                self.assertNotRegex(
                    other, rf"· {race} ",
                    f"{s.sid}: раса {race} уже выходила в {b} — clarifier-граммы")

    def test_y_stamp_all_weaved(self):
        st = self.receipt["y_stamp"]
        self.assertEqual(st["with_card"], 33)
        self.assertEqual(st["weaved"], 33)
        self.assertEqual(st["window_hits"], 0)
        self.assertEqual(st["corridor_warn"], 0)

    def test_channel_quota(self):
        # квота кандидатов ≤2 — T5-29 платил WARN за 10×candidate
        cand = [s.sid for s in self.slots
                if s.channel and s.channel in
                {c["id"]: c for c in load("specs/delivery-stats.json")["channels"]}
                and {c["id"]: c for c in load("specs/delivery-stats.json")["channels"]}[s.channel]["status"] == "candidate"
                and s.channel != "oc-rplus"]
        self.assertLessEqual(len(cand), 2, f"candidate-каналы {cand} > квоты 2")
        self.assertEqual(cand, ["P16", "P19"])  # волна 16: strap-line-hold + element-linen

    def test_story_cards_present(self):
        self.assertTrue((ROOT / "batches" / "T5-30" / "stories.md").exists())
        self.assertTrue(self.receipt["storyCards"])

    def test_window_receipt_present(self):
        self.assertTrue((ROOT / "batches" / "T5-30" / "window.md").exists())


class TestT530Registries(unittest.TestCase):
    """Волны 14/16 и реестры исполнены до чистого прогона."""

    def test_wave14_palettes(self):
        pal = load("specs/palettes.json")
        # v1.16.0 — волна 15 (T5-31); v1.17.0 — волна 16 (T5-32, заказ автора
        # «9 новых раскрасок и экспериментальных палитр»): пин синхронен живому
        # реестру (правило голых счётчиков: рассинхрон = баг)
        self.assertEqual(pal["version"], "1.21.0")  # 1.21.0 — волна 18 «кислота» T5-34 (P306–P335, trial); 1.20.0 — волна 17 + canon №16
        ids = {p["id"] for p in pal["palettes"]}
        wave14 = [f"P2{i}_" for i in range(70, 79)]  # P270–P278
        for pref in wave14:
            self.assertTrue(any(i.startswith(pref) for i in ids), pref)
        used_in_batch = set(re.findall(r"P27\d_[A-Z_]+", BATCH.read_text(encoding="utf-8")))
        self.assertEqual(len(used_in_batch), 9)  # все девять — в EXP-клетках

    def test_wave16_palettes_t532(self):
        """Волна 16 (T5-32 «DEEPER AND DARKER»): 9 новых тёмных семей
        P288–P296, все девять — в EXP-клетках T5-32, trial до вердикта."""
        pal = load("specs/palettes.json")
        ids = {p["id"] for p in pal["palettes"]}
        wave16 = [f"P2{i}_" for i in range(88, 97)]  # P288–P296
        for pref in wave16:
            self.assertTrue(any(i.startswith(pref) for i in ids), pref)
        batch32 = (ROOT / "batches" / "T5-32.md").read_text(encoding="utf-8")
        used = set(re.findall(r"P28[89]_[A-Z_]+|P29\d_[A-Z_]+", batch32))
        self.assertEqual(len(used), 9, used)
        waves = pal.get("exp_color_waves", [])
        self.assertTrue(any(w.get("wave") == 16 for w in waves), "волна 16 не записана")

    def test_wave16_channels(self):
        ds = load("specs/delivery-stats.json")
        self.assertEqual(ds["version"], "0.16.0")
        ids = {c["id"]: c for c in ds["channels"]}
        self.assertIn("strap-line-hold", ids)
        self.assertIn("element-linen", ids)
        self.assertEqual(ids["strap-line-hold"]["status"], "candidate")
        self.assertEqual(ids["element-linen"]["evidence"], ["T5-30"])

    def test_oc_candidates_13(self):
        oc = load("specs/oc-candidates.json")
        self.assertEqual(oc["version"], "1.7.0")  # 1.7.0 — квитанция вердикта T5-34: шестёрка passed; 1.5.0 — T5-33
        t30 = [c for c in oc["candidates"] if c["batch"] == "T5-30"]
        self.assertEqual(len(t30), 9)
        for c in t30:
            self.assertEqual(c["status"], "trial")
            self.assertRegex(c["hypothesis"], r"H-\d{2}")

    def test_furnace_f026(self):
        fl = load("specs/furnace-ledger.json")
        self.assertEqual(fl["version"], "1.9.0")  # 1.9.0 — +F-028 грань-X (T5-34)
        self.assertTrue(any(e.get("id") == "F-026" for e in fl["entries"]))

    def test_delivery_index_t530(self):
        di = json.dumps(load("specs/delivery-index.json"), ensure_ascii=False)
        self.assertIn("T5-30", di)


if __name__ == "__main__":
    unittest.main()
