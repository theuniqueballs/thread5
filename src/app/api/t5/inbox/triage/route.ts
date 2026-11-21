import { NextResponse } from 'next/server';
import {
  applyTriage,
  needsTriage,
  readMeta,
  triageItem,
  withMetaLock,
  writeMeta,
} from '@/lib/t5/inbox';
import { writeAllowed, writeDenied } from '@/lib/t5/guard';

export const runtime = 'nodejs';
export const dynamic = 'force-dynamic';
export const maxDuration = 60;

/**
 * Кап на запрос: ОДИН файл (2026-11-21, вторая итерация фикса 502: «по две»
 * всё ещё ловили Bad Gateway — лестница ретраев под мета-замком растягивала
 * запрос за таймаут шлюза). Один vision-звонок = короткий запрос; клиент
 * докручивает циклом по remaining.
 */
const CAP_PER_REQUEST = 1;

interface TriageBody {
  ids?: string[];
}

/**
 * POST /api/t5/inbox/triage — X-фильтр-триаж порцией (1 файл за запрос).
 *  - без ids: всё, что в очереди (status queued / label unknown);
 *  - с ids: перетриаж указанных (в т.ч. fail-closed карантинов от 429/сбоев).
 *
 * Структура «vision ВНЕ мета-замка» (урок 502 от T5-28): длинный LLM-звонок
 * не держит журнал и не растягивает чужие запроси, ждущие замка. Гонка двух
 * параллельных запросов безвредна: худший случай — один лишний vision-звонок,
 * результат вклеивается по id идемпотентно.
 * Ответ всегда JSON с remaining — клиент крутит цикл, пока очередь не иссякнет.
 */
export async function POST(req: Request) {
  if (!writeAllowed(req)) return writeDenied();
  let body: TriageBody = {};
  try {
    body = (await req.json()) as TriageBody;
  } catch {
    // пустое тело = триаж очереди
  }

  // 1) выбор жертв: чтение журнала атомарно (tmp→rename), замок не нужен
  const items = await readMeta();
  const wanted =
    Array.isArray(body.ids) && body.ids.length > 0
      ? items.filter((i) => body.ids?.includes(i.id)) // ручной выбор автора — всегда можно (в т.ч. вердикты фильтра 1301)
      : items.filter(needsTriage);
  const queue = wanted.slice(0, CAP_PER_REQUEST);

  // 2) vision-звонки БЕЗ замка
  for (const item of queue) {
    await triageItem(item);
  }

  // 3) слияние под замком: перечитали свежий журнал, вклеили по id
  const result = await withMetaLock(async () => {
    const fresh = await readMeta();
    for (const done of queue) {
      const target = fresh.find((i) => i.id === done.id);
      if (target) applyTriage(target, done);
    }
    await writeMeta(fresh);
    const remaining = fresh.filter(needsTriage).length;
    return { triaged: queue.length, remaining, items: fresh };
  });
  return NextResponse.json(result);
}
