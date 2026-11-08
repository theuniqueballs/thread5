'use client';

import { useEffect, useState } from 'react';
import { Aperture, X } from 'lucide-react';
import { cn } from '@/lib/utils';

/**
 * ПРЕ-РЕНДЕРЫ ПРОГОН-ПЕТЛИ (вердикт T5-16: «во вкладке Разбор появлялся твой
 * пре-рендер, интересно посмотреть что он из себя представляет»).
 * Прокси-рендер писца = дымовой тест читаемости промпта, НЕ финальный рендер:
 * финальный арбитр — прогон автора на PixAI. Данные: public/t5/loop/<batch>/loop.json.
 */

export interface LoopSlotInfo {
  name: string;
  note: string;
  circles: Record<string, string>; // c1 → url
  pos?: string;
}

export interface LoopManifest {
  batch: string;
  theme: string;
  updated: string;
  note: string;
  circles: Record<string, { when: string; what: string }>;
  slots: Record<string, LoopSlotInfo>;
}

const CIRCLE_ORDER = ['c1', 'c2', 'c3'] as const;
const CIRCLE_LABEL: Record<string, string> = { c1: 'круг 1', c2: 'круг 2', c3: 'круг 3' };

export function LoopRenders({ info }: { info?: LoopSlotInfo | null }) {
  const [zoom, setZoom] = useState<{ url: string; label: string } | null>(null);

  /* Escape закрывает лайтбокс — клавиатурный выход */
  useEffect(() => {
    if (!zoom) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') setZoom(null);
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [zoom]);

  if (!info) return null;
  const entries = CIRCLE_ORDER.filter((c) => info.circles[c]).map((c) => ({ c, url: info.circles[c] }));
  if (entries.length === 0) return null;

  return (
    <section
      aria-label="Прокси-рендеры прогон-петли"
      className="mt-3 rounded-lg border border-[#ffc24b]/25 bg-[#ffc24b]/[0.045] p-3"
    >
      <div className="mb-2.5 flex flex-wrap items-baseline gap-x-2.5 gap-y-1">
        <span className="flex items-center gap-1.5 font-mono text-[10px] font-bold tracking-[0.18em] text-[#ffc24b]">
          <Aperture className="size-3.5" aria-hidden />
          ПРОГОН-ПЕТЛЯ · ПРОКСИ-РЕНДЕР ПИСЦА
        </span>
        <span className="font-mono text-[10px] text-zinc-500">не PixAI — дымовой тест промпта</span>
      </div>

      <div className="flex flex-wrap gap-2.5">
        {entries.map(({ c, url }) => (
          <button
            key={c}
            type="button"
            onClick={() => setZoom({ url, label: CIRCLE_LABEL[c] ?? c })}
            aria-label={`Открыть прокси-рендер, ${CIRCLE_LABEL[c] ?? c}`}
            className="group relative overflow-hidden rounded-md border border-white/[0.09] transition-all duration-150 hover:border-[#ffc24b]/60 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-[#ffc24b]"
          >
            <img src={url} alt={`Прокси-рендер ${info.name}, ${CIRCLE_LABEL[c] ?? c}`} className="h-32 w-auto object-cover transition-transform duration-200 group-hover:scale-[1.02]" loading="lazy" />
            <span className="absolute inset-x-0 bottom-0 bg-gradient-to-t from-black/80 to-transparent px-1.5 pb-0.5 pt-3 font-mono text-[10px] font-bold text-[#ffc24b]">
              {CIRCLE_LABEL[c] ?? c}
            </span>
          </button>
        ))}
      </div>

      {info.note && (
        <p className="mt-2.5 border-l-2 border-[#ffc24b]/40 pl-2.5 text-xs leading-relaxed text-zinc-400">
          {info.note}
        </p>
      )}

      {zoom && (
        <div
          role="dialog"
          aria-modal="true"
          aria-label="Прокси-рендер крупно"
          className="fixed inset-0 z-50 flex items-center justify-center bg-black/85 p-4 backdrop-blur-sm sm:p-8"
          onClick={() => setZoom(null)}
        >
          <button
            type="button"
            onClick={() => setZoom(null)}
            aria-label="Закрыть"
            className={cn(
              'absolute right-4 top-4 z-10 rounded-lg border border-white/[0.14] bg-black/60 p-2 text-zinc-300',
              'transition-colors hover:bg-black/90 hover:text-white focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-white/60',
            )}
          >
            <X className="size-4" aria-hidden />
          </button>
          <figure className="max-h-full" onClick={(e) => e.stopPropagation()}>
            <img
              src={zoom.url}
              alt={`Прокси-рендер крупно — ${zoom.label}`}
              className="max-h-[86vh] max-w-full rounded-xl border border-white/[0.1] object-contain shadow-2xl"
            />
            <figcaption className="mt-2 text-center font-mono text-[11px] text-zinc-400">
              {zoom.label} · прокси-рендер писца (не финальный)
            </figcaption>
          </figure>
        </div>
      )}
    </section>
  );
}
