'use client';

import { useCallback, useEffect, useRef, useState } from 'react';
import { Volume2, VolumeX, Wind } from 'lucide-react';
import { cn } from '@/lib/utils';

/**
 * JUICE — весёлый слой прилавка: пасхалки, звук, конфетти, «золотая нить».
 * Правила слоя:
 *  1) ничего не ломает основной путь: обычный клик работает как работал;
 *  2) звук только по явному действию автора (долгий тап / пасхалка), мьют в шапке;
 *  3) счётчики — в localStorage, никаких серверных следов;
 *  4) prefers-reduced-motion — без тряски и дискотеки.
 */

/* ── звук: мультяшный синтез без ассетов (Web Audio) ─────────────────── */

let audioCtx: AudioContext | null = null;

function getCtx(): AudioContext | null {
  try {
    if (!audioCtx) {
      const Ctor = window.AudioContext ?? (window as unknown as { webkitAudioContext?: typeof AudioContext }).webkitAudioContext;
      if (!Ctor) return null;
      audioCtx = new Ctor();
    }
    if (audioCtx.state === 'suspended') void audioCtx.resume();
    return audioCtx;
  } catch {
    return null;
  }
}

export function isSoundOn(): boolean {
  try {
    return window.localStorage.getItem('t5-sound') !== '0';
  } catch {
    return true;
  }
}

function setSoundOn(on: boolean) {
  try {
    window.localStorage.setItem('t5-sound', on ? '1' : '0');
  } catch {
    /* приватный режим — живёт до перезагрузки */
  }
}

/** Коричневый шум нужной длины — «тело» звука. */
function brownNoise(ctx: AudioContext, seconds: number): AudioBuffer {
  const len = Math.floor(ctx.sampleRate * seconds);
  const buf = ctx.createBuffer(1, len, ctx.sampleRate);
  const data = buf.getChannelData(0);
  let last = 0;
  for (let i = 0; i < len; i += 1) {
    const white = Math.random() * 2 - 1;
    last = (last + 0.02 * white) / 1.02;
    data[i] = last * 3.2;
  }
  return buf;
}

/**
 * Пердёж: brown noise → lowpass с ЛФО-дрожанием частоты (хлопки сфинктера)
 * + АМ-модуляция громкости (трель). rate = «высота голоса».
 */
function synthFart(opts: { rate: number; seconds: number; volume: number }) {
  const ctx = getCtx();
  if (!ctx) return;
  const now = ctx.currentTime;

  const src = ctx.createBufferSource();
  src.buffer = brownNoise(ctx, opts.seconds + 0.15);
  src.playbackRate.value = opts.rate;

  // «размазанный» корпус: низкие частоты с дрожанием
  const lowpass = ctx.createBiquadFilter();
  lowpass.type = 'lowpass';
  lowpass.frequency.value = 320;
  lowpass.Q.value = 4.5;
  const wobble = ctx.createOscillator();
  wobble.type = 'sine';
  wobble.frequency.value = 24 + Math.random() * 14;
  const wobbleGain = ctx.createGain();
  wobbleGain.gain.value = 190;
  wobble.connect(wobbleGain).connect(lowpass.frequency);

  // трель громкости — «ффф-ффф-ффф»
  const amp = ctx.createGain();
  amp.gain.value = 0.85;
  const trem = ctx.createOscillator();
  trem.type = 'triangle';
  trem.frequency.value = 27 + Math.random() * 11;
  const tremGain = ctx.createGain();
  tremGain.gain.value = 0.35;
  trem.connect(tremGain).connect(amp.gain);

  const master = ctx.createGain();
  master.gain.setValueAtTime(0.0001, now);
  master.gain.exponentialRampToValueAtTime(opts.volume, now + 0.03);
  master.gain.setValueAtTime(opts.volume, now + opts.seconds * 0.55);
  master.gain.exponentialRampToValueAtTime(0.0001, now + opts.seconds);

  const highpass = ctx.createBiquadFilter();
  highpass.type = 'highpass';
  highpass.frequency.value = 55;

  src.connect(lowpass).connect(amp).connect(highpass).connect(master).connect(ctx.destination);

  src.start(now);
  src.stop(now + opts.seconds + 0.1);
  wobble.start(now);
  wobble.stop(now + opts.seconds + 0.1);
  trem.start(now);
  trem.stop(now + opts.seconds + 0.1);
}

/* ── счётчик газов: событие + localStorage ────────────────────────────── */

export const FART_EVENT = 't5:fart';

