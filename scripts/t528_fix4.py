#!/usr/bin/env python3
"""T5-28 fix pass 4: точечные правки по фактическим строкам."""
BATCH = 'batches/T5-28.md'
t = open(BATCH, encoding='utf-8').read()

REPL = [
    # EXP-каналы: убрать строку (прецедент T5-27 — EXP без Channel)
    ("Channel: — (EXP вне каналов)\n", "", 8),
    # P01 claim: класс раскрытия
    ("the skintight plugsuit's vinyl stretched to glass sheen where the lean pulls, both palms flat on the rails, nothing underneath but the seal's own pressure — the pressure seal is the claim, vitrine-made",
     "the skintight plugsuit's vinyl reading her breast shape where the lean pulls it taut, both palms flat on the rails, nothing underneath but the seal's own pressure — the pressure seal is the claim, vitrine-made", 1),
    # P25 claim: объект коридора A + геометрия
    ("the cropped pullover's hem at the ribs with the crest stripe pulling taut across the chest line, the suspender skirt's straps framing the argument,",
     "the cropped pullover's hem at the ribs with the crest stripe pulling taut across the chest line, the fabric gathering where the suspender straps frame it,", 1),
    # P26 claim: класс раскрытия (плюс разнос с P07)
    ("the dress front held by palms pressed flat over the chest line,",
     "the dress front held by palms pressed flat against the chest line,", 1),
    # P27 opener: разнос «neckline falling forward with the lean» с P30
    ("upper body three-quarter, the neckline falling forward with the lean, 1girl, solo, her breast shape reading at the tube top's fallen line,",
     "upper body three-quarter, the neckline giving forward with the lean, 1girl, solo, her breast shape reading at the tube top's fallen line,", 1),
    # P30 claim: класс раскрытия
    ("the oversized mohair's neckline falling forward with the lean, the chest line showing through the mid-tone knit where the gravity takes it,",
     "the oversized mohair's neckline giving forward with the lean, the fabric gathering where the gravity takes it, the chest line showing through the mid-tone knit,", 1),
    # P32 claim: объект коридора + раскрытие + разнос с P25
    ("the linen pinafore's hem pooled in the chalk dust, the crouch's fold crossing her thighs' line where the caustics land, one palm flat on the sapling,",
     "the linen pinafore's hem pooled in the chalk dust, the crouch's fold crossing her thighs' line where the caustics land, her breast shape read at the lean, one palm flat on the sapling, the other palm flat in the chalk,", 1),
    # P26 детали: разнос «a ribbon choker at the throat» с P04
    ("porcelain-blonde hair in long glossy doll-curls, a ribbon choker at the throat,",
     "porcelain-blonde hair in long glossy doll-curls, a ribbon choker with a key charm,", 1),
    # P20 opener: разнос «reading her waist line where the» с P17
    ("the trench's belt cinch reading her waist line where the lean drapes it,",
     "the trench's belt cinch tracing her waist line where the lean drapes it,", 1),
    # приборные остатки
    ("deciding-grey eyes on the needle, lamplit-warm pale skin at the bare shoulder,",
     "deciding-grey eyes on the needle, hour-warm pale skin at the bare shoulder,", 1),
    ("anime eyes (lamp-amber, soft)", "anime eyes (tea-amber, soft)", 1),
]

missed = []
for old, new, expect in REPL:
    n = t.count(old)
    if n != expect:
        missed.append((old[:55], n, expect))
    t = t.replace(old, new)

open(BATCH, 'w', encoding='utf-8').write(t)
print('patched. missed:', missed if missed else 'none')

# Разбивка новых длинных строк (>200), не задевая вплетения
import json
d = json.load(open('specs/camera.json', encoding='utf-8'))
poses = [((c.get('components') or {}).get('pose', '') or '').lower() for c in d['y_cards']['cards']]
poses = [p for p in poses if p]
lines = t.split('\n')
out, split_count = [], 0
for ln in lines:
    if len(ln) <= 200:
        out.append(ln); continue
    if any(p in ln.lower() for p in poses):
        out.append(ln); continue
    parts, cur = [], ln
    while len(cur) > 200:
        cut = cur.rfind(',', 0, 195)
        if cut < 60: cut = cur.rfind(' ', 0, 195)
        parts.append(cur[:cut+1]); cur = ' ' + cur[cut+1:].lstrip()
    parts.append(cur); out.extend(parts); split_count += 1
open(BATCH, 'w', encoding='utf-8').write('\n'.join(out))
print('разбито длинных строк:', split_count)
