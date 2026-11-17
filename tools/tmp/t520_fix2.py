# -*- coding: utf-8 -*-
"""T5-20 ремонт 2: салиенс (P01/P02/P03/P21), EXP-копипаст (уникальные settle-фразы),
char-spec F-016 (стемы цветов по lexicon гейта)."""
p = 'batches/T5-20.md'
s = open(p, encoding='utf-8').read()
R = []

# ── салиенс ──
R += [
 ("long black dress with one thigh-slit, the neckline living by gravity as she leans, nipples a faint press along the silk's fall under the lamp's warmth — the falling neckline is the claim, gravity-made",
  "long black dress with one thigh-slit, nipples a faint press along the silk's fall where the neckline lives by gravity — the falling neckline is the claim, gravity-made"),
 ("Masterpiece, best quality, absurdres, intricate details, head-and-shoulders down to the waist, straight to the lens at eye level, 1girl, solo, violet-black hair in a screwed-high french twist, glass-blue eyes, gloss porcelain-jointed skin with seam-lines at the elbows and knees, metal grommets along the spine with thin threads rising, slim grown build, mid_hand_host",
  "Masterpiece, best quality, absurdres, intricate details, head-and-shoulders, straight to the lens at eye level, 1girl, solo, violet-black hair in a screwed-high french twist, glass-blue eyes, gloss porcelain-jointed skin, metal grommets along the spine with thin threads rising, slim grown build, mid_hand_host"),
 ("backless stage bodysuit with the chest panel missing — a living handbra of small conjured palms cross-laced over the chest, the newest palm still trembling — the palm-host is the claim, sewn-made",
  "backless stage bodysuit, chest panel missing — a living handbra of conjured palms cross-laced over the chest, the newest palm still trembling — the palm-host is the claim, sewn-made"),
 ("she stands centered with arms held away from her sides by two more floating palms, one knee bent, chin up, the performer's stillness while the host does the touching",
  "she stands centered with arms held away from her sides by two more floating palms, one knee bent, chin up, the elbow seam-lines catching gold while the host does the touching"),
 ("Masterpiece, best quality, absurdres, intricate details, half-figure from the hips up, quarter-turned to the lens, 1girl, solo, small curved satin-black horns",
  "Masterpiece, best quality, absurdres, intricate details, half-figure from the hips up, 1girl, solo, small curved satin-black horns"),
 ("a second skin of black gloss poured to the collarbone, every curve printed by the shine, breast shape read whole through the mirror-sheen, the covering line level at the collarbone — the gloss is the claim, poured-made",
  "a second skin of black gloss poured to the collarbone, breast shape printed whole by the mirror-sheen, the covering line level at the throat — the gloss is the claim, poured-made"),
 ("Masterpiece, best quality, absurdres, intricate details, half-figure straight into the rite's front, 1girl, solo, white-hot corona ring light as a halo, black gauze veil mid-lift, exposed nape, mourning robe of heavy black velvet, jet-black hair in a veil-wrapped crown braid, cool pale skin, young solemn build, mid_veil_rite",
  "Masterpiece, best quality, absurdres, intricate details, half-figure straight into the rite's front, 1girl, solo, white-hot corona ring light as a halo, black gauze veil mid-lift, mourning robe of heavy black velvet, jet-black hair in a veil-wrapped crown braid, cool pale skin, mid_veil_rite"),
 ("heavy mourning velvet with the neckline living by gravity, the strapless war running quiet beneath, nipples a cold print against the velvet's pile — the gravity line is the rite, self-made",
  "heavy mourning velvet, nipples a cold print against the pile where the neckline lives by gravity, the strapless war quiet beneath — the gravity line is the rite, self-made"),
 ("she lifts the gauze veil halfway to find the viewer through the gap, the corona ring holding the only light while the bell's ring still stands in the air's lines around her",
  "she lifts the gauze veil halfway to find the viewer through the gap, the corona ring holding the only light, the veil's lift leaving the nape bare to the rite's cold"),
]

