# SLOT-KIT — «Slagfield Bathhouse» (R3, выжимка из памяти проекта; корень thread5/)

## 1. ЖАНРОВЫЕ ЗАКОНЫ
- **OC** — «канон-локи персонажа (P01–P03), тема в слоте. R+» (LAWS.md §5). С T5-10 OC-слоты классом EXQUISITE (FAIL-гейт) и НЕ следуют теме батча (вердикт T5-05); имена OC никогда в POS.
- **VOLT** — «плоть: камера-участник, тело в движении, взгляд-вектор, экспозиция тегом. R+/X» (LAWS.md §5). Закон №18 (TASTE.md, дословно): «Волт — это промпт о теле, девушке и её сексуальности в моменте»; механизм без реакции тела = R максимум. VENUS (ars/03-VENUS.md): у каждого VOLT-слота «своя физика слота — закон ткани/света, который двигает тело»; камера-участник читается из физики, не из прилагательных.
- **NICHE** — (NICHE.md §К, verbatim) «the IMPOSSIBLE image. The race's anatomy does PHYSICAL WORK in the frame (mechanism, not costume) — race tags in the tag block, the impossibility is the FIRST read of the silhouette, the witness object holds the frame». Четыре хода: разворот закона на одной точке / растворение (след, отражение) / раса-механизм / мир со своей логикой. Тир R (PG-13…R).
- **EXQUISITE** — «ультра своего жанра (ultra-VOLT / ultra-NICHE)» (LAWS §5); NICHE.md §З: «то же чудо, но на пределе — предельная невозможность, предельное достоинство подачи. Extremity with dignity: ультра это не „больше“, это „доведённое до конца“». R+.
- **EXP** — «болванки-гипотезы ПОВЕРХ 24-слотового закона, до 9, по умолчанию 2 (1 A/B-пара). Без темы батча… core-4 стек носителей, пары A/B отличаются ровно одной переменной» (LAWS §5); каждая EXP несёт expHypothesis/expVariable/expExpected, берётся с полки specs/open-hypotheses.json. **EXP-кандидаты в ОС**: соло-слоты, ≥3 фишечки канон-уровня (метка тела + предмет-подпись + регистр подачи), иначе «простенько» = FAIL (вердикт T5-07).
- **HEAT** (ARS-NOVEAU §4.9): спред рейтингов объявляется в шапке; диапазоны: NICHE = PG-13…R, VOLT = R…R+, EXQUISITE = PG-13…R+, OC — по канон-тейпу; дефолт без HEAT — R+×14 · R×7. Тир-таблица (LAWS §3): **R** = lingerie / panties / bra / upskirt / erotic pose; **R+** = cameltoe / taped nipples / topless with tape / handbra / visible pantyline / nipples through clothing — «3+ R-сигнала через 2+ слоя»; **X** = «соски или гениталии видимы» (X Cut = один жёсткий факт; X по умолчанию изъят); XXX — никогда. R+/X проходят 9 звеньев салиенса (LAWS §4) и только LOW/MID позы.

## 2. РАССЫ ДЛЯ NICHE (specs/races.json v2.3.0; теги verbatim)
- **R18 Gargoyle-kin**: `small stone horns rough-textured; stone patches at the forearm`.
- **R25 Slime-girl**: `translucent gel body; semi-liquid hair dripping slow; core-orb glowing inside; body holds shape by will`.
- **R32 Golem-kin**: `glowing seam-cracks in smooth clay skin; moss patches; heavy slow build`.
- **R22 Flame-salamander kin**: `crest of low fire along the spine's line; ember-freckles at the jaw`.
- **R15 Porcelain-doll**: `bisque skin with seams at joints; ball-joint elbows-and-knees; painted blush fixed`.
- **R13 Merfolk-adapt**: `scales shin-and-hip; tide-line-tan`. (Запас: R16 Moth-kin `dust-scales at the collarbone`, R21 Mushroom-kin, R17 Jellyfish-kin gold.)
Правила: раса = механизм, не костюм — ≥2 фичи расы в POS; каст 12–14/21; R30 Frog-kin на карантине; banned: dwarves/goblins/trolls/orcs; кин-дрейф: monster-girl латенты усиливать `original character`.

