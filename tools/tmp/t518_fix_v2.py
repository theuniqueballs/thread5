#!/usr/bin/env python3
# T5-18 fix v2: claim-lexemes, unique framings, stem colors, race conversions, headers, NEG trim
import io, re, sys

P = 'batches/T5-18.md'
S = 'batches/T5-18/stories.md'

def load(f):
    with io.open(f, 'r', encoding='utf-8') as fh: return fh.read()

def save(f, t):
    with io.open(f, 'w', encoding='utf-8') as fh: fh.write(t)

t = load(P)
fails = []

def rep(old, new, label):
    global t
    if old in t:
        t = t.replace(old, new, 1)
    else:
        fails.append('MISS: ' + label)

# ── A. device word P01
rep("lacquer-lantern-red accent at the pot's glaze", "lacquer-seal-red accent at the pot's glaze", 'P01 lantern')

# ── B. claim lexemes (R+ mains)
rep("the stretched buttonholes printing honest ovals over the fullest line where the backward arch pulls the weave taut — the placket's gap is the claim, worn and unposed",
    "the stretched buttonholes printing honest ovals where the backward arch pulls the weave taut, nipples a soft twin-print through the gaps — the placket's confession is the claim, worn and unposed", 'P01 claim')
rep("the undershirt printing honest where the climb is wettest, the claim standing in the cloth itself",
    "the undershirt printing honest where the climb is wettest, nipples a dark twin-line under the gauze — the claim standing in the cloth itself", 'P03 claim')
rep("one playing card tucked edge-out at the collar's gap — the tucked card is the claim, king-side out",
    "one playing card tucked edge-out at the collar's gap, shading the top of her bare chest — the tucked card is the claim, king-side out", 'P05 claim')
rep("the dress caught in the door's shut and pulled taut across the hip line, the cup-edge ridge of her collarbone reading where the cloak slid — the caught dress is the claim, the door holding it hostage",
    "the dress caught in the door's shut and pulled taut across the hip line, the thigh-slit yawning one honest inch of black lace panties — the caught dress is the claim, the door holding it hostage", 'P07 claim')
rep("the petticoat's white hem doing its half of the lifted reveal where the updraft takes it, the inner-thigh band honest at the stride's widest — the flying hem is the claim, gravity's new address",
    "the petticoat's white hem doing its half of the lifted reveal where the updraft takes it, the boyshorts' waistband honest beneath the flying tiers — the flying hem is the claim, gravity's new address", 'P09 claim')
rep("the neckline sliding honest off one shoulder as she kneels, the negligee's hem two inches below the robe's own line — the slipped seam is the verdict's first clause, delivered before the kiss",
    "the neckline sliding honest off one shoulder to the bare chest's slope as she kneels, the negligee's hem two inches below the robe's own line — the slipped seam is the verdict's first clause, delivered before the kiss", 'P13 claim')
rep("the wrap's edge letting the lace's line read where the hem lifts, the back dimples' pair showing above the dropped waist at the balance — the lifting hem is the honest weight, measured live",
    "the silk lingerie's line honest at the lift where the hem rises, the back dimples' pair showing above the dropped waist at the balance — the lifting hem is the honest weight, measured live", 'P15 claim')
rep("the old cotton washed to gauze-thin softness printing the cold's verdict through, the swimsuit's thin padding defeated by the downpour's arithmetic — the soaked sheer is the claim, rain-served",
    "the old cotton washed to gauze-thin softness printing the cold's verdict through, nipples a tea-warm press under the soaked lace — the soaked sheer is the claim, rain-served", 'P17 claim')
rep("the collar riding down her arm where the window's stretch takes it, the two straps crossed at the shoulder in an X of loyalties — the reach's pull is the claim, written in cloth tension",
    "the collar riding down her arm where the window's stretch takes it, the knot pulling the neckline low over the bare chest line — the reach's pull is the claim, written in cloth tension", 'P19 claim')
rep("the three layers' confession at the hem where slip and petticoat line up, the hem gathered and handed upward like a piece from hand to hand — the rising wave is the claim, one stitch at a time",
    "the three layers' confession at the hem where slip and petticoat line up, cotton panties flashing one honest beat at the wave's crest — the rising wave is the claim, one stitch at a time", 'P21 claim')
rep("the shrug of embarrassment letting the collar drop off one shoulder, the cutout tank's engineered point honest beneath — the dropped collar is her rebuttal to the quote, submitted live",
    "the shrug of embarrassment letting the collar drop off one shoulder to the bare chest's edge, the cutout tank's engineered point honest beneath — the dropped collar is her rebuttal to the quote, submitted live", 'P22 claim')
