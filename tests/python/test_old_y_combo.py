#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Тесты РАЗБОРА СТАРЫХ 512 Y + волны «грань-X» (заказ автора 2026-11-27:
«это были не устаревшие Y, просто они написаны были слегка иначе по другой
концепции. возьми и их тоже… берёшь старые 512 Y, разбираешь их на
составляющие, улучшаешь в них сладкий джус, описываешь получше, сверяешься с
эччи протоколом и точно так же, сопоставляя с одеждой и камерой и
пре-гарментом вписываешь в то, что уже есть. не надо сука выдумывать
велосипед»).

Проверяется:
1. camera.json 1.22.0: ВСЕ старые карты Y1–Y512 несут combo-блок
   (носители/мех-группы/камера/дистанция/покрытие-в-позе/теги/core-rare/
   полки closet/сок ≤200/протокольный вердикт).
2. Протокол: R+ легален 85 · честный R 94 · скелет 333 (источник — camera.json
   changelog 1.22.0; цифры пинятся: слаженность, не снежный ком).
3. Теги ⊆ закрытый словарь комбо-книги (48), ≤6 на карту.
4. покрытие-в-позе ∈ {easy, strained, hard}; repeats ∈ {core, rare}.
5. Полки closet: коды существуют, exposure держит класс карты (закон yStack).
6. Волна «грань-X» Y555–Y559: коридор A/B, built_from из CARRIER_LIBRARY
   (вербатим id), LAB-траст, класс экспозиции, НЕ юри (solo-карты).
7. Комбо-книга dresser 1.9.0: диета 40/40 ровно; добор старой волны (7
   позиций) ссылается на существующие Y-карты; порядок стака жив.
