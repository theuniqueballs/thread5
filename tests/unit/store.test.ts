/**
 * Юнит-тесты хранилища (bun test) — порядок полки и безопасность слагов.
 * Регресс 2026-11-20: лексикографическая сортировка ломается на разных
 * разрядах номеров («T5-9.md» > «T5-10.md») — прилавок с батчем №100
 * показывал бы хаос, а [ ] ходил бы не туда.
 */
import { describe, expect, test } from 'bun:test';
import * as path from 'node:path';
import { batchKey, isDeliveredBatch, isSafeSlug, resolveT5Root, shelfOrder } from '../../src/lib/t5/store';

describe('shelfOrder — естественный порядок полки', () => {
  test('T5-2 < T5-9 < T5-10 < T5-11 < T5-100 (имена файлов)', () => {
    const names = ['T5-10.md', 'T5-100.md', 'T5-11.md', 'T5-2.md', 'T5-9.md'];
    expect([...names].sort(shelfOrder)).toEqual(['T5-2.md', 'T5-9.md', 'T5-10.md', 'T5-11.md', 'T5-100.md']);
  });

  test('слаги без расширения и с суффиксом R', () => {
    const slugs = ['T5-10', 'T5-2', 'T5-05R', 'T5-05'];
    expect([...slugs].sort(shelfOrder)).toEqual(['T5-2', 'T5-05', 'T5-05R', 'T5-10']);
  });

  test('SO-полка сортируется отдельно от T5', () => {
    expect(shelfOrder('SO-01.md', 'T5-01.md')).not.toBe(0);
  });

  test('не-батчи падают в localeCompare', () => {
    expect(shelfOrder('_BRIEF-TEMPLATE.md', 'T5-01.md')).toBeLessThan(0);
  });
});

describe('batchKey — числовой ключ', () => {
  test('T5-10 → 10, мусор → -1', () => {
    expect(batchKey('T5-10')).toBe(10);
    expect(batchKey('T5-05R')).toBe(5);
    expect(batchKey('не батч')).toBe(-1);
    expect(batchKey(null)).toBe(-1);
  });
});

describe('isSafeSlug — путь не выходит за полку', () => {
  test('легальные слаги', () => {
    expect(isSafeSlug('T5-26')).toBe(true);
    expect(isSafeSlug('SO-10')).toBe(true);
    expect(isSafeSlug('T5-05R')).toBe(true);
  });

  test('обходы каталогов и пустота', () => {
    expect(isSafeSlug('../specs')).toBe(false);
    expect(isSafeSlug('')).toBe(false);
    expect(isSafeSlug('a/b')).toBe(false);
  });
});

describe('resolveT5Root — раскладки контента', () => {
  test('корень репо с batches/ предпочтительнее легаси-вложенности', () => {
    // в чекауте репо batches/ лежит в корне — resolver обязан выбрать его
    const root = resolveT5Root();
    expect(root).toBe(process.cwd());
  });

  test('env T5_ROOT — явное указание сильнее авторазбора', () => {
    const prev = process.env.T5_ROOT;
    process.env.T5_ROOT = '/tmp/t5-content-override';
    try {
      // тикет #1 (платформенная честность): store.ts делает path.resolve(env)
      // — на Windows это C:\tmp\...; ожидание живёт в той же арифметике,
      // а не в POSIX-литерале
      expect(resolveT5Root()).toBe(path.resolve('/tmp/t5-content-override'));
    } finally {
      if (prev === undefined) delete process.env.T5_ROOT;
      else process.env.T5_ROOT = prev;
    }
  });
});

describe('isDeliveredBatch — индекс сдачи (двойной аудит P0-06)', () => {
  test('null-карта = все партии сданы (легаси без индекса)', () => {
    expect(isDeliveredBatch(null, 'T5-27')).toBe(true);
    expect(isDeliveredBatch(null, 'T5-99')).toBe(true);
  });

  test('явный статус решает: delivered проходит, draft/ready/superseded — нет', () => {
    const map = new Map([
      ['T5-27', 'delivered'],
      ['T5-28', 'draft'],
      ['T5-29', 'ready'],
      ['T5-05', 'superseded'],
    ]);
    expect(isDeliveredBatch(map, 'T5-27')).toBe(true);
    expect(isDeliveredBatch(map, 'T5-28')).toBe(false);
    expect(isDeliveredBatch(map, 'T5-29')).toBe(false);
    expect(isDeliveredBatch(map, 'T5-05')).toBe(false);
  });

  test('партия без записи — толерантный дефолт delivered (как в печи t5delivery)', () => {
    const map = new Map([['T5-27', 'delivered']]);
    expect(isDeliveredBatch(map, 'T5-03')).toBe(true);
  });
});
