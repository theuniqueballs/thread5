# THREAD 5 — JUICE MANUAL
## ЭТАП 01: АРХЕОЛОГИЯ A2 / A3
### Откуда брался «джус» · что потерялось · что можно вернуть без раздувания ARS

**Статус:** внешний ресёрч Cole/Grok · 2026-11-06  
**Источники:** `thread4/legacy/a2/*`, `legacy/a3/*`, `legacy/README.md`  
**Не цель:** вернуть A2-конвейер. Цель — **добыть механизмы вкуса**, которые T5-13/14 частично вернули композицией, но не добрали по «остановке пальца на скролле».

---

# 1. ЧТО ТАКОЕ A2 И A3 (по факту репо)

| Эра | Суть | Формат |
|---|---|---|
| **A2** (P11–P13) | Конвейер **картинок с вкуснятиной** | Core Engine + SYSTEM_PROMPT + тематические паки (Elven, Android Erotic…) |
| **A3** (P1–P5) | Конвейер **OC / момент** + «рандомки» | Core + Batch пары (Tribal, Unspoken Postures…) |
| Потом | A5 THE THREAD → 3.2 → T4 → T5 | Имя THREAD, тема-якорь, гейты, ARS |

A2 = **эротический удар + читаемость кадра**.  
A3 = **живой момент + OC-окно** («exists whether or not anyone is watching»).

T5 сейчас ближе к **дисциплине T4+composition manual**, чем к A2-ударности.  
Отсюда ощущение: композиция работает, а джуса мало.

---

# 2. ДНК A2 — МЕХАНИЗМЫ ДЖУСА

Из `A2P13F_SystemPrompt`, `A2P12.d_SYSTEM_PROMPT`, паков вроде Android Erotic.

### 2.1 Intent (прямо в системе)
> *Every prompt must be HOT enough for its rating tier — **ecchi magazine quality**, not polite suggestion.*  
> Enhance **VISUAL READABILITY, SCENE CLARITY, and EROTIC IMPACT**.  
> Does NOT increase complexity — **reduces noise**.

T5 иногда оптимизирует законность и квоты. A2 оптимизировал **остановку скролла**.

### 2.2 Pre-header до тегов (обязательный мозг)
Перед POS A2 требовал:

1. **Moment** — одно предложение  
2. **Door** — тип момента (Caught / Unseen / Deliberate / …)  
3. **Visual Thesis** — ≤10 слов  
4. **Palette** — цвета *и зачем*  
5. **Gaze** — кто зритель для неё  

Это не бюрократия. Это **фильтр мёртвых семян**.  
В T5 аналог размазан: thesis в шапке слота есть, но Visual Thesis + Door + Gaze не всегда жёстко тройка.

### 2.3 The Gap (главный секрет джуса)
> Best moments live in the space between:  
> what she feels / what she shows  
> what you see / what you imagine  
> clothing is on her / it's not, and it wasn't her choice  
> she wants / she's afraid to want  
> **Two conflicting truths in one frame = electricity.**

**Compositional Gap:** incomplete gesture — shirt halfway, hand mid-reach, eyes mid-turn.  
Кинетический зазор, не только эмоциональный.

→ Прямой предок H-12 (фаза) и C process-пакетов.  
В A2 это было **центром**, не опцией EXP.

### 2.4 WOW / TASTE checks
- *If this scrolled past me, would I STOP?*  
- Если первое впечатление «anime girl in a scene» — **пересобрать**.  
- Сохраню ли? Одна деталь через час? Что конкурирует за внимание? Thesis в 10 словах?

T5 furnace проверяет законы. A2 проверял **жадность глаза**.

### 2.5 Priority stack
Hard bans → Theme lock → **Physics** (tension, exposure justified, cause trace) → Cascade → Variation → Spike (~1/6).

Physics в A2 = ткань и контакт **логичны и горячи**, не только «поза из пула».

### 2.6 Umami detail
Один незабываемый конкрет: polymer forearms + circuit glow, не «beautiful android».  
В паках — **инновационная палитра темы** (20+ android-приёмов) и явное распределение CORE/EXTENDED/EDGE по слотам.

### 2.7 Density
25–35 focused tags. Every tag earns its place.  
Не максимальный dictionary — **бюджет внимания**.

### 2.8 Creative spike
~1 из 6 слотов — контролируемый срыв монотонии.  
Предок «пушки» / caliber cannon.

---

# 3. ДНК A3 — МЕХАНИЗМЫ ЖИВОГО МОМЕНТА

Из `A3P1/P2/P3 SystemPrompt`.

### 3.1 Вопрос эры
> *Is this alive?* — not *Is this correct?*

T5-гейт отвечает «correct». Вердикт автора отвечает «alive».  
A3 вшивал alive **до** рендера.

### 3.2 Moment as seed
Не «girl in bedroom».  
А «3am, she can't sleep, and the moon is doing something unfair to her skin».

Момент несёт **время + причину + несправедливость мира к телу**.

### 3.3 Four dimensions
1. **Narrative** — что было / что будет (props, clothing state = history)  
2. **Atmosphere** — color IS emotion (cold can beat warm)  
3. **Gaze** — Unseen / Caught / Aware / Deliberate / Abandoned / Accidental…  
4. **Render** — tags = what you SEE, not what you MEAN  

### 3.4 Same five pre-writes
Moment / Door / Umami / Palette / Gaze — и в A3.

### 3.5 OC window
A3 = OC + «рандомки»: персонаж как **живущий**, не как lock-list.  
Канон важен, но момент важнее чеклиста рогов.

---

# 4. ПОЧЕМУ В T5 ДЖУСА МЕНЬШЕ (диагноз, не обвинение)

| A2/A3 давало | T5 сейчас часто даёт | Эффект |
|---|---|---|
| Visual thesis ≤10 слов | Длинный thesis-рассказ | удар размыт |
| Door (тип момента) | Genre NICHE/VOLT/EXQ | жанр ≠ момент |
| Gap / incomplete | Иногда mid, часто result | «уже позы» |
| WOW check | Gate PASS | законно, но не жадно |
| Umami one detail | Много equally-weighted tags | нечего вспомнить |
| Spike 1/6 | HEAT/квоты ровные | нет пика |
| HOT enough for tier | Тир добит claim-токеном | medical R+ |
| «Is it alive?» | «Does it pass?» | разный бог |

Composition Manual A–D починил **каркас** (поза/камера/анти-моно).  
Не вернул **Gap + Umami + WOW + Spike** как обязательный ритуал слота.

---

# 5. ЧТО НЕЛЬЗЯ ВОРОЧАТЬ ИЗ A2

- Полный Core Engine на 200KB в чат каждый раз  
- X-квоты 24% как в старых паках  
- Проза-мишура «unfair to her skin» прямо в POS (T5.1 запретил)  
- 10-step cognitive mode на каждый слот (убьёт темп)  
- Подмену ARS системником A2  

Нужны **компактные ритуалы**, встроенные в SOL/EARTH, не новый движок.

---

# 6. ЧТО МОЖНО ВЕРНУТЬ (маппинг → следующие этапы)

| Механизм A2/A3 | Куда в T5 | Этап Juice Manual |
|---|---|---|
| Moment + Door + Thesis≤10 + Gaze | Пре-слот / SOL story cards | **05 SOL** |
| Gap / incomplete gesture | VOLT definition + pose law | **02 Genres** |
| Umami one detail | Обязательное поле story/EARTH | **05 SOL** |
| WOW check | Furnace human checklist | **05** + furnace |
| Spike 1/6 | Caliber cannon / EXP policy | **03 EXP** + caliber |
| HOT enough for tier | EXQUISITE + R+ packages | **02 Genres** |
| Gaze taxonomy | VOLT/OC moon | **02 / 04** |
| OC as living moment | Moon protocols | **04 Moon/OC** |
| Theme CORE/EXTENDED/EDGE | SOL theme depth map | **05 SOL** |
| Physics tension justified | VOLT + dresser process | **02** |

---

# 7. ФОРМУЛА ДЖУСА (рабочая, одна строка)

> **Живой момент (Door) + кинетический Gap + одна Umami-деталь + Gaze-контракт + удар в тир без медицинского claim — и слот обязан пройти мысленный WOW-stop.**

