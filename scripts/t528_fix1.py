#!/usr/bin/env python3
"""T5-28 fix pass 1: comp.pose sync (В27-волна 2 v2) + POS-правки по квитанции гейтов."""
import json, re

CAM = 'specs/camera.json'
BATCH = 'batches/T5-28.md'

# ---------- 1. camera.json: comp.pose sync + trims ----------
d = json.load(open(CAM, encoding='utf-8'))
cards = {c['id']: c for c in d['y_cards']['cards']}

SYNC = {
    'Y316': {
        'pose': "cross-legged lean-back against a firm pew-back, the spine's weight given to the wood, one palm fanned flat on the psalter's cover, the habit's front pulled taut by the lean",
        'pattern': "cross-legged lean-back against a firm pew-back, the spine's weight given to the wood, one palm fanned flat on the psalter's cover, the habit's front pulled taut by the lean + upper body three-quarter",
    },
    'Y217': {
        'pose': "sitting cross-legged, both palms flat on the ground behind bearing the shoulders' full weight, chest lifted to the ceiling, head thrown back, throat leading, the stretch riding the ribs",
        'pattern': "sitting cross-legged, both palms flat on the ground behind bearing the shoulders' full weight, chest lifted to the ceiling, head thrown back, throat leading, the stretch riding the ribs + eye level",
    },
    'Y237': {
        'pose': "upper-body close: forehead to a cool wall, eyes closed, both palms flat to the surface at the shoulders, the wall taking the whole pulse's weight",
        'pattern': "upper-body close: forehead to a cool wall, eyes closed, both palms flat to the surface at the shoulders, the wall taking the whole pulse's weight + upper body three-quarter",
    },
    'Y437': {
        'pose': "shaking the dice cup over her own palm, the cup's rattle riding the wrist's snap, dice already settling stacked in her favor",
        'pattern': "shaking the dice cup over her own palm, the cup's rattle riding the wrist's snap, dice already settling stacked in her favor + CAM01",
    },
    'Y92': {
        'pose': "sitting cross-legged, both palms cupping own chin, elbows on knees, weight tipped forward into the viewer's space, the neckline falling with the lean, full attention",
        'pattern': "sitting cross-legged, both palms cupping own chin, elbows on knees, weight tipped forward into the viewer's space, the neckline falling with the lean, full attention",
    },
    'Y47': {
        'pose': "kneeling with both palms flat on the ground, hips lifted high under their own weight, head down between the arms, the arch holding like a drawn bow",
        'pattern': "kneeling with both palms flat on the ground, hips lifted high under their own weight, head down between the arms, the arch holding like a drawn bow + CAM12_aerial",
    },
    'Y348': {
        'pose': "crouched low on the chalk blueprint across the floor, one palm flat on a pine sapling growing along the drawn circle, the crouch's weight on the balls of the feet, the hem pooling in the chalk dust",
        'pattern': "crouched low on the chalk blueprint across the floor, one palm flat on a pine sapling growing along the drawn circle, the crouch's weight on the balls of the feet, the hem pooling in the chalk dust",
    },
    'Y328': {
        'pose': "sitting on the stone edge, feet trailing in the water, the towel hugged tight to the chest with both forearms, its tuck's weight held honest, steam rising",
        'pattern': "sitting on the stone edge, feet trailing in the water, the towel hugged tight to the chest with both forearms, its tuck's weight held honest, steam rising + upper body three-quarter",
    },
}
for yid, spec in SYNC.items():
    c = cards[yid]
    c['pattern'] = spec['pattern']
    comp = c.setdefault('components', {})
    comp['pose'] = spec['pose']
    # re-read cover object so it matches new pose wording where derived
    if comp.get('exposure', {}).get('read', ''):
        pass  # read остаётся историческим; клеймо несёт pose
d['version'] = '1.18.0'
for cl in (d.get('changelog') or []):
    if '1.18.0' in str(cl)[:8]:
        cl = cl  # уже есть
        break
