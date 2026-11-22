#!/usr/bin/env python3
"""T5-30 «WHAT THE FUCK IS THAT?!» — сборщик батча.

Заказ автора 2026-11-22 (вербатим): «Давай ебанём, раз уж на то пошло.
Новая тема: What the Fuck is That?! (21 слот)
Темы для ОС-канона: (3 слота)
- Эро-Интро для Noxx
- Blurry Dreams
- Dirty Whore
EXP-слоты; 9 слотов;
- 9 кандидатов в ОС, 9 экспериментальных комбо одежды и Y в сумме на R+
рейтинг (очень близкие к потолку), 9 новых раскрасок и экспериментальных
палитр».

Режим CLOCK · жребий оракула №4 (seed 2323661502 = 30×2654435761 mod 2³²)
· ПЕРВЫЙ БАТЧ ЭРЫ ГЕЙТОВ 1.18.0 (В39–В43, FAIL с T5-30): вольт-ядро 14/7
вперемешку, кины ≤ 10, EXQUISITE в мейнах, EXP-клетки = полка гипотез,
рейтинг честен по составу (rating_implied).

Карзамены ×9: Y348→Y446 (ОС: дубль №28 + витрина), Y302→Y320, Y237→Y89,
Y194→Y359, Y239→Y366 (дубли №28), Y421→Y250, Y154→Y334, Y188→Y415,
Y181→Y363 (Закон 24: R+×14 — жребий дал 6 класс-карт, канон требует 14).
"""
import json
import re
from pathlib import Path

ROOT = Path('/home/z/my-project')
SPECS = ROOT / 'specs'

cam = json.load(open(SPECS / 'camera.json'))
CARDS = {c['id']: c for c in cam['y_cards']['cards']}
PAL = json.load(open(SPECS / 'palettes.json'))
PALMAP = {p['id']: p for p in PAL['palettes']}
RACES = json.load(open(SPECS / 'races.json'))
RACEMAP = {x['id']: x for x in RACES['races'] if isinstance(x, dict)}
MARKS = {m['id']: m for m in json.load(open(SPECS / 'marks.json'))['marks']}


def weave(yid):
    """Копипаст-юнит 1:1 — components.pose карты (LAWS §17)."""
    return (CARDS[yid].get('components') or {}).get('pose', '').strip()


def corr(yid):
    return CARDS[yid].get('corridor', '—')


def eclass(yid):
    return ((CARDS[yid].get('components') or {}).get('exposure') or {}).get('class', '—')


CAM_SD = {
    "CAM01": "frontal eye-level camera", "CAM02": "camera from above looking down",
    "CAM03": "camera from below looking up", "CAM04": "over the shoulder camera",
    "CAM06": "wide environmental shot, body small in frame",
    "CAM14": "top-down into the cleavage's shaft",
}


def cam_prose(yid):
    """CAM-код карты → проза (В34: кодов в POS нет)."""
    s = str(((CARDS[yid].get('components') or {}).get('camera')) or '').strip()
    m = re.match(r'CAM\d+[_ ](\w+)', s)
    if m:
        return f"{m.group(1).replace('_', ' ').lower()}"
    if s in CAM_SD:
        return CAM_SD[s]
    if s.startswith('CAM'):
        return 'upper body three-quarter'
    return s.lower() or 'upper body three-quarter'


# ────────────────────────── волна 14 «покрытия-настроения» (9 trial, EXP) ──────────────────────────
# Заказ автора: «9 новых раскрасок и экспериментальных палитр». Волна 14 —
# способы раскраски (преемство волны 10): 9 механик цвета, которых в пулaх
# не было. Trial до вердикта T5-30. В palettes.json вносит scripts/t530_registries.py.
WAVE14 = [
    dict(id="P270_GLASSBITE_MINT", name="Glassbite Mint",
         dominant=["cold-mint-glass", "frost-steel"],
         secondary=["breath-warm-fog"],
         accent1=["one copper flake at the rim"],
         accent2="ice-shadow-teal",
         shadow="freezer-shadow-green",
         forbidden=["neon", "pure-white"],
         light_type="стекло-укус: холодный мятный воздух с одной тёплой точкой — дыхание против мороза, свет идёт изнутри стекла",
         sd_fragment="cold-mint-glass over frost-steel, breath-warm-fog at the lips' edge, one copper flake at the rim",
         mood="the-cold-that-flirts",
         family="exp_color_wave_14",
         born="2026-11-22, T5-30 «WHAT THE FUCK IS THAT?!» — волна 14 «покрытия-настроения»",
         trial="trial до вердикта T5-30"),
    dict(id="P271_WAX_SEAL_OXBLOOD", name="Wax Seal Oxblood",
         dominant=["wax-oxblood", "parchment-cream"],
         secondary=["wax-warm-amber"],  # цвет воска, не прибор (закон света v2)
         accent1=["a single unbroken seal"],
         accent2="thread-twined-red",
         shadow="ink-pool-brown",
         forbidden=["neon", "pastel"],
         light_type="печать воском: тёплый оксблад ложится плотным слоем на пергамент — свет от воска, не от прибора",
         sd_fragment="wax-oxblood over parchment-cream, wax-warm-amber at the pour's edge, thread-twined-red accent",
         mood="the-seal-not-yet-broken",
         family="exp_color_wave_14",
         born="2026-11-22, T5-30 «WHAT THE FUCK IS THAT?!» — волна 14 «покрытия-настроения»",
         trial="trial до вердикта T5-30"),
    dict(id="P272_STATIC_LILAC", name="Static Lilac",
         dominant=["static-lilac-grey", "screen-off-indigo"],
         secondary=["signal-pink-flicker"],
         accent1=["one scan-line of gold"],
         accent2="hush-violet",
         shadow="off-shadow-plum",
         forbidden=["pure-white", "flat sky"],
         light_type="статика сирени: воздух звенит розовым шумом, свет мерцает строками — живой экран без прибора",
         sd_fragment="static-lilac-grey over screen-off-indigo, signal-pink-flicker across the frame, one scan-line of gold",
         mood="the-channel-between",
         family="exp_color_wave_14",
         born="2026-11-22, T5-30 «WHAT THE FUCK IS THAT?!» — волна 14 «покрытия-настроения»",
         trial="trial до вердикта T5-30"),
    dict(id="P273_FOIL_BALLOON_COPPER", name="Foil Balloon Copper",
         dominant=["balloon-copper-foil", "party-teal"],
         secondary=["crepe-paper-red"],
         accent1=["one hard crease of light"],
         accent2="string-shadow-blue",
         shadow="under-table-shadow",
         forbidden=["neon", "muted"],
         light_type="фольга-шар: медная плёнка натянута туго, свет скользит складкой — праздник как физика",
         sd_fragment="balloon-copper-foil over party-teal, crepe-paper-red drift, one hard crease of light",
         mood="the-party-still-up",
         family="exp_color_wave_14",
         born="2026-11-22, T5-30 «WHAT THE FUCK IS THAT?!» — волна 14 «покрытия-настроения»",
         trial="trial до вердикта T5-30"),
    dict(id="P274_TIDEPOOL_MIRROR", name="Tidepool Mirror",
         dominant=["tidepool-teal-deep", "wet-sand-bronze"],
         secondary=["anemone-pink-frill"],
         accent1=["one sky-drop caught mid-drip"],
         accent2="shell-nacre-edge",
         shadow="undertow-shadow-blue",
         forbidden=["neon", "pure-white"],
         light_type="зеркало лужи: лужа держит небо целиком — отражение глубже самого неба, свет приходит снизу",
         sd_fragment="tidepool-teal-deep over wet-sand-bronze, anemone-pink-frill at the rim, one sky-drop caught mid-drip",
         mood="the-sky-in-a-puddle",
         family="exp_color_wave_14",
         born="2026-11-22, T5-30 «WHAT THE FUCK IS THAT?!» — волна 14 «покрытия-настроения»",
         trial="trial до вердикта T5-30"),
    dict(id="P275_URANIUM_GLASS_GLOW", name="Uranium Glass Glow",
         dominant=["uranium-green-glass", "cabinet-oak-dark"],
         secondary=["shelf-dust-gold"],
         accent1=["edge-glow where the light passes"],
         accent2="stem-etched-white",
         shadow="cupboard-shadow-umber",
         forbidden=["neon", "pastel"],
         light_type="урановое стекло: зелёное свечение живёт В веществе — свет проходит сквозь и зеленеет на выходе",
         sd_fragment="uranium-green-glass over cabinet-oak-dark, shelf-dust-gold motes, edge-glow where the light passes",
         mood="the-glow-inside-things",
         family="exp_color_wave_14",
         born="2026-11-22, T5-30 «WHAT THE FUCK IS THAT?!» — волна 14 «покрытия-настроения»",
         trial="trial до вердикта T5-30"),
    dict(id="P276_POCKET_DENIM_DUSK", name="Pocket Denim Dusk",
         dominant=["denim-dusk-indigo", "coin-worn-copper"],
         secondary=["lint-fleck-white"],
         accent1=["one ticket-stub red"],
         accent2="seam-gold-thread",
         shadow="pocket-lining-shadow",
         forbidden=["neon", "pure-white"],
         light_type="карманный деним: индиго вытерто до меди на сгибах — свет находит только края, центр держит сумрак",
         sd_fragment="denim-dusk-indigo over coin-worn-copper, lint-flecks adrift, one ticket-stub red accent",
         mood="what-the-pocket-keeps",
         family="exp_color_wave_14",
         born="2026-11-22, T5-30 «WHAT THE FUCK IS THAT?!» — волна 14 «покрытия-настроения»",
         trial="trial до вердикта T5-30"),
    dict(id="P277_SORBET_STAIN", name="Sorbet Stain",
         dominant=["sorbet-mango", "raspberry-drip"],
         secondary=["waffle-cone-gold"],
         accent1=["one drip caught mid-fall"],
         accent2="paper-straw-red",
         shadow="melon-shadow-orange",
         forbidden=["neon", "muted"],
         light_type="след щербета: тёплые пятна соков на светлом — цвет как случайность, которую решили не отстирывать",
         sd_fragment="sorbet-mango over raspberry-drip, waffle-cone-gold base, one drip caught mid-fall",
         mood="the-stain-you-keep",
         family="exp_color_wave_14",
         born="2026-11-22, T5-30 «WHAT THE FUCK IS THAT?!» — волна 14 «покрытия-настроения»",
         trial="trial до вердикта T5-30"),
    dict(id="P278_LEDGER_GREEN", name="Ledger Green",
         dominant=["ledger-green-ink", "banknote-cream"],
         secondary=["rubber-band-amber"],
         accent1=["one column summed in red"],
         accent2="fountain-pen-navy",
         shadow="drawer-shadow-brown",
         forbidden=["neon", "pastel"],
         light_type="бумага-гроссбух: зелень чернил на кремовой строке — бухгалтерия как погода, свет ровный канцелярский",
         sd_fragment="ledger-green-ink over banknote-cream, rubber-band-amber strap, one column summed in red",
         mood="the-count-that-comes-out",
         family="exp_color_wave_14",
         born="2026-11-22, T5-30 «WHAT THE FUCK IS THAT?!» — волна 14 «покрытия-настроения»",
         trial="trial до вердикта T5-30"),
]
WAVE14_MAP = {w['id']: w for w in WAVE14}


def pal_line(pid, sig, wave14=None):
    if pid in WAVE14_MAP:
        w = WAVE14_MAP[pid]
        return f"{w['name']} palette, {w['sd_fragment']}; her colors: {sig}."
    p = PALMAP[pid]
    frag = p.get('sd_fragment', '')
    if not frag:
        frag = f"{p['dominant'][0]} over {p.get('secondary', ['deep'])[0]}"
    return f"{p['name']} palette, {frag}; her colors: {sig}."

# ────────────────────────── каналы волны 16 (2 кандидата ☠) ──────────────────────────
# В реестр delivery-stats.json вносит scripts/t530_registries.py (0.15.0→0.16.0).
# Остальные R+-мейны едут на live-каналах (квота кандидатов ≤2 — закон,
# T5-29 платил 10×candidate WARN; эра 1.18.0 возвращает дисциплину).
WAVE16_CHANNELS = {
    "strap-line-hold": ("Strap-Line Hold",
                        "линия-бретель как единственная крышка: край ткани/пояс/шнур, "
                        "скрученный в одну линию через голую линию груди — панелей нет, "
                        "крышка сама родилась из несущего края (P16: полу-скрученный пояс "
                        "тануки превращает саронг в бретель)"),
    "element-linen": ("Element Linen",
                      "стихия как ткань: линия огня/дыма/воды/света драпирует зону заявки "
                      "как единственная материя — стихию можно схватить кулаком за край "
                      "(P19: линия живого пламени — шарф, который не жжёт свою хозяйку)"),
}

# ────────────────────────── типажи (кап 3, Body: BT-XX в шапке) ──────────────────────────
BT_NAMES = {
    "BT-01": "Ивовый стан", "BT-02": "Танцевальная линия", "BT-03": "Стеклянная",
    "BT-04": "Хрупкая середина", "BT-05": "Речная", "BT-06": "Часы-классика",
    "BT-07": "Колонна", "BT-08": "Лёгкий спорт", "BT-09": "Мягкие часы",
    "BT-11": "Верхняя тяжесть", "BT-12": "Маленькая гордость", "BT-13": "Плоская честность",
    "BT-14": "Полная капля", "BT-10": "Груша", "BT-15": "Огромная мягкая", "BT-16": "Животик",
    "BT-17": "Бёдра-тяжеловес", "BT-18": "Пухлая мягкость", "BT-19": "Сидячая складка",
    "BT-20": "Яблочко", "BT-21": "Плюс-часы", "BT-22": "Высокая мягкая",
    "BT-23": "Коротыши", "BT-24": "Широкая мягкая",
}
BT_MAP = {
    "P01": "BT-12", "P02": "BT-04", "P03": "BT-04",
    "P04": "BT-07", "P05": "BT-14", "P06": "BT-06", "P07": "BT-02", "P08": "BT-14",
    "P09": "BT-01", "P10": "BT-05", "P11": "BT-11", "P12": "BT-04", "P13": "BT-06",
    "P14": "BT-05", "P15": "BT-13", "P16": "BT-21", "P17": "BT-18", "P18": "BT-22",
    "P19": "BT-22", "P20": "BT-02", "P21": "BT-21", "P22": "BT-19", "P23": "BT-08",
    "P24": "BT-08",
    "P25": "BT-03", "P26": "BT-22", "P27": "BT-20", "P28": "BT-06", "P29": "BT-15",
    "P30": "BT-13", "P31": "BT-16", "P32": "BT-10", "P33": "BT-23",
}

# ────────────────────────── слоты ──────────────────────────
SLOTS = []


def slot(sid, slug, paren, **kw):
    kw.update(sid=sid, slug=slug, paren=paren)
    SLOTS.append(kw)


NEG_BASE = [
    "young girl, immature body, oversized head, loli, shota, signature, watermark, artist name, logo, 1boy, candle, lamp, photorealistic, 3d face, realistic facial structure, bad anatomy,",
    " extra fingers, bad hands, washed-out, faded colors, low contrast, flat colors, muddy colors, dull, overexposed, underexposed, pastel colors, muted colors, gray palette, pale colors, desaturated,",
    " white haze, milky fog, soft focus, hazy,",
]

# ══════════════════ ОС P01–P03 (EXQUISITE · канон VERBATIM · жребий №4) ══════════════════

slot("P01", "noxx-ero-intro-flame-curtain", "EXQUISITE · Noxx · R+ · Y375 · P30_VOID_SMOKE",
     channel="oc-rplus",
     corridor="A",
     oc_theme="Эро-Интро для Noxx: предмет = the fire-frame curtain pushed aside by her palm.",
     thesis=("«ЭРО-ИНТРО: NOXX ВПЕРВЫЕ ПОКАЗЫВАЕТСЯ ЧИТАТЕЛЮ КАК ЭРОС — И ПОРОГ ВСТРЕЧАЕТ ЕЁ ОГНЁМ. "
             "РАМА ДВЕРИ ГОРИТ ВЕСЬ, НО ПЛАМЯ ДЛЯ НЕЁ — ЗАНАВЕС: ЛАДОНЬ ОТВОДИТ ОГОНЬ, КАК ШТОРУ, "
             "И ОНА ВЫХОДИТ НАЗАД, В УЛИЦУ, ОДНОЙ НОГОЙ ЕЩЁ В ПЕРЕГОВОРАХ. ВИНИЛОВЫЙ ПЛАЩ РАСКРЫТ, "
             "МОХЕР У ЛОКТЕЙ — МЯГКИМ СЕРЫМ ТЮКОМ, УЗЕЛ ФУТБОЛКИ СПУЩЕН К ТАЛИИ. ЗВЁЗДНАЯ ПЫЛЬ НА "
             "ЧЁРНОЙ КОЖЕ — ЕДИНСТВЕННАЯ НОЧЬ, КОТОРАЯ НОСИТСЯ. СВЕТ НЕ БОРЕТСЯ С НЕЙ — ОНИ "
             "ДОГОВАРИВАЮТСЯ НА ПОРОГЕ, И ЗАНАВЕС ИЗ ОГНЯ ДЕРЖИТ ЕЁ КУЛАК. ЭТО НЕ ДЕБЮТ — ПРЕДСТАВЛЕНИЕ»."),
     gag=("Гэг-стек (4 фишки OC, канон 2.14.0): 1) её тень уже ждёт у стены — приходит раньше и "
          "уходит позже, эскорт-привычка порога; 2) звёздная пыль на чёрной коже — созвездие, "
          "которое она носит собой, у порога вспыхивает ярче; 3) бледное светящееся лицо — "
          "единственная яркая точка кадра, огонь рамы лишь подсвечивает переговорщика; "
          "4) кружевные перчатки у запястий — договор подписан кружевом, не кровью."),
     spine="Y375 Fire-Curtain Threshold (frontal eye-level, combo→Y375, карта-стенд) · CAM— frontal eye level · LEAD the introduced dusk · diplomacy register · upper body",
     race="— (канон VERBATIM, oc-canon.json 2.14.0: Noxx, Two of Swords)",
     gar="прозрачный виниловый плащ (gloss planes, расхлёстнут) + мохер-свитер, спущенный к обоим локтям мягким серым тюком + хлопковая футболка узлом у талии (узел ниже линии груди) + кружевные перчатки у запястий · HS: канон (depth-black hair in a ghost-layer shag)",
     stack=["CR-W21", "CR-A15", "CR-L11", "CR-D42"],
     ycard="Y375",
     pos=[
         "Masterpiece, best quality, absurdres, intricate details, frontal eye-level camera at the threshold, upper body, stepping back through a burning doorway, 1girl, solo, her breast shape claimed by the open vinyl's gloss, depth-black hair in a ghost-layer shag, pale glowing face, silver-grey eyes, black skin with soft star-glow flecks, edges blurring into shade, human face, small high-set chest, slim waist, mid_flamecurtain,",
         "the clear vinyl raincoat worn open at the front, her fist gripping the fire-curtain's hem like a conductor's, nothing underneath the vinyl's gloss but the negotiated light — the introduced dusk is the claim, threshold-made,",
         weave("Y375"),
         "the oversized mohair pushed to both elbows in a soft grey bundle, lace gloves at the wrist-line holding the flame's edge flat, the knotted cotton riding the waist's line below, the strap slipped off the shoulder's slope long ago and the line still honest,",
         "her shadow already waiting at the street-side wall, one step ahead and patient, the star-flecks waking brighter where the frame's heat passes,",
         "one foot still in the doorway's argument, palm pushing the fire aside,",
         "the burning frame throwing no heat her way — the flames part like staff before a familiar diplomat, the street behind her ordinary and dusk-quiet, the threshold's old brackets holding nothing but her business card of smoke,",
         pal_line("P30_VOID_SMOKE", "the dusk that introduces itself"),
     ],
     negx=" shadow gone, star-flecks absent, vinyl opaque, fire roaring",
     face="stylized 2D anime face into the lens, anime eyes (silver-grey, negotiating), small nose, small mouth on the first word of the introduction, one ghost-layer crossing the lens-side cheek.",
     )

slot("P02", "ama-blurry-dreams-towel", "EXQUISITE · Ama · R+ · Y388 · P59_RAINY_WINDOW",
     channel="oc-rplus",
     corridor="A",
     oc_theme="Blurry Dreams: предмет = the towel around her neck, knuckles wrapped, head turned back to the dream.",
     thesis=("«РАЗМЫТЫЕ СНЫ: АМА ИДЁТ ИЗ СНА, КОТОРЫЙ ЕЩЁ НЕ ОТПУСТИЛ. ПОЛОТЕНЦЕ НА ШЕЕ, КУЛАКИ "
             "ЗАМОТОВОГАНЫ В ЕГО КОНЦАХ, ГОЛОВА ПОВЁРНУТА НАЗАД ЧЕРЕЗ ПЛЕЧО — К ДВЕРНОМУ ПРОЁМУ, "
             "ИЗ КОТОРОГО ИДЁТ ДОЖДЬ ВВЕРХ: КАПЛИ ПОДНИМАЮТСЯ, КАК БУДТО СОН ПЕРЕВАРИВАЕТ СЕБЯ "
             "ОБРАТНО. МОКРАЯ ШЕРСТЯНАЯ КОФТА СЛЕЗАЕТ С ОБОИХ ПЛЕЧ — ЛАВАНДОВЫЕ ВОЛОСЫ ДРЕЙФУЮТ "
             "СПОРАМИ В ВОДЕ, ШЛЯПКА-ГРИБ НА МАКУШКЕ ДЕРЖИТ ПОСЛЕДНИЙ СУХОЙ КВАДРАТ НЕБА. "
             "СЫРОСТЬ СНА ОСТАЁТСЯ НА КОЖЕ — И ЭТО ЕЁ РАБОЧАЯ ФОРМА: ДОЖДЬ СЛЕДУЕТ ЗА НЕЙ, "
             "А СНЫ — ЗА ДОЖДЁМ. РАЗМЫТИЕ ЖИВЁТ КАПЛЕЙ И ДРЕЙФОМ, НЕ ФИЛЬТРОМ»."),
     gag=("Гэг-стек (4 фишки OC): 1) дождь идёт ВВЕРХ за её спиной — сон выветривается к небу, "
          "капля за каплей; 2) шляпка-гриб на макушке держит последний сухой квадрат — под "
          "ней всегда сухо, всегда полдень; 3) волосы дрейфуют спорами в воде — на секунду "
          "отстают от поворота головы, как недосмотренный сон; 4) споры-веснушки на плечах "
          "слабо светятся — карта сна, которую она носит кожей."),
     spine="Y388 Towel-Neck Dreamwalk (over the shoulder camera, combo→Y388, карта-стенд) · CAM— over the shoulder · LEAD the unfinished dream · sleepwalk register · upper body",
     race="— (канон VERBATIM, oc-canon.json: Ama, грибная дева дождя)",
     gar="белая шерстяная кофта навыпуск (промокла насквозь, сползла с обоих плеч — канон-униформа дождя) + полотенце на шее (объект карты) · HS: канон (long flowing lavender-white hair, drifting like spores in water)",
     stack=["CR-W33", "CR-B56", "CR-U09", "CR-D53"],
     ycard="Y388",
     pos=[
         "Masterpiece, best quality, absurdres, intricate details, over the shoulder camera, upper body, walking out of a dream with a towel around the neck, 1girl, solo, her breast shape read in the soaked wool's cling, long flowing lavender-white hair drifting like spores in water, deep violet eyes half-open backwards, pale lavender-white skin, spore-marks on the cheek, large lavender mushroom cap as a wide hat, human face, soft slight frame, mid_dreamwalk,",
         "the wet sheer sweater slipping off both shoulders at once, her fists wrapped in the towel's ends, nothing underneath the soaked weave but the dream's own damp — the unfinished dream is the claim, sleepwalk-made,",
         weave("Y388"),
         "the mushroom cap's gill-lines deeper lavender at the brim, one dry square of noon kept under it, the towel's fringe dripping upward-backward toward the doorway of the dream,",
         "the spore-freckles on her shoulders glowing faint as a dream's map, the wool's weight honest and warm-cold at once,",
         "knuckles wrapped in the towel, one fist open, head turned back over the shoulder,",
         "behind her the dream's doorway raining upward, drops climbing back into the dark like a rewound weather, the room ahead ordinary and waiting for her to arrive twice,",
         pal_line("P59_RAINY_WINDOW", "the rain she carries inside"),
     ],
     negx=" rain downward, cap gone, sweater dry, eyes wide awake",
     face="stylized 2D anime face half-turned back into the dream, anime eyes (deep violet, half-open, still seeing it), small nose, small mouth mid-yawn swallowed, one lavender drift crossing the cheek a beat late.",
     )

