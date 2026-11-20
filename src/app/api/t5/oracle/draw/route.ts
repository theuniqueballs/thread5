import { NextResponse } from 'next/server';
import { readSpecJson, listBatches, readBatch } from '@/lib/t5/store';
import {
  buildRotationWindow,
  buildCardUsage,
  buildPoseWindow,
  drawConstellation,
  ENGINE_ERA,
  type OracleCard,
} from '@/lib/t5/oracle-engine';
import type { T5Batch } from '@/lib/t5/parse';

const CACHE_CONTROL = 'public, max-age=30, stale-while-revalidate=60';

/** форма specs/camera.json (нужна только y_cards.cards) */
interface CameraSpec {
  version?: string;
  y_cards?: {
    cards?: {
      id: string;
      corridor?: string;
      components?: { exposure?: { class?: string }; pose?: string };
      pattern?: string;
      built_from?: string;
    }[];
  };
}

/**
 * ЖРЕБИЙ ОРАКУЛА на следующую партию: GET /api/t5/oracle/draw?for=T5-27
 * Параметры: for (номер партии, обязателен) · oc/main/exp (цели) · depth
 * (окно ротации, по умолчанию 3). Детерминизм: тот же for + тот же корпус →
 * тот же расклад (seed = номер партии, см. oracle-engine.ts).
 */
export async function GET(req: Request) {
  const url = new URL(req.url);
  const forParam = url.searchParams.get('for') ?? '';
  const batchNo = Number.parseInt(forParam.replace(/^T5-/iu, ''), 10);
  if (!Number.isFinite(batchNo) || batchNo <= 0 || batchNo > 999) {
    return NextResponse.json(
      { error: 'Нужен номер партии: ?for=T5-27 (1..999)', hint: 'жребий сеется номером партии — расклад воспроизводим' },
      { status: 400 },
    );
  }

  const cam = await readSpecJson<CameraSpec>('specs/camera.json');
  if (!cam || !cam.y_cards?.cards?.length) {
    return NextResponse.json({ error: 'specs/camera.json не читается — жребий бросается только по живому реестру' }, { status: 500 });
  }
  const cards: OracleCard[] = cam.y_cards.cards.map((c) => ({
    id: c.id,
    corridor: c.corridor ?? '—',
    exposureClass: c.components?.exposure?.class ?? '—',
    pattern: c.components?.pose || c.pattern || '',
    builtFrom: c.built_from || undefined,
  }));

  // корпус: партии С НОМЕРОМ МЕНЬШЕ batchNo (окно не должно видеть будущее)
  const all = await Promise.all((await listBatches()).map(async (b) => await readBatch(b.slug)));
  const corpus = all
    .filter((b): b is T5Batch => b !== null)
    .map((b) => ({ slug: b.slug, slots: b.slots.map((s) => ({ yCard: s.yCard, pose: s.pose })) }));

  const depth = Math.max(0, Math.min(10, Number.parseInt(url.searchParams.get('depth') ?? '3', 10) || 3));
  const window = buildRotationWindow(corpus, batchNo, depth);
  const usage = buildCardUsage(corpus, batchNo);
  // обкатка T5-27, проблема №1: PL-окно поз — карты на позах окна не раздаются
  const windowPoses = buildPoseWindow(corpus, batchNo, depth);

  const draw = drawConstellation(batchNo, cards, usage, {
    ocTarget: clampOpt(url.searchParams.get('oc'), 3),
    mainTarget: clampOpt(url.searchParams.get('main'), 21),
    expTarget: clampOpt(url.searchParams.get('exp'), 9),
    windowDepth: depth,
    windowPoses,
  });

  return NextResponse.json(
    {
      draw,
      window,
      windowPoses: { depth, poses: windowPoses.length },
      registry: { version: cam.version ?? '—', cards: cards.length },
      engine: ENGINE_ERA,
    },
    { headers: { 'Cache-Control': CACHE_CONTROL } },
  );
}

function clampOpt(raw: string | null, dflt: number): number {
  if (raw === null) return dflt;
  const n = Number.parseInt(raw, 10);
  if (!Number.isFinite(n)) return dflt;
  return Math.max(0, Math.min(33, n));
}
