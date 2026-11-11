'use client';

import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import {
  Check,
  ChevronLeft,
  ChevronRight,
  Eraser,
  FileWarning,
  Inbox as InboxIcon,
  ListOrdered,
  Loader2,
  Maximize2,
  RefreshCcw,
  ScanSearch,
  ShieldAlert,
  Sparkles,
  Trash2,
  UploadCloud,
  X,
} from 'lucide-react';
import { cn } from '@/lib/utils';
import { Chip } from '@/components/t5/bits';
import { Input } from '@/components/ui/input';
import type { InboxItem } from '@/lib/t5/inbox';

/**
 * ИНБОКС финальных рендеров (вердикт T5-16): автор закидывает итоги кучкой —
 * писец ищет артефакты/ошибки, которые автор не нашёл. X-фильтр-триаж стоит
 * ПЕРЕД разбором: «x» уходит в карантин (fail-closed) и никогда не разбирается.
 *
 * Урок T5-17 («перепиздячились слотами»): слот проставляется ПОФАЙЛОВО —
 * сам вытаскивается из имени (P07 / 07 - name.webp), правится руками и
 * проставляется по порядку одной кнопкой. Файлы хранятся на диске до явной
 * очистки — писец видит пачку между сессиями и читает её по слотам подряд.
 *
 * Урок T5-19 (401 «missing X-Token»): триаж, оборванный сбоем шлюза, остаётся
 * в очереди — поэтому инбокс ДОГОНЯЕТ триаж сам при открытии, без кнопки.
 *
 * Архитектура против «Unexpected token '<'»: загрузка, триаж и разбор —
 * короткие порционные запросы (шлюз не успевает уйти в HTML-таймаут),
 * а readJson() ругается по-человечески, если всё же пришёл HTML.
 */

const STATUS_META: Record<InboxItem['status'], { label: string; cls: string; dot: string }> = {
  queued: { label: 'ждёт X-триаж', cls: 'border-zinc-500/30 bg-zinc-500/10 text-zinc-300', dot: 'bg-zinc-400' },
  ok: { label: 'чистое — ждёт разбора', cls: 'border-emerald-400/35 bg-emerald-400/10 text-emerald-300', dot: 'bg-emerald-400' },
  x: { label: 'X · КАРАНТИН', cls: 'border-red-400/40 bg-red-400/10 text-red-300', dot: 'bg-red-400' },
  analyzed: { label: 'разобрано', cls: 'border-[#ffc24b]/40 bg-[#ffc24b]/10 text-[#ffc24b]', dot: 'bg-[#ffc24b]' },
  error: { label: 'ошибка разбора', cls: 'border-orange-400/40 bg-orange-400/10 text-orange-300', dot: 'bg-orange-400' },
};

const SEVERITY_LABEL: Record<string, string> = { clean: 'чисто', minor: 'мелочи', major: 'крупные дефекты' };
const SEVERITY_CLS: Record<string, string> = {
  clean: 'border-emerald-400/35 bg-emerald-400/[0.08] text-emerald-300',
  minor: 'border-[#ffc24b]/40 bg-[#ffc24b]/[0.08] text-[#ffc24b]',
  major: 'border-red-400/40 bg-red-400/[0.08] text-red-300',
};

const MAX_FILE_MB = 25;
const ALLOWED_EXT = ['png', 'jpg', 'jpeg', 'webp'];
const UPLOAD_CHUNK = 8; // файлов за один POST — короткие запросы, шлюз не злится
const BATCH_STORAGE_KEY = 't5:inbox:batch';

/** JSON-парсер, который не давится HTML-страницей шлюза («Unexpected token '<'»). */
async function readJson<T>(res: Response): Promise<T> {
  const ctype = res.headers.get('content-type') ?? '';
  if (!ctype.includes('application/json')) {
    const head = (await res.text().catch(() => '')).replace(/\s+/gu, ' ').slice(0, 100);
    throw new Error(
      `сервер ответил ${res.status || '??'} не-JSON (${head || 'пустой ответ'}) — запрос упёрся в лимит/таймаут шлюза, пробуй меньшими пачками`,
    );
  }
  return (await res.json()) as T;
}

function fmtSize(n: number): string {
  return n > 1024 * 1024 ? `${(n / 1024 / 1024).toFixed(1)} МБ` : `${Math.round(n / 1024)} КБ`;
}

const RETRIAGE_RE = /fail-closed|429|too many|карантин/iu;

/** Слот из имени файла: «P07.webp», «t5-18 p7.png», «07 - name.webp» → «P07». */
function parseSlotFromName(name: string): string {
  const p = /(?:^|[^a-z0-9])P(\d{1,2})(?![a-z0-9])/iu.exec(name);
  const lead = /^(\d{1,2})(?:[\s_.-]|$)/u.exec(name);
  const m = p ?? lead;
  if (!m) return '';
  const n = Number.parseInt(m[1], 10);
  if (!Number.isInteger(n) || n < 1 || n > 99) return '';
  return `P${n < 10 ? `0${n}` : n}`;
}

