#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""T5-29 вердикт, исполнение №2: specs/gates.json 1.17.0 → 1.18.0.

Пять зубов на уроки В39–В43 (вердикт T5-29, «сделай так, чтобы ты никогда
нахуй больше таких ошибок не повторял»):
  voltCore       В39  вольт-ядро + перемешивание (FAIL с T5-30)
  raceCast v2.0  В40  кины — опция: окно 0–10 вместо вилки 12–14 (FAIL с T5-30)
  exquisiteMain  В41  EXQUISITE в мейнах 1–4 (FAIL с T5-30)
  expHypothesis  В42  EXP-клетки несут H-XX из полки гипотез (FAIL с T5-30)
  ratingTruth    В43  рейтинг = состав, не заявка (FAIL за ложный R+ с T5-30)

Эра: applyFrom 30 — T5-29 и старшие задним числом НЕ бьются (квитанции
заперты, CI на свежайшей сданной партии остаётся PASS); --retro показывает
пробелы WARN-ами (прецедент yStamp/paletteSkin).
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GATES_PATH = ROOT / "specs" / "gates.json"

VERDICT_REF = (
    "2026-11-22, вердикт T5-29: «Но сделай так, чтобы ты никогда нахуй больше "
    "таких ошибок не повторял»"
)

g = json.loads(GATES_PATH.read_text(encoding="utf-8"))
assert g["version"] == "1.17.0", f"ожидалась 1.17.0, стоит {g['version']}"

# ── В40: raceCast v2.0 — кины опция, человек основа ──────────────────────
g["raceCast"] = {
    "min": 0,
    "max": 10,
    "rfMax": 2,
    "quarantine": g["raceCast"].get("quarantine", ["R30"]),
    "applyFrom": 30,
    "failFrom": 30,
    "mode": "warn",
    "note": (
        "Каст кинов policy v2.0 (вердикт T5-29, пункт 3: «почему у нас везде "
        "кины, если кины - опция, а не основа»): ЧЕЛОВЕК — основа мейн-каста, "
        "кин — опция/приправа, доля кинов < половины (≤ 10 из 21). Policy v1.8 "
        "«вилка 12–14» была ошибкой конвейера (T5-27/28/29 ходили с 12–13 кин) "
        "и отменена этим вердиктом. Статусы active/gold по races.json, RF ≤ 2, "
        "карантин R30 (Frog-kin, вердикт T5-07) — как было. Код расы читается "
        "из шапки слота (R##), «human» — без кода. С batch ≥ failFrom выход за "
        "окно = FAIL (В40)."
    ),
}

# ── В39: voltCore — вольт-ядро + перемешивание ───────────────────────────
g["voltCore"] = {
    "born": (
        "2026-11-22, вердикт T5-29, пункты 2 и 4: «Какой перевес в Niche, если "
        "основная масса должна быть - волт» + «почему волт и ниша идут подряд, "
        "хотя должно быть вперемешку»"
    ),
    "law": (
        "ВОЛЬТ-ЯДРО (В39): основная масса мейнов — VOLT (Закон 24 / NICHE.md §В: "
        "R+×14 · R×7; дрейф T5-27/28/29 молча перевернул её в 7/14 и 9/12). "
        "NICHE — приправа (5–8 слотов: чудо обязано присутствовать, density "
        "floor §5). Жанры идут ВПЕРЕМЕШКУ: бег одного класса (вольт-масса / "
        "ниша) подряд ≤ 3 слотов — жанровые блоки-акты запрещены. EXQUISITE "
        "считается в вольт-массе (ультра-регистр)."
    ),
    "applyFrom": 30,
    "failFrom": 30,
    "voltMin": 13,
    "nicheMin": 5,
    "nicheMax": 8,
    "maxRun": 3,
}

# ── В41: exquisiteMain — ультра-регистр в мейнах ─────────────────────────
g["exquisiteMain"] = {
    "born": (
        "2026-11-22, вердикт T5-29, пункт 5: «где Exquisite в основной теме»"
    ),
    "law": (
        "EXQUISITE В МЕЙНАХ (В41): ультра-регистр живёт не только на "
        "ОС-канон-тейпе — в мейн-массе 1–4 EXQUISITE-слота на батч (доктрина "
        "NICHE.md §Б: «ездит по вайбу: 1–2 слота на батч, до 4, когда тема "
        "богата»). T5-29 сдал мейны с нулём EXQUISITE — нарушение. EXQUISITE "
        "входит в вольт-массу voltCore."
    ),
    "applyFrom": 30,
    "failFrom": 30,
    "min": 1,
    "max": 4,
}