slot("P03", "dove-dirty-whore-showcase-jamb", "EXQUISITE · Dove · R+ · Y446 · P131_JUNK_GLASS",
     channel="oc-rplus",
     corridor="A",
     oc_theme="Dirty Whore: предмет = the door-jamb as a shop window, palms on both posts, price-tag cord swaying.",
     thesis=("«ГРЯЗНАЯ ШЛЮХА — ЭТО ПРОФЕССИЯ, КОТОРАЯ СЕБЯ НЕ ИЗВИНЯЕТ: DOVE СТОИТ В ДВЕРНОМ "
             "ПРОЁМЕ, КАК В ВИТРИНЕ НОЧНОГО РЯДА, — ЛАДОНИ НА ОБЕИХ СТОЙКАХ, РАМА НАТЯНУТА НА "
             "НЕЁ, КАК ЧЕХОЛ. ВИНИЛОВЫЙ ТОП РАСКРЫТ, БРЕТЕЛЬКИ ДЕРЖАТ ГОЛУЮ ЛИНИЮ ГРУДИ, "
             "ЦЕННИК НА РОЗОВОМ ШНУРКЕ КАЧАЕТСЯ МЕЖДУ РЁБЕР — И ЭТО НЕ УНИЖЕНИЕ, ЭТО ПРАЙС: "
             "ОНА САМА ПРОДАВЕЦ И САМА ТОВАР, ВЗГЛЯД ТЁПЛЫЙ, КАК КОНФЕТНАЯ ГЛАЗУРЬ. УЛИЦА "
             "СМОТРИТ — ОНА СМОТРИТ В ОТВЕТ, И ВЫИГРЫВАЕТ ТОРГ. ГРЯЗЬ ЗДЕСЬ — ЧЕСТНОСТЬ "
             "НОЧНОГО ГОРОДА, А СТИЛЬ — ДОГОВОР, ПОДПИСАННЫЙ ЦЕННИКОМ»."),
     gag=("Гэг-стек (4 фишки OC): 1) парные кудри-дрели у висков качают счёт завитков при "
          "каждом движении — витрина живая; 2) ценник на розовом шнурке — реквизит кадра и "
          "её визитная карточка: цена написана её почерком; 3) карамельно-красные глаза с "
          "витринным теплом — взгляд продавца, который сам товар; 4) винил натягивается до "
          "стеклянного блика ровно там, где наклон тянет — витрина блестит изнутри."),
     spine="Y446 Door-Jamb Showcase (camera from above looking down, combo→Y446, карта-стенд) · CAM— from above, down the jamb's line · LEAD the priced display · showcase register · upper body",
     race="— (канон VERBATIM, oc-canon.json: Dove, human; candy решает)",
     gar="виниловый топ мокрого блеска (раскрыт спереди, бретельки на голой линии) + джинсовая мини-юбка с бахромой + ценник на розовом шнурке · HS: канон (bubblegum-pink hair in paired drill curls)",
     stack=["CR-W51", "CR-B67", "CR-L14", "CR-M19"],
     ycard="Y446",
     pos=[
         "Masterpiece, best quality, absurdres, intricate details, camera from above, down the door-jamb's line, upper body, braced across the doorway like her own window display, 1girl, solo, her breast shape priced by the straps' honest line, bubblegum-pink hair in paired drill curls, candy-red eyes warm as a shopfront, peach-cream skin, human face, young slight build, small softly-mounded chest, mid_priceddisplay,",
         "the vinyl top worn open at the front, its two straps ruling the chest's bare line like a receipt's rule, nothing underneath the gloss but the price-tag cord's sway — the priced display is the claim, showcase-made,",
         weave("Y446"),
         "her palms pressed flat to both posts, the price-tag on its pink cord swinging between the ribs, handwritten, the frayed denim mini's threads counting the night's trade, the drill curls ticking their coil-count at the sway,",
         "both posts of the jamb taking her palms' weight, the vinyl's wet-look shine pulling one glass highlight down the lean,",
         "braced across the door-jamb, palms set on both posts, filling the frame she chose,",
         "the night street's junk-glass windows running their little auctions both ways, the doorframe's peeling paint honest as a market's floor, nobody haggling her down — the street knows better,",
         pal_line("P131_JUNK_GLASS", "the price she writes herself"),
     ],
     negx=" curls hidden, tag gone, top closed, eyes cold",
     face="stylized 2D anime face up into the lens, anime eyes (candy-red, display-warm), small nose, small mouth holding the start of a deal, one drill curl mid-count at the cheek.",
     )

# ══════════════════ МЕЙНЫ P04–P24 (вольт-ядро 14/7 вперемешку, В39) ══════════════════

slot("P04", "mouse-wellsight", "NICHE · R29 Mouse-kin · R · Y69 · P156_FAULT_CLIFF_IRON",
     channel=None, corridor="—",
     thesis=("«МЫШЬ-КАРТОГРАФКА СМОТРИТ В ШАХТУ-КОЛОДЕЦ, ДНО КОТОРОЙ — ВЧЕРАШНИЙ ДЕНЬ: "
             "ВЕРТИКАЛЬНЫЙ СВЕТ ЗАКРУЧИВАЕТСЯ ВОКРУГ НЕЁ ВОРОНКОЙ, ВЫРЕЗ ГРУДИ ВЕДЁТ КАДР "
             "ВНИЗ, И ОНА ЧИТАЕТ СТЕНКИ ШАХТЫ ПАЛЬЦАМИ — КАК ШРИФТ БРАЙЛЯ. ШАХТА УСТРОЕНА "
             "НЕ ВНИЗ, А НАЗАД ВО ВРЕМЕНИ: КАЖДЫЙ ЯРУС — ПРОШЛЫЙ ВТОРНИК. СВЕРХУ ВИДНО, "
             "КАК ЕЁ ХВОСТИК-ОТВЕС ВИСИТ В ШАХТУ ГЛУБИНОМЕРОМ. ЧТО ЭТО ЗА ШАХТА "
             "ТАКАЯ? — А ЭТО АРХИВ, ПРОСТО СТОЯЩИЙ НА РЕБРЕ»."),
     gag=("Гэг-стек: круглые ушки ловят эхо ярусов — слуховой дальномер; каждый угол "
          "обода тестируется одним пальцем — картография как привычка; манжета-фонарь "
          "со счётчиком ярусов надета поверх локтя; хвостик-отвес меряет глубину «вчера»."),
     spine="Y69 Shaft Lean (top-down into the cleavage's shaft, combo→Y69, карта-стенд) · CAM— top-down shaft · LEAD the yesterday-well · archive register · upper body from above",
     race="R29 — мышь: тестирует каждый угол стены одним пальцем — картография как привычка.",
     gar="рабочая куртка-архивариуса (распахнута, вырез ведёт в шахту кадра) + счётчик ярусов на манжете · HS: HS29 Fitted Work Bun",
     stack=["CR-A12", "CR-E28", "CR-D13", "CR-S14"],
     ycard="Y69",
     pos=[
         "Masterpiece, best quality, absurdres, intricate details, top-down into the cleavage's shaft, upper body, leaning forward over the well-mouth's rail, 1girl, solo, her breast shape leading the frame's drop through the open neckline, earth-brown hair in a fitted work bun, dark-brown button eyes taking the key light whole, warm field skin, mouse girl, round mouse ears, thin mouse tail, human face, average build, medium breasts, mid_wellsight,",
         "the neckline falling open with gravity over the yesterday-shaft, her breast shape read by the drop's honest line — the yesterday-well is the claim, archive-made,",
         weave("Y69"),
         "the thin tail hanging plumb into the shaft as a depth-gauge, a tier-counter strapped over one elbow, one glove tucked in the belt, a brass whistle for the cage-man at her wrist,",
         "the jacket's open fronts framing the drop like book covers, both forearms taking the reading weight,",
         "weight on forearms, the whole pose a librarian's lean over a bottomless card-file,",
         "the shaft's walls shelved with past Tuesdays, each level lit by its own remembered afternoon, the cage-rope running down into last week and still warm,",
         pal_line("P156_FAULT_CLIFF_IRON", "the depth that files itself"),
     ],
     negx=" tail still, ears flat, shaft bottom visible, eyes open wide",
     face="stylized 2D anime face bent to the drop, anime eyes (dark button-brown, happily counting levels), small nose, small mouth on the day's number, one brown strand escaped the bun.",
     )

slot("P05", "jelly-cloud-bath", "VOLT · R17 Jellyfish-kin · R+ · Y89 · P155_CLOUDSEA_NOON",
     channel="handbra-open-palms",
     corridor="A",
     thesis=("«МЕДУЗА ВЫКУПАЛАСЬ В ОБЛАКЕ — И ОБЛАКО СОГЛАСИЛОСЬ. ПОЛОТЕНЦЕ ПЕРЕХВАЧЕНО "
             "СКРЕЩЕННЫМИ РУКАМИ У КЛЮЧИЦЫ, ВЛАЖНЫЕ ВОЛОСЫ-ЩУПАЛЬЦА ЕЩЁ СЧИТАЮТ КАПЛИ, "
             "А НА ПОЛУ ОСТАЛАСЬ ЛУЖА НЕБА — ГОЛУБАЯ, С ОДНИМ БЕЛЫМ ОБЛАКОМ ВНУТРИ. "
             "КУПЕЛЬ БЫЛА НА ТРИДЦАТЬ МЕТРОВ ВЫШЕ КРЫШИ, НО ЕЙ ХВАТИЛО И ЭТОГО: ПОВЕРХНОСТЬ "
             "ДЕРЖАЛА, КАК БАССЕЙН, ПРОСТО ОКАЗАЛАСЬ ИЗ ПОГОДЫ. ВОСКЛИЦАНИЕ «ЧТО ЭТО "
             "БЫЛО?!» ОНА СЛЫШИТ КАЖДУЮ СМЕНУ — И УЖЕ НЕ ОТВЕЧАЕТ»."),
     gag=("Гэг-стек: купол-капюшон на голове держит форму облака — «шапка после бассейна»; "
          "волосы-щупальца отстают от движения на полтакта — Indoor weather; каустика "
          "проходит насквозь и красит стену позади; лужа неба на полу с одним облаком "
          "внутри медленно испаряется обратно в потолок."),
     spine="Y89 Towel-Cross Cloudbath (eye level, combo→Y89, карта-стенд) · CAM— eye level close · LEAD the cloud-bathed bell · weather register · upper body close",
     race="R17 — медуза: волосы-щупальца отстают от течения на полсекунды — домашняя погода.",
     gar="CL-DR-10 (церемониальное платье из вуалей, три слоя убывающей прозрачности — мокрое, облепило) + CL-AC-04 (кружевные перчатки до локтей) + CL-AC-09 (помочи на весу) + полотенце (объект карты — скрещенными руками у ключицы) · HS: HS44 Tentacle Hair, Salt-Dried",
     stack=["CR-W25", "CR-B26", "CR-L12", "CR-M10"],
     ycard="Y89",
     pos=[
         "Masterpiece, best quality, absurdres, intricate details, eye level close, upper body, both arms crossed tight over the chest, 1girl, solo, her breast shape carried by the towel's crossed grip, translucent teal tentacle hair drying in slow curls, pearl-blue eyes one tide calm, gel body with a drifting core, jellyfish girl, translucent bell hood, human face silhouette, large breasts, soft natural shape, average build, mid_cloudbath,",
         "the bath towel's upper edge gripped to the collarbone by both hands, nothing underneath the terry's weave, just the cloud's own cool, the veil dress worn open and clinging where it pleases — the cloud-bathed bell is the claim, weather-made,",
         weave("Y89"),
         "sea-glass earrings at the hood's rim, lace elbow gloves shining wet at the crease, loose suspenders swinging free of the veil dress worn open, the bell hood holding its cloud-shape like a bathing cap,",
         "the towel's crossed grip honest under both fists, hip cocked into the puddle's rim, hair still wet and counting drops,",
         "arms crossed tight, hip cocked, one deep breath from incident,",
         "a puddle of sky on the floor with one white cloud still swimming in it, the room's caustics landing behind her on the wall, the ceiling missing exactly one small cumulus,",
         pal_line("P155_CLOUDSEA_NOON", "the bath that fell from above"),
     ],
     negx=" hood gone, hair dry, towel dropped, puddle empty",
     face="stylized 2D anime face to the lens, anime eyes (pearl-blue, tide-calm), small nose, small mouth on the day's best idea, one tentacle-curl dripping a beat late.",
     )

slot("P06", "seasonpane-warden", "VOLT · human · R+ · Y320 · P141_PHASE_GLASS",
     channel="contact-physics",
     corridor="A",
     thesis=("«СМОТРИТЕЛЬНИЦА ОКНА-СЕЗОНА: ЗА СТЕКЛОМ ЛЕТО, В КОМНАТЕ ЗИМА, И СТЕКЛО ТЁПЛОЕ "
             "ТОЛЬКО С ТОЙ СТОРОНЫ. ЛАДОНЬ ПРИЖАТА К ПАНЕЛИ, ГРУДЬ ВСТРЕЧАЕТ СТЕКЛО "
             "СКВОЗЬ ШЁЛК САРАФАНА — БРЕТЕЛЬКИ ДЕРЖАТ ГОЛУЮ ЛИНИЮ, СВЕТ ИДЁТ СКВОЗЬ ОБЕ "
             "ПОГОДЫ. РАБОТА У НЕЙ ТАКАЯ: ДВАЖДЫ В ДЕНЬ ПРОТИРАТЬ ГРАНИЦУ, ЧТОБЫ СЕЗОНЫ "
             "НЕ ПЕРЕСОРТИРОВАЛИСЬ. ЗРИТЕЛЬ СПРАШИВАЕТ, КАК ТАК МОЖЕТ БЫТЬ, — А ОНА "
             "ОТВЕЧАЕТ МОЛЧА: СТЕКЛО ВИДНО, РАМКА ЦЕЛА, ЗНАЧИТ ВСЁ ЗАКОННО»."),
     gag=("Гэг-стек: на стекле отпечаток её ладони держится с той стороны тёплым контуром; "
          "снежинка за стеклом тает, не долетев до лета; бархатный чокер держит горло — "
          "единственное, что не отдаёт ни одному сезону; заколка-солнце в волосах "
          "поворачивается вслед настоящему."),
     spine="Y320 Season Pane (upper body three-quarter, combo→Y320, карта-стенд) · CAM— three-quarter to the pane · LEAD the two-weather pane · warden register · upper body close",
     race="— (human-служба темы: смотрительница окна-сезона)",
     gar="CL-DR-06 (лёгкий сарафан на бретельках, без лифа — бретельки держат линию) + CL-AC-01 (бархатный чокер) + CL-AC-06 (колокольчик на ошейнике — звонит на сквозняке сезонов) · HS: HS47 Side-Tucked Straight",
     stack=["CR-W27", "CR-C06", "CR-E29", "CR-D25"],
     ycard="Y320",
     pos=[
         "Masterpiece, best quality, absurdres, intricate details, upper body three-quarter to the pane, close on the glass, palm pressed on the glass, 1girl, solo, her breast shape meeting the pane through the sundress's wet-light silk, chestnut hair side-tucked straight, green eyes on the far season, fair skin, human, velvet choker, small gold bell at the throat, healthy build, medium breasts, mid_seasonpane,",
         "the sundress's straps keeping the chest's bare line against the pane's cold-warm border, nothing underneath the season-silk but two weathers arguing politely — the two-weather pane is the claim, warden-made,",
         weave("Y320"),
         "a handprint of her own palm staying warm on the far side of the glass, her palms flat to the pane's border between weathers, one snowflake melting mid-flight on the summer side, the bell ringing its one dry note at the draft,",
         "the silk sheer with both seasons' light at once, the pane taking her press without a word of complaint,",
         "palm pressed on the glass, gaze past the pane into the other season,",
         "the window's summer leaning its heat against the room's winter like a polite queue, the sill's condensation running two directions at once, the warden's rag folded over the frame for the noon wipe,",
         pal_line("P141_PHASE_GLASS", "the border she keeps polished"),
     ],
     negx=" pane broken, seasons mixed, bell silent, strap gone",
     face="stylized 2D anime face half in each light, anime eyes (green, watching the far season), small nose, small mouth level, one chestnut strand stuck to the glass by frost.",
     )

slot("P07", "light-handover-stairs", "NICHE · human · R · Y246 · P64_SUNRISE_INDIGO",
     channel=None, corridor="B",
     thesis=("«ЛЕСТНИЦА, ГДЕ СВЕТ ПЕРЕДАЁТ СЕБЯ ИЗ РУКИ В РУКУ: НА ПЛОЩАДКЕ СМЕНА — "
             "ВЕРХНИЙ ПРОЛЁТ ЕЩЁ ДЕРЖИТ НОЧЬ, НИЖНИЙ УЖЕ ПРИНЯЛ УТРО, И МЕЖДУ НИМИ "
             "СВЕТ ПЕРЕХОДИТ ИЗ ЛАДОНИ В ЛАДОНЬ САМ, БЕЗ НОСИТЕЛЯ. СМОТРИТЕЛЬНИЦА "
             "ОСТАНОВИЛАСЬ НА СЕРЕДИНЕ — РУКА НА ПЕРИЛАХ, ЛИЦО ПОВОРАЧИВАЕТСЯ К БОЛЕЕ "
             "СВЕТЛОМУ МАРШУ, ГРУДНАЯ ЛИНИЯ ЧИТАЕТСЯ СКВОЗЬ ПОВОРОТ. СМЕНЩИЦА СВЕТА "
             "ОПОЗДАЕТ НА ЧЕТВЕРТЬ ЧАСА — И ЭТО ЕДИСТВЕННОЕ, ЧТО ЗДЕСЬ НЕВОЗМОЖНО "
             "ТЕРПИМЫЙ ПЕРЕВОД»."),
     gag=("Гэг-стек: пролетели сумерки-перчатки — свет передаётся в них, как чайник по "
          "смене; ступенька-«передай дальше» истёрта сильнее прочих; бейдж «смена света» "
          "на груди перевёрнут, пока утро не принято полностью; перила тёплые только "
          "с одной стороны."),
     spine="Y246 Light-Handover Landing (upper body three-quarter, combo→Y246, карта-стенд) · CAM— three-quarter at the landing · LEAD the handed-over light · shift register · upper body",
     race="— (human-служба темы: смотрительница смены света)",
     gar="лёгкий форменный сарафан-туника смотрительницы (глубокий вырез, поворот читает линию) + бейдж «смена света» · HS: HS03 Low Twin Braids",
     stack=["CR-B32", "CR-L16", "CR-D31", "CR-C12"],
     ycard="Y246",
     pos=[
         "Masterpiece, best quality, absurdres, intricate details, upper body three-quarter at the landing, stopped mid-stairs where the light changes hands, 1girl, solo, the neckline's turn reading her chest line into the brighter flight, ash-blonde hair in low twin braids, grey eyes on the handover, fair skin, human, slim lithe build, medium breasts, mid_lighthandover,",
         "the light accepting itself from the upper dark into the lower morning across her collarbone's line, the chest line given to the turning face's direction — the handed-over light is the claim, shift-made,",
         weave("Y246"),
         "a pair of twilight gloves hanging on the rail where the last keeper left them, the worn middle step reading pass-it-on in polish, a shift-badge upside down at her sternum until morning is accepted, a brass hairpin through one braid,",
         "the tunic's drape taking the new light first at the shoulder, one hand's weight honest on the rail,",
         "one hand on the rail, face turning toward the brighter flight,",
         "the upper flight still holding its indigo while the lower one runs morning-amber, the window's one pane handing the whole day down stair by stair like a bucket chain,",
         pal_line("P64_SUNRISE_INDIGO", "the shift she clocks in for"),
     ],
     negx=" gloves worn, badge righted, stairs one weather",
     face="stylized 2D anime face turned to the brighter flight, anime eyes (grey, mid-count of the handover), small nose, small mouth on the quarter-hour, one braid tip dipped in the new light.",
     )

slot("P08", "shadow-hammock-prone", "VOLT · human · R+ · Y168 · P81_FAWN_FOLD",
     channel="contact-physics",
     corridor="A",
     thesis=("«ОНА ЛЕЖИТ НА СОБСТВЕННОЙ ТЕНИ — И ТЕНЬ ДЕРЖИТ: ГРУДЬ ПОДНЯТА НА СОБСТВЕННЫХ "
             "ЛАДОНЯХ, ЛОКТИ МЯГКИЕ, ГОЛОВА ОТКИНУТА, ПОЗВОНОЧНИК — ОДИН ДЛИННЫЙ ВОПРОС, "
             "А ТЕНЬ ПОД НЕЙ НЕ НА ПОЛУ, А НА ПОЛТОРАХ САНТИМЕТРОВ НИЖЕ — ГАМАК. ТЕНЬ "
             "ДЕЛАЕТ РАБОТУ ПОДВЕСКИ МОЛЧА И БЕЗ ДОГОВОРА — ПРОСТО УСПЕЛА ПОДСТЕЛИТЬСЯ "
             "ПЕРВОЙ, КОГДА ОНА УПАЛА В ДЕТСТВЕ, И С ТЕХ ПОР НЕ УХОДИЛА С ПОСТА. ВЕС "
             "ЧИТАЕТСЯ ПО СМЯТИЮ ТЕНИ ПОД ЛОКТЯМИ — ВОТ И ВСЯ МАГИЯ, СПАСИБО ЗА ВНИМАНИЕ»."),
     gag=("Гэг-стек: тень-гамак проминается под локтями на полтора сантиметра — видна "
          "честная вытяжка; кимоно распахнуто, рукава — крылья света; колокольчик на "
          "ошейнике звенит от тениного дыхания; на стене вторая тень сидит рядом и "
          "страхует."),
     spine="Y168 Shadow-Hammock Prone (wide environmental shot, combo→Y168, карта-стенд) · CAM— wide, body low in frame · LEAD the held shadow · trust register · full figure prone",
     race="— (human-служба темы: та, чья тень научилась держать)",
     gar="CL-DR-10 (церемониальное платье из вуалей — распахнуто, слои веером по тени) + CL-LG-04 (шёлковое кимоно навыпуск, оби свободно) + CL-AC-06 (колокольчик на ошейнике) · HS: HS52 Loose Waves, Floor-Length",
     stack=["CR-W39", "CR-B37", "CR-L18", "CR-M16"],
     ycard="Y168",
     pos=[
         "Masterpiece, best quality, absurdres, intricate details, wide environmental shot, body low in frame, prone over her own shadow, 1girl, solo, her breast shape lifted onto her own two palms, honey-brown hair in loose waves floor-length, calm brown eyes sideways to the lens, warm ivory skin, human, silk kimono worn open, little bell riding the collar, large breasts, soft natural shape, mid_shadowhammock,",
         "the chest lifted onto both palms with the fingers gripping the floor's seams, nothing underneath the prone's arch but her own two hands' hold, the veil dress worn open, spread wide over the shadow's give — the held shadow is the claim, trust-made,",
         weave("Y168"),
         "the shadow sinking one and a half centimeters under the elbows' weight, a readable stretch and no more, the kimono worn open, sleeves wings of light over both sides, a second shadow sitting by the wall on guard duty,",
         "both palms flat beneath the chest's line, elbows soft, the bell answering the shadow's slow breathing,",
         "prone, chest lifted onto both palms, elbows soft, head relaxed back, the spine one long question,",
         "the room's ordinary floor refusing to be ordinary where her shadow spreads, the veils' three opacities throwing three different shades of her, the ceiling plain and innocent of all this,",
         pal_line("P81_FAWN_FOLD", "the hold she was born with"),
     ],
     negx=" shadow flat, palms empty, bell still",
     face="stylized 2D anime face sideways to the lens, anime eyes (calm brown, half-lidded trust), small nose, small mouth at rest, one loose wave pooling at the cheek.",
     )