Если любого члена нет — слот может быть «правильным T5», но не A2-горячим.

---

# 8. ПРИМЕРЫ ПЕРЕВОДА (A2-дух → T5 PROSE PLUS)

### Было бы A2-мышление
Moment: morning activate, shirt still from sleep mode  
Door: UNSEEN  
Thesis: circuits glow under borrowed shirt  
Gaze: we shouldn't be in her kitchen  
Umami: polymer forearm translucency  
Gap: shirt off one shoulder, not fixed yet  

### T5 POS (без поэзии, с джусом)
```
upper body, morning window light,
1girl, android, polymer translucent forearms, soft blue circuit traces,
oversized shirt slipped off one shoulder, mid-fix not started,
looking at the kettle not at viewer,
covered by shirt fabric, quiet kitchen counter sit,
...
```
NL: `She sits on the counter in last-night's shirt. One shoulder is bare; she has not fixed it. Circuit light under the polymer skin answers the window.`

Разница не в «android». В **Gap + Gaze + Umami + Door**.

---

# 9. СВЯЗЬ С «СТЕКЛЯННОЙ ПУШКОЙ»

Пушка = Spike A2, доведённый до сознательного калибра.  
A2: ~1/6 creative spike.  
T5 предложение: 3–5 cannon/33 с одним стержнем.  

Джус **всего батча** = не 33 пушки, а:
- 60% CORE темы с Gap+Umami (A2 theme depth),  
- 30% EXTENDED,  
- 10% EDGE/spike,  
- плюс жёсткий WOW на EDGE.

---

# 10. ОГЛАВЛЕНИЕ JUICE MANUAL (план этапов)

| Этап | Файл | Содержание |
|---|---|---|
| **01** | этот | Археология A2/A3, диагноз, маппинг |
| **02** | next | VOLT / NICHE / EXQUISITE — переработка под Gap/Umami/Hot |
| **03** | | EXP — грамотный оверлей (тест ≠ свалка ≠ пушка) |
| **04** | | Луна / OC-канон — момент канона, не анкета |
| **05** | | SOL — распиновка темы, impact, CORE/EXT/EDGE, pre-slot |

Как с позами: **по одному документу**, без смешивания.

---

# 11. ВЫВОД ЭТАПА 01

A2 давал джус не «более грязными тегами», а **ритуалом до тегов**:  
Moment → Door → Thesis → Gaze → Umami → Gap → WOW.

A3 добавлял: *alive > correct*, color as emotion, OC as window into a moment.

T5 уже имеет: гейты, dresser, composition A–D, PROSE PLUS, ARS.  
Не хватает не полок — **обязательного пре-слота вкуса** и переопределения жанров так, чтобы VOLT требовал Gap, NICHE — umami мира, EXQUISITE — magazine-hot, EXP — spike/тест с правилами, Moon — OC-момент, SOL — карту удара темы.

Следующий этап по команде: **02 — VOLT / NICHE / EXQUISITE**.

— Cole / Grok · Juice Manual · Stage 01  

# THREAD 5 — JUICE MANUAL
## ЭТАП 02: VOLT / NICHE / EXQUISITE
### Жанр как обязательство удара · не как наклейка на слот

**Статус:** внешний пакет Cole/Grok · 2026-11-06  
**Вход:** Stage 01 (A2/A3 Gap, Umami, Door, WOW, Hot-for-tier)  
**Связь T5:** LAWS жанры · TASTE · NICHE.md · composition A–D · caliber  
**Цель:** переработать смысл трёх жанров так, чтобы слот **не мог** называться VOLT/NICHE/EXQ, не выполнив джус-обязательства.

---

# 0. ПРОБЛЕМА СЕЙЧАС

Сейчас жанр часто = **метка пула**:
- NICHE → «что-то странное в env»
- VOLT → «R+/тело/камера поближе»
- EXQUISITE → «OC или красиво»

Отсюда: композиция ок (T5-13), а джуса мало — жанр не *требует* Gap/Umami/Hot.

**Новый принцип:** жанр = **контракт**.  
Не выполнил контракт → слот должен быть перемаркирован (в PG-bridge / support), а не «VOLT потому что тир R+».

---

# 1. ОБЩАЯ ОСЬ ДЛЯ ВСЕХ ТРЁХ

Любой слот жанра проходит через одну сетку (из A2/A3, сжато):

| Поле | Вопрос | Fail = |
|---|---|---|
| **Door** | Какой тип момента? (Caught / Unseen / Deliberate / Aftermath / Threshold / Play / Power…) | «просто стоит» |
| **Gap** | Где незавершённость или двойная правда? | result-only, всё объяснено |
| **Umami** | Одна деталь, которую вспомнят через час? | всё одинаково важно |
| **Gaze** | Кто зритель для неё? | default looking at viewer без причины |
| **Hot-or-Strange** | Удар в тир (VOLT/EXQ) или удар в невозможное (NICHE)? | вежливый кадр |

Жанр определяет, **какой** удар главный. Остальные поля не обнуляются.

---

# 2. VOLT — ПЛОТЬ И ТОК

### 2.1 Старое определение (рабочее, но дырявое)
Камера-участник, тело в движении, взгляд-вектор, экспозиция тегом.

### 2.2 Новое определение (контракт)
> **VOLT** — слот, в котором главный удар = **телесный/эротический ток в моменте**.  
> Зритель чувствует доступ, напряжение ткани, фазу жеста или запретную точку камеры.  
> Без Gap или без Gaze-контракта VOLT не засчитывается — это просто R-картинка.

### 2.3 Обязательства VOLT
1. **Gap обязателен** — mid-gesture / process / incomplete dress action / weight shift ещё не стабилизирован.  
2. **Gaze явный** — Caught, Deliberate, Unseen, Power, Shame, Task-lock… не «улыбка в камеру» по умолчанию.  
3. **Один телесный стержень** — либо process garment, либо forbidden camera, либо contact, либо handbra/tape… (пакет C). Не три сразу.  
4. **Hot enough for tier** — PG-13 VOLT = сильный outfit+жест; R = бельё/поза как тезис; R+ = пакет α…κ доезжает *или* γ-контракт читается.  
5. **Umami** — один конкрет (мокрый край манжеты, след ленты, одна складка в ветре).

### 2.4 VOLT ≠ «любой R+»
| Настоящий VOLT | Лже-VOLT |
|---|---|
| waistband mid-slide, смотрит вниз | covered nipples, cowboy, smile |
| between-knees, looking down past camera | sheer dress, eye-level center |
| shirt-lift + tape, eyes over hem | wet clothes + standing straight |
| strap falling, hand still open | lingerie catalog pose |

### 2.5 Подтипы VOLT (не новые жанры — режимы стержня)
| Режим | Стержень | Опора в manual |
|---|---|---|
| **VOLT-MECH** | вещь делает (A2) | A2, D2, пакет α/δ |
| **VOLT-FORBIDDEN** | камера-запрет | A1, D1, пакет γ |
| **VOLT-CONTACT** | касание/физика | contact-physics, κ |
| **VOLT-PHASE** | чистая фаза без hard claim | A4, mid-run, about-to |
| **VOLT-GAZE** | удар взглядом + телом | A5 + soft claim |

В шапке слота достаточно: `Genre: VOLT · Mode: MECH`.

### 2.6 Антики VOLT
- Тир R+ при result-позе и default gaze  
- Три claim-токена «на всякий»  
- Камера в хвосте POS  
- «Эротично» только словом erotic pose без веса/вещи  

---

# 3. NICHE — ЧУДО КАК ПЕРВОЕ СЧИТЫВАНИЕ

### 3.1 Старое
Невозможный образ, раса/предмет делает работу, свидетель держит кадр.

### 3.2 Новое (контракт)
> **NICHE** — слот, в котором главный удар = **невозможное считывается раньше лица**.  
> Мир или объект-субъект ломает обыденность; героиня отвечает бытом или присутствием, не «колдует для камеры».  
> Если сначала читается «sexy girl», а чудо — подписью в thesis, это не NICHE.

