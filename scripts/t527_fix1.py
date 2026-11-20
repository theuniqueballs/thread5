#!/usr/bin/env python3
# T5-27 — проход фиксов по квитанции гейтов v1 (FAIL 19 → 0)
import re

P = '/home/z/my-project/thread5/batches/T5-27.md'
src = open(P, encoding='utf-8').read()

FIXES = [
# ── P01 NEG: убрать «no white streak» (neg-no-class) + exposure «off one shoulder»
("hazy, solid black hair, no white streak, patches, covered chest",
 "hazy, solid black hair, all black hair, patches, covered chest"),
("the ceremonial torn white robe hanging open past the shoulder, its rent edge crossing the sternum",
 "the ceremonial torn white robe hanging open off one shoulder, its rent edge crossing the sternum"),
# ── P03 NEG: убрать «no wings / no tail»
("soft focus, hazy, no wings, vestigial wings, small wings, no tail",
 "soft focus, hazy, vestigial wings, small wings, folded-flat wings, antler horns"),
# ── P04: claim-тедзер уникальный + formTokens + NEG-юнит
("the borrowed shirt reading her breast shape where the shoulder escaped",
 "her breast shape read honest where the borrowed shirt's shoulder escaped"),
("soft quick build, strong thighs, small round tail pressed flat to the wall, mid_freezeturn,",
 "soft quick build, strong thighs, small round tail pressed flat to the wall, freckles across the nose bridge, a little bell on the collar's tag, mid_freezeturn,"),
("hazy, ears upright, shirt on both shoulders, second figure",
 "hazy, ears upright, shirt buttoned, both shoulders covered"),
# ── P05: hair legal-стем + formTokens + Corridor A+B
("ink-green hair slicked to a glass sheen with a center part, amber vertical-slit eyes counting the frame, pale scales rising from wrist to elbow — the new skin ahead of the old,",
 "ink-green hair slicked to a glass sheen with a center part, one ear stud at the lobe, amber vertical-slit eyes counting the frame, pale scales rising from wrist to elbow — the new skin ahead of the old,"),
("mid-molt-freeze (☠; замирание в полулиньке: подол остановлен под скрещенными предплечьями, старая кожа уже не нужна — прикрытие скрещенными руками и подолом, не выше)\nCorridor: A",
 "mid-molt-freeze (☠; замирание в полулиньке: подол остановлен под скрещенными предплечьями, старая кожа уже не нужна — прикрытие скрещенными руками и подолом, не выше)\nCorridor: A+B"),
("long limber body, narrow waist, a shed skin-sleeve clinging at one shoulder holding the shape of the last step, mid_moltfreeze,",
 "long limber body, narrow waist, a shed skin-sleeve clinging at one shoulder holding the shape of the last step, a bone hairpin through the slick bun, mid_moltfreeze,"),
# ── P06: hair-стем (cream+curls) + claim-тедзер + formTokens
("ash-cream cloud of wool curls flung wide in the arc, small curled ram horns holding the arc's frame, honey-brown eyes shut mid-shake, rosy wind-flushed skin,",
 "cream wool curls flung wide in the arc, sun freckles at the shoulders, small curled ram horns holding the arc's frame, honey-brown eyes shut mid-shake, rosy wind-flushed skin,"),
("the towel-wrap's tuck reading her breast shape where the shake swings it",
 "her breast shape read at the swung towel-wrap's tuck mid-arc"),
# ── P07: cover_a (palms flat) + formTokens
("the sheer nightgown pressed flat to the glass by the palm's spread, its lace trim going clear with the fog, nothing deciding anything but the condensation — the vitrine is the claim, preserve-made,",
 "the sheer nightgown pressed to the glass, both palms flat against the pane, its lace trim going clear with the fog — the vitrine is the claim, preserve-made,"),
("slender willowy build, long level shoulder line, pointed ears pressed to the pane too — listening through it, mid_vitrinewatch,",
 "slender willowy build, long level shoulder line, a necklace of small brass keys at the collarbone, pointed ears pressed to the pane too — listening through it, mid_vitrinewatch,"),
("garden fog condensing in a ring at her breath, the brass name-plate at the frame's corner turned face-down by her own hand,",
 "garden fog condensing in a ring at her breath, the brass name-plate at the frame's corner turned face-down by her own hand, a keyring hung at the vitrine's latch,"),
# ── P08: hair-стем + wine-plum hair
("wine-plum steam-curled ringlets falling past the horns, gold eyes level from under the raised arm, dusk-rose skin with a heart-line birthmark at the collarbone,",
 "wine-plum hair in steam-curled ringlets falling past the horns, gold eyes level from under the raised arm, dusk-rose skin with a heart-line birthmark at the collarbone,"),
# ── P09: formTokens
("ink-black hair in a wet slick low bun with one stray drip, void-grey eyes reading the horizon through the water, ink-blue skin going glassy at the wrists,",
 "ink-black hair in a wet slick low bun with one stray drip, one ear cuff at the lobe, void-grey eyes reading the horizon through the water, ink-blue skin going glassy at the wrists,"),
("liquid-soft build, the body's edges calm where the ink holds its shape, mid_waterwatch,",
 "liquid-soft build, the body's edges calm where the ink holds its shape, a ring at the thumb holding the column's base, mid_waterwatch,"),
# ── P10: hair-стем + claim-тедзер + cover/exposure + formToken
("charcoal-brown choppy lob with a deep side part, masked bandit eyes bright amber behind the squint, warm dusk skin, round ears tucked into the lob,",
 "charcoal-brown hair in a choppy lob, deep side part, masked bandit eyes bright amber behind the squint, warm dusk skin, round ears tucked into the lob,"),
("the open shirtfront reading her breast shape under the bank's ceramic weight",
 "her breast shape read beneath the open shirtfront's ceramic weight"),
("the tie-front blouse knotted under the bank's line, its gap crossing the sternum where the ceramic balances, one button's thread holding the whole audit — the hoard is the claim, cache-made,",
 "the tie-front blouse knotted under the bank's line, its hem tucked by the ceramic's weight, the fabric gathering where the gap crosses the sternum, one button's thread holding the whole audit — the hoard is the claim, cache-made,"),
("compact sturdy build, ringed tail hooked on the stool leg like an anchor, mid_hoardtilt,",
 "compact sturdy build, ringed tail hooked on the stool leg like an anchor, a coin-string brooch shaped like a pig's snout at the collar, mid_hoardtilt,"),
# ── P11: lamp-флор + formToken
("the room's one lamp-glow of moon ranked behind her like a jury that gave up",
 "the room's one moon-glow ranked behind her like a jury that gave up"),
("raven-black hair loose from the shoulders down, pale violet eyes — the body's pair looking down, the head's pair looking up from her lap, mist-grey skin with a warm seam-line at the neck,",
 "raven-black hair loose from the shoulders down, one earring on the head's ear while the body's ear stays bare, pale violet eyes — the body's pair looking down, the head's pair looking up from her lap, mist-grey skin with a warm seam-line at the neck,"),
# ── P13: formTokens
("clay-brown hair pinned up with two iron hair-sticks, kiln-amber eyes level with the checklist, terracotta skin with seams of warm glow at elbow and hip,",
 "clay-brown hair pinned up with two iron hair-sticks, a signal whistle on a cord at the neck, kiln-amber eyes level with the checklist, terracotta skin with seams of warm glow at elbow and hip,"),
# ── P15: formToken
("soft rounded build, velvet-laid quills down the back and none of them bristling, mid_softsettle,",
 "soft rounded build, a bandage at one palm from the last soft landing, velvet-laid quills down the back and none of them bristling, mid_softsettle,"),
# ── P16: formTokens
("ginger-cream hair one-side-tucked behind a cat ear, green-gold eyes half-lidded and amused at the lens, peach-warm skin with a sun patch at the throat,",
 "ginger-cream hair one-side-tucked behind a cat ear, a little bell on a frayed collar, green-gold eyes half-lidded and amused at the lens, peach-warm skin with a sun patch at the throat, a mole under one eye,"),
# ── P18: hair-стем + lamp-флор + exposure_r (hem drifting)
("sea-salt blonde in mermaid waves half-undone by the gust, slate-blue eyes squinted into the weather, wind-reddened fair skin,",
 "sandy blonde hair in mermaid waves half-undone by the gust, slate-blue eyes squinted into the weather, wind-reddened fair skin,"),
("the trench's belt cinched but the lapel wind-dragged open off one shoulder line, the legging's rain-dark calf telling where the spray reaches, the trench's hem pressed flat against her by the gust — the live scarf is the claim, beacon-made,",
 "the trench's belt cinched but the lapel wind-dragged open off one shoulder line, the legging's rain-dark calf telling where the spray reaches, the trench's hem drifting flat against her front where the gust wins — the live scarf is the claim, beacon-made,"),
("the beacon's lamp-room ranked dark behind — her shift lives in the scarf now",
 "the beacon's light-room ranked dark behind — her shift lives in the scarf now"),
# ── P19: hair-стем + claim-тедзер без «reading her breast shape under»
("oak-brown hat-flattened waves bedhead-soft, doe-amber eyes on the slot's warm dark, hay-dusted freckled skin,",
 "caramel-brown hair in hat-flattened waves, bedhead-soft, doe-amber eyes on the slot's warm dark, hay-dusted freckled skin,"),
# ── P20: hair-стем + formTokens
("wheat-blonde wind-lifted open curtain hair, sky-clear grey eyes holding both horizons at once, sun-and-shade freckled skin,",
 "wheat-blonde hair wind-lifted open like a curtain, a whistle on a cord at her neck, sky-clear grey eyes holding both horizons at once, sun-and-shade freckled skin,"),
("easy outdoors build, the calves bare on the rail's worn wood, mid_borderkeep,",
 "easy outdoors build, a charm bracelet of grass seeds at one wrist, the calves bare on the rail's worn wood, mid_borderkeep,"),
# ── P21: (passed char-spec) — без правок
# ── P22: hair-стем + formTokens
("dark-chestnut french twist screwed high, steady amber eyes holding the viewer's whole attention on purpose, stage-warm skin,",
 "wine-dark hair in a french twist screwed high, a velvet choker at the offered throat, steady amber eyes holding the viewer's whole attention on purpose, stage-warm skin, a beauty mark above the collarbone,"),
# ── P23: hair-стем + formTokens
("sun-bleached chestnut in a volume blowout gone soft with humidity, warm hazel eyes squeezed half-shut, heat-flushed tan skin,",
 "honey-brown hair in a volume blowout gone soft with humidity, damp beads in hair at the temple, warm hazel eyes squeezed half-shut, heat-flushed tan skin with sun freckles,"),
# ── P24: lamp-флор + formTokens
("night-black hair in a star-pinned updo, reading-lamp amber eyes moving line to line, paper-pale calm skin,",
 "night-black hair in a star-pinned updo, thin-frame glasses parked in the collar, a pendant watch ticking at the sternum, ledger-amber eyes moving line to line, paper-pale calm skin,"),
# ── P25: hair-стем + eye-стем + formTokens
("overlapping bronze-grey scale plates fanned down her spine and meeting at the nape — armor that remembers every curl, warm earth-brown skin between the plates,",
 "terracotta hair in an ear-slot cut, overlapping bronze-grey scale plates fanned down her spine and meeting at the nape — armor that remembers every curl, a stitched patch at the wrap's shoulder, warm earth-brown skin between the plates,"),
("stylized 2D anime face patient with sleep, anime eyes (copper, unhurried),",
 "stylized 2D anime face patient with sleep, anime eyes (ember, unhurried),"),
("the burrow wall's root-mattress holding her shape's print, the wrap's shibori stitch-marks pale where the dye was refused,",
 "the burrow wall's root-mattress holding her shape's print, a bone brooch at the wrap's clasp, the wrap's shibori stitch-marks pale where the dye was refused,"),
# ── P26: hair/eye-стемы + skin + cover (fabric gathering) + claim-тедзер + formTokens
("dust-grey cloud of natural curls standing in an aura around the shoulders, soft fur-fog along the arms, big violet dust-dark eyes half-lidded in bliss,",
 "grey dust-cloud curls standing in an aura around the shoulders, soft fur-fog along the arms, big lilac dust-dark eyes half-lidded in bliss,"),
("plush rounded build, the fur holding its cloud-shape even pressed, long whiskers at the cheeks reading the dust's grain, mid_dustwallow,",
 "plush rounded build, warm fair skin, a bracelet of wooden beads, the fur holding its cloud-shape even pressed, long whiskers at the cheeks reading the dust's grain, mid_dustwallow,"),
("the mended vest reading her breast shape under the pinning palm",
 "her breast shape read flat beneath the pinning palm's vest"),
("the mended vest pinned flat to the ribs by one palm, its gold seam running the left panel like a healed lightning, nothing under the knit but the softest maintenance schedule — the dust bloom is the claim, groom-made,",
 "the mended vest pinned flat to the ribs by one palm, its fabric gathering at the gold seam that runs the left panel like a healed lightning — the dust bloom is the claim, groom-made,"),
# ── P27: hair/skin/eye + cover (sleeve caught) + exposure (slipping) + formTokens + NEG-юнит
("winter-white fur giving way to summer-brown along a seam that crosses the collarbone exactly — two seasons worn at once, snow-pale and earth-brown,",
 "platinum hair in a loose sleeping braid, winter-white fur giving way to summer-brown along a seam that crosses the collarbone exactly — two seasons worn at once, rosy fair skin beneath both,"),
("stylized 2D anime face proud at the seam, anime eyes (amber, season-counting),",
 "stylized 2D anime face proud at the seam, anime eyes (hazel, season-counting),"),
("the duster's front panel swung across the chest line by the stretch, one arm free and the other sleeve hanging, the tank's collar reading both furs' colors at the seam — the season's seam is the claim, molt-made,",
 "the duster's front panel swung across the chest line by the stretch, its sleeve caught at the crooked elbow while the winter side slips off the freed arm — the season's seam is the claim, molt-made,"),
("hazy, coat on both arms, tail white, seam crooked",
 "hazy, coat shouldered, tail white, seam crooked"),
("a charred cedar plank propped at the door holding the household's scorch-memory, the shed winter fluff gathered into a nest-shaped ball,",
 "a charred cedar plank propped at the door holding the household's scorch-memory, a trophy cord at the wrist, the shed winter fluff gathered into a nest-shaped ball,"),
# ── P28: hair/eye-стемы + skin + exposure (hem) + formTokens
("ink-black hime-cut bangs with one white streak at the brow, black-and-white wing-panels flared with a petrol-blue sheen, sharp amber eyes on the verdict,",
 "jet-black hime-cut bangs with one white streak at the brow, one brass ear cuff at the lobe, black-and-white wing-panels flared with a petrol-blue sheen, garnet-sharp eyes on the verdict,"),
("small bright build, the chessboard tail longer than she is and ruling the balance, mid_shinyoffer,",
 "small bright build, fair lively skin, the chessboard tail longer than she is and ruling the balance, mid_shinyoffer,"),
("the off-shoulder top's line straight across the collarbones, both palms holding the find at the chest's height, the tulle tiers ranked under the crouch — the offered shine is the claim, gift-made,",
 "the off-shoulder top's line straight across the collarbones, both palms holding the find at the chest's height, the tulle skirt's hem ranked in tiers under the crouch — the offered shine is the claim, gift-made,"),
("the hoard ranked by shine behind the rim — buttons, beads, one watch-face — the find's copper catching flat planes of light,",
 "the hoard ranked by shine behind the rim — buttons, beads, one watch-face — a price-tag cord knotted on the find, its copper catching flat planes of light,"),
# ── P29: hair-стем + skin + cover (fabric gathering) + exposure (hem tucked) + formTokens
("silver-tawny hair nape-tucked with two clips, tall tufted lynx ears — one forward, one swiveled back into the wind, glacier-green eyes level and saving their attention,",
 "steel-tawny hair nape-tucked with two clips, tall tufted lynx ears — one forward, one swiveled back into the wind, glacier-green eyes level and saving their attention,"),
("athletic low build, the haunches high in the crouch, ruff-sideburns flaring at the cheeks, mid_lowlisten,",
 "athletic low build, wind-rough fair skin, a whistle on a thong tucked into the wrap, the haunches high in the crouch, ruff-sideburns flaring at the cheeks, mid_lowlisten,"),
("the knit wrap's fold crossing the chest line flat, the tank beneath it breathing with her stillness, nothing moving that the wind doesn't move first — the turned ear is the claim, listen-made,",
 "the knit wrap's fold crossing the chest line flat, its fabric gathering at the fold, the wrap's hem tucked at the crouch's bend, nothing moving that the wind doesn't move first — the turned ear is the claim, listen-made,"),
# ── P30: eye-стем + cover (elbow fold)
("stylized 2D anime face mid-slow-tilt, anime eyes (triangular amber, depth-reading),",
 "stylized 2D anime face mid-slow-tilt, anime eyes (triangular ember, depth-reading),"),
("the tie-front blouse's knot seated under the folded arms, the pencil skirt's line unmoved for a full minute,",
 "the tie-front blouse's knot seated under the forelegs' elbow fold, a copper comb in hair above one antenna, the pencil skirt's line unmoved for a full minute,"),
("jade-green glass-sleek hair with a center part, triangular ember eyes reading depth not width, leaf-pale green skin with a fine jointed seam at the neck,",
 "jade-green glass-sleek hair with a center part, a talisman of dry grass at the neck, triangular ember eyes reading depth not width, leaf-pale green skin with a fine jointed seam at the neck,"),
# ── P31: hair/eye-стемы + cover (fabric gathering) + exposure (sheer)
("rose-pink steam-curled ringlets going damp at the ends, six frilled gill-petals fanning at the neck in breathing rhythm, dark kind eyes with a gold ring,",
 "strawberry-pink hair in steam-curled ringlets going damp at the ends, six frilled gill-petals fanning at the neck in breathing rhythm, dark eyes with a garnet ring,"),
("the tankini top riding the waterline's crossing, one palm flat on the submerged sill, the new hand's fingers learning their numbers — the new hand is the claim, regrow-made,",
 "the tankini's fabric gathering at the waterline's sheer crossing, one palm flat on the submerged sill, the new hand's fingers learning their numbers — the new hand is the claim, regrow-made,"),
# ── P32: hair/eye-стемы + skin + cover (waistband) + formTokens
("silver-white glass-sleek hair with a center part already tarnishing warm at the lines, gold bell-round eyes with the pupil's good luck, cream-and-ginger patches at ear and cheek,",
 "pearl-white glass-sleek hair with a center part already tarnishing warm at the lines, honey bell-round eyes with the pupil's good luck, cream-and-ginger patches at ear and cheek on warm fair skin,"),
("the cheongsam-cut dress's frog buttons strained one degree honest over the chest, the coin held flat at the chest line in the warming palm, the sash's knot doing structural work — the beckon is the claim, luck-made,",
 "the cheongsam-cut dress's frog buttons strained one degree honest over the chest, the fabric gathering at each button's pull, the coin held flat at the chest line in the warming palm, the sash's waistband doing structural work — the beckon is the claim, luck-made,"),
("the sill's wood silvered by decades of this exact pose, a red collar-bell silent until the luck lands,",
 "the sill's wood silvered by decades of this exact pose, a little bell on the red collar silent until the luck lands, a coin string at the wrist,"),
# ── P33: hair/eye-стемы + skin + cover (hands covering) + formTokens + claim-тедзер
("moon-white hair in a star-pinned updo, wraith-grey eyes already at the horizon they'll warn, silver dust at the lashes — the last note's receipt,",
 "pearl-white hair in a star-pinned updo, a necklace of hawthorn beads, moonstone-grey eyes already at the horizon they'll warn, silver dust at the lashes — the last note's receipt,"),
("willowy weightless build, the three veil layers going sheer one by one toward the face, both hands folded at the sternum like a closed gate, mid_noteintake,",
 "willowy weightless build, moonlit pale skin, the three veil layers going sheer one by one toward the face, both hands folded at the sternum like a closed gate, a talisman stitched into the veil's hem, mid_noteintake,"),
("the veil dress's sheer layer reading her breast shape through the fold",
 "the veil dress's sheer layer reading her breast shape inside the fold"),
("the veil dress's front layer lifting with the intake, both hands folded over the chest line's rise, the sheer going honest at the breath's apex — the intake is the claim, herald-made,",
 "the veil dress's front layer lifting with the intake, both hands covering the chest line's rise, the sheer going honest at the breath's apex — the intake is the claim, herald-made,"),
]

missed = []
for old, new in FIXES:
    if old in src:
        src = src.replace(old, new, 1)
    else:
        missed.append(old[:60])

# L2: убрать «, 1girl, solo,» из строк-паттернов (format >200) — L1 уже несёт 1girl, solo
src = re.sub(r'\b, 1girl, solo,\n', '\n', src)

open(P, 'w', encoding='utf-8').write(src)
print('fixes applied:', len(FIXES) - len(missed), '/', len(FIXES))
if missed:
    print('MISSED:')
    for m in missed: print('  !', m)