slot("P09", "windspirit-aercrawl", "EXQUISITE · R47 Wind-spirit-kin · R+ · Y359 · P27_VOID_STARLIGHT",
     channel="handbra-open-palms",
     corridor="A",
     thesis=("«ВЕТРЯНАЯ ДЕВА ПОЛЗЁТ ПО ВОЗДУХУ НА ЧЕТВЕРЕНЬКАХ — РУКИ И КОЛЕНИ СТОЯТ НИ НА "
             "ЧЁМ, ЛАДОНЬ НА ЛАДОНЬ ВЫШЕ ПОЛА, ПОДНОСНОЙ РЕМЕНЬ ЧЕРЕЗ СПИНУ НЕСЁТ ЧАЙ, "
             "И НИ ОДНА ЧАШКА НЕ ДРОЖИТ. ВОЗДУХ ПОД НЕЙ ПЛОТНЫЙ — КАК ВЫМЫТЫЙ ПАРКЕТ, "
             "И ОНА ДВИГАЕТСЯ ПО НЕМУ С ЛЕНЬЮ УБОРЩИЦЫ В НИЗКИЙ ЧАС. ЭТО НЕ ПОЛЁТ — "
             "ПОЛЗОК: ФИЗИКА СДАЛАСЬ ПЕРВЫМ, А ОНА ПРОСТО ЗАМЕТИЛА И ВНЕСЛА В ОБИХОД. "
         "ЗРИТЕЛЬ ВОСКЛИЦАЕТ — ЧАЙ ОСТАВАЕТСЯ В ЧАШКАХ»."),
     gag=("Гэг-стек: воздух под коленями держит отпечаток — «паркет вымыт»; бумаги "
          "предлагают себя ей сами — комната сквознячит под настроение; края "
          "преломляются тепло-дымкой; подносный ремень через спину держит три "
          "чашки и одно печенье, и всё это — тише, чем шаг."),
     spine="Y359 Air-Floor Crawl (camera from below looking up, combo→Y359, карта-стенд) · CAM— from below the air-floor · LEAD the crawled air · housekeeping register · full figure from below",
     race="R47 — ветряная дева: бумаги сами предлагают себя — комната сквознячит под настроение.",
     gar="CL-TS-07 (топ на открытых плечах, вырез — мягкий горизонт) + CL-DR-11 (льняной сарафан-фартук, нагрудник в плоском свете, плечи открыты) + поднос на ремне (объект карты — через спину) · HS: HS36 Wind-Blown Bob",
     stack=["CR-W42", "CR-B70", "CR-U13", "CR-D58"],
     ycard="Y359",
     pos=[
         "Masterpiece, best quality, absurdres, intricate details, camera from below looking up past the air-floor, full figure, crawling in mid-air a palm above the floor, 1girl, solo, her breast shape under the pinafore's flat-lit bib and the tray strap's line, silver-white hair in a wind-blown bob, pale amber eyes dipped to the point below, mist-pale skin, translucent air-current edges, wind spirit girl, human face, tall slender body, small breasts, mid_aercrawl,",
         "the tray strap's torque across the chest's bare line where the bib's edge ends, nothing underneath the crawl's hang but the air's own floor — the crawled air is the claim, housekeeping-made,",
         weave("Y359"),
         "both palms flat on the air's polished parquet, knee-prints holding behind her like a washed floor's memory, three cups and one biscuit riding the tray without a tremor, a signal whistle clipped to the strap, papers offering themselves from every desk,",
         "the off-shoulder top's soft horizon riding the crawl's sway, the strap's torque honest across the shoulder blades,",
         "hands and knees resting on nothing, face dipped toward the point below,",
         "the room's floor a polite half-meter away and utterly uninvolved, the air's grain showing where her weight taught it to behave, the ceiling's one star of daylight keeping her company,",
         pal_line("P27_VOID_STARLIGHT", "the floor that isn't"),
     ],
     negx=" air gone, cups spilt, knees on floor, papers settled",
     face="stylized 2D anime face dipped toward the point below, anime eyes (pale amber, on the drop), small nose, small mouth on the count of cups, one wind-blown edge of hair refracting.",
     )

slot("P10", "salamander-weatherstake", "VOLT · R22 Flame-salamander-kin · R+ · Y452 · P121_STOPPED_GREEN",
     channel="tape-only",
     corridor="A",
     thesis=("«САЛАМАНДРА СТАВИТ МЕЖУ ПОГОД: КОЛ ВБИВАЕТСЯ ПЛОСКИМИ УДАРАМИ ЛАДОНИ — МОЛОТОК "
             "ОТДЫХАЕТ В ТРАВЕ, ПОСКОЛЬКУ СЛУЖБА ДЕЛАЕТСЯ ТЕЛОМ. ПО ОДНУ СТОРОНУ КОЛА "
             "ИДЁТ ДОЖДЬ, ПО ДРУГУЮ ЖАРИТ — И ЛИНИЯ МЕЖИ ПОСЛУШНА. ЧЕШУЙКИ-УГЛИ ГАСНУТ НА "
             "СТОРОНЕ ДОЖДЯ И ГОРЯТ НА СТОРОНЕ ЖАРА — ЖИВОЙ ИНДИКАТОР МЕЖИ. НА ГРУДИ КРЕСТ "
             "ИЗ МЕЖЕВОЙ ЛЕНТЫ: ГРАНИЦУ НОСЯТ НА СЕБЕ, ПОКА СВЕЖАЯ. ЧТО ЭТО ЗА КОЛ "
             "ТАКОЙ? — ЭТО КАРАНДАШ, ИМ ЖЕ ЧЕРТЯТ НЕБО»."),
     gag=("Гэг-стек: чешуйки-угли гаснут и разгораются с настроением — медленный румянец "
          "межи; рога-угли держат тёплую подсветку на стороне жара; молоток лежит в "
          "траве с биркой «запасной»; межевая лента на груди выцвела ровно до цвета "
          "прошлой границы."),
     spine="Y452 Weather-Stake Strikes (frontal eye-level camera, combo→Y452, карта-стенд) · CAM— frontal eye level · LEAD the staked weather · survey register · upper body",
     race="R22 — саламандра: пятна-чешуи гаснут и разгораются с настроением — медленный румянец углей.",
     gar="CL-UR-10 (кожаная сбруя-обвяз, геометрия теней, кожа между ремнями) + CL-DR-09 (юбка-тулевый подъюбник, ярусы заволакивают свет) + межевая лента крест-накрест на груди (третий сигнал tape-only) · HS: HS11 Silver Storm-Slick",
     stack=["CR-W48", "CR-S08", "CR-E32", "CR-M20"],
     ycard="Y452",
     pos=[
         "Masterpiece, best quality, absurdres, intricate details, frontal eye-level camera on the line, upper body, driving the boundary stake with flat palm-strikes, 1girl, solo, her breast shape crossed by the survey tape's bright X, ember-orange hair in a work-slick, ember-glow scale patches at the forearms, coal-black horns, amber eyes level on the line, ember-warm skin, salamander girl, human face, slender body, small breasts, mid_weatherstake,",
         "nothing underneath the harness' geometry but two weathers waiting their turn, a tape cross naming the fresh border over her chest's bare line — the staked weather is the claim, survey-made,",
         weave("Y452"),
         "the hammer resting unused in the grass with its spare-part tag, a surveyor's bracelet of brass links at one wrist, a hairpin through the work-slick, both palms flat on the stake's cap between strikes, the tulle hem's tiers holding rain on one side and heat-shimmer on the other,",
         "the scale-patches dimming at the rain side and glowing at the heat side, the tape X bright and new-laid,",
         "flat palm-strikes driving the stake deeper, the hammer resting unused in the grass,",
         "the rain-side's curtain stopping mid-air at an invisible wall, the heat-side's haze queuing politely behind it, the field's grass bending two directions at once and getting on with it,",
         pal_line("P121_STOPPED_GREEN", "the border she signs with her palm"),
     ],
     negx=" hammer in hand, tape fallen, weather mixed, scales cold",
     face="stylized 2D anime face level to the line, anime eyes (grey, surveyor-calm), small nose, small mouth on the strike's count, one tear-trail glinting like a plumb line.",
     )

slot("P11", "twoworlds-fare-count", "NICHE · human · R · Y250 · P177_GUTTER_CHAMPAGNE",
     channel=None, corridor="A",
     thesis=("«ПЕРЕВОЗЧИЦА МЕЖДУ МИРАМИ: ОДНА НОГА НА СТУПЕНИ, ДРУГАЯ НА ТРОТУАРЕ — "
             "АВТОБУС ХОДИТ МЕЖДУ ДВУМЯ МИРАМИ, И ПРОЕЗД ПЛАТЯТ МЕЛОЧЬЮ ЛЮБОГО "
             "ИЗ НИХ. МОНЕТЫ ДВУХ ВАЛЮТ ЛЕЖАТ В ОТКРЫТОЙ ЛАДОНИ ПОСЕРЕДИНЕ И НЕ "
             "ПУТАЮТСЯ, ПОТОМУ ЧТО ОНА НЕ ПОЗВОЛЯЕТ. ОДНА НОГА УЖЕ В ЗАВТРАШНЕМ "
             "МИРЕ, ВТОРАЯ ЕЩЁ ВО ВЧЕРАШНЕМ, ЗАРПЛАТА ИДЁТ ПО КУРСУ ОБЕИХ — КУРС "
             "ДЕРЖИТ ОНА ЖЕ. ЧТО ЭТО ЗА АВТОБУС? — РЕЙСОВЫЙ, ПРОСТО МАРШРУТ "
             "НЕСТАНДАРТНЫЙ»."),
     gag=("Гэг-стек: жетоны двух миров звонят по-разному — сдача считается на слух; "
          "компостер пробивает билет с обеих сторон сразу — двухвалютная аккуратность; "
          "вывеска маршрута дописывает себя при каждой посадке; в салоне слева — "
          "вчерашняя погода, справа — завтрашняя, пассажиры сидят по настроению."),
     spine="Y250 Two-Worlds Fare (upper body three-quarter, combo→Y250, карта-стенд) · CAM— three-quarter at the door's line · LEAD the two-currency fare · conductor register · upper body",
     race="— (human-служба темы: кондуктор междумирового рейса)",
     gar="форменный жилет кондукторши (вырез читает линию при полушаге) + сумка-монетница на ремне · HS: HS19 Pin-Curl Set",
     stack=["CR-B63", "CR-E36", "CR-D33", "CR-B68"],
     ycard="Y250",
     pos=[
         "Masterpiece, best quality, absurdres, intricate details, camera from above looking down, upper body, bending over the armrest toward the lens, 1girl, solo, one foot on the bus's step, the vest's fall reading her chest line between the two fares, dark copper hair in a pin-curl set, amber eyes on the count, warm skin, human, full broad-across frame, large breasts, mid_faretwo,",
         "the fare mid-count in the open palm, the vest's neckline holding her chest line at the door's own height while both worlds wait their change — the two-currency fare is the claim, conductor-made,",
         weave("Y250"),
         "the coins of two currencies ringing their different notes in one palm, a ticket punch clipping both sides at once out of manners, the route's sign rewriting itself at each boarding, the fare-bag's strap honest at the hip, a coin string of two worlds wrapped twice round it,",
         "one foot's weight given to the step's tomorrow, the other still holding the curb's yesterday, the count unhurried and exact,",
         "one foot on the bus's step, one still on the curb, fare mid-count in the open palm,",
         "the bus's left windows holding yesterday's weather and its right ones tomorrow's, the passengers seated by mood, the curb's yesterday and the step's tomorrow agreeing on exactly one fare at a time,",
         pal_line("P177_GUTTER_CHAMPAGNE", "the fare both worlds pay"),
     ],
     negx=" coins mixed, ticket one-sided, sign blank, step empty",
     face="stylized 2D anime face at the door's light, anime eyes (amber, mid-count), small nose, small mouth on the fare's number, one pin-curl loose at the brow."
     )

slot("P12", "clockwind-tape-x", "VOLT · human · R+ · Y334 · P234_EGLOMISE_CLOCK_GOLD",
     channel="tape-only",
     corridor="A",
     thesis=("«ЧАСОВЩИЦА ЗАВОДИТ ДВАДЦАТЬ ПЯТЫЙ ЧАС: ЦИФЕРБЛАТ БАШНИ ПОКАЗЫВАЕТ ЧИСЛО, "
             "КОТОРОГО НЕТ В СУТКАХ, — И ОНО ИДЁТ, ТИКАЯ, ПОТОМУ ЧТО ОНА ЕГО ЗАВЕЛА. "
             "РУКА ВКРУЧЕНА В ЗАВОДНОЙ КЛЮЧ, ДРУГАЯ ЛАДОНЬ ПЛОСКО НА СТЁКЛЕ ЦИФЕРБЛАТА, "
             "ПОДЪЁМ НА ЦЫПОЧКАХ ДЕРЖИТ ВСЮ ВЕРТИКАЛЬ. НА ГРУДИ — ВАСИ-ЛЕНТА С "
             "МИНУТНЫМИ ДЕЛЕНИЯМИ: СТРАХОВОЧНЫЙ КРЕСТ ВЫСОТНИЦЫ, ЗАМЕРЕННЫЙ ПО "
             "СОБСТВЕННОЙ ГРУДИ. ГОРОД УЖЕ СВЫКСЯ: НА ДВАДЦАТЬ ПЯТЬ ЧАСОВ ОТКРЫТЫ "
             "ТОЛЬКО ПУЛЬМАНОВЫЕ ПЕКАРНИ. ЧТО ЗА ЧАСЫ? — РАБОЧИЕ, ПРОСТО ИМ "
             "ДОБАВИЛИ СМЕНУ»."),
     gag=("Гэг-стек: ювелирная лупа на лбу держит лунный блик — подъёмный фонарик без "
          "прибора; татуировка-гиря на запястье — точка отсчёта подъёма; васи-лента с "
          "делениями наклеена крест-накрест — «уровень груди» по регламенту высоты; "
          "заводной ключ поворачивается с тем же скрипом, что и сто лет назад — "
          "единственный консерватор в городе."),
     spine="Y334 Clock-Wind Tiptoe (camera from below looking up, combo→Y334, карта-стенд) · CAM— from below the dial · LEAD the twenty-fifth hour · clockwork register · upper body from below",
     race="— (human-служба темы: часовщица 25-го часа — человек заводит невозможное)",
     gar="CL-UR-10 (кожаная сбруя высотницы, геометрия теней) + CL-TS-14 (топ-бандаж из эластичного бинта, спираль теней, тело читается сквозь) + васи-лента с минутными делениями крест-накрест (третий сигнал tape-only) · HS: HS41 Tool-Belt Ponytail",
     stack=["CR-W53", "CR-C09", "CR-E40", "CR-I12"],
     ycard="Y334",
     pos=[
         "Masterpiece, best quality, absurdres, intricate details, camera from below looking up the tower's face, upper body, on tiptoe at the tower clock face, 1girl, solo, her breast shape told by the bandage wrap's spiral in the dial's own glow, slate-grey hair in a tool-belt ponytail, amber eyes on the count, slate-warm skin, human, petite frame, small breasts, mid_clockwind,",
         "the washi tape's minute-marks crossing the chest's bare line in a clockmaker's X, nothing underneath the bandage's spiral but the hour being wound — the twenty-fifth hour is the claim, clockwork-made,",
         weave("Y334"),
         "one arm cranked into the winding key to the shoulder, her other palm flat on the dial's glass, a jeweler's loupe at her brow holding one moon-glint, one wooden hair stick through the ponytail, the harness' shadow-geometry honest against the dawn-blue face,",
         "both palms flat to the work between turns — one on the dial, one in the key's crank — the tiptoe's whole arch honest against the scaffold's rail,",
         "on tiptoe at the tower clock face, chin lifted, other palm flat on the dial,",
         "the dial showing XXV in fresh gilt nobody remembers voting for, the tower's pigeons holding the twenty-fifth hour as private overtime, the city below keeping one bakery open for it out of respect,",
         pal_line("P234_EGLOMISE_CLOCK_GOLD", "the hour she winds by hand"),
     ],
     negx=" loupe dark, dial blank, tape peeling",
     face="stylized 2D anime face up the dial's glow, anime eyes (amber, counting), small nose, small mouth on the last quarter-turn, one tool-belt strand swinging with the crank.",
     )

slot("P13", "lostproperty-collarfall", "VOLT · human · R+ · Y23 · P128_VIAL_AMBER",
     channel="tape-only",
     corridor="B",
     thesis=("«ЗАВЕДУЮЩАЯ СТОЛОМ НАХОДОК ПРЕДСТАВЛЯЕТ ЭКСПОНАТ: НА УГЛУ СТОЛА — ВЕЩЬ, "
             "КОТОРУЮ НЕ ОПОЗНАЛ НИ ОДИН ОТДЕЛ, А ОНА НАКЛОНЯЕТСЯ ЧЕРЕЗ УГОЛ К САМОЙ "
             "ЛИНЗЕ, ОБЕ ЛАДОНИ ПЛОСКО НА ДЕРЕВЕ, ГУБЫ У ВЕРХНЕЙ КРОМКИ КАДРА "
             "СЕРЕДИНОЙ ШЁПОТА — И НА ГРУДИ ЕЁ ЛЕНТА-ОПОЗНАНИЕ: ТАК МЕТЯТ ТО, ЧТО "
             "ЕЩЁ ИЩЕТ ХОЗЯИНА. ВЕЩЬ НА СТОЛЕ ТИХО ДЫШИТ СВЕТОМ. ГОРОД ПРИНОСИТ "
             "СТРАННОЕ К НЕЙ КАК К ПОСЛЕДНЕЙ ИНСТАНЦИИ: ОПОЗНАННОЕ — ЗАБИРАЮТ, "
             "НЕОПОЗНАННОЕ — ОСТАЁТСЯ И ЗАРЫВАЕТСЯ В ТЕТРАДЬ. ЧТО ЭТО ТАКОЕ НА "
             "СТОЛЕ? — ВОТ И ОНА ХОЧЕТ ЗНАТЬ, ПОЭТОМУ ШЕПЧЕТ»."),
     gag=("Гэг-стек: тетрадь находок с резинкой — резинка перегружена; на вещи "
          "сидит бирка «ждёт» и чуть светится в такт; ящик стола заперт на "
          "свисток — свисток у неё на шее; лента-опознание на груди закручена "
          "бантом, как подарок, который сам себя подарил."),
     spine="Y23 Find-Rail Collar-Fall (slight low angle, combo→Y23, карта-стенд) · CAM— slight low, up the rail's edge · LEAD the unclaimed find · lost-property register · upper body",
     race="— (human-служба темы: заведующая столом находок)",
     gar="CL-TS-04 (тонкая ребристая майка, бретельки честные и узкие) + CL-LG-01 (оверсайз-рубашка для сна, полы на бёдрах, ворот сползает с плеча) + лента-опознание бантом на груди (третий сигнал tape-only) · HS: HS24 Pencil Through Bun",
     stack=["CR-W55", "CR-C14", "CR-E48", "CR-D64"],
     ycard="Y23",
     pos=[
         "Masterpiece, best quality, absurdres, intricate details, slight low angle up the counter-rail, upper body, leaning across the finds-rail into the lens zone, 1girl, solo, her breast shape named by the claim-tape's bow, ink-black hair in a bun with a pencil through it, hazel eyes turned fully to the lens, warm skin, human, medium breasts, slim waist, hourglass figure, mid_findtable,",
         "nothing underneath the sleep shirt's borrowed drift but the find's own breathing light, a claim-tape bow naming the unclaimed across her chest's bare line — the unclaimed find is the claim, lost-property-made,",
         weave("Y23"),
         "the find sitting in its evidence square, breathing its slow light, tagged waiting and glowing in time, the ledger's rubber band over-stretched to honesty, the shirt's hem at the thighs and drifting, a whistle-key at her throat for the locked drawer,",
         "her fist gripping the counter-rail's edge where the collar fell, the ribbed tank's straps honest and narrow under the shirt's drift,",
         "the collar's fall held by one finger, face turned fully to the lens mid-whisper,",
         "the lost-property room's shelves holding their surrendered oddities patient as a jury, the rail's whole length dedicated to the one unclaimed glow, the queue outside bringing one more impossible thing to file,",
         pal_line("P128_VIAL_AMBER", "the strange the city brings home"),
     ],
     negx=" find dark, tape straight, drawer open, whisper ended",
     face="stylized 2D anime face to the lens, slight low, anime eyes (hazel, presenting), small nose, small mouth mid-whisper of the find's name she doesn't have yet, one pencil-strand loose at the temple.",
     )

slot("P14", "crane-liftlibrary", "NICHE · R51 Crane-kin · R · Y287 · P197_WILLOW_MORN",
     channel=None, corridor="—",
     thesis=("«БИБЛИОТЕКА, ГДЕ КНИГИ ЛЕГЧЕ ВОЗДУХА: ЖУРАВЛИНАЯ БИБЛИОТЕКАРША НЕСЁТ СТОПКУ "
             "В ОБНИМКУ, ОДИН ТОМ — В ЗУБАХ, И СТОПКА ТЯНЕТ ВВЕРХ, А НЕ ВНИЗ — "
             "ПЕРЕСОРТИРОВКА ИДЁТ ПО ЗАКОНУ АРХИМЕДА, ТОЛЬКО ПЕРЕВЁРНУТОГО. КОЛЕНО "
             "ВЫСОКО НА ЛЕСТНИЦЕ, ПЛИССИРОВАННАЯ ЮБКА КОЛЕШЕТСЯ ПО ВЕТРУ БУМАЖНЫХ "
             "СТРУЙ, ПОД ЮБКОЙ — НИЧЕГО, КРОМЕ ТАТАМИ-УТРА. ЧИТАТЕЛИ НИЖЕ НЕ УДИВЛЯЮТСЯ: "
             "ЗДЕСЬ ДАЖЕ СПРАВОЧНИК ПО ТЯЖЕСТИ ВЕСИТ МЕНЬШЕ ВОПРОСА. ЧТО ЭТО ЗА "
             "БИБЛИОТЕКА? — ОБЫЧНАЯ, ПРОСТО С ГРАВИТАЦИЕЙ НА ВЫБОРЕ ЧИТАТЕЛЯ»."),
     gag=("Гэг-стек: белое оперение на предплечьях листается само, как страницы; "
          "хвостовые перья держат равновесие стопки — третий противовес; том в "
          "зубах — «Тяжесть бытия, том 2», самый лёгкий в фонде; лестничные "
          "пролёты пронумерованы римскими цифрами задом наперёд."),
     spine="Y287 Book-Bite Climb (upper body three-quarter, combo→Y287, карта-стенд) · CAM— three-quarter up the stairs · LEAD the weightless stack · library register · upper body",
     race="R51 — журавлиная: складывается в неподвижность, как бумага — оригами из плоти.",
     gar="лёгкая плиссированная юбка-миди (колошется бумажными струями, под ней ничего) + накидка-карриган библиотекарши · HS: HS39 Pin-Straight Low Tail",
     stack=["CR-B74", "CR-L22", "CR-D48", "CR-C15"],
     ycard="Y287",
     pos=[
         "Masterpiece, best quality, absurdres, intricate details, upper body angled through the stairwell's climb, stack of books in arms, 1girl, solo, the pleats' swing reading her breast line upward against the paper-draft, paper-white hair in a pin-straight low tail, red-crowned eye level on the next landing, warm ivory skin, white feather growth at the arms and nape, crane girl, long tail-feathers, human face, small breasts, slim hips, slender body, mid_liftlibrary,",
         "the pleated hem riding the stair's climb with nothing underneath the swing but the morning's tatami-hush, the stack pulling her upward by its own levity — the weightless stack is the claim, library-made,",
         weave("Y287"),
         "the held volume titled gravity vol. 2 between her teeth, cover lighter than the bite, round reading glasses folded at the collar, a signet ring on the page-turning thumb, white feathers at the forearms riffling themselves like turned pages, the tail-feathers counterweighting the stack's sway,",
         "the cardigan's drape given to the draft, one knee high on the next riser, the whole climb a crane's walk,",
         "one book held in teeth, climbing stairs, knee high,",
         "the stairwell's paper-drafts running upward in a slow gold current, the shelves floating their sections at fetch-height for the polite, the reading room below where the dropped books have to be shooed back down,",
         pal_line("P197_WILLOW_MORN", "the lightness she files daily"),
     ],
     negx=" feathers ruffled, stack heavy, book closed, stairs crowded",
     face="stylized 2D anime face over the bitten spine, anime eyes (red-crowned, on the landing), small nose, small mouth holding the volume, one paper-draft lifting the low tail's tip.",
     )

