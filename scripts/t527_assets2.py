#!/usr/bin/env python3
# T5-27 остаток: палитры волны 12 + каналы волны 13 (poses/camera уже обновлены первым прогоном)
import json

ROOT = '/home/z/my-project/thread5'
def load(p): return json.load(open(f'{ROOT}/{p}', encoding='utf-8'))
def save(p, d): json.dump(d, open(f'{ROOT}/{p}', 'w', encoding='utf-8'), ensure_ascii=False, indent=1); open(f'{ROOT}/{p}','a',encoding='utf-8').write('\n')

pal = load('specs/palettes.json')
if pal['version'] != '1.14.0':
    W12 = [
     dict(id='P252_SHIBORI_STITCH_RESIST', name='Shibori Stitch Resist', dominant=['shibori-indigo deep','thread-bind white'], secondary=['resist-pale cloth'], accent1=['one unbound madder spill'], accent2=['knot-shadow navy'], shadow='dye-shadow-navy', forbidden=['neon','muddy colors','photo color'], light_type='стежок держит краску: где нить стянула ткань — бело, свет читает рельеф стежка как тактильную карту', family='exp_color_wave_12', born='2026-11-20, T5-27 «PREY» — волна 12 «раскраска выживания» (заказ автора)', trial='trial до вердикта T5-27'),
     dict(id='P253_KINTSUGI_GOLD_MEND', name='Kintsugi Gold Mend', dominant=['lacquer-black','mend-gold seam'], secondary=['old-bone porcelain'], accent1=['one fresh-crack copper'], accent2=['resin amber'], shadow='resin-shadow-brown', forbidden=['neon','muddy colors','photo color'], light_type='золото в трещине: свет идёт по шву ремонта, трещина — самый яркий путь кадра', family='exp_color_wave_12', born='2026-11-20, T5-27 «PREY» — волна 12 «раскраска выживания» (заказ автора)', trial='trial до вердикта T5-27'),
     dict(id='P254_SHOUSUGIBAN_CHAR', name='Shou-Sugi-Ban Char', dominant=['char-black satin','cedar-ember line'], secondary=['soot-grey feather'], accent1=['one unburned cedar-gold plank'], accent2=['smoke-ghost silver'], shadow='smoke-shadow', forbidden=['neon','muddy colors','photo color'], light_type='обжиг-хранитель: уголь ест блики, живая доска — единственный тёплый акцент', family='exp_color_wave_12', born='2026-11-20, T5-27 «PREY» — волна 12 «раскраска выживания» (заказ автора)', trial='trial до вердикта T5-27'),
     dict(id='P255_UKIYO_WOODBLOCK', name='Ukiyo-e Woodblock', dominant=['prussian-wave blue','safflower rose'], secondary=['paper-cream','bokashi sky gradient'], accent1=['one vermilion seal'], accent2=['mokuhanga woodgrain'], shadow='woodgrain-shadow', forbidden=['neon','muddy colors','photo color'], light_type='плоские плашки и градиент бокаси: свет — слой туши, не луч; зерно доски дышит под краской', family='exp_color_wave_12', born='2026-11-20, T5-27 «PREY» — волна 12 «раскраска выживания» (заказ автора)', trial='trial до вердикта T5-27'),
     dict(id='P256_FRESCO_LIME', name='Fresco Lime', dominant=['lime-bianco wet','mineral terre-verte'], secondary=['wet-plaster grey'], accent1=['one true-fresco red earth'], accent2=['sand-pink intonaco'], shadow='matte mineral shadow', forbidden=['neon','muddy colors','photo color'], light_type='пигмент утонул в сырой извести: матовый свет изнутри стены, без лака и блика', family='exp_color_wave_12', born='2026-11-20, T5-27 «PREY» — волна 12 «раскраска выживания» (заказ автора)', trial='trial до вердикта T5-27'),
     dict(id='P257_CEL_PAINT_FLAT', name='Cel Animation Paint', dominant=['cel-vinyl two-tone flat'], secondary=['register-line clean'], accent1=['one highlight-bloom white'], accent2=['shadow-edge hard'], shadow='single-tone shadow', forbidden=['neon','muddy colors','photo color'], light_type='аниме-целл: плоские заливки, жёсткая кромка тени, один блик-цветом; никаких градиентов', family='exp_color_wave_12', born='2026-11-20, T5-27 «PREY» — волна 12 «раскраска выживания» (заказ автора)', trial='trial до вердикта T5-27'),
     dict(id='P258_DECALCOMANIA_PRESS', name='Decalcomania Press', dominant=['dendrite-ink black','squid-vein violet'], secondary=['press-pale ground'], accent1=['one coral bloom'], accent2=['fingerprint whorl'], shadow='fold-shadow', forbidden=['neon','muddy colors','photo color'], light_type='краска сжата между двумя поверхностями: свет течёт по жилам-дендритам, узор рождён давлением', family='exp_color_wave_12', born='2026-11-20, T5-27 «PREY» — волна 12 «раскраска выживания» (заказ автора)', trial='trial до вердикта T5-27'),
     dict(id='P259_SILVERPOINT_TARNISH', name='Silverpoint Tarnish', dominant=['toned-ground grey','silver-line pale'], secondary=['warm-tarnish bloom'], accent1=['one red-chalk note'], accent2=['ground-tooth speckle'], shadow='ground-tooth shadow', forbidden=['neon','muddy colors','photo color'], light_type='след серебряного штифта стареет в тёплый тон: свет читает линию ретро-окислом, тонированная бумага ест полутон', family='exp_color_wave_12', born='2026-11-20, T5-27 «PREY» — волна 12 «раскраска выживания» (заказ автора)', trial='trial до вердикта T5-27'),
     dict(id='P260_AMATE_BARK_FIBER', name='Amate Bark Fiber', dominant=['bark-fiber kraft','fig-bark speckle'], secondary=['cochineal earth'], accent1=['one wild-cotton white'], accent2=['fig-leaf green press'], shadow='fiber-shadow', forbidden=['neon','muddy colors','photo color'], light_type='волокно коры держит пигмент как ловчая сеть: свет рассеян в фибре, земляные краски сидят глубоко', family='exp_color_wave_12', born='2026-11-20, T5-27 «PREY» — волна 12 «раскраска выживания» (заказ автора)', trial='trial до вердикта T5-27'),
    ]
    havep = {p['id'] for p in pal['palettes']}
    for p in W12:
        assert p['id'] not in havep, p['id']
        pal['palettes'].append(p)
    pal['version'] = '1.14.0'
    ecw = pal.get('exp_color_waves')
    entry = dict(wave='exp_color_wave_12', name='раскраска выживания', born='2026-11-20, T5-27 «PREY»: заказ автора «новенькие палитры и способы раскраски»', methods=['shibori stitch-resist indigo','kintsugi gold-mend','shou-sugi-ban char','ukiyo-e woodblock','fresco lime','cel animation paint','decalcomania press','silverpoint tarnish','amate bark fiber'], note='девять РАЗНЫХ механик; семьи ни разу не выходили (волны 1–11 не пересечены); методы читают тему: сопротивление/починка/сохранение/плоскость/минерал/жёсткая кромка/отпечаток/линия/волокно')
    if isinstance(ecw, list): ecw.append(entry)
    elif isinstance(ecw, dict): ecw['exp_color_wave_12'] = entry
    else: pal['exp_color_waves'] = [entry]
    save('specs/palettes.json', pal)
    print('palettes.json → 1.14.0, +9 (волна 12)')