function bumpFartCounter(): number {
  let n = 0;
  try {
    n = Number(window.localStorage.getItem('t5-farts') ?? '0') || 0;
    n += 1;
    window.localStorage.setItem('t5-farts', String(n));
  } catch {
    n = 0;
  }
  window.dispatchEvent(new CustomEvent(FART_EVENT, { detail: n }));
  return n;
}

const FART_LINES = [
  'Слот выпустил пар. Конвейер не пострадал.',
  'ПятыйThread дрогнул, но держится.',
  'Это была заявка-вещь. Первый токен — звук.',
  'Газы конвейера: учтено в памяти.',
  'Немного ароматного B23 в NEG.',
];

/** Пердёж по элементу: звук + пшик-облако + счётчик. */
export function fartAt(el: HTMLElement | null, opts: { mega?: boolean } = {}) {
  if (isSoundOn()) {
    if (opts.mega) {
      synthFart({ rate: 0.62, seconds: 1.15, volume: 0.6 });
      window.setTimeout(() => synthFart({ rate: 0.5, seconds: 0.9, volume: 0.5 }), 220);
      window.setTimeout(() => synthFart({ rate: 0.75, seconds: 0.7, volume: 0.42 }), 520);
    } else {
      synthFart({ rate: 0.72 + Math.random() * 0.6, seconds: 0.42 + Math.random() * 0.35, volume: 0.5 });
    }
  }
  if (el) spawnPuff(el, opts.mega ? 7 : 4);
  const count = bumpFartCounter();
  try {
    // лёгкая отдача на мобилах
    navigator.vibrate?.(opts.mega ? [70, 40, 90] : 55);
  } catch {
    /* нет вибромотора */
  }
  return count;
}

export function randomFartLine(): string {
  return FART_LINES[Math.floor(Math.random() * FART_LINES.length)];
}

/* ── пшик-облако: чистый DOM, живёт ~0.9 с ────────────────────────────── */

function spawnPuff(el: HTMLElement, drops: number) {
  try {
    const rect = el.getBoundingClientRect();
    const layer = document.createElement('div');
    layer.setAttribute('aria-hidden', 'true');
    layer.style.cssText = 'position:fixed;inset:0;pointer-events:none;z-index:80;';
    const cx = rect.left + rect.width / 2;
    const cy = rect.top + rect.height * 0.75;
    for (let i = 0; i < drops; i += 1) {
      const p = document.createElement('span');
      const size = 10 + Math.random() * 22;
      const dx = (Math.random() - 0.5) * 90;
      const dy = -(16 + Math.random() * 44);
      const hue = Math.random() > 0.5 ? 'rgba(214,178,106,0.5)' : 'rgba(200,190,170,0.42)';
      p.style.cssText = [
        'position:absolute',
        `left:${cx - size / 2 + (Math.random() - 0.5) * rect.width * 0.5}px`,
        `top:${cy - size / 2}px`,
        `width:${size}px`,
        `height:${size}px`,
        `border-radius:9999px`,
        `background:radial-gradient(circle at 35% 35%, ${hue}, rgba(255,255,255,0.06) 60%, transparent 72%)`,
        `filter:blur(1.5px)`,
        `--dx:${dx}px`,
        `--dy:${dy}px`,
        `animation:t5-puff 0.9s ease-out forwards`,
        `animation-delay:${i * 45}ms`,
      ].join(';');
      layer.appendChild(p);
    }
    document.body.appendChild(layer);
    window.setTimeout(() => layer.remove(), 1400);
  } catch {
    /* нет DOM — нет облака */
  }
}

/* ── конфетти: canvas-вспышка на 1.6 с ────────────────────────────────── */

export function burstConfetti() {
  try {
    const canvas = document.createElement('canvas');
    canvas.setAttribute('aria-hidden', 'true');
    canvas.style.cssText = 'position:fixed;inset:0;pointer-events:none;z-index:90;';
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    document.body.appendChild(canvas);
    const ctx2d = canvas.getContext('2d');
    if (!ctx2d) {
      canvas.remove();
      return;
    }
    const colors = ['#f2c86f', '#d6973c', '#e0608f', '#7fd4b0', '#a98ef2'];
    const parts = Array.from({ length: 130 }, () => ({
      x: canvas.width / 2 + (Math.random() - 0.5) * canvas.width * 0.5,
      y: canvas.height * 0.32 + (Math.random() - 0.5) * 90,
      vx: (Math.random() - 0.5) * 11,
      vy: -(5 + Math.random() * 8),
      w: 4 + Math.random() * 6,
      h: 7 + Math.random() * 7,
      rot: Math.random() * Math.PI,
      vr: (Math.random() - 0.5) * 0.3,
      color: colors[Math.floor(Math.random() * colors.length)],
    }));
    const t0 = performance.now();
    const tick = (t: number) => {
      const dt = t - t0;
      ctx2d.clearRect(0, 0, canvas.width, canvas.height);
      for (const p of parts) {
        p.x += p.vx;
        p.y += p.vy;
        p.vy += 0.24;
        p.rot += p.vr;
        ctx2d.save();
        ctx2d.translate(p.x, p.y);
        ctx2d.rotate(p.rot);
        ctx2d.globalAlpha = Math.max(0, 1 - dt / 1500);
        ctx2d.fillStyle = p.color;
        ctx2d.fillRect(-p.w / 2, -p.h / 2, p.w, p.h);
        ctx2d.restore();
      }
      if (dt < 1600) requestAnimationFrame(tick);
      else canvas.remove();
    };
    requestAnimationFrame(tick);
  } catch {
    /* без конфетти тоже проживём */
  }
}

