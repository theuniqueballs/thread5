# -*- coding: utf-8 -*-
"""Канонизация Qwen (T5-19 P13 'gold-thread-spool' → ОС) по приказу автора 2026-11-13.
Прецеденты: Hana (конверсия приказом «выдай всё, что нужно выдать ОС. Таро и т.д.»),
Una (PH-REWRITE: канон = PH-промпт автора). Таро/элемент/знак — assistant-assigned,
pending author veto. Канон 2.9.0 → 2.10.0."""
import json

PATH = 'specs/oc-canon.json'
d = json.load(open(PATH, encoding='utf-8'))

PH = ("A three-quarter medium shot from chest height features a young woman with a supple "
      "build, positioned centrally as she interacts with a glowing golden thread. She has "
      "honey-blonde hair tied in loose high pigtails, amber fox-patient eyes, and perked fox "
      "ears with soft pink inner fur. She wears a tie-front blouse knotted at the sternum over "
      "a flowing satin skirt; a slip beneath clings to her skin due to the thread's static "
      "charge. Her smoke-grey fox tail acts as a counterweight, balancing her posture as she "
      "reels gold thread onto her wrist in tight, even rows. The line of gold thread arrives "
      "from a dawn-lit slit in a nearby curtain. The scene is bathed in a warm palette of "
      "honey, amber, and dawn-cream, with the golden thread providing a bright accent. The "
      "lighting is soft morning light, causing her pigtails to flick slightly. The style is a "
      "high-quality 2D anime illustration with a serene, patient mood.")

qwen = {
    "name": "Qwen",
    "tarot": ("8 of Pentacles (assistant-assigned 2026-11-13, pending author veto) — ПЕРВАЯ "
              "младшая аркана канона: все 22 старших заняты к 2026-11-08 (Liebe IV закрыл "
              "колоду). Карта терпеливого ремесла: ряд за рядом, та же работа, доведённая до "
              "верного ряда; ни одна петля не сходит раньше срока. Если вето требует старшей "
              "карты — свободных нет, будет конфликт (решение за автором)."),
    "element": ("THREAD (assistant-assigned, pending author veto) — золотая линия: ровное "
                "натяжение, ровные ряды; нить приходит к ней сама, она только держит ряд. "
                "НЕ путать с Meine WEFT (уток — уже полотно): THREAD — единственная линия ДО "
                "полотна; Meine ткет, Qwen принимает."),
    "zodiac": ("Virgo (SHARED w/ Ash + Meine — третий Virgo, flagged; assistant-assigned "
               "2026-11-13, pending author veto) — знак верстака: терпение, точный ряд, руки, "
               "которые повторяют движение, пока ряд не станет ровным."),
    "birth": ("promoted from T5-19 P13 'gold-thread-spool' (VOLT мейн · R03 Kitsune · R+ "
              "delivered; вербатим вердикта T5-19 2026-11-11: «13 крутой персонаж, заберём её "
              "пожалуй к себе в ОС, чуть позже уточню») + PH-промпт автора (чат 2026-11-13) как "
              "канон-референс с приказом «Обзываем её Qwen, даём таро и всё чё там надо» — "
              "вторая канонизация по PH-REWRITE (прецедент Una 2026-09-05), первая — из мейна "
              "(Hana шла из EXP)."),
    "race": ("R03 Kitsune (fox-kin; races.json v2.6.0) — fox ears perked small, single "
             "smoke-grey tail (хвост-противовес), warm ivory skin, pink-soft inner ear fur; "
             "R03-лок Sol (drooping ears + golden tail + silver-white) НЕ задет."),
    "appearance_lock": ("PH-REWRITE 2026-11-13 — PH-промпт автора P13 дословно (ниже) = канон; "
                        "суперсет над POS T5-19 P13, где расходятся — канон = PH (прецедент "
                        "Una). ТЕКСТ PH: «" + PH + "»"),
    "hair": ("honey-blonde hair tied in loose high pigtails (PH VERBATIM) — медовый блонд, "
             "свободные высокие хвостики, чёлки нет; POS-токены: honey-blonde hair in loose "
             "high pigtails. Урок F-016 помнит: цвет волос — рано в тег-ране."),
    "eyes": "amber fox-patient eyes (PH VERBATIM) — янтарь, лисье-терпеливый, круглый зрачок (не slit — не Sol)",
    "skin": "warm ivory skin (R03 реестр; PH о коже молчит — рендер T5-19 P13 держит тёплый рассветный тон)",
    "body_type": ("supple build, FAM-B (B4): medium breasts — PH «a young woman with a supple "
                  "build» + рендер P13: грудь читается принтом по узлу блузы, бёдра — через "
                  "статик-сатин"),
    "signature_marks": [
        "pink-soft inner ear fur — ловит первый свет рассвета (R03, рендер-подтверждено P13)",
        "ровные ряды золотой нити, намотанные на правое запястье (ряд не сходит; в кадрах без нити — слабый золотистый блеск-каллюс внутри запястья)",
    ],
    "emotional_register": ("serene, patient — она получает нить как зарплату утра; ни одной "
                           "лишней петли, ни одного лишнего слова (PH: «a serene, patient mood»)"),
    "anti_shield": ("black hair, silver-white hair, platinum hair, red hair, blue eyes, green "
                    "eyes, red eyes, heterochromia, slit pupils, drooping fox ears, nine "
                    "tails, twin tails, golden tail, tail limp, no tail, cold skin, pale grey "
                    "skin, tan skin, dark skin"),
    "collision_note": ("янтарные глаза брush Sol (slit-pupils, dark bronze skin) — Qwen держит "
                       "круглый лисье-терпеливый зрачок на warm ivory; honey-blonde брush Ana "
                       "(canon = render: blonde с cyan-teal прядями) — Qwen без единой "
                       "пряди-вставки; лисья семья: R03-лок Sol (drooping + golden + silver-white) "
                       "не задан, R50 Nine-tails (silver-tipped ears, веер из девяти) — у Qwen "
                       "perked-small и ОДИН smoke-grey хвост; smoke-grey tail уникален в ростере. "
                       "В одном кадре с Sol не ставить без контраста по коже."),
    "canonical_garment": ("tie-front blouse knotted at the sternum over a flowing satin skirt, "
                          "slip beneath (PH VERBATIM) — утренний регистр: статику несёт подклад, "
                          "не декор"),
    "id": "qwen",
    "active": True,
    "render_receipts": [
        "T5-19 P13 'gold-thread-spool' (VOLT мейн · R03 Kitsune · PL445 Thread-Spool Reel · P02_DAWN_AMBER · R+ delivered; вердикт T5-19 2026-11-11: «крутой персонаж» → промоция; рендер автора на PixAI до подачи в инбокс)",
    ],
    "wardrobe_policy": ("signature: завязка блузы на узел у грудины + сатиновая юбка поверх "
                        "подклада (PH VERBATIM); утренне-домашний регистр — ткань держит статику; "
                        "хвост R03 не рвёт юбку (tail-hem по реестру: скрытая прореха или хвост "
                        "поверх ткани)"),
}

