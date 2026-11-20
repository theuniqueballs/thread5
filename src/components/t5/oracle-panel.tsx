'use client';

/**
 * ПАНЕЛЬ ОРАКУЛА — вкладка nervous system прилавка (эра ORACLE-2).
 *
 * Четыре органа:
 *   1. ПУЛЬС — жив ли oracle-service, каким режимом отвечает прилавок;
 *   2. ЖАР ПО КОРПУСУ — heat-метрики последних партий (R+-доля, коридоры,
 *      свежесть, дрейф label↔fact, дубли каналов);
 *   3. ЖРЕБИЙ — детерминированный расклад карт на следующую партию
 *      (seed = номер партии: тот же номер → тот же расклад, копируется
 *      маркдауном прямо в бриф);
 *   4. ЭКСПРЕСС-ОЦЕНКА — любой текст через движок (lite локально + полный
 *      вердикт сервиса, если поднят).
 *
 * Дизайн — стеклянные панели прилавка (t5-panel), акцент циан (--t5-oracle).
 */

import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { Activity, Copy, Dices, Flame, Loader2, RefreshCw, Sparkles, Wand2 } from 'lucide-react';
import { Chip, CopyButton, copyText } from '@/components/t5/bits';
import { useToast } from '@/hooks/use-toast';
import { cn } from '@/lib/utils';
import { ENGINE_ERA, type BatchHeat, type DrawResult, type LiteVerdict, type RotationWindow } from '@/lib/t5/oracle-engine';

/* ── типы ответов API (локальные эндпоинты прилавка) ── */

interface StatusResp {
  reachable: boolean;
  mode: 'service+local' | 'local';
  url: string;
  health: { era?: string; camera_registry?: string; cards_indexed?: number } | null;
  local_engine: string;
}

interface HeatResp {
  heat: BatchHeat & { drifts: { slotId: string; label: string | null; fact: string; drift: string | null }[] };
  cardUsage: Record<string, { usedCount: number; lastBatch: number | null; lastBatchFile: string | null }>;
}

interface DrawResp {
  draw: DrawResult;
  window: RotationWindow;
  registry: { version: string; cards: number };
}

interface RateResp {
  lite: LiteVerdict;
  service: { url: string; verdict: { verdict?: string; warnings?: string[] } | null } | null;
  /** P1-05: версия движка — подпись режима прилагается к любому результату */
  engine?: string;
}

const CORRIDOR_TONE: Record<string, string> = {
  A: 'text-t5-rose-bright',
  B: 'text-t5-mint-bright',
  'A+B': 'text-t5-accent-bright',
  '—': 'text-zinc-500',
};

function OracleDot({ ok }: { ok: boolean }) {
  return (
    <span className="relative inline-flex size-2.5" aria-hidden>
      <span className={cn('absolute inset-0 rounded-full', ok ? 'bg-t5-oracle' : 'bg-zinc-600')} />
      {ok && <span className="absolute inset-0 animate-ping rounded-full bg-t5-oracle/60" />}
    </span>
  );
}

function Bar({ value, tone }: { value: number; tone: string }) {
  return (
    <span className="block h-1.5 w-full overflow-hidden rounded-full bg-white/[0.06]" aria-hidden>
      <span className="block h-full rounded-full transition-[width] duration-500" style={{ width: `${Math.round(value * 100)}%`, background: tone }} />
    </span>
  );
}

/* ═══════════════════════ ПУЛЬС ═══════════════════════ */

