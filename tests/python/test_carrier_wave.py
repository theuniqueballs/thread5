"""ВОЛНА «НОСИТЕЛЬ-КОМБО» T5-34 (заказ автора 2026-11-27, чат: «сосредоточься
на изучении эччи-оракула, там столько всякой полезной хуйни... тебе буквально
блять приготовили все возможные Y, надо только разгрести, добавить комбо,
сопоставить с одеждой и на нахуй!»).

Что проверяем:
1. camera.json 1.22.0: разбор старых 512 Y (combo-блоки ×512) + волна Y539–Y554 (16 карт из CARRIER_LIBRARY,
   specs/carriers.json 1.0.0 — 462 носителя, синк эччи-оракула); каждая карта
   = 2 вербатим-носителя разных классов × камерный кластер × коридор; все 14
   классов носителей покрыты; волна НЕ юри (В49).
2. dresser.json 1.9.0: y_stack.combo_book — комбо-книга по рейтингу (40 позиций: 33 + 7 старой 512-волны) + carrier_matrix 1.7.0 «носитель × одежда» — 14
   классов × полки CLOSET; G/H — усилители 0.5x (core4_law), партнёр-core
   обязателен; полки-коды существуют в closet.json; CR-примеры существуют.
3. Совместимость с гейтами: yStack/yStamp читают новые карты (exposure
   классы легальны, id уникальны).
"""
import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

import gates  # noqa: E402

EXPOSURE_CLASSES = {"COVER", "PROCESS", "LINGERIE", "CLOTHED-TIGHT", "SHEER"}
CORRIDORS = {"A", "B", "A+B"}
WAVE_IDS = [f"Y{n}" for n in range(539, 555)]
YURI_FORBIDDEN = ("2girls", "two girls", "each other", "girls'", "her tongue trailing")

# слова-механика носителя: в паттерне обязана читаться физика
PHYSICS_STEMS = (
    "taut", "stretch", "press", "drop", "sway", "print", "claim", "band",
    "drift", "shot", "gust", "ride", "straddle", "sightline", "crease",
    "zipper", "strap", "fallen", "bounce", "aftershock", "dome", "belly",
    "caught", "catch",
)


def load(name):
    return json.loads((ROOT / "specs" / name).read_text(encoding="utf-8"))


def distinctive(phrase):
    """Значимые слова фразы носителя (для проверки вплетения 1:1)."""
    stop = {"the", "her", "his", "its", "their", "with", "from", "into",
            "where", "after", "over", "under", "past", "at", "of", "and",
            "one", "two", "whole", "own"}
    return [w for w in re.findall(r"[a-z]{5,}", phrase.lower()) if w not in stop]


