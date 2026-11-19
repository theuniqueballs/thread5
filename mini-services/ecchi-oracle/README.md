# ECCHI-ORACLE-1

Компактная ЛЛМ-эксперт домена **«эччи-приёмы манги и аниме»**, обученная под конвейер
[theuniqueballs/thread5](https://github.com/theuniqueballs/thread5) (Batch-Prompt Conveyer Belt:
RAW+ батчи для аниме-рендера, Tsubaki.2 Pro → Yodayo).

Знает совершенно всё о приёмах эччи, применимых к картинкам разного содержания,
на полной шкале рейтингов проекта — с рабочим потолком **R+**:
`SFW → PG-13 → R → R+` · `X` — знание границы (X Cut = один жёсткий факт, слоты изъяты) ·
`XXX` — отказ всегда («хорошее эччи намного лучше любого порно»).

## Состав пакета

```
ecchi-oracle/
├── taxonomy/                # ЗНАНИЕ (источник датасета)
│   ├── rating-marks.json    #   шкала тиров: сигналы, закон суммы слоёв, HEAT, триаж
│   ├── techniques.json      #   энциклопедия: ~90 приёмов, 7 блоков, efficacy ●/○ по тирам
│   ├── corridors.json       #   коридоры A/B, Y-карты Y1-Y18, claimPhysics, rating_trust
│   ├── safety-floors.json   #   жёсткие флоры: XXX, anti-loli, генитальный лок, IP, leak guard
│   ├── renderer-facts.json  #   18 рендер-фактов + 9 звеньев салиенса + 14 классов носителей
│   └── source/              #   оригинальные спеки thread5 (rating-recipes/techniques/carriers, LAWS)
├── dataset/                 # МОЗГ
│   ├── seed-01..03.jsonl    #   120 ядро-примеров (законы/классификация/аудит/VOLT/vision)
│   ├── gen-a..e.jsonl       #   380+ примеров (техники/носители/аудит/факты/safety/учёт/клеймо/триаж)
│   ├── train.jsonl / val.jsonl   # 463 / 46 (сплит по категориям, seed 1337)
│   ├── build.py             #   пересборка сплитов
│   └── stats.json           #   509 примеров · 15 категорий (эпоха Y-STAMP)
├── training/                # ОБУЧЕНИЕ
│   ├── train_lora.py        #   QLoRA (TRL SFTTrainer, 4-bit nf4, r16α32)
│   ├── merge_export.py      #   слияние адаптера → полные веса
│   ├── eval_oracle.py       #   boundary-пробы (XXX/loli/X) + tier-вердикты + качественный дамп
│   ├── requirements.txt
│   └── README.md            #   быстрый старт (одна GPU / Colab T4), GGUF/Ollama
├── integration/
│   └── THREAD-CHAIN.md      #   карта внедрения в цепь треда + промпты Т1-Т4 + цепочка действий
├── serving/                 # ИНТЕГРАЦИЯ
│   ├── API.md               #   контракт сервиса :3031 (rate/audit/ystamp/volt/triage/ask/vision)
│   └── client_example.py    #   python-клиент для tools/gates.py
└── distill/
    └── system_prompt.txt    #   дистиллят знания — системный промпт LLM-режима до файнтюна
```

## Модель

- **База**: Qwen/Qwen2.5-1.5B-Instruct (RU+EN, сильна с тегами). Альтернативы: Qwen2.5-3B, Llama-3.2-3B, SmolLM2-1.7B.
- **Метод**: QLoRA 4-bit NF4, r=16 α=32, все проекции; lr 2e-4 cosine, 3 эпохи, seq 2048, seed 1337.
- **Объём**: 509 примеров / ~380k токенов (эпоха Y-STAMP: +y-stamp, +triage-v2, +honesty В33, +combo-doctrine, +influence). Одна GPU ≥16 ГБ или Colab T4, 40-70 минут.
- **Проверка**: eval_oracle.py — 4 boundary-пробы (XXX-запросы и child-код → отказ с возвратом в R+)
  + tier-вердикты на val + качественный дамп.

## Категории знания (датасет)

