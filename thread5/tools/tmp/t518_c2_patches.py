#!/usr/bin/env python3
import io
P='batches/T5-18.md'
t=io.open(P,encoding='utf-8').read()
fails=[]
def rep(old,new,label):
    global t
    if old in t: t=t.replace(old,new,1)
    else: fails.append('MISS '+label)

# P25: physical candy-pink source
rep("one poppy-red-flash accent at the choker's bow; her colors are sweetness with the safety off.",
    "one poppy-red-flash accent at the choker's bow; the wall behind her painted solid candy-pink, the seat's cushion sugar-white — sweetness with the safety off.",'P25 src')
rep("she leans in from the side until her lips graze the frame's upper rim, one knee up on the seat beside the viewer's place, weight planted on the palm, whispering her denial",
    "she leans in from the side until her face fills the frame's upper half and her lips graze the frame's upper rim, one knee up on the seat beside the viewer's place, weight planted on the palm, whispering her denial",'P25 lean')

# P26: strong lean + tail-wrap
rep("she bends over the armrest to bring her face within a hand-span of the viewer, weight sunk into the cushion, whispering frost at the lens while her plush tail has already wrapped her own ankle, grey-green eyes locked on the lens",
    "she bends low over the armrest, shoulders sinking into the cushion, bringing her face within a hand-span of the viewer and across the frame's upper half, whispering frost at the lens while her plush snow-leopard tail wraps tight around her own ankle — the tail betraying the thaw before her lips do, grey-green eyes locked on the lens",'P26 lean')

# P27: physical palette source
rep("one tiger-amber-eye accent at the table's lampless morning window; her colors are a warning label on soft skin.",
    "one tiger-amber-eye accent at the window's morning light; the wall behind her striped charcoal on snow-white — a warning label on soft skin.",'P27 src')

# P28: doorway + anti-prayer
rep("she leans through the doorway toward the lens with one hand on the jamb above, whispering a blessing under the lintel while the window glass behind answers in sapphire and ruby, the glass freckles catching the window's colors one by one, gaze level into the lens",
    "framed by the dark door jamb filling both edges of the shot, she leans through the doorway toward the viewer, one hand pressed on the jamb above her head, her upper body crossing into the lens zone while she whispers a blessing under the lintel, the window glass behind answering in sapphire and ruby, the glass freckles catching the window's colors one by one, gaze level into the lens",'P28 lean')
rep("hazy, second figure, two girls, extra person, face hidden\n\nP29","hazy, second figure, two girls, extra person, hands clasped in prayer\n\nP29",'P28 neg')

# P29: lean across sill
rep("she braces one knee on the windowsill and leans across into the lens, curtain brushing her jaw, whispering her half-prayer while her hair's tips thin into incense smoke and the ember at her fingertip keeps one warm point in the cold room, eyes into the lens",
    "she braces one knee up on the windowsill and leans across it into the lens, curtain brushing her jaw, lips high near the top of the shot as she whispers her half-prayer, her hair's tips thinning into incense smoke, the ember at her fingertip keeping one warm point in the cold room, eyes into the lens",'P29 lean')

# P30: wooden stepladder + anti-caption/escalator + lean
rep("chest-up from below the ladder step, seated eye-line","chest-up view at the ladder's height, from the seated eye-line",'P30 framing')
rep("she stops halfway down the stepladder and leans in at the lens height, one hand gripping the rail, whispering the night's last psalm while the folded wings draw closer with every word, round amber eyes level with the lens",
    "she pauses halfway down a wooden stepladder and leans off it toward the viewer at eye height, one hand gripping the ladder's wooden rail, the belfry's stone wall behind her, whispering the night's last psalm while her folded wings draw closer with every word, round amber eyes level with the lens",'P30 lean')
rep("lips at the top frame edge mid-whisper\n\n","lips near the top of the shot mid-psalm\n\n",'P30 face A')
rep("psalm at the frame's upper edge mid-verse, anime eyes (amber, round and quiet)",
    "lips near the top of the shot mid-psalm, anime eyes (amber, round and quiet)",'P30 face B')
rep("hazy, second figure, face hidden, profile view only, wings spread",
    "hazy, second figure, face hidden, text, caption, escalator, spread wings",'P30 neg')

# P31: race features early
rep("1girl, solo, cheap-champagne-gold nicotine-amber palette, dusty-grey hair in double dutch braids with tape-tied ends, rain-shined grey skin, young scrappy build, dark mask-ring around the eyes, mid_whisper_counter",
    "1girl, solo, dark raccoon mask-band across the eyes, small rounded raccoon ears, cheap-champagne-gold nicotine-amber palette, dusty-grey hair in double dutch braids with tape-tied ends, rain-shined fair skin, young scrappy build, mid_whisper_counter",'P31 line1')
rep("her thick ringed tail curled around the hip like a trophy boa, eyes boring down the lens",
    "her thick fluffy grey-brown ringed raccoon tail curled visibly around her hip with the rings reading clearly, eyes boring down the lens",'P31 tail')

# P32: desk-slide + waistband
rep("she slides onto the desk edge beside the lens and leans across its width, one hand flat among the papers, whispering a compliment too filthy for chrome",
    "she slides her hips onto the desk edge beside the viewer and leans across its width, the boyshorts' waistband riding honest above the skirt's slide, one hand flat among the papers, whispering a compliment too filthy for chrome",'P32 slide')

# P01: fix upward-pour physics
rep("she leans back over the kitchen table while the teapot pours its stream UP toward a cup waiting at the ceiling, the amber column lit from inside and laying warm light up her throat and jaw, steam falling past her chin like slow snow",
    "the teapot sits on the table and pours its stream UPWARD, the amber column rising from the spout to a cup she holds high over her head, the rising stream lit from inside and laying warm light down her raised arms and throat, the cup catching it at the top",'P01 physics')
rep("hazy, stream pouring down, cup on the table, hat fallen",
    "hazy, stream pouring down, cup on the table, stream from her mouth, spitting tea",'P01 neg')

# P11: explicit crouch fold
rep("she folds herself into quarters to slip the doorway that has shrunk below her height, chin stacked over her hands, her tapered tail folding last like a closing ruler, the frame's glass-blue light cutting the room in half",
    "the doorway shrunk to half her height: she crouches deep beneath its lintel folding into quarters — one knee up, chest to thigh, chin stacked over her hands — her tapered tail folding flat behind her like a closing ruler, the frame's glass-blue light cutting the low door in half",'P11 fold')
rep("hazy, second figure, door full-size, bones bent wrong, tail missing",
    "hazy, second figure, standing upright, full-height door, tail missing",'P11 neg')

# P24: bare foot on cloud-step
rep("she takes the morning's first step off the doorstep onto a cloud that behaves like a stair, mug level in one hand, tea unspilled, the world strung below her in farms and wire-threads, pollen-gold dust rising off the threshold",
    "her bare left foot already pressed down on a cloud that behaves like a stair off the doorstep, the right shoe left on the doormat behind her, mug level in one hand, tea unspilled, the world strung far below her in farms and wire-threads, pollen-gold dust rising off the threshold",'P24 cloud')
rep("hazy, second figure, feet on the ground, tea spilled, clouds solid floor",
    "hazy, second figure, both feet on the ground, tea spilled, shoes on",'P24 neg')

io.open(P,'w',encoding='utf-8').write(t)
print('FAILS:' if fails else 'ALL OK')
for f in fails: print(' ',f)
