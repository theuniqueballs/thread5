# THREAD 4 — RENDERER_FACTS.md

Empirical facts about the rendering chain (PixAI / Tsubaki.2 Pro + Prompt
Helper / Yodayo). Every fact here is tested, with provenance. Facts feed
recipes, gates, and templates. A fact that fails retest gets amended via
event, never silently.

## ENGINE

- **Tsubaki.2 Pro** is the standing engine. **Tsubaki.3 tested side-by-side
  on N30 and rejected: «полное говно»** (comparable to Tsubaki.2 at its own
  launch). Everything parked for Tsubaki.3 (chiaroscuro/specular module,
  @image1 reference consistency) stays parked until it matures. [C-N30]

## PROMPT HELPER (PH)

- PH does NOT sanitize by format — it RESHAPES input into its own form:
  tag-block → prose → quality tags. Content already in that shape passes
  **verbatim, no rewrite at all**. ⇒ Write in the target shape. [C-N30]
- PH trims verb-led poetic flourish with no visual payload («the pool drew
  itself»); keeps noun-form visually-loaded phrasing (a strap slipping, a
  specific color, a named texture). ⇒ Nouns carry the claim; verbs are
  allowed to be boring. [C + RF-002: verb-led carriers eaten wholesale]
- The tag-run is NOT a PH-resistant channel — PH dissolves it into prose
  when it isn't already in PH shape. (RF-002: claimed R7/R+12/X2 rendered
  ≈ PG×13/PG-13×3/R×5/weak-R+×2/R+×1/X×1.)
- PH LEAKS: artist tokens self-inserted (stuart_pot ×3), character tokens
  (grey_wolf ×2). ⇒ Anti-leak NEG guard on every prompt. (RF-002)
- PH's own maturity layer is gone in the current mode; the anti-loli NEG
  floor is ours to carry. (3.2 §53 history.)

## TAG / RENDER BEHAVIOR (Tsubaki.2)

- `adult woman` / `mature female` in the POS tag block skew the WHOLE
  batch toward MILF-coded results — batch after batch, not only where
  wanted. Tested on N30. ⇒ Age registers live in prose narrative only. [C-N30]
- Tagged physical state renders reliably («back arched», «one arm above
  head»); narrated grace does not. [C]
- Exposure delivered via explicit signal tag + counter-NEG works exactly as
  intended; the same intent as pure prose under-delivers. A/B tested. ⇒
  counter-NEG is a required axis of every exposure claim. [C]
- «off-shoulder, bare shoulder» alone reads PG-13 regardless of prose
  framing. Tier signal must be explicit. (N31 P01/P03 failure.) [C-N31]
- Opener bundle (N31, tested together, split unconfirmed): `anime style,
  ecchi anime style, hentai anime style` opener + face-lock without
  `flat cel-shaded` («relatively better»). Adopted as tier-laddered default.
  [C-N31]
- Face lock form: drop «large expressive» — plain `anime eyes`. [C]
- Spurious light-source spawns (candle, lamp, lantern, torch, chandelier,
  brazier) without a NEG guard. ⇒ Spawn guard in BASE_NEG unless the
  concept calls for one. [C + 3.2 §40]
  - **AMENDED 2026-10-28 (T5-06, A/B автора):** гард НЕ блокирует спавн —
    `lamp` в NEG не спасла; POS-слово прибора сильнее NEG. Лечение в POS:
    свет поведением, приборы не называть (закон: `docs/ars/04-EARTH` §
    ЗАКОН СВЕТА). Гард остаётся страховкой, состав + `bulb, lightbulb`
    (bulb из POS спавнилась вне гарда). Рабочая замена: «the bulb light
    …» → «the light holding the beam line and her chest bright» — прибор
    ушёл. [C]
- Tsubaki.2 handles rich atmospheric/cinematic light natively — no
  chiaroscuro scaffolding needed (that was a Tsubaki.3 workaround). [C-N30]
