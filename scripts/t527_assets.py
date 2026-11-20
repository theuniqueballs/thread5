#!/usr/bin/env python3
# T5-27 «PREY» — создание активов: позы PL578–586, карты Y522–Y530 (В27-физика с рождения),
# палитры волны 12 (P252–P260), каналы волны 13, В27-пересборка карт жребия T5-27.
import json, sys, re

ROOT = '/home/z/my-project/thread5'
def load(p): return json.load(open(f'{ROOT}/{p}', encoding='utf-8'))
def save(p, d): json.dump(d, open(f'{ROOT}/{p}', 'w', encoding='utf-8'), ensure_ascii=False, indent=1); open(f'{ROOT}/{p}','a',encoding='utf-8').write('\n')

# ─── 1. POSES: PL578–PL586 (семья prey_survival, обёртки Y522–Y530) ───
poses = load('specs/poses.json')
if poses['version'] == '1.18.0':
  NEW_POSES = [
 dict(id='PL578', name='Armor-Curl Unfurl', sd='unrolling from the armor-curl against the burrow wall, one knee still folded to the chest, both palms pressing the scale-wrap\'s loose front flat over the ribs', category='OC_T5-27', risk='MID', family='prey_survival', preferred_cams=['CAM02'], use='V', source='first-use T5-27 PREY (EXP-семья prey_survival, 9 карт)', use_note='обёртка Y522: панголин-кандидат — броня-нора раскрывается', corridor='A', rating_trust='MID', combo=True, card='Y522'),
 dict(id='PL579', name='Dust-Hollow Sprawl', sd='sprawled flat in the dust hollow, chin on crossed wrists, both heels kicking a slow dust-bloom, one palm pinning the mended vest flat to the ribs', category='OC_T5-27', risk='LOW', family='prey_survival', preferred_cams=['CAM06_side'], use='N', source='first-use T5-27 PREY (EXP-семья prey_survival, 9 карт)', use_note='обёртка Y523: шиншилла-кандидат — пыльная ванна', corridor='A', rating_trust='LOW', combo=True, card='Y523'),
 dict(id='PL580', name='Half-Shed Coat Stretch', sd='mid-stretch in the half-shed coat, one arm out of the winter sleeve, the coat\'s weight hanging off the crooked elbow, the summer-brown side bared to the shoulder', category='OC_T5-27', risk='MID', family='prey_survival', preferred_cams=['CAM02'], use='V', source='first-use T5-27 PREY (EXP-семья prey_survival, 9 карт)', use_note='обёртка Y524: горностай-кандидат — полулинька', corridor='A', rating_trust='MID', combo=True, card='Y524'),
 dict(id='PL581', name='Hoard-Rim Offer', sd='crouched on the hoard-rim, presenting one shining find in both palms at the lens, the wing-panels flared for balance, tail-feathers counting the wind', category='OC_T5-27', risk='LOW', family='prey_survival', preferred_cams=['CAM02'], use='N', source='first-use T5-27 PREY (EXP-семья prey_survival, 9 карт)', use_note='обёртка Y525: сорока-кандидат — блестяшка в обеих ладонях', corridor='A', rating_trust='LOW', combo=True, card='Y525'),
 dict(id='PL582', name='Low-Track Listen', sd='crouched low, one ear turned back to the wind, both forearms flat on the ground, chin on the wrists, haunches high, the tail-tip\'s one dark segment flagging', category='OC_T5-27', risk='MID', family='prey_survival', preferred_cams=['CAM03_low'], use='V', source='first-use T5-27 PREY (EXP-семья prey_survival, 9 карт)', use_note='обёртка Y526: рысь-кандидат — низкое слушание', corridor='A', rating_trust='MID', combo=True, card='Y526'),
 dict(id='PL583', name='Prayer-Fold Still', sd='stone-still in the prayer fold, both raptorial forelegs bent at the chest like a closed book, the head\'s slow tilt the only motion, one hind-leg\'s spike notched on a stem', category='OC_T5-27', risk='MID', family='prey_survival', preferred_cams=['CAM02'], use='V', source='first-use T5-27 PREY (EXP-семья prey_survival, 9 карт)', use_note='обёртка Y527: богомол-кандидат — неподвижность как оружие', corridor='A', rating_trust='MID', combo=True, card='Y527'),
 dict(id='PL584', name='Regrown-Limb Inspect', sd='sitting in the shallow with the regrown arm held up to the light, the new limb counting its own fingers, gill-frills fanning the water\'s calm, the other palm flat on the submerged sill', category='OC_T5-27', risk='LOW', family='prey_survival', preferred_cams=['CAM02'], use='N', source='first-use T5-27 PREY (EXP-семья prey_survival, 9 карт)', use_note='обёртка Y528: аксолотль-кандидат — новая рука считает пальцы', corridor='A', rating_trust='LOW', combo=True, card='Y528'),
 dict(id='PL585', name='Beckon-Coin Balance', sd='balanced on one heel on the sill\'s edge, the raised paw held in the beckon curl, the coin\'s warmth in the other palm at the chest, the tail counting the balance', category='OC_T5-27', risk='LOW', family='prey_survival', preferred_cams=['CAM02'], use='N', source='first-use T5-27 PREY (EXP-семья prey_survival, 9 карт)', use_note='обёртка Y529: манэки-нэко-кандидат — монета и приглашение', corridor='A', rating_trust='LOW', combo=True, card='Y529'),
 dict(id='PL586', name='Note-Before-Note', sd='standing at the herd\'s edge with both hands folded at the sternum, the breath drawn to the top of the lungs, the mouth one heartbeat from the note, the veil\'s hem lifting with the intake', category='OC_T5-27', risk='MID', family='prey_survival', preferred_cams=['CAM02'], use='V', source='first-use T5-27 PREY (EXP-семья prey_survival, 9 карт)', use_note='обёртка Y530: банши-кандидат — вдох перед нотой', corridor='A', rating_trust='MID', combo=True, card='Y530'),
]
have = {p['id'] for p in poses['poses']}
for p in NEW_POSES:
    assert p['id'] not in have, p['id']
    poses['poses'].append(p)
