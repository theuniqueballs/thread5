# -*- coding: utf-8 -*-
import io

path = '/home/z/my-project/thread5/batches/T5-18.md'
s = io.open(path, encoding='utf-8').read()

def rep(old, new):
    global s
    n = s.count(old)
    assert n == 1, "count=%d for: %r..." % (n, old[:90])
    s = s.replace(old, new)

# --- P01: палитра P69 (burn) -> P08_MIDNIGHT_BLUE; claim-лексема в первые 60 слов ---
rep(u"Masterpiece, best quality, upper body frontal at eye level, 1girl, solo, original character, the hugged gift pressing a soft warm line through thin knit, frost-pale-blue ice-shadow palette with ember-deep-orange-dying warmth, platinum french bob hair with wispy bangs, ice-blue eyes with white lashes, mediterranean bronze skin, slim athletic build with small breasts, thin steel chain with a single small key pendant at the throat, thin pink scar across the neck's front, mid_gift_glance",
u"Masterpiece, best quality, upper body frontal at eye level, 1girl, solo, original character, the hugged gift pressing nipples a faint print through the thin knit, midnight-blue palette with starlight-white and silver, platinum french bob hair with wispy bangs, ice-blue eyes with white lashes, mediterranean bronze skin, slim athletic build with small breasts, thin steel chain with a single small key pendant at the throat, thin pink scar across the neck's front, mid_gift_glance")

rep(u"Ember frost palette, frost-pale-blue and ice-shadow, ember-deep-orange-dying warmth pooling at the floor vents, pale-gold-ember accent at the ribbon; her colors are heat kept strictly indoors and handed out in denials.",
u"Midnight blue palette, midnight-blue over starlight-white, silver frost at the glass ribs, one warm-amber accent at the ribbon she will not hand over; her colors are warmth kept strictly indoors and handed out in denials.")

rep(u"muted colors, gray palette, pale colors, desaturated, white haze, milky fog, soft focus, hazy, black eyelashes, dark eyelashes, brown eyelashes, thick eyelashes, olive skin, large breasts, long hair, tags readable, text, caption, gifts stacked neatly, shoulder covered",
u"muted colors, gray palette, pale colors, desaturated, white haze, milky fog, soft focus, hazy, black eyelashes, dark eyelashes, brown eyelashes, thick eyelashes, olive skin, large breasts, long hair, warm candlelight, bright red, tags readable, text, caption, gifts stacked neatly, shoulder covered")

# --- P02: claim-лексема в первые 60 слов ---
rep(u"Masterpiece, best quality, upper body three-quarter at eye level, 1girl, solo, original character, the open reliquary box held chest-high pressing the cotton to her shape, obsidian-deep gold-leaf ceremonial palette, very long ivory-white hair, thin white veil covering the whole face except the bare mouth, snow-pale skin, slender body with modest neat breasts, thin crown of dark thorns over the veil, mid_vow_openbox",
u"Masterpiece, best quality, upper body three-quarter at eye level, 1girl, solo, original character, the open reliquary box held chest-high with nipples a cold press where the chill finds the weave, obsidian-deep gold-leaf ceremonial palette, very long ivory-white hair, thin white veil covering the whole face except the bare mouth, snow-pale skin, slender body with modest neat breasts, thin crown of dark thorns over the veil, mid_vow_openbox")

# --- P03: канал в реестр, claim-лексема в первые 60 слов, NEG без отрицания существования ---
rep(u"Channel: honey-sheen-delivery (live; медовая нить от пальцев к губам тянет заявку сама — сатин липнет по геометрии тела честно)",
u"Channel: r-geometry (live; медовая нить от пальцев к губам тянет заявку сама — сатин липнет по геометрии тела честно)")

rep(u"Masterpiece, best quality, full-length from a low three-quarter angle, 1girl, solo, original character, the honey-string stretched from raised fingers to her lips, honey-amber-deep beeswax-gold palette, long golden-blonde hair with cyan-teal under-streaks worn loose past the chest, large glossy obsidian-black eyes, fair warm ivory-gold skin with gold-leaf sheen, tall full-figured build with wide hips and full heavy breasts, teal ridged swept-back horns, cyan translucent fin-fans at the head, mid_honey_string",
u"Masterpiece, best quality, full-length from a low three-quarter angle, 1girl, solo, original character, the honey-string stretched from raised fingers to her lips with breast shape printed by the slack neckline, honey-amber-deep beeswax-gold palette, long golden-blonde hair with cyan-teal under-streaks worn loose past the chest, large glossy obsidian-black eyes, fair warm ivory-gold skin with gold-leaf sheen, tall full-figured build with wide hips and full heavy breasts, teal ridged swept-back horns, cyan translucent fin-fans at the head, mid_honey_string")

