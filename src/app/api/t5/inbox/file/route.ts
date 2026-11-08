import { promises as fs } from 'node:fs';
import { NextResponse } from 'next/server';
import { readMeta, resolveUploadPath } from '@/lib/t5/inbox';

export const runtime = 'nodejs';
export const dynamic = 'force-dynamic';

/** GET /api/t5/inbox/file?id=... — отдача изображения из инбокса. */
export async function GET(req: Request) {
  const id = new URL(req.url).searchParams.get('id') ?? '';
  if (!/^[a-f0-9]{6,32}$/u.test(id)) {
    return NextResponse.json({ error: 'битый id' }, { status: 400 });
  }
  const items = await readMeta();
  const item = items.find((i) => i.id === id);
  if (!item) return NextResponse.json({ error: 'не найден' }, { status: 404 });

  const p = resolveUploadPath(item.file);
  if (!p) return NextResponse.json({ error: 'путь отклонён' }, { status: 400 });
  try {
    const buf = await fs.readFile(p);
    return new NextResponse(new Uint8Array(buf), {
      headers: {
        'Content-Type': item.mime,
        'Cache-Control': 'private, max-age=3600',
      },
    });
  } catch {
    return NextResponse.json({ error: 'файл потерян' }, { status: 410 });
  }
}
