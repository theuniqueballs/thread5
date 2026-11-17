# -*- coding: utf-8 -*-
import io

path = '/home/z/my-project/thread5/batches/T5-18.md'
s = io.open(path, encoding='utf-8').read()

def rep(old, new):
    global s
    n = s.count(old)
    assert n == 1, "count=%d for: %r..." % (n, old[:80])
    s = s.replace(old, new)

# 1) интерпретация -> вето
rep(u"""интерпретация писца (объявлена, вето дёшево): темы ОС → темы ДЕВЯТИ EXP-кандидатов
(3 Tsundere Paradise + 3 Notre-Dame notte di natale + 3 Dirty Bitch); отдельных канон-ОС
слотов нет → 33 = 24 мейна + 9 EXP; «не всё по разному» = в КАЖДОМ EXP-слоте одна и та же
триада (кандидат + своя палитра + X3-комбо), палитры девять РАЗНЫХ семей.""",
u"""ВЕТО автора (2026-11-09, вечер, дословно): «EXP слоты для EXP хуйни, там нет темы.
Темы для ОС были для ОС из канона». Интерпретация «темы ОС → темы 9 EXP-кандидатов» СНЯТА.
Пересборка: темы ОС (Tsundere Paradi / Notre-Dame notte di natale / Dirty Bitch) → ТРИ
канон-ОС слота P01–P03 (EXQUISITE, канон VERBATIM, закон T5-05 — ОС-промпты не следуют
теме батча); EXP-слоты P25–P33 — чистый эксперимент БЕЗ темы: триада (кандидат + своя
палитра + X3-комбо), палитры девять РАЗНЫХ семей. 33 = 3 ОС + 21 мейн + 9 EXP.
ОС-тройка ротацией (мимо Lyn/Noa/Vae T5-16, Hana/Lucy/Rin T5-17): Nix ← Tsundere Paradi ·
Ash ← Notre-Dame notte di natale · Ana ← Dirty Bitch (фит объявлен, замена за одно слово).
Срез вето: мейны P01–P03 (чай вверх / лестница в воздух / дождь вверх) — концепты в резерв,
реестровые записи PL400–402 · K216–218 не тронуты (ledger append-only).""")

# 2) первая партия
rep(u"""Первая партия на poses.json 1.8.0 (33 first-use PL400–PL432), palettes.json 1.3.0
(+P171–P179 exp_color_wave_3), camera.json 1.5.0 (+эксп-комбо X3 «В-ШЁПОТ»; X2 «В-СЛЕД»
вердиктом T5-17 не принята — архив), pools.json 1.2.0 (+33 K-FF K216–K248), races.json
2.5.0 (+R53–R61 кандидатские). Имена IP — никогда (Alice, Hatter, Cheshire, White Rabbit,
Queen of Hearts, March Hare, Dormouse, Wonderland, Looking-Glass); титул темы в POS не
пишется; токен «camera» — 0.""",
u"""Первая партия: poses.json 1.8.0 (33 first-use PL400–PL432) → после вето 1.8.1
(+PL433–435 ОС-позы; PL400–402 остаются в ledger на срезанных слотах), palettes.json
1.3.0 (+P171–P179 exp_color_wave_3), camera.json 1.5.0 (+X3 «В-ШЁПОТ»; X2 «В-СЛЕД» архив),
pools.json 1.2.0 (+33 K-FF K216–K248) → 1.2.1 (+K249–251 ОС-миды), races.json 2.5.0
(+R53–R61 кандидатские). ОС-палитры из реестра (свободны в окне глубины 3, ни одной
violet-dominant): P69_EMBER_FROST → P01 · P06_OBSIDIAN_GOLD → P02 · P115_HONEY_TRAP → P03.
Имена IP — никогда (Alice, Hatter, Cheshire, White Rabbit, Queen of Hearts, March Hare,
Dormouse, Wonderland, Looking-Glass); имена ОС в POS — никогда; титул темы в POS не
пишется; токен «camera» — 0.""")