function parseBatchFromName(name: string): string {
  const m = /T5-(\d{1,3})/iu.exec(name);
  return m ? `T5-${m[1]}` : '';
}

function normalizeSlotInput(v: string): string {
  const t = v.trim().toUpperCase().replace(/[^P0-9]/gu, '');
  const m = /^P?(\d{1,2})$/u.exec(t);
  if (!m) return '';
  const n = Number.parseInt(m[1], 10);
  if (n < 1 || n > 99) return '';
  return `P${n < 10 ? `0${n}` : n}`;
}

interface PickedFile {
  key: string;
  file: File;
  slot: string;
}

/* ── статус-пилюля: цветная точка + число, клик — фильтр статуса ───────── */

type StatusFilter = 'all' | InboxItem['status'];

function StatPill({
  dot,
  label,
  count,
  active,
  onClick,
}: {
  dot: string;
  label: string;
  count: number;
  active: boolean;
  onClick: () => void;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      aria-pressed={active}
      disabled={count === 0 && !active}
      className={cn(
        'inline-flex min-h-8 items-center gap-2 rounded-full border px-3 py-1 font-mono text-[11px] font-semibold transition-all duration-150 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-emerald-400/70 disabled:opacity-40',
        active
          ? 'border-white/[0.22] bg-white/[0.09] text-white shadow-[inset_0_1px_0_rgb(255_255_255/0.08)]'
          : 'border-white/[0.08] bg-white/[0.035] text-zinc-400 hover:border-white/[0.16] hover:text-zinc-200',
      )}
    >
      <span className={cn('size-1.5 shrink-0 rounded-full', dot)} aria-hidden />
      {label}
      <span className={cn('tabular-nums', active ? 'text-white' : 'text-zinc-500')}>{count}</span>
    </button>
  );
}