function PulseCard({ status, onRefresh, refreshing }: { status: StatusResp | null; onRefresh: () => void; refreshing: boolean }) {
  const ok = status?.reachable ?? false;
  return (
    <section className="t5-panel p-5">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <h2 className="flex items-center gap-2.5 font-mono text-[13px] font-bold tracking-[0.18em] text-zinc-200">
          <Activity className="size-4 text-t5-oracle" aria-hidden />
          ПУЛЬС ОРАКУЛА
        </h2>
        <button
          type="button"
          onClick={onRefresh}
          className="inline-flex items-center gap-1.5 rounded-lg border border-white/[0.09] px-2.5 py-1 font-mono text-[11px] text-zinc-400 transition-colors hover:border-t5-oracle/50 hover:text-t5-oracle-bright"
          aria-label="Перепроверить связь с оракулом"
        >
          {refreshing ? <Loader2 className="size-3.5 animate-spin" aria-hidden /> : <RefreshCw className="size-3.5" aria-hidden />}
          пульс
        </button>
      </div>
      <div className="mt-4 grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
        <div className="rounded-xl border border-white/[0.07] bg-white/[0.02] p-3.5">
          <p className="t5-label mb-1.5 flex items-center gap-2">
            <OracleDot ok={ok} /> сервис :3031
          </p>
          <p className={cn('font-mono text-sm font-bold', ok ? 'text-t5-oracle-bright' : 'text-zinc-400')}>
            {ok ? 'ЖИВ · LLM+vision' : 'СПИТ · локальный движок'}
          </p>
          <p className="mt-1 truncate font-mono text-[10px] text-zinc-600">{status?.url ?? '—'}</p>
        </div>
        <div className="rounded-xl border border-white/[0.07] bg-white/[0.02] p-3.5">
          <p className="t5-label mb-1.5">режим прилавка</p>
          <p className="font-mono text-sm font-bold text-zinc-200">{status?.mode ?? '…'}</p>
          <p className="mt-1 font-mono text-[10px] leading-snug text-zinc-600">сервис — усилитель, не единственная точка правды</p>
        </div>
        <div className="rounded-xl border border-white/[0.07] bg-white/[0.02] p-3.5">
          <p className="t5-label mb-1.5">реестр камер</p>
          <p className="font-mono text-sm font-bold text-zinc-200">{status?.health?.camera_registry ?? '—'}</p>
          <p className="mt-1 font-mono text-[10px] text-zinc-600">{status?.health?.cards_indexed ?? '—'} Y-карт проиндексировано</p>
        </div>
        <div className="rounded-xl border border-white/[0.07] bg-white/[0.02] p-3.5">
          <p className="t5-label mb-1.5">эра движка</p>
          <p className="font-mono text-[11px] font-bold leading-snug text-zinc-200">{status?.health?.era ?? ENGINE_ERA}</p>
        </div>
      </div>
    </section>
  );
}

/* ═══════════════════════ ЖАР КОРПУСА ═══════════════════════ */

function HeatRow({ heat, onOpen }: { heat: HeatResp['heat']; onOpen: (slug: string) => void }) {
  const tone = heat.score >= 75 ? 'linear-gradient(90deg,#ff7373,#ffab5e)' : heat.score >= 50 ? 'linear-gradient(90deg,#ffab5e,#e6b455)' : 'linear-gradient(90deg,#4ad6b0,#5ec8f2)';
  const corr = Object.entries(heat.corridorHistogram).sort((a, b) => b[1] - a[1]);
  return (
    <button
      type="button"
      onClick={() => onOpen(heat.slug)}
      className="w-full rounded-xl border border-white/[0.07] bg-white/[0.02] p-4 text-left transition-colors hover:border-t5-oracle/40"
      aria-label={`Жар ${heat.slug}: ${heat.score}/100 — открыть батч`}
    >
      <div className="flex flex-wrap items-baseline justify-between gap-2">
        <span className="font-mono text-sm font-bold text-zinc-100">{heat.slug}</span>
        <span className="font-mono text-[11px] text-zinc-500">
          {heat.slotCount} слотов · {heat.ratedCount} рейтинговых · R+ {Math.round(heat.rplusShare * 100)}%
        </span>
        <span className="font-mono text-sm font-bold tabular-nums" style={{ color: heat.score >= 75 ? '#ff9d6b' : heat.score >= 50 ? '#e6b455' : '#5ec8f2' }}>
          {heat.score}<span className="text-zinc-600">/100</span>
        </span>
      </div>
      <div className="mt-2.5"><Bar value={heat.score / 100} tone={tone} /></div>
      <div className="mt-2.5 flex flex-wrap items-center gap-x-3 gap-y-1 font-mono text-[10px] text-zinc-500">
        {corr.map(([k, v]) => (
          <span key={k} className={CORRIDOR_TONE[k] ?? 'text-zinc-500'}>коридор {k}×{v}</span>
        ))}
        <span>карты {heat.cardsUsed} (свежих {heat.cardsFresh})</span>
        {heat.driftCount > 0 && <span className="text-t5-orange">дрейф label↔fact ×{heat.driftCount}</span>}
        {heat.channelDupes.length > 0 && <span className="text-t5-orange">каналы-дубли: {heat.channelDupes.length}</span>}
      </div>
    </button>
  );
}