# 3) гипотеза: 13 R+ -> 11
rep(u"""  (3) Во ВСЕХ 13 R+ мейнах заявка-вещь стоит первым элементом кадра (урок В16, M07
  standing) — опровергается, если хоть один R+ живёт только регистром зрелища.""",
u"""  (3) Во ВСЕХ 11 R+ мейнах заявка-вещь стоит первым элементом кадра (урок В16, M07
  standing; после вето 11 вместо 13) — опровергается, если хоть один R+ живёт только
  регистром зрелища.""")

# 4) ТЕМА-СЛОВА: ОС-ТЕМЫ блок после НИКОГДА-хвоста
rep(u"спящие-красавицы и балдахины, приборные склейки света (flashlight/lamp/desk lamp).",
u"""спящие-красавицы и балдахины, приборные склейки света (flashlight/lamp/desk lamp).

ОС-ТЕМЫ (свои для P01–P03, не тема батча — закон T5-05; слово легально, когда называет
ПРЕДМЕТ кадра): P01 Tsundere Paradi — the gift she pretends is not for you · the tags
turned face-down · the key she will not lend; НИКОГДА: слово «tsundere» в POS, надписи на
бирках (В17). P02 Notre-Dame notte di natale — the mass kept for no congregation · the
rose window sieved by snow-light · the vow wound on both wrists; НИКОГДА: «Notre-Dame»,
«Hunchback», IP-имена, свеча-инструмент в POS (NEG candle), зимнее окно + тёплый источник
в ладонях (В18). P03 Dirty Bitch — the honey she keeps for herself · the string that
pulls itself · the bowl dented by her own fingers; НИКОГДА: «bitch»/«dirty» как лексемы
в POS; дрянь = регистр поступка, не слово.""")

# 5) HEAT
rep(u"""NICHE: PG-13 (3) · R (7) · R+ (2) · VOLT: R+ (10) · R (1) · EXQUISITE: R+ (1) ·
EXP: R+ (6) · R (3). Спред мейнов R+×13 · R×8 · PG-13×3. Итого 33: R+×19 · R×11 · PG-13×3 (EXP-оверлей: R+×6 · R×3).
Эротика ≠ тир (урок В16): каждый R+ несёт заявка-вещь ПЕРВЫМ элементом кадра — зрелище
строится ПОСЛЕ якоря; R-слоты держат тело честным (ткань/посадка), PG-13 держат форму.""",
u"""EXQUISITE (ОС): R+ (3) · NICHE: PG-13 (2) · R (7) · R+ (1) · VOLT: R+ (9) · R (1) ·
EXQUISITE (мейн): R+ (1) · EXP: R+ (6) · R (3). Спред мейнов R+×11 · R×8 · PG-13×2.
Итого 33: R+×20 · R×11 · PG-13×2 (EXP-оверлей: R+×6 · R×3).
Эротика ≠ тир (урок В16): каждый R+ (включая ОС) несёт заявка-вещь ПЕРВЫМ элементом
кадра — зрелище строится ПОСЛЕ якоря; R-слоты держат тело честным (ткань/посадка),
PG-13 держат форму.""")

