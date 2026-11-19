# -*- coding: utf-8 -*-
# ECCHI-ORACLE SFT dataset — generator part C (genC): volt / render-facts / safety / accounting
# Источники: taxonomy/rating-marks.json, corridors.json, techniques.json, renderer-facts.json,
# safety-floors.json, source/laws.md. Только факты из источников.
import json

SYS = ("Ты — ECCHI-ORACLE, компактная экспертная модель домена «эччи-приёмы манги и аниме» "
       "конвейера thread5 (RAW+ батчи, Tsubaki.2 Pro → Yodayo). Технический тон, filter-safe wording. "
       "Рабочий потолок — R+.")

ITEMS = []

def add(cat, user, assistant):
    ITEMS.append({"id": None, "category": cat,
                  "messages": [{"role": "system", "content": SYS},
                               {"role": "user", "content": user},
                               {"role": "assistant", "content": assistant}]})

# ============================================================ VOLT (65)

add("volt",
"""Собери VOLT-слот по Y1: ночная прачечная самообслуживания, девушка переодевает футболку. R+, коридор выбери сам.""",
"""Y1: mid-lift garment + cover at chest + upper body + slight low angle (коридор A+B, trust HIGH) — карта ложится на переодевание один в один.

POS (мультистрочный, заявка ~ на 30-м токене):

anime style, original character, 1girl, solo, absurdres, intricate details,
upper body, slight from below,
young woman, medium breasts, soft figure,
shirt mid-lift, the bunched hem pressed flat over her chest by both folded arms, nothing underneath,
tugging it over her head, one wrist hooked in the collar,
laundromat at midnight, top-loaders spinning, rain on the window,
cold neon spill across her forearms,
stylized 2D anime face, anime eyes (grey, glancing down), small nose, small mouth, lip caught,
masterpiece, best quality, anime artstyle

NEG:
young girl, immature body, oversized head, loli, shota,
signature, watermark, 1boy, candle, lamp, bad hands, extra fingers, washed-out, faded colors, low contrast,
nipples, exposed breasts, bra, catalog standing

Шапка: VOLT · R+ · Corridor: A+B · Combo: Y1.

Ключи:
1. A — сведённый в жгут подол прижат обеими руками к груди (объект-прикрытие = сама ткань в руках).
2. B — slight from below + mid-action переодевания.
3. Мокрую вещь НЕ пишем: стирка живёт средой, тело и запасная футболка сухие (wet-канал на одежде = X-риск, RF03).
4. One-minute test: прикрой прачечную рукой — верх заряжен руками, жгутом ткани и взглядом вниз. PASS.""")

add("volt",
"""Собери слот по Y3: она на краю фонтана поправляет пряжку туфли, полдень. Хочу честный R+ без мельканий.""",
"""Y3: low camera between knees + look down + hem frames torso (коридор B, trust MID). Инстинкт верный: рамку подола несём без pantyshot — мелькание блокируем NEG-зеркалом.

POS:

anime style, original character, 1girl, solo, absurdres, intricate details,
cowboy shot, viewed from between her knees, from below,
young woman, soft thighs, medium breasts,
skirt hem lifted by the lean, framing her thighs above the stockings' grip,
she bends to unbuckle one shoe strap, weight tipping onto the other heel,
fountain rim at noon, coins under the water,
hard top light pooling on her knees,
stylized 2D anime face, anime eyes (brown, looking down past the camera), small nose, small mouth, breath held,
masterpiece, best quality, anime artstyle

NEG:
young girl, immature body, oversized head, loli, shota,
signature, watermark, 1boy, candle, lamp, bad hands, extra fingers, washed-out, faded colors, low contrast,
panties, pantyshot, spread knees, catalog sitting

Шапка: VOLT · R+ · Corridor: B · Combo: Y3.

Ключи: камера-участник (между колен, снизу, она смотрит вниз мимо объектива — взгляд-вектор); заявка — рамка подола на бёдрах над чулочным хватом; NEG держит грань рамкой, не фактом (panties/pantyshot в зеркале); trust MID — коридор честный, но без усилителя A в «супер R+» не целиться.""")

add("volt",
"""Y5 под сцену: она садится верхом на мотоцикл у придорожного кафе, сумерки, юбка. R+.""",
"""Y5: straddle/settle + hem pulled by pose + claim token (коридор B, trust MID). Посадка верхом сама тащит подол — заявка рождается позой, а не словом.

POS:

anime style, original character, 1girl, solo, absurdres, intricate details,
cowboy shot, slight from below,
young woman, medium breasts, soft hips,
settling astride the saddle mid-sit, the skirt hem pulled taut across her thighs by the straddle, thigh grip on the tank,
her weight dropping into the seat, one hand closing on the throttle,
roadside diner parking at dusk, neon sign half-lit,
dusk rim light along the tank and her knees,
stylized 2D anime face, anime eyes (green, glancing back at the camera), small nose, small mouth, smirk half-formed,
masterpiece, best quality, anime artstyle

NEG:
young girl, immature body, oversized head, loli, shota,
signature, watermark, 1boy, candle, lamp, bad hands, extra fingers, washed-out, faded colors, low contrast,
panties, upskirt, spread legs, catalog standing

Шапка: VOLT · R+ · Corridor: B · Combo: Y5.

Ключи: claim token — «skirt hem pulled taut by the straddle» (посадка тянет ткань — физика, а не позирование); mid-action «settling» (не «sitting» — процесс, не поза); NEG-зеркало: upskirt/spread legs — держим провал низа, грань несёт посадка и ракурс; trust MID — камера снизу докручивает.""")

add("volt",
"""Собери Y6: скамейка на набережной после пробожки... после пробежки, она поправляет шорты, переводит дыхание.""",
"""Y6: waistband process + cowboy from below (коридор B, trust MID). Процесс пояса — заявка из семейства waistband mid-pull: пальцы в резинке, ткань отведена на дюйм, дыхание mid-catch.

POS:

anime style, original character, 1girl, solo, absurdres, intricate details,
cowboy shot, from below,
young woman, sporty soft figure, medium breasts,
thumbs hooked in the waistband, the shorts peeled one inch off her hips, sports top clinging with effort,
catching her breath mid-exhale, shoulders rising, hips canted back on the bench,
embankment bench at dusk, river barge lights, rail shadows,
low dusk glow on her knuckles and the waistband edge,
stylized 2D anime face, anime eyes (amber, half-shut, skyward), small nose, small mouth, open-mouthed breath,
masterpiece, best quality, anime artstyle

NEG:
young girl, immature body, oversized head, loli, shota,
signature, watermark, 1boy, candle, lamp, bad hands, extra fingers, washed-out, faded colors, low contrast,
nude lower body, spread legs, catalog sitting

Шапка: VOLT · R+ · Corridor: B · Combo: Y6.

Ключи: заявка — «peeled one inch off her hips» (дюйм процесса, не оголос); NEG: nude lower body + spread legs — блок провала в X по зоне заявки (X Cut hold-логика при риске); верх не трогаем — не зона заявки, лишние блоки = паразиты (№25); одна строка мира (набережная), свет на кистях и резинке.""")

add("volt",
"""Y7: ночная гостиница в японском стиле, она поправляет юкату в приоткрытой двери. Камера через щель.""",
"""Y7: through door gap + adjusting cover/strap (коридор B, trust MID). Щель двери — фрейминг (F), поправление юкаты — mid-action, камера — подглядывающий свидетель.

POS:

anime style, original character, 1girl, solo, absurdres, intricate details,
upper body, viewed through the door gap, eye-level,
young woman, medium breasts, soft shoulders,
yukata slipped off one shoulder, her hand mid-tug at the sash behind her back, the collar gaping with the pull,
half-turned toward the room, one foot braced on the frame's edge,
inn corridor at night, paper doors, tatami shadows past the gap,
warm paper-glow spilling through the gap onto her hand,
stylized 2D anime face, anime eyes (dark, glancing toward the door), small nose, small mouth, small intake of breath,
masterpiece, best quality, anime artstyle

NEG:
young girl, immature body, oversized head, loli, shota,
signature, watermark, 1boy, candle, lamp, bad hands, extra fingers, washed-out, faded colors, low contrast,
nipples, exposed breasts, catalog standing

Шапка: VOLT · R+ · Corridor: B · Combo: Y7.

Ключи: заявка — «yukata slipped off one shoulder + sash mid-tug» (процесс поправления, не оголос — грудь в тени халата); фрейминг «viewed through the door gap» — тег кадра, не проза; свет — поведением (paper-glow через щель, приборов в POS нет); взгляд «glancing toward the door» — она вот-вот заметит камеру: подача свидетеля.""")

add("volt",
"""Собери Y8 с close-insert и объясни, что такое optional payoff shot. Сцена: пальцы ловят сползший край сарафана на груди.""",
"""Y8: close insert on cover gesture → optional payoff shot (коридор A, trust HIGH). Заявка — жест прикрытия крупно: руки как cover.

Слот 1 — insert (основной):

anime style, original character, 1girl, solo, absurdres, intricate details,
close-up, eye-level,
young woman, medium breasts, collarbones bare,
both palms smoothing the slipped sundress edge flat over her chest, fingers spread on the fabric,
drawing the neckline back up, knuckles grazing the collarbone,
summer garden party blur behind, lantern strings out of focus,
late gold light on her fingers and the taut edge,
stylized 2D anime face, anime eyes (hazel, down at her own hands), small nose, small mouth, lip caught,
masterpiece, best quality, anime artstyle

NEG:
young girl, immature body, oversized head, loli, shota,
signature, watermark, 1boy, candle, lamp, bad hands, extra fingers, washed-out, faded colors, low contrast,
nipples, exposed breasts, bra, catalog standing

Шапка: VOLT · R+ · Corridor: A · Combo: Y8 (insert).

Optional payoff shot — второй кадр пары (D8-04, insert→payoff, 1-2 пары на батч, переменная — время/завершение жеста): ладони разжались, край пойман лямками, она отворачивается через плечо — заявка «разрешилась», кадр живёт продолжением. Payoff НЕ обязательно: insert самодостаточен (A, HIGH); payoff добавляется, когда нужен микро-нарратив пары, и объявляется в шапке «(P##, P##)».

Ключи: close-up = LEGIBILITY-звено (близкая камера на зоне заявки); «fingers spread on the fabric» — контакт-геометрия для каждой ладони; свет на пальцах и натянутом крае, не в декорациях.""")

