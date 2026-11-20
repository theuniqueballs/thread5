#!/usr/bin/env python3
"""T5-28 fix pass 2: char-spec волосы, Corridor A+B, NEG-гигиена (гарды ≤4, якоря)."""
import re

BATCH = 'batches/T5-28.md'
t = open(BATCH, encoding='utf-8').read()

REPL = [
    # --- char-spec: слово «hair» рядом с цветом ---
    ("chestnut shoulder shag with curtain bangs, round glasses fogged at the rim",
     "chestnut hair in a shoulder shag with curtain bangs, round glasses fogged at the rim", 1),
    ("champagne blonde vintage waves side-parted and spun loose at the ends",
     "champagne blonde hair in vintage waves, side-parted and spun loose at the ends", 1),
    ("raven black ghost-layer shag with one white crest stripe running from the nape down the spine",
     "raven black hair in a ghost-layer shag, one white crest stripe running from the nape down the spine", 1),
    # --- Corridor: A + B для карт A+B (Y293, Y437) ---
    ("Corridor: A\nTHESIS: «СТУК", "Corridor: A + B\nTHESIS: «СТУК", 1),
    ("an orb of gathered lightning resting on the other open palm + CAM01\nPOS:\nCorridor: A + B\nPOS:",
     "an orb of gathered lightning resting on the other open palm + CAM01\nPOS:", 1),
    ("Corridor: A\nTHESIS: «КОСТИ УДАЧИ", "Corridor: A + B\nTHESIS: «КОСТИ УДАЧИ", 1),
    # --- NEG: гард-диета до ≤4 и якоря ---
    ("towel fallen, towel secure, door open, second figure, steamless",
     "towel fallen, towel secure, door open, steamless", 1),
    ("rod still, line slack, fish visible, hands dry",
     "rod still, line slack, fishless, hands dry", 1),
    ("hair down, body dry, phone in hand, towel worn, both feet in",
     "hair down, body dry, phone in hand, both feet in", 1),
    ("stool forward, standing, eyes away, apron absent, counter clear",
     "stool forward, standing, eyes away, apron absent", 1),
    ("horns full-curl, tail absent, curtain open, both shoulders bare, chin down",
     "horns full-curl, tail absent, curtain open, chin down", 1),
    ("mid-spin, hem still, both straps up, partner visible, crowd visible",
     "mid-spin, hem still, both straps up, crowdless", 1),
    ("day window, second figure, seat occupied, standing, sleeves short",
     "day window, seat occupied, standing, sleeves short", 1),
    ("feet flat, arms folded, indoors, window dark, rain heavy, cocoa steaming",
     "feet flat, arms folded, indoors, window dark", 1),
    ("skirt still, shoes on, straps added, mirror broken, sad",
     "skirt still, shoes, straps added, mirror broken", 1),
    ("umbrella open, downpour, soaked, suckers engaged, running",
     "umbrella open, downpour, soaked, suckers engaged", 1),
    ("snakes awake, eyes up, both feet one side, veil absent, line invisible",
     "snakes awake, eyes up, both feet together, veil absent", 1),
    ("letter open, letter sent, both feet down, shirt buttoned, seal broken, crying",
     "letter sent, both feet down, shirt buttoned, seal broken", 1),
    ("dice landed, cup still, tail on floor, stripe absent, perfume fog",
     "dice landed, cup still, tail on floor, stripe absent", 1),
    ("zipper up, zipper fully down, key visible front, joints hidden, blush living, subsurface glow",
     "zipper up, zipper fully down, key visible front, blush living", 1),
    ("wrap on, wrap off, sash tied, sash absent, symmetric pose, fire visible",
     "wrap off, sash tied, symmetric pose, fire visible", 1),
    ("side angle, hips level, head up, wings spread, feathers flying, skirt",
     "side angle, hips level, head up, feathers flying", 1),
    ("neckline held, sitting back, wings spread, antennae absent, blanket absent",
     "neckline held, sitting back, wings spread, antennae absent", 1),
    ("wings featherless, beads silent, back covered, jacket closed, wind absent, facing forward",
     "beads silent, back covered, jacket closed, wind absent", 1),
    ("standing, sapling absent, spots absent, horns branched, flat light",
     "standing, sapling absent, spots absent, horns branched", 1),
    ("creel full, fish visible, shoulders wet, hem dry, towel loose, fin absent",
     "creel full, fishless, shoulders wet, hem dry", 1),
]

missed = []
for old, new, expect in REPL:
    n = t.count(old)
    if n != expect:
        missed.append((old[:55], n, expect))
    t = t.replace(old, new)

open(BATCH, 'w', encoding='utf-8').write(t)
print('patched. missed:', missed if missed else 'none')
