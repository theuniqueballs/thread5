/**
 * Сверка третьего органа: прилавок (API-роут draw) на живом корпусе.
 * Повторяет код-путь src/app/api/t5/oracle/draw/route.ts без Next-обёртки:
 * readSpecJson(camera) + listBatches/readBatch + buildCardUsage + drawConstellation.
 * Прогон: bun tools/check_draw_parity.ts
 */
import { join } from 'node:path';
import { readdirSync, readFileSync } from 'node:fs';
import { resolveT5Root } from '../src/lib/t5/store';
import { parseBatch } from '../src/lib/t5/parse';
import { buildCardUsage, drawConstellation, type OracleCard } from '../src/lib/t5/oracle-engine';

const root = resolveT5Root();
console.log('T5_ROOT =', root);

const cam = JSON.parse(readFileSync(join(root, 'specs/camera.json'), 'utf8'));
const cards: OracleCard[] = cam.y_cards.cards.map((c: { id: string; corridor?: string; components?: { exposure?: { class?: string }; pose?: string }; pattern?: string }) => ({
  id: c.id,
  corridor: c.corridor ?? '—',
  exposureClass: c.components?.exposure?.class ?? '—',
  pattern: c.components?.pose || c.pattern || '',
}));

const corpus = readdirSync(join(root, 'batches'))
  .filter((f) => /^T5-\d+\.md$/iu.test(f))
  .map((f) => {
    const text = readFileSync(join(root, 'batches', f), 'utf8');
    const batch = parseBatch(text);
    return { slug: batch.slug, slots: batch.slots.map((s) => ({ yCard: s.yCard })) };
  });

const usage = buildCardUsage(corpus, 27);
const draw = drawConstellation(27, cards, usage, { ocTarget: 3, mainTarget: 21, expTarget: 9, windowDepth: 3 });
console.log('OC  :', draw.oc.map((c) => c.id).join(' '));
console.log('MAIN:', draw.main.map((c) => c.id).join(' '));
console.log('EXP :', draw.exp.map((c) => c.id).join(' '));
console.log('seed:', draw.seed, '| windowExcluded:', draw.windowExcluded, '| shortfall:', draw.shortfall);
