# thread5
Batch-Prompt Conveyer Belt

Конвейер промпт-батчей для аниме-рендеров (Tsubaki.2 Pro → Yodayo).
Наследник THREAD 4 — на новом ядре, без посредников.

> **Статус: 5.2 BETA** (счётчики пересчитаны из живых реестров 2026-11-21
> версией двойного аудита: Коула/Grok «сложность цеха» + внешний
> архитектурный «источники истины»; внедрение — ниже в разделе
> «Инженерия»). Гигиена проведена 2026-11-02: винтаж T4, старые аудиты и
> челлендж-эксперимент — в `archive/2026-11-02-hygiene/`. Новый формат
> (NL + аниме-теги + PH) — проект в `docs/T5-1-BETA.md`, переезд —
> `HANDOVER-T5-1.md`. Анализ 5.2: `docs/PROJECT-REVIEW-5.2-2026-11-13.md`.

## Петля (всё, что имеет ценность)

```
тема (автор, чат)
  → контракт (писец показывает экспозицию в чат)
    → батч (файл в batches/, RAW+ формат)
      → рендер (автор, Tsubaki.2 Pro) → пост (Yodayo)
        → вердикт (автор, чат) → квитанции в живые документы
```

Чат — двигатель. Файлы — память. Больше ролей нет.

## Структура

- `batches/` — батчи T5-NN (RAW+ / данбуру-формат);
  рабочие артефакты сеансов — `batches/T5-NN/00-brief, 01-sol … 05-furnace`
  (бриф — по `_BRIEF-TEMPLATE.md`)
- `special/` — SPECIAL ORDERS: штучки вне цикла (заказы автора: подарки, приколы, одна сцена) — SO-NN.md, тот же RAW+ формат, без раскрытия темы
- `docs/ars/` — **ARS NOVEAU v2, солнечная система**: `00-OVERVIEW` (карта),
  `01-SOL` (ядро: идея, HEAT, истории, ЛУНА) → `02-MERCURY` (каст, ULTIMATE
  DICE, Дрессер) → `03-VENUS` (сцена) → `04-EARTH` (сборка POS/NEG) →
  `05-FURNACE` (ревью, блокнот `specs/furnace-ledger.json`)
- `docs/` — LAWS.md (физика системы), TASTE, RENDERER_FACTS, NICHE,
  ANTI-MOVES (библиотека гарантированного трупа), LIVING-NOTES (архив),
  STORAGE-AUDIT, **ENGINEERING** (инженерная карта: архитектура,
  контракты формата, тесты/CI, модель безопасности, реестр фиксов
  апгрейда 2026-11-20)
- `archive/` — гигиена 2026-11-02: винтаж T4 (EXAMPLE-T4-44, _TEMPLATE),
  обработанные аудиты, челлендж-эксперимент «Чистый лист» (+чемоданы)
- `specs/` — данные-активы (счётчики — из живых JSON, 2026-11-21: позы ×586 —
  poses 1.19.0; палитры ×260 — palettes 1.14.0 (волна 12 «раскраска
  выживания» P252–P260 в основном пуле); **Y-множество ×530 — camera.json
  1.19.0, Y-first + Y-STAMP (вплетение 1:1) + POV-якоря В37**; расы ×74 — races 2.7.0 (кин-оверхаул: clarifiers+gimmick+skin_type, LAWS §21);
  OC-канон ×29 — canon 2.13.0 (Nier+Noir); CLOSET ×121 предмет на 13 полках — closet 1.1.0 (exposure-классы, yStack; единственный активный каталог одежды, GAR — legacy); **bodytypes.json 1.0.0 — 24 типажа тел (пункт Е)**; **marks.json 1.0.0 — 42 метки, рейтинг-нейтральные (пункт И)**; **oc-candidates.json 1.0.0 — кандидаты в ОС, oc_hook (пункт Д)**;
  `gates.json` 1.17.0 (yStackGate) + `gate-registry.json` 1.0.0 (реестр «гейт → код →
  квитанция», 28 секций); `raw-plus.json` 2.3.0 (PROSE PLUS + закон ТЕГ-ПОРЯДКА, LAWS §20);
  `delivery-stats.json` 0.14.0 (89 каналов); **`delivery-index.json` 1.0.0 —
  статус сдачи партий draft/ready/delivered/superseded, единственный вход
  окна/жребия/CI**; **`active-pools.json` 1.0.0 — активный пул выбора
  (аудит Коула R5) + режимы CLOCK/LAB/SURGERY**; `ultimate-dice.json`,
  `dresser.json` 1.3.0 (y_stack + ПРЕ-ГАРДЕРОБ, tools/pregarment.py, LAWS §22); `salon.json`, `furnace-ledger.json`,
  `moves-ledger.json`, …)
- `verdicts/` — вербатим-вердикты автора по батчам; **новая эра (двойной
  аудит P1-02): структурированные `verdicts/T5-NN.json` (схема t5-verdict/1:
  loved/ok_with_issues/lessons/hypothesis_hits) — канонический вход вкуса;
  `taste.py` читает JSON, Markdown — фолбэк** (T5-27 — первый JSON-вердикт)
