import { NextResponse } from 'next/server';
import {
  MAX_BATCH_FILES,
  readMeta,
  saveFile,
  writeMeta,
} from '@/lib/t5/inbox';

export const runtime = 'nodejs';
export const dynamic = 'force-dynamic';
export const maxDuration = 60;

/** GET /api/t5/inbox — журнал инбокса (без содержимого файлов). */
export async function GET() {
  try {
    const items = await readMeta();
    return NextResponse.json({ items });
  } catch (err) {
    return NextResponse.json({ error: String(err instanceof Error ? err.message : err) }, { status: 500 });
  }
}

/**
 * POST /api/t5/inbox — bulk-загрузка кучкой (FormData: files[], tag?).
 * ТОЛЬКО диск + мета (status queued): vision-триаж вынесен в /triage,
 * иначе долгий запрос ловит HTML-таймаут шлюза вместо JSON.
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

  const rawTag = form.get('tag');
  const tag = typeof rawTag === 'string' && rawTag.trim().length > 0 ? rawTag.trim().slice(0, 40) : null;

  const items = await readMeta();
  const results: { origName: string; id?: string; status?: string; error?: string }[] = [];
  const saved = [];

  for (const file of files) {
    const out = await saveFile(file, tag);
    if (out.item) {
      saved.push(out.item);
      results.push({ origName: out.origName, id: out.item.id, status: out.item.status });
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
    items,
  });
}
