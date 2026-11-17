# THREAD 5 — Batch T5-23: "VENATOR" — БАТЧ (PROSE PLUS)

заказ (вербатим автора, 2026-11-15, чат → прилавок):
«Новая основная тема: VENATOR. Хочу наборчик девчонок у которых будут какие-то явные
выразительные фишечки и всё крутое. На картинке будет всё как в дедлоке - девушка, у
неё есть какие-то важные отличительные признакИ, интересные и крутые - по типу
туатуировок, очков, повязок на глаз и так далее.. (об этом очень давно забыл дрессер
или он это не умеет, я хуй знает) и у девчонки будет оружие! Оно может быть как
простое, так и спиритическое. В общем, придумаешь что-нибудь клёвое, я уверен.»

Темы для ОС: Intro-Prompt (Dove) R+ · Intro-Prompt R+ · Intro-Prompt R+. «сунешь тех,
кого брали недавно (кроме Meine)» (чат автора, 2026-11-15). EXP ростер: 9 слотов —
9 новых комбо (Y1-Y8, продолжение), 9 новых кандидатов в ОС, 9 новых пробных палитр.
«Всё это размазываешь на 9 слотов. То есть в одном слоте - одно комбо, один кандидат,
она новая пробная палитра.»

Поручения исполнены ДО сборки: (1) новая основная тема — VENATOR (охотницы с
signature-фишечками и оружием; IP-имя в POS — 0; дедлок-вайб живёт ФИШЕЧКАМИ, не
референсами — своих собираем); (2) три ОС-темы «Intro-Prompt» — представление-визитка:
Dove (канонизация вчера, T5-22 P16) · Qwen (R03, канон 2.10.0 — ДЕБЮТ, долг «Qwen ждёт
дебюта» закрыт) · Ruuj (R67, канонизация T5-21) — тройка последних канонизаций, Meine
исключена словом автора; (3) EXP ×9 = девять НОВЫХ Y-карт Y10–Y18 (camera.json 1.11.0,
продолжение серии по повторному приказу; Y1–Y9 в REWORK и в EXP не выходят — урок
вердикта T5-22, В27-физика вшита в каждый паттерн: вес/тяга/зацеп) × девять новых
кандидатов (R43/R50/R48/R45/R39/R58/R35/R33/R57 — все вне EXP-волн T5-21/22, новые расы
НЕ добавляются — урок В21) × девять пробных палитр волны 8 (P216–P224, материалы
отделки); (4) уроки вердикта T5-22 применены при сборке: В26 «якорь следует за заявкой»
(print/through-заявок в батче НЕТ — приоритет честной ткани), В29 NEG-якорь рамок в
insert/gap-сборках (insert-слотов нет — сборка без гэпов), В30 «тема несёт вес позы» —
оружие несёт вес позы в каждом мейне, фишечка читается формой в первых 12 тегах.

## SPINE (AXIS/ANTI/PROMISE)

AXIS: «охотница читается ДО выстрела: силуэт собирают фишечка и оружие — тату-змей
на предплечье, латунный монокль на цепочке, повязка с сигилом, шрам через бровь,
колокольчик-амулет — и копьё, упёртое в тазовую кость, лук-диагональ на спине, кнут,
наработавший шов, призрачная цепь, звенящая холодом. Оружие не висит accessory —
оно её скелет: вес переносится через древко, опора ловит наклон, хват держит кадр».
ANTI: «ни одного хоррор-регистра: ни gore, ни искр, ни разобранных тел; охота вежлива
— трофеи бережные, добыча уважена; никаких приборов света (закон света v2: свет
поведением и материалом — гребень-зола, перламутр-пыльца, жабры-розовость); никакого
IP-мусора: ни одного имени чужих героев, фишечки собираются своими токенами».
PROMISE: каждый мейн несёт ОДНО оружие (простое или спиритическое) ПРЕДМЕТОМ первых
12 тегов POS, и это оружие несёт вес позы (опора/контакт/тяга — В30); каждая охотница
несёт ≥1 явную фишечку формой (тату/очки/повязка на глаз/шрам/амулет/куклы-триске);
каждый R+ кадр открывается ЗАЯВКОЙ (коридор A/B объявлен) — оружие обслуживает
заявку, не наоборот (В25/В22).

## ГИПОТЕЗА ДВИЖКА: «ОРУЖИЕ — СКЕЛЕТ ПОЗЫ» (Г5, новая)

«Если изъять оружие из кадра, охотница рассыпается в generic-эччи; оружие обязано
нести вес позы, а не украшать её» (Г5: В30-проверка на новой теме).
ОЖИДАНИЯ (≥2, фальсифицируемые; вердикт проставит D14):
  (1) 21/21 мейнов несут оружие ПРЕДМЕТОМ в первых 12 тегах POS — опровергается,
  если хоть один слот держит оружие аксессуаром на фоне.
  (2) ≥14 мейнов несут оружие как ОПОРУ/КОНТАКТ/ТЯГУ (упёртое копьё, лук-диагональ,
  кнут-шов, цепь-спуск) — опровергается, если оружие висит мёртвым грузом.
  (3) Каждая охотница несёт фишечку ФОРМОЙ (тату/очки/повязка/шрам/амулет) в первых
  12 тегах — опровергается, если фишечка живёт словом THESIS без тела.

## ХОДЫ (§6, реестр moves-ledger.json)

M02 standing — «анти-открытка» (верхний грейд обязан ломать жанровую сценку).
M07 standing — «R+ заявка вещью»: токен канала — первый элемент заявочного блока (все R+).
M01 применён шапка — метафора батча: «охота — смена опор: оружие несёт вес, вес
строит кадр».
M04 применён P11 — остановленный мир (дозор на гребне: город внизу спит, алебарда —
гномон тишины).
M05 применён P06 — ловля на пролёте (приманка ловится на лету: лента и древко в
одном такте ветра).
M06 применён P24 — финал «трофей легче шага»: добыча весит совесть, сеть пустая.
M03 применён P00 — чужой IP-референс «Deadlock» назван автором КАК ВАЙБ фишечек:
построчный канон-чек чужих героев не требуется (ни один герой/предмет игры не
референсится; проверка: IP-имя в POS — 0, имена героев в POS/THESIS — 0; свои
охотницы собираются реестрами проекта).

## КАСТ

каст 12/21 в мейнах (прецедент T5-22): R02 Elf (P05) · R07 Dragon-kin (P11) · R11 Bat-kin
(P12) · R12 Bunny-kin (P23) · R13 Merfolk-adapt (P16) · R14 Dryad (P07) · R18
Gargoyle-kin (P14) · R22 Flame-salamander (P15) · R23 Shark-kin (P13) · R28 Sheep-kin
(P21) · R34 Phoenix-kin (P20) · R51 Crane-kin (P18); human ×9 (P04/P06/P08/P10/P17/
P19/P22/P24 + P24 EXQ); ОС — трио канона (Dove human · Qwen R03 · Ruuj R67), канон
VERBATIM, В28-сигнатуры отдельным клозом. Новые расы НЕ добавляются (В21). EXP:
R43/R50/R48/R45/R39/R58/R35/R33/R57 — кандидаты в ОС, все вне EXP-волн T5-21/22
(R62–R70 отдыхают после двух прогонов; волна T5-22 не повторяется: ноль зачётов,
урок «фишечка — формой в первых 12 тегах» применён).

## СПРЕД

EXQUISITE (ОС): R+ (3) · NICHE: PG-13 (2) · R (6) · VOLT: R+ (6) · R (5) · EXQUISITE
(мейн): R+ (1) · R (1) · EXP: R+ (8) · R (1). Спред 24 мейнов+ОС: R+×10 · R×12 ·
PG-13×2. Итого 33: R+×18 · R×13 · PG-13×2 (EXP-оверлей: R+×8 + честный R×1 — «супер
R+» = коридор A/B + токен таблицы тиров в каждом слоте, урок В24; кап 8.6-эры T5-23:
перегрев = FAIL — 18 ≤ 18).
Факт-право (rating-repair 2026-11-13): R+ бейдж легален только при коридоре A (грудь
закрыта объектом: рука/ткань/палантин/куртка в руках) или B (поза+камера несут интим:
mid-action, lean-back, kneel) — поле Corridor: объявлено в каждом R+ слоте. Fact 18 =
label 18. Эротика ≠ тир (В16): заявка-вещь — первый элемент кадра во всех R+; красота
— поверх заявки, не вместо (В22). Тема ≠ съесть (В25): оружие и фишечка — первый
слой, заявка — вещь.

## HEAT

HEAT-оплата разнообразия: 12 кинов из 12 разных рас (ни одного повтора),
21 оружие без повторов (копьё/лук/монокль-найденный/кнут/гарпун/цепь призрачная/
алебарда/веер ножей/лоза-сеть/сигнал-свисток/рапира/нагрудник/клинок-полир/сеть),
24 палитры без повторов, 12 фишечек-сигнатур (тату ×4, монокль, повязка-руна,
шрам, колокольчик-амулет, перьевые дорожки, чешуя-гребень, швы камня, спинной
гребень-зола) — ни одна пара слотов не делит пару (оружие, фишечка).

## СТРУКТУРА

33 слота = 3 канон-ОС «Intro-Prompt» (P01–P03, EXQUISITE R+, канон VERBATIM, закон
T5-05: DOVE → P01 · QWEN → P02 · RUUJ → P03; «кого брали недавно» = цепь канонизаций
Hana T5-09 → Meine/Luvv/Liebe T5-16 → Qwen T5-19 → Ruuj T5-21 → Dove T5-22, Meine
вычеркнута автором; Qwen — дебют-долг закрыт) + 21 мейн «VENATOR» (P04–P24) + 9 EXP
(P25–P33, без тем — прецедент вето T5-18).
Камера (мейки): D2×5 · D3×11 · D4×14 · D5×1; ОС: D3·A02 Dove · D2·A01 Qwen · D3·A02
Ruuj; EXP — по Y-картам Y10–Y18 (см. клетки). Токен «camera» — 0; приборы света — 0
(закон света v2; свет поведением: гребень-зола, перламутр-пыльца, роса-жемчуг, туман,
жабры-розовость).

## EXP-КЛЕТКИ (camera.json 1.11.0, y_cards Y10–Y18 — НОВЫЕ карты, продолжение серии)

Y10 = weapon-weight strap torque + cover by the crooked arm + upper body + slight low
angle (A, HIGH) · Y11 = kneel-back settle + hem pinned under shin weight + tails fan
frames the torso (B, MID) · Y12 = jacket sliding off one shoulder + sleeve caught at
the elbow fold + eye-level close (A, MID) · Y13 = apron wrap mid-turn + corner caught
in the elbow bend + hem arc still traveling (B, MID) · Y14 = lean back on both palms +
collar opens by the lean + fabric bridges taut across the ribs (A+B, MID) · Y15 = belt
cinch mid-pull against the perch's lean + weight honest on the seat edge + from below
(B, MID) · Y16 = shirt hem tucked by the raised arm + fabric bridge across the ribs
holds the line + upper body (A, HIGH) · Y17 = hem lifted where no hand holds it +
lower body passing through its own fold + eye-level (B, MID) · Y18 = glove peel
mid-grip + wrist-guard raising the hem line + close insert at eye level (A, MID).
Каждая карта несёт В27-физику (вес/тяга/зацеп) — урок REWORK Y1–Y9 учтён; SHEER сам по
себе слаб — сборка по паттерну целиком.

## EXP-ОВЕРЛЕЙ (palettes.json 1.9.0, exp_color_wave_8 — все 9 РАЗНЫЕ семьи материалов)

EXP-оверлей (9 EXP-слотов) × (кандидат · палитра P216–P224 по одной · Y-карта ·
кинетика 384–416); EXP-рейтинг R+×8 + честный R×1 (P33 — process-заявка без тир-токена).

P216_DAMASCENE_GOLD → P25 · P217_URUSHI_LACQUER → P26 · P218_NIELLO_BLACK → P27 ·
P219_CLOISONNE_EMERALD → P28 · P220_JADE_CARVE → P29 · P221_ABALONE_NACRE → P30 ·
P222_ETCHED_COPPER → P31 · P223_BONE_INLAY_PALE → P32 · P224_TOOLING_LEATHER → P33.

## ТЕМА-СЛОВА (реестр; слово легально, когда называет ПРЕДМЕТ кадра — LAWS §6)

the spear braced at the hip bone · the longbow slung diagonal across the back · the
knife's reverse grip at the hip · the lure ribbon snapped to the shaft · the vine
net's weave · the harpoon line coiled around the forearm · the halberd's butt as her
leaning post · the ghost chain's cold links · the rapier's riposte line · the empty
net rolled at the fist · the eyepatch's sigil stitch · the brass monocle on its chain
· the ink tattoo coiling the forearm · the scar splitting the brow · the trophy cord
at the belt · the signal whistle's knot at the wrist · the gill-plumes flushing with
load · the wolf made of dusk. НИКОГДА: «VENATOR» в POS; deadlock и имена чужих героев
(vindicta, wraith, haze, lash, ivy, beatrix, pocket, mirage, calico, infernus, yamato,
mcginnis, seven, abrams, dynamo, viscous, sinclair, shiv, holliday) в POS/THESIS —
тема живёт фишечками, не референсами (IP-флор); cyberpunk 2077 / night city /
ghostrunner / ghost in the shell / altered carbon / d&d (флор v1.3.1); robot, android
(триггерят чужих персонажей); wires in flesh, exposed gears, sparks, severed skin,
blood (хоррор-флор SPINE); приборы света: candle/lamp/lantern/torch/chandelier/brazier/
campfire (закон v2); экшн-жуть: muzzle flash, blood spray.

## ОС-ТЕМЫ (Intro-Prompt ×3 — свои для P01–P03, не тема батча — закон T5-05; слово
легально, когда называет ПРЕДМЕТ кадра)

Intro-Prompt = представление-визитка: канон-девочка знакомится со зрителем жестом,
который несёт вес (В30: жест представления — опора/подача/разворот).
P01 Intro-Prompt (Dove) R+ — the open palm offered at the showcase turn · the
price-tag cord looping the ankle · the drill curls counting their spins; НИКОГДА:
«Intro-Prompt» в POS, checkout-стойку, чужую витрину-магазин (её витрина — она сама).
P02 Intro-Prompt (Qwen) R+ — the doorstep bow held one beat long · the folded hands
low before the apron · the tail counterweight lifting as the head dips; НИКОГДА:
«Intro-Prompt» в POS, коленопреклонённый оффер-подарок (это поклон-знакомство, не
подача). P03 Intro-Prompt (Ruuj) R+ — the tide-line curtsey pressed flat by the
current · the gill-plumes flared wide by the wind · the one heel drawn back; НИКОГДА:
«Intro-Prompt» в POS, водяной поток в лицо, погружение (кромка, не глубина).

## АКТЫ

