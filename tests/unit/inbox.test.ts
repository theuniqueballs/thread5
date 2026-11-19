/**
 * Юнит-тесты инбокса (bun test) — чистые функции слот-маппинга и порядка.
 * Урок T5-17 (пачка перепуталась слотами) + расширение P999 (2026-11-20):
 * парсер батчей трёхзначный, инбокс не должен отставать — P100 из
 * «Проставить по порядку» больше не стирается при ручной правке.
 */
import { describe, expect, test } from 'bun:test';
import {
  effectiveLabel,
  needsTriage,
  normalizeTag,
  parseBatchFromName,
  parseSlotFromName,
  resolvePreviewPath,
  resolveUploadPath,
  sortItems,
  type InboxItem,
} from '../../src/lib/t5/inbox';

function item(patch: Partial<InboxItem>): InboxItem {
  return {
    id: 'aaaaaa',
    file: 'x.webp',
    origName: 'x.webp',
    size: 100,
    mime: 'image/webp',
    uploadedAt: '2026-11-20T00:00:00Z',
    tag: null,
    batch: null,
    slot: null,
    preview: null,
    status: 'queued',
    triage: { label: 'unknown', reason: 'в очереди', at: '2026-11-20T00:00:00Z' },
    analysis: null,
    authorOverride: null,
    ...patch,
  };
}

describe('parseSlotFromName', () => {
  test('P07 / p7 / 07 - name / _P100', () => {
    expect(parseSlotFromName('P07.webp')).toBe('P07');
    expect(parseSlotFromName('t5-18 p7.png')).toBe('P07');
    expect(parseSlotFromName('07 - name.webp')).toBe('P07');
    expect(parseSlotFromName('T5-26__P100__stamp-id.webp')).toBe('P100'); // регресс P999
  });

  test('мусор → null', () => {
    expect(parseSlotFromName('render final.webp')).toBeNull();
    expect(parseSlotFromName('P1000.webp')).toBeNull(); // за пределами
  });
});

describe('parseBatchFromName', () => {
  test('T5-18_07.webp → T5-18; регистр не важен', () => {
    expect(parseBatchFromName('T5-18_07.webp')).toBe('T5-18');
    expect(parseBatchFromName('t5-07 render.png')).toBe('T5-07');
    expect(parseBatchFromName('no batch.webp')).toBeNull();
  });
});

describe('normalizeTag', () => {
  test('канонический вид «T5-18 P07»', () => {
    expect(normalizeTag('t5-18 p7')).toEqual({ tag: 'T5-18 P07', batch: 'T5-18', slot: 'P07' });
  });

  test('слот числом («СЛОТ 12») и 3-значный слот', () => {
    expect(normalizeTag('СЛОТ 12').slot).toBe('P12');
    expect(normalizeTag('T5-26 P100').slot).toBe('P100');
  });

  test('свободная метка без слота живёт как есть', () => {
    expect(normalizeTag('просто метка')).toEqual({ tag: 'просто метка', batch: null, slot: null });
  });
});

describe('sortItems — батч ↓ по НОМЕРУ, слот ↑ (регресс T5-9 vs T5-10)', () => {
  test('T5-10 выше T5-9, T5-100 выше T5-99', () => {
    const sorted = sortItems([
      item({ batch: 'T5-9', slot: 'P02' }),
      item({ batch: 'T5-10', slot: 'P01' }),
      item({ batch: 'T5-100', slot: 'P01' }),
      item({ batch: 'T5-99', slot: 'P03' }),
    ]);
    expect(sorted.map((i) => i.batch)).toEqual(['T5-100', 'T5-99', 'T5-10', 'T5-9']);
  });

  test('без тега — в конец', () => {
    const sorted = sortItems([item({}), item({ batch: 'T5-01', slot: 'P01' })]);
    expect(sorted[0].batch).toBe('T5-01');
    expect(sorted[1].batch).toBeNull();
  });
});

describe('needsTriage / effectiveLabel', () => {
  test('queued и unknown ждут; fail-closed карантин от 429 перетриажируется', () => {
    expect(needsTriage(item({}))).toBe(true);
    expect(
      needsTriage(item({ status: 'x', triage: { label: 'x', reason: 'триаж упал (429) — карантин (fail-closed)', at: '' } })),
    ).toBe(true);
    expect(
      needsTriage(item({ status: 'x', triage: { label: 'x', reason: 'явный контент', at: '' } })),
    ).toBe(false);
  });

  test('вердикт автора сильнее триажа', () => {
    const i = item({ status: 'x', authorOverride: { label: 'sfw', at: '' } });
    expect(effectiveLabel(i)).toBe('sfw');
  });
});

describe('resolveUploadPath / resolvePreviewPath — путь не выходит из папок', () => {
  test('легальные имена проходят', () => {
    expect(resolveUploadPath('T5-18__P07__20261109-a1b2c3.webp')).toBeTruthy();
    expect(resolvePreviewPath('stamp-preview.webp')).toBeTruthy();
  });

  test('«..» и разделители отсекаются (2026-11-20)', () => {
    expect(resolveUploadPath('..')).toBeNull();
    expect(resolveUploadPath('a/../..')).toBeNull();
    expect(resolveUploadPath('../../etc/passwd')).toBeNull();
    expect(resolvePreviewPath('../meta.json')).toBeNull();
  });
});