json.dump(d, open(CAM, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('camera.json: comp.pose synced for', ', '.join(SYNC))

# ---------- 2. batches/T5-28.md правки ----------
t = open(BATCH, encoding='utf-8').read()

REPL = [
    # --- вплетения: суффиксы карт и точные тексты ---
    ("hem gathered into the crooked arm + skirt's weight hanging off the gathered fold\n",
     "hem gathered into the crooked arm + skirt's weight hanging off the gathered fold + upper body + slight low angle\n", 2),
    ("silk slip settling after the spin + hem still traveling around the knees\n",
     "silk slip settling after the spin + hem still traveling around the knees + three-quarter from below\n", 2),
    ("wrap sliding off one shoulder mid-swap + the crooked arm holding the old wrap at the chest + the fresh sash caught half-tied\n",
     "wrap sliding off one shoulder mid-swap + the crooked arm holding the old wrap at the chest + the fresh sash caught half-tied + eye-level close\n", 2),
    ("standing braced in the storm-cell wind with the long coat billowed hard behind, one hand holding the collar shut at the throat, weight into the gust",
     "standing braced in the storm-cell wind with the long coat billowed hard behind, one hand holding the collar shut at the throat, an orb of gathered lightning resting on the other open palm", 2),
    ("the spine's weight given over to the wood", "the spine's weight given to the wood", 2),
    ("the stretch's pull riding the ribs", "the stretch riding the ribs", 2),
    ("crouched low on the chalk blueprint spread across the floor", "crouched low on the chalk blueprint across the floor", 2),
    ("the crouch's weight balanced on the balls of the feet", "the crouch's weight on the balls of the feet", 2),
    # --- коридор A+B ---
    ("towel slipping, both hands catching it at the chest, knees slightly inward, looking down at the towel + upper body three-quarter\nPOS:",
     "towel slipping, both hands catching it at the chest, knees slightly inward, looking down at the towel + upper body three-quarter\nCorridor: A + B\nPOS:", 1),
    # --- char-spec: цвета как отдельные слова ---
    ("ruby eyes bent with laughter", "rose-red eyes bent with laughter", 1),
    ("anime eyes (ruby, bent with laughter)", "anime eyes (rose-red, bent with laughter)", 1),
    ("moss-dark eyes on her own left hand's stretch", "sage-green eyes on her own left hand's stretch", 1),
    ("anime eyes (moss-dark, patient)", "anime eyes (sage-green, patient)", 1),
    ("tide-line tan cutting the hip above the shorts", "tide-line tanned skin, the line cutting the hip above the shorts", 1),
    ("walnut-brown shoulder shag with curtain bangs, coffee-dark eyes holding one beat past the order",
     "chestnut shoulder shag with curtain bangs, deep brown eyes holding one beat past the order", 1),
    ("anime eyes (coffee-dark, holding past the order)", "anime eyes (deep brown, holding past the order)", 1),
    ("champagne-blonde vintage waves side-parted", "champagne blonde vintage waves side-parted", 1),
    ("raven-black ghost-layer shag", "raven black ghost-layer shag", 1),
    ("downcast eyes under the arch", "storm-grey eyes downcast under the arch", 1),
    ("anime eyes (downcast, counting breaths)", "anime eyes (storm-grey, counting breaths)", 1),
    # --- copypaste FAIL: общая n-грамма ---
    ("the chest line reading through the worn cotton", "her chest line read plain through the worn cotton", 1),
    ("the chest line reading through the mid-tone knit", "the chest line showing through the mid-tone knit", 1),
    # --- приборные слова (закон света v2) ---
    ("the hangar's one long bulb-line doubling in the vinyl's sheen", "the hangar's one long light-line doubling in the vinyl's sheen", 1),
    ("the pier's lantern-glow refracting doubled through the bell-hood", "the pier's moored glow refracting doubled through the bell-hood", 1),
    ("the street's lamps spacing the evening into counted segments", "the street's lit windows spacing the evening into counted segments", 1),
    ("the tally pen's clip catching the lamp", "the tally pen's clip catching the counter's glow", 1),
    ("the empty hall's chandelier burning for an audience of chairs", "the empty hall's high lights burning for an audience of chairs", 1),
    ("the chandelier earring swinging counter to the hem", "the drop earring swinging counter to the hem", 1),
    ("chandelier-spark gold", "hall-spark gold", 1),
    ("lacquer-lantern warm at the doorway", "lacquer-glow warm at the doorway", 1),
    ("honey-domestic-deep over lamp-butter-gold", "honey-domestic-deep over butter-gold", 1),
    ("the study's lamp-breath steady on the coal-to-gold gradient", "the study's ember-breath steady on the coal-to-gold gradient", 1),
    ("lamp-amber eyes soft on the near steam", "tea-amber eyes soft on the near steam", 1),
    ("lamp-amber warm at the steam", "tea-amber warm at the steam", 1),
    # --- NEG-гигиена ---
    ("cross visible, rosary, habit buttoned to the throat, sitting upright, crown absent",
     "cross visible, habit buttoned, sitting upright, crown absent", 1),
    ("solid hair color, tail, wings, head level, horns full-curl", "solid hair color, tail, head level, horns full-curl", 1),
    ("steam gone", "steamless", 1),
    # --- детали В32 (≥2 formTokens в POS) ---
    ("auburn hair in a wet slick low bun with one stray drip down the neck",
     "auburn hair in a wet slick low bun with one stray drip down the neck, a horn-chain earring at one ear", 1),
    ("forearm scale patches raised a drop with the pulse, a thick scaled tail pressed to the tub rim, mid_knockcatch",
     "forearm scale patches raised a drop with the pulse, a heat-polished bangle on one wrist, a thick scaled tail pressed to the tub rim, mid_knockcatch", 1),
    ("leaf-green hair in a thick fishtail braid over one shoulder, vine strands woven toward the fretboard",
     "leaf-green hair in a thick fishtail braid over one shoulder, a carved wooden hairpin through the braid, vine strands woven toward the fretboard", 1),
    ("a seasonal bloom at the temple open on the third, a bark patch at the collarbone warm from the soundboard",
     "a seasonal bloom at the temple open on the third, a sap-amber pendant beside the bark patch warm from the soundboard", 1),
    ("sea-teal hair in salt-crusted mermaid waves whipped with the cast",
     "sea-teal hair in salt-crusted mermaid waves whipped with the cast, a shell pendant at her throat", 1),
    ("athletic lean build, shin-and-hip scale patches gleaming iridescent where the spray lands, a net-vest smelling of night catches, mid_castfollow",
     "athletic lean build, shin-and-hip scale patches gleaming iridescent where the spray lands, a tide-call whistle on the net-vest's cord, mid_castfollow", 1),
    ("caramel hair in a messy top-bun with escaping strands",
     "caramel hair in a messy top-bun with escaping strands, a stolen hair pin through the bun", 1),
    ("long slinky body line, restless quick hands mid-scheme, the bare midriff where the cardigan gave up, mid_chairhover",
     "long slinky body line, restless quick hands mid-scheme, a keyring of borrowed keys at her hip, the bare midriff where the cardigan gave up, mid_chairhover", 1),
    ("silver-blond hair in micro-fringed long straight fall",
     "silver-blond hair in micro-fringed long straight fall, a moonstone pendant at the collarbone", 1),
    ("slender willowy build, long pointed elf ears pressed to the lace too, nothing worn at the ear, mid_lacepart",
     "slender willowy build, an heirloom signet ring on a chain at her wrist, long pointed elf ears pressed to the lace too, nothing worn at the ear, mid_lacepart", 1),
    ("ink-brown hair slicked straight back and piled high, dripping one count at a time",
     "ink-brown hair slicked straight back and piled high, dripping one count at a time, a single drop earring at one ear", 1),
    ("soft athletic build, one knee up as the rim's balance point, the trailing foot making its slow circles, mid_watertrail",
     "soft athletic build, a mole below the collarbone, one knee up as the rim's balance point, the trailing foot making its slow circles, mid_watertrail", 1),
    ("chestnut shoulder shag with curtain bangs, deep brown eyes holding one beat past the order",
     "chestnut shoulder shag with curtain bangs, round glasses fogged at the rim, deep brown eyes holding one beat past the order", 1),
    ("sturdy soft build, elbows stacked square on the backrest, a tally pen behind one ear, apron strings double-knotted, mid_counterlean",
     "sturdy soft build, elbows stacked square on the backrest, a choker of the shop's tag-string, a tally pen behind one ear, apron strings double-knotted, mid_counterlean", 1),
    ("champagne blonde vintage waves side-parted and spun loose at the ends",
     "champagne blonde vintage waves side-parted and spun loose at the ends, one drop earring at the lobe", 1),
    ("mousy-brown hair in a loose sleeping braid over one shoulder",
     "mousy-brown hair in a loose sleeping braid over one shoulder, one sleeper earring at the lobe", 1),
    ("soft slight build, the trench's shoulders swallowing hers, heels up in borrowed slippers, a cold cocoa ring on the rail by her elbow, mid_railvigil",
     "soft slight build, fingerless gloves holding the rail warm, the trench's shoulders swallowing hers, heels up in borrowed slippers, a cold cocoa ring on the rail by her elbow, mid_railvigil", 1),
    ("rain-dark brown hair with one side tucked behind the ear",
     "rain-dark brown hair with one side tucked behind the ear, a beauty mark at the jaw", 1),
    ("kelp-green hair sleeked to a center part and gathering the eaves' damp",
     "kelp-green hair sleeked to a center part and gathering the eaves' damp, a pearl earring at the near ear", 1),
    ("settled sturdy build, smooth suckered arms from the elbows folded ladder-quiet, a mantle-cape down the back beaded with the eaves' drops, mid_rainhold",
     "settled sturdy build, smooth suckered arms from the elbows folded ladder-quiet, a barnacle brooch at the mantle's clasp, a mantle-cape down the back beaded with the eaves' drops, mid_rainhold", 1),
    ("jade-black hair in a low braided chignon under a gauze veil",
     "jade-black hair in a low braided chignon under a gauze veil, one brass earring below the veil's edge", 1),
    ("elegant guarded build, small glossy snake-coils asleep under the gauze, one heel hovering over the lit seam, back-seam stockings honest along the stepping calf, mid_seamcross",
     "elegant guarded build, small glossy snake-coils asleep under the gauze, a scaled garter band at one thigh, one heel hovering over the lit seam, back-seam stockings honest along the stepping calf, mid_seamcross", 1),
    ("ink-chestnut hair in a pencil-skewered bun coming loose at the temple",
     "ink-chestnut hair in a pencil-skewered bun coming loose at the temple, reading glasses pushed up into the bun", 1),
    ("slight soft build, the oversized sleep shirt's hem at the thighs, one shoulder always escaping the washed-wide collar, a wax seal unused on the scale's base, slouch socks at the far foot, mid_letterweigh",
     "slight soft build, a wax-stained signet ring on one hand, the oversized sleep shirt's hem at the thighs, one shoulder always escaping the washed-wide collar, a wax seal unused on the scale's base, slouch socks at the far foot, mid_letterweigh", 1),
    ("raven black ghost-layer shag with one white crest stripe running from the nape down the spine",
     "raven black ghost-layer shag with one white crest stripe running from the nape down the spine, one gold hoop earring", 1),
    ("compact springy build, the plume tail draped across both forearms like a boa, sweet scent-haze drawn as two faint curls at the shoulder, mid_dicecast",
     "compact springy build, a dice-charm bracelet at one wrist, the plume tail draped across both forearms like a boa, sweet scent-haze drawn as two faint curls at the shoulder, mid_dicecast", 1),
    ("porcelain-blonde hair in long glossy doll-curls",
     "porcelain-blonde hair in long glossy doll-curls, a ribbon choker at the throat", 1),
    ("ball-jointed elbows and knees with seam lines honest at the bends, the winding key between the shoulder blades shown in the mirror behind, mid_zipperhold",
     "ball-jointed elbows and knees with seam lines honest at the bends, a brass key brooch at the collar, the winding key between the shoulder blades shown in the mirror behind, mid_zipperhold", 1),
    ("honey-gold hair in a sectioned bubble ponytail tipping with the lean",
     "honey-gold hair in a sectioned bubble ponytail tipping with the lean, pollen freckles across the nose", 1),
    ("soft warm build, chitin antennae above the brows aimed at the lens, four translucent wings at rest behind like mica smoke, a honeycomb comb at the temple, mid_forwardattention",
     "soft warm build, a bee-charm bracelet at one wrist, chitin antennae above the brows aimed at the lens, four translucent wings at rest behind like mica smoke, a honeycomb comb at the temple, mid_forwardattention", 1),
    ("ember-red hair in a voluminous 80s blowout bouncing with the swap",
     "ember-red hair in a voluminous 80s blowout bouncing with the swap, an ember-drop earring at one ear", 1),
    ("generous strong build, feather accents grading coal-to-gold down the forearms, cloth singed soft at the wing-roots, an ember-glow rim at one temple strand, mid_wrapswap",
     "generous strong build, feather accents grading coal-to-gold down the forearms, one thin burn scar along the forearm, cloth singed soft at the wing-roots, an ember-glow rim at one temple strand, mid_wrapswap", 1),
    ("ink-feather-black blunt chin bob with a black feather cap on the crown and one red crown-spot at the hairline",
     "ink-feather-black blunt chin bob with a black feather cap on the crown, a red cord whistle at the neck and one red crown-spot at the hairline", 1),
    ("long elegant build, crane wings folded shawl-wise along the back, not one feather flying, a sports bottle at one knee, long pale legs carrying the lifted line, mid_archhold",
     "long elegant build, one brass bangle at the ankle, crane wings folded shawl-wise along the back, not one feather flying, a sports bottle at one knee, long pale legs carrying the lifted line, mid_archhold", 1),
    ("silverdust-lavender hair in low twin buns with ribbon ties",
     "silverdust-lavender hair in low twin buns with ribbon ties, a moth-charm bracelet at one wrist", 1),
    ("the tea's steam climbing one antenna's curve, a second cup set at the table's far side gone cold while hers steams, the blanket folded in her own wings' pattern at the couch",
     "the tea's steam climbing one antenna's curve, a little bell on the tea tray's edge, a second cup set at the table's far side gone cold while hers steams, the blanket folded in her own wings' pattern at the couch", 1),
    ("meadow-blonde hair half-up tied with a kerchief",
     "meadow-blonde hair half-up tied with a kerchief, a surveyor's signal whistle pinned to the kerchief", 1),
    ("lithe springy build, smooth unbranched deer horns at the hairline, quick deer ears turned to the leaf-whisper, a small deer tail under the pinafore's strap, mid_blueprintcrouch",
     "lithe springy build, a plumb-bob pendant at the collarbone, smooth unbranched deer horns at the hairline, quick deer ears turned to the leaf-whisper, a small deer tail under the pinafore's strap, mid_blueprintcrouch", 1),
    ("steel-grey hair in a rope-twist side ponytail heavy with salt",
     "steel-grey hair in a rope-twist side ponytail heavy with salt, a buoy-tag earring at one ear", 1),
    ("the empty creel's mouth open at the stone, one palm held level before the chest carrying the weight of everything she let go",
     "a fisherman's pouch at the stone, the empty creel's mouth open beside it, one palm held level before the chest carrying the weight of everything she let go", 1),
]

missed = []
for old, new, expect in REPL:
    n = t.count(old)
    if n != expect:
        missed.append((old[:60], n, expect))
    t = t.replace(old, new)

open(BATCH, 'w', encoding='utf-8').write(t)
print('batch patched. missed:', missed if missed else 'none')

# ---------- 3. Разбивка строк >200 знаков (кроме вплетений) ----------
lines = t.split('\n')
poses = []
d2 = json.load(open(CAM, encoding='utf-8'))
for c in d2['y_cards']['cards']:
    p = (c.get('components') or {}).get('pose', '')
    if p: poses.append(p)
poses_lower = [p.lower() for p in poses]

out = []
split_count = 0
for ln in lines:
    if len(ln) <= 200:
        out.append(ln); continue
    low = ln.lower()
    is_weave = any(p in low for p in poses_lower)
    if is_weave:
        out.append(ln)  # вплетение нельзя резать — оно уже ≤200 после тримов
        continue
    # режем по запятой ближе к 190
    parts, cur = [], ln
    while len(cur) > 200:
        cut = cur.rfind(',', 0, 195)
        if cut < 60: cut = cur.rfind(' ', 0, 195)
        parts.append(cur[:cut+1])
        cur = ' ' + cur[cut+1:].lstrip()
    parts.append(cur)
    out.extend(parts)
    split_count += 1
open(BATCH, 'w', encoding='utf-8').write('\n'.join(out))
print(f'длинных строк разбито: {split_count}')