poses['version'] = '1.19.0'
poses['born'] += '\n2026-11-20 — T5-27 «PREY»: +PL578–PL586 (EXP-семья prey_survival, обёртки Y522–Y530, заказ «новенькие Y которых ещё не создавали»)'
save('specs/poses.json', poses)
print('poses.json → 1.19.0, +', len(NEW_POSES))

# ─── 2. CAMERA: Y522–Y530 (новые, В27-физика с рождения) + В27-пересборка жребия ───
cam = load('specs/camera.json')
cards = cam['y_cards']['cards']
byid = {c['id']: c for c in cards}

def mkcard(cid, pl, pattern, cover, profiling, note):
    exposure = {'class': 'COVER', 'cover_object': cover, 'read': f'объект-прикрытие в паттерне (коридор A): {cover}'}
    return {'id': cid, 'pattern': pattern, 'corridor': 'A',
        'trust': f'DERIVED, T5-27 (2026-11-20): карта-обёртка над {pl}; В27-физика в sd с рождения (вес/тяга/зацеп/финал); trust позы MID — тир решает вердикт',
        'verdict': f'T5-27 сборка 2026-11-20 (заказ автора «новенькие Y которых ещё не создавали»): новая карта, sd — копипаст-юнит; {note}',
        'built_from': pl,
        'components': {'exposure': exposure,
            'pose': pattern.split(' + ')[0], 'pov': 'камера позы', 'camera': pattern.split(' + ')[-1], 'profiling': profiling}}