else:
    print('palettes.json уже 1.14.0')

ds = load('specs/delivery-stats.json')
if ds['version'] != '0.13.0':
    W13 = [
     ('shelf-cage-lean','навал в шкаф-клетку: ладони на полки, объект у груди — комната идёт к ней, не она к комнате (P01)'),
     ('afterglow-window-fog','утро-после: лоб к стеклу, пар дыхания, мокрые бретели камисоля съехали честно (P02)'),
     ('coolant-bath-rise','подъём из ванны-охлаждения: полотенце к груди, пар = испарение хладагента (P03)'),
     ('cornered-wall-turn','загнанная разворачивается: спина к стене, подбородок вниз, глаза вверх — стоп-сигнал взгляда (P04)'),
     ('mid-molt-freeze','замирание в полулиньке: подол остановлен под скрещенными предплечьями (P05)'),
     ('fleece-shake-arc','встряска руна: мокрые волосы дугой, полотенце поймано под локоть (P06)'),
     ('preserve-glass-watch','заповедник-витрина: ладонь на стекле, сорочка к панели, силуэт читается наизнанку (P07)'),
     ('cover-grip-closeup','крупно: хват-прикрытие, ткань собирается между пальцами (P08)'),
     ('water-column-watch','водопойная вахта: столб воды в ладонях-лупе, мокрая смена сквозь воду (P09)'),
     ('hoard-mouth-swallow','копилка-хищник: керамика на линии груди, первая блестяшка уходит в горло (P10)'),
    ]
    havech = {c['id'] for c in ds['channels']}
    for cid, note in W13:
        assert cid not in havech, cid
        ds['channels'].append(dict(id=cid, name=note, status='candidate', tier='R+', attempts=1, delivered=0, evidence=['T5-27 (слоты — см. channel field; счётчик честный, кандидат легален до вердикта; волна 13 — режим WARN, эскалация по KPI после двух вердиктов)']))
    ds['version'] = '0.13.0'
    save('specs/delivery-stats.json', ds)
    print('delivery-stats.json → 0.13.0, +10 каналов (волна 13)')
else:
    print('delivery-stats.json уже 0.13.0')

# контроль
cam = load('specs/camera.json')
poses = load('specs/poses.json')
assert cam['version'] == '1.17.0' and poses['version'] == '1.19.0'
ids = [c['id'] for c in cam['y_cards']['cards']]
for y in ['Y522','Y530','Y443','Y258']:
    assert y in ids, y
print('КОНТРОЛЬ: camera 1.17.0 (' + str(len(ids)) + ' карт), poses 1.19.0 (' + str(len(poses['poses'])) + ' поз)')
print('OK')
