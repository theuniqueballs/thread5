# thread5
Batch-Prompt Conveyer Belt

Конвейер промпт-батчей для аниме-рендеров (Tsubaki.2 Pro → Yodayo).
Наследник THREAD 4 — на новом ядре, без посредников.

> **Статус: 5.2 BETA** (счётчики пересчитаны из живых реестров 2026-11-23 —
> «хирургия тройного вердикта»: три внешних ИИ-аудита от 2026-11-22, вербатим
> `docs/CONSILIUM-TRIPLE-VERDICT-2026-11-22.md`, разбор — `docs/CONSILIUM.md`).
> Гигиена: 2026-11-02 (винтаж T4 → `archive/`) и **2026-11-23** — вычищены
> HANDOVER-T5-1, docs/T5-1-BETA, .t5-scratch, одноразовые скрипты batches
> (scripts/), мёртвый Prisma-хвост шаблона, .zscripts-скриншоты; правила
> агента вместо HANDOVER — **`docs/AGENTS.md`**; troubleshooting —
> `docs/TROUBLESHOOTING.md`. Анализ 5.2: `docs/PROJECT-REVIEW-5.2-2026-11-13.md`.
> Лицензия: **All rights reserved** (`LICENSE`).

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
  (бриф — по `_BRIEF-TEMPLATE.md`, с обязательным MODE: CLOCK/LAB/SURGERY/SPECIAL)
- `special/` — SPECIAL ORDERS: штучки вне цикла (заказы автора: подарки, приколы, одна сцена) — SO-NN.md, тот же RAW+ формат, без раскрытия темы; SO-13…SO-18 — синк заказов ботов FORGE (нумерация с конца наших)
- `bot-forge/` — **FORGE: конвейер ботов Yodayo Tavern** (ростер, копировалки `tools/tokens.mjs`/`render-preview.ts`, шаблоны); вход и статус — `bot-forge/INDEX.md`
- `docs/ars/` — **ARS NOVEAU v2, солнечная система**: `00-OVERVIEW` (карта),
  `01-SOL` (ядро: идея, HEAT, истории, ЛУНА, фасеты до жребия) → `02-MERCURY` (каст, ULTIMATE
  DICE, Дрессер) → `03-VENUS` (сцена) → `04-EARTH` (сборка POS/NEG, slot budget) →
  `05-FURNACE` (ревью, блокнот `specs/furnace-ledger.json`)
- `docs/` — LAWS.md (физика системы), **AGENTS.md (правила агента: запреты,
  прогон перед коммитом, режимы цеха — замена HANDOVER)**, TASTE,
  RENDERER_FACTS, NICHE, ANTI-MOVES (библиотека гарантированного трупа),
  LIVING-NOTES (индекс; архив по месяцам — `archive/living-notes/`),
  **TROUBLESHOOTING (топ-ошибок цеха)**, STORAGE-AUDIT, **ENGINEERING**
  (инженерная карта: архитектура, контракты формата, тесты/CI, модель
  безопасности, реестр фиксов), CONSILIUM (внешние пакеты + вердикты,
  включая тройной 2026-11-22)
- `archive/` — гигиена 2026-11-02 (винтаж T4, старые аудиты) и 2026-11-23
  (living-notes по месяцам)