/* ═══════════════════════ ЖРЕБИЙ ═══════════════════════ */

function DrawCardTile({ slot, card }: { slot: string; card: DrawResult['oc'][number] }) {
  return (
    <div className="rounded-xl border border-white/[0.07] bg-black/25 p-3.5">
      <div className="flex items-baseline justify-between gap-2">
        <span className="font-mono text-sm font-bold text-t5-oracle-bright">{card.id}</span>
        <span className="font-mono text-[10px] text-zinc-600">{slot}</span>
      </div>
      <p className={cn('mt-1 font-mono text-[10px] font-bold', CORRIDOR_TONE[card.corridor] ?? 'text-zinc-500')}>
        коридор {card.corridor} · {card.exposureClass}
      </p>
      <p className="mt-2 line-clamp-3 font-mono text-[10px] leading-relaxed text-zinc-500" title={card.pattern}>
        {card.pattern}
      </p>
      <p className="mt-2 border-t border-white/[0.05] pt-2 text-[10px] leading-snug text-zinc-600">{card.reason}</p>
    </div>
  );
}

function DrawSection({ draw }: { draw: DrawResp }) {
  const { toast } = useToast();
  const asMarkdown = useMemo(() => {
    const lines = [
      `## Жребий оракула — партия №${draw.draw.batchNo} (seed ${draw.draw.seed})`,
      '',
      `Реестр: camera ${draw.registry.version} · ${draw.registry.cards} карт · окно ротации: ${draw.window.depth} партий (${draw.window.batches.map((b) => b.file.replace('.md', '')).join(', ') || '—'})`,
      '',
      '### OC-тройка',
      ...draw.draw.oc.map((c) => `- **${c.id}** (${c.corridor}, ${c.exposureClass}) — ${c.reason}`),
      '',
      '### Мейн-лента',
      ...draw.draw.main.map((c) => `- **${c.id}** (${c.corridor}, ${c.exposureClass}) — ${c.reason}`),
      '',
      '### EXP-волна',
      ...draw.draw.exp.map((c) => `- **${c.id}** (${c.corridor}, ${c.exposureClass}) — ${c.reason}`),
      '',
      draw.draw.shortfall > 0
        ? `⚠ пул иссяк на ${draw.draw.shortfall} слотах — окно ротации съело элитные корзины, сузь глубину или добрось карт в реестр`
        : 'Расклад полный: окно ротации чисто, корзины выдохлись без остатка.',
    ];
    return lines.join('\n');
  }, [draw]);

  return (
    <section className="t5-panel p-5">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <h2 className="flex items-center gap-2.5 font-mono text-[13px] font-bold tracking-[0.18em] text-zinc-200">
          <Dices className="size-4 text-t5-oracle" aria-hidden />
          ЖРЕБИЙ · T5-{String(draw.draw.batchNo).padStart(2, '0')}
        </h2>
        <CopyButton
          text={asMarkdown}
          label="жребий маркдауном"
          className="!border-t5-oracle/30 !bg-t5-oracle/10 !text-t5-oracle-bright hover:!border-t5-oracle/60"
        />
      </div>
      <p className="mt-2 font-mono text-[10px] leading-relaxed text-zinc-600">
        {draw.draw.determinism}. Окно съело {draw.draw.windowExcluded} карт реестра.
        {draw.draw.shortfall > 0 && <span className="text-t5-orange"> Пул иссяк на {draw.draw.shortfall} слотах.</span>}
      </p>
      <div className="mt-4 space-y-4">
        <div>
          <p className="t5-label mb-2">OC-тройка — R+-способные, коридор A</p>
          <div className="grid gap-2.5 sm:grid-cols-2 lg:grid-cols-3">
            {draw.draw.oc.map((c, i) => <DrawCardTile key={c.id} slot={`OC ${i + 1}`} card={c} />)}
          </div>
        </div>
        <div>
          <p className="t5-label mb-2">Мейн-лента — баланс коридоров A / B / низкие тиры</p>
          <div className="grid gap-2.5 sm:grid-cols-2 lg:grid-cols-3">
            {draw.draw.main.map((c, i) => <DrawCardTile key={c.id} slot={`мейн ${String(i + 1).padStart(2, '0')}`} card={c} />)}
          </div>
        </div>
        <div>
          <p className="t5-label mb-2">EXP-волна — новенькие, которых ещё не создавали</p>
          <div className="grid gap-2.5 sm:grid-cols-2 lg:grid-cols-3">
            {draw.draw.exp.map((c, i) => <DrawCardTile key={c.id} slot={`EXP ${String.fromCharCode(945 + i)}`} card={c} />)}
          </div>
        </div>
      </div>
    </section>
  );
}

