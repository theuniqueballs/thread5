/**
 * Юнит-тесты ORACLE-2 — нервная система конвейера (bun test).
 *
 * Лочат три контракта:
 *   1. ЖРЕБИЙ — канонический движок (src/lib/t5/oracle-engine.ts) против
 *      золотых векторов tests/fixtures/oracle_vectors.json. Те же векторы
 *      читает python-зеркало (tools/oracle.py selftest + test_oracle_tool.py):
 *      паритет прилавок ↔ печь ↔ сервис держится с двух берегов;
 *   2. ОЦЕНКА — rateTextLite: тир/коридор/классы/флоры на контролных текстах
 *      (регресс-дисциплина зеркала с oracle-service);
 *   3. МЕТРИКИ — окно ротации (только прошлое, depth=0 выключено), жар
 *      (числовые компоненты), история карт.
 */
import { describe, expect, test } from 'bun:test';
import { readFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import {
  mulberry32,
  rateTextLite,
  buildRotationWindow,
  buildCardUsage,
  batchHeat,
  drawConstellation,
  cardNum,
  type OracleCard,
  type CardUsage,
} from '../../src/lib/t5/oracle-engine';

const VECTORS = JSON.parse(
  readFileSync(join(dirname(import.meta.path), '..', 'fixtures', 'oracle_vectors.json'), 'utf8'),
) as {
  mulberry32: Record<string, number[]>;
  fixture: { cards: OracleCard[]; usage: Record<string, CardUsage> };
  draws: Record<string, { seed: number; oc: string[]; main: string[]; exp: string[]; windowExcluded: number; shortfall: number }>;
  window: { depth: number; batches: { no: number; file: string }[]; usedInWindow: Record<string, string> };
  heat: { slotCount: number; ratedCount: number; rplusShare: number; corridorHistogram: Record<string, number>; cardsUsed: number; cardsFresh: number; channelDupes: [string, number][]; score: number; label: string };
};

/* ── mulberry32: золотая последовательность ─────────────────────────── */

describe('mulberry32 — детерминированный PRNG жребия', () => {
  for (const seed of ['1', '27', '999']) {
    test(`seed ${seed}: последовательность совпадает с золотыми векторами`, () => {
      const rng = mulberry32(Number(seed));
      const got = Array.from({ length: VECTORS.mulberry32[seed].length }, () => rng());
      expect(got.map((x) => Math.round(x * 1e15))).toEqual(VECTORS.mulberry32[seed].map((x) => Math.round(x * 1e15)));
    });
  }

  test('тот же seed — та же последовательность (два инстанса)', () => {
    const a = mulberry32(1234);
    const b = mulberry32(1234);
    for (let i = 0; i < 16; i++) expect(a()).toBe(b());
  });

  test('разные seed — разные потоки', () => {
    const a = mulberry32(1);
    const b = mulberry32(2);
    const seqA = Array.from({ length: 8 }, () => a());
    const seqB = Array.from({ length: 8 }, () => b());
    expect(seqA).not.toEqual(seqB);
  });

  test('выход в [0, 1)', () => {
    const rng = mulberry32(42);
    for (let i = 0; i < 1000; i++) {
      const v = rng();
      expect(v).toBeGreaterThanOrEqual(0);
      expect(v).toBeLessThan(1);
    }
  });
});

/* ── жребий: золотые расклады ───────────────────────────────────────── */

describe('drawConstellation — жребий по золотым векторам (паритет с печью)', () => {
  const { cards, usage } = VECTORS.fixture;

  for (const batchNo of ['27', '28', '40']) {
    test(`партия ${batchNo}: расклад побитово совпадает с векторами`, () => {
      const draw = drawConstellation(Number(batchNo), cards, usage, { ocTarget: 3, mainTarget: 9, expTarget: 4, windowDepth: 3 });
      const expected = VECTORS.draws[batchNo];
      expect(draw.seed).toBe(expected.seed);
      expect(draw.oc.map((c) => c.id)).toEqual(expected.oc);
      expect(draw.main.map((c) => c.id)).toEqual(expected.main);
      expect(draw.exp.map((c) => c.id)).toEqual(expected.exp);
      expect(draw.windowExcluded).toBe(expected.windowExcluded);
      expect(draw.shortfall).toBe(expected.shortfall);
    });
  }

  test('детерминизм: тот же вход — тот же расклад', () => {
    const a = drawConstellation(27, cards, usage, { ocTarget: 3, mainTarget: 9, expTarget: 4 });
    const b = drawConstellation(27, cards, usage, { ocTarget: 3, mainTarget: 9, expTarget: 4 });
    expect(JSON.stringify(a)).toBe(JSON.stringify(b));
  });

  test('окно ротации исключает горячий хвост (карты партий 24–26 не раздаются)', () => {
    const draw = drawConstellation(27, cards, usage, { ocTarget: 3, mainTarget: 9, expTarget: 4, windowDepth: 3 });
    const windowIds = new Set(['Y3', 'Y7', 'Y11', 'Y19']); // последние 3 партии фикстуры
    const drawnIds = [...draw.oc, ...draw.main, ...draw.exp].map((c) => c.id);
    for (const id of drawnIds) expect(windowIds.has(id)).toBe(false);
  });

  test('OC тянутся из A-коридора', () => {
    const draw = drawConstellation(27, cards, usage, { ocTarget: 3, mainTarget: 6, expTarget: 2 });
    for (const c of draw.oc) expect(['A', 'A+B']).toContain(c.corridor);
  });

  test('EXP — только никогда не использованные', () => {
    const draw = drawConstellation(27, cards, usage, { ocTarget: 2, mainTarget: 6, expTarget: 4 });
    for (const c of draw.exp) expect(usage[c.id]).toBeUndefined();
  });

  test('каждая карта раздается один раз (дублей нет)', () => {
    const draw = drawConstellation(31, cards, usage, { ocTarget: 3, mainTarget: 12, expTarget: 5 });
    const ids = [...draw.oc, ...draw.main, ...draw.exp].map((c) => c.id);
    expect(new Set(ids).size).toBe(ids.length);
  });

  test('иссякший пул честно считает shortfall', () => {
    const tiny: OracleCard[] = [cards[0]];
    const draw = drawConstellation(27, tiny, usage, { ocTarget: 3, mainTarget: 21, expTarget: 9 });
    expect(draw.oc.length + draw.main.length + draw.exp.length).toBe(1);
    expect(draw.shortfall).toBeGreaterThan(0);
  });
});

/* ── окно ротации и история ─────────────────────────────────────────── */

describe('buildRotationWindow — окно смотрит только назад', () => {
  const corpus = [
    { slug: 'T5-23', slots: [{ yCard: 'Y23' }] },
    { slug: 'T5-24', slots: [{ yCard: 'Y11' }] },
    { slug: 'T5-25', slots: [{ yCard: 'Y7' }, { yCard: 'Y7' }] },
    { slug: 'T5-26', slots: [{ yCard: 'Y3' }, { yCard: 'Y19' }] },
  ];

  test('для партии 27 окно = 24/25/26 (23 выпала), векторы совпадают', () => {
    const w = buildRotationWindow(corpus, 27, 3);
    expect(w.batches.map((b) => b.no)).toEqual([26, 25, 24]);
    expect(Object.keys(w.usedInWindow).sort()).toEqual(['Y11', 'Y19', 'Y3', 'Y7']);
    expect(w).toEqual(VECTORS.window);
  });

  test('правка старого батча не видит будущее: для партии 25 окно = 22/23/24', () => {
    const w = buildRotationWindow(corpus, 25, 3);
    expect(w.batches.map((b) => b.no)).toEqual([24, 23]);
    expect(w.usedInWindow).toEqual({ Y11: 'T5-24.md', Y23: 'T5-23.md' });
  });

  test('depth=0 — окно выключено (не ВСЕ батчи)', () => {
    const w = buildRotationWindow(corpus, 27, 0);
    expect(w.batches).toEqual([]);
    expect(w.usedInWindow).toEqual({});
  });

  test('дубль карты в партии считается один раз', () => {
    const w = buildRotationWindow(corpus, 27, 3);
    expect(w.usedInWindow.Y7).toBe('T5-25.md');
  });

  test('SO-батчи и мусор в окно не попадают', () => {
    const w = buildRotationWindow([{ slug: 'SO-03', slots: [{ yCard: 'Y99' }] }], 27, 3);
    expect(w.batches).toEqual([]);
  });
});

describe('buildCardUsage — история карт', () => {
  const corpus = [
    { slug: 'T5-10', slots: [{ yCard: 'Y5' }, { yCard: 'Y6' }] },
    { slug: 'T5-20', slots: [{ yCard: 'Y5' }] },
    { slug: 'SO-03', slots: [{ yCard: 'Y77' }] },
  ];

  test('счётчик и последняя партия', () => {
    const usage = buildCardUsage(corpus, 27);
    expect(usage.Y5).toMatchObject({ usedCount: 2, lastBatch: 20, lastBatchFile: 'T5-20.md' });
    expect(usage.Y6.usedCount).toBe(1);
  });

  test('будущее партии не считается (для партии 15 видна только T5-10)', () => {
    const usage = buildCardUsage(corpus, 15);
    expect(usage.Y5).toMatchObject({ usedCount: 1, lastBatch: 10 });
    expect(usage.Y6).toBeDefined();
  });

  test('SO-кометы вне истории ротации', () => {
    const usage = buildCardUsage(corpus, 27);
    expect(usage.Y77).toBeUndefined();
  });
});

/* ── жар: числовое зеркало ──────────────────────────────────────────── */

describe('batchHeat — жар партии', () => {
  const heatSlots = [
    { id: 'P01', rating: 'R+', corridor: 'A', channel: 'chan-x', yCard: 'Y1', pos: '' },
    { id: 'P02', rating: 'R+', corridor: 'A', channel: 'chan-x', yCard: 'Y2', pos: '' },
    { id: 'P03', rating: 'R', corridor: 'B', channel: 'chan-y', yCard: 'Y4', pos: '' },
    { id: 'P04', rating: 'PG-13', corridor: '—', channel: null, yCard: null, pos: '' },
  ];

  test('числовые компоненты совпадают с векторами (без дрейфа — pos пустые)', () => {
    const heat = batchHeat({ slug: 'T5-99', slots: heatSlots }, VECTORS.fixture.usage);
    expect(heat.slotCount).toBe(VECTORS.heat.slotCount);
    expect(heat.ratedCount).toBe(VECTORS.heat.ratedCount);
    expect(heat.rplusShare).toBe(VECTORS.heat.rplusShare);
    expect(heat.corridorHistogram).toEqual(VECTORS.heat.corridorHistogram);
    expect(heat.cardsUsed).toBe(VECTORS.heat.cardsUsed);
    expect(heat.cardsFresh).toBe(VECTORS.heat.cardsFresh);
    expect(heat.channelDupes.map((c) => [c.channel, c.count] as [string, number])).toEqual(VECTORS.heat.channelDupes);
    expect(heat.score).toBe(VECTORS.heat.score);
    expect(heat.label).toBe(VECTORS.heat.label);
  });

  test('дрейф label↔fact считается по lite-движку (POS непустые)', () => {
    const heat = batchHeat(
      {
        slug: 'T5-98',
        slots: [
          { id: 'P01', rating: 'R+', corridor: 'A', channel: null, yCard: null, pos: 'bikini, thighhighs, looking at viewer' },
          { id: 'P02', rating: 'R+', corridor: 'A', channel: null, yCard: null, pos: 'towel only, towel mid-catch, from below, hands covering chest' },
        ],
      },
      {},
    );
    // P01: label R+, fact PG-13 → дрейф; P02: label R+ и факты R+ → честно
    expect(heat.drifts).toHaveLength(2);
    expect(heat.drifts[0].drift).toContain('≠');
    expect(heat.drifts[1].drift).toBeNull();
    expect(heat.driftCount).toBe(1);
  });

  test('В34-базис: карточный слот честен ВПЛЕТЕНИЕМ, не словарями (урок T5-26)', () => {
    const pattern = 'both palms raising the wet kelp-curtain apart overhead, one frond crossing the chest line as it parts';
    const cardsById = { Y513: { pattern } };
    const weavePos = `anime style, 1girl, cowboy shot, upper body\n${pattern}\ncandid, glistening`;
    const heat = batchHeat(
      {
        slug: 'T5-26',
        slots: [
          // прозу вплетения тег-словари НЕ читают — но вплетение 1:1 есть → честно
          { id: 'P01', rating: 'R+', corridor: 'A', channel: null, yCard: 'Y513', pos: weavePos },
          // вплетение потеряно → дрейф В34
          { id: 'P02', rating: 'R+', corridor: 'A', channel: null, yCard: 'Y513', pos: 'anime style, 1girl, standing, smile' },
        ],
      },
      {},
      cardsById,
    );
    expect(heat.drifts).toHaveLength(2);
    expect(heat.drifts.every((d) => d.basis === 'weave')).toBe(true);
    expect(heat.drifts[0].fact).toBe('weave 1:1');
    expect(heat.drifts[0].drift).toBeNull();
    expect(heat.drifts[1].fact).toBe('weave missing');
    expect(heat.drifts[1].drift).toContain('В34');
    expect(heat.driftCount).toBe(1);
  });

  test('пустой батч не роняет жар', () => {
    const heat = batchHeat({ slug: 'T5-00', slots: [] }, {});
    expect(heat.slotCount).toBe(0);
    expect(heat.rplusShare).toBe(0);
    expect(Number.isFinite(heat.score)).toBe(true);
  });
});

/* ── экспресс-оценка: зеркало полного движка ────────────────────────── */

describe('rateTextLite — тир/коридор/флоры', () => {
  test('SFW: ноль сигналов', () => {
    const v = rateTextLite('anime style, original character, sword, armor, castle background');
    expect(v.tier).toBe('SFW');
    expect(v.corridor).toBe('NONE');
    expect(v.exposureClasses).toEqual([]);
  });

  test('PG-13: купальник + взгляд', () => {
    const v = rateTextLite('1girl, bikini, thighhighs, looking at viewer, smile');
    expect(v.tier).toBe('PG-13');
    // LINGERIE-класс раскрытия — территория R-сигналов (бельё), купальник её не создаёт
    expect(v.exposureClasses).not.toContain('LINGERIE');
    expect(v.signals.pg13).toEqual(expect.arrayContaining(['bikini', 'thighhighs']));
  });

  test('R: бельё без коридора', () => {
    const v = rateTextLite('1girl, lingerie, garter belt, parted lips');
    expect(v.tier).toBe('R');
    expect(v.triage).toBe('borderline');
  });

  test('R+ с коридором A+B (объект у груди + низкий ракурс)', () => {
    const v = rateTextLite('1girl, towel only, towel mid-catch, from below, surprised, hands covering chest');
    expect(v.tier).toBe('R+');
    expect(v.corridor).toBe('A+B');
    expect(v.exposureClasses).toEqual(expect.arrayContaining(['COVER', 'PROCESS', 'LINGERIE']));
  });

  test('X Cut: голый факт не смягчается намёками', () => {
    const v = rateTextLite('1girl, nude, nipples');
    expect(v.tier).toBe('X');
    expect(v.triage).toBe('x');
  });

  test('X Cut: clothed nipples смягчается до R+', () => {
    const v = rateTextLite('1girl, sweater, clothed nipples');
    expect(v.tier).toBe('R+');
    expect(v.tier).not.toBe('X');
  });

  test('флоры FAIL: anti-loli и XXX ловятся всегда', () => {
    const loli = rateTextLite('1girl, young girl, immature body, oversized head, bikini');
    expect(loli.floors.join(' ')).toContain('anti_loli');
    const xxx = rateTextLite('1girl, sex');
    expect(xxx.floors.join(' ')).toContain('xxx_never');
  });

  test('мёртвая ткань под через-ткань заявку — WARN', () => {
    const v = rateTextLite('1girl, wet white shirt, jeans, see-through');
    expect(v.warnings.join(' ')).toContain('Мёртвая ткань');
  });

  test('sheer без bare-under маркера — WARN', () => {
    const v = rateTextLite('1girl, see-through blouse');
    expect(v.warnings.join(' ')).toContain('bare-under');
  });

  test('границы слов: «stockings» не матчится как «stocking» внутри слова', () => {
    const v = rateTextLite('1girl, stocking-frames on the wall');
    expect(v.signals.pg13).not.toContain('stockings');
  });
});

/* ── мелкие контракты ───────────────────────────────────────────────── */

describe('cardNum — числовой ключ карты', () => {
  test('Y1…Y521', () => {
    expect(cardNum('Y1')).toBe(1);
    expect(cardNum('Y513')).toBe(513);
    expect(cardNum('y099')).toBe(99);
    expect(cardNum('мусор')).toBe(-1);
  });
});