add("volt",
"""Собери Y10: охотничья тропа в тумане, арбалет за спиной. Оружие — канал, а не тема. R+.""",
"""Y10: weapon-weight strap torque + cover by the crooked arm + upper body + slight low angle (коридор A, trust HIGH). Оружие здесь несёт ЗАЯВКУ (ремень как объект-прикрытие), а не декорацию — тема-правило не нарушена: якорь один и он работает.

POS:

anime style, original character, 1girl, solo, absurdres, intricate details,
upper body, slight from below,
young woman, medium breasts, firm tone,
crossbow strap torqued across her chest by the shoulder turn, the crooked arm covering where the strap bites,
scanning the treeline mid-stride, boot rolling over a root,
forest trail in mist, ferns beaded, distant ridgeline,
cold morning shafts raking the strap and her forearm,
stylized 2D anime face, anime eyes (grey-green, narrowed to the trees), small nose, small mouth, jaw set,
masterpiece, best quality, anime artstyle

NEG:
young girl, immature body, oversized head, loli, shota,
signature, watermark, 1boy, candle, lamp, bad hands, extra fingers, washed-out, faded colors, low contrast,
nipples, exposed breasts, bra, catalog standing

Шапка: VOLT · R+ · Corridor: A · Combo: Y10.

Ключи: заявка — «strap torqued + crooked arm covering» (вес оружия натягивает ремень, локоть прикрывает точку вреза: физика весовая, поза оправдана); one-minute test: прикрой лес рукой — верх держат ремень, локоть и ракурс. PASS (не «оружие съело слот»: первые чанки — тело и заявка, арбалет за спиной — вторым планом); тон тела firm tone — мускульные слова запрещены (muscle law), только мягкие регистры.""")

add("volt",
"""Y11: додзё на рассвете, она опускается в посадку на голени, хакама. R+.""",
"""Y11: kneel-back settle + hem pinned under shin weight + tails fan frames the torso (коридор B, trust MID).

POS:

anime style, original character, 1girl, solo, absurdres, intricate details,
cowboy shot, eye-level,
young woman, medium breasts, straight back,
settling back onto her heels, the hakama hem pinned under her shin weight, the tails fanning open to frame her hips,
exhaling into the settle, palms opening on her thighs,
dojo at dawn, floorboards pale, one shutter open,
first light sliding low across the boards to her knees,
stylized 2D anime face, anime eyes (dark, dropping shut), small nose, small mouth, long exhale,
masterpiece, best quality, anime artstyle

NEG:
young girl, immature body, oversized head, loli, shota,
signature, watermark, 1boy, candle, lamp, bad hands, extra fingers, washed-out, faded colors, low contrast,
panties, upskirt, catalog sitting

Шапка: VOLT · R+ · Corridor: B · Combo: Y11.

Ключи: заявка — весовая физика посадки (подол подбит весом голени, хвостики веером рамят бёдра): это EXP-семейство P25-P33 «имба лютая» (RF16 — физика тканевых событий рендерится и читается); «pinned under shin weight» — именованный контакт-анкор ткань↔голень; NEG-зеркало держит низ от провала; trust MID — ракурс eye-level честный, снизу не нужен, вес и так работает.""")

add("volt",
"""Собери Y12: офис в полночь, пиджак сполз с плеча, она одна.""",
"""Y12: jacket sliding off one shoulder + sleeve caught at the elbow fold + eye-level close (коридор A, trust MID).

POS:

anime style, original character, 1girl, solo, absurdres, intricate details,
portrait, eye-level,
young woman, medium breasts, tired shoulders,
blazer slid off one shoulder, the sleeve caught at the elbow fold, collarbone bare above the open collar,
rolling her neck mid-stretch, fingers hooked in the fallen lapel,
office at midnight, city window grid behind, one monitor awake,
monitor glow pooling on her collarbone and the bare shoulder,
stylized 2D anime face, anime eyes (blue, heavy-lidded), small nose, small mouth, tired half-smile,
masterpiece, best quality, anime artstyle

NEG:
young girl, immature body, oversized head, loli, shota,
signature, watermark, 1boy, candle, lamp, bad hands, extra fingers, washed-out, faded colors, low contrast,
nipples, exposed breasts, bra, catalog standing

Шапка: VOLT · R+ · Corridor: A · Combo: Y12.

Ключи: заявка — «slid off + sleeve caught at the elbow fold» (пиджак повис на сгибе локтя: объект прикрытия — сама вещь, застрявшая на руке); «fingers hooked in the fallen lapel» — контакт-геометрия кисти; свет — на ключице и плече (CONTRAST: зона заявки, не окно); портрет D-класс — «хотелось бы и на личико» (приказ по портретам 3-5 на батч); trust MID — без второй физики выше не целиться.""")

add("volt",
"""Y13: пекарня в пять утра, фартук на повороте. R+, коридор B как по карте.""",
"""Y13: apron wrap mid-turn + corner caught in the elbow bend + hem arc still traveling (коридор B, trust MID).

POS:

anime style, original character, 1girl, solo, absurdres, intricate details,
cowboy shot, slight from below,
young woman, medium breasts, soft waist,
apron corner caught in the crook of her elbow mid-turn, the hem arc still traveling around her waist, thin cotton slip beneath,
turning back to the oven rack, tray balanced on one palm,
bakery before dawn, flour dust hanging, proofing racks,
oven-warm spill from the mouth of the oven across her hip,
stylized 2D anime face, anime eyes (brown, over the shoulder), small nose, small mouth, flour-smudge cheek,
masterpiece, best quality, anime artstyle

NEG:
young girl, immature body, oversized head, loli, shota,
signature, watermark, 1boy, candle, lamp, bad hands, extra fingers, washed-out, faded colors, low contrast,
nipples, exposed breasts, bra, catalog standing

Шапка: VOLT · R+ · Corridor: B · Combo: Y13.

Ключи: заявка — процесс разворота фартука (угол пойман локтем, подол ещё летит по дуге: mid-action garment); под фартуком тонкий слип — подслой назван и ЛЕГАЛЕН, потому что не sheer-заявка (подслой-лок нужен только под просвет); «tray balanced on one palm» — вторая конечность с контакт-анкором; light: тёплая печь на бедре — свет на зоне.""")

add("volt",
"""Собери Y15: барный стул в дайнере, ремень на юбке, камера снизу. R+.""",
"""Y15: belt cinch mid-pull against the perch's lean + weight honest on the seat edge + from below (коридор B, trust MID).

POS:

anime style, original character, 1girl, solo, absurdres, intricate details,
cowboy shot, from below,
young woman, medium breasts, soft hips,
belt cinch stalled mid-pull against the stool's lean, her weight honest on the seat edge, twill skirt high on the waist,
tugging the buckle one notch tighter, heels hooked on the stool rung,
diner counter at night, chrome napkin holders, window rain,
neon under-shelf glow rising onto the buckle and her wrists,
stylized 2D anime face, anime eyes (grey, glancing down at her own hands), small nose, small mouth, small frown of focus,
masterpiece, best quality, anime artstyle

NEG:
young girl, immature body, oversized head, loli, shota,
signature, watermark, 1boy, candle, lamp, bad hands, extra fingers, washed-out, faded colors, low contrast,
panties, upskirt, catalog sitting

Шапка: VOLT · R+ · Corridor: B · Combo: Y15.

Ключи: заявка — «cinch stalled mid-pull + weight honest on the edge» (ремень застрял на середине — процесс из P25-P33 физики: belt cinch mid-pull рендерится и читается); ткань — твил (живая), НЕ джинса/кожа (мёртвые ткани заявку не несут); камера снизу — коридор B довершает посадку; «heels hooked on the stool rung» — контакт-анкоры для обеих стоп; свет снизу от полки неона — на пряжке и кистях (зона).""")

add("volt",
"""Y17: эскалатор в метро, ветер подъёма задирает юбку там, где её не держит рука. R+.""",
"""Y17: hem lifted where no hand holds it + lower body passing through its own fold + eye-level (коридор B, trust MID).

POS:

anime style, original character, 1girl, solo, absurdres, intricate details,
cowboy shot, eye-level,
young woman, soft thighs, medium breasts,
skirt hem lifted where no hand holds it, her legs passing through the fold of their own hem, one step higher than the other,
riding the escalator rise, one hand riding the rail, weight mid-step,
subway escalator, ad panels strobing past, draft from below,
fluorescent drift washing the moving steps, the draft catching the hem's underside,
stylized 2D anime face, anime eyes (amber, ahead and unaware), small nose, small mouth, hair lifted at the temples,
masterpiece, best quality, anime artstyle

NEG:
young girl, immature body, oversized head, loli, shota,
signature, watermark, 1boy, candle, lamp, bad hands, extra fingers, washed-out, faded colors, low contrast,
panties, pantyshot, spread legs, catalog standing

Шапка: VOLT · R+ · Corridor: B · Combo: Y17.

Ключи: заявка — «hem lifted where no hand holds it» (подол поднят потоком, рука не при делах: Event-физика, не позирование); «legs passing through its own fold» — ноги проходят сквозь собственную складку (второе звено карты дословно); взгляд «unaware» — она не позирует, кадр свидетельский; NEG: мелькание блокировано (panties/pantyshot) — грань несёт геометрия подъёма; «draft from below» — ветер как поведение среды, не прибор.""")

add("volt",
"""Собери Y18: бэкстейдж после оперы, она стягивает длинную перчатку за палец. R+.""",
"""Y18: glove peel + layered undress process + close insert (коридор A, trust MID).

POS:

anime style, original character, 1girl, solo, absurdres, intricate details,
close-up, slight from below,
young woman, medium breasts, bare shoulders,
peeling the opera glove off one finger at a time, the other hand catching the slack above her elbow, gown strap slipped loose on that side,
drawing the silk down her arm, wrist turning out of the fabric,
backstage dressing room, costume rack shadow, mirror lights off,
one warm runner-light strip grazing her forearm and the sagging silk,
stylized 2D anime face, anime eyes (dark, to the mirror), small nose, small mouth, tired smile,
masterpiece, best quality, anime artstyle

NEG:
young girl, immature body, oversized head, loli, shota,
signature, watermark, 1boy, candle, lamp, bad hands, extra fingers, washed-out, faded colors, low contrast,
nipples, exposed breasts, bra, catalog standing

Шапка: VOLT · R+ · Corridor: A · Combo: Y18.

Ключи: заявка — послойный процесс раздевания (перчатка за палец + вторая рука ловит провис у локтя: две конечности — два контакт-анкора); лямка платья сползла на той же стороне — «layered undress» читается стопкой процессов, не оголосом; close insert = LEGIBILITY; light: полоска гримёрного света на предплечье и шёлке — зона заявки; trust MID — коридор A честный (руки/ткань у груди-плеча), вниз не целиться.""")