ОС (P01–P03): свои темы Intro-Prompt (закон T5-05) — EXQUISITE R+, канон VERBATIM.
ACT I — ТРОПА (P04–P10): след-чтение в приседе, дозор в развилке дерева, приманка на
ветру, лозовая сеть, веер ножей, маники-приманка у ворот, бег-взгляд через плечо.
ACT II — ЗАХВАТ (P11–P18): гребень крыш, спуск с колокольни по призрачной цепи,
гарпун-упор на пирсе, сторож на балке, шаг-зола, вейк-гарпун в лагуне, рипоста у
фонаря-соседа (без прибора: сталь читает свет соседа), плащ-пивот у болота.
ACT III — ТРОФЕЙ (P19–P24): примерка трофейного нагрудника, чистка клинка у окна,
трофейная комната, рубашка-одна после боя, свисток-сигнал в дождь, пустая сеть и
добыча весом совести.
EXP (P25–P33): девять проб-материалов по Y-картам Y10–Y18 (без тем — вето-прецедент).

## ОКНО РОТАЦИИ — Окно глубиной 3, прогон window.py при сборке

Прогон 2026-11-15T09:57Z, глубина 3 (T5-20/21/22): запрет — 99 поз, 99 палитр, 184
носителя, 8 каналов. Т5-23: позы новые PL529–PL549 (21 first-use) + реюзы вне окна
(PL56/PL81/PL97/PL106/PL111/PL115/PL123/PL124/PL125/PL129/PL145/PL150/PL151); палитры
— все вне запрета (свободные семьи + новая волна 8 P216–P224); носители — вне запрета
184; каналы — вне запрета 8 (запрещённые contact-physics / fabric-tension /
wet-sheer-delivery / r-geometry / tape-only / handbra-open-palms /
breast-environment-contact / nipple-ridges не использованы). Burn-актив (19 кодов) не
назначен: P04/P40/P69/P116, PL121/PL181/PL215, K07/K149/K166/K170, CR-W04/W28/H10.

═══════════════════════════════ СЛОТЫ ═══════════════════════════════

P01 — dove-showcase-turn (EXQUISITE · Dove · R+ · PL529 · P184_PEACH_RANSOM)
Channel: showcase-offer (live; открытая ладонь — подача себя, винил тянет блик по наклону)
Corridor: B
Combo: D6-03 OC THEME-OFF · Package: ε (GEOMETRY)
THESIS: «ЕЁ ВИЗИТКА — РАЗВОРОТ ИЗ ВИТРИННОЙ ОПОРЫ: ЛАДОНЬ ОТКРЫВАЕТСЯ К ЗРИТЕЛЮ ВЕСЕЛО
И ЧЕСТНО, КУДРИ-ДРЕЛИ КАЧАЮТ СЧЁТ ЗАВИТКОВ, ЦЕННИК НА ШНУРКЕ ВЕСИТ НА ЛОДЫЖКЕ — ОНА
САМА ПОДАЧА, КОТОРАЯ ПРОСИТСЯ РАСПАКОВАННОЙ».
Гэг-стек (4 фишки OC): 1) ладонь открыта раньше лица — вес уже перетёк на поданную
сторону; 2) парные дрели качают счёт завитков против движения разворота; 3) шнурок
ценника петляет по лодыжке — витрина следует за ней; 4) винил держит стеклянный блик
ровно там, где наклон тянет (канон-механика TAFFY).
Spine: PL529 Doll-Case Turn (OC_T5-23) (OC_T5-23) · K-FF mid_case_turn · CAM02 · D3·A02 · LEAD the open palm · showcase-candy register · closer image-close
Gar: CL-TS-13 (wet-look vinyl top, канон) + CL-SK-03 (frayed denim mini, канон) · HS: HS23 Drill Curls, Paired
Stack: CR-W40 + CR-B16 + CR-E11 + CR-D18
POS:
Masterpiece, best quality, absurdres, intricate details, showcase half-turn rising off the display lean, open palm offered toward the viewer, slight low angle, 1girl, solo, bubblegum-pink hair in paired drill curls, candy-red eyes, peach-cream skin, young slight build, small-and-softly-mounded chest, mid_case_turn
the wet clothes of her vinyl top clinging glass-tight at the chest, the open palm offered flat and honest — the offered palm is the claim, candy-made
the price-tag cord looping her ankle mid-turn, drill curls counting their spins against the turn's direction, the denim mini holding its fray line
Peach ransom palette, peach-cream glow over candy-vinyl-pink, ransom-gold at the price cord, denim-fade-blue faint at the skirt; her colors: the display she walks out of.
stylized 2D anime face lifting into the offer, anime eyes (candy-red, display-warm), small nose, small bright smile, paired drill curls framing the face in twin spirals.
NEG:
young girl, immature body, oversized head, loli, shota, signature, watermark, artist name, logo, 1boy, candle, lamp, photorealistic, 3d face, realistic facial structure, bad anatomy,
extra fingers, bad hands, washed-out, faded colors, low contrast, flat colors, muddy colors, dull, overexposed, underexposed, pastel colors,
muted colors, gray palette, pale colors, desaturated, white haze, milky fog, soft focus, hazy, patches, patched fabric, straight hair, black hair, blue eyes, flat chest, glowing eyes, slit pupils, second figure, checkout counter, foreign storefront

P02 — qwen-fox-greet (EXQUISITE · Qwen · R+ · PL530 · P169_HONEY_COGNAC)
Channel: doorstep-bow (live; поклон-знакомство держится один долгий такт, хвост — противовес)
Corridor: B
Combo: D6-03 OC THEME-OFF · Package: ε (GEOMETRY)
THESIS: «ПЕРВОЕ ЗНАКОМСТВО — ПОКЛОН У ПОРОГА, КОТОРЫЙ ДЕРЖИТСЯ ОДИН ДОЛГИЙ ТАКТ:
РУКИ СЛОЖЕНЫ НИЗКО ПЕРЕД ФАРТУКОМ, ГОЛОВА ОПУСКАЕТСЯ, А ЕДИНСТВЕННЫЙ ДЫМЧАТЫЙ ХВОСТ
ПОДНИМАЕТСЯ ПРОТИВОВЕСОМ — ЗНАКОМСТВО НАЧАЛОСЬ РАНЬШЕ СЛОВА».
Гэг-стек (4 фишки OC): 1) розовая подшёрстка ушей ловит первый свет раньше лица;
2) ряд золотой нити на правом запястье не сходит даже в поклоне; 3) хвост-противовес
поднимается ровно на глубину опущенной головы; 4) узел блузы у грудины держит такт.
Spine: PL530 Fox-Bow Greet (OC_T5-23) (OC_T5-23) · K-FF mid_fox_bow · CAM01 · D2·A01 · LEAD the held bow · honey-thread register · closer image-close
Gar: CL-TS-11 (tie-front blouse knotted at the sternum, канон) + CL-SK-02 (flowing satin skirt over slip, канон) · HS: HS43 High Pigtails, Loose, Face-Framing
Stack: CR-W43 + CR-B19 + CR-E23 + CR-D19
POS:
Masterpiece, best quality, absurdres, intricate details, small honest bow held at the doorstep, hands folded low before the apron, eye level, 1girl, solo, fox ears perked small with soft pink inner fur, single smoke-grey tail lifting behind, honey-blonde hair in loose high pigtails, amber fox-patient eyes, warm ivory skin, supple build, medium breasts, the blouse reading her breast shape at the held breath, mid_fox_bow
the sternum knot holding the bow's one long beat honest, the folded hands low and quiet — the held bow is the claim, thread-made
the smoke-grey tail lifting as the head dips, its counterweight honest, even rows of golden thread wound at the right wrist not slipping one loop
Honey cognac palette, honey-blonde warmth over cognac-amber-depth, thread-gold at the wrist rows, satin-sheen faint along the skirt; her colors: the morning wage she earns.
stylized 2D anime face dipped into the bow, anime eyes (amber, fox-patient), small nose, small mouth in greeting-quiet, pink inner-ear fur catching the first light.
NEG:
young girl, immature body, oversized head, loli, shota, signature, watermark, artist name, logo, 1boy, candle, lamp, photorealistic, 3d face, realistic facial structure, bad anatomy,
extra fingers, bad hands, washed-out, faded colors, low contrast, flat colors, muddy colors, dull, overexposed, underexposed, pastel colors,
muted colors, gray palette, pale colors, desaturated, white haze, milky fog, soft focus, hazy, patches, patched fabric, black hair, silver-white hair, red hair, blue eyes, slit pupils, drooping fox ears, nine tails, golden tail, twin tails, tail limp, gift offering, kneeling offer, second figure

P03 — ruuj-tide-curtsey (EXQUISITE · Ruuj · R+ · PL531 · P170_SEAFOAM_GLASS)
Channel: tide-line curtsey (live; кромка воды прижимает подол, жабры-оборки ловят ветер)
Corridor: A
Combo: D6-03 OC THEME-OFF · Package: ε (GEOMETRY)
THESIS: «ЗНАКОМСТВО У КРОМКИ ПРИЛИВА: ОНА ДЕЛАЕТ МЕЛКИЙ ЧЕСТНЫЙ КИВОК-КУРТСИ,
ОДНА ПЯТОЧКА ОТСТУПИЛА НАЗАД, ТЯЖЁЛЫЙ ПОДОЛ ПРИЖАТ ТЕЧЕНИЕМ ПЛОСКО, И ТРИ ПАРЫ
ЖАБР-ПЁРЫШЕК РАСКРЫВАЮТСЯ ШИРЕ ВЕТРА — ПРИВЕТСТВИЕ ВЕСИТ ЧЕСТНО».
Гэг-стек (4 фишки OC): 1) оборки жабр розовеют ярче под ветром — вес виден на них;
2) подол прижат плоско течением — вода держит ткань честно; 3) пятка назад держит
уход-линию, но она остаётся; 4) хвост-плавник низко за спиной правит баланс.
Spine: PL531 Tide-Curtsey (OC_T5-23) (OC_T5-23) · K-FF mid_tide_curtsey · CAM02 · D3·A02 · LEAD the pressed skirt · seafoam-pearl register · closer image-close
Gar: CL-DR-08 (long black dress with one thigh-slit, канон) · HS: HS46 Dripping Aquamarine Fall
Stack: CR-W46 + CR-B12 + CR-L14 + CR-I19
POS:
Masterpiece, best quality, absurdres, intricate details, shallow water curtsey at the tide line, one heel drawn back, three-quarter, 1girl, solo, three blush-pink gill-plumes each side of the head, turquoise hair in dripping falls, pearl-blue eyes, water-pale skin with a pearl cast, young gentle build, soft-set settled breasts, feathered tail-fin low behind, mid_tide_curtsey
the wet clothes of the long skirt pressed flat by the current at the tide's edge, the thigh-slit holding its one honest line — the pressed skirt is the claim, tide-made
the gill-plumes flared wide by the wind and flushing pink with the load, the wet sand keeping the curtsey's print, the tail-fin ruling the balance low
Seafoam glass palette, seafoam-pale over glass-water-clear, pearl-blue at the eyes, black-dress-depth holding the silhouette; her colors: the tide that learns her name.
stylized 2D anime face turned over the pressed skirt, anime eyes (pearl-blue, gill-rose-calm), small nose, small mouth in tide-quiet, the plumes framing the face three a side.
NEG:
young girl, immature body, oversized head, loli, shota, signature, watermark, artist name, logo, 1boy, candle, lamp, photorealistic, 3d face, realistic facial structure, bad anatomy,
extra fingers, bad hands, washed-out, faded colors, low contrast, flat colors, muddy colors, dull, overexposed, underexposed, pastel colors,
muted colors, gray palette, pale colors, desaturated, white haze, milky fog, soft focus, hazy, patches, patched fabric, fish muzzle, gills on neck sides, slit pupils, petite, dry gills, black hair, blonde hair, amber eyes, water flooding, submerged, deep water, second figure

P04 — track-crouch-read (NICHE · human · PG-13 · PL532 · P05_FOREST_MIST)
ARCH: N20 SILHOUETTE_TRUTH · DOOR: D09 STILLNESS
THESIS: «ТРОПА ЧИТАЕТСЯ ПАЛЬЦЕМ: ОНА В ОХОТНИЧЬЕМ ПРИСЕДЕ У СЛОМАННОЙ ВЕТОЧКИ, ВЕС НА
НОСКАХ, ЛУК-ДИАГОНАЛЬ ДЕРЖИТ СПИНУ, А РУНА-ТАТУ НА ЗАПЯСТЬЕ СВЕРЯЕТ КОМПАС — ЛЕС
МОЛЧИТ, ОНА ЕГО ЧИТАЕТ».
Гэг-стек: сломанная веточка свежим срезом к ней; палец касается земли на полтакт;
лямка колчана прижимает лопатку рамкой; вторая ветка такой же слом качается выше —
ловушка-повтор.
Spine: PL532 Track-Crouch Read (venator) (venator) · K-FF mid_track_read · CAM02 · D3·A02 · LEAD the ground-touch · mist-hush register · closer image-close
Race: — (human; тропа решает)
Gar: CL-DR-11 (linen pinafore dress, bib flat-lit) · HS: HS07 Low Loose Ponytail, Face-Framing Strands
Stack: CR-B15 + CR-E33 + CR-M20
POS:
Masterpiece, best quality, absurdres, intricate details, hunting crouch beside a broken twig, one fingertip reading the ground, weight on the toes, 1girl, solo, longbow slung diagonal across her back, ink rune tattoo coiling the wrist, ashen-blonde hair in a low loose ponytail, moss-green eyes, cool pale skin, young supple build, mid_track_read
the longbow's diagonal holding her spine honest in the crouch, the fingertip touching the ground a half-beat — the ground-touch is the claim, trail-made
the quiver strap pressing its frame across the shoulder blade, the rune tattoo coiling to the wrist-bone compass, the second broken twig swinging its repeat above
Forest mist palette, mist-grey-green over pine-shadow-deep, moss-green at the eyes, linen-pale at the pinafore; her colors: the trail that keeps its mouth shut.
stylized 2D anime face level to the twig, anime eyes (moss-green, hush-read), small nose, small mouth in trail-quiet, the ponytail strand grazing the cheek.
NEG:
young girl, immature body, oversized head, loli, shota, signature, watermark, artist name, logo, 1boy, candle, lamp, photorealistic, 3d face, realistic facial structure, bad anatomy,
extra fingers, bad hands, washed-out, faded colors, low contrast, flat colors, muddy colors, dull, overexposed, underexposed, pastel colors,
muted colors, gray palette, pale colors, desaturated, white haze, milky fog, soft focus, hazy, patches, patched fabric, bow drawn, arrow nocked, campfire glow, second figure, animal companion, sword, blood

