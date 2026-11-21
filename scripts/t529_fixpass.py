#!/usr/bin/env python3
"""T5-29 fix-pass: claim-лексемы, char-spec цвета, cover-токены, details-фишечки,
приборные слова, камерные кластеры (дедуп 6-грамм), NEG ≤4 гардов, длина строк."""
import re
from pathlib import Path

P = Path('/home/z/my-project/scripts/t529_build.py')
t = P.read_text(encoding='utf-8')

R = [
# ── P01 Sol ──
('"upper body close at eye level, the night-shawl slipping off both shoulders"',
 '"eye-level close, upper body, the night-shawl slipping off both shoulders"'),
('"long silver-white thick layered hair, messy side bangs partially covering one eye, bright amber slit pupils, dark bronze skin"',
 '"long silver-white thick layered hair, messy side bangs partially covering one eye, bright amber eyes with slit pupils, dark bronze skin"'),
('"the night-shawl half-off both shoulders, straps caught at the elbow folds, the aurora\'s first light arriving on her collarbones — the shift itself is the claim, dawn-made,"',
 '"the night-shawl half-off both shoulders, straps caught at the elbow folds, the silk reading her breast shape where it still holds — the shift itself is the claim, dawn-made,"'),
('" ears perked, upright ears, tail, fox tail, human ears, shawl gone, straps loose, aurora flat, bangs tidy"',
 '" ears perked, tail, shawl gone, aurora flat"'),
('"the corridor\'s old torch brackets long cold and holding only moss"',
 '"the corridor\'s old bracket nails long cold and holding only moss"'),
# ── P02 Noir ──
('"upper body close at eye level, palms pressed flat over the corset\'s laced front"',
 '"upper body at eye level, close on the laced front, palms pressed flat"'),
('"the black corset laced to the last pair of grommets, ribbon hauled taut through the lacing, palms pressed flat over the laced gap — the open knot is the claim, verdict-made,"',
 '"the black corset laced to the last pair of grommets, ribbon hauled taut, the lacing reading her breast shape held honest, palms pressed flat over the laced gap — the open knot is the claim, verdict-made,"'),
('" halo held in hands, golden halo, blonde hair, thick bangs, blush, open smile, knot tied, corset slack, ribbon cut, corona flicker"',
 '" halo held in hands, golden halo, knot tied, corset slack"'),
# ── P03 Hana ──
('"the tar sheet holding her chest line where it took her shape, weight pooling honest at the elbows, the glossy black falling past her hips in one slow drip — the kept shape is the claim, contract-made,"',
 '"the tar sheet holding her breast shape where it took it, weight pooling honest at the elbows, the glossy black falling past her hips in one slow drip — the kept shape is the claim, contract-made,"'),
('" horns gone, tail whole unchipped, wings large, gown closed, ledger blank, tar dripping off, shape lost, pupils round"',
 '" horns gone, tail whole unchipped, wings large, ledger blank"'),
# ── P04 ──
('"the towel hauled flat against the chest by both fists, the wet hem\'s drag still pulling down, nothing underneath the terry but the wave\'s own temperature — the caught wave is the claim, calibration-made,"',
 '"the towel hauled flat against the chest by both fists, the terry reading her breast shape under the haul, the wet hem\'s drag still pulling down, nothing underneath the terry but the wave\'s own temperature — the caught wave is the claim, calibration-made,"'),
('"a waterlogged test journal in one fist\'s grip,"',
 '"a waterlogged test journal in one fist\'s grip, a brass whistle on a lanyard at her wrist, one diver\'s ring on her thumb,"'),
('" wetsuit on both shoulders, towel dropped, journal dry, wave receded, gauge still"',
 '" wetsuit on both shoulders, towel dropped, journal dry, gauge still"'),
# ── P05 ──
('"the backless dress\'s collar opening by the lean, fabric bridges taut across the ribs, nothing underneath the sequins\' fall but the hall she just accepted — the accepted hall is the claim, inheritance-made,"',
 '"the backless dress\'s collar opening by the lean, fabric bridges taut across the ribs, the sequins reading her breast shape by the bridge, nothing underneath the sequins\' fall but the hall she just accepted — the accepted hall is the claim, inheritance-made,"'),
('"the sequins running coin-showers down the open back\'s field, lace elbow gloves to the crease, the black tail-tip tapping its verdict on the armrest\'s gold,"',
 '"the sequins running coin-showers down the open back\'s field, lace elbow gloves to the crease, a black jet hairpin through the ponytail, the black tail-tip tapping its verdict on the armrest\'s gold,"'),
('" tail white-tipped, gloves gone, dress buttoned, lean forward, hall dark"',
 '" tail white-tipped, dress buttoned, lean forward, hall dark"'),
# ── P06 ──
('"upper body close at eye level toward the lens, shawl hauled taut across the chest by both fists"',
 '"close at eye level toward the lens, upper body, shawl hauled taut by both fists"'),
('"the wool shawl hauled taut across the chest by both fists, the cold\'s goosebumps honest along the collarbones, nothing underneath the shawl\'s line but the warden\'s own winter — the opened cold is the claim, warden-made,"',
 '"the wool shawl hauled taut across the chest by both fists, her breast shape read taut under the haul, the cold\'s goosebumps honest along the collarbones, nothing underneath the shawl\'s line but the warden\'s own winter — the opened cold is the claim, warden-made,"'),
('"a velvet choker at the throat, a small gold bell collar ringing with each shiver"',
 '"a thin velvet choker, neck accent, a small gold bell collar ringing with each shiver"'),
('" shawl dropped, fists loose, gate closed, goosebumps absent, bell silent"',
 '" shawl dropped, gate closed, goosebumps absent, bell silent"'),
# ── P07 ──
('"upper body close at eye level, bow toward the lens, silk sliding off both shoulders"',
 '"upper body close, eye-level bow to the lens, silk sliding off both shoulders"'),
('"the cape\'s silk pooling in the elbow folds honest, the tulle\'s tiers holding the bow\'s angle, nothing underneath the sliding silk but the encore she owes — the held note is the claim, encore-made,"',
 '"the cape\'s silk pooling in the elbow folds honest, the tulle\'s tiers reading her breast shape through their haze, nothing underneath the sliding silk but the encore she owes — the held note is the claim, encore-made,"'),
('"the cape\'s clasp swinging open at the collarbone, loose suspenders riding the tulle\'s fall, the tear-trails holding their permanent silver glint, every glass pane of the hall intact and listening,"',
 '"the cape\'s clasp swinging open at the collarbone, a ribbon-tied choker at the throat, small silver ear studs, loose suspenders riding the tulle\'s fall, the tear-trails holding their permanent silver glint, every glass pane of the hall intact and listening,"'),
('" laugh open, glass cracked, cape clasped, suspenders gone, tear-trails absent"',
 '" glass cracked, cape clasped, laugh open, tear-trails absent"'),
# ── P08 ──
('"the veil dress\'s sheer layers lying flat as inventory cloth, both hands crossed over the chest holding the sprig, nothing underneath the registers\' linen but the certification itself — the certified shelf is the claim, registry-made,"',
 '"the veil dress\'s sheer layers lying flat as inventory cloth, both hands crossed over the chest holding the sprig, her breast shape reading soft under the crossed hands, nothing underneath the registers\' linen but the certification itself — the certified shelf is the claim, registry-made,"'),
('" sitting up, sprig gone, shelves empty, hands apart, kimono belted tight"',
 '" sitting up, sprig gone, shelves empty, kimono belted"'),
# ── P09 ──
('"the halter\'s bare back field facing the door draft, one knee on the seat beside the viewer, weight on the planted palm, nothing underneath the house\'s welcome but the bet itself — the first bet is the claim, house-made,"',
 '"the halter\'s bare back field facing the door draft, the halter reading her breast shape at the lean\'s angle, one knee on the seat beside the viewer, weight on the planted palm, nothing underneath the house\'s welcome but the bet itself — the first bet is the claim, house-made,"'),
('"the raised right paw held up in the greeting, a velvet choker at the throat, the coin mark\'s slot glinting at the collarbone, the halter\'s knot riding between the shoulder blades,"',
 '"the raised right paw held up in the greeting, a velvet choker, collarbone shadow, the coin mark\'s slot glinting, the toll\'s coin string coiled at the counter\'s edge, the halter\'s knot riding between the shoulder blades,"'),
('" paw down, coin mark absent, ears plain, whisper finished, ledger closed"',
 '" paw down, coin mark absent, whisper finished, ledger closed"'),
# ── P10 ──
('"the open robe\'s front reading her chest line through the pinafore\'s bib, the silk\'s belt hanging unused, nothing underneath the audit but the winnings — the won day is the claim, audit-made,"',
 '"the open robe\'s front reading her breast shape through the pinafore\'s bib, the ledger\'s weight hugged to the chest in the free arm\'s crook, the silk\'s belt hanging unused, nothing underneath the audit but the winnings — the won day is the claim, audit-made,"'),
('"the pinafore\'s straps crossing the bare shoulders above the bib, a tiny inner-wrist tattoo under the ledger line, black feathers flashing iridescent at the half-turn, a palm of counted coins going cold beside the book,"',
 '"the pinafore\'s straps crossing the bare shoulders above the bib, a tiny inner-wrist tattoo under the ledger line, a brooch of one bright theft pinned to the bib, black feathers flashing iridescent at the half-turn, a palm of counted coins going cold beside the book,"'),
('" wings gone, pinafore front-open, coins scattered, eyes wide, belt tied"',
 '" wings gone, coins scattered, eyes wide, belt tied"'),
# ── P13 ──
('"the tufted ears already turned down toward the garden rows, the bobbed tail giving the jump its rudder beat, the grate\'s moss holding last visit\'s print,"',
 '"the tufted ears already turned down toward the garden rows, a brass signal whistle pinned to the collar, one hoop earring catching the drop, the bobbed tail giving the jump its rudder beat, the grate\'s moss holding last visit\'s print,"'),
# ── P14 ──
('"chartreuse triangular eyes in triple highlight"',
 '"green triangular eyes in triple highlight"'),
('" pin open, strap up, forearms spread, tilt shallow, scar absent"',
 '" pin open, strap up, forearms spread, tilt shallow"'),
# ── P15 ──
('"the ember core glowing steady through the linen\'s layers, hanging ribbons taking the steam\'s slow curl, the folded towels stacked in level-pairs,"',
 '"the ember core glowing steady through the linen\'s layers, a talisman stitched to the apron\'s hem, prayer beads in her hair, hanging ribbons taking the steam\'s slow curl, the folded towels stacked in level-pairs,"'),
('" core dark, steam gone, cloth dropped, ribbons flat, fold crooked"',
 '" core dark, steam gone, cloth dropped, ribbons flat"'),
# ── P16 ──
('"the overall\'s one strap unbuckled, the bib sagging sideways, the shirt\'s hem knotted above the navel, the lower belly\'s curve honest above the low waistband,"',
 '"the overall\'s one strap unbuckled, the bib sagging sideways, the shirt\'s hem knotted above the navel, the lower belly\'s curve honest above the low waistband,"'),
('"the brass wheel polished mirror-bright by her palms, the cage\'s latch open on its hook, one sock\'s cuff slouched into the boot\'s mouth,"',
 '"the brass wheel polished mirror-bright by her palms, a keyring of cage keys at her hip, a whistle on a chain round her neck, the cage\'s latch open on its hook, one sock\'s cuff slouched into the boot\'s mouth,"'),
('" both straps buckled, wheel dull, cage moving, draft still, calluses absent"',
 '" both straps buckled, wheel dull, cage moving, calluses absent"'),
# ── P17 ──
('"rose-quartz pane face, stained glass girl, translucent rose-glass body, lead-line seams in art-nouveau curves, human face in a clear pane, slender glass build"',
 '"sea-glass eyes in a clear pane face, stained glass girl, translucent rose-glass body, glass-clear skin at the face pane, lead-line seams in art-nouveau curves, slender glass build"'),
('"stylized 2D anime face in a clear pane to the ceiling, pane eyes (rose-quartz, full of the current)"',
 '"stylized 2D anime face in a clear pane to the ceiling, pane eyes (rose-lit sea-glass, full of the current)"'),
('" seams cracked, colors fixed, arch shallow, glow absent, pendants still"',
 '" seams cracked, colors fixed, arch shallow, glow absent"'),
# ── P19 ──
('"the shirt catching the wind off the noon, the fabric billowing against her side between the plates, the hem snapping the door\'s line,"',
 '"the shirt catching the wind off the noon, the noon finding her bare shoulders at every gust, the fabric billowing against her side between the plates, the hem snapping the door\'s line,"'),
('"each plate edge taking its own thin specular row in the sun, a grass blade caught above one brow, forearms braced on the doorframe,"',
 '"each plate edge taking its own thin specular row in the sun, a brooch of hammered brass at the collar, a pouch of surface seeds at the belt, a grass blade caught above one brow, forearms braced on the doorframe,"'),
('" plates dull, wind still, door closed, grass absent, sitting straight"',
 '" plates dull, wind still, door closed, sitting straight"'),
# ── P20 ──
('"the ceiling\'s aurora dimmed to reading-lamp quiet over the shelves"',
 '"the ceiling\'s aurora dimmed to reading quiet over the shelves"'),
('"the wall holding the cool print of her back, one wing-arm folded behind as a shelf for the slide, the day\'s last ledger closed on her knees,"',
 '"the wall holding the cool print of her back, small round glasses pushed up into the layers, one wing-arm folded behind as a shelf for the slide, the day\'s last ledger closed on her knees,"'),
('" disc ruffled, wings out, crouch high, wall clean, eyes shut"',
 '" disc ruffled, wings out, crouch high, eyes shut"'),
# ── P21 ──
('"the striped tail hanging down into the frame below, its tip ticking the count, rosette freckles doubled in the freezer\'s light, breath leaving in one held line of steam,"',
 '"the striped tail hanging down into the frame below, its tip ticking the count, frost-set silver earrings at the spotted ears, rosette freckles doubled in the freezer\'s light, breath leaving in one held line of steam,"'),
('" tail still, freckles absent, steam gone, lean back, slate blank"',
 '" tail still, freckles absent, steam gone, slate blank"'),
# ── P22 ──
('"the guild ledger open to the ninth wave\'s line, a brass tally counter under one thumb, the chair\'s back holding her forearms\' weight,"',
 '"the guild ledger open to the ninth wave\'s line, a keyring of wave-stamps at the ledger\'s edge, a brooch of the guild\'s brass on the collar, a brass tally counter under one thumb, the chair\'s back holding her forearms\' weight,"'),
('"the collarbones reading the ledger lamp"',
 '"the collarbones reading the ledger\'s light"'),
('" chair turned, ledger shut, counter still, eyes bright, sleeves down"',
 '" chair turned, ledger shut, counter still, sleeves down"'),
# ── P24 ──
('"the sanctum\'s candle-niches long cold and holding moss instead"',
 '"the sanctum\'s niches long cold and holding moss instead"'),
('" standing, key gone, water stirred, socks even, halo absent"',
 '" standing, key gone, water stirred, halo absent"'),
# ── P25 ──
('"upper body close at eye level, jacket sliding off one shoulder"',
 '"upper body close, eye-level at the ledge, jacket sliding off one shoulder"'),
('"the suspender skirt\'s straps riding over bare shoulders, fingerless knit gloves at the stone hands, small stone wings folding like a weathervane at rest, moss lining the ledge below in one green biography,"',
 '"the suspender skirt\'s straps riding over bare shoulders, earrings of carved granite at the stone ears, fingerless knit gloves at the stone hands, small stone wings folding like a weathervane at rest, moss lining the ledge below in one green biography,"'),
('" wings spread, jacket on both shoulders, moss absent, stone cracked, gloves gone"',
 '" wings spread, jacket on both shoulders, moss absent, stone cracked"'),
# ── P26 ──
('"pale-lilac white hair in a loose half-worked sleeping braid, moon-milk eyes half-open in the stillness"',
 '"lilac-white hair in a loose half-worked sleeping braid, moonstone-pale eyes half-open in the stillness"'),
('"the open linen shirt\'s front held only by the floating palms\' span, the fabric\'s weave worn to gauze at the panel, nothing underneath the exhibit but the dungeon\'s own holding — the held ghost is the claim, exhibit-made,"',
 '"the open linen shirt\'s front held only by the floating palms\' span, the conjured palms covering the chest line at her sides, the fabric\'s weave worn to gauze at the panel, nothing underneath the exhibit but the dungeon\'s own holding — the held ghost is the claim, exhibit-made,"'),
('"conjured palms cupping both wrists a hand-span from her sides, a small gold bell collar silent at her throat, the braid drifting a beat behind the turn,"',
 '"conjured palms cupping both wrists a hand-span from her sides, a pendant of still-warm silver at her throat, a hairpin through the braid, a small gold bell collar silent below it,"'),
('" palms gone, shirt closed, bell ringing, feet planted, edges solid"',
 '" palms gone, shirt closed, bell ringing, edges solid"'),
# ── P27 ──
('"the long glove coming off finger by finger at the wrist\'s bend, the cuff still holding the palm, the suspenders swinging loose at the ribs, nothing underneath the redress but the next room — the redressed seam is the claim, undertaker-made,"',
 '"the long glove coming off finger by finger at the wrist\'s bend, the cuff still holding the palm, the suspenders\' straps covering the chest\'s bare line between them, nothing underneath the redress but the next room — the redressed seam is the claim, undertaker-made,"'),
('" seam dark, scarf gone, glove on, suspenders hooked, eyes matched"',
 '" seam dark, glove on, eyes matched, scarf gone"'),
# ── P28 ──
('"terracotta hair in a pinned twist with wooden hair-sticks"',
 '"terracotta hair in a pinned twist with wooden hair sticks"'),
('"fresh-carved notes riding the forearm\'s plate, runes holding a lazy amber glow at the joints, the off-shoulder top\'s neckline a soft horizon across the upper arms,"',
 '"fresh-carved notes riding the forearm\'s plate, a bracelet of clay beads at the wrist, runes holding a lazy amber glow at the joints, the off-shoulder top\'s neckline a soft horizon across the upper arms,"'),
('" runes dark, arm down, hem loose, sticks gone, plates bare"',
 '" runes dark, arm down, hem loose, plates bare"'),
# ── P29 ──
('"dark-plum hair in a sectioned bubble ponytail, mulberry eyes on the stitch count"',
 '"dark-plum hair in a sectioned bubble ponytail, violet eyes on the stitch count"'),
('" arms two, eyes open, glove on, knit dropped, tea cold"',
 '" arms two, eyes open, knit dropped, tea cold"'),
# ── P30 ──
('"aqua-translucent hair slicked straight back, drift-core eyes glowing one tide behind"',
 '"translucent teal hair slicked straight back, pearl-blue eyes glowing one tide behind"'),
('"the towel caught at the shoulder line mid-dry, the rash guard\'s zipper frozen mid-descent, nothing underneath the gel but what she took in — the cleaned level is the claim, caretaker-made,"',
 '"the towel caught at the shoulder line mid-dry, the rash guard\'s zipper frozen mid-descent, her breast shape read through the gel\'s clear line, nothing underneath the gel but what she took in — the cleaned level is the claim, caretaker-made,"'),
('"wet footprints leading away from the drain\'s rectangle, the waterline cutting her hip line in two honest halves, the gold body chain floating a centimeter into her and back,"',
 '"wet footprints leading away from the drain\'s rectangle, the waterline cutting her hip line in two honest halves, a pendant floating a centimeter into the gel beside the gold body chain, one brass ring suspended at her collarbone,"'),
('" core dark, zipper up, chain out, towel down, floor dry"',
 '" core dark, zipper up, towel down, floor dry"'),
# ── P31 ──
('"a velvet choker at the throat holding the laugh, the cap growth\'s gills catching their own rim of gold,"',
 '"the velvet choker\'s line at her throat holding the laugh, the cap growth\'s gills catching their own rim of gold,"'),
('" strap caught, spores gone, cap absent, laugh open, backlight flat"',
 '" strap caught, spores gone, cap absent, laugh open"'),
# ── P32 ──
('"upper body close at eye level through clear vinyl, strap slipped off the shoulder\'s slope"',
 '"eye-level close-up through clear vinyl, upper body, strap slipped off the shoulder\'s slope"'),
('" vinyl opaque, shadow gone, strap up, sweater on, star-flecks absent"',
 '" vinyl opaque, shadow gone, strap up, star-flecks absent"'),
# ── P33 ──
('"the organza blouse\'s film of light over the torso, the pinafore\'s bib flat-lit between its straps, nothing underneath the claim but the cushion\'s slow give — the claimed heart is the claim, matriarch-made,"',
 '"the organza blouse\'s film of light over the torso, the pinafore\'s bib flat-lit between its straps, the straddle-settle\'s weight given in one slow give, nothing underneath the claim but the cushion\'s mid-settle — the claimed heart is the claim, matriarch-made,"'),
('"nine tails fanning behind her in display, each tail-tip holding its own gold rim, twin tails\' ribbons crossing the collarbones, a velvet choker with a coin at the throat,"',
 '"nine tails fanning behind her in display, each tail-tip holding its own gold rim, twin tails\' ribbons crossing the collarbones, a throne-brass hairpin through one ribbon, a velvet choker with a coin at the throat,"'),
('" tails fewer, ears plain, blouse opaque, cushion firm, palms elsewhere"',
 '" tails fewer, ears plain, blouse opaque, cushion firm"'),
# ── P12 (keyring) ──
('"star-shaped fingertip pads flat on the brake\'s brass, the tank\'s straps honest and narrow, the cart\'s latch catching with a jolt up one arm,"',
 '"star-shaped fingertip pads flat on the brake\'s brass, a keyring of passage keys hooked to the cart\'s rail, the tank\'s straps honest and narrow, the cart\'s latch catching with a jolt up one arm,"'),
('" pads gloved, eyes wide open, skirt still, shorts loose, tunnel dark"',
 '" pads gloved, eyes wide open, skirt still, tunnel dark"'),
# ── волна 13: переименование SPORE_LANTERN → SPORE_GLOW ──
('P264_SPORE_LANTERN', 'P264_SPORE_GLOW'),
('"Spore Lantern"', '"Spore Glow"'),
]

missed = []
for old, new in R:
    if old in t:
        t = t.replace(old, new, 1)
    else:
        missed.append(old[:70])

P.write_text(t, encoding='utf-8')
print(f"применено {len(R) - len(missed)}/{len(R)} замен")
for m in missed:
    print("  MISS:", m)