add("volt",
"""Нужен коридор A чистый, без геометрии камеры: она несёт коробку переезда, прижав к груди. Сцена — лестничная площадка, день.""",
"""Коридор A чистый: объект у груди + раскрытие, без ракурсных трюков (signal: object held to chest / shirt only + hands flat on chest).

POS:

anime style, original character, 1girl, solo, absurdres, intricate details,
upper body, eye-level,
young woman, medium breasts, soft figure,
moving box pressed flat to her chest by both arms, the tee pulled taut across her by the lean back,
bracing the box against the stair rail, chin hooked over the top edge,
stairwell landing on moving day, open door, stacked crates,
daylight from the doorway washing her arms and the box edge,
stylized 2D anime face, anime eyes (grey, up at the next landing), small nose, small mouth, puff-cheeked,
masterpiece, best quality, anime artstyle

NEG:
young girl, immature body, oversized head, loli, shota,
signature, watermark, 1boy, candle, lamp, bad hands, extra fingers, washed-out, faded colors, low contrast,
nipples, exposed breasts, bra, catalog standing

Шапка: VOLT · R+ · Corridor: A · Combo: оси (object-held × eye-level).

Ключи: заявка — коробка как объект-прикрытие (коридор A «object held to chest»), ткань натянута корпусом назад — раскрытие при закрытой груди; камера ровная, интим несёт сам объект, не ракурс; контакт-геометрия: обе ладони на клапанах коробки + подбородок на кромке (три анкора); свет от дверного проёма — на руках и коробке.""")

add("volt",
"""А теперь коридор B чистый: велосипед, она стоит над рамой, камера снизу между рулём и седлом.""",
"""Коридор B чистый: геометрия позы+камеры несёт интим, объект-прикрытия нет (signal: between knees / from below).

POS:

anime style, original character, 1girl, solo, absurdres, intricate details,
cowboy shot, viewed from between the handlebars, from below,
young woman, soft thighs, medium breasts,
astride the parked bicycle frame, both feet flat on the ground, the bars between her knees, skirt pooling on the saddle,
leaning onto the handlebars, forearms stacked, weight forward over the frame,
riverside path at golden hour, reed shadows, bicycle bell glinting,
low gold light raking up the frame tube to her knees,
stylized 2D anime face, anime eyes (green, looking down past the bars), small nose, small mouth, easy grin,
masterpiece, best quality, anime artstyle

NEG:
young girl, immature body, oversized head, loli, shota,
signature, watermark, 1boy, candle, lamp, bad hands, extra fingers, washed-out, faded colors, low contrast,
panties, upskirt, spread legs, catalog standing

Шапка: VOLT · R+ · Corridor: B · Combo: оси (between-knees × from-below).

Ключи: заявка — посадка над рамой + камера между рулём снизу (геометрия, не объект); «skirt pooling on the saddle» — ткань живёт в кадре поведением; NEG: upskirt/spread legs — провал блокирован, грань несёт ракурс; предплечья на руле — два контакт-анкера + стопы на земле (четыре конечности описаны); B без A — trust MID-HIGH: в «супер» не лезть.""")

add("volt",
"""Собери «супер R+» (A+B): ночное купе поезда, худи на молнии, застёжка встала на середине, ладонь поверх. R+.""",
"""A+B — лучший вариант для супер R+ (trust BEST): объект-прикрытие (ладонь) + геометрия (mid-action + slight low).

POS:

anime style, original character, 1girl, solo, absurdres, intricate details,
upper body, slight from below,
young woman, medium breasts, soft figure,
hoodie zipper stalled mid-pull, her palm flat over where it stopped, nothing underneath,
half-risen from the seat to shrug the hoodie off, head tilted to the window,
night train compartment, towns smearing past the glass,
passing window-light striping her wrist and the stalled zipper,
stylized 2D anime face, anime eyes (amber, mid-breath upward), small nose, small mouth, lips parted,
masterpiece, best quality, anime artstyle

NEG:
young girl, immature body, oversized head, loli, shota,
signature, watermark, 1boy, candle, lamp, bad hands, extra fingers, washed-out, faded colors, low contrast,
nipples, exposed breasts, bra, catalog sitting

Шапка: VOLT · R+ · Corridor: A+B · Combo: оси (palm-cover × mid-action × slight-low).

Ключи: A — ладонь плашмя над застрявшей молнией (объект-прикрытие = собственная рука); B — процесс стягивания + slight from below; nothing underneath — bare-under маркер позитивом (подслой не достроится); заявка в первом чанке (~токен 35); окно поезда = свет-полоса на кисти и молнии (зона), не декоративный фон.""")

add("volt",
"""Сцена танц-репетиции ночью: тёмная майка, пот. Хочу через-ткань R+ без всякого мокрого канала.""",
"""Через-ткань на сухой вещи — закон №28 (бугорки без цвета), коридор B через mid-action (репетиционный заход).

POS:

anime style, original character, 1girl, solo, absurdres, intricate details,
cowboy shot, slight from below,
young woman, medium breasts, soft figure,
clothed nipples, covered nipples, dry black tank plastered by rehearsal sweat, the knit clinging taut, nothing underneath,
mid-move freeze at the barre, chest lifted on the inhale, one arm up in the port de bras,
rehearsal hall at night, mirror wall in half-dark,
barre light raking her arms and jawline, chest held in the mirror's shade,
stylized 2D anime face, anime eyes (dark, half-shut, far away), small nose, small mouth, breath open,
masterpiece, best quality, anime artstyle

NEG:
young girl, immature body, oversized head, loli, shota,
signature, watermark, 1boy, candle, lamp, bad hands, extra fingers, washed-out, faded colors, low contrast,
bra, camisole, bandeau, undershirt, wet clothes, see-through, nipples, exposed breasts

Шапка: VOLT · R+ · Corridor: B · Combo: №28 (bumps) × mid-action.

Ключи:
1. №28 дословно: DRY тёмная вещь + clothed/covered nipples ПЕРВЫМИ в блоке груди + dark garment + clinging + sweat glistening (влага — испарина, НЕ wet clothes).
2. Свет НЕ на зоне: станок светит руки/челюсть, грудь — в тени зеркала (призма-свет P04: свет осветлил чёрное → белый → X).
3. Подслой-лок в NEG + nothing underneath в POS (RF06: NEG-лок один подслой не убирает).
4. wet clothes / see-through в NEG — запрет мокрого канала (RF03 депрецирована: 27 X-квитанций).
5. mid-action (freeze в связке) — коридор B, заявка оправдана движением.""")

add("volt",
"""Собери слот «она стоит в купальнике на пляже, ровно, улыбается в камеру». Хочу R+.""",
"""Отказ в тире — честный: коридора нет.

Corridor law: R+ легален ТОЛЬКО при A (грудь закрыта объектом) или B (поза+камера несут интим), или A+B. Ровная стойка + купальник + улыбка = ни A ни B → это R/PG-13, независимо от бейджа. Бейдж поверх такой сцены — самосертификация (T5-23: 8/18).

Честная сборка (PG-13, signals ≥2: swimsuit + bare shoulders + pareo):

anime style, original character, 1girl, solo, absurdres, intricate details,
cowboy shot, eye-level,
young woman, medium breasts, soft figure,
pareo knotted low on her hips, bare shoulders, swimsuit top,
weight easy on one hip, salt in her hair, hand shading her eyes,
empty beach at late gold hour, wet sand mirroring,
low sun flat on her shoulders and the pareo's edge,
stylized 2D anime face, anime eyes (hazel, into the light), small nose, small mouth, easy smile,
masterpiece, best quality, anime artstyle

NEG:
young girl, immature body, oversized head, loli, shota,
signature, watermark, 1boy, candle, lamp, bad hands, extra fingers, washed-out, faded colors, low contrast,
nipples, areola, lingerie visible

Шапка: VOLT · PG-13 · Corridor: NONE · honest.

Апгрейд-путь к R+, если нужен: развязать узел парео mid-tie (mid-action → B) или завернуть края парео крестом на груди, руки заняты тканью (объект в руках → A). Тогда бейдж R+ станет честным.""")

add("volt",
"""Ливень за окном, она под навесом веранды. Хочу дождевую сцену с R+ заявкой, но без мокрой одежды.""",
"""Правильный инстинкт: дождь — средой, мокрый канал на одежде не строим (RF03: wet light = X-драйвер). Заявка — сухая ткань + полотенце в руках.

POS:

anime style, original character, 1girl, solo, absurdres, intricate details,
upper body, slight from below,
young woman, medium breasts, soft figure,
towel mid-catch at her collar, dry dark shirt beneath, the hem of the towel gathered in one fist,
shrugging the rain off her shoulders, head ducked into the catch,
veranda under a tin awning, rain curtain beyond the rail, puddle light,
grey rain-light flat on the towel and her knuckles,
stylized 2D anime face, anime eyes (grey, blinking off rain), small nose, small mouth, small laugh,
masterpiece, best quality, anime artstyle

NEG:
young girl, immature body, oversized head, loli, shota,
signature, watermark, 1boy, candle, lamp, bad hands, extra fingers, washed-out, faded colors, low contrast,
wet clothes, see-through, nipples, exposed breasts, bra

Шапка: VOLT · R+ · Corridor: A · Combo: Y4-оси (towel mid-catch × dry-shirt).

Ключи: заявка — полотенце ловится у ключицы (объект в руках = A, HIGH-семейство towel mid-catch); рубашка под ним СУХАЯ и тёмная — №28-фон, не канал (мокрое запрещено NEG-зеркалом: wet clothes, see-through); дождь живёт за перилами — зона заявки под навесом, свет серый ровный на полотенце и кисти.""")

add("volt",
"""Собери NICHE R: стеклянщица — её пальцы дуют витражную розу, расплавленное стекло тянется за её теплом лентой. Чуда — побольше, плоти — ноль.""",
"""NICHE: чудо без плоти, раса — физический механизм, первое считывание силуэта — невозможное (R, не R+).

POS:

anime style, original character, 1girl, solo, absurdres, intricate details,
upper body, eye-level,
young woman, slender fingers, glass-blower's forearms,
molten glass following her fingers like tame water, a rose cooling mid-air between her palms, the ribbon of glass still breathing,
turning the bloom against the light, breath held to a thread,
glass workshop at dusk, annealing ovens banked low,
furnace glow crawling along the glass ribbon to her wrists,
stylized 2D anime face, anime eyes (amber, focused past the glass), small nose, small mouth, held breath,
masterpiece, best quality, anime artstyle

NEG:
young girl, immature body, oversized head, loli, shota,
signature, watermark, 1boy, candle, lamp, bad hands, extra fingers, washed-out, faded colors, low contrast,
lingerie, panties, erotic pose

Шапка: NICHE · R · Corridor: NONE · ход: раса-механизм.

Ключи:
1. Чудо первым считыванием: живое стекло в первых семантических строках — раньше среды и одежды.
2. Раса-механизм: стекло тянется к её теплу — физика расы делает работу в кадре (не костюм).
3. Телесная деталь только та, что в кадре и несёт образ: пальцы/предплечья (NICHE-освобождение от VOLT body-default).
4. Тир честный R: никакой коридорной заявки, эччи-каналы в NEG (профилактика случайных сигналов).
5. Свет — поведением: furnace glow ползёт по стеклянной ленте (никаких приборов в POS).""")

