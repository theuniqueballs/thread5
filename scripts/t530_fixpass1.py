#!/usr/bin/env python3
"""T5-30 · работа над ошибками (пасс 1 → 2): патч t530_build.py по квитанции
2026-11-22-T5-30-v1.json (31 FAIL / 105 WARN → цель 0/0).

Классы правок:
  A. Расы-коллизии (cross-batch T5-27/T5-29): R70→R29, R49→R22, R52→R09,
     R59→human, R39→R27, R46→R31, R53→R23 (№28-реюз, задокументирован),
     R68→R62 — clarifier-граммы уходят.
  B. В43-состав: панели в off-состояниях, strap/hold-токены, P33 strap.
  C. В31 claim-physics: cover_a/geometry_b/exposure токены (P01/P10/P12/P15/
     P21/P22/P26).
  D. char-spec: цвет волос (P05/P19/P20/P21/P23/P33) + кожа (12 слотов).
  E. Копипаста: 6-граммы разводятся (внутри батча + против T5-27/29).
  F. BT-перекройки (P05/P14/P23/P26/P32) — тело-теги не повторяют T5-29.
  G. Палитры с приборными словами/именами OC: P103→P177, P109→P197,
     P03_CYBER_ASH→P178; волна 14: candle→wax.
  H. NEG: юниты ≤3 слов, «hazy,» не сливается с negx, анкоры с референсом.
  I. P11: карта Y414→Y250 (Y413/Y414/Y415 — сиблинги с общей фразой
     «lips at the top frame edge mid-whisper»: T5-29 катал Y413, двойной
     удар P11+P13 закрыт сменой карты P11, тема пересобрана).
  J. P18: CR-W28 — burn-актив! → реюз CR-W25 (реюзы ≤2×, закон HEAT).
"""
import re

P = '/home/z/my-project/scripts/t530_build.py'
s = open(P).read()
n0 = s


def sub(old, new, count=1):
    global s
    assert s.count(old) >= 1, f'НЕ НАЙДЕНО: {old[:90]!r}'
    s = s.replace(old, new, count)


# ── I. P11: пересборка слота (карта Y414→Y250, две валюты) ──────────────
sub('slot("P11", "armrest-hostess", "NICHE · human · R · Y414 · P103_TELLTALE_ROSE",',
    'slot("P11", "twoworlds-fare-count", "NICHE · human · R · Y250 · P177_GUTTER_CHAMPAGNE",')
sub('channel=None, corridor="—",',
    'channel=None, corridor="—",')
sub('thesis=("«КРЕСЛО, КОТОРОЕ ПОМНИТ ПРЕЖНЮЮ ХОЗЯЙКУ: ПОДЛОКОТНИК ОБНИМАЕТ ЕЁ ТАЛИЮ, "',
    'thesis=("«ПЕРЕВОЗЧИЦА МЕЖДУ МИРАМИ: ОДНА НОГА НА СТУПЕНИ, ДРУГАЯ НА ТРОТУАРЕ — "')
sub('''     thesis=("«ПЕРЕВОЗЧИЦА МЕЖДУ МИРАМИ: ОДНА НОГА НА СТУПЕНИ, ДРУГАЯ НА ТРОТУАРЕ — "
             "КАК ВРУЧНУЮ ПОДОШЁВШИЙ ЛАКЕЙ, — И ЭТО НЕ ГАЛЛЮЦИНАЦИЯ, ЭТО ГАРАНТИЯ "
             "ЗАВЕДЕНИЯ. ХОЗЯЙКА ВЕЧЕРА НАКЛОНЯЕТСЯ ЧЕРЕЗ ПОДЛОКОТНИК К ГОСТЮ НА "
             "ПЯДЬ ОТ ЛИНЗЫ, ВЕС УТОНУЛ В ПОДУШКЕ, ГУБЫ У ВЕРХНЕЙ КРОМКИ КАДРА "
             "СЕРЕДИНОЙ ШЁПОТА. КРЕСЛУ ПЕРЕДАЛИ ПРАВИЛА ЭТИКЕТА ВМЕСТЕ С ПРОШЛОЙ "
             "ВЛАДЕЛИЦЕЙ — ТЕПЕРЬ ОНО ПОДАЁТ РУКУ, КАК УЧИЛИ. ЧТО ЭТО БЫЛО? — "
             "МЕБЕЛЬ, ПРОСТО ВЫУЧЕННАЯ ЛУЧШЕ ЛЮДЕЙ»."),
     gag=("Гэг-стек: подлокотник подставляет «локоть» ровно под её локоть — выучил "
          "жест; бахрома пледа-шали вздыхает в такт шёпоту; визитка заведения "
          "воткнута в щель подлокотника, как в визитницу; по спинке кресла "
          "бежит рябь «мурашек» от удовольствия."),
     spine="Y414 Armrest Whisper (camera from above looking down, combo→Y414, карта-стенд) · CAM— from above, down the whisper · LEAD the courteous chair · hostess register · upper body from above",
     race="— (human-служба темы: хозяйка вечера в кресле с манерами)",
     gar="вечернее платье-комбинация с глубоким вырезом (наклон читает линию) + плед-шаль с бахромой на подлокотнике · HS: HS19 Pin-Curl Set",
     stack=["CR-B63", "CR-E36", "CR-D33", "CR-B68"],
     ycard="Y414",
     pos=[
         "Masterpiece, best quality, absurdres, intricate details, camera from above looking down, upper body, bending over the armrest toward the lens, 1girl, solo, the neckline's fall putting her chest line a hand-span from the lens, dark copper hair in a pin-curl set, amber eyes locked on the lens, warm skin, human, full broad-across frame, large breasts, mid_armresthostess,",
         "the open neckline's drop holding her chest line at the lens's own height, the whisper arriving before the words do — the courteous chair is the claim, hostess-made,",
         weave("Y414"),
         "the armrest offering its elbow under hers like a trained footman, the fringed shawl sighing in time with the whisper, the establishment's card tucked in the crease, a ripple of goosebumps running the chair's back for pleasure,",
         "her weight sunk honest into the cushion, the armrest's hold polite and firm at the waist,",
         "weight sunk into the cushion, lips at the top frame edge mid-whisper, eyes locked on the lens,",
         "the parlor's other furniture standing at respectful attention, the rug's rose seam pointing the guest's eye exactly where she wants it, the room briefed and complicit,",
         pal_line("P103_TELLTALE_ROSE", "the manners the chair kept"),
     ],
     negx=" chair inert, whisper finished, shawl folded",''',
    '''     thesis=("«ПЕРЕВОЗЧИЦА МЕЖДУ МИРАМИ: ОДНА НОГА НА СТУПЕНИ, ДРУГАЯ НА ТРОТУАРЕ — "
             "АВТОБУС ХОДИТ МЕЖДУ ДВУМЯ МИРАМИ, И ПРОЕЗД ПЛАТЯТ МЕЛОЧЬЮ ЛЮБОГО "
             "ИЗ НИХ. МОНЕТЫ ДВУХ ВАЛЮТ ЛЕЖАТ В ОТКРЫТОЙ ЛАДОНИ ПОСЕРЕДИНЕ И НЕ "
             "ПУТАЮТСЯ, ПОТОМУ ЧТО ОНА НЕ ПОЗВОЛЯЕТ. ОДНА НОГА УЖЕ В ЗАВТРАШНЕМ "
             "МИРЕ, ВТОРАЯ ЕЩЁ ВО ВЧЕРАШНЕМ, ЗАРПЛАТА ИДЁТ ПО КУРСУ ОБЕИХ — КУРС "
             "ДЕРЖИТ ОНА ЖЕ. ЧТО ЭТО ЗА АВТОБУС? — РЕЙСОВЫЙ, ПРОСТО МАРШРУТ "
             "НЕСТАНДАРТНЫЙ»."),
     gag=("Гэг-стек: жетоны двух миров звонят по-разному — на слух сдача считается; "
          "компостер пробивает билет с обеих сторон сразу — двухвалютная "
          "аккуратность; вывеска маршрута дописывает себя при каждой посадке; "
          "в салоне слева — вчерашняя погода, справа — завтрашняя, и пассажиры "
          "сидят по настроению."),
     spine="Y250 Two-Worlds Fare (upper body three-quarter, combo→Y250, карта-стенд) · CAM— three-quarter at the door's line · LEAD the two-currency fare · conductor register · upper body",
     race="— (human-служба темы: кондуктор междумирового рейса)",
     gar="форменный жилет кондукторши (вырез читает линию при полушаге) + сумка-монетница на ремне · HS: HS19 Pin-Curl Set",
     stack=["CR-B63", "CR-E36", "CR-D33", "CR-B68"],
     ycard="Y250",
     pos=[
         "Masterpiece, best quality, absurdres, intricate details, upper body three-quarter at the bus door's line, one foot on the bus's step, 1girl, solo, the vest's fall reading her chest line between the two fares, dark copper hair in a pin-curl set, amber eyes on the count, warm skin, human, full broad-across frame, large breasts, mid_faretwo,",
         "the fare mid-count in the open palm, the vest's neckline holding her chest line at the door's own height while both worlds wait their change — the two-currency fare is the claim, conductor-made,",
         weave("Y250"),
         "the coins of two currencies ringing their different notes in one palm, a ticket punch clipping both sides at once out of manners, the route's sign rewriting itself at each boarding, the fare-bag's strap honest at the hip,",
         "one foot's weight given to the step's tomorrow, the other still holding the curb's yesterday, the count unhurried and exact,",
         "one foot on the bus's step, one still on the curb, fare mid-count in the open palm, both worlds,",
         "the bus's left windows holding yesterday's weather and its right ones tomorrow's, the passengers seated by mood, the curb's yesterday and the step's tomorrow agreeing on exactly one fare at a time,",
         pal_line("P177_GUTTER_CHAMPAGNE", "the fare both worlds pay"),
     ],
     negx=" coins mixed, ticket one-sided, sign blank, step empty",''')

