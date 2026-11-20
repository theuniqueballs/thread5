#!/usr/bin/env python3
"""T5-28 fix pass 5: классы раскрытия, геометрия B, приборные остатки, копипасты."""
BATCH = 'batches/T5-28.md'
t = open(BATCH, encoding='utf-8').read()

REPL = [
    # P01: класс раскрытия (sheer) + разнос с P17
    ("the skintight plugsuit's vinyl reading her breast shape where the lean pulls it taut, both palms flat on the rails,",
     "the skintight plugsuit's vinyl gone sheer where the lean pulls it taut, both palms flat on the rails,", 1),
    # P25: геометрия B (waistband) + разнос с P32
    ("the fabric gathering where the suspender straps frame it,",
     "the fabric gathering where the suspender skirt's waistband frames it,", 1),
    ("the cropped pullover reading her breast shape at the pull of the crest stripe",
     "the crest stripe reading her breast shape at its pull over the cropped pullover", 1),
    # P26: класс раскрытия (sheer)
    ("the zipper's half-down spine baring the named slip's cream line with its one amber ribbon",
     "the zipper's half-down spine baring the named slip's cream line sheer in the gap, one amber ribbon", 1),
    # P27: разнос «neckline giving forward» с P30
    ("upper body three-quarter, the neckline giving forward with the lean,",
     "upper body three-quarter, the neckline tipping forward with the lean,", 1),
    # P30: приборный остаток
    ("the scale-dust catching the lamp's low ring", "the scale-dust catching the low ring of the glow", 1),
    # P32: объект A (palms flat) + геометрия B (hem tucked)
    ("one palm flat on the sapling, the other palm flat in the chalk,",
     "both palms flat — one on the sapling, the other in the chalk,", 1),
    ("the linen pinafore's hem pooled in the chalk dust,",
     "the linen pinafore's hem tucked in the chalk dust,", 1),
]

missed = []
for old, new, expect in REPL:
    n = t.count(old)
    if n != expect:
        missed.append((old[:55], n, expect))
    t = t.replace(old, new)

open(BATCH, 'w', encoding='utf-8').write(t)
print('patched. missed:', missed if missed else 'none')