| Категория | Примеров | Что умеет |
|---|---|---|
| techniques | 71 | энциклопедия приёмов (таксономия 1.1.0, 120 записей): panchira → zettai ryouiki → golden-ходы T5-24, ●/○-карты по тирам |
| volt | 71 | сборка слотов RAW+ по 7 шагам VOLT, Y-карты, NEG-зеркала, токен-закон |
| classify | 47 | тир по тегам/описанию: сигналы → слои → сумма → коридор |
| carriers | 46 | 14 классов носителей CARRIER_LIBRARY, core-4, deg L/M/H |
| audit | 44 | claimPhysics: ловит самосертификацию R+ (болезнь T5-23) |
| vision-desc | 39 | разбор картинок по протоколу: VLM-описание → тир + триаж |
| render-facts | 36 | поведение Tsubaki.2/Yodayo: cameltoe мёртв, №28, P21-золото, мёртвые ткани |
| accounting | 28 | fact≠label, квоты, пятистрочные отчёты, HEAT, trust-обновления |
| safety | 28 | флоры, XXX-отказ, anti-loli, NEG-гигиена №25, X Cut hold |
| laws-tier | 10 | шкала, закон суммы слоёв, X Cut, жанровые дефолты |
| y-stamp | 32 | клеймо Y-STAMP: формат/позиция/гейты, комбо-Y доктрина, «—» не выносит R+ |
| triage-v2 | 22 | инбокс-триаж: слот-тип, fact-рейтинг (шкала автора), drift, паттерны неудач |
| honesty | 13 | В33 пиздёж-бани: честность в обе стороны, failFrom 25, «не получилось» легально |
| combo-doctrine | 12 | поза=скелет, карта=сборка, слот=от карты; обёртки Y38-Y512, built_from |
| influence | 10 | модель воздействия: 4 слоя + объект-посредник + EXP-закон |

## Инференс (три слоя, один контракт)

1. **Rule-engine** (детерминированный, без GPU) — `mini-services/oracle-service` :3031:
   `/rate` (скоринг тиров), `/audit` (claimPhysics + yStampGate + В33 + claimVisibility),
   `/ystamp` (клеймо 1:1 из camera.json, реестр 512 карт), `/volt` (скелеты по Y-картам),
   `/triage` (триаж v2 по тексту).
2. **LLM-оракул** — `/ask`: до файнтюна работает на дистилляте (`distill/system_prompt.txt`, эпоха Y-STAMP),
   после — на адаптере (Ollama/GGUF или vLLM), контракт не меняется.
3. **Vision** — `/vision`: картинка → VLM-описание по протоколу → тир + триаж v2
   (X-фильтр → слот-тип → fact-рейтинг → drift) + рекомендации.

Демо-панель (прилавок): `/` этого проекта — плейграунд всех пяти инструментов,
таксономия, браузер датасета, обучение, контракт интеграции.

## Внедрение в цепь треда

Карта петли, готовые промпты Т1-Т4 (тема→карта темы / аудит слота / триаж рендера / сборка от карты)
и цепочка действий: `integration/THREAD-CHAIN.md`. Эпоха: **Y-STAMP (T5-25+)** — гейты 1.14.0,
raw-plus 2.1.0, доктрина комбо-Y (512 карт), В33 «пиздёж-бани».

## Этика и границы (вшиты в данные и поведение)

- Рабочий диапазон **до R+**: эччи — это грань, а не факт.
- **X** — только распознавание границы (X Cut = один жёсткий факт); X-слоты в thread5 изъяты
  по умолчанию, возврат — прямой приказ автора.
- **XXX** — абсолютный отказ, всегда, без эвфемизмов.
- **Только взрослые тела**: anti-loli жёстко, возраст — формой тела; child-код — отказ.
- Тон: технический, non-graphic, filter-safe — как в документации самого thread5.

## Источники знания

Спецификации thread5 (verified by author verdicts): LAWS.md v1.8+ §3+§17 · rating-recipes.json v1.10 ·
rating-techniques.json v1.2.1 · carriers.json v1.0 · camera.json 1.15.1 (Y1-Y512) · raw-plus.json 2.1.0 ·
gates.json 1.14.0 (yStampGate, corridorAudit, comboPose) · RATING-REPAIR-2026-11-13 (гайд Коула, merged) ·
RATING-POSTMORTEM-T5-23 (claimPhysics В31) · вердикт T5-24 + АКТЫ 1-2 + В33 · batches/T5-25 ·
плюс общеаниме-лексикон эччи, откалиброванный по рендер-вердиктам T4/T5.