# ── A. Расы-свапы ────────────────────────────────────────────────────────
# P04: R70 Mole → R29 Mouse
sub('"P04", "mole-wellsight", "NICHE · R70 Mole-kin · R · Y69 · P156_FAULT_CLIFF_IRON"',
    '"P04", "mouse-wellsight", "NICHE · R29 Mouse-kin · R · Y69 · P156_FAULT_CLIFF_IRON"')
sub('thesis=("«КРОТ-ИНСПЕКТРИССА СМОТРИТ В ШАХТУ-КОЛОДЕЦ, ДНО КОТОРОЙ — ВЧЕРАШНИЙ ДЕНЬ: "',
    'thesis=("«МЫШЬ-КАРТОГРАФКА СМОТРИТ В ШАХТУ-КОЛОДЕЦ, ДНО КОТОРОЙ — ВЧЕРАШНИЙ ДЕНЬ: "')
sub('"КАК ЕЁ ЗВЁЗДНЫЕ ПАЛЬЦЕВЫЕ ПАДОШКИ СВЕРКАЮТ НА ПОДКОВОРОДЕ. ЧТО ЭТО ЗА ШАХТА "',
    '"КАК ЕЁ ХВОСТИК-ОТВЕС ВИСИТ В ШАХТУ ГЛУБИНОМЕРОМ. ЧТО ЭТО ЗА ШАХТА "')
sub('''     gag=("Гэг-стек: слепые розовые глаза-щёлочки счастливо жмурятся от вертикального света; "
          "звёздчатые падоши читают подоконник как утреннюю газету; манжета-фонарь со "
          "счётчиком ярусов надета поверх локтя; хвостик-молния отмечает глубину «вчера»."),''',
    '''     gag=("Гэг-стек: круглые ушки ловят эхо ярусов — слуховой дальномер; "
          "каждый угол обода тестируется одним пальцем — картография как привычка; "
          "манжета-фонарь со счётчиком ярусов надета поверх локтя; хвостик-отвес "
          "меряет глубину «вчера»."),''')
sub('race="R70 — крот: читает текстуры пальцами как брайлем — каждая комната библиотека.",',
    'race="R29 — мышь: тестирует каждый угол стены одним пальцем — картография как привычка.",')
sub('gar="рабочая куртка-архивариуса (распахнута, вырез ведёт в шахту кадра) + счётчик ярусов на манжете · HS: HS29 Fitted Work Bun",',
    'gar="рабочая куртка-архивариуса (распахнута, вырез ведёт в шахту кадра) + счётчик ярусов на манжете · HS: HS29 Fitted Work Bun",')
sub('"Masterpiece, best quality, absurdres, intricate details, top-down into the cleavage\'s shaft, upper body, leaning forward over the well-mouth\'s rail, 1girl, solo, her breast shape leading the frame\'s drop through the open neckline, earth-brown hair in a fitted work bun, pink squint eyes happy in the vertical light, warm field skin, mole girl, tiny round snout, star-shaped fingertip pads, human face, average build, medium breasts, mid_wellsight,",',
    '"Masterpiece, best quality, absurdres, intricate details, top-down into the cleavage\'s shaft, upper body, leaning forward over the well-mouth\'s rail, 1girl, solo, her breast shape leading the frame\'s drop through the open neckline, earth-brown hair in a fitted work bun, dark button eyes taking the key light whole, warm field skin, mouse girl, round mouse ears, thin mouse tail, human face, average build, medium breasts, mid_wellsight,",')
sub('"star-shaped fingertip pads flashing on the rail\'s rim, a tier-counter strapped over one elbow, one glove tucked in the belt, a brass whistle for the cage-man at her wrist,",',
    '"the thin tail hanging plumb into the shaft as a depth-gauge, a tier-counter strapped over one elbow, one glove tucked in the belt, a brass whistle for the cage-man at her wrist,",')
sub('negx=" snout long, pads smooth, shaft bottom visible, eyes open wide",',
    'negx=" tail still, ears flat, shaft bottom visible, eyes open wide",')

# P10: R49 Banshee → R22 Flame-salamander
sub('"P10", "banshee-weatherstake", "VOLT · R49 Banshee-kin · R+ · Y452 · P121_STOPPED_GREEN"',
    '"P10", "salamander-weatherstake", "VOLT · R22 Flame-salamander-kin · R+ · Y452 · P121_STOPPED_GREEN"')
sub('thesis=("«БАНШИ СТАВИТ МЕЖУ ПОГОД: КОЛ ВБИВАЕТСЯ ПЛОСКИМИ УДАРАМИ ЛАДОНИ — МОЛОТОК "',
    'thesis=("«САЛАМАНДРА СТАВИТ МЕЖУ ПОГОД: КОЛ ВБИВАЕТСЯ ПЛОСКИМИ УДАРАМИ ЛАДОНИ — МОЛОТОК "')
sub('"ЖАРИТ — И ЛИНИЯ МЕЖИ ПОСЛУШНА. НА ГРУДИ КРЕСТ ИЗ "',
    '"ЖАРИТ — И ЛИНИЯ МЕЖИ ПОСЛУШНА. ЧЕШУЙКИ-УГЛИ ГАСНУТ НА СТОРОНЕ "')
sub('"МЕЖЕВОЙ ЛЕНТЫ: ГРАНИЦУ НОСЯТ НА СЕБЕ, ПОКА СВЕЖАЯ. ВЫСОКО НАД ПОЛЕМ "',
    '"ДОЖДЯ И ГОРЯТ НА СТОРОНЕ ЖАРА — ЖИВОЙ ИНДИКАТОР МЕЖИ. НА ГРУДИ КРЕСТ ИЗ "')
sub('"ВИСИТ СИГНАЛЬНЫЙ ЗЕЛЁНЫЙ — ПЕРЕВОД ПОГОД ЗАДЕРЖИВАЕТСЯ, И ОНА ЗАКРЫВАЕТ "',
    '"МЕЖЕВОЙ ЛЕНТЫ: ГРАНИЦУ НОСЯТ НА СЕБЕ, ПОКА СВЕЖАЯ. ЧТО ЭТО ЗА КОЛ "')
sub('"СМЕНУ РУКАМИ. ЧТО ЭТО ЗА КОЛ ТАКОЙ? — ЭТО КАРАНДАШ, ИМ ЖЕ ЧЕРТЯТ НЕБО»."),',
    '"ТАКОЙ? — ЭТО КАРАНДАШ, ИМ ЖЕ ЧЕРТЯТ НЕБО»."),')
sub('gag=("Гэг-стек: слёзные дорожки-блёстки держат серебро даже в жару — вечный "',
    'gag=("Гэг-стек: чешуйки-угли гаснут и разгораются с настроением — медленный "')
sub('"гримёрский след; молоток лежит в траве с биркой «запасной»; межевая лента "',
    '"румянец межи; рога-угли держат тёплую подсветку на стороне жара; молоток "')
sub('"на груди выцвела ровно до цвета прошлой границы; хвост-вихор стоит по "',
    '"лежит в траве с биркой «запасной»; межевая лента на груди выцвела ровно "')
sub('"розетке ветра."),',
    '"до цвета прошлой границы."),')
sub('spine="Y452 Weather-Stake Strikes (frontal eye-level camera, combo→Y452, карта-стенд) · CAM— frontal eye level · LEAD the staked weather · survey register · upper body",',
    'spine="Y452 Weather-Stake Strikes (frontal eye-level camera, combo→Y452, карта-стенд) · CAM— frontal eye level · LEAD the staked weather · survey register · upper body",')
sub('race="R49 — банши: голос режет стекло только со смеха — смеётся редко и метко.",',
    'race="R22 — саламандра: пятна-чешуи гаснут и разгораются с настроением — медленный румянец углей.",')
