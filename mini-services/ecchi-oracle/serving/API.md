# ECCHI-ORACLE — API-контракт для thread5 (v3, эпоха В34/В35)

Сервис: `mini-services/oracle-service` (bun, `bun --hot`). Порт — env
`ORACLE_PORT` (дефолт **3031**), хост — env `ORACLE_HOST` (дефолт
**127.0.0.1**, 2026-11-20: наружу — только через платформенный прокси).
Из `tools/` thread5: `http://localhost:3031/<action>`.
Прилавок НЕ ходит в оракул напрямую — общее знание (camera.json/gates.json)
читается независимо с обеих сторон (THREAD-CHAIN.md §5).

Все ответы — JSON. Ошибки: `{ "error": "..." }` + 4xx/5xx (500 — общий
`internal error`, детали в логе сервиса).

Эпоха: **В34/В35 (T5-25+)** — гейты 1.15.0, raw-plus 2.2.0, клеймо = вплетённый
смысл (метка в POS запрещена). Реестр карт: env `THREAD5_ROOT` → `specs/camera.json`
рядом с чекаутом (текущая версия — 1.16.0, **521 карта**) → fallback taxonomy/corridors.json.

---

## GET /health

```json
{ "ok": true, "service": "ecchi-oracle", "port": 3031,
  "layers": ["rule-engine", "llm", "vision"],
  "era": "Y-STAMP v1.15.0 (В34/В35: вплетение 1:1, метки в POS запрещены)",
  "camera_registry": "1.16.0", "cards_indexed": 521 }
```

## GET /taxonomy

Машиночитаемая таксономия: шкала марок (SFW/PG-13/R/R+/X/XXX с сигналами),
коридоры A/B/A+B, Y-карты, **y_stamp** (формат/позиция/правила), **combo_doctrine**,
**В33**, **triage_v2**, 14 классов носителей, safety-флоры.

## GET /dataset

Индекс датасета: stats (total/train/val/by_category — 509 примеров · 15 категорий,
включая y-stamp / triage-v2 / honesty / combo-doctrine / influence) + сэмплы
всех примеров (id, category, split, question, answer) + `broken_lines` —
счётчик битых строк (2026-11-20: не молча) — для аудита знаний модели.
Индекс кэшируется по mtime файлов датасета.

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
  "card_id": "Y29" }
```

`card_id` необязателен: карта берётся из поля, из Y-card в POS или из шапки.
Лимит: pos ≤ 20 000 символов (413). Нестроковый `pos` — 400 (2026-11-20,
раньше долетал до движка и ронял сервис в TypeError-500).

Ответ:

```json
{
  "verdict": "FAIL",                  // PASS | WARN | FAIL (сумма проверок)
  "self_certified": true,             // бейдж R+ без коридора в физике POS (В33)
  "В33_honesty": "...",               // подсказка честности при self_certified
  "stamp": { "card_id": "Y29", "weaved": true, "registry_version": "1.16.0", "era": "..." },
  "checks": [ ... ],                  // claimPhysics + yStampChecks(1.15.0) + claimVisibility
  "warnings": [...], "fixes": [...],
  "one_minute_test": "..."
}
```

## GET|POST /ystamp — печать клейма из карты (клавиша паспорта)

```json
{ "card": "Y29" }
```

Реестр — camera.json thread5 (текущая версия 1.16.0, 521 карта; диапазон Y1–Y521).
Ответ (эпоха В34: **weave** — единственный текст, легальный в POS;
**stamp_metadata** — паспорт-метка, в POS НЕ печатается):

```json
{
  "card_id": "Y29",
  "era": "gates 1.15.0 — В34/В35: клеймо = вплетённый смысл, метки в POS запрещены",
  "weave": "<паттерн карты 1:1 с физикой — строка 3 POS>",
  "weave_rules": {
    "position": "строка 3 POS: после claim-строки, до деталей (LAWS §17.1)",
    "doctrine": "паттерн карты копипастом 1:1 с физикой ЦЕЛИКОМ (В35)",
    "banned_in_pos": ["строка-метка Y-STAMP:", "«класс» в кавычках", "CAM-коды", "corridor-токен"],
    "camera_note": "камера — отдельным камерным кластером OPENER",
    "corridor_note": "коридор — физикой claim-строки (В31)"
  },
  "stamp_metadata": "Y-STAMP: Y29 «...» × ... · corridor A",
  "class": "COVER", "corridor": "A", "camera": "...", "pattern": "...",
  "trust": "...", "built_from": null,
  "В33_note": null,
  "camera_version": "1.16.0"
}
```

Формат синхронизирован с прилавком (`/api/t5/ystamp`, `src/lib/t5/ystamp.ts`)
и гейтом yStamp (gates 1.15.0). Неизвестная карта — 404 со счётчиком карт.

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

→ `{ tier, ycard, ycard_found, corridor, trust, pos_skeleton, neg, header, checklist, reminder }`
— RAW+ скелет с заявкой по карте, NEG-зеркалом и шапкой слота.
`ycard_found: false` (2026-11-20) — карта не найдена в реестре: скелет
построен без неё, проверь id.

## POST /ask — LLM-оракул

```json
{ "question": "Почему cameltoe не работает как заявка?", "mode": "distill" }
```

Лимит: question ≤ 32 000 символов (413). Персона подаётся системным ходом (2026-11-20).

- `mode: "distill"` (дефолт) — полный мозг: системный промпт `distill/system_prompt.txt`
  (знание датасета: законы, коридоры, Y-карты, носители, рендер-факты, флоры).
- `mode: "short"` — только персона (демо разницы «до файнтюна»).

Ответ: `{ "question", "answer", "mode", "system" }`.

## POST /vision — анализ картинки (+ триаж v2)

```json
{ "image_base64": "<base64>", "mime": "image/jpeg", "detailed": true,
  "file_tag": "T5-24 P08", "file_name": "P08 - zipper-half-spine.webp", "label": "R+" }
```

Лимиты (2026-11-20): base64 ≤ ~8 МБ картинки (413), mime — только
`image/png|image/jpeg|image/webp` (400).

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
                            "card_id": slot.y_card},
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

def oracle_weave(card_id: str) -> str:
    r = requests.get(f"http://localhost:3031/ystamp", params={"card": card_id}, timeout=15)
    r.raise_for_status()
    return r.json()["weave"]      # В34: вплетение 1:1 из карты — строка 3 POS;
                                  # stamp_metadata — только паспорт, в POS не идёт
```

Счётчики батча: `self_certified_Rplus = sum(audit(s)["self_certified"] for s in slots if s.tier == "R+")` ·
`weaved = sum(1 for s in slots if audit(s)["stamp"]["weaved"])` (цель: = числу карт) ·
`drift_count = sum(1 for f in renders if triage(f)["drift"])`.

---

## Changelog контракта

- **v3 (2026-11-20)**: `weave`/`stamp_metadata` вместо `stamp`/`position` в
  /ystamp (В34); /audit `stamp = {card_id, weaved, registry_version, era}`;
  лимиты /ask 32k · /vision ~8 МБ + mime-whitelist · /audit pos-coerce;
  500-е не светят внутренности; HOST/PORT из env; /dataset mtime-кэш +
  broken_lines; /volt ycard_found; реестр 1.16.0 (521 карта).
- v2 (2026-11-18, RESYNC-1.15.0): yStampChecks перевёрнут под В34/В35.