/* ── LongPressable: долгий тап, не ломающий обычный клик ──────────────── */

interface LongPressableProps {
  children: React.ReactNode;
  /** длительность, мс (по умолчанию 550) */
  ms?: number;
  onLongPress: (el: HTMLElement) => void;
  className?: string;
  /** доступно с клавиатуры (Enter/Space) — для не-кнопок */
  interactive?: boolean;
  ariaLabel?: string;
  as?: 'span' | 'div';
}

export function LongPressable({ children, ms = 550, onLongPress, className, interactive = true, ariaLabel, as = 'span' }: LongPressableProps) {
  const timer = useRef<number | null>(null);
  const fired = useRef(false);
  const startXY = useRef<{ x: number; y: number } | null>(null);

  const clear = useCallback(() => {
    if (timer.current !== null) {
      window.clearTimeout(timer.current);
      timer.current = null;
    }
  }, []);

  const onPointerDown = useCallback(
    (e: React.PointerEvent<HTMLElement>) => {
      if (e.button !== 0 && e.pointerType === 'mouse') return;
      fired.current = false;
      startXY.current = { x: e.clientX, y: e.clientY };
      clear();
      timer.current = window.setTimeout(() => {
        fired.current = true;
        onLongPress(e.currentTarget);
      }, ms);
    },
    [clear, ms, onLongPress],
  );

  const onPointerMove = useCallback(
    (e: React.PointerEvent<HTMLElement>) => {
      if (!startXY.current) return;
      const dx = e.clientX - startXY.current.x;
      const dy = e.clientY - startXY.current.y;
      if (dx * dx + dy * dy > 64) {
        clear(); // палец поехал — это скролл, не пасхалка
        startXY.current = null;
      }
    },
    [clear],
  );

  const end = useCallback(() => {
    clear();
    startXY.current = null;
    // гасим флаг чуть позже pointerup: click успеет прийти и будет съеден
    window.setTimeout(() => {
      fired.current = false;
    }, 120);
  }, [clear]);

  const onClickCapture = useCallback((e: React.MouseEvent) => {
    if (fired.current) {
      e.preventDefault();
      e.stopPropagation();
    }
  }, []);

  const onKeyDown = useCallback(
    (e: React.KeyboardEvent<HTMLElement>) => {
      if (!interactive) return;
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        onLongPress(e.currentTarget);
      }
    },
    [interactive, onLongPress],
  );

  const Tag = as;
  return (
    <Tag
      className={cn('inline-flex touch-manipulation select-none', className)}
      onPointerDown={onPointerDown}
      onPointerMove={onPointerMove}
      onPointerUp={end}
      onPointerCancel={end}
      onPointerLeave={end}
      onClickCapture={onClickCapture}
      onContextMenu={(e) => e.preventDefault()}
      onKeyDown={onKeyDown}
      role={interactive ? 'button' : undefined}
      tabIndex={interactive ? 0 : undefined}
      aria-label={ariaLabel}
      style={{ WebkitTouchCallout: 'none' } as React.CSSProperties}
    >
      {children}
    </Tag>
  );
}

/* ── пасхалки: Konami → дискотека ─────────────────────────────────────── */

const KONAMI = ['ArrowUp', 'ArrowUp', 'ArrowDown', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'ArrowLeft', 'ArrowRight', 'b', 'a'];

export function useKonami(onHit: () => void) {
  const idx = useRef(0);
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      const t = e.target as HTMLElement | null;
      if (t && (t.tagName === 'INPUT' || t.tagName === 'TEXTAREA' || t.isContentEditable)) return;
      const want = KONAMI[idx.current];
      const got = e.key.length === 1 ? e.key.toLowerCase() : e.key;
      if (got === want) {
        idx.current += 1;
        if (idx.current === KONAMI.length) {
          idx.current = 0;
          onHit();
        }
      } else {
        idx.current = got === KONAMI[0] ? 1 : 0;
      }
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [onHit]);
}