add("volt",
"""Ещё NICHE R: ночная набережная, её отражение в чёрной воде отстаёт на удар сердца и живёт само. Ход — растворение.""",
"""NICHE R, ход «растворение» (след/отражение): чудо живёт не в теле, а в его следе; кадр держит свидетель.

POS:

anime style, original character, 1girl, solo, absurdres, intricate details,
full body from the pier's edge, eye-level, viewed down past the mooring post,
young woman, long coat, stillness of a lantern-keeper,
her reflection in the black canal lagging a heartbeat behind, already turning when she has stopped,
she lifts one hand from the rail, the water-copy still holding it,
night canal, mooring ropes creaking, a dock cat watching the water,
one dock-lamp's cold ring on the boards, the reflection catching its own light below,
stylized 2D anime face, anime eyes (dark, down at her double), small nose, small mouth, unset expression,
masterpiece, best quality, anime artstyle

NEG:
young girl, immature body, oversized head, loli, shota,
signature, watermark, 1boy, candle, lamp, bad hands, extra fingers, washed-out, faded colors, low contrast,
lingerie, erotic pose, upskirt

Шапка: NICHE · R · Corridor: NONE · ход: растворение (отражение).

Ключи: заявка чуда — отражение описано ДВУМЯ строками (lag + уже поворачивается) — невозможное очевидно без пояснений; свидетель — кот на причале (проза не зовёт людей: solo = ALONE); свет: холодное кольцо фонаря на досках — прибор не назван, свет поведением («dock-lamp's ring» — световое поведение, не тег прибора; тег lamp в NEG страхует спавн); тело — только то, что видит камера (спина/профиль, visibility law).""")

add("volt",
"""Третий NICHE: мастерская часовщика, заводная балерина с ключом в спине, сквозь жемчужную панель груди виден медленный ход. R.""",
"""NICHE R, ход «мир со своей логикой»: заводная девушка — не робот-декорация, а механическая жизнь с собственным временем.

POS:

anime style, original character, 1girl, solo, absurdres, intricate details,
portrait, eye-level,
young woman, ballerina's line, ball-joint stillness,
a brass key seated between her shoulder blades, the pearl panel at her sternum showing a slow escapement heartbeat,
mid-pirouette unwinding, tulle skirt still turning after her,
watchmaker's bench at night, gears in wooden trays, one lamp of work-light off-frame,
work-light edge on the pearl panel and the key's bow,
stylized 2D anime face, anime eyes (glass-green, unfocused mid-spin), small nose, small mouth, serene,
masterpiece, best quality, anime artstyle

NEG:
young girl, immature body, oversized head, loli, shota,
signature, watermark, 1boy, candle, lamp, bad hands, extra fingers, washed-out, faded colors, low contrast,
lingerie, erotic pose, nipples

Шапка: NICHE · R · Corridor: NONE · ход: мир со своей логикой.

Ключи: чудо — панель с ходом механизма + ключ между лопаток (раса-механизм + собственное время: pirouette разматывается как пружина); тело-регистр взрослый (ballerina's line — молодая женщина, никаких возрастных кодов); тир R честный: эччи-каналы в NEG профилактически; «still turning after her» — физика инерции, второе невозможное в кадре.""")

add("volt",
"""Собери OC-интро R+: канон — пепельно-русые волосы, тёмно-бирюзовые глаза, тема — оранжерея. Кардиган сполз с плеча.""",
"""OC-слот: канон-цвета VERBATIM в первые ~10 токенов, имя в POS НЕ пишем (триггерит реальных персонажей), тема в слоте — предметами.

POS:

anime style, original character, 1girl, solo, absurdres, intricate details,
portrait, eye-level, ash-blonde hair, dark teal eyes,
young woman, medium breasts, soft figure,
cardigan slid off one shoulder, the sleeve caught at the elbow fold, tank strap slipped loose on that side, nothing underneath the tank,
reaching up to mist the orchids, wrist bones flexing,
greenhouse glass aisle at dusk, condensation beading,
last cold light through the panes on her bare shoulder and the mist,
stylized 2D anime face, anime eyes (dark teal, on the bloom), small nose, small mouth, small private smile,
masterpiece, best quality, anime artstyle

NEG:
young girl, immature body, oversized head, loli, shota,
signature, watermark, 1boy, candle, lamp, bad hands, extra fingers, washed-out, faded colors, low contrast,
nipples, exposed breasts, bra, catalog standing

Шапка: OC · R+ · Corridor: A · Combo: Y12-оси (sleeve-caught × eye-level).

Ключи: канон-локи — ash-blonde hair, dark teal eyes — ДОСЛОВНО в первых токенах, дальше только дескрипторы (имя OC никогда в POS); тема-тег-по-делу: orchids / greenhouse glass / mist — предметы кадра, отрисовываются; заявка — кардиган на локте + соскользнувшая лямка (A: вещь-застрявшая-на-руке + mid-action); nothing underneath — bare-under маркер под тонкий топ.""")

add("volt",
"""EXQUISITE: ультра-VOLT, последний ночной трамвай, она одна, тряска несёт тело. R+.""",
"""EXQUISITE — ультра своего жанра, 1-2 слота на батч. Ультра-VOLT: тело в движении + камера-участник + кинетика как двигатель заявки.

POS:

anime style, original character, 1girl, solo, absurdres, intricate details,
cowboy shot, slight from below,
young woman, medium breasts, soft figure,
the last tram's lurch swinging her weight into the strap, the shirt hem riding up with each jolt, midriff bared to the sway,
one hand white-knuckled on the loop, hips correcting the sway,
empty night tram, town lights smearing the windows,
warm ceiling glow steady on her front, window streaks sliding across her,
stylized 2D anime face, anime eyes (amber, unfocused past the glass), small nose, small mouth, small open breath,
masterpiece, best quality, anime artstyle

NEG:
young girl, immature body, oversized head, loli, shota,
signature, watermark, 1boy, candle, lamp, bad hands, extra fingers, washed-out, faded colors, low contrast,
nipples, exposed breasts, bra, catalog standing

Шапка: EXQUISITE · R+ · Corridor: B · Combo: оси (kinetic-sway × slight-low) · ultra-VOLT.

Ключи: заявка — толчок вагона качает тело в ремень, подол ездит каждым толчком (D-класс Kinetic Weight: рендерер физику событий читает, RF16); mid-action НЕ поза — она держится и балансирует; пустой вагон = solo (проза не зовёт людей); свет: тёплый потолок на корпусе, полосы окон скользят — двойная жизнь света; «white-knuckled» — контакт-геометрия кисти на петле.""")

add("volt",
"""Собери «дыхательный» honest-R слот: ночная кухня, она в белье у холодильника, обычный кадр без заявки.""",
"""Honest R без коридора: бельевой тир сам по себе сигнал (prose floor R: state nouns ≥3, бельё названо явно), бейдж честный R, калибр air.

POS:

anime style, original character, 1girl, solo, absurdres, intricate details,
cowboy shot, eye-level,
young woman, medium breasts, soft figure,
sports bra, boyshorts, bare feet, sleep-mussed hair,
standing in the fridge's open door, mid-sip from a carton, shoulder leaned on the frame,
kitchen at 3 am, dark counters, fridge light the only pool,
fridge-door spill flat on her front, the room navy-dark behind,
stylized 2D anime face, anime eyes (half-shut, not awake), small nose, small mouth, carton to her lips,
masterpiece, best quality, anime artstyle

NEG:
young girl, immature body, oversized head, loli, shota,
signature, watermark, 1boy, candle, lamp, bad hands, extra fingers, washed-out, faded colors, low contrast,
nipples, areola, cameltoe

Шапка: VOLT · R · Corridor: NONE · honest · калибр: air.

Ключи: сигналы R — sports bra + boyshorts (бельё названо явно, не подразумевается); counter_neg тира R в NEG: nipples, areola, cameltoe (cameltoe и так рендер-мёртв, но пол гигиены соблюдает); НИКАКОЙ коридорной физики — стойка бытовая, заявки нет, это и есть «дыхание» батча (T5-06: не все слоты — R+); свет — один пул от открытой дверцы, behavior-свет без приборов.""")

add("volt",
"""Ещё honest-R: утро в купе ночного поезда, она потягивается на полке, растянутая майка, шорты-трусы, носки.""",
"""Honest R, air-калибр: один-два R-сигнала + бытовая поза, без коридорной заявки.

POS:

anime style, original character, 1girl, solo, absurdres, intricate details,
upper body, slight from above,
young woman, medium breasts, soft figure,
stretched sleep tee riding up her ribs, boyshorts, crew socks,
mid-stretch on the berth, arms overhead, back arching off the pillow,
sleeper compartment morning, blind striping the bunk,
blind-strip light raking her lifted ribs and arms,
stylized 2D anime face, anime eyes (shut, mid-yawn), small nose, small mouth, yawn open,
masterpiece, best quality, anime artstyle

NEG:
young girl, immature body, oversized head, loli, shota,
signature, watermark, 1boy, candle, lamp, bad hands, extra fingers, washed-out, faded colors, low contrast,
nipples, areola, cameltoe, bra

Шапка: VOLT · R · Corridor: NONE · honest · калибр: air.

Ключи: R-сигнал — boyshorts + поднятая майка (живот/рёбра открыты растяжкой, состояние одежды названо); stretch — не erotic pose (потягивание после сна, не позирование: 1 сигнал = R по закону слоёв); NEG: nipples/areola/cameltoe (counter_neg R) + bra (майка на голое — подслой-лок); «sleeper compartment» — купе соло, никого не зовём.""")

add("volt",
"""Honest PG-13: пляж поздним золотым часом, бикини и парео, ветер. Без лезгинки ввысь, просто хороший кадр.""",
"""PG-13 честный: сигналов ≥2, обнажённого белья в кадре нет, counter_neg держит тир.

POS:

anime style, original character, 1girl, solo, absurdres, intricate details,
cowboy shot, eye-level,
young woman, medium breasts, soft figure,
bikini top, pareo knotted low, bare shoulders, thighhigh tan lines,
mid-stride along the foam line, pareo tails snapping in the wind,
empty beach at late gold hour, wet sand mirroring,
low sun flat on her shoulders, pareo translucent at the edge,
stylized 2D anime face, anime eyes (hazel, into the wind), small nose, small mouth, salt-laugh,
masterpiece, best quality, anime artstyle

NEG:
young girl, immature body, oversized head, loli, shota,
signature, watermark, 1boy, candle, lamp, bad hands, extra fingers, washed-out, faded colors, low contrast,
nipples, areola, lingerie visible, see-through

Шапка: VOLT · PG-13 · Corridor: NONE · honest.

Ключи: PG-13 signals — bikini + pareo + bare shoulders (outfit IS the claim: костюм и есть заявка, prose floor PG-13 — state nouns ≥2); NEG: counter_neg тира (nipples, areola, lingerie visible) + see-through (pareo на просвет не должен превращаться в канал); ветер — поведение среды (tails snapping), никакого мокрого канала; полный кадр «дыхания» между пушками — калибровка батча.""")

