# -*- coding: utf-8 -*-
"""Тесты КОМБО-КНИГИ ПО РЕЙТИНГУ (dresser.json 1.9.0 y_stack.combo_book)
+ ЗАКОНА 3 «покрытие-в-позе» (rating-techniques.json 1.6.0).

Заказ автора 2026-11-27: «чекни датасет эччи оракла и забери всё... разберёшь комбо
по рейтингу, сопоставишь с одеждой, подберёшь хорошие и правильные, выделишь
повторяющиеся, сложные - снабдишь нужными тегами... слегка ужирнять, но не борщить...
для R+ достаточно просто прикрыть соски, а конкретно в позе - этого добиться сложней».

Пины:
1. rating-techniques.json 1.6.0 — ЗАКОН 3 (законы автора 1-2 не тронуты);
2. dresser.json 1.9.0 — y_stack.combo_book (третий стак после matrix и carrier_matrix;
   1.9.0 — добор старой 512-волны, диета 33→40 ровно);
3. порядок стака y_stack.order получил шаг 0 — комбо-книга до матрицы;
4. слаженность: Y-ссылки в camera.json, записи-источники в датасете оракула,
   полки в closet.json ∩ carrier_matrix, теги в словаре, диета ≤40 позиций.
"""
import json
import re
import unittest

# 2026-11-27: абсолютный путь песочницы ("/home/z/my-project") убит — на CI/чужом
# клоне его нет, тест падал ImportError вне песочницы (найден внешним аудитором
# при прогоне полного сьюта). Тот же корень, но от файла — переносимо.
from pathlib import Path as _P
ROOT = str(_P(__file__).resolve().parents[2])
SPECS = f"{ROOT}/specs"
DATASET = f"{ROOT}/mini-services/ecchi-oracle/dataset"

DR = json.load(open(f"{SPECS}/dresser.json"))
RT = json.load(open(f"{SPECS}/rating-techniques.json"))
CL = json.load(open(f"{SPECS}/closet.json"))
CAM = json.load(open(f"{SPECS}/camera.json"))

BOOK = DR["y_stack"]["combo_book"]
GROUPS = BOOK["groups"]
ALL_COMBOS = GROUPS["R_PLUS"]["combos"] + GROUPS["R"]["combos"] + GROUPS["PG13"]["combos"]
ANTI = GROUPS["ANTI"]["patterns"]


class TestPins(unittest.TestCase):
    def test_versions(self):
        self.assertEqual(DR["version"], "1.10.0")  # 1.10.0 — two_carrier В52/В53
        self.assertEqual(RT["version"], "1.7.0")  # 1.7.0 — volt_run (В45)
        self.assertIn("combo_book", DR["y_stack"])
        self.assertIn("combo_book", DR["y_stack"]["order"][:200])  # шаг 0 стака

    def test_rating_techniques_laws_intact(self):
        la = RT["principle"]["laws_author"]
        texts = " | ".join(la)
        self.assertIn("ЗАКОН 1", texts)   # tapeEvidence не тронут
        self.assertIn("ЗАКОН 2", texts)   # crotchFocus не тронут
        self.assertIn("ЗАКОН 3", texts)   # покрытие-в-позе влито
        self.assertIn("для R+ достаточно просто прикрыть соски", texts)
        self.assertIn("в позе", texts)
        self.assertIn("сложней", texts)
        self.assertEqual(len(RT["techniques"]), 166)  # техники 1.5.0 не тронуты

    def test_pose_coverage_law_block(self):
        pcl = BOOK["pose_coverage_law"]
        self.assertIn("2026-11-27", pcl["born"])
        self.assertIn("ПРИВЯЗАННОЕ", pcl["law"])
        self.assertIn("СВОБОДНОЕ", pcl["law"])
        self.assertEqual(set(pcl["gradations"]), {"easy", "strained", "hard"})

    def test_juice_doctrine(self):
        jd = BOOK["juice_doctrine"]
        self.assertIn("ОБЕЩАНИЕ", jd["law"])
        self.assertIn("ПОЛУРЕШЕНИЕ", jd["law"])
        self.assertIn("ПАУЗА", jd["law"])
        self.assertIn("НАСЛОЖЕНИЕ", jd["law"])
        self.assertIn("АНТИ-БОРЩ", jd["law"])  # не борщить — заказ автора


