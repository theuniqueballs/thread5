# PH (Prompt Helper) — ДАЙДЖЕСТ ИЗ THREAD 4 → для T5.1
Составлено R1 из /tmp/thread4. «Чудит» дословно в thread4 НЕ встречается — странности задокументированы как «adversarial mutation layer» + конкретные баги (см. §3).

## 1. ЧТО ТАКОЕ PH
- PH — прослойка рендер-цепочки «PixAI / Tsubaki.2 Pro + Prompt Helper / Yodayo» между твоим промптом и рендерером. Это НЕ поле и НЕ секция промпта — слой, который ПЕРЕПИСЫВАЕТ весь промпт перед отправкой в рендер. (thread4/RENDERER_FACTS.md:3-4)
- В UI Yodayo есть вид «PH Rewritten» — показывает, что PH реально отправил в рендерер. Авторские вердикты построены как «Оценено/Указано + PH Rewritten + комментарий»; этот корпус = канон того, что рендерер читает на самом деле. (thread4/verdicts/T4-04-author-verdict.md:1-7)
- Альтернативный режим генерации Yodayo — «Raw» (без PH). С T4-23 (2026-10-06) thread4 целиком перешёл на Raw: «автор генерил в Raw — нейтрально для пар». (thread4/batches/T4-23.md:3; thread4/thread4/LIVING-NOTES.md:87)
- Отдельных input-полей PH (character/scene/style) в thread4 НЕ найдено — PH принимал целиком POS-блок (теги+проза+квалити) и NEG шёл отдельным блоком мимо PH. (thread4/batches/T4-04.md:40-46; thread4/GROK-PROMPT.md:204-205)

## 2. ВХОД/ВЫХОД PH
- Вход: весь POS-промпт. Выход: каноническая форма PH = «tag-block → prose → quality tags». (thread4/RENDERER_FACTS.md:17-19)
- КЛЮЧЕВОЙ ФАКТ: контент, УЖЕ в PH-форме, проходит verbatim, без единого рерайта. Поэтому доктрина: «PH SHAPE IS THE DELIVERY SHAPE» — пишем сразу в целевой форме: (1) тег-блок (заявка: identity+signal+state), (2) проза (noun-led), (3) квалити-теги (палитровые, не генерические). (thread4/CONSTITUTION.md:132-141; thread4/thread4/RULES_CORE-ORIGINAL.md:155-166)
- Рабочий шаблон слота: тег-ран → проза-тело → face-lock предложение → «Masterpiece, best quality, anime artstyle». (thread4/batches/T4-04.md:42)

