#!/usr/bin/env python3
# T5-18 REVERSE WONDERLAND — заливка реестров
import json, io

BASE = '/home/z/my-project/thread5/specs/'

def load(f):
    with io.open(BASE + f, 'r', encoding='utf-8') as fh:
        return json.load(fh)

def save(f, d):
    with io.open(BASE + f, 'w', encoding='utf-8') as fh:
        json.dump(d, fh, ensure_ascii=False, indent=1)
        fh.write('\n')

NEW_POSES = [
 {"id":"PL400","name":"Upward-Pour Catch","sd":"standing with head tilted back, catching an upward-pouring stream from the teapot in a raised cup, sleeves fallen back along the forearms","category":"erotic_presentation_v2","risk":"MID","family":"main","preferred_cams":["CAM06"],"use":"N","source":"first-use T5-18 REVERSE WONDERLAND (custom card)"},
 {"id":"PL401","name":"Mid-Air Stair Stride","sd":"mid-stride up invisible stairs above the broken staircase, laundry basket on the hip, hem mid-swing","category":"dynamic_v2","risk":"MID","family":"main","preferred_cams":["CAM04"],"use":"NV","source":"first-use T5-18 REVERSE WONDERLAND (custom card)"},
 {"id":"PL402","name":"Un-Rain Stand-Still","sd":"standing in rain rising from the ground to the sky, chin lifted, arms loose, thin shirt drying upward","category":"erotic_presentation_v2","risk":"MID","family":"main","preferred_cams":["CAM02"],"use":"V","source":"first-use T5-18 REVERSE WONDERLAND (custom card)"},
 {"id":"PL403","name":"Backward-Alarm Reach","sd":"half-awake on one elbow, reaching to set the clock's alarm backward, the minute hand running under her fingertip","category":"micropose_expression","risk":"LOW","family":"main","preferred_cams":["CAM01"],"use":"N","source":"first-use T5-18 REVERSE WONDERLAND (custom card)"},
 {"id":"PL404","name":"Self-Dealing Fan","sd":"shuffling cards with one hand against her hip, the deck fanning and dealing itself across the checker floor, a card tucked at her collar","category":"performance_mirror","risk":"MID","family":"main","preferred_cams":["CAM06"],"use":"V","source":"first-use T5-18 REVERSE WONDERLAND (custom card)"},
 {"id":"PL405","name":"Garden Prune Stand","sd":"standing among self-working shears, accepting a cup of tea from the rose bush, thorn-vine curled loose around her ankle","category":"env_interaction","risk":"LOW","family":"main","preferred_cams":["CAM06"],"use":"V","source":"first-use T5-18 REVERSE WONDERLAND (custom card)"},
 {"id":"PL406","name":"Outside-Key Door Pull","sd":"pulling a door that opens from the wrong side, hip braced against the jamb, the key turning itself above her hand","category":"env_interaction","risk":"MID","family":"main","preferred_cams":["CAM02"],"use":"V","source":"first-use T5-18 REVERSE WONDERLAND (custom card)"},
 {"id":"PL407","name":"Delayed-Mirror Wait","sd":"standing at the mirror, arms crossed, watching her reflection catch up three seconds late","category":"base","risk":"LOW","family":"main","preferred_cams":["CAM11"],"use":"N","source":"first-use T5-18 REVERSE WONDERLAND (custom card)"},
 {"id":"PL408","name":"Ceiling-Sweep Balancer","sd":"balancing on a lifted broom handle above the floor, sweeping dust off the ceiling-floor, skirt falling toward the sky","category":"dynamic_v2","risk":"MID","family":"main","preferred_cams":["CAM04"],"use":"V","source":"first-use T5-18 REVERSE WONDERLAND (custom card)"},
 {"id":"PL409","name":"Self-Writing Letter Reader","sd":"seated on the desk edge, reading a letter as the ink crawls itself across the page toward the ending she already knows","category":"base","risk":"LOW","family":"main","preferred_cams":["CAM06"],"use":"N","source":"first-use T5-18 REVERSE WONDERLAND (custom card)"},
 {"id":"PL410","name":"Fold-Through Doorway","sd":"folding herself into quarters like a folding ruler to slip through the shrinking door, chin over stacked hands","category":"dynamic_v2","risk":"HIGH","family":"main","preferred_cams":["CAM06"],"use":"V","source":"first-use T5-18 REVERSE WONDERLAND (custom card)"},
 {"id":"PL411","name":"Tide-Floor Wring","sd":"kneeling in knee-deep room-tide, wringing a rag over the water, hem floating a ring around her","category":"env_interaction","risk":"LOW","family":"main","preferred_cams":["CAM02"],"use":"NV","source":"first-use T5-18 REVERSE WONDERLAND (custom card)"},
 {"id":"PL412","name":"Crown-Verdict Kneel","sd":"kneeling on the checker floor with hands crown-shaped above her head, nightgown slipping off one shoulder, chess pieces tall around her","category":"threshold_limen","risk":"MID","family":"main","preferred_cams":["CAM03"],"use":"V","source":"first-use T5-18 REVERSE WONDERLAND (custom card)"},
 {"id":"PL413","name":"Scent-Smoke Sip","sd":"standing in a coil of visible scent pulled backward into her nose, eyes half-closed, one hand fanning the smoke back","category":"micropose_expression","risk":"LOW","family":"main","preferred_cams":["CAM02"],"use":"N","source":"first-use T5-18 REVERSE WONDERLAND (custom card)"},
 {"id":"PL414","name":"Lie-Weigh Balance","sd":"standing on one pan of a room-scale, opposite pan holding yesterday's excuse, nightshirt hem lifted by the updraft of honest weight","category":"erotic_presentation_v2","risk":"MID","family":"main","preferred_cams":["CAM04"],"use":"V","source":"first-use T5-18 REVERSE WONDERLAND (custom card)"},
 {"id":"PL415","name":"Dream-File Browse","sd":"standing at the dream-catalogue wall, pulling one file of somebody else's sleep, reading it like a letter","category":"base","risk":"LOW","family":"main","preferred_cams":["CAM06"],"use":"N","source":"first-use T5-18 REVERSE WONDERLAND (custom card)"},
 {"id":"PL416","name":"Tea-Rain Dry-Off","sd":"standing under the four-o'clock tea-rain with arms spread to dry herself with crest-heat, soaked chemise printing honest","category":"erotic_presentation_v2","risk":"MID","family":"main","preferred_cams":["CAM02"],"use":"V","source":"first-use T5-18 REVERSE WONDERLAND (custom card)"},
 {"id":"PL417","name":"Snail-Post Signature","sd":"signing a snail's shell with one fingernail, letters curving with the spiral, other hand smoothing the wall","category":"micropose_expression","risk":"LOW","family":"main","preferred_cams":["CAM06"],"use":"N","source":"first-use T5-18 REVERSE WONDERLAND (custom card)"},
 {"id":"PL418","name":"Vitrail-Ladder Reach","sd":"perched high on a stepladder washing a cathedral window that grew overnight, reaching across the stained-glass panel","category":"env_interaction","risk":"MID","family":"main","preferred_cams":["CAM04"],"use":"V","source":"first-use T5-18 REVERSE WONDERLAND (custom card)"},
 {"id":"PL419","name":"Smile-First Greeting","sd":"conversing with a floating grin while the rest of the cat assembles itself behind it, teacup steady in one hand","category":"micropose_expression","risk":"LOW","family":"main","preferred_cams":["CAM01"],"use":"N","source":"first-use T5-18 REVERSE WONDERLAND (custom card)"},
 {"id":"PL420","name":"Floor-to-Sky Line Thread","sd":"threading a laundry line stretched from floor to sky, on tiptoe, shift lifting in a slow wave with the reach, tails steadying the rope","category":"erotic_presentation_v2","risk":"MID","family":"main","preferred_cams":["CAM04"],"use":"V","source":"first-use T5-18 REVERSE WONDERLAND (custom card)"},
 {"id":"PL421","name":"Read-Aloud Blush","sd":"standing among open books turned toward her, reading her biography aloud, nightgown dropped off one shoulder in protest","category":"erotic_presentation_v2","risk":"MID","family":"main","preferred_cams":["CAM02"],"use":"V","source":"first-use T5-18 REVERSE WONDERLAND (custom card)"},
 {"id":"PL422","name":"Kettle-Sun Breakfast","sd":"leaning back against the counter away from the kettle's sunrise, thin chemise backlit through by the spout-light, breakfast tray on palm","category":"erotic_presentation_v2","risk":"MID","family":"main","preferred_cams":["CAM02"],"use":"V","source":"first-use T5-18 REVERSE WONDERLAND (custom card)"},
 {"id":"PL423","name":"Sky-Doorstep First Step","sd":"one bare foot already set on the first cloud-step off the doorstep, morning mug still in hand, hem standing in the wind of the drop","category":"threshold_limen","risk":"MID","family":"main","preferred_cams":["CAM03"],"use":"N","source":"first-use T5-18 REVERSE WONDERLAND (custom card)"},
 {"id":"PL424","name":"Whisper Seat-Knee (X3)","sd":"leaning in from the side a hand-span from the lens, one knee on the seat beside the viewer, weight on the planted palm, lips at the top frame edge mid-whisper, eyes straight into the lens","category":"X3","risk":"LOW","family":"X3","preferred_cams":["CAM02"],"use":"V","source":"first-use T5-18 REVERSE WONDERLAND (EXP-combo X3 «В-ШЁПОТ», custom card)"},
 {"id":"PL425","name":"Whisper Armrest (X3)","sd":"bending over the armrest to bring her face within a hand-span of the lens, weight sunk into the cushion, lips at the top frame edge mid-whisper, eyes locked on the lens","category":"X3","risk":"LOW","family":"X3","preferred_cams":["CAM02"],"use":"V","source":"first-use T5-18 REVERSE WONDERLAND (EXP-combo X3 «В-ШЁПОТ», custom card)"},
 {"id":"PL426","name":"Whisper Table-Lean (X3)","sd":"leaning across the table's corner into the lens zone, both palms flat on the wood, face turned fully to the lens, lips at the top frame edge mid-whisper","category":"X3","risk":"LOW","family":"X3","preferred_cams":["CAM02"],"use":"V","source":"first-use T5-18 REVERSE WONDERLAND (EXP-combo X3 «В-ШЁПОТ», custom card)"},
 {"id":"PL427","name":"Whisper Doorframe (X3)","sd":"framed in the doorway and leaning through it toward the lens, one hand on the jamb above, face fully toward the lens, lips at the frame's top edge mid-whisper","category":"X3","risk":"LOW","family":"X3","preferred_cams":["CAM02"],"use":"V","source":"first-use T5-18 REVERSE WONDERLAND (EXP-combo X3 «В-ШЁПОТ», custom card)"},
 {"id":"PL428","name":"Whisper Sill (X3)","sd":"bracing one knee on the windowsill to lean across into the lens, curtain brushing her jaw, lips at the top frame edge mid-whisper, eyes into the lens","category":"X3","risk":"LOW","family":"X3","preferred_cams":["CAM02"],"use":"V","source":"first-use T5-18 REVERSE WONDERLAND (EXP-combo X3 «В-ШЁПОТ», custom card)"},
 {"id":"PL429","name":"Whisper Ladder (X3)","sd":"halfway down a stepladder, stopping to lean in at the lens height, one hand gripping the rail, lips at the top frame edge mid-whisper, eyes on the lens","category":"X3","risk":"LOW","family":"X3","preferred_cams":["CAM02"],"use":"V","source":"first-use T5-18 REVERSE WONDERLAND (EXP-combo X3 «В-ШЁПОТ», custom card)"},
 {"id":"PL430","name":"Whisper Counter (X3)","sd":"leaning over the counter's edge into the lens, elbows planted, weight forward, face fully toward the lens, lips at the top frame edge mid-whisper","category":"X3","risk":"LOW","family":"X3","preferred_cams":["CAM02"],"use":"V","source":"first-use T5-18 REVERSE WONDERLAND (EXP-combo X3 «В-ШЁПОТ», custom card)"},
 {"id":"PL431","name":"Whisper Desk (X3)","sd":"sliding onto the desk edge beside the lens and leaning across its width, one hand flat among the papers, lips at the top frame edge mid-whisper, eyes into the lens","category":"X3","risk":"LOW","family":"X3","preferred_cams":["CAM02"],"use":"V","source":"first-use T5-18 REVERSE WONDERLAND (EXP-combo X3 «В-ШЁПОТ», custom card)"},
 {"id":"PL432","name":"Whisper Fence (X3)","sd":"hanging over the garden fence to reach the lens, forearms on the top rail, chin low, lips at the top frame edge mid-whisper, eyes straight into the lens","category":"X3","risk":"LOW","family":"X3","preferred_cams":["CAM02"],"use":"V","source":"first-use T5-18 REVERSE WONDERLAND (EXP-combo X3 «В-ШЁПОТ», custom card)"}
]