P05 — elf-fork-scan (NICHE · R02 Elf · R · PL115 · P167_MOSS_GOLD)
ARCH: N28 ANIMAL_GAZE_FRAMING · DOOR: D15 AWARE
THESIS: «РАЗВИЛКА ДЕРЕВА — ЕЁ БАЛКОН: ЭЛЬФИЙСКАЯ СЛЕДОПЫТКА ВЕТВЬЮ ВЫШЕ ГОРИЗОНТА,
ЛАТУННЫЙ МОНОКЛЬ НА ЦЕПОЧКЕ ПОДНЯТ К ГЛАЗУ, ЛУК ГОТОВ, КОЛЬЦА-МЕТКИ НА УШЕ СЧИТАЮТ
ГЕКТАРЫ — КТО-ТО ШЁЛ ЗДЕСЬ ДО НЕЁ».
Гэг-стек: монокль ловит один золотой просвет сквозь крону; кольца-метки на ушной
кромке качают счёт; кора держит холод через ткань юбки; колчан-стрела ловит первые
капли листьев.
Spine: PL115 Sitting in Tree's Fork (base) (base) · K-FF mid_fork_scan · CAM03 · D4·A03 · LEAD the monocle lift · moss-gold register · closer image-close
Race: R02 Elf — long pointed ears swept back, moonlit-pale skin · RF: ear-tip catches the key light first.
Gar: CL-TS-04 (ribbed tank top) + CL-SK-04 (breezy maxi skirt) · HS: HS16 Hair-Sticks + Pinned Twist
Stack: CR-B18 + CR-E14 + CR-C13
POS:
Masterpiece, best quality, absurdres, intricate details, seated in the tree fork one knee up against the trunk, brass monocle lifted to one eye on its chain, 1girl, solo, longbow ready across the lap, quiver at the hip, long pointed ears swept back with ring-marks at the rim, moonlit-pale skin, sage-white hair in hair-sticks pinned twist, amber-lit eyes, lithe young build, mid_fork_scan
the longbow ready across the lap and one knee honest against the trunk — the ready bow is the claim, forest-made
the brass monocle catching one gold slit through the canopy, ring-marks counting hectares at the ear rim, bark's cold kiss arriving through the maxi skirt
Moss gold palette, moss-green-gold over bark-brown-deep, amber slit through the leaves, moonlit-pale at the skin; the estate she patrols alone reads her: moss, amber, moonlit.
stylized 2D anime face raised to the canopy's slit, anime eyes (amber-lit, estate-count), small nose, small mouth in patrol-calm, the ear-tip holding the key light.
NEG:
young girl, immature body, oversized head, loli, shota, signature, watermark, artist name, logo, 1boy, candle, lamp, photorealistic, 3d face, realistic facial structure, bad anatomy,
extra fingers, bad hands, washed-out, faded colors, low contrast, flat colors, muddy colors, dull, overexposed, underexposed, pastel colors,
muted colors, gray palette, pale colors, desaturated, white haze, milky fog, soft focus, hazy, patches, patched fabric, human ears, round ears, monocle taped, glasses both eyes, bow drawn, second figure, falling, broken branch under her

P06 — lure-off-wind (VOLT · human · R+ · PL533 · P103_TELLTALE_ROSE)
Channel: wind-press offer (live; ветер прижимает сарафан, лента-приманка снапает вдоль древка)
Corridor: B
Combo: D3-01 WIND-PRESS SUNDRESS · Package: ε (GEOMETRY)
THESIS: «ПРИМАНКА ЛОВИТСЯ НА ЛЕТУ: ОНА СТОИТ В ГОЛОВНОЙ ВЕТЕР, КОПЬЁ ВЕРТИКАЛЬНО КАК
ШТЫК-ЯКОРЬ, АЛЫЙ ЛЕНТЯЙ-ПРИМАНКА СНАПАЕТ ВСЮ ДЛИНУ ШАФТА, А САРАФАН ЛОВИТ ВЕТЕР
ВКРУГ ТЕЛА — КТО ЕЁ ПРОСЛЕДИТ, ТОТ УЖЕ НА КРЮЧКЕ».
Гэг-стек: лента снапает ровно по шафту — ни один узел не болтается; сарафан прижат
телу куполом ветра; прогиб спины дугой в грудной ветер; петля-стопор на древке
держит место руки.
Spine: PL533 Lure-Off Wind (venator) (venator) · K-FF mid_lure_snap · CAM03 · D4·A03 · LEAD the snapping ribbon · telltale-rose register · closer image-close
Race: — (human; ветер решает)
Gar: CL-DR-04 (cotton sundress, sun-washed pattern) · HS: HS22 Cloud of Natural Curls
Stack: CR-W38 + CR-A18 + CR-L22 + CR-D20
POS:
Masterpiece, best quality, absurdres, intricate details, standing into the headwind, spear held vertical as the anchor stake, three-quarter from below, 1girl, solo, the wind dome pressing the sundress flat around her breast shape, crimson lure ribbon snapping its length along the shaft, ink swallow-tattoo at the collarbone, honey-wheat hair in a cloud of natural curls, rust-rosewood eyes, sun-warmed skin, supple young build, mid_lure_snap
the spear's shaft anchoring her stance while the lure ribbon snaps the whole length honest — the snapped lure is the claim, wind-made
the sundress caught by the wind's dome around her body, the collarbone swallow-tattoo fluttering, the back arching into the gust one honest curve
Telltale rose palette, rose-scarlet over wind-grey-green, telltale-ribbon crimson along the shaft, sun-wash cream at the dress; her colors: the lie that walks on two feet.
stylized 2D anime face turned into the gust, anime eyes (rust-rosewood, lure-calm), small nose, small mouth mid-call, the curls whipping one direction.
NEG:
young girl, immature body, oversized head, loli, shota, signature, watermark, artist name, logo, 1boy, candle, lamp, photorealistic, 3d face, realistic facial structure, bad anatomy,
extra fingers, bad hands, washed-out, faded colors, low contrast, flat colors, muddy colors, dull, overexposed, underexposed, pastel colors,
muted colors, gray palette, pale colors, desaturated, white haze, milky fog, soft focus, hazy, patches, patched fabric, ribbon slack, ribbon tangled, spear thrown, fallen spear, dress blown open, second figure, tent, market stalls

P07 — dryad-vine-trap (NICHE · R14 Dryad · R · PL125 · P172_NETTLE_BRAMBLE)
ARCH: N18 PATTERN_EATS_FIGURE · DOOR: D07 SECRET
THESIS: «ЛОВУШКА ИЗ ЖИВОЙ ЛОЗЫ: СИДЯ НА МХОВОМ КАМНЕ ОНА ТКАНЬЮ СВОИХ ПАЛЬЦЕВ
ДОТЯГИВАЕТ УЗЕЛ СЕТИ, ЛОЗОВЫЕ ПРЯДИ В ВОЛОСАХ ТЯНУТСЯ К СВОИМ, СОК ЛОЗЫ СУШИТ БЕЛЫЙ
СЛЕД НА ТЕМНОЙ ТКАНИ — ЛЕС СТАВИТ КЛЕТКУ СВОИМИ РУКАМИ».
Гэг-стек: узел дотянут на полвитка — палец держит петлю честно; лозовые пряди в
волосах тянутся к сети сами; сок сушит белый росчерк по тёмному саронгу; под сетью
успевает лежать приманка-яблоко.
Spine: PL125 Propped on Mossy Stone (base) (base) · K-FF mid_trap_loosen · CAM02 · D3·A02 · LEAD the half-turn knot · nettle-bramble register · closer image-close
Race: R14 Dryad — vine-strands woven in the hair, bark-soft skin · RF: лоза узнаёт свою.
Gar: CL-SK-08 (sarong wrap, diagonal folds) · HS: HS09 Twin Braids
Stack: CR-B17 + CR-E24 + CR-M14
POS:
Masterpiece, best quality, absurdres, intricate details, propped on one elbow on the mossy stone, knees stacked, fingers half-turning the vine net's knot, 1girl, solo, vine-strands woven into twin braids, bark-soft warm skin, birch-cream hair in twin braids, leaf-green eyes, lithe young build, mid_trap_loosen
the vine net's weave gathered at her working fingers, the half-turned knot honest — the woven net is the claim, forest-made
the vine strands in her braids leaning toward the net of their own accord, sap drying a white chalk-draw across the dark sarong, the bait apple already resting under the weave
Nettle bramble palette, bramble-green-dark over nettle-sting-silver, sap-white draw at the sarong, leaf-green in the gaze; the cage the forest grows wears her colors close: nettle silver, bramble dark.
stylized 2D anime face low over the working knot, anime eyes (leaf-green, knot-patient), small nose, small mouth in weave-quiet, the vine strands framing the temples.
NEG:
young girl, immature body, oversized head, loli, shota, signature, watermark, artist name, logo, 1boy, candle, lamp, photorealistic, 3d face, realistic facial structure, bad anatomy,
extra fingers, bad hands, washed-out, faded colors, low contrast, flat colors, muddy colors, dull, overexposed, underexposed, pastel colors,
muted colors, gray palette, pale colors, desaturated, white haze, milky fog, soft focus, hazy, patches, patched fabric, net caught on her, trapped in net, thorn scratches, blood drops, second figure, bird in net, fox in net

P08 — blade-fan-release (VOLT · human · R · PL534 · P112_POCKET_THEFT_GOLD)
Channel: reverse-grip fan (live; веер ножей раскрывается с бедра, запястье в следствии)
Combo: D5-03 OBJECT-SUBJECT FIRST · Package: ε (GEOMETRY)
THESIS: «ВЕЕР НОЖЕЙ РАСКРЫТ С БЕДРА: ОДИН УЖЕ В ПОЛЁТЕ, ЗАПЯСТЬЕ ДОЕЗЖАЕТ
СЛЕДСТВИЕ, ВТОРОЙ ДЕРЖИТСЯ ОБРАТНЫМ ХВАТОМ У ЛИНИИ БЕДРА — БЕДРО ПОДНЯЛО КРАЙ
ПЛИССЕ, И ВЕС НАКЛОНЯЕТ ВЕСЬ ВЕЕР».
Гэг-стек: брошенный нож поймал один солнечный просвет; второй нож обратным хватом
от бедра; плиссированная юбка поднята краем бедра — складки веером; на коже бедра
старая тату-метка точности.
Spine: PL534 Blade-Fan Release (venator) (venator) · K-FF mid_blade_fan · CAM03 · D4·A03 · LEAD the follow-through · theft-gold register · closer image-close
Race: — (human; веер решает)
Gar: CL-TS-03 (knotted slim tee) + CL-SK-05 (plaid pleated skirt) · HS: HS04 Wolf Cut, Choppy
Stack: CR-B21 + CR-U20 + CR-I14
POS:
Masterpiece, best quality, absurdres, intricate details, mid-release of a thrown knife, wrist held in the follow-through, second blade reversed at the hip, three-quarter low, 1girl, solo, throwing knives fanned at the belt, accuracy-marks tattoo at the outer thigh, storm-black hair in a choppy wolf cut, flint-grey eyes, cool ivory skin, athletic young build, mid_blade_fan
the thrown knife's follow-through honest in the wrist, the second blade reversed at the hip line — the follow-through is the claim, steel-made
the plaid pleats fanned hard by the raised thigh's edge, accuracy-marks tattoo reading its old tally at the thigh, sand-dust clinging to the damp calves of the range
Pocket theft gold palette, theft-gold-warm over storm-slate-dark, flint-grey at the eyes, blade-steel-glint along the fan; her colors: the tally nobody counts.
stylized 2D anime face turned after the flight, anime eyes (flint-grey, tally-cold), small nose, small mouth in release-flat, the wolf cut's tail caught mid-whip.
NEG:
young girl, immature body, oversized head, loli, shota, signature, watermark, artist name, logo, 1boy, candle, lamp, photorealistic, 3d face, realistic facial structure, bad anatomy,
extra fingers, bad hands, washed-out, faded colors, low contrast, flat colors, muddy colors, dull, overexposed, underexposed, pastel colors,
muted colors, gray palette, pale colors, desaturated, white haze, milky fog, soft focus, hazy, patches, patched fabric, knife in body, blood, wounds, slash marks, blade at throat, second figure, target board, crowd

P09 — maneki-gate-lure (NICHE · R52 Fortune-cat-kin · PG-13 · PL124 · P89_THRESHOLD_GOLD)
ARCH: N02 SCALE_EPIC · DOOR: D06 OFFERING
THESIS: «ПРИМАНКА У ВОРОТ: МАНИКИ-КАЛИКО СИДИТ НА ШИРОКОЙ ПЕРИЛЕ ГЛАВНЫХ ВОРОТ,
ПРОПУСКАЯ ДАЛЬШЕ СЕБЯ ТОЛЬКО ТЕХ, КТО ПОГЛАДИЛ КОЛОКОЛЬЧИК НА ЛОДЫЖКЕ, ПАТЧИ В
ВОЛОСАХ ЛОВЯТ ЗОЛОТО ПОРОГА — ВОРОТА РЕШАЮТ, КОГО ПУСКАТЬ».
Гэг-стек: колокольчик-амулет на лодыжке поймал один звон; calico-патчи (рыжий и
чёрный) в волосах ловят золото порога; тюлевые слои юбки качаются от чужого ветра;
след лапки на периле — официальная печать.
Spine: PL124 Perched on Wide Railing (base) (base) · K-FF mid_paw_bell · CAM02 · D3·A02 · LEAD the bell note · threshold-gold register · closer image-close
Race: R52 Fortune-cat-kin — calico patches in the hair: one ginger, one black; round soft ears · RF: колокольчик решает вход.
Gar: CL-TS-05 (knit tube top, bare shoulders) + CL-SK-07 (layered tulle skirt) · HS: HS14 Double Buns (Space Buns)
Stack: CR-B13 + CR-L23 + CR-D22
POS:
Masterpiece, best quality, absurdres, intricate details, perched on the wide gate railing, feet hooked on the lower rung, torso leaned to one point, 1girl, solo, calico patches in the hair one ginger one black, round soft ears, golden bell-charm anklet, cream-gold hair in double buns, coin-yellow eyes, warm honey skin, petite young build, mid_paw_bell
the golden bell-charm at the anklet caught mid-note at the gate's threshold — the bell note is the claim, gold-made
the tulle layers swinging on somebody else's wind, calico patches catching the gate's gold, one paw-print stamped honest on the rail's stone
Threshold gold palette, threshold-gold-warm over gate-stone-grey, coin-yellow at the eyes, tulle-cream layers at the skirt; her colors: the toll paid in kindness.
stylized 2D anime face tilted from the perch, anime eyes (coin-yellow, toll-warm), small nose, small open smile, the buns holding one escaping ginger strand.
NEG:
young girl, immature body, oversized head, loli, shota, signature, watermark, artist name, logo, 1boy, candle, lamp, photorealistic, 3d face, realistic facial structure, bad anatomy,
extra fingers, bad hands, washed-out, faded colors, low contrast, flat colors, muddy colors, dull, overexposed, underexposed, pastel colors,
muted colors, gray palette, pale colors, desaturated, white haze, milky fog, soft focus, hazy, patches, patched fabric, cat muzzle, feral, tail visible, paw hands, crowd at gate, second figure, falling, lantern row, paper charms