class TestBookStructure(unittest.TestCase):
    def test_groups_and_diet(self):
        self.assertEqual(set(GROUPS.keys()), {"R_PLUS", "R", "PG13", "ANTI"})
        total = len(ALL_COMBOS) + len(ANTI)
        self.assertLessEqual(total, 40, "снежный ком: книга распухла")
        self.assertEqual(len(GROUPS["R_PLUS"]["combos"]), 21)  # 17 + добор старой 512-волны ×4
        self.assertEqual(len(GROUPS["R"]["combos"]), 8)      # 6 + ×2
        self.assertEqual(len(GROUPS["PG13"]["combos"]), 4)  # 3 + ×1
        self.assertEqual(len(ANTI), 7)

    def test_combo_fields_complete(self):
        for c in ALL_COMBOS:
            for field in ("id", "name", "source", "corridor", "mech_groups",
                          "closet", "repeats", "complexity", "pose_coverage",
                          "tags", "juice", "anti_neg", "note"):
                self.assertIn(field, c, f"{c.get('id')}: нет поля {field}")
                self.assertTrue(c[field], f"{c.get('id')}: поле {field} пусто")

    def test_id_unique_prefixes(self):
        ids = [c["id"] for c in ALL_COMBOS] + [p["id"] for p in ANTI]
        self.assertEqual(len(ids), len(set(ids)), "дубль id в книге")
        for cid in ids:
            self.assertTrue(cid.startswith("CB-"), f"{cid}: не CB-префикс")
        rp = [c["id"] for c in GROUPS["R_PLUS"]["combos"]]
        self.assertTrue(all(i.startswith("CB-RP-") for i in rp))

    def test_tag_vocab_controlled(self):
        vocab = set(BOOK["tag_vocab"])
        # дисциплина: словарь ЗАКРЫТ (вне словаря тегов не бывает) и ограничен;
        # мёртвых тегов нет — каждый тег словаря реально используется книгой
        self.assertLessEqual(len(vocab), 50, "словарь тегов распух — борщ")
        used = set()
        for c in ALL_COMBOS:
            self.assertGreaterEqual(len(c["tags"]), 3, f"{c['id']}: голод по тегам")
            self.assertLessEqual(len(c["tags"]), 6, f"{c['id']}: борщ по тегам")
            for t in c["tags"]:
                self.assertIn(t, vocab, f"{c['id']}: тег {t} вне словаря")
                used.add(t)
        self.assertEqual(used, vocab, f"мёртвые теги словаря: {sorted(vocab - used)}")

    def test_juice_cap(self):
        for c in ALL_COMBOS:
            self.assertLessEqual(len(c["juice"]), 200, f"{c['id']}: сок-борщ >200")
            self.assertFalse(re.search(r"[а-яё]", c["juice"], re.I),
                             f"{c['id']}: juice должен быть EN claim-строкой (POS-язык)")

    def test_corridor_law(self):
        for c in GROUPS["R_PLUS"]["combos"]:
            self.assertIn(c["corridor"], ("A", "B", "A+B"),
                          f"{c['id']}: R+ без коридора — corridor law")
        for c in GROUPS["R"]["combos"] + GROUPS["PG13"]["combos"]:
            self.assertEqual(c["corridor"], "NONE",
                             f"{c['id']}: honest-тир обязан быть без коридора")

    def test_pose_coverage_all_gradations_in_rplus(self):
        pc = {c["pose_coverage"] for c in GROUPS["R_PLUS"]["combos"]}
        self.assertEqual(pc, {"easy", "strained", "hard"},
                         "закон покрытия-в-позе отражён не всеми градациями")
        hard = [c["id"] for c in GROUPS["R_PLUS"]["combos"] if c["pose_coverage"] == "hard"]
        self.assertGreaterEqual(len(hard), 3, "hard-комбо должно быть выделено (автор: «сложней, сильно сложней»)")
        self.assertIn("CB-RP-14", hard)  # lean-back: руки заняты опорой
        self.assertIn("CB-RP-09", [c["id"] for c in GROUPS["R_PLUS"]["combos"] if c["pose_coverage"] == "easy"],
                      "тейп-исключение (ЗАКОН 1) обязано остаться easy")

    def test_repeats_marked(self):
        rdef = BOOK["repeats_def"]
        self.assertEqual(set(rdef), {"core", "rare"})
        n_core = sum(1 for c in ALL_COMBOS if c["repeats"] == "core")
        self.assertGreaterEqual(n_core, 14, "повторяющиеся ядра не выделены")
        self.assertGreater(len(ALL_COMBOS) - n_core, 4, "редкие не выделены")