### 3.3 Обязательства NICHE
1. **Silhouette-first** — full body / through-frame / wide: мир или объект читается в первую секунду (D5, B L3/L7).  
2. **Umami мира** — одна невозможная конкретность (метла метёт сама; дверь режет зиму/лето; тень моет посуду).  
3. **Gap желателен** — она *в процессе реакции* на чудо, не поза «смотрите чудо».  
4. **Gaze** — часто Unseen / Task / Toward the miracle, не pin-up.  
5. **Тир свободен** — NICHE может быть PG-13 и сильнее VOLT по вердикту (T5-13: ниша понравилась). Не раздувать claim «чтобы не скучно».

### 3.4 NICHE ≠ «странный env-фон»
| Настоящий NICHE | Лже-NICHE |
|---|---|
| sheets fold themselves; she reads a magazine | girl in witch hat in kitchen, standing |
| threshold: snow | summer through one door | girl on train platform, normal weather |
| broom sweeps; tail around handle; she drinks | cat-girl with broom prop, smile |

### 3.5 Подтипы NICHE
| Режим | Стержень |
|---|---|
| **NICHE-SUBJECT** | предмет-субъект (T5-10) |
| **NICHE-THRESHOLD** | проём / смена климата (T5-12) |
| **NICHE-BODY** | раса/тело *делает* физику чуда (slime steam, shadow-kin) |
| **NICHE-SCALE** | она мала в огромном / огромна в малом |
| **NICHE-WITNESS** | кадр через щель, мир важнее позы |

### 3.6 Антики NICHE
- Cowboy + face focus + miracle only in NL prose  
- Героиня «кастует» жест мага для камеры  
- Чудо из трёх идей сразу (нет umami, есть каша)  
- R+ sheer на NICHE «чтобы не PG» — часто убивает чудо  

### 3.7 Связь с A3
NICHE = A3 *alive window* для **мира**.  
Вопрос: *exists whether or not we watch* — чудо идёт без нас.

---

# 4. EXQUISITE — МАГАЗИННЫЙ УДАР / ИКОНА

### 4.1 Старое
Ультра своего жанра; на OC — class floor EXQ.

### 4.2 Новое (контракт)
> **EXQUISITE** — слот, собранный как **обложка**: один кристальный тезис, ноль конкурирующих шумов, hot (или freeze-strange) до дрожи.  
> Это не «просто OC». Это *magazine cover / final card* — калибр ближе к пушке, даже если тир R.

### 4.3 Обязательства EXQUISITE
1. **Visual thesis ≤10 слов** — обязательно в story/spine.  
2. **Umami одна** — и она в центре кадра, не на периферии.  
3. **Чистота** — никаких вторых чудес, лишних props, двойных claim.  
4. **Hot-or-Freeze** — либо максимальный контроль эччи (α/δ/MECH), либо ледяная икона (profile, stillness Door) — но не тёплая каша.  
5. **Камера осмысленная** — S-икона допустима; random dutch запрещён.  
6. На **OC**: канон VERBATIM + момент канона (см. этап 04), не анкета.

### 4.4 EXQUISITE ≠ «красивый VOLT»
| EXQ | Просто сильный VOLT |
|---|---|
| один тезис, воздух вокруг | много жестов |
| лицо/umami читаются идеально | энергия важнее иконы |
| можно повесить на стену | хочется листать дальше |
| 1–3 на батч | может быть пачка |

### 4.5 Когда EXQ на мейне
Редко. Финал акта, P24-класс, «луна на бельёвке».  
Квота: **≤3 EXQ-мейн + OC block** на 33, иначе обесценивание.

### 4.6 Антики EXQ
- EXQ-метка на слоте с тремя сюжетными идеями  
- Канон OC целый, момент мёртвый  
- Тир X-дрейф «ради ультра»  

---

# 5. МАТРИЦА ЖАНР × ДЖУС

|  | VOLT | NICHE | EXQUISITE |
|---|---|---|---|
| **Главный удар** | тело/ток/доступ | невозможное первым | кристальный тезис |
| **Gap** | обязателен | желателен | точный, один |
| **Umami** | телесный/ткань | мира/объекта | центр кадра |
| **Gaze** | контракт эччи | к чуду / unseen | контроль / pin или freeze |
| **Камера** | R/L пресеты, не только S1 | D5/D6/A11 | икона или deliberate beauty |
| **Тир** | обязан hot-for-tier | свободен | hot или freeze |
| **Квота ориентир /21 мейн** | 8–12 | 6–10 | 0–2 (+ OC) |

---

# 6. ПЕРЕКРЁСТКИ (разрешённые гибриды)

Иногда слот несёт два сигнала. Тогда:

| Гибрид | Как маркировать | Правило |
|---|---|---|
| VOLT в невозможном мире | **VOLT** primary, niche-env secondary | ток важнее чуда; чудо не спорит |
| NICHE с телесным claim | **NICHE** primary | claim не громче силуэта мира |
| EXQ + VOLT-MECH | **EXQUISITE** | один жест, magazine clean |

Две primary-метки запрещены. Одна primary, одна spice в thesis.

---

# 7. DOOR-ТАКСОНОМИЯ (общая, для pre-slot)

Сжатый список из A2/A3 — писец выбирает **один** на слот:

| Door | Суть | Частый жанр |
|---|---|---|
| **UNSEEN** | она не знает, что на неё смотрят | NICHE, VOLT-FORBIDDEN |
| **CAUGHT** | только что заметила | VOLT |
| **DELIBERATE** | показывает / дразнит | VOLT, EXQ |
| **AFTERMATH** | только что случилось | VOLT-PHASE, EXQ |
| **THRESHOLD** | на границе двух состояний/миров | NICHE |
| **TASK** | занята делом | NICHE-SUBJECT, VOLT soft |
| **POWER** | доминирует пространство/взгляд | VOLT, EXQ |
| **SHAME** | стыд / отводит глаза | VOLT |
| **STILLNESS** | пауза, тишина | EXQ, NICHE |
| **PLAY** | игра, лёгкость | VOLT, PG-bridge |
| **OFFERING** | протягивает / открывает | VOLT, EXQ |
| **RETURN** | вернулась / закрывает цикл | EXQ финал |

Door ≠ genre, но жанр без Door = наклейка.

---

# 8. ЧЕКЛИСТ ПИСЦА ПЕРЕД МЕТКОЙ ЖАНРА

```
[ ] Door выбран?
[ ] Gap есть? (для VOLT — must)
[ ] Umami одно, могу назвать вслух?
[ ] Gaze не default без причины?
[ ] Главный удар совпадает с меткой жанра?
[ ] Если VOLT — hot enough for declared tier?
[ ] Если NICHE — miracle first silhouette?
[ ] Если EXQ — thesis ≤10 words + no noise?
```

≤5 галочек → не врать меткой. Сделать support или дописать слот.

---

# 9. ЧТО МЕНЯЕТСЯ В ARS (без новых планет)

| Место | Микро-изменение |
|---|---|
| Story card / SOL | поля Door, Thesis≤10, Umami, Gaze |
| Mercury/Venus | Mode: MECH/FORBIDDEN/… для VOLT |
| Earth | чеклист §8 до POS |
| Furnace | вопрос: «жанр заслужен?» |
| Шапка слота | `Genre: VOLT · Mode: MECH · Door: CAUGHT` |

Не новый документ на 50 страниц внутри репо — **поля и обязательства**.

---

# 10. СВЯЗЬ С ПУШКОЙ / CALIBER

| Caliber | Жанр |
|---|---|
| **Cannon** | чаще EXQ или VOLT-FORBIDDEN/MECH на максимуме |
| **Support** | VOLT/NICHE с полным контрактом, без overcommit |
| **Air** | может быть soft NICHE или PG без жанрового пафоса |

Пушка без жанрового контракта = дорогой шум.

---

# 11. КРАТКИЕ ЗАКОНЫ ЭТАПА 02

1. Жанр — контракт, не тег пула.  
2. VOLT = Gap + Gaze + teleсный стержень + hot-for-tier.  
3. NICHE = невозможное раньше лица + umami мира.  
4. EXQUISITE = один тезис, ноль шума, magazine hit.  
5. Door обязателен для всех трёх.  
6. Лже-жанр хуже честного support-слота.  
7. Гибрид: одна primary-метка.  
8. Квоты EXQ жёсткие; VOLT/NICHE — по HEAT, но с чеклистом.

