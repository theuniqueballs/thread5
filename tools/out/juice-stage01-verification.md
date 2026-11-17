# JUICE MANUAL — ЭТАП 01: ИНТЕРПРЕТАЦИЯ И СВЕРКА С ИСТОЧНИКАМИ

**Статус:** писцовая обработка пакета Cole/Grok · 2026-11-05 (вечер)
**Вход:** `upload/T5-JUICE-MANUAL-STAGE-01-A2A3-ARCHAEOLOGY.md` (в файле лежат ВСЕ 5 этапов 01–05, «END OF SERIES»; интерпретация — по одному за раз, сейчас только 01)
**Источники для сверки:** репо `theuniqueballs/thread4`, ветка `theuniqueballs-OLD` (плоский корень; путь `legacy/a2/*` у Коула условен — файлы лежат корнем)

---

## 0. ВЕРДИКТ ЭТАПА 01 ОДНОЙ СТРОКОЙ

Диагноз Коула подтверждён источниками и фактами T5: джус в предках жил в **ритуале до тегов** (Moment → Door → Thesis≤10 → Palette → Gaze → Umami → Gap → WOW), T5 сохранил законность, но выронил **субъективный стоп-скролл-тест**, который существовал у предка как §22 закона 3.2. Возвращать — компактными полями (этапы 02–05), не движком.

---

## 1. СВЕРКА ЦИТАТ (не верить Коулу — проверить)

