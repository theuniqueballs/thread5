#!/usr/bin/env python3
"""T5-29 планировщик: жребий + карзамен + EXP-пул у потолка R+."""
import json, re, sys
from pathlib import Path

ROOT = Path('/home/z/my-project')
cam = json.load(open(ROOT/'specs/camera.json'))
cards = {c['id']: c for c in cam['y_cards']['cards']}
poses = {p['id']: p for p in json.load(open(ROOT/'specs/poses.json')).get('poses', [])}

# --- окно ротации (T5-25/26/27) — Y-карты из файлов партий ---
win_cards = set()
for b in ('T5-25', 'T5-26', 'T5-27'):
    txt = open(ROOT/f'batches/{b}.md').read()
    win_cards |= set(re.findall(r'\bY(\d{1,3})\b', txt))
win_cards = {'Y'+n for n in win_cards}
# точный список из window.py-квитанции T5-28 (агрегат 57):
receipt = open(ROOT/'batches/T5-28/window.md').read()
m = re.search(r'Y-карты.*?\n(.*?)(?:\n\n|\n[А-Я#])', receipt, re.S)
win_exact = set(re.findall(r'Y\d{1,3}', receipt))
# позы окна (95)
win_poses = set(re.findall(r'PL\d{1,3}', receipt))
# T5-28 использованные карты (гейты)
t528_cards = set("Y2 Y10 Y19 Y21 Y29 Y36 Y47 Y81 Y90 Y92 Y98 Y106 Y117 Y158 Y161 Y184 Y194 Y207 Y216 Y217 Y237 Y239 Y292 Y293 Y302 Y316 Y328 Y348 Y370 Y403 Y437 Y442 Y494".split())

def info(cid):
    c = cards.get(cid)
    if not c:
        return f"{cid}: НЕТ"
    e = c.get('components', {}).get('exposure', {})
    pl = c.get('builtFrom', '')
    flags = []
    if cid in win_exact: flags.append("ОКНО!")
    if cid in t528_cards: flags.append("T5-28!")
    if pl and pl in win_poses: flags.append(f"Поза-окно!({pl})")
    return (f"{cid} [{c['corridor']}/{e.get('class','—')}] PL={pl} {' '.join(flags)}\n    {c['pattern'][:150]}")

print("=== ЖРЕБИЙ ОС (Y293 дубль → замена, Y26, Y497) ===")
for cid in ('Y293', 'Y26', 'Y497', 'Y37', 'Y5'):
    print(info(cid)); print()

print("=== КАНДИДАТЫ НА ЗАМЕНУ Y293 (A/A+B, COVER, чистые, без поз-окна/T5-28) ===")
def clean(c):
    cid = c['id']
    e = c.get('components', {}).get('exposure', {})
    if c['corridor'] not in ('A', 'A+B'): return False
    if e.get('class') != 'COVER': return False
    if cid in win_exact or cid in t528_cards: return False
    pl = c.get('builtFrom', '')
    if pl and pl in win_poses: return False
    return True
cands = [c for c in cards.values() if clean(c)]
cands.sort(key=lambda c: int(c['id'][1:]))
for c in cands[:40]:
    print(f"{c['id']} [{c['corridor']}] PL={c.get('builtFrom','')} · {c['pattern'][:120]}")
print(f"... всего чистых A/A+B COVER: {len(cands)}")

print("\n=== ЗАМЕНЫ ДЛЯ МЕЙН-ДУБЛЕЙ (Y98/Y239/Y10) ===")
print("Нужны: 2×A (COVER) + 1×B")

print("\n=== EXP-ПУЛ: PROCESS A-карты (свежие для потолка) ===")
for cid in ('Y9', 'Y12', 'Y18', 'Y27', 'Y26', 'Y37', 'Y1'):
    print(info(cid)); print()

print("=== САМЫЕ ДЕРЗКИЕ COVER A-карты (handbra/towel/palm/minimal) ===")
import re as _re
bold_kw = ('handbra', 'hand bra', 'palm', 'towel', 'steam', 'foam', 'soap', 'one finger', 'finger', 'barely', 'single', 'lift')
for c in cands:
    p = c['pattern'].lower()
    if any(k in p for k in bold_kw):
        print(f"{c['id']} [{c['corridor']}] · {c['pattern'][:130]}")