rep("the morning lean opening the neckline one honest inch — the spout's backlight draws the coverage border on the cloth, honest and ruled",
    "the morning lean opening the neckline over the bare chest's curve — the spout's backlight draws the coverage border on the cloth, honest and ruled", 'P23 claim')
rep("the hem arrested at the hip line neither falling nor flying, the inner-thigh band honest at the step's widest split — the standing hem is the claim, altitude's own tailor",
    "the hem arrested at the hip line neither falling nor flying, cotton panties' white waistband flashing one honest beat at the split — the standing hem is the claim, altitude's own tailor", 'P24 claim')
# EXP R+
rep("the buttonholes stretched into ovals over the fullest line by the lean, one strap tugged loose by her own thumb — the stretched buttonholes are the claim, lean-made",
    "the buttonholes stretched into ovals by the lean, one strap tugged loose by her own thumb, nipples a soft press through the bralette's honest seams — the stretched buttonholes are the claim, lean-made", 'P25 claim')
rep("the spiral pulled taut across the chest by the lean itself, the old tee washed to gauze-thin at the collar where the cream fur line shows, the apron's cross-straps leaving her back bare behind — the taut spiral is the claim, lean-earned",
    "the wrap printing her breast shape honest through the spiral as the lean pulls it taut, the old tee washed to gauze-thin at the collar where the cream fur line shows — the taut spiral is the claim, lean-earned", 'P27 claim')
rep("the shoulder seam giving one thread's worth where the doorframe squeeze takes her, the lace elbow gloves' pattern on the jamb above — the squeezing doorframe is the frame's own embrace",
    "the shoulder seam giving one thread's worth where the doorframe squeeze takes her, the veil's top layer sliding so covered nipples sit one layer deep — the squeeze is the frame's own embrace", 'P28 claim')
rep("one overall strap unbuckled so the bib sags sideways, the counter's lip pressed honest into the underboob line at the lean — the sagging bib is the claim, work-worn and shameless",
    "one overall strap unbuckled so the bib sags sideways off the bare chest's side-line at the lean, the counter's lip pressing the soft undercurve honest — the sagging bib is the claim, work-worn and shameless", 'P31 claim')
rep("the beam-press of the rail flattening honest across the chest's soft weight — the slack lacing is the claim, fence-earned",
    "the beam-press of the rail flattening honest across the chest's soft weight, breast shape reading through the thin cotton — the slack lacing is the claim, fence-earned", 'P33 claim')

# ── C. unique framings (mains)
rep("Masterpiece, best quality, side profile at chest height, 1girl, solo, honey-blonde hair in a loose sleeping braid",
    "Masterpiece, best quality, profile from the ribs up, facing left, 1girl, solo, honey-blonde hair in a loose sleeping braid", 'P01 framing')
rep("Masterpiece, best quality, side profile at chest height, 1girl, solo, jet-black hair with a side shave and a long sweep-over",
    "Masterpiece, best quality, profile view from the waist up, 1girl, solo, jet-black hair with a side shave and a long sweep-over", 'P05 framing')
rep("Masterpiece, best quality, side profile at chest height, 1girl, solo, black hair in a low loose ponytail",
    "Masterpiece, best quality, waist-up profile, faced left, 1girl, solo, black hair in a low loose ponytail", 'P10 framing')
rep("Masterpiece, best quality, side profile at chest height, 1girl, solo, moss-green hair in twin braids",
    "Masterpiece, best quality, profile to the sternum, right side on, 1girl, solo, moss-green hair in twin braids", 'P18 framing')
rep("Masterpiece, best quality, side profile at chest height, 1girl, solo, strawberry-blonde hair half-up",
    "Masterpiece, best quality, side-on view from hips to crown, 1girl, solo, strawberry-blonde hair half-up", 'P23 framing')
rep("Masterpiece, best quality, three-quarter at chest height, 1girl, solo, rain-grey glass-rain-blue palette",
    "Masterpiece, best quality, three-quarter view, ribs to crown, 1girl, solo, rain-grey glass-rain-blue palette", 'P03 framing')
rep("Masterpiece, best quality, three-quarter at chest height, 1girl, solo, honey-blonde hair in a waterfall braid",
    "Masterpiece, best quality, three-quarter-on, waist to crown, 1girl, solo, blonde hair in a waterfall braid", 'P06 framing')