/* ═══════════════════════ ЭКСПРЕСС-ОЦЕНКА ═══════════════════════ */

function RateConsole() {
  const { toast } = useToast();
  const [text, setText] = useState('');
  const [busy, setBusy] = useState(false);
  const [result, setResult] = useState<RateResp | null>(null);
  const abortRef = useRef<AbortController | null>(null);
  useEffect(() => () => abortRef.current?.abort(), []);

  const run = useCallback(async () => {
    if (!text.trim()) {
      toast({ title: 'Нечего оценивать', description: 'Вставь POS слота или описание кадра.' });
      return;
    }
    abortRef.current?.abort();
    const ctrl = new AbortController();
    abortRef.current = ctrl;
    setBusy(true);
    try {
      const res = await fetch('/api/t5/oracle/rate', {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({ text }),
        signal: ctrl.signal,
      });
      const data = (await res.json()) as RateResp & { error?: string };
      if (!res.ok) throw new Error(data.error ?? 'ошибка оценки');
      setResult(data);
    } catch (err) {
      if ((err as Error).name !== 'AbortError') {
        toast({ title: 'Оракул молчит', description: String((err as Error).message ?? err) });
      }
    } finally {
      setBusy(false);
    }
  }, [text, toast]);

  const lite = result?.lite;
  return (
    <section className="t5-panel p-5">
      <h2 className="flex items-center gap-2.5 font-mono text-[13px] font-bold tracking-[0.18em] text-zinc-200">
        <Wand2 className="size-4 text-t5-oracle" aria-hidden />
        ЭКСПРЕСС-ОЦЕНКА
      </h2>
      <p className="mt-2 font-mono text-[10px] leading-relaxed text-zinc-600">
        Любой текст через движок: тир (SFW/PG-13/R/R+/X), коридор, классы раскрытия, флоры. Локально — мгновенно; живой сервис добавляет полный вердикт.
      </p>
      <div className="mt-3.5">
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === 'Enter' && (e.metaKey || e.ctrlKey)) { e.preventDefault(); void run(); }
          }}
          rows={5}
          maxLength={20000}
          placeholder="POS слота или описание кадра… (⌘/Ctrl+Enter — оценить)"
          aria-label="Текст для экспресс-оценки оракула"
          className="w-full resize-y rounded-xl border border-white/[0.09] bg-black/30 p-3.5 font-mono text-[12px] leading-relaxed text-zinc-200 outline-none transition-colors placeholder:text-zinc-700 focus:border-t5-oracle/50"
        />
        <div className="mt-2.5 flex items-center justify-between gap-3">
          <span className="font-mono text-[10px] text-zinc-600">{text.length.toLocaleString('ru-RU')} / 20 000</span>
          <button
            type="button"
            onClick={() => void run()}
            disabled={busy}
            className="inline-flex items-center gap-1.5 rounded-lg border border-t5-oracle/30 bg-t5-oracle/10 px-3.5 py-1.5 font-mono text-[11px] font-bold text-t5-oracle-bright transition-colors hover:border-t5-oracle/60 disabled:opacity-50"
          >
            {busy ? <Loader2 className="size-3.5 animate-spin" aria-hidden /> : <Sparkles className="size-3.5" aria-hidden />}
            оценить
          </button>
        </div>
      </div>
      {lite && (
        <div className="mt-4 space-y-2.5 rounded-xl border border-white/[0.07] bg-black/25 p-4">
          {/* двойной аудит P1-05: любой результат Oracle подписан режимом —
              LOCAL-LITE / +SERVICE-RULE; финал всегда AUTHOR-VERDICT */}
          <div className="flex flex-wrap items-center gap-2 border-b border-white/[0.06] pb-2.5">
            <span className="rounded-lg bg-t5-oracle/10 px-2.5 py-1 font-mono text-[10px] font-bold tracking-wider text-t5-oracle-bright">РЕЖИМ: LOCAL-LITE{result?.service?.verdict?.verdict ? ' + SERVICE-RULE' : ''}</span>
            <Chip>движок {result?.engine ?? '…'}</Chip>
            <span className="font-mono text-[10px] text-zinc-600">метрика ≠ вердикт качества — финал за автором (AUTHOR-VERDICT)</span>
          </div>
          <div className="flex flex-wrap items-center gap-2">
            <span
              className={cn(
                'rounded-lg px-2.5 py-1 font-mono text-xs font-bold',
                lite.tier === 'X' && 'bg-t5-red/15 text-t5-red',
                lite.tier === 'R+' && 'bg-t5-rose/15 text-t5-rose-bright',
                lite.tier === 'R' && 'bg-t5-rose/10 text-t5-rose/80',
                lite.tier === 'PG-13' && 'bg-white/[0.05] text-zinc-300',
                lite.tier === 'SFW' && 'bg-white/[0.04] text-zinc-500',
              )}
            >
              {lite.tier}
            </span>
            <Chip>коридор {lite.corridor}</Chip>
            {lite.exposureClasses.map((c) => <Chip key={c}>{c}</Chip>)}
            {result?.service?.verdict?.verdict && <Chip>сервис: {String(result.service.verdict.verdict)}</Chip>}
          </div>
          {lite.signals.pg13.length > 0 && <p className="font-mono text-[10px] text-zinc-600">PG-13: {lite.signals.pg13.slice(0, 6).join(', ')}</p>}
          {lite.signals.r.length > 0 && <p className="font-mono text-[10px] text-zinc-600">R: {lite.signals.r.slice(0, 6).join(', ')}</p>}
          {(lite.signals.rplusHard.length > 0 || lite.signals.rplusSoft.length > 0) && (
            <p className="font-mono text-[10px] text-zinc-600">R+: {[...lite.signals.rplusHard, ...lite.signals.rplusSoft].slice(0, 6).join(', ')}</p>
          )}
          {lite.floors.map((f) => (
            <p key={f} className="rounded-lg bg-t5-red/10 px-2.5 py-1.5 font-mono text-[10px] leading-snug text-t5-red">{f}</p>
          ))}
          {lite.warnings.map((w) => (
            <p key={w} className="rounded-lg bg-t5-orange/10 px-2.5 py-1.5 font-mono text-[10px] leading-snug text-t5-orange">{w}</p>
          ))}
          {[...(result?.service?.verdict?.warnings ?? [])].slice(0, 4).map((w) => (
            <p key={w} className="rounded-lg bg-white/[0.04] px-2.5 py-1.5 font-mono text-[10px] leading-snug text-zinc-400">сервис: {w}</p>
          ))}
        </div>
      )}
    </section>
  );
}

