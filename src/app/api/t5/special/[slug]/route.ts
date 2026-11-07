import { NextResponse } from 'next/server';
import { readSpecial } from '@/lib/t5/store';
import type { T5Batch } from '@/lib/t5/parse';

const CACHE_CONTROL = 'public, max-age=5, stale-while-revalidate=30';

/** raw (полный текст) возим только по требованию ?raw=1 — он дублирует слоты */
function withoutRaw(batch: T5Batch): Omit<T5Batch, 'raw'> {
  const { raw, ...body } = batch;
  void raw;
  return body;
}

export async function GET(req: Request, { params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const order = await readSpecial(slug);
  if (!order) {
    return NextResponse.json({ error: 'Заказ не найден', slug }, { status: 404 });
  }
  const headers = { 'Cache-Control': CACHE_CONTROL };
  const includeRaw = new URL(req.url).searchParams.get('raw') === '1';
  return NextResponse.json({ batch: includeRaw ? order : withoutRaw(order) }, { headers });
}
