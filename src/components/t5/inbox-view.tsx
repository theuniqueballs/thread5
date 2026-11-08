'use client';

import { useCallback, useEffect, useRef, useState } from 'react';
import { Check, FileWarning, Inbox as InboxIcon, Loader2, ScanSearch, ShieldAlert, Sparkles, Trash2, UploadCloud } from 'lucide-react';
import { cn } from '@/lib/utils';
import { Chip } from '@/components/t5/bits';
import { Input } from '@/components/ui/input';
import type { InboxItem } from '@/lib/t5/inbox';

/**
 * ИНБОКС финальных рендеров (вердикт T5-16): автор закидывает итоги кучкой —
 * писец ищет артефакты/ошибки, которые автор не нашёл. X-фильтр-триаж стоит
 * ПЕРЕД всем: «x» уходит в карантин (fail-closed) и никогда не разбирается.
 */

const STATUS_META: Record<InboxItem['status'], { label: string; cls: string }> = {
  queued: { label: 'триаж…', cls: 'border-zinc-500/30 bg-zinc-500/10 text-zinc-300' },
  ok: { label: 'чистое — ждёт разбора', cls: 'border-emerald-400/35 bg-emerald-400/10 text-emerald-300' },
  x: { label: 'X · КАРАНТИН', cls: 'border-red-400/40 bg-red-400/10 text-red-300' },
  analyzed: { label: 'разобрано', cls: 'border-[#ffc24b]/40 bg-[#ffc24b]/10 text-[#ffc24b]' },
  error: { label: 'ошибка разбора', cls: 'border-orange-400/40 bg-orange-400/10 text-orange-300' },
};

const SEVERITY_LABEL: Record<string, string> = { clean: 'чисто', minor: 'мелочи', major: 'крупные дефекты' };

function fmtSize(n: number): string {
  return n > 1024 * 1024 ? `${(n / 1024 / 1024).toFixed(1)} МБ` : `${Math.round(n / 1024)} КБ`;
}