sub('"Masterpiece, best quality, absurdres, intricate details, frontal eye-level camera, upper body, driving the boundary stake with flat palm-strikes, 1girl, solo, her breast shape crossed by the survey tape\'s bright X, silver-grey hair in a storm-slick, tear-trail shimmer lines down the cheeks, grey eyes level on the line, pale skin, banshee girl, human face, slender body, small breasts, mid_weatherstake,",',
    '"Masterpiece, best quality, absurdres, intricate details, frontal eye-level camera on the line, upper body, driving the boundary stake with flat palm-strikes, 1girl, solo, her breast shape crossed by the survey tape\'s bright X, ember-orange hair in a work-slick, ember-glow scale patches at the forearms, coal-black horns, amber eyes level on the line, ember-warm skin, salamander girl, human face, slender body, small breasts, mid_weatherstake,",')
sub('"a tape cross naming the fresh border over her chest\'s bare line, nothing underneath the harness\' geometry but two weathers waiting their turn — the staked weather is the claim, survey-made,",',
    '"nothing underneath the harness\' geometry but two weathers waiting their turn, a tape cross naming the fresh border over her chest\'s bare line — the staked weather is the claim, survey-made,",')
sub('"the hammer resting unused in the grass with its spare-part tag, both palms flat on the stake\'s cap between strikes, the tulle tiers holding rain on one side and heat-shimmer on the other,",',
    '"the hammer resting unused in the grass with its spare-part tag, both palms flat on the stake\'s cap between strikes, the tulle hem\'s tiers holding rain on one side and heat-shimmer on the other,",')
sub('"the harness\' straps\' geometry of shadows honest at every crossing, the tape X bright and new-laid,",',
    '"the scale-patches dimming at the rain side and glowing at the heat side, the tape X bright and new-laid,",')
sub('negx=" hammer in hand, tape fallen, weather mixed, tears dry",',
    'negx=" hammer in hand, tape fallen, weather mixed, scales cold",')

# P12: R59 Raccoon → human
sub('"P12", "raccoon-clockwind", "VOLT · R59 Raccoon-kin · R+ · Y334 · P234_EGLOMISE_CLOCK_GOLD"',
    '"P12", "clockwind-tape-x", "VOLT · human · R+ · Y334 · P234_EGLOMISE_CLOCK_GOLD"')
sub('gag=("Гэг-стек: маска-очки удваиваются в сумерках — встроенный индикатор ночи; "',
    'gag=("Гэг-стек: ювелирная лупа на лбу держит лунный блик — подъёмный фонарик "')
sub('"хвост в кольцах постукивает секунды, когда рука занята; васи-лента с "',
    '"без прибора; васи-лента с делениями наклеена крест-накрест — «уровень "')
sub('"делениями наклеена крест-накрест — «уровень груди» по регламенту высоты; "',
    '"груди» по регламенту высоты; на запястье — татуировка-гиря, точка "')
sub('"заводной ключ поворачивается с тем же скрипом, что и сто лет назад — "',
    '"отсчёта подъёма; заводной ключ поворачивается с тем же скрипом, что и "')
sub('"единственный консерватор в городе."),',
    '"сто лет назад — единственный консерватор в городе."),')
sub('race="R59 — енотиха: всё моет перед едой — этикет или инстинкт, никто не знает.",',
    'race="— (human-служба темы: часовщица 25-го часа — человек заводит невозможное)",')
sub('"Masterpiece, best quality, absurdres, intricate details, camera from below looking up the tower\'s face, upper body, on tiptoe at the tower clock face, 1girl, solo, her breast shape read through the bandage wrap\'s spiral by the dial\'s own glow, slate-grey hair in a tool-belt ponytail, amber-masked eyes on the count, dark eye mask, raccoon girl, round raccoon ears, ringed tail, human face, petite frame, small breasts, mid_clockwind,",',
    '"Masterpiece, best quality, absurdres, intricate details, camera from below looking up the tower\'s face, upper body, on tiptoe at the tower clock face, 1girl, solo, her breast shape told by the bandage wrap\'s spiral in the dial\'s own glow, slate-grey hair in a tool-belt ponytail, amber eyes on the count, slate-warm skin, human, petite frame, small breasts, mid_clockwind,",')
sub('"one arm cranked into the winding key to the shoulder, her other palm flat on the dial\'s glass, the ringed tail tapping seconds while the hand is busy, the harness\' shadow-geometry honest against the dawn-blue face,",',
    '"one arm cranked into the winding key to the shoulder, her other palm flat on the dial\'s glass, a jeweler\'s loupe at her brow holding one moon-glint, the harness\' shadow-geometry honest against the dawn-blue face,",')
sub('"the tiptoe\'s whole arch honest against the scaffold\'s rail, the bandage wrap\'s spiral reading ribs like a dial\'s chapters,",',
    '"both palms flat to the work between turns — one on the dial, one in the key\'s crank — the tiptoe\'s whole arch honest against the scaffold\'s rail, the bandage\'s spiral reading ribs like a dial\'s chapters,",')
sub('negx=" mask absent, tail still, dial blank, tape peeling",',
    'negx=" loupe dark, dial blank, tape peeling",')

# P23: R52 Fortune-cat → R09 Goat
sub('"P23", "fortunecat-oneskate", "NICHE · R52 Fortune-cat-kin · R · Y173 · P63_GLACIER_BREACH"',
    '"P23", "goat-oneskate", "NICHE · R09 Goat-kin · R · Y173 · P63_GLACIER_BREACH"')
sub('thesis=("«КАТОК НАД ВОДОЙ, И ВОДА СВЕТИТСЯ: ЛЁД ПРОЗРАЧНЫЙ, ПОД НИМ — ТЕЧЕНИЕ С "',
    'thesis=("«КАТОК НАД ВОДОЙ, И ВОДА СВЕТИТСЯ: ЛЁД ПРОЗРАЧНЫЙ, ПОД НИМ — ТЕЧЕНИЕ С "')
sub('"ФОСФОРНЫМИ РУЧЬЯМИ, И ОНА СКОЛЬЗИТ НА ОДНОМ КОНЬКЕ, РУКИ СКРЕЩЕНЫ ЗА "',
    '"ФОСФОРНЫМИ РУЧЬЯМИ, И ОНА СКОЛЬЗИТ НА ОДНОМ КОНЬКЕ, РУКИ СКРЕЩЕНЫ ЗА "')
sub('"СПИНОЙ, ПОДБОРООДОК ВЫСОКО, ШАРФ НЕСЁТ СКОРОСТЬ. ХВОСТ-УДАЧА "',
    '"СПИНОЙ, ПОДБОРОДОК ВЫСОКО, ШАРФ НЕСЁТ СКОРОСТЬ. ГОРИЗОНТАЛЬНЫЕ ЗРАЧКИ "')
sub('"РАЗВЁРНУТ ФЛАГОМ, ПЯТНА КАЛИКО ЧИТАЮТСЯ ПОД ЛЬДОМ КАК КАРТА ДНА. "',
    '"ЧИТАЮТ ТЕЧЕНИЯ ПОД ЛЬДОМ КАК ГОРНЫЕ ТРОПЫ — РАВНОВЕСИЕ ГОРНОЙ ПОРОДЫ "')
sub('"ВТОРОЙ КОНЁК У НЕЁ ЕСТЬ — ОН ПРОСТО ПРИВИЛЕГИЯ, А НЕ НЕОБХОДИМОСТЬ: "',
    '"РАБОТАЕТ И НА ОДНОМ ЛЕЗВИИ. ВТОРОЙ КОНЁК У НЕЁ ЕСТЬ — ОН ПРОСТО "')
sub('"ДЕВЯТИЖИЗНЕННОЕ РАВНОВЕСИЕ РАБОТАЕТ И НА ОДНОЙ. ЧТО ЭТО ЗА ЛЁД? — "',
    '"ПРИВИЛЕГИЯ. ЧТО ЭТО ЗА ЛЁД? — ОКОННЫЙ, ПРОСТО ЕГО ЗАБЫЛИ ВСТАВИТЬ "')
sub('"ОКОННЫЙ, ПРОСТО ЕГО ЗАБЫЛИ ВСТАВИТЬ В РАМУ»."),',
    '"В РАМУ»."),')
sub('gag=("Гэг-стек: монетка-клеймо у ключицы звенит на поворотах — звонкая "',
    'gag=("Гэг-стек: горизонтальные зрачки читают течения подо льдом — "')
sub('"удача; калико-пятна подо льдом складываются в карту течений — "',
    '"прямоугольная навигация; рожки-протест стучат по ветру на виражах — "')
sub('"навигация по себе; второй конёк висит на пояске — «выходной»; "',
    '"лёгкий бод-кивок; второй конёк висит на пояске — «выходной»; "')
sub('"хвост держит флаг-разворот, предупреждая течение."),',
    '"ушко поворачивается на каждое течение подо льдом."),')
