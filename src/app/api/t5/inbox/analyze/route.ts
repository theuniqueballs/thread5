import { NextResponse } from 'next/server';
import { analyzeItem, readMeta, withMetaLock, writeMeta } from '@/lib/t5/inbox';
import { writeAllowed, writeDenied } from '@/lib/t5/guard';

export const runtime = 'nodejs';
export const dynamic = 'force-dynamic';
export const maxDuration = 120;

/** Кап на запрос: клиент докручивает циклом по remaining (короткие запросы — без таймаутов).
 *  2026-11-21: 3 → 2 (приказ автора «по две штуки, чтобы не перегружать») —
 *  разбор теперь тяжелее: дефекты + рейтинг по Коу + слот зрением в одном звонке. */
const CAP_PER_REQUEST = 2;

interface AnalyzeBody {
  action?: 'analyze' | 'override';
  ids?: string[];
  id?: string;
  label?: 'sfw' | 'x';
  /** Батч, выбранный в UI — фолбэй для файлов без тега (слот зрением). */
  batch?: string;
}

/**
 * POST /api/t5/inbox/analyze
 *  - {action:'analyze', ids:[...]} — авто-разбор артефактов (некарантина);
 *    ids без элементов = всё, что ждёт разбора.
 *  - {action:'override', id, label:'sfw'|'x'} — вердикт автора поверх триажа.
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

  // action: analyze (по умолчанию) — тоже под замком: цикл клиента и
  // параллельный override не должны перезаписывать журнал друг друга
  const batchHint = typeof body.batch === 'string' && body.batch.trim() ? body.batch.trim().slice(0, 8) : null;
  const result = await withMetaLock(async () => {
    const items = await readMeta();
    const wanted =
      Array.isArray(body.ids) && body.ids.length > 0
        ? items.filter((i) => body.ids?.includes(i.id))
        : items.filter((i) => i.status === 'ok' && !i.analysis);
    const queue = wanted.filter(
      (i) => !(i.authorOverride?.label === 'x' || (i.authorOverride === null && i.triage.label === 'x') || i.triage.label === 'x'),
    );

    if (queue.length === 0) {
      return { analyzed: 0, remaining: 0, items };
    }

    const batch = queue.slice(0, CAP_PER_REQUEST);
    // последовательно и бережно: SDK не любит залпы
    for (const item of batch) {
      await analyzeItem(item, batchHint);
    }
    await writeMeta(items);

    return {
      analyzed: batch.length,
      remaining: queue.length - batch.length,
      items,
    };
  });
  return NextResponse.json(result);
}
