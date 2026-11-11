# -*- coding: utf-8 -*-
"""T5-20 активы: poses 1.11.0 (PL469–PL501), palettes 1.5.0 (P189–P197),
pools 1.4.0 (K285–K317). Камера 1.7.0 уже несёт X5."""
import json

# ── POSES ────────────────────────────────────────────────────────────────
pp = 'specs/poses.json'
d = json.load(open(pp, encoding='utf-8'))
have = {p['id'] for p in d['poses']}
assert not (have & {f'PL{i}' for i in range(469, 502)}), 'пересечение PL-диапазона'

def pose(pid, name, sd, family, risk, cams, use, cat=None):
    return {"id": pid, "name": name, "sd": sd, "category": cat or family,
            "risk": risk, "family": family, "preferred_cams": cams, "use": use}

new = []
# X5 saddle-settle (PL469–477) — cam D3×A03, вес вниз в незримое сиденье
x5 = [
 ("PL469", "Saddle-Settle Armchair", "settling astride the seated point's knees on the armchair facing the lens, knees sinking past the bottom frame corners, weight dropping through the thighs into the unseen seat, hands flat on her own thighs"),
 ("PL470", "Saddle-Settle Office-Chair", "settling astride the seated point's knees on the swivel office chair, the chair giving a slow half-turn under the weight, knees past the bottom corners, hands on her own thighs"),
 ("PL471", "Saddle-Settle Couch-Cushion", "settling astride the seated point's knees over the couch cushion, the cushion swallowing the weight in one slow give, knees past the bottom corners, palms on her own thighs"),
 ("PL472", "Saddle-Settle Bench", "settling astride the seated point's knees on the bench edge facing the lens, knees sinking past the bottom frame corners, weight dropping straight down through the thighs"),
 ("PL473", "Saddle-Settle Bar-Stool", "settling astride the seated point's knees on the tall bar stool, toes short of the floor's rung, the whole weight reading in the bare waist, hands on her own thighs"),
 ("PL474", "Saddle-Settle Floor-Cushion", "settling astride the seated point's knees on the floor cushion facing the lens, knees past the bottom frame corners, one hand raised at the chest, weight sinking through the cushion's give"),
 ("PL475", "Saddle-Settle Bed-Edge", "settling astride the seated point's knees at the bed's edge facing the lens, the mattress taking the weight with a slow dip, knees past the bottom corners, one arm's crook raised to lens height"),
 ("PL476", "Saddle-Settle Desk-Chair", "settling astride the seated point's knees at the desk chair facing the lens, weight dropping into the chair's creak, knees past the bottom corners, hands on her own thighs"),
 ("PL477", "Saddle-Settle Sill", "settling astride the seated point's knees at the deep windowsill facing the lens, knees sinking past the bottom frame corners, weight dropping through the thighs onto the unseen seat"),
]
for pid, name, sd in x5:
    new.append(pose(pid, name + " (X5)", sd, "X5", "MID", ["CAM03"], "V"))

