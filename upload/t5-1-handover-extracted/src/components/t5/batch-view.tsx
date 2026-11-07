'use client';

import { useCallback, useEffect, useState } from 'react';
import { ArrowLeft, Check, ChevronRight, ClipboardList, Copy, Loader2, MessageSquareQuote, RotateCcw, Search, SearchX } from 'lucide-react';
import { Chip, CopyButton, GenreBadge, RatingBadge, copyText } from '@/components/t5/bits';
import { Input } from '@/components/ui/input';
import { cn } from '@/lib/utils';
import type { T5BatchBody, T5Slot } from '@/lib/t5/parse';

interface VerdictItem {
  file: string;
  slug: string;
  createdAt: string;
  text: string;
}

function TagBlock({ title, text }: { title: string; text: string }) {
  const isPos = title === 'POS';
  return (
    <div className="flex min-w-0 flex-col overflow-hidden rounded-lg border border-white/[0.07] bg-black/25">
      <div className="flex items-center justify-between border-b border-white/[0.06] px-3 py-2">
        <span className="flex items-center gap-2 font-mono text-[11px] font-bold tracking-[0.2em] text-zinc-300">
          <span className={cn('size-1.5 rounded-full', isPos ? 'bg-cyan-400' : 'bg-pink-500')} aria-hidden />
          {title}
        </span>
        <CopyButton text={text} label={title} className="!px-2 !py-1 !text-[11px]" />
      </div>
      <pre className="t5-scroll max-h-80 overflow-y-auto whitespace-pre-wrap break-words p-3 font-mono text-xs leading-relaxed text-zinc-300">
        {text}
      </pre>
    </div>
  );
}

function SlotCard({ slot }: { slot: T5Slot }) {
  const [openCanon, setOpenCanon] = useState(false);
  return (
    <article className="t5-panel p-5">
      <header className="mb-3 flex flex-wrap items-center gap-2">
        <span className="font-mono text-sm font-bold text-white">{slot.id}</span>
        <span className="font-mono text-[13px] text-zinc-400">— {slot.slug}</span>
        <span className="ml-auto flex flex-wrap items-center gap-1.5">
          <CopyButton
            text={`${slot.id} — ${slot.slug}\nPOS: ${slot.pos}\n\nNEG: ${slot.neg}`}
            label="Слот"
          />
          <GenreBadge genre={slot.genre} />
          {slot.character && <Chip>{slot.character}</Chip>}
          <RatingBadge rating={slot.rating} />
          {slot.pose && <Chip>{slot.pose}</Chip>}
          {slot.palette && <Chip>{slot.palette}</Chip>}
          {slot.experimental && (
            <span title="экспериментальный слот" className="inline-flex items-center rounded-md border border-cyan-400/40 bg-cyan-400/[0.08] px-1.5 py-0.5 font-mono text-[10px] font-bold text-cyan-300">
              ⚗ EXP
            </span>
          )}
          {slot.expLetter && (
            <Chip>
              EXP {slot.expLetter}-{slot.expHalf}
            </Chip>
          )}
        </span>
      </header>

      {slot.thesis && (
        <p className="mb-2.5 border-l-2 border-pink-500/70 pl-3 text-sm italic leading-relaxed text-zinc-300">
          <span className="mr-1.5 font-sans text-[11px] font-bold not-italic uppercase tracking-widest text-pink-400">thesis</span>
          {slot.thesis}
        </p>
      )}
      {slot.spine && (
        <p className="mb-1 font-mono text-xs leading-relaxed text-zinc-500">
          <span className="font-semibold text-zinc-400">Spine:</span> {slot.spine}
        </p>
      )}
      {slot.stackIds.length > 0 && (
        <p className="mb-1 font-mono text-xs text-zinc-500">
          <span className="font-semibold text-zinc-400">Stack:</span> {slot.stackIds.join(' + ')}
        </p>
      )}
      {slot.canon && (
        <div className="mb-2.5">
          <button
            type="button"
            onClick={() => setOpenCanon((v) => !v)}
            aria-expanded={openCanon}
            className="text-xs font-semibold text-cyan-300/80 underline decoration-dotted underline-offset-2 transition-colors hover:text-cyan-200"
          >
            Canon {openCanon ? '▲' : '▼'}
          </button>
          {openCanon && <p className="mt-1.5 rounded-lg border border-white/[0.07] bg-black/25 p-2.5 font-mono text-xs leading-relaxed text-zinc-400">{slot.canon}</p>}
        </div>
      )}

      <div className="grid gap-3 lg:grid-cols-2">
        <TagBlock title="POS" text={slot.pos} />
        <TagBlock title="NEG" text={slot.neg} />
      </div>
    </article>
  );
}

