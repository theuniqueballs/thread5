import { NextResponse } from 'next/server';
import { listSpecial } from '@/lib/t5/store';

const CACHE_CONTROL = 'public, max-age=5, stale-while-revalidate=30';

export async function GET() {
  try {
    const items = await listSpecial();
    return NextResponse.json({ special: items }, { headers: { 'Cache-Control': CACHE_CONTROL } });
  } catch (err) {
    return NextResponse.json({ error: 'Не удалось прочитать special orders', detail: String(err) }, { status: 500 });
  }
}