rep("Masterpiece, best quality, three-quarter at chest height, 1girl, solo, storm-grey hair in a horn-threaded loop",
    "Masterpiece, best quality, three-quarter from the ribs up, half-turned to the door, 1girl, solo, storm-grey hair in a horn-threaded loop", 'P07 framing')
rep("Masterpiece, best quality, three-quarter at chest height, 1girl, solo, aqua-translucent hair",
    "Masterpiece, best quality, chest-height three-quarter, faced slightly left, 1girl, solo, wet-teal hair", 'P12 framing')
rep("Masterpiece, best quality, three-quarter at chest height, 1girl, solo, sleep-mussed lavender-grey hair",
    "Masterpiece, best quality, three-quarter torso view, hips up, 1girl, solo, sleep-mussed lavender-grey hair", 'P16 framing')
rep("Masterpiece, best quality, three-quarter at chest height, 1girl, solo, ember-copper hair",
    "Masterpiece, best quality, three-quarter from the waist up, angled right, 1girl, solo, ember-copper hair", 'P17 framing')
rep("Masterpiece, best quality, three-quarter at chest height, 1girl, solo, walnut-brown pixie crop",
    "Masterpiece, best quality, three-quarter bust view, faced on, 1girl, solo, walnut-brown pixie crop", 'P22 framing')
rep("Masterpiece, best quality, wide interior view from above, 1girl, solo, copper-red hair",
    "Masterpiece, best quality, high wide interior, room in frame, 1girl, solo, copper-red hair", 'P02 framing')
rep("Masterpiece, best quality, wide interior view at eye level, 1girl, solo, bottle-green hair",
    "Masterpiece, best quality, wide corridor view at eye height, 1girl, solo, bottle-green hair", 'P11 framing')
rep("Masterpiece, best quality, close view at eye level, 1girl, solo, ash-brown hair",
    "Masterpiece, best quality, close-in view, face and clock, 1girl, solo, ash-brown hair", 'P04 framing')
rep("Masterpiece, best quality, close view at eye level, 1girl, solo, calico patchwork hair",
    "Masterpiece, best quality, tight eye-level frame, her and the grin, 1girl, solo, auburn hair", 'P20 framing')

# ── D. EXP framing ×9 unique
rep("Masterpiece, best quality, close-up bust, viewed from the seated eye-level a hand-span away, 1girl, solo, candy-pink-bright",
    "Masterpiece, best quality, close bust framing, shoulder-up, from the seated eye-line a hand-span off, 1girl, solo, candy-pink-bright", 'P25 framing')
rep("Masterpiece, best quality, close-up bust, viewed from the seated eye-level a hand-span away, 1girl, solo, nettle-silver-green",
    "Masterpiece, best quality, bust-framed over the armrest's edge, from the seated viewer's eye height, 1girl, solo, nettle-silver-green", 'P26 framing')
rep("Masterpiece, best quality, close-up bust, viewed from the seated eye-level a hand-span away, 1girl, solo, snow-white-flat",
    "Masterpiece, best quality, chest-up view across the table corner, at the seated eye-line, 1girl, solo, snow-white-flat", 'P27 framing')
rep("Masterpiece, best quality, close-up bust, viewed from the seated eye-level a hand-span away, 1girl, solo, sapphire-glass-deep",
    "Masterpiece, best quality, framed in the doorway, bust height, from the seated eye-line inside, 1girl, solo, sapphire-glass-deep", 'P28 framing')
rep("Masterpiece, best quality, close-up bust, viewed from the seated eye-level a hand-span away, 1girl, solo, bell-bronze-green",
    "Masterpiece, best quality, bust framing at the sill, from the seated eye-level close, 1girl, solo, bell-bronze-green", 'P29 framing')
rep("Masterpiece, best quality, close-up bust, viewed from the seated eye-level a hand-span away, 1girl, solo, incense-smoke-warm-grey",
    "Masterpiece, best quality, chest-up from below the ladder step, seated eye-line, 1girl, solo, incense-smoke-warm-grey", 'P30 framing')
rep("Masterpiece, best quality, close-up bust, viewed from the seated eye-level a hand-span away, 1girl, solo, cheap-champagne-gold",
    "Masterpiece, best quality, bust view over the counter's edge, from the seated eye height, 1girl, solo, cheap-champagne-gold", 'P31 framing')
rep("Masterpiece, best quality, close-up bust, viewed from the seated eye-level a hand-span away, 1girl, solo, oil-black-iridescent",
    "Masterpiece, best quality, bust-close across the desk, from the seated eye-line beside, 1girl, solo, oil-black-iridescent", 'P32 framing')