slot("P15", "rainwall-neon-cami", "VOLT · human · R+ · Y82 · P178_OILSLICK_CHROME",
     channel="wet-sheer-delivery",
     corridor="A",
     thesis=("«ПОСЛЕ ЛИВНЯ СТЕНА ЕДИНСТВЕННАЯ СУХАЯ, И ОНА ПРИНЯЛА ЭТО КАК ПРЕДЛОЖЕНИЕ: "
             "СПИНА ПЛОСКО К КИРПИЧУ, ЛАДОНИ ПРИЖАТЫ ЗА БЁДРАМИ, БЁДРА ГРАДУС ВПЕРЁД, "
             "ГОЛОВА НАКЛОНЕНА — ЛИНИЯ ГОРЛА ЧИТАЕТ УЛИЦУ. МАЙКА ПРОМОКЛА ДО ВТОРОЙ "
             "КОЖИ, БРЕТЕЛЬКИ ДЕРЖАТ ГОЛУЮ ЛИНИЮ ГРУДИ, НЕОН ПЕРЕСЕКАЕТ ЗОНУ ЗАЯВКИ "
             "БИРЮЗОЙ И МЕДЬЮ — СВЕТ ИДЁТ ПО МАЙКЕ, КАК ПО РЕКЕ. ЭТО НЕ ВИТРИНА — "
             "ПЕРЕДЫШКА: ГОРОД МОКРЫЙ, ОНА СУХАЯ ТОЛЬКО ИЗНУТРИ, И ЭТОГО ХВАТАЕТ»."),
     gag=("Гэг-стек: помочи висят расстёгнутые — качаются в такт стекающей воде; "
          "капли с карниза идут по её следу на стене — сухой силуэт-микрофон; "
          "неоновая вывеска за углом мигает ровно её дыханию (совпадение, "
          "конечно); каблук чертит на асфальте малый круг терпения."),
     spine="Y82 Rainwall Spine (upper body three-quarter, combo→Y82, карта-стенд) · CAM— three-quarter along the wall · LEAD the neon-dried line · interlude register · upper body",
     race="— (human-служба темы: горожанка после ливня)",
     gar="CL-TS-04 (тонкая ребристая майка, промокла насквозь, бретельки честные и узкие) + CL-DR-04 (хлопковый сарафан на тонких бретелях, сполз с плеч) + CL-AC-09 (помочи на весу) · HS: HS33 Wet Slick Low Bun",
     stack=["CR-W60", "CR-B15", "CR-E52", "CR-M22"],
     ycard="Y82",
     pos=[
         "Masterpiece, best quality, absurdres, intricate details, upper body three-quarter along the brick, spine flat to the wall, 1girl, solo, her breast shape borne by the ribbed tank's soaked honesty, river-brown hair in a rain-slick low bun, grey eyes level at the street, fair skin rain-cooled, human, flat chest, soft middle, wide hips, mid_rainwall,",
         "the ribbed tank's straps carrying the chest's bare line under the neon's own light, nothing underneath the soaked rib but the street's slow drying, the sundress's hem slipped to both elbows' crook — the neon-dried line is the claim, interlude-made,",
         weave("Y82"),
         "loose suspenders swinging their two dry arcs, one copper ear cuff taking the neon's trawl, a beauty mark under the eye level with the street, the neon's teal and copper crossing the claim-zone in one slow trawl, a wet silhouette of her own shoulders left on the brick like a signed receipt,",
         "both palms pressed back against the wall beside the hips, hips pushed a degree forward into the street's business,",
         "spine flat to the wall, hips pushed a degree forward, head tilted to expose the throat's line,",
         "the street's gutter running its whole storm downhill at once, the awnings dripping their applause, the crossing's reflections laid out flat as spilled signage,",
         pal_line("P178_OILSLICK_CHROME", "the dry line she keeps"),
     ],
     negx=" tank dry, neon off, palms forward, hair blown",
     face="stylized 2D anime face tilted to the street, anime eyes (grey, level), small nose, small mouth at rest, one wet strand mapping the jaw.",
     )

slot("P16", "tanuki-mobius-waistband", "VOLT · R36 Tanuki-kin · R+ · Y6 · P152_LEATHER_TANNERY_AMBER",
     channel="strap-line-hold",
     corridor="B",
     thesis=("«ТАНУКИ-ФОКУСНИЦА ПОКАЗЫВАЕТ ТРЮК «МЁБИУС»: ПОЯС САРОНГА ПОЛУСКРУЧЕН ПОД "
             "ОБОИМИ БОЛЬШИМИ ПАЛЬЦАМИ, НАТЯЖЕНИЕ ПРИКАЛЫВАЕТ ТКАНЬ НИЗКО НА БЁДРАХ — "
             "И ВТОРОЙ КРАЙ ТКАНИ, СЛЕДУЯ ЗАКРУТКЕ, САМ ВЫРАСТАЕТ БРЕТЕЛЬЮ ЧЕРЕЗ "
             "ГОЛУЮ ЛИНИЮ ГРУДИ. ОДНА ПОЛОСА ТКАНИ — И ПОЯС, И ЛЯМКА: ШВА НЕТ, "
             "ШВА НЕТ, ПОНЯТИЯ «ВНУТРИ НАРУЖУ» ТОЖЕ НЕТ. ОНА КЛЯНЁТСЯ, ЧТО ЭТО "
             "МАСТЕРСТВО, А НЕ ЧУДО, И ПРИСЯГУ ПРИНИМАЮТ ТЕ, КТО ХОТЬ РАЗ ПРОБОВАЛ "
             "ПОВЯЗАТЬ САРОНГ НА ВЕТРУ. ЧТО ЭТО БЫЛО? — ГЕОМЕТРИЯ, ПРОСТО ОНА "
             "ПРОБУЖДЕНА ВЕЧЕРОМ»."),
     gag=("Гэг-стек: лист-гаман на поясе балансирует монетку — фокус «уплата вперёд»; "
          "хвост-кисточка держит равновесие закрутки, как юла; кружевная перчатка "
          "на одной руке — вторая «ушла в шов»; в кармашке саоронга — свёрнутая "
          "лента с меткой «возврату подлежит»."),
     spine="Y6 Mobius Waistband (cowboy shot from below, combo→Y6, карта-стенд) · CAM— low along the waistband's line · LEAD the one-band trick · illusionist register · mid body from below",
     race="R36 — тануки: её монетные фокусы с листом на носу не падают никогда — она клянётся, что это мастерство.",
     gar="CL-SK-08 (саронг-обмотка низко на бёдрах, диагональные складки) + CL-BT-05 (хлопковые шорты для дома, подол задирается к бедру) + CL-LG-05 (полотенце-обмотка, держится последним подворотом) · HS: HS26 Twin-Tail Foxloops",
     stack=["CR-W63", "CR-S11", "CR-L10", "CR-I15"],
     ycard="Y6",
     pos=[
         "Masterpiece, best quality, absurdres, intricate details, cowboy shot from below along the waistband's line, mid body, the sarong's half-rolled band under both thumbs, 1girl, solo, her breast shape strung on the band's own second edge, chestnut-brown hair in twin-tail foxloops, warm brown eyes drinking the light, warm tan skin, tanuki girl, round tanuki ears, thick fluffy tail, human face, large breasts, soft belly, hourglass figure, mid_mobiusband,",
         "the half-rolled waistband's edge reeled up into a single strap-line over the chest's bare line, nothing underneath the wrap's diagonal but the trick's own tension — the one-band trick is the claim, illusionist-made,",
         weave("Y6"),
         "a leaf-coin pendant on its green string balanced at the waistband's roll, the tail-tip spinning counterweight to the twist, one lace glove at the near hand while the far hand claims it went into the seam, a return-tag tucked in the fold,",
         "the wrap's diagonal honest across the hip's bone, both thumbs' roll paying out the tension low and slow,",
         "the waistband half-rolled under both thumbs, the roll's tension pinning the fabric low on the hips,",
         "the evening room's floorboards running their grain the wrong way in sympathy, the paper screen's shadow showing the band's far side already tied in a knot that isn't there yet, the audience of one coin flipping itself for attention,",
         pal_line("P152_LEATHER_TANNERY_AMBER", "the seam she swears by"),
     ],
     negx=" tail still, coin dropped, band straight, glove paired",
     face="stylized 2D anime face down the band's line, anime eyes (warm brown, mid-wink), small nose, small mouth on the trick's count, one foxloop swinging with the reeling.",
     )

slot("P17", "bedmemory-crawl", "NICHE · human · R · Y93 · P230_PERFUME_SMOKE_NIGHT",
     channel=None, corridor="—",
     thesis=("«КРОВАТЬ ПОМНИТ ЕЁ СНЫ И ТЯНЕТСЯ СЛЕДОМ: ОНА ПОЛЗЁТ ПО ОДЕЯЛУ К КРАЮ, "
             "КОЛЕНО ОБГОНЯЕТ КОЛЕНО, А ПРОСТЫНЯ ТЯНЕТСЯ ЗА ЗАДНЕЙ РУКОЙ ВЯЗКИМ "
             "ВОСПОМИНАНИЕМ — НЕ ОТПУСКАЕТ, ПОКА НЕ ДОСМОТРИТ. ПЛЕЧИ НИЗКИЕ И РОВНЫЕ, "
             "ГРУДНАЯ ЛИНИЯ ЧИТАЕТСЯ СКВОЗЬ ПОВОРОТ, ДЫШИТ ЛЁГКОЙ ДЫМОЧНОСТЬЮ "
             "СНА. УТРОМ ПРОСТЫНЮ СВЕРНУТ И УСПОКОЯТ, А СЕЙЧАС ОНА ДОЛЖНА ДОПОЛЗТИ "
             "ДО КРАЯ — ТАМ, ГДЕ ЕЁ ЖДЁТ ЧАШКА, КИПЯЧЁННАЯ СОБСТВЕННЫМ ТЕРПЕНИЕМ. "
             "ЧТО ЭТО ЗА ПРОСТЫНЯ? — ЧИТАТЕЛЬ СНОВ, ПРОСТО ЕЙ НРАВИТСЯ ЭТА ГЛАВА»."),
     gag=("Гэг-стек: простыня держит форму её сна — по складке читается сюжет; "
          "второй подушки больше нет — ушла досматривать; духи-дымка висят "
          "отдельной занавесой и не мешают; след на одеяле остаётся тёплым "
          "на девять минут ровно."),
     spine="Y93 Dreamsheet Crawl (upper body three-quarter, combo→Y93, карта-стенд) · CAM— three-quarter down the bed's length · LEAD the remembered sheet · morning register · upper body",
     race="— (human-служба темы: та, чья постель читает сны)",
     gar="ночная рубашка на бретельках (бретель съехала в повороте) + простыня-воспоминание в задней руке (объект карты) · HS: HS61 Loose Sleeping Braid",
     stack=["CR-B58", "CR-E16", "CR-D56", "CR-B72"],
     ycard="Y93",
     pos=[
         "Masterpiece, best quality, absurdres, intricate details, upper body tilted down the bed's slope, crawling toward the viewer, 1girl, solo, the sheet's drag reading her breast line through the turn, wheat-blonde hair in a half-undone morning braid, sleep-grey eyes half-in the dream, sleep-warm skin, human, chubby, plump build, large breasts, mid_bedmemory,",
         "the sheet dragging from the trailing hand as one slow memory, her breast line given to the crawl's low turn, the dream still folded at the sheet's far corner — the remembered sheet is the claim, morning-made,",
         weave("Y93"),
         "the nightshirt's slipped strap marking the shoulder the dream left last, a hair ribbon loose at the braid's end, sleep freckles across the nose, the second pillow's dent already gone to finish watching, a perfume-smoke curtain hanging apart from the business,",
         "both shoulders low and level, the trailing hand's grip honest in the linen, one knee advancing past the other,",
         "one knee advancing past the other, a sheet dragging from the trailing hand,",
         "the bed holding her warmth-prints nine minutes exactly, the duvet's hills settling like a read story, the kettle's distant note counting her patience at the far edge,",
         pal_line("P230_PERFUME_SMOKE_NIGHT", "the dream the linen keeps"),
     ],
     negx=" sheet flat, strap righted, braid tight, bed empty",
     face="stylized 2D anime face toward the viewer low, anime eyes (morning-grey, half-in the dream), small nose, small mouth on the cup's thought, one braid-loop dragging its own memory.",
     )

slot("P18", "kettlesunrise-counter", "VOLT · human · R+ · Y411 · P77_LATE_MILK",
     channel="wet-sheer-delivery",
     corridor="A",
     thesis=("«ЧАЙНИК ВСХОДИТ: ИЗ НОСИКА ИДЁТ НЕ ПАР — РАССВЕТ, МАЛЕНЬКИЙ И ПОЛНЫЙ, "
             "С ЛИЧНЫМ ГОРИЗОНТОМ И ЧАСТНОЙ ЗОРОЙ. ОНА ОТКИНУЛАСЬ СПИНОЙ К БУФЕТУ, "
             "УХОДЯ ОТ ЭТОГО ВОСХОДА, ПОДСНОЖНИКОВЫЙ СВЕТ ПРОСВЕЧИВАЕТ СОРOЧКУ "
             "НАСКВОЗЬ, ПОДНОС НА ЛАДОНИ — ЗАВТРАК ПОДАН НА ОБОИХ. БРЕТЕЛЬКИ "
             "ДЕРЖАТ ГОЛУЮ ЛИНИЮ ГРУДИ, СВЕТ ЛОЖИТСЯ ПРЯМО НА ЗОНУ ЗАЯВКИ, КАК "
             "В КАТАЛОГЕ ДОСТАВКИ. КОРОБКА ЧАЯ ГОВОРИТ «БОДРЯЩИЙ» — НИКОГДА ЕЩЁ "
             "НЕ БЫЛО ТАК БУКВАЛЬНО. ЧТО ЭТО ЗА ЧАЙНИК? — СВЕТОВОЙ, ЗАВОДСКОЙ, "
             "С ГАРАНТИЕЙ УТРА»."),
     gag=("Гэг-стек: у рассвета из носика есть свои мини-лучи — по расписанию "
          "подъёма; бант-чокер на горле повязан бантовой лентой от коробки "
          "чая; на подносе — две чашки и один тост, тост тоже с поджаркой-зарёй; "
          "вуалевое платье-халат распахнуто, ярусы держат утренний свет, как "
          "молочные полки."),
     spine="Y411 Kettle-Dawn Counter (camera from above looking down, combo→Y411, карта-стенд) · CAM— from above the counter · LEAD the spouted dawn · breakfast register · upper body",
     race="— (human-служба темы: кухарка рассветов)",
     gar="сорочка (объект карты — тонкая, просвечена носиковым светом) + CL-DR-10 (вуалевое платье-халат поверх, распахнуто) + CL-AC-02 (бант-чокер из чайной ленты) + поднос на ладони · HS: HS14 Braid-Crown, Flour-Dusted",
     stack=["CR-W25", "CR-C11", "CR-E57", "CR-M12"],
     ycard="Y411",
     pos=[
         "Masterpiece, best quality, absurdres, intricate details, camera from above at the kettle's counter, upper body, leaning back against the counter away from the kettle's sunrise, 1girl, solo, her breast shape backlit through the chemise by the spout-light, wheat-gold hair in a braid-crown flour-dusted, brown eyes on the pour, warm kitchen skin, human, tall soft waist, medium breasts, mid_kettledawn,",
         "the chemise's straps framing the chest's bare line in the spout-light's own aim, nothing underneath the dawn-damp weave but the morning's first pour, the veil coat worn open and tiered with light — the spouted dawn is the claim, breakfast-made,",
         weave("Y411"),
         "a bow-ribbon choker tied from the tea-box's own ribbon, flour freckles across the forearm's lift, the tray riding one palm with two cups and a toast browning to the same dawn, the kettle's mini-rays fanning their schedule across the shelf,",
         "both palms flat under the tray's balanced weight, the counter's edge taking her lean, the light landing on the claim-zone like a catalog promise,",
         "thin chemise backlit through by the spout-light, breakfast tray on palm,",
         "the kitchen's shelves holding their jars of yesterday, the window still deciding whether to compete, the whole small dawn steaming politely upward from the spout in gold,",
         pal_line("P77_LATE_MILK", "the morning she pours"),
     ],
     negx=" kettle steaming plain, chemise opaque, tray empty, choker untied",
     face="stylized 2D anime face into the pour's gold, anime eyes (brown, on the schedule), small nose, small mouth on the first sip's word, one flour-dust fleck at the brow.",
     )

slot("P19", "phoenix-firedoor", "EXQUISITE · R34 Phoenix-kin · R+ · Y366 · P35_VOID_EMBER",
     channel="element-linen",
     corridor="A",
     thesis=("«ПОЖАРНАЯ ДВЕРЬ ВЫПУСКАЕТ СМЕНУ: ФЕНИКС ВЫХОДИТ ИЗ НЕЁ СРЕДИ ШАГА, ВОЛОСЫ "
             "ПОЛНЫ ЖИВОГО ОГНЯ — ПЛАМЯ ЖИВЁТ В ПРЯДЯХ, КАК ШАРФ, И НЕ ЖЖЁТ СВОЮ "
             "ХОЗЯЙКУ: ОНИ ЗАКЛЮЧИЛИ ДОГОВОР ТЫСЯЧУ ЛЕТ НАЗАД И НЕ РАЗОРВАЛИ НИ "
             "РАЗУ. ЛАДОНЬ ВЕДЁТ ЛИНИЮ ОГНЯ ВДОЛЬ СТЕНЫ, КАК КРАЙ ЗАНАВЕСА, "
             "КУЛАК ДЕРЖИТ ЕГО КРАЙ У КЛЮЧИЦЫ — ОГОНЬ ДРАПИРУЕТ ГРУДЬ, КАК "
             "ЕДИНСТВЕННАЯ ТКАНЬ ВЕЧЕРА. ТРИКОТАЖНЫЙ УЗЕЛ РАСПАХНУТ, САРАФАН-ФАРТУК "
             "РАССТЁГНУТ ДО БЁДЕР. ЗА ДВЕРЬЮ — СМЕНА ПОЖАРА, ПЕРЕД НЕЙ — УЛИЦА, "
             "И ОБА МИРА УВАЖАЮТ ФОРМУ»."),
     gag=("Гэг-стек: огонь в волосах идёт по прядям, как по инструкции причёски — "
          "ни один волос не пострадал; линия огня на стене остаётся тёплой "
          "подписью на девять минут; фартук-нагрудник висит на одной завязке — "
          "смена кончилась; пепел на пороге сложен в аккуратную горку — "
          "собирает его сама смена."),
     spine="Y366 Fire-Door Shift-End (frontal eye-level camera, combo→Y366, карта-станд) · CAM— frontal eye level down the street · LEAD the living scarf · shift-end register · full figure mid-stride",
     race="R34 — феникс: когда она в ярости, волосы светятся, как последние угли — комната теплеет.",
     gar="CL-TS-03 (хлопковый топ узлом у рёбер, узел распахнут) + CL-DR-11 (льняной сарафан-фартук, расстёгнут до бёдер) + линия живого огня (объект карты — драпирует грудь, держится кулаком) · HS: HS55 Ember Gradient Wolfcut",
     stack=["CR-W54", "CR-A13", "CR-U15", "CR-D59"],
     ycard="Y366",
     pos=[
         "Masterpiece, best quality, absurdres, intricate details, frontal eye-level camera, full figure mid-stride, walking out of a fire door mid-stride, 1girl, solo, her breast shape draped by the fire-line's living hem, ember-red gradient hair in a wolfcut full of live flame, ember-amber eyes on the street ahead, warm-gradient skin, phoenix girl, ember-tipped feathers at the shoulders, human face, tall soft build, medium breasts, soft waist, mid_fireshift,",
         "her fists hauling the fire-line's hem closed at the collarbone, nothing underneath the fire's weave but its own kept word, the knotted tee worn open beneath the drape — the living scarf is the claim, shift-end-made,",
         weave("Y366"),
         "the linen pinafore unbuckled to the hips and hanging by one tie, ember ear cuffs at the lobes, the flame running the strands like a hairdresser who signed a contract, the wall's fire-line staying warm nine minutes as her signature,",
         "one palm trailing the fire's edge along the wall at walk pace, the ember-tips holding their patience,",
         "hair full of live flame, one palm trailing a line of fire along the wall,",
         "the fire door's exit sign of scorch marks spelling someone's honest overtime, the street's evening traffic slowing a beat in respect, the ash heaped neatly at the threshold by the shift itself,",
         pal_line("P35_VOID_EMBER", "the word the fire keeps"),
     ],
     negx=" flame gone, hair smoking, tee knotted, pinafore buckled",
     face="stylized 2D anime face to the street, anime eyes (ember-amber, off-duty calm), small nose, small mouth on the shift's last word, one ember-tipped strand waving goodbye to the door.",
     )

slot("P20", "headwind-private", "NICHE · human · R · Y85 · P80_SALT_APPETITE",
     channel=None, corridor="—",
     thesis=("«ВЕТЕР ДУЕТ ТОЛЬКО НА НЕЁ: ЛИЧНЫЙ ВСТРЕЧНЫЙ, ШАГАЮЩИЙ РЯДОМ, КАК ПРИКРЕПЛЁННЫЙ "
             "К НЕЙ КОНТРАКТОМ. СРЕДНИЙ ШАГ УХОДИТ В НАКЛОН, ШЛЯПА ПРИЖАТА РУКОЙ, "
             "ДРУГАЯ ЛАДОНЬ ПЛОСКО НА ЮБКЕ, УШЕДШЕЙ ВБОК, ПАЛЬТО ЗВОНКО ОТКИНУТО. "
             "ГОРОД СТОИТ В ШТИЛЬ — МЕТЕОСТАНЦИЯ ПИШЕТ «ЯСНО, БЕЗОБИДНО», И ТОЛЬКО "
             "ОДИН КВАДРАТ УЛИЦЫ ЖИВЁТ ПОГОДОЙ. ВЕТЕР — ЕЁ, ПОДПИСАН И ЗАПЛАЧЕН "
             "ОДНОЙ ЛИШНЕЙ УЛЫБКОЙ В ПРОШЛОЙ ЖИЗНИ. ЧТО ЭТО ЗА ВЕТЕР? — СОТРУДНИК, "
             "ПРОСТО ОЧЕНЬ ПРИВЯЗАННЫЙ»."),
     gag=("Гэг-стек: подол уходит вбок строго по направлению ветра — как стрелка "
          "компаса; листья выстраиваются за ней в очередь, не смея обогнать; "
          "шляпа держится на одной левой руке — правая занята юбкой; на "
          "асфальте её квадрат улицы полит — ветер приносит с собой прилив."),
     spine="Y85 Private Headwind (upper body three-quarter, combo→Y85, карта-станд) · CAM— three-quarter into the gust · LEAD the private weather · commuter register · full figure mid-stride",
     race="— (human-служба темы: хозяйка личного ветра)",
     gar="лёгкое пальто навыпуск (звонко откинуто) + юбка-миди на поясе (ушла вбок) + соломенная шляпа · HS: HS58 Scarf-Anchor Ponytail",
     stack=["CR-B20", "CR-L24", "CR-D61", "CR-C19"],
     ycard="Y85",
     pos=[
         "Masterpiece, best quality, absurdres, intricate details, upper body three-quarter against the gust, full figure mid-stride, mid-stride leaning into a headwind, 1girl, solo, the wind's dome pressing the coat to her breast shape like weather with an agenda, sea-salt blonde hair in a scarf-anchor ponytail, green eyes narrowed ahead, fair wind-flushed skin, human, slim athletic build, medium breasts, mid_privatewind,",
         "the wind reading her breast shape against the pinned coat like a letter it already opened, the walk itself almost losing and refusing to — the private weather is the claim, commuter-made,",
         weave("Y85"),
         "the skirt's whole drape gone sideways like a compass needle with opinions, leaves queueing behind her at a respectful distance, one hand pinning the hat brim down to its job,",
         "the coat belled back and ringing with the gust, the free palm flat to the skirt's argument,",
         "one hand pinning a hat, the other flat to a skirt gone sideways, coat belled back,",
         "the street's other squares holding their still heat honestly, the crosswalk's stripes lying flat for everyone but her, the distant harbor windsock pointing at her block and only her block,",
         pal_line("P80_SALT_APPETITE", "the wind she pays for"),
     ],
     negx=" wind still, hat held, skirt down, coat buttoned",
     face="stylized 2D anime face into the gust, anime eyes (green, narrowed to a squint of habit), small nose, small mouth breathing with it, one salt strand drawn straight back.",
     )

