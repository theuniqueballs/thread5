# -*- coding: utf-8 -*-
"""Разбор поз (приказ автора 2026-11-13): нормализация enum, статусные пометки
семьям-экспериментам, версия 1.9.0 → 1.10.0. Детальный razbor живёт в
docs/POSE-RAZBOR-2026-11-13.md — здесь только машинные патчи."""
import json
from collections import Counter

PATH = 'specs/poses.json'
d = json.load(open(PATH, encoding='utf-8'))
poses = d['poses']

patched = {'mid': 0, 'x2': 0, 'x4': 0, 'x3': 0, 'x1': 0, 'erotic': 0}

for p in poses:
    # 1) enum-гигиена: MEDIUM → MID (волна T5-17)
    if p.get('risk') == 'MEDIUM':
        p['risk'] = 'MID'
        patched['mid'] += 1

    fam = p.get('family', '')
    # 2) статусные пометки по вердиктам
    notes = {
        'X2': 'архив эксперимента (вердикт T5-17: «вышло слабовато») — в ротацию не ставить, реюз только ребилдом комбо',
        'X4': 'архив эксперимента (вердикт T5-19: «не особо»; P25 — единственный зачёт и референс X5: навал + намёк на около-эротику)',
        'X3': 'клетка расформирована: ядро 6/9 принято вердиктом 2026-11-10 — карты живут как NV в обычной ротации (EXP-константа снята)',
        'X1': 'ЖИВАЯ семья (вердикт T5-16 принял комбо; авторские пики PL358/359/361/362) — первый приоритет VOLT-ротации',
    }
    if fam in notes:
        p['use_note'] = notes[fam]
        patched[fam.lower().replace('x', 'x', 1) if fam != 'X1' else 'x1'] += 1
    elif fam in ('erotic_presentation', 'erotic_presentation_v2'):
        p['use_note'] = ('R+ движок библиотеки: геометрия HIGH — по §4.9 законна в R и ниже; '
                         'R+ добирается каналом дрессера (bumps/on_skin/pantyline/through) поверх LOW/MID геометрии')
        patched['erotic'] += 1

# 3) use_division: аудит-пометка
use = Counter(p.get('use', '?') for p in poses)
d['use_division']['audit'] = (
    "2026-11-13 (razbor, приказ автора «сунься туда где у нас позы и разбери»): делёж "
    "перечитан по всем 468 картам. Исправлено: enum MEDIUM→MID (19), статус-пометки "
    "X1–X4 (вердикты T5-16/17/18/19), R+ движку (erotic_presentation 12+24) прописан "
    "потолок: геометрия HIGH = R и ниже, R+ достраивает дрессер. Главное правило "
    "разбора: use=V/N — первичный контур, НЕ эксклюзив; полная таблица — "
    "docs/POSE-RAZBOR-2026-11-13.md. Поле use остаётся V для X2/X4 как память семьи "
    "(архивность несёт use_note).")
d['use_division']['counts'] = {'N': use['N'], 'NV': use['NV'], 'V': use['V']}

# 4) версия + changelog
d['version'] = '1.10.0'
d['changelog'].insert(0, "2026-11-13 — 1.10.0 razbor: enum-гигиена (MEDIUM→MID ×19); статус-пометки "
    "семьям X1 (живая) / X2 (архив, T5-17) / X3 (ядро 6/9 → NV) / X4 (архив, T5-19); R+ движку "
    "(PL49–60, PL181–204) прописан потолок §4.9 и канал-зависимость; use_division.audit. "
    "Полный разбор — docs/POSE-RAZBOR-2026-11-13.md")

json.dump(d, open(PATH, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('OK poses.json 1.10.0:', patched, '| use counts:', dict(use))
