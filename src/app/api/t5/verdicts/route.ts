import { NextResponse } from 'next/server';
import { listVerdicts, saveVerdict } from '@/lib/t5/store';

const CACHE_CONTROL = 'public, max-age=5, stale-while-revalidate=30';

export async function GET(req: Request) {
  const url = new URL(req.url);
  const slug = url.searchParams.get('slug') ?? undefined;
  try {
    const verdicts = await listVerdicts(slug || undefined);
    return NextResponse.json({ verdicts }, { headers: { 'Cache-Control': CACHE_CONTROL } });
  } catch (err) {
    return NextResponse.json({ error: 'Не удалось прочитать вердикты', detail: String(err) }, { status: 500 });
  }
}

export async function POST(req: Request) {
  let body: unknown;
  try {
    body = await req.json();
  } catch {
    return NextResponse.json({ error: 'Ожидался JSON' }, { status: 400 });
  }
  const { slug, text } = (body ?? {}) as { slug?: string; text?: string };
  if (typeof slug !== 'string' || slug.length === 0) {
    return NextResponse.json({ error: 'Нужен slug батча' }, { status: 400 });
  }
  if (typeof text !== 'string' || text.trim().length < 2) {
    return NextResponse.json({ error: 'Вердикт пустой' }, { status: 400 });
  }
  try {
    const saved = await saveVerdict(slug, text.slice(0, 20000));
    return NextResponse.json({ verdict: saved }, { status: 201 });
  } catch (err) {
    return NextResponse.json({ error: 'Не удалось сохранить вердикт', detail: String(err) }, { status: 500 });
  }
}