slot("P21", "medusa-organpipe", "VOLT · R40 Medusa-kin · R+ · Y451 · P51_RAIN_STAINED_GLASS",
     channel="wet-sheer-delivery",
     corridor="A + B",
     thesis=("«ОРГАННАЯ ТРУБА ПОЁТ БЕЗ ОРГАНА: ОДНА, ВЫШЕ ДОМА, И ГОЛОС ИДЁТ ИЗ САМОЙ "
             "МЕДИ — КОНДЕНСАТ СТЕКАЕТ ПО МЕТАЛЛУ РУЧЬЯМИ, И ОНА СТОИТ В ЭТОМ "
             "ПОТОКЕ, ЛАДОНЬ ОПУСКАЕТСЯ НА ТРУБУ, КАК НА КОЛОННУ СОБРА. ЗМЕИ-ВОЛОСЫ "
             "ВТОРЯТ АККОРДАМ, КАЖДАЯ — СВОЯ ПАРТИЯ. МОКРАЯ ТОНКАЯ СОРОЧКА ВТОРОЙ "
             "КОЖЕЙ, БРЕТЕЛЬКИ ДЕРЖАТ ГОЛУЮ ЛИНИЮ ГРУДИ, СВЕТ ВИТРАЖА ЛОЖИТСЯ ПРЯМО "
             "НА ЗОНУ ЗАЯВКИ. НЕФИЛИМСКИЕ ХОРАЛЫ ВЫКЛЮЧЕНЫ — ИГРАЕТ ЛИЧНЫЙ КОНЦЕРТ "
             "ДЛЯ ОДНОЙ ТРУБЫ. ЧТО ЭТО ЗА МУЗЫКА? — КОНДЕНСАТ, ПРОСТО ОН УМЕЕТ "
             "ПЕТЬ»."),
     gag=("Гэг-стек: каждая змея-прядь держит свою ноту — партия расписана по "
          "чешуйкам; ладонь на трубе оставляет тёплый отзвук-отпечаток; "
          "влажный след по трубе идёт вверх, против стекания — труба пьёт "
          "сама; чешуйки на висках мерцают в такт."),
     spine="Y451 Organ-Column Palm (frontal eye-level camera, combo→Y451, карта-стенд) · CAM— frontal, up the pipe · LEAD the singing brass · concert register · full figure",
     race="R40 — медуза: её змеи-волосы смотрят на собеседника — все и сразу.",
     gar="CL-TS-03 (хлопковый топ узлом у рёбер, вымок от конденсата) + CL-SM-07 (гидрокостюм, спущен до талии, рукава вне) + сорочка-подклад (объект мокрой доставки, просвечена) · HS: HS46 Serpent Braid-Cascade",
     stack=["CR-W56", "CR-B28", "CR-E61", "CR-I18"],
     ycard="Y451",
     pos=[
         "Masterpiece, best quality, absurdres, intricate details, frontal eye-level camera up the pipe's height, full figure, standing at the single organ pipe taller than her, 1girl, solo, her breast shape reading through the condensate-damp chemise in the stained-glass aim, sea-jade green hair in a serpent braid-cascade, gold-green eyes on the brass, olive-warm skin at the scaled temples, medusa girl, snake-hair tendrils, human face, hourglass figure, large breasts, soft belly, mid_organpipe,",
         "the chemise's straps pinning the chest's bare line beneath the pipe's cold stream, nothing underneath the running condensate but the note being held, the wetsuit shucked at the waist, its sleeves gone — the singing brass is the claim, concert-made,",
         weave("Y451"),
         "her crooked arm to the pipe's height with the palm flat on the metal like on a cathedral column, each snake-tendril holding its own line of the chord, the wet trace climbing the brass against the drip,",
         "one palm settling on the metal like on a column, her stance a slow settle of weight, the stained light walking the claim-zone in slow procession,",
         "standing at the single organ pipe taller than her, one palm settling on the metal like on a column,",
         "the pipe's mouth far above breathing its pedal note into the street's hush, the condensate running a bright ring around its foot, the stained window trading its saints' colors for the duration,",
         pal_line("P51_RAIN_STAINED_GLASS", "the note held in her palm"),
     ],
     negx=" snakes still, pipe silent, chemise dry, wetsuit up",
     face="stylized 2D anime face up the brass, anime eyes (gold-green, on the held note), small nose, small mouth humming the octave below, one serpent tendril swaying to its own part.",
     )

slot("P22", "memorial-warmth-slide", "VOLT · human · R+ · Y480 · P47_PORCELAIN_LACQUER",
     channel="handbra-open-palms",
     corridor="A",
     thesis=("«ПАМЯТЬ ГРЕЕТ: МЕМОРИАЛЬНАЯ СТЕНА С ДВУМЯ ВЫСЕЧЕННЫМИ ИМЕНАМИ ТЕПЛА НА "
             "ОЩУПЬ, И ОНА СПУСКАЕТСЯ ПО ЭТОМУ ТЕПЛУ, КАК ПО СПИНКЕ СТАРОГО КРЕСЛА — "
             "ЛАДОНИ ПЛОСКО ПО КАМНЮ ПОБОКУ ОТ БЁДЕР, ЗАБИРАЯ ХОЛОД ОБОИХ. ЛОКОНЫ "
             "СМЫКАЮТСЯ НА ГОЛОЙ ЛИНИИ ГРУДИ, СЪЕХАВШИЙ ПОДОЛ ДЕРЖИТ ТОЛЬКО ТРЕНИЕ "
             "О КАМЕНЬ. ИМЕНА НЕ ЕЁ — НО СТЕНА ПРИНЯЛА ЕЁ КАК СВОЮ, И ЭТОГО "
             "ДОСТАТОЧНО ДЛЯ ОБОИХ. ЧТО ЭТО ЗА СТЕНА? — ПАМЯТЬ, ПРОСТО С "
             "ОБОГРЕВОМ»."),
     gag=("Гэг-стек: тёплые буквы читаются ладонью на проходе — брайль памяти; "
          "цветочные бумажки у подножия сложены самолетиками — кто-то из "
          "вечных шутит; лаковый бант на запястье оставлен кем-то из "
          "посетителей; стена держит тепло ровно до второго имени — дальше "
          "мрамор снова мрамор."),
     spine="Y480 Warm-Memorial Slide (camera from above looking down, combo→Y480, карта-стенд) · CAM— from above, down the wall · LEAD the heated memory · vigil register · full figure sliding",
     race="— (human-служба темы: та, кому стена отдаёт тепло)",
     gar="CL-DR-12 (вечернее платье-комбинация на открытой спине, паетки — душа монет) + CL-TS-01 (блузка с бантом, сползла с плеч узлом к запястьям) + CL-AC-03 (золотая цепь в ложбинке) · HS: HS09 Soft Over-One Braid",
     stack=["CR-W47", "CR-B35", "CR-E30", "CR-M13"],
     ycard="Y480",
     pos=[
         "Masterpiece, best quality, absurdres, intricate details, camera from above along the memorial wall, full figure, sliding down the memorial wall, 1girl, solo, her breast shape covered by her own hair's spill in the lacquer light, ink-black hair in a soft over-one braid, quiet grey eyes on the names, porcelain-pale skin, human, stomach fold at the slide, soft belly, medium breasts, mid_memorialslide,",
         "her hair's spill covering the chest's bare line after the straps gave up, nothing underneath the slid wrap's ride but the stone's kept warmth, the sequins running their coin-shower down the open back — the heated memory is the claim, vigil-made,",
         weave("Y480"),
         "both palms flat on the stone beside her hips taking the wall's patient heat, the tie-collar blouse knotted loose at both wrists behind her, a lacquer brooch of remembrance pinned to it, the sequins' fall sliding off the open back, a gold chain pooling in the clavicle's notch, the paper planes of old flowers nosediving soft at the base,",
         "the wall's warmth running out exactly at the second name, her weight given to the slide's slow meter,",
         "sliding down the memorial wall beside the two cut names, taking the wall's cold,",
         "the memorial's letters holding their body-heat like a signature the stone kept, the square's evening crowd giving the wall its polite distance, the two names lit by nothing and warm anyway,",
         pal_line("P47_PORCELAIN_LACQUER", "the warmth the stone kept"),
     ],
     negx=" wall cold, hair short, names unreadable, blouse worn",
     face="stylized 2D anime face to the names' height, anime eyes (quiet grey, reading by touch of light), small nose, small mouth at rest with the wall, one ink strand crossing the warm letters.",
     )

slot("P23", "goat-oneskate", "NICHE · R09 Goat-kin · R · Y173 · P63_GLACIER_BREACH",
     channel=None, corridor="B",
     thesis=("«КАТОК НАД ВОДОЙ, И ВОДА СВЕТИТСЯ: ЛЁД ПРОЗРАЧНЫЙ, ПОД НИМ — ТЕЧЕНИЕ С "
             "ФОСФОРНЫМИ РУЧЬЯМИ, И ОНА СКОЛЬЗИТ НА ОДНОМ КОНЬКЕ, РУКИ СКРЕЩЕНЫ ЗА "
             "СПИНОЙ, ПОДБОРООДОК ВЫСОКО, ШАРФ НЕСЁТ СКОРОСТЬ. ХВОСТ-УДАЧА "
             "ЧИТАЮТ ТЕЧЕНИЯ ПОД ЛЬДОМ КАК ГОРНЫЕ ТРОПЫ — РАВНОВЕСИЕ ГОРНОЙ ПОРОДЫ. "
             "ВТОРОЙ КОНЁК У НЕЁ ЕСТЬ — ОН ПРОСТО ПРИВИЛЕГИЯ, А НЕ НЕОБХОДИМОСТЬ: "
             "РАБОТАЕТ И НА ОДНОМ ЛЕЗВИИ. ВТОРОЙ КОНЁК — ПРОСТО ПРИВИЛЕГИЯ. ЧТО ЭТО ЗА ЛЁД? — "
             "ОКОННЫЙ, ПРОСТО ЕГО ЗАБЫЛИ ВСТАВИТЬ В РАМУ»."),
     gag=("Гэг-стек: горизонтальные зрачки читают течения подо льдом — прямоугольная "
          "навигация; рожки стучат лёгкий протест на виражах — бод-кивок удачи; "
          "второй конёк висит на пояске — «выходной»; ушко поворачивается на "
          "каждое течение подо льдом."),
     spine="Y173 One-Blade Glide (wide environmental shot, combo→Y173, карта-стенд) · CAM— wide along the ice · LEAD the single edge · rink register · full figure gliding",
     race="R09 — козочка: слегка бодает дверные косяки, когда недовольна — стук протеста.",
     gar="тёплое платье-свитер для катка (юбка колышется скоростью) + шарф-стремительность + конёк-одиночка · HS: HS31 Ears-Through Braids",
     stack=["CR-B30", "CR-L20", "CR-I22", "CR-C16"],
     ycard="Y173",
     pos=[
         "Masterpiece, best quality, absurdres, intricate details, wide environmental shot along the ice, full figure, mid-glide on one blade, 1girl, solo, the blade's wind peeling the sweater-dress to her chest line, snow-white hair in ears-through braids, goat-gold eyes with rectangular pupils, cream-warm skin, goat horns, goat ears, goat girl, human face, medium breasts, flat stomach, healthy build, mid_oneblade,",
         "the glide's own wind reading her chest line through the sweater's knit like a fortune being told, the speed honest and on one edge only — the single edge is the claim, rink-made,",
         weave("Y173"),
         "the spare skate hanging from a hip-ribbon on its day off, a bone hairpin through each braid, one ear swiveling to each stream under the ice, the horns tapping a light knock of protest at each hard turn, her braids mapping the streams' pull,",
         "both arms crossed behind the back in old rink discipline, the chin high, the scarf streaming the speed's full argument,",
         "mid-glide on one blade, arms crossed behind the back, chin high, the scarf streaming the speed,",
         "the phosphor streams under the clear ice running their own races, the rink's far shore holding its benches of breathers, the second blade's outline pressed in the ice somewhere back — unused and proud of it,",
         pal_line("P63_GLACIER_BREACH", "the edge she keeps one of"),
     ],
     negx=" horns dull, ears flat, second blade worn, scarf slack",
     face="stylized 2D anime face high against the cold, anime eyes (goat-gold, rectangular, on the long arc), small nose, small mouth breathing the glide's rhythm, one braid-tip streaming with the scarf.",
     )

slot("P24", "rooftop-invisible-steps", "VOLT · human · R+ · Y363 · P236_SPRAY_DRIP_ROOFTOP",
     channel="contact-physics",
     corridor="A",
     thesis=("«НЕВИДИМАЯ ЛЕСТНИЦА: ОНА ОТТАЛКИВАЕТСЯ ЛАДОНЬЮ ОТ ПЕРИЛ КРЫШИ И ШАГАЕТ "
             "ВНИЗ ПО ВОЗДУХУ — СТУПЕНИ ЕСТЬ, ИХ ПРОСТО НЕ ВИДНО, НО ОНИ ЗВУЧАТ: "
             "КАЖДЫЙ ШАГ ОТЗЫВАЕТСЯ ГРАВИЕЙ НАКЛЕЕННОЙ БУМАЖКОЙ. ТЕЛО СЛОЖЕНО "
             "ПОЛЁТОМ ВПЕРЁД, ЛИЦО СРЕЗАНО НАЗАД К ЛИНЗЕ, САРАФАН НАТЯНУТ ВЕТРОМ "
             "ВСПЫШКОЙ, БРЕТЕЛЬКИ ДЕРЖАТ ГОЛУЮ ЛИНИЮ ГРУДИ. ГРУДЬ ВСТРЕЧАЕТ "
             "ХОЛОД ПЕРИЛ В СКЛАДКЕ НАКЛОНА — И УХОДИТ ДАЛЬШЕ, ПО СВОЕЙ "
             "ЛЕСТНИЦЕ. ЭТО НЕ ПАДЕНИЕ — СПУСК: РАБОЧИЙ МАРШРУТ КУРЬЕРШИ, КОТОРАЯ "
             "ЗНАЕТ ДОРОГУ, НЕВИДИМУЮ ПРОЧИМ. ЧТО ЭТО ЗА СТУПЕНИ? — СЛУЖЕБНЫЕ, "
             "ПРОПУСК ВЫДАН ВЕТЕРОМ»."),
     gag=("Гэг-стек: на невидимых ступенях остаются звуковые метки — шуршащие "
          "квититочки воздуха; сарафан держит вспышку-парус только на спуске — "
          "по маршруту; помочи отстёгнуты и поют две ноты; в руке — свёрнутая "
          "квитанция, брошенная вниз, долетает раньше неё."),
     spine="Y363 Air-Stair Vault (wide environmental shot, combo→Y363, карта-стенд) · CAM— wide, down the invisible flight · LEAD the unlisted stairs · courier register · full figure in flight",
     race="— (human-служба темы: крышная курьерша невидимым маршрутом)",
     gar="CL-DR-04 (хлопковый сарафан на тонких бретелях, ветер держит вспышкой) + CL-TS-07 (топ на открытых плечах) + CL-AC-09 (помочи на весу, поют две ноты) · HS: HS48 Wind-Thread High Tail",
     stack=["CR-W59", "CR-B62", "CR-U21", "CR-D16"],
     ycard="Y363",
     pos=[
         "Masterpiece, best quality, absurdres, intricate details, wide environmental shot down the invisible flight, full figure, mid-stride vault off a rooftop rail, 1girl, solo, her breast shape meeting the rail's cold in the fold and released, copper-red hair in a wind-thread high tail, sky-grey eyes cut back to the lens, city-tan skin, human, tall soft build, medium breasts, mid_airstairs,",
         "the off-shoulder top's straps crossing the chest's bare line mid-vault, nothing underneath the sundress's flashed bell but the route's own wind, her fists hauling the hem's edge taut for balance — the unlisted stairs is the claim, courier-made,",
         weave("Y363"),
         "flight goggles parked on the crown, a courier's wrist-guard buckled at one wrist, loose suspenders singing their two free notes off the hips, each invisible step leaving its paper-rustle receipt in the air, the folded delivery slip already gliding below to beat her down,",
         "one palm flat on the rail's last cold inch, the body folded forward in flight, face cut back toward the lens,",
         "one palm flat on the rail, body folded forward in flight, face cut back toward the lens,",
         "the alley's depth opening under her heel-politeness, the fire-escape landings she ignores hanging their rusty honesty, the evening pigeons giving way to the schedule they somehow know,",
         pal_line("P236_SPRAY_DRIP_ROOFTOP", "the route only she can see"),
     ],
     negx=" stairs visible, rail held, sundress still, suspenders clipped",
     face="stylized 2D anime face cut back to the lens, anime eyes (sky-grey, mid-wink of the route), small nose, small mouth on the count of steps, one wind-thread strand writing a note in the air.",
     )

# ══════════════════ EXP P25–P33: 9 кандидатов в ОС · комбо у потолка R+ · волна 14 ══════════════════
# В42: EXP = полка гипотез (H-XX в строке ТЕСТ), тема партии клетки не кастует;
# заказ автора «9 кандидатов × 9 комбо у потолка × 9 палитр» исполнен КАК гипотезы:
# кандидат-механика = H-13 (пара P27/P28), остальные клетки несут свободные
# гипотезы полки (≤2 клеток на гипотезу — закон A/B).

slot("P25", "porcelain-tailgate-dusk", "EXP · R15 Porcelain-doll · R+ · Y147 · P270_GLASSBITE_MINT",
     channel=None, corridor="A",
     thesis=("«ФАРФОРОВАЯ КУКЛА НА ОПУЩЕННОМ БОРТУ ГРУЗОВИКА: КАБИНА СДАНА В СМЕНУ, "
             "ЗАДНИЙ БОРТ — ЕЁ ТРИБУНА, ПЯТКИ ВЫСТУКИВАЮТ ПО БАМПЕРУ ЧАСОВОЙ РИТМ, "
             "ЛАДОНИ УПИРАЮТСЯ В СТАЛЬ ПОЗАДИ, ЛИЦО — К ПОСЛЕДНЕМУ ЦВЕТУ НЕБА. "
             "ГИДРОКОСТЮМ СПУЩЕН ДО ТАЛИИ, МАЙКА-РЕЗИНКА ВТОРОЙ КОЖЕЙ, ШАРНИРЫ "
             "БЛЕСТЯТ ВЕЧЕРНЕЙ ГЛАЗУРЬЮ. ПОЗА ДЕРЖИТСЯ НА ПОЛСЕКУНДЫ ДОЛЬШЕ "
             "ЧЕЛОВЕЧЕСКОЙ — ПРИВЫЧКА ВИТРИННОЙ ПОЛКИ, И ЭТА ПОЛСЕКУНДА — САМАЯ "
             "ЖИВАЯ ВЕЩЬ НА СКЛАДЕ»."),
     gag=("Гэг-стек (канон-ран ≥3): 1) поза держится на полсекунды дольше — привычка "
          "выставочной полки; 2) шарнирные швы ловят вечер блик-глазурью; 3) на "
          "борту мелом написано её сменное имя — «Фарфор, смена 2»; 4) кабина "
          "гудит домом — холодильник внутри тоже сменился."),
     test=("ТЕСТ (⚗ H-12: mid-action против статики — фаза действия как переменная): "
           "пятки стучат по бамперу В СЕРЕДИНЕ такта, локоны догоняют голову, "
           "последний цвет неба ловится в глазури шарниров на середине наклона. "
           "Проверка: пятки в такте, шарниры в блике, поза на полсекунды длиннее"),
     spine="Y147 Tailgate Half-Second (eye level, combo→Y147, карта-стенд) · CAM— eye level along the steel · LEAD the held half-second · display register · full figure seated",
     race="R15 — фарфоровая кукла: держит позы на полсекунды дольше — привычка витринной полки.",
     gar="CL-TS-04 (тонкая ребристая майка, бретельки честные и узкие) + CL-SM-07 (гидрокостюм спущен до талии, рукава вне) · HS: HS53 Doll-Loop Twintails",
     stack=["CR-W58", "CR-B27", "CR-E13", "CR-D21"],
     ycard="Y147",
     pos=[
         "Masterpiece, best quality, absurdres, intricate details, eye level along the tailgate's steel, full figure, sitting on a dropped tailgate, 1girl, solo, her breast shape kept by the ribbed tank's soaked strap-line, white porcelain hair in doll-loop twintails, glaze-blue eyes to the last color, porcelain skin, doll seam lines, ball joints, porcelain doll, human face, very slender, flat chest, narrow shoulders, mid_tailgatedusk,",
         "the wetsuit rolled to the waist, its sleeves empty, the neoprene's fold a slow peel at the hips, nothing underneath the tank's honest rib but the evening's cool, the strap taking the chest's bare line in glaze — the held half-second is the claim, display-made,",
         weave("Y147"),
         "both palms flat on the dropped steel taking the lean, the ball-joints' seams catching one hard glaze highlight each, ear studs winking their own glaze, a keyring of past shifts at the belt loop, heels tapping the bumper mid-beat, a chalk name on the tailgate reading shift two,",
         "the tank's rib reading ribs like a music box's drum, the hips' ball-joints ticking their half-second overtime,",
         "heels tapping the bumper, palms planted behind, face to the sky's last color,",
         "the yard's floodlights still warming up like stagehands, the truck's cab humming its domestic fridge-note, the last color holding exactly as long as she does,",
         pal_line("P270_GLASSBITE_MINT", "the half-second she keeps"),
     ],
     negx=" joints dull, heels still, tank opaque, last color gone",
     face="stylized 2D anime face up into the last color, anime eyes (glaze-blue, mid-hold), small nose, small mouth on the beat's end, one doll-loop ticking with the bumper's rhythm.",
     )