interface SlotMarks {
  pos: boolean;
  neg: boolean;
}

type MarkKind = keyof SlotMarks;

/* POS/NEG кнопка копировалки: зелёная навсегда, пока слот не отработан */
function PartButton({ text, label, copied, onCopied, ariaLabel }: { text: string; label: string; copied: boolean; onCopied: () => void; ariaLabel?: string }) {
  const [done, setDone] = useState(false);
  const onCopy = useCallback(async () => {
    const ok = await copyText(text);
    if (ok) {
      setDone(true);
      window.setTimeout(() => setDone(false), 1400);
      onCopied();
    }
  }, [text, onCopied]);
  const lit = copied || done;
  return (
    <button
      type="button"
      onClick={onCopy}
      aria-label={ariaLabel ?? `Скопировать ${label} слота`}
      aria-pressed={copied}
      className={cn(
        'inline-flex min-h-8 items-center gap-1 rounded-md border px-2.5 py-1 font-mono text-[11px] font-bold tracking-wider transition-all duration-150 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-emerald-500',
        lit
          ? 'border-emerald-500/50 bg-emerald-500/[0.12] text-emerald-300'
          : 'border-white/[0.09] bg-white/[0.04] text-zinc-400 hover:border-white/25 hover:bg-white/[0.07] hover:text-white'
      )}
    >
      {lit ? <Check className="size-3" /> : <Copy className="size-3" />}
      {done ? 'Ок' : label}
    </button>
  );
}

function CopyRow({ slot, marks, onMark }: { slot: T5Slot; marks: SlotMarks; onMark: (kind: MarkKind) => void }) {
  const full = marks.pos && marks.neg;
  const part = !full && (marks.pos || marks.neg);
  return (
    <div
      className={cn(
        'relative flex flex-wrap items-center gap-x-2.5 gap-y-1.5 px-3 py-2 transition-colors sm:flex-nowrap sm:px-4',
        full
          ? 'bg-emerald-500/[0.05]'
          : part
            ? 'bg-white/[0.015]'
            : 'hover:bg-white/[0.025]'
      )}
    >
      {/* статус-рельса строки */}
      <span
        aria-hidden
        className={cn(
          'absolute inset-y-0 left-0 w-[2.5px] transition-colors',
          full ? 'bg-emerald-400' : part ? 'bg-emerald-400/35' : 'bg-transparent'
        )}
      />
      <span
        className={cn(
          'ml-1 flex w-10 shrink-0 items-center gap-0.5 font-mono text-[13px] font-bold',
          full ? 'text-emerald-300' : 'text-zinc-200'
        )}
      >
        {slot.id}
        {full && <Check className="size-3" aria-hidden />}
      </span>
      <GenreBadge genre={slot.genre} />
      <RatingBadge rating={slot.rating} />
      <span className="min-w-0 flex-1 truncate font-mono text-xs text-zinc-500" title={slot.slug}>
        {slot.slug}
      </span>
      <span className="flex shrink-0 items-center gap-1.5">
        <PartButton text={slot.pos} label="POS" copied={marks.pos} onCopied={() => onMark('pos')} />
        <PartButton text={slot.neg} label="NEG" copied={marks.neg} onCopied={() => onMark('neg')} />
        <PartButton
          text={`POS:\n${slot.pos}\n\nNEG:\n${slot.neg}`}
          label="Оба"
          copied={full}
          ariaLabel="Скопировать POS и NEG слота одной связкой"
          onCopied={() => {
            onMark('pos');
            onMark('neg');
          }}
        />
      </span>
    </div>
  );
}

/* ── фильтры копировалки ──────────────────────────────────────────── */

type StatusFilter = 'all' | 'todo' | 'done';

const GENRE_ORDER = ['OC', 'NICHE', 'VOLT', 'EXQUISITE', 'EXP'] as const;
const RATING_ORDER = ['R+', 'R', 'PG-13', 'X'] as const;