p = load('poses.json')
existing = {x['id'] for x in p['poses']}
add = [x for x in NEW_POSES if x['id'] not in existing]
p['poses'].extend(add)
p['version'] = '1.8.0'
p['changelog'].append("1.8.0: T5-18 REVERSE WONDERLAND: +PL400–PL423 (24 мейна) + PL424–PL432 (EXP-семья X3 whisper-lean, 9 карт, use V) — X3 «В-ШЁПОТ» по приказу «над комбо поработай очень хорошо. ОЧЕНЬ хорошо»; first_use_ledger догнал T5-17 (PL367–PL399)")
if 'first_use_ledger' in p and isinstance(p['first_use_ledger'], dict):
    p['first_use_ledger'].setdefault('T5-17', [])
    p['first_use_ledger']['T5-17'] = sorted(set(p['first_use_ledger']['T5-17']) | {('PL%d' % i) for i in range(367,400)})
    p['first_use_ledger'].setdefault('T5-18', [])
    p['first_use_ledger']['T5-18'] = sorted(set(p['first_use_ledger']['T5-18']) | {x['id'] for x in add})
if isinstance(p.get('family_counts'), dict):
    p['family_counts']['X3'] = 9
save('poses.json', p)
print('poses.json: +', len(add), '->', len(p['poses']))

