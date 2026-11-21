#!/usr/bin/env python3
"""T5-29: обновление реестров — волна 13 палитр, волна 15 каналов, кандидаты ОС,
запись в delivery-index (draft → ready после гейтов)."""
import json
import sys
from pathlib import Path

ROOT = Path('/home/z/my-project')
sys.path.insert(0, str(ROOT / 'scripts'))
from t529_build import WAVE13, WAVE15_CHANNELS, SLOTS, BT_MAP  # noqa

# ── 1. palettes.json: волна 13 ──
pal_path = ROOT / 'specs' / 'palettes.json'
pal = json.loads(pal_path.read_text(encoding='utf-8'))
existing_ids = {p['id'] for p in pal['palettes']}
added = 0
for w in WAVE13:
    if w['id'] in existing_ids:
        continue
    entry = {
        "id": w['id'], "name": w['name'],
        "dominant": w['dominant'], "secondary": w['secondary'],
        "accent1": w['accent1'], "accent2": w['accent2'],
        "shadow": w['shadow'], "forbidden": w['forbidden'],
        "light_type": w['light_type'], "sd_fragment": w['sd_fragment'],
        "mood": w['mood'], "family": w['family'],
        "born": f"2026-11-22, T5-29 «THE SECRETS BEHIND AURORA DUNGEON» — {w['born_note']}",
        "trial": "trial до вердикта T5-29",
    }
    pal['palettes'].append(entry)
    added += 1
pal['exp_color_waves'].append({
    "wave": "exp_color_wave_13",
    "name": "свет подземелья",
    "born": "2026-11-22, T5-29 «THE SECRETS BEHIND AURORA DUNGEON» — заказ автора: «9 новых раскрасок и экспериментальных палитр»",
    "methods": "жила сияния (aurora as vein) / моховая кромка (moss-edge light) / мел оссуария (chalk pale) / выращенный свет (spore backlight) / нить-шёлк (thread sheen) / паводок-патина (flooded waterline) / латунь архива (brass glow) / сумеречная привязь (dusk that clothes) / сердце-пульс (the heart's pulse)",
    "note": "9 РАЗНЫХ механик света подземелья: свет — поведение, не прибор (закон v2); семьи ни разу не выходили (волны 1–12 не пересекаются)",
    "palette_ids": [w['id'] for w in WAVE13],
})
pal['version'] = '1.15.0'
pal_path.write_text(json.dumps(pal, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
print(f"palettes.json: +{added} палитр волны 13, версия 1.15.0, всего {len(pal['palettes'])}")

# ── 2. delivery-stats.json: волна 15 каналов ──
ds_path = ROOT / 'specs' / 'delivery-stats.json'
ds = json.loads(ds_path.read_text(encoding='utf-8'))
have = {c['id'] for c in ds['channels']}
added = 0
for cid, name, slot, note in WAVE15_CHANNELS:
    if cid in have:
        continue
    ds['channels'].append({
        "id": cid, "name": name, "status": "candidate", "tier": "R+",
        "attempts": 1, "delivered": 0, "evidence": ["T5-29"], "note": note,
    })
    added += 1
ds['version'] = '0.15.0'
ds_path.write_text(json.dumps(ds, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
print(f"delivery-stats.json: +{added} каналов волны 15, версия 0.15.0, всего {len(ds['channels'])}")

# ── 3. oc-candidates.json: 9 кандидатов EXP ──
oc_path = ROOT / 'specs' / 'oc-candidates.json'
occ = json.loads(oc_path.read_text(encoding='utf-8'))
RACE_NAME = {
    'R18': 'Gargoyle-kin', 'R33': 'Ghost-kin', 'R43': 'Dullahan-kin',
    'R32': 'Golem-kin', 'R35': 'Arachne-kin', 'R25': 'Slime-girl',
    'R21': 'Mushroom-kin', 'R45': 'Shadow-kin', 'R50': 'Nine-tails-kin',
}
NOTES = {
    'P25': 'гаргулья, кончающая век стояния: куртка сползает с плеча, мох на карнизе — биография зелёным',
    'P26': 'призрак-экспонат: подземелье держит её за запястья парящими ладонями — единственное прикосновение, которое регистрирует',
    'P27': 'дуллахан с двумя мнениями: гетерохромия головы и тела, перчатка снимается с руки, что держала голову',
    'P28': 'голем-архивариус: память выбита на предплечье, подол подтянут поднятой к полке рукой',
    'P29': 'арахна у вязания: четыре руки — спицы, перчатка, чай; подарок всегда тёплый',
    'P30': 'слизь-уборщица затопленного яруса: вещи на сантиметр в неё возвращаются чище',
    'P31': 'грибница-фонарщица: свет, который выращивают; смех придержан — иначе споры погасят ярус',
    'P32': 'тень в виниловом плаще: свет договаривается с ней сквозь прозрачность',
    'P33': 'девятихвостка на троне сердца: гость сидит на её месте — она села ему на колени',
}
have_c = {c.get('slot') for c in occ.get('candidates', [])}
added = 0
for s in SLOTS:
    if s['sid'] < 'P25':
        continue
    if s['sid'] in have_c:
        continue
    race_id = next((t for t in s['paren'].split() if t.startswith('R') and t[1:].isdigit()), None)
    pal_id = next((t for t in s['paren'].split() if t.startswith('P2')), None)
    occ['candidates'].append({
        "slot": s['sid'], "batch": "T5-29", "race": f"{race_id} {RACE_NAME[race_id]}",
        "bodytype": BT_MAP[s['sid']],
        "marks": "MK-E01 (oc_hook)" if s['sid'] == 'P27' else "—",
        "gimmick": s['race'].split('— ')[1].split('.')[0] if '— ' in s['race'] else s['race'][:60],
        "palette": pal_id, "y_card": s['ycard'],
        "oc_hook_mark": "MK-E01" if s['sid'] == 'P27' else None,
        "status": "trial",
        "note": NOTES[s['sid']],
    })
    added += 1
occ['version'] = '1.1.0'
oc_path.write_text(json.dumps(occ, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
print(f"oc-candidates.json: +{added} кандидатов, версия 1.1.0")

# ── 4. delivery-index.json: запись T5-29 (draft) ──
di_path = ROOT / 'specs' / 'delivery-index.json'
di = json.loads(di_path.read_text(encoding='utf-8'))
if not any(b['batch'] == 'T5-29' for b in di['batches']):
    di['batches'].append({"batch": "T5-29", "status": "draft",
                          "note": "собран 2026-11-22; после гейтов → ready"})
    di_path.write_text(json.dumps(di, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print("delivery-index.json: T5-29 draft")
else:
    print("delivery-index.json: T5-29 уже есть")
print("реестры готовы")