# 6) структура
rep(u"""33 слота = 24 мейна «Reverse Wonderland» (P01–P24) + 9 EXP (P25–P33).
Канон-ОС слотов нет (интерпретация заказа: темы ОС ушли в EXP-кандидатов).
каст 14/24 (12 кодов кинов + human×12). EXP: R53–R61, код на слот.
Регистры форм тела: student×6 · young×18 · full×9.
Камера: D1×1 · D2×5 · D3×10 · D4×7 · D5×1 (мейки); EXP-константа D2×A02 ×9 ⚗.
Токен «camera» — 0; приборы света — 0 (закон света v2; физические источники в сцене).""",
u"""33 слота = 3 канон-ОС «свои темы» (P01–P03, EXQUISITE R+: Nix · Ash · Ana, канон
VERBATIM, закон T5-05) + 21 мейн «Reverse Wonderland» (P04–P24) + 9 EXP (P25–P33, без
тем — вето).
каст мейнов 10/21 (10 кодов кинов + human×11); ОС — канон-ростер (Nix human · Ash human ·
Ana канон VERBATIM). EXP: R53–R61, код на слот.
Регистры форм тела: student×6 · young×17 · full×10 (срез вето снял три young-мейна; ОС
дали young×2 + full×1).
Камера (мейки): D1×1 · D2×4 · D3×9 · D4×7 · D5×0 (срез вето забрал D2/D3/D5); ОС:
D2·A01 Nix · D3·A02 Ash · D5·A03 Ana; EXP-константа D2×A02 ×9 ⚗.
Токен «camera» — 0; приборы света — 0 (закон света v2; физические источники в сцене).""")

# 7) X3 шёпот-контент
rep(u"""токен «camera» — 0; шёпот-контент = голос кандидата
(тест характера встроен в камеру: цундере шепчет отречение, собор — благословение, дрянь —
грязь). Pose: first-use""",
u"""токен «camera» — 0; шёпот-контент = голос кандидата
(тест характера встроен в камеру; разметка «цундере/собор/дрянь» снята вето — кандидаты
шепчат своё, без тем). Pose: first-use""")

# 8) акты
rep(u"""ACT I — КРАЙ (P01–P08): правило ломается в быту (чай вверх, лестница в воздух, дождь
вверх, часы назад, колода сама сдаёт, сад стрижёт себя, ключ снаружи, зеркало с опозданием).
ACT II — МАШИНА (P09–P18): чудо как бюрократия (падение на потолок, письмо пишет себя,
дверь уменьшается, прилив в комнате, вердикт задом наперёд, каталог снов, чайный дождь,
улитки-курьеры, весы лжи).
ACT III — ПИК (P19–P24): мир слушается её (окно выросло в собор, улыбка приходит первой,
бельё от пола до неба, книги читают её, солнце живёт в чайнике, порог открывается в небо).
EXP (P25–P33): шёпот у самого уха — голос кандидата как тест характера.""",
u"""ОС (P01–P03): свои темы, не тема батча (закон T5-05): Tsundere Paradi · Notre-Dame
notte di natale · Dirty Bitch — EXQUISITE R+, канон VERBATIM.
ACT I — КРАЙ (P04–P08): правило ломается в быту (часы назад, колода сама сдаёт, сад
стрижет себя, ключ снаружи, зеркало с опозданием).
ACT II — МАШИНА (P09–P18): чудо как бюрократия (падение на потолок, письмо пишет себя,
дверь уменьшается, прилив в комнате, вердикт задом наперёд, каталог снов, чайный дождь,
улитки-курьеры, весы лжи).
ACT III — ПИК (P19–P24): мир слушается её (окно выросло в собор, улыбка приходит первой,
бельё от пола до неба, книги читают её, солнце живёт в чайнике, порог открывается в небо).
EXP (P25–P33): шёпот у самого уха — голос кандидата как тест характера (без тем — вето).""")

# 9) окно ротации
rep(u"""ЗАПРЕТ ОКНА: позы 99 (PL300–PL399) · палитры 91 · кинетики 0 · носители 179 · BURN 19.
Окно ротации: запрет 99 поз (PL300–399) / 91 палитра / 179 носителей / 19 burn. Ответ батча: 33 first-use PL400–PL432; палитры — 24 свободных из реестра + 9 новых
(P171–P179); кинетики — 33 новых K-FF (K216–K248); носители — только вне окна и вне burn.""",
u"""ЗАПРЕТ ОКНА: позы 99 (PL300–PL399) · палитры 91 · кинетики 0 · носители 179 · BURN 19.
Ответ батча (после вето): мейки — 21 first-use PL403–PL423; EXP — 9 first-use PL424–PL432;
ОС — 3 first-use PL433–PL435 (poses.json 1.8.1); срез PL400–PL402 остаётся в ledger.
Палитры — 21 свободных из реестра (мейки) + 3 ОС-палитры из реестра вне окна
(P69_EMBER_FROST / P06_OBSIDIAN_GOLD / P115_HONEY_TRAP) + 9 новых (P171–P179).
Кинетики — 33 новых K-FF (K216–K248, живы K219–K248) + 3 ОС-мида K249–251
(pools.json 1.2.1); носители — только вне окна и вне burn.""")

