import { NextResponse } from 'next/server';
import {
  MAX_BATCH_FILES,
  deleteAll,
  deleteItems,
  readMeta,
  saveFile,
  sortItems,
  writeMeta,
} from '@/lib/t5/inbox';

export const runtime = 'nodejs';
export const dynamic = 'force-dynamic';
export const maxDuration = 60;

/** GET /api/t5/inbox — журнал инбокса (без содержимого файлов), батч ↓ слот ↑. */
export async function GET() {
  try {
    const items = sortItems(await readMeta());
    return NextResponse.json({ items });
  } catch (err) {
    return NextResponse.json({ error: String(err instanceof Error ? err.message : err) }, { status: 500 });
  }
}

/**
 * POST /api/t5/inbox — bulk-загрузка кучкой (FormData: files[], tags?[], tag?).
 * ТОЛЬКО диск + мета (status queued): vision-триаж вынесен в /triage,
 * иначе долгий запрос ловит HTML-таймаут шлюза вместо JSON.
 *
 * tags — JSON-массив пофайловых меток, параллельный files[] («T5-18 P07»).
 * Если метки нет — слот вытаскивается из имени файла (P07 / 07 - name.webp).
 */
export async function POST(req: Request) {
  let form: FormData;
  try {
    form = await req.formData();
  } catch {
    return NextResponse.json({ error: 'ожидаю multipart/form-data' }, { status: 400 });
  }

  const files = form.getAll('files').filter((f): f is File => f instanceof File);
  if (files.length === 0) return NextResponse.json({ error: 'файлов нет' }, { status: 400 });
  if (files.length > MAX_BATCH_FILES) {
    return NextResponse.json({ error: `максимум ${MAX_BATCH_FILES} файлов за раз` }, { status: 400 });
  }

  let perFileTags: string[] = [];
  try {
    const rawTags = form.get('tags');
    if (typeof rawTags === 'string' && rawTags.trim()) {
      const parsed: unknown = JSON.parse(rawTags);
      if (Array.isArray(parsed)) perFileTags = parsed.map((t) => (typeof t === 'string' ? t : ''));
    }
  } catch {
    perFileTags = [];
  }
  const fallbackTag = form.get('tag');
  const fallback = typeof fallbackTag === 'string' && fallbackTag.trim() ? fallbackTag.trim().slice(0, 40) : null;

  const items = await readMeta();
  const results: { origName: string; id?: string; tag?: string | null; status?: string; error?: string }[] = [];
  const saved = [];

  for (let i = 0; i < files.length; i++) {
    const tag = (perFileTags[i] ?? '').trim() || fallback;
    const out = await saveFile(files[i], tag);
    if (out.item) {
      saved.push(out.item);
      results.push({ origName: out.origName, id: out.item.id, tag: out.item.tag, status: out.item.status });
    } else {
      results.push({ origName: out.origName, error: out.error ?? 'не сохранён' });
    }
  }

  if (saved.length > 0) {
    items.unshift(...saved);
    await writeMeta(items);
  }

  return NextResponse.json({
    uploaded: saved.length,
    failed: results.filter((r) => r.error).length,
    queued: saved.length,
    results,
    items: sortItems(items),
  });
}

/**
 * DELETE /api/t5/inbox — очистка после разбора (чтобы диск не пух).
 *  - ?all=1        — снести всё (файлы + превью + журнал);
 *  - ?ids=a,b,c    — убрать перечисленные;
 *  - ?status=...   — убрать всё с перечисленными статусами (analyzed,x,error).
 */
export async function DELETE(req: Request) {
  const url = new URL(req.url);
  try {
    if (url.searchParams.get('all') === '1') {
      const report = await deleteAll();
      return NextResponse.json({ ...report, items: [] });
    }
    const idsParam = url.searchParams.get('ids');
    const statusParam = url.searchParams.get('status');
    let ids: string[] = [];
    if (idsParam) {
      ids = idsParam.split(',').map((s) => s.trim()).filter((s) => /^[a-f0-9]{6,32}$/u.test(s));
    } else if (statusParam) {
      const statuses = new Set(statusParam.split(',').map((s) => s.trim()).filter(Boolean));
      ids = (await readMeta()).filter((i) => statuses.has(i.status)).map((i) => i.id);
    }
    if (ids.length === 0) {
      return NextResponse.json({ error: 'укажи ids=, status= или all=1' }, { status: 400 });
    }
    const report = await deleteItems(ids);
    return NextResponse.json({ ...report, items: sortItems(await readMeta()) });
  } catch (err) {
    return NextResponse.json({ error: String(err instanceof Error ? err.message : err) }, { status: 500 });
  }
}