# Мейки (PL478–498)
mains = [
 ("PL478", "Empty-Bracket Perch", "niche_watch", "LOW", ["CAM01"], "N", "curling on the night windowsill beneath the empty lamp bracket, wings folded tight, antennae testing the dark"),
 ("PL479", "Letter-Wind Read", "letter_read", "MID", ["CAM02"], "V", "reading the letter aloud over the grave's stone, one finger holding the line, the wind dragging the page toward the marker"),
 ("PL480", "Pedestal Step-Down", "marker_rise", "MID", ["CAM04"], "N", "stepping down off her own pedestal at night, the hollow of her feet printed in the stone behind, moss shoulders taking the air"),
 ("PL481", "Flooded-Rim Drape", "flood_rim", "MID", ["CAM05"], "V", "hanging in the flooded chapel's stone rim, both arms draped over the edge, chin stacked on crossed wrists, waterline riding the ribs"),
 ("PL482", "Two-Cups Seiza", "cups_seiza", "LOW", ["CAM02"], "N", "kneeling seiza at the low table pouring for two, the second cup full and going cold, ears lowered a beat before the face"),
 ("PL483", "Mound Side-Lounge", "mound_lounge", "MID", ["CAM03"], "V", "lying along the grave mound like a hill of her own, one knee bent, a wrist thrown over the eyes against the first light"),
 ("PL484", "Mid-Turn Shadow-Lead", "shadow_lead", "MID", ["CAM06"], "V", "caught mid-turn: her detached shadow already kneels at the stone with hands folded while she arrives a half-step behind"),
 ("PL485", "Frame-Silk Weave", "silk_frame", "MID", ["CAM02"], "N", "leaning chest-first over the empty coffin-lid used as a frame, drawing the shroud's silk line from her fingertips"),
 ("PL486", "Coffin-Desk Drape", "coffin_drape", "MID", ["CAM02"], "V", "draped across the coffin's lid used as a desk, elbows claiming its polished curve, writing while sunrise walks the grain"),
 ("PL487", "Stair-Skip Bell-Ring", "bell_skip", "LOW", ["CAM06"], "N", "skipping down the bell-tower stairs backward-facing, the collar's bell swinging its own service at every step"),
 ("PL488", "Coat Shrug-Off Window", "coat_shrug", "MID", ["CAM06"], "V", "shrugging the heirloom coat off one shoulder at the rainy window, one arm still in the sleeve that remembers a bigger shoulder"),
 ("PL489", "Bell-Jar Meadow", "bell_jar_meadow", "MID", ["CAM05"], "N", "lying spread in the grave-garden under the glass bell jar, eyes up to the condensation bead, stems bending around her"),
 ("PL490", "Whisper-Name Lean", "name_whisper", "MID", ["CAM01"], "V", "leaning in to read the name off the list to the lens, one finger holding the ink-blot line, dusk glow standing in for the lamp"),
 ("PL491", "Brow-to-Glass Eye-Lock", "mirror_lock", "LOW", ["CAM07"], "V", "leaning brow-to-glass with her own reflection, gaze locked, the empty chair reflected behind her shoulder"),
 ("PL492", "Curtain-Case Swagger", "case_swagger", "MID", ["CAM03"], "V", "shouldering through the velvet curtain with the locked case, the lock warm from carrying, weight hanging a half-beat in the stride"),
 ("PL493", "Umbrella Path-Walk", "path_walk", "LOW", ["CAM02"], "V", "walking the graveyard path under a closed umbrella never opened, a soft pool of warm light moving with her over the gravel"),
 ("PL494", "Rail-Perch Cliff-Count", "cliff_perch", "MID", ["CAM08"], "N", "perching on the lookout rail above the cliffside rows of graves, the rail printing its line, horn-ribs striping the falling light"),
 ("PL495", "Veil Half-Lift Rite", "veil_rite", "MID", ["CAM01"], "V", "lifting the gauze veil halfway to find the viewer through the gap, the corona ring holding the only light"),
 ("PL496", "Stone-Wall Slide-Down", "stone_slide", "MID", ["CAM02"], "V", "sliding down the memorial wall beside the two cut names, palms flat on the stone beside her hips, taking the wall's cold"),
 ("PL497", "Crypt-Slab Display", "slab_display", "LOW", ["CAM05"], "N", "lying on the crypt slab as its own exhibit, one knee bent, the halo ring keeping its line above her hair"),
 ("PL498", "Run-Look-Back Shroud", "shroud_run", "MID", ["CAM06"], "V", "running the linen-line path with the folded shroud on the shoulder and the look-back over it"),
]
for pid, name, fam, risk, cams, use, sd in mains:
    new.append(pose(pid, name, sd, fam, risk, cams, use))

