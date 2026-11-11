'use client';

import { useCallback, useState } from 'react';
import { Check, Copy } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { cn } from '@/lib/utils';

/* ── копирование в буфер ─────────────────────────────────────────── */

export async function copyText(text: string): Promise<boolean> {
  try {
    await navigator.clipboard.writeText(text);
    return true;
  } catch {
    try {
      const ta = document.createElement('textarea');
      ta.value = text;
      ta.style.position = 'fixed';
      ta.style.opacity = '0';
      document.body.appendChild(ta);
      ta.select();
      const ok = document.execCommand('copy');
      document.body.removeChild(ta);
      return ok;
    } catch {
      return false;
    }
  }
}

interface CopyButtonProps {
  text: string;
  label?: string;
  className?: string;
}

export function CopyButton({ text, label, className }: CopyButtonProps) {
  const [done, setDone] = useState(false);
  const onCopy = useCallback(async () => {
    const ok = await copyText(text);
    if (ok) {
      setDone(true);
      window.setTimeout(() => setDone(false), 1400);
    }
  }, [text]);
  return (
    <button
      type="button"
      onClick={onCopy}
      aria-label={label ?? 'Скопировать'}
      className={cn('t5-btn t5-btn-sm', className)}
    >
      {done ? <Check className="size-3.5 text-t5-mint" /> : <Copy className="size-3.5" />}
      {done ? 'Скопировано' : (label ?? 'Копировать')}
    </button>
  );
}

/* ── бейджи единой системы (см. .t5-badge в globals.css):
      жанр — золото/малина/фиолет/нейтрал, рейтинг — малина по нарастанию,
      мята не участвует: она зарезервирована под статусы триажа ─────── */

const GENRE_STYLES: Record<string, string> = {
  OC: 't5-badge--gold',
  VOLT: 't5-badge--rose',
  NICHE: 't5-badge--violet',
  EXQUISITE: 't5-badge--neutral',
  EXP: 't5-badge--gold',
};

const RATING_STYLES: Record<string, string> = {
  'PG-13': 't5-badge--neutral',
  R: 't5-badge--rose-dim',
  'R+': 't5-badge--rose',
  X: 't5-badge--red',
  XXX: 't5-badge--red-strong',
};

export function GenreBadge({ genre }: { genre: string | null }) {
  if (!genre) return null;
  return (
    <span className={cn('t5-badge tracking-[0.14em]', GENRE_STYLES[genre] ?? 't5-badge--neutral')}>
      {genre}
    </span>
  );
}

export function RatingBadge({ rating }: { rating: string | null }) {
  if (!rating) return null;
  return (
    <span className={cn('t5-badge', RATING_STYLES[rating] ?? 't5-badge--neutral')}>
      {rating}
    </span>
  );
}

export function Chip({ children }: { children: React.ReactNode }) {
  return (
    <span className="t5-badge t5-badge--neutral !text-[11px] font-medium normal-case tracking-normal">
      {children}
    </span>
  );
}

/* ── markdown доков ──────────────────────────────────────────────── */

export function T5Markdown({ content }: { content: string }) {
  return (
    <div className="t5-prose max-w-none">
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={{
          h1: (p) => <h1 className="mb-5 mt-8 border-b border-white/[0.08] pb-3 font-display text-lg font-bold text-white first:mt-0" {...p} />,
          h2: (p) => <h2 className="mb-3 mt-9 text-base font-extrabold tracking-wide text-white" {...p} />,
          h3: (p) => <h3 className="mb-2 mt-7 flex items-center gap-2 text-sm font-bold text-t5-violet-bright" {...p} />,
          p: (p) => <p className="mb-3 max-w-[78ch] text-sm leading-relaxed text-zinc-300" {...p} />,
          ul: (p) => <ul className="mb-3 max-w-[78ch] list-disc space-y-1 pl-5 text-sm text-zinc-300 marker:text-t5-accent/70" {...p} />,
          ol: (p) => <ol className="mb-3 max-w-[78ch] list-decimal space-y-1 pl-5 text-sm text-zinc-300 marker:text-zinc-600" {...p} />,
          li: (p) => <li className="leading-relaxed" {...p} />,
          strong: (p) => <strong className="font-bold text-white" {...p} />,
          em: (p) => <em className="text-zinc-400" {...p} />,
          hr: () => <hr className="my-7 h-px border-0 bg-gradient-to-r from-transparent via-white/15 to-transparent" />,
          blockquote: (p) => <blockquote className="mb-3 border-l-2 border-t5-accent/40 bg-white/[0.02] py-1 pl-3 text-sm italic text-zinc-400" {...p} />,
          code: ({ children, className }) =>
            className?.includes('language-') ? (
              <code className="t5-scroll block whitespace-pre-wrap break-words rounded-lg border border-white/[0.07] bg-black/30 p-3.5 font-mono text-xs leading-relaxed text-zinc-300">{children}</code>
            ) : (
              <code className="rounded-md bg-white/[0.07] px-1.5 py-0.5 font-mono text-xs text-t5-accent-bright">{children}</code>
            ),
          pre: (p) => <pre className="mb-3 overflow-x-auto" {...p} />,
          table: (p) => (
            <div className="t5-scroll mb-5 overflow-x-auto rounded-lg border border-white/[0.08]">
              <table className="w-full border-collapse text-sm" {...p} />
            </div>
          ),
          thead: (p) => <thead className="bg-white/[0.04]" {...p} />,
          th: (p) => <th className="border-b border-white/[0.08] px-3 py-2 text-left text-[11px] font-bold uppercase tracking-wider text-zinc-200" {...p} />,
          td: (p) => <td className="border-b border-white/[0.05] px-3 py-2 align-top text-zinc-300" {...p} />,
          a: (p) => <a className="text-t5-accent-bright underline decoration-t5-accent/45 underline-offset-2 transition-colors hover:text-white hover:decoration-t5-accent" {...p} />,
        }}
      >
        {content}
      </ReactMarkdown>
    </div>
  );
}