SRC18 = "T5-18 REVERSE WONDERLAND (приказ автора 2026-11-09: 9 новых экспериментальных палитр, ВСЕ разные — одна на кандидата, «следи чтобы и палитры были разные»; directed override C067)"
NEW_PAL = [
 {"id":"P171_CANDY_PISTOL","name":"Candy Pistol","dominant":["candy-pink-bright","sugar-white-hot"],"secondary":["poppy-red-flash"],"accent1":["cherry-bow-red"],"accent2":["bubblegum-rose-deep"],"shadow":"candy-shadow-never-grey","forbidden":["grey shadow","black shadow","neon","fluorescent","violet-dominant","pastel-dominant","muddy-brown"],"light_type":"sugar-shop bright — candy pink floods the light, one poppy-red strike like a shot through the sweetness; shadows stay rose and never grey","sd_fragment":"candy-pistol-bright","mood":"","family":"exp_color_wave_3","legacy_3slot":False,"source":SRC18},
 {"id":"P172_NETTLE_BRAMBLE","name":"Nettle Bramble","dominant":["nettle-silver-green","bramble-brown-dark"],"secondary":["berryle-red-wine"],"accent1":["sting-rose-bright"],"accent2":["bark-umber-deep"],"shadow":"bramble-shadow-never-grey","forbidden":["grey shadow","black shadow","neon","violet-dominant","pastel-dominant","muddy-brown"],"light_type":"cold nettle green with bramble shade; the sting is one bright berry-red strike through the dark leaves","sd_fragment":"nettle-bramble-cold","mood":"","family":"exp_color_wave_3","legacy_3slot":False,"source":SRC18},
 {"id":"P173_SNOW_TIGER_MARK","name":"Snow Tiger Mark","dominant":["snow-white-flat","charcoal-stripe-black"],"secondary":["tundra-cream-warm"],"accent1":["tiger-amber-eye"],"accent2":["storm-slate-mid"],"shadow":"tiger-shadow-never-grey","forbidden":["grey shadow","black shadow","neon","violet-dominant","pastel-dominant","muddy-brown"],"light_type":"flat snow-white world striped by charcoal bars; one amber mark burning like an eye in the white","sd_fragment":"snow-tiger-mark","mood":"","family":"exp_color_wave_3","legacy_3slot":False,"source":SRC18},
 {"id":"P174_ROSE_WINDOW","name":"Rose Window","dominant":["sapphire-glass-deep","ruby-garnet-glow"],"secondary":["gold-leadline-warm"],"accent1":["emerald-glass-bright"],"accent2":["stone-shadow-cold"],"shadow":"glass-shadow-never-grey","forbidden":["grey shadow","black shadow","neon","violet-dominant","pastel-dominant","muddy-brown"],"light_type":"cathedral glass at night: sapphire floods the nave, ruby burns at the center, gold leadlines draw where the light may walk","sd_fragment":"rose-window-glass","mood":"","family":"exp_color_wave_3","legacy_3slot":False,"source":SRC18},
 {"id":"P175_BELLFROST_NOEL","name":"Bellfrost Noel","dominant":["bell-bronze-green","frost-snow-blue-pale"],"secondary":["ember-window-orange"],"accent1":["midnight-mass-gold"],"accent2":["bronze-patina-mid"],"shadow":"bell-shadow-never-grey","forbidden":["grey shadow","black shadow","neon","violet-dominant","pastel-dominant","muddy-brown"],"light_type":"frosted bell-bronze night with one ember-warm window breathing light; snow keeps the shadows blue-pale and never grey","sd_fragment":"bellfrost-noel","mood":"","family":"exp_color_wave_3","legacy_3slot":False,"source":SRC18},
 {"id":"P176_INCENSE_AND_MYRRH","name":"Incense and Myrrh","dominant":["incense-smoke-warm-grey","myrrh-brown-deep"],"secondary":["frankincense-cream-pale"],"accent1":["nave-gold-dim"],"accent2":["thurible-ember-soft"],"shadow":"incense-shadow-never-grey","forbidden":["grey shadow","black shadow","neon","violet-dominant","pastel-dominant","muddy-brown"],"light_type":"smoke-warm grey air sweetened by myrrh; gold lives small and dim, like light through a thurible's holes","sd_fragment":"incense-myrrh-smoke","mood":"","family":"exp_color_wave_3","legacy_3slot":False,"source":SRC18},
 {"id":"P177_GUTTER_CHAMPAGNE","name":"Gutter Champagne","dominant":["cheap-champagne-gold","nicotine-amber"],"secondary":["cardboard-tan-flat"],"accent1":["red-lacquer-lip"],"accent2":["alley-brick-dark"],"shadow":"gutter-shadow-never-grey","forbidden":["grey shadow","black shadow","neon","violet-dominant","pastel-dominant","muddy-brown"],"light_type":"discount glam: champagne gold poured over nicotine amber, one hard red lacquer strike, shadows the color of brick dust","sd_fragment":"gutter-champagne","mood":"","family":"exp_color_wave_3","legacy_3slot":False,"source":SRC18},
 {"id":"P178_OILSLICK_CHROME","name":"Oilslick Chrome","dominant":["oil-black-iridescent","chrome-silver-hard"],"secondary":["acid-green-flash"],"accent1":["spark-arc-white"],"accent2":["garage-iron-dark"],"shadow":"oil-shadow-never-grey","forbidden":["grey shadow","black shadow","neon","violet-dominant","pastel-dominant","muddy-brown"],"light_type":"black oil under a hard chrome sheen; acid-green flashes ride the surface like leaks of color","sd_fragment":"oilslick-chrome","mood":"","family":"exp_color_wave_3","legacy_3slot":False,"source":SRC18},
 {"id":"P179_MUD_LEOPARD","name":"Mud Leopard","dominant":["mud-brown-warm","leopard-amber-spot"],"secondary":["bone-print-cream"],"accent1":["jet-rosette-black"],"accent2":["swamp-moss-dark"],"shadow":"mud-shadow-never-grey","forbidden":["grey shadow","black shadow","neon","violet-dominant","pastel-dominant","muddy-brown"],"light_type":"warm mud ground spotted with leopard amber and jet rosettes; the print works as a light-map, shadows stay moss-green","sd_fragment":"mud-leopard-print","mood":"","family":"exp_color_wave_3","legacy_3slot":False,"source":SRC18}
]
pal = load('palettes.json')
have = {x['id'] for x in pal['palettes']}
addp = [x for x in NEW_PAL if x['id'] not in have]
pal['palettes'].extend(addp)
pal['version'] = '1.3.0'
if isinstance(pal.get('changelog'), list):
    pal['changelog'].append("1.3.0: T5-18 REVERSE WONDERLAND: +P171–P179 exp_color_wave_3 (9 семей: candy-pistol / nettle-bramble / snow-tiger-mark / rose-window / bellfrost-noel / incense-and-myrrh / gutter-champagne / oilslick-chrome / mud-leopard) — ни одной violet/plum в доминанте, все 9 разных")
