#!/usr/bin/env python3
"""T5-28 CLOCK: В27-пересборка слабых карт (LAWS §17.4, прецедент T5-27 волна 1)
+ волна 14 каналов доставки (delivery-stats 0.13.0 -> 0.14.0)."""
import json, sys

# ---------- 1. camera.json: В27-пересборка ----------
CAM = 'specs/camera.json'
d = json.load(open(CAM, encoding='utf-8'))
cards = d['y_cards']['cards']
idx = {c['id']: c for c in cards}

REBUILD = {
    # OC
    'Y316': ("cross-legged lean-back against a firm pew-back, the spine's weight given over to the wood, "
             "one palm fanned flat on the psalter's cover, the habit's front pulled taut by the lean "
             "+ upper body three-quarter"),
    'Y217': ("sitting cross-legged, both palms flat on the ground behind bearing the shoulders' full weight, "
             "chest lifted to the ceiling, head thrown back, throat leading, the stretch's pull riding the ribs "
             "+ eye level"),
    # мейн R+
    'Y237': ("upper-body close: forehead to a cool wall, eyes closed, both palms flat to the surface at the "
             "shoulders, the wall taking the whole pulse's weight + upper body three-quarter"),
    # EXP R+
    'Y437': ("shaking the dice cup over her own palm, the cup's rattle riding the wrist's snap, "
             "dice already settling stacked in her favor + CAM01"),
    'Y92':  ("sitting cross-legged, both palms cupping own chin, elbows on knees, weight tipped forward "
             "into the viewer's space, the neckline falling with the lean, full attention"),
    'Y47':  ("kneeling with both palms flat on the ground, hips lifted high under their own weight, "
             "head down between the arms, the arch holding like a drawn bow + CAM12_aerial"),
    'Y348': ("crouched low on the chalk blueprint spread across the floor, one palm flat on a pine sapling "
             "growing along the drawn circle, the crouch's weight balanced on the balls of the feet, "
             "the hem pooling in the chalk dust"),
    'Y328': ("sitting on the stone edge, feet trailing in the water, the towel hugged tight to the chest "
             "with both forearms, its tuck's weight held honest, steam rising + upper body three-quarter"),
}
changed = []
for yid, newpat in REBUILD.items():
    c = idx[yid]
    old = c['pattern']
    if old.strip() != newpat.strip():
        c['pattern'] = newpat
        changed.append(yid)

d['version'] = '1.18.0'
cl = d.get('changelog')
entry = ("1.18.0 (2026-11-21, T5-28 CLOCK): В27-пересборка волна 2 (прецедент — волна 1 T5-27, LAWS §17.4): "
         + ', '.join(changed) + " — физика (вес/тяга/зацеп) влита в паттерны ДО сборки, карты получили право на R+; "
         "клеймо переродилось само. Компоненты/коридоры/id не тронуты — паритет жребия побитово цел.")
if isinstance(cl, list):
    cl.insert(0, entry)
elif isinstance(cl, dict):
    cl['1.18.0'] = entry
else:
    d['changelog'] = entry
json.dump(d, open(CAM, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('camera.json -> 1.18.0; rebuilt:', ', '.join(changed))

# ---------- 2. delivery-stats.json: волна 14 ----------
DS = 'specs/delivery-stats.json'
ds = json.load(open(DS, encoding='utf-8'))
WAVE14 = [
    ("plugsuit-pressure-seal", "Plugsuit Pressure-Seal",
     "винил плагсьюта как вторая кожа: шов герметизации читает форму давлением, ткань-нетканое тело; тир несёт натяжение, не прозрачность"),
    ("pew-sprawl-lie-back", "Pew Sprawl Lie-Back",
     "развал в нефе: вес целиком отдан спинке скамьи, мантия натянута прогибом, псалтырь-веер прижат к груди; святое место, карнальная посадка"),
    ("kill-hill-throat-sky", "Kill-Hill Throat-Sky",
     "растяжка победительницы: ладони в землю за спиной, грудь к небу, горло ведёт; экспозиция рождается изгибом победы, не из раздевания"),
    ("party-wall-pulse", "Party-Wall Pulse",
     "стена-мембрана: лоб и ладони плоско к штукатурке, чужой пульс читается сквозь толщу; кадр слушает комнату рядом"),
    ("mirror-fog-rehearse", "Mirror-Fog Rehearse",
     "полотенце в размахе флипа, зеркало запотело от репетиций улыбки; заявка живёт в мокрой ткани и отражении"),
    ("bell-hem-crook", "Bell-Hem Crook",
     "юбка-купол собрана в сгиб локтя: вес подола висит на руке, колокол ткани держит форму — прикрытие весом, не поверхностью"),
    ("caught-name-hold", "Caught-Name Hold",
     "имя поймано на лету: обе ладони плоско к груди как клетка для птицы-пульса; heartbeat читается пальцами"),
    ("grate-updraft-press", "Grate Updraft Press",
     "восходящий поток решётки против обеих ладоней: юбка-колокол спорит с ветром, колени вместе, смех вниз — Мэри-момент без юбки-результата"),
    ("knock-catch-towel", "Knock-Catch Towel",
     "стук в дверь на середине ванны: полотенце соскальзывает и ловится обеими руками у груди, колени внутрь — паника как заявка"),
    ("borrowed-wood-hum", "Borrowed-Wood Hum",
     "его гитара на её плече: ремень торком через грудь, прикрытие сгибом локтя, дека гудит под чужими пальцами — чужая вещь как индульгенция"),
]
have = {c['id'] for c in ds['channels']}
added = 0
for cid, name, note in WAVE14:
    if cid in have:
        continue
    ds['channels'].append({
        "id": cid, "name": name, "status": "candidate", "tier": "R+",
        "attempts": 1, "delivered": 0,
        "evidence": ["T5-28"],
        "note": note,
    })
    added += 1
ds['version'] = '0.14.0'
json.dump(ds, open(DS, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(f'delivery-stats.json -> 0.14.0; wave 14 added: {added} channels')