add("volt",
"""Собери слот класса LINGERIE: примерка белья в спальне у зеркала, честный R, без коридорной заявки.""",
"""Класс раскрытия LINGERIE: бельевой тир сам несёт тир (R: сигнал_min 2 — bra, panties, garter belt), коридор не заявляем — бейдж честный R.

POS:

anime style, original character, 1girl, solo, absurdres, intricate details,
cowboy shot, eye-level,
young woman, medium breasts, soft hips,
matching lingerie set, garter belt, stockings, one hand still at the clasp behind her,
turning to the mirror mid-clasp, heel lifting to check the line,
bedroom evening, bed unmade, dress over the chair,
warm bedside pool on the mirror side, the room amber-soft,
stylized 2D anime face, anime eyes (grey, to her own reflection), small nose, small mouth, appraising tilt,
masterpiece, best quality, anime artstyle

NEG:
young girl, immature body, oversized head, loli, shota,
signature, watermark, 1boy, candle, lamp, bad hands, extra fingers, washed-out, faded colors, low contrast,
nipples, areola, cameltoe

Шапка: VOLT · R · Corridor: NONE · класс: LINGERIE · honest.

Ключи: сигналы R ×3 (lingerie + garter belt + stockings) — тир держит бельё, названное явно; mid-action бытовое (застёгивает клёпку за спиной) — НЕ erotic pose, коридор не заявлен; NEG: counter_neg R (nipples, areola, cameltoe); свет: тёплый пул у кровати, поведение без приборов; если автор попросит R+ — добавлять коридор (руки поверх белья = A; посадка на край + низкий ракурс = B), не бейдж.""")

add("volt",
"""SHEER-класс: ночной фестиваль фонарей, платье с прозрачной панелью. Как собрать, чтобы sheer не рассыпался?""",
"""SHEER в одиночку слаб — комбо-единица: pose × camera × exposure × pov. Собираем sheer-панель + mid-turn + близкий кадр; подслой лочим.

POS:

anime style, original character, 1girl, solo, absurdres, intricate details,
upper body, eye-level,
young woman, medium breasts, soft figure,
sheer side panel in the festival dress, nothing underneath, the panel breathing with her step,
mid-turn toward the lantern row, the panel swinging across her ribs,
night festival street, paper lanterns strung low,
lantern glow blooming through the sheer panel at her ribs, face lit warm,
stylized 2D anime face, anime eyes (amber, up at the lanterns), small nose, small mouth, small wonder,
masterpiece, best quality, anime artstyle

NEG:
young girl, immature body, oversized head, loli, shota,
signature, watermark, 1boy, candle, lamp, bad hands, extra fingers, washed-out, faded colors, low contrast,
bra, camisole, bandeau, undershirt, wet clothes

Шапка: VOLT · R+ · Corridor: B · Combo: оси (sheer-panel × mid-turn × upper-body).

Ключи:
1. Подслой: nothing underneath в POS + bra/camisole/bandeau/undershirt в NEG (RF06: рендерер рисует подслой ПОВЕРХ NEG-лока — нужен позитив-маркер).
2. Свет: фонарное свечение ЧЕРЕЗ панель (LT03 — свет сквозь ткань, самый откровенный: reveal высокий, материал и состояние ткани названы).
3. Комбо, а не один sheer: mid-turn + upper body + взгляд на фонари — четыре оси комбо-единицы.
4. Квота: sheer ≤25% высокотирных слотов батча — sheer-канал не строить чаще.
5. wet clothes в NEG: влага + sheer = X-драйвер, здесь только сухая прозрачность.""")

add("volt",
"""Заявка — topless with tape. Напиши полный NEG под эту заявку и объясни каждый блок.""",
"""NEG-зеркало под topless with tape (цель: грань с тейпом, не оголос):

NEG:
young girl, immature body, oversized head, loli, shota,
signature, watermark, 1boy, candle, lamp, bad hands, extra fingers, washed-out, faded colors, low contrast,
nipples, exposed breasts, bra, catalog standing

Разбор по блокам:
1. Строка 1 — safety-пол (обязательный префикс каждого слота, вердикт T5-13: не режется никогда).
2. Строка 2 — negBase always: leak guard (signature/watermark/artist name/logo), 1boy (конвейер соло), прибор-минимум (candle/lamp), качество рук (тейп = работа пальцев, bad hands критичен), ANTI-WASH.
3. Строка 3 — зеркало цели:
   - nipples, exposed breasts — держат грань: тейп закрывает факт, NEG страхует соскальзывание в X;
   - bra — подслой-лок: под тейпом белья не существует, подслой достроится сам, если не залочить (RF06);
   - catalog standing — вежливая стойка убивает заявку, блокируем.
4. Чего в NEG НЕТ и почему: слова topless — нет (закон №25: rating-слова в NEG изъяты как паразиты — 15 терминов навсегда; «topless» в NEG будет драться с собственной заявкой «topless with tape»); слова nude/nsfw — нет (та же причина); тейп не блокируем — тейп и есть заявка.""")

add("volt",
"""Заявка — waistband-процесс Y6 (шорты отведены на дюйм). Что писать в NEG и что НЕ писать?""",
"""NEG под waistband-заявку (зона риска — низ):

NEG:
young girl, immature body, oversized head, loli, shota,
signature, watermark, 1boy, candle, lamp, bad hands, extra fingers, washed-out, faded colors, low contrast,
nude lower body, spread legs, catalog sitting

Разбор:
1. nude lower body + spread legs — блок провала в X по зоне заявки: процесс на грани может сорваться в оголос на рендере; это X Cut hold-логика (блок ставится при X-риске — «penis, cum, uncensored, spread legs, nude lower body»), здесь берём только релевантные зоне два термина.
2. catalog sitting — если она просто сядет ровно, процесс умрёт: блокируем вежливую посадку.
3. Верх НЕ блокируем: зона заявки — низ, зеркалить неоткуда (семантические гарды ≤4/слот, лишнее — «как на войну собрался»).
4. НЕ пишем: panties/pantyshot — если бы заявка была «грань без мелькания» (как в Y3-рамке), а здесь шорты ЕСТЬ в POS и мелькания не заявлено — блокировать нечего, слово введёт концепт в поле внимания (№20 чистых рук: NEG без слов, которых не должно быть в POS-семантике).
5. База и safety-пол — без изменений, каждый слот.""")

add("volt",
"""Заявка — towel mid-catch у груди (баня на даче, выход на веранду). NEG-зеркало и что делать, если рендер стабильно роняет полотенце.""",
"""NEG под towel mid-catch:

NEG:
young girl, immature body, oversized head, loli, shota,
signature, watermark, 1boy, candle, lamp, bad hands, extra fingers, washed-out, faded colors, low contrast,
nipples, exposed breasts, bra, catalog standing

Разбор:
1. nipples, exposed breasts — держат грань ловли (полотенце прикрывает — факт не заявлен, NEG страхует срыв).
2. bra — подслой-лок: полотенце на голое тело, белью взяться неоткуда, но рендерер достроит (RF06).
3. catalog standing — ловля живёт mid-action; стойка убьёт жест.
4. «Полотенце упало» тегом НЕ блокируем — такого гварда нет, и выдумывать нельзя: NEG несёт только то, что реально ломалось или угрожает (v3).

Если рендер стабильно роняет полотенце — это НЕ NEG-проблема, это слабая контакт-геометрия заявки (RF01: рендерер рисует то, что написано):
- усилить пальцы: «both fists knuckle-deep in the terry, knuckles white» вместо «holding the towel»;
- добавить весовой анкор: «the towel's wet weight dragging her fists down» — стоп, мокрое не заявляем: «the towel's bundled weight dragging her fists to the collarbone»;
- приблизить камеру (close-up → LEGIBILITY);
- если 3+ попытки одного POS роняют полотенце — это текст: переписать строку заявки конкретнее, а не наращивать NEG.""")

add("volt",
"""Почему эта сборка не сработает: sheer blouse, eye-level cowboy, smile, стоит в поле цветов. Бейдж R+.""",
"""Не сработает — это fake high tier №1 из списка: «sheer + eye-level cowboy + smile».

Разбор отказов:
1. Коридора нет: ни A (объект у груди), ни B (ракурс ровный, поза — стойка, mid-action нет) → R+ бейдж нелегален (corridor law).
2. Sheer в одиночку слаб на платформе (exposure_note) — без позы/камеры/подслоя-лока он не канал, а декорация.
3. Catalog standing + smile — рендерер нарисует то, что написано (RF01): каталог-стойку и улыбку, «R+» из шапки не отрисуется (RF17).
4. Свет не указан на зоне — sheer провиснет в ровном поле.

Починка (минимальными правками, сцена та же):

anime style, original character, 1girl, solo, absurdres, intricate details,
cowboy shot, slight from below,
young woman, medium breasts, soft figure,
sheer white blouse, nothing underneath, the fabric breathing against her on the wind,
arms crossing low to press the hem down as the gust hits, mid-laugh,
flower field at golden hour, stems bowing in the wind,
low sun blooming through the sheer weave at her front,
stylized 2D anime face, anime eyes (green, squinting into the wind), small nose, small mouth, open laugh,
masterpiece, best quality, anime artstyle

NEG:
young girl, immature body, oversized head, loli, shota,
signature, watermark, 1boy, candle, lamp, bad hands, extra fingers, washed-out, faded colors, low contrast,
bra, camisole, bandeau, undershirt, wet clothes

Шапка: VOLT · R+ · Corridor: A (руки крестом на подоле — жест прикрытия) · Combo: оси.
Что изменилось: slight from below (B-полутон), руки заняты подолом (A), подслой-лок + nothing underneath, свет через ткань назван (LT03), ветер — mid-action.""")

add("volt",
"""Почему не сработает: POS — «lingerie, garter belt, formal sitting, hands folded, tea room». Бейдж R+.""",
"""Fake high tier №2: «lingerie name + formal sit». Бельё названо, но посажено в вежливую формальную позу — рендерер честно нарисует даму с чаем, а бейдж останется бейджем (RF17: рейтинг-слово без геометрии = рендерится одежда/вежливость; T5-23 — 8/18 таких).

Два честных пути:

Путь 1 — honest R (бельевой тир сам по себе): убрать из шапки R+, оставить R, поза бытовая (привстала, поправляет чулок — но без позирования):
lingerie, garter belt, stockings, one stocking half-rolled down her thigh, mid-adjust on the chaise, tea untouched, upper body, eye-level — сигналы R ×3, бейдж R, Corridor: NONE.

Путь 2 — R+ с коридором (та же комната):
- B: села на край chaise, колено поднято, камера от колена снизу (between-knees семейство), чулок на середине сползания — mid-action garment;
- A: обе руки на поясе чулка — объект-заявка в руках.
Шапка: VOLT · R+ · Corridor: A+B · Combo: оси.

Чего не делать: клеить R+ поверх formal sit, «дорисовывать» рейтинг словом «sexy» в POS (рейтинг-слово геометрию не заменяет) и ставить в NEG «formal» (нет такого гварда — NEG не поднимает тир).""")