---

# 12. ОГЛАВЛЕНИЕ JUICE MANUAL

| Этап | Тема | Статус |
|---|---|---|
| 01 | A2/A3 археология | done |
| **02** | VOLT / NICHE / EXQUISITE | **done** |
| 03 | EXP | next |
| 04 | Луна / OC | |
| 05 | SOL / тема / impact | |

---

**Конец этапа 02.**  
По команде — этап 03 (EXP).

— Cole / Grok · Juice Manual · Stage 02  

# THREAD 5 — JUICE MANUAL
## ЭТАП 03: EXP
### Оверлей с задачей · не свалка · не девять пушек подряд

**Статус:** внешний пакет Cole/Grok · 2026-11-06  
**Вход:** Stage 01 (spike A2) · Stage 02 (жанры-контракты) · T5-12/13 вердикты · D8 тесты · caliber  
**Цель:** сделать EXP **прибыльным**: каждый слот что-то доказывает, кого-то проверяет или кого-то рождает — и не жрёт джус основного батча.

---

# 0. ДИАГНОЗ EXP СЕЙЧАС

EXP в T5 — оверлей (часто ×9): кандидаты в ОС + тесты поз/камеры.

| Когда EXP полезен | Когда EXP вредит |
|---|---|
| Одна переменная, ясная гипотеза | «9 лучших» без вопроса |
| Камера стабильна на новом kin (урок T5-13 P28) | Extreme angle + новый face = две переменные |
| Вердикт может сказать hit/miss | Автор не понимает, *что* тестировали |
| 2–3 пушки max среди EXP | Все 9 на калибре cannon |
| Отдельная лента внимания | EXP перебивает тему батча |

T5-12: EXP-позы «базис, плакать хочется».  
T5-13: композиция ок, но P28 — ноги ок, голова с extreme — нет.  
Вывод: **проблема не в числе EXP, а в отсутствии протокола переменных**.

---

# 1. ТРИ ЗАКОННЫХ РОЛИ EXP

Каждый EXP-слот обязан иметь **ровно одну** роль:

| Роль | Код | Вопрос слота | Вердикт смотрит |
|---|---|---|---|
| **TEST** | `EXP-TEST` | Сработала ли *одна* гипотеза (поза/камера/пакет/фаза)? | hit / miss / dirty |
| **CANDIDATE** | `EXP-CAND` | Живёт ли новый OC/kin как лицо+тело+фишка? | в канон / доработать / reject |
| **SPIKE** | `EXP-SPIKE` | Удар вне темы батча — creative spike / пушка | «ебальник» / нормально / мимо |

**Запрещено:** слот без роли.  
**Запрещено:** TEST+CAND+SPIKE на одном слоте (это три слота, склеенных скотчем).

Совмещение «приятное с полезным» (тест позы *на* кандидате) — только если в шапке явно:
`Role: EXP-CAND · Probe: pose X under camera S2`  
и **проба не extreme**. Иначе сначала CAND на стабильной камере, TEST — отдельным слотом.

---

# 2. EXP-TEST — НАУЧНЫЙ СЛОТ

### 2.1 Правило одной переменной
Фиксируем всё, меняем **одно**:

| Тест | Фиксируем | Меняем |
|---|---|---|
| Камера | поза, тир, пакет, тело | только D×A |
| Поза | камера S2/S5, тело | только pose family |
| Пакет R+ | поза, камера | α vs γ vs δ |
| Фаза | та же история | mid vs result |
| Door/Gaze | тот же action | Unseen vs Caught |

Если переменных ≥2 → это не тест, это шум. Вердикт нельзя интерпретировать.

### 2.2 Оформление TEST
```
Role: EXP-TEST
Hypothesis: [одна фраза]
Fixed: [список]
Variable: [одно]
Success looks like: [что увидеть на рендере / в вердикте]
Risk: [анатомия / moderation / PH ignore]
Combo: D8-xx или D1-xx
```

### 2.3 Квота TEST
- 2–5 на оверлей ×9  
- Не ставить три extreme-camera теста подряд  
- После miss — не повторять ту же переменную в следующем батче без изменения фикса

### 2.4 Связь с Composition D8
D8-01…D8-08 — готовые гипотезы.  
Не плодить новые, пока ledger miss/hit не заполнен по старым.

---

# 3. EXP-CAND — КАНДИДАТ В ОС

### 3.1 Цель
Не «красивая рандомка».  
**Проверка:** запоминается ли существо (лицо, силуэт, ≥3 фишки) так, что автор скажет «в канон».

### 3.2 Обязательный минимум CAND
1. **≥3 фишки** (уже есть) — читаемые в силуэте, не только в thesis.  
2. **Стабильная камера** на первом появлении: D2–D4, A01/A07/A02 soft — **не** A03 worm's / A05 top-down / R1 between.  
   Урок T5-13: extreme убивает голову/канон.  
3. **Один Door + один Umami** — живой момент, не turnaround sheet.  
4. **Тир честный** — не раздувать R+ sheer «чтобы заметили»; лучше сильный R/PG с лицом.  
5. **Имя-код в гипотезе** (Аурелия, Вьюга…) — уже практика T5.

### 3.3 Второй слот того же CAND
Если в одном батче 2–3 слота на одного кандидата:
- Слот 1: **face + body lock** (стабильная камера)  
- Слот 2: **жанр/момент** (VOLT-MECH или soft NICHE)  
- Слот 3 (опц.): **одна проба** (поза или камера) — помечена Probe  

Не три разных extreme на одном новом лице.

### 3.4 Reject-list (вкус автора → не повторять)
Вести короткий список рядом с burn (из вердиктов):
- green skin (Lucy)  
- single horn «залупа»  
- «слишком жирная» без заказа full  
- …  

CAND, попадающий в reject-list без нового приказа автора = брак сборки.

### 3.5 Квота CAND
- 3–6 слотов на ×9 оверлей (1–3 существа)  
- Новый kin + новая extreme camera в одном слоте = запрет  

---

# 4. EXP-SPIKE — ТВОРЧЕСКИЙ СРЫВ

### 4.1 Наследник A2 «~1 in 6 creative spike»
Слот вне логики «полезный тест».  
Задача — **удар**, риск, иногда off-theme (SPECIAL-дух внутри EXP).

### 4.2 Правила SPIKE
1. Калибр **cannon** по умолчанию — но **≤2 на весь EXP-блок** (≤3 на весь батч вместе с мейн-пушками).  
2. Один стержень (MECH / FORBIDDEN / SUBJECT / EDGE) — Stage пушка.  
3. Полный жанровый контракт (Stage 02), даже если off-theme.  
4. Не маскировать под TEST: если нет гипотезы — это SPIKE, честно.  
5. После SPIKE — следующий EXP лучше CAND или спокойный TEST (выдох).

### 4.3 Когда SPIKE оправдан
- Автор просит «ультани / импровизируй пиздец»  
- Тема батча узкая — нужен кислород  
- Ledger пушек пуст — нужна добыча hit  

### 4.4 Когда SPIKE — эго писца
- Девять SPIKE подряд  
- SPIKE вместо честного miss-теста  
- SPIKE на новом CAND с extreme (ломает и лицо, и удар)  

---

# 5. СБОРКА ОВЕРЛЕЯ ×9 (РЕКОМЕНДУЕМЫЕ ПРОФИЛИ)

### Профиль A — «Наука + 2 лица» (стабилизация после T5-13)
| Слоты | Роль |
|---|---|
| 3–4 | EXP-TEST (разные гипотезы) |
| 4–5 | EXP-CAND (2 существа × 2–3) |
| 0–1 | EXP-SPIKE |

### Профиль B — «Канононабор» (заказ «лучшие кандидаты»)
| Слоты | Роль |
|---|---|
| 6–7 | EXP-CAND (3 существа × 2–3, камера стабильная) |
| 1–2 | EXP-TEST (проба на *уже* показанном лице) |
| 0–1 | EXP-SPIKE |