## 3. КОДЫ (bathhouse/steam/industrial)
**Позы** (specs/poses.json; R+/X → только LOW/MID): PL72 Bath-Rim Knee-Sit (MID) · PL113 Tub Rim Arm-Drape (MID) · PL71 Towel Clamp Stand (MID) · PL232 Mirror-Lean Across (MID) · PL226 Steam-Squint Emerge (LOW) · PL147 Mirror Eye-Lock (LOW) · PL124 Railing Perch Lean (LOW) · PL114 Pool Chin-Rest (LOW) · PL29 Mirror Face-Off (LOW; статик-вертикаль, кап 2/батч) · PL197 Bath-Sheet Step-Out (HIGH — только R/PG-13).
**Кинетика** (отдельного kinetics*.json НЕТ; K-коды живут в specs/pools.json → sections.kinetics_k): K61 mid_drip «single drop mid-fall (sweat/water/rain)» · K92 mid_waterline_rise · K160 mid_towel_last_grip · K162 mid_float_surrender · K165 mid_shiver_wrap · K168 mid_hair_squeeze · K178 mid_puddle_leave · K131 mid_wade_dark · K80 mid_pour · K148 mid_heat_bank («anger banked like a forge at night»).
**Носители** (specs/carriers.json; core-4: группы FABRIC+BODY+POSITION+PHYSICS, классы W=Fabric State, B=Body Topography, E=Garment Displacement, D=Kinetic Weight, S=Skin Framing, I=импринты…): CR-W27 Steam-Damp · CR-W32 Steam-Cling Front · CR-W53 Steam-Soft Knit · CR-W07 Plastered Wet Shirt · CR-S22 Steam-Gloss Skin · CR-S12 Water Beads · CR-E06 Towel Fold · CR-E07 Robe Drift · CR-U22 Bath-Steam Bare · CR-D29 Steam Curtain Rise · CR-D53 Steam-Rise Lift · CR-I20 Steam-Fog Mirror · CR-I17 Wet Footprints.
**Палитры** (specs/palettes.json, 160 шт): P15_INDUSTRIAL_STEEL «raw_mechanical_contrast» · P58_INDUSTRIAL_DUST «industrial_decay_atmospheric» · P69_EMBER_FROST · P116_AFTERGLOW_EMBERS «the-room-keeps-her-warmth» · P76_IRON_TIDE · P78_RUST_LULL · P60_FIRE_ASH · P31_VOID_ASH · P35_VOID_EMBER · P03_CYBER_ASH · P12_AUTUMN_RUST · P152_LEATHER_TANNERY_AMBER. Правила: ≥7 палитр/батч, ≤3 повторов, ANTI-WASH в NEG (`washed-out, faded colors, low contrast`).

## 4. HAIR-EYE (specs/hair-eye-library.json v1.0.0) — для рандом-девушек
Структура: `hair` (31 значение) + `eyes` (20) + `suggestions.a5_bindings` (подсказки палитра→цвет) + `rules`. Закон E3: «hair/eye выбираются НЕЗАВИСИМО от палитры: палитра — настроение/свет, hair/eye — идентичность персонажа»; соседние слоты не несут один цвет волос (цель 12+ цветов на 21 мейн); OC берут канон (oc-canon старше библиотеки). Примеры verbatim — hair: `ash-brown`, `copper`, `ice-blue`, `teal`; eyes: `hazel`, `sea-glass`, `pearl-grey`, `heterochromia`; binding: `{"palette": "Forge Ember", "hair": "red", "eyes": "amber"}`.

