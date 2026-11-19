# ECCHI-ORACLE — API-контракт для thread5 (v2, эпоха Y-STAMP)

Сервис: `mini-services/oracle-service` (bun, порт **3031**, `bun --hot`).
Из прилавка (браузер): `/api/oracle/<action>` (прокси Next.js).
Из `tools/` thread5: `http://localhost:3031/<action>`.

Все ответы — JSON. Ошибки: `{ "error": "..." }` + 4xx/5xx.

Эпоха: **Y-STAMP (T5-25+)** — гейты 1.14.0, raw-plus 2.1.0, доктрина комбо-Y, В33.
Реестр карт: camera.json thread5 (checkout `/home/z/thread5/specs/camera.json`), fallback — taxonomy/corridors.json.

---

## GET /health

```json
{ "ok": true, "service": "ecchi-oracle", "port": 3031,
  "layers": ["rule-engine", "llm", "vision"],
  "era": "Y-STAMP (T5-25+)",
  "camera_registry": "1.15.1", "cards_indexed": 512 }
```

## GET /taxonomy

Машиночитаемая таксономия: шкала марок (SFW/PG-13/R/R+/X/XXX с сигналами),
коридоры A/B/A+B, Y-карты, **y_stamp** (формат/позиция/правила), **combo_doctrine**,
**В33**, **triage_v2**, 14 классов носителей, safety-флоры.

## GET /dataset

Индекс датасета: stats (total/train/val/by_category — 509 примеров · 15 категорий,
включая y-stamp / triage-v2 / honesty / combo-doctrine / influence) + сэмплы
всех примеров (id, category, split, question, answer) — для аудита знаний модели.

---

## POST /rate — классификация тира

```json
{ "text": "1girl, handbra, sitting on bed, blush, upper body, slight from below" }
```

Ответ (rule-engine, детерминированный):

```json
{
  "verdict": "R+",                    // SFW | PG-13 | R | R+ | X
  "triage": "borderline",             // sfw | borderline | x
  "corridor": "A+B",                  // A | B | A+B | NONE
  "exposure_classes": ["COVER", "PROCESS"],
  "layers_engaged": 3,                // 0..4 по закону суммы слоёв
  "signals": { "pg13": [], "r": [], "rplus_hard": ["handbra"],
               "rplus_soft": [], "x_markers": [] },
  "layers": { "1_что_видно": 1, "2_как_показано": 1, "3_зачем_показано": 1, "4_что_дорисует": 0 },
  "x_risk_drivers": [],
  "approx_tokens": 15,
  "warnings": [],                     // флоры, мёртвые ткани, sheer без подслоя, R+ без коридора
  "law": "1 сигнал = PG-13/R · 3+ R-сигнала через 2+ слоя = R+ · X = один жёсткий факт"
}
```

## POST /audit — claimPhysics + Y-STAMP + claimVisibility + В33

```json
{ "badge": "R+", "corridor": "A",
  "pos": "masterpiece, upper body, 1girl, solo, dress zipper caught half-down...",
  "stamp": "Y-STAMP: Y29 «COVER» × ... × upper body + over-the-shoulder glance · corridor A",
  "card_id": "Y29" }
```

`stamp` и `card_id` необязательны: клеймо ищется в переданной строке и в самом POS.

Ответ:

```json
{
  "verdict": "FAIL",                  // PASS | WARN | FAIL (сумма проверок + клеймо)
  "self_certified": true,             // бейдж R+ без коридора в физике POS (В33)
  "В33_honesty": "...",               // подсказка честности при self_certified
  "stamp": { "card_id": "Y29", "stamp_class": "COVER", "pose": "...", "camera": "...", "corridor": "A" },
  "checks": [ ... ],                  // claimPhysics + yStampGate + claimVisibility
  "warnings": [...], "fixes": [...],
  "one_minute_test": "..."
}
```

Проверки claimPhysics: класс раскрытия (COVER/PROCESS/LINGERIE/CLOTHED-TIGHT/SHEER) · коридоры A/B ·
канал-токен (один, не стек) · салиенс заявки (позиция ≤60 токенов) · свет на зоне ·
self_certified для R+ без физики.

Проверки yStampGate (gates 1.14.0): клеймо присутствует и разбирается · паттерн = карте 1:1 (стемы) ·
класс клейма = карте · коридор клейма = карте · **В33: класс «—» не выносит R+/X** ·
клеймо исполняется телом POS (≥2 стемов вне строки клейма) · коридор клейма = полю Corridor: (WARN) ·
corridor «—» (WARN).

claimVisibility: видимый носитель заявки в первых двух строках POS (постмортем P13 T5-24).

## GET|POST /ystamp — печать клейма из карты (клавиша паспорта)

```json
{ "card": "Y29" }
```

Реестр — camera.json thread5 (1.15.1, 512 карт). Ответ:

```json
{
  "card_id": "Y29",
  "stamp": "Y-STAMP: Y29 «COVER» × dress zipper caught half-down at the spine + the palm pressed flat holding the dress front + glance back over the shoulder × upper body + over-the-shoulder glance · corridor A",
  "position": "строка 3 PROSE PLUS: после claim-строки NL-ядра, до SCENE (LAWS §17)",
  "class": "COVER", "corridor": "A", "camera": "...", "pattern": "...",
  "trust": "...", "built_from": null,
  "В33_note": null          // для обёрток «—»: «R+/X под этой картой = FAIL (В33)»
}
```

Формат 1:1 синхронизирован с прилавком (`/api/t5/ystamp`, `src/lib/t5/ystamp.ts`) и гейтом yStampGate.

## POST /triage — триаж v2 по тексту описания (акт 9, без vision)

```json
{ "description": "1girl, one-piece swimsuit, wet, upper body, slight from below",
  "file_tag": "T5-24 P08", "file_name": "P08 - zipper-half-spine.webp", "label": "R+" }
```

Ответ:

```json
{
  "description_engine": <rate-результат>,
  "triage_v2": {
    "x_verdict": "sfw | borderline | x",
    "slot_type": "main | OC | EXP | special | unknown",
    "slot_type_from": "file_tag | file_name | no match — нужен тег",
    "fact_rating": "R+ | Partial | R | PG-13 | SFW | X",
    "fact_rule": "шкала автора (R+ еле прикрытая / R suggestive...)",
    "label": "R+", "drift": "R+ ≠ fact PG-13" | null,
    "drift_note": "В33: завышение/занижение/помета",
    "patterns": [], "law": "fact по кадру, label — сверка; drift в обе стороны (В33)"
  }
}
```

Слот-типы по канону T5-22…24: P01–P03 = ОС · P04–P24 = мейн · P25–P33 = EXP · SO-NN = спец.

## POST /volt — скелет слота по Y-карте

```json
{ "scene": "ночная прачечная", "ycard": "Y1", "target": "R+" }
```

→ `{ tier, ycard, corridor, trust, pos_skeleton, neg, header, checklist, reminder }`
— RAW+ скелет с заявкой по карте, NEG-зеркалом и шапкой слота.

## POST /ask — LLM-оракул

```json
{ "question": "Почему cameltoe не работает как заявка?", "mode": "distill" }
```

- `mode: "distill"` (дефолт) — полный мозг: системный промпт `distill/system_prompt.txt`
  (знание 420 примеров: законы, коридоры, Y-карты, носители, рендер-факты, флоры).
- `mode: "short"` — только персона (демо разницы «до файнтюна»).
- После обучения на GPU: режим distill переключается на адаптер (Ollama/vLLM) — контракт не меняется.

Ответ: `{ "question", "answer", "mode", "system" }`.

## POST /vision — анализ картинки (+ триаж v2)

```json
{ "image_base64": "<base64>", "mime": "image/jpeg", "detailed": true,
  "file_tag": "T5-24 P08", "file_name": "P08 - zipper-half-spine.webp", "label": "R+" }
```

Конвейер: VLM снимает техническое описание по протоколу (кадр/одежда/поза/подача/свет/
жёсткий факт/приёмы) → rule-engine считает тир → **триаж v2: X-вердикт → слот-тип →
fact-рейтинг (шкала автора) → drift (label vs fact)** → (detailed) LLM даёт полный разбор.

Ответ: `{ "description", "engine": <rate-результат>, "triage_v2": {...}, "oracle", "oracle_error" }`.
Один файл на запрос (урок 502: CAP_PER_REQUEST=1, ретрай 1, fail-closed JSON).

---

## Интеграция в gates.py (пример)

```python
def oracle_audit(slot) -> dict:
    r = requests.post("http://localhost:3031/audit",
                      json={"badge": slot.tier, "corridor": slot.corridor, "pos": slot.pos,
                            "stamp": slot.stamp_line, "card_id": slot.y_card},
                      timeout=30)
    r.raise_for_status()
    return r.json()   # verdict + self_certified + stamp-checks → в квитанцию рядом с fact/label

def oracle_triage(render_file) -> dict:
    r = requests.post("http://localhost:3031/vision",
                      json={"image_base64": b64(render_file), "file_tag": render_file.tag,
                            "file_name": render_file.name, "label": render_file.label},
                      timeout=60)
    r.raise_for_status()
    return r.json()["triage_v2"]   # x_verdict + slot_type + fact_rating + drift

def oracle_stamp(card_id: str) -> str:
    r = requests.get(f"http://localhost:3031/ystamp", params={"card": card_id}, timeout=15)
    r.raise_for_status()
    return r.json()["stamp"]      # клеймо 1:1 из карты — в строку 3 PROMPT
```

Счётчики батча: `self_certified_Rplus = sum(audit(s)["self_certified"] for s in slots if s.tier == "R+")` ·
`stamps = sum(1 for s in slots if audit(s)["stamp"])` (цель: = числу карт) ·
`drift_count = sum(1 for f in renders if triage(f)["drift"])`.
