/**
 * ORACLE CLIENT — прилавок ↔ oracle-service (:3031).
 *
 * Правило выживания: сервис — УСИЛИТЕЛЬ, не единственная точка правды.
 * Прилавок всегда работает на локальном движке (oracle-engine.ts); сервис
 * добавляет LLM-мозг (/ask), зрение (/vision) и полный аудит. Сервис лежит
 * или не поднят — прилавок не ломается, просто показывает «локальный режим».
 *
 * Все запросы с таймаутом и AbortController: зависший сервис не вешает
 * вкладку. ORACLE_URL — env (по умолчанию http://127.0.0.1:3031, как
 * ORACLE_HOST/PORT сервиса).
 */

export const ORACLE_URL_DEFAULT = 'http://127.0.0.1:3031';

export function oracleUrl(): string {
  const env = process.env.ORACLE_URL?.trim();
  return env || ORACLE_URL_DEFAULT;
}

export interface OracleServiceStatus {
  reachable: boolean;
  url: string;
  /** ответ /health сервиса (если доехал) */
  health: {
    ok?: boolean;
    service?: string;
    port?: number;
    layers?: string[];
    era?: string;
    camera_registry?: string;
    cards_indexed?: number;
  } | null;
  /** чем отвечает прилавок, когда сервиса нет */
  mode: 'service+local' | 'local';
  checkedAt: string;
  error?: string;
}

async function oracleFetch<T>(path: string, init: RequestInit = {}, timeoutMs = 2500): Promise<T | null> {
  const ctrl = new AbortController();
  const timer = setTimeout(() => ctrl.abort(), timeoutMs);
  try {
    const res = await fetch(`${oracleUrl()}${path}`, { ...init, signal: ctrl.signal, cache: 'no-store' });
    if (!res.ok) return null;
    return (await res.json()) as T;
  } catch {
    return null; // сервис лежит/не поднят/таймаут — молча деградируем
  } finally {
    clearTimeout(timer);
  }
}

/** кэш статуса на 15 с: пинговать сервис на каждый рендер незачем */
let statusCache: { at: number; value: OracleServiceStatus } | null = null;

export async function oracleStatus(force = false): Promise<OracleServiceStatus> {
  if (!force && statusCache && Date.now() - statusCache.at < 15_000) return statusCache.value;
  const health = await oracleFetch<OracleServiceStatus['health']>('/health', {}, 1500);
  const value: OracleServiceStatus = health
    ? { reachable: true, url: oracleUrl(), health, mode: 'service+local', checkedAt: new Date().toISOString() }
    : { reachable: false, url: oracleUrl(), health: null, mode: 'local', checkedAt: new Date().toISOString(), error: 'сервис не отвечает (не поднят?) — прилавок на локальном движке' };
  statusCache = { at: Date.now(), value };
  return value;
}

/* Мёртвый путь убран (чистка 2026-11-21): клиенты /audit, /batch, /ask жили
 * здесь без единого вызова из прилавка — агрегированный аудит и вопросы
 * LLM-мозгу ходят через CLI (tools/oracle.py audit|ask) напрямую в сервис.
 * Сервисные эндпоинты живы; прилавку они не нужны (усилитель, не замена). */