export function InboxView() {
  const [items, setItems] = useState<InboxItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [busy, setBusy] = useState<string | null>(null);
  const [message, setMessage] = useState<string | null>(null);
  const [tag, setTag] = useState('');
  const [dragOver, setDragOver] = useState(false);
  const [picked, setPicked] = useState<File[]>([]);
  const fileRef = useRef<HTMLInputElement>(null);

  const load = useCallback(async () => {
    try {
      const res = await fetch('/api/t5/inbox');
      const data = (await res.json()) as { items?: InboxItem[]; error?: string };
      setItems(data.items ?? []);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void load();
  }, [load]);

  const upload = useCallback(async () => {
    if (picked.length === 0 || busy) return;
    setBusy(`Заливаю ${picked.length} файл(ов) и гоню X-триаж…`);
    setMessage(null);
    try {
      const fd = new FormData();
      for (const f of picked) fd.append('files', f);
      if (tag.trim()) fd.append('tag', tag.trim());
      const res = await fetch('/api/t5/inbox', { method: 'POST', body: fd });
      const data = (await res.json()) as { uploaded?: number; failed?: number; items?: InboxItem[]; error?: string };
      if (!res.ok) throw new Error(data.error ?? 'загрузка не удалась');
      setItems(data.items ?? []);
      setPicked([]);
      if (fileRef.current) fileRef.current.value = '';
      setMessage(`Залито: ${data.uploaded ?? 0} · отсеяно X-фильтром/ошибками: ${data.failed ?? 0}`);
    } catch (err) {
      setMessage(`Ошибка: ${String(err instanceof Error ? err.message : err)}`);
    } finally {
      setBusy(null);
    }
  }, [picked, tag, busy]);

  const analyze = useCallback(async (ids?: string[]) => {
    if (busy) return;
    setBusy(ids ? 'Разбираю…' : 'Разбираю всё новое…');
    setMessage(null);
    try {
      const res = await fetch('/api/t5/inbox/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(ids ? { ids } : { action: 'analyze' }),
      });
      const data = (await res.json()) as { analyzed?: number; items?: InboxItem[]; error?: string };
      if (!res.ok) throw new Error(data.error ?? 'разбор не удался');
      setItems(data.items ?? []);
      setMessage(`Разобрано: ${data.analyzed ?? 0}`);
    } catch (err) {
      setMessage(`Ошибка: ${String(err instanceof Error ? err.message : err)}`);
    } finally {
      setBusy(null);
    }
  }, [busy]);

  const override = useCallback(async (id: string, label: 'sfw' | 'x') => {
    if (busy) return;
    setBusy(label === 'sfw' ? 'Разблокирую…' : 'Убираю в карантин…');
    try {
      const res = await fetch('/api/t5/inbox/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action: 'override', id, label }),
      });
      const data = (await res.json()) as { item?: InboxItem; error?: string };
      if (!res.ok) throw new Error(data.error ?? 'не вышло');
      setItems((list) => list.map((i) => (i.id === id && data.item ? data.item : i)));
    } catch (err) {
      setMessage(`Ошибка: ${String(err instanceof Error ? err.message : err)}`);
    } finally {
      setBusy(null);
    }
  }, [busy]);

  const onDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(false);
    const dropped = Array.from(e.dataTransfer.files ?? []).filter((f) => f.type.startsWith('image/'));
    if (dropped.length > 0) setPicked((p) => [...p, ...dropped]);
  }, []);

  const stats = {
    total: items.length,
    x: items.filter((i) => i.triage.label === 'x' && !i.authorOverride).length,
    pending: items.filter((i) => i.status === 'ok').length,
    analyzed: items.filter((i) => i.status === 'analyzed').length,
  };

  return (
    <div className="space-y-6" aria-label="Инбокс финальных рендеров">
      {/* загрузка кучкой */}
      <section
        onDragOver={(e) => {
          e.preventDefault();
          setDragOver(true);
        }}
        onDragLeave={() => setDragOver(false)}
        onDrop={onDrop}
        aria-label="Загрузка рендеров"
        className={cn(
          't5-panel rounded-2xl border-2 border-dashed p-6 transition-colors duration-150 sm:p-8',
          dragOver ? 'border-emerald-400/60 bg-emerald-400/[0.05]' : 'border-white/[0.1]',
        )}
      >
        <div className="flex flex-col gap-4 sm:flex-row sm:items-center">
          <div className="min-w-0 flex-1">
            <h2 className="flex items-center gap-2 text-lg font-bold text-white">
              <UploadCloud className="size-5 text-emerald-300" aria-hidden />
              Сбрось итоговые рендеры кучкой
            </h2>
            <p className="mt-1 text-sm leading-relaxed text-zinc-400">
              Перетащи файлы сюда или выбери вручную — png/jpg/webp, до 25 МБ каждый, до 40 за раз.
              Каждое изображение проходит X-фильтр: что отсечено — уходит в карантин и никогда не разбирается
              (fail-closed: сбой триажа = карантин). Остальное я разбираю на артефакты, анатомию, камеру и палитру.
            </p>
          </div>
          <div className="flex shrink-0 items-center gap-2">
            <Input
              ref={fileRef}
              type="file"
              multiple
              accept="image/png,image/jpeg,image/webp"
              onChange={(e) => setPicked(Array.from(e.target.files ?? []))}
              aria-label="Выбрать файлы"
              className="h-9 w-56 cursor-pointer text-xs text-zinc-300 file:mr-2 file:rounded-md file:border-0 file:bg-white/[0.07] file:px-2 file:py-1 file:text-xs file:text-zinc-200"
            />
            <button
              type="button"
              onClick={() => void upload()}
              disabled={picked.length === 0 || busy !== null}
              className="t5-btn shrink-0 disabled:opacity-40"
            >
              {busy ? <Loader2 className="size-3.5 animate-spin" /> : <UploadCloud className="size-3.5" />}
              {picked.length > 0 ? `Закинуть (${picked.length})` : 'Закинуть кучкой'}
            </button>
          </div>
        </div>
        <div className="mt-4 flex flex-wrap items-center gap-2.5">
          <label htmlFor="inbox-tag" className="font-mono text-[11px] uppercase tracking-widest text-zinc-500">
            Метка слота (необязательно)
          </label>
          <input
            id="inbox-tag"
            value={tag}
            onChange={(e) => setTag(e.target.value)}
            placeholder="T5-16 P28 — сверю рендер с промптом слота"
            className="h-8 w-64 rounded-lg border border-white/[0.09] bg-black/25 px-2.5 font-mono text-xs text-zinc-200 placeholder:text-zinc-600 focus-visible:border-emerald-400/50 focus-visible:outline-none"
          />
          {picked.length > 0 && (
            <Chip>
              {picked.length} файл(ов) выбрано · {fmtSize(picked.reduce((a, f) => a + f.size, 0))}
            </Chip>
          )}
        </div>
      </section>

      {/* статус-панель */}
      <section className="flex flex-wrap items-center gap-x-6 gap-y-2" aria-label="Статистика инбокса">
        <h2 className="flex items-center gap-2 text-sm font-bold text-zinc-200">
          <InboxIcon className="size-4 text-emerald-300" aria-hidden />
          Инбокс — {stats.total}
        </h2>
        <Chip>карантин X: {stats.x}</Chip>
        <Chip>ждут разбора: {stats.pending}</Chip>
        <Chip>разобрано: {stats.analyzed}</Chip>
        <button
          type="button"
          onClick={() => void analyze()}
          disabled={busy !== null || stats.pending === 0}
          className="t5-btn ml-auto disabled:opacity-40"
        >
          {busy ? <Loader2 className="size-3.5 animate-spin" /> : <ScanSearch className="size-3.5" />}
          Разобрать всё новое
        </button>
      </section>

      {busy && (
        <div className="flex items-center gap-2.5 rounded-xl border border-white/[0.08] bg-white/[0.03] px-4 py-3 text-sm text-zinc-300">
          <Loader2 className="size-4 animate-spin text-emerald-300" aria-hidden />
          {busy}
          <span className="text-xs text-zinc-500">триаж и разбор идут последовательно — не закрывай вкладку</span>
        </div>
      )}
      {message && !busy && <p className="text-sm text-zinc-400">{message}</p>}

      {/* журнал */}
      {loading ? (
        <div className="flex items-center justify-center py-16 text-sm text-zinc-500">
          <Loader2 className="mr-2.5 size-5 animate-spin text-emerald-300" /> Читаю журнал…
        </div>
      ) : items.length === 0 ? (
        <div className="t5-panel p-10 text-center">
          <Sparkles className="mx-auto mb-3 size-5 text-zinc-600" aria-hidden />
          <p className="mb-2 text-lg font-bold text-zinc-200">Инбокс пуст</p>
          <p className="mx-auto max-w-md text-sm leading-relaxed text-zinc-400">
            Заливай пачками после каждого прогона на PixAI — я записываю находки в журнал, а ты смотришь, что
            прошло мимо твоих глаз. Цикл «рендер → инбокс → находки → патчи промптов» и есть импрув воркфлоу.
          </p>
        </div>
      ) : (
        <div className="grid gap-3.5 sm:grid-cols-2 xl:grid-cols-3">
          {items.map((item) => {
            const meta = STATUS_META[item.status];
            const quarantined = item.triage.label === 'x' && item.authorOverride?.label !== 'sfw';
            return (
              <article
                key={item.id}
                className={cn(
                  't5-panel flex flex-col overflow-hidden rounded-xl p-0',
                  quarantined && 'border-red-400/25',
                )}
              >
                <div className="relative bg-black/40">
                  <img
                    src={`/api/t5/inbox/file?id=${item.id}`}
                    alt={quarantined ? 'Карантированное изображение (размыто)' : `Загруженный рендер ${item.origName}`}
                    className={cn('h-44 w-full object-cover', quarantined && 'blur-2xl scale-110 grayscale')}
                    loading="lazy"
                  />
                  <span className={cn('absolute left-2 top-2 rounded-md border px-1.5 py-0.5 font-mono text-[10px] font-bold', meta.cls)}>
                    {meta.label}
                  </span>
                  {item.tag && (
                    <span className="absolute right-2 top-2 rounded-md border border-white/[0.14] bg-black/70 px-1.5 py-0.5 font-mono text-[10px] text-cyan-200">
                      {item.tag}
                    </span>
                  )}
                </div>
                <div className="flex min-w-0 flex-1 flex-col gap-2 p-4">
                  <p className="truncate font-mono text-xs text-zinc-300" title={item.origName}>
                    {item.origName} · {fmtSize(item.size)}
                  </p>
                  <p className="text-xs leading-relaxed text-zinc-500">
                    {quarantined ? (
                      <span className="flex items-start gap-1.5 text-red-300/90">
                        <ShieldAlert className="mt-0.5 size-3.5 shrink-0" aria-hidden />
                        X-фильтр: {item.triage.reason}
                      </span>
                    ) : (
                      <>Триаж: {item.triage.label} — {item.triage.reason}</>
                    )}
                  </p>

                  {item.analysis && (
                    <div className="rounded-lg border border-white/[0.07] bg-black/25 p-2.5 text-xs leading-relaxed">
                      <p className="mb-1.5 flex items-center gap-1.5 font-bold text-[#ffc24b]">
                        <FileWarning className="size-3.5" aria-hidden />
                        Разбор: {SEVERITY_LABEL[item.analysis.severity] ?? item.analysis.severity}
                      </p>
                      {item.analysis.findings.length > 0 ? (
                        <ul className="space-y-1.5">
                          {item.analysis.findings.map((f, i) => (
                            <li key={i} className="text-zinc-400">
                              <span className="mr-1.5 rounded bg-white/[0.07] px-1 py-0.5 font-mono text-[10px] text-zinc-300">{f.kind}</span>
                              {f.what}
                              <span className="text-zinc-600"> · {f.where}</span>
                            </li>
                          ))}
                        </ul>
                      ) : (
                        <p className="text-zinc-500">Дефектов не нашлось</p>
                      )}
                      {item.analysis.note && <p className="mt-1.5 italic text-zinc-500">{item.analysis.note}</p>}
                    </div>
                  )}

                  <div className="mt-auto flex flex-wrap gap-1.5 pt-1">
                    {!quarantined && (
                      <button type="button" onClick={() => void analyze([item.id])} disabled={busy !== null} className="t5-btn !px-2 !py-1 !text-[11px] disabled:opacity-40">
                        <ScanSearch className="size-3" aria-hidden />
                        {item.analysis ? 'Переразобрать' : 'Разобрать'}
                      </button>
                    )}
                    {quarantined && (
                      <button type="button" onClick={() => void override(item.id, 'sfw')} disabled={busy !== null} className="t5-btn !px-2 !py-1 !text-[11px] disabled:opacity-40">
                        <Check className="size-3" aria-hidden />
                        Это чистое — разблокировать
                      </button>
                    )}
                    {!quarantined && item.triage.label !== 'x' && (
                      <button type="button" onClick={() => void override(item.id, 'x')} disabled={busy !== null} className="t5-btn !px-2 !py-1 !text-[11px] disabled:opacity-40" aria-label="Убрать в карантин вручную">
                        <Trash2 className="size-3" aria-hidden />
                        В карантин
                      </button>
                    )}
                  </div>
                </div>
              </article>
            );
          })}
        </div>
      )}
    </div>
  );
}
