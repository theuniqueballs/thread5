'use client';

import { useCallback, useEffect, useMemo, useState } from 'react';
import { ArrowUpRight, BookOpenText, Gift, Inbox, Layers, RefreshCw, Sparkles } from 'lucide-react';
import { format } from 'date-fns';
import { cn } from '@/lib/utils';
import { T5Markdown } from '@/components/t5/bits';
import { BatchView } from '@/components/t5/batch-view';
import { InboxView } from '@/components/t5/inbox-view';
import type { BatchListItem, T5DocMeta } from '@/lib/t5/types';
import { T5_DOCS } from '@/lib/t5/types';

type Tab = 'batches' | 'special' | 'inbox' | 'docs';
type View = { kind: 'list' } | { kind: 'batch'; slug: string } | { kind: 'special'; slug: string };

const DEFAULT_DOC = 'LAWS';
const SLUG_HASH_RE = /^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$/u;

/* вкладки в единой системе «золотая нить» (globals.css):
   золото — конвейер, малина — заказы, мята — триаж инбокса, фиолет — память */
const TAB_ACCENT: Record<Tab, string> = {
  batches: 'var(--t5-accent)',
  special: 'var(--t5-rose)',
  inbox: 'var(--t5-mint)',
  docs: 'var(--t5-violet)',
};

interface HashState {
  tab: Tab;
  view: View;
  doc: string;
}