slot("P26", "moth-bededge-lookdown", "EXP · R16 Moth-kin · R+ · Y209 · P272_STATIC_LILAC",
     channel=None, corridor="A",
     thesis=("«МОТЫЛЁК НА КРАЮ ВЫСОКОЙ КРОВАТИ: ОНА ДОПОЛЗАЕТ КОЛЕНОМ К КРАЮ, "
             "ЛАДОНЬ СТУПАЕТ ЗА ГРАНЬ, ВЗГЛЯД ПАДАЕТ ВНИЗ ЧЕРЕЗ СВОБОДНЫЙ ВЫРЕЗ — "
             "НА ТОГО, КТО СНИЗУ, И ВЫРЕЗ РАБОТАЕТ РАМОЙ. КИМОНО ДЛЯ ПЛЯЖА "
             "РАСПАХНУТО И НЕ ЗАВЯЗАНО НИ РАЗУ, ЗОЛОТАЯ ЦЕПЬ ПЬЁТ КЛЮЧЕВОЙ СВЕТ, "
             "УСИКИ-АНТЕННЫ ВЕДУТ ПОИСК ТЕПЛА ВЕРТИКАЛЬНО. ОНА НЕ ПОЛЗЁТ К СМЕРТИ — "
             "ОНА ДОСТАВЛЯЕТ СЕБЯ, КАК ГРУЗ, И ГРУЗ ХОРОШ»."),
     gag=("Гэг-стек (канон-ран ≥3): 1) усики ведут вертикальный поиск — тепло "
          "определяется позицией; 2) крылья-пыльца держат обод — rims только на "
          "каемке; 3) ворсовый шейный воротник собирает ночную пыль в перстень; "
          "4) кимоно не завязано НИ РАЗУ за весь кадр — это принцип."),
     test=("ТЕСТ (⚗ H-10: композиция-носитель R+ — ракурс «от края вниз», героиня "
           "смотрит на зрителя снизу вверх): доставка R+ тащится РАКУРСОМ и "
           "взглядом (вырез как рама, зритель на полу), не тканью. "
           "Проверка: взгляд вниз-на-зрителя, вырез-рама, цепь в ключевом свете"),
     spine="Y209 Bed-Edge Lookdown (over the shoulder camera, combo→Y209, карта-стенд) · CAM— from above the edge, gaze reversed · LEAD the delivered gaze · freight register · upper body",
     race="R16 — мотылёк: дрейфует к теплу посреди фразы — лучший клиент любого свечения.",
     gar="CL-SM-10 (пляжное кимоно навыпуск, рукава широкие, не завязано) + CL-AC-03 (золотая цепь в ложбинке, звенья пьют ключевой свет) · HS: HS57 Antenne-Fringe Bob",
     stack=["CR-W50", "CR-C08", "CR-L01", "CR-M11"],
     ycard="Y209",
     pos=[
         "Masterpiece, best quality, absurdres, intricate details, over the shoulder camera down the bed's height, upper body, knee-crawling to the edge of a high bed, 1girl, solo, her breast shape framed by the neckline's fall at the viewer below, dusk-silver hair in an antennae-fringe bob, moth-eye amber aimed low, moth-dust pale skin, fuzzy moth collar, moth girl, dust-silver wings, moth antennae, human face, tall, medium breasts, soft waist, mid_bededge,",
         "the beach kimono worn open and never once tied, nothing underneath the loose neckline's drop but the aim of it, her fists pinning the hem at the mattress edge — the delivered gaze is the claim, freight-made,",
         weave("Y209"),
         "a moth-wing pendant at the throat, gold chain in the valley drinking the key light link by link, the wing-dust rims holding their glow only at the edges, the antennae triangulating warmth straight down,",
         "both palms flat in the crawl's work, one planted past the edge into the air's trust, the knees' crawl honest on the spread,",
         "one palm planted past the edge, gaze dropped down the loose neckline at the viewer below,",
         "the room's low floor holding its viewer-sized patch of light, the bed's height playing cathedral to a moth, the whole delivery run on one unwavering aim,",
         pal_line("P272_STATIC_LILAC", "the aim she delivers by"),
     ],
     negx=" antennae still, kimono tied, wings spread, gaze away",
     face="stylized 2D anime face down through the neckline's frame, anime eyes (moth-amber, on the one below), small nose, small mouth mid-landing, one fringe-strand triangulating with the antennae.",
     )

slot("P27", "oni-panel-overtime", "EXP · R24 Oni-kin · R+ · Y342 · P277_SORBET_STAIN",
     channel=None, corridor="A",
     thesis=("«ОНИ-ЭЛЕКТРИК НА СВЕРХУРОЧНОЙ СМЕНЕ: ОТКРЫТАЯ ПРОВОДНАЯ ПАНЕЛЬ, ОНА "
             "НА ЧЕТВЕРЕНЬКАХ, ОТВЁРТКА ЛЕЖИТ НА ЛАДОНИ ПЛОСКО, ПОЗВОНОЧНИК — "
             "ЛИНИЯ ЩИТА, ОДНО КОЛЕНО ПОДВЁРНУТО. ГИДРОКОСТЮМ СПУЩЕН, УЗЕЛ "
             "ТРИКОТАЖА ДЕРЖИТ ЛИНИЮ ГРУДИ, РОЖКИ ПОСТУЧАЛИ ПО РАМЕ ДВАЖДЫ — "
             "НА УДАЧУ, КАК ВСЕГДА. ЩИТ ЖИВЁТ СВОЕЙ ЖИЗНЬЮ, НО ПРОВОДИТ ТОК "
             "ТОЛЬКО ЧЕРЕЗ НЕЁ: ГАРАНТИЯ ЗАВЕДЕНИЯ — РАБОТНИЦА НЕ ГОРИТ»."),
     gag=("Гэг-стек (канон-ран ≥3): 1) рожки стучат по раме дважды на входе — на "
          "удачу, всегда; 2) они-румянец пылает ярче, когда щит доволен; 3) "
          "отвёртка на ладони — тестовая, стерильная, моется по этикету; 4) "
          "колокольчик на ошейнике звенит в ритм прозвона."),
     test=("ТЕСТ (⚗ H-13: кандидат-клетка A — бандл раса-гиммик × типаж × палитра "
           "волны 14 × комбо у потолка находит забираемого персонажа): "
           "они-электрик с рожками на удачу и румянем-индикатором. "
           "Проверка: рожки по раме, румянец горит, колокольчик в такт прозвона"),
     spine="Y342 Panel Overtime (camera from below looking up, combo→Y342, карта-стенд) · CAM— from below the panel · LEAD the live shift · electrician register · full figure on all fours",
     race="R24 — они: рожки стучат по дверному косяку дважды на входе — она клянётся, что на удачу.",
     gar="CL-TS-03 (хлопковый топ узлом у рёбер) + CL-SM-07 (гидрокостюм спущен до талии, рукава вне) + CL-AC-06 (колокольчик на ошейнике — в такт прозвону) · HS: HS43 Horn-Clear High Tail",
     stack=["CR-W41", "CR-B16", "CR-E34", "CR-I01"],
     ycard="Y342",
     pos=[
         "Masterpiece, best quality, absurdres, intricate details, camera from below looking up into the open panel, full figure, on hands and knees at an open wiring panel, 1girl, solo, her breast shape carried on the knotted tee's strap-line, storm-red hair in a horn-clear high tail, ember eyes on the circuit, blush-warm skin, oni blush lit like a gauge, small horns, oni girl, human face, full breasts, soft belly, round middle, mid_panelovertime,",
         "the wetsuit down at the waist, sleeves empty, nothing underneath the strap-line's honesty but the shift's own hum, the strap over the chest's bare line ringing with the panel's live note — the live shift is the claim, electrician-made,",
         weave("Y342"),
         "a sterile screwdriver flat on the palm as the etiquette demands, both palms flat on the panel's frame one at a time, the horn-tap twice on entry for luck, the little bell keeping the continuity-test rhythm,",
         "the spine one long breaker-line, one knee drawn under, the blush-meter honest at the cheeks,",
         "screwdriver flat on the palm, spine long, one knee drawn under,",
         "the panel's guts glowing their patient amber routework, the workshop's floor dust settling in awe, the shift-board's chalk line growing one honest stroke,",
         pal_line("P277_SORBET_STAIN", "the shift that conducts through her"),
     ],
     negx=" horns untapped, blush cold, screwdriver held, panel dark",
     face="stylized 2D anime face into the circuit's glow, anime eyes (ember, on the live line), small nose, small mouth on the count of contacts, one high-tail strand lifting with the hum.",
     )

slot("P28", "bee-mossring-count", "EXP · R26 Bee-kin · R+ · Y428 · P275_URANIUM_GLASS_GLOW",
     channel=None, corridor="A",
     thesis=("«ПЧЕЛА-ИНВЕНТАРИЗАТОРША У МОХОВОЙ СТЕНЫ: ЛАДОНЬ ПРИЖАТА ПЛОСКО, ПАЛЬЦЫ "
             "СЧИТАЮТ КОЛЬЦА РОСТА ПО МЕРЕ ПРИБЫТИЯ — МОХ РАСТЁТ НА ГЛАЗАХ, КОЛЬЦА "
             "ПРИХОДЯТ ПО ОДНОМУ В МИНУТУ, И ОНА ИХ ОПРИХОДОВЫВАЕТ. СБРУЯ "
             "ГЕОМЕТРИИ ТЕНЕЙ, ПОД НЕЙ НИЧЕГО, КРОМЕ СЧЁТА; КРЫЛЫШКИ МУРЛЫЧУТ "
             "УДОВЛЕТВОРЕНИЕ — КОМНАТА ДОСТАТОЧНО ТЁПЛАЯ. СТЕНА ЗНАЕТ, СКОЛЬКО "
             "ЕЙ ЛЕТ, НИКТО НЕ ЗНАЕТ, ПОЧЕМУ ОНА РАСТЁТ ВПРАВО»."),
     gag=("Гэг-стек (канон-ран ≥3): 1) крылья дают радужный сдвиг только на прямом "
          "свету — инвентарная маркировка; 2) мурлыканье-жужжание стартует при "
          "достаточном тепле — термометр из себя; 3) хитиновые манжеты на "
          "запястьях звенят приписью; 4) кольцо роста, пришедшее в момент "
             "касания, отмечается усиками — галочка."),
     test=("ТЕСТ (⚗ H-13: кандидат-клетка B — бандл раса-гиммик × типаж × палитра "
           "волны 14 × комбо у потолка, A/B-пара с P27: одна механика промоции, "
           "разный регистр — щит против стены): пчела-инвентаризаторша. "
           "Проверка: пальцы считают кольца, мурлыканье в тепле, манжеты-припись"),
     spine="Y428 Moss-Ring Count (frontal eye-level camera, combo→Y428, карта-стенд) · CAM— frontal, close on the wall · LEAD the counted rings · inventory register · upper body close",
     race="R26 — пчела: тихое довольное жужжание стартует, когда комнате достаточно тепло.",
     gar="CL-UR-10 (кожаная сбруя, геометрия теней, кожа между как отрицательное пространство) + CL-AC-06 (колокольчик на ошейнике — отбивает минуты колец) · HS: HS45 Antennae-Crown Bun",
     stack=["CR-W38", "CR-S05", "CR-E10", "CR-D22"],
     ycard="Y428",
     pos=[
         "Masterpiece, best quality, absurdres, intricate details, frontal eye-level camera close on the moss wall, upper body, palm pressed flat on the moss-grown wall, 1girl, solo, her breast shape strung between the harness' shadow-lines, honey-blonde hair in an antennae-crown bun, nectar-brown eyes on the count, honey-toned skin, bee girl, antennae, thin chitin cuffs at the wrists, small wings, human face, hourglass figure, slim waist, medium breasts, mid_mosscount,",
         "the harness' geometry of shadows with nothing underneath but the wall's patient arithmetic, the chest's bare line read between the straps' crossings like a tally mark — the counted rings is the claim, inventory-made,",
         weave("Y428"),
         "both palms flat on the moss-grown stone as the rings arrive, fingers tallying each new growth-circle on the beat, the chitin cuffs chiming their small ledger-note, the little bell of the collar off for the count, the wings' rainbow sheen marking good light,",
         "the harness' gathering at the small of the back honest with the count's lean, the bell keeping minutes at the throat,",
         "palm pressed flat on the moss-grown wall, fingers counting the growth rings as they arrive,",
         "the moss wall growing rightward at its own lawful pace, the rings arriving one a minute like a heartbeat with paperwork, the room warm enough that even the count hums,",
         pal_line("P275_URANIUM_GLASS_GLOW", "the count that grows on her"),
     ],
     negx=" wings still, moss still, cuffs silent, count lost",
     face="stylized 2D anime face to the wall's slow ledger, anime eyes (nectar-brown, on the newest ring), small nose, small mouth on the minute's number, one antennae-bun strand ticking with the tally.",
     )

slot("P29", "cow-crossdraft-robe", "EXP · R27 Cow-kin · R+ · Y492 · P271_WAX_SEAL_OXBLOOD",
     channel=None, corridor="A",
     thesis=("«КОРОВКА В СКВОЗНЯКЕ ВЕСТИБЮЛЯ: ПОТОКИ ИДУТ С ДВУХ СТОРОН, ОНА СТОИТ "
             "В ПЕРЕКРЁСТКЕ, ОБЕ ЛАДОНИ ПРИЖИМАЮТ ПОЛЫ ХАЛАТА К ГРУДИНЕ, ПОДОЛ "
             "ИДЁТ КОНТР-КАЧКОМ ПРОТИВ КАЖДОГО ПОТОКА. ХВОСТ-КИСТОЧКА СЧИТАЕТ "
             "ТЕРПЕНИЕ — УЖЕ ВТОРОЙ ДЕСЯТОК, И ЭТО СЛЫШНО. УШИ РАЗВЕДЕНЫ ПО ОДНОЙ "
             "НА ПОТОК — СТЕРЕО-СЛУХ ПОГОДЫ, ГАРТЕР-ЛЕНТА НА БЕДРЕ ГОВОРИТ, ЧТО "
             "ПРИЛИЧИЕ ЗДЕСЬ ОПЦИОНАЛЬНО. ВЕС ПОГРУЖЁН В ПОДУШКУ ПОЗАДИ, "
             "НЕСИММЕТРИЧНО, КАК И ПОЛАГАЕТ»."),
     gag=("Гэг-стек (канон-ран ≥3): 1) хвост-флик считает терпение — все вокруг "
          "учатся читать; 2) одно ухо — на один поток, второе — на другой, "
          "стерео-слух двух погод; 3) гартер-лента на бедре — резинка кусается "
          "мягко, честность; 4) восковая печать на поясе халата — не вскрыта, "
          "но уже тает от сквозняка."),
     test=("ТЕСТ (⚗ H-11: анти-стерильность позы — тройка «несимметричный вес + "
           "вещь-механика + взгляд-вектор»): вес утонул в подушке наискось, "
           "халат — вещь в середине драки потоков, взгляд — через плечо в "
           "дальний поток. Контроль стерильности — сам кадр. "
           "Проверка: вес косой, халат в контр-качке, нимб мигает"),
     spine="Y492 Cross-Draft Robe (upper body three-quarter, combo→Y492, карта-стенд) · CAM— three-quarter into the draft's cross · LEAD the counter-sway · vestibule register · upper body",
     race="R27 — коровка: хвост-флик считает её терпение — все учатся читать.",
     gar="CL-DR-05 (хлопковый халат-платье на полпуговицы, пояс свободен, ворот открыт у горла) + CL-AC-10 (гартер-лента на бедре, резинка кусается мягко) · HS: HS40 Broken-Wing Braid",
     stack=["CR-W15", "CR-B33", "CR-U17", "CR-M17"],
     ycard="Y492",
     pos=[
         "Masterpiece, best quality, absurdres, intricate details, upper body three-quarter across the cross-draft, standing in the vestibule's two winds, 1girl, solo, her breast shape pressed to the robe's half-buttoned line by the opposing gusts, cream-blonde hair in a bell-braid, warm brown eyes on the far draft, warm cream skin, cow girl, cow ears, small rounded horns, cow tail with tuft, human face, large breasts, wide hips, huge soft build, mid_crossdraft,",
         "the shirt dress worn open to the draft's argument, its straps spanning the chest's bare line through the counter-sway, nothing underneath but the garter's honest bite, her fists hauling the wrap's edge closed at the sternum — the counter-sway is the claim, vestibule-made,",
         weave("Y492"),
         "a wax seal at the robe's belt already softening in the wind, one ear turned to each draft's testimony, the tail-flick counting patience out loud, the hem's arc answering both streams at once,",
         "both palms pressing the robe's wrap flat against the sternum between gusts, the weight sunk aslant into the cushion behind,",
         "both palms pressing the robe's wrap flat against the sternum, hem in counter-sway,",
         "the vestibule's two doors holding their two weathers politely ajar, the mosaic floor's arrows disagreeing about the exit, the whole crossing running on her one opinion,",
         pal_line("P271_WAX_SEAL_OXBLOOD", "the draft she disagrees with"),
     ],
     negx=" tail still, horns bare, robe buttoned, seal broken",
     face="stylized 2D anime face through the crossing winds, anime eyes (warm brown, on the far draft), small nose, small mouth mid-moo of protest swallowed into dignity, one cream strand flagging the winner.",
     )

slot("P30", "flower-mortar-kneel", "EXP · R31 Flower-kin · R+ · Y356 · P273_FOIL_BALLOON_COPPER",
     channel=None, corridor="A + B",
     thesis=("«ЦВЕТОЧНАЯ ДЕВА ЗА МЕЛКОЙ СМЕНОЙ: ОНА СТОИТ НА КОЛЕНЯХ НАД ТОЧКОЙ "
             "ПОМОЛА, ПЕСТ ОТЛОЖЕН НА КРАЙ СТУПКИ, ОБЕ ЛАДОНИ ПЛОСКО ПО ДОСКЕ "
             "ПОБОКУ, ГОЛОВА ОПУЩЕНА — СМОТРИТ ВНИЗ, ГДЕ ЖИЛКИ-ВЕНЫ ЛИСТА "
             "НАЛИВАЮТСЯ ЗЕЛЁНЫМ ПРИ КАЖДОЙ МЫСЛИ: РАСТЕНИЕ ПОМНИТ ВСЁ СОЛНЦЕ. "
             "ТЮЛЕВЫЙ ПОДОЛ ИМЕНОВАННОГО ПОДСЛОЯ — «ЛАВАНДА» — ГОВОРИТ СВОЁ ИМЯ "
             "КРАЕМ ВЫШИВКИ, КИМОНО РАСПАХНУТО. ЭТО НЕ АПОКРИФ — ЭТО РЕЦЕПТ, "
             "ЗАПИСАННЫЙ САМИМ РАСТЕНИЕМ»."),
     gag=("Гэг-стек (канон-ран ≥3): 1) жилки-вены наливаются зелёным при каждой "
          "мысли — рецепт виден на просвет; 2) именованный подслой "
          "«Лаванда» вышит по краю — подпись самой вещи; 3) лепестки на плечах "
          "держат медный отблеск — фольга в капле росы; 4) пест отложен — "
          "смена помола кончается, начинается смена чтения."),
     test=("ТЕСТ (⚗ H-09: named-underlayer-display — именованный подслой назван и "
           "показан): именованный нижний слой «Лаванда» — вышитая метка на "
           "краю, кимоно распахнуто, подслой показан и назван в кадре. "
           "Проверка: метка-вышивка читается, кимоно распахнуто, мысли всплывают"),
     spine="Y356 Mortar-Kneel Read (camera from below looking up, combo→Y356, карта-стенд) · CAM— from below the boards · LEAD the named underslip · recipe register · full figure kneeling",
     race="R31 — цветочная: поворачивается за солнцем весь день — всё растение помнит.",
     gar="CL-DR-09 (тюлевое платье-подъюбник, ярусы заволакивают свет) + CL-LG-04 (шёлковое кимоно навыпуск, оби свободно) + именованный подслой «Лаванда» (вышитая метка по краю) · HS: HS35 Gloss-Drip Short Bob",
     stack=["CR-W24", "CR-B29", "CR-L13", "CR-D26"],
     ycard="Y356",
     pos=[
         "Masterpiece, best quality, absurdres, intricate details, camera from below, along the boards' grain, full figure, kneeling above the point below, 1girl, solo, her breast shape riding the named underslip's strap-line in coppered light, petal-rose hair in a loose crown braid, pollen-gold eyes on the point, vine-vein skin lines backlit green, flower girl, petal growth at the shoulders and hair, human face, wide hips, soft middle, flat chest, mid_mortarkneel,",
         "the silk kimono worn open over the petticoat's named underslip, nothing underneath the named lavender but the morning's grind, the half-slip's straps riding the chest's bare line at the embroidery's own name — the named underslip is the claim, recipe-made,",
         weave("Y356"),
         "a wooden hair stick through the crown braid, pollen beads in hair at the temples, a lavender embroidery tag reading its own name at the slip's hem, both palms flat on the boards on either side, the vine-vein lines flushing green at each thought and settling like a read page, the pestle resting on the mortar rim off-duty,",
         "the tulle tiers holding the light in waterfalls around the kneel, the head dropped to look down where the recipe writes itself,",
         "pestle set aside on the mortar rim, both palms flat on the boards on either side, head dropped to look down,",
         "the floorboards' grain running copper where the gel's ripples foil it, the mortar's dark holding one last unsunk thought, the kitchen's morning shift paging through her like a ledger,",
         pal_line("P273_FOIL_BALLOON_COPPER", "the name she wears underneath"),
     ],
     negx=" veins empty, kimono tied, tag unstitched, pestle held",
     face="stylized 2D anime face dropped toward the point, anime eyes (pollen-gold, reading the recipe), small nose, small mouth on the last line, one gloss-drip strand curling into a note.",
     )

slot("P31", "shark-surf-hemline", "EXP · R23 Shark-kin · R+ · Y30 · P110_RIPOSTE_SILVER",
     channel=None, corridor="B",
     thesis=("«АКУЛЬЯ СМЕНА НА ПРИБОЕ: НАКАТ ПРИЖИМАЕТ НИЗ К АСФАЛЬТУ СУХОГО "
             "ПЛЯЖА, ОТЛИВ ТЯНЕТ ПОДОЛ В СЕРЕДИНЕ ПОДЪЁМА — ВОДА ИДЁТ ЛИШЬ ДО "
             "ТАЛИИ, ВЕРХ ОСТАЁТСЯ СУХИМ, И ЭТО НЕ НАСИЛИЕ, А ДОГОВОР С "
             "ЛУНОЙ-ПРИЛИВОМ. СПИННОЙ ПЛАВНИК РЕЖЕТ НАКАТ, ЖАБРЫ ЛОВЯТ ДЕВЯТЫЙ "
             "ВАЛ ЗАРАНЕЕ, УЛЫБКА ДЕРЖИТ СЛИШКОМ МНОГО ЗУБОВ ДЛЯ ЛИЧНОЙ ПОБЕДЫ. "
             "ОНА ПОЛУМОКРАЯ ТОЧНО ПО ЛИНИИ — КАК СЛЕД НА ПЕСКЕ, "
             "КОТОРЫЙ ВОЛНА РЕШИЛА ОСТАВИТЬ НАПОЛОВИНУ»."),
     gag=("Гэг-стек (канон-ран ≥3): 1) спинной плавник читает высоту наката "
          "позади неё — эхолот скорости; 2) жабры пробуют девятый вал заранее — "
          "прогноз по вкусу; 3) шнурок-бант на шортах развязывается на каждый "
          "девятый счёт; 4) в улыбке слишком много зубов, когда считает вслух — "
          "и ей всё равно."),
     test=("ТЕСТ (⚗ H-08: частичное мокрое состояние — мокрый подол при сухом "
           "верху): вода идёт ровно до талии, верх сухой, граница — как "
           "горизонт в миниатюре. Одна переменная — где граница. "
           "Проверка: подол мокрый, верх сухой, уши врозь, бант на девятом валу"),
     spine="Y30 Surfline Half-Soak (water-line from below, combo→Y30, карта-стенд) · CAM— from the waterline, low · LEAD the half-line · lifeguard register · full figure in the run-up",
     race="R23 — акула: слишком много зубов в улыбке, когда выигрывает — она знает, и ей всё равно.",
     gar="CL-SM-08 (пляжные шорты со шнурком-бантом, укороченный рашгард выше) + CL-SW-05 (кроп-пуловер до пупка, середина живота открыта) · HS: HS21 Lop-Ears Through Hair",
     stack=["CR-W52", "CR-B39", "CR-F09", "CR-D30"],
     ycard="Y30",
     pos=[
         "Masterpiece, best quality, absurdres, intricate details, from the waterline below, full figure, surf run-up at the dry beach's edge, 1girl, solo, her breast shape kept dry by the upper weave's honest cut, silver-grey hair slicked by spray, tide-pool blue eyes on the ninth wave, shark girl, dorsal fin at the spine, gill-slits at the ribs, shark tail, human face, sea-slate skin, slightly plump, soft belly, medium breasts, mid_surfhemline,",
         "the run-up sheeting the knit's lower half wet against the ribs' base with nothing underneath the wet hem's drag, her arms covering chest above the waterline, the swim straps' line across the chest's bare line, dry and level — the half-line is the claim, lifeguard-made,",
         weave("Y30"),
         "the dorsal fin reading the run-up's height behind her, the gill-slits tasting the ninth wave early, a lifeguard's whistle on the drawstring, the bow coming loose on every ninth count, the grin holding too many teeth for a personal victory,",
         "the ebb hauling the hem mid-lift while the shoulders stay dry as a verdict, the boundary honest at the waist's line,",
         "the ebb hauling the hem mid-lift, water-line from below,",
         "the dry beach's asphalt ending where her contract with the tide begins, the mirror of a puddle holding the whole sky at her feet, the ninth wave arriving on schedule and on name,",
         pal_line("P110_RIPOSTE_SILVER", "the line the tide respects"),
     ],
     negx=" fin flat, gills dry, upper wet, bow tied",
     face="stylized 2D anime face against the spray, anime eyes (tide-pool blue, on the ninth), small nose, small mouth on the wave's name with the grin's full ledger of teeth, one gill-slit fluttering with the count.",
     )