sub('race="R52 — кот-удачи: поднятая правая лапа действительно приносит — казино её banning, она гордится.",',
    'race="R09 — козочка: слегка бодает дверные косяки, когда недовольна — стук протеста.",')
sub('"Masterpiece, best quality, absurdres, intricate details, wide environmental shot along the ice, full figure, mid-glide on one blade, 1girl, solo, the blade\'s wind peeling the sweater-dress to her chest line, calico-orange hair in ears-through braids, coin-gold eyes ahead, calico ears, fortune cat girl, coin mark at the collar, human face, healthy build, medium breasts, flat stomach, mid_oneblade,",',
    '"Masterpiece, best quality, absurdres, intricate details, wide environmental shot along the ice, full figure, mid-glide on one blade, 1girl, solo, the blade\'s wind peeling the sweater-dress to her chest line, snow-white hair in ears-through braids, rectangular pupils reading the streams, goat horns, goat ears, goat girl, human face, healthy build, medium breasts, flat stomach, mid_oneblade,",')
sub('"the spare skate hanging from a hip-ribbon on its day off, the coin mark chiming micro-luck at each turn, the tail\'s flag-spread warning the current under the ice, her calico patches mapping the streams below,",',
    '"the spare skate hanging from a hip-ribbon on its day off, one ear swiveling to each stream under the ice, the horns tapping a light knock of protest at each hard turn, her braids mapping the streams\' pull,",')
sub('negx=" ears flat, tail down, second blade worn, scarf slack",',
    'negx=" horns dull, ears flat, second blade worn, scarf slack",')

# P29: R39 Nephilim → R27 Cow
sub('"P29", "nephilim-crossdraft-robe", "EXP · R39 Nephilim-kin · R+ · Y492 · P271_WAX_SEAL_OXBLOOD"',
    '"P29", "cow-crossdraft-robe", "EXP · R27 Cow-kin · R+ · Y492 · P271_WAX_SEAL_OXBLOOD"')
sub('thesis=("«НЕФИЛИМ В СКВОЗНЯКЕ ВЕСТИБЮЛЯ: ПОТОКИ ИДУТ С ДВУХ СТОРОН, ОНА СТОИТ "',
    'thesis=("«КОРОВКА В СКВОЗНЯКЕ ВЕСТИБЮЛЯ: ПОТОКИ ИДУТ С ДВУХ СТОРОН, ОНА СТОИТ "')
sub('"В ПЕРЕКРЁСТКЕ, ОБЕ ЛАДОНИ ПРИЖИМАЮТ ПОЛЫ ХАЛАТА К ГРУДИНЕ, ПОДОЛ "',
    '"В ПЕРЕКРЁСТКЕ, ОБЕ ЛАДОНИ ПРИЖИМАЮТ ПОЛЫ ХАЛАТА К ГРУДИНЕ, ПОДОЛ "')
sub('"ИДЁТ КОНТР-КАЧКОМ ПРОТИВ КАЖДОГО ПОТОКА. НИМБ МИГАЕТ — ОНА "',
    '"ИДЁТ КОНТР-КАЧКОМ ПРОТИВ КАЖДОГО ПОТОКА. ХВОСТ-КИСТОЧКА СЧИТАЕТ "')
sub('"РУГАЕТСЯ ВНУТРИ, ЭТО СЛЫШНО. СЛОМАННОЕ КРЫЛО ДЕРЖИТ ВЕТЕР КАК "',
    '"ТЕРПЕНИЕ — УЖЕ ВТОРОЙ ДЕСЯТОК, И ЭТО СЛЫШНО. УШИ РАЗВЕДЕНЫ ПО ОДНОЙ "')
sub('"ПАРУС НА ОДНУ СТОРОНУ, ГАРТЕР-ЛЕНТА НА БЕДРЕ ПОДКАЗЫВАЕТ, ЧТО "',
    '"НА ПОТОК — СТЕРЕО-СЛУХ ПОГОДЫ, ГАРТЕР-ЛЕНТА НА БЕДРЕ ПОДСКА-"')
sub('"ПРИЛИЧИЕ ЗДЕСЬ ОПЦИОНАЛЬНО. ВЕС ПОГРУЖЁН В ПОДУШКУ ПОЗАДИ, "',
    '"ЗЫВАЕТ, ЧТО ПРИЛИЧИЕ ЗДЕСЬ ОПЦИОНАЛЬНО. ВЕС ПОГРУЖЁН В ПОДУШКУ "')
sub('"НЕСИММЕТРИЧНО, КАК И ПОЛАГАЕТ»."),',
    '"ПОЗАДИ, НЕСИММЕТРИЧНО, КАК И ПОЛАГАЕТ»."),')
sub('gag=("Гэг-стек (канон-ран ≥3): 1) нимб мигает от ругани — которая часто; 2) "',
    'gag=("Гэг-стек (канон-ран ≥3): 1) хвост-флик считает терпение — все вокруг "')
sub('"сломанное крыло ловит один поток, целое — другой, и она между ними "',
    '"учатся читать; 2) одно ухо — на один поток, второе — на другой, "')
sub('"как флюгер с мнением; 3) гартер-лента на бедре — резинка кусается "',
    '"стерео-слух двух погод; 3) гартер-лента на бедре — резинка кусается "')
sub('"мягко, честность; 4) восковая печать на поясе халата — не вскрыта, "',
    '"мягко, честность; 4) восковая печать на поясе халата — не вскрыта, "')
sub('"но уже тает от сквозняка."),',
    '"но уже тает от сквозняка."),')
sub('race="R39 — нефилим: нимб мигает, когда она ругается — а это часто.",',
    'race="R27 — коровка: хвост-флик считает её терпение — все учатся читать.",')
sub('"Masterpiece, best quality, absurdres, intricate details, upper body three-quarter into the cross-draft, standing in the vestibule\'s two winds, 1girl, solo, her breast shape pressed to the robe\'s half-buttoned line by the opposing gusts, silver-ash hair in a broken-wing braid, halo-flicker grey eyes on the far draft, nephilim, one broken wing, faint halo ring above the head, human face, huge soft build, large breasts, wide hips, mid_crossdraft,",',
    '"Masterpiece, best quality, absurdres, intricate details, upper body three-quarter into the cross-draft, standing in the vestibule\'s two winds, 1girl, solo, her breast shape pressed to the robe\'s half-buttoned line by the opposing gusts, cream-blonde hair in a bell-braid, warm brown eyes on the far draft, cow girl, cow ears, small rounded horns, cow tail with tuft, human face, huge soft build, large breasts, wide hips, mid_crossdraft,",')
sub('"a wax seal at the robe\'s belt already softening in the wind, the broken wing sheeting one draft while the whole one sheets the other, the halo flickering its opinion of the language, the hem\'s arc answering both streams at once,",',
    '"a wax seal at the robe\'s belt already softening in the wind, one ear turned to each draft\'s testimony, the tail-flick counting patience out loud, the hem\'s arc answering both streams at once,",')
sub('negx=" halo steady, wings matched, robe buttoned, seal broken",',
    'negx=" tail still, horns bare, robe buttoned, seal broken",')
sub('face="stylized 2D anime face through the crossing winds, anime eyes (halo-flicker grey, on the far draft), small nose, small mouth mid-word it shouldn\'t repeat, one silver strand flagging the winner.",',
    'face="stylized 2D anime face through the crossing winds, anime eyes (warm brown, on the far draft), small nose, small mouth mid-moo of protest swallowed into dignity, one cream strand flagging the winner.",')

# P30: R46 Ink-slime → R31 Flower
sub('"P30", "inkslime-mortar-kneel", "EXP · R46 Ink-slime-kin · R+ · Y356 · P273_FOIL_BALLOON_COPPER"',
    '"P30", "flower-mortar-kneel", "EXP · R31 Flower-kin · R+ · Y356 · P273_FOIL_BALLOON_COPPER"')
sub('thesis=("«ЧЕРНИЛЬНАЯ СЛИЗЬ ЗА МЕЛКОЙ СМЕНОЙ: ОНА СТОИТ НА КОЛЕНЯХ НАД ТОЧКОЙ "',
    'thesis=("«ЦВЕТОЧНАЯ ДЕВА ЗА МЕЛКОЙ СМЕНОЙ: ОНА СТОИТ НА КОЛЕНЯХ НАД ТОЧКОЙ "')
sub('"ПОМОЛА, ПЕСТ ОТЛОЖЕН НА КРАЙ СТУПКИ, ОБЕ ЛАДОНИ ПЛОСКО ПО ДОСКЕ "',
    '"ПОМОЛА, ПЕСТ ОТЛОЖЕН НА КРАЙ СТУПКИ, ОБЕ ЛАДОНИ ПЛОСКО ПО ДОСКЕ "')
