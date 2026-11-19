import { NextResponse } from 'next/server';
import { readSpecJson } from '@/lib/t5/store';
import { buildYStampLine, buildWeave, type YCardLike } from '@/lib/t5/ystamp';

const CACHE_CONTROL = 'public, max-age=30, stale-while-revalidate=60';

/** форма specs/camera.json (нас интересует только y_cards.cards) */
interface CameraSpec {
  version?: string;
  y_cards?: { cards?: YCardLike[] };
}

export async function GET(req: Request) {
  const url = new URL(req.url);
  const id = (url.searchParams.get('card') ?? '').trim().toUpperCase();
  if (!/^Y\d{1,3}$/.test(id)) {
    return NextResponse.json(
      { error: 'Нужен id карты вида Y{NN} (например Y29 или Y513)' },
      { status: 400 },
    );
  }
  const cam = await readSpecJson<CameraSpec>('specs/camera.json');
  if (!cam) {
    return NextResponse.json(
      { error: 'specs/camera.json не читается — клеймо печатается только из карты' },
      { status: 500 },
    );
  }
  const cards = cam.y_cards?.cards ?? [];
  const card = cards.find((c) => c.id === id);
  if (!card) {
    return NextResponse.json(
      {
        error: 'Карта не найдена в camera.json',
        card: id,
        total: cards.length,
        registry: cam.version ?? '—',
      },
      { status: 404 },
    );
  }
  return NextResponse.json(
    {
      cardId: id,
      weave: buildWeave(card),
      stamp: buildYStampLine(card),
      exposureClass: card.components?.exposure?.class ?? '—',
      corridor: card.corridor ?? '—',
      builtFrom: card.built_from ?? null,
      registry: cam.version ?? '—',
    },
    { headers: { 'Cache-Control': CACHE_CONTROL } },
  );
}