function FilterChip({ active, onClick, children }: { active: boolean; onClick: () => void; children: React.ReactNode }) {
  return (
    <button
      type="button"
      onClick={onClick}
      aria-pressed={active}
      className={cn(
        'inline-flex min-h-8 items-center rounded-md border px-2.5 py-1 font-mono text-[11px] font-bold tracking-wider transition-all duration-150 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-pink-400',
        active
          ? 'border-pink-500/50 bg-pink-500/[0.12] text-pink-200'
          : 'border-white/[0.08] bg-white/[0.03] text-zinc-500 hover:border-white/20 hover:text-zinc-300'
      )}
    >
      {children}
    </button>
  );
}

function StatusToggle({ value, active, onClick }: { value: StatusFilter; active: boolean; onClick: () => void }) {
  const labels: Record<StatusFilter, string> = { all: 'Все', todo: 'Несделанные', done: 'Сделанные' };
  return (
    <button
      type="button"
      onClick={onClick}
      aria-pressed={active}
      className={cn(
        'rounded-lg px-2.5 py-1.5 text-xs font-semibold transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-pink-400',
        active ? 'bg-white/[0.08] text-white' : 'text-zinc-500 hover:text-zinc-300'
      )}
    >
      {labels[value]}
    </button>
  );
}