rep("Masterpiece, best quality, close-up bust, viewed from the seated eye-level a hand-span away, 1girl, solo, mud-brown-warm",
    "Masterpiece, best quality, bust framing over the fence rail, seated eye-level near, 1girl, solo, mud-brown-warm", 'P33 framing')

# ── E. vary whisper/lens phrases (scene lines + face lines)
rep("whispering her denial while both ears spring upright mid-word, eyes straight into the lens",
    "whispering her denial while both ears spring upright mid-word, gaze aimed down the lens", 'P25 lens')
rep("she leans in from the side until her lips reach the top edge of the frame",
    "she leans in from the side until her lips graze the frame's upper rim", 'P25 lips')
rep("anime face a hand-span from the lens, lips at the top frame edge mid-whisper, anime eyes (rose, tsun-lidded over a dere gleam)",
    "anime face a hand-span from the lens, lips grazing the frame's upper rim mid-whisper, anime eyes (pink, tsun-lidded over a dere gleam)", 'P25 face')
rep("whispering frost at the lens while her plush tail has already wrapped her own ankle, eyes locked grey-green into the lens",
    "whispering frost at the lens while her plush tail has already wrapped her own ankle, grey-green eyes locked on the lens", 'P26 lens')
rep("brings her face within a hand-span of the lens", "brings her face within a hand-span of the viewer", 'P26 lips')
rep("anime face a hand-span from the lens, lips at the top frame edge mid-whisper, anime eyes (grey-green, arctic over ember)",
    "anime face near the cushion, mouth at the frame's upper rim mid-frost, anime eyes (grey-green, arctic over ember)", 'P26 face')
rep("whispering one sharp syllable stack while every spine lies smooth along her arms, dark round eyes straight into the lens",
    "whispering one sharp syllable stack while every spine lies smooth along her arms, dark round eyes fixed through the lens", 'P27 lens')
rep("lips at the top frame edge mid-whisper, anime eyes (dark round, prickly-soft)",
    "lips entering the frame's top corner mid-hiss, anime eyes (black, prickly-soft)", 'P27 face')
rep("whispering a blessing under the lintel while the window glass behind answers in sapphire and ruby, the glass freckles catching the window's colors one by one",
    "whispering a blessing under the lintel while the window glass behind answers in sapphire and ruby, the glass freckles catching the window's colors one by one, gaze level into the lens", 'P28 lens')
rep("lips at the frame's top edge mid-whisper, anime eyes (garnet, benedictory)",
    "whisper cresting the lintel's edge, anime eyes (dark-red, benedictory)", 'P28 face')
rep("whispering her half-prayer while her hair's tips thin into incense smoke and the ember at her fingertip keeps one warm point in the cold room",
    "whispering her half-prayer while her hair's tips thin into incense smoke and the ember at her fingertip keeps one warm point in the cold room, eyes into the lens", 'P29 lens')
rep("lips at the top frame edge mid-whisper, anime eyes (myrrh-brown, vigiled-soft)",
    "breath cresting the sill's line mid-psalm, anime eyes (brown, vigiled-soft)", 'P29 face')
rep("whispering the night's last psalm while the folded wings draw closer with every word, round amber eyes on the lens",
    "whispering the night's last psalm while the folded wings draw closer with every word, round amber eyes level with the lens", 'P30 lens')
rep("lips at the top frame edge mid-whisper, anime eyes (amber, round and quiet)",
    "psalm at the frame's upper edge mid-verse, anime eyes (amber, round and quiet)", 'P30 face')
rep("whispering tonight's heist plan syllable by syllable, whiskers twitching at each number, her thick ringed tail curled around the hip like a trophy boa, eyes straight into the lens",
    "whispering tonight's heist plan syllable by syllable, whiskers twitching at each number, her thick ringed tail curled around the hip like a trophy boa, eyes boring down the lens", 'P31 lens')
rep("lips at the top frame edge mid-whisper, anime eyes (mask-ringed, gleeful-sly)",
    "numbers at the frame's lip mid-count, anime eyes (black, mask-ringed and gleeful-sly)", 'P31 face')
rep("whispering a compliment too filthy for chrome, the sweet scent-haze curling from her collar in visible curls, eyes into the lens",
    "whispering a compliment too filthy for chrome, the sweet scent-haze curling from her collar in visible curls, gaze steady into the lens", 'P32 lens')
rep("lips at the top frame edge mid-whisper, anime eyes (amber-brown, insolent-lush)",
    "innuendo at the frame's upper border, anime eyes (amber, insolent-lush)", 'P32 face')