save('palettes.json', pal)
print('palettes.json: +', len(addp), '->', len(pal['palettes']))

K = [
 ("K216","mid_pour_up","the stream mid-rising from the spout to the cup held overhead — tea drinking upward"),
 ("K217","mid_airstep","the invisible stair mid-step above the broken flight — the basket's weight swinging late"),
 ("K218","mid_unrain","the raindrops mid-climb from the puddle to the sky — the shirt drying upward"),
 ("K219","mid_backtick","the minute hand mid-run backward under her fingertip — the alarm set for yesterday"),
 ("K220","mid_selfdeal","the cards mid-deal by themselves across the checker floor — her hands only fanning"),
 ("K221","mid_pruneself","the shears mid-cut by themselves on the bush — the teacup already reaching her hand"),
 ("K222","mid_outkey","the key mid-turn from the wrong side of the door — the lock answering her pull"),
 ("K223","mid_delaymirror","the reflection mid-catch-up three seconds late — her arms crossed, waiting"),
 ("K224","mid_upsweep","the fallen cups mid-fall toward the ceiling-floor — the broom bristles just landing"),
 ("K225","mid_selfwrite","the ink mid-crawl into the next word — the page finishing its sentence without her"),
 ("K226","mid_shrinkdoor","the door frame mid-shrink below her height — the fold already begun at the waist"),
 ("K227","mid_tidefloor","the room-tide mid-flood over the threshold — the rag lifting from the water"),
 ("K228","mid_verdict_crown","the pieces mid-vote around her kneel — the crown-shaped hands held level"),
 ("K229","mid_smell_pull","the visible scent mid-drink back into her nose — the coil of air bent double"),
 ("K230","mid_lie_weigh","the opposite pan mid-dip under the excuse's weight — her own pan rising"),
 ("K231","mid_dreamfile","the dream-file mid-slide from the wall slot — somebody else's sleep in her hand"),
 ("K232","mid_teapour_rain","the tea-rain mid-hour over her arms — the crest heat just flaring to dry"),
 ("K233","mid_snailmail","the shell mid-signature under the fingernail — the spiral letter half-curled"),
 ("K234","mid_aisle_grow","the cathedral window mid-wash on the grown ladder — the squeegee pausing at the leadline"),
 ("K235","mid_smile_first","the grin mid-hang before the cat arrives — the teacup steady beneath it"),
 ("K236","mid_line_hang","the laundry line mid-thread from floor to sky — the shift's hem lifting in the reach"),
 ("K237","mid_readback","the open books mid-read of her biography — the page turning itself to the embarrassing year"),
 ("K238","mid_sun_spout","the kettle's sunrise mid-spill across the ceiling — the tray level on her palm"),
 ("K239","mid_doorstep_sky","the first cloud-step mid-take beneath her bare foot — the mug still level"),
 ("K240","mid_whisper_ear","the whisper mid-syllable at the lens corner — the ears mid-betrayal upright"),
 ("K241","mid_whisper_armrest","the whisper mid-word over the armrest — the tail mid-wrap on her own ankle"),
 ("K242","mid_whisper_table","the whisper mid-sentence across the table corner — the spines mid-flatten along the forearm"),
 ("K243","mid_whisper_frame","the whisper mid-breath through the doorway — the glass freckles mid-catch of window light"),
 ("K244","mid_whisper_sill","the whisper mid-word at the sill — the hair-tips mid-dissolve into incense smoke"),
 ("K245","mid_whisper_ladder","the whisper mid-phrase from the ladder step — the wing mid-fold closer as a cloak"),
 ("K246","mid_whisper_counter","the whisper mid-syllable over the counter — the ringed tail mid-curl at the hip"),
 ("K247","mid_whisper_desk","the whisper mid-word across the desk — the scent-haze mid-curl from her collar"),
 ("K248","mid_whisper_fence","the whisper mid-breath over the fence rail — the quick hands mid-deal of a small stolen trinket"),
]
pool = load('pools.json')
kk = pool['sections']['kinetics_k']
havek = {x['id'] for x in kk}
addk = [{"id":i,"name":n,"sd":sd,"source":"T5-18 K-FF"} for (i,n,sd) in K if i not in havek]
kk.extend(addk)
pool['version'] = '1.2.0'
if isinstance(pool.get('inventory'), dict):
    pool['inventory']['kinetics_k'] = len(kk)