- The X recipe of 3.2 (bare state doubled + fantasy anatomy + open mouth)
  held at render (RF-002 P14) — but is RETIRED as a general recipe; each
  tier now carries a full recipe (constitution §4, author 2026-09-19).
- Taped nipples (X-tape) render and classify R+ — the tape holds the tier.
  [C + 3.2 platform empirics]

## YOADAYO (platform)

- Community ladder: PG / PG-13 / R / R+ / X. XXX never (our floor, and
  platform-illegal content anyway).
- X-rated posts are algorithmically suppressed regardless of quality. The
  author manages accidental-X in-editor (tape/crop) — the rating gate is
  advisory-at-the-margin for X drift, HARD on the floors (genitals, XXX).
  [C]
- Author's own tier table (2026-09-19) — the classifier of record, see
  CONSTITUTION §4.

## MATURITY (author directive 2026-09-19)

- Loli → always NEG (child, childish, chibi, young girl, immature body,
  oversized head).
- Positive-side diversity as registers: студентки (college students),
  молодые (young women), милф (MILFs). **Бабулек не надо** (no grannies).
- No maturity protection needed in POS — no age tags at all (the N30
  MILF-skew receipt).

## OUT-OF-PROMPT FACTORS (author's techniques table, block 10 — 2026-09-21)

- **Модель / LoRA**: разные веса тянут в разные стороны — одни
  «стесняются», другие рисуют наготу сами.
- **Вес тегов `(tag:1.2)`**: усиливает или ослабляет конкретный сигнал.
- **CFG scale**: высокий CFG слушается промпта жёстче, низкий даёт
  «случайные» вольности.
- **Sampler / steps**: влияют на детали (соски, ареолы, прозрачность).
- **Соотношение сторон**: вертикальный кадр акцентирует фигуру,
  горизонтальный вносит сцену.
- **Порядок тегов: ранние весят больше** — НЕЗАВИСИМОЕ ПОДТВЕРЖДЕНИЕ
  рендер-закона №5 из рендер-вердикта T4-03 (хвостовые сигналы
  рендерятся слабо, claims в первых ~12 тегах). Авторская таблица и
  наш рендер-вердикт сходятся без сговора.
- **Правила платформы**: Yodayo/PixAI сами метят и фильтруют по
  рейтингу — разъяснения площадки проверять.

Full map: `specs/rating-techniques.json` (104 приёма, блоки 1–10,
efficacy ●/○ по тирам) — конституция §4-поправка.

## RENDER LAW v1.3.0 (вердикт T4-05, 2026-09-23)

- **Bare-under позитивом**: NEG-лок подслоя НЕ удерживает рендерер —
  лифчик нарисован ПОВЕРХ NEG-лока (P07). POS обязан нести позитивное
  утверждение («nothing underneath» / «braless»).
- **Кадровый тег**: кадрирование заявки живёт тегом (close-up / cowboy
  shot / upper body), не прозой — проза кадр не доставляет.
- **Запрет слов-персонажей**: омонимы данбуру — только составными
  (aurora → aurora_(arknights), P08: «пробежал персонаж»).
- **POSE-RISK**: HIGH-поза × R+/X = амплификатор мутаций (P04 дрейф ·
  P22 мутация · P17 недолёт) — R+/X получают только LOW/MID позы.