rep("whispering a trade offer with the small stolen trinket already palmed and mid-deal in quick fingers, bright near-black eyes straight into the lens",
    "whispering a trade offer with the small stolen trinket already palmed and mid-deal in quick fingers, bright near-black eyes pinned to the lens", 'P33 lens')
rep("lips at the top frame edge mid-whisper, anime eyes (near-black, scheme-bright)",
    "offer riding the rail's top edge mid-trade, anime eyes (black, scheme-bright)", 'P33 face')

# ── F. stems: eyes
rep("anime eyes (pale silver, patient)", "anime eyes (silver, patient)", 'P03 eyes')
rep("anime eyes (dark, three-quarters asleep)", "anime eyes (black, three-quarters asleep)", 'P04 eyes')
rep("anime eyes (charcoal, sharp-amused)", "anime eyes (grey, sharp-amused)", 'P05 eyes')
rep("anime eyes (molten gold, unimpressed)", "anime eyes (gold, unimpressed)", 'P07 eyes')
rep("anime eyes (deep aqua, scheduled-calm)", "anime eyes (teal, scheduled-calm)", 'P12 eyes')
rep("anime eyes (cobalt, closed for the kiss)", "anime eyes (blue, closed for the kiss)", 'P13 eyes')
rep("anime eyes (umber, savoring)", "anime eyes (brown, savoring)", 'P14 eyes')
rep("anime eyes (brass, one degree from smiling)", "anime eyes (gold, one degree from smiling)", 'P15 eyes')
rep("anime eyes (molten amber, slit-pupiled pride)", "anime eyes (amber, slit-pupiled pride)", 'P19 eyes')
rep("anime eyes (gold-green, conspiratorial)", "anime eyes (green, gold-flecked conspiratorial)", 'P20 eyes')
rep("anime eyes (rose, tsun-lidded over a dere gleam)", "anime eyes (pink, tsun-lidded over a dere gleam)", 'P25 eyes')
# stems: hair
rep("umber hair in steam-curled loose ringlets, warm spore-pale skin, young soft build, soft cap at the crown puffing one ring",
    "brown hair in steam-curled loose ringlets, warm pale skin, young soft build, kitchen steam coiling one ring above her head", 'P14 hair')
rep("calico patchwork hair in double space buns, cream skin with calico freckles, young nimble build, cat ears angled at the grin",
    "auburn hair patched cream in double space buns, cream skin with calico freckles, young nimble build", 'P20 hair')
# P25 skin
rep("cream-white winter coat of fine fur, young slight build, long upright ears flat back in denial",
    "cream-white winter coat of fine fur over fair skin, young slight build, long upright ears flat back in denial", 'P25 skin')

# ── G. race conversions P12/P14/P20
rep("P12 — room-tide-two-floods (NICHE · R25 Slime-girl · PG-13 · PL411 · P83_MIDNIGHT_LAGOON)",
    "P12 — room-tide-two-floods (NICHE · human · PG-13 · PL411 · P83_MIDNIGHT_LAGOON)", 'P12 header')
rep("Race: R25 Slime-girl — translucent aqua body with soft core-glow, hair ending in drip-tips · RF: ни одного",
    "Race: — (human; комната-прилив несёт невозможное)", 'P12 race')
rep("aqua-translucent hair in a slick low bun ending in drip-tips, glass-blue translucent skin with a soft core-glow, young fluid build",
    "wet-teal hair in a slick low bun, damp fair skin, young limber build", 'P12 pos')
rep("small drip-tip strand at the jaw", "small damp strand at the jaw", 'P12 face')
rep("P14 — scent-smoke-drinks-back (NICHE · R21 Mushroom-kin · R · PL413 · P73_VERMEIL_SMOKE)",
    "P14 — scent-smoke-drinks-back (NICHE · human · R · PL413 · P73_VERMEIL_SMOKE)", 'P14 header')
rep("Race: R21 Mushroom-kin — soft cap at the crown puffing one ring, gill-lines at the collar · RF: ни одного",
    "Race: — (human; видимая спираль запаха несёт правило)", 'P14 race')
rep("vermilion-ember accent at the spore sparks", "vermilion-ember accent at the warm sparks", 'P14 palette')
rep("spore-embers flaring at the elbow's fold like punctuation", "ember sparks flaring at the elbow's fold like punctuation", 'P14 pos')
rep("hazy, second figure, smoke blowing away, cap missing, generic fog",
    "hazy, second figure, smoke blowing away, ring broken, generic fog", 'P14 neg')