if isinstance(pool.get('changelog'), list):
    pool['changelog'].append("1.2.0: T5-18 REVERSE WONDERLAND: +K216–K248 (миды 24 мейнов + 9 whisper-EXP); inventory.kinetics_k пересчитан по факту")
save('pools.json', pool)
print('pools.json: +', len(addk), '->', len(kk), '| inventory =', pool['inventory']['kinetics_k'])

cam = load('camera.json')
ec = cam['exp_combos']
ec['X2']['status'] = "вердикт T5-17 (2026-11-09): «вышло слабовато» — В РОТАЦИЮ НЕ ПРИНЯТА; семья PL391–PL399 остаётся архивом эксперимента; диагноз: полуповорот 3/4 теряет лицо, шаг статичен, участие зрителя нулевое — против четырёх столпов живого X1 (участие / вес / глаз-в-линзу / лицо целиком); X3 заказан приказом «над комбо поработай очень хорошо. ОЧЕНЬ хорошо»"
ec['X3'] = {
 "name": "В-ШЁПОТ (whisper-close)",
 "born": "2026-11-09, T5-18 — приказ автора: «над комбо поработай очень хорошо. ОЧЕНЬ хорошо»; вердикт T5-17 по X2 «вышло слабовато» — X3 спроектирован по четырём столпам принятого X1: POV-участие зрителя, вес тела вперёд, глаз-в-линзу, лицо целиком в кадре",
 "cam": "D2×A02 (ближний план, три четверти) — губы у верхнего края кадра, глаз-линия целиком в кадре, лицо никогда не в полуповороте (урок X2)",
 "pos": "она входит вплотную СБОКУ: колено на опоре рядом со зрителем (сиденье/подлокотник/стол/рама/подоконник/стремянка/стойка/парта/плетень), вес на опорной ладони или колене — корпус пересекает линзу; руки — ТОЛЬКО на твёрдой опоре, никогда у лица (урок рук)",
 "pov": "lens = глаза сидящего зрителя; второй человек НЕ рисуется (solo) — присутствие зрителя несут опоры у края кадра; POV-дисциплина: без selfie-рук, лицо В кадре целиком, глаза прямо в линзу, токен «camera» — 0; шёпот-контент = голос кандидата (тест характера встроен в камеру: цундере шепчет отречение, собор — благословение, дрянь — грязь)",
 "pose": "first-use карты семьи whisper-lean PL424–PL432, по одной на слот; опора у каждой своя; K-FF миды K240–K248",
 "status": "⚗ эксперимент: 9 EXP-слотов T5-18, вердикт решает судьбу комбо",
 "neg_guard": "second figure, two girls, extra person, hand over the lens, face hidden, profile view only"
}
cam['version'] = '1.5.0'
save('camera.json', cam)
print('camera.json: X2 stamped, X3 added, v1.5.0')