rep(u"muted colors, gray palette, pale colors, desaturated, white haze, milky fog, soft focus, hazy, black hair, brown hair, short hair, dark skin, grey skin, green skin, no wings, small wings, vestigial wings, wings folded, no tail, small tail, antler horns, branching horns, broken honey-string, offered spoon, second figure",
u"muted colors, gray palette, pale colors, desaturated, white haze, milky fog, soft focus, hazy, black hair, brown hair, short hair, dark skin, grey skin, green skin, small wings, vestigial wings, wings folded, small tail, antler horns, branching horns, broken honey-string, offered spoon, second figure")

# --- шапка: окно ротации (парсер ищет «Окно») ---
rep(u"""ЗАПРЕТ ОКНА: позы 99 (PL300–PL399) · палитры 91 · кинетики 0 · носители 179 · BURN 19.
Ответ батча (после вето): мейки — 21 first-use PL403–PL423; EXP — 9 first-use PL424–PL432;
ОС — 3 first-use PL433–PL435 (poses.json 1.8.1); срез PL400–PL402 остаётся в ledger.
Палитры — 21 свободных из реестра (мейки) + 3 ОС-палитры из реестра вне окна
(P69_EMBER_FROST / P06_OBSIDIAN_GOLD / P115_HONEY_TRAP) + 9 новых (P171–P179).
Кинетики — 33 новых K-FF (K216–K248, живы K219–K248) + 3 ОС-мида K249–251
(pools.json 1.2.1); носители — только вне окна и вне burn.""",
u"""Окно ротации: запрет 99 поз (PL300–399) / 91 палитра / 179 носителей / 19 burn.
Ответ батча (после вето): мейки — 21 first-use PL403–PL423; EXP — 9 first-use PL424–PL432;
ОС — 3 first-use PL433–PL435 (poses.json 1.8.1); срез PL400–PL402 остаётся в ledger.
Палитры — 21 свободных из реестра (мейки) + 3 ОС-палитры из реестра вне окна
(P08_MIDNIGHT_BLUE / P06_OBSIDIAN_GOLD / P115_HONEY_TRAP) + 9 новых (P171–P179).
Кинетики — 33 новых K-FF (K216–K248, живы K219–K248) + 3 ОС-мида K249–251
(pools.json 1.2.1); носители — только вне окна и вне burn.""")

# --- шапка: первая партия, P69 -> P08 ---
rep(u"violet-dominant): P69_EMBER_FROST → P01 · P06_OBSIDIAN_GOLD → P02 · P115_HONEY_TRAP → P03.",
u"violet-dominant): P08_MIDNIGHT_BLUE → P01 · P06_OBSIDIAN_GOLD → P02 · P115_HONEY_TRAP → P03.")

# --- шапка: каст 10/21 -> 12/21 (факт: 12 кин-слотов, 12 уникальных кодов, human×9) ---
rep(u"""каст мейнов 10/21 (10 кодов кинов + human×11); ОС — канон-ростер (Nix human · Ash human ·
Ana канон VERBATIM). EXP: R53–R61, код на слот.""",
u"""каст 12/21 (12 кодов кинов на 12 слотах + human×9); ОС — канон-ростер (Nix human ·
Ash human · Ana канон VERBATIM). EXP: R53–R61, код на слот.""")

# --- шапка: EXP-оверлей в парсируемом формате ---
rep(u"EXP-оверлей: 9 EXP-слотов × (кандидат R53–R61 · палитра P171–P179 по одной · X3 «В-ШЁПОТ» D2×A02 · миды K240–K248); EXP-рейтинг R+×6 · R×3.",
u"EXP-оверлей (9 EXP-слотов) × (кандидат R53–R61 · палитра P171–P179 по одной · X3 «В-ШЁПОТ» D2×A02 · миды K240–K248); EXP-рейтинг R+×6 · R×3.")

io.open(path, 'w', encoding='utf-8').write(s)
print("fixes OK")