NEW_CARDS = [
 mkcard('Y522','PL578','unrolling from the armor-curl against the burrow wall, one knee still folded to the chest, both palms pressing the scale-wrap\'s loose front flat over the ribs, its weight dragging one shoulder lower + full body three-quarter','the scale-wrap\'s loose front flat over the ribs','prey_survival · VERTICAL · use: V','панголин: броня-нора'),
 mkcard('Y523','PL579','sprawled flat in the dust hollow, chin on crossed wrists, both heels kicking a slow dust-bloom, one palm pinning the mended vest flat to the ribs, the kicks\' rhythm riding the vest\'s hem + full body from the side','one palm pinning the mended vest flat to the ribs','prey_survival · HORIZONTAL · use: N','шиншилла: пыльная ванна'),
 mkcard('Y524','PL580','mid-stretch in the half-shed coat, one arm out of the winter sleeve, the coat\'s weight hanging off the crooked elbow and its front panel swung across the chest line, the summer-brown side bared to the shoulder + upper body three-quarter','the coat\'s front panel swung across the chest line','prey_survival · DIAGONAL · use: V','горностай: полулинька'),
 mkcard('Y525','PL581','crouched on the hoard-rim, presenting one shining find in both palms at the lens, the wing-panels flared for balance, tail-feathers counting the wind\'s one direction + upper body three-quarter','one shining find in both palms at the lens','prey_survival · FRONTAL · use: N','сорока: блестяшка в дар'),
 mkcard('Y526','PL582','crouched low with one ear turned back to the wind, both forearms flat on the ground and the knit wrap\'s fold crossing the chest line, chin on the wrists, haunches high, the tail-tip\'s one dark segment flagging + full body profile','the knit wrap\'s fold crossing the chest line','prey_survival · PROFILE · use: V','рысь: низкое слушание'),
 mkcard('Y527','PL583','stone-still in the prayer fold, both raptorial forelegs bent at the chest like a closed book, the head\'s slow tilt the only motion, one hind-leg\'s spike notched on a stem, the stillness holding the whole frame + upper body frontal','both raptorial forelegs bent at the chest like a closed book','prey_survival · FRONTAL · use: V','богомол: неподвижность как заявка'),
 mkcard('Y528','PL584','sitting in the shallow with the regrown arm held up to the light, the new limb counting its own fingers, the waterline crossing the chest line while the other palm stays flat on the submerged sill + upper body three-quarter','the waterline crossing the chest line','prey_survival · THREE-QUARTER · use: N','аксолотль: новая рука'),
 mkcard('Y529','PL585','balanced on one heel on the sill\'s edge, the raised paw held in the beckon curl, the coin\'s warmth in the other palm held flat at the chest, the tail counting the balance + full body three-quarter','the coin\'s warmth in the other palm held flat at the chest','prey_survival · THREE-QUARTER · use: N','манэки-нэко: монета и приглашение'),
 mkcard('Y530','PL586','standing at the herd\'s edge with both hands folded at the sternum, the breath drawn to the top of the lungs, the mouth one heartbeat from the note, the veil\'s hem lifting with the intake + upper body frontal','both hands folded at the sternum','prey_survival · FRONTAL · use: V','банши: вдох перед нотой'),
]
havec = {c['id'] for c in cards}
for c in NEW_CARDS:
    assert c['id'] not in havec, c['id']
    cards.append(c)