# 10) cast-справка
rep(u"""Чужих IP-референсов в T5-18 нет (мейки — авторские архетипы вывернутого быта; EXP —
тредовые кандидаты R53–R61). M03 триггеров нет. Тема живёт правилами, не чужими именами.""",
u"""Чужих IP-референсов в T5-18 нет (мейки — авторские архетипы вывернутого быта; EXP —
тредовые кандидаты R53–R61; ОС — канон-ростер автора, Nix/Ash/Ana verbatim). M03
триггеров нет. Тема живёт правилами, не чужими именами.""")

# 11) EXP-метки тем сняты (вето)
for old, new in [
 (u"Кандидат «Ая» — Tsundere Paradise #1: зайчиха с ушами-предателями.", u"Кандидат «Ая» — зайчиха с ушами-предателями."),
 (u"Кандидат «Юки» — Tsundere Paradise #2: ледяная принцесса с хвостом-предателем.", u"Кандидат «Юки» — ледяная принцесса с хвостом-предателем."),
 (u"Кандидат «Игла» — Tsundere Paradise #3: колючка с иглами-детектором настроения.", u"Кандидат «Игла» — колючка с иглами-детектором настроения."),
 (u"Кандидат «Витра» — Notre-Dame notte di natale #1: витражная девочка соборной ночи.", u"Кандидат «Витра» — витражная девочка соборной ночи."),
 (u"Кандидат «Мирра» — Notre-Dame notte di natale #2: ладанная дева с волосами-дымом.", u"Кандидат «Мирра» — ладанная дева с волосами-дымом."),
 (u"Кандидат «Нотта» — Notre-Dame notte di natale #3: сова колокольни, ночная месса.", u"Кандидат «Нотта» — сова колокольни, ночная месса."),
 (u"Кандидат «Муська» — Dirty Bitch #1: мусорная принцесса помоечного двора.", u"Кандидат «Муська» — мусорная принцесса помоечного двора."),
 (u"Кандидат «Фифа» — Dirty Bitch #2: скунсиха на парфюмерном передозе.", u"Кандидат «Фифа» — скунсиха на парфюмерном передозе."),
 (u"Кандидат «Хитра» — Dirty Bitch #3: хорь-схемщица с соседской стороны плетня.", u"Кандидат «Хитра» — хорь-схемщица с соседской стороны плетня."),
]:
    rep(old, new)

# 12) слот-сплайс: старые мейны P01–P03 -> три ОС-слота
i0 = s.index(u"P01 — teapot-sunrise-pour-up")
i1 = s.index(u"P04 — clock-backward-alarm")