# ── В42: expHypothesis — EXP проверяет штуки ─────────────────────────────
g["expHypothesis"] = {
    "born": (
        "2026-11-22, вердикт T5-29, пункт 6: «Почему EXP слоты следуют теме, "
        "если они должны проверять штуки. Ты тратишь мощность вообще не на то, "
        "что надо»"
    ),
    "law": (
        "EXP = ПОЛКА ГИПОТЕЗ (В42): каждая EXP-клетка несёт ОДНУ переменную из "
        "specs/open-hypotheses.json — id H-XX в строке «ТЕСТ (⚗ …)» тела слота. "
        "Тема партии НЕ кастует EXP-клетки (LAWS §5: «тема-слова батча в EXP не "
        "входят»; T5-29 нарушил: 9 монстров-резидентов данжа). «Полка отдыхает» "
        "незаконна: заказ автора на кандидатов/комбо/палитры исполняется КАК "
        "гипотезы (кандидат-механика = H-13, open-hypotheses.json 1.2.0). Одна "
        "гипотеза ≤ 2 клеток (A/B-пара с одной переменной)."
    ),
    "applyFrom": 30,
    "failFrom": 30,
    "hypIdRe": "H-\\d{2}",
    "testLineRe": "ТЕСТ\\s*\\(⚗",
    "maxPerHyp": 2,
}

# ── В43: ratingTruth — рейтинг = состав ──────────────────────────────────
g["ratingTruth"] = {
    "born": (
        "2026-11-22, вердикт T5-29, пункт 7: «Несоответствие рейтингу "
        "присутствует. Делай отладку системы которая за это отвечает. "
        "Не соответствуют рейтингу: почти все слоты, кроме: 4, 11, 18, 27»"
    ),
    "law": (
        "РЕЙТИНГ-ЧЕСТНОСТЬ (В43): рейтинг слота = что кадр несёт СОСТАВОМ, а "
        "не что заявка декларирует. Заявка-строка («the X is the claim, "
        "Y-made») не делает слот R+. Прикрытие ПАНЕЛЬЮ ткани (платье/лиф/биб/"
        "топ/тюль/мостик/корсет — включая просвечивающие плёнки и статичную "
        "драпировку) держит потолок R. R+-доказательство ровно два: (а) "
        "транзиентный холд объекта РУКАМИ как единственная крышка груди "
        "(полотенце поймано на пол-скольжения, кулаками держит, нижний слой "
        "снят) или (б) bare-line со стрэпами — линии, не панели. R-доказательство: "
        "слип бретели бельевого класса / мокрая кожа по рёбрам / tan lines / "
        "поле голой спины / интим-геометрия с партнёром (дип, посадка на "
        "колени зрителю) / ноги-демонстрация. PG-13: мидрифф, плечи, бок, "
        "бёдра сквозь ткань, слип бретели платья. Ложный R+ бейдж = FAIL "
        "(наследие В33), R↔PG-13 дрейф = WARN. Калибровка на ground truth "
        "T5-29: 33/33 — совпали P04/P11/P18/P27, помечены остальные 29 "
        "(docs/POSTMORTEM-T5-29.md)."
    ),
    "applyFrom": 30,
    "failFrom": 30,
    "bareClaim": ["nothing underneath"],
    "breastRead": ["breast shape", "chest line", "breast line"],
    "handHold": ["fists", "hauling", "haul of", "hauled", "gripping"],
    "strapOnly": ["chest's bare line", "straps covering the chest", "bare chest"],
    "panels": [
        "dress", "top", "tee", "bib", "halter", "corset", "tulle", "organza",
        "kimono", "robe", "veil", "pinafore", "apron", "tank", "sundress",
        "jersey", "wetsuit", "rash guard", "shirt", "blouse", "raincoat",
        "leotard", "bodysuit", "sweater",
    ],
    "offMarkers": [
        "peeled", "out of the sleeves", "caught at the elbow", "slipping off",
        "off one shoulder", "half-off", "unbuckled", "sagging",
        "pushed to both elbows", "slid to the elbows", "worn open",
        "cardigan off",
    ],
    "rTokens": {
        "wet_skin": [
            "sheeting down the ribs", "down the ribs", "tan lines",
            "sunburned shoulder", "wet skin",
        ],
        "partner_geometry": [
            "held mid-dip", "astride the viewer", "astride the seated",
            "over the missing arm", "hand-span from the lens",
        ],
        "display_geometry": [
            "legs raised and crossed at the ankle above the hips",
        ],
        "bare_back": ["the back bare", "bare back", "leaving the back bare"],
    },
    "window": 100,
}

g["version"] = "1.18.0"
GATES_PATH.write_text(json.dumps(g, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("gates.json → 1.18.0: voltCore · raceCast v2.0 · exquisiteMain · expHypothesis · ratingTruth")
print("секции:", len([k for k in g if not isinstance(g[k], (str,))]))