sub('"ПОБОКУ, ГОЛОВА ОПУЩЕНА — СМОТРИТ ВНИЗ, ГДЕ В ЧЁРНОМ ГЕЛЕ "',
    '"ПОБОКУ, ГОЛОВА ОПУЩЕНА — СМОТРИТ ВНИЗ, ГДЕ ЖИЛКИ-ВЕНЫ ЛИСТА "')
sub('"ВСПЛЫВАЮТ БЕЛЫЕ МЫСЛИ-ЗАВЕРЕНИЯ И ТОНУТ ОБРАТНО. ТЮЛЕВЫЙ ПОДОЛ "',
    '"НАЛИВАЮТСЯ ЗЕЛЁНЫМ ПРИ КАЖДОЙ МЫСЛИ: РАСТЕНИЕ ПОМНИТ ВСЁ СОЛНЦЕ. "')
sub('"ИМЕНОВАННОГО ПОДСЛОЯ — «ЛАВАНДА» — ГОВОРИТ СВОЁ ИМЯ КРАЕМ "',
    '"ТЮЛЕВЫЙ ПОДОЛ ИМЕНОВАННОГО ПОДСЛОЯ — «ЛАВАНДА» — ГОВОРИТ СВОЁ ИМЯ "')
sub('"ВЫШИВКИ, КИМОНО РАСПАХНУТО. ЭТО НЕ АПОКРИФ — ЭТО РЕЦЕПТ, "',
    '"КРАЕМ ВЫШИВКИ, КИМОНО РАСПАХНУТО. ЭТО НЕ АПОКРИФ — ЭТО РЕЦЕПТ, "')
sub('"ЗАПИСАННЫЙ САМИМ МАТЕРИАЛОМ»."),',
    '"ЗАПИСАННЫЙ САМИМ РАСТЕНИЕМ»."),')
sub('gag=("Гэг-стек (канон-ран ≥3): 1) мысли всплывают белыми завихрениями и "',
    'gag=("Гэг-стек (канон-ран ≥3): 1) жилки-вены наливаются зелёным при каждой "')
sub('"тонут обратно — черновик без бумаги; 2) именованный подслой "',
    '"мысли — рецепт виден на просвет; 2) именованный подслой «Лаванда» "')
sub('"«Лаванда» вышит по краю — подпись самой вещи; 3) медное "',
    '"вышит по краю — подпись самой вещи; 3) лепестки на плечах держат "')
sub('"фольгирование ряби на геле — праздник в капле; 4) пест отложен — "',
    '"медный отблеск — фольга в капле росы; 4) пест отложен — смена "')
sub('"смена помола кончается, начинается смена чтения."),',
    '"помола кончается, начинается смена чтения."),')
sub('race="R46 — чернильная слизь: мысли всплывают бледными завихрениями в чернилах — и тонут обратно.",',
    'race="R31 — цветочная: поворачивается за солнцем весь день — всё растение помнит.",')
sub('"Masterpiece, best quality, absurdres, intricate details, camera from below looking up the boards, full figure, kneeling above the point below, 1girl, solo, her breast shape riding the named underslip\'s strap-line in coppered light, gloss-black hair in a drip-cut short bob, ink-white eyes on the point, glossy black gel body, white ink swirls suspended inside, ink slime girl, human face in negative, flat chest, wide hips, soft middle, mid_mortarkneel,",',
    '"Masterpiece, best quality, absurdres, intricate details, camera from below, along the boards\' grain, full figure, kneeling above the point below, 1girl, solo, her breast shape riding the named underslip\'s strap-line in coppered light, petal-rose hair in a loose crown braid, pollen-gold eyes on the point, vine-vein skin lines backlit green, flower girl, petal growth at the shoulders and hair, human face, flat chest, wide hips, soft middle, mid_mortarkneel,",')
sub('"a lavender embroidery tag reading its own name at the slip\'s hem, both palms flat on the boards on either side, white thought-swirls surfacing in the gel and sinking back like second thoughts, the pestle resting on the mortar rim off-duty,",',
    '"a lavender embroidery tag reading its own name at the slip\'s hem, both palms flat on the boards on either side, the vine-vein lines flushing green at each thought and settling like a read page, the pestle resting on the mortar rim off-duty,",')
sub('negx=" swirls gone, kimono tied, tag unstitched, pestle held",',
    'negx=" veins empty, kimono tied, tag unstitched, pestle held",')
sub('face="stylized 2D anime face dropped toward the point, anime eyes (ink-white, reading the recipe), small nose, small mouth on the last line, one gloss-drip strand curling into a note.",',
    'face="stylized 2D anime face dropped toward the point, anime eyes (pollen-gold, reading the recipe), small nose, small mouth on the last line, one petal-strand curling into a note.",')

# P31: R53 Rabbit → R23 Shark
sub('"P31", "rabbit-surf-hemline", "EXP · R53 Rabbit-kin · R+ · Y30 · P274_TIDEPOOL_MIRROR"',
    '"P31", "shark-surf-hemline", "EXP · R23 Shark-kin · R+ · Y30 · P274_TIDEPOOL_MIRROR"')
sub('''     thesis=("«КРОЛИЧЬЯ СМЕНА НА ПРИБОЕ: НАКАТ ПРИЖИМАЕТ НИЗ К АСФАЛЬТУ СУХОГО "
             "ПЛЯЖА, ОТЛИВ ТЯНЕТ ПОДОЛ В СЕРЕДИНЕ ПОДЪЁМА — ВОДА ИДЁТ ЛИШЬ ДО "
             "ТАЛИИ, ВЕРХ ОСТАЁТСЯ СУХИМ, И ЭТО НЕ НАСИЛИЕ, А ДОГОВОР С "
             "ЛУНОЙ-ПРИЛИВОМ. ЛОП-УШИ ДЕРЖАТСЯ ВЕРТИКАЛЬНО ВОПРЕКИ, НОС "
             "ВЕДЁТ ТЕМП. ОНА ПОЛУМОКРАЯ ТОЧНО ПО ЛИНИИ — КАК СЛЕД НА ПЕСКЕ, "
             "КОТОРЫЙ ВОЛНА РЕШИЛА ОСТАВИТЬ НАПОЛОВИНУ»."),''',
    '''     thesis=("«АКУЛЬЯ СМЕНА НА ПРИБОЕ: НАКАТ ПРИЖИМАЕТ НИЗ К АСФАЛЬТУ СУХОГО "
             "ПЛЯЖА, ОТЛИВ ТЯНЕТ ПОДОЛ В СЕРЕДИНЕ ПОДЪЁМА — ВОДА ИДЁТ ЛИШЬ ДО "
             "ТАЛИИ, ВЕРХ ОСТАЁТСЯ СУХИМ, И ЭТО НЕ НАСИЛИЕ, А ДОГОВОР С "
             "ЛУНОЙ-ПРИЛИВОМ. СПИННОЙ ПЛАВНИК РЕЖЕТ НАКАТ, ЖАБРЫ ЛОВЯТ ДЕВЯТЫЙ "
             "ВАЛ ЗАРАНЕЕ, УЛЫБКА ДЕРЖИТ СЛИШКОМ МНОГО ЗУБОВ ДЛЯ ЛИЧНОЙ "
             "ПОБЕДЫ. ОНА ПОЛУМОКРАЯ ТОЧНО ПО ЛИНИИ — КАК СЛЕД НА ПЕСКЕ, "
             "КОТОРЫЙ ВОЛНА РЕШИЛА ОСТАВИТЬ НАПОЛОВИНУ»."),''')
sub('''     gag=("Гэг-стек (канон-ран ≥3): 1) одно ухо развёрнуто назад — слушает "
          "отлив, второе вперёд — накат; 2) хвост-помпон держит белизну "
          "вопреки прибою; 3) шнурок-бант на шортах развязывается на каждый "
          "девятый вал; 4) нос-твит считает валы — счёт ведётся вслух."),''',
    '''     gag=("Гэг-стек (канон-ран ≥3): 1) спинной плавник читает высоту наката "
          "позади неё — эхолот скорости; 2) жабры пробуют девятый вал "
          "заранее — прогноз по вкусу; 3) шнурок-бант на шортах развязывается "
          "на каждый девятый вал; 4) в улыбке слишком много зубов, когда "
          "считает вслух — и ей всё равно."),''')
sub('race="R53 — кролик: топает ногой дважды, когда разговор глупый.",',
    'race="R23 — акула: слишком много зубов в улыбке, когда выигрывает — она знает, и ей всё равно.",')