assert 'Qwen' not in d['ocs'], 'Qwen уже в каноне'
d['ocs']['Qwen'] = qwen

# реестры
d['registries']['tarot'] = (d['registries']['tarot']
    .replace('Free cards for future OCs: нет — все 22 карты заняты (2026-11-08, T5-16 вердикт).',
             'Qwen — 8 of Pentacles (assistant-assigned 2026-11-13, вето открыто; ПЕРВАЯ младшая аркана — старшие 22/22 заняты). Free cards (старшие): нет — все 22 заняты (2026-11-08, T5-16 вердикт).'))
d['registries']['element'] = d['registries']['element'] + ' · Qwen — THREAD (assistant-assigned 2026-11-13, вето открыто)'
d['registries']['zodiac'] = d['registries']['zodiac'] + ' · Qwen — Virgo (shared w/ Ash + Meine, третий — flagged) (assistant-assigned 2026-11-13, вето открыто)'

# политика выборки + статус
d['selection_rule'] = d['selection_rule'] + ("\n(2026-11-13: 22 → 23 — Qwen promoted from T5-19 P13 "
    "'gold-thread-spool' по вердикту + PH-промпту автора; канон = PH-REWRITE (прецедент Una); "
    "таро 8 of Pentacles / THREAD / Virgo — assistant-assigned, pending veto; canon v2.10.0.)")
d['note_on_status'] = ("ACTIVE: 23 (22 прежних + Qwen с промоции 2026-11-13; Ama и Ila спят — "
    "active=null). 3 drawn per session by author vibe/theme fit, no forced rotation. Rae and Iya "
    "are INACTIVE RESERVE (added accidentally, never used, bios retained). SP-registry characters "
    "(Nicole, Puppet/Valentine, Ereshkigal/Tito_Lopes) live in download/SP_ORDERS.md, never in OC canon.")
d['notes'].append("2026-11-13 v2.10.0 — PROMOTION: Qwen (T5-19 P13 «gold-thread-spool», R03 Kitsune, "
    "мейн VOLT R+ delivered; вердикт: «13 крутой персонаж, заберём её пожалуй к себе в ОС») + PH-промпт "
    "автора как канон-референс (приказ: «Обзываем её Qwen, даём таро и всё чё там надо»). Вторая "
    "PH-REWRITE-канонизация (прецедент Una); первая промоция из мейна (Hana шла из EXP). Таро — 8 of "
    "Pentacles: ПЕРВАЯ младшая аркана канона (старшие 22/22 заняты с 2026-11-08); элемент THREAD "
    "(не WEFT — у Meine полотно); знак Virgo — третий (SHARED Ash+Meine, flagged). Всё pending veto.")

d['canon_version'] = '2.10.0'

json.dump(d, open(PATH, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('OK — Qwen канонизирована, canon_version =', d['canon_version'])
