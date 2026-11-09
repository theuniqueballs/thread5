#!/usr/bin/env python3
import io
P='batches/T5-18.md'; S='batches/T5-18/stories.md'
t=io.open(P,encoding='utf-8').read(); s=io.open(S,encoding='utf-8').read()
fails=[]
def rep(txt,old,new,label):
    if old in txt: return txt.replace(old,new,1)
    fails.append('MISS '+label); return txt
t=rep(t,"wet-teal hair in a slick low bun ending in drip-tips, glass-blue translucent skin with a soft core-glow, young fluid build",
        "wet-teal hair in a slick low bun, damp fair skin, young resilient build",'P12 pos cleanup')
t=rep(t,"young nimble build, cat ears angled at the grin, theft-gold-bright",
        "young nimble build, theft-gold-bright",'P20 ears')
t=rep(t,"she bends over the armrest to bring her face within a hand-span of the lens, weight sunk into the cushion",
        "she bends over the armrest to bring her face within a hand-span of the viewer, weight sunk into the cushion",'P26 lips')
io.open(P,'w',encoding='utf-8').write(t)
s=rep(s,"шляпка пыхает кольцом; споры-угольки вспыхивают на локте","пар над её головой пыхает кольцом; тёплые искры вспыхивают на локте",'P14 scene')
s=rep(s,"cast: register: young nimble, кошка R04 (дубль кода с P06 — легален, ≤2 на код).","cast: register: young nimble, человек с недособранным котом.",'P20 cast')
io.open(S,'w',encoding='utf-8').write(s)
print('FAILS:' if fails else 'ALL OK')
for f in fails: print(' ',f)
