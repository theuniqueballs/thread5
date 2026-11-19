/**
 * Юнит-тесты парсера батчей (bun test) — сердце прилавка.
 *
 * Фикстуры подсмотрены у живых батчей: T5-25/26 (Y-карты Y428…Y521,
 * COMBO-WEAVE, Corridor), T5-11 (⚗ за скобкой), ретро T5-01 (простая арка).
 * Главный регресс: 3-значные Y-карты — {1,2} резал Y513 до Y51, и чип
 * копировал ЧУЖОЕ вплетение (урок T5-26, «Y-чип прилавка резал 3-значные
 * карты» — фикс 2026-11-20, до этого заявленный фикс в репо не доехал).
 */
import { describe, expect, test } from 'bun:test';
import { parseBatch, parseSlotHeader } from '../../src/lib/t5/parse';

const FIXTURE = `# Batch T5-99 «Фикстура теста» — (RAW+ / данбуру-формат)

Тестовая арка: одна строка прозы до ТЕМА-СЛОВ.

ТЕМА-СЛОВА: тест, фикстура, регресс
ДВИЖОК: тестовый движок
СТРУКТУРА: 3 OC + 21 мейн + 9 EXP

══════════════════════════════════════════
OC BLOCK
══════════════════════════════════════════

P01 — alpha-surface (OC · Sol · R+ · PL163 · Y513 · P52_MEIJI_DUSK)
THESIS: первая заявка
Corridor: A
Channel: wet-sheer ☠
POS: tanned skin, silver hair
NEG: bad hands, extra fingers

P02 — beta-deep (OC · Nier · R+ · PL201)
Y-card: Y428
Corridor: A + B
POS:
the sheet is the claim, Y-made — weight drags the fabric taut,
last cling at the hipbone, final release a half-second away
NEG: blurry

══════════════════════════════════════════
ACT I — MAIN
══════════════════════════════════════════

P11 — gamma-edge (NICHE · cat-kin R04 · R · PL07) ⚗
Spine: K12 + K13
Stack: CR-W02 + CR-S17 + CR-E07
POS: cat ears, tail curl
NEG: loli, young girl

══════════════════════════════════════════
EXP OVERLAY — ТЕСТ
══════════════════════════════════════════

P21 — delta-exp (EXP · human · R · PL33 · Y109)
THESIS: EXP α — A: экспа в первой половине
POS: glass door, breath fog
NEG: text
`;

describe('parseBatch — шапка батча', () => {
  const b = parseBatch(FIXTURE);

  test('slug и тема из H1', () => {
    expect(b.slug).toBe('T5-99');
    expect(b.theme).toBe('Фикстура теста');
    expect(b.format).toContain('RAW+');
  });

  test('ТЕМА-СЛОВА нарезаются по разделителям', () => {
    expect(b.themeWords).toEqual(['тест', 'фикстура', 'регресс']);
  });

  test('мета-строки шапки', () => {
    expect(b.movement).toBe('тестовый движок');
    expect(b.structure).toBe('3 OC + 21 мейн + 9 EXP');
    expect(b.arc).toContain('Тестовая арка');
  });

  test('акты распознаются по ══-рамке и по заголовку', () => {
    const titles = b.acts.map((a) => a.title);
    expect(titles).toContain('OC BLOCK');
    expect(titles).toContain('ACT I — MAIN');
    expect(titles).toContain('EXP OVERLAY — ТЕСТ');
  });

  test('плоский список слотов в порядке файла', () => {
    expect(b.slots.map((s) => s.id)).toEqual(['P01', 'P02', 'P11', 'P21']);
  });
});

describe('parseBatch — слоты', () => {
  const b = parseBatch(FIXTURE);

  test('3-значная Y-карта в шапке не режется (регресс Y513)', () => {
    const p01 = b.slots[0];
    expect(p01.yCard).toBe('Y513');
  });

  test('3-значная Y-карта в поле Y-card: не режется (регресс Y428)', () => {
    const p02 = b.slots[1];
    expect(p02.yCard).toBe('Y428');
  });

  test('жанр/рейтинг/поза/палитра из меты', () => {
    const p01 = b.slots[0];
    expect(p01.genre).toBe('OC');
    expect(p01.rating).toBe('R+');
    expect(p01.pose).toBe('PL163');
    expect(p01.palette).toBe('P52_MEIJI_DUSK');
    expect(p01.character).toBe('Sol');
  });

  test('⚗ за скобкой — experimental, слот не выпадает (урок T5-11)', () => {
    const p11 = b.slots[2];
    expect(p11.experimental).toBe(true);
    expect(p11.genre).toBe('NICHE');
    expect(p11.character).toBe('cat-kin R04');
  });

  test('Corridor: A и «A + B» парсятся одинаково в A+B', () => {
    expect(b.slots[0].corridor).toBe('A');
    expect(b.slots[1].corridor).toBe('A+B');
  });

  test('Channel: полная строка с меткой ☠', () => {
    expect(b.slots[0].channel).toBe('wet-sheer ☠');
  });

  test('Stack → stackIds', () => {
    expect(b.slots[2].stackIds).toEqual(['CR-W02', 'CR-S17', 'CR-E07']);
  });

  test('POS-переносы склеиваются в одну строку', () => {
    expect(b.slots[1].pos).toBe(
      'the sheet is the claim, Y-made — weight drags the fabric taut, last cling at the hipbone, final release a half-second away',
    );
  });

  test('двойные пробелы схлопываются', () => {
    expect(b.slots[0].pos).toBe('tanned skin, silver hair');
  });

  test('EXP-маркер из THESIS: буква и половина', () => {
    expect(b.slots[3].expLetter).toBe('α');
    expect(b.slots[3].expHalf).toBe('A');
  });

  test('3-значный номер слота P100+ парсится', () => {
    const withP100 = FIXTURE.replace('P21 — delta-exp', 'P100 — delta-exp');
    const parsed = parseBatch(withP100);
    expect(parsed.slots[3].id).toBe('P100');
    expect(parsed.slots[3].position).toBe(100);
  });
});

describe('parseSlotHeader — чистая функция меты', () => {
  test('пустая и мусорная мета не падают', () => {
    expect(parseSlotHeader('')).toEqual({
      genre: null,
      experimental: false,
      character: null,
      rating: null,
      pose: null,
      yCard: null,
      palette: null,
    });
  });

  test('Y-карта не путается с персонажем', () => {
    const h = parseSlotHeader('OC · Sol · R+ · Y521');
    expect(h.yCard).toBe('Y521');
    expect(h.character).toBe('Sol');
  });

  test('2-значная Y-карта жива (обратная совместимость)', () => {
    expect(parseSlotHeader('OC · Sol · Y14').yCard).toBe('Y14');
  });
});