P10 — mid-run-glance (VOLT · human · R+ · PL97 · P143_COIL_VERDIGRIS)
Channel: mid-run claim (live; бег-взгляд через плечо, кнут тянет шов — тяга по ткани)
Corridor: B
Combo: D5-03 OBJECT-SUBJECT FIRST · Package: ε (GEOMETRY)
THESIS: «СЛЕД НАЙДЕН НА ХОДУ: ОНА БЕЖИТ СКЛОНЕ́ННОЙ ТАКТОВОЙ ЛИНИЕЙ И УЖЕ ПОВЕРНУЛА
ЛИЦО ЧЕРЕЗ ПЛЕЧО, КНУТ НА ПОЯСЕ ТРЁТ ШОВ ДО НИТЕЙ, ПОСЛЕДНЯЯ ПУГОВИЦА РУБАШКИ ДЕРЖИТ
ВСЁ АРГУМЕНТ — ПОГОНЯ НАЧАЛАСЬ РАНЬШЕ РЕШЕНИЯ».
Гэг-стек: лицо уже в профиль через плечо, корпус ещё бежит вперёд; кнутовый шов
распушён до нитей; последняя пуговица несёт весь спор рубашки; пыль-след позади
ложится ровной линией.
Spine: PL97 Mid-Run Glance (dynamic_v2) (dynamic_v2) · K-FF mid_run_glance · CAM03 · D4·A03 · LEAD the shoulder glance · coil-verdigris register · closer image-close
Race: — (human; погоня решает)
Gar: CL-TS-09 (open linen shirt over athletic crop top) + CL-BT-01 (cutoff denim shorts) · HS: HS37 Bubble Ponytail (Sectioned)
Stack: CR-W54 + CR-B22 + CR-E12 + CR-D24
POS:
Masterpiece, best quality, absurdres, intricate details, mid-run torso turned enough to glance over the shoulder, one arm still pumping, three-quarter from below, 1girl, solo, leather whip coiled at the belt fraying the seam, rust-copper hair in a sectioned bubble ponytail, verdigris-teal eyes, sun-brown skin, athletic young build, the open linen reading her breast shape at every stride, mid_run_glance
the whip's work fraying the shoulder seam to honest threads while she runs — the frayed seam is the claim, hunt-made
the last button of the open linen shirt holding the whole argument, dust line laying straight behind the cutoffs, the bubble ponytail swinging its sections late
Coil verdigris palette, verdigris-teal-deep over rust-copper-warm, whip-leather-brown at the belt, dust-gold faint at the trail; her colors: the chase that started without her.
stylized 2D anime face turned through the glance, anime eyes (verdigris-teal, chase-lit), small nose, small mouth mid-breath, the ponytail sections carrying their lag.
NEG:
young girl, immature body, oversized head, loli, shota, signature, watermark, artist name, logo, 1boy, candle, lamp, photorealistic, 3d face, realistic facial structure, bad anatomy,
extra fingers, bad hands, washed-out, faded colors, low contrast, flat colors, muddy colors, dull, overexposed, underexposed, pastel colors,
muted colors, gray palette, pale colors, desaturated, white haze, milky fog, soft focus, hazy, patches, patched fabric, whip raised, whip strike, person chased, second figure, blood, weapon drawn, standing still

P11 — ridge-watch-halberd (NICHE · R07 Dragon-kin · R · PL123 · P66_DUSK_VERMILION)
ARCH: N10 TIME_FREEZE_TABLEAU · DOOR: D09 STILLNESS (M04 — остановленный мир)
THESIS: «ГРЕБЕНЬ КРЫШ — ЕЁ ВЫШКА: ДРАКОНЬЯ СТОРОЖ ГОРИЗОНТАЛЬНО ОПЁРЛАСЬ НА
АЛЕБАРДУ КАК НА ГНОМОН, ГОРОД ВНИЗУ СПИТ, ЧЕШУЯ-ГРЕБЕНЬ ЛОВИТ ПОСЛЕДНЮЮ КРАСКУ
СУМЕРЕК — МИР ОСТАНОВЛЕН, ДОЗОР НЕТ».
Гэг-стек: алебарда — гномон: её тень ложится стрелкой на спящий город; чешуйчатый
гребень ловит последнюю вермильон-краску; хвост обвивает печную трубу якорем; урод
дым из чужой печки рисует её направление.
Spine: PL123 Reclined Against Roof Tiles (base) (base) · K-FF mid_ridge_watch · CAM03 · D4·A03 · LEAD the gnomon shadow · dusk-vermilion register · closer image-close
Race: R07 Dragon-kin — horns ridged swept-back, scale-crest along the spine, slate-teal skin · RF: гребень ловит закат.
Gar: CL-OU-01 (cropped denim jacket) + CL-SK-06 (pencil skirt with back slit) · HS: HS10 Single Thick Braid, Over Shoulder
Stack: CR-B12 + CR-E37 + CR-D46
POS:
Masterpiece, best quality, absurdres, intricate details, reclined against roof tiles one knee up, the halberd's butt planted as her leaning post, its shadow an arrow over the sleeping roofs, 1girl, solo, halberd braced as the gnomon of her watch, ridged swept-back horns, scale-crest catching the dusk line, slate-teal skin, slate-teal skin with scale-crest along the spine, ember-copper hair in a thick over-shoulder braid, kiln-orange eyes, tall lithe build, mid_ridge_watch
the halberd's butt as her leaning post holding the whole recline — the gnomon is the claim, dusk-made
the scale-crest reading its dusk-vermilion edge, the tail coiling the chimney as her anchor, sleeve rolled working-high over the elbow of the grip
Dusk vermilion palette, dusk-vermilion over slate-teal-dark, kiln-orange at the eyes, roof-tile-brown beneath; her colors: the watch nobody signed.
stylized 2D anime face level over the sleeping town, anime eyes (kiln-orange, watch-still), small nose, small mouth in dusk-quiet, the horns ruling the silhouette.
NEG:
young girl, immature body, oversized head, loli, shota, signature, watermark, artist name, logo, 1boy, candle, lamp, photorealistic, 3d face, realistic facial structure, bad anatomy,
extra fingers, bad hands, washed-out, faded colors, low contrast, flat colors, muddy colors, dull, overexposed, underexposed, pastel colors,
muted colors, gray palette, pale colors, desaturated, white haze, milky fog, soft focus, hazy, patches, patched fabric, halberd swinging, weapon raised, wings, dragon muzzle, feral, second figure, falling, city lights on, neon

P12 — ghost-chain-drop (VOLT · R11 Bat-kin · R+ · PL106 · P25_VOID_ABYSS)
Channel: drop-claim (live; спуск с подоконника колокольни по призрачной цепи)
Corridor: B
Combo: D5-04 SHADOW WORKER · Package: κ (CONTACT)
THESIS: «СПУСК БЕЗ ЛЕСТНИЦЫ: ОНА БРОСАЕТСЯ С ПОДОКОННИКА КОЛОКОЛЬНИ, ПРИЗРАЧНАЯ
ЦЕПЬ ЗВЕНАМИ ЛОВИТ ВЕС СТАРТ-РЫВКА, ПЛАЩ СОСКАЛЬЗЫВАЕТ С ОДНОГО ПЛЕЧА В ПОЛЁТЕ,
ПЫЛЬ КОЛОКОЛЬНИ СЕДЕЕТ НА ПЛЕЧАХ — НОЧЬ НАЧИНАЕТСЯ С УСКОРЕНИЯ».
Гэг-стек: цепь провисает ровно на вес рывка — звенья честные; перепончатые крылья
за спиной полу-раскрыты тормозом; плащ уходит с плеча против движения; пыль оседает
серым следом на плечах.
Spine: PL106 Mid-Drop from Windowsill (dynamic_v2) (dynamic_v2) · K-FF mid_chain_throw · CAM03 · D4·A03 · LEAD the chain catch · void-abyss register · closer image-close
Race: R11 Bat-kin — ribbed tall ears, membrane wing-folds at the arms, dusk-violet skin · RF: уши читают пустоту.
Gar: CL-TS-06 (backless halter top) + CL-SK-02 (flowing satin skirt) + night cloak · HS: HS36 Side Shave + Long Sweep-Over
Stack: CR-W55 + CR-B57 + CR-E54 + CR-D54
POS:
Masterpiece, best quality, absurdres, intricate details, mid-drop from the belfry windowsill, body angled to the fall, the ghost chain catching the launch weight link by link, three-quarter from below, 1girl, solo, the halter holding her breast shape into the fall, ghost chain's cold links leading the descent, ribbed tall ears, membrane wing-folds half-spread as brakes, dusk-violet skin, black-violet hair in a side shave with long sweep-over, void-lilac eyes, slender young build, mid_chain_throw
the ghost chain's cold links catching her launch weight honest — the caught chain is the claim, spirit-made
the cloak sliding off one shoulder mid-step of the fall, belfry dust settling grey on the shoulders, wing-folds braking the spin one beat
Void abyss palette, abyss-black-deep over void-violet-faint, cold-link-pale along the chain, dusk-violet at the skin; the drop nobody hears paints her: abyss and violet.
stylized 2D anime face already into the fall, anime eyes (void-lilac, drop-quiet), small nose, small mouth in descent-flat, the sweep-over strand riding the fall's wind.
NEG:
young girl, immature body, oversized head, loli, shota, signature, watermark, artist name, logo, 1boy, candle, lamp, photorealistic, 3d face, realistic facial structure, bad anatomy,
extra fingers, bad hands, washed-out, faded colors, low contrast, flat colors, muddy colors, dull, overexposed, underexposed, pastel colors,
muted colors, gray palette, pale colors, desaturated, white haze, milky fog, soft focus, hazy, patches, patched fabric, bat muzzle, feral, full wingspan, horror register, wires in flesh, gore, second figure, solid rope, iron chain rust, falling body limp

P13 — harpoon-brace-pier (VOLT · R23 Shark-kin · R · PL535 · P160_BONE_WHALF_BRINE)
Channel: harpoon-set (live; гарпун упёрт в тазовую кость, линь дважды обвит вокруг предплечья)
Combo: D3-04 SEATED COMPRESS · Package: κ (CONTACT)
THESIS: «ПИРС ДЕРЖИТ ЕЁ КАК СВОЮ: АКУЛЬЯ ГАРПУНЩИЦА УПЁРЛА ГАРПУН В ТАЗОВУЮ КОСТЬ,
ЗАДНЯЯ СТУПНЯ ЗАКРЮЧЕНА ЗА КРАЙ ПИРСА, ЛИНЬ ДВАЖДЫ ОБВИТ ВОКРУГ ПРЕДПЛЕЧЬЯ — ВОДА
УЖЕ ЗНАЕТ, ЧТО ОНА БРОСИТ».
Гэг-стек: линь обвит дважды — второй виток слабее, вода тянет; спинной плавник
ловит соль ветра; чешуя на бедре ловит один блик; край пирса держит ступню крючком.
Spine: PL535 Harpoon-Brace (venator) (venator) · K-FF mid_harpoon_set · CAM03 · D4·A03 · LEAD the coiled line · bone-wharf register · closer image-close
Race: R23 Shark-kin — dorsal fin at the spine, scale patch at the hip, grey-blue skin, fin-tail low · RF: плавник читает соль.
Gar: CL-SK-08 (sarong wrap low on the hips) · HS: HS18 Wet Slicked-Back
Stack: CR-B68 + CR-E35 + CR-D61
POS:
Masterpiece, best quality, absurdres, intricate details, harpoon braced against the hip bone, rear foot hooked over the pier's edge, three-quarter low, 1girl, solo, harpoon line coiled twice around the forearm, dorsal fin at the spine catching salt wind, scale patch at the hip curve, grey-blue skin, drift-steel hair slicked back wet, chum-white eyes, athletic young build, mid_harpoon_set
the harpoon braced at the hip bone while the line coils twice around the forearm — the coiled line, the claim itself, tide-made
the sarong's wet hem pulling its heavy straight line at the thighs, the tail-fin cutting its first wake below, scale patch catching one brine glint
Bone wharf brine palette, wharf-bone-pale over brine-black-green, chum-white at the eyes, steel-glint along the harpoon; her colors: the throw before the throw.
stylized 2D anime face set over the braced line, anime eyes (chum-white, throw-calm), small nose, small mouth in brace-flat, the dorsal fin ruling the silhouette.
NEG:
young girl, immature body, oversized head, loli, shota, signature, watermark, artist name, logo, 1boy, candle, lamp, photorealistic, 3d face, realistic facial structure, bad anatomy,
extra fingers, bad hands, washed-out, faded colors, low contrast, flat colors, muddy colors, dull, overexposed, underexposed, pastel colors,
muted colors, gray palette, pale colors, desaturated, white haze, milky fog, soft focus, hazy, patches, patched fabric, shark muzzle, feral, full shark tail, teeth bared, gills on neck, harpoon thrown, harpoon in water, blood, fish catch, second figure

P14 — gargoyle-beam-watch (NICHE · R18 Gargoyle-kin · R · PL56 · P156_FAULT_CLIFF_IRON)
ARCH: N23 MECHANICAL_BALLET · DOOR: D09 STILLNESS
THESIS: «БАЛКА — ЕЁ СТУЛ: КАМЕННАЯ СТОРОЖ СИДИТ АСТРИД НА БАЛКЕ СОБОРНОГО ЛЕТА,
ПОДОЛ УЗЛОМ НА КОЛЕНЕ, КАМЕННЫЕ ШВЫ ЛОВЯТ РЖАВЦУ, А ПАЛЬЦЫ ИЗ КАРБОНА СЧИТАЮТ
ВЕСЬ ГОРОД ПО ОДНОЙ ЛАДОНИ».
Гэг-стек: швы камня читаются трещинами-меловыми, но кожа тёплая; рукав стёрт до
войлочной бледности о край балки; сиденье расплылось честно на балке; голубиный
пух осел на плечах — город доверяет.
Spine: PL56 Astride Chair/Ledge/Beam (erotic_presentation) (erotic_presentation) · K-FF mid_gargoyle_fold · CAM03 · D4·A03 · LEAD the beam sit · fault-iron register · closer image-close
Race: R18 Gargoyle-kin — small stone horns rough-textured, kiln-clay skin with seam-cracks faint, ash-grey-bone palette · RF: швы ловят погоду.
Gar: CL-DR-02 (ribbed knit turtleneck dress) · HS: HS20 Undercut Buzz + Long Top
Stack: CR-B14 + CR-E52 + CR-C17
POS:
Masterpiece, best quality, absurdres, intricate details, astride the wide ledge beam, knees wide, weight sinking forward onto the surface, three-quarter from below, 1girl, solo, small stone horns rough-textured, kiln-clay skin with faint seam-cracks at the joints, ash-bone-grey skin, slate-mauve hair in an undercut buzz with long top, mortar-grey eyes, sturdy young build, mid_gargoyle_fold
the skirt hem knotted up under the working knee while she holds the beam astride — the knot under the knee is the claim, stone-made
the seam-cracks catching their rust line at the joints, the sleeve's nap rubbed pale where her forearm rides the beam's edge, the seat's line spreading honest on the beam
Fault cliff iron palette, fault-iron-grey over cliff-rust-warm, mortar-grey at the eyes, knit-ash at the dress; her colors: the ledge that never moves.
stylized 2D anime face low over the town square, anime eyes (mortar-grey, ledge-still), small nose, small mouth in stone-calm, the horns catching one weather line.
NEG:
young girl, immature body, oversized head, loli, shota, signature, watermark, artist name, logo, 1boy, candle, lamp, photorealistic, 3d face, realistic facial structure, bad anatomy,
extra fingers, bad hands, washed-out, faded colors, low contrast, flat colors, muddy colors, dull, overexposed, underexposed, pastel colors,
muted colors, gray palette, pale colors, desaturated, white haze, milky fog, soft focus, hazy, patches, patched fabric, stone face, statue, cracked skin deep, moss on skin, wings, horror register, second figure, falling from beam

