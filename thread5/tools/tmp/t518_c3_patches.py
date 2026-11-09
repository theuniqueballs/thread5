#!/usr/bin/env python3
import io
P='batches/T5-18.md'
t=io.open(P,encoding='utf-8').read()
fails=[]
def rep(old,new,label):
    global t
    if old in t: t=t.replace(old,new,1)
    else: fails.append('MISS '+label)

# P29: kill candle reading
rep("the ember at her fingertip keeping one warm point in the cold room, eyes into the lens",
    "a coal-warm glow cupped in her bare palm — no flame, only warmth — while her gaze stays locked on the viewer, not the glow",'P29 candle')
rep("ember glow at the fingertips, drifting scent drawn as visible curls","a coal-warm glow held in her bare palm, drifting scent drawn as visible curls",'P29 race line')

# P31: human face + mask, drop "cheap"
rep("1girl, solo, dark raccoon mask-band across the eyes, small rounded raccoon ears, cheap-champagne-gold nicotine-amber palette",
    "1girl, solo, dark bandit-mask smudged around her human eyes, small rounded raccoon ears on top of her head, champagne-gold nicotine-amber palette",'P31 line1')
rep("Gutter champagne palette, cheap-champagne-gold poured over nicotine-amber, one red-lacquer-lip strike",
    "Gutter champagne palette, champagne-gold poured over nicotine-amber, one red-lacquer-lip strike",'P31 palette')
rep("hazy, second figure, face hidden, thin tail, tail raised",
    "hazy, second figure, text, caption, animal muzzle, fur-covered face",'P31 neg')

# P32: honest->bare, text guard
rep("the boyshorts' waistband riding honest above the skirt's slide","the boyshorts' waistband riding bare above the skirt's slide",'P32 scene')
rep("the boyshorts' waistband reading honest above the low line at the spine's bend","the boyshorts' waistband riding bare above the low line at the spine's bend",'P32 line1')
rep("hazy, second figure, two girls, extra person, face hidden\n\nP33","hazy, second figure, text, caption, face hidden\n\nP33",'P32 neg')

# P24: drop "Pixie", cloud-stair
rep("Pixie summer palette, worn-denim-blue-faded with shift-cotton-soft white, pollen-gold-heavy light and one glint-wing-green accent in the ribbon",
    "Summer shift palette, worn-denim-blue-faded with shift-cotton-soft white, pollen-gold-heavy light and one glint-wing-green accent in the ribbon",'P24 palette')
rep("her bare left foot already pressed down on a cloud that behaves like a stair off the doorstep",
    "her bare left foot already pressed down on the white cloud firm underfoot like a stair off the doorstep",'P24 cloud2')
rep("hazy, second figure, both feet on the ground, tea spilled, shoes on",
    "hazy, second figure, text, caption, both feet on the ground, shoes on",'P24 neg')

# P30: wings furled + stepladder
rep("whispering the night's last psalm while her folded wings draw closer with every word, round amber eyes level with the lens",
    "whispering the night's last psalm while her furled wings — wingtips tucked at her waist like a folded umbrella — draw closer with every word, round amber eyes level with the lens",'P30 wings')
rep("she pauses halfway down a wooden stepladder and leans off it toward the viewer at eye height, one hand gripping the ladder's wooden rail, the belfry's stone wall behind her",
    "she pauses halfway down a wooden kitchen stepladder with flat steps under her left foot and leans off it toward the viewer at eye height, one hand gripping the ladder's wooden rail, the belfry's stone wall behind her",'P30 ladder')

# P01: pour-up final geometry
rep("the teapot sits on the table and pours its stream UPWARD, the amber column rising from the spout to a cup she holds high over her head, the rising stream lit from inside and laying warm light down her raised arms and throat, the cup catching it at the top",
    "the teapot rests tipped on the table, its spout aimed at the ceiling, and a ribbon of tea climbs the air in an arc into the cup she steadies high overhead, the climbing column lighting her raised arms from below",'P01 pour')

# P11: lintel at head height
rep("the doorway shrunk to half her height: she crouches deep beneath its lintel folding into quarters — one knee up, chest to thigh, chin stacked over her hands — her tapered tail folding flat behind her like a closing ruler, the frame's glass-blue light cutting the low door in half",
    "the doorway's lintel now at her head height: she kneels deep beneath it, folded under the blue frame — one knee up, chin over stacked hands — her snake tail flat behind her, the glass-blue light crowding her from above",'P11 lintel')
rep("hazy, second figure, standing upright, full-height door, tail missing",
    "hazy, second figure, standing upright, tall doorway, tail missing",'P11 neg')

# P25: ears explicit early
rep("1girl, solo, nipples a soft twin-print through the stretched buttonholes, candy-pink-bright sugar-white-hot palette, white hair in high loose pigtails",
    "1girl, solo, white rabbit ears folded flat back in denial with rose-pink inner sides, nipples a soft twin-print through the stretched buttonholes, candy-pink-bright sugar-white-hot palette, white hair in high loose pigtails",'P25 ears')

io.open(P,'w',encoding='utf-8').write(t)
print('FAILS:' if fails else 'ALL OK')
for f in fails: print(' ',f)