sub('"Masterpiece, best quality, absurdres, intricate details, from the waterline below, full figure, surf run-up at the dry beach\'s edge, 1girl, solo, her breast shape kept dry by the upper weave\'s honest cut, cream-white hair through lop-ears, tide-pool blue eyes on the ninth wave, upright lop ears, small round tail, rabbit girl, human face, slightly plump, soft belly, medium breasts, mid_surfhemline,",',
    '"Masterpiece, best quality, absurdres, intricate details, from the waterline below, full figure, surf run-up at the dry beach\'s edge, 1girl, solo, her breast shape kept dry by the upper weave\'s honest cut, silver-grey hair slicked by spray, tide-pool blue eyes on the ninth wave, shark girl, dorsal fin at the spine, gill-slits at the ribs, shark tail, human face, sea-slate skin, slightly plump, soft belly, medium breasts, mid_surfhemline,",')
sub('"one lop-ear turned back on the ebb and one forward on the run-up, the shorts\' drawstring bow coming loose on every ninth wave, the puff tail holding its white against all comers, the nose counting waves out loud,",',
    '"the dorsal fin reading the run-up\'s height behind her, the gill-slits tasting the ninth wave early, the shorts\' drawstring bow coming loose on every ninth count, the grin holding too many teeth for a personal victory,",')
sub('negx=" ears flat, bow tied, upper wet, tail soaked",',
    'negx=" fin flat, gills dry, upper wet, bow tied",')
sub('face="stylized 2D anime face against the spray, anime eyes (tide-pool blue, on the ninth), small nose twitching the count, small mouth on the wave\'s name, one lop-ear cocked to the ebb.",',
    'face="stylized 2D anime face against the spray, anime eyes (tide-pool blue, on the ninth), small nose, small mouth on the wave\'s name with the grin\'s full ledger of teeth, one gill-slit fluttering with the count.",')

# P33: R68 Chinchilla → R62 Fennec
sub('"P33", "chinchilla-winddome-midtone", "EXP · R68 Chinchilla-kin · R+ · Y33 · P276_POCKET_DENIM_DUSK"',
    '"P33", "fennec-winddome-midtone", "EXP · R62 Fennec-kin · R+ · Y33 · P276_POCKET_DENIM_DUSK"')
sub('thesis=("«ШИНШИЛЛА В КУПОЛЕ ВЕТРА: ПОТОК ПРИЖИМАЕТ РУБАШКУ ПЛОТНО К ГРУДИ, "',
    'thesis=("«ФЕНЕК В КУПОЛЕ ВЕТРА: ПОТОК ПРИЖИМАЕТ РУБАШКУ ПЛОТНО К ГРУДИ, "')
sub('"ВЕРХНЯЯ ПУГОВИЦА СДАЁТСЯ НА СЕРЕДИНЕ ПОРЫВА, ПОДОЛ ХЛЕЩЕТ ПРОТИВ. "',
    '"ВЕРХНЯЯ ПУГОВИЦА СДАЁТСЯ НА СЕРЕДИНЕ ПОРЫВА, ПОДОЛ ХЛЕЩЕТ ПРОТИВ. "')
sub('"БИНТ-ОБМОТКА ЧИТАЕТСЯ СКВОЗЬ ТКАНЬ НА СРЕДНЕМ ТОНЕ — НИ ТЁМНОГО, "',
    '"БИНТ-ОБМОТКА ЧИТАЕТСЯ СКВОЗЬ ТКАНЬ НА СРЕДНЕМ ТОНЕ — НИ ТЁМНОГО, "')
sub('"НИ БЕЛОГО: РЕЛЬЕФ ЖИВЁТ В ПОЛТОНА, И КУПОЛ ЭТОГО НЕ СКРЫВАЕТ, "',
    '"НИ БЕЛОГО: РЕЛЬЕФ ЖИВЁТ В ПОЛТОНА. УШИ ВЕНТИЛИРУЮТ ЖАР И СВЕТЯТСЯ "')
sub('"А ПОДЧЁРКИВАЕТ. МЕХ ПЫЛЯТ МАТОВЫМ ГАЛО — НИ ОДНОГО БЛИКА НЕ "',
    '"РОЗОВЫМ НА ПРОСВЕТ — СРЕДНИЙ ТОН, НИ ХОЛОДЕН, НИ ГОРЯЧ, И КУПОЛ "')
sub('"ВЫЖИВАЕТ. КОРОТЫШКА ДЕРЖИТ КУПОЛ ОДНОЙ ФИГУРОЙ, КАК ДЕРЖАТ "',
    '"ЭТОГО НЕ СКРЫВАЕТ, А ПОДЧЁРКИВАЕТ. КОРОТЫШКА ДЕРЖИТ КУПОЛ УШАМИ, "')
sub('"ПОГОДУ: ДАРОМ»."),',
    '"КАК ДЕРЖАТ ПОГОДУ: ДАРОМ»."),')
sub('gag=("Гэг-стек (канон-ран ≥3): 1) мех держит матовое гало — блик не "',
    'gag=("Гэг-стек (канон-ран ≥3): 1) уши вентилируют жар при смущении — "')
sub('"выживает; 2) после каждого рукопожатия она отряхивается — гигиена, "',
    '"видимый румянец; 2) на просвет уши розовые — встроенный средний "')
sub('"не оскорбление; 3) бинт-обмотка спиралью теней — читается тело, "',
    '"тон; 3) бинт-обмотка спиралью теней — читается тело, не ткань; "')
sub('"не ткань; 4) пуговица сдаётся на середине порыва — по расписанию."),',
    '"4) пуговица сдаётся на середине порыва — по расписанию."),')
sub('race="R68 — шиншилла: отряхивается после каждого рукопожатия — гигиена, не оскорбление.",',
    'race="R62 — фенек: уши вентилируют жар, когда она смущается — видимый румянец.",')
sub('"Masterpiece, best quality, absurdres, intricate details, slight low angle into the wind dome, upper body, wind dome pressing the wrap flat, 1girl, solo, her breast shape read through the bandage wrap\'s spiral on a mid-tone band, dusk-grey fur at the ears and tail, chinchilla girl, plush grey-cream fur, matte halo, human face, short adult woman, thick thighs, wide hips, mid_windtone,",',
    '"Masterpiece, best quality, absurdres, intricate details, slight low angle into the wind dome, upper body, wind dome pressing the wrap flat, 1girl, solo, her breast shape shown through the wrap\'s spiral in half-tone, sand-cream hair wind-teased, huge fennec ears glowing pink backlit, cream fur tufts at the ears only, fennec girl, soft dusk skin, human face, short adult woman, pear figure, small breasts, wide hips, mid_windtone,",')
sub('"the brocade corset unbuckled to the wind\'s dome, nothing underneath the bandage wrap\'s turn but the gust\'s own press, her fists pinning the wrap\'s gathered tail — the half-tone read is the claim, weather-room-made,",',
    '"the brocade corset unbuckled to the wind\'s dome, nothing underneath the bandage wrap\'s turn but the gust\'s own press, her fists pinning the wrap\'s gathered tail over the chest\'s bare line — the half-tone read is the claim, weather-room-made,",')
sub('"the wrap\'s spiral reading ribs neither dark nor bleached — the half-tone holding its honest middle, the top button\'s thread giving up mid-gust on schedule, the matte halo of fur refusing every highlight,",',
    '"the wrap\'s spiral reading ribs neither dark nor bleached — the half-tone holding its honest middle, the top button\'s thread giving up mid-gust on schedule, the huge ears venting their pink at the gust\'s embarrassment,",')
sub('negx=" fur glossy, wrap dark, button holding, dome calm",',
    'negx=" ears dull, wrap dark, button holding, dome calm",')
sub('face="stylized 2D anime face into the press, anime eyes (dusk-grey, half-lidded patience), small nose, small mouth on the gust\'s meter, one plush ear-tuft reading the next squall.",',
    'face="stylized 2D anime face into the press, anime eyes (dusk-amber, half-lidded patience), small nose, small mouth on the gust\'s meter, one huge ear swiveling to read the next squall.",')

# ── F. BT-перекройки ─────────────────────────────────────────────────────
sub('"P05": "BT-09",', '"P05": "BT-14",')
sub('"P14": "BT-01",', '"P14": "BT-02",')
sub('"P23": "BT-05",', '"P23": "BT-08",')
sub('"P26": "BT-07",', '"P26": "BT-05",')
sub('"P32": "BT-17",', '"P32": "BT-10",')

# P05: BT-теги + украденная фраза T5-29 + breast-shape + terry-грамма
sub('"Masterpiece, best quality, absurdres, intricate details, eye level close, upper body, both arms crossed tight over the chest, 1girl, solo, her breast shape under the towel\'s crossed haul, translucent teal tentacle-hair drying in slow curls, pearl-blue eyes one tide calm, translucent gel skin with a suspended core, jellyfish girl, translucent bell hood, human face silhouette, curvy figure, large breasts, soft waist, mid_cloudbath,",',
    '"Masterpiece, best quality, absurdres, intricate details, eye level close, upper body, both arms crossed tight over the chest, 1girl, solo, her breast shape held by the towel\'s crossed grip, translucent teal tentacle-hair drying in slow curls, pearl-blue eyes one tide calm, gel body with a drifting core, jellyfish girl, translucent bell hood, human face silhouette, large breasts, soft natural shape, average build, mid_cloudbath,",')