rep("P20 — smile-arrives-first (NICHE · R04 Cat-kin · R · PL419 · P112_POCKET_THEFT_GOLD)",
    "P20 — smile-arrives-first (NICHE · human · R · PL419 · P112_POCKET_THEFT_GOLD)", 'P20 header')
rep("hazy, second figure, full cat first, grin on the cat, cup spilled",
    "hazy, second figure, full cat first, grin attached to the cat, cup spilled", 'P20 neg')

# ── H. P11 channel line removal
rep("Channel: — (R-слот; заявка не требуется)\n", "", 'P11 channel')

# ── I. P26/P30 collars/dress rephrase (in-batch dup)
rep("the cup-edge ridge of her collarbone reading where the weight sinks into the cushion",
    "her collarbone's edge reading where the weight sinks into the cushion", 'P26 collarbone')
rep("hooded wool cloak over a long black dress with one thigh-slit",
    "hooded wool cloak over a floor-length black dress slit high at the thigh", 'P30 dress')
rep("myrrh-brown hair in a loose sleeping braid dissolving into pale smoke at the tips",
    "myrrh-brown hair braided loose and low, dissolving into pale smoke at the tips", 'P29 braid')
rep("rust-rose hair in a waterfall braid with loose waves", "rust-rose hair braided in a falling-water pattern, waves breaking loose", 'P21 braid')

# ── J. NEG guards EXP trim
rep("hazy, second figure, two girls, extra person, hand over the lens, face hidden, profile view only, ears drooping, generic smile",
    "hazy, second figure, two girls, extra person, face hidden", 'P25 neg')
rep("hazy, second figure, two girls, extra person, hand over the lens, face hidden, profile view only, tail free, leopard print body",
    "hazy, second figure, face hidden, profile view only, tail free", 'P26 neg')
rep("hazy, second figure, two girls, extra person, hand over the lens, face hidden, profile view only, spines raised, quill ball",
    "hazy, second figure, two girls, extra person, face hidden", 'P27 neg')
rep("hazy, second figure, two girls, extra person, hand over the lens, face hidden, profile view only, window plain, freckles missing",
    "hazy, second figure, two girls, extra person, face hidden", 'P28 neg')
rep("hazy, second figure, two girls, extra person, hand over the lens, face hidden, profile view only, hair normal solid, ember missing",
    "hazy, second figure, face hidden, profile view only, hair solid", 'P29 neg')
rep("hazy, second figure, two girls, extra person, hand over the lens, face hidden, profile view only, wings spread, feathers loose",
    "hazy, second figure, face hidden, profile view only, wings spread", 'P30 neg')
rep("hazy, second figure, two girls, extra person, hand over the lens, face hidden, profile view only, tail thin, tail raised, mask missing",
    "hazy, second figure, face hidden, thin tail, tail raised", 'P31 neg')
rep("hazy, second figure, two girls, extra person, hand over the lens, face hidden, profile view only, tail at the hip raised, stripe missing",
    "hazy, second figure, two girls, extra person, face hidden", 'P32 neg')
rep("hazy, second figure, two girls, extra person, hand over the lens, face hidden, profile view only, hands empty, fence broken",
    "hazy, second figure, two girls, extra person, face hidden", 'P33 neg')

