import { promises as fs } from 'node:fs';
import { NextResponse } from 'next/server';
import { readMeta, resolvePreviewPath, resolveUploadPath } from '@/lib/t5/inbox';

export const runtime = 'nodejs';
export const dynamic = 'force-dynamic';

/**
 * GET /api/t5/inbox/file?id=... — отдача изображения из инбокса.
 * &preview=1 — облегчённая копия (для сетки карточек и чтения писцом),
 * отсутствует/не сгенерировалось — отдаём оригинал.
 */
export async function GET(req: Request) {
  const params = new URL(req.url).searchParams;
  const id = params.get('id') ?? '';
  const wantPreview = params.get('preview') === '1';
  if (!/^[a-f0-9]{6,32}$/u.test(id)) {
    return NextResponse.json({ error: 'битый id' }, { status: 400 });
  }
  const items = await readMeta();
  const item = items.find((i) => i.id === id);
  if (!item) return NextResponse.json({ error: 'не найден' }, { status: 404 });

  const previewPath = wantPreview && item.preview ? resolvePreviewPath(item.preview) : null;
  const p = previewPath ?? resolveUploadPath(item.file);
  if (!p) return NextResponse.json({ error: 'путь отклонён' }, { status: 400 });
  try {
    const buf = await fs.readFile(p);
    const headers: Record<string, string> = {
      'Cache-Control': 'private, max-age=3600',
    };
    if (previewPath) headers['Content-Type'] = 'image/webp';
    else headers['Content-Type'] = item.mime;
    return new NextResponse(new Uint8Array(buf), { headers });
  } catch {
    return NextResponse.json({ error: 'файл потерян' }, { status: 410 });
  }
}