## 5. TASTE — 28 законов (титулы; сквозная нумерация, в файле счёт перезапускается блоками)
1. 24-slot law (21 мейн + 3 OC) · 2. Genre visibility · 3. Prop geometry (контакт-анкоры) · 4. R+ hard-claim (именованный edge-объект) · 5. Mechanism-aware counter-NEG · 6. Claim visibility + layer clarity · 7. Render-proven claims only (cameltoe никогда) · 8. Fabric state mandatory · 9. No underlayer on the claim zone · 10. Dead fabrics carry no edge · 11. OC names never in POS · 12. Салиенс решает тир, не присутствие тега · 13. Измерение системно или его нет (A/B) · 14. ЗАКОН КОНТАКТА (расширенный) · 15. ЗАКОН NEG-СМЕЖНОСТИ (NEG лочит слой, не ступень) · 16. ЗАКОН NATURAL (вес/провис тегами) · 17. ЗАКОН ПАРАЗИТА (предмет из POS стремится на тело) · 18. ЗАКОН VOLT-ТЕЛЕСНОСТИ · 19. ЗАКОН NICHE-МИРА (невозможность = физический объект ≥1/3 кадра) · 20. ЗАКОН ЧИСТЫХ РУК (без мета-слоёв; +RICH-СТЕЙДЖИНГ) · 21. ЗАКОН ПЛОСКОЙ НАТЯЖКИ (X-риск без света-на-зоне) · 22. ЗАКОН РАЗБРОСА (интерлив) · 23. ЗАКОН ЦВЕТОВКИ (палитра каждому промпту) · 24. ЗАКОН ОПОРНОЙ ГЕОМЕТРИИ · 25. ЗАКОН NEG-ГИГИЕНЫ (бан-лист nude-смежных в NEG) · 26. ЗАКОН «ТЕМА — НЕ ТЕГ» · 27. КАНАЛ R+ «БУГОРОК — ДА, РОЗОВОЕ — НЕТ» (through-заявка только на тёмной ткани) · 28. ПРОСВЕТ-ЧЁТКОСТЬ (law №1: поза — главный носитель тира).
(Док-путь: docs/TASTE.md; отсылки №1 = «поза — главный носитель», №13 = контакт-физика по карте T4-25.)

## 6. RENDERER — top-10 фактов (docs/RENDERER_FACTS.md)
1. Движок **Tsubaki.2 Pro** постоянный; Tsubaki.3 отвергнут («полное говно»).
2. **PH RESHAPES**: писать сразу в PH-форме; noun-form живёт verbatim, verb-led flourish съедается целиком.
3. **Milf skew**: `adult woman`/`mature female` в POS перекашивает ВЕСЬ батч → слово milf запрещено (LAWS §2.7); возраст — только формой тела (регистры: petite/slender=студентка, athletic/curvy=молодая, full=милф).
4. **State tags рендерятся** («back arched», «one arm above head»); narrated grace — нет. Экспозиция = явный тег + counter-NEG, прозой недодаётся.
5. **Candle/lamp spawn guard**: приборы не называть в POS вообще (гард в NEG не спасает — ЗАКОН СВЕТА v2, 04-EARTH); свет поведением («the light holding the beam line bright»).
6. **TAG = COMMAND**: `see-through` / `nipples through clothing` рисуют цветной сосок через ЛЮБУЮ ткань → through-заявка только на ТЁМНОЙ ткани; светлой/средней — `covered nipples` + `wet clothes`/`see-through` (закон №27 «бугорок без цвета»); `light on chest` запрещён. Cameltoe — рендер-мёртв.
7. **Bare-under позитивом**: `nothing underneath` в POS; NEG-лок подслоя не держит (рисует поверх) — подслой лочится в NEG.
8. **Кадрирование тегом** (close-up / cowboy shot / upper body), не прозой.
9. **POSE-RISK**: HIGH-поза × R+/X = амплификатор мутаций → только LOW/MID.
10. **Порядок тегов: ранние весят больше** — заявка ≤ токена 60, POS ≤130 слов (150 hard). Плюс: каждая рисуемая деталь — в POS явно (policy v1.11.0 posFullSpec, FAIL с T5-10; палитра — не паннацея); Yodayo = доверенный оракул тира, X-посты алгоритмически душатся.