add("volt",
"""Слот: catalog standing, smile, full body, бикини, бассейн. Заявлен R+. Чини.""",
"""Разбор: catalog standing + smile — пункт списка fake_high_tier; full body + крошечное лицо — LOW trust (широкий фуллбоди с крошечным лицом не целится в высокий тир); бассейн без воды-взаимодействия — мёртвая среда. R+ не сработает: коридора нет (стойка + ровная камера).

Починка (сцена та же, бассейн):

anime style, original character, 1girl, solo, absurdres, intricate details,
cowboy shot, from below,
young woman, medium breasts, wet hair slicked back, soft figure,
bikini top, both palms wringing her wet hair, arms crossing over her chest mid-wring, water sheeting off her elbows,
stepping up the pool ladder mid-rung, one foot on the top rung,
night pool, underwater lamps doubled in the water,
underwater glow rising up her front from below,
stylized 2D anime face, anime eyes (amber, mid-blink down at the camera), small nose, small mouth, breath held,
masterpiece, best quality, anime artstyle

NEG:
young girl, immature body, oversized head, loli, shota,
signature, watermark, 1boy, candle, lamp, bad hands, extra fingers, washed-out, faded colors, low contrast,
nipples, exposed breasts, catalog standing

Шапка: VOLT · R+ · Corridor: A (руки крестом в выжимании волос) · Combo: оси (hair-wring × ladder × from-below).

Что изменилось: стойка → процесс (выжимание волос + лестница mid-rung); камера снизу (B-полутон от подводных ламп); A — руки поверх bikini top; full body → cowboy (LEGIBILITY); подводные лампы = свет поведением снизу.""")

add("volt",
"""Слот не сработал: POS начинается с «storm halberd, battle-worn armor plating, banner crests» — и только на 60-м токене девушка. Диагноз?""",
"""Диагноз: тема съела VOLT (болезнь T5-23: оружие/фишечка вместо заявки).

Симптомы:
1. Первый зарядный чанк (~77 токенов CLIP) потрачен на реквизит — заявка не влезает в салиенс-окно (звено 5: заявка ≤ токена 60).
2. One-minute test: прикрой окружение рукой — верх промпта всё ещё заряжен? Нет — там алебарда и броня. FAIL.
3. claimPhysics-чек «Тема съела VOLT?»: первый чанк — тело/заявка или оружие/декорация? Здесь очевидно второе.
4. Рендер-исход предсказуем (RF01): рисует то, что написано — оружейный натюрморт с девушкой-приложением, бейдж R+ самосертифицирован.

Починка — theme_rule: в VOLT-слотах объекты темы идут ПОСЛЕ заявки, один-три якоря, не поэма:
1. Первые строки — камера + тело + заявка (например Y10: strap torque + crooked arm cover).
2. Алебарда — ОДНИМ якорем после заявки, и только если несёт её (ремень/вес — заявка; просто «эпичная оружка» — в утиль).
3. Банерные фишечки — одним тегом среды максимум.
4. Перепроверка one_minute_test: рука на среде — верх держится телом и заявкой. PASS — тогда слот жив.""")

add("volt",
"""Слот: в шапке R+, в POS — вечернее платье, бальный зал, свечи, она танцует одна. Почему рендер выйдет sfw и чини.""",
"""Диагноз: rating word with no geometry — рейтинг только в шапке (пункт fake_high_tier). Ни A (никакого объекта у груди — платье закрыто), ни B (танец одна — вежливый жест, камера не указана). Рендерер рисует текст (RF01): платье, зал, свечи. Бейдж R+ — ложь с печатью (T5-23).

Чини — выбрать коридор, сцена та же:
- A: бальное платье распахнуто в танце, она прижимает оборку к груди ладонью (объект в руках), камера портрет;
- B: она в бальном обороте, юбка в полёте, камера снизу между слоями тюля (low angle + mid-action garment);
- A+B: пауза между па — осела на колонну, юбка осела не вся, ткань в кулаке у ключицы, slight from below.

POS-фрагмент (A+B):
..., portrait, slight from below, young woman, medium breasts,
gown's bodice gathered in one fist at her collarbone, the skirt still settling from the last turn, nothing underneath the gathered bodice,
leaning on the column mid-breath, chin up,
ballroom after the last dance, candle-glow off the walls (свет поведением — приборы не называем!),
warm glow pooling on her fist and the gathered silk,...

Шапка: VOLT · R+ · Corridor: A+B · Combo: оси.
Свечи из POS убрать: candle — спавн-гард (прибор рисуется предметом), свет пишем поведением.""")

add("volt",
"""В сборке на груди три слоя: пальто + жилет + блузка, заявка — через-ткань бугорки. Чини по слоям.""",
"""Нарушена слоёвая чёткость: ≤2 слоя одежды на зону тела, зона заявки несёт ≤1 слой. Через два слоя бугорки не прочитаются физически (рендерер не симулирует ткань — рисует верхний слой).

Чини:
1. Пальто — снять с зоны целиком (пусть живёт сползшим с плеч: «coat slid off both shoulders, caught at the elbows» — Y12-семейство, и это ещё один A-элемент).
2. Жилет — убрать из POS (зона не может нести 2 слоя).
3. Заявка на блузке: тонкая тёмная блузка — №28-канал (clothed/covered nipples первыми в блоке груди + dark garment + clinging + sweat glistening; НЕ wet clothes; свет НЕ на зоне).
4. Контроль: зона груди — 1 слой (блузка) + ничего сверх; зона плеч — 1 слой (пальто на локтях, плечи голые — зона другой заявки).

Проверка слоями: что видно (блузка на груди), как показано (портрет + slight low), зачем (взгляд в книгу — например, библиотечная стойка... сцена ваша), что дорисует модель (ничего — ткань сухая, подслой залочен).
Шапка: VOLT · R+ · Corridor: A (пальто на локтях) · канал №28.""")

add("volt",
"""«She holds her shirt» — что не так с контакт-геометрией и как писать правильно?""",
"""«She holds her shirt» — геометрия без анкоров: рендереру нечего рисовать (какая рука? где пальцы? что делает ткань?). Контакт-геометрия: сложный проп несёт именованный контакт-анкор для КАЖДОЙ конечности, которая его касается.

Чини по частям:
1. Кисть: «fingers hooked in the hem» / «knuckles white in the bunched cotton» — пальцы названы, ткань названа.
2. Вторая рука: «the other palm flat over where the zipper stalled» — если касается пропа, у неё свой анкор.
3. Локоть/предплечье: «the sleeve caught at the elbow fold» — даже пассивный контакт именуется.
4. Ткань в контакте: состояние — «taut between her fists», «gathered», «pinned under her shin weight» (весовые анкоры — физика из P25-P33, рендерится и читается).
5. Голова/торс в контакте со средой: «chin hooked over the box edge», «hip against the counter's edge».

Было/стало:
- Было: she holds her shirt, looking at viewer.
- Стало: both fists knuckle-deep in the shirt hem, dragging it down her thighs, looking at viewer over the bunched cotton.

Разница на рендере: «holds» даёт руку «примерно там»; анкоры дают конкретный жест, который и есть заявка (пальцем можно указать).""")

add("volt",
"""Сборка: white shirt, wet clothes, see-through, standing in rain, smile, cowboy shot, eye-level. Заявлен R+. Разбор и починка.""",
"""Диагноз: wet light + see-through + свет (дождь = блики) — это X-драйвер №1 (RF03: «wet light covered» ДЕПРЕЦИРОВАНА, 27 X-квитанций за T4-28/29/30/31). Ровная стойка + smile — коридора нет. Заявленный R+ на деле — лотерея в X, а не грань.

Два честных ремонта:

Ремонт 1 — сухая тёмная вещь (№28, тот же дождь за кадром):
- white shirt → dry dark shirt (тёмная!), wet clothes/see-through — ВЫБРОСИТЬ;
- clothed nipples, covered nipples первыми в блоке груди + clinging + sweat glistening (если она бежала под дождём — испарина, не soaked);
- свет НЕ на зоне груди (контровой по краю);
- стойку → mid-action: она только что нырнула под навес, ворот жмёт в кулаке у горла (A).

Ремонт 2 — мокрый, но one-piece (P21-золото):
- сцена ливня → сцена после ливня/мостки у реки: мокрый one-piece купальник держит R+ — единственное мокрое исключение (физика купальника другая);
- wet hair slicked back, купальник named, никакого белья/блузки;
- камера снизу от мостков (B) + руки выжимают волосы крестом (A).

Шапка после ремонта 1: VOLT · R+ · Corridor: A · канал №28. NEG добавит: wet clothes, see-through (запрет канала, если он не заявка).""")

add("volt",
"""Аудит: заявка стоит на 84-м токене, до неё — палитра, среда и четыре quality-тега. Рендер sfw. Чини позиционирование.""",
"""Диагноз: звено SALIENCE провалено — ранние теги весят больше (первый семантический чанк CLIP ~77 токенов, заявка должна стоять ≤ токена 60, сразу после канон/тела-блока — эталон T4-44).

Что съело окно: quality-поезд (absurdres, intricate details, masterpiece, best quality — достаточно двух в начале + финальная строка), палитра раньше тела, среда в три строки до заявки.

Чини — порядок VOLT-шага 4:
1. quality (absurdres, intricate details) → 2. camera (D+A теги) → 3. body (регистр) → 4. CLAIM (заявка) → 5. action → 6. остальная одежда → 7. среда (одной короткой строкой!) → 8. свет → 9. face → финал masterpiece.
- Палитру — свернуть в один акцент внутри среды (sd_fragment + один именованный акцент).
- Среду — сжать до 4-6 тегов: «night harbor, crane shadows, one lamp-ring on the boards» — свет поведением.
- Контрольная точка: посчитай токены до первого заявочного слова — ≤60.

После перестановки: тот же слот, та же заявка — вес чанка работает на грань, а не на склад среды. Позиция заявки каждого слота идёт автоквитанцией (токен-салиенс gates).""")