P15 — ember-stride-stalk (VOLT · R22 Flame-salamander · R+ · PL536 · P135_EMBER_STUDY)
Channel: ember-stole cover (live; шаль-газа крестом держит грудь, гребень-зола греет шерсть)
Corridor: A
Combo: D2-02 STRAP CATCH · Package: ε (GEOMETRY)
THESIS: «ШАГ-ЗОЛА: ОНА КРАДЁТСЯ НОСКАМИ ПО КРАЮ КОТЛОВАННОЙ ТЕНИ, ЛАДОНЬ ВЕДЁТ
ГРЕБЕНЬ-ЗОЛУ ВДОЛЬ ПОЗВОНОЧНИКА, КРЕСТ-НАКРЕСТ ШАЛЬ-ГАЗА ДЕРЖИТ ГРУДЬ ЧЕСТНО, А
ТЕПЛО ГРЕБНЯ ОСЛАБЛЯЕТ ШЕРСТЬ ПАЛАНТИНА — ОГОНЬ НОСИТ ОНА САМА».
Гэг-стек: гребень-зола читается угольной линией по хребту — не пламя, зола; палец
уже тянется к клинку раньше лица; мох у следа не загорается — только тёплый; шаль
крестом: перекрестье ровно у грудины.
Spine: PL536 Ember-Stride Stalk (venator) (venator) · K-FF mid_ember_strap · CAM03 · D4·A03 · LEAD the ember line · ember-study register · closer image-close
Race: R22 Flame-salamander-kin — crest of low ember along the spine's line, coal-black skin with warm mottling, ember-amber freckles · RF: зола, не пламя.
Gar: CL-TS-14 (bandage wrap top) + CL-SK-04 (breezy maxi skirt) + ember-gauze stole crossed · HS: HS26 Glossy Doll-Curls, Long
Stack: CR-W63 + CR-B73 + CR-L15 + CR-D49
POS:
Masterpiece, best quality, absurdres, intricate details, low stalking stride on the balls of the feet, one palm trailing the ember line that runs her spine crest, three-quarter from below, 1girl, solo, forearms crossed over the gauze stole at her chest, ember-gauze stole crossed and held over the chest, crest of low ember along the spine's line, coal-black skin with warm mottling, ember-amber freckles, cinder-red hair in long glossy doll curls, forge-ember eyes, supple young build, mid_ember_strap
the gauze stole crossed and held over her chest honest while the stalk rides low — the crossed stole is the claim, ember-made
the crest's low ember drawing its charcoal line up the spine, one finger already twitching toward the blade before the face allows, wool's fall loosening in the crest's warmth
Ember study palette, ember-study-amber over charcoal-black-deep, forge-ember at the freckles, gauze-warm-cream at the stole; her colors: the heat that walks ahead.
stylized 2D anime face level to the stalk line, anime eyes (forge-ember, stalk-warm), small nose, small mouth in ember-quiet, the doll curls catching one amber edge.
NEG:
young girl, immature body, oversized head, loli, shota, signature, watermark, artist name, logo, 1boy, candle, lamp, photorealistic, 3d face, realistic facial structure, bad anatomy,
extra fingers, bad hands, washed-out, faded colors, low contrast, flat colors, muddy colors, dull, overexposed, underexposed, pastel colors,
muted colors, gray palette, pale colors, desaturated, white haze, milky fog, soft focus, hazy, patches, patched fabric, open flame, fire burst, burning clothes, sparks, flame tail, lizard muzzle, feral, gauze torn, second figure, burning forest

P16 — wake-harpoon-lagoon (VOLT · R13 Merfolk-adapt · R · PL537 · P83_MIDNIGHT_LAGOON)
Channel: wake-line roll (live; вейк раскрывается веером за толчок бёдер)
Combo: D5-05 GLASS WITNESS · Package: ε (GEOMETRY)
THESIS: «ЛАГУНА НОЧЬЮ — СТЕКЛО: МЕРФОЛК-ГАРПУНЩИЦА ПРОКАТЫВАЕТ БЕДРО ЧЕРЕЗ МЕЛКУЮ
ВОДУ, ГАРПУН НИЗКО ВДОЛЬ БЕДРА, ВЕЙК РАСКРЫВАЕТСЯ ВЕЕРОМ ПОЗАДИ ТОЛЧКА, ЧЕШУЯ НА
ГОЛЕНИ ЛОВИТ ОДИН ЛУННЫЙ ЛОСК — ЛУНУ НИКТО НЕ ЗВАЛ».
Гэг-стек: вейк веером — три чистых гребня; чешуя shin-and-hip ловит лунный лоск
одной полосой; вода держит её отражение на полтакта позже; гарпунная линия ведёт в
глубину-обещание.
Spine: PL537 Wake-Harpoon Roll (venator) (venator) · K-FF mid_wake_roll · CAM03 · D4·A03 · LEAD the fan wake · midnight-lagoon register · closer image-close
Race: R13 Merfolk-adapt — scales shin-and-hip, fin-fringe at the forearms, sea-glass skin · RF: лоск читает луну.
Gar: CL-DR-01 (silk slip dress, bias-cut) · HS: HS18 Wet Slicked-Back
Stack: CR-B71 + CR-E59 + CR-F17
POS:
Masterpiece, best quality, absurdres, intricate details, hip-roll through shallow midnight water, harpoon run low along the thigh, the wake opening in a fan behind the push, three-quarter low, 1girl, solo, scales shin-and-hip catching one moon glint, fin-fringe at the forearms, sea-glass skin, lagoon-blue-green hair slicked back wet, abalone-nacre eyes, supple young build, mid_wake_roll
the harpoon run low along the thigh while the wake opens its fan honest — the fan wake, claim outright, tide-made
the silk slip dress dipped where the water pulled it, the waist's sway given away by the water's own hand, scales reading their moon glint one band wide
Midnight lagoon palette, lagoon-blue-black over moon-green-faint, abalone-dark at the eyes, sea-glass-pale at the skin; the lagoon rides her throw: blue-black, moon-green, one glint.
stylized 2D anime face level over the wake line, anime eyes (abalone-nacre, tide-patient), small nose, small mouth in lagoon-quiet, the fin-fringe holding one droplet.
NEG:
young girl, immature body, oversized head, loli, shota, signature, watermark, artist name, logo, 1boy, candle, lamp, photorealistic, 3d face, realistic facial structure, bad anatomy,
extra fingers, bad hands, washed-out, faded colors, low contrast, flat colors, muddy colors, dull, overexposed, underexposed, pastel colors,
muted colors, gray palette, pale colors, desaturated, white haze, milky fog, soft focus, hazy, patches, patched fabric, fish tail full, mermaid tail, gills, fish muzzle, feral, harpoon thrown, harpoon in fish, blood, deep diving, second figure

P17 — riposte-lantern-line (VOLT · human · R+ · PL150 · P110_RIPOSTE_SILVER)
Channel: wrap-claim line (live; выпад-риposta, wrap-узел держит грудь честно)
Corridor: A
Combo: D5-04 SHADOW WORKER · Package: ε (GEOMETRY)
THESIS: «РЕПОСТА УЗНАЁТСЯ ДО УДАРА: ОНА В ЭН-ГАРДЕ У КРАЯ МОКРОЙ МОСТОВОЙ, КЛИНОК
ВЕДЁТ ЛИНИЮ, ЗАДНЯЯ РУКА В АРКЕ, ВЕС ЧЕРЕЗ БЕДРО ДОЕЗЖАЕТ НА ТАКТ ПОЗЖЕ РЕШЕНИЯ,
ШНУРОВКА ПЛАТЬЯ ОСЛАБЛА ОТ НАКЛОНА — СТАЛЬ ЧИТАЕТ СВЕТ МОКРОЙ МОСТОВОЙ».
Гэг-стек: клинок ловит линию чужого фонаря — свет приписан соседу, не прибору;
шнуровка спереди ослабла от выпада честно; вес через бедро на такт позже; след
выпада на гравии — короткая борозда.
Spine: PL150 En-Garde Foil Line (performance_mirror) (performance_mirror) · K-FF mid_riposte_hold · CAM02 · D3·A02 · LEAD the riposte line · riposte-silver register · closer image-close
Race: — (human; репоста решает)
Gar: CL-DR-07 (jersey wrap dress, deep V, wrap-knot) + fencing gloves · HS: HS06 Deep Side Wave, Over One Shoulder
Stack: CR-W45 + CR-B59 + CR-E55 + CR-D45
POS:
Masterpiece, best quality, absurdres, intricate details, en-garde line with the rapier extended, rear arm raised in arch behind, knees bent, chest forward of the line, 1girl, solo, the deep V reading her breast shape through the lunge, rapier's silver line leading the frame, dueling scar splitting the left brow, garnet-black hair in a deep side wave over one shoulder, storm-steel eyes, cool porcelain skin, womanly build with soft settled breasts, mid_riposte_hold
the wrap dress's knot holding her chest honest through the lunge — the held knot is the claim, steel-made
the front lacing gone slack from the lean, the weight transfer arriving one beat late through the hip, the gravel keeping the lunge's short furrow
Riposte silver palette, riposte-steel-silver over garnet-black-deep, blade-line-pale across the frame, porcelain-cool at the skin; the answer nobody read wears her: steel, garnet, porcelain.
stylized 2D anime face over the blade's line, anime eyes (storm-steel, duelist-calm), small nose, small mouth in lunge-flat, the scar splitting the brow honest.
NEG:
young girl, immature body, oversized head, loli, shota, signature, watermark, artist name, logo, 1boy, candle, lamp, photorealistic, 3d face, realistic facial structure, bad anatomy,
extra fingers, bad hands, washed-out, faded colors, low contrast, flat colors, muddy colors, dull, overexposed, underexposed, pastel colors,
muted colors, gray palette, pale colors, desaturated, white haze, milky fog, soft focus, hazy, patches, patched fabric, opponent figure, second person, fencing mask, blood, wound, scar fresh, lantern glowing, lamp lit, streetlamp pole glowing, dress torn open

P18 — cloak-pivot-marsh (VOLT · R51 Crane-kin · R · PL145 · P56_AURORA_BOREALIS_NIGHT)
Channel: cloak-pivot line (live; плащ-пивот раскрывает подкладку на повороте)
Combo: D2-07 MID-STEP THRESHOLD · Package: ε (GEOMETRY)
THESIS: «ПОВОРОТ НА ТРОПЕ БОЛОТА: КРАН-КИН РАЗВОРАЧИВАЕТСЯ ЧЕРЕЗ ШАГ, КРЫЛЬЯ-ШАЛЬ
ЗАМЁРТВО СЛОЖЕНЫ НА ПРЕДПЛЕЧЬЯХ, ПОДКЛАДКА ПЛАЩА ВСПЫХИВАЕТ НОЧНОЙ АВРОРОЙ
НА ПОЛ-ОБОРОТА, ПЕРЬЕВЫЕ ДОРОЖКИ НА ПРЕДПЛЕЧЬЯХ СЧИТАЮТ ШАГИ — БОЛОТО ЗНАЕТ ЕЁ ПО
ТРОПЕ».
Гэг-стек: подкладка ловит пол-оборота авророй — ткань несёт север; перьевые дорожки
на предплечьях печатают параллельные линии; утренний туман поднимает ворот честно;
след шага в сфагнуме держит отпечаток.
Spine: PL145 Mid-Pivot in Long Coat (performance_mirror) (performance_mirror) · K-FF mid_cloak_pivot · CAM03 · D4·A03 · LEAD the lining flash · aurora-night register · closer image-close
Race: R51 Crane-kin — wings folded at rest like a wrapped shawl over the forearms, feather-track lines along the arms, marsh-white skin · RF: крылья — шаль, не парус.
Gar: CL-OU-01 (cropped denim jacket) + CL-SK-04 (breezy maxi skirt) + long hooded cloak · HS: HS05 Long Classic Layers, Center Part
Stack: CR-B56 + CR-E47 + CR-D53
POS:
Masterpiece, best quality, absurdres, intricate details, mid-pivot in the long cloak, collar up, hem flared by the turn, three-quarter low, 1girl, solo, wings folded like a wrapped shawl over the forearms, feather-track lines printing fine parallels along the arms, marsh-white skin, snow-silver hair in long classic layers center part, aurora-grey eyes, tall lithe build, mid_cloak_pivot
the cloak's lining flashing its aurora band at the half-turn honest — the lining flash is the claim, marsh-made
the back seam twisted open by the half-turn one line of spine bare, morning marsh mist lifting the collar as it climbs, the sphagnum keeping the step's print
Aurora borealis night palette, aurora-green-violet over marsh-black-deep, snow-silver at the hair line, feather-white at the forearms; her colors: the north she came from.
stylized 2D anime face turned through the pivot, anime eyes (aurora-grey, marsh-still), small nose, small mouth in pivot-quiet, the folded shawl-wings ruling the arms.
NEG:
young girl, immature body, oversized head, loli, shota, signature, watermark, artist name, logo, 1boy, candle, lamp, photorealistic, 3d face, realistic facial structure, bad anatomy,
extra fingers, bad hands, washed-out, faded colors, low contrast, flat colors, muddy colors, dull, overexposed, underexposed, pastel colors,
muted colors, gray palette, pale colors, desaturated, white haze, milky fog, soft focus, hazy, patches, patched fabric, crane muzzle, beak, feral, wings spread, flight, feathers falling, swamp water deep, sinking, second figure