function CopyWorkbench({ batch }: { batch: T5BatchBody }) {
  const storeKey = `t5-copied:${batch.slug}`;
  const [marks, setMarks] = useState<Record<string, SlotMarks>>({});
  const [ready, setReady] = useState(false);
  const [genreFilter, setGenreFilter] = useState<string | null>(null);
  const [ratingFilter, setRatingFilter] = useState<string | null>(null);
  const [statusFilter, setStatusFilter] = useState<StatusFilter>('all');
  const [query, setQuery] = useState('');

  useEffect(() => {
    let alive = true;
    void (async () => {
      await Promise.resolve(); // асинхронно: отметки нужны только после гидрации
      if (!alive) return;
      try {
        const raw = window.localStorage.getItem(storeKey);
        setMarks(raw ? (JSON.parse(raw) as Record<string, SlotMarks>) : {});
      } catch {
        setMarks({});
      }
      setReady(true);
    })();
    return () => {
      alive = false;
    };
  }, [storeKey]);

  const mark = useCallback(
    (slotId: string, kind: MarkKind) => {
      setMarks((prev) => {
        const prevMarks = prev[slotId] ?? { pos: false, neg: false };
        const next = { ...prev, [slotId]: { ...prevMarks, [kind]: true } };
        try {
          window.localStorage.setItem(storeKey, JSON.stringify(next));
        } catch {
          /* приватный режим — отметки живут до перезагрузки */
        }
        return next;
      });
    },
    [storeKey]
  );

  const clear = useCallback(() => {
    setMarks({});
    try {
      window.localStorage.removeItem(storeKey);
    } catch {
      /* ignore */
    }
  }, [storeKey]);

  const allPos = batch.slots.map((s) => `${s.id} POS\n${s.pos}`).join('\n\n');
  const allNeg = batch.slots.map((s) => `${s.id} NEG\n${s.neg}`).join('\n\n');
  const doneCount = batch.slots.filter((s) => {
    const m = marks[s.id];
    return m?.pos && m?.neg;
  }).length;
  const total = batch.slots.length;
  const progressPct = total === 0 ? 0 : Math.round((doneCount / total) * 100);

  // фильтры: только жанры/тиры, которые реально есть в батче
  const presentGenres = GENRE_ORDER.filter((g) => batch.slots.some((s) => s.genre === g));
  const presentRatings = RATING_ORDER.filter((r) => batch.slots.some((s) => s.rating === r));

  const q = query.trim().toLowerCase();
  const visible = batch.slots.filter((s) => {
    if (genreFilter && s.genre !== genreFilter) return false;
    if (ratingFilter && s.rating !== ratingFilter) return false;
    const m = marks[s.id];
    const done = Boolean(m?.pos && m?.neg);
    if (statusFilter === 'todo' && done) return false;
    if (statusFilter === 'done' && !done) return false;
    if (q && !s.id.toLowerCase().includes(q) && !s.slug.toLowerCase().includes(q)) return false;
    return true;
  });

  return (
    <section aria-label="Копировалка" className="t5-panel overflow-hidden">
      <div className="flex flex-wrap items-center gap-2 border-b border-white/[0.06] px-4 py-3">
        <h3 className="t5-label mr-auto flex items-center gap-2.5 !text-[11px] text-zinc-300">
          <ClipboardList className="size-4 text-cyan-300" /> Копировалка · {total}
        </h3>
        <Chip>
          готово {doneCount}/{total}
        </Chip>
        <CopyButton text={allPos} label={`Все POS (${total})`} />
        <CopyButton text={allNeg} label={`Все NEG (${total})`} />
        {ready && doneCount > 0 && (
          <button type="button" onClick={clear} title="Снять зелёные отметки этого батча" className="t5-btn">
            <RotateCcw className="size-3.5" /> Сброс
          </button>
        )}
      </div>

      {/* прогресс: единственная дышащая точка панели */}
      <div className="border-b border-white/[0.06] px-4 py-2.5">
        <div
          role="progressbar"
          aria-valuemin={0}
          aria-valuemax={total}
          aria-valuenow={doneCount}
          aria-label={`Готово ${doneCount} из ${total} слотов`}
          className="h-1 w-full overflow-hidden rounded-full bg-white/[0.06]"
        >
          <div
            className="h-full rounded-full bg-gradient-to-r from-[#ff3d8a] to-[#d946ef] shadow-[0_0_10px_rgb(255_61_138/0.45)] transition-[width] duration-300"
            style={{ width: `${progressPct}%` }}
          />
        </div>
      </div>

      {/* фильтры: жанр · тир · статус · поиск */}
      <div className="space-y-2 border-b border-white/[0.06] px-4 py-3">
        {(presentGenres.length > 0 || presentRatings.length > 0) && (
          <div className="flex flex-wrap items-center gap-1.5">
            {presentGenres.map((g) => (
              <FilterChip key={g} active={genreFilter === g} onClick={() => setGenreFilter((cur) => (cur === g ? null : g))}>
                {g}
              </FilterChip>
            ))}
            <span className="mx-1 h-4 w-px bg-white/10" aria-hidden />
            {presentRatings.map((r) => (
              <FilterChip key={r} active={ratingFilter === r} onClick={() => setRatingFilter((cur) => (cur === r ? null : r))}>
                {r}
              </FilterChip>
            ))}
          </div>
        )}
        <div className="flex flex-wrap items-center gap-2">
          <div className="flex rounded-xl border border-white/[0.07] bg-white/[0.03] p-1" role="group" aria-label="Фильтр по отметкам копировалки">
            {(['all', 'todo', 'done'] as const).map((v) => (
              <StatusToggle key={v} value={v} active={statusFilter === v} onClick={() => setStatusFilter(v)} />
            ))}
          </div>
          <div className="relative ml-auto w-full sm:w-52">
            <Search className="pointer-events-none absolute left-2.5 top-1/2 size-3.5 -translate-y-1/2 text-zinc-600" aria-hidden />
            <Input
              type="search"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Поиск: P01, slug…"
              aria-label="Поиск слота по ID или слагу"
              className="h-8 rounded-lg border-white/[0.09] bg-black/25 pl-8 text-xs text-zinc-200 shadow-none placeholder:text-zinc-600 focus-visible:border-pink-500/50 focus-visible:ring-pink-500/25"
            />
          </div>
        </div>
      </div>

      <div className="divide-y divide-white/[0.045]">
        {visible.length === 0 ? (
          <p className="flex items-center justify-center gap-2 py-10 text-sm text-zinc-500">
            <SearchX className="size-4" aria-hidden /> Ничего не совпало
          </p>
        ) : (
          visible.map((slot) => (
            <CopyRow
              key={slot.id}
              slot={slot}
              marks={marks[slot.id] ?? { pos: false, neg: false }}
              onMark={(kind) => mark(slot.id, kind)}
            />
          ))
        )}
      </div>
    </section>
  );
}

