import { NextResponse } from 'next/server';
import { rateTextLite, ENGINE_ERA } from '@/lib/t5/oracle-engine';
import { oracleUrl } from '@/lib/t5/oracle-client';

const MAX_TEXT = 20_000; // паритет с лимитом /audit сервиса

/**
 * Экспресс-оценка текста: POST /api/t5/oracle/rate { text }.
 * Локальный движок (без сервиса) — мгновенно и бесплатно. Если поднят
 * oracle-service, поле service.verdict доносит полный вердикт (те же словари
 * + x_risk_drivers + WARN-флоры); упал сервис — отвечаем только локально.
 */
export async function POST(req: Request) {
  let text = '';
  try {
    const body = (await req.json()) as { text?: unknown };
    text = typeof body.text === 'string' ? body.text : '';
  } catch {
    return NextResponse.json({ error: 'Нужен JSON: { "text": "…" }' }, { status: 400 });
  }
  if (!text.trim()) {
    return NextResponse.json({ error: 'text required — оценим POS/NEG/описание кадра' }, { status: 400 });
  }
  if (text.length > MAX_TEXT) {
    return NextResponse.json({ error: `text слишком большой (лимит ${MAX_TEXT} символов)` }, { status: 413 });
  }

  const lite = rateTextLite(text);

  // обогащение полным движком сервиса (не критично: 1.5 с таймаут)
  let service: { url: string; verdict: Record<string, unknown> | null } | null = null;
  try {
    const ctrl = new AbortController();
    const timer = setTimeout(() => ctrl.abort(), 1500);
    const res = await fetch(`${oracleUrl()}/rate`, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ text }),
      signal: ctrl.signal,
      cache: 'no-store',
    });
    clearTimeout(timer);
    service = { url: oracleUrl(), verdict: res.ok ? await res.json() : null };
  } catch {
    service = { url: oracleUrl(), verdict: null };
  }

  return NextResponse.json({ lite, service, engine: ENGINE_ERA });
}
