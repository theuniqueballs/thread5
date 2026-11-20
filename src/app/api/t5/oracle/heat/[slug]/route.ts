import { NextResponse } from 'next/server';
import { readBatch, readSpecJson } from '@/lib/t5/store';
import { buildCardUsage, batchHeat, ENGINE_ERA } from '@/lib/t5/oracle-engine';
import type { T5Batch } from '@/lib/t5/parse';

const CACHE_CONTROL = 'public, max-age=10, stale-while-revalidate=30';

/** форма specs/camera.json (нужна только y_cards.cards) */
interface CameraSpec {
  version?: string;
  y_cards?: {
    cards?: {
      id: string;
      corridor?: string;
      components?: { exposure?: { class?: string }; pose?: string };
      pattern?: string;
    }[];
  };
}

/**
 * ЖАР партии — локальный движок, сервис не нужен.
 * ?full=1 — с послотовым дрейфом (по умолчанию дрейфы ужаты в счётчик,
 * чтобы список в UI не таскал лишний вес).
 */
export async function GET(req: Request, { params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const batch = await readBatch(slug);
  if (!batch) {
    return NextResponse.json({ error: 'Батч не найден', slug }, { status: 404 });
  }

  // корпус для истории карт: все партии КРОМЕ этой (использование до неё)
  const { listBatches } = await import('@/lib/t5/store');
  const all = await Promise.all((await listBatches()).map(async (b) => await readBatch(b.slug)));
  const corpus = all.filter((b): b is T5Batch => b !== null && b.slug !== batch.slug);
  const usage = buildCardUsage(
    corpus.map((b) => ({ slug: b.slug, slots: b.slots })),
    Number.parseInt(/(\d+)$/u.exec(slug)?.[1] ?? '0', 10),
  );

  // В34-базис честности: слоты с картой сверяются ВПЛЕТЕНИЕМ (реестровое —
  // прозо-устойчиво); словари lite — только для бескарточных (урок T5-26)
  const cam = await readSpecJson<CameraSpec>('specs/camera.json');
  const cardsById: Record<string, { pattern?: string; components?: { pose?: string } }> = {};
  for (const c of cam?.y_cards?.cards ?? []) cardsById[c.id] = c;

  const heat = batchHeat(
    { slug: batch.slug, slots: batch.slots.map((s) => ({ id: s.id, rating: s.rating, corridor: s.corridor, channel: s.channel, yCard: s.yCard, pos: s.pos })) },
    usage,
    cardsById,
  );

  const full = new URL(req.url).searchParams.get('full') === '1';
  return NextResponse.json(
    {
      heat: full ? heat : { ...heat, drifts: heat.drifts.filter((d) => d.drift).slice(0, 12) },
      engine: ENGINE_ERA,
      cardUsage: Object.fromEntries(
        batch.slots
          .map((s) => s.yCard)
          .filter((y): y is string => Boolean(y))
          .filter((y, i, arr) => arr.indexOf(y) === i)
          .map((y) => [y, usage[y] ?? { id: y, usedCount: 0, lastBatch: null, lastBatchFile: null }]),
      ),
    },
    { headers: { 'Cache-Control': CACHE_CONTROL } },
  );
}
