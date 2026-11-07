import { NextResponse } from 'next/server';
import { listBatches } from '@/lib/t5/store';

const CACHE_CONTROL = 'public, max-age=5, stale-while-revalidate=30';

export async function GET() {
  try {
    const items = await listBatches();
    return NextResponse.json({ batches: items }, { headers: { 'Cache-Control': CACHE_CONTROL } });
  } catch (err) {
    return NextResponse.json({ error: 'Не удалось прочитать батчи', detail: String(err) }, { status: 500 });
  }
}