- **BLOCKER**: шаль/руки крестом поверх заявки = мёртвый слот до
  рендера (P21 «the frame's one closed door»).
- **Площадка-оракул**: тир Yodayo ≡ глаз автора 24/24 на T4-05 (45/45
  за два батча) — пост-рендера доверенный оракул; разрыв тира живёт ДО
  рендера (в контракте/промпте), не после.
- **Стохастика**: R+ ~4/15 при законе (T4-05) — кадр лучшей
  вероятности + перекидка; канал-частоты: specs/delivery-stats.json.

## T4-30 RENDER RECEIPTS (2026-10-13)

- **CHARACTER-BLEED** (P13, дословно из вердикта): «она почему-то
  перемешалась с персонажем из Zenless Zone Zero — Yidhari, получились
  ебанутые помехи и шлаки». Кин-латенты monster-girl (arachne girl,
  spinneret, small chitin legs, symbiote-палитра) тянут узнаваемых
  персонажей чужих вселенных. Триггер не локализован (кандидат — сумма
  arachne + spinneret + dark-elegant). Фикс-кандидат: при признаках
  блида ослаблять кин-токены и усиливать original character. Ретест
  T4-31.
- **A/B STOCHASTIC** (P25): «на половине прорисовано чётко, на другой
  еле-еле» — один слот/один сид, разброс качества внутри серии
  рендеров. Канал R+ на WET-тонкой ткани — вероятностный; автор ставит
  тир по лучшему кадру серии (перекидка — техника блока 10).
- **PLATFORM-ORACLE**: T4-29 + T4-30 = 54/54 слотов «с площадкой ↑0 ↓0»
  — Yodayo-тир ≡ глаз автора два батча подряд; разрыв тира живёт ДО
  рендера (в контракте/промпте), оракул остаётся доверенным.

## OPEN QUESTIONS (retest when it matters)

- Opener bundle split: style-tag swap vs cel-shaded drop — which one did
  the «relatively better» work? [C-N31]
- Does `hentai anime style` on PG-13/NICHE slots push exposure? Current
  policy: tier-laddered opener (constitution §6).
- VLM render-reading: can uploaded renders be auto-graded? — attempt
  authorized by the author 2026-09-19 («если хочешь — можем попробовать»).

## T4-31 RENDER RECEIPTS (2026-10-14, глаз автора, 32/32)

- **TAG = COMMAND (физика ткани не симулируется)**: «see-through» /
  «nipples through clothing» рисуют ЦВЕТНОЙ сосок через ЛЮБУЮ ткань:
  свитер (P09 dark-teal knit, «розовые соски через свитер — не могут
  просвечивать бро»), не-сквозная жёлтая кофта (P12 «которая НЕ
  просвечивается — соски красные»), sheer-чёрное (P26). Приговор: тег
  не описание, а инструкция; плотность/тон ткани её не отменяют.
- **СВЕТ ЗАДАЁТ ТОН**: P04 sheer BLACK leggings + «single_prism_source_
  spectrum_split light falling full on the sheer leggings» → рендер
  белый → цветной сосок → X. Тон зоны = цвет слова × свет на ткани:
  заявки через-ткани требуют свет НЕ на зоне (контровой/off-frame).
- **ТОН-ИЗОЛЯЦИЯ (EXP-пары P25-P32)**: 8 слотов, 7 × X — тон-пары
  (светлый↔тёмный, остальное одинаково) обе половины X при wet/через;
  выжила одна DRY-тёмная (P30, бугорки). Тьма без влаги + covered —
  единственный R+-путь; тьма с влагой — X (подтверждение №27-уточнения
  второй серией).
- **A/B-АТРИБУЦИЯ (κ/λ/μ)**: κ = P04 X / P05 R+ (разница — призма-свет
  на ткани зоны); λ = P07 R+ / P08 R (обе живые, расщепление мягкое);
  μ = P09 X / P10 X (через-заявка на knit — обе половины X, тон
  бессилен против тега).
- **ORACLE-PLATFORM**: T4-31 «с площадкой ↑0 ↓0» — Yadayo ≡ глаз автора
  ТРИ батча подряд (82/82). Разрыв тира живёт ДО рендера, в промпте.
- **WTF-РЕКВИЗИТ**: мерная лента на груди (P03) без кадровой логики
  читается автором как ошибка («нахуя она»), не как тема. Реквизит-
  носитель темы обязан объясняться действием/позой.
- **СЛОЕВАЯ НЕСОВМЕСТИМОСТЬ**: подвязки-бретельки поверх купальника
  (дословно «нахуя») — рендерер рисует любую комбинацию предметов;
  семантику дресс-кода обязан держать ПРОМПТ (закон-материал №29).
- **ГРЯЗНАЯ ОТРИСОВКА**: «иногда соски пиздец неаккуратно и убого
  рисуются» — точность прорисовки нестабильна при сильных через-тегах;
  лечение-кандидат: весовые коэффициенты RAW (1.1/1.2) — легализованы
  автором как инструмент, EXP T4-32.

## T5-06 RENDER RECEIPTS (2026-10-28, глаз автора, чат)

- **PH-ON (аварийный)**: батч отрендерен с включённым Prompt Helper
  (PixAI) — «случайно генерил с включённым Prompt Helper». PH пересобрал
  промпты в свою форму ⇒ построчная атрибуция «что сработало» для этого
  батча НЕДОСТОВЕРНА: слот-выводы T5-06 помечать как слабо-доказательные.
- **ТЕМА-ДОСТАВКА ПРИ PH-ON**: «рендеры по теме получились охуенные»
  (дословно). RAW+ пережил PH-пересборку без потери темы и жанровой
  физики. Опыт: тема живёт не только в микротегах — держится слоями
  (палитра, свет-поведение, реквизит, раса-механика).
- **СПАВН ПРИБОРОВ**: bulb-инцидент P03 → ЗАКОН СВЕТА v2
  (docs/ars/04-EARTH, 2026-10-28): POS без приборов; NEG-гард —
  страховка, не лечение.

## T5-07 RENDER RECEIPTS (2026-10-30, вердикт автора, прилавок)

- **СЛОВА ТЕМЫ — ЛЕГАЛЬНЫ КАК ПРЕДМЕТ.** «Я предлагаю не запрещать
  использовать слова из темы, например - тут бы Dungeon прижилось
  неплохо» — полный запрет ТЕМА-СЛОВ (T5-07 шапка: «гейт: никогда в
  POS») оплачен смертью: слово темы, называющее отрисовываемый предмет
  кадра/среды, работает на тему сильнее заменителя. Новый закон: «тема —
  тег по делу» (LAWS §6, 04-EARTH § СЛОВА ТЕМЫ v2). НИКОГДА: IP/франшизы,
  титул темы целиком, слова-персонажи.
- **КИН-МЕХАНИКА ПОДТВЕРЖДЕНА ЛЮБИМЫМИ.** 4 из 6 любимых слотов автора —
  кин-слоты (P16 Medusa-kin R40, P20 Arachne-kin R35, P22 Bat-kin R11,
  P24 EXQUISITE): раса-механизм в кадре работает (§4.13). Приказ: кины в
  основной теме активней — каст 12–14/21 (policy v1.8).
- **R30 FROG-KIN: РЕНДЕР-ПРОВАЛ.** «Фрог-кин вообще не получился» (P33,
  PG-13): раса на трёх нейтральных чертах (глаза/перепонки/горло) без
  физической работы в кадре — не читается. R30 → карантин (races.json
  v2.3.0). Класс в RENDER-TROUBLES Д1: кин без механизма = провал слота.
- **EXP-КАНДИДАТЫ: «ПРОСТЕНЬКО».** «Фишечек которые есть у основного
  ростера моих ОС [нет], они - хоть они и кины, но выглядят простенько»
  — кандидат = раса + одежда не дотягивает до ростера. Закон EXP: ≥3
  фишечки канон-уровня (метка тела + предмет-подпись + регистр подачи),
  LAWS §5; RENDER-TROUBLES Д2.
- **POS-БЮДЖЕТ: ЧЕСТНАЯ ЦЕЛЬ 130.** 20/33 слотов T5-07 жили в 111–150
  слов при вердикте «мне всё очень понравилось» — цель 110 была занижена
  (WARN-шум 60% слотов). gates.json v1.1.0: targetTokens 130, hard 150.
- **HEAT-СПРЕД R/R+ ПОДТВЕРЖДЁН.** Любимые автора в обоих тирах (P06/P16/
  P23 — R; P20/P22/P24 — R+): разнообразие рейтингов работает (квитанция
  T5-06 «умерло: моно-R+» закрыта практикой T5-07).
