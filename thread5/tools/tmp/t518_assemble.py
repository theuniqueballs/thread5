#!/usr/bin/env python3
# Assemble loop files: c1 (all 12 originals), c2 (11 дожимов), c3 (9 финалов) → webp
import io, os, json
from PIL import Image

SRC = '/home/z/my-project/thread5/tools/tmp/'
DST = '/home/z/my-project/public/t5/loop/T5-18/'
C1 = ['P01','P11','P24','P25','P26','P27','P28','P29','P30','P31','P32','P33']
C2 = ['P25','P26','P27','P28','P29','P30','P31','P32','P01','P11','P24']
C3 = ['P25','P26','P29','P31','P32','P01','P11','P24','P30']

def conv(src, dst):
    img = Image.open(src).convert('RGBA')
    img.save(dst, 'WEBP', quality=86, method=4)

for d in ['c1','c2','c3']:
    os.makedirs(DST + d, exist_ok=True)

plan = [('c1', C1, 'render_c1'), ('c2', C2, 'render_c2'), ('c3', C3, 'render_c3')]
count = 0
for circ, ids, folder in plan:
    for pid in ids:
        src = SRC + folder + '/' + pid + '.png'
        dst = DST + circ + '/' + pid + '.webp'
        if os.path.exists(src):
            conv(src, dst); count += 1
        else:
            print('MISSING', src)
print('converted', count)