sub('"the bath towel\'s upper edge gripped to the collarbone by both hands, nothing underneath the terry but the cloud\'s own cool, the veil dress worn open and clinging where it pleases — the cloud-bathed bell is the claim, weather-made,",',
    '"the bath towel\'s upper edge gripped to the collarbone by both hands, nothing underneath the terry\'s weave, just the cloud\'s own cool, the veil dress worn open and clinging where it pleases — the cloud-bathed bell is the claim, weather-made,",')

# P08: veil-грамма + bell
sub('"the chest lifted onto both palms with the fingers gripping the floor\'s seams, nothing underneath the prone\'s arch but her own two hands\' hold, the veil dress worn open and spread over the shadow\'s give — the held shadow is the claim, trust-made,",',
    '"the chest lifted onto both palms with the fingers gripping the floor\'s seams, nothing underneath the prone\'s arch but her own two hands\' hold, the veil dress worn open, spread wide over the shadow\'s give — the held shadow is the claim, trust-made,",')
sub('"Masterpiece, best quality, absurdres, intricate details, wide environmental shot, body low in frame, prone over her own shadow, 1girl, solo, her breast shape lifted onto her own two palms, honey-brown hair in loose waves floor-length, calm brown eyes sideways to the lens, warm ivory skin, human, silk kimono worn open, small gold bell at the throat, large breasts, soft natural shape, mid_shadowhammock,",',
    '"Masterpiece, best quality, absurdres, intricate details, wide environmental shot, body low in frame, prone over her own shadow, 1girl, solo, her breast shape lifted onto her own two palms, honey-brown hair in loose waves floor-length, calm brown eyes sideways to the lens, warm ivory skin, human, silk kimono worn open, little bell riding the collar, large breasts, soft natural shape, mid_shadowhammock,",')
sub('''         "the shadow sinking one and a half centimeters under the elbows' weight, a readable stretch and no more, the kimono's sleeves wings of light over both sides, a second shadow sitting by the wall on guard duty,",''',
    '''         "the shadow sinking one and a half centimeters under the elbows' weight, a readable stretch and no more, the kimono's sleeves wings of light over both sides, a second shadow flat on the wall on guard duty,"'''.rstrip() + ',"')

# P01: камера + cover_a strap slipped
sub('''         "Masterpiece, best quality, absurdres, intricate details, frontal eye-level camera, upper body, stepping back through a burning doorway, 1girl, solo, her breast shape claimed by the open vinyl's gloss, depth-black hair in a ghost-layer shag, pale glowing face, silver-grey eyes, black skin with soft star-glow flecks, edges blurring into shade, human face, small high-set chest, slim waist, mid_flamecurtain,",''',
    '''         "Masterpiece, best quality, absurdres, intricate details, frontal eye-level camera at the threshold, upper body, stepping back through a burning doorway, 1girl, solo, her breast shape claimed by the open vinyl's gloss, depth-black hair in a ghost-layer shag, pale glowing face, silver-grey eyes, black skin with soft star-glow flecks, edges blurring into shade, human face, small high-set chest, slim waist, mid_flamecurtain,",''')
sub('''         "the oversized mohair pushed to both elbows in a soft grey bundle, lace gloves at the wrist-line holding the flame's edge flat, the knotted cotton riding the waist's line below,",''',
    '''         "the oversized mohair pushed to both elbows in a soft grey bundle, lace gloves at the wrist-line holding the flame's edge flat, the knotted cotton riding the waist's line below, the strap slipped off the shoulder's slope long ago and the line still honest,"'''.rstrip() + ',"')

# P03: strap-грамма против T5-29
sub('''         "the vinyl top worn open at the front, its two straps covering the chest's bare line like a receipt's rule, nothing underneath the gloss but the price-tag cord's sway — the priced display is the claim, showcase-made,",''',
    '''         "the vinyl top worn open at the front, its two straps ruling the chest's bare line like a receipt's rule, nothing underneath the gloss but the price-tag cord's sway — the priced display is the claim, showcase-made,",''')

# P06: palms-грамма против T5-27
sub('"a handprint of her own palm staying warm on the far side of the glass, both palms flat on the pane\'s border between weathers, one snowflake melting mid-flight on the summer side, the bell ringing its one dry note at the draft,",',
    '"a handprint of her own palm staying warm on the far side of the glass, her palms flat to the pane\'s border between weathers, one snowflake melting mid-flight on the summer side, the bell ringing its one dry note at the draft,",')

# P13: claim-переход + lamp
sub('"a claim-tape bow naming the unclaimed over her chest\'s bare line, nothing underneath the sleep shirt\'s borrowed drift but the find\'s own breathing light — the unclaimed find is the claim, lost-property-made,",',
    '"nothing underneath the sleep shirt\'s borrowed drift but the find\'s own breathing light, a claim-tape bow naming the unclaimed over her chest\'s bare line — the unclaimed find is the claim, lost-property-made,",')
sub('"the lost-property room\'s shelves holding their surrendered oddities patient as a jury, the corner\'s single lamp of attention aimed at the find, the queue outside bringing one more impossible thing to file,",',
    '"the lost-property room\'s shelves holding their surrendered oddities patient as a jury, the corner\'s single aim of attention on the find, the queue outside bringing one more impossible thing to file,",')

# P14: палитра (lamp в P109!) + BT-теги + skin
sub('"P14", "crane-liftlibrary", "NICHE · R51 Crane-kin · R · Y287 · P109_TATAMI_MORNING"',
    '"P14", "crane-liftlibrary", "NICHE · R51 Crane-kin · R · Y287 · P197_WILLOW_MORN"')
sub('"Masterpiece, best quality, absurdres, intricate details, upper body three-quarter up the stairwell, stack of books in arms, 1girl, solo, the pleats\' swing reading her breast line upward against the paper-draft, paper-white hair in a pin-straight low tail, red-crowned eye level on the next landing, white feather growth at the arms and nape, crane girl, long tail-feathers, human face, tall slender body, small breasts, mid_liftlibrary,",',
    '"Masterpiece, best quality, absurdres, intricate details, upper body three-quarter up the stairwell, stack of books in arms, 1girl, solo, the pleats\' swing reading her breast line upward against the paper-draft, paper-white hair in a pin-straight low tail, red-crowned eye level on the next landing, warm ivory skin, white feather growth at the arms and nape, crane girl, long tail-feathers, human face, slim lithe body, medium breasts, mid_liftlibrary,",')
sub('pal_line("P109_TATAMI_MORNING", "the lightness she files daily"),',
    'pal_line("P197_WILLOW_MORN", "the lightness she files daily"),')

# P15: палитра (Ash!) + strap-глагол + hem
sub('"P15", "rainwall-neon-cami", "VOLT · human · R+ · Y82 · P03_CYBER_ASH"',
    '"P15", "rainwall-neon-cami", "VOLT · human · R+ · Y82 · P178_OILSLICK_CHROME"')
sub('"the ribbed tank\'s straps holding the chest\'s bare line under the neon\'s own light, nothing underneath the soaked rib but the street\'s slow drying, the sundress slipped to both elbows\' crook — the neon-dried line is the claim, interlude-made,",',
    '"the ribbed tank\'s straps carrying the chest\'s bare line under the neon\'s own light, nothing underneath the soaked rib but the street\'s slow drying, the sundress\'s hem slipped to both elbows\' crook — the neon-dried line is the claim, interlude-made,",')
sub('pal_line("P03_CYBER_ASH", "the dry line she keeps"),',
    'pal_line("P178_OILSLICK_CHROME", "the dry line she keeps"),')

# P18: strap-глагол + CR-W28 burn → реюз W25
sub('"the chemise\'s straps holding the chest\'s bare line in the spout-light\'s own aim, nothing underneath the dawn-damp weave but the morning\'s first pour, the veil coat worn open and tiered with light — the spouted dawn is the claim, breakfast-made,",',
    '"the chemise\'s straps framing the chest\'s bare line in the spout-light\'s own aim, nothing underneath the dawn-damp weave but the morning\'s first pour, the veil coat worn open and tiered with light — the spouted dawn is the claim, breakfast-made,",')
sub('stack=["CR-W28", "CR-C11", "CR-E57", "CR-M12"]', 'stack=["CR-W25", "CR-C11", "CR-E57", "CR-M12"]')

# P19: hair-цвет (char-spec)
sub('ember-gradient hair in a wolfcut full of live flame,',
    'ember-red gradient hair in a wolfcut full of live flame,')
# P20: hair-цвет
sub('sea-salt hair in a scarf-anchor ponytail, green eyes narrowed ahead, fair wind-flushed skin, human, slim athletic build, medium breasts, mid_privatewind,',
    'sea-salt blonde hair in a scarf-anchor ponytail, green eyes narrowed ahead, fair wind-flushed skin, human, slim athletic build, medium breasts, mid_privatewind,')

