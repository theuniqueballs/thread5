# -*- coding: utf-8 -*-
"""T5-19 DEVIL'S GREED — обновление реестров (SOL-сеанс 2026-11-10).
poses 1.9.0 (+PL436–468) · palettes 1.4.0 (+P180–188, exp_color_wave_4) ·
camera 1.6.0 (X4 «В-КЛЕТКУ») · pools 1.3.0 (+K252–284) · races 2.6.0 (+R62–70).
Append-only: ledger/changelog дополняются, ничего не переписывается.
"""
import json

ROOT = '/home/z/my-project/thread5/specs'


def load(name):
    with open(f'{ROOT}/{name}', encoding='utf-8') as f:
        return json.load(f)


def save(name, data):
    with open(f'{ROOT}/{name}', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
        f.write('\n')


# ── poses.json 1.9.0 ─────────────────────────────────────────────────────
MAIN_POSES = [
    ("PL436", "Coin-Bite Reach", "fingers closing around the fresh coin still trembling from her bite, teeth-marks set in the metal, the mouth paying first", "greed_toll"),
    ("PL437", "Key-Harvest Loop", "both hands lifting keys off door-rings in a walking line, each ring already swinging lighter", "greed_toll"),
    ("PL438", "Slot-Swallow Tilt", "tilting the piggy-bank over her open palm while its mouth swallows the nearest shine first", "greed_toll"),
    ("PL439", "Moss-Ledger Press", "palm pressed flat on the moss-grown wall, fingers counting the growth rings as they arrive", "greed_toll"),
    ("PL440", "Scale-Tip Stand", "standing on the low pan as it sinks her side down, the far pan climbing empty", "greed_toll"),
    ("PL441", "Vault-Swallow Step", "stepping into the vault's mouth as the door folds the room in after her", "greed_engine"),
    ("PL442", "Contract-Seal Lean", "leaning over the contract while gold writes the seal by itself across the page", "greed_engine"),
    ("PL443", "Hoard-Nest Settle", "settling into the coin-hoard that shifts itself to cradle her hip", "greed_engine"),
    ("PL444", "Ledger-Debt Flip", "flipping the ledger's pages backward toward zero-owed, debts running in reverse", "greed_engine"),
    ("PL445", "Thread-Spool Reel", "reeling the self-spooling gold thread onto her own wrist in tight even rows", "greed_engine"),
    ("PL446", "Drawer-Feed Crouch", "crouched at the open drawer, feeding the swallowing wood one more possession", "greed_engine"),
    ("PL447", "Purse-Weight Carry", "carrying the purse that outweighs her, the strap winning the shoulder's argument", "greed_engine"),
    ("PL448", "Dice-Cup Verdict", "shaking the dice cup over her own palm, dice already settling stacked in her favor", "greed_engine"),
    ("PL449", "Mirror-Pay Collect", "collecting coins from the mirror's silver edge where the reflection pays out", "greed_engine"),
    ("PL450", "Debt-Swallow Lean", "leaning over the mouth-pit as it swallows the stack of IOUs whole", "greed_engine"),
    ("PL451", "Ten-Rings Spread", "spreading both hands flat, one ring per finger, the count closing at ten", "greed_crown"),
    ("PL452", "Wardrobe-Feed Open", "holding the wardrobe's maw wide as the hangers feed themselves into it", "greed_crown"),
    ("PL453", "Promise-Paving Stride", "striding the floor as promissory notes press themselves flat to marble underfoot", "greed_crown"),
    ("PL454", "Crown-Take Fit", "fitting the crown on with both hands, taking it like a wage owed and paid", "greed_crown"),
    ("PL455", "Pit-Count Crouch", "crouched over her palm's tally of cherry pits, one more dropping in", "greed_crown"),
    ("PL456", "Sunset-Pocket Walk", "walking off with the folded sunset tucked under her arm like a bolt of cloth", "greed_crown"),
]
X4_POSES = [
    ("PL457", "Cage-Lean Headboard", "braced over the viewer's headboard, both palms on the rails behind the lens, weight forward on the arms, the chest the closest claim after the face"),
    ("PL458", "Cage-Lean Bookcase", "braced into the bookcase behind the viewer, palms flat on the shelf-boards either side of the frame"),
    ("PL459", "Cage-Lean Couch-Back", "braced over the couch's backrest behind the viewer, forearms sunk into the cushion's give"),
    ("PL460", "Cage-Lean Glass", "braced on the glass partition behind the viewer, both palms flat on the pane, breath fogging a small circle"),
    ("PL461", "Cage-Lean Door-Jamb", "braced across the door-jamb behind the viewer, palms set on both posts"),
    ("PL462", "Cage-Lean Poolside", "braced on the pool's stone lip behind the viewer, wrists riding the wet edge"),
    ("PL463", "Cage-Lean Fur-Wall", "braced into the wall of hanging coats behind the viewer, forearms parting the fur"),
    ("PL464", "Cage-Lean Counter", "braced across the counter behind the viewer, spread fingers on the till's lip"),
    ("PL465", "Cage-Lean Larder", "braced against the larder's brick behind the viewer, palms flat on the cool mortar joints"),
]
OC_POSES = [
    ("PL466", "Organ-Column One", "standing at the single organ pipe taller than her, one palm settling on the metal like on a column", "OC_T5-19"),
    ("PL467", "Stake-Claim Strike", "driving the boundary stake deeper with flat palm-strikes, the hammer resting unused in the grass", "OC_T5-19"),
    ("PL468", "Stud-Collar Strut", "mid-stride through the travertine street, the studded collar catching the night's shine stud by stud", "OC_T5-19"),
]

p = load('poses.json')
p['version'] = '1.9.0'
p['born'] = p['born'] + "\n2026-11-10 — T5-19: +PL436–PL456 (мейны 21, family greed_*), PL457–PL465 (EXP-семья X4 cage-lean 9), PL466–PL468 (canon-OS P01–P03)"
existing = {x['id'] for x in p['poses']}
new_poses = []
for pid, name, sd, fam in MAIN_POSES:
    new_poses.append({"id": pid, "name": name, "sd": sd, "category": fam, "risk": "MID",
                      "family": fam, "preferred_cams": ["CAM01", "CAM02", "CAM06"], "use": "N",
                      "source": "first-use T5-19 DEVIL'S GREED (мейн)"})
for pid, name, sd in X4_POSES:
    new_poses.append({"id": pid, "name": name, "sd": sd, "category": "X4", "risk": "MID",
                      "family": "X4", "preferred_cams": ["CAM02"], "use": "V",
                      "source": "first-use T5-19 DEVIL'S GREED (EXP-семья X4 cage-lean, 9 карт)"})
for pid, name, sd, fam in OC_POSES:
    new_poses.append({"id": pid, "name": name, "sd": sd, "category": "threshold_limen", "risk": "MID",
                      "family": fam, "preferred_cams": ["CAM01", "CAM06"], "use": "N",
                      "source": "first-use T5-19 DEVIL'S GREED (canon-OS card)"})
for np_ in new_poses:
    assert np_['id'] not in existing, np_['id']
    p['poses'].append(np_)
fc = p.setdefault('family_counts', {})
fc['greed_toll'] = 5
fc['greed_engine'] = 11
fc['greed_crown'] = 5
fc['X4'] = 9
fc['OC_T5-19'] = 3
ful = p.setdefault('first_use_ledger', {})
ful['T5-19'] = [x[0] for x in MAIN_POSES] + [x[0] for x in X4_POSES] + [x[0] for x in OC_POSES]
p.setdefault('changelog', []).append(
    "1.9.0: T5-19 DEVIL'S GREED: +PL436–PL456 (21 мейн, families greed_toll/greed_engine/greed_crown) + "
    "PL457–PL465 (EXP-семья X4 cage-lean, 9 карт, use V) + PL466–PL468 (canon-OS P01–P03, family OC_T5-19) — "
    "X4 «В-КЛЕТКУ» по приказу автора «с жёстким упором в R++»; темы ОС → канон-ОС слоты сразу (прецедент вето T5-18)")
save('poses.json', p)

# ── palettes.json 1.4.0 ──────────────────────────────────────────────────
EXP_PALETTES = [
    ("P180_COPPER_TONGUE", "Copper Tongue", ["copper-hot", "burnished-gold"], ["forge-amber"], ["oxid-green-flash"], None,
     "copper-shadow-ember", "forge-hot — copper floods the frame, one oxid-green strike where the metal has been licked; shadows stay warm and never grey",
     "copper-tongue-hot", "greed register: the coin still warm from the mouth"),
    ("P181_MINT_BOUNTY", "Mint Bounty", ["mint-emerald-deep", "coin-silver"], ["foam-white"], ["black-leaf-line"], None,
     "mint-shadow-cool", "mint-house cold — emerald fills the frame like stacked banknotes, silver strikes where light lands; shadows stay green-cold",
     "mint-bounty-deep", "greed register: the harvest counted in cold silver"),
    ("P182_CHERRY_LACQUER", "Cherry Lacquer", ["cherry-lacquer-deep", "stem-green"], ["pit-black"], ["cream-flesh-pale"], None,
     "lacquer-shadow-brown", "lacquer-box deep — cherry red poured over green stems, cream strikes where skin opens; shadows lacquer-dark",
     "cherry-lacquer-deep", "greed register: the fruit taken pit and all"),
    ("P183_VAULT_INK", "Vault Ink", ["vault-ink-black", "dial-brass"], ["ledger-ivory"], ["seal-wax-red"], None,
     "vault-shadow-iron", "vault-dark — ink-black air, brass dials striking thin lines, ivory paper glow; shadows are iron and deeper",
     "vault-ink-black", "greed register: the door that opens only inward"),
    ("P184_PEACH_RANSOM", "Peach Ransom", ["peach-amber-deep", "blush-cream"], ["skin-warm-gold"], ["bruise-plum-soft"], None,
     "peach-shadow-fuzz", "peach-flesh warm — amber-fruit light over cream skin, one soft plum bruise where the hand pressed; shadows stay fuzzy-warm",
     "peach-ransom-warm", "greed register: the soft thing kept, not given"),
    ("P185_SALT_GLASS", "Salt Glass", ["glass-pale-blue", "salt-white-shine"], ["waterline-teal"], ["brine-dark"], None,
     "salt-shadow-cold", "salt-pan bright — glass-blue light, white salt strikes drying at the edges, one teal waterline; shadows cold and clean",
     "salt-glass-pale", "greed register: the cup filled past its use"),
    ("P186_EMERALD_TOLL", "Emerald Toll", ["emerald-deep", "toll-gold"], ["booth-wood-warm"], ["feather-green-dark"], None,
     "emerald-shadow-moss", "toll-booth dark — emerald depth, gold coin-strikes at the gate's slot, warm wood at the frame; shadows moss-green",
     "emerald-toll-deep", "greed register: the gate that charges both ways"),
    ("P187_BONE_PORCELAIN", "Bone Porcelain", ["bone-pale", "porcelain-warm"], ["dust-rose-soft"], ["crack-gold-thin"], None,
     "porcelain-shadow-grey-warm", "relic-case calm — bone-pale fields, warm porcelain skin-light, one thin gold crack-line; shadows soft and warm-grey",
     "bone-porcelain-pale", "greed register: the relic kept behind its glass"),
    ("P188_ASH_ROSE", "Ash Rose", ["ash-rose-deep", "ember-blush"], ["charcoal-warm"], ["smoke-thread-pale"], None,
     "ash-shadow-warm", "banked-fire dusk — ash-rose over charcoal warmth, one pale smoke-thread where breath crosses; shadows stay ember-warm",
     "ash-rose-deep", "greed register: the fire kept banked, never shared"),
]
pa = load('palettes.json')
pa['version'] = '1.4.0'
existingP = {x['id'] for x in pa['palettes']}
for pid, name, dom, sec, acc1, acc2, shadow, light, sdfrag, src in EXP_PALETTES:
    assert pid not in existingP, pid
    pa['palettes'].append({
        "id": pid, "name": name, "dominant": dom, "secondary": sec, "accent1": acc1,
        "accent2": acc2, "shadow": shadow, "forbidden": ["grey shadow", "violet-dominant", "plum-dominant", "muddy-brown"],
        "light_type": light, "sd_fragment": sdfrag, "mood": "",
        "family": "exp_color_wave_4", "legacy_3slot": False,
        "source": f"T5-19 DEVIL'S GREED ({src}; приказ автора 2026-11-10: новЫЕ экспериментальнЫЕ палитры и раскраски, «с жёстким упором в R++»; девять РАЗНЫХ семей — одна на кандидата)",
    })
save('palettes.json', pa)

# ── camera.json 1.6.0 (X4) ───────────────────────────────────────────────
cam = load('camera.json')
cam['version'] = '1.6.0'
cam['exp_combos']['X4'] = {
    "name": "В-КЛЕТКУ (cage-close)",
    "born": "2026-11-10, T5-19 — приказ автора: «новое экспериментальное комбо для VOLT (Комбо Cam/Pos/POV/Pose), в этот раз с жёстким упором в R++»",
    "cam": "D2×A02 (ближний план, три четверти) — лицо целиком в верхних двух третях кадра, глаз-линия в кадре; каймы кадра читаются её предплечьями-стойками",
    "pos": "она наваливается СВЕРХУ-ВПЕРЕДИ: ладони упираются в опору ЗА спиной зрителя (изголовье/стеллаж/спинка/стекло/косяк/бортик/шкаф/прилавок/кладовая), предплечья-стойки по обе стороны кадра, вес вперёд на руки, грудь — самый близкий к линзе элемент после лица; ткань честно съезжает и натягивается под весом; руки НИКОГДА не тянутся к линзе",
    "pov": "lens = глаза зрителя, прижатого спиной к опоре; второй человек НЕ рисуется (solo) — присутствие зрителя несут её предплечья-стойки у краёв кадра; POV-дисциплина X1/X3: без selfie-рук, лицо В кадре целиком, глаза прямо в линзу, токен «camera» — 0; R++-контент = вес и ткань: съехавшая лямка, натянутый шов, честный отпечаток — заявка-вещь стоит первой (В16/M07)",
    "pose": "first-use карты семьи cage-lean PL457–PL465, по одной на слот; K-FF миды K273–K281",
    "status": "⚗ эксперимент: 9 EXP-слотов T5-19, все R+ (жёсткий упор в R++ — интерпретация токена «R++» объявлена, вето дёшево); вердикт решает судьбу комбо",
    "neg_guard": "second figure, two girls, extra person, arms toward lens, selfie arm, face hidden, profile view only",
}
save('camera.json', cam)

# ── pools.json 1.3.0 (+K252–284) ─────────────────────────────────────────
MAIN_KS = [
    ("K252", "mid_coin_bite", "the fresh coin still trembling from the bite as the fingers close around it — the mouth pays first"),
    ("K253", "mid_key_lift", "the key mid-lift off its ring while the door behind her locks itself for good"),
    ("K254", "mid_slot_swallow", "the coin mid-drop into the slot's mouth, the rim already swallowing the shine"),
    ("K255", "mid_moss_count", "the fingertip mid-count across the moss rings, new growth arriving under the nail"),
    ("K256", "mid_scale_tip", "the pan sinking under her heel while the far pan climbs empty and defeated"),
    ("K257", "mid_vault_step", "the vault's door mid-fold around her ankle as the room follows her in"),
    ("K258", "mid_gold_seal", "the gold mid-writing the seal by itself, the ink still arguing with it"),
    ("K259", "mid_hoard_settle", "the coin-hoard mid-settling to cradle her hip, the clink still travelling"),
    ("K260", "mid_ledger_flip", "the ledger's page mid-flip toward zero-owed, the debts running backward"),
    ("K261", "mid_thread_reel", "the gold thread mid-spooling onto her wrist in tight even rows"),
    ("K262", "mid_drawer_feed", "the drawer mid-swallow of the offered thing, the wood parting around it"),
    ("K263", "mid_purse_carry", "the purse mid-swing heavy enough to carry her shoulder along"),
    ("K264", "mid_dice_stack", "the dice mid-settling into a stacked six, the cup already lifted away"),
    ("K265", "mid_mirror_pay", "the coin mid-emerging from the mirror's silver edge, wet with reflection"),
    ("K266", "mid_debt_gulp", "the IOU mid-vanish into the mouth-pit, the paper's corner still visible"),
    ("K267", "mid_rings_count", "the tenth ring mid-slide over the knuckle, the count closing"),
    ("K268", "mid_wardrobe_feed", "the hanger mid-slide into the wardrobe's maw, the maw receiving"),
    ("K269", "mid_pave_stride", "the promissory note mid-pressing itself flat to marble under her heel"),
    ("K270", "mid_crown_fit", "the crown mid-settling onto the verdict of her hands, the weight agreeing"),
    ("K271", "mid_pit_count", "the cherry pit mid-drop into her palm's tally"),
    ("K272", "mid_sunset_fold", "the folded sunset mid-tuck under her arm, the light folding like cloth"),
]
X4_KS = [
    ("K273", "mid_cage_headboard", "the headboard's rails mid-taking both braced palms, the weight arriving forward between them"),
    ("K274", "mid_cage_shelf", "the shelf-boards mid-accepting the two flat palms, the books leaning away from the press"),
    ("K275", "mid_cage_couch", "the couch-back mid-sinking under her braced forearms, the cushion's give already hers"),
    ("K276", "mid_cage_glass", "the pane mid-fogging where her breath lands, the two palms holding their lines"),
    ("K277", "mid_cage_jamb", "the door-jamb mid-carrying both palms, the wood grain lifting under the press"),
    ("K278", "mid_cage_poolside", "the pool's stone lip mid-taking both wrists, the waterline swaying with her weight"),
    ("K279", "mid_cage_furwall", "the hanging coats mid-parting under her forearms, the hangers rolling aside"),
    ("K280", "mid_cage_counter", "the counter's lip mid-taking the spread fingers, the till's drawer half-open"),
    ("K281", "mid_cage_larder", "the larder's brick mid-catching the two flat palms, the jars keeping their cool"),
]
OC_KS = [
    ("K282", "mid_organ_column", "the palm mid-settling on the single pipe, the metal remembering the warmth"),
    ("K283", "mid_stake_strike", "the flat palm mid-strike driving the stake's head a hair deeper"),
    ("K284", "mid_stud_catch", "the studded collar mid-catching the street's shine, stud by stud"),
]
po = load('pools.json')
po['version'] = '1.3.0'
kin = po['sections']['kinetics_k']
existingK = {x['id'] for x in kin}
for pid, name, sd in MAIN_KS + X4_KS:
    assert pid not in existingK, pid
    kin.append({"id": pid, "name": name, "sd": sd, "source": "T5-19 K-FF"})
for pid, name, sd in OC_KS:
    kin.append({"id": pid, "name": name, "sd": sd, "source": "T5-19 canon-OS K-FF"})
save('pools.json', po)

# ── races.json 2.6.0 (+R62–70) ───────────────────────────────────────────
NEW_RACES = [
    ("R62", "Fennec-kin", "Тыша",
     ["oversized fennec ears that swivel toward whatever interests her before the head turns",
      "cream-sand fur pale as dry grass", "black-tipped tail with a soft brush",
      "large amber-dark eyes with a night-vision shine"],
     ["oversized fennec ears swiveled toward the lens", "cream-sand fur pale as dry grass",
      "black-tipped tail brush", "amber-dark eyes with a night shine"],
     "T5-19 кандидат X4 «В-КЛЕТКУ» #1: уши-локаторы разворачиваются на зрителя раньше головы — клетку её рук читают уши первыми; collision: R04 Cat-kin / R03 Kitsune не задеты (треугольник ушей с тёмной кромкой); light: кромки ушей ловят ключ первыми"),
    ("R63", "Magpie-kin", "Крада",
     ["long magpie tail with an oil-sheen green-blue cast", "black-and-white plumage mapping the shoulders with a white belly panel",
      "quick clever fingers", "one wing-fold line along the arm"],
     ["long magpie tail with an oil-sheen green-blue cast", "black-and-white plumage with a white belly panel",
      "quick clever fingers", "wing-fold line along the arm"],
     "кандидат #2: хвост-балансир рисует геометрию кадра, пальцы всегда заняты блеском; light: хвост несёт масляный отлив в контровом"),
    ("R64", "Lynx-kin", "Кисть",
     ["lynx ear-tufts standing like antennae", "spot-pattered winter fur on shoulders and forearms",
      "wide quiet paws with a silent step", "short tail with a black tip"],
     ["lynx ear-tufts standing like antennae", "spot-pattered winter fur on the shoulders",
      "wide quiet paws", "short black-tipped tail"],
     "кандидат #3: кисточки — антенны настроения (морда ровная, кисточки дрожат); collision: R54 Snow-leopard-kin не задет (пятна-точки, не розетки); light: кисточки режут контровой свет"),
    ("R65", "Mantis-kin", "Серп",
     ["forearms folded in a praying-triangle of smooth chitin", "leaf-green skin with a pale vein-map",
      "triangular face tilting with uncanny patience", "delicate wing-shelves folded along the spine"],
     ["forearms folded in a praying triangle", "leaf-green skin with a pale vein-map",
      "triangular face tilted patient", "wing-shelves folded along the spine"],
     "кандидат #4: серпы сложены аккуратно — молитва, которая не режет кадр; light: хитин ловит холодный глянец"),
    ("R66", "Pangolin-kin", "Чешка",
     ["scale-mantle draping shoulder to hip like a settled cloak", "each scale edged in a warm horn-line",
      "soft pale under-skin at the wrists and throat", "tail curled into a half-question mark"],
     ["scale-mantle draped shoulder to hip", "horn-edged scales",
      "soft pale under-skin at wrists and throat", "tail curled half-question"],
     "кандидат #5: черепица чешуи лежит ровно, приподнимаясь только краем на вдохе; light: чешуя даёт ступенчатый блик"),
    ("R67", "Axolotl-kin", "Мила",
     ["three frilled gill-plumes at each side of the head, blush-pink, moving with mood",
      "smooth water-pale skin with a faint pearl cast", "wide gentle mouth reading as a settled smile",
      "feathered tail-fin low behind"],
     ["three blush-pink gill-plumes each side of the head", "water-pale skin with a pearl cast",
      "wide gentle settled smile", "feathered tail-fin"],
     "кандидат #6: лицо спокойно — настроение читают перья жабр; collision: R17 Jellyfish-kin / R13 Merfolk не задеты (жабры-пёрышки, не купол и не рыбий хвост); light: перья подсвечиваются контражуром"),
    ("R68", "Chinchilla-kin", "Плюша",
     ["plush grey-blue fur lifting a halo under back light", "wide thin ears that flush pink when she warms",
      "powder-soft tail", "small rounded muzzle"],
     ["plush grey-blue fur lifting a halo in back light", "wide thin ears flushing pink",
      "powder-soft tail", "small rounded muzzle"],
     "кандидат #7: пух ловит контровой ореолом; фыркнула — вскинулся весь пух; light: ореол пуха держит свет за контуром"),
    ("R69", "Ermine-kin", "Тайка",
     ["winter-white ermine pelt with the black tail-tip writing its own flourish",
      "sleek collar-to-cuff fur line", "dark quick eyes with a bead-bright gleam", "small pointed face"],
     ["winter-white pelt with a black tail-tip", "sleek fur line collar to cuff",
      "dark bead-bright eyes", "small pointed face"],
     "кандидат #8: кисточка-хвост ставит росчерк в композиции; light: белая шубка держит снежный блик"),
    ("R70", "Mole-kin", "Копка",
     ["star-tipped pink nose reading the air in small quick twitches", "velvet dark-mauve fur, matte, light-eating",
      "eyes as soft slits, half-shut against daylight", "wide flat digging hands with pale palms"],
     ["star-tipped pink nose mid-read of the air", "velvet dark-mauve fur matte",
      "eyes as soft half-shut slits", "wide digging hands with pale palms"],
     "кандидат #9: смотрит носом — линия «взгляда» идёт от звезды-носа в линзу, глаза-щёлки всё равно в кадре; light: бархат шубки гасит блик, свет держат нос и ладони"),
]
r = load('races.json')
r['version'] = '2.6.0'
existingR = {x['id'] for x in r['races']}
for rid, name, cand, features, pos_tags, note in NEW_RACES:
    assert rid not in existingR, rid
    r['races'].append({
        "id": rid, "name": name, "status": "active", "features": features,
        "pos_tags": pos_tags, "note": f"{note}; кандидат-коднейм «{cand}» — временный, имя при канонизации за автором (прецедент Meine/Luvv/Liebe/Hana)",
    })
save('races.json', r)

print('OK: poses 1.9.0 | palettes 1.4.0 | camera 1.6.0 | pools 1.3.0 | races 2.6.0')
