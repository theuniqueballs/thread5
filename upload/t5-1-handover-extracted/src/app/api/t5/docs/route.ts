import { NextResponse } from 'next/server';
import { readDoc } from '@/lib/t5/store';

const CACHE_CONTROL = 'public, max-age=5, stale-while-revalidate=30';

export async function GET(req: Request) {
  const url = new URL(req.url);
  const name = url.searchParams.get('name') ?? '';
  const content = await readDoc(name);
  if (content === null) {
    return NextResponse.json({ error: 'Документ не найден', name }, { status: 404 });
  }
  return NextResponse.json({ name, content }, { headers: { 'Cache-Control': CACHE_CONTROL } });
}