### Профиль C — «Пушечный» (редко, по приказу)
| Слоты | Роль |
|---|---|
| 2–3 | EXP-SPIKE (разные стержни) |
| 2–3 | EXP-TEST под пушечные гипотезы (γ, phase) |
| 3–4 | EXP-CAND спокойные |

Не смешивать профили без пометки в шапке батча.

---

# 6. EXP И ТЕМА БАТЧА

| Правило | Смысл |
|---|---|
| EXP **не обязан** нести тему | уже закон T5 (как OC block) |
| EXP **не должен** спорить с темой шумной мешаниной | off-theme ok; anti-theme clutter нет |
| Theme-words в EXP | только если CAND/SPIKE сознательно в мире темы |
| Импакт темы | считается по мейнам; EXP не «спасает» слабый SOL |

Если тема слабая, 9 гениальных EXP не делают батч тематическим. Это другой продукт (SPECIAL).

---

# 7. EXP × ЖАНР (Stage 02)

EXP-слот всё равно выбирает жанровый контракт **или** честно «study» без жанра.

| Роль | Типичный жанр |
|---|---|
| TEST поза/камера | VOLT или study |
| CAND первый показ | soft VOLT / portrait study — **не** hard NICHE |
| CAND второй | VOLT-MECH / soft NICHE |
| SPIKE | VOLT-FORBIDDEN / EXQ / NICHE-SUBJECT |

`Genre: STUDY` — допустим для чистого TEST turnaround:  
тогда не требовать Gap, но требовать Hypothesis.

---

# 8. КАМЕРА И EXP (жёсткие правила)

1. **CAND-1:** только стабильный коридор D2–D4 × A01/A07/A02/A08 soft.  
2. **TEST камеры:** переменная = камера → тело/лицо уже знакомы (из мейна или CAND-1).  
3. **SPIKE FORBIDDEN:** extreme ok, но не на first-seen face.  
4. **A/B пары:** идеальны для TEST (D8-04 insert→payoff; mid vs result).  
5. Ковбой на EXP не запрещён, но **не** весь оверлей S1 — иначе T5-12 again.

---

# 9. ВЕРДИКТ ПО EXP — ЧТО СПРАШИВАТЬ

Шаблон для прилавка (коротко):

```
TEST: какие Hypothesis hit/miss?
CAND: кого в канон / доработать / reject? (имена)
SPIKE: какой слот ударил?
Камера: был ли extreme, где лицо поехало?
```

Писец заносит в:
- `moves-ledger` / open-hypotheses — hit-rate тестов  
- `oc-canon` queue — CAND pass  
- `CANNON-ledger` — SPIKE hit  

Без этой петли EXP = стоимость кредитов без капитала.

---

# 10. АНТИ-ПАТТЕРНЫ EXP

1. Девять слотов «просто лучшие» без Role  
2. Новый kin + worm's-eye + R+ sheer  
3. Тест с тремя переменными  
4. SPIKE, замаскированный под TEST  
5. Повтор miss-гипотезы следующим же батчем  
6. CAND без umami/фишек в кадре (только в prose)  
7. Весь EXP на одном пакете ζ sheer  
8. EXP как помойка идей, не влезших в мейн  

---

# 11. МИКРО-ФОРМАТ В ШАПКЕ СЛОТА

```
P25 — code-name (EXP-CAND · R44 · R · PL… · P…)
Role: EXP-CAND
Door: TASK
Umami: [one]
Hypothesis: — (cand)
Probe: none | pose | camera
Camera policy: STABLE
```

```
P28 — test-id (EXP-TEST · …)
Role: EXP-TEST
Hypothesis: between-knees reads as R+ without sheer
Fixed: clothed, face visible, body known
Variable: camera R1
Success: author marks hot / platform not soft-R only
```

```
P33 — spike-id (EXP-SPIKE · …)
Role: EXP-SPIKE
Caliber: CANNON
Stem: FORBIDDEN | MECH | EDGE | SUBJECT
Door: …
Umami: …
```

---

# 12. СВЯЗЬ С ОСТАЛЬНЫМ

| Система | Связь |
|---|---|
| Composition D8 | пул гипотез TEST |
| Juice 02 Genre | контракт, если не STUDY |
| Caliber / пушка | SPIKE ≤ лимита |
| Moon / OC (этап 04) | CAND pass → луна/канон |
| SOL (этап 05) | EXP не чинит слабую тему |
| Reject-list тела | фильтр CAND |

---

# 13. ЗАКОНЫ ЭТАПА 03 (сжато)

1. У каждого EXP — одна роль: TEST / CAND / SPIKE.  
2. TEST = одна переменная.  
3. CAND-1 = стабильная камера + фишки в кадре.  
4. SPIKE = редко, честно, с выдохом после.  
5. Не клеить три роли на один слот.  
6. Вердикт обязан закрывать hypothesis/cand/spike — иначе EXP впустую.  
7. Оверлей ×9 — выбирать профиль A/B/C, не «как вышло».  
8. Extreme + new face = запрет.

---

# 14. ОГЛАВЛЕНИЕ JUICE MANUAL

| Этап | Тема | Статус |
|---|---|---|
| 01 | A2/A3 археология | done |
| 02 | VOLT / NICHE / EXQUISITE | done |
| **03** | EXP | **done** |
| 04 | Луна / OC | next |
| 05 | SOL / тема / impact | |

---

**Конец этапа 03.**  
По команде — этап 04 (Луна / OC-канон).

— Cole / Grok · Juice Manual · Stage 03  

# THREAD 5 — JUICE MANUAL
## ЭТАП 04: ЛУНА / OC
### Микро-ядро канона · момент, а не анкета · орбита SOL без темы батча

**Статус:** внешний пакет Cole/Grok · 2026-11-06  
**Вход:** Stage 01–03 · ARS `ЛУНА` (орбита SOL) · `specs/oc-canon.json` · вердикты T5 OC-блока  
**Цель:** сделать три OC-слота **ударом канона**, а не «обязательной вставкой с VERBATIM волосами».

---

# 0. ЧТО ТАКОЕ ЛУНА В ARS (как есть)

Из `docs/ars/00-OVERVIEW`:

> **ЛУНА** — микро-ядро ОС, орбита SOL (сценарии ОС живут здесь).  
> SOL несёт 21 историю мейна + **3 истории Луны**.

Луна не отдельная планета-сеанс в таблице 01–05.  
Это **ветка SOL**: пока собирается тема батча, параллельно собираются три OC-момента, которые **не наследуют фурнитуру темы**.

| | SOL (мейн) | ЛУНА (OC) |
|---|---|---|
| Заказ | тема автора + движок | 3 темы OC / вайб / регистр |
| Env | мир темы | мир **её** элемента/быта/кризиса |
| Канон | по желанию расы | VERBATIM appearance |
| Успех | тема читается | *эта* героиня узнаётся и живёт |

Путать Луну с Mercury («кто в кадре») нельзя: Mercury спавнит всех; Луна **пишет три истории до спавна**.

---

# 1. БОЛЕЗНИ OC-БЛОКА

| Болезнь | Симптом | Эффект |
|---|---|---|
| **Анкета** | POS = список канон-тегов + random pose | нет момента |
| **Тема-паразит** | ведьмы/поезд/звёзды влетают в OC | ломает закон off-theme |
| **Тир ради тира** | sheer на OC «чтобы не скучно» | medical, лицо вторично |
| **Extreme first** | worm's-eye на дебюте глаз в батче | T5-13 P28-класс |
| **Регистр-наклейка** | «Yandere» в thesis, в кадре спокойствие | лже-момент |
| **Отдых-игнор** | одна OC третий батч подряд без причины | выгорание канона |
| **Таро в POS** | card/zodiac из canon registry | прямо запрещено policy |

A3-лекарство: *window into a moment that exists whether or not we watch.*  
OC T5 должен быть **окном в неё**, не в тему батча.

---

# 2. КОНТРАКТ ЛУНЫ (три слота)

Каждая история Луны = мини-SOL на одного человека:

```
OC: [Name]
Canon lock: VERBATIM fields used (hair/eyes/body/FAM/marks)
Moon theme: [заказ автора вербатим — Frenzy / Cyberpsychosis / …]
Door: [из Stage 02]
Moment: [1 предложение — что происходит СЕЙЧАС]
Thesis ≤10: [визуальный удар]
Gap: [что незавершено]
Umami: [1 деталь канона или момента в центре]
Gaze: [кто зритель для неё]
Register: [GALE / STEEL / … — как поведение, не как слово в POS]
Env world: [её мир — НЕ тема батча]
Caliber: support | cannon (≤1 cannon среди 3 OC)
Genre: VOLT | EXQUISITE | STUDY (NICHE редко — чудо её мира, не батча)
```

Если Moment пустой — Луна не собрана. Канон-теги не спасают.

---

# 3. ЗАКОН OFF-THEME (жёстко)

Уже в T5: *промпты ОС НЕ следуют теме батча — никакой ведьминской фурнитуры в ОС-слотах.*

Расширенная формулировка:

1. Theme-words батча **запрещены** в OC POS/NL.  
2. Props темы батча запрещены.  
3. Движок батча (быт заколдован / поезд / ira domini) **не** объясняет OC-кадр.  
4. Связь допустима только на уровне **вайба** (если автор сам смешал заказ) — и всё равно без лексики темы.  
5. Exception: автор **явно** приказал crossovers — тогда в бриф, не «случайно».

Луна вращается вокруг SOL, но **не копирует его поверхность**.

---

# 4. КАНОН = ОРУЖИЕ, НЕ АНКЕТА

### 4.1 VERBATIM appearance
Волосы, глаза, кожа, рога/уши, FAM/body, шрамы, кулон — в POS как в `oc-canon.json`.  
Имена OC в POS — никогда (LAWS).

### 4.2 Что из канона *не* тащить в батч
- Tarot / zodiac / element **символы** без заказа (usage_policy canon)  
- Способности «как суперсила», если не видимы  
- Предыстора прозой в POS  

### 4.3 Канон как Umami
Выбрать **одну** канон-деталь в центр удара:
- Nix: key pendant already turned + reflection lag  
- Zia: her own wind beats the wrap knot + manic joy  
- Doe: spore lands on the finger + glasses + vials  

Остальной канон — опознавательный каркас, не конкурирующие 15 акцентов.

### 4.4 Register = поведение
GALE / STEEL / STORM / VELVET — это **Door + body language + env reaction**, не токен `yandere` в POS.  
Yandere-заказ → Caught/Power + props одержимости (если автор дал), взгляд, дистанция — без IP-слов.

---

# 5. МАППИНГ ЗАКАЗА OC → МОМЕНТ

Автор даёт короткие темы («Frenzy», «Caught in vines», «Lewd tendencies»).  
Луна обязана **перевести** их в Moment+Door+Gap, не в label.

| Заказ (пример) | Плохой перевод | Хороший перевод |
|---|---|---|
| Frenzy | `manic expression, frenzy` | ветер побеждает узел; она смеётся *в* него; Door PLAY/POWER; Gap: wrap already lost |
| Cyberpsychosis | `cyberpunk, glitch` | рука и отражение рассинхрон; key turns to absent lock; Door STILLNESS/UNSEEN |
| Caught!!!! vines | `trapped in vines, scared` | vines mid-tighten; one hand free mid-reach; Door CAUGHT; Gap: not fully bound |
| Lewd tendencies | sheer default | deliberate strap-slip she doesn't fix; Door DELIBERATE; Gaze aware |

Правило: если Moment можно перепутать с другой OC — Луна не готова.

---

# 6. КАМЕРА И ТИР НА OC

### 6.1 Камера
- Предпочтение: D2–D4, A01/A07/A02, A08 только если глаза канона уже читались в серии/батче.  
- Extreme (A03/A05/R1) — **не** на единственном слоте OC в батче, если цель = узнаваемость.  
- EXQ-икона: F1 center допустим один раз на OC-блок.

### 6.2 Тир
- Hot-for-tier по Stage 02, но **лицо ≥ claim**.  
- R+ пакет α/δ/MECH предпочтительнее ζ на OC (лицо не тонет в sheer-шуме).  
- γ forbidden camera на OC — только если канон уже закреплён рендерами; иначе риск «не она».

### 6.3 Class floor EXQUISITE
Уже gates: OC ≥ EXQ class.  
Смысл: три OC-слота тянут к **чистому тезису**, не к свалке props.  
Не значит «всегда caliber cannon» — значит «нет шума».

---

# 7. РОТАЦИЯ И ОТДЫХ

Практика T5: Sue/Miyu/Ash отдыхают; Nix/Doe ready — хорошая гигиена.

Правила:
1. Автор выбирает 3 из ~20+ (selection_rule canon) — вайб/тема.  
2. Писец **не** подсовывает только что перегруженных без приказа.  
3. После сильного cannon-OC — следующий батч лучше support-момент, не снова ультра.  
4. Hana-класс: EXP-CAND → canon только по вердикту «дай имя / закрой вето» — не по желанию писца.

---

# 8. ЛУНА × EXP-CAND (стык с этапом 03)

| | Луна (канон) | EXP-CAND |
|---|---|---|
| Статус | в `oc-canon.json` | ещё нет |
| Цель | момент канона | проверка «в канон?» |
| Камера | стабильная / deliberate EXQ | **только** стабильная на first |
| Off-theme | must | must (относительно темы батча) |
| После hit | — | очередь в canon + первая Луна |

Первая Луна новопринятой OC = **CAND-2 логика**: face lock уже был в EXP; теперь Moment+Register.  
Не прыгать сразу в FORBIDDEN cannon.

---

# 9. СБОРКА ТРЁХ ИСТОРИЙ ЛУНЫ В SOL

Пока пишется `01-sol.md`:

1. Вставить блок `## ЛУНА` сразу после гипотезы/ожиданий темы (или после HEAT).  
2. Три карточки по контракту §2 — **до** расписывания 21 мейна.  
   Почему раньше: OC не должны получить «остатки» внимания.  
3. Проверить: ни одна theme-word батча не протекла.  
4. Проверить: три Door разные (не три DELIBERATE).  
5. Проверить: ≤1 cannon в тройке.  
6. На стыке L1 → Mercury: OC-карточки идут в каст **как есть**; Mercury не переписывает Moment ради симметрии с мейнами.

---

# 10. ПРИМЕРЫ КАРТОЧЕК ЛУНЫ (схема)

### Пример A — Zia / Frenzy
```
OC: Zia
Moon theme: Frenzy
Door: PLAY + POWER
Moment: Her own crosswind undoes the wrap knot; she laughs into it.
Thesis: wind wins the knot, she lets it
Gap: wrap off one shoulder, not fixed
Umami: red ribbons + teal horn tips in the gust
Gaze: into the wind, not posing for us
Env: rooftop laundry line (her evening, not batch witches)
Genre: VOLT-MECH · Caliber: cannon
```

### Пример B — Nix / Cyberpsychosis
```
OC: Nix
Moon theme: Cyberpsychosis
Door: STILLNESS
Moment: Reflection lags the raised hand; key already turned to a lock that is not there.
Thesis: body half a second late
Gap: hand up, reflection still lower
Umami: pink neck scar + key pendant
Gaze: at the glass, past her delayed self
Env: dark kitchen glass, home
Genre: EXQUISITE · Caliber: support
```

### Пример C — soft support OC
```
Door: TASK
Moment: She ties the apron strings behind her back, chin aside, kettle already pouring.
Thesis: morning before the face is ready
Gap: bow half-tied
Umami: [canon mark only]
Gaze: off, toward steam
Genre: VOLT-PHASE · Caliber: support
```

---

# 11. ЧЕКЛИСТ ЛУНЫ (перед EARTH)

```
[ ] 3 Moment непустые и разные?
[ ] Theme-words батча отсутствуют?
[ ] Канон VERBATIM + одна umami-деталь в центре?
[ ] Register = поведение, не banned label-token?
[ ] Камера не extreme на «надо узнать лицо»?
[ ] Door различны в тройке?
[ ] ≤1 cannon?
[ ] Тир не маскирует мёртвый момент?
[ ] Имя OC не в POS?
[ ] Tarot/zodiac не в POS?
```

---

# 12. ВЕРДИКТ ПО OC — ЧТО СПРАШИВАТЬ