export function InboxView() {
  const [items, setItems] = useState<InboxItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [busy, setBusy] = useState<string | null>(null);
  const [message, setMessage] = useState<string | null>(null);
  const [batch, setBatch] = useState('');
  const [dragOver, setDragOver] = useState(false);
  const [picked, setPicked] = useState<PickedFile[]>([]);
  const [wipeArmed, setWipeArmed] = useState(false);
  const [statusFilter, setStatusFilter] = useState<StatusFilter>('all');
  const [lightbox, setLightbox] = useState<number | null>(null); // индекс в visibleItems
  const fileRef = useRef<HTMLInputElement>(null);
  const wipeTimer = useRef<ReturnType<typeof setTimeout> | null>(null);
  const autoTriageRef = useRef(false);

  const load = useCallback(async () => {
    try {
      const res = await fetch('/api/t5/inbox');
      const data = await readJson<{ items?: InboxItem[]; error?: string }>(res);
      setItems(data.items ?? []);
    } catch (err) {
      setMessage(`Журнал не прочитался: ${String(err instanceof Error ? err.message : err)}`);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void load();
    try {
      setBatch(localStorage.getItem(BATCH_STORAGE_KEY) ?? '');
    } catch {
      /* без localStorage — просто пустой батч */
    }
    return () => {
      if (wipeTimer.current) clearTimeout(wipeTimer.current);
    };
  }, [load]);

  const changeBatch = useCallback((v: string) => {
    setBatch(v);
    try {
      localStorage.setItem(BATCH_STORAGE_KEY, v);
    } catch {
      /* окружение без localStorage */
    }
  }, []);

  /* ── валидация файлов на клиенте: сразу видно, что отсеяно и почему ── */
  const addFiles = useCallback(
    (incoming: File[]) => {
      const ok: PickedFile[] = [];
      const bad: string[] = [];
      let batchHint = '';
      for (const f of incoming) {
        const ext = f.name.includes('.') ? (f.name.split('.').pop() ?? '').toLowerCase() : '';
        if (!ALLOWED_EXT.includes(ext)) {
          bad.push(`${f.name} — не png/jpg/webp`);
          continue;
        }
        if (f.size > MAX_FILE_MB * 1024 * 1024) {
          bad.push(`${f.name} — больше ${MAX_FILE_MB} МБ`);
          continue;
        }
        batchHint = batchHint || parseBatchFromName(f.name);
        ok.push({ key: `${f.name}:${f.size}:${Math.random().toString(36).slice(2, 7)}`, file: f, slot: parseSlotFromName(f.name) });
      }
      setPicked((prev) => {
        const seen = new Set(prev.map((p) => `${p.file.name}:${p.file.size}`));
        return [...prev, ...ok.filter((p) => !seen.has(`${p.file.name}:${p.file.size}`))];
      });
      if (batchHint && !batch) changeBatch(batchHint);
      setMessage(
        bad.length > 0
          ? `Пропущено: ${bad.slice(0, 4).join('; ')}${bad.length > 4 ? ` …и ещё ${bad.length - 4}` : ''}`
          : null,
      );
    },
    [batch, changeBatch],
  );

  const setPickedSlot = useCallback((key: string, slot: string) => {
    setPicked((prev) => prev.map((p) => (p.key === key ? { ...p, slot: normalizeSlotInput(slot) } : p)));
  }, []);

  const dropPicked = useCallback((key: string) => {
    setPicked((prev) => prev.filter((p) => p.key !== key));
  }, []);

  const clearPicked = useCallback(() => {
    setPicked([]);
    if (fileRef.current) fileRef.current.value = '';
  }, []);

  /** Проставить слоты по порядку списка: P01, P02, … — порядок = порядок закидки. */
  const assignSlotsInOrder = useCallback(() => {
    setPicked((prev) => prev.map((p, i) => ({ ...p, slot: `P${i + 1 < 10 ? `0${i + 1}` : i + 1}` })));
  }, []);

  const slotsFilled = picked.filter((p) => p.slot).length;

  /* ── X-триаж порционным циклом (сервер капает по 2 файла на запрос) ── */
  const runTriage = useCallback(async (ids?: string[], onProgress?: (done: number, remaining: number) => void) => {
    let done = 0;
    for (let guard = 0; guard < 80; guard++) {
      const res = await fetch('/api/t5/inbox/triage', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(ids && ids.length > 0 ? { ids } : {}),
      });
      const data = await readJson<{ triaged?: number; remaining?: number; items?: InboxItem[]; error?: string }>(res);
      if (!res.ok) throw new Error(data.error ?? 'триаж не удался');
      setItems(data.items ?? []);
      done += data.triaged ?? 0;
      onProgress?.(done, data.remaining ?? 0);
      if ((data.remaining ?? 0) === 0 || (data.triaged ?? 0) === 0) break;
    }
    return done;
  }, []);

  /* ── загрузка кучкой: чанки по 8, теги пофайлово → затем триаж-цикл ── */
  const upload = useCallback(async () => {
    if (picked.length === 0 || busy) return;
    setMessage(null);
    try {
      let uploaded = 0;
      let failed = 0;
      for (let i = 0; i < picked.length; i += UPLOAD_CHUNK) {
        const chunk = picked.slice(i, i + UPLOAD_CHUNK);
        setBusy(`Заливаю ${Math.min(i + chunk.length, picked.length)}/${picked.length}…`);
        const fd = new FormData();
        const tags = chunk.map((p) => [batch.trim(), p.slot].filter(Boolean).join(' '));
        for (const p of chunk) fd.append('files', p.file);
        fd.append('tags', JSON.stringify(tags));
        const res = await fetch('/api/t5/inbox', { method: 'POST', body: fd });
        const data = await readJson<{ uploaded?: number; failed?: number; items?: InboxItem[]; error?: string }>(res);
        if (!res.ok) throw new Error(data.error ?? 'загрузка не удалась');
        uploaded += data.uploaded ?? 0;
        failed += data.failed ?? 0;
        setItems(data.items ?? []);
      }
      clearPicked();

      let triaged = 0;
      try {
        setBusy('Залито. Гоню X-триаж порциями…');
        triaged = await runTriage(undefined, (done, remaining) => {
          setBusy(`X-триаж: обработано ${done}, осталось ${remaining}…`);
        });
      } catch (err) {
        setMessage(
          `Залито: ${uploaded}, но X-триаж прервался (${String(err instanceof Error ? err.message : err)}) — жми «Прогнать X-триаж» ниже, очередь не теряется`,
        );
        return;
      }
      setMessage(
        `Залито: ${uploaded}${failed > 0 ? ` · отброшено: ${failed}` : ''} · X-триаж пройден: ${triaged}. Файлы лежат на диске до очистки.`,
      );
    } catch (err) {
      setMessage(`Ошибка: ${String(err instanceof Error ? err.message : err)}`);
    } finally {
      setBusy(null);
    }
  }, [picked, batch, busy, runTriage, clearPicked]);

  const triageQueue = useCallback(async () => {
    if (busy) return;
    setMessage(null);
    try {
      setBusy('X-триаж очереди…');
      const done = await runTriage(undefined, (d, remaining) => {
        setBusy(`X-триаж: обработано ${d}, осталось ${remaining}…`);
      });
      setMessage(done > 0 ? `X-триаж пройден: ${done}` : 'Очередь триажа пуста');
    } catch (err) {
      setMessage(`Ошибка триажа: ${String(err instanceof Error ? err.message : err)} — очередь сохранена, можно жать снова`);
    } finally {
      setBusy(null);
    }
  }, [busy, runTriage]);

  /* ── автотриаж: инбокс открыт, а очередь осталась (урок T5-19 про 401) ── */
  useEffect(() => {
    if (loading || autoTriageRef.current || busy) return;
    const queued = items.filter((i) => i.status === 'queued' || i.triage.label === 'unknown').length;
    if (queued === 0) return;
    autoTriageRef.current = true;
    setMessage(null);
    void (async () => {
      try {
        setBusy(`Автотриаж: в очереди ${queued}…`);
        const done = await runTriage(undefined, (d, remaining) => {
          setBusy(`Автотриаж: обработано ${d}, осталось ${remaining}…`);
        });
        setMessage(done > 0 ? `Автотриаж догнал очередь: ${done} — можно разбирать` : null);
      } catch (err) {
        setMessage(`Автотриаж прервался: ${String(err instanceof Error ? err.message : err)} — очередь цела, жми «Прогнать X-триаж»`);
      } finally {
        setBusy(null);
      }
    })();
  }, [items, loading, busy, runTriage]);

  const retriageQuarantine = useCallback(async () => {
    if (busy) return;
    const ids = items
      .filter((i) => !i.authorOverride && i.triage.label === 'x' && RETRIAGE_RE.test(i.triage.reason))
      .map((i) => i.id);
    if (ids.length === 0) return;
    setMessage(null);
    try {
      setBusy(`Перетриаживаю карантин (${ids.length})…`);
      const done = await runTriage(ids, (d, remaining) => {
        setBusy(`Перетриаж карантина: обработано ${d}, осталось ${remaining}…`);
      });
      setMessage(`Перетриажено: ${done} — fail-closed карантины пересмотрены`);
    } catch (err) {
      setMessage(`Ошибка перетриажа: ${String(err instanceof Error ? err.message : err)}`);
    } finally {
      setBusy(null);
    }
  }, [busy, items, runTriage]);

  /* ── разбор порционным циклом (сервер капает по 3 файла на запрос) ── */
  const analyze = useCallback(async (ids?: string[]) => {
    if (busy) return;
    setMessage(null);
    let total = 0;
    try {
      for (let guard = 0; guard < 40; guard++) {
        setBusy(total === 0 ? 'Разбираю…' : `Разобрано ${total}, докручиваю…`);
        const res = await fetch('/api/t5/inbox/analyze', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(ids && ids.length > 0 ? { ids } : { action: 'analyze' }),
        });
        const data = await readJson<{ analyzed?: number; remaining?: number; items?: InboxItem[]; error?: string }>(res);
        if (!res.ok) throw new Error(data.error ?? 'разбор не удался');
        setItems(data.items ?? []);
        total += data.analyzed ?? 0;
        if ((data.analyzed ?? 0) === 0 || (data.remaining ?? 0) === 0) break;
      }
      setMessage(total > 0 ? `Разобрано: ${total}` : 'Разбирать нечего — всё разобрано или в карантине');
    } catch (err) {
      setMessage(
        total > 0
          ? `Разобрано ${total}, дальше прервалось: ${String(err instanceof Error ? err.message : err)} — жми ещё раз, докрутит`
          : `Ошибка: ${String(err instanceof Error ? err.message : err)}`,
      );
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
      const data = await readJson<{ item?: InboxItem; error?: string }>(res);
      if (!res.ok) throw new Error(data.error ?? 'не вышло');
      setItems((list) => list.map((i) => (i.id === id && data.item ? data.item : i)));
    } catch (err) {
      setMessage(`Ошибка: ${String(err instanceof Error ? err.message : err)}`);
    } finally {
      setBusy(null);
    }
  }, [busy]);

  /* ── очистка: после разбора пачку убираем, чтобы диск не пух ── */
  const removeByQuery = useCallback(async (query: string, okText: string) => {
    if (busy) return;
    setMessage(null);
    try {
      setBusy('Убираю файлы…');
      const res = await fetch(`/api/t5/inbox?${query}`, { method: 'DELETE' });
      const data = await readJson<{ count?: number; bytes?: number; items?: InboxItem[]; error?: string }>(res);
      if (!res.ok) throw new Error(data.error ?? 'не вышло');
      setItems(data.items ?? []);
      setMessage(`${okText}: ${data.count ?? 0}, освобождено ${fmtSize(data.bytes ?? 0)}`);
    } catch (err) {
      setMessage(`Ошибка очистки: ${String(err instanceof Error ? err.message : err)}`);
    } finally {
      setBusy(null);
    }
  }, [busy]);

  const removeProcessed = useCallback(() => {
    const ids = items.filter((i) => i.status === 'analyzed' || i.status === 'x' || i.status === 'error').map((i) => i.id);
    if (ids.length === 0) return;
    void removeByQuery(`ids=${ids.join(',')}`, 'Убрано обработанных');
  }, [items, removeByQuery]);

  const wipeAll = useCallback(() => {
    if (!wipeArmed) {
      setWipeArmed(true);
      if (wipeTimer.current) clearTimeout(wipeTimer.current);
      wipeTimer.current = setTimeout(() => setWipeArmed(false), 5000);
      return;
    }
    setWipeArmed(false);
    if (wipeTimer.current) clearTimeout(wipeTimer.current);
    void removeByQuery('all=1', 'Инбокс снесён');
  }, [wipeArmed, removeByQuery]);

  const removeOne = useCallback((id: string) => {
    void removeByQuery(`ids=${id}`, 'Убран файл');
  }, [removeByQuery]);

  const onDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      setDragOver(false);
      addFiles(Array.from(e.dataTransfer.files ?? []));
    },
    [addFiles],
  );

  const stats = useMemo(
    () => ({
      total: items.length,
      x: items.filter((i) => i.triage.label === 'x' && !i.authorOverride).length,
      queued: items.filter((i) => i.status === 'queued' || i.triage.label === 'unknown').length,
      pending: items.filter((i) => i.status === 'ok').length,
      analyzed: items.filter((i) => i.status === 'analyzed').length,
      error: items.filter((i) => i.status === 'error').length,
      processed: items.filter((i) => i.status === 'analyzed' || i.status === 'x' || i.status === 'error').length,
    }),
    [items],
  );
  const retriageCount = items.filter(
    (i) => !i.authorOverride && i.triage.label === 'x' && i.status === 'x' && RETRIAGE_RE.test(i.triage.reason),
  ).length;

  /* фильтр по статусу + порядок журнала сохраняется (батч ↓, слот ↑) */
  const visibleItems = useMemo(
    () => (statusFilter === 'all' ? items : items.filter((i) => i.status === statusFilter)),
    [items, statusFilter],
  );

  /* прогресс конвейера: обработанные (разобранные + карантин + ошибки) от всех */
  const progressPct = stats.total === 0 ? 0 : Math.round((stats.processed / stats.total) * 100);

  /* лайтбокс: Esc — закрыть, стрелки — листать галерею */
  useEffect(() => {
    if (lightbox === null) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') setLightbox(null);
      if (e.key === 'ArrowRight') setLightbox((v) => (v === null ? v : Math.min(v + 1, visibleItems.length - 1)));
      if (e.key === 'ArrowLeft') setLightbox((v) => (v === null ? v : Math.max(v - 1, 0)));
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [lightbox, visibleItems.length]);

  const lightboxItem = lightbox !== null ? visibleItems[lightbox] : null;

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
          dragOver ? '!border-emerald-400/60 !bg-emerald-400/[0.06]' : '!border-white/[0.12]',
        )}
      >
        <div className="flex flex-col gap-4 sm:flex-row sm:items-center">
          <div className="min-w-0 flex-1">
            <h2 className="flex items-center gap-2 font-display text-base font-bold text-white sm:text-lg">
              <UploadCloud className="size-5 text-emerald-300" aria-hidden />
              Сбрось итоговые рендеры кучкой
            </h2>
            <p className="mt-1.5 text-sm leading-relaxed text-zinc-400">
              Перетащи файлы сюда или выбери вручную — png/jpg/webp, до 25 МБ каждый, хоть все 33 разом. Заливаю
              порциями по 8, затем X-триаж идёт маленькими шагами (без таймаутов). Слот ставится пофайлово —
              сама вытаскивается из имени («P07.webp», «07 - name»), правится в списке ниже или проставляется
              по порядку одной кнопкой. Файлы лежат на диске до явной очистки — после разбора жми «Убрать обработанные».
            </p>
          </div>
          <div className="flex shrink-0 items-center gap-2">
            <Input
              ref={fileRef}
              type="file"
              multiple
              accept="image/png,image/jpeg,image/webp"
              onChange={(e) => addFiles(Array.from(e.target.files ?? []))}
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
          <label htmlFor="inbox-batch" className="font-mono text-[11px] uppercase tracking-widest text-zinc-500">
            Батч
          </label>
          <input
            id="inbox-batch"
            value={batch}
            onChange={(e) => changeBatch(e.target.value)}
            placeholder="T5-19"
            className="h-8 w-24 rounded-lg border border-white/[0.09] bg-black/30 px-2.5 font-mono text-xs text-zinc-200 placeholder:text-zinc-600 focus-visible:border-emerald-400/50 focus-visible:outline-none"
          />
          {picked.length > 0 && (
            <>
              <Chip>
                {picked.length} файл(ов) · {fmtSize(picked.reduce((a, p) => a + p.file.size, 0))} · слотов проставлено:{' '}
                {slotsFilled}/{picked.length}
              </Chip>
              <button
                type="button"
                onClick={assignSlotsInOrder}
                disabled={busy !== null}
                className="t5-btn !px-2 !py-1 !text-[11px] disabled:opacity-40"
                title="Порядок списка = порядок закидки: P01, P02, … — как в галерее рендера"
              >
                <ListOrdered className="size-3" aria-hidden />
                Проставить по порядку
              </button>
              <button
                type="button"
                onClick={clearPicked}
                disabled={busy !== null}
                className="t5-btn !px-2 !py-1 !text-[11px] disabled:opacity-40"
              >
                <X className="size-3" aria-hidden />
                Сбросить список
              </button>
            </>
          )}
        </div>

        {/* список выбранных: пофайловые слоты — пачка больше не путается */}
        {picked.length > 0 && (
          <div className="t5-scroll mt-3 max-h-64 space-y-1.5 overflow-y-auto rounded-xl border border-white/[0.07] bg-black/30 p-2.5">
            {picked.map((p, i) => (
              <div key={p.key} className="flex items-center gap-2 rounded-lg px-1.5 py-1 hover:bg-white/[0.04]">
                <span className="w-6 shrink-0 text-right font-mono text-[11px] text-zinc-600">{i + 1}</span>
                <span className="min-w-0 flex-1 truncate font-mono text-xs text-zinc-300" title={p.file.name}>
                  {p.file.name}
                </span>
                <span className="shrink-0 font-mono text-[11px] text-zinc-600">{fmtSize(p.file.size)}</span>
                <input
                  value={p.slot}
                  onChange={(e) => setPickedSlot(p.key, e.target.value)}
                  placeholder="—"
                  aria-label={`Слот для ${p.file.name}`}
                  className={cn(
                    'h-7 w-14 shrink-0 rounded-md border bg-black/40 px-1.5 text-center font-mono text-xs uppercase focus-visible:outline-none',
                    p.slot
                      ? 'border-emerald-400/40 text-emerald-300'
                      : 'border-white/[0.12] text-zinc-500 placeholder:text-zinc-700',
                  )}
                />
                <button
                  type="button"
                  onClick={() => dropPicked(p.key)}
                  aria-label={`Убрать ${p.file.name} из списка`}
                  className="shrink-0 rounded-md p-1 text-zinc-600 transition-colors hover:bg-white/[0.06] hover:text-zinc-300"
                >
                  <X className="size-3.5" aria-hidden />
                </button>
              </div>
            ))}
          </div>
        )}
      </section>

      {/* статус-панель: пилюли-фильтры + конвейерный прогресс */}
      <section className="t5-panel p-4" aria-label="Статистика инбокса">
        <div className="flex flex-wrap items-center gap-x-3 gap-y-2">
          <h2 className="flex items-center gap-2 text-sm font-bold text-zinc-200">
            <InboxIcon className="size-4 text-emerald-300" aria-hidden />
            Инбокс — {stats.total}
          </h2>
          <div className="flex flex-wrap items-center gap-1.5">
            <StatPill dot="bg-zinc-400" label="триаж" count={stats.queued} active={statusFilter === 'queued'} onClick={() => setStatusFilter((s) => (s === 'queued' ? 'all' : 'queued'))} />
            <StatPill dot="bg-emerald-400" label="разбор" count={stats.pending} active={statusFilter === 'ok'} onClick={() => setStatusFilter((s) => (s === 'ok' ? 'all' : 'ok'))} />
            <StatPill dot="bg-[#ffc24b]" label="готово" count={stats.analyzed} active={statusFilter === 'analyzed'} onClick={() => setStatusFilter((s) => (s === 'analyzed' ? 'all' : 'analyzed'))} />
            <StatPill dot="bg-red-400" label="X" count={stats.x} active={statusFilter === 'x'} onClick={() => setStatusFilter((s) => (s === 'x' ? 'all' : 'x'))} />
            {stats.error > 0 && (
              <StatPill dot="bg-orange-400" label="ошибки" count={stats.error} active={statusFilter === 'error'} onClick={() => setStatusFilter((s) => (s === 'error' ? 'all' : 'error'))} />
            )}
          </div>
          <div className="ml-auto flex flex-wrap gap-2">
            {stats.processed > 0 && (
              <button
                type="button"
                onClick={removeProcessed}
                disabled={busy !== null}
                className="t5-btn disabled:opacity-40"
                title="Разобранные, карантин и ошибки: файлы с диска и записи журнала"
              >
                <Eraser className="size-3.5" aria-hidden />
                Убрать обработанные ({stats.processed})
              </button>
            )}
            {items.length > 0 && (
              <button
                type="button"
                onClick={wipeAll}
                disabled={busy !== null}
                className={cn('t5-btn disabled:opacity-40', wipeArmed && '!border-red-400/60 !text-red-300')}
                title="Снести весь инбокс: файлы, превью и журнал"
              >
                <Trash2 className="size-3.5" aria-hidden />
                {wipeArmed ? 'Точно снести всё?' : 'Очистить инбокс'}
              </button>
            )}
            {retriageCount > 0 && (
              <button
                type="button"
                onClick={() => void retriageQuarantine()}
                disabled={busy !== null}
                className="t5-btn disabled:opacity-40"
                title="Карантин от сбоев/429 триажа — пересматриваю заново"
              >
                <RefreshCcw className="size-3.5" aria-hidden />
                Перетриажнуть карантин ({retriageCount})
              </button>
            )}
            {stats.queued > 0 && (
              <button type="button" onClick={() => void triageQueue()} disabled={busy !== null} className="t5-btn disabled:opacity-40">
                {busy ? <Loader2 className="size-3.5 animate-spin" /> : <ShieldAlert className="size-3.5" />}
                Прогнать X-триаж ({stats.queued})
              </button>
            )}
            <button
              type="button"
              onClick={() => void analyze()}
              disabled={busy !== null || stats.pending === 0}
              className="t5-btn disabled:opacity-40"
            >
              {busy ? <Loader2 className="size-3.5 animate-spin" /> : <ScanSearch className="size-3.5" />}
              Разобрать всё новое
            </button>
          </div>
        </div>

        {/* конвейер инбокса: обработано от общего числа */}
        <div className="mt-3.5 flex items-center gap-3">
          <div
            role="progressbar"
            aria-valuemin={0}
            aria-valuemax={stats.total}
            aria-valuenow={stats.processed}
            aria-label={`Обработано ${stats.processed} из ${stats.total}`}
            className="h-1.5 flex-1 overflow-hidden rounded-full bg-white/[0.06]"
          >
            <div
              className={cn('h-full rounded-full bg-gradient-to-r from-[#3ddc97] via-[#2de2e6] to-[#ffc24b] shadow-[0_0_10px_rgb(61_220_151/0.35)] transition-[width] duration-500', progressPct < 100 && stats.total > 0 && 't5-shimmer')}
              style={{ width: `${progressPct}%` }}
            />
          </div>
          <span className="shrink-0 font-mono text-[11px] tabular-nums text-zinc-500">
            конвейер {stats.processed}/{stats.total}
          </span>
        </div>
      </section>

      {busy && (
        <div className="flex items-center gap-2.5 rounded-xl border border-emerald-400/20 bg-emerald-400/[0.05] px-4 py-3 text-sm text-zinc-200">
          <Loader2 className="size-4 animate-spin text-emerald-300" aria-hidden />
          {busy}
          <span className="text-xs text-zinc-500">иду порциями — даже если оборвётся, очередь сохранится</span>
        </div>
      )}
      {message && !busy && (
        <p className="flex items-start gap-2 rounded-xl border border-white/[0.07] bg-white/[0.03] px-4 py-2.5 text-sm text-zinc-400">
          <Sparkles className="mt-0.5 size-3.5 shrink-0 text-zinc-600" aria-hidden />
          {message}
        </p>
      )}

      {/* журнал */}
      {loading ? (
        <div className="flex items-center justify-center py-16 text-sm text-zinc-500">
          <Loader2 className="mr-2.5 size-5 animate-spin text-emerald-300" /> Читаю журнал…
        </div>
      ) : items.length === 0 ? (
        <div className="t5-panel p-12 text-center">
          <Sparkles className="mx-auto mb-4 size-5 text-zinc-600" aria-hidden />
          <p className="t5-gradient-text mb-2 font-display text-lg font-bold uppercase">Инбокс пуст</p>
          <p className="mx-auto max-w-md text-sm leading-relaxed text-zinc-400">
            Заливай пачками после каждого прогона на PixAI — я записываю находки в журнал, а ты смотришь, что
            прошло мимо твоих глаз. Цикл «рендер → инбокс → находки → патчи промптов» и есть импрув воркфлоу.
          </p>
        </div>
      ) : visibleItems.length === 0 ? (
        <div className="t5-panel p-10 text-center text-sm text-zinc-500">Под этот фильтр ничего не попало</div>
      ) : (
        <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
          {visibleItems.map((item, idx) => {
            const meta = STATUS_META[item.status];
            const quarantined = item.triage.label === 'x' && item.authorOverride?.label !== 'sfw';
            const canAnalyze = !quarantined && item.status !== 'queued';
            return (
              <article
                key={item.id}
                className={cn(
                  't5-card group flex flex-col overflow-hidden !rounded-xl p-0',
                  quarantined && '!border-red-400/30',
                )}
              >
                <div className="relative bg-black/45">
                  <button
                    type="button"
                    onClick={() => setLightbox(idx)}
                    aria-label={`Открыть ${item.origName} крупно`}
                    className="block w-full cursor-zoom-in focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-emerald-400"
                  >
                    <img
                      src={`/api/t5/inbox/file?id=${item.id}&preview=1`}
                      alt={quarantined ? 'Карантированное изображение (размыто)' : `Загруженный рендер ${item.origName}`}
                      className={cn('h-48 w-full object-cover transition-transform duration-200 group-hover:scale-[1.02]', quarantined && 'scale-110 grayscale blur-2xl')}
                      loading="lazy"
                    />
                  </button>
                  <span className={cn('pointer-events-none absolute left-2 top-2 rounded-md border px-1.5 py-0.5 font-mono text-[10px] font-bold backdrop-blur-sm', meta.cls)}>
                    {meta.label}
                  </span>
                  {item.tag && (
                    <span className="pointer-events-none absolute right-2 top-2 rounded-md border border-white/[0.14] bg-black/70 px-1.5 py-0.5 font-mono text-[10px] text-cyan-200 backdrop-blur-sm">
                      {item.tag}
                    </span>
                  )}
                  {!quarantined && (
                    <span className="pointer-events-none absolute bottom-2 right-2 rounded-md border border-white/[0.12] bg-black/60 p-1.5 text-zinc-300 opacity-0 backdrop-blur-sm transition-opacity duration-150 group-hover:opacity-100">
                      <Maximize2 className="size-3.5" aria-hidden />
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
                    <div className={cn('rounded-lg border p-2.5 text-xs leading-relaxed', SEVERITY_CLS[item.analysis.severity] ?? 'border-white/[0.07] bg-black/25')}>
                      <p className="mb-1.5 flex items-center gap-1.5 font-bold">
                        <FileWarning className="size-3.5" aria-hidden />
                        Разбор: {SEVERITY_LABEL[item.analysis.severity] ?? item.analysis.severity}
                      </p>
                      {item.analysis.findings.length > 0 ? (
                        <ul className="space-y-1.5 text-zinc-400">
                          {item.analysis.findings.map((f, i) => (
                            <li key={i}>
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
                    {canAnalyze && (
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
                        <ShieldAlert className="size-3" aria-hidden />
                        В карантин
                      </button>
                    )}
                    <button
                      type="button"
                      onClick={() => removeOne(item.id)}
                      disabled={busy !== null}
                      className="t5-btn !px-2 !py-1 !text-[11px] disabled:opacity-40"
                      aria-label={`Убрать ${item.origName} с диска`}
                      title="Убрать этот файл с диска и из журнала"
                    >
                      <Trash2 className="size-3" aria-hidden />
                      Убрать
                    </button>
                  </div>
                </div>
              </article>
            );
          })}
        </div>
      )}

      {/* лайтбокс галереи: портал в body — должен перекрывать шапку (z-20)
          и жить выше stacking-контекста main (урок: fixed внутри z-10 main не перебивает шапку) */}
      {lightboxItem && createPortal(
        <div
          role="dialog"
          aria-modal="true"
          aria-label={`Просмотр рендера ${lightboxItem.origName}`}
          className="fixed inset-0 z-50 flex flex-col bg-black/90 p-4 backdrop-blur-md sm:p-6"
          onClick={() => setLightbox(null)}
        >
          <div className="mx-auto flex w-full max-w-5xl items-center justify-between gap-3" onClick={(e) => e.stopPropagation()}>
            <div className="flex min-w-0 flex-wrap items-center gap-2 font-mono text-xs text-zinc-400">
              <span className="rounded-md border border-white/[0.14] bg-black/60 px-2 py-1 text-cyan-200">{lightboxItem.tag ?? '—'}</span>
              <span className="truncate">{lightboxItem.origName}</span>
              <span className="text-zinc-600">· {lightbox + 1}/{visibleItems.length}</span>
            </div>
            <button
              type="button"
              onClick={() => setLightbox(null)}
              aria-label="Закрыть просмотр"
              className="rounded-lg border border-white/[0.14] bg-black/60 p-2 text-zinc-300 transition-colors hover:bg-black/90 hover:text-white focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-white/60"
            >
              <X className="size-4" aria-hidden />
            </button>
          </div>
          <div className="relative mx-auto flex min-h-0 w-full max-w-5xl flex-1 items-center justify-center gap-3 py-4" onClick={(e) => e.stopPropagation()}>
            <button
              type="button"
              onClick={() => setLightbox((v) => (v === null ? v : Math.max(0, v - 1)))}
              disabled={lightbox === 0}
              aria-label="Предыдущий рендер"
              className="shrink-0 rounded-lg border border-white/[0.12] bg-black/60 p-2.5 text-zinc-300 transition-colors hover:bg-black/90 hover:text-white disabled:opacity-25 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-white/60"
            >
              <ChevronLeft className="size-5" aria-hidden />
            </button>
            <img
              src={`/api/t5/inbox/file?id=${lightboxItem.id}&preview=1`}
              alt={`Рендер крупно — ${lightboxItem.origName}`}
              className="min-h-0 max-h-full max-w-full rounded-xl border border-white/[0.1] object-contain shadow-2xl"
              onClick={(e) => e.stopPropagation()}
            />
            <button
              type="button"
              onClick={() => setLightbox((v) => (v === null ? v : Math.min(visibleItems.length - 1, v + 1)))}
              disabled={lightbox >= visibleItems.length - 1}
              aria-label="Следующий рендер"
              className="shrink-0 rounded-lg border border-white/[0.12] bg-black/60 p-2.5 text-zinc-300 transition-colors hover:bg-black/90 hover:text-white disabled:opacity-25 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-white/60"
            >
              <ChevronRight className="size-5" aria-hidden />
            </button>
          </div>
          <p className="text-center font-mono text-[11px] text-zinc-500">Esc — закрыть · ← → — листать галерею</p>
        </div>,
        document.body,
      )}
    </div>
  );
}
