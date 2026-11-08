import { NextResponse } from 'next/server';
import { analyzeItem, readMeta, writeMeta } from '@/lib/t5/inbox';

export const runtime = 'nodejs';
export const dynamic = 'force-dynamic';
export const maxDuration = 120;

/** Кап на запрос: клиент докручивает циклом по remaining (короткие запросы — без таймаутов). */
const CAP_PER_REQUEST = 3;

interface AnalyzeBody {
  action?: 'analyze' | 'override';
  ids?: string[];
  id?: string;
  label?: 'sfw' | 'x';
}

/**
 * POST /api/t5/inbox/analyze
 *  - {action:'analyze', ids:[...]} — авто-разбор артефактов (некарантина);
 *    ids без элементов = всё, что ждёт разбора.
 *  - {action:'override', id, label:'sfw'|'x'} — вердикт автора поверх триажа.
 */
export async function POST(req: Request) {
  let body: AnalyzeBody;
  try {
    body = (await req.json()) as AnalyzeBody;
  } catch {
    return NextResponse.json({ error: 'ожидаю JSON' }, { status: 400 });
  }

  const items = await readMeta();

  if (body.action === 'override') {
    const item = items.find((i) => i.id === body.id);
    if (!item) return NextResponse.json({ error: 'файл не найден' }, { status: 404 });
    if (body.label !== 'sfw' && body.label !== 'x') {
      return NextResponse.json({ error: 'label: sfw|x' }, { status: 400 });
    }
    item.authorOverride = { label: body.label, at: new Date().toISOString() };
    item.status = body.label === 'x' ? 'x' : item.analysis ? 'analyzed' : 'ok';
    await writeMeta(items);
    return NextResponse.json({ item });
  }

  // action: analyze (по умолчанию)
  const wanted =
    Array.isArray(body.ids) && body.ids.length > 0
      ? items.filter((i) => body.ids?.includes(i.id))
      : items.filter((i) => i.status === 'ok' && !i.analysis);
  const queue = wanted.filter(
    (i) => !(i.authorOverride?.label === 'x' || (i.authorOverride === null && i.triage.label === 'x') || i.triage.label === 'x'),
  );

  if (queue.length === 0) {
    return NextResponse.json({ analyzed: 0, remaining: 0, items });
  }

  const batch = queue.slice(0, CAP_PER_REQUEST);
  // последовательно и бережно: SDK не любит залпы
  for (const item of batch) {
    await analyzeItem(item);
  }
  await writeMeta(items);

  return NextResponse.json({
    analyzed: batch.length,
    remaining: queue.length - batch.length,
    items,
  });
}