function ViewToggle({ view, onChange }: { view: 'copy' | 'detail'; onChange: (v: 'copy' | 'detail') => void }) {
  const base =
    'rounded-lg px-3 py-1.5 text-[13px] font-semibold transition-all duration-150 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-pink-400';
  return (
    <div className="flex rounded-xl border border-white/[0.07] bg-white/[0.03] p-1" role="tablist" aria-label="Вид батча">
      <button type="button" role="tab" aria-selected={view === 'copy'} onClick={() => onChange('copy')} className={cn(base, view === 'copy' ? 'bg-[#1d1c29] text-white shadow-[inset_0_1px_0_rgb(255_255_255/0.06)]' : 'text-zinc-500 hover:text-zinc-200')}>
        Копировалка
      </button>
      <button type="button" role="tab" aria-selected={view === 'detail'} onClick={() => onChange('detail')} className={cn(base, view === 'detail' ? 'bg-[#1d1c29] text-white shadow-[inset_0_1px_0_rgb(255_255_255/0.06)]' : 'text-zinc-500 hover:text-zinc-200')}>
        Разбор
      </button>
    </div>
  );
}

/* ── ленивый «Батч целиком»: raw дожимается по ?raw=1 при первом клике ── */

function LazyCopyButton({ getText, label }: { getText: () => Promise<string | null>; label: string }) {
  const [done, setDone] = useState(false);
  const [busy, setBusy] = useState(false);
  const onClick = useCallback(async () => {
    if (busy) return;
    setBusy(true);
    try {
      const text = await getText();
      if (text && (await copyText(text))) {
        setDone(true);
        window.setTimeout(() => setDone(false), 1400);
      }
    } finally {
      setBusy(false);
    }
  }, [busy, getText]);
  return (
    <button type="button" onClick={onClick} disabled={busy} aria-label={label} className="t5-btn">
      {busy ? <Loader2 className="size-3.5 animate-spin" /> : done ? <Check className="size-3.5 text-emerald-400" /> : <Copy className="size-3.5" />}
      {busy ? 'Читаю…' : done ? 'Скопировано' : label}
    </button>
  );
}

function VerdictBox({ slug, onSaved }: { slug: string; onSaved: () => void }) {
  const [text, setText] = useState('');
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const save = useCallback(async () => {
    if (text.trim().length < 2) {
      setError('Вердикт пустой');
      return;
    }
    setSaving(true);
    setError(null);
    try {
      const res = await fetch('/api/t5/verdicts', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ slug, text }),
      });
      const data = (await res.json()) as { error?: string };
      if (!res.ok) throw new Error(data.error ?? 'Ошибка сохранения');
      setText('');
      onSaved();
    } catch (err) {
      setError(String(err instanceof Error ? err.message : err));
    } finally {
      setSaving(false);
    }
  }, [slug, text, onSaved]);

  return (
    <section aria-label="Вердикт" className="overflow-hidden rounded-xl border border-[#ffc24b]/25 bg-[#16120a]/70">
      {/* hazard-полоса: голос автора — единственный золотой блок интерфейса */}
      <div className="t5-hazard h-1 w-full opacity-60" aria-hidden />
      <div className="p-5">
        <h3 className="mb-1.5 flex items-center gap-2.5 font-display text-[13px] font-bold tracking-wider text-[#ffc24b]">
          <MessageSquareQuote className="size-4" /> ВЕРДИКТ АВТОРА — {slug}
        </h3>
        <p className="mb-3.5 text-xs leading-relaxed text-zinc-400">
          Что сработало / что умерло, по слотам или в целом. Писец разберёт вердикт в чате и разложит квитанции в память.
        </p>
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          rows={5}
          placeholder={'P09 — сумма слоёв доезжает, свет на зоне — огонь.\nP14 — поза HIGH, заявку съел дрейф…'}
          className="w-full rounded-lg border border-white/[0.09] bg-black/30 p-3.5 text-sm leading-relaxed text-zinc-200 shadow-[inset_0_1px_3px_rgb(0_0_0/0.35)] placeholder:text-zinc-600 focus:border-[#ffc24b]/50 focus:outline-none focus:ring-1 focus:ring-[#ffc24b]/30"
        />
        {error && <p className="mt-2 text-xs text-red-400">{error}</p>}
        <div className="mt-4 flex flex-wrap items-center gap-3">
          <span className="t5-glow inline-flex">
            <button type="button" onClick={save} disabled={saving} className="t5-btn-primary t5-clip">
              {saving ? <Loader2 className="size-4 animate-spin" /> : null}
              Сохранить вердикт
            </button>
          </span>
          <span className="text-xs text-zinc-600">вербатим в verdicts/ — писец заберёт из чата</span>
        </div>
      </div>
    </section>
  );
}