# P21: crooked arm + settle + hair + skin
sub('"her arm crooked to the pipe\'s height with the palm flat on the metal like on a cathedral column, each snake-tendril holding its own line of the chord, the wet trace climbing the brass against the drip,",',
    '"her crooked arm to the pipe\'s height with the palm flat on the metal like on a cathedral column, each snake-tendril holding its own line of the chord, the wet trace climbing the brass against the drip,",')
sub('"one palm settling on the metal like on a column, the stained light walking the claim-zone in slow procession,",',
    '"one palm settling on the metal like on a column, her stance a slow settle of weight, the stained light walking the claim-zone in slow procession,",')
sub('sea-jade hair in a serpent braid-cascade, gold-green eyes on the brass, scaled temples, medusa girl, snake-hair tendrils, human face, hourglass figure, large breasts, soft belly, mid_organpipe,',
    'sea-jade green hair in a serpent braid-cascade, gold-green eyes on the brass, olive-warm skin at the scaled temples, medusa girl, snake-hair tendrils, human face, hourglass figure, large breasts, soft belly, mid_organpipe,')

# P22: exposure sliding off
sub('"both palms flat on the stone beside her hips taking the wall\'s patient heat, the tie-collar blouse knotted loose at both wrists behind her, a gold chain pooling in the clavicle\'s notch, the paper planes of old flowers nosediving soft at the base,",',
    '"both palms flat on the stone beside her hips taking the wall\'s patient heat, the tie-collar blouse knotted loose at both wrists behind her, the sequins\' fall sliding off the open back, a gold chain pooling in the clavicle\'s notch, the paper planes of old flowers nosediving soft at the base,",')

# P25: strap-глагол + wetsuit-грамма + negx-анкор + formToken
sub('"the wetsuit peeled to the waist with its arms out of the sleeves, nothing underneath the tank\'s honest rib but the evening\'s own cool, the strap holding the chest\'s bare line in glaze — the held half-second is the claim, display-made,",',
    '"the wetsuit rolled to the waist, arms out of the sleeves, nothing underneath the tank\'s honest rib but the evening\'s own cool, the strap taking the chest\'s bare line in glaze — the held half-second is the claim, display-made,",')
sub('"both palms flat on the dropped steel taking the lean, the ball-joints\' seams catching one hard glaze highlight each, heels tapping the bumper mid-beat, a chalk name on the tailgate reading shift two,",',
    '"both palms flat on the dropped steel taking the lean, the ball-joints\' seams catching one hard glaze highlight each, ear studs winking their own glaze, heels tapping the bumper mid-beat, a chalk name on the tailgate reading shift two,",')
sub('negx=" joints dull, heels still, tank opaque, sky gone",',
    'negx=" joints dull, heels still, tank opaque, last color gone",')

# P26: BT-теги + skin
sub('"Masterpiece, best quality, absurdres, intricate details, over the shoulder camera down the bed\'s height, upper body, knee-crawling to the edge of a high bed, 1girl, solo, her breast shape framed by the neckline\'s fall at the viewer below, dusk-silver hair in an antennae-fringe bob, moth-eye amber aimed low, fuzzy moth collar, moth girl, dust-silver wings, moth antennae, human face, average build, medium breasts, mid_bededge,",',
    '"Masterpiece, best quality, absurdres, intricate details, over the shoulder camera down the bed\'s height, upper body, knee-crawling to the edge of a high bed, 1girl, solo, her breast shape framed by the neckline\'s fall at the viewer below, dusk-silver hair in an antennae-fringe bob, moth-eye amber aimed low, moth-dust pale skin, fuzzy moth collar, moth girl, dust-silver wings, moth antennae, human face, slender body, small breasts, slim hips, mid_bededge,",')

# P27: breast-грамма + bell + skin + lamp
sub('"Masterpiece, best quality, absurdres, intricate details, camera from below looking up into the open panel, full figure, on hands and knees at an open wiring panel, 1girl, solo, her breast shape strung on the knotted tee\'s strap-line, storm-red hair in a horn-clear high tail, ember eyes on the circuit, oni blush lit like a lamp, small horns, oni girl, human face, full breasts, soft belly, round middle, mid_panelovertime,",',
    '"Masterpiece, best quality, absurdres, intricate details, camera from below looking up into the open panel, full figure, on hands and knees at an open wiring panel, 1girl, solo, her breast shape carried on the knotted tee\'s strap-line, storm-red hair in a horn-clear high tail, ember eyes on the circuit, blush-warm skin, oni blush lit like a gauge, small horns, oni girl, human face, full breasts, soft belly, round middle, mid_panelovertime,",')
sub('"a sterile screwdriver flat on the palm as the etiquette demands, both palms flat on the panel\'s frame one at a time, the horn-tap twice on entry for luck, the small gold bell keeping the continuity-test rhythm,",',
    '"a sterile screwdriver flat on the palm as the etiquette demands, both palms flat on the panel\'s frame one at a time, the horn-tap twice on entry for luck, the little bell keeping the continuity-test rhythm,",')
sub('negx=" horns bare of tap, blush cold, screwdriver held, panel dark",',
    'negx=" horns untapped, blush cold, screwdriver held, panel dark",')

# P28: bell + skin
sub('honey-blonde hair in an antennae-crown bun, nectar-brown eyes on the count, bee girl, antennae, thin chitin cuffs at the wrists, small wings, human face, hourglass figure, medium breasts, mid_mosscount,',
    'honey-blonde hair in an antennae-crown bun, nectar-brown eyes on the count, honey-toned skin, bee girl, antennae, thin chitin cuffs at the wrists, small wings, human face, hourglass figure, medium breasts, mid_mosscount,')
sub('''         "both palms flat on the moss-grown stone as the rings arrive, fingers tallying each new growth-circle on the beat, the chitin cuffs chiming their small ledger-note, the wings' rainbow sheen marking good light,",''',
    '''         "both palms flat on the moss-grown stone as the rings arrive, fingers tallying each new growth-circle on the beat, the chitin cuffs chiming their small ledger-note, the little bell of the collar off for the count, the wings' rainbow sheen marking good light,"'''.rstrip() + ',"')

# P32: BT-теги + skin
sub('''         "Masterpiece, best quality, absurdres, intricate details, slight low angle up the melt-line, upper body, ice cube melting a slow line from the collarbone, 1girl, solo, her breast shape under the athletic crop's dry-fit honesty, ink-black hair with a white stripe part, ledger-green eyes tipped to the sun, fluffy skunk tail, white stripe through the hair, skunk girl, human face, thick thighs, wide hips, small breasts, mid_iceline,",''',
    '''         "Masterpiece, best quality, absurdres, intricate details, slight low angle up the melt-line, upper body, ice cube melting a slow line from the collarbone, 1girl, solo, her breast shape under the athletic crop's dry-fit honesty, ink-black hair with a white stripe part, ledger-green eyes tipped to the sun, night-warm skin, fluffy skunk tail, white stripe through the hair, skunk girl, human face, pear figure, small breasts, wide hips, mid_iceline,",''')

# P09: skin
sub('silver-white hair in a wind-blown bob, pale amber eyes dipped to the point below, translucent air-current edges, wind spirit girl, human face, tall slender body, small breasts, mid_aercrawl,',
    'silver-white hair in a wind-blown bob, pale amber eyes dipped to the point below, mist-pale skin, translucent air-current edges, wind spirit girl, human face, tall slender body, small breasts, mid_aercrawl,')

# P17: skin
sub('wheat-blonde hair in a loose sleeping braid, morning-grey eyes half-in the dream, warm skin sleep-soft, human, chubby, plump build, large breasts, mid_bedmemory,',
    'wheat-blonde hair in a loose sleeping braid, morning-grey eyes half-in the dream, sleep-warm skin, human, chubby, plump build, large breasts, mid_bedmemory,')

# P16: копипаста «line over the chest's bare line» — P31 уже разведено, P16 ок

# ── G. Волна 14: candle → wax (закон света) ─────────────────────────────
sub('secondary=["candle-warm-amber"],  # цвет, не прибор: воск как материал',
    'secondary=["wax-warm-amber"],  # цвет воска, не прибор (закон света v2)')
sub("wax-oxblood over parchment-cream, candle-warm-amber at the pour's edge",
    "wax-oxblood over parchment-cream, wax-warm-amber at the pour's edge")

# ── H. NEG: не ронять запятую после «hazy» ──────────────────────────────
sub('neg3 = NEG_BASE[2].rstrip(",") + " " + s["negx"].strip()',
    'neg3 = NEG_BASE[2] + s["negx"].strip()  # «hazy,» остаётся юнитом (negBase v3)')

open(P, 'w').write(s)
print('патч применён, изменений:', len(s) - len(n0), 'байт дельта')