NEW_RACES = [
 {"id":"R53","name":"Rabbit-kin","status":"active","features":["long upright ears that betray her mood — flat back in denial, springing up when she softens","cream-white winter coat","powder-puff tail","rose-pink inner ears"],"pos_tags":["long upright ears flat back in denial","cream-white winter coat","powder-puff tail","rose-pink inner ears"],"note":"T5-18 кандидат-носитель tsundere-голоса #1: уши = детектор дэре (губы шепчут «нет», уши уже «да»); collision: R29 Mouse-kin не задет (уши зайца — длинные стоячие); light: уши ловят ключевой свет первыми"},
 {"id":"R54","name":"Snow-leopard-kin","status":"active","features":["plush snow-leopard tail that wraps her own ankle when caught off-guard","snow-pale skin with faint rosettes at the shoulders only","small round snow-leopard ears","grey-green eyes"],"pos_tags":["plush snow-leopard tail wrapped around her own ankle","snow-pale skin with faint shoulder rosettes","small round snow-leopard ears","grey-green eyes"],"note":"T5-18 tsundere-голос #2: хвост-предатель (обвил щиколотку сам = дэре); rosettes только на плечах, не принт по всему телу; collision: R04 Cat-kin не задет"},
 {"id":"R55","name":"Hedgehog-kin","status":"active","features":["brown spines along forearms and shoulder line that flatten when she relaxes","soft cream fur line at the collar and belly","small dark nose","dark round eyes"],"pos_tags":["brown spines smoothed flat along the forearms","cream fur line at the collar","small dark nose","dark round eyes"],"note":"T5-18 tsundere-голос #3: иглы-метафора (разгладились при зрителе = уже спокойно); спины не колют окружение в кадре, сидят плоско по руке"},
 {"id":"R56","name":"Rose-glass-kin","status":"active","features":["skin freckles patterned like leaded stained-glass shards over nose and cheeks","small jewel-glass beads woven into the hair","a faint nave echo under the voice","pale skin warmed by glass light"],"pos_tags":["stained-glass freckles over nose and cheeks","small jewel-glass beads in the hair","pale skin lit warm through glass"],"note":"T5-18 notre-dame голос #1: фрекнелы-витраж — рождественское стекло рисует по лицу; jewel-бусин в волосах ≤3; echo — просодия, не звук в кадре"},
 {"id":"R57","name":"Incense-wisp-kin","status":"active","features":["hair rising and thinning into pale incense smoke at the tips","ember glow at the fingertips","faint drifting scent drawn as curls in the air","warm dusk skin"],"pos_tags":["hair tips dissolving into pale incense smoke","ember glow at the fingertips","drifting scent drawn as visible curls","warm dusk skin"],"note":"T5-18 notre-dame #2: волосы-дым (урок В14: дым — существительное с позицией); ember на пальцах — не светильник: она сама тёплая точка, закон света v2 совместим"},
 {"id":"R58","name":"Belfry-owl-kin","status":"active","features":["huge silent owl wings folded close like a cloak","moonlit grey-white plumage at the collar and cuffs","round amber eyes","near-silent head turns"],"pos_tags":["huge owl wings folded close like a cloak","moonlit grey-white plumage at collar and cuffs","round amber eyes"],"note":"T5-18 notre-dame #3: крылья-плащ (сложены, не раскрыты за спиной); её свет — луна через витраж; движение головы беззвучно"},
 {"id":"R59","name":"Raccoon-kin","status":"active","features":["dark mask-ring around the eyes","ringed tail thick and fluffy, carried curled around the hip","clever small fingers","dusty-grey coat that shines after rain"],"pos_tags":["dark mask-ring around the eyes","thick fluffy ringed tail curled around the hip","clever small fingers","dusty-grey coat shining after rain"],"note":"T5-18 dirty голос #1: мусорная принцесса; хвост = толстый-пушистый-завитой у бедра — патч В12 вшит в теги сразу"},
 {"id":"R60","name":"Skunk-kin","status":"active","features":["jet-black coat with a white crest stripe over the crown and down the spine","plume tail carried like a boa across the forearms","visible sweet scent-haze drawn as faint curls","dark amber-brown eyes"],"pos_tags":["jet-black coat with a white crest stripe down the spine","plume tail draped across the forearms like a boa","sweet scent-haze drawn as faint curls","dark amber-brown eyes"],"note":"T5-18 dirty #2: парфюм-передоз (запах видим — дымка-завитки); хвост-боа НА предплечьях, никогда не у таза вверх (В12)"},
 {"id":"R61","name":"Weasel-kin","status":"active","features":["long slinky body line","honey-brown fur with a cream throat patch","restless quick hands always mid-scheme","bright near-black eyes"],"pos_tags":["long slinky body line","honey-brown fur with a cream throat patch","restless quick hands mid-scheme","bright near-black eyes"],"note":"T5-18 dirty #3: хорь-схемщица; тело — длинная линия, руки в постоянной середине трюка"}
]
r = load('races.json')
rkey = None
for k in r.keys():
    v = r[k]
    if isinstance(v, list) and v and isinstance(v[0], dict) and 'id' in v[0] and str(v[0]['id']).startswith('R'):
        rkey = k; break
if rkey is None:
    rkey = 'races' if 'races' in r else list(r.keys())[0]
haver = {x['id'] for x in r[rkey]}
addr = [x for x in NEW_RACES if x['id'] not in haver]
r[rkey].extend(addr)
r['version'] = '2.5.0'
save('races.json', r)
print('races.json (' + rkey + '): +', len(addr), '->', len(r[rkey]))
print('DONE')