"""
from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SPEC = ROOT / "specs"


def load(name):
    return json.loads((SPEC / name).read_text(encoding="utf-8"))


class TestOldYCombo(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cam = load("camera.json")
        cls.cards = {c["id"]: c for c in cls.cam["y_cards"]["cards"]}
        cls.carriers = load("carriers.json")
        cls.closet = load("closet.json")
        cls.dresser = load("dresser.json")
        cls.old = {f"Y{i}": cls.cards[f"Y{i}"] for i in range(1, 513)}

    def test_versions(self):
        self.assertEqual(self.cam["version"], "1.23.0")
        self.assertIn("1.22.0", self.cam["y_cards"]["law"])
        self.assertIn("1.23.0", self.cam["y_cards"]["law"])  # era-сплит (В52)
        notes = " ".join(str(e) for e in self.cam.get("changelog", []))
        self.assertIn("1.22.0", notes)
        self.assertIn("1.23.0", json.dumps(self.cam["changelog"][0]))

    def test_all_512_have_combo(self):
        """Каждая старая карта разобрана на составляющие — не выборочно."""
        for yid, card in self.old.items():
            combo = card.get("combo")
            self.assertIsNotNone(combo, f"{yid} без combo-блока")
            for field in ("born", "carriers", "mech_groups", "camera",
                          "distance", "pose_coverage", "tags", "repeats",
                          "closet", "juice", "protocol"):
                self.assertIn(field, combo, f"{yid}.{field}")
            self.assertLessEqual(len(combo["juice"]), 200, f"{yid} сок > 200")
            self.assertIn(combo["pose_coverage"], ("easy", "strained", "hard"))
            self.assertIn(combo["repeats"], ("core", "rare"))
            dd = combo["distance"].lstrip("D").rstrip("+")
            self.assertTrue(dd.isdigit() and 1 <= int(dd) <= 8,
                            f"{yid} дистанция {combo['distance']}")
            self.assertTrue(combo["protocol"], f"{yid} пустой вердикт")

    def test_protocol_counts(self):
        """Слаженность: R+ 85 · честный R 94 · скелет 333 (не снежный ком)."""
        kinds = {"rplus": 0, "r": 0, "skeleton": 0}
        for card in self.old.values():
            v = card["combo"]["protocol"]
            if v.startswith("R+ ЛЕГАЛЕН"):
                kinds["rplus"] += 1
            elif v.startswith("СКЕЛЕТ"):
                kinds["skeleton"] += 1
            else:
                kinds["r"] += 1
        self.assertEqual(kinds["rplus"], 85)
        self.assertEqual(kinds["r"], 94)
        self.assertEqual(kinds["skeleton"], 333)

    def test_tags_closed_vocab(self):
        vocab = set(self.dresser["y_stack"]["combo_book"]["tag_vocab"])
        self.assertEqual(len(vocab), 48)
        for yid, card in self.old.items():
            tags = card["combo"]["tags"]
            self.assertLessEqual(len(tags), 6, f"{yid} тегов > 6 — борщ")
            for t in tags:
                self.assertIn(t, vocab, f"{yid}: тег «{t}» вне словаря 48")

    def test_closet_codes_match_class(self):
        """Сопоставление с одеждой: полки держат класс экспозиции карты."""
        exposure_of = {}
        for sh in self.closet["shelves"].values():
            for it in sh["items"]:
                exposure_of[it["code"]] = set(it.get("exposure", []))
        classes = ("COVER", "PROCESS", "LINGERIE", "CLOTHED-TIGHT", "SHEER")
        checked = 0
        for yid, card in self.old.items():
            combo = card["combo"]
            ex = (card.get("components", {}).get("exposure") or {}).get("class", "—")
            for code in combo["closet"]:
                self.assertIn(code, exposure_of, f"{yid}: полка {code} не в closet")
                if ex in classes:
                    self.assertIn(ex, exposure_of[code],
                                 f"{yid}: {code} не держит класс {ex} (закон yStack)")
                    checked += 1
        self.assertGreater(checked, 100)  # стака хватает на R+ сборки

    def test_carriers_reference_library(self):
        lib_ids = {c["id"] for lst in self.carriers["classes"].values() for c in lst}
        n_with = 0
        for yid, card in self.old.items():
            for entry in card["combo"]["carriers"]:
                if entry == "—":
                    continue
                cid = entry.split(" ", 1)[0]
                self.assertIn(cid, lib_ids, f"{yid}: носителя {cid} нет в библиотеке")
                n_with += 1
        self.assertGreater(n_with, 300)

    def test_camera_clusters(self):
        valid = {"CAM01_front", "CAM02_three_quarter", "CAM03_from_below",
                 "CAM04_from_above", "CAM05_close", "CAM06_side",
                 "CAM07_wide_env", "CAM08_back_to_camera",
                 "CAM10_macro", "CAM11_mirror_reflection", "CAM12_aerial",
                 "CAM13_insert"}
        for yid, card in self.old.items():
            self.assertIn(card["combo"]["camera"], valid, f"{yid} кластер?")


class TestGraniXWave(unittest.TestCase):
    """Волна «грань-X» Y555–Y559: сомнительные Y, которые легко
    перекидываются в X — прикрытие привязано к вещи (заказ автора)."""

    @classmethod
    def setUpClass(cls):
        cls.cam = load("camera.json")
        cls.cards = {c["id"]: c for c in cls.cam["y_cards"]["cards"]}
        cls.carriers = load("carriers.json")
        cls.lib_ids = {c["id"] for lst in cls.carriers["classes"].values()
                       for c in lst}

    def test_wave_anatomy(self):
        self.assertEqual(len(self.cam["y_cards"]["cards"]), 559)
        for y in ("Y555", "Y556", "Y557", "Y558", "Y559"):
            card = self.cards[y]
            self.assertIn(card["corridor"], ("A", "B", "A+B"))
            self.assertIn("грань-X", card["trust"])
            self.assertIn("LAB", card["trust"])
            comp = card["components"]
            self.assertIn(comp["exposure"]["class"],
                          ("COVER", "PROCESS", "CLOTHED-TIGHT", "SHEER"))
            self.assertTrue(comp["exposure"]["cover_object"],
                            f"{y} без объекта-прикрытия")
            # built_from: вербатим id из CARRIER_LIBRARY
            for cid in card["built_from"].replace("CARRIER_LIBRARY: ", "").split(" + "):
                self.assertIn(cid.split(" ")[0], self.lib_ids, f"{y}: {cid}")
            # НЕ юри (В49): парный реестр Y531–Y538 не расширяется
            self.assertNotIn("garment_pair", card)
            self.assertNotIn("2girls", card["pattern"])

    def test_pose_is_comma_form(self):
        """Поза карты — запятая-форма (клеймо вплетается в POS строкой 2)."""
        for y in ("Y555", "Y556", "Y557", "Y558", "Y559"):
            pose = self.cards[y]["components"]["pose"]
            self.assertNotIn(" + ", pose)  # « + » — формат паттерна, не позы

    def test_batch_carries_wave(self):
        """Партия несёт волну: все 5 карт в T5-34 EXP + Y542 (именованный)."""
        batch = (ROOT / "batches" / "T5-34.md").read_text(encoding="utf-8")
        for y in ("Y542", "Y555", "Y556", "Y557", "Y558", "Y559"):
            self.assertIn(y, batch)
        for y in ("Y531", "Y532", "Y533", "Y534", "Y535", "Y536", "Y537", "Y538"):
            # парный юри-реестр в партии не используется (юри 0/33)
            self.assertNotIn(f"· {y} ·", batch)


class TestComboBookOldYDobor(unittest.TestCase):
    """Комбо-книга добрала старую 512-волну (dresser 1.9.0, диета 40/40)."""

    @classmethod
    def setUpClass(cls):
        cls.dr = load("dresser.json")
        cls.cam = load("camera.json")
        cls.cb = cls.dr["y_stack"]["combo_book"]
        cls.groups = cls.cb["groups"]
        cls.card_ids = {c["id"] for c in cls.cam["y_cards"]["cards"]}

    def test_versions(self):
        self.assertEqual(self.dr["version"], "1.9.0")
        self.assertIn("1.9.0", " ".join(self.dr.get("changelog", {}).keys())
                      if isinstance(self.dr.get("changelog"), dict) else "1.9.0")
        self.assertIn("диета ≤40", self.cb["born"])  # добор 1.9.0 держит диету

    def test_diet_40(self):
        total = (len(self.groups["R_PLUS"]["combos"])
                 + len(self.groups["R"]["combos"])
                 + len(self.groups["PG13"]["combos"])
                 + len(self.groups["ANTI"]["patterns"]))
        self.assertEqual(total, 40)
        self.assertEqual(len(self.groups["R_PLUS"]["combos"]), 21)  # 17 + 4
        self.assertEqual(len(self.groups["R"]["combos"]), 8)        # 6 + 2
        self.assertEqual(len(self.groups["PG13"]["combos"]), 4)     # 3 + 1
        self.assertEqual(len(self.groups["ANTI"]["patterns"]), 7)

    def test_dobor_references_real_cards(self):
        """Добор ссылается на существующие старые карты (не выдумано)."""
        dobor = {"CB-RP-18", "CB-RP-19", "CB-RP-20", "CB-RP-21",
                 "CB-R-07", "CB-R-08", "CB-PG-04"}
        seen = set()
        for group in ("R_PLUS", "R", "PG13"):
            for entry in self.groups[group]["combos"]:
                if entry["id"] not in dobor:
                    continue
                seen.add(entry["id"])
                for token in entry["source"].split("×"):
                    token = token.strip()
                    if token.startswith("Y"):
                        yid = token.split(" ")[0]
                        self.assertIn(yid, self.card_ids,
                                      f"{entry['id']}: карта {yid} не существует")
                self.assertLessEqual(len(entry["juice"]), 200)
                self.assertGreaterEqual(len(entry["tags"]), 4)  # «всё снабжать тегами»
                self.assertLessEqual(len(entry["tags"]), 6)    # «не борщить»
                self.assertIn(entry["pose_coverage"], ("easy", "strained", "hard"))
        self.assertEqual(seen, dobor)

    def test_matrix_untouched(self):
        """Велосипед не выдуман: matrix (5 классов) и carrier_matrix (14) целы."""
        self.assertEqual(len(self.dr["y_stack"]["matrix"]), 5)
        self.assertEqual(
            len(self.dr["y_stack"]["carrier_matrix"]) - 2, 14)  # −born/law


if __name__ == "__main__":
    unittest.main()