P19 — arsenal-fit-hug (EXQUISITE · human · R+ · PL538 · P54_ART_DECO_PLATINUM)
Channel: plate-hug fit (live; трофейный нагрудник обнимает грудь в обеих руках — прикрытие объектом)
Corridor: A
Combo: D5-03 OBJECT-SUBJECT FIRST · Package: κ (CONTACT)
THESIS: «ПРИМЕРКА ТРОФЕЯ: ОНА ОБНИМАЕТ НАГРУДНИК ПОБЕЖДЁННОЙ ОХОТНИЦЫ ОБОИМИ
РУКАМИ, ПОДБОРОДОК ЧУТЬ ЗА КРАЕМ, РЕМЕНЬ БРОНИ ПЕЧАТАЕТ СВОЮ ПОЛОСУ СКВОЗЬ ШЕРСТЬ,
ЗЕРКАЛО АРСЕНАЛА ДЕРЖИТ ПОЛ-ЛИЦА — ОНА ПРИМЕРЯЕТ ВЕС, А НЕ РАЗМЕР».
Гэг-стек: нагрудник охвачен крест-накрест — пальцы честно переплетены; ремень брони
печатает полосу сквозь шерстяное платье; зеркало держит пол-лица — вторая половина
у задумчивости; гравировка трофея ловит арт-деко-линию.
Spine: PL538 Arsenal-Fit Hug (venator) (venator) · K-FF mid_plate_hug · CAM02 · D3·A02 · LEAD the plate rim · art-deco register · closer image-close
Race: — (human; трофей решает)
Gar: CL-DR-13 (oversized cardigan worn as a dress, wool) · HS: HS12 Low Braided Chignon
Stack: CR-W47 + CR-B57 + CR-E42 + CR-D41
POS:
Masterpiece, best quality, absurdres, intricate details, trophy breastplate hugged to the chest in both arms, chin just over its rim, the fitting mirror holding her half-face, three-quarter, 1girl, solo, the wool above the plate's rim reading her breast shape, inked family-crest tattoo at the nape, oak-brown hair in a low braided chignon, deco-green eyes, warm porcelain skin, womanly build with soft settled breasts, mid_plate_hug
the trophy breastplate hugged honest in both crossed arms — the hugged plate is the claim, trophy-made
the breastplate's strap printing its stripe through the wool dress, the lean to the mirror opening the neckline one honest inch, the hem still carrying one beat of the placement
Art deco platinum palette, deco-platinum-pale over oak-brown-warm, graving-gold at the plate's lines, deco-green in the gaze; the war she ended leaves its colors on her: platinum, oak, one gold line.
stylized 2D anime face half in the mirror, anime eyes (deco-green, trophy-thought), small nose, small mouth in fit-quiet, the chignon holding one escaped strand.
NEG:
young girl, immature body, oversized head, loli, shota, signature, watermark, artist name, logo, 1boy, candle, lamp, photorealistic, 3d face, realistic facial structure, bad anatomy,
extra fingers, bad hands, washed-out, faded colors, low contrast, flat colors, muddy colors, dull, overexposed, underexposed, pastel colors,
muted colors, gray palette, pale colors, desaturated, white haze, milky fog, soft focus, hazy, patches, patched fabric, armor worn on body, plate closed over chest, sword raised, blood on plate, second figure, trophy rack, skull decor

P20 — blade-polish-window (NICHE · R34 Phoenix-kin · R · PL81 · P73_VERMEIL_SMOKE)
ARCH: N07 STILL_LIFE_WITH_BODY · DOOR: D03 AFTERMATH
THESIS: «ПОСЛЕ ОХОТЫ: ФЕНИКС-КИН НАКЛОНЕНА ЧЕРЕЗ НИЗКИЙ СТОЛ У ОКНА, ОБЕ ЛАДОНИ
ПЛОСКО НА СТОЛЕШНИЦЕ, КЛИНОК ЛОВИТ ДНЕВНУЮ СЕРУЮ ЛЕНТУ, ДВЕ НИЗКИЕ ЛИНИИ
ПЛЕЧОВЫХ ПЕРЬЕВ ЧИТАЮТСЯ СКВОЗЬ ТОНКУЮ ТКАНЬ, ПОЛИР-ПАСТА ОСЕДАЕТ ПЫЛЬЮ НА ПЛЕЧЕ».
Гэг-стек: клинок держит одну честную ленту света окна; перьевые гребни на плечах
читаются двумя линиями сквозь ткань; полир-паста оседает мелом на шерсти; перо
поймало один тёплый лоск.
Spine: PL81 Leaning Across Low Table (ecchi_classic) (ecchi_classic) · K-FF mid_blade_polish · CAM02 · D3·A02 · LEAD the blade band · vermeil-smoke register · closer image-close
Race: R34 Phoenix-kin — flame-feather accents at the shoulders, two low feather-ridges, warm ember skin · RF: перо ловит тёплый лоск.
Gar: CL-TS-02 (organza blouse translucent) + CL-SK-06 (pencil skirt back-slit) · HS: HS13 Messy Top-Bun, Strands Escaping
Stack: CR-B55 + CR-E46 + CR-D48
POS:
Masterpiece, best quality, absurdres, intricate details, leaning forward across the low window table, palms flat on the far edge, the blade catching one honest window band, eye level, 1girl, solo, two low feather-ridges reading through the thin blouse, flame-feather accents at the shoulders, warm ember skin, cinnamon-gold hair in a messy top bun, ember-rose eyes, lithe young build, mid_blade_polish
the blade's one clean window band running the frame — the window band is the claim, polish-made
the raised arm opening the collarbone's vault to the window's grey line, polish-paste settling chalk-fine on the wool shoulder, the two ridges reading their warmth through the organza
Vermeil smoke palette, vermeil-warm over smoke-grey-soft, cinnamon-gold at the hair line, smoke-rose at the eyes; her colors: the fire that learned to sit still.
stylized 2D anime face level to the blade's band, anime eyes (ember-rose, after-hunt calm), small nose, small mouth in polish-quiet, the top bun holding its escaped strands.
NEG:
young girl, immature body, oversized head, loli, shota, signature, watermark, artist name, logo, 1boy, candle, lamp, photorealistic, 3d face, realistic facial structure, bad anatomy,
extra fingers, bad hands, washed-out, faded colors, low contrast, flat colors, muddy colors, dull, overexposed, underexposed, pastel colors,
muted colors, gray palette, pale colors, desaturated, white haze, milky fog, soft focus, hazy, patches, patched fabric, phoenix muzzle, bird wings spread, flight, feathers falling, open flame, fire, organza fully clear, nude under blouse, second figure, sword raised

P21 — trophy-room-count (NICHE · R28 Sheep-kin · R · PL129 · P187_BONE_PORCELAIN)
ARCH: N39 COLLECTION_WALL · DOOR: D15 AWARE
THESIS: «ТРОФЕЙНАЯ КОМНАТА: ОВЦЬЯ СТОРОЖ НА КОРОТКАХ ПЕРЕД СТЕНОЙ РОГОВ ЧУЖИХ
ОХОТ, МАНТИЯ-ПЛАЩ ДРАПИРУЕТ СПИНУ, ПОДОЛ ЗАПРАВЛЕН ПОД КОЛЕНО, ХОЛОДНАЯ ПРЯЖКА
ТРОФЕЯ ОТПЕЧАТАЛА КОЛЬЦО НА ГОЛОМ ПРЕДПЛЕЧЬЕ — ОНА СЧИТАЕТ НЕ ТРОФЕИ, А ОХОТНИКОВ,
КОТОРЫЕ ЗА НИМИ НЕ ВЕРНУЛИСЬ».
Гэг-стек: кольцо-отпечаток пряжки на предплечье — час давности; подол заправлен под
колено — счёт на корточках; спиральные рожки ловят фарфоровый лоск стены; мантия
драпирует спину одной честной дугой.
Spine: PL129 Sitting on Wide Stone Steps (env_interaction) (env_interaction) · K-FF mid_trophy_count · CAM02 · D3·A02 · LEAD the ring-print · bone-porcelain register · closer image-close
Race: R28 Sheep-kin — spiral curled horns small, wool-soft skin, cloud-cream skin · RF: рожки — её счёт.
Gar: CL-SW-01 (oversized mohair sweater) + trophy cloak · HS: HS42 Two Dutch Braids Pinned Into a Crown
Stack: CR-B66 + CR-E63 + CR-D50
POS:
Masterpiece, best quality, absurdres, intricate details, kneeling low before the wall of horns, hem tucked under the working knee, the trophy cloak draping the back's whole line, three-quarter, 1girl, solo, spiral curled horns small at the crown, cloud-cream wool-soft skin, bone-white hair in two dutch braids pinned crown, milk-moonstone eyes, plush young build, mid_trophy_count
the cold trophy buckle's ring-print honest on the bare forearm — the ring-print is the claim, count-made
the mantle-cloak draping the back one honest arc, the braided crown catching the porcelain glint of the horn wall, one hunt's cord still knotted at the belt
Bone porcelain palette, porcelain-pale over bone-white-warm, milk-glass at the eyes, cloak-dye-deep at the mantle; her colors: the wall that remembers.
stylized 2D anime face low to the count, anime eyes (milk-moonstone, ledger-patient), small nose, small mouth in count-quiet, the spiral horns framing the crown braids.
NEG:
young girl, immature body, oversized head, loli, shota, signature, watermark, artist name, logo, 1boy, candle, lamp, photorealistic, 3d face, realistic facial structure, bad anatomy,
extra fingers, bad hands, washed-out, faded colors, low contrast, flat colors, muddy colors, dull, overexposed, underexposed, pastel colors,
muted colors, gray palette, pale colors, desaturated, white haze, milky fog, soft focus, hazy, patches, patched fabric, sheep muzzle, feral, wool coat full, hooves, horn wall falling, skull decor, blood, second figure, trophy taken down

P22 — shirt-only-settle (VOLT · human · R+ · PL539 · P152_LEATHER_TANNERY_AMBER)
Channel: shirt-claim (live; рубашка-одна оседает на плечо, ладонь прижимает ткань как фигуру на доске)
Corridor: A
Combo: D2-05 ZIPPER STUCK · Package: κ (CONTACT)
THESIS: «ПОСЛЕ БОЯ: ЕДИНСТВЕННАЯ РУБАШКА ОСЕДАЕТ НА ОДНО ПЛЕЧО, КОСТЯШКИ ЕЩЁ В
БИНТАХ, ЛАДОНЬ ПРИЖИМАЕТ ТКАНЬ ПЛОСКО — КАК ФИГУРУ НА ДОСКЕ — И АМБРА ДУБИЛЬНИ
ДЕРЖИТ ТЕПЛО ПОСЛЕДНЕЙ СХВАТКИ В СКЛАДКАХ».
Гэг-стек: рубашка осела на плечо против бинтов — ткань выбрала сторону; ладонь
прижала ткань плоско, как фигуру на доске; бинты на костяшках держат свои узлы;
складки хранят тепло дубильной амбры.
Spine: PL539 Shirt-Only Resettle (venator) (venator) · K-FF mid_shirt_settle · CAM03 · D4·A03 · LEAD the settling shirt · tannery-amber register · closer image-close
Race: — (human; рубашка решает)
Gar: CL-TS-10 (borrowed oversized button-up, worn as the only shirt) · HS: HS02 Shoulder Shag + Curtain Bangs
Stack: CR-W39 + CR-B22 + CR-E50 + CR-D22
POS:
Masterpiece, best quality, absurdres, intricate details, standing after the fight, the only shirt settling onto one shoulder, knuckles still wrapped, three-quarter from below, 1girl, solo, the thin shirt reading her breast shape honest, oversized button-up worn as the only shirt, hands pressed flat against her own chest line, bandage knots at the knuckles, umber-brown hair in a shoulder shag with curtain bangs, hide-amber eyes, warm tan skin, athletic young build, mid_shirt_settle
the thin shirt pressed flat against her by her own palm the way a piece is set on its square — the pressed shirt is the claim, after-made
the top two buttons undone like items crossed off a checklist, the collarbone field open under the collar's verdict, the settle still warm with the fight's amber
Leather tannery amber palette, tannery-amber-warm over hide-brown-deep, hide-amber at the eyes, shirt-cream at the weave; her colors: the match that ended polite.
stylized 2D anime face half into the settle, anime eyes (hide-amber, after-fight warm), small nose, small mouth in settle-flat, the curtain bangs parting one band.
NEG:
young girl, immature body, oversized head, loli, shota, signature, watermark, artist name, logo, 1boy, candle, lamp, photorealistic, 3d face, realistic facial structure, bad anatomy,
extra fingers, bad hands, washed-out, faded colors, low contrast, flat colors, muddy colors, dull, overexposed, underexposed, pastel colors,
muted colors, gray palette, pale colors, desaturated, white haze, milky fog, soft focus, hazy, patches, patched fabric, nude, topless, bra visible, shirt gone, bruise face, cuts, blood, fight scene, opponent figure, second figure

P23 — signal-whistle-rain (NICHE · R12 Bunny-kin · R · PL111 · P123_BEACON_RED_RAIN)
ARCH: N38 STATIONARY_RAIN · DOOR: D05 RETURN
THESIS: «ДОЖДЬ СТОИТ, А СИГНАЛ ИДЁТ: КРОЛЬЧИХА-СКАУТ СИДИТ НА СТУПЕНЯХ В НОЧНОЙ
ЛИВЕНЬ, СВИСТОК-СИГНАЛ НА ЗАПЯСТНОМ УЗЛЕ УЖЕ ПРОВИЗЖАЛ, КОСА-ФЛИК ДУГОЙ СБРОСИЛА
КАПЛИ, БЕДРО ЧИТАЕТ СВОЙ НАКЛОН ЧЕРЕЗ МОКРУЮ ТКАНЬ — ДЕЖУРСТВО НЕ ЖДЁТ СУХОГО».
Гэг-стек: свисток-узел на запястье мокрый блеском; коса сбросила капли дугой; мокрая
ткань держит тяжёлую прямую линию по бедру; лужа держит её отражение на полтакта
позже.
Spine: PL111 Sitting on Stairs Midway Up (env_interaction) (env_interaction) · K-FF mid_signal_whistle · CAM03 · D3·A03 · LEAD the whistle line · beacon-rain register · closer image-close
Race: R12 Bunny-kin — ears long-upright, one ear rain-bent, cotton-cream skin · RF: ухо читает дождь.
Gar: CL-TS-10 (borrowed oversized button-up over athletic crop) + CL-BT-01 (cutoff denim shorts) · HS: HS38 Fishtail Braid, Thick, Over Shoulder
Stack: CR-B52 + CR-E61 + CR-D60
POS:
Masterpiece, best quality, absurdres, intricate details, sitting on the midway steps in standing rain, knees two steps higher, the signal whistle's knot wet at the wrist, three-quarter from below, 1girl, solo, long-upright ears one rain-bent, signal whistle cord at the wrist, cotton-cream skin, rain-grey hair in a thick fishtail braid, beacon-red eyes, slight young build, mid_signal_whistle
the wet hem pulling its heavy straight line at the thigh honest — the wet hem line is the claim, rain-made
the sash feeding through its loop mid-motion at the wrist, the fishtail braid's flick arcing its own line of shaken drops, the puddle keeping her reflection one beat late
Beacon red rain palette, beacon-red-faint over rain-blue-grey-deep, rain-grey at the hair line, beacon-red in the gaze; the post never leaves her: red rain, grey sky, one wet hem line.
stylized 2D anime face lifted into the rain line, anime eyes (beacon-red, watch-wet), small nose, small mouth in signal-flat, the bent ear carrying its raindrop.
NEG:
young girl, immature body, oversized head, loli, shota, signature, watermark, artist name, logo, 1boy, candle, lamp, photorealistic, 3d face, realistic facial structure, bad anatomy,
extra fingers, bad hands, washed-out, faded colors, low contrast, flat colors, muddy colors, dull, overexposed, underexposed, pastel colors,
muted colors, gray palette, pale colors, desaturated, white haze, milky fog, soft focus, hazy, patches, patched fabric, bunny muzzle, feral, paws, tail puff visible, umbrella, rain stopped, downpour blurred, second figure, soaked underwear line, bra visible through shirt

