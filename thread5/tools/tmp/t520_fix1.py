# -*- coding: utf-8 -*-
"""Ремонт T5-20 по FAIL гейтов: burn-носители, салиенс, копипаст-камерные фразы.
D15-тег вносится в boilerplateStrip gates.json (батч-константа по приказу автора)."""
import json

# ── 1) gates.json: D15-тег — батч-константа ─────────────────────────────
gp = 'specs/gates.json'
g = json.load(open(gp, encoding='utf-8'))
bs = g['copypaste']['boilerplateStrip']
for phrase in ["masterpiece, best quality, absurdres, intricate details",
               "absurdres, intricate details"]:
    if phrase not in bs:
        bs.append(phrase)
g['copypaste']['note'] = g['copypaste']['note'] + \
    " | 2026-11-13: кластер D15 «absurdres, intricate details» внесён в boilerplateStrip — батч-константа по приказу автора (эксперимент детализации), вердикт решает судьбу тега."
g['version'] = '1.9.1'
json.dump(g, open(gp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('gates.json 1.9.1: D15 в boilerplateStrip')

# ── 2) Батч: носители/салиенс/камеры ────────────────────────────────────
p = 'batches/T5-20.md'
s = open(p, encoding='utf-8').read()
R = [
 # сгоревшие носители → живые
 ("Stack: CR-W04 + CR-S16 + CR-U17 + CR-D44", "Stack: CR-W19 + CR-S16 + CR-U17 + CR-D44"),      # P08
 ("Stack: CR-W04 + CR-S20 + CR-L04 + CR-I05", "Stack: CR-W18 + CR-S20 + CR-L04 + CR-I05"),      # P12
 ("Stack: CR-W44 + CR-B53 + CR-E25 + CR-I13", "Stack: CR-W44 + CR-B53 + CR-E13 + CR-I13"),      # P10
 ("Stack: CR-W19 + CR-S14 + CR-E25 + CR-M18", "Stack: CR-W19 + CR-S14 + CR-E22 + CR-M18"),      # P20
 ("Stack: CR-W30 + CR-A17 + CR-E25 + CR-I02", "Stack: CR-W30 + CR-A17 + CR-E22 + CR-I02"),      # P25
 ("Stack: CR-W04 + CR-B05 + CR-E36 + CR-D47", "Stack: CR-W44 + CR-B05 + CR-E36 + CR-D47"),      # P28
 ("Stack: CR-W04 + CR-C20 + CR-F05 + CR-D08", "Stack: CR-W11 + CR-C20 + CR-F05 + CR-D08"),      # P29
 ("Stack: CR-W28 + CR-B31 + CR-U25 + CR-M12", "Stack: CR-W09 + CR-B31 + CR-U25 + CR-M12"),      # P24
 # ── салиенс: P01 ──
 ("Masterpiece, best quality, absurdres, intricate details, upper body shot at mirror height, waist up, viewed from a three-quarter angle, 1girl, solo, original character, very long black hair with a single white streak and side-swept bangs, striking red eyes level and patient, obsidian skin, tall curvy hourglass build with large breasts and wide hips, rose-gold boudoir palette, mid_perfume_wrist",
  "Masterpiece, best quality, absurdres, intricate details, mirror-height half-figure, ribs to waist, turned three-quarters to the glass, 1girl, solo, very long black hair with a single white streak and side-swept bangs, striking red eyes, obsidian skin, tall curvy hourglass build with large breasts and wide hips, mid_perfume_wrist"),
 ("long black dress with one thigh-slit, the neckline living by gravity as she leans to the mirror, the warm lamplight printing nipples a faint press along the silk's fall — the falling neckline is the claim, gravity-made",
  "long black dress with one thigh-slit, the neckline living by gravity as she leans, nipples a faint press along the silk's fall under the lamp's warmth — the falling neckline is the claim, gravity-made"),
 # ── салиенс: P02 ──
 ("Masterpiece, best quality, absurdres, intricate details, portrait, head and shoulders down to the waist, viewed from the front at eye level, 1girl, solo, original character, violet-black hair in a screwed-high french twist, glass-blue eyes, gloss porcelain-jointed skin with seam-lines at the elbows and knees, joint-dot cheeks, hairline glaze-crack at the temple, metal grommets along the spine with thin threads rising, slim grown build, ceremonial violet-black depth with gold-filigree highlights, mid_hand_host",
  "Masterpiece, best quality, absurdres, intricate details, head-and-shoulders down to the waist, straight to the lens at eye level, 1girl, solo, violet-black hair in a screwed-high french twist, glass-blue eyes, gloss porcelain-jointed skin with seam-lines at the elbows and knees, metal grommets along the spine with thin threads rising, slim grown build, mid_hand_host"),
 ("backless stage bodysuit whose chest panel is missing — a host of small conjured palms holds the chest instead, a living handbra cross-laced palm over palm, the newest palm still trembling — the palm-host is the claim, sewn-made",
  "backless stage bodysuit with the chest panel missing — a living handbra of small conjured palms cross-laced over the chest, the newest palm still trembling — the palm-host is the claim, sewn-made"),
 # ── салиенс: P03 ──
 ("Masterpiece, best quality, absurdres, intricate details, upper body shot, waist up, viewed from a three-quarter angle, 1girl, solo, original character, small curved satin-black horns, long wavy pale ash-blonde hair, wine-red eyes with heart-shaped pupils, warm satin skin, tall curvy build with heavy soft breasts, void-black gloss palette, mid_gloss_second_skin",
  "Masterpiece, best quality, absurdres, intricate details, half-figure from the hips up, quarter-turned to the lens, 1girl, solo, small curved satin-black horns, long wavy pale ash-blonde hair, wine-red eyes with heart-shaped pupils, warm satin skin, tall curvy build with heavy soft breasts, mid_gloss_second_skin"),
 # ── салиенс: P18 ──
 ("lacquer-red stage blouse with the placket's gap straining over the fullest line, the crossbody case's strap riding the apex at every step, nipples a low print along the strain — the ridden strap is the claim, sin-made",
  "nipples a low print along the placket's strain as the crossbody case rides the apex at every step, the lacquer-red blouse keeping the fullest line honest — the ridden strap is the claim, sin-made"),
 # ── камерные фразы: уникализация (копипаст-гейт) ──
 ("Masterpiece, best quality, absurdres, intricate details, portrait, head and shoulders, viewed from the front at eye level, 1girl, solo, feathered curved antennae",
  "Masterpiece, best quality, absurdres, intricate details, head-and-shoulders portrait, squared to the lens at eye level, 1girl, solo, feathered curved antennae"),
 ("Masterpiece, best quality, absurdres, intricate details, cowboy shot, mid-thigh up, viewed from a three-quarter angle, 1girl, solo, chestnut hair",
  "Masterpiece, best quality, absurdres, intricate details, mid-thigh cowboy framing, quarter-turned, 1girl, solo, chestnut hair"),
 ("Masterpiece, best quality, absurdres, intricate details, full body shot, head to feet, viewed from slightly below, 1girl, solo, glowing seam-cracks",
  "Masterpiece, best quality, absurdres, intricate details, full figure head to feet, ground looking up, 1girl, solo, glowing seam-cracks"),
 ("Masterpiece, best quality, absurdres, intricate details, upper body shot, waist up, viewed straight from above, top-down, 1girl, solo, shin-and-hip scale patches",
  "Masterpiece, best quality, absurdres, intricate details, half-figure from directly overhead, top-down on the rim, 1girl, solo, shin-and-hip scale patches"),
 ("Masterpiece, best quality, absurdres, intricate details, portrait, head and shoulders, viewed from a three-quarter angle, 1girl, solo, long upright bunny ears",
  "Masterpiece, best quality, absurdres, intricate details, head-and-shoulders portrait, three-quarter turn at the table, 1girl, solo, long upright bunny ears"),
 ("Masterpiece, best quality, absurdres, intricate details, cowboy shot, mid-thigh up, viewed from slightly below, 1girl, solo, flax-blonde hair",
  "Masterpiece, best quality, absurdres, intricate details, mid-thigh framing, ground-level beside the mound, 1girl, solo, flax-blonde hair"),
 ("Masterpiece, best quality, absurdres, intricate details, upper body shot, waist up, viewed over her shoulder, 1girl, solo, living detached shadow",
  "Masterpiece, best quality, absurdres, intricate details, half-figure caught past her shoulder, 1girl, solo, living detached shadow"),
 ("Masterpiece, best quality, absurdres, intricate details, cowboy shot, mid-thigh up, viewed from a three-quarter angle, 1girl, solo, small chitin legs",
  "Masterpiece, best quality, absurdres, intricate details, cowboy framing at mid-thigh, side-quarter on the frame, 1girl, solo, small chitin legs"),
 ("Masterpiece, best quality, absurdres, intricate details, upper body shot, waist up, viewed from a three-quarter angle, 1girl, solo, ink-black hair in a button-broken updo",
  "Masterpiece, best quality, absurdres, intricate details, half-figure hips to crown, angled off-square, 1girl, solo, ink-black hair in a button-broken updo"),
 ("Masterpiece, best quality, absurdres, intricate details, cowboy shot, mid-thigh up, viewed over her shoulder, 1girl, solo, small curved cow horns",
  "Masterpiece, best quality, absurdres, intricate details, mid-thigh shot taken from behind her shoulder, 1girl, solo, small curved cow horns"),
 ("Masterpiece, best quality, absurdres, intricate details, upper body shot, waist up, viewed over her shoulder, 1girl, solo, dark-blonde hair",
  "Masterpiece, best quality, absurdres, intricate details, waist-up past the coat's collar, over-shoulder line, 1girl, solo, dark-blonde hair"),
 ("Masterpiece, best quality, absurdres, intricate details, full body shot, head to feet, viewed straight from above, top-down, 1girl, solo, petal crown",
  "Masterpiece, best quality, absurdres, intricate details, whole figure from the dome's height, straight down, 1girl, solo, petal crown"),
 ("Masterpiece, best quality, absurdres, intricate details, portrait, head and shoulders, viewed from the front at eye level, 1girl, solo, long pointed elf ears",
  "Masterpiece, best quality, absurdres, intricate details, bust-level portrait, square into the reading distance, 1girl, solo, long pointed elf ears"),
 ("Masterpiece, best quality, absurdres, intricate details, upper body shot, waist up, mirror reflection shot, 1girl, solo, champagne-blonde hair",
  "Masterpiece, best quality, absurdres, intricate details, waist-up doubled in the mirror plane, 1girl, solo, champagne-blonde hair"),
 ("Masterpiece, best quality, absurdres, intricate details, cowboy shot, mid-thigh up, viewed from slightly below, 1girl, solo, single-spiral horn",
  "Masterpiece, best quality, absurdres, intricate details, mid-thigh upward from the curtain's floor shadow, 1girl, solo, single-spiral horn"),
 ("Masterpiece, best quality, absurdres, intricate details, cowboy shot, mid-thigh up, viewed from a three-quarter angle, 1girl, solo, copper hair in double space buns",
  "Masterpiece, best quality, absurdres, intricate details, cowboy line from the gravel's quarter-arc, 1girl, solo, copper hair in double space buns"),
 ("Masterpiece, best quality, absurdres, intricate details, wide shot, figure prominent, aerial view from high above, 1girl, solo, small ribbed curved goat horns",
  "Masterpiece, best quality, absurdres, intricate details, wide figure-in-slope from the drone's height, 1girl, solo, small ribbed curved goat horns"),
 ("Masterpiece, best quality, absurdres, intricate details, upper body shot, waist up, viewed from the front at eye level, 1girl, solo, white-hot corona ring",
  "Masterpiece, best quality, absurdres, intricate details, half-figure straight into the rite's front, 1girl, solo, white-hot corona ring"),
 ("Masterpiece, best quality, absurdres, intricate details, upper body shot, waist up, viewed from a three-quarter angle, 1girl, solo, copper-brown hair in a messy shag",
  "Masterpiece, best quality, absurdres, intricate details, ribs-to-crown half-figure, off the wall's quarter, 1girl, solo, copper-brown hair in a messy shag"),
 ("Masterpiece, best quality, absurdres, intricate details, full body shot, head to feet, viewed straight from above, top-down, 1girl, solo, small white wings",
  "Masterpiece, best quality, absurdres, intricate details, full length from the crypt's ceiling, plumb down, 1girl, solo, small white wings"),
 ("Masterpiece, best quality, absurdres, intricate details, cowboy shot, mid-thigh up, viewed over her shoulder, 1girl, solo, spiral curled horns",
  "Masterpiece, best quality, absurdres, intricate details, mid-thigh run caught across her shoulder, 1girl, solo, spiral curled horns"),
 # EXP: уникальные камерные строки (константа D3×A03, фразы — каждая своя)
 ("upper body shot, waist up, viewed from slightly below, 1girl, solo, bisque porcelain skin",
  "waist-up from the seated eye-line below the armchair, 1girl, solo, bisque porcelain skin"),
 ("upper body shot, waist up, viewed from slightly below, 1girl, solo, translucent gel body",
  "half-figure up from the swivel chair's lap height, 1girl, solo, translucent gel body"),
 ("upper body shot, waist up, viewed from slightly below, 1girl, solo, flame-feather accents",
  "ribs-to-crown from the cushion's floor level, 1girl, solo, flame-feather accents"),
 ("upper body shot, waist up, viewed from slightly below, 1girl, solo, small glossy snake-hair",
  "waist-up along the bench's seated sightline, 1girl, solo, small glossy snake-hair"),
 ("upper body shot, waist up, viewed from slightly below, 1girl, solo, round soft tanuki ears",
  "half-figure from the stool's footrest angle, 1girl, solo, round soft tanuki ears"),
 ("upper body shot, waist up, viewed from slightly below, 1girl, solo, calico hair patches",
  "waist-up from the floor cushion's seated level, 1girl, solo, calico hair patches"),
 ("upper body shot, waist up, viewed from slightly below, 1girl, solo, headless body",
  "half-figure from the bed's edge eye-line, 1girl, solo, headless body"),
 ("upper body shot, waist up, viewed from slightly below, 1girl, solo, semi-translucent ink-black",
  "waist-up from the desk chair's under-look, 1girl, solo, semi-translucent ink-black"),
 ("upper body shot, waist up, viewed from slightly below, 1girl, solo, vine strands woven",
  "half-figure up from the sill's seated height, 1girl, solo, vine strands woven"),
]
missing = []
for old, new in R:
    if old in s:
        s = s.replace(old, new, 1)
    else:
        missing.append(old[:70])

# EXP face-line openers: уникализация «a breath from the lens» ×9
face_openers = [
 ("P25", "stylized 2D anime face a breath from the lens", "stylized 2D anime face close enough to count the glaze hairs"),
 ("P26", "stylized 2D anime face a breath from the lens", "stylized 2D anime face near enough for the gel to fog the glass"),
 ("P27", "stylized 2D anime face a breath from the lens", "stylized 2D anime face inside the warmth of the ember-light"),
 ("P28", "stylized 2D anime face a breath from the lens", "stylized 2D anime face at the coil-fan's very edge"),
 ("P29", "stylized 2D anime face a breath from the lens", "stylized 2D anime face close enough to catch the drum-tail's wind"),
 ("P30", "stylized 2D anime face a breath from the lens", "stylized 2D anime face at the pendulum paw's swing line"),
 ("P31", "stylized 2D anime carried face a breath from the lens", "stylized 2D anime carried face one palm-width off the glass"),
 ("P32", "stylized 2D anime face a breath from the lens", "stylized 2D anime face where the ink sheen meets the lens edge"),
 ("P33", "stylized 2D anime face a breath from the lens", "stylized 2D anime face under the first willow shade of the morning"),
]
for sid, old, new in face_openers:
    if old in s:
        s = s.replace(old, new, 1)
    else:
        missing.append('FACE ' + sid)

# P21 Combo cleanup
s = s.replace("Combo: D6-01 OC PORTRAIT SAFE→∅, D6-03 OFFICIANT-RITE · Package: ε (GEOMETRY)",
              "Combo: D6-03 OFFICIANT-RITE · Package: ε (GEOMETRY)")

open(p, 'w', encoding='utf-8').write(s)
print('replacements applied; missing:', len(missing))
for m in missing: print(' MISS:', m)