## 7. ШАБЛОН СЛОТА (verbatim из batches/T5-10.md, P01) + POS + NEG
```
P01 — zia-gale-frenzy (EXQUISITE · Zia · R+ · PL104 · P112_POCKET_THEFT_GOLD)
Channel: r-geometry (live; ветер несёт геометрию юбки и обёртки)
THESIS: «ВЕТЕР ЗАБРАЛ УПРАВЛЕНИЕ — ОНА СМЕЁТСЯ»: Frenzy как восторг, не
ужас; … Канонический регистр «lets it lead» доведён до предела.
Canon: small half-curling ram horns in dark teal-green; … — VERBATIM
specs/oc-canon.json (Zia, GALE, VI — The Lovers). Гэг-стек: …
Spine: PL104 Dance-Break Snap · K88 mid_scale_tilt · CAM02_rooftop_front ·
LEAD the-own-wind · frenzy register · closer scene-close
Race: — (human; канон VERBATIM; хвостов НЕТ — канон-лок)
Gar: — (канонический гардероб: …)
Stack: CR-W24 + CR-B03 + CR-E02 + CR-D02
POS:
anime style, original character, 1girl, solo, dark brown hair with teal-green ends streaming, vivid crimson-red glowing eyes, manic with joy, small half-curling ram horns in dark teal-green, pointed elf-like ears in red ribbons, warm tan skin, full broad-across frame, heavy set breasts, the gust defeats her wrap top's knot, the wrap off one shoulder, covered nipples one soft flash in the cold crosswind, heavy satin skirt belled high by the same gust, pale-blue-cool lining flashing, loose ribbons spiraling around her forearms, rooftop laundry line snapping overhead, wide laughing mouth with small pointed canines, low three-quarter view into the wind, scene-close, theft-gold-bright asphalt-black with denim-night-blue secondary, ticket-red-vivid accent on the streaming ribbons, streetlamp-silver-edge glint, stylized 2D anime face, anime eyes (vivid crimson-red, manic with joy), small nose, small laughing open mouth, cold crosswind light holding the bare shoulder line bright, masterpiece, best quality, anime artstyle.
NEG:
exposed genitals, vulva, pubic hair, child, children, childish, chibi, young girl, immature body, oversized head, loli, shota, signature, watermark, artist name, logo, candle, candles, candelabra, lamp, bulb, lightbulb, lantern, torch, chandelier, brazier, male, man, 1boy, 2girls, multiple girls, milf, mature female, adult woman, [анти-канон/анти-теза слота], washed-out, faded colors, low contrast, photorealistic, 3d face, realistic facial structure, flat colors, muddy colors, dull, overexposed, underexposed, bad anatomy, extra fingers, bad hands
```
Скелет NEG (BASE-флор hard-флоров §2: genital lock, anti-loli, leak guard, candle-гард, male/multiple girls, milf — затем анти-канон слота, затем ANTI-WASH + quality-хвост). Полный P01-NEG у меня на руках (81 «слово»), в эхо-батче просто зеркалить структуру.

## 8. OC-BODY-ARCHIVE (specs/oc-body-archive.json; born 2026-10-16, canon v2.3.0 FAM-нормализация)
Структура: `bodies{}` — проза-телословие по каждой OC (родословная; машина в POS несёт тело 3–5 тегами формы). FAM-коды: **FAM-A** = full / broad-across, вес решает, куда идёт ткань (Lucy, Zia, Rin); **FAM-B** = soft and settled, gently full for her frame (Rue); **FAM-C** = small-boned, compact, softly mounded (Mab, Lyn). Прочие тела вне FAM: Vae (tall curvy hourglass), Ana (tall full-figured, «bearing of dominion»), Nix (slim athletic, small breasts explicit), Ila (athletic stone-kin build), Doe (thick toned thighs), Sue/Miyu/Ash (slender), Ama (rain-sag comfort) — всего ~20 записей. Регистры возраста формой: petite/slender=студентка · athletic/curvy=молодая · full=милф (milf-квота 1/33 по тегу, только Sue).