P24 — empty-net-carry (EXQUISITE · human · R · PL540 · P168_INK_SILVER)
ARCH: N03 BODY_AS_LANDSCAPE · DOOR: D05 RETURN (M06 — финал: трофей легче шага)
THESIS: «ФИНАЛ ОХОТЫ — ШАГ ДОМОЙ: ПУСТАЯ СЕТЬ СВЁРНУЛА В ОДИН КУЛАК ЧЕРЕЗ ПЛЕЧО, А
ЗАКРЫТАЯ ЛАДОНЬ НЕСЁТ ПЕРЕД ГРУДЬЮ ДОБЫЧУ, КОТОРАЯ ВЕСИТ СОВЕСТЬ — ПЕРЛАМУТРОВАЯ
ПЫЛЬЦА ДУХА ОСЕДАЕТ НА ФАРТУКЕ, ПОДОЛ НЕСЁТ ОДИН БИТ ПОСАДКИ».
Гэг-стек: закрытая ладонь держит уровень чёрного чая — ни капли не пролито; пустая
сеть ловит один краешк света; пыльца духа оседает перламутром на фартуке; ступень
дома ловит её тень — тень вошла раньше неё.
Spine: PL540 Empty-Net Carry (venator) (venator) · K-FF mid_palm_carry · CAM02 · D2·A02 · LEAD the level palm · ink-silver register · closer image-close
Race: — (human; добыча решает)
Gar: CL-DR-11 (linen pinafore dress, bib flat) · HS: HS12 Low Braided Chignon
Stack: CR-W60 + CR-B41 + CR-F15 + CR-D41
POS:
Masterpiece, best quality, absurdres, intricate details, walking home with the empty net rolled in one fist over the shoulder, the other palm held carefully level before the chest, eye level, 1girl, solo, nape-to-wrist ink tattoo coiling the forearm, pearl-dust settling on the pinafore bib, raven-black hair in a low braided chignon, ink-graphite eyes, cool pale skin, gentle young build, mid_palm_carry
the closed palm carrying what weighs nothing honest and level — the level palm is the claim, spirit-made
both palms pressed flat-tense where the knuckles read, shell-dust leaving a nacre sheen on the apron, the hem still carrying one beat of the settle
Ink silver palette, ink-black-deep over silver-thread-pale, pearl-nacre at the apron dust, ink-pool at the eyes; her colors: the catch that agreed to come.
stylized 2D anime face level to the doorway's dusk, anime eyes (ink-graphite, carry-gentle), small nose, small mouth in carry-quiet, the chignon holding one silver strand.
NEG:
young girl, immature body, oversized head, loli, shota, signature, watermark, artist name, logo, 1boy, candle, lamp, photorealistic, 3d face, realistic facial structure, bad anatomy,
extra fingers, bad hands, washed-out, faded colors, low contrast, flat colors, muddy colors, dull, overexposed, underexposed, pastel colors,
muted colors, gray palette, pale colors, desaturated, white haze, milky fog, soft focus, hazy, patches, patched fabric, spirit visible, ghost figure, wisp creature flying, net full, fish in net, horror register, second figure, doorway crowd, lantern glowing

P25 — head-cradle-damascene (EXP · R43 Dullahan-kin · R+ · PL541 · P216_DAMASCENE_GOLD) ⚗
«Ладонь-колыбель» — голова несётся в собственном локтевом сгибе, мягко и гордо.
Фишечки: голова в собственном локтевом сгибе на высоте плеч · шов света на шее —
одна чистая линия · ремень тянут большим пальцем честно · регистр: вес держит близкий
кадр · расовый закон: the head cradled in her own arm.
ТЕСТ (постоянные: P216_DAMASCENE_GOLD + Y10 «weapon-weight strap torque + cover by the crooked arm»): верхний корпус слегка снизу: ремень тянет от веса, локоть-крюк держит прикрытие, голова в колыбели дремлет. Коридор A — локоть-крюк честно закрывает грудь.
Проверка: тяга ремня серединой кадра, шов света без жути, золото насечки тонко.
Corridor: A
Race: R43 Dullahan-kin — head carried separately in the crook of her own arm, neck-seam a clean line of soft light, pale moonlit skin · RF: голова — её знамя.
Spine: PL541 Head-Cradle Lean (y_card_build) (y_card_build) · K-FF mid_head_cradle · CAM04 · D2·A02 · LEAD the cradle · damascene register · closer image-close
Gar: CL-TS-01 (tie-collar blouse, strap mid-tug) · HS: HS24 Hip-Length Straight Sheet
Stack: CR-W61 + CR-S26 + CR-E60 + CR-D40
POS:
Masterpiece, best quality, absurdres, intricate details, upper body slight low angle, the head cradled in her own elbow-crook at shoulder height, the neck seam one clean line of soft light, 1girl, solo, strap tugged loose by her own thumb, bone-chalk dust drying white on the dark weave, silver-moon hair hip-length straight sheet, opal-grey eyes, pale moonlit skin, slender young build, mid_head_cradle
the weapon-weight strap pulling its torque honest while the crooked arm covers the chest line — the strap torque is the claim, cradle-made
the head resting its weight in the elbow-crook calm, the neck seam reading its one soft light line, one hair trembling off the still line
Damascene gold inlay palette, damascene-gold lines over forge-steel-grey, inlay-gold thin at the seams, cord-crimson-faint at the strap; her colors: the crest she carries herself.
stylized 2D anime face cradled level, anime eyes (opal-grey, cradle-calm), small nose, small mouth in cradle-quiet, the straight sheet pooling in the elbow-crook.
NEG:
young girl, immature body, oversized head, loli, shota, signature, watermark, artist name, logo, 1boy, candle, lamp, photorealistic, 3d face, realistic facial structure, bad anatomy,
extra fingers, bad hands, washed-out, faded colors, low contrast, flat colors, muddy colors, dull, overexposed, underexposed, pastel colors,
muted colors, gray palette, pale colors, desaturated, white haze, milky fog, soft focus, hazy, patches, patched fabric, horror register, gore, blood, exposed neck stump, wound, headless body horror, wires, second figure, two heads, head on ground

P26 — fan-tail-urushi (EXP · R50 Nine-tails-kin · R+ · PL542 · P217_URUSHI_LACQUER) ⚗
«Веер-экран» — девять хвостов веером за спиной, прижатые весом голеней.
Фишечки: девять хвостов веером как складная ширма · подол прижат весом голеней ·
лунная пыльца оседает на фартуке · регистр: kneel-settle честный · расовый закон: tails fanned behind her like a folding screen.
ТЕСТ (постоянные: P217_URUSHI_LACQUER + Y11 «kneel-back settle + hem pinned under shin weight»): kneel-settle назад на пятки, подол прижат, веер хвостов рама торса. Коридор B — поза и камера несут интим.
Проверка: вес голеней прижимает подол честно, веер читается рамой, лак держит один блик.
Corridor: B
Race: R50 Nine-tails-kin — nine tails fanned behind her like a folding screen, silver-tipped fox ears, moon-white skin · RF: ширма решает раму.
Spine: PL542 Fan-Tail Settle (y_card_build) (y_card_build) · K-FF mid_tail_fan · CAM03 · D2·A02 · LEAD the pinned hem · urushi register · closer image-close
Gar: CL-SK-04 (breezy maxi skirt) + CL-TS-07 (off-shoulder top) · HS: HS34 Volume Blowout, 80s Bounce
Stack: CR-W60 + CR-S09 + CR-L20 + CR-D59
POS:
Masterpiece, best quality, absurdres, intricate details, kneeling back onto her heels mid-settle, hem pinned under the shin weight, the nine tails fanned framing the torso, slight low angle, 1girl, solo, nine tails fanned behind her like a folding screen, silver-tipped fox ears, moon-white skin, shell-white hair in an 80s volume blowout, lacquer-red eyes, plush young build, mid_tail_fan
the hem pinned honest under the shin weight while the settle rides back — the pinned hem is the claim, fan-made
the nine tails holding their folding-screen arc frame, shell-dust leaving a nacre sheen on the apron, the wrap's edge letting the lace's line read
Urushi lacquer palette, urushi-lacquer-red over lacquer-black-deep, shell-gold-dust at the tails, one wet-resin highlight at the settle; her colors: the screen nobody opens.
stylized 2D anime face set above the fan frame, anime eyes (lacquer-red, settle-calm), small nose, small mouth in screen-quiet, the silver ear-tips catching first.
NEG:
young girl, immature body, oversized head, loli, shota, signature, watermark, artist name, logo, 1boy, candle, lamp, photorealistic, 3d face, realistic facial structure, bad anatomy,
extra fingers, bad hands, washed-out, faded colors, low contrast, flat colors, muddy colors, dull, overexposed, underexposed, pastel colors,
muted colors, gray palette, pale colors, desaturated, white haze, milky fog, soft focus, hazy, patches, patched fabric, eight tails, ten tails, tail count wrong, one tail, fox muzzle, feral, tails tangled, second figure, tail lifting hem, tail around body

P27 — halo-tilt-niello (EXP · R48 Eclipse-officiant-kin · R+ · PL543 · P218_NIELLO_BLACK) ⚗
«Ореол-знамя» — куртка сползает с плеча, рукав зацеп за сгиб локтя, ореол-кольцо ровно.
Фишечки: ореол как бело-горячее корона-кольцо в руке · рукав пойман за сгиб локтя ·
гусиная кожа от снятой куртки · регистр: честное сползание · расовый закон: halo as a white-hot corona ring held or hovering.
ТЕСТ (постоянные: P218_NIELLO_BLACK + Y12 «jacket sliding off one shoulder + sleeve caught at the elbow fold»): куртка сползает в медленном наклоне, рукав зацеп честно, ореол-кольцо держит ровность. Коридор A — рукав и наклон несут прикрытие.
Проверка: зацеп рукава серединой кадра, ореол не мигает, чернь держит серебро.
Corridor: A
Race: R48 Eclipse-officiant-kin — halo as a white-hot corona ring held or hovering, eclipse-dusk skin, ritual calm · RF: кольцо держит ровность.
Spine: PL543 Halo-Tilt Slide (y_card_build) (y_card_build) · K-FF mid_halo_slide · CAM02 · D2·A02 · LEAD the sleeve catch · niello register · closer image-close
Gar: CL-OU-02 (ritual jacket, sleeve mid-slide) · HS: HS35 Micro-Fringe + Long Straight
Stack: CR-W56 + CR-S13 + CR-E44 + CR-D43
POS:
Masterpiece, best quality, absurdres, intricate details, eye level close, jacket sliding off one shoulder in a slow tilt, sleeve caught at the elbow fold, the halo ring held steady above, 1girl, solo, white-hot corona ring hovering level, eclipse-dusk skin, ash-lilac hair micro-fringe long straight, umbral-purple eyes, slender young build, mid_halo_slide
the jacket's slide honest with the sleeve caught at the elbow fold — the caught sleeve is the claim, rite-made
the goosebumps' field rising across the bare shoulder at the hall's cold, the shrug letting the cardigan drop one shoulder, the corridor draft running through the opened door
Niello engraved silver palette, niello-black over engraved-silver-line, old-mirror-grey at the ring, ember-faint at the edges; her colors: the eclipse she officiates.
stylized 2D anime face level under the ring, anime eyes (umbral-purple, rite-calm), small nose, small mouth in rite-quiet, the micro-fringe ruling the brow line.
NEG:
young girl, immature body, oversized head, loli, shota, signature, watermark, artist name, logo, 1boy, candle, lamp, photorealistic, 3d face, realistic facial structure, bad anatomy,
extra fingers, bad hands, washed-out, faded colors, low contrast, flat colors, muddy colors, dull, overexposed, underexposed, pastel colors,
muted colors, gray palette, pale colors, desaturated, white haze, milky fog, soft focus, hazy, patches, patched fabric, halo flickering, halo on ground, ring tilted, angel wings, religious cross, horror register, second figure, jacket gone, sleeve free

P28 — shadow-turn-cloisonne (EXP · R45 Shadow-kin · R+ · PL544 · P219_CLOISONNE_EMERALD) ⚗
«Тень на полтакта раньше» — фартук в повороте, угол пойман сгибом локтя.
Фишечки: живая тень отставшая от ног на пол-такта · угол фартука в сгибе локтя ·
две мягкие тени, которые топ не прячет · регистр: поворот-в-двух-телах · расовый закон: living shadow detached from her feet, a half-beat ahead.
ТЕСТ (постоянные: P219_CLOISONNE_EMERALD + Y13 «apron wrap mid-turn + corner caught in the elbow bend»): фартук обёрнут в повороте, угол пойман локтем, дуга подола доезжает. Коридор B — поворот и камера несут интим.
Проверка: угол в локте серединой кадра, тень честно впереди, эмаль держит ячейки.
Corridor: B
Race: R45 Shadow-kin — living shadow detached from her feet moving a half-beat ahead, ink-velvet skin · RF: тень — её напарник.
Spine: PL544 Shadow-Turn Wrap (y_card_build) (y_card_build) · K-FF mid_shadow_turn · CAM02 · D3·A02 · LEAD the caught corner · cloisonne register · closer image-close
Gar: CL-DR-05 (shirt dress half-buttoned) + work apron · HS: HS28 Twin Buns Low (Princess) With Ribbon Ties
Stack: CR-W37 + CR-B24 + CR-E53 + CR-D51
POS:
Masterpiece, best quality, absurdres, intricate details, apron wrap caught mid-turn, corner taken by the elbow bend, hem arc still traveling, eye level, 1girl, solo, living shadow a half-beat ahead of her feet, the two soft shadows the tee cannot hide, ink-velvet skin, ink-black hair in low twin buns with ribbon ties, cloisonne-green eyes, lithe young build, mid_shadow_turn
the apron's corner caught honest in the elbow bend while the turn rides — the caught corner is the claim, shadow-made
the cross-straps of the apron leaving the back bare, the rope's swing of the hem carrying her hip one beat late, the shadow finishing the turn first
Cloisonne emerald palette, cloisonne-emerald cells over enamel-cream-base, gilt-wire-gold at the cell walls, ink-velvet at the skin; the clock she outruns chases her in emerald cells and gilt.
stylized 2D anime face arriving into the turn, anime eyes (cloisonne-green, shadow-playful), small nose, small mouth in turn-quiet, the ribbon ties mid-swing.
NEG:
young girl, immature body, oversized head, loli, shota, signature, watermark, artist name, logo, 1boy, candle, lamp, photorealistic, 3d face, realistic facial structure, bad anatomy,
extra fingers, bad hands, washed-out, faded colors, low contrast, flat colors, muddy colors, dull, overexposed, underexposed, pastel colors,
muted colors, gray palette, pale colors, desaturated, white haze, milky fog, soft focus, hazy, patches, patched fabric, shadow person, second figure, doppelganger, shadow on wall only, apron gone, apron untied, horror register, dark aura, smoke body