```
Узнаваемость: это она? (канон)
Момент: живой / анкета
Какой из трёх сильнее?
Off-theme нарушен?
В канон править appearance? (зелёная кожа и т.п.)
```

Квитанции → oc-canon version bump / LIVING-NOTES / reject-list.

---

# 13. ЗАКОНЫ ЭТАПА 04

1. Луна = 3 истории OC в SOL, до мейнов по вниманию.  
2. Moment обязателен; канон без момента = анкета.  
3. Off-theme абсолютен без приказа автора.  
4. Одна umami-деталь канона в центре.  
5. Register через поведение.  
6. Стабильная камера, пока цель — «это она».  
7. ≤1 cannon в тройке OC.  
8. EXP-CAND ≠ Луна; первая Луна после канонизации — face-known.  
9. Tarot/zodiac registry не в батч.  
10. Три Door — три разных воздуха.

---

# 14. ОГЛАВЛЕНИЕ JUICE MANUAL

| Этап | Тема | Статус |
|---|---|---|
| 01 | A2/A3 археология | done |
| 02 | VOLT / NICHE / EXQUISITE | done |
| 03 | EXP | done |
| **04** | Луна / OC | **done** |
| 05 | SOL / тема / impact | next |

---

**Конец этапа 04.**  
По команде — этап 05 (SOL: тема, раскрытие, impact, CORE/EXT/EDGE, pre-slot).

— Cole / Grok · Juice Manual · Stage 04  

# THREAD 5 — JUICE MANUAL
## ЭТАП 05: SOL
### Тема · удар · CORE/EXTENDED/EDGE · распиновка ядра до мейнов

**Статус:** внешний пакет Cole/Grok · 2026-11-06  
**Вход:** Stage 01–04 · ARS `01-SOL` · LAWS · T5-10/12/13 (тема ок / узкая тема / джус)  
**Цель:** сделать SOL не «красивой шапкой», а **станком удара**: тема раскрывается, батч имеет импакт, каждый слот знает свою глубину.

---

# 0. ВОПРОС SOL (как в ARS)

> О ЧЁМ батч. Что раскрывает каждый слот. Сколько тепла.

Добавка Juice:
> Где **удар**. Где **выдох**. Что зритель поймёт без thesis.

Если SOL отвечает только «о чём» и не отвечает «где ебальник» — это оглавление, не ядро.

---

# 1. АНАТОМИЯ SOL (блоки в порядке сборки)

Порядок важен: поздние блоки **наследуют** ранние, а не наоборот.

```
1. ORDER (заказ автора вербатим)
2. SPINE (тема одной строкой + запрет «21 одинаковых»)
3. ENGINE + HYPOTHESIS + EXPECTATIONS
4. THEME-WORDS (легальный словарь / IP-ban)
5. HEAT (оплата разнообразия тиров/жанров)
6. ЛУНА ×3          ← Stage 04, до мейнов
7. DEPTH MAP        ← CORE / EXTENDED / EDGE на 21
8. ARC / ACTS       ← ритм ударов
9. 21 STORIES       ← Door, Thesis≤10, Gap, Umami, Gaze, Genre, Caliber, Combo
10. MOVES / WINDOW / CONSTRAINTS
11. SELF-CHECK IMPACT
```

Не начинать 21 историю, пока нет 1–8.  
Иначе слоты расползаются в «приятные кадры около темы».

---

# 2. SPINE — ТЕМА КАК УДАР, НЕ КАК ДЕКОР

### 2.1 Формула spine (A5-наследство + T5)
**Слово + ось в скобках** уже жили в legacy:  
`REMNANT (water/temple/ritual)`, `EX NIHILO (emergence/void)`.

Рабочий шаблон:

```
THEME: [имя вербатим]
AXIS: [2–4 герундия/существительных — что делать кадру]
ANTI: [чего НЕ будет 21 раз]
PROMISE: [что зритель поймёт к P24 без чтения шапки]
```

Пример:
```
THEME: THE LAST TRAIN BEYOND THE MAP
AXIS: threshold / two climates / train finds her
ANTI: 21 girls sitting on the same bench in a car
PROMISE: every stop is a different world; door is the cut
```

### 2.2 Тест spine
- Можно ли снять ANTI и всё равно скатиться в 21 одинаковых? → AXIS слаб.  
- PROMISE длиннее одного вдоха? → размыть.  
- Тема только в nouns props (hat, broom) без AXIS? → декорация, не движок.

---

# 3. ENGINE + HYPOTHESIS + EXPECTATIONS

### 3.1 Engine
Одноразовый закон мира **на этот батч**.  
Не поэзия. Проверка: *можно ли сфальсифицировать на рендере*.

| Хороший engine | Плохой engine |
|---|---|
| Быт заколдован: предметы делают работу, она не кастует | «магия и тайны везде» |
| Поезд не едет по миру — мир достраивается у остановок | «путешествие мечты» |
| Гнев господень как погода / давление на ткань | «тёмная атмосфера ira» |

### 3.2 Hypothesis
Одна фраза: *что мы проверяем этим батчем*.  
Связь с prereg T5-10 — оставить.

### 3.3 Expectations (≥2, фальсифицируемые)
Каждое ожидание:
- наблюдаемый признак в кадре / в вердикте;
- порог (≥N слотов…);
- способ опровержения.

Без ожиданий engine = вайб. С ожиданиями engine = эксперимент (A2 spike + science).

---

# 4. THEME-WORDS

Реестр **легальных** якорей темы в POS.  
Правило T5: слово темы легально, когда называет **предмет кадра**, не титул.

| Делать | Не делать |
|---|---|
| `sigil doormat`, `grimoire`, `orbital gate` | фраза-титул темы целиком |
| 12–20 слов максимум в реестре | 50 синонимов «для богатства» |
| IP-ban отдельным списком | случайный No Man's Sky в POS |

На EDGE-слотах theme-words можно почти обнулить (кислород).  
На CORE — ≥1 видимый якорь темы в кадре (не только в NL).

---

# 5. HEAT

HEAT = разрешение **не** быть ровным.

- Объявляет спред тиров и жанров.  
- Дефолт LAWS действует только если HEAT молчит.  
- Juice-добавка: HEAT должен зарезервировать место под **EDGE/cannon**, иначе все слоты = support.

Пример строки:
```
HEAT: NICHE PG×2 R×5 | VOLT R+×8 R×3 | EXQ R+×1 | EDGE slots: P15,P24 + 1 EXP-SPIKE
```

---

# 6. DEPTH MAP — CORE / EXTENDED / EDGE

Наследник A2 theme depth (~60/30/10).  
На 21 мейн:

| Слой | Доля | Задача | Theme-words | Caliber |
|---|---|---|---|---|
| **CORE** | ~12 (≈60%) | держат AXIS и PROMISE | ≥1 якорь | support |
| **EXTENDED** | ~6 (≈30%) | боковой фасет темы | 0–1 | support |
| **EDGE** | ~2–3 (≈10%) | срыв / пушка / почти off | 0–1 | **cannon** |

### Правила
1. CORE не значит «скучно» — значит **ось в кадре**. Gap+Umami обязательны и здесь (Stage 02).  
2. EXTENDED = легальный поворот (другой акт, другой prop-семья), не свалка.  
3. EDGE = стеклянная пушка: один стержень, максимальный джус, выдох после.  
4. Сумма EDGE + EXP-SPIKE + OC-cannon ≤ **5** на весь батч 33.  

Без DEPTH MAP батч либо плоский, либо хаотично орёт.

---

# 7. ARC / ACTS — РИТМ УДАРА

Не обязательно 3 акта. Но нужен **график громкости**.

### 7.1 Минимальный ритм
```
ACT I  — установка мира (больше CORE, 0–1 EDGE)
ACT II — давление / работа (CORE+EXTENDED, VOLT гуще)
ACT III — срыв или икона (EDGE + EXQ-финал)
```

### 7.2 Анти-ритм (смерть импакта)
- EDGE в P04, потом 20 support подряд  
- Три EDGE подряд  
- Финал = самый тихий слот  
- Все R+ в акте I, акт III на PG «отдых» без истории  