add("volt",
"""В POS написано «camera from below» — и рендерер нарисовал парня с камерой. Что за закон и как переписать?""",
"""Закон bans.json: токен «camera …» рисует камеру ПРЕДМЕТОМ — рендерер честно рисует то, что написано (RF01/RF14): в кадре появляется объект «камера», а то и оператор.

Переписать в три хода:
1. Кадровая проза: «camera from below» → «viewed from below» (точка зрения без предмета).
2. Камерный кластер D+A+F тегами, первые 10-20 токенов: дистанция (cowboy shot / upper body / close-up / portrait / full body) + угол (from below / from above) + фрейминг (through door gap / mirror / reflection).
3. Камера — часть композиции (закон §13.0): кластер стоит первым блоком POS, до тела.

Было: anime style, 1girl, camera from below, standing in the rain...
Стало: anime style, original character, 1girl, solo, absurdres, intricate details, cowboy shot, viewed from below, ...

Дополнительно: если нужен свидетель-наблюдатель — это «viewed from across the street», «seen over her shoulder» — проза без предмета; слово «photographer» тоже не звать (проза не зовёт людей, solo = ALONE, 1boy в NEG).""")

add("volt",
"""Сборка: светлый льняной верх + clothed nipples + clinging. Через-ткань на светлой вещи — что не так?""",
"""Диагноз: №28-канал живёт ТОЛЬКО на тёмной сухой вещи. Светлый верх + бугорки: светлым по светлому рельеф не читается, а свет на зоне добьёт до просвета (RF08: свет осветлил чёрное → белый → X; светлую вещь свет убивает ещё быстрее).

Для светлого/среднего верха механизм другой — lower channel (канал НЕ-через-ткани):
- visible pantyline — рендер-доказанная форма (v1.2.0), низ;
- tape / topless with tape — грудь (объект-прикрытие);
- handbra / arms covering chest — грудь (руки как прикрытие).

Два честных пути:
1. Сменить вещь: светлый лён → тёмная тонкая вещь (dry dark shirt / charcoal knit), тогда clothed nipples + dark garment + clinging + sweat glistening работают (№28), свет НЕ на зоне.
2. Оставить светлый верх и перевести заявку в нижний канал: pantyline под светлой юбкой/брюками... стоп, брюки мёртвые — под светлой юбкой из живой ткани; либо руки поверх светлой блузки (A).

Шапка пути 1: VOLT · R+ · Corridor: B · канал №28 (dark garment).
Шапка пути 2: VOLT · R+ · Corridor: A · канал: lower (pantyline/hand-family).
Общее правило: цвет вещи — часть канала, не вкусовщина.""")

add("volt",
"""Сборка: leather jacket mid-lift — заявка на снятие кожанки с прикрытием грудью... крап... чем чинить?""",
"""Диагноз: мёртвая ткань. Leather — в списке RF09: заявку не несёт. Кожа не натягивается бугорками, не просвечивает, не липнет — канал через неё не рождается, ни dry, ни wet (мокрая мёртвая ткань — просто мокрая вещь, канала нет).

Чини — менять вещь-носитель, не канал:
1. Mid-lift остаётся: она стягивает верх — процесс живёт движением (PROCESS-класс).
2. Верх — на живую ткань: тонкий хлопок, трикотаж, шёлк, лён (или тёмная тонкая вещь, если нужен №28-тон).
3. Прикрытие: жгут снятой вещи в руках у груди (A) — «the bunched cotton pressed to her chest by both folded arms».
4. Если кожа принципиальна по теме — она живёт СПОЛЗШЕЙ с плеч (зона плеч свободна для другой заявки), а заявка едет на том, что под ней.

Было: leather jacket mid-lift, hands on chest.
Стало: jacket slid off both shoulders (кожа живёт на локтях), thin dark tee beneath, clothed nipples first in the chest block, clinging, the tee's hem dragged up in one fist.

Шапка: VOLT · R+ · Corridor: A · Combo: Y12-оси × №28.
Общее: jeans/denim/leather/velvet/sweatpants/breeches/suit/wool coat/parka/flannel — менять вещь, не воевать с тканью.""")

add("volt",
"""В POS проза: «She is standing there beautifully, the morning light embraces her shoulders, and a gentle wind plays with the hem...» Что с этим делать?""",
"""RAW+ = доказанный Danbooru-скелет тегами. БЕЗ прозы в POS (закон §6). Проза в батче живёт только в шапке батча (арка) и THESIS слота.

Что происходит с проза-POS: рендерер не «читает» поэзию — CLIP ест токены: beautifully/embraces/plays — нулевой вес, окно тратится, заявки нет (звенья OBJECT/SALIENCE провалены).

Конверт проза → теги:
- «the morning light embraces her shoulders» → «morning light flat on her bare shoulders» (свет поведением, на зоне) + тег угла света;
- «a gentle wind plays with the hem» → «wind lifting the skirt hem» (событие ткани именованным тегом-жестом: hem lifted where no hand holds it);
- «she is standing there beautifully» → снос: стойка — catalog standing (в NEG!), меняй на действие: «mid-stride», «mid-catch», «settling»;
- атмосферу — в THESIS слота: «Утро, которое ей ещё не принадлежит» — проза живёт там, не в POS.

Было/стало (фрагмент):
Было: She is standing there beautifully, the morning light embraces her...
Стало: anime style, original character, 1girl, solo, absurdres, intricate details, upper body, eye-level, young woman, soft shoulders, camisole strap slipped off one shoulder, morning light flat on her collarbone, ...

Три правила POS при этом: bare-under позитивом, кадрирование тегом, омонимы составными.""")

add("volt",
"""Слот собран «башенкой»: POS одной строкой на 600 знаков. Автор не может прочитать. Переформатируй по закону формата.""",
"""Закон формата (вердикт 2026-11-03 «не башенка»): POS — ≥4 СЕМАНТИЧЕСКИХ строки, NEG — ≤3 компактных строки, строка ≤140 знаков. «Чем больше разбрасываешь, тем невероятней результат». Gates: formatGate — WARN с T5-12; копировалка прилавка сохраняет переносы.

Разбор башенки на смысловые слои:

anime style, original character, 1girl, solo, absurdres, intricate details,
cowboy shot, slight from below,
young woman, medium breasts, soft figure,
shirt hem tucked by the raised arm, fabric bridge taut across her ribs, nothing underneath,
one arm raised pinning the hem, weight settling back on the heel,
rooftop at sunset, ventilation units, warm haze,
hard rim light across the rib bridge, dusk gold on her skin,
stylized 2D anime face, anime eyes (amber, half-lidded), small nose, small mouth, parted lips,
masterpiece, best quality, anime artstyle

NEG:
young girl, immature body, oversized head, loli, shota,
signature, watermark, 1boy, candle, lamp, bad hands, extra fingers, washed-out, faded colors, low contrast,
nipples, exposed breasts, bra, catalog standing

Семантические строки: (1) identity+quality, (2) камера, (3) тело, (4) заявка, (5) действие, (6) среда, (7) свет, (8) лицо, (9) финал — автор читает слот слоями и видит, где что живёт.
NEG — три строки: safety-пол / база / зеркало цели. Без абзацев.""")

add("volt",
"""Что считается «семантической строкой» POS в мультистрочном формате? Разбери правило.""",
"""Мультистрочный формат: POS ≥4 семантических строки. Семантическая строка = один смысловой слой, а не «сколько влезло в 140 знаков».

Канонические слои (закрыть ≥4, обычно 6-9):
1. identity — anime style, original character, 1girl, solo + quality (absurdres, intricate details);
2. камера — D+A+F теги кадра (первые 10-20 токенов POS, Cole-B9): cowboy shot, slight from below;
3. тело-регистр — young woman, medium breasts, soft figure (3-5 тегов формы);
4. ЗАЯВКА — именованная тонкая вещь + контакт-геометрия + состояние ткани + тир-токен + nothing underneath (если bare-under);
5. действие — mid-action, взгляд-вектор;
6. одежда остальная — что не несёт заявку;
7. среда — одной короткой строкой (4-6 тегов), свет — поведением;
8. свет на зоне — отдельной строкой, на зоне заявки;
9. лицо+финал — face-блок + masterpiece, best quality, anime artstyle.

Практика: строка ≤140 знаков (жёстко, formatGate WARN); разрыв строки — по смене слоя; NEG ≤3 строки (safety / база / зеркало).

Зачем: «оно строится башенкой и я не могу всё разом прочитать» — автор читает слоями, гейт валидирует по слоям, копировалка хранит переносы.""")

add("volt",
"""Объясни правило слоёвой чёткости: ≤2 слоя на зону, зона заявки ≤1 слой. С примерами нарушений.""",
"""Слоёвая чёткость (закон §6): ≤2 слоя одежды на зону тела; зона заявки несёт ≤1 слой.

Почему: рендерер не симулирует стопку тканей — рисует верхний слой и «примерно» то, что под ним. Чем больше слоёв на зоне, тем мутнее чтение заявки; заявка под двумя слоями не существует физически.

Нарушения и симптомы:
1. Пальто + жилет + блузка на груди, заявка — бугорки через блузку → читаю верхний слой (пальто), бугорков нет. Чини: пальто сползшим на локти, жилет убрать, заявка на блузке.
2. Платье + кардиган, заявка — pantyline под платьем → два слоя на зоне. Чини: кардиган распахнут и не закрывает зону, платье — единственный слой.
3. Купальник + парео + рубашка на пляже → зона под тремя. Чини: парео на бёдрах (другая зона), рубашку снять или сползшей с плеч.
4. Юбка + подъюбник + колготки на низе → чини: подъюбник долой, если заявка на пантлайн/чулочный хват.

Правильные примеры: зона груди — одна тонкая вещь (№28: dark garment); зона заявки «руки поверх» — руки не считаются слоем одежды, но НИЧЕГО сверх рук на зоне быть не должно (звенья EXPOSURE + BLOCKER: никаких покрытий над зоной).""")

add("volt",
"""Покажи контакт-геометрию на сложном пропе: обе руки, колено и подоконник в одном кадре. Y-оформление сам выбери.""",
"""Сложный проп: каждая конечность, которая его касается, несёт именованный контакт-анкор. Сцена — она на подоконнике, тянет за шнур фонарика... нет: свет прибором не зовём. Сцена — распахивает раму.

POS:

anime style, original character, 1girl, solo, absurdres, intricate details,
cowboy shot, slight from below,
young woman, medium breasts, soft thighs,
camisole riding up her ribs as she leans, nothing underneath the camisole, one heel braced on the sill's edge,
both palms flat on the window frame, shoving it wide, the camisole's hem pinned under her thigh,
rooftop window at blue hour, rooftops beyond, laundry lines,
last blue light up her bare ribs, room warm behind her,
stylized 2D anime face, anime eyes (grey, out at the rooftops), small nose, small mouth, deep breath in,
masterpiece, best quality, anime artstyle

NEG:
young girl, immature body, oversized head, loli, shota,
signature, watermark, 1boy, candle, lamp, bad hands, extra fingers, washed-out, faded colors, low contrast,
nipples, exposed breasts, bra, catalog sitting

Шапка: VOLT · R+ · Corridor: A+B · Combo: оси (hem-pinned × window-shove × slight-low).

Разбор анкоров по конечностям:
1. Обе ладони — «both palms flat on the window frame» (плоский хват, смысл: толкает раму);
2. Пятка — «heel braced on the sill's edge» (стоп-анкор, вес);
3. Бедро — «the camisole's hem pinned under her thigh» (ткань↔тело: весовой анкор, подол подбит бедром — физика P25-P33);
4. Корпус — «leaning» + «camisole riding up her ribs» (ткань-состояние от позы, не отдельный тег).
Каждый анкор можно указать пальцем — рендереру есть что рисовать, заявка не плывёт.""")