# ── K. Race lines for slots missing them (insert before "Gar:" of each slot)
RACE_INSERT = {
 'P01 —': ("Race: R41 Witch-kin — witch hat with a soft droop, star-charms swinging at the brim · RF: ни одного\n", "Gar: CL-LG-01"),
 'P02 —': ("Race: — (human; тени несуществующих ступеней несут невозможное)\n", "Gar: CL-LG-07"),
 'P04 —': ("Race: R29 Mouse-kin — round mouse ears half-folded in sleep, small mouse mouth · RF: ни одного\n", "Gar: CL-LG-08"),
 'P05 —': ("Race: — (human; колода сдаёт себя сама)\n", "Gar: CL-TS-04 (thin ribbed tank top, straps honest and narrow)"),
 'P06 —': ("Race: R04 Cat-kin — cat ears tipped toward the shears' rhythm, calico freckles · RF: ни одного\n", "Gar: CL-DR-04"),
 'P08 —': ("Race: R33 Ghost-kin — outline dissolving into the wash at the edges, translucent pale skin · RF: ни одного\n", "Gar: CL-LG-06"),
 'P09 —': ("Race: R20 Harpy-kin — feathered legs from knee to ankle, talon-toes · RF: ни одного\n", "Gar: CL-TS-05"),
 'P10 —': ("Race: — (human; письмо пишет себя)\n", "Gar: CL-TS-01"),
 'P11 —': ("Race: R08 Serpent-kin — tapered snake tail folding like a ruler, fine scale-line at the temples, vertical pupils · RF: ни одного\n", "Gar: CL-DR-02"),
 'P12 —': ("Race: — (human; комната-прилив несёт невозможное)\n", "PLACEHOLDER12"),
 'P13 —': ("Race: — (human; шахматный суд несёт ритуал)\n", "Gar: CL-LG-01 (oversized sleep shirt, hem at the thighs)"),
 'P14 —': ("Race: — (human; видимая спираль запаха несёт правило)\n", "PLACEHOLDER14"),
 'P15 —': ("Race: R44 Marionette-kin — joint-lines at elbows and knees like porcelain doll seams, control threads faint to the ceiling · RF: ни одного\n", "Gar: CL-LG-02"),
 'P16 —': ("Race: R47 Wind-spirit-kin — hair strands held mid-air by no wind anyone can name, pale air-light skin · RF: ни одного\n", "Gar: CL-TS-10"),
 'P17 —': ("Race: R22 Flame-salamander-kin — crest of low fire along the spine's line, ember freckles at the jaw · RF: ни одного\n", "PLACEHOLDER17"),
 'P18 —': ("Race: R41 Witch-kin — witch hat hung on a wall peg behind her · RF: ни одного\n", "Gar: CL-DR-11"),
 'P19 —': ("Race: R07 Dragon-kin — fine iridescent scales at the forearms and throat, slit pupils · RF: ни одного\n", "PLACEHOLDER19"),
 'P20 —': ("Race: — (human; улыбка приходит первой, кот собирается после)\n", "Gar: CL-TS-07"),
 'P21 —': ("Race: R50 Nine-tails-kin — nine cream tails with ember-gold tips steadying the rope, silver-tipped fox ears · RF: ни одного\n", "PLACEHOLDER21"),
 'P22 —': ("Race: — (human; книги читают её вслух)\n", "PLACEHOLDER22"),
 'P23 —': ("Race: — (human; солнце живёт в чайнике)\n", "PLACEHOLDER23"),
 'P24 —': ("Race: — (human; порог открывается в небо)\n", "PLACEHOLDER24"),
 'P25 —': ("Race: R53 Rabbit-kin — long upright ears flat back in denial, cream-white winter coat, rose-pink inner ears · RF: ear-tips catch the key first\n", "PLACEHOLDER25"),
 'P26 —': ("Race: R54 Snow-leopard-kin — plush tail wrapped around her own ankle, snow-pale skin with faint shoulder rosettes, small round snow-leopard ears · RF: tail betrays the thaw first\n", "PLACEHOLDER26"),
 'P27 —': ("Race: R55 Hedgehog-kin — brown spines smoothed flat along the forearms, cream fur line at the collar · RF: spines read the mood\n", "PLACEHOLDER27"),
 'P28 —': ("Race: R56 Rose-glass-kin — stained-glass freckles over nose and cheeks, jewel-glass beads in the hair · RF: face is a small rose window\n", "PLACEHOLDER28"),
 'P29 —': ("Race: R57 Incense-wisp-kin — hair tips dissolving into pale incense smoke, ember glow at the fingertips · RF: smoke is a noun with a position\n", "PLACEHOLDER29"),
 'P30 —': ("Race: R58 Belfry-owl-kin — huge owl wings folded close like a cloak, moonlit plumage at collar and cuffs · RF: silent head turns\n", "PLACEHOLDER30"),
 'P31 —': ("Race: R59 Raccoon-kin — dark mask-ring around the eyes, thick fluffy ringed tail curled around the hip · RF: coat shines after rain\n", "PLACEHOLDER31"),
 'P32 —': ("Race: R60 Skunk-kin — white crest stripe at the crown, plume tail draped across the forearms like a boa · RF: scent drawn as visible curls\n", "PLACEHOLDER32"),
 'P33 —': ("Race: R61 Weasel-kin — long slinky body line, cream throat patch, restless quick hands mid-scheme · RF: never-empty hands\n", "PLACEHOLDER33"),
}
# resolve placeholders to actual Gar prefixes per slot
PLACE = {
 'PLACEHOLDER12': 'Gar: CL-BT-08', 'PLACEHOLDER14': 'Gar: CL-TS-14 (elastic bandage wrapped as a top, spiral of shadows)',
 'PLACEHOLDER17': 'Gar: CL-LG-06 (sheer lace-trim nightgown) + CL-AC-01', 'PLACEHOLDER19': 'Gar: CL-TS-11',
 'PLACEHOLDER21': 'Gar: CL-DR-04', 'PLACEHOLDER22': 'Gar: CL-LG-01 (oversized sleep shirt slipping',
 'PLACEHOLDER23': 'Gar: CL-LG-02', 'PLACEHOLDER24': 'Gar: CL-DR-04 (cotton sundress, sun-washed pattern)',
 'PLACEHOLDER25': 'Gar: CL-SW-04', 'PLACEHOLDER26': 'Gar: CL-SW-02', 'PLACEHOLDER27': 'Gar: CL-TS-14 (elastic bandage wrapped as a top) + CL-BT-01',
 'PLACEHOLDER28': 'Gar: CL-DR-10', 'PLACEHOLDER29': 'Gar: CL-OU-06', 'PLACEHOLDER30': 'Gar: CL-OU-03',
 'PLACEHOLDER31': 'Gar: CL-BT-06', 'PLACEHOLDER32': 'Gar: CL-SK-01', 'PLACEHOLDER33': 'Gar: CL-TS-03',
}
import re as _re
blocks = _re.split(r'(?=^P\d\d — )', t, flags=_re.M)
for i, b in enumerate(blocks):
    m = _re.match(r'^(P\d\d) — ', b)
    if not m: continue
    sid = m.group(1)
    if sid in ('P03', 'P07'):  # already have Race lines
        continue
    entry = RACE_INSERT.get(sid + ' —')
    if not entry: continue
    race_line, gar_key = entry
    if gar_key.startswith('PLACEHOLDER'):
        gar_key = PLACE[gar_key]
    idx = b.find('Gar: ')
    if idx == -1:
        fails.append('NOGAR ' + sid); continue
    # ensure slot doesn't already have Race:
    if 'Race: ' in b.split('POS:')[0]:
        continue
    nb = b[:idx] + race_line + b[idx:]
    blocks[i] = nb