- `specs/` — данные-активы (счётчики — из живых JSON, 2026-11-26: позы ×586 —
  poses 1.19.0; палитры ×305 — palettes 1.19.0 (волны 11–13 приняты автором в
  canon 2026-11-26 «Да забери ты уже эти палитры ебаные»; волна 17 «носители»
  P297–P305, trial до вердикта T5-33); **Y-множество ×538 — camera.json
  1.20.0, Y-first + Y-STAMP (вплетение 1:1) + POV-якоря В37 + траст-слой +
  юри-домен Y531–Y538 (пара-геометрия, garment_pair)**;
  расы ×74 — races 2.7.0 (кин-оверхаул: clarifiers+gimmick+skin_type, LAWS §21);
  OC-канон ×31 — canon 2.16.0 (Nun Harrow: вторая промоция из EXP T5-32 P29;
  Doe очки-пенсне закреплены по треду 4, 2026-11-26);
  CLOSET ×121 предмет на 13 полках — closet 1.1.0
  (exposure-классы, yStack); **bodytypes.json 1.0.0 — 24 типажа тел (пункт Е)**;
  **marks.json 1.0.0 — 42 метки, рейтинг-нейтральные (пункт И)**;
  **oc-candidates.json 1.4.0 — кандидаты в ОС: 27 trial (статусы
  passed/promoted/pending), вердикт только автора (пункт Д)**; `gates.json`
  1.30.0 (тикет #7 + приказ автора: carrierTruth В61 — заявка R+ живёт в
  каноничных данбоору-носителях, ≥2 в POS каждого R+ слота (≥1
  тела/прикрытия), бельё-импакт только вторым+; приватный диалект
  («breast shape»/«nothing underneath»/«soft crests») носителем не
  считается; канон-просвет: see-through = R+ носитель; носитель в своём
  NEG мёртв; nudeTruth.directNude += covered nipples/clothed nipples/
  pasties/nipple tape; wetSheerSkin вычищен от фраз-фрагментов; applyFrom
  36 — T5-36 пересобрана danbooru-first приказом автора, контроль отменён,
  FAIL с T5-36; предыдущее — 1.29.0 вердикт T5-35: nudeTruth В57/В58 —
  прямой ню-токен обязателен в R+ POS, поэтическое «nothing underneath»
  носителем не считается, collisionGuard bare-зон POS/NEG; ratingTruth 1.19.0 — законы автора 2026-11-26: тейп/cameltoe-фокус/
  pointRead/pairContact = HARD R+; «chest's bare line» отстрелен от R+;
  voltCore В39, raceCast v2.0 В40, exquisiteMain В41, expHypothesis В42,
  ratingTruth В43 — все FAIL-эра с T5-30; skinCast В48; **ratingMass В51 —
  R+-масса мейнов ≥ 14 / PG-13 = 0, FAIL с T5-35, вердикт T5-34; yStamp
  eraGuard В52 — клеймо 1:1 только modern, legacy = материал, вербатим
  legacy под R+ = FAIL с T5-35; **negCanonGuard В55 — именные фишки заказа
  и канон-локи никогда в NEG, FAIL с T5-35, special/SO — всегда; **voltRun В45 — второй тег-ран R+-слота (грудь/
  руки-что-ДЕЛАЮТ/бёдра-кожа), WARN с T5-35; **themeEcho В54 — THEME-SPEC в брифе (≥3
  рендеримых аксиомы + машинострока THEME-ECHO), доля мейнов с эхом < 60%
  → WARN «тема — гарнир»; **k1Sense — смысл-поле К-1 в каждой карточке
  stories.md обязательно с T5-35 (тикет #2: «объявлено ≠ исполнено»
  исправлено — форма+гейт+реестр+тесты); **claimFact В56 — fact-слой заявки
  R+: named object в тег-ране + зона грудь/низ + материал/холд носитель,
  процесс — только второй (two-carrier), WARN с T5-35; калибровка: ретро
  T5-34 ловит 13 из 15 ложных R+, P04/P13 чисто (тикет #5)**)
  + `gate-registry.json` 1.9.0
  (реестр «гейт → код → тест → квитанция», 41 секция); `raw-plus.json` 2.3.0
  (PROSE PLUS + закон ТЕГ-ПОРЯДКА, LAWS §20); `delivery-stats.json` 0.16.0
  (101 канал, волна 16); **`delivery-index.json` 1.1.0 — статус сдачи
  draft/ready/delivered/superseded + поле mode (CLOCK-дисциплина Коула §4),
  единственный вход окна/жребия/CI**; **`active-pools.json` 1.0.0 — режимы
  CLOCK/LAB/SURGERY + активный пул**; **`y-trust.json` 1.0.0 — траст-слой Y
  (HIGH/MID/LOW из JSON-вердиктов, Коул §7; draw --trust — CLOCK-жребий по
  HIGH+MID ≤ 80)**; `ultimate-dice.json`, `open-hypotheses.json` 1.3.0
  (+H-14 СБОРЩИК-ЧЕРНОВИКА, testing на T5-33),
  `rating-techniques.json` 1.9.0 — 166 приёмов + nude_truth-блок (В57
  прямые ню-токены · В58 коллизия POS/NEG · В59 гравитационный якорь ·
  В60 лестница носителей — вердикт T5-35; В61 carrier_tokens —
  данбоору-first, ≥2 носителя в каждый R+ слот, P01-паттерн, канон-просвет
  see-through = R+ — тикет #7; volt_run.groups + carriers — voltRun
  считает данбоору-носители; импорт из базового таксонома
  эччи-оракла + законы автора 2026-11-26 в principle.laws_author,
  sum_rules.hard_carriers),
  `dresser.json` 1.5.0 (y_stack + **carrier-first В47** + ПРЕ-ГАРДЕРОБ с
  кулдауном наборов 3 партии —
  вердикт автора 2026-11-23 «комбо не должны навсегда баниться», LAWS §22);
  `salon.json`, `furnace-ledger.json`, `moves-ledger.json`, …)
- `verdicts/` — вербатим-вердикты автора по батчам; **новая эра (двойной
  аудит P1-02): структурированные `verdicts/T5-NN.json` (схема t5-verdict/1:
  loved/ok_with_issues/lessons/hypothesis_hits) — канонический вход вкуса;
  `taste.py` читает JSON, Markdown — фолбэк** (T5-27 — первый JSON-вердикт)
- `tools/` — `gates.py` (машинные гейты печи: 41 секция, реестр
  specs/gate-registry.json 1.9.0 «гейт → код → тест → квитанция», валидатор
  сверяет цепочку; флоры, заявка/салиенс, claim-exists, char-spec,
  oc-class-floor, neg-anchor, header-contract, movesGate, storyCardsGate,
  yCardGate — Y-first, claimPhysics — В31, conceptFlag, negDressGuards,
  detailsGate — В32, **yStamp — вплетение 1:1 В34/В35 + eraGuard В52
  (клеймо 1:1 только modern: legacy-карта = материал — скелет, джус
  заново; вердикт T5-34)**, paletteSkin — В36,
  ratingMass — В51 (R+-масса мейнов, вердикт T5-34), **negCanonGuard —
  В55 (именные фишки/канон-локи не в NEG: очки SO-20 больше не теряются;
  special/SO-парсер POS:/NEG:), voltRun — В45 (второй тег-ран
  R+-слота, WARN), themeEcho — В54 (тема = визуальная система,
  THEME-ECHO-словарь брифа, WARN), **k1Sense — К-1: смысл-поле каждой
  карточки stories.md с T5-35 (тикет #2, WARN)**, **claimFact — В56: fact-слой
  заявки R+ (named object + зона + материал/холд носитель; процесс — только
  второй носитель, ⚗ не освобождает), WARN с T5-35 (тикет #5)**;
  `--md-from-receipt` — отчёт как производная JSON-квитанции), **`spec_io.py`
  + `commit_hygiene.py` — тикет #4: единый канон сериализации specs/*.json
  (ensure_ascii=False, формат-паспорт indent, round-trip идемпотентен) +
  ловушка реформат-чурна: полный дифф vs `git -w` > 5× = WARN, pre-commit
  1.14 гоняет по индексу; закон AGENTS №9 «format: — отдельный коммит»**,
  **`renderqc.py` —
  RENDER-QC fact-слой (В56): слоты/промпт/таблица из VLM-разбора инбокса,
  драфт rating_truth_delta, спорные файлы — автору (T2.1)**, **`pregarment.py` —
  пре-гардероб: свежие комбо под жребий, набор в кулдауне 3 сданные партии,
  затем свободен (LAWS §22, ревизия 2026-11-23)**, **`testforge.py` — тест-горн
  PROTO-2 (протоколы «пробы и ошибки»/«зализывание ран»/«вонючие яйца»
  2026-11-22, docs/PROTO-TRIALS-2026-11-22.md): болванки tests/test-corpus/ (вне
  прилавка), roll/check/coverage/compare — петля воспроизводимости А/Б/В/Г + цель
  Д: законы В39–В43 в ролле и чеке, эра-скип proto 1, CI-шаг + pre-commit 1.12, 19
  юнит-тестов; coverage с 2026-11-23 пересчитывается с нуля (копилка вылечена)**,
  `window.py` (станция окна: квитанция ротации — позы/палитры/Y-карты/**
  OC-окно машинно**; `--for T5-NN` — окно задним числом), `taste.py`
  (вкус → план: ВКУС-БРИФ из verdicts/*.json + MD-фолбэк с архивами), `validate.py`
  (валидатор спеков до гейтов, проверки №1–№15: в т.ч. delivery-index + mode,
  gate-report ≡ JSON-квитанция, gate-registry, свежесть y-trust), **`t5delivery.py`
  (единый модуль сдачи партий — единственный источник «кто сдан» для окна/
  жребия/гейтов/CI; status печатает MODE-дисциплину — CLOCK подряд)**,
  `oracle.py` (жребий/окно/`pool` — активный пул/heat/audit/selftest/
  **`trust` — траст-слой Y: rebuild из verdicts, отчёт; `draw --trust` —
  CLOCK-жребий по траст-пулу**)
- **ORACLE-2 — нервная система** (`docs/ORACLE.md`): канонический движок
  `src/lib/t5/oracle-engine.ts` вплетён во все органы — вкладка «Оракул»
  прилавка (жар партий, жребий карт, экспресс-оценка; клавиша 5), API
  `/api/t5/oracle/*`, сервисные `/batch /window /draw`, CLI печи
  `tools/oracle.py` (window/draw/heat/audit/selftest/trust/pool). Жребий
  детерминирован (seed = номер партии), паритет прилавок↔печь↔сервис
  лочат золотые векторы `tests/fixtures/oracle_vectors.json`;
  траст-фильтр — опция CLI (--trust), дефолтный жребий и вектора нетронуты
- прилавок (корень репо): Next.js-вью цикла — список батчей/SO, батч-вью
  (POS/NEG/вердикт-редактор), инбокс, командная палитра ⌘K, loop-рендеры;
  компоненты в `src/components/t5/`, API в `src/app/api/t5/`.
  Инженерия (2026-11-20–21, двойной аудит; чистка 2026-11-23): прилавок читает
  КОРНЕВОЕ дерево контента (resolver T5_ROOT в `src/lib/t5/store.ts`); юнит-тесты
  `bun run test` / `bun run test:py`, CI `.github/workflows/ci.yml`
  (+ production build; Prisma/db-хвост шаблона вырезан — прилавку БД не нужна);
  опциональный замок пишущих эндпоинтов — env `T5_WRITE_TOKEN` (прилавок —
  личный инструмент; при публичном деплое токен ОБЯЗАТЕЛЕН, см.
  docs/TROUBLESHOOTING.md); **жребий и окно фильтруют корпус по индексу сдачи
  (delivery-index.json) — черновик не считается «предыдущей партией»;
  экспресс-оценка оракула показывает режим (LOCAL-LITE / SERVICE-RULE)**
- sha-замок квитанций: `git config core.hooksPath .githooks` — изменённый
  батч без свежей машинной квитанции не коммитится (аудит 2026-10-31, F2);
  **pre-commit 1.13 (2026-11-23, тройной вердикт): валидатор + тест-горн +
  юнит-тесты печи (unittest) + юнит-тесты прилавка (bun test) — полный прогон
  ~3 с до каждого коммита**; CI на каждый пуш/PR: типы+линт+тесты прилавка,
  тесты печи, валидатор, гейты свежайшей партии

## Законы кратко

- Формат: **PROSE PLUS** (raw-plus.json 2.3.0: Danbooru-скелет в OPENER +
  NL-ядро заявки строкой «— the X is the claim, Y-made»; без метафор),
  24 слота = 3 OC + 21 мейн + EXP-оверлей
- **Y-first**: слот с заявкой собирается ОТ Y-карты (активный диапазон —
  из живого `specs/camera.json`, сейчас 1.19.0 / 530 карт; статические
  диапазоны эпохи Y1–Y18 изъяты из доков — двойной аудит P0-03) — комбо
  экспозиция+поза+POV+камера+профайлинг; PL-каталог — слой поддержки;
  В31: коридор = физика в POS, не поле; R-спред несёт класс раскрытия;
  В32: ≥2 фишечки-ФОРМЫ на мейн/EXP
- **Траст-слой Y (2026-11-23, Коул §7 + заказ автора)**: `specs/y-trust.json` —
  HIGH (хит в JSON-вердикте) / MID (нет улик) / LOW (промах); жребий CLOCK —
  только HIGH+MID, потолок 80 (`oracle.py draw --trust`); «window-eligible» ≠
  «активный пул» (квитанция жребия несёт active_trust_count / window_eligible_count)
- **Урок T5-29 (В39–В43, FAIL-эра с T5-30)**: вольт-ядро мейнов (Закон 24: вольт-масса ≥ 13, ниша 5–8, бег жанра ≤ 3 — вперемешку, не блоками); кины — опция (человек — основа, ≤ 10 из 21); EXQUISITE 1–4 в мейнах; EXP = полка гипотез (H-XX в каждой клетке, тема партии их не кастует); рейтинг = что кадр несёт составом (панель ткани = потолок R, ложный R+ = FAIL); калибровка 33/33 — docs/POSTMORTEM-T5-29.md
- Hard-флоры никогда не расслабляются; X-слоты изъяты по умолчанию
- Окно ротации: позы/палитры/Y-карты/**OC** последних 3 СДАННЫХ партий
  (статус — specs/delivery-index.json) не повторяются; тема гуглится ДО
  шторма образов (§16, урок VENATOR); активный пул выбора —
  specs/active-pools.json + траст y-trust.json (long tail — только LAB);
  пре-гардероб: набор в кулдауне 3 партии, вечного бана нет (§22)
- **Режимы цеха (Коул §4)**: MODE в брифе обязателен; CLOCK (по умолчанию,
  без волн реестров) · LAB (long tail, по приказу) · SURGERY (по багрепорту)
  · SPECIAL; счётчик CLOCK подряд — `t5delivery.py status`
- Единственный законодатель — вердикт автора после рендера

Полная версия законов: `docs/LAWS.md`. Правила для агентов: `docs/AGENTS.md`.
