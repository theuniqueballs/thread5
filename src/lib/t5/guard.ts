/**
 * THREAD 5 — опциональная охрана пишущих эндпоинтов (инженерный апгрейд
 * 2026-11-20). Прилавок — личный инструмент автора, по умолчанию пишет
 * свободно (текущее поведение сохранено). Но если задан env T5_WRITE_TOKEN,
 * все POST/DELETE требуют его: заголовок `x-t5-token: <token>` или
 * `Authorization: Bearer <token>`.
 *
 * Это закрывает сценарий «превью-ссылка ушла дальше автора» без смены
 * рабочего процесса: не задан токен — ничего не меняется.
 */
import { NextResponse } from 'next/server';

/** true — доступ разрешён (токен не задан или совпал). */
export function writeAllowed(req: Request): boolean {
  const token = (process.env.T5_WRITE_TOKEN ?? '').trim();
  if (!token) return true; // режим автора: без замка
  const header = req.headers.get('x-t5-token') ?? '';
  if (header && timingSafeEqualStr(header, token)) return true;
  const auth = req.headers.get('authorization') ?? '';
  const bearer = auth.startsWith('Bearer ') ? auth.slice(7).trim() : '';
  return bearer !== '' && timingSafeEqualStr(bearer, token);
}

/** ответ 401 с подсказкой (не раскрывает сам токен). */
export function writeDenied(): NextResponse {
  return NextResponse.json(
    { error: 'Пишущие эндпоинты закрыты: нужен заголовок x-t5-token (T5_WRITE_TOKEN)' },
    { status: 401 },
  );
}

/** сравнение строк без утечки времени (best-effort в рантайме edge/node). */
function timingSafeEqualStr(a: string, b: string): boolean {
  if (a.length !== b.length) return false;
  let diff = 0;
  for (let i = 0; i < a.length; i++) diff |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return diff === 0;
}
