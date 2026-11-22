#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Тесты цикла 4 «КОНВЕЙЕР ВОСПРОИЗВОДИМОСТИ» (заказ А–К, 2026-11-21):
  - bodytypes.json (Е): 24 типажа, веса, запреты дрейфа
  - marks.json (И): 42 метки, рейтинг-нейтральность, kin_compat
  - races.json v2.7.0 (З): кин-оверхаул — clarifiers/gimmick/skin_type
  - raw-plus v2.3.0 (В): закон тег-порядка
  - dresser v1.3.0 (Ж): закон пре-гардероба + tools/pregarment.py
  - tools/testforge.py (А/Б/Г): ролл/чек/покрытие/сравнение
  - oc-candidates.json (Д): реестр кандидатов

Прогон: python3 -m unittest discover -s tests/python -v
"""

import json
import random
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO / "tools"))

import pregarment as pg  # noqa: E402
import testforge as tf  # noqa: E402

SPEC = REPO / "specs"


def load(name):
    return json.loads((SPEC / name).read_text(encoding="utf-8"))


class TestBodytypesE(unittest.TestCase):
    """пункт Е: типажи тел — 24 категории с тегами и балансом."""

    def setUp(self):
        self.d = load("bodytypes.json")
        self.types = self.d["types"]

    def test_24_categories_unique(self):
        ids = [t["id"] for t in self.types]
        self.assertEqual(len(ids), 24)
        self.assertEqual(len(set(ids)), 24)

    def test_weights_balance(self):
        total = sum(t["weight"] for t in self.types)
        self.assertEqual(total, 146)
        # середина+мягкость ≈ 60% (балансик, не petite-уклон и не жёсткая полнота)
        soft = sum(t["weight"] for t in self.types if t["axes"]["frame"] in ("average", "soft"))
        self.assertGreater(soft / total, 0.5)
        # petite-край — редкость
        petite = sum(t["weight"] for t in self.types if t["id"] in ("BT-03", "BT-04"))
        self.assertLess(petite / total, 0.06)

    def test_no_banned_drift(self):
        banned = self.d["forbidden_drift"]["tags_never_in_bodytypes"]
        for t in self.types:
            for tag in t["tags"]:
                for b in banned:
                    self.assertNotIn(b, tag.lower(), f"{t['id']} несёт запретный тег {b}")

    def test_tags_english_danbooru(self):
        for t in self.types:
            self.assertTrue(3 <= len(t["tags"]) <= 6, f"{t['id']}: тегов {len(t['tags'])}")
            for tag in t["tags"]:
                self.assertTrue(tag.replace(" ", "").replace("-", "").replace("'", "").isascii(),
                                f"{t['id']}: не-ASCII тег {tag}")

    def test_belly_spectrum_honest(self):
        # животик приемлем (BT-16), жёстких толстух нет: belly максимум 'slight'
        for t in self.types:
            self.assertIn(t["axes"]["belly"], ("flat", "soft", "slight"))

    def test_bridge_in_body_json(self):
        b = load("body.json")
        self.assertEqual(b["version"], "1.1.0")
        self.assertIn("bodytypes_bridge", b)
        self.assertIn("order", b["bodytypes_bridge"])


class TestMarksI(unittest.TestCase):
    """пункт И: метки — тату/пятна/шрамы/ожоги/глаза/кожа."""

    def setUp(self):
        self.d = load("marks.json")
        self.marks = self.d["marks"]

    def test_counts_and_categories(self):
        cats = {}
        for m in self.marks:
            cats[m["category"]] = cats.get(m["category"], 0) + 1
        self.assertEqual(sum(cats.values()), 42)
        for c in ("tattoo", "birthmark", "scar", "burn", "eyes", "skin"):
            self.assertIn(c, cats, f"нет категории {c}")

    def test_rating_neutrality_law(self):
        self.assertIn("РЕЙТИНГ-НЕЙТРАЛЬНА", self.d["law"])

    def test_oc_hooks_rare(self):
        oc = [m for m in self.marks if m["oc_hook"]]
        self.assertLessEqual(len(oc), 6)
        for m in oc:
            self.assertLessEqual(m["weight"], 2, "ОС-сигнатура обязана быть редкой")

    def test_kin_compat_covers_gel(self):
        inc = self.d["kin_compat_rules"]["incompat_ids"]
        for rid in ("R17", "R25", "R46", "R57"):
            self.assertIn(rid, inc["gel"])

    def test_burns_old_only(self):
        for m in self.marks:
            if m["category"] == "burn":
                self.assertIn("old", m["pos"].lower(), "ожоги только старые/зажившие")

    def test_visibility_zones_mapped(self):
        zmap = self.d["visibility_pairs"]["zone_to_frame"]
        for m in self.marks:
            self.assertIn(m["zone"], zmap, f"{m['id']}: зона {m['zone']} без рамки видимости")


class TestRacesZ(unittest.TestCase):
    """пункт З: кин-оверхаул — clarifiers/gimmick/skin_type у всех активных."""

    def setUp(self):
        self.d = load("races.json")
        self.races = self.d["races"]

    def test_version(self):
        self.assertEqual(self.d["version"], "2.7.0")
        self.assertIn("kin_law", self.d)

    def test_every_active_race_overhauled(self):
        for r in self.races:
            if r["id"].startswith("BAN"):
                continue
            self.assertIn("skin_type", r, f"{r['id']}: нет skin_type")
            self.assertIn("clarifiers", r, f"{r['id']}: нет clarifiers")
            self.assertIn("wardrobe_hook", r, f"{r['id']}: нет wardrobe_hook")
            self.assertIn("light_hook", r, f"{r['id']}: нет light_hook")
            if r["id"] != "R01":
                self.assertTrue(r.get("gimmick"), f"{r['id']}: нет гиммика")

    def test_form_lock_every_kin(self):
        # модель слегка туповатая: форм-лок обязателен, иначе рисует мордой
        for r in self.races:
            if r["id"].startswith("BAN") or r["id"] == "R01":
                continue
            joined = " ".join(r.get("clarifiers", []))
            self.assertTrue("human face" in joined or "human upper body" in joined,
                            f"{r['id']}: clarifiers без форм-лока")

    def test_skin_types_valid(self):
        valid = {"skin", "mixed", "scales", "gel", "glass", "stone", "smoke"}
        for r in self.races:
            if r["id"].startswith("BAN"):
                continue
            self.assertIn(r["skin_type"], valid)

    def test_gimmick_drawable(self):
        # гиммик = рисуемое поведение: глагольный стем в наличии (модель слегка
        # туповатая — характер делом, не описанием)
        stems = (r"\b(flick|betray|drift|hold|puff|wrap|cove|lean|rise|turn|swish|pop|wash|"
                 r"thump|pound|set|slacken|surface|arriv|offer|curl|dimp|inspect|read|map|"
                 r"know|fold|watch|learn|dust|win|headbutt|freez|escap|flicker|tap|count|"
                 r"sniff|still|yawn|blush|pocket|point|go|dread|sleep|squint|grin|deny|"
                 r"shine|swing|vent|flush|blink|dim|brighten|flutter|releas|crack|glow|"
                 r"hum|start|fail|trick|knit|carve|test|float|register|miss|answer|"
                 r"lead|take|give|get|keep|put|call|make|need|feel|try|ask|use|find|"
                 r"reach|bring|shift|enter|twitch|apolog|borrow|ban)\w*")
        for r in self.races:
            g = r.get("gimmick")
            if not g:
                continue
            self.assertRegex(g.lower(), stems, f"{r['id']}: гиммик без действия")

    def test_bans_untouched(self):
        bans = [r["id"] for r in self.races if r["id"].startswith("BAN")]
        self.assertEqual(len(bans), 4)


class TestTagOrderV(unittest.TestCase):
    """пункт В: закон тег-порядка в raw-plus v2.3.0."""

    def test_section(self):
        d = load("raw-plus.json")
        self.assertEqual(d["version"], "2.3.0")
        self.assertIn("tag_order", d)
        self.assertIn("primary_registers", d["tag_order"])
        self.assertIn("secondary_registers", d["tag_order"])
        # OPENER: квалити → кластер → 1girl → канон → кин → тело → кинетика
        self.assertEqual(d["tag_order"]["primary_registers"][2], "1girl, solo")
        self.assertIn("кин-clarifiers", d["tag_order"]["primary_registers"][4])
        self.assertIn("тело-регистр BT", d["tag_order"]["primary_registers"][5])

    def test_template_line1_updated(self):
        d = load("raw-plus.json")
        self.assertIn("кин-регистр", d["template"][0])
        self.assertIn("BT-XX", d["template"][0])


class TestPregarmentJ(unittest.TestCase):
    """пункт Ж: пре-гардероб — свежие комбо под жребий, набор не повторяется."""

    def setUp(self):
        self.closet = pg.load_closet()
        self.matrix = pg.load_matrix()
        self.camera = load("camera.json")
        self.cards = {c["id"]: c for c in self.camera["y_cards"]["cards"]}

    def test_deterministic_seed(self):
        rng1, rng2 = random.Random(7), random.Random(7)
        ledger = {"version": "1.0.0", "combos_used": {}}
        card = self.cards["Y442"]
        c1 = pg.roll_combo(rng1, card, "street", self.closet, self.matrix, ledger)
        ledger2 = {"version": "1.0.0", "combos_used": {}}
        c2 = pg.roll_combo(rng2, card, "street", self.closet, self.matrix, ledger2)
        self.assertEqual([x["code"] for x in c1["codes"]], [x["code"] for x in c2["codes"]])

    def test_combo_holds_class(self):
        rng = random.Random(11)
        ledger = {"version": "1.0.0", "combos_used": {}}
        for yid, cls in (("Y442", "COVER"), ("Y316", "COVER")):
            card = self.cards[yid]
            self.assertEqual(card["components"]["exposure"]["class"], cls)
            combo = pg.roll_combo(rng, card, "lounge", self.closet, self.matrix, ledger)
            for code in combo["codes"]:
                item = next(i for sh in self.closet["shelves"].values()
                            for i in sh["items"] if i["code"] == code["code"])
                self.assertIn(cls, item["exposure"],
                              f"{code['code']} не держит класс {cls}")

    def test_geometry_only_cards_skip(self):
        rng = random.Random(3)
        ledger = {"version": "1.0.0", "combos_used": {}}
        geo = [c for c in self.cards.values()
               if (c.get("components") or {}).get("exposure", {}).get("class") not in self.matrix]
        self.assertTrue(geo, "в пуле нет карт класса «—»")
        combo = pg.roll_combo(rng, geo[0], "street", self.closet, self.matrix, ledger)
        self.assertTrue(combo.get("geometry_only"))

    def test_no_combo_reuse(self):
        rng = random.Random(5)
        ledger = {"version": "1.0.0", "combos_used": {}}
        card = self.cards["Y442"]
        seen = set()
        for _ in range(6):
            combo = pg.roll_combo(rng, card, "street", self.closet, self.matrix, ledger)
            if "combo_key" in combo:
                self.assertNotIn(combo["combo_key"], seen,
                                 "кубик выдал повторный набор (реюз запрещён)")
                seen.add(combo["combo_key"])
                ledger["combos_used"][combo["combo_key"]] = {"batch": "test"}

    def test_dresser_law_section(self):
        d = load("dresser.json")
        self.assertEqual(d["version"], "1.3.0")
        self.assertIn("pregarderobe", d)
        self.assertIn("реестр", d["pregarderobe"]["law"])


class TestOcCandidatesD(unittest.TestCase):
    """пункт Д: реестр кандидатов в ОС."""

    def test_spec(self):
        d = load("oc-candidates.json")
        # v1.0.0 born-empty (ЦИКЛ 4); v1.1.0 — первый боевой лог: 9 кандидатов
        # EXP-партии T5-29 (заказ автора «9 кандидатов в ОС»), статус trial
        self.assertIn(d["version"], ("1.0.0", "1.1.0", "1.2.0", "1.3.0"))  # 1.3.0 — девятка кандидатов T5-30
        self.assertIn("bundle", d)
        self.assertIn("candidates", d)
        if d["version"] == "1.0.0":
            self.assertEqual(d["candidates"], [])
        else:
            # боевой лог: схема бандла bundle.fields у каждой записи
            fields = set(d["bundle"]["fields"])
            for c in d["candidates"]:
                self.assertTrue(fields & set(c), f"кандидат без полей бандла: {c.get('slot')}")
                self.assertIn(c["status"], ("trial", "taken", "promoted", "passed"))
        # promoted — канонический статус промоции по закону реестра
        # (oc-candidates.json law: «строка здесь получает статус promoted»);
        # первая промоция: T5-29 P32 → Noxx (canon 2.14.0)


class TestForgeABG(unittest.TestCase):
    """пункты А/Б/Г: тест-горн — болванки, инварианты, покрытие, сходимость."""

    @classmethod
    def setUpClass(cls):
        cls.forge = tf.Forge()
        cls.out = tempfile.mkdtemp(prefix="tb-test-")

    def test_roll_and_check_pass(self):
        doc = tf.roll(12, 987654, Path(self.out) / "TB-TEST.json")
        errs = tf.check_batch(doc, self.forge)
        self.assertEqual(errs, [], f"инварианты нарушены: {errs[:5]}")

    def test_manifest_full(self):
        doc = tf.roll(8, 222, Path(self.out) / "TB-TEST2.json")
        for s in doc["slots"]:
            for f in ("y_card", "race", "bodytype", "marks", "cl_codes",
                      "palette", "predicted", "pos", "neg", "signals", "gimmick"):
                self.assertIn(f, s, f"манифест неполон: нет {f}")
            self.assertIn("tier", s["predicted"])
            self.assertIn(s["predicted"]["tier"], ("PG-13", "R", "R+"))

    def test_tier_signals_honest(self):
        doc = tf.roll(16, 333, Path(self.out) / "TB-TEST3.json")
        for s in doc["slots"]:
            text = " ".join(s["pos"]).lower()
            if s["predicted"]["tier"] == "R+":
                for sig in s["signals"]:
                    self.assertIn(sig.lower(), text, "R+ без своего сигнала")
            else:
                for bad in ("covered nipples", "clothed nipples", "handbra",
                            "taped nipples", "topless with tape"):
                    self.assertNotIn(bad, text, f"{s['predicted']['tier']}-слот несёт R+ сигнал")

    def test_no_service_codes_in_pos(self):
        import re
        doc = tf.roll(10, 444, Path(self.out) / "TB-TEST4.json")
        for s in doc["slots"]:
            self.assertIsNone(re.search(r"CAM\d+", " ".join(s["pos"])),
                              "служебный CAM-код в POS (В34)")

    def test_compare_convergence_loop(self):
        # синтетический инбокс: предикт R+ у первого R+ слота, промах у второго
        doc = tf.roll(12, 987654, Path(self.out) / "TB-TEST.json")
        rplus = [s for s in doc["slots"] if s["predicted"]["tier"] == "R+"]
        self.assertTrue(rplus, "в болванке нет R+ слотов")
        rows = []
        for i, s in enumerate(rplus[:2]):
            fact = s["predicted"]["tier"] if i == 0 else "R"
            rows.append({"tag": f"{doc['id']} P{s['n']:02d}", "identity": {
                "rating": fact, "note": "синтетика для теста петли"}})
        with tempfile.TemporaryDirectory() as td:
            meta = Path(td) / "meta.json"
            meta.write_text(json.dumps({"items": rows}, ensure_ascii=False), encoding="utf-8")
            conv_path = Path(td) / "convergence.json"
            rc = tf.cmd_compare("all", meta_path=meta, corpus_dir=Path(self.out),
                                convergence_path=conv_path)
            self.assertEqual(rc, 0)
            conv = json.loads(conv_path.read_text(encoding="utf-8"))
            self.assertEqual(conv["total"], 2)
            self.assertEqual(conv["matched"], 1)
            self.assertEqual(conv["convergence"], 0.5)
            self.assertEqual(len(conv["misses"]), 1)

    def test_coverage_ledger_counts(self):
        doc = tf.roll(9, 555, Path(self.out) / "TB-TEST5.json")
        led_path = tf.CORPUS / "coverage-ledger.json"
        before = json.loads(led_path.read_text(encoding="utf-8")) if led_path.exists() else {}
        # coverage обновляет ledger из файлов корпуса — после ролла файл на месте
        tf.cmd_coverage()
        led = json.loads(led_path.read_text(encoding="utf-8"))
        total_y = sum(led["y_cards"].values())
        self.assertGreater(total_y, 0)
        if before.get("y_cards"):
            self.assertGreaterEqual(total_y, sum(before["y_cards"].values()))


if __name__ == "__main__":
    unittest.main()