class TestCoherence(unittest.TestCase):
    """Слаженность: книга не воюет с живыми реестрами — не снежный ком."""

    def setUp(self):
        self.y_ids = {c["id"] for c in CAM["y_cards"]["cards"]}
        self.shelves = set(CL["shelves"].keys())
        self.ds_ids = set()
        for f in ("train.jsonl", "val.jsonl"):
            for line in open(f"{DATASET}/{f}"):
                self.ds_ids.add(json.loads(line)["id"])
        self.cm_shelves = {
            k: set(v["shelves"]) for k, v in DR["y_stack"]["carrier_matrix"].items()
            if isinstance(v, dict) and "shelves" in v
        }

    def test_y_refs_exist(self):
        for c in ALL_COMBOS:
            for yid in re.findall(r"\bY\d{1,3}\b", c["source"]):
                self.assertIn(yid, self.y_ids,
                              f"{c['id']}: Y-ссылка {yid} отсутствует в camera.json")

    def test_dataset_sources_exist(self):
        """Каждая запись-источник реально есть в датасете оракула (забрали всё — ничего не выдумано)."""
        for c in ALL_COMBOS:
            for ds in re.findall(r"\b(?:gen[ABCE]-\d{3}|seed-\d{3})\b", c["source"]):
                self.assertIn(ds, self.ds_ids, f"{c['id']}: {ds} нет в датасете")
        for p in ANTI:
            for ds in re.findall(r"\b(?:gen[ABCE]-\d{3}|seed-\d{3})\b", p["source"]):
                self.assertIn(ds, self.ds_ids, f"{p['id']}: {ds} нет в датасете")

    def test_closet_codes_exist_and_match_matrix(self):
        for c in ALL_COMBOS:
            core = [g for g in c["mech_groups"] if g not in ("G", "H")]
            self.assertTrue(core, f"{c['id']}: только усилители G/H — нет ядра")
            union = set()
            for g in core:
                self.assertIn(g, self.cm_shelves,
                              f"{c['id']}: класс {g} без полок в carrier_matrix")
                union |= self.cm_shelves[g]
            for s in c["closet"]:
                self.assertIn(s, self.shelves, f"{c['id']}: полки {s} нет в closet.json")
                self.assertIn(s, union,
                              f"{c['id']}: полка {s} вне объединения carrier_matrix {sorted(union)} ({core})")

    def test_no_registry_snowball(self):
        """Книга — раздел существующего y_stack, файлы не размножены; матрица/порядок не тронуты."""
        self.assertEqual(len(DR["y_stack"]["matrix"]), 5)      # 5 классов экспозиции целы
        self.assertEqual(len(DR["y_stack"]["carrier_matrix"]), 16)  # born+law+14 классов
        self.assertIn("yuri_quota", DR["y_stack"])              # В49 цела
        self.assertIn("carrier_first", DR["y_stack"])           # В45 цела
        self.assertEqual(len(CAM["y_cards"]["cards"]), 559)     # camera.json: 554 + волна «грань-X» Y555–Y559

    def test_anti_patterns_complete(self):
        for p in ANTI:
            self.assertTrue(p["pattern"] and p["why"] and p["fix"],
                            f"{p['id']}: ANTI обязан нести pattern/why/fix")
        names = " | ".join(p["name"] for p in ANTI)
        self.assertIn("КАТАЛОГ", names)
        self.assertIn("МОКРЫЙ", names)          # RF03 — 27 X-квитанций
        self.assertIn("HIGH-ПОЗА", names)       # T516


class TestSourceVerbatim(unittest.TestCase):
    """Сочность: juice-якоря — вербатим-формулы из сборок датасета, не самодел."""

    def test_key_juice_lines_from_dataset(self):
        book = json.dumps(BOOK, ensure_ascii=False)
        for frag in (
            "the bunched hem pressed flat over her chest by both folded arms",   # Y1 genC-001
            "dress zipper caught half-down at the spine",                        # Y29 genE-002
            "sleeve caught at the elbow fold",                                   # Y12 genC-009
            "apron, apron only, nothing underneath, bare back",                  # T113 genA-007
            "dry black tank plastered by rehearsal sweat",                       # №28 genC-017
            "both fists knuckle-deep in the terry",                              # Y4 genC-032
            "the hakama hem pinned under her shin weight",                       # Y11 genC-008
            "belt cinch stalled mid-pull against the stool's lean",              # Y15 genC-011
            "the skirt hem pulled taut across her thighs by the straddle",       # Y5 genC-003
            "fabric bridges taut across the ribs",                               # Y14 genA-042
            "crossbow strap torqued across her chest",                           # Y10 genC-007
            "matching lingerie set, garter belt, stockings",                     # genC-028
            "sports bra, boyshorts, bare feet",                                  # genC-025
            "pareo knotted low",                                                 # genC-027
        ):
            self.assertIn(frag, book, f"juice-якорь утерян: {frag}")


if __name__ == "__main__":
    unittest.main()
