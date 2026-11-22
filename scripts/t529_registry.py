#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""T5-29 вердикт, исполнение №3: gate-registry.json 1.0.0 → 1.1.0 + validate.py.

Пять новых секций урока T5-29 (voltCore / raceCast v2.0 / exquisiteMain /
expHypothesis / ratingTruth) + закрывается дыра 1.17.0: yStack жил в
gates.json, но выпал из реестра и из REQUIRED-списка валидатора
(«объявлено ≠ отражено» — тот же класс бага, который реестр и закрывает).
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REG = ROOT / "specs" / "gate-registry.json"

reg = json.loads(REG.read_text(encoding="utf-8"))
assert reg["version"] == "1.0.0"

rows = reg["gates"]
have = {r["section"] for r in rows}

def upsert(row):
    for i, r in enumerate(rows):
        if r["section"] == row["section"]:
            rows[i] = row
            return
    rows.append(row)

# yStack — был в gates.json 1.17.0, но не в реестре (дыра закрыта)
if "yStack" not in have:
    upsert({
        "section": "yStack",
        "impl": ["check_ystack"],
        "receiptField": "y_stack",
        "test": None,
        "owner": "VENUS",
        "note": (
            "1.17.0 Y×CLOSET STACK (заказ 2026-11-21 после вердикта T5-28): "
            "одежда держит класс карты; между 1.17.0 и 1.1.0 реестра секция "
            "жила в gates.json БЕЗ строки реестра — дыра закрыта 2026-11-22 "
            "при внесении урока T5-29; прямой тест — видимый долг (null), "
            "эра проверяется живым прогоном T5-29"
        ),
    })

upsert({
    "section": "raceCast",
    "impl": ["check_race_cast"],
    "receiptField": "race_cast",
    "test": "tests/python/test_t529_lessons.py",
    "owner": "MERCURY",
    "note": (
        "v1.18.0 policy v2.0 (В40, вердикт T5-29 п.3 «кины - опция, а не "
        "основа»): человек — основа каста, кин — опция, окно 0–10 из 21 "
        "(вилка 12–14 policy v1.8 отменена); карантин/RF как были; FAIL с "
        "T5-30; тампер-тест: кин 13/21 → FAIL"
    ),
})
upsert({
    "section": "voltCore",
    "impl": ["check_volt_core"],
    "receiptField": "volt_core",
    "test": "tests/python/test_t529_lessons.py",
    "owner": "SOL",
    "note": (
        "В39 (вердикт T5-29 п.2+4): вольт-ядро мейнов по Закону 24 "
        "(вольт-масса VOLT+EXQUISITE ≥ 13, ниша 5–8) + перемешивание (бег "
        "жанра ≤ 3, блоки-акты запрещены); FAIL с T5-30; тампер-тест: "
        "T5-29 (7/14, бег 14) ловится в retro"
    ),
})
upsert({
    "section": "exquisiteMain",
    "impl": ["check_exquisite_main"],
    "receiptField": "exquisite_main",
    "test": "tests/python/test_t529_lessons.py",
    "owner": "SOL",
    "note": (
        "В41 (вердикт T5-29 п.5 «где Exquisite в основной теме»): 1–4 "
        "EXQUISITE-слота в мейн-массе, не только на ОС-тейпе; FAIL с T5-30; "
        "тампер-тест: T5-29 (0) ловится в retro"
    ),
})
upsert({
    "section": "expHypothesis",
    "impl": ["check_exp_hypothesis"],
    "receiptField": "exp_hypothesis",
    "test": "tests/python/test_t529_lessons.py",
    "owner": "FURNACE",
    "note": (
        "В42 (вердикт T5-29 п.6 «EXP должны проверять штуки»): каждая "
        "EXP-клетка несёт H-XX из specs/open-hypotheses.json в строке ТЕСТ; "
        "«полка отдыхает» незаконна, тема партии клетки не кастует; одна "
        "гипотеза ≤ 2 клеток (A/B); FAIL с T5-30; тампер-тест: T5-29 "
        "(9 клеток без H-XX) ловится в retro"
    ),
})
upsert({
    "section": "ratingTruth",
    "impl": ["check_rating_truth", "rating_implied"],
    "receiptField": "rating_truth",
    "test": "tests/python/test_t529_lessons.py",
    "owner": "FURNACE",
    "note": (
        "В43 (вердикт T5-29 п.7 «отладка системы рейтинга»): модель состава "
        "rating_implied() — bareClaim/strapOnly/handHold/panels/offMarkers/"
        "rTokens из gates.json; ложный R+ бейдж = FAIL (наследие В33), "
        "R↔PG-13 дрейф = WARN; калибровка ground truth T5-29: 33/33 "
        "(совпали P04/P11/P18/P27, помечены 29); FAIL с T5-30"
    ),
})

reg["version"] = "1.1.0"
reg["born_from"] += (
    " · 1.1.0 (2026-11-22, вердикт T5-29): пять секций урока В39–В43 "
    "(voltCore/raceCast v2.0/exquisiteMain/expHypothesis/ratingTruth) + "
    "закрыта дыра 1.17.0 (yStack жил в gates.json без строки реестра)"
)
REG.write_text(json.dumps(reg, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"gate-registry.json → 1.1.0: {len(rows)} секций")

# ── validate.py: REQUIRED_GATES_KEYS += пять новых + yStack ────────────
vp = ROOT / "tools" / "validate.py"
vt = vp.read_text(encoding="utf-8")
old = '''    # эры 1.8.0–1.16.0
    "negBase", "formatGate", "corridorAudit", "claimPhysics", "yCards",
    "yStamp", "comboPose", "conceptFlag", "negDressGuards", "detailsGate",
    "paletteSkin",
]'''
new = '''    # эры 1.8.0–1.16.0
    "negBase", "formatGate", "corridorAudit", "claimPhysics", "yCards",
    "yStamp", "comboPose", "conceptFlag", "negDressGuards", "detailsGate",
    "paletteSkin",
    # эра 1.17.0 (дыра закрыта 2026-11-22: жил в gates.json без реестра)
    "yStack",
    # эра 1.18.0 — уроки T5-29 (В39–В43)
    "voltCore", "exquisiteMain", "expHypothesis", "ratingTruth",
]'''
assert old in vt, "REQUIRED_GATES_KEYS не найден"
vt = vt.replace(old, new, 1)
vp.write_text(vt, encoding="utf-8")
print("validate.py: REQUIRED_GATES_KEYS + yStack + 4 новых секций")