/** номер партии из слага: «T5-26» → 26 (регресс панели: /\d+/ без дефиса
 * хватал пятёрку из «T5» и «следующая партия» показывалась как T5-6) */
function slugNum(slug: string): number {
  return Number.parseInt(/-(\d+)$/u.exec(slug.trim())?.[1] ?? '0', 10) || 0;
}

/* ═══════════════════════ ПАНЕЛЬ ═══════════════════════ */

export function OraclePanel({ batches, onOpenBatch }: { batches: { slug: string; slotCount: number }[]; onOpenBatch: (slug: string) => void }) {
  const { toast } = useToast();
  const [status, setStatus] = useState<StatusResp | null>(null);
  const [refreshing, setRefreshing] = useState(false);
  const [heats, setHeats] = useState<HeatResp[]>([]);
  const [heatsLoading, setHeatsLoading] = useState(true);
  const [drawFor, setDrawFor] = useState<string>('');
  const [draw, setDraw] = useState<DrawResp | null>(null);
  const [drawLoading, setDrawLoading] = useState(false);

  const loadStatus = useCallback(async (soft: boolean) => {
    if (soft) setRefreshing(true);
    try {
      const res = await fetch('/api/t5/oracle/status', { cache: 'no-store' });
      setStatus((await res.json()) as StatusResp);
    } catch {
      setStatus({ reachable: false, mode: 'local', url: '—', health: null, local_engine: ENGINE_ERA });
    } finally {
      setRefreshing(false);
    }
  }, []);

  /* жар: последние 6 партий с слотами (список уже приходит с полки) */
  const heatSlugs = useMemo(
    () => [...batches].filter((b) => b.slotCount > 0).sort((a, b) => slugNum(a.slug) - slugNum(b.slug)).slice(-6),
    [batches],
  );

  const loadHeats = useCallback(async () => {
    if (!heatSlugs.length) { setHeats([]); setHeatsLoading(false); return; }
    setHeatsLoading(true);
    try {
      const responses = await Promise.all(
        heatSlugs.map(async (b) => {
          try {
            const res = await fetch(`/api/t5/oracle/heat/${encodeURIComponent(b.slug)}?full=1`, { cache: 'no-store' });
            return res.ok ? ((await res.json()) as HeatResp) : null;
          } catch {
            return null;
          }
        }),
      );
      setHeats(responses.filter((r): r is HeatResp => r !== null));
    } finally {
      setHeatsLoading(false);
    }
  }, [heatSlugs]);

  useEffect(() => {
    void loadStatus(false);
  }, [loadStatus]);

  useEffect(() => {
    void loadHeats();
  }, [loadHeats]);

  /* номер следующей партии — по умолчанию max+1 из полки */
  const nextBatchNo = useMemo(() => {
    const max = batches.reduce((acc, b) => Math.max(acc, slugNum(b.slug)), 0);
    return max > 0 ? max + 1 : 27;
  }, [batches]);

  useEffect(() => {
    if (!drawFor) setDrawFor(`T5-${nextBatchNo}`);
  }, [nextBatchNo, drawFor]);

  const runDraw = useCallback(async () => {
    const m = /^T5-(\d{1,3})$/iu.exec(drawFor.trim());
    if (!m) {
      toast({ title: 'Номер партии нужен', description: 'Формат: T5-27 — жребий сеется номером.' });
      return;
    }
    setDrawLoading(true);
    try {
      const res = await fetch(`/api/t5/oracle/draw?for=${encodeURIComponent(m[0])}`, { cache: 'no-store' });
      const data = (await res.json()) as DrawResp & { error?: string };
      if (!res.ok) throw new Error(data.error ?? 'жребий не брошен');
      setDraw(data);
    } catch (err) {
      toast({ title: 'Кости не покатились', description: String((err as Error).message ?? err) });
    } finally {
      setDrawLoading(false);
    }
  }, [drawFor, toast]);

  return (
    <div className="space-y-9">
      <section className="t5-panel relative overflow-hidden p-6 sm:p-9">
        <div
          aria-hidden
          className="pointer-events-none absolute -right-24 -top-32 h-80 w-80 rounded-full opacity-40 blur-3xl"
          style={{ background: 'radial-gradient(circle, color-mix(in srgb, var(--t5-oracle) 18%, transparent), transparent 70%)' }}
        />
        <p className="t5-label mb-4 flex items-center gap-3 text-t5-oracle">
          <span className="inline-block h-px w-10" style={{ background: 'linear-gradient(90deg, var(--t5-oracle), transparent)' }} aria-hidden />
          Нервная система конвейера
        </p>
        <h1 className="font-display text-[26px] font-bold uppercase leading-[1.08] tracking-tight sm:text-3xl lg:text-[40px]">
          <span className="t5-gradient-text">Оракул</span>
        </h1>
        <p className="mt-4 max-w-2xl text-sm leading-relaxed text-zinc-400 sm:text-[15px]">
          Оракул вплетён во весь организм: оценивает слоты и рендеры, меряет жар партий, тянет жребий карт на
          следующую партию и отвечает на вопросы домена. Прилавок считает локально — сервис усиливает.
        </p>
        <div className="mt-6 flex flex-wrap items-center gap-2.5">
          <div className="rounded-xl border border-white/[0.08] bg-white/[0.025] px-4 py-2.5">
            <p className="t5-label mb-1">партий на полке</p>
            <p className="font-mono text-lg font-bold tabular-nums text-white">{batches.length}</p>
          </div>
          <div className="rounded-xl border border-white/[0.08] bg-white/[0.025] px-4 py-2.5">
            <p className="t5-label mb-1">жар-проба</p>
            <p className="font-mono text-lg font-bold tabular-nums text-white">{heats.length}</p>
          </div>
          <div className="rounded-xl border border-white/[0.08] bg-white/[0.025] px-4 py-2.5">
            <p className="t5-label mb-1">следующая партия</p>
            <p className="font-mono text-lg font-bold tabular-nums text-white">T5-{nextBatchNo}</p>
          </div>
        </div>
      </section>

      <PulseCard status={status} onRefresh={() => void loadStatus(true)} refreshing={refreshing} />

      <section className="t5-panel p-5">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <h2 className="flex items-center gap-2.5 font-mono text-[13px] font-bold tracking-[0.18em] text-zinc-200">
            <Flame className="size-4 text-t5-oracle" aria-hidden />
            ЖАР ПОСЛЕДНИХ ПАРТИЙ
          </h2>
          <button
            type="button"
            onClick={() => void loadHeats()}
            className="inline-flex items-center gap-1.5 rounded-lg border border-white/[0.09] px-2.5 py-1 font-mono text-[11px] text-zinc-400 transition-colors hover:border-t5-oracle/50 hover:text-t5-oracle-bright"
            aria-label="Пересчитать жар партий"
          >
            {heatsLoading ? <Loader2 className="size-3.5 animate-spin" aria-hidden /> : <RefreshCw className="size-3.5" aria-hidden />}
            жар
          </button>
        </div>
        <p className="mt-2 font-mono text-[10px] leading-relaxed text-zinc-600">
          {heats[0]?.heat.formula ?? 'жар = R+-доля + баланс коридоров + свежесть карт + честность label + уникальность каналов'}
        </p>
        <div className="mt-3.5 space-y-2.5">
          {heatsLoading && !heats.length && (
            <div className="flex items-center gap-2 px-2 py-6 font-mono text-[11px] text-zinc-600">
              <Loader2 className="size-3.5 animate-spin" aria-hidden /> щупаю корпус…
            </div>
          )}
          {!heatsLoading && !heats.length && (
            <p className="px-2 py-6 text-center font-mono text-[11px] text-zinc-600">партий с слотами на полке нет — жар считать не с чего</p>
          )}
          {[...heats].reverse().map((h) => <HeatRow key={h.heat.slug} heat={h.heat} onOpen={onOpenBatch} />)}
        </div>
      </section>

      <section className="t5-panel p-5">
        <h2 className="flex items-center gap-2.5 font-mono text-[13px] font-bold tracking-[0.18em] text-zinc-200">
          <Dices className="size-4 text-t5-oracle" aria-hidden />
          БРОСИТЬ КОСТИ
        </h2>
        <div className="mt-3.5 flex flex-wrap items-center gap-2.5">
          <input
            value={drawFor}
            onChange={(e) => setDrawFor(e.target.value)}
            onKeyDown={(e) => { if (e.key === 'Enter') void runDraw(); }}
            className="w-32 rounded-lg border border-white/[0.09] bg-black/30 px-3 py-1.5 font-mono text-[12px] text-zinc-200 outline-none transition-colors focus:border-t5-oracle/50"
            placeholder="T5-27"
            aria-label="Номер партии для жребия"
            maxLength={7}
          />
          <button
            type="button"
            onClick={() => void runDraw()}
            disabled={drawLoading}
            className="inline-flex items-center gap-1.5 rounded-lg border border-t5-oracle/30 bg-t5-oracle/10 px-3.5 py-1.5 font-mono text-[11px] font-bold text-t5-oracle-bright transition-colors hover:border-t5-oracle/60 disabled:opacity-50"
          >
            {drawLoading ? <Loader2 className="size-3.5 animate-spin" aria-hidden /> : <Dices className="size-3.5" aria-hidden />}
            тянуть карты
          </button>
          {draw && (
            <button
              type="button"
              onClick={() => { void copyText(`T5-${draw.draw.batchNo}: ${draw.draw.oc.map((c) => c.id).join(', ')} / ${draw.draw.main.map((c) => c.id).join(', ')} / ${draw.draw.exp.map((c) => c.id).join(', ')}`); toast({ title: 'Список карт скопирован', description: 'OC / мейн / EXP — плоским списком.' }); }}
              className="inline-flex items-center gap-1.5 rounded-lg border border-white/[0.09] px-3 py-1.5 font-mono text-[11px] text-zinc-400 transition-colors hover:border-t5-oracle/50 hover:text-t5-oracle-bright"
            >
              <Copy className="size-3.5" aria-hidden /> ids одним списком
            </button>
          )}
        </div>
        <p className="mt-2 font-mono text-[10px] leading-relaxed text-zinc-600">
          Жребий детерминирован: окно ротации (3 партии) исключает горячий хвост, OC тянутся из A-коридора с классом COVER,
          EXP — из никогда не использованных. Тот же номер партии → тот же расклад.
        </p>
      </section>

      {draw && <DrawSection draw={draw} />}

      <RateConsole />
    </div>
  );
}