# ОС-карты (PL499–501)
ocs = [
 ("PL499", "Lace-Edge Recline", "reclining along the chaise edge toward the mirror, one wrist raised to the collarbone with a single drop of perfume, the neckline living by gravity"),
 ("PL500", "Puppet-Bodice Levitation", "standing centered with arms held away from her sides by floating conjured palms, one knee bent, chin up, the performer's stillness while the host holds the chest"),
 ("PL501", "Gloss-Slip Stand", "standing in the shallow black gloss pool that holds her upright, one hand slicking the line along the sternum, the tail lifted clear above the surface"),
]
for pid, name, sd in ocs:
    new.append(pose(pid, name, sd, "OC_T5-20", "MID", ["CAM02"], "N", cat="OC_T5-20"))

d['poses'].extend(new)
d['version'] = '1.11.0'
d['changelog'].insert(0, "2026-11-13 — 1.11.0 T5-20: +PL469–PL477 (X5 saddle-settle, 9), +PL478–PL498 "
    "(мейки unburied_watch/unburied_duty, 21), +PL499–PL501 (OC_T5-20: Vae/Meine/Hana карты, 3)")
fam = d['family_counts']
for k, n in [("X5", 9), ("unburied_watch", 8), ("unburied_duty", 13), ("OC_T5-20", 3)]:
    fam[k] = fam.get(k, 0) + n