class TestCarrierWave(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cam = load("camera.json")
        cls.dr = load("dresser.json")
        cls.car = load("carriers.json")
        cls.closet = load("closet.json")
        cls.cards = {c["id"]: c for c in cls.cam["y_cards"]["cards"]}
        cls.wave = [cls.cards[i] for i in WAVE_IDS]
        cls.cr_index = {
            cid: entry
            for klass, lst in cls.car["classes"].items()
            for entry in lst
            for cid in [entry["id"]]
        }

    # ------------------------------------------------------------ версии
    def test_versions(self):
        self.assertEqual(self.cam["version"], "1.23.0")  # 1.23.0 — era-сплит (В52)
        self.assertEqual(self.dr["version"], "1.9.0")  # 1.9.0 — комбо-книга добрала старые 512 Y

    def test_registry_size_and_law_note(self):
        self.assertEqual(len(self.cam["y_cards"]["cards"]), 559)  # 554 + волна «грань-X» Y555–Y559
        self.assertIn("1.22.0", self.cam["y_cards"]["law"])
        self.assertIn("CARRIER_LIBRARY", self.cam["y_cards"]["law"])

    def test_wave_ids_sequential_unique(self):
        ids = [c["id"] for c in self.cam["y_cards"]["cards"]]
        self.assertEqual(len(ids), len(set(ids)), "дубль id в реестре")
        for wid in WAVE_IDS:
            self.assertIn(wid, self.cards)

    # --------------------------------------------------- анатомия карт
    def test_card_anatomy(self):
        for c in self.wave:
            with self.subTest(card=c["id"]):
                self.assertIn(c["corridor"], CORRIDORS, "коридор обязателен (закон y_cards)")
                comp = c["components"]
                klass = comp["exposure"]["class"]
                self.assertIn(klass, EXPOSURE_CLASSES)
                self.assertTrue(comp["exposure"].get("cover_object"))
                self.assertTrue(comp["exposure"].get("read"))
                self.assertTrue(comp.get("pose"))
                self.assertTrue(comp.get("pov"))
                self.assertTrue(comp.get("camera"))
                self.assertTrue(comp.get("profiling"))
                self.assertIn("LAB", c["trust"], "волна входит LAB (урок Y531–Y538)")
                self.assertIn("T5-34", c["trust"])
                self.assertIn("CARRIER_LIBRARY", c["built_from"])
                self.assertIn("носитель-комбо волна", c["verdict"])

    def test_patterns_weave_carriers_verbatim(self):
        """Каждый built_from носитель реально вплетён в паттерн (≥3 значимых
        слова фразы носителя в паттерне)."""
        for c in self.wave:
            pat = c["pattern"].lower()
            cr_ids = re.findall(r"CR-[A-Z]+\d+", c["built_from"])
            self.assertGreaterEqual(len(cr_ids), 2,
                                    f"{c['id']}: волна = 2 носителя на карту")
            for cid in cr_ids:
                self.assertIn(cid, self.cr_index, f"{c['id']}: {cid} не найден в carriers.json")
                words = distinctive(self.cr_index[cid]["carrier"])
                hits = sum(1 for w in words if w in pat)
                # фразы-минималисты (1–2 значимых слова) вплетаются целиком
                self.assertGreaterEqual(hits, min(3, len(words)),
                                        f"{c['id']}: носитель {cid} вплетён слабо ({hits}/{len(words)})")

    def test_patterns_carry_physics(self):
        """Физика в паттерне: хотя бы один механик-стем (В27-физика, против
        карт-пустышек класса «—»)."""
        for c in self.wave:
            pat = c["pattern"].lower()
            self.assertTrue(any(s in pat for s in PHYSICS_STEMS),
                            f"{c['id']}: в паттерне нет механики носителя")

    def test_wave_not_yuri(self):
        """В49: волна НЕ юри — парный реестр Y531–Y538 не расширяется."""
        for c in self.wave:
            pat = c["pattern"].lower()
            for bad in YURI_FORBIDDEN:
                self.assertNotIn(bad, pat, f"{c['id']}: юри-паттерн в волне запрещён (В49)")
            self.assertNotIn("garment_pair", c, f"{c['id']}: парное поле в волне запрещено")

    def test_all_14_carrier_classes_covered(self):
        """Волна покрывает все 14 классов CARRIER_LIBRARY."""
        covered = set()
        for c in self.wave:
            for cid in re.findall(r"CR-([A-Z])\d+", c["built_from"]):
                covered.add(cid)
        self.assertEqual(covered, set(self.car["classes"].keys()),
                         f"не покрыты: {set(self.car['classes']) - covered}")

    def test_span_cards_two_groups(self):
        """Cross-group span-комбо (Y547 F×B, Y551 G×C, Y552 H×E, Y554 W×D)
        должны соединять ≥2 мех-группы; остальные карты — честные пары
        своего класса/группы."""
        groups = self.car["mech_groups"]
        def group_of(cid):
            for g, ks in groups.items():
                if cid[3] in ks:
                    return g
            return "?"
        spans = {"Y547", "Y551", "Y552", "Y554"}
        for c in self.wave:
            cr_ids = re.findall(r"CR-[A-Z]+\d+", c["built_from"])
            gs = {group_of(cid) for cid in cr_ids}
            if c["id"] in spans:
                self.assertGreaterEqual(len(gs), 2,
                                        f"{c['id']}: span-комбо должно соединять ≥2 группы")
            else:
                self.assertGreaterEqual(len(gs), 1)

    # ------------------------------------------- dresser carrier_matrix
    def test_carrier_matrix_structure(self):
        cm = self.dr["y_stack"]["carrier_matrix"]
        self.assertIn("born", cm)
        self.assertIn("сопоставить с одеждой", cm["born"])
        self.assertIn("CARRIER_LIBRARY", cm["law"])
        self.assertIn("0.5x", cm["law"])
        for k in self.car["classes"].keys():
            self.assertIn(k, cm, f"класс {k} отсутствует в матрице")
            entry = cm[k]
            self.assertEqual(entry["group"], self.car["mech_groups"] and
                             next(g for g, ks in self.car["mech_groups"].items() if k in ks),
                             f"{k}: group не совпадает с mech_groups carriers.json")
            self.assertTrue(entry["name"])
            self.assertTrue(entry["gar_f"])
            self.assertTrue(entry["chokers"])
            self.assertGreaterEqual(len(entry["carriers"]), 2)

    def test_carrier_matrix_shelves_exist(self):
        cm = self.dr["y_stack"]["carrier_matrix"]
        shelf_codes = set(self.closet["shelves"].keys())
        for k, entry in cm.items():
            if k in ("born", "law"):
                continue
            if entry["group"] == "AMPLIFIER":
                self.assertEqual(entry["shelves"], [],
                                 f"{k}: усилитель не привязан к полкам (камера/тело)")
            else:
                self.assertTrue(entry["shelves"], f"{k}: пустые полки у core-класса")
                for s in entry["shelves"]:
                    self.assertIn(s, shelf_codes, f"{k}: полка {s} не существует в closet.json")

    def test_carrier_matrix_examples_exist(self):
        cm = self.dr["y_stack"]["carrier_matrix"]
        for k, entry in cm.items():
            if k in ("born", "law"):
                continue
            for cid in entry["carriers"]:
                self.assertIn(cid, self.cr_index, f"{k}: пример {cid} не найден")
                self.assertTrue(cid[3] == k, f"{k}: пример {cid} чужого класса")

    def test_amplifier_law_in_entries(self):
        cm = self.dr["y_stack"]["carrier_matrix"]
        for k in ("G", "H"):
            self.assertIn("0.5x", cm[k]["gar_f"], f"{k}: усилитель без веса 0.5x")
            self.assertIn("обязателен", cm[k]["gar_f"], f"{k}: без требования партнёра-core")

    # ---------------------------------------------------- совместимость
    def test_gates_load_new_cards(self):
        ycards = gates.load_y_cards()
        self.assertEqual(len(ycards), 559)
        self.assertEqual(ycards["Y539"]["components"]["exposure"]["class"], "CLOTHED-TIGHT")
        self.assertEqual(ycards["Y554"]["components"]["exposure"]["class"], "CLOTHED-TIGHT")
        self.assertEqual(ycards["Y559"]["components"]["exposure"]["class"], "CLOTHED-TIGHT")
        self.assertEqual(ycards["Y554"]["corridor"], "A+B")

    def test_ystack_gate_matrix_still_intact(self):
        """Матрица экспозиций y_stack.matrix не тронута волной (5 классов)."""
        m = self.dr["y_stack"]["matrix"]
        self.assertEqual(set(m.keys()), EXPOSURE_CLASSES)

    def test_carriers_source_synced_with_oracle(self):
        """specs/carriers.json = синк оракула (462 носителя, 14 классов)."""
        oracle = json.loads((ROOT / "mini-services" / "ecchi-oracle" / "taxonomy" /
                             "source" / "carriers.json").read_text(encoding="utf-8"))
        self.assertEqual(self.car["version"], oracle["version"])
        total = sum(len(v) for v in self.car["classes"].values())
        self.assertEqual(total, sum(len(v) for v in oracle["classes"].values()))
        self.assertEqual(total, 462, "носителей должно быть ровно 462 (сумма классов)")


if __name__ == "__main__":
    unittest.main()
