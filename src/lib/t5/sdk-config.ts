/**
 * THREAD 5 — само-проверка SDK-конфига перед vision-звонками.
 *
 * Живой урок (2026-11-24, повторение T5-19): триаж падал пачкой с
 * «API request failed with status 401: {"error":"missing X-Token header"}»
 * и по fail-closed карантинил весь инбокс. Корень: z-ai-web-dev-sdk берёт
 * ПЕРВЫЙ файл конфига, у которого есть baseUrl && apiKey (cwd → home →
 * /etc/.z-ai-config), даже если поля token в нём НЕТ — запрос уходит без
 * заголовка X-Token, шлюз отвечает 401. Ретраи тут бессмысленны: конфиг
 * не станет другим за 4 секунды.
 *
 * Модуль делает ровно то, что SDK, но с отчётом ПОЧЕМУ конфиг не готов,
 * и отдаёт triageImage/analyzeItem быстрый падеж СКВОЗНОЙ ошибкой
 * (SdkConfigError) до первого vision-звонка. Причина карантина матчит
 * RETRIAGE_RE («карантин») — после починки конфига «Перетриажнуть
 * карантин» пересматривает всё одним нажатием, очередь не теряется.
 *
 * СЕКРЕТЫ: наружу отдаётся только наличие полей (boolean) и путь к файлу —
 * ни значений token/apiKey, ни кусков конфига.
 */
import { promises as fs } from 'node:fs';
import os from 'node:os';
import path from 'node:path';

export interface SdkConfigState {
  /** Конфиг, который SDK реально возьмёт (первый валидный baseUrl+apiKey). */
  found: boolean;
  /** Путь файла-победителя (без содержимого). */
  file: string | null;
  /** Поле token заполнено — иначе шлюз ответит 401 missing X-Token. */
  hasToken: boolean;
  /** ok = found && hasToken: vision-звонки имеют смысл. */
  ok: boolean;
  /** Человекочитаемая причина неготовности (null — всё хорошо). */
  problem: string | null;
}

async function readConfigFile(file: string): Promise<Record<string, unknown> | null> {
  try {
    const parsed: unknown = JSON.parse(await fs.readFile(file, 'utf8'));
    return parsed && typeof parsed === 'object' && !Array.isArray(parsed)
      ? (parsed as Record<string, unknown>)
      : null;
  } catch {
    return null; // нет файла / битый JSON — SDK молча пойдёт дальше по списку
  }
}

function nonEmptyString(v: unknown): boolean {
  return typeof v === 'string' && v.length > 0;
}

/**
 * Тот же порядок поиска и то же правило «первый файл с baseUrl && apiKey
 * выигрывает», что у SDK (loadConfig в z-ai-web-dev-sdk) — но вместо
 * падежа с туманным «Configuration file not found or invalid» возвращает
 * диагноз. Читается на каждый вызов: починил конфиг — следующий триаж
 * уже живой, кэша-зомби нет.
 */
export async function readSdkConfigState(): Promise<SdkConfigState> {
  const candidates = [
    path.join(process.cwd(), '.z-ai-config'),
    path.join(os.homedir(), '.z-ai-config'),
    '/etc/.z-ai-config',
  ];
  for (const file of candidates) {
    const cfg = await readConfigFile(file);
    if (!cfg) continue;
    // правило SDK: файл конфигом считается только с baseUrl && apiKey
    if (!nonEmptyString(cfg.baseUrl) || !nonEmptyString(cfg.apiKey)) continue;
    const hasToken = nonEmptyString(cfg.token);
    return {
      found: true,
      file,
      hasToken,
      ok: hasToken,
      problem: hasToken
        ? null
        : `файл ${file} выиграл поиск, но без поля token — SDK шлёт запросы без заголовка X-Token и шлюз отвечает 401. Добавь token в этот файл (или убери его, чтобы SDK взял следующий по списку, где token есть)`,
    };
  }
  return {
    found: false,
    file: null,
    hasToken: false,
    ok: false,
    problem:
      'конфиг SDK не найден (порядок поиска: ./.z-ai-config → ~/.z-ai-config → /etc/.z-ai-config; нужен baseUrl + apiKey + token) — vision-звонки триажа/разбора невозможны',
  };
}

/**
 * Сквозная ошибка конфига: triageImage/analyzeItem отличают её от сетевых
 * сбоев (это НЕ 429 и не мимолётный 502 — ретраи не нужны) и пишут в
 * карантин причину, которую RETRIAGE_RE потом лечит. visionJsonRetry
 * ре-троит её мгновенно, без лестницы пауз.
 */
export class SdkConfigError extends Error {
  constructor(problem: string) {
    super(problem);
    this.name = 'SdkConfigError';
  }
}

/** Гвард перед vision-звонком: конфиг без token → быстрый падеж с внятной
 *  причиной вместо 401-шторма на всю пачку. */
export async function assertSdkVisionReady(): Promise<void> {
  const state = await readSdkConfigState();
  if (!state.ok) throw new SdkConfigError(state.problem ?? 'SDK-конфиг не готов к vision-звонкам');
}
