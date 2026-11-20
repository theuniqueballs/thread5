import { NextResponse } from 'next/server';
import { oracleStatus } from '@/lib/t5/oracle-client';
import { ENGINE_ERA } from '@/lib/t5/oracle-engine';

const CACHE_CONTROL = 'public, max-age=10, stale-while-revalidate=30';

/** Статус нервной системы: жив ли сервис, каким режимом отвечает прилавок. */
export async function GET() {
  const status = await oracleStatus(true);
  return NextResponse.json(
    {
      ...status,
      local_engine: ENGINE_ERA,
      endpoints: {
        local: ['/api/t5/oracle/status', '/api/t5/oracle/heat/[slug]', '/api/t5/oracle/draw?for=T5-27', '/api/t5/oracle/rate'],
        service: ['/health', '/rate', '/audit', '/batch', '/ystamp', '/triage', '/volt', '/ask', '/vision', '/window', '/draw'],
      },
    },
    { headers: { 'Cache-Control': CACHE_CONTROL } },
  );
}
