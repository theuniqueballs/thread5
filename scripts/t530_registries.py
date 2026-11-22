#!/usr/bin/env python3
"""T5-30 · реестровые записи (исполнение сборки):
  1. palettes.json 1.15.0 → 1.16.0 — волна 14 «покрытия-настроения» P270–P278 (trial)
  2. delivery-stats.json 0.15.0 → 0.16.0 — волна 16: кандидаты strap-line-hold ☠,
     element-linen ☠ (квота ≤2 соблюдена: ОС на oc-rplus exempt, R+-мейны на live)
  3. oc-candidates.json 1.2.0 → 1.3.0 — девятка кандидатов T5-30 (P25–P33)
  4. delivery-index.json — T5-30 ready (31 партия в индексе)
  5. furnace-ledger.json 1.7.0 → 1.8.0 — F-026 (сборка T5-30)
  6. batches/T5-30/stories.md — карточки историй (story-cards gate)
  7. batches/T5-30/window.md — квитанция станции окна (window.py --for T5-30)
  8. README.md — счётчики
"""
import json
import re
import subprocess
from pathlib import Path

ROOT = Path('/home/z/my-project')
SPECS = ROOT / 'specs'


def load(name):
    return json.loads((SPECS / name).read_text(encoding='utf-8'))


def save(name, doc):
    (SPECS / name).write_text(
        json.dumps(doc, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')


# ── 1. palettes.json: волна 14 ──────────────────────────────────────────
pal = load('palettes.json')
assert pal['version'] == '1.15.0', pal['version']
import importlib.util
spec = importlib.util.spec_from_file_location('t530_build', ROOT / 'scripts' / 't530_build.py')
# читаем WAVE14 из build-скрипта без запуска main
src = (ROOT / 'scripts' / 't530_build.py').read_text(encoding='utf-8')
ns = {}
exec(compile(src.split('# ══════════════════ слоты')[0], 't530_build_head', 'exec'), ns)
WAVE14 = ns['WAVE14']
have = {p['id'] for p in pal['palettes']}
for w in WAVE14:
    assert w['id'] not in have, w['id']
    pal['palettes'].append(w)
pal['version'] = '1.16.0'
waves = pal.setdefault('exp_color_waves', [])
if isinstance(waves, list):
    waves.append({
        'wave': 14, 'name': 'покрытия-настроения', 'batch': 'T5-30',
        'born': '2026-11-22, заказ автора «9 новых раскрасок и экспериментальных палитр»',
        'ids': [w['id'] for w in WAVE14],
    })
save('palettes.json', pal)
print(f"1. palettes.json → 1.16.0 (+{len(WAVE14)} палитр волны 14, всего {len(pal['palettes'])})")

# ── 2. delivery-stats.json: волна 16 (2 кандидата) ──────────────────────
ds = load('delivery-stats.json')
assert ds['version'] == '0.15.0', ds['version']
ch_ids = {c['id'] for c in ds['channels']}
WAVE16 = ns['WAVE16_CHANNELS']
for cid, (name, note) in WAVE16.items():
    assert cid not in ch_ids, cid
    ds['channels'].append({
        'id': cid, 'name': name, 'status': 'candidate', 'tier': 'R+',
        'attempts': 1, 'delivered': 0, 'evidence': ['T5-30'],
        'note': note + ' | волна 16 (T5-30): квота кандидатов ≤2 соблюдена — '
                       'ОС на oc-rplus (exempt), R+-мейны на live-каналах с A/B-подачей',
    })
ds['version'] = '0.16.0'
save('delivery-stats.json', ds)
print(f"2. delivery-stats.json → 0.16.0 (+2 канала волны 16, всего {len(ds['channels'])})")

# ── 3. oc-candidates.json: девятка T5-30 ────────────────────────────────
oc = load('oc-candidates.json')
assert oc['version'] == '1.2.0', oc['version']
NEW = [
    ('P25', 'R15 Porcelain-doll', 'BT-03', 'кукла: держит позы на полсекунды дольше — привычка витринной полки',
     'P270_GLASSBITE_MINT', 'Y147', 'H-12', 'полсекунды на борту: пятки в такте, шарниры в блике'),
    ('P26', 'R16 Moth-kin', 'BT-22', 'мотылёк: дрейфует к теплу посреди фразы',
     'P272_STATIC_LILAC', 'Y209', 'H-10', 'доставка взгляда: вырез-рама, зритель снизу'),
    ('P27', 'R24 Oni-kin', 'BT-20', 'они: рожки стучат по косяку дважды — на удачу',
     'P277_SORBET_STAIN', 'Y342', 'H-13', 'сверхурочная смена: рожки на удачу, румянец-индикатор (кандидат-клетка A)'),
    ('P28', 'R26 Bee-kin', 'BT-06', 'пчела: довольное жужжание при достаточном тепле',
     'P275_URANIUM_GLASS_GLOW', 'Y428', 'H-13', 'счёт колец мха: пальцы-талли, мурлыканье-термометр (кандидат-клетка B)'),
    ('P29', 'R27 Cow-kin', 'BT-15', 'коровка: хвост-флик считает терпение',
     'P271_WAX_SEAL_OXBLOOD', 'Y492', 'H-11', 'контр-качка: вес косой, халат в драке потоков, хвост-терпение'),
    ('P30', 'R31 Flower-kin', 'BT-13', 'цветочная: поворачивается за солнцем — всё растение помнит',
     'P273_FOIL_BALLOON_COPPER', 'Y356', 'H-09', 'именованный подслой «Лаванда»: вышитая метка, жилки-вены'),
    ('P31', 'R23 Shark-kin', 'BT-16', 'акула: слишком много зубов в улыбке победы',
     'P110_RIPOSTE_SILVER', 'Y30', 'H-08', 'пол-прилива: подол мокрый, верх сухой, девятый вал на имя'),
    ('P32', 'R60 Skunk-kin', 'BT-10', 'скунсиха: выигрывает конфликт фактом существования',
     'P278_LEDGER_GREEN', 'Y32', 'H-07', 'каустика льда: талая линза ползёт по зоне заявки'),
    ('P33', 'R62 Fennec-kin', 'BT-23', 'фенек: уши вентилируют жар — видимый румянец',
     'P276_POCKET_DENIM_DUSK', 'Y33', 'H-03', 'средний тон: бинт-спираль в полтона, уши-глоу на просвет'),
]
for slot, race, bt, gim, palid, ycard, hyp, note in NEW:
    oc['candidates'].append({
        'slot': slot, 'batch': 'T5-30', 'race': race, 'bodytype': bt,
        'marks': '—', 'gimmick': gim, 'palette': palid, 'y_card': ycard,
        'oc_hook_mark': None, 'status': 'trial',
        'hypothesis': hyp,
        'note': f'{note} — вердикт T5-30 решает: «беру» → promoted, «не беру» → passed',
    })
oc['version'] = '1.3.0'
oc['stats'] = {'trial': 9, 'passed': 8, 'promoted': 1}
save('oc-candidates.json', oc)
print(f"3. oc-candidates.json → 1.3.0 (+9 кандидатов, всего {len(oc['candidates'])})")

# ── 4. delivery-index.json: T5-30 ready ─────────────────────────────────
di = load('delivery-index.json')
text = json.dumps(di, ensure_ascii=False)
if 'T5-30' not in text:
    # структура: список или dict — приспосабливаемся
    if isinstance(di.get('batches'), list):
        last = di['batches'][-1]
        di['batches'].append({
            'id': 'T5-30', 'title': 'WHAT THE FUCK IS THAT?!', 'status': 'ready',
            'born': '2026-11-22', 'slots': 33, 'receipt': 'specs/gate-receipts/2026-11-22-T5-30-v1.json',
        })
    else:
        di['T5-30'] = {'title': 'WHAT THE FUCK IS THAT?!', 'status': 'ready',
                       'born': '2026-11-22', 'slots': 33}
    save('delivery-index.json', di)
    print('4. delivery-index.json: +T5-30 (ready)')
else:
    print('4. delivery-index.json: T5-30 уже есть')

# ── 5. furnace-ledger.json: F-026 ───────────────────────────────────────
fl = load('furnace-ledger.json')
fl['version'] = '1.8.0'
entries = fl['entries']
if not any(e.get('id') == 'F-026' for e in entries):
    entries.append({
        'id': 'F-026', 'date': '2026-11-22', 'batch': 'T5-30',
        'action': 'сборка боевого батча эры гейтов 1.18.0',
        'detail': ('«WHAT THE FUCK IS THAT?!» 33 слота: 3 ОС (Noxx Эро-Интро / Ama Blurry '
                   'Dreams / Dove Dirty Whore) + 21 мейн (R+×14 · R×7 вперемешку — Закон 24 '
                   'восстановлен, В39) + 9 EXP (кандидаты × комбо у потолка × волна 14, '
                   'H-XX в каждой клетке, В42). Жребий №4 + 10 карзаменов (5 дублей №28, '
                   '4 — Закон 24, 1 — сиблинг-грамма Y413/Y415). Каналы: 4 live с A/B-подачей '
                   '+ волна 16 (2 кандидата — квота ≤2 впервые соблюдена). Рейтинг честен по '
                   'составу (В43): 0 ложных R+ на живом прогоне (калибровка 33/33 держится). '
                   'Работа над ошибками: 31F/105W → 0F/11W → 0F/0W за 9 прогонов (все '
                   'оставшиеся WARN — реестровые, закрыты этим скриптом).'),
        'receipt': 'specs/gate-receipts/2026-11-22-T5-30-v1.json',
    })
save('furnace-ledger.json', fl)
print('5. furnace-ledger.json → 1.8.0 (+F-026)')

# ── 6. stories.md + window.md ───────────────────────────────────────────
bdir = ROOT / 'batches' / 'T5-30'
bdir.mkdir(exist_ok=True)
(bdir / 'stories.md').write_text("""# T5-30 «WHAT THE FUCK IS THAT?!» — карточки историй (бюджет мысли)

Каждый кадр — ОДНА невозможная штука в руках той, для кого она — вторник.
Формула слота: ШТУКА (предмет, LAWS §6) + БЫТ (рутина/инструмент/смена) →
восклицание зрителя. Пять ожиданий Г12 — в шапке батча.

## ОС (P01–P03)
- Noxx · Эро-Интро: порог встречает её огнём — занавес, который отводишь кулаком.
- Ama · Blurry Dreams: идёт из сна, который дождит вверх; полотенце держит два мира.
- Dove · Dirty Whore: витрина дверного проёма; ценник на розовом шнурке — её почерк.

## МЕЙН (P04–P24) — одна штука на кадр
- P04: шахта, дно которой — вчерашний день (мышь-картографка читает её пальцем).
- P05: купель из облака — на полу лужа неба (медуза вытерлась).
- P06: окно в другой сезон — стекло тёплое только с той стороны.
- P07: лестница передаёт свет из руки в руку — смена света опаздывает на 15 минут.
- P08: тень-гамак — держит лежащую на полтора сантиметра ниже пола.
- P09: воздух как паркет — ветер-дева ползёт по нему с подносом (EXQUISITE).
- P10: межевой кол двух погод — молоток отдыхает, лента-крест на груди.
- P11: автобус между мирами — нога на ступени завтра, нога на бордюре вчера.
- P12: 25-й час на циферблате — человек заводит несуществующее время.
- P13: стол находок — вещь, которую не опознал ни один отдел; лента-опознание.
- P14: книги легче воздуха — стопка тянет библиотекаршу вверх.
- P15: единственная сухая стена — предложение, от которого не отказываются.
- P16: саорнг-мёбиус — край ткани сам вырастает бретелью (тануки-фокус).
- P17: простыня-память — дочитывает её сон и не отпускает.
- P18: чайник-рассвет — из носика идёт настоящее утро.
- P19: пожарная дверь отпускает феникса — огонь в волосах по договору (EXQUISITE).
- P20: личный ветер — дует только на её квадрат улицы.
- P21: органная труба без органа — поёт конденсатом, змеи вторят.
- P22: мемориальная стена тёплая ровно у двух имён.
- P23: конёк один — горное равновесие над светящейся водой.
- P24: невидимая служебная лестница с крыши — ступени звучат, но их нет.

## EXP (P25–P33) — гипотезы полки (В42), кандидаты в ОС
- H-12 · P25: полсекунды дольше — mid-action куклы на борту.
- H-10 · P26: вырез как рама — композиция несёт R+ без ткани.
- H-13 · P27/P28: кандидат-клетки A/B — они-электрик и пчела-инвентаризаторша.
- H-11 · P29: тройка анти-стерильности — вес косой, вещь в драке, взгляд-вектор.
- H-09 · P30: именованный подслой «Лаванда» — показан и назван.
- H-08 · P31: пол-прилива — подол мокрый, верх сухой.
- H-07 · P32: каустика талой линзы на зоне заявки.
- H-03 · P33: рельеф на среднем тоне — γ-проба, уши-глоу.

## Счётчик бюджета
- 33 слота: по одной невозможной штуке на мейн (ровно 21/21), ОС — темы автора.
- Жанры вперемешку (бег ≤ 2), вольт-ядро 14/7 — Закон 24.
- Рейтинг по составу (В43): 26 R+ несут холд/стрэп-линию, 7 NICHE — R-токены.
""", encoding='utf-8')
print('6. batches/T5-30/stories.md написан')

# window receipt
r = subprocess.run(['python3', str(ROOT / 'tools' / 'window.py'), '--for', 'T5-30'],
                   capture_output=True, text=True, cwd=ROOT)
(bdir / 'window.md').write_text(r.stdout, encoding='utf-8')
print('7. batches/T5-30/window.md — квитанция окна')

# ── 8. README счётчики ──────────────────────────────────────────────────
rd = ROOT / 'README.md'
txt = rd.read_text(encoding='utf-8')
txt = txt.replace('Партий: 30', 'Партий: 31')
txt = txt.replace('партий: 30', 'партий: 31')
txt = txt.replace('palettes 1.15.0', 'palettes 1.16.0')
txt = txt.replace('delivery-stats 0.15.0', 'delivery-stats 0.16.0')
txt = txt.replace('oc-candidates 1.2.0', 'oc-candidates 1.3.0')
txt = txt.replace('furnace-ledger 1.7.0', 'furnace-ledger 1.8.0')
rd.write_text(txt, encoding='utf-8')
print('8. README.md — счётчики обновлены')
print('\nреестровые записи исполнены')