const DISCO_MS = 9000;
let discoTimer: number | null = null;

export function startDisco() {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  document.documentElement.classList.add('t5-disco');
  /* повторный Konami перезапускает таймер, а не даёт старому снять класс раньше времени */
  if (discoTimer !== null) window.clearTimeout(discoTimer);
  discoTimer = window.setTimeout(() => {
    document.documentElement.classList.remove('t5-disco');
    discoTimer = null;
  }, DISCO_MS);
}

/* ── виджеты: золотая нить, звук, счётчик газов ───────────────────────── */

/** Прогресс чтения страницы — «золотая нить» по верхнему краю. */
export function GoldenThread() {
  const ref = useRef<HTMLDivElement | null>(null);
  useEffect(() => {
    let raf = 0;
    const update = () => {
      raf = 0;
      const el = ref.current;
      if (!el) return;
      const doc = document.documentElement;
      const max = doc.scrollHeight - window.innerHeight;
      const pct = max > 0 ? Math.min(1, Math.max(0, window.scrollY / max)) : 0;
      el.style.transform = `scaleX(${pct})`;
      el.style.opacity = pct > 0.005 ? '1' : '0';
    };
    const onScroll = () => {
      if (!raf) raf = requestAnimationFrame(update);
    };
    update();
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onScroll);
    return () => {
      window.removeEventListener('scroll', onScroll);
      window.removeEventListener('resize', onScroll);
      if (raf) cancelAnimationFrame(raf);
    };
  }, []);
  return (
    <div className="pointer-events-none fixed inset-x-0 top-0 z-40 h-[2.5px]" aria-hidden>
      <div
        ref={ref}
        className="h-full w-full origin-left bg-gradient-to-r from-[#f2c86f] via-[#d6973c] to-[#e0608f] opacity-0 shadow-[0_0_8px_rgba(214,151,60,0.55)] transition-opacity duration-300"
        style={{ transform: 'scaleX(0)' }}
      />
    </div>
  );
}

/** Кнопка звука в шапке: мьют/анмьют пасхалок. */
export function SoundToggle() {
  const [on, setOn] = useState(true);
  useEffect(() => {
    let alive = true;
    void (async () => {
      await Promise.resolve();
      if (alive) setOn(isSoundOn());
    })();
    return () => {
      alive = false;
    };
  }, []);
  const toggle = useCallback(() => {
    // вычисляем вне апдейтера: сеттер чистый, звук и localStorage — по одному разу
    const next = !on;
    setOn(next);
    setSoundOn(next);
    if (next) synthFart({ rate: 1.15, seconds: 0.28, volume: 0.32 });
  }, [on]);
  return (
    <button
      type="button"
      onClick={toggle}
      role="switch"
      aria-checked={on}
      title={on ? 'Звук пасхалок: включён (долгий тап на номер слота)' : 'Звук пасхалок: выключен'}
      aria-label={on ? 'Выключить звук пасхалок' : 'Включить звук пасхалок'}
      className={cn(
        't5-btn !px-2.5',
        on ? 'text-t5-accent-bright hover:!border-t5-accent/50' : 'text-zinc-500 hover:text-zinc-300',
      )}
    >
      {on ? <Volume2 className="size-4" /> : <VolumeX className="size-4" />}
    </button>
  );
}

/** Счётчик выпущенных газов — живёт в подвале, появляется после первого пука. */
export function FartBadge() {
  const [count, setCount] = useState(0);
  useEffect(() => {
    let alive = true;
    void (async () => {
      await Promise.resolve();
      if (!alive) return;
      try {
        setCount(Number(window.localStorage.getItem('t5-farts') ?? '0') || 0);
      } catch {
        /* ignore */
      }
    })();
    const onFart = (e: Event) => {
      const n = (e as CustomEvent<number>).detail;
      if (typeof n === 'number') setCount(n);
    };
    window.addEventListener(FART_EVENT, onFart);
    return () => {
      alive = false;
      window.removeEventListener(FART_EVENT, onFart);
    };
  }, []);
  if (count === 0) return null;
  return (
    <span
      className="inline-flex items-center gap-1.5 rounded-md border border-white/[0.08] bg-white/[0.03] px-2 py-1 font-mono text-[10px] tracking-wider text-zinc-500"
      title="Счётчик долгих тапов по номерам слотов и пятёрке. Санитарная норма конвейера."
    >
      <Wind className="size-3 text-t5-mint/70" aria-hidden />
      газов: <span className="font-bold tabular-nums text-t5-mint-bright">{count}</span>
    </span>
  );
}
