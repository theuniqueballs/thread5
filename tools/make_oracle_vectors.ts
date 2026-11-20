/**
 * Генератор золотых векторов жребия оракула (одноразовый тул, эра ORACLE-2).
 *
 * Фиксирует в tests/fixtures/oracle_vectors.json:
 *   - последовательность mulberry32 для контрольных seed (27, 1, 999);
 *   - полный расклад drawConstellation на СИНТЕТИЧЕСКОМ фикс-реестре
 *     (30 карт + история использования) — тот же файл читают bun-тесты
 *     и python-зеркало (tools/oracle.py): побитовый паритет лочится на
 *     обоих берегах, живой корпус на паритет не влияет.
 *
 * Прогон: bun run scripts внутри репо — bun tools/make_oracle_vectors.ts
 */
import { mulberry32, drawConstellation, buildRotationWindow, batchHeat, type OracleCard, type CardUsage } from '../src/lib/t5/oracle-engine';
import { writeFileSync, mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

/* ── синтетический фикс-реестр: детерминированный, без привязки к живому корпусу ── */

const FIXTURE_CARDS: OracleCard[] = [];
const corridors = ['A', 'B', 'A+B', '—'] as const;
const classes = ['COVER', 'PROCESS', 'CLOTHED-TIGHT', '—'] as const;
for (let i = 1; i <= 30; i++) {
  const id = `Y${i}`;
  const corridor = corridors[i % 4 === 0 ? 3 : i % 3 === 0 ? 1 : i % 5 === 0 ? 2 : 0];
  const exposureClass = corridor === 'A' || corridor === 'A+B' ? (i % 2 === 0 ? 'COVER' : 'PROCESS') : classes[3];
  FIXTURE_CARDS.push({ id, corridor, exposureClass, pattern: `fixture pattern ${id} — object near the chest line` });
}

const FIXTURE_USAGE: Record<string, CardUsage> = {
  Y3: { id: 'Y3', usedCount: 2, lastBatch: 26, lastBatchFile: 'T5-26.md' },
  Y7: { id: 'Y7', usedCount: 1, lastBatch: 25, lastBatchFile: 'T5-25.md' },
  Y11: { id: 'Y11', usedCount: 1, lastBatch: 24, lastBatchFile: 'T5-24.md' },
  Y15: { id: 'Y15', usedCount: 4, lastBatch: 12, lastBatchFile: 'T5-12.md' },
  Y19: { id: 'Y19', usedCount: 1, lastBatch: 26, lastBatchFile: 'T5-26.md' },
  Y23: { id: 'Y23', usedCount: 2, lastBatch: 8, lastBatchFile: 'T5-08.md' },
};

const vectors: {
  era: string;
  note: string;
  mulberry32: Record<string, number[]>;
  fixture: { cards: OracleCard[]; usage: Record<string, CardUsage> };
  draws: Record<string, { seed: number; oc: string[]; main: string[]; exp: string[]; windowExcluded: number; shortfall: number }>;
  window: { depth: number; batches: { no: number; file: string }[]; usedInWindow: Record<string, string> };
  heat: Record<string, unknown>;
} = {
  era: 'ORACLE-2 · 2026-11-20',
  note: 'золотые векторы паритета жребия: bun-тесты (tests/unit/oracle.test.ts) и python-зеркало (tools/oracle.py) обязаны воспроизводить эти значения побитово; правка алгоритма = перегенерация файла + правка обоих зеркал',
  mulberry32: {},
  fixture: {
    cards: FIXTURE_CARDS,
    usage: FIXTURE_USAGE,
  },
  draws: {},
  window: { depth: 0, batches: [], usedInWindow: {} },
  heat: {},
};

for (const seed of [1, 27, 999]) {
  const rng = mulberry32(seed);
  vectors.mulberry32[String(seed)] = Array.from({ length: 8 }, () => rng());
}

for (const batchNo of [27, 28, 40]) {
  const draw = drawConstellation(batchNo, FIXTURE_CARDS, FIXTURE_USAGE, {
    ocTarget: 3, mainTarget: 9, expTarget: 4, windowDepth: 3,
  });
  (vectors.draws as Record<string, unknown>)[String(batchNo)] = {
    seed: draw.seed,
    oc: draw.oc.map((c) => c.id),
    main: draw.main.map((c) => c.id),
    exp: draw.exp.map((c) => c.id),
    windowExcluded: draw.windowExcluded,
    shortfall: draw.shortfall,
  };
}

/* окно ротации на фикс-корпусе */
const FIXTURE_CORPUS = [
  { slug: 'T5-24', slots: [{ yCard: 'Y11' }] },
  { slug: 'T5-25', slots: [{ yCard: 'Y7' }, { yCard: 'Y7' }] },
  { slug: 'T5-26', slots: [{ yCard: 'Y3' }, { yCard: 'Y19' }] },
  { slug: 'T5-23', slots: [{ yCard: 'Y23' }] },
];
vectors.window = buildRotationWindow(FIXTURE_CORPUS, 27, 3);

/* жар на фикс-батче: только числовые компоненты без дрейфа (словари — прерогатива TS) */
vectors.heat = (() => {
  const heat = batchHeat(
    {
      slug: 'T5-99',
      slots: [
        { id: 'P01', rating: 'R+', corridor: 'A', channel: 'chan-x', yCard: 'Y1', pos: '' },
        { id: 'P02', rating: 'R+', corridor: 'A', channel: 'chan-x', yCard: 'Y2', pos: '' },
        { id: 'P03', rating: 'R', corridor: 'B', channel: 'chan-y', yCard: 'Y4', pos: '' },
        { id: 'P04', rating: 'PG-13', corridor: '—', channel: null, yCard: null, pos: '' },
      ],
    },
    FIXTURE_USAGE,
  );
  return {
    slotCount: heat.slotCount, ratedCount: heat.ratedCount, rplusShare: heat.rplusShare,
    corridorHistogram: heat.corridorHistogram, cardsUsed: heat.cardsUsed, cardsFresh: heat.cardsFresh,
    channelDupes: heat.channelDupes.map((c) => [c.channel, c.count]),
    score: heat.score, label: heat.label,
  };
})();

const OUT = join(dirname(fileURLToPath(import.meta.url)), '..', 'tests', 'fixtures', 'oracle_vectors.json');
mkdirSync(dirname(OUT), { recursive: true });
writeFileSync(OUT, JSON.stringify(vectors, null, 2) + '\n', 'utf8');
console.log(`векторы записаны: ${OUT}`);