# ── char-spec: стемы ──
R += [
 # P06 golem: ember eyes
 ("slender kiln-ceramic build, pale-grey hair in a straight-cut long bob, young lithe build, mid_pedestal_step",
  "slender kiln-ceramic build, pale-grey hair in a straight-cut long bob, ember eyes, young lithe build, mid_pedestal_step"),
 ("stylized 2D anime face turning from the pedestal, anime eyes (copper, patient-lit)",
  "stylized 2D anime face turning from the pedestal, anime eyes (ember, kiln-patient)"),
 # P08 bunny: honey + curls
 ("honey-blonde bedhead waves, young soft build, mid_two_cups",
  "honey-blonde hair in loose bedhead curls, young soft build, mid_two_cups"),
 ("the gold square holding the waves.", "the gold square holding the curls."),
 # P10 shadow: graphite eyes
 ("smoke-grey hair in layered cut, young wiry build, mid_shadow_lead",
  "smoke-grey hair in layered cut, graphite eyes, young wiry build, mid_shadow_lead"),
 # P13 cow: skin
 ("auburn hair in twin loose braids, young sturdy build, mid_bell_skip",
  "auburn hair in twin loose braids, warm tan skin, young sturdy build, mid_bell_skip"),
 # P20 goat: honey eyes
 ("sandy-blonde hair in a wind-lifted shag, young sturdy build, mid_cliff_perch",
  "sandy-blonde hair in a wind-lifted shag, honey eyes, young sturdy build, mid_cliff_perch"),
 ("anime eyes (brass, horizontal-pupiled calm)", "anime eyes (honey, horizontal-pupiled calm)"),
 # P25 doll: pearl-grey hair
 ("pale taupe hair in twin braids, slight doll-slender build",
  "pearl-grey hair in twin braids, slight doll-slender build"),
 ("the gold crack holding the braids.", "the gold crack holding the twin braids."),
 # P26 slime: turquoise hair + cyan eyes
 ("semi-liquid aquamarine hair dripping slow, glowing core-orb inside the chest, glossy dark eyes",
  "semi-liquid turquoise hair dripping slow, glowing core-orb inside the chest, glossy cyan eyes"),
 ("anime eyes (deep-water, refract-calm)", "anime eyes (cyan, refract-calm)"),
 # P29 tanuki: honey eyes
 ("chestnut hair in tight ringlets, warm brown skin, young cozy build, mid_saddle_stool",
  "chestnut hair in tight ringlets, warm brown skin, honey eyes, young cozy build, mid_saddle_stool"),
 ("anime eyes (warm chestnut, tap-bright)", "anime eyes (honey, tap-bright)"),
 # P30 fortune-cat: ginger hair
 ("calico hair patches, gold bell on a red cord collar",
  "calico-patched ginger hair, gold bell on a red cord collar"),
 # P32 ink-slime: turquoise twin-tails + graphite eyes
 ("cyan inner glow at the chest, teal twin-tails holding the air, glossy dark eyes",
  "cyan inner glow at the chest, turquoise hair in twin-tails holding the air, graphite eyes"),
 ("anime eyes (ink-dark, cyan-lit)", "anime eyes (graphite, cyan-lit)"),
]

