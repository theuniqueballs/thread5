#!/usr/bin/env python3
"""T5-28 fix pass 3: claim-физика (В31), Corridor A+B (P32), детали, копипасты, EXP-каналы, якоря."""
BATCH = 'batches/T5-28.md'
t = open(BATCH, encoding='utf-8').read()

REPL = [
    # --- Corridor P32 (Y348 = A+B) ---
    ("Corridor: A\nTHESIS: «СИНИЙ ЧЕРТЁЖ", "Corridor: A + B\nTHESIS: «СИНИЙ ЧЕРТЁЖ", 1),
    # --- EXP: убрать Channel-строку (T5-27 прецедент: EXP без Channel) ---
    ("Channel: — (EXP вне каналов, прецедент T5-24/27)\n", "", 9),
    # --- якоря NEG ---
    ("stinger visible", "stinger absent", 1),
    ("symmetric pose, fire visible", "symmetric pose, flameless", 1),
    # --- neg-dress P31: гард одетости ---
    ("beads silent, back covered, jacket closed, wind absent", "beads silent, back covered, wind absent", 1),
    # --- приборные остатки ---
    ("lamp-amber far at the street", "amber far at the street", 1),
    # --- claim-физика (В31): класс раскрытия + объект коридора A ---
    ("the skintight plugsuit's vinyl stretched to glass sheen where the lean pulls, nothing underneath but the seal's own pressure — the pressure seal is the claim, vitrine-made",
     "the skintight plugsuit's vinyl stretched to glass sheen where the lean pulls, both palms flat on the rails, nothing underneath but the seal's own pressure — the pressure seal is the claim, vitrine-made", 1),
    ("the psalter pressed flat above the heart by one fanned palm — the sprawl is the claim, heresy-made",
     "the psalter pressed flat above the heart by both palms — the sprawl is the claim, heresy-made", 1),
    ("the suspender skirt's straps framing the argument, nothing underneath the luck but its own math — the rattle's snap is the claim, luck-made",
     "the fabric gathering where the suspender straps frame it, nothing underneath the luck but its own math — the rattle's snap is the claim, luck-made", 1),
    ("the dress front held flat by one pressed palm, the zipper's half-down spine baring the named slip's cream line",
     "the dress front held by palms pressed flat over the chest line, the zipper's half-down spine baring the named slip's cream line", 1),
    ("the knit tube top's neckline falling with the forward weight, the chest line reading honest at the fallen edge, the satin skirt pooled around the cross-legged fold",
     "the knit tube top's neckline falling with the forward weight, the fabric gathering at the fallen edge, the chest line reading honest at the gather, the satin skirt pooled around the cross-legged fold", 1),
    ("the oversized mohair's neckline falling forward with the lean, the chest line reading through the mid-tone knit where the gravity takes it, nothing holding the fold but wool's weight — the falling neckline is the claim, tea-made",
     "the oversized mohair's neckline giving forward with the lean, the fabric gathering where the gravity takes it, the chest line reading through the mid-tone knit, nothing holding the fold but wool's weight — the falling neckline is the claim, tea-made", 1),
    ("the open leather jacket's left lapel given to the gust, the bandage wrap pulled flat across the chest line by the same wind",
     "the jacket sliding open to the gust, one sleeve caught at the crook, the bandage wrap pulled flat over the chest line by the same wind", 1),
    ("the linen pinafore's hem pooled in the chalk dust, the crouch's fold crossing her thighs' line where the caustics land, one palm flat on the sapling, nothing between the plan and the soil but her shadow — the caustic hem is the claim, drafting-made",
     "the linen pinafore's hem pooled in the chalk dust, the crouch's fold crossing her thighs' line where the caustics land, her breast shape read at the crouch's lean, one palm flat on the sapling, the other palm flat in the chalk, nothing between the plan and the soil but her shadow — the caustic hem is the claim, drafting-made", 1),
    # --- детали В32: P06/P07/P08 ---
    ("willowy drifting build, tendril strands at the nape braiding themselves, one tendril wrapped at the gathering wrist, mid_bellsettle",
     "willowy drifting build, a small shell pendant inside the bell-hood's rim, tendril strands at the nape braiding themselves, one tendril wrapped at the gathering wrist, mid_bellsettle", 1),
    ("quick wiry build, pointed grey-furred wolf ears swiveled across the yard, fur-cuffed wrists softening the hold, a small fang in the caught grin, mid_pulsehold",
     "quick wiry build, pointed grey-furred wolf ears swiveled across the yard, a brass earring at the near ear, fur-cuffed wrists softening the hold, a small fang in the caught grin, mid_pulsehold", 1),
    ("petite springy build, long upright bunny ears flagging in the updraft with pink inner-ear blush lit through",
     "petite springy build, a carrot-charm bracelet at one wrist, light freckles across the nose, long upright bunny ears flagging in the updraft with pink inner-ear blush lit through", 1),
    # --- внутрибатчевые копипасты ---
    ("pulled flat across the chest line by the same wind", "pulled flat over the chest line by the same wind", 1),
    ("a ribbon choker at the throat, ball-jointed", "a ribbon choker with a key charm, ball-jointed", 1),
    ("the clock's minute hand halfway to midnight on the wall", "the clock's hand halfway to midnight on the wall", 1),
    ("upper body three-quarter, towel caught mid-slip at the chest, 1girl, solo, her breast shape read in the caught towel's clutch",
     "upper body three-quarter, towel caught mid-slip at the sternum, 1girl, solo, her breast shape read in the caught towel's clutch", 1),
    ("her breast shape read in the sundress's bodice where the laugh lifts it",
     "her breast shape reading in the sundress's bodice as the laugh lifts it", 1),
    ("the bandage wrap reading her breast shape where the gust pulls it flat",
     "the bandage wrap flat across her breast shape in the gust", 1),
    ("the cropped pullover reading her breast shape at the crest stripe's pull",
     "the cropped pullover reading her breast shape at the pull of the crest stripe", 1),
]

missed = []
for old, new, expect in REPL:
    n = t.count(old)
    if n != expect:
        missed.append((old[:55], n, expect))
    t = t.replace(old, new)

open(BATCH, 'w', encoding='utf-8').write(t)
print('patched. missed:', missed if missed else 'none')

# приборные остатки — доконтроль
import re
for pat in ('lamp', 'bulb', 'lantern', 'chandelier', 'candle', 'torch'):
    for m in re.finditer(r'.{40}' + pat + r'.{40}', t):
        seg = m.group(0)
        if 'NEG:' in seg or ', lamp,' in seg or 'candle, lamp' in seg:
            continue
        print('CHECK', pat, ':', seg[:95])
