/**
 * Юнит-тесты Y-STAMP (bun test) — клеймо/паспорт слота (В34/В35).
 * Контракт: weave = паттерн карты 1:1 (единственный текст, легальный в POS),
 * stamp = метка-паспорт (только метаданные чипа, в POS НЕ печатается).
 */
import { describe, expect, test } from 'bun:test';
import { buildWeave, buildYStampLine, parseYStampLine, type YCardLike } from '../../src/lib/t5/ystamp';

const CARD: YCardLike = {
  id: 'Y513',
  corridor: 'A',
  builtFrom: 'PL518 + CAM12',
  trust: 'HIGH',
  components: {
    exposure: { class: 'wet-sheer', cover_object: 'sheet', read: 'ткань читает тело' },
    pose: 'the sheet is the claim, weight drags the fabric taut, final release a half-second away',
    pov: 'eye-level',
    camera: '50mm, shallow focus',
    profiling: 'silver hair, amber eyes',
  },
};

describe('buildWeave (В34: вплетение — единственный текст в POS)', () => {
  test('возвращает паттерн карты 1:1 без обозначений', () => {
    expect(buildWeave(CARD)).toBe(
      'the sheet is the claim, weight drags the fabric taut, final release a half-second away',
    );
  });

  test('нет паттерна — пустая строка, не undefined', () => {
    expect(buildWeave({ id: 'Y1' })).toBe('');
  });
});

describe('buildYStampLine (метка-паспорт — только метаданные)', () => {
  test('формат Y-STAMP: id «класс» × поза × камера · corridor', () => {
    const line = buildYStampLine(CARD);
    expect(line).toContain('Y-STAMP: Y513');
    expect(line).toContain('«wet-sheer»');
    expect(line).toContain('corridor A');
  });

  test('пустые поля печатаются честным «—»', () => {
    const line = buildYStampLine({ id: 'Y2' });
    expect(line).toContain('«—»');
    expect(line).toContain('corridor —');
  });
});

describe('parseYStampLine (сверка с картой — как в гейте)', () => {
  test('round-trip: build → parse', () => {
    const parsed = parseYStampLine(buildYStampLine(CARD));
    expect(parsed).not.toBeNull();
    expect(parsed?.id).toBe('Y513');
    expect(parsed?.cls).toBe('wet-sheer');
    expect(parsed?.corridor).toBe('A');
  });

  test('3-значные id читаются (регресс эпохи Y513+)', () => {
    const parsed = parseYStampLine('Y-STAMP: Y521 «class» × pose body · corridor B');
    expect(parsed?.id).toBe('Y521');
  });

  test('мусор и пустая строка → null', () => {
    expect(parseYStampLine('')).toBeNull();
    expect(parseYStampLine('произвольная проза POS без клейма')).toBeNull();
  });
});