P29 — wing-tuck-jade (EXP · R39 Nephilim-kin · R+ · PL545 · P220_JADE_CARVE) ⚗
«Наклон на обе ладони» — ворот открывается наклоном, крылья сложены под весом.
Фишечки: маленькие белые крылья сложены тесно за спиной · ворот открывается наклоном ·
мост ткани натянут по рёбрам · регистр: опора честная · расовый закон: small white wings folded tight at the back.
ТЕСТ (постоянные: P220_JADE_CARVE + Y14 «lean back on both palms + collar opens by the lean»): наклон назад на обе ладони, мост ткани по рёбрам, ворот открывается весом. Коридор A+B — прикрытие мостом ткани, наклон несёт интим.
Проверка: мост ткани серединой кадра, крылья под весом лопаток, нефрит глубока.
Corridor: A+B
Race: R39 Nephilim-kin — small white wings folded tight at the back, feather-soft shoulders, dawn-pearl skin · RF: крылья — её молчание.
Spine: PL545 Wing-Tuck Lean-Back (y_card_build) (y_card_build) · K-FF mid_wing_tuck · CAM03 · D3·A02 · LEAD the fabric bridge · jade register · closer image-close
Gar: CL-TS-01 (tie-collar blouse, collar mid-open) · HS: HS24 Hip-Length Straight Sheet
Stack: CR-W62 + CR-A15 + CR-E42 + CR-D58
POS:
Masterpiece, best quality, absurdres, intricate details, leaning back onto both palms, collar opening by the lean, fabric bridging taut across the ribs, slight low angle, 1girl, solo, small white wings folded tight at the back, dawn-pearl skin, pearl-white hair hip-length straight sheet, jade-pool eyes, feather-soft shoulders, supple young build, mid_wing_tuck
the fabric's bridge taut across the ribs while the lean opens the collar honest — the fabric bridge is the claim, dawn-made
the lean to the mirror line opening the neckline one honest inch, the coil's release dropping her weight a knuckle onto both palms, wings holding their fold under the shoulder-blades' weight
Jade stone carve palette, jade-green-stone over celadon-pale-mist, carve-bone-white at the wings, iron-oxide-faint at the edges; her colors: the gate she watches.
stylized 2D anime face tilted above the lean, anime eyes (jade-pool, gate-patient), small nose, small mouth in gate-quiet, the straight sheet falling open one line.
NEG:
young girl, immature body, oversized head, loli, shota, signature, watermark, artist name, logo, 1boy, candle, lamp, photorealistic, 3d face, realistic facial structure, bad anatomy,
extra fingers, bad hands, washed-out, faded colors, low contrast, flat colors, muddy colors, dull, overexposed, underexposed, pastel colors,
muted colors, gray palette, pale colors, desaturated, white haze, milky fog, soft focus, hazy, patches, patched fabric, wings spread, flight, halo, angel glow, wings torn, feather falling, nude, blouse open wide, second figure, sitting on lap

P30 — cloak-perch-abalone (EXP · R58 Belfry-owl-kin · R+ · PL546 · P221_ABALONE_NACRE) ⚗
«Затяжка ремня на насесте» — ремень затягивается против наклона, вес честный.
Фишечки: огромные безмолвные совиные крылья сложены плащом · ремень затягивается
против наклона · крылатая дрожь при оседании · регистр: насест честный · расовый закон: huge silent owl wings folded close like a cloak.
ТЕСТ (постоянные: P221_ABALONE_NACRE + Y15 «belt cinch mid-pull against the perch's lean»): на широкой балке колокольни, ремень в тяге, вес на кромке сиденья честный. Коридор B — насест и снизу-камера несут интим.
Проверка: тяга ремня против наклона, вес на кромке, перламутр меняет оттенок.
Corridor: B
Race: R58 Belfry-owl-kin — huge silent owl wings folded close like a cloak, dusk-plumage feathering at the collarbones, moon-bone skin · RF: крылья — её тишина.
Spine: PL546 Cloak-Perch Cinch (y_card_build) (y_card_build) · K-FF mid_perch_cinch · CAM04 · D2·A02 · LEAD the cinch pull · abalone register · closer image-close
Gar: CL-OU-01 (cropped denim jacket) + CL-SK-10 (high-low asymmetric skirt) · HS: HS29 French Twist, Screwed High
Stack: CR-W42 + CR-S07 + CR-E57 + CR-D63
POS:
Masterpiece, best quality, absurdres, intricate details, perched on the belfry beam, belt cinched mid-pull against the perch's lean, weight honest on the seat edge, from below, 1girl, solo, huge silent owl wings folded close like a cloak, dusk-plumage feathering at the collarbones, moon-bone skin, dawn-mauve hair in a screwed-high french twist, abalone-opal eyes, lithe young build, mid_perch_cinch
the belt's cinch pulling honest against the lean while the weight rides the seat edge — the cinch pull is the claim, belfry-made
the cage rail catching the shirt's hem up one honest fold, the latch's jolt running its line up her arm, shell-dust nacre sheen shifting with the tilt
Abalone nacre palette, abalone-nacre over oil-sheen-green-pink, mother-of-pearl-pale at the wings, cobalt-faint at the shell rim; her colors: the silence that hunts.
stylized 2D anime face turned down from the perch, anime eyes (abalone-opal, perch-calm), small nose, small mouth in belfry-quiet, the french twist holding one loose feather strand.
NEG:
young girl, immature body, oversized head, loli, shota, signature, watermark, artist name, logo, 1boy, candle, lamp, photorealistic, 3d face, realistic facial structure, bad anatomy,
extra fingers, bad hands, washed-out, faded colors, low contrast, flat colors, muddy colors, dull, overexposed, underexposed, pastel colors,
muted colors, gray palette, pale colors, desaturated, white haze, milky fog, soft focus, hazy, patches, patched fabric, owl muzzle, feral, wings spread, flight, talons, feathers falling, horror register, second figure, falling off beam, bells swinging

P31 — silk-bridge-copper (EXP · R35 Arachne-kin · R+ · PL547 · P222_ETCHED_COPPER) ⚗
«Мост ткани» — подол заправлен поднятой рукой, ткань мостом по рёбрам.
Фишечки: маленькие хитиновые ноги у нижней части спины держат контрвес · подол
заправлен поднятой рукой · вены-паутинка на боку честно · регистр: мост натянут ·
расовый закон: small chitin legs at the lower back.
ТЕСТ (постоянные: P222_ETCHED_COPPER + Y16 «shirt hem tucked by the raised arm + fabric bridge across the ribs»): рука вверх заправляет подол, мост ткани по рёбрам, хитин держит скрутку. Коридор A — мост ткани несёт прикрытие.
Проверка: мост по рёбрам серединой кадра, хитиновый контрвес, медь травлённая.
Corridor: A
Race: R35 Arachne-kin — small chitin legs at the lower back, silk-soft skin, web-silk patience · RF: хитин — её контрвес.
Spine: PL547 Silk-Spin Bridge (y_card_build) (y_card_build) · K-FF mid_silk_bridge · CAM02 · D3·A02 · LEAD the rib bridge · etched-copper register · closer image-close
Gar: CL-TS-14 (bandage wrap top) + CL-SK-05 (plaid pleated skirt) · HS: HS31 Box Braids, Long, Beaded Tips
Stack: CR-W36 + CR-B65 + CR-E56 + CR-D62
POS:
Masterpiece, best quality, absurdres, intricate details, upper body, shirt hem tucked by the raised arm, fabric bridging taut across the ribs, slight low angle, 1girl, solo, small chitin legs at the lower back holding the twist's counterweight, silk-soft skin, web-vein map climbing the side honest, bronze-brown skin, copper-knot hair in long box braids with beaded tips, patina-green eyes, lithe young build, mid_silk_bridge
the fabric bridge holding its taut line across the ribs while the arm tucks the hem — the rib bridge is the claim, web-made
the bandage roll open along the ribs one honest line, the cold's shiver rippling across the silk where the chitin legs counterweight the twist, beaded tips clicking their count
Etched copper palette, etched-copper-warm over verdigris-green-deep, patina-teal in the grooves, ink-etch-black at the chitin; her colors: the weave that waits.
stylized 2D anime face level over the bridge line, anime eyes (patina-green, web-patient), small nose, small mouth in bridge-quiet, the beaded braid tips holding their rhythm.
NEG:
young girl, immature body, oversized head, loli, shota, signature, watermark, artist name, logo, 1boy, candle, lamp, photorealistic, 3d face, realistic facial structure, bad anatomy,
extra fingers, bad hands, washed-out, faded colors, low contrast, flat colors, muddy colors, dull, overexposed, underexposed, pastel colors,
muted colors, gray palette, pale colors, desaturated, white haze, milky fog, soft focus, hazy, patches, patched fabric, spider muzzle, feral, eight legs full, web cocoon, silk wrapped body, horror register, extra limbs on torso front, second figure, web ceiling

P32 — ghost-hem-bone-inlay (EXP · R33 Ghost-kin · R+ · PL548 · P223_BONE_INLAY_PALE) ⚗
«Подол без руки» — подол поднят телом, не рукой: проход сквозь собственную складку.
Фишечки: полупрозрачный низ тела проходит сквозь собственную складку подола ·
сквозняк обнимает пончо · жемчужные линии конденсата у ключиц · регистр: тихий проход ·
расовый закон: semi-transparent lower body.
ТЕСТ (постоянные: P223_BONE_INLAY_PALE + Y17 «hem lifted where no hand holds it + lower body passing through its own fold»): подол поднят проходом тела, сквозняк в пончо, ключицы в жемчужных линиях. Коридор B — проход и камера несут интим.
Проверка: проход сквозь складку серединой кадра, прозрачность только нижней трети, кость-инкрустация геометрична.
Corridor: B
Race: R33 Ghost-kin — semi-transparent lower body, mist-soft edges, bone-pale skin · RF: прозрачность — её лестница.
Spine: PL548 Ghost-Step Hem-Lift (y_card_build) (y_card_build) · K-FF mid_ghost_hem · CAM02 · D2·A02 · LEAD the no-hand hem · bone-inlay register · closer image-close
Gar: CL-DR-09 (layered tulle petticoat dress) + short poncho · HS: HS40 Choppy Lob + Deep Side Part
Stack: CR-W53 + CR-B74 + CR-E64 + CR-D64
POS:
Masterpiece, best quality, absurdres, intricate details, eye level, the hem lifted where no hand holds it, the body passing halfway through its own fold, feet already a step into the next room, 1girl, solo, semi-transparent lower body through the tulle fold, bone-pale skin, frost-white hair in a choppy lob with deep side part, moonstone-pale eyes, slight young build, mid_ghost_hem
the hem lifted honest by the body's own pass — the no-hand hem is the claim, ghost-made
the draft billowing the short poncho against her side, salt drying as pearl lines along the collarbone, the tulle keeping its layers where the body crosses
Bone inlay pale palette, bone-inlay-pale over ebony-black-deep, ivory-cream-line at the tulle edges, charcoal-silver-faint at the mist; her colors: the room she leaves.
stylized 2D anime face level through the hem's lift, anime eyes (moonstone-pale, pass-gentle), small nose, small mouth in pass-quiet, the side part ruling the frost strands.
NEG:
young girl, immature body, oversized head, loli, shota, signature, watermark, artist name, logo, 1boy, candle, lamp, photorealistic, 3d face, realistic facial structure, bad anatomy,
extra fingers, bad hands, washed-out, faded colors, low contrast, flat colors, muddy colors, dull, overexposed, underexposed, pastel colors,
muted colors, gray palette, pale colors, desaturated, white haze, milky fog, soft focus, hazy, patches, patched fabric, full body transparent, head transparent, horror register, ghost face scream, spirit floating full, second figure, body split, fog monster, see-through chest

P33 — smoke-taper-tooling (EXP · R57 Incense-wisp-kin · R · PL549 · P224_TOOLING_LEATHER) ⚗
«Перчатка с хвата» — перчатка снимается С ХВАТА, напястник несёт линию подола.
Фишечки: волосы на кончиках редеют в бледный дым ладана · перчатка снята до костяшек
с рабочего хвата · напястник поднимает линию подола · регистр: process честный ·
расовый закон: hair rising and thinning into pale incense smoke at the tips.
ТЕСТ (постоянные: P224_TOOLING_LEATHER + Y18 «glove peel mid-grip + wrist-guard raising the hem line»): близкий инзерт у арсенального стеллажа: перчатка с хвата, дым кончиков волос наклоняется с тягой. Честный R — процесс-заявка без тир-токена.
Проверка: снятие с хвата серединой кадра, дым наклоняется честно, кожа тиснёная.
Race: R57 Incense-wisp-kin — hair rising and thinning into pale incense smoke at the tips, ash-cream skin, slow-burn calm · RF: дым — её дыхание.
Spine: PL549 Smoke-Taper Peel (y_card_build) (y_card_build) · K-FF mid_smoke_peel · CAM02 · D2·A02 · LEAD the mid-grip peel · tooling-leather register · closer image-close
Gar: CL-TS-08 (athletic crop top) + work apron + wrist guards · HS: HS21 Pixie Crop, Tousled
Stack: CR-A12 + CR-E62 + CR-D55
POS:
Masterpiece, best quality, absurdres, intricate details, close insert at eye level on the glove peel mid-grip, wrist-guard raising the hem line where it passes, 1girl, solo, hair rising and thinning into pale incense smoke at the tips, one glove peeled to the knuckles, ash-cream skin, sage-grey hair in a tousled pixie crop, ember-tipped eyes, slight young build, mid_smoke_peel
the glove peeling off the working grip honest while the wrist-guard raises the hem line — the mid-grip peel is the count, process-made
the smoke tips leaning with the pull's direction, the bell-hum of the armory trembling the fabric a hairline, the cross-legged wrap's cloth between the thighs at the sit
Tooling leather palette, tooled-leather-amber-brown over wax-brown-deep, saddle-stitch-cream at the seams, brass-buckle-dim at the guard; her colors: the burn that never hurries.
stylized 2D anime face close over the peel, anime eyes (ember-tipped, burn-patient), small nose, small mouth in process-quiet, the pixie crop smoking at its tips.
NEG:
young girl, immature body, oversized head, loli, shota, signature, watermark, artist name, logo, 1boy, candle, lamp, photorealistic, 3d face, realistic facial structure, bad anatomy,
extra fingers, bad hands, washed-out, faded colors, low contrast, flat colors, muddy colors, dull, overexposed, underexposed, pastel colors,
muted colors, gray palette, pale colors, desaturated, white haze, milky fog, soft focus, hazy, patches, patched fabric, smoke monster, full smoke body, incense censor swung, fire, burning, ash falling heavy, horror register, second figure, glove gone, hands bare both

═══════════════════════════════ КОНЕЦ СЛОТОВ ═══════════════════════════════
