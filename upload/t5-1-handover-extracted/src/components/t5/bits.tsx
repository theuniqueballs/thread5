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
      className={cn('t5-btn', className)}
    >
      {done ? <Check className="size-3.5 text-emerald-400" /> : <Copy className="size-3.5" />}
      {done ? 'Скопировано' : (label ?? 'Копировать')}
    </button>
  );
}

/* ── бейджи шапки слота: приглушённые семантические краски ───────── */

const GENRE_STYLES: Record<string, string> = {
  OC: 'border-pink-500/35 bg-pink-500/[0.08] text-pink-300',
  VOLT: 'border-rose-500/35 bg-rose-500/[0.08] text-rose-300',
  NICHE: 'border-emerald-500/35 bg-emerald-500/[0.08] text-emerald-300',
  EXQUISITE: 'border-violet-500/35 bg-violet-500/[0.08] text-violet-300',
  EXP: 'border-cyan-400/35 bg-cyan-400/[0.08] text-cyan-300',
};

const RATING_STYLES: Record<string, string> = {
  'PG-13': 'border-cyan-400/30 bg-cyan-400/[0.06] text-cyan-300/90',
  R: 'border-violet-500/35 bg-violet-500/[0.07] text-violet-300',
  'R+': 'border-pink-500/40 bg-pink-500/[0.09] text-pink-300',
  X: 'border-red-500/40 bg-red-500/[0.08] text-red-300',
  XXX: 'border-red-500/60 bg-red-500/15 text-red-300',
};

export function GenreBadge({ genre }: { genre: string | null }) {
  if (!genre) return null;
  return (
    <span className={cn('inline-flex items-center rounded-md border px-1.5 py-0.5 font-mono text-[10px] font-bold tracking-widest', GENRE_STYLES[genre] ?? 'border-white/10 bg-white/[0.04] text-zinc-400')}>
      {genre}
    </span>
  );
}

export function RatingBadge({ rating }: { rating: string | null }) {
  if (!rating) return null;
  return (
    <span className={cn('inline-flex items-center rounded-md border px-1.5 py-0.5 font-mono text-[10px] font-bold', RATING_STYLES[rating] ?? 'border-white/10 bg-white/[0.04] text-zinc-400')}>
      {rating}
    </span>
  );
}

export function Chip({ children }: { children: React.ReactNode }) {
  return (
    <span className="inline-flex items-center rounded-md border border-white/[0.07] bg-white/[0.035] px-1.5 py-0.5 font-mono text-[11px] text-zinc-400">
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
          h3: (p) => <h3 className="mb-2 mt-7 flex items-center gap-2 text-sm font-bold text-violet-200" {...p} />,
          p: (p) => <p className="mb-3 text-sm leading-relaxed text-zinc-300" {...p} />,
          ul: (p) => <ul className="mb-3 list-disc space-y-1 pl-5 text-sm text-zinc-300 marker:text-violet-400/70" {...p} />,
          ol: (p) => <ol className="mb-3 list-decimal space-y-1 pl-5 text-sm text-zinc-300 marker:text-zinc-600" {...p} />,
          li: (p) => <li className="leading-relaxed" {...p} />,
          strong: (p) => <strong className="font-bold text-white" {...p} />,
          em: (p) => <em className="text-zinc-400" {...p} />,
          hr: () => <hr className="my-7 h-px border-0 bg-gradient-to-r from-transparent via-white/15 to-transparent" />,
          blockquote: (p) => <blockquote className="mb-3 border-l-2 border-violet-400/40 bg-white/[0.02] py-1 pl-3 text-sm italic text-zinc-400" {...p} />,
          code: ({ children, className }) =>
            className?.includes('language-') ? (
              <code className="t5-scroll block whitespace-pre-wrap break-words rounded-lg border border-white/[0.07] bg-black/30 p-3.5 font-mono text-xs leading-relaxed text-zinc-300">{children}</code>
            ) : (
              <code className="rounded-md bg-white/[0.07] px-1.5 py-0.5 font-mono text-xs text-violet-200">{children}</code>
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
          a: (p) => <a className="text-cyan-300 underline decoration-cyan-500/40 underline-offset-2 transition-colors hover:text-cyan-100 hover:decoration-cyan-300" {...p} />,
        }}
      >
        {content}
      </ReactMarkdown>
    </div>
  );
}