t = '\n'.join(blocks) if False else ''.join(blocks)

# ── L. header fixes
rep("Каст мейнов: 14 кодов кинов + human×7 (17 кин-слотов). EXP: R53–R61, код на слот.",
    "каст 14/24 (12 кодов кинов + human×12). EXP: R53–R61, код на слот.", 'cast line')
rep("Итого 33: R+×19 · R×11 · PG-13×3.",
    "Спред мейнов R+×13 · R×8 · PG-13×3. Итого 33: R+×19 · R×11 · PG-13×3 (EXP-оверлей: R+×6 · R×3).", 'spread')
rep("## ОКНО (window.py --depth 3, прогон 2026-11-09T14:38:28+00:00)",
    "## ОКНО РОТАЦИИ (window.py --depth 3, прогон 2026-11-09T14:38:28+00:00)", 'window head')
rep("Ответ батча: 33 first-use PL400–PL432;",
    "Окно ротации: запрет 99 поз (PL300–399) / 91 палитра / 179 носителей / 19 burn. Ответ батча: 33 first-use PL400–PL432;", 'window stmt')
rep("## EXP-ПАЛИТРЫ (palettes.json 1.3.0, exp_color_wave_3 — все 9 РАЗНЫЕ, ни одной violet/plum)",
    "## EXP-ОВЕРЛЕЙ (palettes.json 1.3.0, exp_color_wave_3 — все 9 РАЗНЫЕ, ни одной violet/plum)\n\nEXP-оверлей: 9 EXP-слотов × (кандидат R53–R61 · палитра P171–P179 по одной · X3 «В-ШЁПОТ» D2×A02 · миды K240–K248); EXP-рейтинг R+×6 · R×3.", 'exp overlay')

save(P, t)

# ── stories.md race mentions
s = load(S)
reps_s = [
 ("register: young fluid, слизь R25", "register: young limber, человек-домработница прилива"),
 ("water по колено, отмечат на обоях границу прилива", "вода по колено, линия прилива отмечена на обоях"),
 ("register: young soft, гриб R21", "register: young soft, человек-дегустатор воздуха"),
 ("register: young nimble, кошка R04 (дубль R04 с P06 — в касте один код дважды)", "register: young nimble, человек с недособранным котом"),
 ("- scene: грибной угол кухни, дым вылеплен как шарф.", "- scene: грибной угол кухни, дым вылеплен как шарф; пар над её головой пыхает кольцом."),
]
for old, new in reps_s:
    if old in s: s = s.replace(old, new, 1)
    else: fails.append('S-MISS: ' + old[:40])
save(S, s)

print('FAILS:' if fails else 'ALL REPLACEMENTS OK')
for f in fails: print(' ', f)