d['first_use_ledger']['T5-20'] = [f'PL{i}' for i in range(469, 502)]
json.dump(d, open(pp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('poses 1.11.0: +', len(new))

# ── PALETTES ─────────────────────────────────────────────────────────────
pp = 'specs/palettes.json'
d = json.load(open(pp, encoding='utf-8'))
have = {p['id'] for p in d['palettes']}
assert not (have & {f'P{i}' for i in range(189, 198)})
wave = [
 ("P189_PORCELAIN_CRACK", "Porcelain Crack", "bisque-porcelain pale with kintsugi-gold crack lines, seal-red painted accent, hairline-silver seams", "exp_color_wave_5"),
 ("P190_POND_GLASS", "Pond Glass", "aqua-emerald translucent over deep-water base, cyan core-glow, refraction rings", "exp_color_wave_5"),
 ("P191_EMBER_PILLOW", "Ember Pillow", "ash-warm grey over coal-orange, ember-glow accents, heat-shimmer edge", "exp_color_wave_5"),
 ("P192_BRONZE_COIL", "Bronze Coil", "burnished bronze over olive-green, patina-sheen, gold scale accents", "exp_color_wave_5"),
 ("P193_CHESTNUT_TAP", "Chestnut Tap", "chestnut-brown warm over drum-leather, cream stripe accents, maple-syrup glow", "exp_color_wave_5"),
 ("P194_CALICO_COIN", "Calico Coin", "calico-white warm over coin-gold, red-cord accent, amber-glow", "exp_color_wave_5"),
 ("P195_HEARSE_GLASS", "Hearse Glass", "night-green glass over silver-sheen, lace-ribbon black accent, moonlit-pale edge", "exp_color_wave_5"),
 ("P196_INK_LETHE", "Ink Lethe", "ink-black gloss over paper-white, cyan inner-glow accent, teal rim", "exp_color_wave_5"),
 ("P197_WILLOW_MORN", "Willow Morn", "willow-green over morning-cream, silver-dew accents, pollen-gold", "exp_color_wave_5"),
]
for pid, name, sd, fam in wave:
    d['palettes'].append({"id": pid, "name": name,
        "dominant": [sd.split(' over ')[0]], "secondary": [], "accent1": [], "accent2": None,
        "shadow": None, "forbidden": ["washed-out", "muddy-grey"], "light_type": "batch-declared",
        "sd_fragment": sd, "mood": "EXP candidate register", "family": fam,
        "legacy_3slot": False, "source": "T5-20 EXP-оверлей (exp_color_wave_5, 9 разных семей)"})
d['version'] = '1.5.0'
json.dump(d, open(pp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('palettes 1.5.0: +9')

# ── KINETICS ─────────────────────────────────────────────────────────────
pp = 'specs/pools.json'
d = json.load(open(pp, encoding='utf-8'))
have = {k['id'] for k in d['sections']['kinetics_k']}
assert not (have & {f'K{i}' for i in range(285, 318)})
kmids = [
 ("K285", "mid_perfume_wrist", "the perfume drop already on the inner wrist, the mirror's second angle waiting"),
 ("K286", "mid_hand_host", "the host of conjured palms holding the chest, the newest palm still trembling"),
 ("K287", "mid_gloss_second_skin", "the gloss line level at the collarbone, the tail's tip swaying above the surface"),
 ("K288", "mid_moth_empty_bracket", "the antennae testing the dark where the light used to live"),
 ("K289", "mid_letter_wind", "the page bending toward the stone like it wants to be heard there"),
 ("K290", "mid_pedestal_step", "the hollow of her feet still printed in the pedestal stone behind"),
 ("K291", "mid_flooded_rim", "the waterline riding her ribs while the dome's broken light moves"),
 ("K292", "mid_two_cups", "the second cup already full and going cold, ears lowered first"),
 ("K293", "mid_mound_lounge", "the grass keeping her warmth in the shape of her rest"),
 ("K294", "mid_shadow_lead", "the shadow kneeling at the stone half a beat before her"),
 ("K295", "mid_silk_frame", "the silk line drawn from the fingertips in one even count"),
 ("K296", "mid_coffin_desk", "sunrise walking the lid's grain like a ruler under the letter"),
 ("K297", "mid_bell_skip", "the collar bell swinging its own service step by step"),
 ("K298", "mid_coat_shrug", "the sleeve remembering a bigger shoulder as the lapel slides"),
 ("K299", "mid_bell_jar_meadow", "the condensation bead hanging over her heart under the dome"),
 ("K300", "mid_name_whisper", "the finger holding the ink-blot where the hand had hurried"),
 ("K301", "mid_mirror_lock", "the reflected strap fallen where the real one holds"),
 ("K302", "mid_case_swagger", "the case's strap riding the apex at every step's bounce"),
 ("K303", "mid_path_walk", "the soft pool of light moving with her over the gravel"),
 ("K304", "mid_cliff_perch", "the horn-ribs striping the falling light down the slope"),
 ("K305", "mid_veil_rite", "the corona ring holding the only light of the rite"),
 ("K306", "mid_stone_slide", "the dew stripe walking her tank as she takes the wall's cold"),
 ("K307", "mid_slab_display", "the halo keeping its line above the hair on the slab"),
 ("K308", "mid_shroud_run", "the shroud roll's chest strap counting the stride"),
 ("K309", "mid_saddle_armchair", "the pinafore caught and dragged up between the thighs by the settle"),
 ("K310", "mid_saddle_office", "the chair giving a slow half-turn under the weight"),
 ("K311", "mid_saddle_couch", "the cushion swallowing the weight in one slow give"),
 ("K312", "mid_saddle_bench", "the waistband dragged honest along the settle's line"),
 ("K313", "mid_saddle_stool", "the toes short of the floor's rung, the weight bare at the waist"),
 ("K314", "mid_saddle_cushion", "the raised paw swinging its patient pendulum"),
 ("K315", "mid_saddle_bed", "the carried head raised to lens height in the arm's crook"),
 ("K316", "mid_saddle_desk", "the black halo spreading under the unseen seat"),
 ("K317", "mid_saddle_sill", "the willow branches resting their weight on the frame"),
]
for kid, name, sd in kmids:
    d['sections']['kinetics_k'].append({"id": kid, "name": name, "sd": sd,
        "source": "T5-20 K-FF wave (мейки K288–K308, EXP K309–K317, ОС K285–K287)"})
d['version'] = '1.4.0'
json.dump(d, open(pp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('pools 1.4.0: +33 K')
