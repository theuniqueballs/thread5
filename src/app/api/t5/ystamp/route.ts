import { NextResponse } from 'next/server';
import { readFile } from 'fs/promises';
import path from 'path';
import { buildYStampLine, type YCardLike } from '@/lib/t5/ystamp';

/**
 * Y-STAMP API (акт 2 вердикта T5-24, приказ Б): клеймо печатается
 * автоматически из id карты — никаких ручных строк. Прилавок запрашивает
 * строку-паспорт по id (Y{NN}) и кладёт её в буфер одним кликом.
 */
const T5_ROOT = path.join(process.cwd(), 'thread5');
const CACHE_CONTROL = 'public, max-age=30, stale-while-revalidate=60';

export async function GET(req: Request) {
  const url = new URL(req.url);
  const id = (url.searchParams.get('card') ?? '').trim().toUpperCase();
  if (!/^Y\d{1,3}$/.test(id)) {
    return NextResponse.json(
      { error: 'Нужен id карты вида Y{NN} (например Y29)' },
      { status: 400 },
    );
  }
  let cards: YCardLike[] = [];
  try {
    const raw = await readFile(path.join(T5_ROOT, 'specs/camera.json'), 'utf8');
    const parsed = JSON.parse(raw) as { y_cards?: { cards?: YCardLike[] } };
    cards = parsed?.y_cards?.cards ?? [];
  } catch {
    return NextResponse.json(
      { error: 'specs/camera.json не читается — клеймо печатается только из карты' },
      { status: 500 },
    );
  }
  const card = cards.find((c) => c.id === id);
  if (!card) {
    return NextResponse.json(
      { error: 'Карта не найдена в camera.json', card: id, total: cards.length },
      { status: 404 },
    );
  }
  return NextResponse.json(
    {
      cardId: id,
      stamp: buildYStampLine(card),
      exposureClass: card.components?.exposure?.class ?? '—',
      corridor: card.corridor ?? '—',
      builtFrom: card.built_from ?? null,
    },
    { headers: { 'Cache-Control': CACHE_CONTROL } },
  );
}
