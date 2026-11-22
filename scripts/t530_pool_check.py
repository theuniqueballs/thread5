#!/usr/bin/env python3
"""T5-30: точный расчёт запретов карт — по НАЗНАЧЕНИЯМ (поле Y-card:),
не по упоминаниям в прозе. Окно = 3 сданные (T5-26/27/29) + №28 ready
(прямые дубли неаккуратны, прецедент карзамена T5-29)."""
import json
import re
from pathlib import Path

ROOT = Path('/home/z/my-project')
BATCHES = ROOT / 'batches'
cam = json.load(open(ROOT / 'specs/camera.json'))
cards = {c['id']: c for c in cam['y_cards']['cards']}


def assigned_cards(md_path):
    """Назначенные карты партии: поле Y-card + шапки слотов (жребий)."""
    text = md_path.read_text(encoding='utf-8')
    out = set(re.findall(r'^Y-card:\s*(Y\d{1,3})', text, re.M))
    return out

# окно = 3 сданные
window_cards = set()
for name in ('T5-26.md', 'T5-27.md', 'T5-29.md'):
    window_cards |= assigned_cards(BATCHES / name)
b28_cards = assigned_cards(BATCHES / 'T5-28.md')
print(f'окно (T5-26/27/29, назначения): {len(window_cards)} карт')
print(f'№28 ready (назначения): {len(b28_cards)} карт')

draw_oc = ['Y348', 'Y375', 'Y388']
draw_main = 'Y302 Y194 Y69 Y237 Y239 Y421 Y451 Y246 Y414 Y411 Y173 Y287 Y168 Y188 Y154 Y480 Y6 Y93 Y82 Y181 Y85'.split()
draw_exp = 'Y307 Y59 Y468 Y382 Y128 Y78 Y420 Y407 Y220'.split()

print('\n── ЖРЕБИЙ vs ЗАПРЕТЫ ──')
for grp, ids in (('OC', draw_oc), ('МЕЙН', draw_main), ('EXP', draw_exp)):
    for y in ids:
        tags = []
        if y in window_cards:
            tags.append('ОКНО')
        if y in b28_cards:
            tags.append('№28')
        if tags:
            print(f'  {grp} {y}: {" + ".join(tags)}')

oc_final = {'Noxx': 'Y375', 'Ama': 'Y388', 'Dove': 'Y446'}
main_rplus = ['Y451', 'Y411', 'Y168', 'Y480', 'Y82', 'Y6',
              'Y89', 'Y359', 'Y366', 'Y320', 'Y334', 'Y452', 'Y415', 'Y363']
main_niche = ['Y69', 'Y414', 'Y93', 'Y246', 'Y287', 'Y85', 'Y173']
exp_cards = ['Y147', 'Y209', 'Y342', 'Y428', 'Y492', 'Y356', 'Y30', 'Y32', 'Y33']

all_picks = list(oc_final.values()) + main_rplus + main_niche + exp_cards
print('\n── ВЫБОРЫ vs ЗАПРЕТЫ ──')
ok = True
for y in all_picks:
    tags = []
    if y in window_cards:
        tags.append('ОКНО!')
    if y in b28_cards:
        tags.append('№28!')
    if y not in cards:
        tags.append('НЕТ В camera.json!')
    if tags:
        ok = False
        print(f'  {y}: {" + ".join(tags)}')
dups = sorted({y for y in all_picks if all_picks.count(y) > 1})
if dups:
    ok = False
    print('  ДУБЛИ внутри батча:', dups)
print('  выборы чисты ✓' if ok else '  !! КОНФЛИКТЫ')

print('\n── ПАСПОРТА ──')
for grp, ids in (('OC', list(oc_final.values())), ('R+-МЕЙН', main_rplus),
                 ('NICHE', main_niche), ('EXP', exp_cards)):
    for y in ids:
        c = cards[y]
        comp = c.get('components') or {}
        exp = comp.get('exposure') or {}
        cls = exp.get('class', '—')
        print(f'  {grp:9s} {y:5s} corr={c.get("corridor","?"):4s} class={cls:13s} '
              f'{(comp.get("pose") or "")[:72]}')

banned = window_cards | b28_cards | set(all_picks)
pool_ab = []
for yid, c in cards.items():
    if yid in banned:
        continue
    comp = c.get('components') or {}
    exp = comp.get('exposure') or {}
    cls = exp.get('class', '—')
    if cls in ('COVER', 'PROCESS', 'LINGERIE', 'CLOTHED-TIGHT', 'SHEER') \
            and c.get('corridor') in ('A', 'A+B', 'B'):
        pool_ab.append((yid, c.get('corridor'), cls))
print(f'\nсвободных A/B класс-карт после всех выборов: {len(pool_ab)}')
print(', '.join(f'{y}({c}/{k})' for y, c, k in sorted(pool_ab)))

# жанровый план мейнов (В39): бег ≤ 3, вперемешку
plan = ('NICHE VOLT VOLT NICHE VOLT EXQUISITE VOLT NICHE VOLT VOLT NICHE VOLT VOLT '
        'NICHE VOLT EXQUISITE NICHE VOLT VOLT NICHE VOLT').split()
assert len(plan) == 21, len(plan)
run = cur = 1
for i in range(1, len(plan)):
    cur = cur + 1 if plan[i] == plan[i-1] else 1
    run = max(run, cur)
volt = sum(1 for g in plan if g in ('VOLT', 'EXQUISITE'))
niche = plan.count('NICHE')
exq = plan.count('EXQUISITE')
print(f'\nжанровый план: {len(plan)} позиций · вольт-масса {volt} · ниша {niche} · '
      f'EXQUISITE {exq} · макс бег {run}')