slot("P32", "skunk-iceline-caustic", "EXP · R60 Skunk-kin · R+ · Y32 · P278_LEDGER_GREEN",
     channel=None, corridor="B",
     thesis=("«СКУСИХА И КУБИК ЛЬДА: ТАЛАЯ ЛИНИЯ ИДЁТ ОТ КЛЮЧИЦЫ МЕЖ РЁБЕР, "
             "ХАЛТЕР СПАЛ НА ОДНО ПЛЕЧО РОВНО ТАМ, ГДЕ ПРОХОДИТ ТАЯНИЕ, ГОЛОВА "
             "ЗАПРОКИНУТА В СОЛНЦЕ. КАУСТИКА ЛЬДА ПОЛЗЁТ ПО ЗОНЕ ЗАЯВКИ — "
             "СВЕТ ЧЕРЕЗ ТАЛУЮ ЛИНЗУ РИСУЕТ НА КОЖЕ ДРОЖАЩУЮ ТАБЛИЦУ. ХВОСТ "
             "ПОЛОСАТОЙ ГОРДОСТИ ЗАНЯТ: ДЕРЖИТ ТЕНЬ, КАК ЗОНТИК. ЭТО НЕ "
             "ЛЕДЯНАЯ ДРАМА — ЭТО СПОРТИВНЫЙ РЕЖИМ ВОССТАНОВЛЕНИЯ ПОСЛЕ "
             "ЧИСЛЕННОЙ ПОБЕДЫ»."),
     gag=("Гэг-стек (канон-ран ≥3): 1) белая полоса в волосах ловит жёсткий "
          "свет, как сцену — аплодисменты; 2) хвост держит тень-зонтик над "
          "зоной таяния — сервис; 3) чир-топ несёт командные цвета — "
          "победные; 4) кубик тает ровно на девять минут — она засекала."),
     test=("ТЕСТ (⚗ H-07: каустический свет на зоне заявки — доставляет ли R+ "
           "так же, как направленный): каустика талой линзы ползёт по зоне, "
           "свет рисует таблицу на коже. Дифференциал — направленный свет "
           "против каустики. Проверка: линия талой воды, каустика на зоне, "
           "хвост-зонтик, кубик на девять минут"),
     spine="Y32 Ice-Line Caustic (slight low angle, combo→Y32, карта-стенд) · CAM— slight low, up the melt-line · LEAD the crawling table · recovery register · upper body",
     race="R60 — скунсиха: выигрывает любой конфликт фактом существования — никто не рискует.",
     gar="CL-FX-07 (чир-сет: кроп-топ и плиссе-юбка, командные цвета насыщенны) + CL-OU-05 (сатиновый бомбер, блеск скользит по плечам) + CL-TS-08 (спортивный кроп-топ, живот открыт, ткань матовая) · HS: HS34 Stripe-Part Long Hair",
     stack=["CR-W61", "CR-B72", "CR-E18", "CR-D32"],
     ycard="Y32",
     pos=[
         "Masterpiece, best quality, absurdres, intricate details, slight low angle up the melt-line, upper body, ice cube melting a slow line from the collarbone, 1girl, solo, her breast shape under the athletic crop's dry-fit honesty, ink-black hair with a white stripe part, ledger-green eyes tipped to the sun, night-warm skin, fluffy skunk tail, white stripe through the hair, skunk girl, human face, small breasts, wide hips, pear figure, mid_iceline,",
         "the halter sagging off one shoulder exactly where the melt passes, nothing underneath the ice-line's track but the caustic's crawl, her fist gripping the halter's edge pinned under, the halter's line laid across her chest's bare line with the melt — the crawling table is the claim, recovery-made,",
         weave("Y32"),
         "the caustic light crawling the claim-zone as the melt draws its lens, the tail holding shade like a service umbrella, a tiny lip ring catching the melt's glint, a hair ribbon tied at the stripe-part, the satin bomber sheened and forgotten at the elbows, the ice cube booked for exactly nine minutes,",
         "the head tipped back into the sun with the melt's slow ledger running, the cheer skirt's pleats holding their saturated team colors,",
         "ice cube melting a slow line from the collarbone between the ribs, halter pulled aside where the melt passes, head tipped back into the sun,",
         "the sideline's chalk holding the score nobody needs to check, the cooler's remaining cubes queuing like substitutes, the whole victory melting at a lawful nine-minute pace,",
         pal_line("P278_LEDGER_GREEN", "the table the melt draws"),
     ],
     negx=" stripe dull, tail down, caustic gone, ice gone",
     face="stylized 2D anime face tipped into the sun, anime eyes (ledger-green, half-closed in the glare), small nose, small mouth on the ninth minute, one white-stripe strand holding the light like a headline.",
     )

slot("P33", "fennec-winddome-midtone", "EXP · R62 Fennec-kin · R+ · Y33 · P276_POCKET_DENIM_DUSK",
     channel=None, corridor="B",
     thesis=("«ФЕНЕК В КУПОЛЕ ВЕТРА: ПОТОК ПРИЖИМАЕТ РУБАШКУ ПЛОТНО К ГРУДИ, "
             "ВЕРХНЯЯ ПУГОВИЦА СДАЁТСЯ НА СЕРЕДИНЕ ПОРЫВА, ПОДОЛ ХЛЕЩЕТ ПРОТИВ. "
             "БИНТ-ОБМОТКА ЧИТАЕТСЯ СКВОЗЬ ТКАНЬ НА СРЕДНЕМ ТОНЕ — НИ ТЁМНОГО, "
             "НИ БЕЛОГО: РЕЛЬЕФ ЖИВЁТ В ПОЛТОНА, И КУПОЛ ЭТОГО НЕ СКРЫВАЕТ, "
             "А ПОДЧЁРКИВАЕТ. УШИ ВЕНТИЛИРУЮТ ЖАР И СВЕТЯТСЯ РОЗОВЫМ НА ПРОСВЕТ — "
             "СРЕДНИЙ ТОН, НИ ХОЛОДЕН, НИ ГОРЯЧ. КОРОТЫШКА ДЕРЖИТ КУПОЛ УШАМИ, "
             "КАК ДЕРЖАТ ПОГОДУ: ДАРОМ»."),
     gag=("Гэг-стек (канон-ран ≥3): 1) уши вентилируют жар при смущении — видимый "
          "румянец; 2) на просвет уши розовые — встроенный средний тон; "
          "3) бинт-обмотка спиралью теней — читается тело, "
          "не ткань; 4) пуговица сдаётся на середине порыва — по расписанию."),
     test=("ТЕСТ (⚗ H-03: тон ткани — читается ли рельеф на среднем тоне): "
           "бинт-обмотка на СРЕДНЕМ тоне — рельеф без тёмного канона и без "
           "белого перелёта. γ-проба среднего тона. "
           "Проверка: средний тон заявлен, спираль читается, пуговица на середине порыва"),
     spine="Y33 Wind-Dome Midtone (slight low angle, combo→Y33, карта-стенд) · CAM— slight low, into the dome · LEAD the half-tone read · weather-room register · upper body",
     race="R62 — фенек: уши вентилируют жар, когда она смущается — видимый румянец.",
     gar="CL-TS-14 (бинт-обмотка как топ, спираль теней, тело читается сквозь) + CL-UR-07 (парчовый корсет на шнуровке, расстёгнут до бёдер) · HS: HS59 Fur-Framed Choppy Cut",
     stack=["CR-W64", "CR-C13", "CR-E22", "CR-I03"],
     ycard="Y33",
     pos=[
         "Masterpiece, best quality, absurdres, intricate details, slight low angle into the wind dome, upper body, wind dome pressing the wrap flat, 1girl, solo, her breast shape shown through the wrap's spiral in half-tone, sand-cream hair wind-teased, huge fennec ears glowing pink backlit, cream fur tufts at the ears only, fennec girl, soft dusk skin, human face, short adult woman, thick thighs, wide hips, mid_windtone,",
         "the brocade corset unbuckled to the wind's dome, nothing underneath the bandage wrap's turn but the gust's own press, her fists pinning the wrap's gathered tail over the chest's bare line — the half-tone read is the claim, weather-room-made,",
         weave("Y33"),
         "brass ear cuffs riding the big ears' rims, the wrap's spiral reading ribs neither dark nor bleached — the half-tone holding its honest middle, the top button's thread giving up mid-gust on schedule, the huge ears venting their pink at the gust's embarrassment,",
         "the hem snapping against the wind's argument, both fists' grip honest on the wrap's tail, the corset's busk catching one last light,",
         "the wind dome pressing the shirt flat against her breast shape, the hem snapping against the wind,",
         "the weather-room's gauges all agreeing with her and not each other, the test corridor's chalk marks from yesterday's dome still holding, the air doing its honest work of showing fabric what fabric is,",
         pal_line("P276_POCKET_DENIM_DUSK", "the tone she keeps between"),
     ],
     negx=" ears dull, wrap dark, button holding, dome calm",
     face="stylized 2D anime face into the press, anime eyes (dusk-amber, half-lidded patience), small nose, small mouth on the gust's meter, one huge ear swiveling to read the next squall.",
     )