# ── EXP: уникальные settle-фразы (L3) + вариации claim-фраз ──
R += [
 ("she settles astride the seated viewer's knees facing the lens, knees sinking past the bottom frame corners, both hands flat on her own thighs while the chair's leather cools under her palms",
  "she folds down astride the seated viewer's knees, knees dropping past the frame's lower corners, both hands flat on her own thighs while the chair's leather cools under her palms"),
 ("she settles astride the seated viewer's knees facing the lens, the office chair giving a slow half-turn under the weight, gel dripping in slow beads past her waist toward the unseen seat",
  "she pours herself down over the seated viewer's knees, the chair turning its slow half-mile under her, gel beads running past her waist for the unseen seat"),
 ("she settles astride the seated viewer's knees facing the lens, the cushion swallowing her weight in one slow give, ash-flakes landing their even count on the armrests",
  "she sinks onto the seated viewer's lap astride the cushion, the weight landing in one slow swallow, ash-flakes landing their even count on the armrests"),
 ("she settles astride the seated viewer's knees on the bench edge facing the lens, knees sinking past the bottom frame corners, the snake coils fanning wide of her face so nothing hides the eyes",
  "she claims the seated viewer's lap on the bench edge, knees lowering past the frame's bottom corners, the snake coils fanning wide of her face so nothing hides the eyes"),
 ("she settles astride the seated viewer's knees on the tall bar stool facing the lens, toes short of the floor's rung, the striped tail slapping the armrest in the settle's own rhythm",
  "she lands astride the seated viewer's knees on the tall stool, toes short of the floor's rung, the striped tail slapping the armrest in the settle's own rhythm"),
 ("she settles astride the seated viewer's knees on the floor cushion facing the lens, knees sinking past the bottom frame corners, the raised paw swinging its patient pendulum while the bell keeps the count",
  "she folds astride the seated viewer's knees onto the floor cushion, knees slipping past the bottom corners, the raised paw swinging its patient pendulum while the bell keeps the count"),
 ("she settles astride the seated viewer's knees at the bed's edge facing the lens, raising her own head to the lens height in the crook of her arm while the body finds its balance a half-beat late",
  "she balances astride the seated viewer's knees at the bed's edge, the mattress dipping, her carried head raised to the lens in the arm's crook while the body finds its balance a half-beat late"),
 ("she settles astride the seated viewer's knees at the desk chair facing the lens, ink beading down her thighs into a slow black halo spreading under the unseen seat",
  "she spreads astride the seated viewer's knees at the desk chair, ink beading down her thighs into a slow black halo pooling under the unseen seat"),
 ("she settles astride the seated viewer's knees at the deep sill facing the lens, knees sinking past the bottom frame corners, willow branches from her hair resting their weight on the frame",
  "she roots herself astride the seated viewer's knees at the deep sill, knees passing the frame's lower corners, willow branches from her hair resting their weight on the frame"),
 # claim-фразы-дубли
 ("waffle-knit lounge wrap with the hem singed soft by the wing-roots, pressed flat by the settle, nipples a low print along the knit's press — the pressed singe is the claim, heat-made",
  "waffle-knit lounge wrap with the hem singed soft by the wing-roots, pressed flat by the settle, nipples a low press under the knit's weight — the pressed singe is the claim, heat-made"),
 ("lace-trimmed nightgown dragged high between the straddling thighs by the settle, the lace ribbon at the neckline catching the green glass light, nipples a low print along the gown's thin fall — the dragged lace is the claim, weight-made",
  "lace-trimmed nightgown pulled up over the straddling thighs by the settle, the lace ribbon at the neckline catching the green glass light, nipples a cold print beneath the gown's thin fall — the pulled lace is the claim, weight-made"),
 ("short kimono robe gone loose at the settle, the hem dragged high between the straddling thighs, visible pantyline honest along the settle's print — the dragged hem is the claim, fortune-made",
  "short kimono robe gone loose at the settle, the hem dragged up between the straddling legs, visible pantyline honest along the settle's print — the raised hem is the claim, fortune-made"),
 ("willow-green slip dragged high between the straddling thighs by the settle, the hem's morning damp pressing flat, nipples a low print along the slip's thin ride — the dragged hem is the claim, root-made",
  "willow-green slip pulled up over the straddling thighs by the settle, the hem's morning damp pressing flat, nipples a soft print under the slip's thin ride — the pulled hem is the claim, root-made"),
]

missing = []
for old, new in R:
    if old in s:
        s = s.replace(old, new, 1)
    else:
        missing.append(old[:64])
open(p, 'w', encoding='utf-8').write(s)
print('fix2 applied; missing:', len(missing))
for m in missing: print(' MISS:', m)