/* чип акта: «ACT I — ВЕРХНИЙ ЯРУС (световод, …)» → «ACT I — ВЕРХНИЙ ЯРУС» */
function shortActTitle(title: string): string {
  const base = title.split(' (')[0].trim();
  return base.length > 42 ? `${base.slice(0, 41)}…` : base;
}

export function BatchView({ slug, onBack, source = 'batches' }: { slug: string; onBack: () => void; source?: 'batches' | 'special' }) {
  const [batch, setBatch] = useState<T5BatchBody | null>(null);
  const [verdicts, setVerdicts] = useState<VerdictItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [view, setView] = useState<'copy' | 'detail'>('copy');
  const [rawText, setRawText] = useState<string | null>(null);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    setRawText(null); // raw перечитаем лениво при следующем клике
    try {
      const [bRes, vRes] = await Promise.all([fetch(`/api/t5/${source}/${slug}`), fetch(`/api/t5/verdicts?slug=${encodeURIComponent(slug)}`)]);
      const bData = (await bRes.json()) as { batch?: T5BatchBody; error?: string };
      if (!bRes.ok || !bData.batch) throw new Error(bData.error ?? 'Не найдено');
      setBatch(bData.batch);
      const vData = (await vRes.json()) as { verdicts?: VerdictItem[] };
      setVerdicts(vData.verdicts ?? []);
    } catch (err) {
      setError(String(err instanceof Error ? err.message : err));
    } finally {
      setLoading(false);
    }
  }, [slug, source]);

  useEffect(() => {
    void load();
  }, [load]);

  const fetchRaw = useCallback(async (): Promise<string | null> => {
    if (rawText) return rawText;
    try {
      const res = await fetch(`/api/t5/${source}/${slug}?raw=1`);
      const data = (await res.json()) as { batch?: { raw?: string }; error?: string };
      if (!res.ok || !data.batch?.raw) return null;
      setRawText(data.batch.raw);
      return data.batch.raw;
    } catch {
      return null;
    }
  }, [rawText, source, slug]);

  if (loading) {
    return (
      <div className="flex items-center justify-center py-28 text-sm text-zinc-500">
        <Loader2 className="mr-2.5 size-5 animate-spin text-pink-400" /> Читаю материал…
      </div>
    );
  }
  if (error || !batch) {
    return (
      <div className="t5-panel py-14 text-center">
        <p className="mb-5 text-sm text-red-400">{error ?? 'Не найдено'}</p>
        <button type="button" onClick={onBack} className="t5-btn">
          <ArrowLeft className="size-4" /> К списку
        </button>
      </div>
    );
  }

  const verdictSlots = verdicts.length;
  const detailActs = batch.acts.filter((act) => act.slots.length > 0);

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-center gap-x-3 gap-y-2">
        <button type="button" onClick={onBack} className="t5-btn">
          <ArrowLeft className="size-4" /> Список
        </button>
        <ViewToggle view={view} onChange={setView} />
        <span className="ml-auto">
          <LazyCopyButton getText={fetchRaw} label={source === 'special' ? 'Заказ целиком' : 'Батч целиком'} />
        </span>
      </div>

      {/* шапка батча */}
      <header className="t5-panel relative overflow-hidden p-6">
        <span
          aria-hidden
          className="absolute inset-y-0 left-0 w-[3px]"
          style={{ background: source === 'special' ? 'linear-gradient(180deg,#2de2e6,rgba(45,226,230,0.1))' : 'linear-gradient(180deg,#ff3d8a,rgba(255,61,138,0.1))' }}
        />
        <h2 className="mb-1.5 pl-2.5 font-display text-lg font-bold leading-snug text-white sm:text-xl">{batch.title}</h2>
        {batch.theme && <p className="mb-3.5 pl-2.5 text-sm text-zinc-400">Тема: <span className="text-zinc-200">«{batch.theme}»</span></p>}
        <div className="mb-4 flex flex-wrap gap-1.5 pl-2.5">
          <Chip>{batch.slots.length} слотов</Chip>
          {batch.slots.some((s) => s.genre === 'OC') && <Chip>OC {batch.slots.filter((s) => s.genre === 'OC').length}</Chip>}
          {batch.slots.some((s) => s.genre === 'EXP') && <Chip>EXP {batch.slots.filter((s) => s.genre === 'EXP').length}</Chip>}
          <Chip>вердиктов: {verdictSlots}</Chip>
        </div>
        {batch.arc && <p className="mb-4 max-w-4xl pl-2.5 text-sm italic leading-relaxed text-zinc-500">{batch.arc}</p>}
        <dl className="grid gap-2 pl-2.5 text-[13px] text-zinc-400">
          {batch.movement && (
            <div>
              <dt className="t5-label mr-2 inline">Движок</dt>
              <dd className="inline">{batch.movement}</dd>
            </div>
          )}
          {batch.themeWords.length > 0 && (
            <div>
              <dt className="t5-label mr-2 inline">Тема-слова</dt>
              <dd className="inline-flex flex-wrap gap-1 align-middle">
                {batch.themeWords.map((w) => (
                  <Chip key={w}>{w}</Chip>
                ))}
              </dd>
            </div>
          )}
          {batch.structure && (
            <div>
              <dt className="t5-label mr-2 inline">Структура</dt>
              <dd className="inline">{batch.structure}</dd>
            </div>
          )}
          {batch.protocol && (
            <div>
              <dt className="t5-label mr-2 inline">Render protocol</dt>
              <dd className="inline">{batch.protocol}</dd>
            </div>
          )}
        </dl>
      </header>

      {/* копировалка или детальный разбор */}
      {view === 'copy' ? (
        <CopyWorkbench batch={batch} />
      ) : detailActs.length > 0 ? (
        <>
          {/* лента якорей актов */}
          <nav aria-label="Переход к акту" className="t5-scroll -mx-1 flex gap-2 overflow-x-auto px-1 pb-1">
            {detailActs.map((act, i) => (
              <button
                key={act.title}
                type="button"
                onClick={() => document.getElementById(`t5-act-${i}`)?.scrollIntoView({ behavior: 'smooth', block: 'start' })}
                className="t5-btn shrink-0 whitespace-nowrap !rounded-lg font-semibold"
              >
                {shortActTitle(act.title)}
              </button>
            ))}
          </nav>
          {detailActs.map((act, i) => (
            <section key={act.title} id={`t5-act-${i}`} aria-label={act.title} className="scroll-mt-24">
              <h3 className="mb-4 mt-2 flex items-center gap-3">
                <span className="h-px flex-1 bg-gradient-to-r from-transparent to-white/15" aria-hidden />
                <span className="t5-label text-zinc-300">{act.title}</span>
                <span className="h-px flex-1 bg-gradient-to-l from-transparent to-white/15" aria-hidden />
              </h3>
              <div className="space-y-4">
                {act.slots.map((slot) => (
                  <SlotCard key={slot.id} slot={slot} />
                ))}
              </div>
            </section>
          ))}
        </>
      ) : (
        <div className="space-y-4">
          {batch.slots.map((slot) => (
            <SlotCard key={slot.id} slot={slot} />
          ))}
        </div>
      )}

      {/* вердикты */}
      <VerdictBox slug={slug} onSaved={load} />
      {verdicts.length > 0 && (
        <section aria-label="Сохранённые вердикты" className="t5-panel p-5">
          <h3 className="t5-label mb-3.5 text-zinc-400">Сохранённые вердикты — {verdicts.length}</h3>
          <div className="space-y-2">
            {verdicts.map((v) => (
              <details key={v.file} className="group rounded-lg border border-white/[0.07] bg-black/25">
                <summary className="cursor-pointer list-none px-3.5 py-2.5 text-xs text-zinc-500 transition-colors hover:text-zinc-200">
                  <ChevronRight className="mr-1.5 inline size-3 rotate-0 transition-transform group-open:rotate-90" aria-hidden />
                  <span className="mr-2 inline-block h-1.5 w-1.5 rounded-full bg-[#ffc24b]/70 align-middle" aria-hidden />
                  <span className="font-mono text-zinc-300">{v.file}</span> · {v.createdAt || '—'}
                </summary>
                <pre className="t5-scroll max-h-96 overflow-y-auto whitespace-pre-wrap break-words border-t border-white/[0.06] p-3.5 font-mono text-xs leading-relaxed text-zinc-300">
                  {v.text}
                </pre>
              </details>
            ))}
          </div>
        </section>
      )}
    </div>
  );
}
