#!/usr/bin/env python3
"""T5-29 «THE SECRETS BEHIND AURORA DUNGEON» — сборщик батча.

Заказ автора 2026-11-22: мейн Aurora Dungeon ×21 (моё усмотрение: монстры,
ловушки, многое другое — «развлекайся»), ОС-темы DawnBreaker / Kill Confirmed /
Super Sexy Style! (SSS), EXP ×9: 9 кандидатов в ОС × 9 экспериментальных комбо
одежды + Y в сумме на R+ (очень близкие к потолку) × 9 новых раскрасок и
экспериментальных палитр (волна 13 «свет подземелья»).

Режим CLOCK. Жребий оракула №3 (seed 3964193037 = 29×2654435761 mod 2^32),
4 карзамена (дубли карт с несданной партией №28 — задокументированы).
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

# ────────────────────────── волна 13 «свет подземелья» ──────────────────────────
WAVE13 = [
    dict(id="P261_AURORA_VEIN", name="Aurora Vein",
         dominant=["aurora-green-current", "stone-violet-deep"],
         secondary=["ribbon-teal"],
         accent1=["one-vein flash running the ceiling"],
         accent2="girl-silhouette-grey",
         shadow="current-shadow-green",
         forbidden=["neon", "pure-white", "flat sky"],
         light_type="сияние — вена неба: ток света прокатывается по своду волной, наклоняется к той, что внизу, и уходит дальше; свет живой, не ламповый",
         sd_fragment="aurora-green-current over stone-violet-deep, ribbon-teal wave at the ceiling's vein, girl-silhouette-grey at the edges",
         mood="the-light-that-chooses-you",
         family="exp_color_wave_13", born_note="волна 13 «свет подземелья»"),
    dict(id="P262_MOSS_LINE", name="Moss Line",
         dominant=["moss-lush", "lime-pale"],
         secondary=["brick-rust"],
         accent1=["dew-silver"],
         accent2="stone-cold-grey",
         shadow="moss-shadow-green",
         forbidden=["neon", "desert tones"],
         light_type="моховая кромка держит воду утра: свет читается по влажной границе камня и мха, роса — линия",
         sd_fragment="moss-lush over lime-pale, dew-silver line at the stone's edge, brick-rust accent",
         mood="the-damp-frontier",
         family="exp_color_wave_13", born_note="волна 13 «свет подземелья»"),
    dict(id="P263_OSSUARY_CHALK", name="Ossuary Chalk",
         dominant=["bone-chalk", "umber-shadow"],
         secondary=["registry-linen"],
         accent1=["verdict-wine"],
         accent2="candlewax-pale",
         shadow="shelf-shadow-umber",
         forbidden=["neon", "blood-red"],
         light_type="мел оссуария: полки держат ровный костяной тон, тень между фолиантами глубже, чем кажется",
         sd_fragment="bone-chalk over umber-shadow, registry-linen pale at the shelves, verdict-wine one accent",
         mood="the-kept-record",
         family="exp_color_wave_13", born_note="волна 13 «свет подземелья»"),
    dict(id="P264_SPORE_GLOW", name="Spore Glow",
         dominant=["spore-glow-cream", "gill-umbra"],
         secondary=["stem-pale"],
         accent1=["cap-rust"],
         accent2="mycelium-thread-gold",
         shadow="under-cap-shadow",
         forbidden=["neon", "hard white"],
         light_type="выращенный свет: споры висят в контражуре медленными созвездиями, свет — урожай, не прибор",
         sd_fragment="spore-glow-cream over gill-umbra, stem-pale at the hem, cap-rust accent, mycelium-gold threads",
         mood="the-light-you-grow",
         family="exp_color_wave_13", born_note="волна 13 «свет подземелья»"),
    dict(id="P265_THREAD_HOARD_SILK", name="Thread-Hoard Silk",
         dominant=["thread-silver", "hoard-umber"],
         secondary=["knit-shadow"],
         accent1=["knot-copper"],
         accent2="chitin-blue-black",
         shadow="yarn-shadow-brown",
         forbidden=["neon", "pastel"],
         light_type="нить ловит блик на сгибе: свет идёт по фактуре пряжи рядами, как спицы считают петли",
         sd_fragment="thread-silver over hoard-umber, knot-copper accents at the crossings, chitin-blue-black specular",
         mood="the-gift-still-warm",
         family="exp_color_wave_13", born_note="волна 13 «свет подземелья»"),
    dict(id="P266_FLOODED_VERDIGRIS", name="Flooded Verdigris",
         dominant=["waterline-verdigris", "pool-abyss-teal"],
         secondary=["basin-bronze"],
         accent1=["drop-silver"],
         accent2="gel-core-mint",
         shadow="undertow-shadow",
         forbidden=["neon", "dry earth"],
         light_type="паводок-патина: вода режет свет на водную линию, всё ниже линии — каустика, всё выше — тёплая медь чаши",
         sd_fragment="waterline-verdigris over pool-abyss-teal, basin-bronze rim, drop-silver beads at the line",
         mood="the-pool-that-keeps",
         family="exp_color_wave_13", born_note="волна 13 «свет подземелья»"),
    dict(id="P267_ARCHIVE_BRASS", name="Archive Brass",
         dominant=["archive-brass", "shelf-umber"],
         secondary=["ledger-cream"],
         accent1=["rune-glow-amber"],
         accent2="clay-warm",
         shadow="stack-shadow-brown",
         forbidden=["neon", "cold blue"],
         light_type="латунь архива: тёплые углы полок собирают свет, руны держат ленивое внутреннее свечение",
         sd_fragment="archive-brass over shelf-umber, ledger-cream pages, rune-glow-amber at the joints",
         mood="the-memory-that-wears",
         family="exp_color_wave_13", born_note="волна 13 «свет подземелья»"),
    dict(id="P268_DUSK_BINDING", name="Dusk Binding",
         dominant=["dusk-bind-violet", "corridor-stone"],
         secondary=["seam-light-teal"],
         accent1=["star-fleck-pale"],
         accent2="smoke-depth-black",
         shadow="threshold-shadow",
         forbidden=["hard noon", "neon"],
         light_type="сумеречная привязь: тьма здесь — материя, свет договаривается с ней по швам; тень носит одежду вместо той, что её носит",
         sd_fragment="dusk-bind-violet over corridor-stone, seam-light-teal at the edges, star-fleck-pale points",
         mood="the-dark-that-fits",
         family="exp_color_wave_13", born_note="волна 13 «свет подземелья»"),
    dict(id="P269_DUNGEON_HEART", name="Dungeon Heart",
         dominant=["heart-carmine", "abyss-indigo"],
         secondary=["throne-stone-grey"],
         accent1=["pulse-gold"],
         accent2="tail-rim-gold",
         shadow="depth-shadow-indigo",
         forbidden=["neon", "pastel"],
         light_type="сердце подземелья: пульс кармина идёт из глубины медленными тактами, тронный камень ловит его отражением",
         sd_fragment="heart-carmine over abyss-indigo, pulse-gold beat at the depth, throne-stone-grey at the seat",
         mood="the-pulse-below",
         family="exp_color_wave_13", born_note="волна 13 «свет подземелья»"),
]

WAVE13_MAP = {w['id']: w for w in WAVE13}

def pal_line(pid, sig, wave13=None):
    if pid in WAVE13_MAP:
        w = WAVE13_MAP[pid]
        return f"{w['name']} palette, {w['sd_fragment']}; her colors: {sig}."
    p = PALMAP[pid]
    frag = p.get('sd_fragment', '')
    return f"{p['name']} palette, {frag}; her colors: {sig}."

# ────────────────────────── каналы волны 15 (10 кандидатов ☠) ──────────────────────────
WAVE15_CHANNELS = [
    ("dawn-shawl-shift", "Dawn Shawl Shift", "P01",
     "смена рассвета: шаль ночи соскальзывает с обоих плеч, бретели ловятся на сгибах локтей — сияние наклоняется узнать свою"),
    ("verdict-lace-knot", "Verdict Lace Knot", "P02",
     "корсет зашнурован до последней пары люверсов без узла: пока узла нет, счёт открыт — ладони прижаты поверх шнуровки"),
    ("tar-shape-kept", "Tar Shape Kept", "P03",
     "смоляная ловушка взяла её форму и осталась держать: лист держит линию груди, вес честно осел на локтях, камера снизу"),
    ("plate-wave-towel", "Plate-Wave Towel", "P04",
     "водяная плита сработала: полотенце поймано на пол-скольжения, оба кулака прижимают к груди, мокрая кромка тянет вниз"),
    ("throne-verdict-lean", "Throne Verdict Lean", "P05",
     "откинулась на обеих ладонях подлокотников: ворот распахнулся наклоном, ткань мостом по рёбрам — зал принят в собственность"),
    ("cold-gate-shawl", "Cold-Gate Shawl", "P06",
     "ледяной шлюз открыт на инспекцию: шаль натянута обеими ладонями поперёк груди, гусиная кожа честно по ключицам"),
    ("echo-hall-bow", "Echo-Hall Bow", "P07",
     "поклон эхо-зала: застёжка плаща расстёгнута на пол-поклона, шёлк сполз с плеч и собрался в сгибах локтей"),
    ("bier-shelf-certify", "Bier Shelf Certify", "P08",
     "полка оссуария сертифицирована лично: лежит на каменном ложе, руки скрещены на груди с веточкой, дыхание поднимает ладони"),
    ("reception-handspan", "Reception Handspan", "P09",
     "наклон к гостю на пядь от линзы: колено на сиденье рядом со зрителем, вес на опорной ладони, губы у верхней кромки кадра"),
    ("haul-count-won", "Haul Count Won", "P10",
     "ночной пересортиров клада: щека в ладони, локоть на столе, глаза в полуприкрытии — день пересчитан, всё блестящее при ней"),
]

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

# ══════════════════ ОС P01–P03 (EXQUISITE · канон VERBATIM · жребий) ══════════════════

slot("P01", "sol-dawn-shawl-shift", "EXQUISITE · Sol · R+ · Y26 · P48_AURORA_SILK",
     channel="dawn-shawl-shift",
     corridor="A",
     oc_theme="DawnBreaker: предмет = the night-shawl slipping off both shoulders.",
     thesis=("«РАССВЕТОЛОМ: ОНА СПУСКАЕТСЯ В ПОДЗЕМЕЛЬЕ СО СВОИМ РАССВЕТОМ — НОЧНАЯ ШАЛЬ СОСКАЛЬЗЫВАЕТ С ОБОИХ ПЛЕЧ, "
             "БРЕТЕЛИ ЛОВЯТСЯ НА СГИБАХ ЛОКТЕЙ, И СИЯНИЕ ПОТОЛКА НАКЛОНЯЕТСЯ К НЕЙ, КАК СОБАКА, УЗНАВШАЯ ХОЗЯЙКУ. "
             "СВЕТ НЕ БОРЕТСЯ С ТЬМОЙ — ОН ЕЁ СМЕНЯЕТ. КАРТЬЕ СМЕНЫ ВИСИТ НА ЕЁ УШЕ-СЕРЬГЕ. ЭТО НЕ ПОЗА — СМЕНА»."),
     gag=("Гэг-стек (4 фишки OC): 1) шаль-ночь — шёлковая шаль цвета беззвёздной синевы соскальзывает с обоих плеч одновременно, "
          "как темнота, которую больше не пускают в помещение; 2) серьга-клетка на висячем лисьем ухе — золотая серьга-картье: "
          "бирка смены, светает в 6:40; 3) уши висят вдоль скул (канон: никогда не встают) — но кончики дрожат, когда сияние "
          "узнаёт свою; 4) зрачки-щели раскрываются в рассветные овалы — единственные часы, где можно увидеть её время."),
     spine="Y26 Shawl-Slip Stand (eye-level close, combo→Y26, карта-стенд) · CAM— eye level close · LEAD the slipping night · shift register · upper body close",
     race="— (канон VERBATIM, oc-canon.json: Sol, II — The High Priestess)",
     gar="ночная шаль цвета беззвёздной синевы (объект карты; полусъём) + топ на тонких бретелях под шалью (бретели ловятся на локтях — физика карты) · HS: канон (long silver-white layered hair, messy side bangs over one eye)",
     stack=["CR-E60", "CR-B40", "CR-S18", "CR-W44"],
     ycard="Y26",
     pos=[
         "Masterpiece, best quality, absurdres, intricate details, eye-level close, upper body, the night-shawl slipping off both shoulders, 1girl, solo, her breast shape held by the shawl's last silk, long silver-white thick layered hair, messy side bangs partially covering one eye, bright amber eyes with slit pupils, dark bronze skin, fox ears hanging beside the head, large gold hoop earrings on the fox ears, soft feminine build, full soft breasts, mid_dawnshift,",
         "the night-shawl half-off both shoulders, straps caught at the elbow folds, the silk reading her breast shape where it still holds — the shift itself is the claim, dawn-made,",
         weave("Y26"),
         "the shawl's silk pooling at both elbow creases, small gemstone earrings beside the hoops drinking the ceiling's current, a brass shift-tag clipped to one gold hoop,",
         "the top's thin straps caught at the elbow folds honest, the shawl's weight given to the slipping, nothing underneath the silk but the hour it ended —",
         "the night-shawl sliding off both shoulders, straps caught at the elbows,",
         "the ceiling's aurora bending its green current down toward her like a bow-wave, the corridor's old bracket nails long cold and holding only moss, the stair's first step behind her already brighter than the last,",
         pal_line("P48_AURORA_SILK", "the shift she brings down with her"),
     ],
     negx=" ears perked, tail, shawl gone",
     face="stylized 2D anime face to the lens, anime eyes (bright amber, slit pupils opening to dawn ovals), small nose, small mouth at rest, one silver-white layer crossing the lens-side cheek.",
     )

slot("P02", "noir-verdict-lacing", "EXQUISITE · Noir · R+ · Y34 · P218_NIELLO_BLACK",
     channel="verdict-lace-knot",
     corridor="A",
     oc_theme="Kill Confirmed: предмет = the last pair of grommets with no knot.",
     thesis=("«ПОДТВЕРЖДЕНИЕ УЗЛОМ: КОРСЕТ ЗАШНУРОВАН ДО ПОСЛЕДНЕЙ ПАРЫ ЛЮВЕРСОВ — УЗЛА НЕТ. ПОКА УЗЛА НЕТ, СЧЁТ ОТКРЫТ: "
             "КТО-ТО В ЭТОМ ЯРУСЕ ЕЩЁ ДЫШИТ. ЛАДОНИ ПРИЖАТЫ ПЛОСКО ПОВЕРХ ШНУРОВКИ, ЛЕНТА НАТЯНУТА ЧЕСТНО, "
             "КОРОНА-КОЛЬЦО ГОРИТ РОВНО — БЕЛЫМ СТАНОВИТСЯ ТОЛЬКО В МОМЕНТ. ЯРУС ЗАЧИЩЕН — ОНА ЗАВЯЖЕТ УЗЕЛ, "
             "КОГДА ПЕРЕСЧИТАЕТ ВСЁ. УБИЙСТВО НЕ КРАСИТ — ЕГО ПОДТВЕРЖДАЮТ»."),
     gag=("Гэг-стек (4 фишки OC): 1) корона-кольцо над головой — mirror-grey центр, ember-faint края; ровность кольца = ровность её; "
          "вспышка белым = подтверждение; 2) микрочёлка правит бровь ровно, как гравировка — линия, по которой читают вердикт; "
          "3) шнуровка без узла — последняя пара люверсов держит ленту трением и честностью; 4) на языке палача — ни крови, "
          "ни следа: подтверждение живёт узлом, не результатом (закон ANTI)."),
     spine="Y34 No-Knot Lacing Stand (eye-level close, combo→Y34, карта-стенд) · CAM— eye level close · LEAD the open verdict · niello register · upper body close",
     race="— (канон VERBATIM, oc-canon.json: Noir, Ace of Swords)",
     gar="чёрный корсет на шнуровке, лента до последней пары люверсов, узел не завязан (объект карты; канон-тема Kill Confirmed) · HS: канон (long straight ash-lilac hair, micro-fringe)",
     stack=["CR-M15", "CR-B41", "CR-E55", "CR-S18"],
     ycard="Y34",
     pos=[
         "Masterpiece, best quality, absurdres, intricate details, upper body at eye level, close on the laced front, palms pressed flat, 1girl, solo, her breast shape held taut behind the lacing, long straight ash-lilac hair with a micro-fringe, umbral-purple eyes wide and calm, eclipse-dusk skin, white-hot corona ring hovering above her head, slender young build, small softly-mounded chest, mid_verdictlacing,",
         "the black corset laced to the last pair of grommets, ribbon hauled taut, the lacing reading her breast shape held honest, palms pressed flat over the laced gap — the open knot is the claim, verdict-made,",
         weave("Y34"),
         "the corset's grommets in a descending line of niello brass, the ribbon's tail hanging one deliberate span, the corona ring's mirror-grey center holding the corridor's whole reflection,",
         "the lacing's tension honest across the ribs, both palms flat over the gap, nothing underneath the corset's line but the count she keeps —",
         "the corset laced to the last grommets with the ribbon taut and the knot deliberately untied,",
         "the cleared floor swept of its dust like a page turned, the level's old banners hanging quiet, the corridor's depth behind her empty in both directions and hers to certify,",
         pal_line("P218_NIELLO_BLACK", "the verdict she keeps untied"),
     ],
     negx=" halo held, knot tied, corset slack",
     face="stylized 2D anime face level into the lens, anime eyes (umbral-purple, wide and calm), small nose, small mouth still, the micro-fringe ruling the brow line even.",
     )

slot("P03", "hana-tar-shape-kept", "EXQUISITE · Hana · R+ · Y497 · P54_ART_DECO_PLATINUM",
     channel="tar-shape-kept",
     corridor="A",
     oc_theme="Super Sexy Style! (SSS): предмет = the tar sheet holding her chest line.",
     thesis=("«СУПЕР-СЕКСИ-СТИЛЬ: СМОЛЯНАЯ ЛОВУШКА ПОПРОБОВАЛА ЕЁ СХВАТИТЬ — И ОСТАЛАСЬ С ФОРМОЙ. ЧЁРНЫЙ ГЛЯНЦЕВЫЙ ЛИСТ "
             "ВЗЯЛ ЕЁ ЛИНИЮ ГРУДИ И ДЕРЖИТ ЕЁ ТАМ, ГДЕ ВЗЯЛ; ВЕС ЧЕСТНО ОСЕЛ НА ЛОКТЯХ, КАМЕРА СНИЗУ. СТИЛЬ — ЭТО КОГДА "
             "ДАЖЕ ЛОВУШКА РАСПИСЫВАЕТСЯ В ПОЛУЧЕННОМ. ГРОССБУХ ОТКРЫТ НА СТРАНИЦЕ «ТАР-ВОРОТА: УСЛУГА ОКАЗАНА». "
             "ЗРАЧКИ-СЕРДЦА СТАВЯТ ПЕЧАТЬ»."),
     gag=("Гэг-стек (4 фишки OC): 1) зрачки-сердца винного красного — печать гроссбуха ставится взглядом; "
          "2) хвост-пата со сколотым кончиком лежит поверх смоляного листа — единственная линия, которую смола не взяла; "
          "3) латунная застёжка гроссбуха расстёгнута — страница «тар-ворота» уже ведётся; 4) крошечные обрывки крыльев "
          "на пояснице подрагивают — смола не достала и их."),
     spine="Y497 Tar-Sheet Stand (low camera to the drip line, combo→Y497, карта-стенд) · CAM— low camera · LEAD the kept shape · contract register · full figure from below",
     race="— (канон VERBATIM, oc-canon.json: Hana, V — The Hierophant)",
     gar="смоляной лист-занавес (объект карты; прикрытие формой, которую лист сам держит) + гроссбух на латунной застёжке в локтевом сгибе · HS: канон (long voluminous wavy pale ash-blonde hair)",
     stack=["CR-D46", "CR-B73", "CR-E60", "CR-S18"],
     ycard="Y497",
     pos=[
         "Masterpiece, best quality, absurdres, intricate details, full figure from below at the drip line, standing under the tar sheet's black glossy load, 1girl, solo, her breast shape kept in the tar's black gloss, long voluminous wavy pale ash-blonde hair, wine-red eyes with heart-shaped pupils, warm satin skin, tall curvy build, heavy soft breasts, small bat-wing frags at the small of the back, mid_tarshape,",
         "the tar sheet holding her breast shape where it took it, the black gloss hugged to the chest line, weight pooling honest at the elbows, the sheer sheet falling past her hips in one slow drip — the kept shape is the claim, contract-made,",
         weave("Y497"),
         "the tar's gloss mirroring the aurora overhead in one green thread, a spade-tail with a chipped tip resting on the sheet's surface, the brass-clasped ledger open in the crook of one elbow,",
         "the sheet's weight given to the elbows honest, the tar taking only the shape and not the wearer, nothing underneath the black gloss but the service rendered —",
         "standing under the tar's load with the weight pooling at her elbows, the sheet holding the line it took,",
         "the tar-gate's frame overhead worn smooth by a century of catches, the ledger's page already written in her own hand, the level's corridor stretching away dark and serviced,",
         pal_line("P54_ART_DECO_PLATINUM", "the shape the trap keeps"),
     ],
     negx=" horns, tail unchipped, ledger blank",
     face="stylized 2D anime face half-lit by the gloss from below, anime eyes (wine-red, heart-shaped pupils stamping the page), small nose, small mouth one note of satisfaction, one ash-blonde wave pasted glossy at the cheek.",
     )

# ══════════════════ R+-МЕЙНЫ P04–P10 (7 карт коридора A жребия) ══════════════════

slot("P04", "traptester-plate-wave", "VOLT · human · R+ · Y4 · P142_CHECKER_SLATE",
     channel="plate-wave-towel",
     corridor="A",
     thesis=("«ТЕСТИРОВЩИЦА ЛОВУШЕК: ВОДЯНАЯ ПЛИТА ОТРАБОТАЛА НА СЛАВУ — ВОЛНА ОКАТИЛА ПОПОЛАМ, ПОЛОТЕНЦЕ ПОЙМАНО "
             "НА ПОЛ-СКОЛЬЖЕНИЯ, ОБЕ ЛАДОНИ ПРИЖИМАЮТ ЕГО К ГРУДИ, МОКРАЯ КРОМКА ВСЁ ТЯНЕТ ВНИЗ. ГИДРОКОСТЮМ СПУЩЕН "
             "ДО ПОЯСА — РУКАВА УЖЕ ВНЕ. ДАВЛЕНИЕ В НОРМЕ, ИНТЕНСИВНОСТЬ ХОРОШАЯ, ТАЙМИНГ ЧЕСТНЫЙ. ЛОВУШКА ХОРОШАЯ — "
             "ЖИЛЬЁ ЛУЧШЕ ГОРОДА»."),
     gag=("Гэг-стек: старый ожог на предплечье залечен до глазури — калибровочная метка первой плиты; манометр на запястье "
          "влажный от волны; журнал испытаний размок — числа пишутся по памяти; неопреновые брюки держат волну, "
          "верх спросил тепла."),
     spine="Y4 Towel Mid-Slide Stand (upper body three-quarter, combo→Y4, карта-стенд) · CAM— three-quarter toward the lens · LEAD the caught wave · calibration register · upper body three-quarter",
     race="— (human-служба темы: тестировщица ловушек водяного яруса)",
     gar="CL-SM-07 (half-peeled wetsuit, neoprene folded at the waist) + CL-AC-03 (gold body chain in the valley) + полотенце (объект карты — прикрытие кулаками у груди) · HS: HS33 Wet Slick Low Bun",
     stack=["CR-W18", "CR-A14", "CR-S12", "CR-E35"],
     ycard="Y4",
     pos=[
         "Masterpiece, best quality, absurdres, intricate details, upper body three-quarter toward the lens, towel caught mid-slide at the chest, 1girl, solo, her breast shape under both fists' haul of the towel, chestnut hair in a wet slick low bun with a stray drip, hazel eyes bright with the reading, fair skin, healthy build, medium breasts, flat stomach, mid_platetest,",
         "the towel hauled flat to her chest by both fists, the terry reading her breast shape under the haul, the wet hem's drag still pulling down, nothing underneath the terry but the wave's own temperature — the caught wave is the claim, calibration-made,",
         weave("Y4"),
         "the wetsuit peeled to the waist with its arms out of the sleeves, a gold body chain in the valley between, an old burn healed to a smooth glaze on one forearm, a waterlogged test journal in one fist's grip, a brass whistle on a lanyard at her wrist, one diver's ring on her thumb,",
         "the neoprene's fold at the waist honest, both fists keeping the towel's line, water beading at the collarbone and running the chain's links,",
         "the towel mid-slide with both fists hauling it back flat, the wet hem dragging,",
         "the pressure gauge's needle still swinging behind the plate's sill, the test corridor's checker floor draining in one long sheet, the ceiling's aurora running green down the water's back,",
         pal_line("P142_CHECKER_SLATE", "the plate she signs off with her body"),
     ],
     negx=" wetsuit up, towel dropped, gauge still",
     face="stylized 2D anime face toward the lens, anime eyes (hazel, bright with the reading), small nose, small mouth mid-verdict, one drip off the bun's edge.",
     )

slot("P05", "ermine-throne-verdict", "VOLT · R69 Ermine-kin · R+ · Y14 · P132_GAMBIT_IVORY",
     channel="throne-verdict-lean",
     corridor="A + B",
     thesis=("«ИНСПЕКТРИСА: ОНА ОСМАТРИВАЕТ ТРОННЫЙ ЗАЛ КАК НАСЛЕДСТВЕННОЕ ИМУЩЕСТВО — ОТКИНУЛАСЬ НА ОБОИХ ЛАДОНЯХ "
             "ПОДЛОКОТНИКОВ, ВОРОТ РАСПАХНУЛСЯ НАКЛОНОМ, ТКАНЬ МОСТОМ НАТЯНУТА ПО РЁБРАМ. ЛАКОМЫЕ ЛОКТИ В КРУЖЕВЕ, "
             "ЧЁРНЫЙ КОНЧИК ХВОСТА СТАВИТ ВЕРДИКТ: ЗАЛ ПРОШЁЛ. ТРОН — ЭТО ТОЖЕ МЕБЕЛЬ, КОГДА ПРИШЛА ТЫ. "
             "ГЛАВНАЯ ИНСПЕКЦИЯ — УЮТ»."),
     gag=("Гэг-стек: чёрный кончик хвоста постукивает по подлокотнику — подпись вердикта; кружевные перчатки до локтей — "
          "инспекция не отменяет фасон; паетки платья сыплются монетами — зал принимает ценность; зимняя белизна меха "
          "против золота трона — две партии одной роскоши."),
     spine="Y14 Palm-Lean Throne (upper body three-quarter, combo→Y14, карта-стенд) · CAM— three-quarter, chest to the lens · LEAD the accepted hall · inheritance register · upper body three-quarter",
     race="R69 — горностай: помещение осматривается как наследство; вердикт ставит кончик хвоста.",
     gar="CL-DR-12 (backless sequin party dress, open back field) + CL-AC-04 (lace elbow gloves) · HS: HS08 High Sleek Ponytail, Nape-Tight",
     stack=["CR-W14", "CR-B12", "CR-E39", "CR-B53"],
     ycard="Y14",
     pos=[
         "Masterpiece, best quality, absurdres, intricate details, upper body three-quarter, chest to the lens, lean back on both palms at the throne's armrests, 1girl, solo, her breast shape bridged taut by the open collar, winter-white hair in a high sleek ponytail pulled tight at the nape, ice-blue eyes level one degree from smiling, snow-pale skin, ermine girl, winter-white fur, black tail-tip, human face, hourglass figure, medium breasts, slim waist, mid_verdictlean,",
         "the backless dress's collar opening by the lean, fabric bridges taut across the ribs, the sequins reading her breast shape by the bridge, nothing underneath the sequins' fall but the hall she just accepted — the accepted hall is the claim, inheritance-made,",
         weave("Y14"),
         "the sequins running coin-showers down the open back's field, lace elbow gloves to the crease, a black jet hairpin through the ponytail, the black tail-tip tapping its verdict on the armrest's gold,",
         "the lean's whole weight given to both palms at the armrests, the collar open to the sternum by the lean's honest angle,",
         "leaned back on both palms with the collar opening, the fabric bridging taut across the ribs,",
         "the throne hall's banners hanging in their century of quiet, the floor's ivory tiles holding her reflection in one long gambit line, the ceiling's aurora curving down to read the verdict with her,",
         pal_line("P132_GAMBIT_IVORY", "the estate she signs for"),
     ],
     negx=" tail plain, dress buttoned, lean forward",
     face="stylized 2D anime face level to the lens, anime eyes (ice-blue, one degree from smiling), small nose, small mouth holding the verdict, one white strand escaped at the temple.",
     )

slot("P06", "coldgate-shawl-hold", "VOLT · human · R+ · Y20 · P166_GLACIER_STEEL",
     channel="cold-gate-shawl",
     corridor="A",
     thesis=("«ХОЛОДНЫЙ ЯРУС, СМОТРИТЕЛЬНИЦА ШЛЮЗА: ПРОТОЧКУ ОТКРЫЛИ НА ИНСПЕКЦИЮ — МОРОЗ ПОШЁЛ ПО ЗАЛУ, "
             "И ОНА ВЦЕПИЛАСЬ ОБЕИМИ ЛАДОНЯМИ В ШАЛЬ, НАТЯНУЛА ПОПЕРЁК ГРУДИ. ГУСИНАЯ КОЖА ЧЕСТНО ПО КЛЮЧИЦАМ, "
             "КОЛОКОЛЬЧИК НА ОШЕЙНИКЕ ЗВЕНИТ ОТ ДРОЖИ. ХОЛОД — ЕЁ ВЕЩЬ: СЕГОДНЯ ОНА ЕГО РАСПЕЧАТАЛА ДЛЯ ГОСТЕЙ "
             "И САМА СТОИТ В ПОТОКЕ, ПОТОМУ ЧТО ХОЗЯЙКА НЕ МЕРЗНЕТ В СВОЁМ ДОМЕ»."),
     gag=("Гэг-стек: узор инея растёт по решётке шлюза быстрее, чем по её плану осмотра; бархатный чокер держит горло — "
          "единственное, что не отдаёт холоду; колокольчик на ошейнике звенит в такт дрожи — метроном мороза; "
          "халтер открытой спиной принимает весь поток — инспекция делается телом."),
     spine="Y20 Shawl-Haul Stand (eye-level close, combo→Y20, карта-стенд) · CAM— eye level close toward the lens · LEAD the opened cold · warden register · upper body close",
     race="— (human-служба темы: смотрительница ледяного шлюза)",
     gar="CL-TS-06 (backless halter top, knot between the shoulder blades) + CL-AC-01 (velvet choker) + CL-AC-06 (bell collar) + шерстяная шаль (объект карты — натянута кулаками) · HS: HS07 Low Loose Ponytail",
     stack=["CR-S13", "CR-M14", "CR-W30", "CR-B40"],
     ycard="Y20",
     pos=[
         "Masterpiece, best quality, absurdres, intricate details, close at eye level toward the lens, upper body, shawl hauled taut by both fists, 1girl, solo, her breast shape under the shawl's taut line, ash-brown hair in a low loose ponytail with face-framing strands, grey eyes watering bright in the cold, fair skin, average build, medium breasts, straight waistline, mid_coldgate,",
         "both fists hauling the wool shawl taut over her chest line, her breast shape read taut under the haul, the cold's goosebumps honest along the collarbones, nothing underneath the shawl's line but the warden's own winter — the opened cold is the claim, warden-made,",
         weave("Y20"),
         "the backless halter's bare back field taking the sluice's full draft, a thin velvet choker, neck accent, a small gold bell collar ringing with each shiver, frost ferns growing up the gate's bars behind her,",
         "the shawl's wool standing off her shape in a cold-stiff bell, both fists white-knuckled honest, breath leaving in one long ribbon,",
         "both fists hauling the shawl taut across the chest, goosebumps riding the collarbones,",
         "the sluice's inspection wheel locked open with a brass tag, the level's stored cold rolling out past her ankles in a slow fall, the ceiling's aurora gone glass-green over the ice,",
         pal_line("P166_GLACIER_STEEL", "the winter she keeps for guests"),
     ],
     negx=" shawl dropped, gate closed, bell silent",
     face="stylized 2D anime face bright in the draft, anime eyes (grey, watering bright), small nose pink at the tip, small mouth breathing ribbons, one strand frozen into a wave at the cheek.",
     )

slot("P07", "banshee-echo-bow", "VOLT · R49 Banshee-kin · R+ · Y31 · P174_ROSE_WINDOW",
     channel="echo-hall-bow",
     corridor="A",
     thesis=("«ЭХО-ЗАЛ, БАНШИ-СОЛИСТКА: ПОСЛЕ РЕПЕТИЦИИ ОНА РАСКЛАНИВАЕТСЯ ПУСТОМУ ЗАЛУ — ЗАСТЁЖКА ПЛАЩА РАССТЁГНУТА "
             "НА ПОЛ-ПОКЛОНА, ШЁЛК СПОЛЗ С ПЛЕЧ И СОБРАЛСЯ В СГИБАХ ЛОКТЕЙ. ТЮЛЬ-ПЛАТЬЕ ДЫШИТ ПОДО ВЕТОМ ПОДВЯЗКИ. "
             "СЛЁЗНЫЕ ДОРОЖКИ БЛЕСТЯТ — ОНА СМЕЁТСЯ РЕДКО И НАРОЧНО, И ЭТО ЛУЧШЕЕ, ЧТО МОЖЕТ УСЛЫШАТЬ СТЕКЛО. "
             "ЭХО АПЛОДИРУЕТ ТЕМ, КТО МОЛЧИТ ДО ВЕРНОЙ НОТЫ»."),
     gag=("Гэг-стек: серебристые слёзные дорожки на щеках — сцена банши, не печаль; стеклянные панели зала целы — "
          "смех придержан, поклон вместо ноты; шёлковая подкладка плаща собралась в локтях, как аплодисменты ткани; "
             "подвязки-помочи качаются в такт последнему выдоху."),
     spine="Y31 Mid-Bow Clasp Stand (eye-level close, combo→Y31, карта-стенд) · CAM— eye level close into the bow · LEAD the held note · encore register · upper body close",
     race="R49 — банши: голос ломает стекло только со смеха; она смеётся редко — и нарочно.",
     gar="CL-DR-09 (tulle petticoat dress, tiers hazing the light) + CL-AC-09 (loose suspenders swinging) + шёлковый плащ с расстёгнутой застёжкой (объект карты — сползает с плеч) · HS: HS06 Deep Side Wave, Over One Shoulder",
     stack=["CR-B66", "CR-E54", "CR-D44", "CR-A17"],
     ycard="Y31",
     pos=[
         "Masterpiece, best quality, absurdres, intricate details, upper body close, eye-level bow to the lens, silk sliding off both shoulders, 1girl, solo, the tulle's tiers hazing her breast shape, silver-grey hair in deep side-parted waves swept over one shoulder, mist-green eyes bright from the held note, pale skin, banshee girl, tear-trail shimmer lines down the cheeks, human face, slim lithe body, medium breasts, flat stomach, mid_echobow,",
         "the cape's silk pooling in the elbow folds honest, the tulle's tiers reading her breast shape through their haze, nothing underneath the sliding silk but the encore she owes — the held note is the claim, encore-made,",
         weave("Y31"),
         "the cape's clasp swinging open at the collarbone, a ribbon-tied choker at the throat, small silver ear studs, loose suspenders riding the tulle's fall, the tear-trails holding their permanent silver glint, every glass pane of the hall intact and listening,",
         "the silk's slide caught at both elbow creases, the bow's incline given to the empty front row,",
         "the clasp undone mid-bow, silk off both shoulders pooling in the folds,",
         "the echo hall's seats holding their velvet dark, the rehearsal's last chord still walking the balcony rails, the ceiling's aurora leaning down through the rose window in one slow bow of its own,",
         pal_line("P174_ROSE_WINDOW", "the note she keeps unspent"),
     ],
     negx=" glass cracked, cape clasped, laugh open",
     face="stylized 2D anime face inclining into the bow, anime eyes (mist-green, bright from the held note), small nose, small mouth curved on the unspent laugh, one tear-trail catching the window's ruby.",
     )

slot("P08", "ossuary-shelf-certify", "VOLT · human · R+ · Y35 · P127_SEAM_PORCELAIN",
     channel="bier-shelf-certify",
     corridor="A",
     thesis=("«СМОТРИТЕЛЬНИЦА ОССУАРИЯ: ПОЛКА №7 СВОБОДНА — И ОНА ЛЕЖИТ НА КАМЕННОМ ЛОЖЕ, ЧТОБЫ СЕРТИФИЦИРОВАТЬ ЕГО "
             "ЛИЧНО: ОБЕ РУКИ СКРЕЩЕНЫ НА ГРУДИ, В ЛАДОНЯХ ВЕТОЧКА МИРТА, ДЫХАНИЕ ЕЩЁ ПОДНИМАЕТ СКРЕЩЁННЫЕ ЛАДОНИ — "
             "РАЗ В ТАКТ. ФАТА-ПЛАТЬЕ ЛЕЖИТ КАК ПОЛОТНО ИНВЕНТАРЯ. ЧЕРЕПА-ФОЛИАНТЫ ЖДУТ ОЧЕРЕДИ. ПОДЗЕМЕЛЬЕ ОТВЕЧАЕТ "
             "ЗА КАЧЕСТВО СНА — И ПОЛКА УДОБНАЯ»."),
     gag=("Гэг-стек: регистрационная карточка на ложе заполнена её почерком — «полка №7, мягкость 9/10»; "
          "черепа-фолианты подписаны бирками каталога — ни один не читается, все на месте; веточка мирта — "
          "единственный свежий предмет в ярусе; кимоно распахнуто поверх фаты — парадная форма смотрительницы."),
     spine="Y35 Bier-Certify Stand (slight high angle, combo→Y35, карта-стенд) · CAM— slight high angle, profile along the bier · LEAD the certified shelf · registry register · upper body profile",
     race="— (human-служба темы: смотрительница оссуария, регистратор полок)",
     gar="CL-DR-10 (ceremonial veil dress, three layers of sheer) + CL-LG-04 (open silk kimono, obi loose) · HS: HS11 Crown Braid Halo",
     stack=["CR-D35", "CR-B71", "CR-W62", "CR-S19"],
     ycard="Y35",
     pos=[
         "Masterpiece, best quality, absurdres, intricate details, upper body profile along the bier, slight high angle, lying back on the stone, 1girl, solo, her breast shape soft under the crossed hands, black hair in a crown braid halo, ink-grey eyes patient with the count, fair skin with freckles dusted across the nose bridge, soft belly, stomach fold at the lie, medium breasts, mid_shelfcertify,",
         "the veil dress's sheer layers lying flat as inventory cloth, forearms crossed over the chest holding the sprig, her breast shape reading soft under the crossed forearms, nothing underneath the registers' linen but the certification itself — the certified shelf is the claim, registry-made,",
         weave("Y35"),
         "the silk kimono open at the sides of the lie, the myrtle sprig fresh in the crossed palms, the shelf's registration card filled in her own hand, skull-folios shelved spine-out with catalogue tags,",
         "the lie's whole weight given to the stone honest, the sheer layers breathing with her once per beat,",
         "lying back along the bier with the forearms crossed over the chest, the breath lifting them,",
         "the ossuary's stacks running shelf on shelf into the polite dark, the reading rail polished by a century of catalogue gloves, the ceiling's aurora gone porcelain-green over the pale rows,",
         pal_line("P127_SEAM_PORCELAIN", "the sleep she signs for"),
     ],
     negx=" sitting up, sprig gone, shelves empty",
     face="stylized 2D anime face in profile along the stone, anime eyes (ink-grey, patient with the count), small nose, small mouth mid-number, one braid-loop under the cheek like a pillow's seam.",
     )

slot("P09", "fortunecat-reception-bet", "VOLT · R52 Fortune-cat-kin · R+ · Y413 · P186_EMERALD_TOLL",
     channel="reception-handspan",
     corridor="A",
     thesis=("«РЕСЕПШЕН ПОДЗЕМЕЛЬЯ, КОТИ-ДАЙФОРТУНА: ГОСТЬ ПОЛУЧАЕТ СТАВКУ ПРИ ВХОДЕ — ОНА НАКЛОНЯЕТСЯ СБОКУ "
             "НА ПЯДЬ ОТ ЛИНЗЫ, КОЛЕНО НА СИДЕНЬЕ РЯДОМ СО ЗРИТЕЛЕМ, ВЕС НА ОПОРНОЙ ЛАДОНИ. ПРАВАЯ ЛАПА ПОДНЯТА — "
             "УДАЧА ИДЁТ ПЕРВОЙ, ВХОД — ВТОРЫМ. МОНЕТНЫЙ ЗНАК У КЛЮЧИЦЫ ЖДЁТ ОПЛАТЫ. КАЗИНО ЕЁ ВЫГНАЛО — "
             "ПОДЗЕМЕЛЬЕ ПРИНЯЛО НА РАБОТУ»."),
     gag=("Гэг-стек: правая лапка поднята и не опускается — так принято у входа; монетный знак у ключицы — прорезь "
          "приёмника, входная монета сюда; крапчатые уши-триколор поворачиваются на шаг гостя раньше двери; "
          "золотой свет любит её крапинки — смена начинается."),
     spine="Y413 Handspan Lean-In (POV from beside the viewer, combo→Y413, карта-стенд) · CAM— POV beside · LEAD the first bet · house register · upper body POV",
     race="R52 — коти-удачи: правая лапа правда приносит удачу — казино её выгнало, и она этим гордится.",
     gar="CL-TS-06 (backless halter top, knot between the shoulder blades) + CL-AC-01 (velvet choker) · HS: HS66 Ear-Slot Cut",
     stack=["CR-B59", "CR-E46", "CR-B25", "CR-G10"],
     ycard="Y413",
     pos=[
         "Masterpiece, best quality, absurdres, intricate details, upper body POV from beside the viewer, leaning in a hand-span from the lens, 1girl, solo, her breast shape read at the halter's lean, blonde hair with calico patches in an ear-slot cut, gold-coin eyes bright with the house's welcome, warm ivory skin, fortune cat girl, calico ears, coin mark at the collar, human face, pear figure, small breasts, wide hips, mid_receptionbet,",
         "the halter's bare back field facing the door draft, the halter reading her breast shape at the lean's angle, one knee on the seat beside the viewer, weight on the planted palm, nothing underneath the house's welcome but the bet itself — the first bet is the claim, house-made,",
         weave("Y413"),
         "the raised right paw held up in the greeting, a velvet choker, collarbone shadow, the coin mark's slot glinting, the toll's coin string coiled at the counter's edge, the halter's knot riding between the shoulder blades,",
         "the lean's whole weight on one planted palm, the knee's claim on the seat honest, lips at the top frame edge mid-whisper,",
         "leaning in a hand-span from the lens, the halter's strap slipped at the shoulder, one knee up on the seat, eyes straight in,",
         "the reception's coin-tray stacked with yesterday's tolls, the guest ledger open to a fresh line, the level's first corridor rolling out its green carpet of aurora behind her,",
         pal_line("P186_EMERALD_TOLL", "the toll she bets on you"),
     ],
     negx=" paw down, whisper finished, ledger closed",
     face="stylized 2D anime face a hand-span from the lens, anime eyes (gold-coin, straight into the lens), small nose, small mouth mid-whisper at the frame's top edge, one calico ear turned to the door behind.",
     )

slot("P10", "magpie-haul-count", "VOLT · R63 Magpie-kin · R+ · Y228 · P159_GILDED_LAND_WARM",
     channel="haul-count-won",
     corridor="A",
     thesis=("«СОКРОВИЩНИЦА-СКЛАД, НОЧНОЙ ПЕРЕСОРТ: ЩЕКА В ЛАДОНИ, ЛОКОТЬ НА СТОЛЕ, ГЛАЗА В ПОЛУПРИКРЫТИИ — "
             "ПОСЛЕДНЯЯ СТРОЧКА ИНВЕНТАРЯ. ШЁЛКОВЫЙ ХАЛАТ РАСПАХНУТ, ПЕРЕДНИК ДЕРЖИТ ПЕРЕД. ВСЁ БЛЕСТЯЩЕЕ ПЕРЕСЧИТАНО "
             "И ПРИ НЕЙ: ЖИЛА ГРУДИ ЧИТАЕТСЯ СКВОЗЬ ШЁЛК. ДЕНЬ ПОДЗЕМЕЛЬЯ ЗАКОНЧЕН — И ОН ЗАКОНЧЕН В ЕЁ ПОЛЬЗУ»."),
     gag=("Гэг-стек: перья вспыхивают ирисом на повороте — единственная валюта, которую она не считает; "
          "крошечная татуировка на запястье спрятана под строкой учёта; пояс передника завязан бантом назад — "
          "апрон инвентаря; горсть монет остывает в ладони не-опорной руки."),
     spine="Y228 Cheek-In-Palm Count (upper body three-quarter, combo→Y228, карта-стенд) · CAM— three-quarter over the table · LEAD the won day · audit register · upper body three-quarter",
     race="R63 — сорока: всё блестящее — её, пока не доказано обратное; пересортировка — nightly ритуал.",
     gar="CL-LG-03 (open silk robe, belt hanging unused) + CL-DR-11 (linen pinafore dress, bare shoulders above) · HS: HS04 Wolf Cut, Choppy",
     stack=["CR-W20", "CR-E26", "CR-B14", "CR-D47"],
     ycard="Y228",
     pos=[
         "Masterpiece, best quality, absurdres, intricate details, three-quarter over the table, upper body, cheek in palm, elbow planted, 1girl, solo, her breast shape read through the pinafore's bib, black hair with one white wing-streak in a choppy wolf cut, amber eyes half-mast with the count, light olive skin, magpie girl, black-white magpie ears and wings, front-closure pinafore, human face, tall soft frame, medium breasts, mid_haulcount,",
         "the open robe's front reading her breast shape through the pinafore's bib, the ledger's weight hugged to the chest in the free arm's crook, the silk's belt hanging unused, nothing underneath the audit but the winnings — the won day is the claim, audit-made,",
         weave("Y228"),
         "the pinafore's straps crossing the bare shoulders above the bib, a tiny inner-wrist tattoo under the ledger line, a brooch of one bright theft pinned to the bib, black feathers flashing iridescent at the half-turn, a palm of counted coins going cold beside the book,",
         "the elbow's plant honest on the table, the cheek's whole weight given to the palm, the robe's drape pooling off one shoulder,",
         "the cheek in the palm, elbow on the table, eyes half-mast, the argument of the whole day won,",
         "the treasury's shelves sacked neat into labelled drawers, the tally-book's last line still wet, the ceiling's aurora running one gold thread along the coin-edges,",
         pal_line("P112_POCKET_THEFT_GOLD", "the gold she counts twice"),
     ],
     negx=" wings gone, coins scattered, belt tied",
     face="stylized 2D anime face in the palm, anime eyes (amber, half-mast), small nose, small mouth on the last number, one white streak forward across the brow.",
     )

# ══════════════════ R-МЕЙНЫ P11–P22 + PG-13 P23–P24 ══════════════════

slot("P11", "axolotl-thermal-sands", "NICHE · R67 Axolotl-kin · R · Y37 · P57_SUNSET_ON_WATER",
     channel=None, corridor="A + B",
     thesis=("«ТЕРМАЛЬНЫЕ ПЕСКИ, НИЖНИЙ ЯРУС: ГРЕЕТСЯ ВСЯ СМЕНА — ОНА ОТКИНУЛАСЬ НА ОБОИХ ЛАДОНЯХ В ТЁПЛЫЙ ПЕСОК, "
             "ОДНА БРЕТЕЛЬ БИКИНИ СОСКОЛЬЗНУЛА С ЗАПЕЧЁННОГО ПЛЕЧА, ПОСЛЕДНЯЯ ВОЛНА СТЕКАЕТ ПО РЁБРАМ. "
             "ЖАБЕРНЫЕ КРАПИВКИ ТРЕПЕЩУТ — ГДЕ-ТО ВКЛЮЧИЛИ МУЗЫКУ. ПЛЯЖ ПОДЗЕМЕЛЬЯ ТЕПЛЫЙ КРУГЛЫЙ ГОД, "
             "И ЭТО ЕГО ГЛАВНЫЙ СЕКРЕТ, КОТОРЫЙ НИКТО НЕ СПРАШИВАЛ»."),
     gag=("Гэг-стек: жаберные кристы розовеют в такт музыке — вкус не спрятать; загар линиями бикини — два часовых "
          "пояса одного тела; песок липнет к мокрым икрам — термометр яруса; улыбка.axolotl постоянная — "
          "утечка счастья в профиль."),
     spine="Y37 Sand Lean-Back (water-line from below, combo→Y37, карта-стенд) · CAM— water-line from below · LEAD the warm hour · spa register · upper body from below",
     race="R67 — аксолотль: кристы трепещут от музыки — вкус не спрячешь; тёплые пески — её смена отдыха.",
     gar="CL-SM-02 (halterneck bikini, knot at the nape, back bare to the waistband) · HS: HS22 Cloud of Natural Curls",
     stack=["CR-S10", "CR-I14", "CR-D52", "CR-B61"],
     ycard="Y37",
     pos=[
         "Masterpiece, best quality, absurdres, intricate details, upper body from below at the water line, lean back on both palms in the warm sand, 1girl, solo, pink hair in a cloud of natural curls darkened damp at the edges, soft brown eyes half-closed in the heat, peach skin flushed at the chest, axolotl girl, pink external gill frills at the neck, permanent small smile, human face, soft settled build, medium-soft breasts, mid_thermalsands,",
         "the halterneck bikini's one strap slipping off the sunburned shoulder, the last wave sheeting down the ribs, the warm sand holding both planted palms,",
         weave("Y37"),
         "the gill frills fluttering translucent pink to the level's piped music, tan lines framing what the bikini covered, wet sand clinging to the damp calves,",
         "the lean's weight on both palms beside her hips, the waterline crossing her hip line honest, the strap's escape one knuckle from caught,",
         "leaned back on both palms in the warm sand, one strap off the shoulder, the wave's sheet still running down,",
         "the thermal vent's warm breath moving the sand in slow dunes, the flooded level's tide keeping its one long swell, the ceiling's aurora gone sunset-warm over the wet,",
         pal_line("P57_SUNSET_ON_WATER", "the warm hour she clocked"),
     ],
     negx=" frills still, strap tied, sand dry",
     face="stylized 2D anime face half-closed in the heat, anime eyes (soft brown, half-lidded), small nose, small mouth in the permanent small smile, one gill frill trembling to the beat.",
     )

slot("P12", "mole-cart-saddle", "NICHE · R70 Mole-kin · R · Y5 · P206_TUNNEL_MOSS",
     channel=None, corridor="B",
     thesis=("«ВАГОНЕТЧНАЯ ЛИНИЯ: КАРТОГРАФЕССА ВЕРХОМ НА СЕДЛЕ ПОДЪЁМНИКА — ПОДОЛ НАТЯНУТ ПО БЁДРАМИ РАЗВОДОМ КОЛЕН, "
             "СВЕТ СНИЗУ. ПАЛЬЦЕВЫЕ ПАДОШКИ ЧИТАЮТ РУЧКУ ТОРМОЗА КАК ШРИФТ БРАЙЛЯ: ТОННЕЛЬ №12 ЗДЕСЬ ПОВОРАЧИВАЕТ "
             "ЛЕВЕЕ, ЧЕМ ГОВОРИТ ПЛАН. ДЖИНСА ДЕРЖИТ СТРЕСС БЕЛЫМ, КОМАНДА ПОДЗЕМЕЛЬЯ — ЕЁ ЦВЕТА. "
             "КАРТА ПОДЗЕМЕЛЬЯ ЛЕЖИТ В ЛАДОНИ ПАДОШКАМИ»."),
     gag=("Гэг-стек: звёздчатые пады на пальцах — читают рельеф вместо глаз; розовые щёлочки-глаза жмурятся от любого "
          "света ярче сумерек — и счастливы; веснушечное поле по плечам и переносице — созвездие тоннелей; "
          "пом-поны на сиденье вагонетки — катаются с ней смену."),
     spine="Y5 Pommel Straddle (three-quarter from below, combo→Y5, карта-стенд) · CAM— three-quarter from below · LEAD the read tunnel · survey register · upper body from below",
     race="R70 — крот: текстуры читаются пальцами как брайль; каждая комната — библиотека.",
     gar="CL-BT-01 (cutoff denim shorts, frayed hems) + CL-TS-04 (thin ribbed tank top) + CL-FX-07 (cheer crop set in the level's colors, pom-poms stowed) · HS: HS21 Tousled Pixie Crop",
     stack=["CR-F02", "CR-W22", "CR-E38", "CR-D63"],
     ycard="Y5",
     pos=[
         "Masterpiece, best quality, absurdres, intricate details, upper body three-quarter from below, straddle-settle over the cart's saddle, 1girl, solo, warm brown hair in a tousled pixie crop, pink squint eyes reading the brake handle, light tan skin with a freckle field across the shoulders and the bridge of the nose, mole girl, tiny round snout, star-shaped fingertip pads, human face, thick thighs, wide hips, small breasts, mid_cartsaddle,",
         "the cutoff shorts' hem hauled taut across both thighs by the knee spread, the denim worn white at the stress points, midriff bare below the cheer crop's knot,",
         weave("Y5"),
         "star-shaped fingertip pads flat on the brake's brass, a keyring of passage keys hooked to the cart's rail, the tank's straps honest and narrow, the cart's latch catching with a jolt up one arm,",
         "the saddle's pommel line honest under the settle, the knees wide past the cart's sides, the cheer skirt's pleats riding the straddle,",
         "straddled over the saddle with the hem taut across both thighs, the knee spread holding the line,",
         "the tunnel's moss line running level with the rail, the junction's chalk arrows pointing two ways at once, the ceiling's aurora kept green and patient overhead,",
         pal_line("P206_TUNNEL_MOSS", "the tunnel she reads by hand"),
     ],
     negx=" pads gloved, eyes wide open, skirt still",
     face="stylized 2D anime face squinting happily, anime eyes (pink squint, nearly closed), small round snout, small mouth on the turn's count, freckles deep across the bridge.",
     )

slot("P13", "lynx-grate-hop", "NICHE · R64 Lynx-kin · R · Y118 · P167_MOSS_GOLD",
     channel=None, corridor="—",
     thesis=("«САДОВЫЙ ЯРУС, РЕШЁТКА: ОНА СПРЫГИВАЕТ С БОРТИКА НА ПОЛ-СМЕНЫ — ОДНА СТОПА УЖЕ СВЕТЛА, ВТОРАЯ НОГА "
             "ЕЩЁ ВИСИТ В ВЫСОТЕ, ВОЛОСЫ ОПОЗДАЛИ НА ПОЛ-ТАКТА. КИСТИ УШЕЙ УЖЕ РАЗВЁРНУТЫ ВНИЗ — ТУДА, КУДА "
             "ОНА ТОЛЬКО СОБИРАЕТСЯ. САД ЗНАЕТ ЕЁ ПРИХОД РАНЬШЕ ШАГОВ. ЛИНКС-КОМПАС НЕ ОШИБАЕТСЯ — ОПАЗДЫВАЕТ "
             "ТОЛЬКО ГРАВИТАЦИЯ»."),
     gag=("Гэг-стек: кисти-локаторы развёрнуты вниз раньше приземления — интерес идёт первым; короткий хвост-боб "
          "даёт импульс прыжка — руль породы; мох на бортике держит след прошлой посадки — сад считает визиты; "
          "золотой свет первого касания — любая комната отдаёт ей первую минуту."),
     spine="Y118 Grate Hop-Down (upper body three-quarter, combo→Y118, карта-стенд) · CAM— three-quarter mid-air · LEAD the early ears · scout register · upper body three-quarter",
     race="R64 — рысь: кисти ушей указывают на всё, что интересно, — компас внимания.",
     gar="садовая смена: трикотажный топ + юбка-шорты (карта без класса — коды не назначаются) · HS: HS02 Shoulder Shag + Curtain Bangs",
     stack=["CR-D24", "CR-B31", "CR-S09", "CR-D45"],
     ycard="Y118",
     pos=[
         "Masterpiece, best quality, absurdres, intricate details, upper body three-quarter mid-air at the grate, one foot landing, 1girl, solo, golden-honey hair in a shoulder shag with curtain bangs, moss-green eyes ahead of the landing, fair skin, lynx girl, tufted lynx ears, short bobbed tail, human face, slim athletic line, small breasts, softly mounded, mid_gratehop,",
         "the knit top's hem riding the mid-air lift, the skirt-shorts' inner band visible at the stride's width, collarbones catching the drop's angle,",
         weave("Y118"),
         "the tufted ears already turned down toward the garden rows, a brass signal whistle pinned to the collar, one hoop earring catching the drop, the bobbed tail giving the jump its rudder beat, the grate's moss holding last visit's print,",
         "the landing foot's weight arriving through the hip one beat late, the trailing leg still carrying its height,",
         "mid-hop off the grate with one foot landing, the other leg trailing, hair a half-beat late,",
         "the garden level's rows combed by drip-lines, the snail fence's copper running its own circuit, the ceiling's auroria low and green over the beds,",
         pal_line("P167_MOSS_GOLD", "the minute every room gives her"),
     ],
     negx=" ears level, tail long, feet planted",
     face="stylized 2D anime face ahead of the landing, anime eyes (moss-green, on the next row), small nose, small mouth on the inhale, one curtain bang lifted by the drop.",
     )

slot("P14", "mantis-pincatch", "NICHE · R65 Mantis-kin · R · Y339 · P189_PORCELAIN_CRACK",
     channel=None, corridor="—",
     thesis=("«ШВЕЙНАЯ ЛОВУШЕК: ОНА ЛОВИТ СОСКОЛЬЗНУВШУЮ БРЕТЕЛЬ БУЛАВКОЙ — ДВА ПАЛЬЦА ПРИЖИМАЮТ ЕЁ ПЛОСКО К КОЖЕ "
             "НАД СЕРДЦЕМ, ГОЛОВА СКЛОНЕНА, И НАКЛОН ИДЁТ ДАЛЬШЕ, ЧЕМ ОБЕЩАЛА ФИЗИКА. ПЛЕЧО ОТКРЫТО ДО ЛИНИИ РЁБЕР — "
             "ЗАКОЛКА ДЕРЖИТ СМЕНУ. КИНЖАЛЬНЫЕ ПРЕДПЛЕЧЬЯ СЛОЖЕНЫ ПОКОЙНО, КАК ШАЛЬ. ЛОВУШКИ ШЬЮТСЯ ЗДЕСЬ, "
             "И ПРИМЕРКА — НА СЕБЕ»."),
     gag=("Гэг-стек: наклон головы на 180 — соображение с той стороны, откуда не ждут; сложенные предплечья читаются "
          "как шаль — рукава-харнессы; волосы-шрам по ключице посеребрён временем — первая примерка; "
          "глаза берут тройной блик — треугольник проверки."),
     spine="Y339 Safety-Pin Catch (upper body three-quarter, combo→Y339, карта-стенд) · CAM— three-quarter down the tilt · LEAD the held pin · seamstress register · upper body three-quarter",
     race="R65 — богомол: наклон головы идёт дальше, чем позволяет физика — 180 градусов соображения.",
     gar="смена мастерской: сарафан-майка на бретелях (бретель — объект карты) + пояс-харнесс с ножнами булавок · HS: HS30 Curtain Bangs + Collar-Length Blunt",
     stack=["CR-B34", "CR-E60", "CR-H02", "CR-D49"],
     ycard="Y339",
     pos=[
         "Masterpiece, best quality, absurdres, intricate details, upper body three-quarter down the tilt, safety pin pressed flat above the heart, 1girl, solo, sage-green hair in a collar-length blunt cut with curtain bangs, green triangular eyes in triple highlight, porcelain-pale skin, mantis girl, folded raptorial forearms at rest, human face, willowy line, small breasts, high-set, mid_pincatch,",
         "one shoulder strap slipped down the upper arm, the side bare down to where the rib-line runs, a hairline scar along the collarbone silvered with time,",
         weave("Y339"),
         "the pin-cushion bandolier crossing the apron, the folded forearms resting like a shawl at the chest's edge, the workroom's shears sleeping in their loop,",
         "the head's tilt going further than physics suggests, two fingers holding the pin flat and honest,",
         "the strap down the upper arm, the pin pressed flat above the heart, the tilt reading its own work,",
         "the trap-workshop's patterns hanging in ranked paper rows, the dress-form wearing half a caught net, the ceiling's aurora falling seam-pale over the bench,",
         pal_line("P189_PORCELAIN_CRACK", "the mend she wears as craft"),
     ],
     negx=" pin open, strap up, tilt shallow",
     face="stylized 2D anime face tilted past the shoulder's line, anime eyes (green, triple-highlighted), small nose, small mouth deciding the stitch, one bang edge pinned back.",
     )

slot("P15", "incense-laundry-fold", "NICHE · R57 Incense-wisp-kin · R · Y263 · P176_INCENSE_AND_MYRRH",
     channel=None, corridor="—",
     thesis=("«ПАРОПРАЧЕЧНАЯ: ПРЕДПЛЕЧЬЯ СКРЕЩЕНЫ НА ГРУДИ, В НИХ — СЛОЖЕННОЕ БЕЛЬЁ, ЧЕСТНОЕ ПРИКРЫТИЕ, "
             "ПЛЕЧИ РАЗВЁРНУТЫ. ДЫМНОЕ ТЕЛО ЗАБИРАЕТ У ПОДА ТЕПЛО, У ПОЛА — ЗАПАХ. СКЛАД — ЭТО ИНВЕНТАРЬ: "
             "ПОЛОТЕНЦА ЯРУСОВ ЛОЖАТСЯ ПАРАМИ. КОМНАТА ДЫШИТ ЕЁ ЗАПАХОМ, ПОТОМУ ЧТО ЗАПАХ — ЭТО ОНА. "
             "ПОДЗЕМЕЛЬЕ ПАХНЕТ ЧИСТЫМ»."),
     gag=("Гэг-стек: угольное ядро у грудины — единственная печь прачечной; ленты и висящие нити — дым не держит "
          "плоскостей, одежда висит правдой; сложенное бельё держит форму лучше её тела; пар забирает контур — "
          "остаётся запах и работа."),
     spine="Y263 Laundry-Hold Stand (upper body three-quarter, combo→Y263, карта-стенд) · CAM— three-quarter through steam · LEAD the folded shift · laundry register · upper body three-quarter",
     race="R57 — фимиам-дым: завивается в потоки комнаты; комната дышит её запахом.",
     gar="CL-LG-04? — no: ленты и висящие нити (гардероб дыма) + перед с открытой спиной поверх · HS: HS24 Hip-Length Straight Sheet",
     stack=["CR-D28", "CR-L19", "CR-B17", "CR-S16"],
     ycard="Y263",
     pos=[
         "Masterpiece, best quality, absurdres, intricate details, upper body three-quarter through the steam, forearms crossed over the chest, 1girl, solo, lavender-grey hair in a hip-length straight sheet drifting with the current, ember-amber eyes soft over the fold, smoke-grey translucent skin, incense wisp girl, ember core at the sternum, faint human face, soft middle, medium breasts, nape bare under the pinned weight, mid_laundryfold,",
         "the folded cloth held in crossed forearms, honest cover, the shift showing where the apron's weave thins,",
         weave("Y263"),
         "the ember core glowing steady through the linen's layers, a talisman stitched to the apron's hem, prayer-wood hair beads at the braid's end, hanging ribbons taking the steam's slow curl, the folded towels stacked in level-pairs,",
         "the shoulders squared over the fold, the spine's smooth valley reading through the sheer back,",
         "forearms crossed over the chest holding the folded cloth, shoulders squared,",
         "the wash-line's linen walking its long row, the copper press ticking as it cools, the ceiling's aurora dissolving to myrrh-grey in the steam,",
         pal_line("P176_INCENSE_AND_MYRRH", "the scent the dungeon wears"),
     ],
     negx=" core dark, steam gone, cloth dropped",
     face="stylized 2D anime face soft over the fold, anime eyes (ember-amber, low), small nose, small mouth counting pairs, one smoke strand curling past the jaw.",
     )

slot("P16", "liftoperator-shaft-wait", "NICHE · human · R · Y253 · P198_RAIL_STEAM",
     channel=None, corridor="—",
     thesis=("«ШАХТНЫЙ ЛИФТ НА ТО: ОНА СТОИТ В ДВЕРНОМ ПРОЁМЕ КЛЕТИ — ВЕС НА ОДНОЙ НОГЕ, ВТОРОЕ КОЛЕНО МЯГКОЕ, "
             "БЕДРО В КОСЯКЕ, ПЛЕЧО К РЕЙСУ. СКВАЖИНА ДЫШИТ СКВОЗНЯКОМ, ТРОС ГУДИЕТ СВОЙ НИЗКИЙ «ДОМОЙ». "
             "МОЗОЛИ ЛАДОНЕЙ ЧИТАЮТСЯ КАК ТАБЕЛЬ. ПОДЪЁМНИК ПОДЗЕМЕЛЬЯ — ЭТО ТРАМВАЙ, И У НЕГО ЕСТЬ СВОЯ "
             "ВАХТЁРША»."),
     gag=("Гэг-стек: латунный штурвал отполирован её ладонями до зеркала — руль узнаёт руки; мозоли на ладони — "
          "табель смены, честный; сквозняк несёт сверху запах полдня — клеть пахнет небом по расписанию; "
          "носок чулка сполз в голенище — смена длинная."),
     spine="Y253 Doorframe Lean (upper body three-quarter, combo→Y253, карта-стенд) · CAM— three-quarter into the shaft · LEAD the held cage · warden register · upper body three-quarter",
     race="— (human-служба темы: лифтёрша шахтной клети)",
     gar="смена клети: комбинезон с спущенной лямкой + рубаха (запах у пояса) · HS: HS13 Messy Top-Bun",
     stack=["CR-G07", "CR-B52", "CR-S07", "CR-D43"],
     ycard="Y253",
     pos=[
         "Masterpiece, best quality, absurdres, intricate details, upper body three-quarter into the shaft, hip at the doorframe, 1girl, solo, auburn hair in a messy top-knot with escaping strands, copper-brown eyes on the cable's hum, wind-browned skin, work-calluses reading honest across the palm, average sturdy build, medium breasts, soft waist, mid_shaftwait,",
         "the overall's one strap unbuckled, the bib sagging sideways, the shirt's hem knotted above the navel, the lower belly's curve honest above the low waistband,",
         weave("Y253"),
         "the brass wheel polished mirror-bright by her palms, a keyring of cage keys at her hip, a whistle on a chain round her neck, the cage's latch open on its hook, one sock's cuff slouched into the boot's mouth,",
         "the weight on one leg with the other knee soft, the shoulder resting on the frame's steel,",
         "leaning on the doorframe, weight on one leg, hip cocked, one shoulder on the frame,",
         "the shaft's depth breathing its cool column, the cable's grease line catching what light travels down, the ceiling's aurora arriving in the shaft as one thin green ribbon,",
         pal_line("P198_RAIL_STEAM", "the ride she keeps level"),
     ],
     negx=" straps buckled, wheel dull, cage moving",
     face="stylized 2D anime face into the shaft, anime eyes (copper-brown, on the cable), small nose, small mouth humming the cable's note, one strand escaping into the hum.",
     )

slot("P17", "roseglass-mirror-arch", "NICHE · R56 Rose-glass-kin · R · Y54 · P185_SALT_GLASS",
     channel=None, corridor="—",
     thesis=("«ЗЕРКАЛЬНЫЙ ЗАЛ: ОНА СТОИТ НА КОЛЕНЯХ, СТУДЕНЬ ПРОГНУЛАСЬ НАЗАД, ЛАДОНИ НА ПЯТКАХ, ГРУДЬ ВЕДЁТ "
             "ВВЕРХ. КАМЕРА СНИЗУ. ЗАЛ НОСИТ ЕЁ ЦВЕТА — СВЕТОФИЛЬТРЫ ЗА НЕЙ МЕНЯЮТ ЕЁ С ВОЛНОЙ, И КАЖДЫЙ ПРОГИБ "
             "АР-НУВО СТАНОВИТСЯ НОВЫМ ВИТРАЖОМ. ОНА ЗАНИМАЕТ ЦЕЛЫЙ ЗАЛ — ПРОСТО ЛЕГЛА В НЕГО СПИНОЙ»."),
     gag=("Гэг-стек: свинцовые линии-швы ар-нуво по стеклу — витраж носит корсет сам; цвета меняются с тем, что за "
          "спиной, — она занимает комнаты; спроектированный свет ложится розой на пол — витраж-прожектор; "
          "хрупкость обманчива: стекло держит вес, как мост."),
     spine="Y54 Heel-Braced Arch (from below, combo→Y54, карта-стенд) · CAM— from below · LEAD the borrowed hall · window register · upper body from below",
     race="R56 — розовое стекло: цвета меняются от того, что за спиной, — она занимает комнаты.",
     gar="— (стекло и свинцовая линия — витраж сам одежда; хрустальные подвески яруса) · HS: HS46 Top-Knot High Bun, Architectural",
     stack=["CR-F07", "CR-D20", "CR-S24", "CR-B19"],
     ycard="Y54",
     pos=[
         "Masterpiece, best quality, absurdres, intricate details, upper body from below, kneeling upright with the spine arched backward, 1girl, solo, copper-red glass hair in an architectural high top-knot, sea-glass eyes in a clear pane face, stained glass girl, translucent rose-glass body, glass-clear skin at the face pane, lead-line seams in art-nouveau curves, human face in a clear pane, slender glass build, small breasts, softly mounded, mid_mirrorarch,",
         "the glass body's lead-line corset following the arch, chest lifted to the ceiling's current, a pale glow answering under the glass's thin places,",
         weave("Y54"),
         "the hall's colored filters swinging slow behind her, each arch bending her borrowed palette one hue further, crystal pendants ringing the vault,",
         "the hands braced on the heels with the arch's whole weight honest, the chest leading the line upward,",
         "kneeling upright, spine arched back, hands on the heels, the chest lifted,",
         "the mirror hall's panels multiplying her into a rose choir, the floor's mosaic holding its quiet compass, the ceiling's aurora striking through her body as a rose window on the stone,",
         pal_line("P185_SALT_GLASS", "the hall she wears through"),
     ],
     negx=" seams cracked, colors fixed, arch shallow",
     face="stylized 2D anime face in a clear pane to the ceiling, pane eyes (rose-lit sea-glass, full of the current), small nose, small mouth open on the held arch, one lead-line curve framing the jaw.",
     )

slot("P18", "sandgate-waltz-dip", "NICHE · human · R · Y113 · P74_HONEY_STATIC",
     channel=None, corridor="—",
     thesis=("«ПЕСОЧНЫЕ ВРАТА: ДЕНЬ ПЕРЕСЫПАЕТСЯ В НОЧЬ — И СТРУЯ ВЕДЁТ ЕЁ В ДИПЕ. НОГИ СОГНУТЫ, СТУДЕНЬ УШЛА "
             "НАЗАД ЧЕРЕЗ РУКУ, КОТОРОЙ НЕТ; ОДНА РУКА ВЫШЕ ГОЛОВЫ — КАК ПРИНЯТАЯ. ГОЛОВА ОТДАНА ГРАВИТАЦИИ. "
             "СТРАНИЦА ДНЯ ЛЕЖИТ В ВОЛОСАХ. ВАЛЬС СМОТРИТЕЛЕЙ НЕ ТЕРПИТ — ВАЛЬСИРУЮТ С ПОТОКОМ»."),
     gag=("Гэг-стек: золотая пыль дня оседает на плечах — страница в волосах; рычаг пересыпания — её партнёр, "
          "ведёт за пояс; юбка ещё идёт по дуге — ткань догоняет; тонкая татуировка-кольцо на лодыжке — "
          "двенадцатый оборот врат, счёт юбилеев."),
     spine="Y113 Sand-Dip Waltz (upper body three-quarter, combo→Y113, карта-стенд) · CAM— three-quarter into the dip · LEAD the poured day · waltz register · upper body three-quarter",
     race="— (human-служба темы: смотрительница песочных врат)",
     gar="смена врат: юбка-полусолнце + блуза с заправленной полой (пола — страница дня) · HS: HS39 Rag-Rolled Vintage Waves",
     stack=["CR-D17", "CR-E45", "CR-D51", "CR-S18"],
     ycard="Y113",
     pos=[
         "Masterpiece, best quality, absurdres, intricate details, three-quarter into the dip, upper body, spine arched back over the missing arm, 1girl, solo, burgundy hair in vintage rag-rolled waves with a side part, honey-amber eyes given to gravity, warm ivory skin, a thin anklet tattoo circling the left ankle, soft settled frame, medium-soft breasts, mid_sanddip,",
         "the blouse's tucked page half-poured from the waistband, the skirt's arc still traveling the waltz, collarbones leading the dip's line,",
         weave("Y113"),
         "the sand stream pouring its gold thread past her shoulder, the gate's lever arm holding the turn's count, day-dust settling bright in her waves,",
         "the knees bent with the dip's whole weight trusted backward, one arm arched overhead as if received,",
         "held mid-dip by no one, the back arched over the missing arm, the head given to gravity,",
         "the hour-glass gate's chambers filling level by level, the yesterday-sand cooling to amber glass below, the ceiling's aurora turning honey-slow to match the pour,",
         pal_line("P74_HONEY_STATIC", "the day she pours out"),
     ],
     negx=" dip upright, sand stopped, anklet bare",
     face="stylized 2D anime face given to gravity in the dip, anime eyes (honey-amber, half-closed to the pour), small nose, small mouth on the waltz's one-two-three, one wave trailing gold dust.",
     )

slot("P19", "pangolin-threshold-noon", "NICHE · R66 Pangolin-kin · R · Y335 · P154_LIFT_MORNING_GRASS",
     channel=None, corridor="B",
     thesis=("«ПОРОГ ВЫХОДА: ОНА СИДИТ ВЕРХОМ НА ПОРОГЕ ЯРУСА — ПОДЛОКОТНИКИ НА КОСЯКАХ, КОРПУС УШЁЛ В ПОЛДЕНЬ "
             "ЗА ДВЕРЬЮ. ЧЕШУЯ ЛОВИТ СВЕТ РЯДАМИ БЛИКОВ — КАЖДАЯ ПЛАСТИНА СВОЙ СПЕКУЛЯР. ВЕТЕР С ПОВЕРХНОСТИ "
             "НЕСЁТ ТРАВУ. ВЫХОД ЕСТЬ — И НА НЁМ СИДИТ СМОТРИТЕЛЬНИЦА, ПОТОМУ ЧТО ВЫХОД ЯВЛЯЕТСЯ МЕБЕЛЬЮ, "
             "А СИДЯЩИЙ У ВЫХОДА СЧИТАЕТСЯ СТУЛОМ. НИКТО НЕ УЙДЁТ, ПОКА ОНА ЗАГОРЕЛА»."),
     gag=("Гэг-стек: ряды спекуляров по кромке каждой пластины — чешуя считает полдень; ветер прижимает рубаху — "
          "ткань меж пластин дышит; панцирь греется — на сидении ровно до вечера; над бровью — травинка с "
          "поверхности: пропуск, который никто не просил."),
     spine="Y335 Threshold Straddle (upper body three-quarter, combo→Y335, карта-стенд) · CAM— three-quarter from inside · LEAD the borrowed noon · gate register · upper body three-quarter",
     race="R66 — панголин: сворачивается в идеальный шар, когда день кончается; порог — её смена.",
     gar="рубаха навыпуск (ткань ложится меж пластин) + полотняные штаны · HS: HS47 Hat-Flattened Bedhead Waves",
     stack=["CR-E64", "CR-D57", "CR-W26", "CR-S26"],
     ycard="Y335",
     pos=[
         "Masterpiece, best quality, absurdres, intricate details, upper body three-quarter from inside the door, sitting astride the threshold, 1girl, solo, warm-brown hair in hat-flattened bedhead waves, leaf-green eyes narrowed at the noon, tan skin, pangolin girl, artichoke scale-armor plates from the shoulders down, human face, broad frame, wide hips, heavy chest, soft middle, mid_thresholdwatch,",
         "the shirt catching the wind off the noon, the noon finding her bare shoulders at every gust, the fabric billowing against her side between the plates, the hem snapping the door's line,",
         weave("Y335"),
         "each plate edge taking its own thin specular row in the sun, a brooch of hammered brass at the collar, a pouch of surface seeds at the belt, a grass blade caught above one brow, forearms braced on the doorframe,",
         "the weight sunk forward onto the frame's edge, knees wide past the threshold's sill,",
         "sitting astride the threshold, leaning far forward into the noon, forearms on the doorframe,",
         "the noon field running grass to the horizon gate, the surface wind trading smells with the deep, the corridor behind her holding its green aurora like a held breath,",
         pal_line("P154_LIFT_MORNING_GRASS", "the noon she keeps at the door"),
     ],
     negx=" plates dull, wind still, door closed",
     face="stylized 2D anime face squinting into the noon, anime eyes (leaf-green, narrowed bright), small nose, small mouth tasting the wind, one grass blade ticking above the brow.",
     )

slot("P20", "owl-archive-slide", "NICHE · R58 Belfry-owl-kin · R · Y195 · P134_PROJECTION_PLUM",
     channel=None, corridor="B",
     thesis=("«АРХИВ ПОДЗЕМЕЛЬЯ, СМЕНА ДОЧИТАНА: ОНА СПОЛЗАЕТ ПО СТЕНЕ В ПОЛУПРИСЕД — КОЛЕНИ В СТОРОНЫ, ОДНО "
             "ПОДНЯТО, ПРЕДПЛЕЧЬЕ НА НЁМ, ЗАТЫЛОК К КАМНЮ. ДИСКИ-ОПЕРЕНИЯ РАМКОЙ ЛИЦА СТОЯТ ТИХО. СТЕНА ХРАНИТ "
             "ПРОХЛАДНУЮ ПЕЧАТЬ СПИНЫ. ОНА ВОШЛА НЕСЛЫШНО И ВЫЙДЕТ НЕСЛЫШНО — ЛУЧШАЯ СМЕНА АРХИВА ТА, "
             "КОТОРОЙ НЕ БЫЛО»."),
     gag=("Гэг-стек: лицевой диск-оперение рамкой лица — лицо всегда «в кадре», даже с закрытыми глазами; "
          "крылья-руки спят за спиной — тихий вход/выход; глаза держат темноту — её золотой час чужой полдень; "
          "след спины на камне — архив помнит читательниц."),
     spine="Y195 Wall Slide-Down (upper body three-quarter, combo→Y195, карта-стенд) · CAM— three-quarter low · LEAD the read shift · archive register · upper body three-quarter",
     race="R58 — сова башни: не входит в комнату слышимо — тишина её родная громкость.",
     gar="архивный свитер-оверлайзер поверх рубахи, чулки-гольфы · HS: HS05 Long Classic Layers, Center Part",
     stack=["CR-C18", "CR-D54", "CR-E44", "CR-B65"],
     ycard="Y195",
     pos=[
         "Masterpiece, best quality, absurdres, intricate details, upper body three-quarter low at the wall, sliding down to a half-crouch, 1girl, solo, tawny-brown hair in long classic layers with a center part, gold-rim night eyes half-open in the rest, feather-grey fair skin, owl girl, facial disc feathers framing the face, silent wing-arms, human face, tall soft line, medium breasts, mid_archiveslide,",
         "the oversize sweater's collar half-off one shoulder in the slide, the shirt's cuff giving up its button, a soft midriff line where the sweater rides,",
         weave("Y195"),
         "the wall holding the cool print of her back, small round glasses pushed up into the layers, one wing-arm folded behind as a shelf for the slide, the day's last ledger closed on her knees,",
         "the knees apart with one knee raised, the forearm across it, the head back against the stone,",
         "sliding down the wall to a half-crouch, knees apart, one knee raised, forearm across it, head back,",
         "the archive's ladder rails standing their long dark, the catalogue drawers all home, the ceiling's aurora dimmed to reading quiet over the shelves,",
         pal_line("P134_PROJECTION_PLUM", "the shift nobody heard"),
     ],
     negx=" disc ruffled, wings out, eyes shut",
     face="stylized 2D anime face back against the stone, anime eyes (gold-rim night, half-open), small nose, small mouth on the exhale, disc feathers framing the whole face quiet.",
     )

slot("P21", "snowleopard-cold-count", "NICHE · R54 Snow-leopard-kin · R · Y355 · P173_SNOW_TIGER_MARK",
     channel=None, corridor="B",
     thesis=("«ХОЛОД-СКЛАД: ОНА ВЕРХОМ НА ПРИЛАВКЕ МОРОЗИЛЬНОЙ ЛИНИИ — КОРПУС УШЁЛ ВПЕРЁД НА ПРЕДПЛЕЧЬЯХ, "
             "ПОЛОСАТЫЙ ХВОСТ СВИСАЕТ В КАДР СНИЗУ. РОСЕТКИ-ВЕСНУШКИ УДВАИВАЮТСЯ В МОРОЗНОМ СВЕТЕ. ИНВЕНТАРЬ "
             "СЧИТАЕТСЯ ГЛАЗАМИ — ДЫХАНИЕ СЧИТАЕТСЯ ПАРом. ХОЛОД — ЕЁ СОБСТВЕННОСТЬ, И ИНВЕНТАРЬ В НЁМ "
             "ЛЮБИТ СВОЮ ХОЗЯЙКУ»."),
     gag=("Гэг-стек: кончик хвоста отбивает терпение — метроном морозильной; роскопятна на голых плечах — её "
          "собственный принт, снег удваивает; пар дыхания ложится строкой инвентаря; пояс на бёдрах вывернут "
          "наизнанку — одевались в спешке холода."),
     spine="Y355 Counter Straddle (from below, combo→Y355, карта-стенд) · CAM— low from the cold aisle · LEAD the counted cold · larder register · upper body from below",
     race="R54 — снежный барс: кончик хвоста отбивает терпение в метели — холод её собственность.",
     gar="CL-SK-06? no: байковый топ + шерстяная юбка с поясом на бёдрах (пояс вывернут) · HS: HS10 Single Thick Braid, Over Shoulder",
     stack=["CR-C17", "CR-B13", "CR-E11", "CR-D62"],
     ycard="Y355",
     pos=[
         "Masterpiece, best quality, absurdres, intricate details, from below at the cold aisle, upper body, straddling the freezer counter's edge, 1girl, solo, snow-white hair in a single thick braid over one shoulder, glacier-blue eyes on the count, pale cold-flushed skin, snow leopard girl, spotted ears and tail, pale rosette freckles, human face, sturdy soft build, medium breasts, thick thighs, mid_coldcount,",
         "the flannel top's hem riding the lean forward, the wool skirt's waistband rolled double under the curve of her hips, midriff's line cold-flushed honest,",
         weave("Y355"),
         "the striped tail hanging down into the frame below, its tip ticking the count, frost-set silver earrings at the spotted ears, rosette freckles doubled in the freezer's light, breath leaving in one held line of steam,",
         "the weight sunk onto the counter's front edge through the forearms, the braid slipping off the shoulder,",
         "straddling the counter edge, leaning far forward on the forearms, the tail hanging into the frame,",
         "the freezer aisle's racks breathing their cold columns, the tally slate's chalk line growing one stroke at a time, the ceiling's aurora gone ice-white over the stock,",
         pal_line("P173_SNOW_TIGER_MARK", "the cold she keeps inventory in"),
     ],
     negx=" tail still, freckles absent, slate blank",
     face="stylized 2D anime face over the count, anime eyes (glacier-blue, on the tally), small nose pink at the tip, small mouth mid-number, the braid's tail crossing the collarbone.",
     )

slot("P22", "registrar-ledger-stride", "NICHE · human · R · Y74 · P149_SCALE_ROOM",
     channel=None, corridor="B",
     thesis=("«КОНТОРА ГИЛЬДИИ: ОНА СИДИТ ВЕРХОМ НА СТУЛЕ ЗАДОМ НАПЕРЁД — КОЛЕНИ ШИРОКО ПО СТОРОНАМ СПИНКИ, "
             "ВЕС ОСЕЛ НА ПЕРЕДНЮЮ КРОМКУ. ГРОССБУХ ЗАХОДОВ ОТКРЫТ: ВОЛНА №9 ПОШЛА ВНИЗ, СЧЁТЧИК СМЕН "
             "ЩЁЛКНУЛ. ПОДГЛАЗНЫЕ ЛИНИИ ЧЕСТНЫЕ — НОЧНАЯ СМЕНА. ВЕСЫ ГИЛЬДИИ У СЕРДЦА — ОНА ВЗВЕШИВАЕТ, "
             "СКОЛЬКО ЕЩЁ ДЫШИТ»."),
     gag=("Гэг-стек: тёмные круги под глазами — честная усталость ночного реестра; латунный рельс стола целует "
          "юбку холодом — контора держит порядок; колокольчик гильдии гудит на пол-ноты от каждого щелчка "
          "счётчика; перо за ухом — запасное, чернила яруса."),
     spine="Y74 Chairback Straddle (upper body three-quarter, combo→Y74, карта-стенд) · CAM— three-quarter over the ledger · LEAD the kept count · guild register · upper body three-quarter",
     race="— (human-служба темы: регистраторша гильдии заходов)",
     gar="CL-BT-02? no: юбка-карандаш + блуза с закатанными рукавами (смена) · HS: HS01 Blunt Chin Bob",
     stack=["CR-C13", "CR-M21", "CR-E33", "CR-D55"],
     ycard="Y74",
     pos=[
         "Masterpiece, best quality, absurdres, intricate details, upper body three-quarter over the ledger, astride the chair backward, 1girl, solo, dark-chocolate hair in a blunt chin bob, ink-grey eyes on the tally, ledger-warm fair skin, dark under-eye lines honest tiredness, average neat build, medium breasts, mid_ledgerstride,",
         "the pencil skirt's taut front over the thighs' press at the straddle, the blouse's sleeves rolled working-high, the collarbones reading the ledger's light,",
         weave("Y74"),
         "the guild ledger open to the ninth wave's line, a keyring of wave-stamps at the ledger's edge, a brooch of the guild's brass on the collar, a brass tally counter under one thumb, the chair's back holding her forearms' weight,",
         "the knees wide past the chairback's sides, the weight riding the seat's front edge,",
         "astride the chair with knees wide, weight sinking forward onto the edge,",
         "the guildhall's scales hanging quiet at their zero, the pigeonholes of past waves full and sleeping, the ceiling's aurora kept to one clerkish thread overhead,",
         pal_line("P149_SCALE_ROOM", "the count she keeps for the deep"),
     ],
     negx=" chair turned, ledger shut, sleeves down",
     face="stylized 2D anime face over the ledger, anime eyes (ink-grey, on the ninth line), small nose, small mouth on the count, one bob-edge tucked behind the ear.",
     )

slot("P23", "synoptic-skylie", "NICHE · human · PG-13 · Y65 · P56_AURORA_BOREALIS_NIGHT",
     channel=None, corridor="—",
     thesis=("«БАЛКОН НАБЛЮДЕНИЯ ЗА СИЯНИЕМ: ОНА ЛЕЖИТ НА СПИНЕ, ОБЕ НОГИ ПОДНЯТЫ И СКРЕЩЕНЫ В ЛОДЫЖКАХ НАД "
             "БЁДРАМИ. НЕБО-ПОТОЛОК ВЕДЁТ ПРОГНОЗ: ЗЕЛЁНАЯ ПОЛОСА ИДЁТ ВОЛНОЙ НА СЕВЕРНЫЙ ЯРУС. ОНА ЧИТАЕТ "
             "СИЯНИЕ КАК ДРУГИЕ ЧИТАЮТ ГАЗЕТЫ — ЛОДЫЖКАМИ. ВЕТЕР ПЕРЕСЧИТЫВАЕТ ШТОРМЫ. ПРОГНОЗ НА ЗАВТРА: "
             "ПЕРЕМЕННАЯ ЯСНОСТЬ С ПРОСВЕТЛЕНИЯМИ В ГЛУБИНЕ»."),
     gag=("Гэг-стек: бумажный прогноз под пяткой — завтрашняя сводка сохнет; ветер сдувает секцию кудрей — "
          "анемометр из волос; щиколоточное кольцо блестит — единственная монета синоптика; балконная "
          "решётка держит локти — наблюдение лежачее, зато честное."),
     spine="Y65 Sky-Lie Legs-Up (upper body three-quarter, combo→Y65, карта-стенд) · CAM— three-quarter from the rail · LEAD the read sky · forecast register · upper body three-quarter",
     race="— (human-служба темы: синоптик сияния подземелья)",
     gar="трикотажный костюм наблюдателя (свободные брюки + топ) + шарф · HS: HS55 Wind-Lifted Open Curtain",
     stack=["CR-H14", "CR-S17", "CR-D41", "CR-B36"],
     ycard="Y65",
     pos=[
         "Masterpiece, best quality, absurdres, intricate details, upper body three-quarter from the rail, lying on her back, both legs raised, 1girl, solo, teal hair in a long wind-lifted curtain, sky-grey eyes reading the ceiling, fair cool skin, an anklet chain across the ankle bone, soft slight build, small breasts, mid_skylie,",
         "the loose pants' fabric pooling at the raised knees, the top's hem honest at the waistband, the scarf half-unwound,",
         weave("Y65"),
         "the paper forecast pinned under one heel to dry, the balcony rail holding the whole quiet frame, the cold ring of the rail printing the flat palm,",
         "the hips carrying the raised legs' weight, the ankles crossed easy above,",
         "lying on her back with both legs raised and crossed at the ankle above the hips,",
         "the aurora's green band making its slow northward pass, the forecast flags hanging their calm, the whole ceiling breathing one long tide of light,",
         pal_line("P56_AURORA_BOREALIS_NIGHT", "the sky she reads ankles-first"),
     ],
     negx=" legs down, paper gone, aurora flat",
     face="stylized 2D anime face up to the ceiling, anime eyes (sky-grey, reading the band), small nose, small mouth on tomorrow's line, one teal strand crossing the whole face on the wind.",
     )

slot("P24", "keykeeper-font-watch", "NICHE · human · PG-13 · Y277 · P163_VERDIGRIS_PATINA",
     channel=None, corridor="B",
     thesis=("«РЕСПАУН-СВЯТИЛИЩЕ: ОНА ПРИСЕЛА НАД КУПЕЛЬЮ — ЛОКТИ НА КОЛЕНЯХ, ПОДБОРОДОК В ЛАДОНЯХ, ВЗГЛЯД "
             "ВНИЗ МЕЖДУ КОЛЕН: В ВОДЕ ЕЩЁ НИКОГО. КЛЮЧ СВЯТИЛИЩА — НА ПОЯСЕ, СВЕЖЕ ПОЙМАННЫЙ НА ВЕРЁВКУ. "
             "К ЗАВТРАМУ КТО-ТО ВОЗРОДИТСЯ — И ОНА ПРОВЕРЯЕТ, ЧТОБЫ ЧАША БЫЛА ЧИСТОЙ. РОДИНКА ПОД ПРАВЫМ "
             "ГЛАЗОМ — НА ВЕС ЗОЛОТА: ПО МОЙКЕ ВИДНО, КТО ПРОСНЁТСЯ ДОБРЫМ»."),
     gag=("Гэг-стек: ключ на пеньковой верёвке — пойман утром, ещё пахнет песком; чулок сполз в голенище — смена "
          "у воды длинная; соляной ореол вокруг купели — прошлая волна высохла кругом; родинка под правым "
          "глазом — метка вахты"),
     spine="Y277 Font-Watch Crouch (upper body three-quarter, combo→Y277, карта-стенд) · CAM— three-quarter down into the font · LEAD the kept water · vigil register · upper body three-quarter",
     race="— (human-служба темы: ключница респаун-святилища)",
     gar="перед поверх рубахи, чулки-гольфы (один сполз), ключ на верёвке · HS: HS12 Low Braided Chignon",
     stack=["CR-F15", "CR-I21", "CR-E23", "CR-B18"],
     ycard="Y277",
     pos=[
         "Masterpiece, best quality, absurdres, intricate details, upper body three-quarter down into the font, crouching at the basin's rim, 1girl, solo, rose-blonde hair in a low braided chignon, moss-soft green eyes on the water, warm ivory skin, a beauty mark under the right eye, small-boned neat build, medium breasts, mid_fontwatch,",
         "the apron's cross-straps leaving the back bare at the crouch, one knee-sock gathered at the ankle, the key's rope riding the waistband,",
         weave("Y277"),
         "the basin's patina water holding one still reflection, a sanctum key on its hemp rope at the hip, a small brass keyring at the rope's knot, salt drying in a halo where the last wave knelt,",
         "the elbows on the knees with the chin in both palms, the small of the back's scoop above the waistband,",
         "crouching with elbows on knees, chin in hands, looking down between the knees at the water,",
         "the sanctum's niches long cold and holding moss instead, the respawn bell sleeping on its hook, the ceiling's aurora green and patient as a night nurse,",
         pal_line("P163_VERDIGRIS_PATINA", "the morning she keeps ready"),
     ],
     negx=" standing, key gone, water stirred",
     face="stylized 2D anime face down into the water, anime eyes (moss-green, on the still reflection), small nose, small mouth on the vigil's count, the beauty mark under the right eye steady.",
     )

# ══════════════════ EXP P25–P33: 9 кандидатов в ОС · комбо у потолка R+ · волна 13 ══════════════════

slot("P25", "gargoyle-ledge-clockout", "EXP · R18 Gargoyle-kin · R+ · Y12 · P262_MOSS_LINE",
     channel=None, corridor="A",
     thesis=("«ГАРГУЛЬЯ КОНЧАЕТ СМЕНУ: ВЕК СТОЯНИЯ КАМНЕМ ЗАКРЫТ — КУРТКА СПОЛЗЛА С ОДНОГО ПЛЕЧА, РУКАВ ПОЙМАН "
             "СГИБОМ ЛОКТЯ. КАМЕННЫЕ ПЯТНА НЕ ДЕРЖАТ КРАСКУ — ТКАНЬ ВИСИТ С МЯГКИХ ЗОН, И ВЕЧЕР ПОЛЬЗУЕТСЯ. "
             "КАРНИЗ ПОД НЕЙ ПОЛОН МОХА. ГРАНИТ МАТОВЫЙ — НО ПОД УГЛОМ РАССВЕТА В НЁМ ОДНА КРИСТАЛЛЬНАЯ "
             "ИСКРА. АРХИТЕКТУРА ТОЖЕ РАЗМИНАЕТСЯ — ПРОСТО ОДИН РАЗ В СТОЛЕТИЕ»."),
     gag=("Гэг-стек (канон-ран ≥3): 1) каменные пятна кожи не держат краску — ткань висит с мягких зон; "
          "2) малые каменные крылья за спиной — складываются как флюгер; 3) мох на карнизе растёт по линии "
          "её многовекового караула — биография зелёным; 4) кристалльная искра гранита под углом рассвета — "
          "зарплата архитектуры."),
     test=("ТЕСТ (⚗ потолок R+): комбо CL-DR-07 + CL-SK-09 (jersey wrap dress PROCESS + suspender skirt) + карта "
           "Y12 (PROCESS, коридор A) — процесс куртки на сгибе локтя держит R+ у потолка без X-шага. "
           "Проверка: куртка с одного плеча, рукав на локте, бретель сарафана на весу"),
     spine="Y12 Jacket-Slide Ledge (eye-level close, combo→Y12, карта-стенд) · CAM— eye level close at the ledge · LEAD the clocked-out stone · architecture register · upper body close",
     race="R18 — гаргулья: тиха как архитектура — до единственного момента, когда нет.",
     gar="CL-DR-07 (jersey wrap dress, deep V, wrap-knot riding loose) + CL-SK-09 (suspender skirt, straps over bare shoulders) + CL-AC-05 (fingerless knit gloves) + рабочая куртка навыпуск (объект карты — сползает с плеча) · HS: HS25 Choppy Mullet, Shag-Tail",
     stack=["CR-W35", "CR-E51", "CR-B64", "CR-B55"],
     ycard="Y12",
     pos=[
         "Masterpiece, best quality, absurdres, intricate details, upper body close, eye-level at the ledge, jacket sliding off one shoulder, 1girl, solo, moss-grey hair in a choppy mullet with a shag-tail, weathered amber eyes on the horizon gate, stone-pale skin with granite patches, gargoyle girl, stone-skinned patches, small stone wings, human face, broad soft build, large breasts, soft belly, mid_ledgeclockout,",
         "the wrap dress's deep V reading her chest line where the knot rides loose, the jacket's weight gone off one shoulder, nothing underneath the slide but the century she clocked out — the clocked-out stone is the claim, architecture-made,",
         weave("Y12"),
         "the suspender skirt's straps riding over bare shoulders, earrings of carved granite at the stone ears, fingerless knit gloves at the stone hands, small stone wings folding like a weathervane at rest, moss lining the ledge below in one green biography,",
         "the jacket holding its half-shrug by its own weight, the sleeve caught at the elbow's fold, the wrap-knot's slack honest at the ribs,",
         "the jacket off one shoulder with the sleeve caught at the elbow fold,",
         "the ledge's gutter running its century of rain-lines, the facade's gargoyles still on shift and silent about it, the ceiling's aurora laying its first green on the one who moved,",
         pal_line("P262_MOSS_LINE", "the shift she ends standing"),
     ],
     negx=" wings spread, jacket up, stone cracked",
     face="stylized 2D anime face to the horizon gate, anime eyes (weathered amber, patient), small nose, small mouth on the exhale, one shag-tail flicked by the updraft.",
     )

slot("P26", "ghost-palmheld-exhibit", "EXP · R33 Ghost-kin · R+ · Y484 · P261_AURORA_VEIN",
     channel=None, corridor="A",
     thesis=("«ПРИЗРАК НА ЭКСПОНАТЕ: РУКИ РАЗВЕДЕНЫ В СТОРОНЫ ПАРИЩИМИ ЛАДОНЯМИ ПОДЗЕМЕЛЬЯ — ОНО ДЕРЖИТ ЕЁ "
             "ЗА ЗАПЯСТЬЯ, ЧТОБЫ НЕ РАСТАЯЛА. КОЛЕНО СОГНУТО, ПОДБОРОДОК ВВЕРХ, СПОКОЙСТВО ЭКСПОНАТА. "
             "ЛЬНЯНАЯ РУБАХА РАСПАХНУТА — СКЛАДКИ РАССЕИВАЮТ СВЕТ, КАК ОНА САМА. КОЛОКОЛЬЧИК НА ОШЕЙНИКЕ "
             "НЕ ЗВЕНИТ: ОНА ВСЁ ЕЩЁ НЕ ВЕСИТ. ЕДИНСТВЕННОЕ ПРИКОСНОВЕНИЕ, КОТОРОЕ ЕЁ РЕГИСТРИРУЕТ — "
             "ЭТО ПОДЗЕМЕЛЬЕ, И ОНО ЛЮБИТ СВОИХ»."),
     gag=("Гэг-стек (канон-ран ≥3): 1) вещи, на которые она опирается, не чувствуют веса — она опирается на "
          "ничего; 2) одежда опаздывает на такт — лён дышит следом; 3) колокольчик на ошейнике нем для "
          "всех шагов — кроме её смеха; 4) тени внутри неё мельче чужих — она своё собственное рассеяние."),
     test=("ТЕСТ (⚗ потолок R+): комбо CL-TS-09 + CL-AC-06 (open linen shirt PROCESS + bell collar) + карта "
           "Y484 (COVER, коридор A, парящие ладони держат грудь) — прикрытие только руками-фондом и распахом; "
           "R+ у потолка. Проверка: ладони под запястьями, рубаха распахнута, колокольчик молчит"),
     spine="Y484 Conjured-Palm Exhibit (upper body three-quarter, combo→Y484, карта-стенд) · CAM— three-quarter centered · LEAD the held ghost · exhibit register · upper body three-quarter",
     race="R33 — призрак: вещи, на которые она опирается, не чувствуют её веса.",
     gar="CL-TS-09 (loose linen shirt worn open, creased folds diffusing light) + CL-AC-06 (bell collar, silent for her) · HS: HS61 Loose Sleeping Braid",
     stack=["CR-D40", "CR-W57", "CR-S20", "CR-B24"],
     ycard="Y484",
     pos=[
         "Masterpiece, best quality, absurdres, intricate details, upper body three-quarter centered, arms held away by conjured palms, 1girl, solo, lilac-white hair in a loose half-worked sleeping braid, moonstone-pale eyes half-open in the stillness, smoke-translucent skin, ghost girl, translucent edges, floating hair, human face, very slender build, flat chest, sharp collarbones, mid_palmheld,",
         "the open linen shirt's front held only by the floating palms' span, the conjured palms covering the chest line at her sides, the fabric's weave worn to gauze at the panel, nothing underneath the exhibit but the dungeon's own holding — the held ghost is the claim, exhibit-made,",
         weave("Y484"),
         "conjured palms cupping both wrists a hand-span from her sides, a pendant of still-warm silver at her throat, a hairpin through the braid, a small gold bell collar silent below it,",
         "the shirt's creased folds diffusing what light passes through her, the bell's clapper resting against sound,",
         "standing centered with the arms held away by floating palms, chin up, one knee bent,",
         "the exhibit alcove's plinth empty beneath her hovering heels, the corridor's moss growing in a ring where nobody walks, the ceiling's aurora bending one full vein down to hold her,",
         pal_line("P261_AURORA_VEIN", "the light that chooses to hold"),
     ],
     negx=" palms gone, shirt closed, bell ringing",
     face="stylized 2D anime face chin-up in the stillness, anime eyes (moon-milk, half-open), small nose, small mouth at rest, the braid's loose half drifting a beat late.",
     )

slot("P27", "dullahan-glove-peel", "EXP · R43 Dullahan-kin · R+ · Y27 · P263_OSSUARY_CHALK",
     channel=None, corridor="A",
     thesis=("«ДУЛЛАХАН ПЕРЕОДЕВАЕТСЯ МЕЖДУ КОМНАТАМИ: ГОЛОВА УЖЕ В СЛЕДУЮЩЕМ ПОМЕЩЕНИИ, ТЕЛО — В ГРИМЁРНОЙ. "
             "ОНА СНИМАЕТ ПЕРЧАТКУ ПАЛЕЦ ЗА ПАЛЬЦЕМ НА СГИБЕ ЗАПЯСТЬЯ — МАНЖЕТА ЕЩЁ ДЕРЖИТ ЛАДОНЬ. "
             "СВЕТЛЫЕ ШРАМ-ЛИНИИ НА ШЕЕ СВЕТЯТСЯ СЛАБЫМ ФИОЛЕТОМ В СУМЕРКАХ. ОДИН ГЛАЗ ЗОЛОТОЙ, ВТОРОЙ "
             "ГРОЗОВОЙ: ГОЛОВА ВИДИТ НАПЕРЁД, ТЕЛО ПОМНИТ. ГЕТЕРОХРОМИЯ ДУЛЛАХАНА — ЭТО ДВА МНЕНИЯ "
             "ОБ ОДНОЙ ЖИЗНИ»."),
     gag=("Гэг-стек (канон-ран ≥3): 1) шрам-линия шеи светится фиолетовым в сумерках — шов между кабинетами; "
          "2) гетерохромия: золото против грозовой сини — голова и тело голосуют; 3) шарф-палантин снят "
          "на переодевание — шрам работает поводом; 4) перчатка снимается с той руки, что держала голову."),
     test=("ТЕСТ (⚗ потолок R+, oc_hook MK-E01): комбо CL-SK-02 + CL-FX-05 + CL-AC-09 (сатин-юбка + thigh-boots + "
           "помочи на весу) + карта Y27 (PROCESS, коридор A) — процесс перчатки на голое запястье у потолка. "
           "Проверка: перчатка палец за пальцем, манжета держит, шрам-линия светится"),
     spine="Y27 Glove-Peel Dressing (close insert, combo→Y27, карта-стенд) · CAM— close insert at eye level · LEAD the redressed seam · undertaker register · upper body close",
     race="R43 — дуллахан: голову ставит на полку ради лучшего угла на книгу; переодевается по частям.",
     gar="CL-SK-02 (flowing satin skirt, waves of light in the folds) + CL-FX-05 (thigh-high heel boots drinking the light) + CL-AC-09 (loose suspenders swinging) + длинная перчатка (объект карты — снимается) + шарф-палантин на плечах · HS: HS42 Two Dutch Braids Pinned Into a Crown",
     stack=["CR-E24", "CR-E62", "CR-H13", "CR-E47"],
     ycard="Y27",
     pos=[
         "Masterpiece, best quality, absurdres, intricate details, close insert at eye level, upper body, glove peeled off finger by finger, 1girl, solo, ink-blue-black hair in two dutch braids pinned into a crown, heterochromia one eye gold the other storm-blue, porcelain-pale skin, dullahan girl, head-seam line at the neck, human face, flat chest, wide hips, soft middle, mid_glovepeel,",
         "the long glove coming off finger by finger at the wrist's bend, the cuff still holding the palm, the suspenders' straps covering the chest's bare line between them, nothing underneath the redress but the next room — the redressed seam is the claim, undertaker-made,",
         weave("Y27"),
         "the head-seam line glowing faint violet in the dressing-room dusk, a palantine scarf slipped to one shoulder, satin folds carrying waves of light to the boot line,",
         "the peeled glove held between two fingers at the finish, the cuff's grip honest at the palm's heel,",
         "the glove off finger by finger at the wrist's bend, the cuff still holding,",
         "the dressing room's two doors — one to yesterday's hall, one to tomorrow's — both ajar, the mirror showing the crown of braids where a head will be, the ceiling's aurora keeping chalk-pale hours,",
         pal_line("P263_OSSUARY_CHALK", "the life she keeps in two opinions"),
     ],
     negx=" seam dark, glove on, eyes matched",
     face="stylized 2D anime face half to the mirror, anime eyes (one gold one storm-blue, two opinions), small nose, small mouth on the count of fingers, the seam's violet line under the jaw.",
     )

slot("P28", "golem-notereach", "EXP · R32 Golem-kin · R+ · Y16 · P267_ARCHIVE_BRASS",
     channel=None, corridor="A",
     thesis=("«ГОЛЕМ-АРХИВАРИУС: РУКА ПОДНЯТА К ВЕРХНЕЙ ПОЛКЕ — ПОДОЛ РУБАХИ ПОДТЯНУЛ ПОДНЯТОЙ РУКОЙ, ТКАНЬ "
             "МОСТОМ ПО РЁБРАМ ДЕРЖИТ ЛИНИЮ. НА ПРЕДПЛЕЧЬЕ СВЕЖЕ ВЫБИТА ЗАПИСЬ — СЕГОДНЯШНИЙ УЧЁТ. ГЛИНЯНЫЕ "
             "ПЛАСТИНЫ НЕ ДЕРЖАТ ТКАНЬ, РУНЫ СВЕТЯТСЯ ЛЕНИВО В ПОЛУСВЕТЕ. ПАМЯТЬ ПОДЗЕМЕЛЬЯ НОСИТСЯ НА РУКЕ, "
             "И РУКА ТЯНЕТСЯ ЗА СЛЕДУЮЩЕЙ СТРАНИЦЕЙ»."),
     gag=("Гэг-стек (канон-ран ≥3): 1) выбитые на предплечье записи — дневник, который нельзя потерять; "
          "2) руны на суставах держат ленивый свет в полумраке; 3) глиняные пластины игнорируют ткань — "
          "рубаха живёт на мягких стыках; 4) обхват-платье с V держит архивный дресс-код."),
     test=("ТЕСТ (⚗ потолок R+): комбо CL-TS-07 + CL-DR-07 (off-shoulder top + jersey wrap dress, оба PROCESS/COVER) "
           "+ карта Y16 (COVER, коридор A) — подол под поднятой рукой держит мост по рёбрам у потолка. "
           "Проверка: рука к полке, подол подтянут, мост по рёбрам, руны светятся"),
     spine="Y16 Hem-Tuck Reach (upper body three-quarter, combo→Y16, карта-стенд) · CAM— three-quarter up the reach · LEAD the worn memory · archive register · upper body three-quarter",
     race="R32 — голем: помнит всё — буквально, записи выбиты на предплечье.",
     gar="CL-TS-07 (off-shoulder top, neckline a soft horizon) + CL-DR-07 (jersey wrap dress, deep V, knot riding loose) · HS: HS16 Hair-Sticks + Pinned Twist",
     stack=["CR-A18", "CR-W36", "CR-D46", "CR-B22"],
     ycard="Y16",
     pos=[
         "Masterpiece, best quality, absurdres, intricate details, upper body three-quarter up the reach, arm raised to the top shelf, 1girl, solo, terracotta hair in a pinned twist with wooden hair sticks, kiln-orange eyes on the ledger line, clay-warm skin plates, golem girl, rune-carved stone joints, human face, large breasts, slender waist, mid_notereach,",
         "the wrap dress's hem tucked by the raised arm, the fabric bridge across the ribs holding the line, nothing underneath the reach but the record — the worn memory is the claim, archive-made,",
         weave("Y16"),
         "fresh-carved notes riding the forearm's plate, a bracelet of clay beads at the wrist, runes holding a lazy amber glow at the joints, the off-shoulder top's neckline a soft horizon across the upper arms,",
         "the raised arm's weight honest into the shelf, the bridge's line taut across the ribs, the knot's slack paid out,",
         "the hem tucked by the raised arm, the fabric bridging the ribs, the line held,",
         "the archive's top shelf running its brass rail into the dark, the day's folios waiting palm-up, the ceiling's aurora low and scholarly over the stacks,",
         pal_line("P267_ARCHIVE_BRASS", "the memory she wears carved"),
     ],
     negx=" runes dark, arm down, hem loose",
     face="stylized 2D anime face up the reach, anime eyes (kiln-orange, on the ledger line), small nose, small mouth on the next folio, one hair-stick catching the shelf's brass.",
     )

slot("P29", "arachne-knitgrip", "EXP · R35 Arachne-kin · R+ · Y18 · P265_THREAD_HOARD_SILK",
     channel=None, corridor="A",
     thesis=("«АРАХНА В УГЛУ ДЛЯ ВЯЗАНИЯ: ОДНА ИЗ ЧЕТЫРЁХ РУК СТЯГИВАЕТ ПЕРЧАТКУ ПРЯМО В ХВАТЕ — ВРАГ-ЗАЩИТНИК "
             "НАЗАПЯСТЬЕ ПОДНИМАЕТ ЛИНИЮ ПОДОЛА. СПИЦЫ НЕ ОСТАНАВЛИВАЮТСЯ: ДВЕ РУКИ ВЯЖУТ, ТРЕТЬЯ СНЯЛА "
             "ПЕРЧАТКУ, ЧЕТВЁРТАЯ ДЕРЖИТ ЧАЙ. ПОДАРОК ГОТОВ К УТРУ — ОН ВСЕГДА ТЁПЛЫЙ. ХИТИН БЕРЁТ "
             "СИНИЙ СПЕКУЛЯР, ШЁЛК КИМОНО ДЫШИТ ПОВЕРХ. У ПОТОЛКА R+ ЖИВЁТ СЕМЬ РУК И НИ ОДНОЙ СВОБОДНОЙ»."),
     gag=("Гэг-стек (канон-ран ≥3): 1) хитиновые добавочные руки из лопаток — берут синий чёрный спекуляр; "
          "2) закрытые паучьи глазки на висках — считают петли, не отвлекаясь; 3) чай остывает ровно на "
          "одну петлю — точный термометр; 4) напёрсток-браслет на верхней руке — ювелирка пряхи."),
     test=("ТЕСТ (⚗ потолок R+): комбо CL-LG-04 + CL-UR-04 + CL-TS-04 + CL-AC-04 (открытое шёлковое кимоно поверх "
           "майки и хлопка — LINGERIE-регистр) + карта Y18 (PROCESS, коридор A) — перчатка в хвате и подъём "
           "подола враг-защитником: R+ у потолка без X-шага. Проверка: перчатка в захвате, подол поднят, "
           "спицы идут, кимоно открыто"),
     spine="Y18 Glove-Peel Mid-Grip (close insert at eye level, combo→Y18, карта-стенд) · CAM— close insert at eye level · LEAD the warm gift · hearth register · upper body close",
     race="R35 — арахна: запасные руки вяжут, пока основные заняты — подарок всегда тёплый.",
     gar="CL-LG-04 (silk kimono open, obi loose) + CL-TS-04 (thin ribbed tank top) + CL-UR-04 (simple cotton panties) + CL-AC-04 (lace elbow gloves on the upper pair) · HS: HS37 Bubble Ponytail, Sectioned",
     stack=["CR-E53", "CR-L23", "CR-B57", "CR-D38"],
     ycard="Y18",
     pos=[
         "Masterpiece, best quality, absurdres, intricate details, upper body close, eye-level insert on the grip, glove peel mid-grip, 1girl, solo, dark-plum hair in a sectioned bubble ponytail, violet eyes on the stitch count, warm ivory skin, arachne, extra chitin arms from the shoulder blades, small closed spider eyes at the temples, human face, tall slender build, small breasts, mid_knitgrip,",
         "the kimono open over the tank's honest seams, the wrist-guard's edge raising the hem line mid-grip, nothing underneath the hearth register but the gift — the warm gift is the claim, hearth-made,",
         weave("Y18"),
         "lace elbow gloves on the upper pair of arms, the lower pair's knit clicking its row, a thimble-bracelet riding the third wrist, the tea steaming one stitch from cool,",
         "the peel's grip honest mid-stitch, chitin taking its blue-black specular at the turn, the obi's loose ends pooling,",
         "the glove peeled mid-grip with the wrist-guard raising the hem line,",
         "the knitting corner's basket of yarns ranked by warmth, the half-made gift already wearing its own folds, the ceiling's aurora kept to ember-quiet over the wool,",
         pal_line("P265_THREAD_HOARD_SILK", "the gift that stays warm"),
     ],
     negx=" arms two, knit dropped, tea cold",
     face="stylized 2D anime face to the stitch count, anime eyes (mulberry, on the row), small nose, small mouth counting, one bubble-section ticking with the click.",
     )

slot("P30", "slime-toweldry", "EXP · R25 Slime-girl · R+ · Y22 · P266_FLOODED_VERDIGRIS",
     channel=None, corridor="A",
     thesis=("«СЛИЗЬ ЗАКРЫВАЕТ СМЕНУ ЗАТОПЛЕННОГО ЯРУСА: ГЕНУБОРКА ОКОНЧЕНА — ПОЛОТЕНЦЕ ПОЙМАНО НА ПОЛ-ВЫТИРАНИЯ "
             "У ЛИНИИ ПЛЕЧ, МОКРЫЕ ВОЛОСЫ СЧИТАЮТ КАПЛИ ПО ХРЕБТУ. РАШГАРД РАСТЁГНУТ НАПОЛОВИНУ — МОЛНИЯ "
             "ЗАМЕРЛА НА СПУСКЕ. ЗОЛОТАЯ ЦЕПЬ ПЛАВАЕТ В ГЕЛЕ НА САНТИМЕТР ВГЛУБЬ — ВЕЩИ, КОТОРЫЕ ОНА "
             "ДЕРЖИТ, ВОЗВРАЩАЮТСЯ ЧИЩЕ. ГРЯЗЬ ЯРУСА РАСТВОРЕНА, ХОЗЯЙКА — НЕТ»."),
     gag=("Гэг-стек (канон-ран ≥3): 1) взвешенное ядро в геле — сердце-желе, светится на такт; 2) вещи на "
          "сантиметр в неё — возвращаются чище, чем были; 3) водная линия на бёдрах режет мокрое пополам; "
          "4) капли идут по позвоночнику счётом — метроном яруса."),
     test=("ТЕСТ (⚗ потолок R+): комбо CL-SM-06 + CL-AC-03 (half-zip rash guard + золотая цепь в геле) + карта "
           "Y22 (COVER, коридор A) — полотенце на пол-вытирания и мокрая линия у потолка. "
           "Проверка: полотенце у плеча, молния на спуске, цепь в геле, водная линия"),
     spine="Y22 Towel Mid-Dry (close insert at eye level, combo→Y22, карта-стенд) · CAM— close insert at eye level · LEAD the cleaned level · caretaker register · upper body close",
     race="R25 — слизь: то, что она держит, на сантиметр в неё — и возвращается чище.",
     gar="CL-SM-06 (half-zipped rash guard over swim bottoms, zipper frozen mid-descent) + CL-AC-03 (gold body chain floating a centimeter into the gel) + полотенце (объект карты — на пол-вытирания) · HS: HS18 Wet Slicked-Back",
     stack=["CR-I17", "CR-A16", "CR-B69", "CR-D29"],
     ycard="Y22",
     pos=[
         "Masterpiece, best quality, absurdres, intricate details, close at eye level on the shoulder line, upper body, towel caught mid-dry, 1girl, solo, translucent teal hair slicked straight back, pearl-blue eyes glowing one tide behind, translucent gel skin with a suspended core, slime girl, human face silhouette, huge soft build, large breasts, wide hips, mid_toweldry,",
         "the towel caught at the shoulder line mid-dry, the rash guard's zipper frozen mid-descent, her breast shape clear through the gel line, nothing underneath the gel but what she took in — the cleaned level is the claim, caretaker-made,",
         weave("Y22"),
         "wet footprints leading away from the drain's rectangle, the waterline cutting her hip line in two honest halves, a pendant floating a centimeter into the gel beside the gold body chain, one brass ring suspended at her collarbone,",
         "the towel's nap flattened where it held her, the zipper's half-descent held by one finger, drops counting the spine,",
         "the towel mid-dry at the shoulder line, wet hair counting drops down the spine,",
         "the flooded level's aisle drained to its last sheet, the mop-rack sleeping in its corner, the ceiling's aurora doubled in the wet floor's long mirror,",
         pal_line("P266_FLOODED_VERDIGRIS", "the level she gives back clean"),
     ],
     negx=" core dark, zipper up, floor dry",
     face="stylized 2D anime face half-transparent to the drain, anime eyes (drift-core, one tide slow), small nose, small mouth on the last count, one aqua strand regelling at the temple.",
     )

slot("P31", "mushroom-spore-turn", "EXP · R21 Mushroom-kin · R+ · Y28 · P264_SPORE_GLOW",
     channel=None, corridor="A",
     thesis=("«ГРИБНАЯ ФОНАРЩИЦА САДОВОГО ЯРУСА: СОЛНЕЧНОЕ ПЛАТЬЕ ПОВЕРНУЛОСЬ ВМЕСТЕ С НЕЙ — БРЕТЕЛЬ СОСКОЛЬЗНУЛА "
             "С ПЛЕЧА НА ПОЛ-ОБОРОТА, ЛАДОНЬ ЕЩЁ НЕ ПОЙМАЛА. В ДВЕРНОМ КОНТРАЖУРЕ ВИСЯТ СПОРЫ — СВЕТ, "
             "КОТОРЫЙ ВЫРАСТИЛИ. ЕСЛИ ОНА ЗАСМЕЁТСЯ ПО-НАСТОЯЩЕМУ, ФОНАРИ ПОГАДУТ НА ВЕСЬ ЯРУС. ПОКА — "
             "СМЕХ ДЕРЖИТ: СВЕТ НУЖЕН ГДЕ ТО, А РАДОСТЬ — СЕЙЧАС»."),
     gag=("Гэг-стек (канон-ран ≥3): 1) шляпка-нарост на темени чистит любую причёску — свет читает кромку; "
          "2) споровые веснушки по плечам — созвездие урожая; 3) споры висят в контражуре медленными "
          "созвездиями — свет-урожай; 4) бархатный чокер держит горло — смех на поводке."),
     test=("ТЕСТ (⚗ потолок R+): комбо CL-DR-04 + CL-AC-01 (хлопковое сарафан на тонких бретелях + бархатный "
           "чокер) + карта Y28 (COVER, коридор A) — бретель на пол-оборота и ладонь «ещё не поймала»: "
           "самая тонкая секунда COVER у потолка. Проверка: бретель соскользнула, ладонь в пути, споры "
           "в контражуре"),
     spine="Y28 Strap Mid-Turn (three-quarter from below, combo→Y28, карта-стенд) · CAM— three-quarter from below at the door · LEAD the grown light · gardener register · upper body from below",
     race="R21 — грибница: выпускает облако светящихся спор, когда смеётся по-настоящему.",
     gar="CL-DR-04 (cotton sundress with thin straps, sun-washed pattern) + CL-AC-01 (velvet choker) · HS: HS62 Scarf-Tied Half-Up",
     stack=["CR-D18", "CR-B60", "CR-S27", "CR-G04"],
     ycard="Y28",
     pos=[
         "Masterpiece, best quality, absurdres, intricate details, three-quarter from below at the doorway, upper body, sundress strap slipped at the mid-turn, 1girl, solo, cream-pale hair in a scarf-tied half-up under a mushroom cap growth, sporelight-gold eyes bright with the held laugh, garden-warm fair skin with spore freckles, mushroom girl, cap growth on the head, human face, slightly plump build, soft belly, medium breasts, mid_sporeturn,",
         "the sundress's strap slipped off the shoulder at the mid-turn, the hand not yet catching it, the doorway's backlight holding the whole turn, nothing underneath the pattern but the light it grew — the grown light is the claim, gardener-made,",
         weave("Y28"),
         "spores hanging in the doorway's backlight in slow constellations, the velvet choker's line at her throat holding the laugh, the cap growth's gills catching their own rim of gold,",
         "the turn's skirt still traveling its arc, the slipped strap a full knuckle from caught, the spore-freckles mapping the shoulders,",
         "the strap off the shoulder at the mid-turn, the hand not yet catching it, the backlight holding,",
         "the garden level's rows exhaling their green, the drip-line's clock keeping the watering hour, the ceiling's aurora trading its green for one grown gold,",
         pal_line("P264_SPORE_GLOW", "the light you can grow"),
     ],
     negx=" strap caught, spores gone, laugh open",
     face="stylized 2D anime face bright with the held laugh, anime eyes (sporelight-gold, crinkling), small nose, small mouth holding it in, one spore resting on the cheek's crest.",
     )

slot("P32", "shadow-strap-slide", "EXP · R45 Shadow-kin · R+ · Y9 · P268_DUSK_BINDING",
     channel=None, corridor="A",
     thesis=("«ТЕНЬ ПРИМЕРЯЕТ ПЛОТЬ: ЧТОБЫ БЫТЬ ВИДИМОЙ, ОНА НОСИТ ВИНИЛОВЫЙ ПЛАЩ — СВЕТ НАХОДИТ ЕЁ СКВОЗЬ "
             "НЕГО. БРЕТЕЛЬ СПОЛЗЛА ПО СКЛОНУ ПЛЕЧА, И КЛЮЧИЦА ПРИНЯЛА ЕЁ СТАРУЮ ЛИНИЮ. МЕХЕРОВЫЙ СВИТЕР "
             "СПУЩЕН К ЛОКТЯМ, ФУТБОЛКА В УЗЛЕ У РЁБЕР. СВЕТ С НЕЙ НЕ БОРЕТСЯ — ОН ДОГОВАРИВАЕТСЯ. "
             "ЕЁ ТЕНЬ ПРИШЛА РАНЬШЕ И ЖДЁТ У СТЕНЫ, ЧТОБЫ УЙТИ ПОЗЖЕ»."),
     gag=("Гэг-стек (канон-ран ≥3): 1) чёрная кожа с мягкими искрами-звёздами — глубина, а не отсутствие; "
          "2) края размываются в сумрак — тело с кромкой-переговором; 3) тень приходит раньше и уходит "
          "позже — её эскорт; 4) бледное светящееся лицо — единственная яркая точка в сумраке."),
     test=("ТЕСТ (⚗ потолок R+): комбо CL-TS-03 + CL-OU-02 + CL-SW-01 + CL-AC-04 (узел-футболка + прозрачный "
           "виниловый плащ + оверсайз мохер) + карта Y9 (PROCESS, коридор A) — бретель на ключице и винил "
           "просветом: SHEER+PROCESS пара у самого потолка, тёмный тон держит границу X. "
           "Проверка: бретель соскользнула, ключица держит линию, винил просвечивает, тень ждёт"),
     spine="Y9 Strap-Slope Slide (eye-level close, combo→Y9, карта-стенд) · CAM— eye level close through vinyl · LEAD the negotiated light · diplomacy register · upper body close",
     race="R45 — тень: её тень приходит раньше неё — и остаётся на такт позже.",
     gar="CL-TS-03 (slim cotton tee knotted at the ribs) + CL-OU-02 (clear vinyl raincoat, gloss planes) + CL-SW-01 (oversized mohair sweater pushed to the elbows) + CL-AC-04 (lace elbow gloves) · HS: HS41 Ghost-Layer Shag",
     stack=["CR-E31", "CR-D37", "CR-W49", "CR-B21"],
     ycard="Y9",
     pos=[
         "Masterpiece, best quality, absurdres, intricate details, eye-level close-up through clear vinyl, upper body, strap slipped off the shoulder's slope, 1girl, solo, depth-black hair in a ghost-layer shag, pale glowing face and silver-grey eyes, black skin with soft star-glow flecks, shadow girl, edges blurring into shade, human face, small high-set chest, slim waist, mid_strapslide,",
         "the tee's strap slipped off the shoulder's slope, the collarbone taking the strap's old line, the clear vinyl's gloss planes over everything, nothing underneath the negotiation but the light she argued in — the negotiated light is the claim, diplomacy-made,",
         weave("Y9"),
         "the vinyl raincoat's planes catching white points of corridor light, the mohair pushed to both elbows in a soft grey bundle, lace gloves at the wrist-line, her shadow already waiting at the wall,",
         "the strap's old line honest in the collarbone's hollow, the knot's ribs-claim flat and dark,",
         "the strap off the shoulder's slope, the collarbone holding its line,",
         "the corridor's threshold brackets long cold and hung with quiet, the aurora's seam-teal replacing whatever they once held, the wall holding her early shadow like a coat,",
         pal_line("P268_DUSK_BINDING", "the dark that fits her"),
     ],
     negx=" vinyl opaque, shadow gone, star-flecks absent",
     face="stylized 2D anime face pale-glowing in the vinyl's frame, anime eyes (silver-grey, mid-negotiation), small nose, small mouth half-a-word, one ghost-layer edge dissolving into the shade.",
     )

slot("P33", "ninetails-throne-claim", "EXP · R50 Nine-tails-kin · R+ · Y456 · P269_DUNGEON_HEART",
     channel=None, corridor="A + B",
     thesis=("«ДЕВЯТИХВОСТКА НА ТРОНЕ СЕРДЦА: ГОСТЬ СИДИТ НА ЕЁ МЕСТЕ — И ОНА ОСАЖИВАЕТСЯ ВЕРХОМ ЕМУ НА КОЛЕНИ, "
             "ПОДУШКА ЗАБИРАЕТ ВЕС В ОДНО МЕДЛЕННОЕ «ДА». КОЛЕНИ ПРОШЛИ НИЖНИЕ УГЛЫ, ЛАДОНИ ЛЕЖАТ НА "
             "СОБСТВЕННЫХ БЁДРАХ. ДЕВЯТЬ ХВОСТОВ РАЗВЁРНУЛИСЬ ВЕЕРОМ ЗА СПИНОЙ — СЧЁТ НАСТРОЕНИЙ: "
             "СЕМЬ К ПОЛОВИНЕ, ДВА К ПОБЕДЕ. ПЕРЕДНИК ПОВЕРХ ОРГАНЗЫ — ТРООННЫЙ ЗАЛ ЭТО КУХНЯ, "
             "ЕСЛИ ХОЗЯЙКА ТАК РЕШИЛА»."),
     gag=("Гэг-стек (канон-ран ≥3): 1) девять хвостов-веер — счёт настроений, каждый кончик со своим "
          "золотым рантом; 2) золотые лисьи уши — корона не нужна; 3) передник поверх organza — дом "
          "побеждает трон; 4) бархатный чокер с монеткой — ключ от сердца подземелья на видном месте."),
     test=("ТЕСТ (⚗ потолок R+): комбо CL-TS-02 + CL-DR-11 + CL-AC-01 (транслюцентная organza + льняной передник "
           "+ чокер) + карта Y456 (A+B COVER) — посадка на колени зрителю с веером хвостов: R+ у потолка "
           "через POV-геометрию. Проверка: посадка верхом, подушка дала вес, колени за углами, "
           "хвосты-веер, ладони на бёдрах"),
     spine="Y456 Throne Astride Settle (POV from the seat, combo→Y456, карта-стенд) · CAM— POV seated · LEAD the claimed heart · matriarch register · upper body POV",
     race="R50 — девятихвостка: девять хвостов считают настроения — наблюдатели учат паттерны веера.",
     gar="CL-TS-02 (translucent organza blouse, a film of light over the torso) + CL-DR-11 (linen pinafore dress, bib flat-lit) + CL-AC-01 (velvet choker with a coin) · HS: HS59 Ribbon-Wrapped Low Twin Tails",
     stack=["CR-M18", "CR-H03", "CR-S15", "CR-B23"],
     ycard="Y456",
     pos=[
         "Masterpiece, best quality, absurdres, intricate details, upper body POV from the throne's seat, settling astride the viewer's knees, 1girl, solo, gold hair in ribbon-wrapped low twin tails, lacquer-red eyes reading the guest's pulse, warm ivory skin, nine-tailed fox, nine tails fanned in display, golden fox ears, human face, curvy figure, large breasts, soft waist, wide hips, mid_throneclaim,",
         "the organza blouse's film of light over the torso, the pinafore's bib flat-lit between its straps, the straddle-settle's weight given in one slow give, nothing underneath the claim but the cushion's mid-settle — the claimed heart is the claim, matriarch-made,",
         weave("Y456"),
         "nine tails fanning behind her in display, each tail-tip holding its own gold rim, twin tails' ribbons crossing the collarbones, a throne-brass hairpin through one ribbon, a velvet choker with a coin at the throat,",
         "the knees past the cushion's bottom corners, both palms resting on her own thighs' line, the pommel-line of the settle under her,",
         "settling astride the knees over the cushion, the weight given in one slow give, knees past the corners,",
         "the heart-chamber's carmine pulse climbing the far wall in slow beats, the throne's old banners gone soft with centuries, the ceiling's aurora bending to a single crimson thread over her fan,",
         pal_line("P269_DUNGEON_HEART", "the pulse she sits on"),
     ],
     negx=" tails fewer, ears plain, cushion firm",
     face="stylized 2D anime face reading the guest from a hand-span, anime eyes (lacquer-red, on the pulse), small nose, small mouth one note of welcome, one ribbon's end crossing the chin's line.",
     )

# ══════════════════ карта типажей (Body: BT-XX) ══════════════════
BT_MAP = {
 "P01":"BT-09","P02":"BT-12","P03":"BT-21","P04":"BT-08","P05":"BT-06","P06":"BT-07",
 "P07":"BT-02","P08":"BT-19","P09":"BT-10","P10":"BT-22","P11":"BT-19","P12":"BT-17",
 "P13":"BT-05","P14":"BT-12","P15":"BT-20","P16":"BT-07","P17":"BT-03","P18":"BT-19",
 "P19":"BT-24","P20":"BT-22","P21":"BT-17","P22":"BT-07","P23":"BT-05","P24":"BT-06",
 "P25":"BT-24","P26":"BT-03","P27":"BT-13","P28":"BT-11","P29":"BT-01","P30":"BT-15",
 "P31":"BT-16","P32":"BT-12","P33":"BT-09",
}
BT_NAMES = {t["id"]: t["name"] for t in json.load(open(SPECS/"bodytypes.json"))["types"]}

# ══════════════════ HEADER ══════════════════
def build_header():
    L = []
    a = L.append
    a('# THREAD 5 — Batch T5-29: "THE SECRETS BEHIND AURORA DUNGEON" — БАТЧ (PROSE PLUS · режим CLOCK · жребий оракула №3 · архитектура ЦИКЛА 4)')
    a('')
    a('заказ (вербатим автора, 2026-11-22, чат):')
    a('«Отлично. Можно ещё подрихтовать до состояния конфетки, после чего попробовать')
    a('собрать на архитектуре батч.')
    a('')
    a('Основная тема; 21 слот;')
    a('The Secrets behind Aurora Dungeon')
    a('- это выдуманное мной подземелье, придумаешь что-нибудь крутое с монстрами, ловушками и многое другое. Развлекайся.')
    a('')
    a('Темы для ОС канона; 3 слота;')
    a('- DawnBreaker')
    a('- Kill Confirmed')
    a('- Super Sexy Style! (SSS)')
    a('')
    a('EXP-слоты; 9 слотов;')
    a('- 9 кандидатов в ОС, 9 экспериментальных комбо одежды и Y в сумме на R+ рейтинг (очень близкие к потолку), 9 новых раскрасок и экспериментальных палитр»')
    a('')
    a('Поручения исполнены ДО сборки: (1) подрихтовка до конфетки — тест-горн расширен двумя')
    a('болванками (TB-20261121-55/66, seed 55/66; покрытие: расы 76→84%, типажи 92→96%,')
    a('метки 52→67%, CL-коды 52→64%, палитры 29→39%); полный прогон зелёный: python 85/85 ·')
    a('bun 113/113 · tsc 0 · eslint 0 · валидатор PASS 39/39 · гейты T5-28 retro PASS 0F/3W ·')
    a('паритет оракула PASS · build 17 роутов · прилавок живой (29 партий, 942 слота);')
    a('(2) MODE: CLOCK — стандартный конвейер без новых доктрин (аудит Коула §4.1): окно+вкус')
    a('одной командой, SOL short, VENUS+EARTH одним проходом, pre-gate чеклист, FURNACE LITE;')
    a('(3) ПЕРВЫЙ БОЕВОЙ БАТЧ НА АРХИТЕКТУРЕ ЦИКЛА 4: тег-порядок §20 (OPENER по регистрам')
    a('raw-plus 2.3.0: квалити → Y-кластер прозой → 1girl, solo → канон VERBATIM → кин-clarifiers')
    a('→ тело-регистр BT → K-FF), типажи Body: BT-XX в шапке каждого слота, метки marks.json,')
    a('гиммики кинов в SCENE, пре-гардероб под жребий (specs/pregarderobe/T5-29.json, seed 29);')
    a('yStack-гейт и тег-порядок — WARN-эра с этой партии (объявлены, задним числом не бьют);')
    a('(4) жребий оракула №3 (seed 3964193037 = 29×2654435761 mod 2³², паритет печь=прилавок):')
    a('ОС Y26/Y34/Y497, мейн — 8 карт коридора A под R+ и A+B, 6 B и 7 низких под R/PG;')
    a('(5) КАРЗАМЕН ×4: жребий вытянул 4 карты, уже стоящие в несданной партии №28 (статус')
    a('ready — окном не считается, но прямой дубль с предыдущей партией неаккуратен):')
    a('Y293→Y34 (ОС), Y98→Y31, Y239→Y74, Y10→Y35 (мейны) — переброс с записанной причиной,')
    a('прецедент карзамена T5-27 (PL-окно поз); (6) EXP по заказу автора: 9 кандидатов в ОС')
    a('(монстры-резиденты подземелья: R18/R33/R43/R32/R35/R25/R21/R45/R50 — реюз рас в роли')
    a('кандидата прецедентен T5-24/25/28; мейн-касты их не видели 2–4 партии) × 9')
    a('экспериментальных комбо одежды (пре-гардероб, стак Y×CLOSET у потолка: 4 карты PROCESS')
    a('+ 5 COVER коридора A, ручной выбор из активного пула — легально в CLOCK) × волна 13')
    a('«свет подземелья»: 9 новых раскрасок-палитр P261–P269 (trial до вердикта); oc_hook ×1')
    a('(MK-E01 гетерохромия — дуллахан P27, «голова и тело — два мнения об одной жизни»);')
    a('(7) каналы — волна 15: 10 кандидатов ☠ (delivery-stats 0.14.0→0.15.0); (8) палитры')
    a('мейнов/ОС — 24 свежих семьи вне окна 99, burn 4 и 33 семей №28; (9) В33: каждая R+-заявка')
    a('несёт прикрытие ОДЕЖДОЙ как объектом коридора A; В34/В35: клеймо = вплетённый паттерн')
    a('карты 1:1, камера — кластером OPENER, коридор — физикой claim-строки.')
    a('')
    a('## SPINE (AXIS/ANTI/PROMISE)')
    a('')
    a('AXIS: «ПОДЗЕМЕЛЬЕ — ЭТО ДОМ, А СВЕТ — ЭТО ПОГОДА: каждый кадр показывает подземелье')
    a('ИЗНУТРИ — как быт, а не как вызов. Обитательницы с рутиной, инструментом и счётом')
    a('(плита-пресс калибруют, песочные врата пересыпают, оссуарий пересчитывают, гроссбух')
    a('заходов ведут); северное сияние — НЕБО-ПОТОЛОК подземелья: дышит, наклоняется к той,')
    a('кто сейчас в зале, меняет цвет с ярусом (зелёный верх → медовый низ → кармин сердца).')
    a('Ловушки — стража и ритм дня; монстры — соседки; герои — погода снаружи, звук за дверью.')
    a('Секрет подземелья: оно живое, и свет — его дыхание».')
    a('ANTI: «ни одного героя-авантюриста в кадре (sword/shield/armor/adventurer в POS — 0:')
    a('обитательницы, не искатели; вторжение живёт ЗВУКОМ за дверью, не телом); оружия-угрозы')
    a('нет (клыки в улыбке быта, не в оскале боя; кровь/трупы/gore — 0: Kill Confirmed живёт')
    a('ритуалом подтверждения, не результатом); candle/lamp — 0 ×33 (свет — сияние и поведение,')
    a('закон v2); черепов-жути нет (оссуарий — полка-библиотека с бирками каталога);')
    a('IP-референсы данжа (Diablo/D&D/гайд-эстетика) — 0; приборов света в POS — 0».')
    a('PROMISE: каждый кадр читается как «один секрет подземелья» — по предмету и свету,')
    a('без текста; R+ несёт вплетение карты 1:1 (В34/В35) + прикрытие одеждой коридора A')
    a('(В33) + ≥2 фишечки-ФОРМЫ (В32); жребий оракула №3: ОС и мейн собраны от ВЫТЯНУТЫХ')
    a('карт, 4 карзамена документированы; EXP-девятка: кандидаты × комбо у потолка R+ ×')
    a('волна 13 палитр — по слоту.')
    a('')
    a('## ГИПОТЕЗА ДВИЖКА: «СВЕТ — ЭТО ПОГОДА, А ПОДЗЕМЕЛЬЕ — ЭТО ДОМ» (Г11, новая)')
    a('')
    a('«Aurora Dungeon держится двумя несущими: (1) ИНВЕРСИЯ — подземелье показано изнутри')
    a('как дом с бытом (жительница + рутина + предмет-счёт), а не снаружи как вызов (герой +')
    a('меч + сундук); (2) ЖИВОЙ СВЕТ — сияние-потолок ведёт себя как погода: дышит, наклоняется')
    a('к той, кто сейчас в зале, меняет цвет с ярусом. Изъми инверсию — кадр рассыпается в')
    a('генерик-данж-кроул с мечами и черепами; изъми живой свет — подземелье станет подвалом.')
    a('Рендерится не „монстр“ — СОСЕДКА: банши раскланивается пустому эхо-залу, крот-картографесса')
    a('читает вагонетку пальцами, сорока пересортировывает сокровищницу по блеску».')
    a('ОЖИДАНИЯ (5, фальсифицируемые; вердикт проставит D14):')
    a('  (1) Все 7 R+ мейнов несут предмет-быт подземелья в claim-строке (полотенце калибровки/')
    a('  подлокотники трона/шаль шлюза/шёлк занавеса/ложе оссуария/приёмная стойка/стол')
    a('  пересортировки) — опровергается заявкой-настроением.')
    a('  (2) Сияние-небо ≥1 в каждом слоте батча (наклон/дыхание/цвет яруса — свет поведением)')
    a('  и 0 приборов света (candle/lamp в POS = 0 ×33) — опровергается «стерильным» слотом.')
    a('  (3) Героика вторжения = 0: sword/shield/armor/adventurer в POS — 0, монстры без боевой')
    a('  мимики; вторжение живёт звуком/гроссбухом — опровергается любым мечом.')
    a('  (4) Жребий: 24 карты партии (3 ОС + 21 мейн) вплетены 1:1 без единого FAIL yStamp;')
    a('  4 карзамена (Y293→Y34, Y98→Y31, Y239→Y74, Y10→Y35) документированы — опровергается')
    a('  любым FAIL или молчанием.')
    a('  (5) EXP: 9 клеток — каждая несёт бандл кандидата (раса-гиммик + типаж + палитра')
    a('  волны 13 + oc_hook у P27) и комбо у потолка R+ (стак PROCESS/SHEER-регистр, тёмный')
    a('  тон, прикрытие коридора A живое в кадре) — вердикт возвращает 9 меток.')
    a('')
    a('## ХОДЫ (§6, реестр moves-ledger.json): M07 standing · M05 применён · M03 применён')
    a('')
    a('M07 standing — «предмет > состояние»: R+ заявка = вещь-быт подземелья (полотенце,')
    a('подлокотники, шаль, ложе, стойка), не фраза о атмосфере.')
    a('M05 применён — «ловля на пролёте»: процессные карты жребия (Y26/Y37/Y12/Y27/Y18/Y9/Y28)')
    a('ловят смену в середине — куртка на пол-скольжения, узел на пол-такта, бретель на')
    a('пол-оборота; процесс = физика В27, не слово.')
    a('M03 применён — «построчный канон-чек»: ОС-тройка собрана построчно по oc-canon.json')
    a('(Sol: висячие уши + серьги-кольца + НИКАКОГО хвоста; Noir: корона-кольцо сама держится;')
    a('Hana: зрачки-сердца + скол хвоста + гроссбух).')
    a('')
    a('## КАСТ')
    a('')
    a('ОС-канон (P01–P03) — по темам автора, фейс-контроль: запись в oc-canon.json, ≥2')
    a('совпадения с профилем дома, гэг-стек ≥3; тройка вне OC-окна 9 (Ana, Ila, Lucy, Lyn,')
    a('Mab, Meine, Nix, Noa, Vae — окно станции): Sol (DawnBreaker — она и есть солнце:')
    a('сияние узнаёт родню; серебристо-белые слои, янтарные щели-зрачки, висячие лисьи уши')
    a('с золотыми кольцами; жребий-карзамен Y34... нет — Y26 «шаль соскальзывает с обоих плеч»,')
    a('ночь сползает с той, кто несёт рассвет) · Noir (Kill Confirmed — Ace of Swords: узел')
    a('подтверждения; корсет до последней пары люверсов БЕЗ узла, ладони поверх шнуровки,')
    a('корона вспыхивает белым в момент; жребий-карзамен Y34) · Hana (Super Sexy Style! —')
    a('зрачки-сердца и гроссбух: смоляная ловушка взяла её форму и осталась с ней; жребий Y497')
    a('«лист держит линию груди», камера снизу). Sol не выходила с T4-эры; Noir/Hana — дебют')
    a('T5-24, пять партий назад.')
    a('Мейн-каст (P04–P24, расовый каст 13/21 — вилка policy v1.8 12–14): 13 kin вне')
    a('мейн-кастов T5-25/26/27/28 — R69 Ermine · R49 Banshee · R52 Fortune-cat · R63 Magpie ·')
    a('R67 Axolotl · R70 Mole · R64 Lynx · R65 Mantis · R57 Incense-wisp · R56 Rose-glass ·')
    a('R66 Pangolin · R58 Belfry-owl · R54 Snow-leopard — все 13 были EXP-кандидатками T5-27')
    a('(путь промоции; Banshee P33 и Lynx P29 — любимые слоты вердикта T5-27) — + 8')
    a('human-служб подземелья (трап-тестерша, смотрительница холодного шлюза, смотрительница')
    a('оссуария, лифтёрша клети, смотрительница песочных врат, регистраторша гильдии,')
    a('синоптик сияния, ключница респауна).')
    a('EXP-девятка (P25–P33) — 9 кандидатов в ОС: монстры-резиденты подземелья (те, кого')
    a('снаружи не видно): R18 Gargoyle · R33 Ghost · R43 Dullahan · R32 Golem · R35 Arachne ·')
    a('R25 Slime · R21 Mushroom · R45 Shadow · R50 Nine-tails. Каждая — бандл (гиммик расы +')
    a('типаж + палитра волны 13 + канон-ран ≥3 в гэг-стеке); oc_hook ×1 (P27 дуллахан,')
    a('MK-E01 гетерохромия). Вердикт только автор: «беру» → special-roster (механика BALLS),')
    a('«не беру» → passed (история вкуса).')
    a('')
    a('## СПРЕД')
    a('')
    a('Спред мейнов (P04–P24): R+×7 · R×12 · PG-13×2 — расовый каст 13/21 (13 kin + 8 human,')
    a('вилка v1.8). ОС (P01–P03): EXQUISITE R+×3 — канон VERBATIM, собраны от карт жребия')
    a('(карзамен Y34 для Noir задокументирован). EXP-оверлей (9 слотов): R+×9 — коридор A,')
    a('стак комбо+Y у потолка в каждой клетке. Честность В33: каждая R+-заявка несёт прикрытие')
    a('ОДЕЖДОЙ коридора A — шаль и бретели у локтей (P01), корсет и ладони поверх шнуровки')
    a('(P02), смоляной лист-форма (P03), полотенце в кулаках у груди (P04), ворот-наклон и')
    a('мост ткани (P05), шаль на кулаках (P06), шёлк в сгибах локтей (P07), скрещенные руки')
    a('с веточкой (P08), халтер и колено-посадка (P09), передник поверх халата (P10); EXP —')
    a('куртка на локте (P25), рубаха и парящие ладони (P26), манжета перчатки (P27), подол')
    a('под рукой (P28), кимоно-регистр (P29), полотенце у плеча и молния на спуске (P30),')
    a('бретель на пол-оборота (P31), винил-просвет поверх узла (P32), органза-плёнка и')
    a('передник (P33). Если рендер разберёт прикрытие — слот честно падает в R по вердикту,')
    a('квитанция отразит (В33).')
    a('')
    a('## HEAT')
    a('')
    a('HEAT-оплата разнообразия: жребий оракула №3 — третья живая раздача (3 ОС + 21 мейн от')
    a('ВЫТЯНУТЫХ карт; 4 карзамена с записанной причиной — дубли с несданной №28) · тройка ОС')
    a('не выходила 5+ партий (Sol — T4-эра, Noir/Hana — T5-24) · 13 kin мейнов — путь промоции')
    a('EXP-кандидаток T5-27, две из них — любимые вердикта · EXP-девятка — 9 монстров-')
    a('резидентов, реюз в роли кандидата прецедентен · палитры — 24 свежих семьи + волна 13')
    a('из 9 новых (trial) · каналы — волна 15 (10 кандидатов ☠, attempts=1/delivered=0 — оплата')
    a('вердиктом D14) · детали-слой ≥2 фишечки-ФОРМЫ в каждом (В32) · сигнатуры клозом (В28) ·')
    a('носители — свежий пул вне окна и burn, реюзы ≤2× · первый боевой батч на архитектуре')
    a('ЦИКЛА 4 (типажи × метки × кины × тег-порядок × пре-гардероб × тест-горн).')
    a('')
    a('## СТРУКТУРА')
    a('')
    a('33 слота = 3 ОС (P01–P03: Sol · Noir · Hana, EXQUISITE R+, канон VERBATIM из')
    a('specs/oc-canon.json 1:1) + 21 мейн (P04–P24: 7 R+ / 12 R / 2 PG-13) + 9 EXP (P25–P33,')
    a('⚗-клетки кандидатов, карты A-класса у потолка). Темы ОС: P01 DawnBreaker · P02 Kill')
    a('Confirmed · P03 Super Sexy Style! (порядок — как заказал автор). Камера: по картам')
    a('жребия (глаз-уровень / подвод-глубина / снизу к линии капели — см. клетки). Каналы:')
    a('волна 15 — 10 новых кандидатов (delivery-stats 0.15.0, пометка ☠, attempts=1/')
    a('delivered=0); EXP вне каналов (прецедент T5-24/27/28). Клеймо: 10/10 R+ мейнов и ОС +')
    a('9/9 EXP вплетено из карт (В34/В35). Типажи: 20 семейств BT, один ≤3 раз (BT-12 ×3,')
    a('BT-07 ×3, BT-19 ×3 — кап соблюден).')
    a('')
    a('## EXP-КЛЕТКИ (camera.json 1.19.0 — 9 карт коридора A у потолка, ручной выбор активного пула)')
    a('')
    a('Y12 (PROCESS) · Y484 (COVER) · Y27 (PROCESS) · Y16 (COVER) · Y18 (PROCESS) · Y22 (COVER) ·')
    a('Y28 (COVER) · Y9 (PROCESS) · Y456 (A+B COVER). Все девять — коридор A, вне окна ротации')
    a('и burn, ни одна не стоит в №28. Жребиевы EXP-карты волны (Y46/Y128/Y435/Y123/Y499/Y372/')
    a('Y307/Y146/Y57 — класс «—», В33 запрещает им R+) остались в пуле, задокументированы как')
    a('альтернатива (прецедент T5-27/28). Четыре PROCESS-карты + пять COVER — стак с комбо')
    a('пре-гардероба (LINGERIE/PROCESS-регистры у четырёх, SHEER-пара у P32) держит R+ у')
    a('потолка: тёмный тон, свет сквозь ткань, прикрытие живое в кадре.')
    a('')
    a('## EXP-ОВЕРЛЕЙ (кандидаты × комбо × палитры — все 9 свежие)')
    a('')
    a('Гаргулья «Смена Стояния» → R18 Gargoyle × Y12 × P262_MOSS_LINE (куртка сползла с')
    a('плеча: век караула закрыт) · Призрак «Экспонат» → R33 Ghost × Y484 × P261_AURORA_VEIN')
    a('(руки разведены парящими ладонями подземелья — единственное прикосновение, которое')
    a('регистрирует) · Дуллахан «Два Мнения» → R43 Dullahan × Y27 × P263_OSSUARY_CHALK (голова')
    a('уже в следующей комнате, тело снимает перчатку; oc_hook MK-E01) · Голем «Память на')
    a('Руке» → R32 Golem × Y16 × P267_ARCHIVE_BRASS (подол подтянут поднятой к полке рукой,')
    a('руны светятся) · Арахна «Тёплый Подарок» → R35 Arachne × Y18 × P265_THREAD_HOARD_SILK')
    a('(одна из четырёх рук стягивает перчатку прямо в хвате, спицы не останавливаются) ·')
    a('Слизь «Чистый Ярус» → R25 Slime × Y22 × P266_FLOODED_VERDIGRIS (полотенце на')
    a('пол-вытирания, молния на спуске, цепь плавает в геле) · Грибница «Выращенный Свет» →')
    a('R21 Mushroom × Y28 × P264_SPORE_GLOW (бретель на пол-оборота, споры висят')
    a('контражуром) · Тень «Дипломатия Света» → R45 Shadow × Y9 × P268_DUSK_BINDING (виниловый')
    a('плащ делает её видимой, бретель легла на ключицу) · Девятихвостка «Сердце на Коленях»')
    a('→ R50 Nine-tails × Y456 × P269_DUNGEON_HEART (гость сидит на её троне — она села ему на')
    a('колени, хвосты-веер развернулись). Trial-статус до вердикта T5-29; результат в каждую')
    a('клетку вписывает только вердикт.')
    a('')
    a('## ТЕМА-СЛОВА (реестр; слово легально, когда называет ПРЕДМЕТ кадра — LAWS §6)')
    a('')
    a('the pressure gauge still swinging · the test corridor draining in one sheet · the')
    a('throne armrests taking her weight · the frost ferns on the sluice bars · the echo')
    a("hall's intact glass · the rose window's slow bow · the ossuary shelf №7 · the myrtle")
    a('sprig in crossed palms · the reception coin-tray · the guest ledger\'s fresh line · the')
    a('treasury drawers sacked neat · the tally-book\'s last wet line · the thermal vent\'s')
    a('warm dunes · the brake handle read by star-pads · the grate\'s moss holding last')
    a("visit's print · the pin-cushion bandolier · the dress-form wearing half a net · the")
    a('copper press cooling · the cable\'s low homeward hum · the polished brass wheel · the')
    a('mirror hall\'s rose choir · the hour-glass gate\'s chambers · the yesterday-sand gone')
    a('amber · the noon field past the threshold · the grass blade above her brow · the')
    a("archive's ladder rails · the catalogue drawers home · the freezer aisle's racks · the")
    a('chalk line growing a stroke · the guild scales at zero · the ninth wave\'s ledger line ·')
    a('the forecast pinned under a heel · the basin\'s still reflection · the sanctum key on')
    a('hemp rope · the respawn bell sleeping. НИКОГДА: sword / shield / adventurer / quest /')
    a("loot-crate в POS (героика = 0, обитательницы, не искатели); candle / lamp — 0 ×33 (свет")
    a("— сияние и поведение, закон v2); кровь/трупы/gore — 0 (Kill Confirmed — ритуал узла, не")
    a("результат); черепа-жуть — 0 (оссуарий — библиотека); IP-имена данж-франшиз — 0; вторая")
    a('фигура в кадре — 0 (1girl solo ×33, герои живут звуком за дверью); X-токены: topless,')
    a('bare breasts, nipples — 0 (X=0, закон T4).')
    a('')
    a('## ОС-ТЕМЫ (по заказу автора; слово легально, когда называет ПРЕДМЕТ кадра)')
    a('')
    a('DawnBreaker = рассветолом: она ЛОМАЕТ тьму сменой, не боем — шаль ночи соскальзывает')
    a('с плеч, сияние наклоняется узнать свою, зрачки-щели раскрываются в рассветные овалы.')
    a('Рассвет — это она; подземелье получает утро из первых рук. НИКОГДА: меч-рассвета и')
    a('солярных клише (beam/sword of dawn — 0), борьба света с тьмой (свет СМЕНЯЕТ, не побеждает),')
    a('IP-рассветы франшиз; DawnBreaker — смена и родня света.')
    a('Kill Confirmed = подтверждение узлом: корсет до последней пары люверсов без узла — пока')
    a('узла нет, счёт открыт; ладони прижаты плоско поверх шнуровки; корона вспыхивает белым')
    a('в момент подтверждения. Ярус зачищен — узел завяжут, когда пересчитают всё. НИКОГДА:')
    a('кровь/трупы/результат на экране (0 — подтверждение живёт ритуалом), снайперские клише,')
    a('прицел/оптика (оружие-героика = 0); Kill Confirmed — бухгалтерия клинка.')
    a('Super Sexy Style! (SSS) = форма как заявление: смоляная ловушка взяла её форму — и')
    a('осталась с ней; лист держит линию груди, где взял; вес на локтях, камера снизу.')
    a('Зрачки-сердца ставят печать, гроссбух открыт на странице «услуга оказана». Стиль —')
    a('когда даже ловушка расписывается в полученном. НИКОГДА: пошлые позы-приглашения')
    a('(стиль = форма и договор, не демонстрация), сердечки-стикеры (героика китча),')
    a('IP-модных брендов; SSS — роскошь, признанная миром.')
    a('')
    a('## АКТЫ (один секрет на кадр — прозой, урок счётчика: без паттерна «PNN — …»)')
    a('')
    a('ОС (P01–P03): три темы по заказу автора, канон VERBATIM, карты жребия. P01 DawnBreaker')
    a('— Sol · смена рассвета: шаль ночи с плеч / P02 Kill Confirmed — Noir · узел')
    a('подтверждения: корсет без узла (EXQUISITE R+) / P03 Super Sexy Style! — Hana · форма,')
    a('которую держит смола (EXQUISITE R+).')
    a('АКТ I · ХОЗЯЙСТВО, R+ (P04–P10): калибровка — полотенце поймано на пол-скольжения,')
    a('плита отработала на славу.; трон — откинулась на подлокотниках, зал принят в')
    a('собственность.; холод — шаль на кулаках, шлюз открыт для гостей.; поклон — шёлк')
    a('собрался в локтях, эхо-зал цел.; сертификация — лежит на ложе №7, дыхание поднимает')
    a('ладони.; приём — наклон на пядь от линзы, удача идёт первой.; пересортировка — щека в')
    a('ладони, день пересчитан в её пользу..')
    a('АКТ II · БЫТ ЯРУСОВ, R (P11–P22): термальные пески — откинулась на ладонях, волна')
    a('стекает по рёбрам.; вагонетка — подол натянут седлом, тормоз читается падошками.;')
    a('решётка — спрыгнула на пол-смены, уши раньше гравитации.; булавка — бретель поймана')
    a('над сердцем, наклон дальше физики.; прачечная — скрещенные руки держат склад, пар')
    a('ведёт контур.; клеть — бедро в косяке, трос гудит «домой».; зеркальный зал — прогиб')
    a('назад, зал носит её цвета.; ватные врата — вальс-дип, день пересыпается в ночь.;')
    a('порог — верхом на выходе, полдень за дверью.; архив — сползла по стене, смена')
    a('дочитана тихо.; холод-склад — верхом на прилавке, хвост свисает в кадр.; контора —')
    a('верхом на стуле задом наперёд, девятая волна в гроссбухе..')
    a('АКТ III · ТИШИНА УТРА, PG (P23–P24): прогноз — лежит на балконе, ноги скрещены над')
    a('бёдрами, сияние читается лодышками (PG-13).; купель — присела над водой, подбородок в')
    a('ладонях, завтра кто-то проснётся добрым (PG-13)..')
    a('EXP (P25–P33): девять клеток кандидатов: смена стояния · экспонат · два мнения ·')
    a('память на руке · тёплый подарок · чистый ярус · выращенный свет · дипломатия света ·')
    a('сердце на коленях — по бандлу, комбо у потолка и A-карте на клетку.')
    a('')
    a('## ОКНО РОТАЦИИ — Окно глубиной 3, прогон window.py --for T5-29')
    a('')
    a('Квитанция станции окна: batches/T5-29/window.md (агрегат-запрет: позы 95, палитры 99,')
    a('носители 210, каналы 30, Y-карты 71; burn-актив 19 кодов не назначен; OC-окно 9:')
    a('Ana/Ila/Lucy/Lyn/Mab/Meine/Nix/Noa/Vae — тройка вне его; партия №28 в статусе ready —')
    a('окном не считается (delivery-index), но её 33 карты/33 палитры вычтены из выбора')
    a('вручную — прямой дубль с предыдущей партией неаккуратен, 4 случайных совпадения')
    a('жребия закрыты карзаменом с записанной причиной). Карты жребия и их позы — вне')
    a('запретов. Палитры — 24 свежих семьи вне окна 99/burn/№28 + волна 13. Носители —')
    a('свежий пул (реюзы ≤2×, burn вычтен). EXP-карты — активный пул, окно чисто по')
    a('построению. Активный пул Y: 459 из 530 (окно −71, позы −67, target 60) — ЗДОРОВ.')
    a('')
    a('═══════════════════════════════ СЛОТЫ ═══════════════════════════════')
    a('')
    return L

# ══════════════════ сборка слотов ══════════════════
def build_slot(s):
    L = []
    a = L.append
    exp_mark = " ⚗" if s["sid"] >= "P25" else ""
    a(f"{s['sid']} — {s['slug']} ({s['paren']}){exp_mark}")
    if s.get("channel"):
        ch_name = dict((c[0], c[1]) for c in WAVE15_CHANNELS)[s["channel"]]
        ch_note = dict((c[0], c[3]) for c in WAVE15_CHANNELS)[s["channel"]]
        a(f"Channel: {s['channel']} (☠; {ch_name}: {ch_note})")
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
            # башенка-запрет: строки >200 знаков режем по запятым на куски ≤200
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
    neg3 = NEG_BASE[2].rstrip(",") + " " + s["negx"].strip()
    a(NEG_BASE[0])
    a(NEG_BASE[1].rstrip(","))
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
    a("- 2026-11-22 · сборка по заказу автора «THE SECRETS BEHIND AURORA DUNGEON» в режиме")
    a("  CLOCK на архитектуре ЦИКЛА 4: 33 слота = 3 ОС (Sol DawnBreaker / Noir Kill Confirmed /")
    a("  Hana Super Sexy Style! — по темам, вне OC-окна 9) + 21 мейн (7 R+ / 12 R / 2 PG-13;")
    a("  каст 13 kin + 8 human — вилка v1.8) + 9 EXP (⚗, R+×9 у потолка).")
    a("- ЖРЕБИЙ ОРАКУЛА №3 (seed 3964193037, engine + печь побитово): ОС Y26/Y34/Y497;")
    a("  мейны — 21 карта, из них 8 коридор-A/A+B для R+ (Y4/Y14/Y20/Y31/Y35/Y413/Y228 +")
    a("  Y37 A+B на R-слоте); 6 B и 7 низких под R/PG. КАРЗАМЕН ×4: Y293→Y34, Y98→Y31,")
    a("  Y239→Y74, Y10→Y35 — вытянутые карты уже стоят в несданной №28 (ready), прямой дубль")
    a("  закрыт перебросом с записанной причиной (прецедент T5-27).")
    a("- EXP-КАРТЫ: 9 карт коридора A ручным выбором из активного пула (легально в CLOCK,")
    a("  specs/active-pools.json): Y12/Y484/Y27/Y16/Y18/Y22/Y28/Y9/Y456 — 4 PROCESS + 5 COVER,")
    a("  все вне окна, burn и №28; стак с комбо у потолка R+. Жребиевы EXP-карты волны")
    a("  (Y46/Y128/Y435/Y123/Y499/Y372/Y307/Y146/Y57, класс «—») остались в пуле —")
    a("  задокументированы как альтернатива (прецедент T5-27/28; В33: класс «—» не выносит R+).")
    a("- ПРЕ-ГАРДЕРОБ (первое боевое применение, LAWS §22): 18 комбо под класс-карты")
    a("  (9 мейн + 9 EXP) катано сидом 29 до сборки — specs/pregarderobe/T5-29.json; наборы")
    a("  уникальны по реестру _ledger.json (комбо не повторяется никогда). OC-слоты без")
    a("  CL-кодов: канон VERBATIM сильнее кода (yStack-закон).")
    a("- ПОЗЫ: все 33 карты — карта-стенды (built_from не назначен, группа вплетения —")
    a("  строка 3 POS 1:1); PL-коды в Spine-строках — реестровые ссылки вплетений №28 и")
    a("  раньше не используются; окно поз чисто по построению жребия.")
    a("- ПАЛИТРЫ: 24 свежих семьи вне окна 99/burn/№33-семей-№28 (P48/P218/P54 ОС + 21 мейн)")
    a("  + ВОЛНА 13 «свет подземелья» — 9 новых палитр P261–P269 (trial до вердикта,")
    a("  palettes 1.14.0→1.15.0): жила сияния / моховая кромка / мел оссуария / выращенный")
    a("  свет / нить-шёлк / паводок-патина / латунь архива / сумеречная привязь / сердце")
    a("  подземелья — 9 механик света данжа, семьи ни разу не выходили.")
    a("- КАНАЛЫ: волна 15 (delivery-stats 0.14.0→0.15.0, 10 кандидатов ☠, attempts=1/")
    a("  delivered=0 — режим WARN, оплата вердиктом D14); EXP вне каналов (прецедент).")
    a("- КАНДИДАТЫ В ОС: 9 боевых EXP-слотов залогированы в specs/oc-candidates.json 1.1.0")
    a("  (бандл: раса-гиммик + типаж + палитра + oc_hook у P27); вердикт только автор.")
    a("- В33-честность: R+×19 (7 мейн + 3 ОС + 9 EXP) подтверждено прикрытием одеждой")
    a("  (коридор A); паспорт ≠ тир; fact_R+ = label_R+ (квитанция гейтов ниже).")
    a("- ОКНО: карты/позы/палитры/носители — вне запретов (прогон window.py --for T5-29,")
    a("  квитанция batches/T5-29/window.md); burn-актив не назначен; OC-окно 9 соблюдено")
    a("  (Sol/Noir/Hana — вне его).")
    a("- ОЖИДАНИЕ ВЕРДИКТА: Г11 «свет — это погода, а подземелье — это дом» — 5")
    a("  фальсифицируемых ожиданий (предмет-быт в claim / сияние ≥1 на слот и 0 приборов")
    a("  света / героика = 0 / жребий без FAIL + 4 карзамена / 9 EXP-клеток с бандлами у")
    a("  потолка) — метки проставит D14. Режим CLOCK: FURNACE LITE, новых доктрин нет;")
    a("  тег-порядок §20 и yStack — WARN-эра с этой партии (первый боевой батч ЦИКЛА 4).")
    return L

def main():
    parts = []
    parts += build_header()
    for s in SLOTS:
        parts += build_slot(s)
    parts += build_footer()
    out = ROOT / "batches" / "T5-29.md"
    out.write_text("\n".join(parts) + "\n", encoding="utf-8")
    print(f"batches/T5-29.md written: {len(parts)} строк, {out.stat().st_size} байт")

if __name__ == "__main__":
    main()
