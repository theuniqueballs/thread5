/**
 * Юнит-тесты инбокса (bun test) — чистые функции слот-маппинга и порядка.
 * Урок T5-17 (пачка перепуталась слотами) + расширение P999 (2026-11-20):
 * парсер батчей трёхзначный, инбокс не должен отставать — P100 из
 * «Проставить по порядку» больше не стирается при ручной правке.
 */
import { describe, expect, test } from 'bun:test';
import {
  effectiveLabel,
  latestBatchCode,
  needsTriage,
  normalizeTag,
  parseBatchFromName,
  parseSlotFromName,
  resolvePreviewPath,
  resolveUploadPath,
  slotCandidates,
  sortItems,
  type InboxItem,
} from '../../src/lib/t5/inbox';
import { buildUploadChunks } from '../../src/lib/t5/upload-chunks';

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
    identity: null,
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

  test('1301-вердикт фильтра — детерминированный: авто-ретрая НЕ заказывает (урок 2026-11-21)', () => {
    // живая причина из triageImage: без слов-триггеров fail-closed/429/too many/карантин —
    // иначе очередь триажа не дренируется (13 отказов крутились циклом бесконечно)
    expect(
      needsTriage(
        item({ status: 'x', triage: { label: 'x', reason: 'контент-фильтр зрения отклонил кадр (1301) — вероятный X, вердикт фильтра (не сбой)', at: '' } }),
      ),
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

/* ── 2026-11-21: нарезка пачек по 2/≤8МБ (502 шлюза) + слот-кандидаты ───── */

describe('buildUploadChunks — приказ автора «по две штуки» (2026-11-21)', () => {
  const MB = 1024 * 1024;
  const f = (size: number) => ({ file: { size } });

  test('пачка нарезается по 2 файла: 5 → 2+2+1', () => {
    const chunks = buildUploadChunks([f(MB), f(MB), f(MB), f(MB), f(MB)]);
    expect(chunks.map((c) => c.length)).toEqual([2, 2, 1]);
  });

  test('байтовый кап: 5+5 МБ > 8 МБ — каждый летит один', () => {
    const chunks = buildUploadChunks([f(5 * MB), f(5 * MB)]);
    expect(chunks.map((c) => c.length)).toEqual([1, 1]);
  });

  test('2×4 МБ = 8 МБ ровно — влезают вместе', () => {
    const chunks = buildUploadChunks([f(4 * MB), f(4 * MB)]);
    expect(chunks.map((c) => c.length)).toEqual([2]);
  });

  test('тяжёлая одиночка 20 МБ — чанк из одного файла', () => {
    const chunks = buildUploadChunks([f(20 * MB)]);
    expect(chunks).toHaveLength(1);
    expect(chunks[0]).toHaveLength(1);
  });

  test('пустая пачка → пустой набор чанков', () => {
    expect(buildUploadChunks([])).toEqual([]);
  });
});

describe('latestBatchCode / slotCandidates — слот зрением (2026-11-21)', () => {
  test('последний батч — реальный максимум в batches/ (не по строке)', async () => {
    const code = await latestBatchCode();
    expect(code).toMatch(/^T5-\d{1,3}$/u);
    // корпус живой: T5-27 уже существует — максимум не может быть меньше
    expect(Number.parseInt(code!.slice(3), 10)).toBeGreaterThanOrEqual(27);
  });

  test('T5-27 отдаёт 33 слота-кандидата с сигнатурами POS', async () => {
    const list = await slotCandidates('T5-27');
    expect(list).toBeTruthy();
    const lines = list!.split('\n');
    expect(lines).toHaveLength(33);
    expect(lines[0]).toContain('P01');
    expect(lines[0]).toContain('Vae');
  });

  test('несуществующий батч → null (зрение не получит мусор)', async () => {
    expect(await slotCandidates('T5-999')).toBeNull();
  });
});