## 3. КАК ИМЕННО PH «ЧУДИТ» (все квирки)
- РЕШАПИНГ: PH не «санитизирует по формату», а перекраивает вход под себя. Тег-ран НЕ PH-стойкий канал — PH растворяет его в прозу, если он не в PH-форме (провал RF-002: заявлено R7/R+12/X2, отрендерилось ≈PG×13/PG-13×3/R×5/weak-R+×2/R+×1/X×1). (thread4/RENDERER_FACTS.md:17-26; thread4/thread4/ISSUES-FRED-2026-09-28.md:172-195 — ISSUE 06)
- МУТАЦИИ ЗАЯВКИ: PH = adversarial mutation layer — рендерер мутирует заявку (sheet→рубашка, леотард→халат, вышка→вагончик — T4-04). Kill criterion: мутация заявки = слот мёртв. Ловились VLM 24/24. (thread4/thread4/TASTE.md:285-290; thread4/thread4/CONSTITUTION.md:261-263)
- УТЕЧКИ (LEAKS): artist-токены сами вставляются в промпт (stuart_pot ×3), character-токены (grey_wolf ×2) ⇒ анти-лик NEG-guard на КАЖДЫЙ промпт. Симптом-паттерн для детекта: `character:` / `_\(...\)` в PH-тексте (U1/U3, не внедрено). (thread4/RENDERER_FACTS.md:27-28; thread4/thread4/docs/AUDIT-V3-2026-09-27.md:30-32)
- ОСТРИЖЁТ ПРОЗУ: verb-led flourish без визуального payload («the pool drew itself») выбрасывает; noun-form выживает. (thread4/RENDERER_FACTS.md:20-23)
- ПРОЗА НЕ ДОХОДИТ ВООБЩЕ: машинная сверка T4-22 — проза дошла в PH на 0% (0/162 шинглов), теги — 37% (79/214). Чем меньше тегов дошло, тем ниже тир (P12 1/9→PG-13). Вывод: теги = единственный проверяемый канал, проза — расход бюджета без следа. (thread4/thread4/LIVING-NOTES.md:89-94)
- ВЫКИДЫВАЕТ СВИДЕТЕЛЯ: свидетель в прозе, но не в тег-блоке — риск, что PH его выкинет ⇒ «сильный слот даёт свидетелю тег И прозаическую работу». (thread4/thread4/NICHE.md:181-183)
- ДРЕЙФ В ПЕРСОНАЖА: OC-тег стоял, но коса+изгородь+платье стянули рендер в аниме-персонажа vermeil_(kinsou_no_vermeil) — PH-текст начинался с «character: vermeil…». Лечение: уникальные hair/eyes/skin per slot. (thread4/thread4/LIVING-NOTES.md:43)
- СМЯГЧАЮЩИЙ ЯЗЫК = ПАДЕНИЕ ТИРА: «subtle outlines» / «silhouette of her braless chest» / «partially submerged» → PG-13; R+ язык: «detailed outline of her nipples», «erotic pose», «sheer and see-through» как главная деталь. НО (вердикт Кенни, n=48): выборки мизерные (p≈0.3–0.55), PH-язык = диагностика ПОСЛЕ вердикта («модель увидела заявку или смягчила»), НЕ правило и НЕ гейт. (thread4/thread4/LIVING-NOTES.md:34-47)
- Честный ретранслятор позы: токен «erotic pose» PH повторил дословно («as she poses erotically»), кадр с токеном живее — токен в рабочий словарь писца (H2 T4-22-EXP, подтверждено). (thread4/thread4/LIVING-NOTES.md:82)
- МАТУРИТИ-СЛОЙ PH ОТКЛЮЧЁН в текущем режиме: анти-лоли NEG-пол — наша ноша. (thread4/RENDERER_FACTS.md:29-30)
- Артефакты рендера по PH-тексту: «какое-то некрасивое пятно на месте, где должны быть соски. Посмотри чё там PH написал» (T4-04 #5). (thread4/thread4/verdicts/T4-04-author-verdict.md:31-32)
- КОГДА НАДЁЖЕН: при входе уже в PH-форме — verbatim;PH-версия промпта может бить без-PH «в разы» (T4-04 #10: PH-версия «в разы круче и конкретней»). КОГДА НЕ НАДЁЖЕН: сырой тег-ран/чужая форма, verb-проза, свидетели и заявки только прозой. (thread4/RENDERER_FACTS.md:17-26; T4-04-author-verdict.md:50-53)

## 4. WORKFLOW THREAD 4 (что давали PH / что брали / что держали руками)
- «RENDER PROTOCOL: PH ON — тег-блок канал правды, проза несёт красоту» — шапка каждого PH-батча. Писали промпт сразу в PH-форме, чтобы PH нечего было переписывать. (thread4/batches/T4-04.md:20-28)
- Давали: тег-ран (вся заявка: раса/состояние ткани/невозможное — первыми ~12 тегами), проза как красота/интерпретация, квалити-хвост. Руками (не через PH) держали: NEG-блок целиком (веса 1.2/1.3 — «в NEG, не через PH»), возрастные регистры (только проза-нарратив, не теги), кадрирование (тегом, не прозой). (thread4/NICHE.md:144-148; thread4/GROK-PROMPT.md:82; thread4/RENDERER_FACTS.md:33-36,105-106)
- Брали из PH: «PH Rewritten» как ground-truth → корпус T4-04 переработан в рецепты/гейты/RENDERER_FACTS; PH-язык слотов как диагностику доставки заявки; наряд Ana канонизирован «по PH» (PH-rewrite автора = канон-референс). (verdicts/T4-04-author-verdict.md:4-7; specs/oc-canon.json:320)
- Хронология: PH-эра T4-04→T4-22 (пик T4-09: 10/12 R+); T4-23 (10-06) — переход на RAW/данбуру-формат для Raw-генерации без PH; RAW-батчи T4-24 «одинаково средние», T4-26 — ПИК всей истории 17/25 уже без PH; приказ автора 2026-10-09: мигрировать PH-наработки в RAW+ (палитры, face-блок «аниме-лица», квалити-цвет — ТЕГАМИ, без прозы). (docs/VERDICT-ANALYSIS-2026-10-11.md:19-33; thread4/specs/policy.json:115-123)

## 5. ПРАВИЛА DO/DON'T (конституция, вердикты, факты)
- DO: писать сразу в PH-форме (тег-блок → noun-led проза → квалити-теги); заявка — тегами в начале тег-рана; существительное несёт заявку, глаголам можно быть скучными. (thread4/CONSTITUTION.md:132-141; RULES_CORE-ORIGINAL.md:155-166)
- DO: анти-лик guard в каждом NEG; counter-NEG обязателен для каждой exposure-заявки; анти-лоли пол в NEG. (RENDERER_FACTS.md:27-28,39-41,71-74)
- DON'T: не класть заявку только в прозу («PH не рисует прозу» — failure mode «Sermon»); не доверять тег-рану вне PH-формы; не строить гейтов на PH-словах (вердикт Кенни: PH — посредник POS→PH→картинка→тир, отделить «слово вызвало тир» от «слово отражает заявку» нельзя). (thread4/NICHE.md:412-414; LIVING-NOTES.md:47)
- DON'T: PH-simulation/grinding НЕ обязателен — ph_sim_gate-тулинг = опциональная страховка, никогда не обязательная стадия пайплайна. (RULES_CORE-ORIGINAL.md:162-163,233)
- NOT FOUND: токен-лимиты PH, поведение PH с weights `(tag:1.3)`, PH на Tsubaki.3 — в thread4 не найдено. Вопрос «стрипает ли PH "2D hand-drawn anime illustration"» признан мутным/Tsubaki.3-специфичным. (RULES_CORE-ORIGINAL.md:167-169)

## 6. ВЕРБАТИМ-ПРИМЕРЫ
- Протокол из шапки батча: «RENDER PROTOCOL: PH ON — the tag-run is the truth channel; prose carries the beauty». (thread4/batches/T4-04.md:20-21)
- Фрагмент POS P01 (T4-04), PH-форма: «anime style, ecchi anime style, 1girl, solo, … see-through, nipples through clothing, … steam press room, … — The steam press room runs night-ink blue … the dark of her nipples reading plain through the weave … Her face is rendered in stylized 2D anime style: anime eyes (red left, blue right…), small nose, small mouth… — Masterpiece, best quality, anime artstyle.» (thread4/batches/T4-04.md:42)
- Что PH реально отправил (PH Rewritten, T4-04 OC-1, фрагмент): «An eye-level medium shot captures a lone female student kneeling forward in a dim, atmospheric steam press room… the blouse is damp and see-through from the steam, revealing her nipples… rendered in a high-quality, stylized 2D anime style…» (verdicts/T4-04-author-verdict.md:12)
- Токен-репликация (H2): PH повторил «erotic pose» дословно — «as she poses erotically». (thread4/thread4/LIVING-NOTES.md:82)

## 7. ПРОТИВОРЕЧИЯ
- Польза PH: T4-04 #10 «PH-версия в разы круче» vs T4-22 «проза доходит 0%, теги 37%» vs итог — T4-26 (RAW, без PH) стал пиком 17/25. Обе стороны подтверждены; консенсус треда: PH-форма полезна как ДИСЦИПЛИНА письма, но канал доставки — теги; финальный выбор треда — Raw без PH + перенос PH-наработок в RAW+ тегами. (VERDICT-ANALYSIS-2026-10-11.md:23,30-32; policy.json:115-123)
- GROK-PROMPT.md называет PH «placeholder» и «мы НЕ работаем через него» — это консультация RAW-эры, согласуется с переходом T4-23+, но не с PH-эрой T4-04..T4-22. (thread4/GROK-PROMPT.md:205)
