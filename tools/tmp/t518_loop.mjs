import ZAI from 'z-ai-web-dev-sdk';
import fs from 'fs';
import path from 'path';

const BATCH = '/home/z/my-project/thread5/batches/T5-18.md';
const OUT = '/home/z/my-project/thread5/tools/tmp/render_c3';

function parseSlots() {
  const txt = fs.readFileSync(BATCH, 'utf-8');
  const parts = txt.split(/^P(\d\d) — /m).slice(1);
  const slots = {};
  for (let i = 0; i < parts.length; i += 2) {
    const id = 'P' + parts[i];
    const body = parts[i + 1];
    const posIdx = body.indexOf('POS:\n');
    const negIdx = body.indexOf('NEG:\n');
    if (posIdx === -1 || negIdx === -1) continue;
    const pos = body.slice(posIdx + 5, negIdx).trim();
    slots[id] = pos;
  }
  return slots;
}

const want = process.argv.slice(2);
const slots = parseSlots();
fs.mkdirSync(OUT, { recursive: true });
const zai = await ZAI.create();

for (const id of want) {
  const pos = slots[id];
  if (!pos) { console.error('NO POS for', id); continue; }
  const outPng = path.join(OUT, `${id}.png`);
  if (fs.existsSync(outPng) && fs.statSync(outPng).size > 10000) { console.log('skip', id); continue; }
  let done = false;
  for (let a = 1; a <= 3 && !done; a++) {
    try {
      const t0 = Date.now();
      const r = await zai.images.generations.create({ prompt: pos, size: '864x1152' });
      const b64 = r?.data?.[0]?.base64;
      if (!b64) throw new Error('empty response');
      fs.writeFileSync(outPng, Buffer.from(b64, 'base64'));
      console.log(`OK ${id} ${((Date.now()-t0)/1000).toFixed(1)}s ${(fs.statSync(outPng).size/1024).toFixed(0)}KB`);
      done = true;
    } catch (e) {
      console.error(`ERR ${id} try${a}: ${e.message}`);
      if (a < 3) await new Promise(r => setTimeout(r, 6000 * a));
    }
  }
}
console.log('DONE');
