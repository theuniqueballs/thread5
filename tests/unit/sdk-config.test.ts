/**
 * Юнит-тесты sdk-config (bun test) — урок 2026-11-24 про 401 «missing
 * X-Token»: SDK берёт ПЕРВЫЙ конфиг с baseUrl && apiKey, даже если token
 * пуст, и шлюз карантинит пачку. Модуль обязан ставить диагноз ДО
 * vision-звонка, искать конфиг в том же порядке, что SDK, и не выносить
 * секреты наружу.
 */
import { afterEach, beforeEach, describe, expect, test } from 'bun:test';
import { promises as fs } from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { SdkConfigError, assertSdkVisionReady, readSdkConfigState } from '../../src/lib/t5/sdk-config';

const SECRET_TOKEN = 'super-secret-token-value-XYZ-НЕ-НАРУЖУ';

let tmpDir: string;
const prevCwd = process.cwd();

beforeEach(async () => {
  tmpDir = await fs.mkdtemp(path.join(os.tmpdir(), 't5-sdk-config-'));
  process.chdir(tmpDir);
});

afterEach(async () => {
  process.chdir(prevCwd);
  await fs.rm(tmpDir, { recursive: true, force: true });
});

function writeConfig(body: Record<string, unknown>): Promise<string> {
  const file = path.join(process.cwd(), '.z-ai-config');
  return fs.writeFile(file, JSON.stringify(body), 'utf8');
}

describe('readSdkConfigState — тот же порядок/правила, что у SDK', () => {
  test('полный конфиг в cwd → ok, файл-победитель = cwd (до /etc очередь не доходит)', async () => {
    await writeConfig({ baseUrl: 'https://x', apiKey: 'k', token: SECRET_TOKEN });
    const st = await readSdkConfigState();
    expect(st.found).toBe(true);
    expect(st.hasToken).toBe(true);
    expect(st.ok).toBe(true);
    expect(st.problem).toBeNull();
    expect(st.file).toBe(path.join(process.cwd(), '.z-ai-config'));
  });

  test('конфиг в cwd БЕЗ token → ок:false, диагноз с путём (урок 401 missing X-Token)', async () => {
    await writeConfig({ baseUrl: 'https://x', apiKey: 'k' });
    const st = await readSdkConfigState();
    expect(st.found).toBe(true);
    expect(st.hasToken).toBe(false);
    expect(st.ok).toBe(false);
    expect(st.problem).toContain('token');
    expect(st.problem).toContain(path.join(process.cwd(), '.z-ai-config'));
  });

  test('файл без apiKey SDK конфигом НЕ считает (правило baseUrl && apiKey) — не он победитель', async () => {
    await writeConfig({ baseUrl: 'https://x' });
    const st = await readSdkConfigState();
    expect(st.file).not.toBe(path.join(process.cwd(), '.z-ai-config'));
    // дальше по списку SDK нашёл бы другой конфиг или вернул бы found:false
    if (st.found) expect(st.file).not.toBeNull();
  });

  test('конфигов нет вообще → found:false, внятный диагноз с порядком поиска', async () => {
    // cwd пуст (tmp); чтобы тест не зависел от /etc и home — проверяем
    // только ЧТО диагноз перечисляет порядок поиска, когда победителя нет
    const st = await readSdkConfigState();
    if (!st.found) {
      expect(st.ok).toBe(false);
      expect(st.problem).toContain('/etc/.z-ai-config');
    } else {
      expect(st.file).not.toBe(path.join(process.cwd(), '.z-ai-config'));
    }
  });
});

describe('readSdkConfigState — секреты наружу не текут', () => {
  test('ни problem, ни весь стейт не содержат значения token', async () => {
    await writeConfig({ baseUrl: 'https://x', apiKey: 'k', token: SECRET_TOKEN });
    const st = await readSdkConfigState();
    expect(JSON.stringify(st)).not.toContain('XYZ');
    const broken = await (async () => {
      await writeConfig({ baseUrl: 'https://x', apiKey: 'k', token: SECRET_TOKEN, note: 'x' });
      const s = await readSdkConfigState();
      return JSON.stringify(s);
    })();
    expect(broken).not.toContain('XYZ');
  });
});

describe('SdkConfigError / assertSdkVisionReady — быстрый падеж до vision-звонка', () => {
  test('конфиг без token → SdkConfigError с диагнозом; полный конфиг → гвард молчит', async () => {
    await writeConfig({ baseUrl: 'https://x', apiKey: 'k' });
    let caught: unknown = null;
    try {
      await assertSdkVisionReady();
    } catch (err) {
      caught = err;
    }
    expect(caught).toBeInstanceOf(SdkConfigError);
    expect(caught instanceof Error && caught.message.includes('token')).toBe(true);

    await writeConfig({ baseUrl: 'https://x', apiKey: 'k', token: SECRET_TOKEN });
    await assertSdkVisionReady(); // не бросает
  });

  test('SdkConfigError — это Error с именем класса (триаж отличает от сетевых сбоев)', () => {
    const err = new SdkConfigError('диагноз');
    expect(err instanceof Error).toBe(true);
    expect(err.name).toBe('SdkConfigError');
    expect(err.message).toBe('диагноз');
  });
});