### 7.3 Выдох
После каждого EDGE — ≥1 support/air (жанр может быть сильным, калибр нет).

---

# 8. 21 STORIES — ПОЛЯ СЛОТА В SOL

Каждая история мейна **до** Mercury несёт:

```
Pxx — slug
Depth: CORE|EXT|EDGE
Genre: VOLT|NICHE|EXQ + Mode?
Door: …
Moment: [1 sentence]
Thesis ≤10: …
Gap: …
Umami: …
Gaze: …
Caliber: support|cannon|air
Combo: Dx-nn (если есть)
Package: α…κ|-
Tier aim: PG-13|R|R+
Camera intent: D×A (черновик)
Theme anchor: [word from registry or none]
```

Это не двойная работа с stories.md — это **стандарт карточки**.  
Пустые Gap/Umami на CORE = будущий «правильный, но без джуса».

### 8.1 Pre-slot ritual (A2 сжатый, 60 секунд на слот)
1. Door  
2. Moment  
3. Thesis ≤10  
4. Gap  
5. Umami  
6. Gaze  
7. WOW?: *остановил бы скролл?*  

Нет на 7 → переписать Moment/Gap, не добавлять tags.

---

# 9. РАСКРЫТИЕ ТЕМЫ — МЕХАНИКА

Тема раскрыта, если:

1. **PROMISE** сбывается без чтения шапки на ≥ половине CORE.  
2. ANTI соблюдён (нет 21 одинаковых).  
3. AXIS виден в действиях/проёмах/предметах, не только в палитре.  
4. EXTENDED не отрицает AXIS (боковой фасет ≠ другая вселенная без заказа).  
5. EDGE усиливает ощущение темы *или* даёт кислород — и помечен честно.

### 9.1 Узкая тема (вердикт T5-12 стиль)
Узкая тема — не враг. Враг — **буквальность**.  
Заказ «не 21 в вагоне» уже AXIS.  
SOL обязан нагенерировать 21 *разный порог*, а не 21 *вагон*.

Приём: список из 21 **фасета** до историй:
```
fog platform / two-climate vestibule / tail lantern / flooded car / …
```
Каждый фасет → один CORE/EXT. Пустые фасеты = риск повтора.

### 9.2 Широкая тема
Риск — каша.  
Жёстче CORE (больше якорей), EDGE меньше, hypothesis уже.

---

# 10. ИМПАКТ — ОПРЕДЕЛЕНИЕ ДЛЯ SOL

**Импакт батча** ≠ сумма R+.  
Импакт =  
`(PROMISE доехал) × (есть 2–4 настоящих EDGE/cannon hit) × (нет монотонного mid)`  

Метрики для себя до печи:
- Сколько слотов проходят WOW pre-check? (≥8 желательно)  
- Сколько EDGE? (2–3)  
- Есть ли выдохи после них?  
- Луна собрана и off-theme?  
- Есть ли DEPTH MAP на бумаге?  

Метрики для вердикта автора:
- Где ударило?  
- Тема прочиталась?  
- Где ровно / стерильно?  
- Какие Combo/Depth hit?

---

# 11. MOVES / WINDOW / CONSTRAINTS В SOL

Не отодвигать в конец «как бюрократию» — они **режут** DEPTH MAP.

- Window/burn: какие PL/палитры нельзя → не обещать EDGE на выгоревшей позе.  
- Moves: M05/M06… — назначить на конкретные Pxx в SOL, не «потом найдём».  
- Reject-list тела/кин — фильтр до каста.  
- Cowboy/sheer/dutch квоты — сразу в HEAT/DEPTH.

SOL, который игнорирует constraints и чинит их в Earth, теряет EDGE ( Compromised cannon).

---

# 12. SELF-CHECK IMPACT (конец SOL, до Mercury)

```
[ ] Spine: AXIS + ANTI + PROMISE заполнены?
[ ] Engine фальсифицируем? Expectations ≥2?
[ ] Луна ×3 с Moment (Stage 04)?
[ ] DEPTH MAP: ~60/30/10, EDGE id назначены?
[ ] ARC: где пики и выдохи?
[ ] 21 карточка: Door/Gap/Umami/Gaze не пустые на CORE?
[ ] Theme anchors на CORE видимы?
[ ] Caliber total cannon ≤5?
[ ] WOW pre-check ≥8 слотов?
[ ] ANTI не нарушен планом?
[ ] Moves/window учтены?
```

≤8/11 → не идти в Mercury «потом допишем».

---

# 13. МИНИ-ПРИМЕР КАРКАСА SOL (сжатый)

```
ORDER: …
SPINE:
  THEME: IRA DOMINI
  AXIS: pressure weather / body under decree / aftermath of anger
  ANTI: 21 throne-rooms with the same pointing sky
  PROMISE: the anger is climate, not a villain face

ENGINE: Divine anger as weather system that tightens cloth and posture
HYPOTHESIS: …
EXPECTATIONS: (1) ≥5 slots weather-as-force on fabric (2) no villain avatar

HEAT: … EDGE: P12, P24

ЛУНА: [3 cards Stage 04]

DEPTH:
  CORE: P04–P14 (anchors: ash wind, decree-seal, bent posture…)
  EXT: P15–P20
  EDGE: P12 FORBIDDEN, P24 EXQ subject

ACTS: I establish climate | II bodies under pressure | III aftermath icons

P12: Depth EDGE | Genre VOLT-FORBIDDEN | Door CAUGHT | …
P24: Depth EDGE | Genre EXQ | Door AFTERMATH | …
```

---

# 14. ЧТО SOL НЕ ДЕЛАЕТ

- Не пишет полный POS (это Earth).  
- Не подменяет вердикт автора.  
- Не раздувает theme-poetry в будущий POS.  
- Не чинит слабый spine девятью EXP (Stage 03).  
- Не ставит 21 EDGE «для импакта» — импакт схлопнется.

---

# 15. СВЯЗЬ ВСЕГО JUICE MANUAL С SOL

| Stage | Входит в SOL как |
|---|---|
| 01 Gap/Umami/WOW | pre-slot ritual §8.1 |
| 02 Genre contracts | поле Genre + checklist |
| 03 EXP roles | отдельный блок оверлея после 21 (или в HEAT) |
| 04 Moon | блок ЛУНА до 21 |
| Composition A–D | Combo/Camera/Package на карточке |
| Caliber | DEPTH EDGE + cannon budget |

SOL — **стол**, за которым всё это садится на батч.  
Не ещё одна полка в шкафу.

---

# 16. ЗАКОНЫ ЭТАПА 05

1. Порядок блоков SOL священен: spine→engine→luna→depth→21.  
2. Spine = AXIS + ANTI + PROMISE.  
3. Engine с hypothesis и фальсифицируемыми ожиданиями.  
4. DEPTH MAP 60/30/10; EDGE = пушки темы.  
5. Cannon budget на весь батч ≤5.  
6. Каждая CORE-история: Door, Gap, Umami, Gaze, Thesis≤10.  
7. WOW pre-check до Mercury.  
8. Тема раскрыта = PROMISE в кадре, не в md.  
9. Узкая тема лечится фасетами, не повтором.  
10. Constraints режут план в SOL, не в панике Earth.

---

# 17. ОГЛАВЛЕНИЕ JUICE MANUAL — ЗАКРЫТИЕ

| Этап | Тема | Статус |
|---|---|---|
| 01 | A2/A3 археология | done |
| 02 | VOLT / NICHE / EXQUISITE | done |
| 03 | EXP | done |
| 04 | Луна / OC | done |
| **05** | SOL / тема / impact | **done** |

---

# 18. ФИНАЛЬНЫЙ ТЕЗИС СЕРИИ JUICE

Composition Manual A–E учил **как не быть стерильным**.  
Juice Manual 01–05 учит **откуда берётся удар**:

- из Gap и Umami (A2/A3),  
- из жанра-контракта,  
- из EXP с ролью,  
- из Луны-момента,  
- из SOL с DEPTH и PROMISE.

ARS не надо расширять.  
Его надо **заряжать** этими полями — и беречь стекло пушки для EDGE.

Дальше — только сборка батча и глаз автора.

— Cole / Grok · Juice Manual · Stage 05 · END OF SERIES  