# ══════════════════ HEADER ══════════════════
def build_header():
    L = []
    a = L.append
    a("# THREAD 5 — Batch T5-30: «WHAT THE FUCK IS THAT?!» — БАТЧ (PROSE PLUS · режим CLOCK · жребий оракула №4 · эра гейтов 1.18.0)")
    a("")
    a("заказ (вербатим автора, 2026-11-22, чат):")
    a("«Давай ебанём, раз уж на то пошло.")
    a("")
    a("Новая тема: What the Fuck is That?! (21 слот)")
    a("")
    a("Темы для ОС-канона: (3 слота)")
    a("- Эро-Интро для Noxx")
    a("- Blurry Dreams")
    a("- Dirty Whore")
    a("")
    a("EXP-слоты; 9 слотов;")
    a("- 9 кандидатов в ОС, 9 экспериментальных комбо одежды и Y в сумме на R+ рейтинг (очень близкие к потолку), 9 новых раскрасок и экспериментальных палитр»")
    a("")
    a("Поручения исполнены ДО сборки: (1) протоколы «пробы и ошибки» → «зализывание")
    a("ран» → «вонючие яйца» (заказ 2026-11-22) отработаны: проба TB-20261122-20261122")
    a("разобрана послотово, 25 причин задокументированы (docs/PROTO-TRIALS-2026-11-22.md),")
    a("тест-горн PROTO-2 собирает болванки по всем законам эры (4 сида PASS 30/30), CI и")
    a("pre-commit держат деградацию; (2) MODE: CLOCK — стандартный конвейер без новых")
    a("доктрин; (3) ПЕРВЫЙ БАТЧ ЭРЫ ГЕЙТОВ 1.18.0 (В39–В43, FAIL с T5-30): вольт-ядро")
    a("R+×14 · R×7 ВПЕРЕМЕШКУ (бег ≤ 3, закон 24 восстановлен после дрейфа 27/28/29),")
    a("кины ≤ 10 из 21 (человек — основа, policy v2.0), EXQUISITE ×2 в мейн-массе (В41),")
    a("EXP-клетки несут H-XX из полки гипотез (В42), рейтинг честен ПО СОСТАВУ —")
    a("rating_implied (В43): R+ = транзиентный холд объекта руками или bare-line со")
    a("стрэпами, панель ткани на груди = потолок R; (4) жребий оракула №4 (seed")
    a("2323661502 = 30×2654435761 mod 2³², паритет печь=прилавок): ОС Y375/Y388/Y446,")
    a("мейн — 21 карта; (5) КАРЗАМЕН ×10: Y348→Y446 (ОС: дубль с несданной №28 +")
    a("витринная посадка под Dirty Whore), Y302→Y320, Y237→Y89, Y194→Y359, Y239→Y366")
    a("(дубли с несданной №28 — прецедент карзамена T5-29), Y421→Y250, Y154→Y334,")
    a("Y188→Y415, Y181→Y363 (Закон 24: жребий дал мейнам 6 класс-карт экспозиции,")
    a("канон требует 14 — класс «—» не выносит R+, В33/В27; переброс с записанной")
    a("причиной); (6) EXP по заказу автора, исполнен КАК гипотезы (В42): 9 кандидатов")
    a("в ОС (бандл раса-гиммик × типаж × палитра × комбо у потолка; кандидат-механика")
    a("H-13 на A/B-паре P27/P28, остальные клетки несут свободные гипотезы полки:")
    a("H-12/H-10/H-11/H-09/H-08/H-07/H-03 — по одной, ≤2 клеток на гипотезу) × 9")
    a("экспериментальных комбо одежды (пре-гардероб, стак Y×CLOSET у потолка: 6 COVER +")
    a("2 PROCESS + 1 CLOTHED-TIGHT, все коридор A/A+B/B, ручной выбор активного пула —")
    a("легально в CLOCK, прецедент T5-29) × волна 14 «покрытия-настроения»: 9 новых")
    a("раскрасок-палитр P270–P278 (trial до вердикта; способы раскраски — преемство")
    a("волны 10); oc_hook ×0 (волна отдыха: ~35% — вероятность, не квота); (7) каналы —")
    a("дисциплина эры 1.18.0: ОС на oc-rplus (exempt), R+-мейны на LIVE-каналах")
    a("(contact-physics ×3 · handbra-open-palms ×3 · tape-only ×3 · wet-sheer-delivery ×3,")
    a("A/B-подача по 2-3 слота — директива §10) + волна 16: ровно 2 кандидата ☠")
    a("(strap-line-hold, element-linen — квота ≤2 соблюдена впервые со времён T5-24);")
    a("(8) палитры мейнов/ОС — 24 свежих семьи вне окна 99, burn 4, 33 семей №28 и")
    a("волны 13; (9) В43-честность: каждая R+-заявка несёт состав-доказательство (холд")
    a("руками / bare-line со стрэпами), NICHE-мейны несут R-токены (breastRead/rTokens);")
    a("В32: ≥2 фишечки-ФОРМЫ; В34/В35: клеймо — вплетённый паттерн карты 1:1, камера —")
    a("кластером OPENER, коридор — физикой claim-строки.")
    a("")
    a("Жанровая легенда (NICHE.md §Б): OC — персонаж-канон (R+); NICHE — чудо")
    a("невозможного (R); VOLT — плоть и камера-участник (R+); EXQUISITE — экстремум")
    a("своего жанра, ультра-регистр (R+). Токен стоит первым в скобках каждого слота.")
    a("")
    a("## SPINE (AXIS/ANTI/PROMISE)")
    a("")
    a("AXIS: «НЕВОЗМОЖНОЕ ПОСЛУШНО БЫТУ: каждый кадр несёт РОВНО одну штуку, которой")
    a("не может быть — предмет, явление или физика — и ЭТУ ШТУКУ ОБСЛУЖИВАЮТ КАК")
    a("РУТИНУ: калибруют, заводят, пересчитывают, протирают, подают с чаем. Героиня")
    a("профессионально спокойна; восклицание «WHAT THE FUCK IS THAT?!» — работа")
    a("зрителя, не её. Чудо живёт предметом (LAWS §6), не спецэффектом: шахта в")
    a("вчерашний день, чайник-рассвет, лестница из воздуха, тень-гамак, окно в другой")
    a("сезон, 25-й час на циферблате. У каждой штуки — график смены и инструкция.")
    a("ANTI: «мистической жути нет (horror-клише: creepy smile, ghost-fog, jump-scare")
    a("— 0: невозможное не угрожает, оно обслуживается); оружие-угрозы нет (клыки в")
    a("улыбке быта); candle/lamp/приборы света — 0 ×33 (закон света v2: свет —")
    a("поведение и стихия, не прибор); IP-монстров и франшизных WTF нет; вторая")
    a("фигура в кадре — 0 (1girl solo ×33); X-токены — 0 (закон T4)».")
    a("PROMISE: каждый кадр читается как ОДНО восклицание с ответом-бытом — по")
    a("предмету и покою, без текста; R+ несёт вплетение карты 1:1 (В34/В35) +")
    a("состав-доказательство В43 + ≥2 фишечки-ФОРМЫ (В32); жребий оракула №4: 24")
    a("карты партии собраны от ВЫТЯНУТЫХ, 9 карзаменов документированы; EXP-девятка:")
    a("кандидаты × комбо у потолка R+ × волна 14 — по клетке, каждая с H-XX.")
    a("")
    a("## ГИПОТЕЗА ДВИЖКА: «ОДНА НЕВОЗМОЖНАЯ ШТУКА + ДОМАШНЕЕ СПОКОЙСТВИЕ» (Г12, новая)")
    a("")
    a("«Кадр WTF держится двумя несущими: (1) ШТУКА-НАРУШЕНИЕ — ровно один предмет/")
    a("физика/закон, которых не может быть, названный ПРЕДМЕТОМ (LAWS §6); (2) БЫТ —")
    a("рутина, инструмент, смена, инструкция, спокойствие профессионала. Изъми штуку —")
    a("останется бытовая зарисовка; изъми быт — станет фэнтези-кличем или хоррором.")
    a("Восклицание зрителя рождается ТОЛЬКО из их суммы: чудо + человек, которому")
    a("все равно, потому что у него смена».")
    a("ОЖИДАНИЯ (5, фальсифицируемые; вердикт проставит D14):")
    a("  (1) Каждый мейн-слот несёт ровно ОДНУ невозможную штуку, названную предметом,")
    a("  и ноль хоррор-клише — опровергается второй штукой или жутью в кадре.")
    a("  (2) Героиня при невозможном профессионально спокойна: предмет-инструмент/смена")
    a("  в claim-строке каждого кадра — опровергается испугом/пафосом.")
    a("  (3) Рейтинг-честность В43: 17 R+ (3 ОС + 14 мейнов) несут состав-доказательства")
    a("  (холд/стрэп-линия), 7 NICHE — R-токены; гейт ratingTruth — 0 ложных бейджей.")
    a("  (4) Вольт-ядро В39: R+×14 · R×7 вперемешку (бег ≤ 3), EXQUISITE ×2 в мейнах,")
    a("  кины 10/21 — гейты voltCore/raceCast/exquisiteMain PASS без нарушений.")
    a("  (5) EXP: 9 клеток = 9 кандидатов × комбо у потолка × волна 14, каждая несёт")
    a("  H-XX из полки (В42), гипотез ≤2 клеток — вердикт возвращает 9 меток.")
    a("")
    a("## ХОДЫ (§6, реестр moves-ledger.json): M07 standing · M05 применён · M03 применён")
    a("")
    a("M07 standing — «предмет > состояние»: невозможная штука названа предметом (кол,")
    a("чайник, простыня-память, окно-сезон), не «атмосферой».")
    a("M05 применён — «ловля на пролёте»: процессные карты жребия ловят смену в")
    a("середине (полотенце на пол-вытирания, лента на пол-удара, завод на пол-оборота,")
    a("прыжок на пол-шага).")
    a("M03 применён — «построчный канон-чек»: ОС-тройка собрана построчно по")
    a("oc-canon.json 2.14.0 (Noxx: ghost-layer shag + star-flecks + тень-эскорт;")
    a("Ama: гриб-шляпка + споры-волосы + дождь-шеврон; Dove: кудри-дрели + ценник-шнур")
    a("+ витринное тепло).")
    a("")
    a("## КАСТ")
    a("")
    a("ОС-канон (P01–P03) — по темам автора, фейс-контроль: Noxx (Эро-Интро — первая")
    a("эротическая representация: порог-пламя как занавес, винил расхлёстнут, свет")
    a("договаривается; канон 2.14.0, промоция T5-29 P32) · Ama (Blurry Dreams —")
    a("девочка-дождь идёт из сна, который дождит вверх; мокрая белая кофта — канон-")
    a("униформа) · Dove (Dirty Whore — витрина дверного проёма: ладони на стойках,")
    a("ценник на розовом шнурке, взгляд продавца-товара; дебют T5-22, три партии")
    a("назад). Тройка вне OC-окна 9 (Ana, Hana, Lucy, Mab, Meine, Noa, Noir, Sol, Vae).")
    a("Мейн-каст (P04–P24, расовый каст 9/21 — policy v2.0, В40: человек основа,")
    a("кины опция, окно 0–10): 9 kin — R29 Mouse · R17 Jellyfish · R47 Wind-spirit ·")
    a("R22 Flame-salamander · R51 Crane · R36 Tanuki · R34 Phoenix · R40 Medusa ·")
    a("R09 Goat (все — не выходили в сданных T5-26/27/29 — clarifier-граммы чисты,")
    a("канон-локи ОС соблюдены) + 12 human-служб")
    a("WTF-мира (смотрительница окна-сезона, смотрительница смены света, хозяйка")
    a("стола находок, горожанка после ливня, хозяйка тени-гамака, часовщица")
    a("25-го часа, сновидческая постель, кухарка рассветов, хозяйка личного")
    a("ветра, кондуктор междумирового рейса, хранительница мемориала, крышная")
    a("курьерша).")
    a("EXP-девятка (P25–P33) — 9 кандидатов в ОС: R15 Porcelain-doll · R16 Moth ·")
    a("R24 Oni · R26 Bee · R27 Cow · R31 Flower · R23 Shark · R60 Skunk · R62 Fennec")
    a("расы чисты по сданным T5-27/29; R23 — осознанный реюз несданной №28,")
    a("задокументирован. Каждая — бандл (гиммик расы + типаж + палитра волны 14 + комбо")
    a("у потолка + H-XX в строке ТЕСТ); oc_hook ×0 (волна отдыха — вероятность, не")
    a("квота; закон реестра кандидатов). Вердикт только автор: «беру» → special-roster,")
    a("«не беру» → passed.")
    a("")
    a("## СПРЕД")
    a("")
    a("Спред мейнов (P04–P24): R+×14 · R×7 — Закон 24 восстановлен после дрейфа 27/28/29")
    a("(7/12/2): вольт-масса 14 (VOLT×12 + EXQUISITE×2 — P09/P19), ниша 7 (P04/P07/")
    a("P11/P14/P17/P20/P23), жанры ВПЕРЕМЕШКУ, макс бег 2 (гейт voltCore, В39).")
    a("ОС (P01–P03): EXQUISITE R+×3 — канон VERBATIM, жребий №4 (карзамен Y348→Y446")
    a("задокументирован). EXP-оверлей (9 слотов): R+×9 — комбо+Y у потолка в каждой")
    a("клетке (6 COVER + 2 PROCESS + 1 CLOTHED-TIGHT). Честность В43: каждая R+-заявка")
    a("несёт состав-доказательство — холд руками (полотенце в кулаках P05, кулак огня")
    a("P01, кулаки перил P24) или bare-line со стрэпами (стрэп-линия стекла P06,")
    a("бретель пояса-Мёбиуса P16, лента-межа P10); панель ткани на груди держит")
    a("потолок R. Если рендер разберёт прикрытие — слот честно падает в R по вердикту,")
    a("квитанция отразит (В43).")
    a("")
    a("## HEAT")
    a("")
    a("HEAT-оплата разнообразия: жребий оракула №4 — четвёртая живая раздача (3 ОС +")
    a("21 мейн от ВЫТЯНУТЫХ карт; 9 карзаменов с записанной причиной: 5 дублей с")
    a("несданной №28, 4 — Закон 24) · ОС-тройка не выходила: Noxx — промоция T5-29")
    a("(первое appearing после канонизации), Ama — T4-эра, Dove — T5-22 · 9 кин")
    a("мейнов — свежие расы вне сданных T5-26/27/29 (канон-локи не тронуты; R23")
    a("Shark в EXP — осознанный реюз несданной №28, задокументирован) · EXP — 9")
    a("свежих рас-кандидатов, реюз в роли кандидата прецедентен T5-24/25/28/29 ·")
    a("палитры — 24 свежих семьи вне окна/burn/№28 + волна 14 из 9 новых (trial) ·")
    a("каналы — 4 live с A/B-подачей (по 2-3 слота, директива §10) + волна 16 (ровно")
    a("2 кандидата ☠ — квота соблюдена) · детали-слой ≥2 фишечки-ФОРМЫ в каждом (В32) ·")
    a("сигнатуры клозом (В28) · носители — свежий пул вне окна 252, burn CR-W04/CR-H10")
    a("вычтены, реюзы ≤2× (фактически 0 — все 132 кода уникальны) · первый батч эры")
    a("гейтов 1.18.0: пять новых машин (В39–В43) работают в FAIL-режиме впервые.")
    a("")
    a("## СТРУКТУРА")
    a("")
    a("33 слота = 3 ОС (P01–P03: Noxx Эро-Интро · Ama Blurry Dreams · Dove Dirty")
    a("Whore — EXQUISITE R+, канон VERBATIM из specs/oc-canon.json 2.14.0 1:1) +")
    a("21 мейн (P04–P24: 14 R+ / 7 R — R+×14 · R×7, закон 24) + 9 EXP (P25–P33, ⚗-")
    a("клетки: кандидаты × комбо у потолка × волна 14, H-XX в каждой). Темы ОС: P01")
    a("Эро-Интро для Noxx · P02 Blurry Dreams · P03 Dirty Whore (порядок — как")
    a("заказал автор). Камера: по картам жребия (frontal eye-level / сверху вниз /")
    a("снизу вверх / through shoulder — см. клетки). Каналы: 3 ОС — oc-rplus (exempt);")
    a("14 R+-мейнов — 4 live (contact-physics ×3: P06/P08/P24; handbra-open-palms ×3:")
    a("P05/P09/P22; tape-only ×3: P10/P12/P13; wet-sheer-delivery ×3: P15/P18/P21) +")
    a("волна 16 кандидаты ☠ ×2: strap-line-hold (P16) · element-linen (P19); EXP вне")
    a("каналов (прецедент T5-24/27/28/29); NICHE-мейны без каналов (закон: канал —")
    a("заявка R+). Клеймо: 17/17 R+ мейнов и ОС + 9/9 EXP вплетено из карт (В34/В35).")
    a("Типажи: 21 семейство BT, никто не выше 3 раз (BT-04 ×3, BT-06 ×3 — кап)")
    a("соблюден).")
    a("")
    a("## EXP-КЛЕТКИ (camera.json — 9 карт у потолка, ручной выбор активного пула)")
    a("")
    a("Y147 (COVER A) · Y209 (COVER A) · Y342 (COVER A) · Y428 (COVER A) · Y492 (COVER")
    a("A) · Y356 (COVER A+B) · Y30 (PROCESS B) · Y32 (PROCESS B) · Y33 (CLOTHED-TIGHT")
    a("B). Все девять вне окна ротации, несданной №28 и жребия мейнов, ни одна не")
    a("дублируется в батче. Жребиевы EXP-карты волны (Y307/Y59/Y468/Y382/Y128/Y78/")
    a("Y420/Y407/Y220 — все класс «—», В33/В27 запрещают им R+) остались в пуле,")
    a("задокументированы как альтернатива (прецедент T5-27/28/29). Стак с комбо")
    a("пре-гардероба (преемство T5-29: тёмная/CLOTHED-TIGHT-гамма, прикрытие живое")
    a("в кадре) держит R+ у потолка: композиция — холд руками или стрэп-линия,")
    a("панели — в off-состоянии (worn open / peeled / sagging / unbuckled).")
    a("")
    a("## EXP-ОВЕРЛЕЙ (кандидаты × комбо × палитры — все 9 свежие)")
    a("")
    a("Фарфор «Полсекунды» → R15 Porcelain-doll × Y147 × P270_GLASSBITE_MINT (H-12:")
    a("mid-action — пятки стучат на середине такта, поза на полсекунды дольше)")
    a("· Мотылёк «Доставка Взгляда» → R16 Moth × Y209 × P272_STATIC_LILAC (H-10:")
    a("композиция-носитель — вырез как рама, зритель снизу) · Они «Сверхурочная")
    a("Смена» → R24 Oni × Y342 × P277_SORBET_STAIN (H-13 A: кандидат-клетка — рожки")
    a("на удачу, румянец-индикатор) · Пчела «Счёт Колец» → R26 Bee × Y428 ×")
    a("P275_URANIUM_GLASS_GLOW (H-13 B: кандидат-клетка, A/B-пара с P27 — стена")
    a("против щита) · Коровка «Контр-Качка» → R27 Cow × Y492 ×")
    a("P271_WAX_SEAL_OXBLOOD (H-11: анти-стерильность — вес косой, халат в драке")
    a("потоков, хвост-терпение) · Цветочная «Именованный Подслой» → R31 Flower ×")
    a("Y356 × P273_FOIL_BALLOON_COPPER (H-09: named-underlayer — «Лаванда» вышита")
    a("по краю, жилки-вены читают рецепт) · Акула «Пол-Прилива» → R23 Shark × Y30 × P274_TIDEPOOL_MIRROR")
    a("(H-08: частичное мокрое — подол мокрый, верх сухой) · Скунсиха «Каустика")
    a("Льда» → R60 Skunk × Y32 × P278_LEDGER_GREEN (H-07: каустический свет на")
    a("зоне заявки) · Фенек «Средний Тон» → R62 Fennec × Y33 ×")
    a("P276_POCKET_DENIM_DUSK (H-03: рельеф на среднем тоне, γ-проба, уши-глоу).")
    a("Trial-статус до вердикта T5-30; результат в каждую клетку вписывает только")
    a("вердикт.")
    a("")
    a("## ТЕМА-СЛОВА (реестр; слово легально, когда называет ПРЕДМЕТ кадра — LAWS §6)")
    a("")
    a("the yesterday-shaft's shelved Tuesdays · the puddle of sky with one cloud left ·")
    a("the two-weather pane and its noon rag · the light handing itself down the")
    a("stairs · the shadow-hammock's one-and-a-half centimeters · the air's polished")
    a("parquet under her knees · the weather-stake and its tape-cross border · the")
    a("two-currency fare and its both-worlds step · the dial's twenty-fifth hour · the find that")
    a("breathes light · the stack lighter than its reader · the wall dry on her side ·")
    a("the sarong's möbius strap-line · the sheet that reads dreams back · the")
    a("kettle's private sunrise · the fire-scarf on contract · the wind that walks")
    a("her block only · the pipe that sings un-organed · the memorial wall warm at")
    a("two names · the phosphor streams under clear ice · the invisible service")
    a("stairs. НИКОГДА: sword/shield/adventurer в POS (героика = 0); candle/lamp и")
    a("прочие приборы света — 0 ×33 (закон v2: свет — поведение и стихия);")
    a("хоррор-клише (creepy fog, sinister grin) — 0 (невозможное обслуживается, не")
    a("пугает); IP-имена франшиз — 0; вторая фигура — 0 (1girl solo ×33); X-токены:")
    a("topless, bare breasts, nipples — 0 (X=0, закон T4); тема-титул «what the fuck")
    a("is that» целиком в POS — 0 (тема живёт предметами, LAWS §6).")
    a("")
    a("## ОС-ТЕМЫ (по заказу автора; слово легально, когда называет ПРЕДМЕТ кадра)")
    a("")
    a("Эро-Интро для Noxx = первая эротическая представация: порог встречает её")
    a("огнём, пламя — занавес, который ладонь отводит как штору; винил расхлёстнут,")
    a("под ним — только договор света; кулак держит край огня у ключицы. Интро — не")
    a("стриптиз, а представление: её представляют читателю, и порог аплодирует")
    a("пламенем. НИКОГДА: стриптиз-клише (медленное сползание по шесту), пошлые")
    a("приглашающие позы, «первый раз»-смущение (Noxx не смущается — она")
    a("договаривается); Эро-Интро = канон + заявка + порог-занавес.")
    a("Blurry Dreams = сон наяву, размытие — ПРЕДМЕТОМ, не фильтром: дождь идёт")
    a("вверх из дверного проёма сна, волосы дрейфуют спорами на полтакта позади,")
    a("полотенце на шее держит два мира за концы. Мокрая белая кофта — канон-униформа")
    a("дождя, сползшая с обоих плеч. НИКОГДА: «soft focus/hazy/blur» как теги (анти-")
    a("ваш в NEG — размытие живёт каплей, дрейфом и сном-дверью, не фильтром);")
    a("сновидческие клише (мыльные пузыри, единороги, сюрреал-пустыня); Blurry")
    a("Dreams = дождь вверх + дрейф-волосы + полусон-взгляд.")
    a("Dirty Whore = витринная честность ночного ряда: дверной проём — её витрина,")
    a("ладони на стойках рамы, ценник на розовом шнурке качается между рёбер — цена")
    a("написана её почерком. Она сама продавец и товар, взгляд тёплый, как")
    a("карамельная глазурь; улица смотрит — она смотрит в ответ и выигрывает торг.")
    a("НИКОГДА: унижение, «slut»-токены, пошлые приглашения без договора, дешёвый")
    a("трип-клише; Dirty = честность ночного города, Whore = профессия с прайсом,")
    a("стиль = форма и сделка (ценник-шнур — реквизит и подпись).")
    a("")
    a("## АКТЫ (одна невозможная штука на кадр — прозой, урок счётчика: без паттерна «PNN — …»)")
    a("")
    a("ОС (P01–P03): три темы по заказу автора, канон VERBATIM, карты жребия №4. P01")
    a("Эро-Интро для Noxx — порог-занавес из огня, винил расхлёстнут / P02 Blurry")
    a("Dreams — Ama идёт из сна, который дождит вверх / P03 Dirty Whore — Dove в")
    a("дверной витрине с ценником-шнуром (EXQUISITE R+).")
    a("МЕЙН (P04–P24), вперемешку, жанры в скобках кадра: мышь-картографка читает шахту")
    a("вчерашнего дня (NICHE) · медуза вытерлась после купели в облаке (VOLT) ·")
    a("окно, за которым лето, а в комнате зима (VOLT) · лестница передаёт свет из")
    a("руки в руку (NICHE) · тень-гамак держит лежащую (VOLT) · ветер-дева ползёт")
    a("по воздуху с подносом (EXQUISITE) · саламандра вбивает межу двух погод (VOLT) ·")
    a("кондуктор считает плату двух миров (NICHE) · часовщица заводит 25-й час")
    a("(VOLT) · стол находок дышит светом (VOLT) · книги легче читателя тянут её")
    a("вверх (NICHE) · стена единственная сухая, и это предложение (VOLT) ·")
    a("саорнг-пояс закручен в мёбиус-бретель (VOLT) · простыня дочитывает её сон")
    a("(NICHE) · чайник всходит рассветом из носика (VOLT) · пожарная дверь")
    a("отпускает феникса со огнём в волосах (EXQUISITE) · ветер дует только на неё")
    a("(NICHE) · органная труба поёт без органа, конденсатом (VOLT) · мемориальная")
    a("стена тёплая на ощупь у двух имён (VOLT) · конёк один, горное равновесие над")
    a("водой (NICHE) · невидимая служебная лестница с крыши (VOLT).")
    a("EXP (P25–P33): девять клеток кандидатов: полсекунды · доставка взгляда ·")
    a("сверхурочная смена · счёт колец · контр-качка · именованный подслой ·")
    a("пол-прилива · каустика льда · средний тон — по бандлу, комбо у потолка и")
    a("H-XX на клетку.")
    a("")
    a("## ОКНО РОТАЦИИ — Окно глубиной 3, прогон window.py --for T5-30")
    a("")
    a("Квитанция станции окна: batches/T5-30/window.md (агрегат-запрет: позы 62,")
    a("палитры 99, носители 252, каналы 30, Y-карты 85 — сданные T5-26/27/29;")
    a("burn-актив 19 кодов не назначен; OC-окно 9: Ana/Hana/Lucy/Mab/Meine/Noa/")
    a("Noir/Sol/Vae — тройка Noxx/Ama/Dove вне его; партия №28 в статусе ready —")
    a("окном не считается (delivery-index), но её 33 карты/33 палитры вычтены из")
    a("выбора вручную — прямой дубль с предыдущей несданной партией неаккуратен:")
    a("5 случайных совпадений жребия закрыты карзаменом с записанной причиной,")
    a("прецедент T5-29). Карты жребия и их позы — вне запретов. Палитры — 24 свежих")
    a("семьи вне окна/burn/№28 + волна 14. Носители — свежий пул: все 132 кода")
    a("уникальны, окно чисто по построению. Каналы — 4 live вне окна 30 + 2 новых")
    a("кандидата волны 16. Активный пул Y: 445 из 530 (окно −85, target 60) — ЗДОРОВ.")
    a("")
    a("═══════════════════════════════ СЛОТЫ ═══════════════════════════════")
    a("")
    return L

# ══════════════════ сборка слотов ══════════════════
def build_slot(s):
    L = []
    a = L.append
    exp_mark = " ⚗" if s["sid"] >= "P25" else ""
    a(f"{s['sid']} — {s['slug']} ({s['paren']}){exp_mark}")
    if s.get("channel"):
        if s["channel"] == "oc-rplus":
            a("Channel: oc-rplus (OC R+ — канон-локи + заявка; exempt по закону каналов)")
        elif s["channel"] in WAVE16_CHANNELS:
            name, note = WAVE16_CHANNELS[s["channel"]]
            a(f"Channel: {s['channel']} (☠; {name}: {note})")
        else:
            live_names = {
                "contact-physics": "Физика касаний — мягкое мнётся о поверхность",
                "handbra-open-palms": "handbra — раскрытые ладони пальцами врозь",
                "tape-only": "tape как единственная заявка",
                "wet-sheer-delivery": "wet-sheer + подача + свет НА зоне",
            }
            a(f"Channel: {s['channel']} (live; {live_names.get(s['channel'], '')})")
    a(f"Corridor: {s['corridor']}")
    if s.get("oc_theme"):
        a(f"Тема ОС: {s['oc_theme']}")
    a(f"THESIS: {s['thesis']}")
    a(f"{s['gag']}")
    if s.get("test"):
        a(s["test"])
        tv = s["test"].split("Проверка: ")[-1].rstrip(")")
        a(f"Проверка: {tv}")
    a(f"Spine: {s['spine']}")
    a(f"Race: {s['race']}")
    bt = BT_MAP[s["sid"]]
    a(f"Body: {bt} ({BT_NAMES[bt]})")
    a(f"Gar: {s['gar']}")
    a(f"Stack: {' + '.join(s['stack'])}")
    a(f"Y-card: {s['ycard']} — {weave(s['ycard'])}")
    a("POS:")
    for ln in s["pos"]:
        if ln == weave(s["ycard"]) or len(ln) <= 200:
            a(ln)
        else:
            parts, cur = [], ""
            for chunk in ln.split(", "):
                cand = (cur + ", " + chunk) if cur else chunk
                if len(cand) > 195 and cur:
                    parts.append(cur + ",")
                    cur = chunk
                else:
                    cur = cand
            if cur:
                parts.append(cur if cur.endswith(",") else cur + ",")
            parts[0] = parts[0].rstrip(",")
            if len(parts) > 1:
                parts[0] += ","
            for pl in parts:
                a(pl)
    a("NEG:")
    neg3 = NEG_BASE[2] + s["negx"].strip()  # «hazy,» остаётся юнитом (negBase v3)
    a(NEG_BASE[0])
    a(NEG_BASE[1])  # «desaturated,» остаётся юнитом (negBase v3)
    a(neg3)
    a("")
    return L

def build_footer():
    L = []
    a = L.append
    a("═══════════════════════════════ КОНЕЦ СЛОТОВ ═══════════════════════════════")
    a("")
    a("## ПЕЧЬ — квитанция сборки")
    a("")
    a("- 2026-11-22 · сборка по заказу автора «WHAT THE FUCK IS THAT?!» в режиме")
    a("  CLOCK, ПЕРВЫЙ БАТЧ ЭРЫ ГЕЙТОВ 1.18.0: 33 слота = 3 ОС (Noxx Эро-Интро /")
    a("  Ama Blurry Dreams / Dove Dirty Whore — по темам, вне OC-окна 9) + 21 мейн")
    a("  (R+×14 · R×7 — Закон 24 восстановлен; каст 9 kin + 12 human, policy v2.0)")
    a("  + 9 EXP (⚗, R+×9 у потолка, H-XX в каждой клетке).")
    a("- ЖРЕБИЙ ОРАКУЛА №4 (seed 2323661502 = 30×2654435761 mod 2³², engine + печь")
    a("  побитово): ОС Y375/Y388/Y348; мейн — 21 карта (6 класс-карт: Y451/Y411/")
    a("  Y168/Y480/Y82/Y6). КАРЗАМЕН ×10: Y348→Y446 (дубль №28 + витрина Dirty")
    a("  Whore), Y302→Y320, Y237→Y89, Y194→Y359, Y239→Y366 (дубли с несданной №28),")
    a("  Y421→Y250, Y154→Y334, Y188→Y23 (P13), Y181→Y363 (Закон 24: класс «—» не выносит")
    a("  R+ — В33/В27) + Y414→Y250/Y415→Y23: сиблинги Y413/Y414/Y415 несут общую")
    a("  фразу «lips at the top frame edge», T5-29 катал Y413 — двойной удар пары")
    a("  P11+P13 закрыт сменой обеих карт, темы пересобраны; прецедент T5-27/29).")
    a("- EXP-КАРТЫ: 9 карт ручным выбором из активного пула (легально в CLOCK,")
    a("  specs/active-pools.json): Y147/Y209/Y342/Y428/Y492/Y356 (COVER, A/A+B) +")
    a("  Y30/Y32 (PROCESS, B) + Y33 (CLOTHED-TIGHT, B) — все вне окна, №28 и жребия.")
    a("  Жребиевы EXP-карты волны (Y307/Y59/Y468/Y382/Y128/Y78/Y420/Y407/Y220, класс")
    a("  «—») остались в пуле — задокументированы как альтернатива (В33: класс «—»")
    a("  не выносит R+; прецедент T5-27/28/29).")
    a("- ПРЕ-ГАРДЕРОБ (LAWS §22): 23 комбо под класс-карты (14 R+-мейнов + 9 EXP)")
    a("  катано сидом 30 до сборки + 3 досыпки (Y366 сид 31 — досыпка после основного")
    a("  ролла; Y411/Y428 — вывод повтора CL-DR-10 ×4 → ×3; Y363 — CL-AC-06 ×4 → ×3;")
    a("  Y33 — уход от дубля канон-вещи Dove CL-TS-13 и повтора CL-TS-04 ×4 → ×3) —")
    a("  specs/pregarererobe/T5-30.json".replace('pregarererobe', 'pregarderobe') + ";")
    a("  наборы уникальны по реестру _ledger.json (комбо не повторяется никогда);")
    a("  повторы вещей ≤3 на батч. OC-слоты без CL-кодов: канон VERBATIM сильнее")
    a("  кода (yStack-закон, прецедент T5-29).")
    a("- ПОЗЫ: все 33 карты — карта-стенды (вплетение — строка 3 POS 1:1);")
    a("  PL-коды не используются; окно поз чисто по построению жребия.")
    a("- ПАЛИТРЫ: 24 свежих семьи вне окна 99/burn/№28 (P30/P59/P131 ОС + 21 мейн)")
    a("  + ВОЛНА 14 «покрытия-настроения» — 9 новых палитр P270–P278 (trial до")
    a("  вердикта, palettes 1.15.0→1.16.0): стекло-укус · печать воском · статика")
    a("  сирени · фольга-шар · зеркало лужи · урановое стекло · карманный деним ·")
    a("  след щербета · бумага-гроссбух — 9 механик цвета, семьи ни разу не выходили")
    a("  (преемство волны 10 «способы раскраски»).")
    a("- КАНАЛЫ: дисциплина квоты — ОС на oc-rplus (exempt), R+-мейны на 4 live")
    a("  (contact-physics ×3, handbra-open-palms ×3, tape-only ×3, wet-sheer-delivery")
    a("  ×3 — A/B-подача по 2-3 слота, директива §10) + волна 16: ровно 2 кандидата")
    a("  ☠ — strap-line-hold (P16: линия-бретель как единственная крышка) и")
    a("  element-linen (P19: стихия как ткань) — delivery-stats 0.15.0→0.16.0;")
    a("  квота кандидатов ≤2 соблюдена (T5-29 платил WARN за 10×candidate);")
    a("  EXP вне каналов (прецедент); NICHE-мейны без каналов (канал — заявка R+).")
    a("- КАНДИДАТЫ В ОС: 9 боевых EXP-слотов залогированы в specs/oc-candidates.json")
    a("  1.2.0→1.3.0 (бандл: раса-гиммик + типаж + палитра волны 14 + комбо у")
    a("  потолка + H-XX); oc_hook ×0 — волна отдыха (~35% вероятность, не квота);")
    a("  вердикт только автор.")
    a("- В43-ЧЕСТНОСТЬ: R+×26 (14 мейн + 3 ОС + 9 EXP) подтверждено составом —")
    a("  транзиентный холд объекта руками (полотенце P05, огонь-кукул P01, кулаки")
    a("  перил P24, подносный ремень P09) или bare-line со стрэпами (стрэп-линия")
    a("  стекла P06, мёбиус-бретель P16, лента-межа P10, straps у P13/P15/P21/P25/"); 
    a("  P27/P28/P30); панели — только в off-состояниях (worn open/peeled/sagging/")
    a("  unbuckled); паспорт ≠ тир; гейт ratingTruth — калибровка 33/33 (T5-29).")
    a("- ОКНО: карты/позы/палитры/носители/каналы — вне запретов (прогон")
    a("  window.py --for T5-30, квитанция batches/T5-30/window.md); burn-актив не")
    a("  назначен; OC-окно 9 соблюдено (Noxx/Ama/Dove — вне его).")
    a("- ОЖИДАНИЕ ВЕРДИКТА: Г12 «одна невозможная штука + домашнее спокойствие» — 5")
    a("  фальсифицируемых ожиданий (одна штука на кадр / быт в claim / рейтинг-")
    a("  честность 0 ложных R+ / вольт-ядро 14/7 вперемешку / 9 EXP-клеток с H-XX) —")
    a("  метки проставит D14. Режим CLOCK: FURNACE LITE, новых доктрин нет.")
    a("- ПАЛИТРЫ/РЕЕСТРЫ: palettes 1.16.0 (волна 14) · delivery-stats 0.16.0 (волна")
    a("  16) · oc-candidates 1.3.0 (девятка T5-30) · delivery-index +T5-30 ready ·")
    a("  furnace-ledger F-026 (запись сборки) · README счётчики.")
    return L

def main():
    parts = []
    parts += build_header()
    for s in SLOTS:
        parts += build_slot(s)
    parts += build_footer()
    out = ROOT / "batches" / "T5-30.md"
    out.write_text("\n".join(parts) + "\n", encoding="utf-8")
    print(f"batches/T5-30.md written: {len(parts)} строк, {out.stat().st_size} байт")

if __name__ == "__main__":
    main()
