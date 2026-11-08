import { NextResponse } from 'next/server';
import { needsTriage, readMeta, triageItem, writeMeta } from '@/lib/t5/inbox';

export const runtime = 'nodejs';
export const dynamic = 'force-dynamic';
export const maxDuration = 120;

/** Кап на запрос: короткие запросы не ловят таймаут шлюза; клиент докручивает циклом. */
const CAP_PER_REQUEST = 2;

interface TriageBody {
  ids?: string[];
}

/**
 * POST /api/t5/inbox/triage — X-фильтр-триаж порцией (≤2 файла за запрос).
 *  - без ids: всё, что в очереди (status queued / label unknown);
 *  - с ids: перетриаж указанных (в т.ч. fail-closed карантинов от 429/сбоев).
 * Ответ всегда JSON с remaining — клиент крутит цикл, пока очередь не иссякнет.
 */
export async function POST(req: Request) {
  let body: TriageBody = {};
  try {
    body = (await req.json()) as TriageBody;
  } catch {
    // пустое тело = триаж очереди
  }

  const items = await readMeta();

  const wanted =
    Array.isArray(body.ids) && body.ids.length > 0
      ? items.filter((i) => body.ids?.includes(i.id) && needsTriage(i))
      : items.filter(needsTriage);
  const queue = wanted.slice(0, CAP_PER_REQUEST);

  for (const item of queue) {
    await triageItem(item);
  }
  await writeMeta(items);

  const remaining = items.filter(needsTriage).length;
  return NextResponse.json({ triaged: queue.length, remaining, items });
}
