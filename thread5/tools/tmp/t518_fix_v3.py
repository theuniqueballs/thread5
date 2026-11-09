#!/usr/bin/env python3
import io
P='batches/T5-18.md'; S='batches/T5-18/stories.md'
t=io.open(P,encoding='utf-8').read(); s=io.open(S,encoding='utf-8').read()
fails=[]
def rep(txt,old,new,label):
    if old in txt: return txt.replace(old,new,1)
    fails.append('MISS '+label); return txt

# P26 lens
t=rep(t,"over the armrest to bring her face within a hand-span of the lens, weight sunk into the",
        "over the armrest to bring her face within a hand-span of the viewer, weight sunk into the",'P26 lens')
# P14 stories scene
s=rep(s,"шляпка пыхает кольцом; споры-угольки\nвспыхивают на локте","пар над её головой пыхает кольцом; тёплые искры\nвспыхивают на локте",'P14 scene')
if 'шляпка пыхает кольцом' in s: s=s.replace('шляпка пыхает кольцом','пар над её головой пыхает кольцом',1)

# ── salience: move claim lexeme into line1 after "1girl, solo," and strip from line2
moves = [
 # P01
 ("1girl, solo, honey-blonde hair in a loose sleeping braid, warm dusk-pale skin",
  "1girl, solo, nipples a soft twin-print through the stretched buttonholes, honey-blonde hair in a loose sleeping braid, warm dusk-pale skin"),
 ("the stretched buttonholes printing honest ovals where the backward arch pulls the weave taut, nipples a soft twin-print through the gaps — the placket's confession is the claim",
  "the stretched buttonholes printing honest ovals where the backward arch pulls the weave taut — the placket's confession is the claim"),
 # P03
 ("1girl, solo, rain-grey glass-rain-blue palette, long dove-grey hair",
  "1girl, solo, nipples a dark twin-line under the wet gauze, rain-grey glass-rain-blue palette, long dove-grey hair"),
 ("the undershirt printing honest where the climb is wettest, nipples a dark twin-line under the gauze — the claim standing in the cloth itself",
  "the undershirt printing honest where the climb is wettest — the claim standing in the cloth itself"),
 # P05
 ("1girl, solo, jet-black hair with a side shave and a long sweep-over, pale skin",
  "1girl, solo, one card shading the top of her bare chest at the collar's gap, jet-black hair with a side shave and a long sweep-over, pale skin"),
 ("one playing card tucked edge-out at the collar's gap, shading the top of her bare chest — the tucked card is the claim, king-side out",
  "one playing card tucked edge-out at the collar's gap — the tucked card is the claim, king-side out"),
 # P07
 ("1girl, solo, storm-grey hair in a horn-threaded loop, granite-grain pale skin",
  "1girl, solo, black lace panties one honest inch in the thigh-slit, storm-grey hair in a horn-threaded loop, granite-grain pale skin"),
 ("the thigh-slit yawning one honest inch of black lace panties — the caught dress is the claim, the door holding it hostage",
  "— the caught dress is the claim, the door holding it hostage"),
 # P09
 ("1girl, solo, cloud-white hair in a blunt hime cut, porcelain-cool skin",
  "1girl, solo, boyshorts waistband honest under the flying tiers, cloud-white hair in a blunt hime cut, porcelain-cool skin"),
 ("the petticoat's white hem doing its half of the lifted reveal where the updraft takes it, the boyshorts' waistband honest beneath the flying tiers — the flying hem is the claim",
  "the petticoat's white hem doing its half of the lifted reveal where the updraft takes it — the flying hem is the claim"),
 # P17
 ("1girl, solo, ember-copper hair in a deep side wave over one shoulder, heat-warmed skin tone",
  "1girl, solo, nipples a tea-warm press under soaked lace, ember-copper hair in a deep side wave over one shoulder, heat-warmed skin tone"),
 ("nipples a tea-warm press under the soaked lace — the soaked sheer is the claim, rain-served",
  "— the soaked sheer is the claim, rain-served"),
 # P19
 ("1girl, solo, dragon-blood red hair in a thick fishtail braid over the shoulder, sunlit fair skin",
  "1girl, solo, neckline low over the bare chest at the knot, dragon-blood red hair in a thick fishtail braid over the shoulder, sunlit fair skin"),
 ("the knot pulling the neckline low over the bare chest line — the reach's pull is the claim, written in cloth tension",
  "— the reach's pull is the claim, written in cloth tension"),
 # P21
 ("1girl, solo, rust-rose hair braided in a falling-water pattern, waves breaking loose, sun-warmed ivory skin",
  "1girl, solo, cotton panties flashing one honest beat at the wave's crest, rust-rose hair braided in a falling-water pattern, waves breaking loose, sun-warmed ivory skin"),
 ("cotton panties flashing one honest beat at the wave's crest — the rising wave is the claim, one stitch at a time",
  "— the rising wave is the claim, one stitch at a time"),
 # P23
 ("1girl, solo, strawberry-blonde hair half-up pinned in loose cascade, sun-pinked cream skin",
  "1girl, solo, neckline open over the bare chest at the morning lean, strawberry-blonde hair half-up pinned in loose cascade, sun-pinked cream skin"),
 ("the morning lean opening the neckline over the bare chest's curve — the spout's backlight draws the coverage border on the cloth, honest and ruled",
  "the spout's backlight draws the coverage border on the cloth, honest and ruled"),
 # P24
 ("1girl, solo, wheat-blonde hair breeze-split to mid-back with a trailing silk ribbon, sun-freckled warm skin",
  "1girl, solo, cotton panties' white waistband one honest beat, wheat-blonde hair breeze-split to mid-back with a trailing silk ribbon, sun-freckled warm skin"),
 ("cotton panties' white waistband flashing one honest beat at the split — the standing hem is the claim, altitude's own tailor",
  "— the standing hem is the claim, altitude's own tailor"),
]
for old,new in moves:
    t=rep(t,old,new,'move: '+old[:50])
io.open(P,'w',encoding='utf-8').write(t)
io.open(S,'w',encoding='utf-8').write(s)
print('FAILS:' if fails else 'ALL OK')
for f in fails: print(' ',f)