/** hash → состояние: #T5-07 · #SO-03 · #memory/LAWS · #batches · #special */
function parseHash(): HashState {
  let raw = '';
  try {
    raw = decodeURIComponent(window.location.hash.replace(/^#/, ''));
  } catch {
    raw = window.location.hash.replace(/^#/, '');
  }
  if (raw.startsWith('memory')) {
    const doc = raw.slice('memory/'.length);
    const known = T5_DOCS.find((d) => d.name === doc);
    return { tab: 'docs', view: { kind: 'list' }, doc: known ? known.name : DEFAULT_DOC };
  }
  if (raw === 'special') return { tab: 'special', view: { kind: 'list' }, doc: DEFAULT_DOC };
  if (raw === 'inbox') return { tab: 'inbox', view: { kind: 'list' }, doc: DEFAULT_DOC };
  if (raw.startsWith('SO-') && SLUG_HASH_RE.test(raw)) {
    return { tab: 'special', view: { kind: 'special', slug: raw }, doc: DEFAULT_DOC };
  }
  if (raw.startsWith('T5-') && SLUG_HASH_RE.test(raw)) {
    return { tab: 'batches', view: { kind: 'batch', slug: raw }, doc: DEFAULT_DOC };
  }
  return { tab: 'batches', view: { kind: 'list' }, doc: DEFAULT_DOC };
}

/* «12 слотов / 3 слота / 1 слот» — русская множественность для спек-строки */
function slotsLabel(n: number): string {
  const m10 = n % 10;
  const m100 = n % 100;
  if (m10 === 1 && m100 !== 11) return 'слот';
  if (m10 >= 2 && m10 <= 4 && (m100 < 12 || m100 > 14)) return 'слота';
  return 'слотов';
}

/* дата файла батча: mtime, DD.MM HH:mm */
function MtimeLabel({ mtime }: { mtime: string }) {
  const d = new Date(mtime);
  if (Number.isNaN(d.getTime())) return null;
  return <span className="ml-auto shrink-0 font-mono text-[11px] tabular-nums text-zinc-500">{format(d, 'dd.MM HH:mm')}</span>;
}

function Hero({
  accent,
  overline,
  title,
  sub,
  stats,
}: {
  accent: string;
  overline: string;
  title: string;
  sub: string;
  stats: { value: string; label: string }[];
}) {
  return (
    <section
      className="t5-frame relative overflow-hidden rounded-2xl border border-white/[0.08]"
      aria-label={overline}
    >
      {/* город-подложка: монохром, тихий — титул издателя, а не постер */}
      <img
        src="/t5/hero-city.jpg"
        alt=""
        aria-hidden
        className="pointer-events-none absolute inset-0 h-full w-full object-cover object-[center_78%] opacity-40 grayscale contrast-[1.06]"
      />
      <div className="absolute inset-0 bg-gradient-to-t from-background via-background/70 to-background/15" aria-hidden />
      <div className="absolute inset-0 bg-gradient-to-r from-background/95 via-background/45 to-transparent" aria-hidden />
      {/* тихое тёплое свечение поверх города */}
      <div
        aria-hidden
        className="pointer-events-none absolute -right-24 -top-32 h-80 w-80 rounded-full opacity-40 blur-3xl"
        style={{ background: `radial-gradient(circle, color-mix(in srgb, ${accent} 16%, transparent), transparent 70%)` }}
      />

      <div className="relative flex flex-col gap-8 p-6 sm:p-9 lg:p-11">
        <div className="max-w-2xl">
          <p className="t5-label mb-5 flex items-center gap-3" style={{ color: accent }}>
            <span className="inline-block h-px w-10" style={{ background: `linear-gradient(90deg, ${accent}, transparent)` }} aria-hidden />
            {overline}
          </p>
          <h1 className="font-display text-[26px] font-bold uppercase leading-[1.08] tracking-tight sm:text-3xl lg:text-[40px]">
            <span className="t5-gradient-text">{title}</span>
          </h1>
          <p className="mt-4 max-w-xl text-sm leading-relaxed text-zinc-400 sm:text-[15px]">{sub}</p>
        </div>

        {/* статистика: тонкие медальоны с моно-цифрами на одном поручне */}
        <dl className="flex flex-wrap items-stretch gap-2.5">
          {stats.map((s) => (
            <div
              key={s.label}
              className="rounded-xl border border-white/[0.08] bg-white/[0.025] px-4 py-2.5 shadow-[inset_0_1px_0_rgb(255_255_255/0.05)] backdrop-blur-md transition-colors duration-200 hover:border-white/[0.16]"
            >
              <dt className="t5-label mb-1">{s.label}</dt>
              <dd className="font-mono text-lg font-bold leading-none tabular-nums text-white sm:text-xl">{s.value}</dd>
            </div>
          ))}
        </dl>
      </div>

      {/* переливающаяся золотая кромка низа: единственная анимация героя */}
      <div className="t5-shimmer h-px w-full bg-gradient-to-r from-transparent via-t5-accent/40 to-transparent" aria-hidden />
    </section>
  );
}

/* ── спек-строка карточки: слоты · OC · EXP · рейтинги — одна моно-строка ── */
function SpecRow({ b }: { b: BatchListItem }) {
  const ratingTone: Record<string, string> = {
    'R+': 'text-t5-rose',
    R: 'text-t5-rose/70',
    X: 'text-t5-red/90',
    'PG-13': 'text-zinc-400',
  };
  const order = ['R+', 'R', 'X', 'PG-13'];
  const ratings = order.filter((k) => b.ratingSpread[k]);
  return (
    <div className="relative z-10 mt-auto flex flex-wrap items-center gap-x-2 gap-y-1 border-t border-white/[0.06] pl-2 pt-3 font-mono text-[11px] tabular-nums">
      <span>
        <span className="font-bold text-zinc-200">{b.slotCount}</span>
        <span className="text-zinc-500"> {slotsLabel(b.slotCount)}</span>
      </span>
      {b.ocCount > 0 && (
        <>
          <span aria-hidden className="text-zinc-700">·</span>
          <span>
            <span className="text-zinc-500">OC</span> <span className="font-bold text-zinc-200">{b.ocCount}</span>
          </span>
        </>
      )}
      {b.expCount > 0 && (
        <>
          <span aria-hidden className="text-zinc-700">·</span>
          <span>
            <span className="text-zinc-500">EXP</span> <span className="font-bold text-t5-accent">{b.expCount}</span>
          </span>
        </>
      )}
      {ratings.map((k) => (
        <span key={k} className={ratingTone[k] ?? 'text-zinc-400'}>
          <span aria-hidden className="text-zinc-700">· </span>
          {k}×{b.ratingSpread[k]}
        </span>
      ))}
    </div>
  );
}

/* скелетон полки: вместо спиннера — тихие стеклянные заглушки */
function ListSkeleton({ variant }: { variant: 'batches' | 'special' }) {
  return (
    <section aria-label={variant === 'special' ? 'Полка заказов' : 'Прилавок батчей'} aria-busy="true" className="space-y-4">
      <div className="flex items-center justify-between">
        <div className="t5-skel h-3 w-40" />
        <div className="t5-skel h-9 w-28 rounded-lg" />
      </div>
      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-3" aria-hidden>
        {Array.from({ length: 6 }, (_, i) => (
          <div key={i} className="t5-panel p-5">
            <div className="t5-skel mb-3 h-4 w-24" />
            <div className="t5-skel mb-6 h-3.5 w-3/4" />
            <div className="t5-skel h-3 w-1/2" />
          </div>
        ))}
      </div>
    </section>
  );
}

function BatchList({
  items,
  variant = 'batches',
  onOpen,
  onRefresh,
  refreshing,
}: {
  items: BatchListItem[];
  variant?: 'batches' | 'special';
  onOpen: (slug: string) => void;
  onRefresh: () => void;
  refreshing: boolean;
}) {
  const isSpecial = variant === 'special';
  const accent = isSpecial ? 'var(--t5-rose)' : 'var(--t5-accent)';
  return (
    <section aria-label={isSpecial ? 'Полка заказов' : 'Прилавок батчей'} className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="t5-label flex items-center gap-2.5 !text-[11px] text-zinc-300">
          <span
            className="inline-block h-3.5 w-[3px] rounded-full"
            style={{ background: `linear-gradient(180deg, ${accent}, color-mix(in srgb, ${accent} 10%, transparent))` }}
            aria-hidden
          />
          {isSpecial ? `Special Orders — ${items.length}` : `Батчи — ${items.length}`}
        </h2>
        <button type="button" onClick={onRefresh} className="t5-btn">
          <RefreshCw className={cn('size-3.5', refreshing && 'animate-spin')} /> Обновить
        </button>
      </div>

      {items.length === 0 ? (
        <div className="t5-panel p-12 text-center">
          <Sparkles className="mx-auto mb-4 size-5 text-zinc-600" aria-hidden />
          <p className="t5-gradient-text mb-2 font-display text-lg font-bold uppercase">{isSpecial ? 'Полка заказов пуста' : 'Батчей пока нет'}</p>
          <p className="mx-auto max-w-md text-sm leading-relaxed text-zinc-400">
            {isSpecial ? (
              <>
                Заказы рождаются в чате: говоришь, что сделать (прикол, подарок, одна сцена) —
                писец пишет промпт по доктрине и кладёт файл в{' '}
                <span className="font-mono text-t5-rose-bright/90">special/SO-NN.md</span>. Здесь его забираешь.
              </>
            ) : (
              <>
                Петля начинается в чате: ты даёшь тему — писец показывает контракт,
                пишет батч <span className="font-mono text-t5-accent-bright/90">T5-01</span> — и он
                появляется здесь. Формат — RAW+, мастер{' '}
                <span className="font-mono text-zinc-400">specs/raw-plus.json</span>.
              </>
            )}
          </p>
        </div>
      ) : (
        <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
          {items.map((b) => (
            <button
              key={b.slug}
              type="button"
              onClick={() => onOpen(b.slug)}
              aria-label={`Открыть ${b.slug}`}
              className="t5-frame group relative flex flex-col overflow-hidden p-5 text-left transition-transform duration-200 ease-out hover:-translate-y-0.5 focus-visible:outline-none"
            >
              <span className="t5-card absolute inset-0" aria-hidden />
              {/* цветовая рельса батча */}
              <span
                aria-hidden
                className="absolute inset-y-0 left-0 z-10 w-[3px] opacity-80 transition-opacity group-hover:opacity-100"
                style={{ background: `linear-gradient(180deg, ${accent}, color-mix(in srgb, ${accent} 8%, transparent))` }}
              />
              {/* стрелка-приглашение: выезжает на ховере */}
              <ArrowUpRight
                aria-hidden
                className="absolute right-4 top-4 z-10 size-4 text-zinc-600 opacity-0 transition-all duration-200 group-hover:translate-x-0.5 group-hover:-translate-y-0.5 group-hover:opacity-100"
                style={{ color: accent }}
              />

              <div className="relative z-10 mb-1.5 flex items-baseline gap-2.5 pl-2">
                <span
                  className={cn(
                    'font-mono text-[17px] font-bold tracking-tight text-zinc-100 transition-colors',
                    isSpecial ? 'group-hover:text-t5-rose-bright' : 'group-hover:text-t5-accent-bright',
                  )}
                >
                  {b.slug}
                </span>
                {b.verdictCount > 0 && (
                  <span className="t5-badge t5-badge--gold">
                    ✓ {b.verdictCount}
                  </span>
                )}
                <MtimeLabel mtime={b.mtime} />
              </div>
              <p className="relative z-10 mb-4 line-clamp-1 pl-2 text-sm font-semibold text-zinc-200">{b.theme ?? b.title}</p>
              <SpecRow b={b} />
            </button>
          ))}
        </div>
      )}
    </section>
  );
}

function DocButton({ doc, active, onSelect }: { doc: T5DocMeta; active: boolean; onSelect: () => void }) {
  return (
    <button
      type="button"
      onClick={onSelect}
      aria-current={active ? 'true' : undefined}
      className={cn(
        'relative w-full rounded-lg border px-3.5 py-2.5 text-left transition-all duration-150',
        active
          ? 'border-white/[0.15] bg-white/[0.07] shadow-[inset_0_1px_0_rgb(255_255_255/0.06)]'
          : 'border-transparent hover:border-white/[0.09] hover:bg-white/[0.035]',
      )}
    >
      {active && (
        <span
          className="absolute inset-y-2 left-0 w-[2.5px] rounded-full bg-t5-violet shadow-[0_0_10px_color-mix(in_srgb,var(--t5-violet)_65%,transparent)]"
          aria-hidden
        />
      )}
      <span className={cn('block text-[13px] font-bold tracking-wide', active ? 'text-white' : 'text-zinc-300')}>
        {doc.title}
      </span>
      <span className="mt-0.5 block text-xs leading-snug text-zinc-400">{doc.hint}</span>
    </button>
  );
}

/* скелетон читаемого документа: строки вместо спиннера */
function DocSkeleton() {
  return (
    <div className="space-y-3 py-6" aria-busy="true" aria-hidden>
      <div className="t5-skel mb-6 h-5 w-52" />
      {Array.from({ length: 9 }, (_, i) => (
        <div key={i} className="t5-skel h-3.5" style={{ width: `${58 + ((i * 13) % 38)}%` }} />
      ))}
    </div>
  );
}

function DocsView({ active, onActive }: { active: string; onActive: (name: string) => void }) {
  const [cache, setCache] = useState<Record<string, string>>({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const load = useCallback(async (name: string) => {
    if (cache[name]) return;
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`/api/t5/docs?name=${encodeURIComponent(name)}`);
      const data = (await res.json()) as { content?: string; error?: string };
      if (!res.ok || typeof data.content !== 'string') throw new Error(data.error ?? 'Документ не найден');
      setCache((c) => ({ ...c, [name]: data.content as string }));
    } catch (err) {
      setError(String(err instanceof Error ? err.message : err));
    } finally {
      setLoading(false);
    }
  }, [cache]);

  useEffect(() => {
    void load(active);
  }, [active, load]);

  const memoryDocs = T5_DOCS.filter((d) => d.group === 'memory');
  const arsDocs = T5_DOCS.filter((d) => d.group === 'ars');

  return (
    <div className="grid items-start gap-5 lg:grid-cols-[270px_1fr]">
      <nav
        aria-label="Документы памяти"
        className="t5-scroll space-y-1 lg:sticky lg:top-[84px] lg:max-h-[calc(100vh-110px)] lg:overflow-y-auto lg:pr-1"
      >
        <p className="t5-label px-3.5 pb-1.5">Память</p>
        {memoryDocs.map((d) => (
          <DocButton key={d.name} doc={d} active={active === d.name} onSelect={() => onActive(d.name)} />
        ))}
        <p className="t5-label px-3.5 pb-1.5 pt-5" style={{ color: 'var(--t5-violet)' }}>
          АРС · Планеты
        </p>
        {arsDocs.map((d) => (
          <DocButton key={d.name} doc={d} active={active === d.name} onSelect={() => onActive(d.name)} />
        ))}
      </nav>
      <div className="t5-panel t5-scroll min-h-[420px] overflow-y-auto rounded-xl p-6 lg:sticky lg:top-[84px] lg:max-h-[calc(100vh-110px)] lg:p-8">
        {loading && <DocSkeleton />}
        {error && !loading && <p className="text-sm text-red-400">{error}</p>}
        {!loading && !error && cache[active] && <T5Markdown content={cache[active]} />}
      </div>
    </div>
  );
}

export default function Home() {
  const [tab, setTab] = useState<Tab>('batches');
  const [view, setView] = useState<View>({ kind: 'list' });
  const [doc, setDoc] = useState<string>(DEFAULT_DOC);
  const [batches, setBatches] = useState<BatchListItem[]>([]);
  const [special, setSpecial] = useState<BatchListItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const syncHash = useCallback((next: string) => {
    try {
      if (window.location.hash !== `#${next}`) window.history.replaceState(null, '', `#${next}`);
    } catch {
      /* окружение без history — навигация просто не пишется */
    }
  }, []);

  /* deep-link: hash ↔ view, без перезагрузки */
  useEffect(() => {
    const apply = () => {
      const s = parseHash();
      setTab(s.tab);
      setView(s.view);
      setDoc(s.doc);
    };
    apply();
    window.addEventListener('hashchange', apply);
    return () => window.removeEventListener('hashchange', apply);
  }, []);

  /* батч из hash не нашёлся в списке → молча показываем список */
  useEffect(() => {
    if (loading) return;
    if (view.kind === 'batch' && !batches.some((b) => b.slug === view.slug)) {
      setView({ kind: 'list' });
      syncHash('batches');
    }
  }, [loading, view, batches, syncHash]);

  useEffect(() => {
    if (loading) return;
    if (view.kind === 'special' && !special.some((b) => b.slug === view.slug)) {
      setView({ kind: 'list' });
      syncHash('special');
    }
  }, [loading, view, special, syncHash]);

  const loadBatches = useCallback(async (soft: boolean) => {
    if (soft) setRefreshing(true);
    else setLoading(true);
    setError(null);
    try {
      const [res, sRes] = await Promise.all([fetch('/api/t5/batches'), fetch('/api/t5/special')]);
      const data = (await res.json()) as { batches?: BatchListItem[]; error?: string };
      if (!res.ok) throw new Error(data.error ?? 'Ошибка чтения');
      setBatches(data.batches ?? []);
      const sData = (await sRes.json()) as { special?: BatchListItem[] };
      setSpecial(sData.special ?? []);
    } catch (err) {
      setError(String(err instanceof Error ? err.message : err));
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }, []);

  useEffect(() => {
    void loadBatches(false);
  }, [loadBatches]);

  const openTab = (t: Tab) => {
    if (t === 'docs') {
      setTab('docs');
      syncHash(`memory/${doc}`);
      return;
    }
    setTab(t);
    setView({ kind: 'list' });
    syncHash(t);
  };

  const openBatch = (slug: string) => {
    setTab('batches');
    setView({ kind: 'batch', slug });
    syncHash(slug);
  };

  const openSpecial = (slug: string) => {
    setTab('special');
    setView({ kind: 'special', slug });
    syncHash(slug);
  };

  const backToList = () => {
    const t: Tab = view.kind === 'special' ? 'special' : 'batches';
    setTab(t);
    setView({ kind: 'list' });
    syncHash(t);
  };

  const openDoc = (name: string) => {
    setDoc(name);
    syncHash(`memory/${name}`);
  };

  /* статистика прилавка для героя — считается из живых списков */
  const stats = useMemo(() => {
    const slots = batches.reduce((acc, b) => acc + b.slotCount, 0);
    const verdicts = batches.reduce((acc, b) => acc + b.verdictCount, 0);
    const soSlots = special.reduce((acc, b) => acc + b.slotCount, 0);
    return {
      batches,
      special,
      batchStats: [
        { value: String(batches.length), label: 'батчей' },
        { value: String(slots), label: 'слотов' },
        { value: String(verdicts), label: 'вердиктов' },
        { value: String(special.length), label: 'SO-заказов' },
      ],
      specialStats: [
        { value: String(special.length), label: 'заказов' },
        { value: String(soSlots), label: 'слотов' },
        { value: String(special.reduce((acc, b) => acc + b.verdictCount, 0)), label: 'вердиктов' },
      ],
    };
  }, [batches, special]);

  const tabs: { id: Tab; label: string; icon: React.ReactNode }[] = [
    { id: 'batches', label: 'Батчи', icon: <Layers className="size-4" /> },
    { id: 'special', label: 'Special', icon: <Gift className="size-4" /> },
    { id: 'inbox', label: 'Инбокс', icon: <Inbox className="size-4" /> },
    { id: 'docs', label: 'Память', icon: <BookOpenText className="size-4" /> },
  ];

  return (
    <div className="t5-bg relative flex min-h-screen flex-col text-zinc-100">
      {/* глубина: сияния + виньетка + зерно */}
      <div className="t5-vignette" aria-hidden />
      <div className="t5-noise" aria-hidden />
      <div className="pointer-events-none fixed right-5 top-1/2 z-0 hidden -translate-y-1/2 xl:block" aria-hidden>
        <p className="t5-vertical font-mono text-[10px] tracking-[0.5em] text-white/[0.12]">
          スレッド・ファイブ — 五番目の糸
        </p>
      </div>

      {/* командная шапка: стекло + золотая кромка */}
      <header className="sticky top-0 z-20">
        <div className="border-b border-white/[0.06] bg-background/80 backdrop-blur-xl">
          <div className="mx-auto flex max-w-6xl flex-wrap items-center gap-x-3 gap-y-2 px-4 py-3 sm:gap-x-6 sm:px-6">
            <button type="button" onClick={() => openTab('batches')} className="flex items-center gap-3 rounded-lg focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-t5-accent" aria-label="Thread 5 — на главную">
              <span className="t5-glow inline-flex">
                <span className="t5-clip grid size-9 shrink-0 place-items-center bg-gradient-to-br from-[#f2c86f] via-[#d6973c] to-[#8a5a1e] font-display text-sm font-black text-[#241703]">
                  5
                </span>
              </span>
              <span className="leading-none">
                <span className="block font-display text-[13px] font-bold tracking-wider text-white">THREAD·5</span>
                <span className="mt-1 block font-mono text-[10px] tracking-[0.28em] text-zinc-500">прилавок писца</span>
              </span>
              <span className="ml-2 hidden font-mono text-[10px] tracking-[0.3em] text-white/[0.18] lg:inline" aria-hidden>
                スレッド・ファイブ
              </span>
            </button>

            <nav aria-label="Разделы" className="t5-seg ml-auto">
              {tabs.map((t) => {
                const active = tab === t.id;
                return (
                  <button
                    key={t.id}
                    type="button"
                    onClick={() => openTab(t.id)}
                    aria-current={active ? 'page' : undefined}
                    aria-label={t.label}
                    title={t.label}
                    data-active={active}
                    className={cn('t5-seg-item inline-flex items-center gap-1.5', !active && 'hover:!text-zinc-200')}
                  >
                    <span style={{ color: active ? TAB_ACCENT[t.id] : undefined }} className={cn(!active && 'text-zinc-600')}>
                      {t.icon}
                    </span>
                    <span className="hidden sm:inline">{t.label}</span>
                    {t.id === 'special' && <span className="hidden xl:inline">Orders</span>}
                  </button>
                );
              })}
            </nav>
          </div>
        </div>
        {/* градиентная кромка шапки: золото → малина → мята */}
        <div className="h-px w-full bg-gradient-to-r from-t5-accent/40 via-t5-rose/25 to-t5-mint/40" aria-hidden />
      </header>

      {/* содержимое */}
      <main className="relative z-10 mx-auto w-full max-w-6xl flex-1 px-4 py-7 sm:px-6 sm:py-9">
        {tab === 'batches' &&
          (view.kind === 'batch' ? (
            <BatchView slug={view.slug} onBack={backToList} />
          ) : loading ? (
            <div className="space-y-9">
              <ListSkeleton variant="batches" />
            </div>
          ) : error ? (
            <div className="t5-panel p-10 text-center text-sm text-red-400">{error}</div>
          ) : (
            <div className="space-y-9">
              <Hero
                accent="var(--t5-accent)"
                overline="Прилавок · конвейер"
                title="Батчи"
                sub="Тема рождается в чате — писец показывает контракт и кладёт батч на прилавок. Забирай POS/NEG в копировалку, вердикт оставляй автору."
                stats={stats.batchStats}
              />
              <BatchList items={batches} refreshing={refreshing} onRefresh={() => void loadBatches(true)} onOpen={openBatch} />
            </div>
          ))}
        {tab === 'special' &&
          (view.kind === 'special' ? (
            <BatchView slug={view.slug} source="special" onBack={backToList} />
          ) : loading ? (
            <div className="space-y-9">
              <ListSkeleton variant="special" />
            </div>
          ) : error ? (
            <div className="t5-panel p-10 text-center text-sm text-red-400">{error}</div>
          ) : (
            <div className="space-y-9">
              <Hero
                accent="var(--t5-rose)"
                overline="Прилавок · витрина"
                title="Special Orders"
                sub="Приколы, подарки и одиночные сцены вне конвейера: заказ звучит в чате, писец пишет промпт по доктрине — полка хранит готовое."
                stats={stats.specialStats}
              />
              <BatchList items={special} variant="special" refreshing={refreshing} onRefresh={() => void loadBatches(true)} onOpen={openSpecial} />
            </div>
          ))}
        {tab === 'inbox' && <InboxView />}
        {tab === 'docs' && <DocsView active={doc} onActive={openDoc} />}
      </main>

      {/* подвал — прилипает к низу */}
      <footer className="relative z-10 mt-auto border-t border-white/[0.06] pb-[env(safe-area-inset-bottom)]">
        <div className="mx-auto flex max-w-6xl flex-wrap items-end justify-between gap-x-8 gap-y-3 px-4 py-5 text-xs leading-relaxed text-zinc-500 sm:px-6">
          <div>
            <p className="flex flex-wrap items-center gap-x-1 font-mono">
              <span className="text-zinc-500">тема</span> <span className="text-t5-accent/70">→</span>
              <span className="text-zinc-500">контракт</span> <span className="text-zinc-600">→</span>
              <span className="text-zinc-500">батч</span> <span className="text-zinc-600">→</span>
              <span className="text-zinc-500">рендер</span> <span className="text-t5-accent/70">→</span>
              <span className="text-zinc-500">вердикт</span> <span className="text-t5-mint/60">→</span>
              <span className="text-zinc-500">вкус</span>
            </p>
            <p className="mt-1.5">Thread 5 · наследие Thread 4 (45 батчей, 28 законов вкуса) · чат — двигатель, файлы — память</p>
          </div>
          <p className="t5-label !tracking-[0.3em] text-white/[0.16]">五番目の糸 · thread five</p>
        </div>
      </footer>
    </div>
  );
}
