'use client';

import { useEffect, useMemo } from 'react';
import { BookOpenText, Dices, FileText, Gift, Hash, Layers, MessageSquareQuote, Sparkles, Wand2 } from 'lucide-react';
import { CommandDialog, CommandEmpty, CommandGroup, CommandInput, CommandItem, CommandList, CommandSeparator } from '@/components/ui/command';
import type { BatchListItem } from '@/lib/t5/types';
import { T5_DOCS } from '@/lib/t5/types';

/**
 * КОМАНДНАЯ ПАЛИТРА — быстрый прыжок к батчу / заказу / доку / разделу.
 * ⌘K или Ctrl+K. Ничего не фетчит: списки приходят из состояния страницы,
 * доки — из статического реестра T5_DOCS (контент докачает DocsView).
 */

type NavTab = 'batches' | 'special' | 'inbox' | 'docs' | 'oracle';

interface CommandPaletteProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  batches: BatchListItem[];
  special: BatchListItem[];
  onTab: (tab: NavTab) => void;
  onBatch: (slug: string) => void;
  onSpecial: (slug: string) => void;
  onDoc: (name: string) => void;
}

export function CommandPalette({ open, onOpenChange, batches, special, onTab, onBatch, onSpecial, onDoc }: CommandPaletteProps) {
  useEffect(() => {
    const down = (e: KeyboardEvent) => {
      if (e.key === 'k' && (e.metaKey || e.ctrlKey)) {
        e.preventDefault();
        onOpenChange(!open);
      }
    };
    document.addEventListener('keydown', down);
    return () => document.removeEventListener('keydown', down);
  }, [open, onOpenChange]);

  const docItems = useMemo(() => T5_DOCS.map((d) => ({ name: d.name, title: d.title, hint: d.hint })), []);
  const running = (run: () => void) => () => {
    onOpenChange(false);
    run();
  };

  return (
    <CommandDialog open={open} onOpenChange={onOpenChange}>
      <CommandInput placeholder="Прыжок: T5-07, тема, LAWS, SO-02…" aria-label="Поиск по батчам, заказам и памяти" />
      <CommandList aria-label="Результаты командной палитры">
        <CommandEmpty>Ничего не нашлось — попробуй «T5-» или тему.</CommandEmpty>
        <CommandGroup heading="Разделы">
          <CommandItem onSelect={running(() => onTab('batches'))}>
            <Layers className="size-4 text-t5-accent" /> Батчи <span className="ml-auto font-mono text-[10px] text-zinc-600">1</span>
          </CommandItem>
          <CommandItem onSelect={running(() => onTab('special'))}>
            <Gift className="size-4 text-t5-rose" /> Special Orders <span className="ml-auto font-mono text-[10px] text-zinc-600">2</span>
          </CommandItem>
          <CommandItem onSelect={running(() => onTab('inbox'))}>
            <MessageSquareQuote className="size-4 text-t5-mint" /> Инбокс <span className="ml-auto font-mono text-[10px] text-zinc-600">3</span>
          </CommandItem>
          <CommandItem onSelect={running(() => onTab('docs'))}>
            <BookOpenText className="size-4 text-t5-violet" /> Память <span className="ml-auto font-mono text-[10px] text-zinc-600">4</span>
          </CommandItem>
          <CommandItem onSelect={running(() => onTab('oracle'))}>
            <Wand2 className="size-4 text-t5-oracle" /> Оракул <span className="ml-auto font-mono text-[10px] text-zinc-600">5</span>
          </CommandItem>
          <CommandItem onSelect={running(() => onTab('oracle'))}>
            <Dices className="size-4 text-t5-oracle/80" /> Жребий на следующую партию <span className="ml-auto font-mono text-[10px] text-zinc-600">жребий · кости</span>
          </CommandItem>
        </CommandGroup>
        <CommandSeparator />
        {batches.length > 0 && (
          <CommandGroup heading={`Батчи — ${batches.length}`}>
            {batches.map((b) => (
              <CommandItem key={b.slug} value={`${b.slug} ${b.theme ?? ''} ${b.title}`} onSelect={running(() => onBatch(b.slug))}>
                <Hash className="size-3.5 shrink-0 text-t5-accent/70" />
                <span className="font-mono font-semibold">{b.slug}</span>
                <span className="truncate text-zinc-500">{b.theme ?? b.title}</span>
                {b.verdictCount > 0 && <span className="ml-auto font-mono text-[10px] text-t5-accent/70">✓{b.verdictCount}</span>}
              </CommandItem>
            ))}
          </CommandGroup>
        )}
        {special.length > 0 && (
          <>
            <CommandSeparator />
            <CommandGroup heading={`Special Orders — ${special.length}`}>
              {special.map((s) => (
                <CommandItem key={s.slug} value={`${s.slug} ${s.theme ?? ''} ${s.title}`} onSelect={running(() => onSpecial(s.slug))}>
                  <Sparkles className="size-3.5 shrink-0 text-t5-rose/70" />
                  <span className="font-mono font-semibold">{s.slug}</span>
                  <span className="truncate text-zinc-500">{s.theme ?? s.title}</span>
                </CommandItem>
              ))}
            </CommandGroup>
          </>
        )}
        <CommandSeparator />
        <CommandGroup heading="Память">
          {docItems.map((d) => (
            <CommandItem key={d.name} value={`${d.name} ${d.title} ${d.hint}`} onSelect={running(() => onDoc(d.name))}>
              <FileText className="size-3.5 shrink-0 text-t5-violet/70" />
              <span className="font-semibold">{d.title}</span>
              <span className="truncate text-zinc-500">{d.hint}</span>
            </CommandItem>
          ))}
        </CommandGroup>
      </CommandList>
    </CommandDialog>
  );
}