| § Stage 01 | Цитата Коула | Реальный источник | Вердикт |
|---|---|---|---|
| 2.1 Intent «HOT enough for its rating tier — ecchi magazine quality…» | A2P13F_SystemPrompt | `A2P13F_SystemPrompt.txt:6–11` | ✓ вербатим, атрибуция верна |
| 2.2 Pre-header (Moment/Door/Visual Thesis≤10/Palette/Gaze) | «A2» | **A3P2_SystemPrompt.txt STEP 6** (5 строк pre-header вербатимом); A2P13F имел только когнитивные вопросы MOMENT/CAUSE/FEELING/LIGHT/FOCUS (`:83–101`) | ⚠ **атрибуция ошибочна: это A3, не A2** |
| 2.3 The Gap «Best moments live in the space between…» | A2 | **A3P2_SystemPrompt.txt:77–88** вербатимом (включая «compositional gap… not emotional but KINETIC»); в A2-файлах «space between» = только negative space между конечностями в юри | ⚠ **атрибуция ошибочна: это A3** |
| 2.4 WOW/TASTE «would I STOP?» | A2 | A3P2 STEP 8/9 + **RULES_CORE 3.2 §22** (право эры: «would I actually stop scrolling?», PASS/REWORK-аудит в шапке батча, «the only non-mechanical check») | ⚠ атрибуция неполна: механизм дожил до 3.2 как §22 |
| 2.5 Priority stack (Physics #3, cause trace) | A2 | `A2P13F_SystemPrompt.txt:31–46` + `A2P12.d_SYSTEM_PROMPT.txt:38–52` | ✓ вербатим, атрибуция верна |
| 2.6 Umami «polymer forearms + circuit glow» + CORE/EXT/EDGE | паки Android | `A2P12c_Android_Erotic_Pack.txt:55–66` (umami) + `:23–26` (**CORE ~60% ×12 / EXTENDED ~30% ×6 / EDGE ~10% ×2 — прямой предок DEPTH MAP 60/30/10 Стейджа 05**) | ✓ вербатим, атрибуция верна |
| 2.7 Density «25–35 focused tags. Every tag earns its place» | A2 | **A3P2_SystemPrompt.txt:61** вербатимом; у A2 — скелеты 25–30/30–36/36–42 + ANTI-BLOAT (`A2P13F:156–167`) | ⚠ атрибуция наполовину: фраза — A3, анти-блоут — общий |
| 2.8 Spike ~1/6 | A2 | `A2P13F_SystemPrompt.txt:44` + `A2P12.d:171–179` (Controlled Chaos: ломается только уровень 5–7 стека, 1–3 никогда) | ✓ вербатим, атрибуция верна |
| 3.1 «Is this alive?» — not «Is this correct?» | A3 | `A3P1_SystemPrompt.txt:7` | ✓ вербатим |
| 3.2 Moment as seed «3am… moon doing something unfair to her skin» | A3 | `A3P1_SystemPrompt.txt:13–19` | ✓ вербатим |
| 3.3 Четыре измерения + Gaze-таксономия | A3 | `A3P1_SystemPrompt.txt:22–41` (Unseen/Caught/Aware/Deliberate/Abandoned/Accidental/Melancholy/Playful) | ✓ вербатим |
| 3.4 Пять pre-writes | A3 | `A3P1_SystemPrompt.txt:44–52` | ✓ вербатим |
| 3.5 OC window «exists whether or not anyone is watching» | A3 | `A3P1_SystemPrompt.txt:5` | ✓ вербатим |
| 5 X-квоты 24% | паки | `A2P12c:14,1064` | ✓ вербатим |
| 5 «200KB Core Engine» | — | `A2P13F_CoreEngine.txt` = **239KB**; загрузка батча 3.2 = RULES_CORE **522KB** + POOLS + POSE_LIBRARY | ✓ подтверждён, даже жирнее |
| Таблица эр (A2 P11–P13, A3 P1–P5, A5→3.2→T4→T5) | — | файлы репо + шапка RULES_CORE («pipeline: author → Claude → batch → PixAI/Tsubaki2 → Yodayo») | ✓ |

**Итог сверки:** 11 из 13 цитат — вербатим; 4 атрибуции съехали в пользу A2, хотя механизм живёт в A3/3.2. На смысл диагноза не влияет, но в каноне джус-генеалогии A3 должен носить титул «философия момента», A2 — «философия удара».

---

## 2. ЧЕГО КОУЛ НЕ ДОКОПАЛ (новые находки той же археологии)

1. **§22 RULES_CORE 3.2 — субъективный тест был ИНСТИТУТОМ, не привычкой.** «If this came up in my feed, would I actually stop scrolling?» → PASS/REWORK на каждый промпт, REWORK обязан назвать причину («too uniform with P14», «no wow-element», «feels clinical»), лог в шапке батча. T5 не изобрёл дыру — он **унаследовал** её, выронив §22 из цепочки предков. Furnace-чеклист (этап 05) имеет готовую форму предка.
2. **§35 EMOTIVE COUNTERPOINT ≥3/батч (3.2):** «Coherence is calm; counterpoint is electricity» — эмоциональный Gap был **квантифицирован законом батча**. Это сильнейший прецедент для Stage 02: Gap можно требовать квотой, а не настроением.
3. **§21 RULES_CORE — Visual Thesis дожил до 3.2 как закон:** «THESIS: <10 words» в pre-header, «if it reads like a metadata line rather than a sentence → reject».
4. **A2 имел и кинетический Gap — TENSION vs RELEASE** (`A2P13F:386–393`): «held breath, incomplete action» = tension; R+ льнёт к tension, X — к release. Коул отдал Gap целиком A3; честнее: **A2 = механика фазы, A3 = философия зазора**. Оба стержня уже в T5-инфраструктуре (H-12 «фаза», D8-02 «process > result», δ PROCESS STRIP).
5. **TAG WEIGHT CLASSES (A2):** NUCLEAR+3 / HEAVY+2 / MEDIUM+1 / LIGHT+0, бюджет 14pt, NUCLEAR → скелет MINIMAL, Focus Lock Hard → max 2 env-тега. Компактный механизм «удар в тир без каши» — кандидат в контракт Stage 02 (EXQ/VOLT), Коул его не упомянул.
6. **«No orphan thoughts» (A2P12.d):** когнитивный ответ без соответствующего тега = мусорное мышление («either add the tag or revise the answer») — готовый закон связки «поле story-карточки ↔ тег POS» для Stage 05.
7. **Вилка тёплого, уже решённая T5:** A2P13F — WARM STRICT (2/3 минимума, «full cold = ALWAYS FORBIDDEN»), A3P1 — «COLOR IS EMOTION… Cold can be more powerful than warm». T5 стоит на стороне A3 (вердикт T5-13: «молоко + холодное свечение» легальны). Возвращать A2-строгий тёплый НЕ надо — развилка закрыта каноном.
8. **G20 T5 = компактный потомок A2-VECTOR CAP.** A2: «R+ → MAX 2 vectors» (`A2P13F:207–210`); T5: «R+ слот = ОДИН пакет + один hard-claim (G20)» (rating-techniques v1.2.1:2210). Закон «не три стержня сразу» в T5 уже есть — Stage 02 не изобретает, а привязывает его к жанровому контракту.
9. **Двери:** A3P2 STEP 4 даёт 15 дверей (UNSEEN, TURNING, AFTERMATH, THRESHOLD, RETURN, OFFERING, SECRET, ACCIDENT, STILLNESS, DREAM, MELANCHOLY, PLAY, POWER, ABANDONED, AWARE); A3P1 — 8. Таксономия Коула из Stage 02 §7 (12 дверей) = консолидация, при этом **TASK и SHAME — его изобретения** (в A3 их нет), а TURNING/SECRET/ACCIDENT/DREAM/MELANCHOLY/ABANDONED/AWARE выброшены. Для Stage 02: принять 12 как рабочее ядро, пометить TASK/SHAME как добавку, полную A3-полку держать в архиве.
10. **A3P2 финал — готовая формула серии:** «The story is the seed. The composition is the spine. One makes it alive. The other makes it STRIKE.»

---

## 3. СВЕРКА ДИАГНОЗА §4 С ФАКТАМИ T5 (по строкам таблицы)

| Строка Коула | Факт T5 | Вердикт диагноза |
|---|---|---|
| Visual thesis ≤10 → «длинный thesis-рассказ» | story-карточки T5-14: поле SOL = абзац, поля Thesis≤10/Door/Umami/Gaze отсутствуют | ✓ честно |
| Door → «Genre NICHE/VOLT/EXQ» | LAWS.md:116–123 — определения жанров дословно совпали с цитатами Stage 02 §2.1/3.1/4.1 («камера-участник, тело в движении, взгляд-вектор» и т.д.) | ✓ честно: жанр = метка пула |
| Gap «иногда mid, часто result» | H-12 (mid-action) открыт с 2026-11-04; D8-02 «process > result» — в леджере непрогнан | ✓ честно |
| WOW → «Gate PASS» | gates.py проверяет законность; субъективного стоп-теста нет нигде | ✓ честно; предок §22 даёт форму |
| Umami → «много equally-weighted» | поля Umami нет ни в карточках, ни в Earth | ✓ честно |
| Spike 1/6 → «HEAT ровные» | HEAT-спред есть, пушка-квота не кодифицирована (стеклянная пушка описана в NICHE.md как эра T4.2, не как квота T5) | ✓ честно |
| HOT for tier → «тир добит claim-токеном» | G20 уже режет «три стержня»; anti-mono квоты γ/δ/η/ι=0 → моноканал — известная боль вердиктов | ✓ честно, механизм половинный |
| «Is it alive?» vs «Does it pass?» | вердикт T5-12 (H-12 source): «Картинки хочется сильно живее» — автор уже отвечает «alive», машина до рендера не спрашивает | ✓ честно |

**Диагноз подтверждён целиком, ни одной натяжки против T5.**

---

## 4. МАППИНГ §6 — ПОДТВЕРЖДЁН ПОСТРОЧНО

- Moment+Door+Thesis≤10+Gaze → story-карточки/SOL (Stage 05): поля отсутствуют → реализуемо без конфликтов.
- Gap → VOLT-определение + pose law (Stage 02): LAWS VOLT без Gap-обязательства; H-12/D8-02/δ — готовые опоры.
- Umami → story/EARTH (Stage 05): поле отсутствует.
- WOW → furnace human checklist (Stage 05): субъективного шага в печи нет; предок §22 даёт формат PASS/REWORK.
- Spike → EXP + калибр (Stage 03): EXP ×9 есть, Role/профили/лимит пушек отсутствуют.
- HOT for tier → EXQ + R+ пакеты (Stage 02): class floor OC есть, hot-for-tier для VOLT не сформулирован.
- Gaze-таксономия → VOLT/OC (Stage 02/04): в camera.json есть взгляд-вектор, контракта Gaze нет.
- OC как живой момент → Moon (Stage 04): oc-canon VERBATIM есть, Moment-контракта нет.
- Theme CORE/EXTENDED/EDGE → SOL (Stage 05): HEAT есть, DEPTH MAP 60/30/10 нет.
- Physics tension → VOLT (Stage 02): 9 звеньев §4 LAWS уже покрывают cause trace — тут T5 сильнее A2, Stage 02 ничего ломать не должен.

---

## 5. ЧТО ДЕЛАТЬ (без раздувания ARS — согласен с Коулом)

1. **Принять Stage 01 как канон диагноза** с двумя поправками писца: генеалогия — Gap/Umami/WOW/Door/pre-header = **A3** (A2 — Intent/Stack/Spike/Umami-паки/CORE-EXT-EDGE/вес-классы), и «C process-пакетов» = **δ PROCESS STRIP** (пакета «C» в T5 нет).
2. Формула §7 — рабочая, в LAWS не писать до вердикта автора (она собирается из этапов 02–05).
3. Пример §8 (A2-дух → PROSE PLUS) — корректен, нарушений T5-законов нет: mid-fix без «not started»-прозы, Gaze тегом «looking at the kettle», umami в теге «polymer translucent forearms». Брать как образец перевода.
4. Стейджи 02–05 уже лежат в том же upload-файле — новый подгон не нужен; ждать команды на этап 02 (VOLT/NICHE/EXQUISITE).
5. Субъективный WOW — единственное, что нельзя автоматизировать гейтом; предок §22 прямо говорит: «the only non-mechanical check, and that's exactly why it matters». Значит: поля карточек + чек-лист писца, гейт — только на НАЛИЧИЕ полей, не на их качество.

---

## 6. СТАТУС СЕРИИ

| Этап | Содержание | Статус |
|---|---|---|
| **01** | A2/A3 археология | **интерпретирован** (этот файл) |
| 02 | VOLT / NICHE / EXQUISITE — жанр-контракт | пакет в руках, ждёт команды |
| 03 | EXP — роли TEST/CAND/SPIKE | пакет в руках, ждёт команды |
| 04 | Луна / OC — момент канона | пакет в руках, ждёт команды |
| 05 | SOL — тема, DEPTH MAP, pre-slot | пакет в руках, ждёт команды |

— писец THREAD 5 · обработка Juice Manual, этап 01 из 5