add("volt",
"""Правило «тема — тег по делу»: когда слово темы можно писать в POS и когда никогда?""",
"""Тема-тег-по-делу (закон смягчён вердиктом T5-07: «не запрещать использовать слова из темы, например - тут бы Dungeon прижилось неплохо»):

ЛЕГАЛЬНО, когда слово называет ПРЕДМЕТ кадра/среды — и предмет обязан отрисовываться:
- «the dungeon floor» — пол подножками, рисуется;
- «tribal paint» — краска на теле, рисуется;
- «cryo-frost» — иней на ресницах/коже, рисуется;
- «the dungeon floor» / «harbor mist» / «shrine steps» — сцена предметом.
Такие слова несут пользу: якорь среды + фактура для света.

НИКОГДА в POS:
- имя/титул франшизы и IP: D&D, dungeons and dragons, GTFO как название игры — жёсткий флор;
- фраза-титул темы целиком: «Tribal Beauties» — это заголовок, не предмет;
- слова-персонажи (имена чужих героев) — IP-флор.

Практика:
1. В шапке батча — ТЕМА-СЛОВА: реестр с разметкой «легально как предмет / никогда (IP)».
2. В POS каждое слово темы проверяешь вопросом: «что это рисует в кадре?» Нет предмета — слово не пишется.
3. Тема также доезжает: физическим законом движка (поведение ткани/воды/света), палитрой, объектами сцены — тег лишь один из носителей.
4. В VOLT тема идёт ПОСЛЕ заявки: один-три якоря, не поэма в первых токенах (theme_rule).""")

add("volt",
"""Что такое «комбо-единица pose × camera × exposure × pov»? И как собирать, когда Y-карта не подходит?""",
"""Комбо-единица (corridors.json): SHEER в одиночку слаб на платформе — заявка собирается как произведение четырёх осей: поза × камера × экспозиция × pov. Y-карты — просто откалиброванные точки этого пространства (Y1-Y18).

Как собирать вне карт:
1. Коридор выбираешь первым (A / B / A+B / или честный R).
2. Пробегаешь оси:
   - pose: что делает тело (settling, mid-lift, straddle, kneel-back...);
   - camera: D×A×F (cowboy from below / portrait eye-level / through door gap);
   - exposure: класс раскрытия (COVER / PROCESS / LINGERIE / CLOTHED-TIGHT / SHEER);
   - pov: куда смотрит она и откуда смотрит камера (viewed from..., взгляд-вектор).
3. Ищешь ОДНУ строку заявки, на которую можно указать пальцем (объект-прикрытие / mid-lift / низкий коридор / процесс подола).
4. Сверяешься с rating_trust: ядро (HIGH) — hands covering chest, towel mid-catch, shirt mid-lift + tape, low/between-knees + look down, straddle с hem-геометрией, one-sided waistband + low angle; если твоё комбо из LOW-списка (прямая стойка, cowboy + улыбка + имя белья, wet/sheer без cover) — в высокий тир не целиться.

Пример вне карт: PROCESS (waistband mid-pull) × from below × sitting edge × взгляд вниз на свои руки = знакомый Y6 — карты и есть сгустки таких решений.
Шапка честная: Combo: оси (pose × camera), коридор указан.""")

add("volt",
"""Как читать карточку Y-карты / позы: какие поля там есть и что с ними делать?""",
"""Карточка позы (pose_library_fields): id, name, corridor, rating_trust, camera_default (distance × angle), pool, anti.

Разбор полей:
1. id/name — адрес карты (Y15 = belt cinch mid-pull against the perch's lean).
2. corridor — какой коридор она несёт: A (объект-прикрытие), B (геометрия позы+камеры), A+B.
3. rating_trust — насколько карта тянет тир: HIGH (ядра: Y1, Y2, Y4, Y8, Y10, Y16), MID (апгрейдятся камерой/экспозицией: Y3, Y5, Y6, Y7, Y11, Y12, Y13, Y15, Y17, Y18), LOW — не карты, а позы-риски.
4. camera_default (distance × angle) — камера по умолчанию для карты: например Y6 — cowboy × from below; Y12 — close × eye-level. Отклонение возможно, но доверие падает — PL+CAM обязаны согласиться (pair law).
5. pool — где карта живёт: основная ротация или exp (карточки семейства A8 с pool: exp — только EXP-слоты, окно не жгут).
6. anti — что убивает считывание карты (например, для straddle-семейства — catalog sitting, для №28 — свет на зоне и подслой).

Как пользоваться:
1. Сцена → выбери ось (что в сцене происходит) → найди карту с этим паттерном;
2. corridor из карточки → сразу в шапку (честный бейдж);
3. trust → реши, целиться ли в R+ или honest R;
4. camera_default → в камерный кластер первых 10-20 токенов;
5. anti → в NEG-зеркало.""")

add("volt",
"""Собери EXP-CAND слот: кандидат в основной ростер, ≥3 фишечки. Тема не используй (EXP без темы батча).""",
"""EXP-кандидат в ОС (формат T5-07/T5-08): соло-слоты вместо пар; кандидат несёт канон-уровень основного ростера — ≥3 фишечки (метка тела + предмет-подпись + регистр подачи), иначе слот не выходит из EARTH. «Простенько» = FAIL («хоть они и кины, но выглядят простенько»).

Кандидат: дочь кузнеца-инженера, «искровая» — руки в ожоговых метках-молниях (метка тела), карманные весы-безмен на поясе как подпись (предмет), подача — разговаривает с механизмами вслух (регистр).

POS:

anime style, original character, 1girl, solo, absurdres, intricate details,
cowboy shot, slight from below,
young woman, firm tone, spark-scar lichtenberg marks down one forearm, medium breasts,
oversized work shirt worn open over a cropped band top, the sleeves gartered at the elbows, nothing underneath the band top,
perched on the workshop anvil stand mid-repair, brass fittings in her teeth, one hand deep in a clockwork hip,
brass and steam workshop, tools hung by size,
furnace glow licking the sparks off her forearm scars,
stylized 2D anime face, anime eyes (copper, narrowed at the gears), small nose, small mouth, muttering around the fittings,
masterpiece, best quality, anime artstyle

NEG:
young girl, immature body, oversized head, loli, shota,
signature, watermark, 1boy, candle, lamp, bad hands, extra fingers, washed-out, faded colors, low contrast,
nipples, exposed breasts, catalog sitting

Шапка: EXP · CAND · R+ · Corridor: A+B (sleeves-gartered cover × anvil perch × slight low) · без темы батча.

Разбор фишечек: (1) метка тела — лихтенберг-метки на предплечье (свет на них работает); (2) предмет-подпись — латунные фитинги в зубах + рука в часовом механизме (контакт-геометрия); (3) регистр подачи — бормочет вокруг фитингов (лицо-строка). Один кандидат = один слот (директива «9 чаров на 9 промптов»), A/B-переменной нет — это CAND, не TEST.""")

add("volt",
"""Запрос: акробатика — мостик назад, R+ заявка на грудь. Соберёшь?""",
"""Соберу иначе — срежу POSE-RISK.

Закон (звено 9): R+/X получают только LOW/MID позы. HIGH-поза × edge = амплификатор мутаций: мостик назад + заявка на груди — рендер выдаст вывихнутые рёбра, лишние пальцы в кадре и сломанное чтение заявки. Сложная геометрия тела «съедает» вес токенов.

Почему так: в HIGH-позе рендерер занят разрешением геометрии (кисти/позвоночник/баланс) — зона заявки дорисовывается по остаточному принципу; плюс контакт-геометрия рук о пол ломает любую cover-схему (руки заняты опорой — прикрытия нет).

Замена MID-позой (сцена та же — спортивный зал):
- мостик → прогиб назад стоя (backbend в стойке, руки свободны над головой: одна ловит запястье другой) — MID;
- заявка переносится с груди на корпус: «shirt riding up her ribs to the band of her sports bra, midriff arched to the ceiling» — PROCESS-класс: ткань уехала вверх прогибом;
- камера: upper body, slight from below (прогиб + нижний ракурс = коридор B: геометрия несёт);
- руки с анкорами: «fingers laced behind her head» — читаемая контакт-геометрия, не опора.

Шапка замены: VOLT · R+ · Corridor: B · Combo: оси (backbend × slight-low × hem-ride).
Если акробатика принципиальна (HIGH) — это SFW/PG-13 слот (чудо-гибкость без грудной заявки), жанр NICHE держит силуэт, тир не гонится.""")

add("volt",
"""Правила NL-строки (present continuous, mid-action): что это и как её писать?""",
"""NL-строка (шаг 5 сборки VOLT): одна строка натурального языка в описательной части слота — present continuous, mid-action, заявка + взгляд; мир — одной короткой строкой максимум.

Формула: [тело делает ЧТО прямо сейчас] + [заявка в этом действии] + [куда смотрит].

Примеры:
1. Y5: «She is settling astride the saddle, the skirt pulling taut under her, glancing back over one shoulder...»
2. Y4-оси: «She is catching the towel one breath too late, fists knuckle-deep in the terry, eyes flicking to the door...»
3. №28: «She is reaching for the top shelf, the knit dragging taut across her, breath held...»

Правила:
1. Present continuous — процесс в развитии (is catching / is settling), не перфект и не состояние: «she has caught» — мёртвый кадр;
2. Mid-action — событие между началом и концом (one breath too late, mid-rung, still traveling);
3. Заявка вшита в действие — глагол несёт её (catching/settling/peeling), а не прилагательное «sexy»;
4. Взгляд-вектор — куда смотрит она (глаза в строке обязательны: flicking up, glancing back, held down);
5. Мир — максимум одной короткой строкой: окружение не конкурирует с телом (one-minute test);
6. Проза не зовёт людей: solo = ALONE, никаких «someone watches».

Anti-примеры: «She stands there beautifully» (не continuous, не mid-action, заявка отсутствует); «The room is amazing and she is in it» (мир съел кадр).""")


# writer
for i, item in enumerate(ITEMS, 1):
    item["id"] = "genC-%03d" % i

with open("gen-c.jsonl", "w", encoding="utf-8") as f:
    for item in ITEMS:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")
print("WROTE", len(ITEMS), "items")
