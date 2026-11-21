import { NextResponse } from 'next/server';
import {
  applyAnalyzed,
  analyzeItem,
  readMeta,
  withMetaLock,
  writeMeta,
} from '@/lib/t5/inbox';
import { writeAllowed, writeDenied } from '@/lib/t5/guard';

export const runtime = 'nodejs';
export const dynamic = 'force-dynamic';
export const maxDuration = 60;

/**
 * Кап на запрос: ОДИН файл (2026-11-21, вторая итерация фикса 502). Разбор
 * тяжелее триажа — дефекты + факт-рейтинг по Коу + слот зрением в одном
 * звонке; два таких под мета-замком ловили Bad Gateway шлюза.
 */
const CAP_PER_REQUEST = 1;

interface AnalyzeBody {
  action?: 'analyze' | 'override';
  ids?: string[];
  id?: string;
  label?: 'sfw' | 'x';
  /** Батч, выбранный в UI — фолбэк для файлов без тега (слот зрением). */
  batch?: string;
}

/**
 * POST /api/t5/inbox/analyze
 *  - {action:'analyze', ids:[...]} — авто-разбор артефактов (некарантина);
 *    ids без элементов = всё, что ждёт разбора.
 *  - {action:'override', id, label:'sfw'|'x'} — вердикт автора поверх триажа.
 *
 * Разбор (action:'analyze') идёт по схеме «vision ВНЕ мета-замка» (урок 502
 * от T5-28): выбор жертв → звонки без замка → слияние под замком по id.
 * Вердикт автора, вынесенный за время звонка, сильнее — applyAnalyzed
 * считает статус от него.
 */
export async function POST(req: Request) {
  if (!writeAllowed(req)) return writeDenied();
  let body: AnalyzeBody;
  try {
    body = (await req.json()) as AnalyzeBody;
  } catch {
    return NextResponse.json({ error: 'ожидаю JSON' }, { status: 400 });
  }

  if (body.action === 'override') {
    const result = await withMetaLock(async () => {
      const items = await readMeta();
      const item = items.find((i) => i.id === body.id);
      if (!item) return { error: 'файл не найден', status: 404 as const };
      if (body.label !== 'sfw' && body.label !== 'x') {
        return { error: 'label: sfw|x', status: 400 as const };
      }
      item.authorOverride = { label: body.label, at: new Date().toISOString() };
      item.status = body.label === 'x' ? 'x' : item.analysis ? 'analyzed' : 'ok';
      await writeMeta(items);
      return { item, status: 200 as const };
    });
    if ('error' in result && result.error) {
      return NextResponse.json({ error: result.error }, { status: result.status });
    }
    return NextResponse.json({ item: result.item });
  }

  // action: analyze (по умолчанию)
  const batchHint = typeof body.batch === 'string' && body.batch.trim() ? body.batch.trim().slice(0, 8) : null;
  const idsGiven = Array.isArray(body.ids) && body.ids.length > 0;

  // 1) выбор жертв: журнал атомарный, замок не нужен
  const items = await readMeta();
  const wanted = idsGiven
    ? items.filter((i) => body.ids?.includes(i.id))
    : items.filter((i) => i.status === 'ok' && !i.analysis);
  // не разбираем ЭФФЕКТИВНЫЙ карантин: вердикт автора «x» ИЛИ триаж X без
        // разблокировки — оба бьют. НО sfw-оверрайд автора над X-триажем снимает
  // карантин (живой случай T5-28: 2 файла с 401-карантином разблокированы
  // автором в 12:23 — effectiveLabel уже знает про это, фильтр отставал)
  const queue = wanted.filter((i) => effectiveLabel(i) !== 'x');

  if (queue.length === 0) {
    return NextResponse.json({ analyzed: 0, remaining: 0, items });
  }

  // 2) vision-звонки ВНЕ замка: последовательно и бережно, SDK не любит залпы
  const batch = queue.slice(0, CAP_PER_REQUEST);
  for (const item of batch) {
    await analyzeItem(item, batchHint);
  }

  // 3) слияние под замком по id
  const result = await withMetaLock(async () => {
    const fresh = await readMeta();
    for (const done of batch) {
      const target = fresh.find((i) => i.id === done.id);
      if (target) applyAnalyzed(target, done);
    }
    await writeMeta(fresh);
    // remaining: явные ids — в рамках запроса (клиент перезапускает их
    // тем же списком, «Переразобрать» — одиночный id → remaining 0 → стоп);
    // без ids — вся живая очередь разбора
    const remaining = idsGiven
      ? Math.max(0, queue.length - batch.length)
      : fresh.filter(
        (i) => i.status === 'ok' && !i.analysis && !(i.authorOverride?.label === 'x' || i.triage.label === 'x'),
      ).length;
    return { analyzed: batch.length, remaining, items: fresh };
  });
  return NextResponse.json(result);
}