# В27-пересборка (акт 3, первая волна): карты жребия T5-27 получают физику в паттерне, клеймо перерождается (LAWS §17.4)
REBUILD = {
 'Y443': ('braced into the bookcase behind the viewer, both palms flat on the shelf-boards either side of the frame, the spine\'s weight leaning its curve into the shelf\'s edge, one knee notched on the lower rail + CAM02',
          'both palms flat on the shelf-boards either side of the frame'),
 'Y351': ('forehead pressed to cool window glass above the basin, both palms flat on the pane, breath fog starting, the wet camisole straps\' weight slipping off both shoulders honest + upper body three-quarter',
          'the wet camisole straps\' weight slipping off both shoulders honest'),
 'Y486': ('rising from a wide dark bath, both palms pressing a folded towel flat against the chest, the towel\'s hem caught between forearms, steam leaning with the rise\'s slow pull + upper body three-quarter',
          'both palms pressing a folded towel flat against the chest'),
 'Y333': ('standing at the tub, both palms cupped around a vertical column of water lifted from the bath, leaning in to look through it, the column\'s weight bowing both wrists inward, soaked shift clinging to the chest line + eye level',
          'the vertical column of water lifted from the bath'),
 'Y1': ('shirt hem stopped mid-lift under crossed forearms, the lifted hem\'s weight hanging off both elbows, the under-curve of the chest reading where the cotton\'s gone transparent with the stretch + upper body + slight low angle',
          'the lifted hem\'s weight hanging off both elbows'),
 'Y427': ('tilting the piggy-bank over her open palm while its mouth swallows the nearest shine first, the bank\'s ceramic weight balanced on the sternum\'s line, one coin already warm in the palm + CAM01',
          'the bank\'s ceramic weight balanced on the sternum\'s line'),
 'Y265': ('behind glass, palm on the pane, eyes finding the viewer outside, the nightgown\'s front pressed flat to the glass by the palm\'s spread, the chest line reading through the sheer layer against the pane + upper body three-quarter',
          'the nightgown\'s front pressed flat to the glass'),
 'Y8': ('close on the hands\' cover grip, the fabric gathering between the fingers over the sternum, the knuckles\' tension telling how little the cover weighs + eye level',
          'the fabric gathering between the fingers over the sternum'),
 'Y45': ('spine flat against wall or glass, both palms pressed beside the hips, chin tilted down and eyes lifted under the lashes, the wall taking the shoulders\' full weight + CAM05_over_shoulder',
          'the wall taking the shoulders\' full weight'),
 'Y258': ('mid-flip of wet hair after the towel, face briefly hidden by the hair arc, arms up, the towel-wrap\'s tuck caught under one elbow while both wrists shake the water out + upper body three-quarter',
          'the towel-wrap\'s tuck caught under one elbow'),
}
for cid, (newpat, cover) in REBUILD.items():
    c = byid[cid]
    old = c['pattern']
    c['pattern'] = newpat
    c['trust'] = c['trust'].replace('В27 ПУСТО в sd — до пересборки печью карта не выходит в R+',
        'В27-ПЕРЕСБОРКА акт 3, волна 1 (T5-27): физика в sd залита, карта легальна под R+')
    if 'В27 ПУСТО' not in old and 'В27-физика' not in c['trust']:
        c['trust'] += '; В27-ПЕРЕСБОРКА акт 3, волна 1 (T5-27)'
    comp = c['components']
    comp['exposure']['cover_object'] = cover
    comp['exposure']['read'] = f'объект-прикрытие (коридор A, пересборка T5-27): {cover}'
    comp['pose'] = newpat.split(' + ')[0]
cam['version'] = '1.17.0'
cam.setdefault('changelog', [])
cam['changelog'].append('1.17.0 (2026-11-20, T5-27 «PREY»): +Y522–Y530 — девять НОВЫХ карт по заказу «новенькие Y которых ещё не создавали» (обёртки PL578–PL586, В27-физика с рождения: вес/тяга/зацеп/финал); В27-пересборка акта 3, волна 1 — 10 карт жребия T5-27 (Y443/Y351/Y486/Y333/Y1/Y427/Y265/Y8/Y45/Y258) получили физику в паттерне, клеймо переродилось само (LAWS §17.4)')
save('specs/camera.json', cam)
print('camera.json → 1.17.0, +9 карт, В27-пересборка ×10')

# ─── 3. PALETTES: волна 12 «раскраска выживания» (P252–P260) ───
pal = load('specs/palettes.json')
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
pal.setdefault('exp_color_waves', {})
pal['exp_color_waves']['exp_color_wave_12'] = dict(name='раскраска выживания', born='2026-11-20, T5-27 «PREY»: заказ автора «новенькие палитры и способы раскраски»', methods=['shibori stitch-resist indigo','kintsugi gold-mend','shou-sugi-ban char','ukiyo-e woodblock','fresco lime','cel animation paint','decalcomania press','silverpoint tarnish','amate bark fiber'], note='девять РАЗНЫХ механик; семьи ни разу не выходили (волны 1–11 не пересечены); методы читают тему: сопротивление/починка/сохранение/плоскость/минерал/жёсткая кромка/отпечаток/линия/волокно')
save('specs/palettes.json', pal)
print('palettes.json → 1.14.0, +9 (волна 12)')

# ─── 4. CHANNELS: волна 13 (10 кандидатов ☠) ───
ds = load('specs/delivery-stats.json')
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
print('OK — все активы T5-27 созданы')