- `tools/` — `gates.py` (машинные гейты печи: 28 секций, реестр
  specs/gate-registry.json «гейт → код → тест → квитанция», валидатор
  сверяет цепочку; флоры, заявка/салиенс, claim-exists, char-spec,
  oc-class-floor, neg-anchor, header-contract, movesGate, storyCardsGate,
  yCardGate — Y-first, claimPhysics — В31, conceptFlag, negDressGuards,
  detailsGate — В32, **yStamp — вплетение 1:1 В34/В35, paletteSkin — В36**;
  `--md-from-receipt` — отчёт как производная JSON-квитанции), **`pregarment.py` — пре-гардероб: свежие комбо под жребий, набор не повторяется (LAWS §22)**, **`testforge.py` — тест-горн: болванки tests/test-corpus/ (вне прилавка), roll/check/coverage/compare — петля воспроизводимости А/Б/В/Г (LAWS §23)**,
  `window.py` (станция окна: квитанция ротации — позы/палитры/Y-карты/**
  OC-окно машинно**; `--for T5-NN` — окно задним числом), `taste.py`
  (вкус → план: ВКУС-БРИФ из verdicts/*.json + MD-фолбэк), `validate.py`
  (валидатор спеков до гейтов, проверки №1–№14: в т.ч. delivery-index,
  gate-report ≡ JSON-квитанция, gate-registry), **`t5delivery.py` (единый
  модуль сдачи партий — единственный источник «кто сдан» для окна/
  жребия/гейтов/CI)**, `oracle.py` (жребий/окно/`pool` — активный пул
  Y-карт/heat/audit/selftest)
- **ORACLE-2 — нервная система** (`docs/ORACLE.md`): канонический движок
  `src/lib/t5/oracle-engine.ts` вплетён во все органы — вкладка «Оракул»
  прилавка (жар партий, жребий карт, экспресс-оценка; клавиша 5), API
  `/api/t5/oracle/*`, сервисные `/batch /window /draw`, CLI печи
  `tools/oracle.py` (window/draw/heat/audit/selftest). Жребий
  детерминирован (seed = номер партии), паритет прилавок↔печь↔сервис
  лочат золотые векторы `tests/fixtures/oracle_vectors.json`;
- прилавок (корень репо): Next.js-вью цикла — список батчей/SO, батч-вью
  (POS/NEG/вердикт-редактор), инбокс, командная палитра ⌘K, loop-рендеры;
  компоненты в `src/components/t5/`, API в `src/app/api/t5/`.
  Инженерия (2026-11-20–21, двойной аудит): прилавок читает КОРНЕВОЕ
  дерево контента (resolver T5_ROOT в `src/lib/t5/store.ts`); юнит-тесты
  `bun run test` / `bun run test:py`, CI `.github/workflows/ci.yml`
  (+ production build); опциональный замок пишущих эндпоинтов — env
  `T5_WRITE_TOKEN`; **жребий и окно фильтруют корпус по индексу сдачи
  (delivery-index.json) — черновик не считается «предыдущей партией»;
  экспресс-оценка оракула показывает режим (LOCAL-LITE / SERVICE-RULE)**
- sha-замок квитанций: `git config core.hooksPath .githooks` — изменённый
  батч без свежей машинной квитанции не коммитится (аудит 2026-10-31, F2);
  CI на каждый пуш/PR: типы+линт+тесты прилавка, тесты печи, валидатор,
  гейты свежайшей партии

## Законы кратко

- Формат: **PROSE PLUS** (raw-plus.json 2.2.0: Danbooru-скелет в OPENER +
  NL-ядро заявки строкой «— the X is the claim, Y-made»; без метафор),
  24 слота = 3 OC + 21 мейн + EXP-оверлей
- **Y-first**: слот с заявкой собирается ОТ Y-карты (активный диапазон —
  из живого `specs/camera.json`, сейчас 1.18.0 / 530 карт; статические
  диапазоны эпохи Y1–Y18 изъяты из доков — двойной аудит P0-03) — комбо
  экспозиция+поза+POV+камера+профайлинг; PL-каталог — слой поддержки;
  В31: коридор = физика в POS, не поле; R-спред несёт класс раскрытия;
  В32: ≥2 фишечки-ФОРМЫ на мейн/EXP
- Hard-флоры никогда не расслабляются; X-слоты изъяты по умолчанию
- Окно ротации: позы/палитры/Y-карты/**OC** последних 3 СДАННЫХ партий
  (статус — specs/delivery-index.json) не повторяются; тема гуглится ДО
  шторма образов (§16, урок VENATOR); активный пул выбора —
  specs/active-pools.json (long tail — только режим LAB)
- Единственный законодатель — вердикт автора после рендера

Полная версия законов: `docs/LAWS.md`.