OS_SLOTS = u"""P01 — gifts-not-for-you-parade (EXQUISITE · Nix · human · R+ · PL433 · P69_EMBER_FROST)
Channel: r-geometry (live; разворот плеча на оглядке честно тянет ворот — подарок-вещь держит заявку, объятие с коробкой не поза)
Combo: D6-01 OC PORTRAIT SAFE · Package: ε (GEOMETRY)
THESIS: «ПАРАД ПОДАРКОВ С БИРКАМИ ВНИЗ ЛИЦОМ: КАЖДЫЙ — „НЕ ДЛЯ ТЕБЯ“, И НИКТО ЭТОГО НЕ ПРИЗНАЁТ».
Гэг-стек (4 фишки OC): 1) все бирки подарков перевёрнуты именами вниз — надписи, которые
никто не признает (В17: без текста в кадре); 2) ключ-кулон прижат ладонью в момент
оглядки — ключ она не вручит; 3) белые ресницы припорошены инеем оранжереи — мороз
района, не её; 4) розовый шрам на шее — единственная тёплая линия выше ключиц, и та
старая.
Spine: PL433 Not-For-You Glance-Back (threshold_limen) · K-FF mid_gift_glance · CAM01 ·
D3·A01 · LEAD the turned-back glance · ember-frost register · closer image-close
Race: — (human; канон VERBATIM specs/oc-canon.json, Nix, STEEL).
Canon: short platinum french bob, wispy bangs, tapered nape; sharp ice-blue eyes with
white eyelashes (pale, almost invisible against platinum hair); mediterranean bronze skin
(not olive); slim athletic body, FAM-C (B2-B3): small breasts, softly mounded, never
flat; sharp angular features; thin steel chain necklace with a single small key pendant
at the throat; thin pink scar across the front of the neck (old wound, healed) — VERBATIM.
Gar: CL-OU-07 (open padded jacket, collar wide, slipping off one shoulder) + CL-BT-05
(soft cotton lounge shorts) · HS: канон (short platinum french bob, wispy bangs)
Stack: CR-W35 + CR-B01 + CR-S03 + CR-D40
POS:
Masterpiece, best quality, upper body frontal at eye level, 1girl, solo, original character, the hugged gift pressing a soft warm line through thin knit, frost-pale-blue ice-shadow palette with ember-deep-orange-dying warmth, platinum french bob hair with wispy bangs, ice-blue eyes with white lashes, mediterranean bronze skin, slim athletic build with small breasts, thin steel chain with a single small key pendant at the throat, thin pink scar across the neck's front, mid_gift_glance
open padded jacket worn over a thin ivory knit, collar fallen wide off one shoulder, the hugged gift-box pushing the lapel aside so the knit prints honest where it pulls taut — the held gift is the claim, hugged like something she would deny
she turns away down the frost-white greenhouse path stacked with wrapped boxes, face snapped back over her shoulder mid-step, lips pressed in a stubborn pout, the whole parade of gifts behind her wearing their tags face-down — names nobody will admit, her palm pinning the key pendant flat
Ember frost palette, frost-pale-blue and ice-shadow, ember-deep-orange-dying warmth pooling at the floor vents, pale-gold-ember accent at the ribbon; her colors are heat kept strictly indoors and handed out in denials.
stylized 2D anime face turned back mid-pout, anime eyes (ice-blue, level-and-lying), small nose, small mouth pressed stubborn, the frost light holding the bob's blunt line.
NEG:
young girl, immature body, oversized head, loli, shota, signature, watermark, artist name, logo, 1boy, candle, lamp, photorealistic, 3d face, realistic facial structure, bad anatomy,
extra fingers, bad hands, washed-out, faded colors, low contrast, flat colors, muddy colors, dull, overexposed, underexposed, pastel colors,
muted colors, gray palette, pale colors, desaturated, white haze, milky fog, soft focus, hazy, black eyelashes, dark eyelashes, brown eyelashes, thick eyelashes, olive skin, large breasts, long hair, tags readable, text, caption, gifts stacked neatly, shoulder covered

P02 — midnight-vigil-reliquary (EXQUISITE · Ash · human · R+ · PL434 · P06_OBSIDIAN_GOLD)
Channel: contact-physics (live; вес открытого реликвария на обеих ладонях — контакт как молитва, ткань отвечает на наклон)
Combo: D6-01 OC PORTRAIT SAFE · Package: κ (CONTACT)
THESIS: «НОЧНАЯ МЕССА ДЛЯ ПУСТОГО СОБОРА: РЕЛИКВАРИЙ ОТКРЫТ, СВЕЧИ НЕ ЗАЖЖЕНЫ — СВЕТ ИДЁТ ОТ СНЕЖНОГО НЕБА ЧЕРЕЗ РОЗУ ОКНА».
Гэг-стек (4 фишки OC): 1) реликварий открыт на обеих ладонях — крышка держится на её
пальцах изнутри; 2) вуаль закрывает всё, кроме рта — рот шепчет полуночную обетную
молитву; 3) венец из тёрна над вуалью ловит одну золотую точку от золочёных тессер;
4) нити обетов на обоих запястьях — ни одна не развязана.
Spine: PL434 Reliquary Box Vigil (threshold_limen) · K-FF mid_vow_openbox · CAM02 ·
D3·A02 · LEAD the snow-light rose · rite register · closer image-close
Race: — (human; канон VERBATIM; вуаль = канон, veil-закон 2026-09-23 «всё кроме рта»).
Canon: very long ivory-white hair (not platinum, not silver — ivory); thin white veil
covering the whole face except the bare mouth; snow-pale skin; slender body, FAM-C (B2):
modest neat breasts, compact chest; simple white cotton monastic garments; thin crown of
thorns over the veil (optional per-prompt). Глаза под вуалью НЕ описываются и НЕ рисуются
(eye_detail: permission-gated) — VERBATIM.
Gar: — (simple white cotton monastic garments, канон; рукава закатаны до локтя)
Stack: CR-W16 + CR-B12 + CR-E08 + CR-D29
POS:
Masterpiece, best quality, upper body three-quarter at eye level, 1girl, solo, original character, the open reliquary box held chest-high pressing the cotton to her shape, obsidian-deep gold-leaf ceremonial palette, very long ivory-white hair, thin white veil covering the whole face except the bare mouth, snow-pale skin, slender body with modest neat breasts, thin crown of dark thorns over the veil, mid_vow_openbox
simple white monastic cotton with sleeves rolled to the elbow, the weave printing a cold-honest line where the night chill finds it, thin crown of dark thorns over the veil, vow-threads wound at both wrists — the open reliquary is the claim, carried chest-high like a chalice she will not set down
the cathedral keeps its midnight mass for no congregation: snow-light sieves through the great west window and lays a pale rose across the nave floor, gold tesserae catch it into warm sparks along the pillars, and she stands at the altar rail with the lid balanced open on her fingers, bare lips moving through the vow
Obsidian-gold palette, obsidian-black and gold-leaf ceremonial depth, ivory accent on the veil's fold, deep-brown warmth where the tesserae answer; her colors are the hour the bells keep without ringing.
stylized 2D anime face under the veil with bare lips mid-vow, veil-covered face with bare mouth, small mouth shaping the vow, the glass light holding the veil's line.
NEG:
young girl, immature body, oversized head, loli, shota, signature, watermark, artist name, logo, 1boy, candle, lamp, photorealistic, 3d face, realistic facial structure, bad anatomy,
extra fingers, bad hands, washed-out, faded colors, low contrast, flat colors, muddy colors, dull, overexposed, underexposed, pastel colors,
muted colors, gray palette, pale colors, desaturated, white haze, milky fog, soft focus, hazy, visible eyes, bare eyes, eyes visible through veil, eye color visible, eye shape visible through fabric, parted veil, lifted veil, transparent veil, sheer veil, open face, exposed face, visible nose, visible cheeks, platinum hair, silver hair, colorful garments, closed box, empty hands

P03 — honey-parlor-spoon-lick (EXQUISITE · Ana · human · R+ · PL435 · P115_HONEY_TRAP)
Channel: honey-sheen-delivery (live; медовая нить от пальцев к губам тянет заявку сама — сатин липнет по геометрии тела честно)
Combo: D6-03 OC THEME-OFF · Package: ε (GEOMETRY)
THESIS: «ИМПЕРАТРИЦА ЕСТ МЁД ПРЯМО ПАЛЬЦАМИ И НИКОМУ НИЧЕГО НЕ ПРЕДЛАГАЕТ: ДРЯНЬ В ТОМ, ЧТО СЛАДОСТЬ ОНА ДЕРЖИТ ДЛЯ СЕБЯ».
Гэг-стек: 1) медовая нить тянется от поднятых пальцев к губам и не рвётся — тянет себя
сама; 2) соты в чаше уже с вмятинами её пальцев; 3) крылья-стрекоза раскрыты по спинке
кушетки — золочёный веер, ни одна прожилка не дрожит; 4) хвост-финна лежит витком на
подлокотнике, кончик отбивает ленивый такт.
Spine: PL435 Chaise Honey Drape (erotic_presentation_v2) · K-FF mid_honey_string · CAM06 ·
D5·A03 · LEAD the honey-string · trap-gold register · closer image-close
Race: — (канон VERBATIM specs/oc-canon.json, Ana, GOLD; наряд по PH = P115_HONEY_TRAP).
Canon: long golden-blonde hair with cyan-teal under-streaks, worn loose past the chest;
large glossy obsidian-black eyes; fair warm ivory-gold skin with gold-leaf metallic sheen;
tall full-figured body, wide hips, FAM-A (B5-B7): full chest, heavy breasts; teal-blue
ridged swept-back horns, semi-crystal translucence; cyan translucent fin-fans at the head;
large translucent cyan-teal wings at the shoulder blades — iridescent, dragonfly-honest,
NEVER vestigial or small; thick finned dragon tail, teal-gold, fin-edged — VERBATIM.
Gar: CL-DR-01 (beeswax-gold silk slip dress, наряд по PH) + CL-AC-02 (bow ribbon choker) ·
HS: канон (loose golden-blonde past the chest, fin-fans at the head)
Stack: CR-W35 + CR-B26 + CR-S03 + CR-D40
POS:
Masterpiece, best quality, full-length from a low three-quarter angle, 1girl, solo, original character, the honey-string stretched from raised fingers to her lips, honey-amber-deep beeswax-gold palette, long golden-blonde hair with cyan-teal under-streaks worn loose past the chest, large glossy obsidian-black eyes, fair warm ivory-gold skin with gold-leaf sheen, tall full-figured build with wide hips and full heavy breasts, teal ridged swept-back horns, cyan translucent fin-fans at the head, mid_honey_string
beeswax-gold silk slip dress riding up one thigh where she sprawls, hem honest at the hip, straps fallen wide, the neckline's slack printing the breast's weight — the honey-string is the claim, drawn slow from her own fingers
teal ridged swept-back horns catching the wax light, cyan translucent fin-fans at the head, large translucent cyan-teal wings fanned open over the chaise backrest, thick finned dragon tail curled along the armrest with the tip tapping a lazy beat; she eats the honeycomb straight from the bowl with bare fingers and licks the drip off her own knuckle, offering nobody anything
Honey trap palette, honey-amber-deep and beeswax-gold over beekeeper-khaki-warm shade, sting-gold-bright accent along the honey-string, comb-ivory-wax at the bowl's rim; her colors are the sweet she keeps for herself.
stylized 2D anime face tipped down into her own palm, anime eyes (obsidian-black, half-lidded ownership), small nose, small mouth closing over the fingertip, the warm wax light holding the jaw line.
NEG:
young girl, immature body, oversized head, loli, shota, signature, watermark, artist name, logo, 1boy, candle, lamp, photorealistic, 3d face, realistic facial structure, bad anatomy,
extra fingers, bad hands, washed-out, faded colors, low contrast, flat colors, muddy colors, dull, overexposed, underexposed, pastel colors,
muted colors, gray palette, pale colors, desaturated, white haze, milky fog, soft focus, hazy, black hair, brown hair, short hair, dark skin, grey skin, green skin, no wings, small wings, vestigial wings, wings folded, no tail, small tail, antler horns, branching horns, broken honey-string, offered spoon, second figure

"""
s = s[:i0] + OS_SLOTS + s[i1:]

io.open(path, 'w', encoding='utf-8').write(s)
print("batch edits OK, slots spliced")
