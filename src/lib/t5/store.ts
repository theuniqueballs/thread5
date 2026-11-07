/**
 * THREAD 5 — доступ к памяти (файлы репо thread5/).
 * Прилавок и API читают одни и те же файлы; никакого другого состояния нет.
 *
 * Кэш: всё, что дорого читать+парсить, живёт в памяти процесса с
 * mtime-инвалидацией. Алгоритм один: stat файла → если mtime/size не
 * изменились — отдаём из кэша, иначе перечитываем и перепарсиваем.
 * Списки (listBatches/listSpecial) не читают файлы вовсе, пока сигнатура
 * набора (имя+mtime+size каждого файла) совпадает — только readdir + stat.
 */
import { readFile, readdir, stat, writeFile, mkdir } from 'node:fs/promises';
import path from 'node:path';
import { parseBatch, type T5Batch } from './parse';
import type { BatchListItem, StoredVerdict } from './types';

export const T5_ROOT = path.join(process.cwd(), 'thread5');
export const BATCHES_DIR = path.join(T5_ROOT, 'batches');
export const VERDICTS_DIR = path.join(T5_ROOT, 'verdicts');
export const DOCS_DIR = path.join(T5_ROOT, 'docs');
export const SPECIAL_DIR = path.join(T5_ROOT, 'special');

const SLUG_RE = /^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$/u;

export function isSafeSlug(slug: string): boolean {
  return SLUG_RE.test(slug);
}

/* ── mtime-кэш: общие механики ─────────────────────────────────────── */

interface FileStat {
  mtime: Date;
  mtimeMs: number;
  size: number;
}

/** ключ свежести файла: mtimeMs + size */
function freshnessKey(s: FileStat): string {
  return `${s.mtimeMs}:${s.size}`;
}

async function statFile(p: string): Promise<FileStat> {
  const s = await stat(p);
  return { mtime: s.mtime, mtimeMs: s.mtimeMs, size: s.size };
}

interface CacheEntry<T> {
  key: string;
  value: T;
}

/** распарсенные батчи: "batches/T5-07" → T5Batch */
const batchCache = new Map<string, CacheEntry<T5Batch>>();

/** читает файл батча и парсит его только если mtime/size изменились */
async function cachedBatch(
  source: 'batches' | 'special',
  slug: string,
  file: string,
  fresh: string
): Promise<T5Batch> {
  const cacheKey = `${source}/${slug}`;
  const hit = batchCache.get(cacheKey);
  if (hit && hit.key === fresh) return hit.value;
  const dir = source === 'batches' ? BATCHES_DIR : SPECIAL_DIR;
  const text = await readFile(path.join(dir, file), 'utf8');
  const parsed = parseBatch(text);
  batchCache.set(cacheKey, { key: fresh, value: parsed });
  return parsed;
}

/* ── списки батчей / special orders ────────────────────────────────── */

const listCache = new Map<'batches' | 'special', CacheEntry<BatchListItem[]>>();

function summarize(slug: string, batch: T5Batch, mtime: Date, verdictCount: number): BatchListItem {
  const slots = batch.slots;
  const ratingSpread: Record<string, number> = {};
  for (const s of slots) {
    const key = s.rating ?? '—';
    ratingSpread[key] = (ratingSpread[key] ?? 0) + 1;
  }
  return {
    slug,
    file: `${slug}.md`,
    theme: batch.theme,
    title: batch.title,
    slotCount: slots.length,
    expCount: slots.filter((s) => s.genre === 'EXP').length,
    ocCount: slots.filter((s) => s.genre === 'OC').length,
    ratingSpread,
    verdictCount,
    mtime: mtime.toISOString(),
  };
}

/**
 * Список одной полки. Пока сигнатура набора файлов (имя+mtime+size) не
 * изменилась — файлы не читаются и не парсятся: один readdir + волна stat.
 */
async function listSource(source: 'batches' | 'special'): Promise<BatchListItem[]> {
  const dir = source === 'batches' ? BATCHES_DIR : SPECIAL_DIR;
  const prefix = source === 'batches' ? 'T5-' : 'SO-';
  let files: string[] = [];
  try {
    files = (await readdir(dir))
      .filter((f) => f.endsWith('.md') && f.startsWith(prefix) && !f.includes('.gate-report.'))
      .sort();
  } catch {
    return []; // папки может не быть (friend-pass) — полка просто пуста
  }

  const stats: (FileStat | null)[] = await Promise.all(
    files.map((f) => statFile(path.join(dir, f)).catch(() => null))
  );
  const sigParts: string[] = [];
  for (let i = 0; i < files.length; i++) {
    const s = stats[i];
    sigParts.push(s ? `${files[i]}:${freshnessKey(s)}` : `${files[i]}:gone`);
  }
  const sig = sigParts.join('|');

  const cached = listCache.get(source);
  if (cached && cached.key === sig) return cached.value;

  // набор изменился — пересобираем (парсинг берём из batchCache по файлам)
  const verdictCounts = new Map<string, number>();
  for (const v of await listVerdicts()) {
    verdictCounts.set(v.slug, (verdictCounts.get(v.slug) ?? 0) + 1);
  }

  const items: BatchListItem[] = [];
  for (let i = 0; i < files.length; i++) {
    const s = stats[i];
    if (!s) continue;
    const file = files[i];
    const slug = file.replace(/\.md$/u, '');
    try {
      const batch = await cachedBatch(source, slug, file, freshnessKey(s));
      items.push(summarize(slug, batch, s.mtime, verdictCounts.get(slug) ?? 0));
    } catch {
      // битый файл не роняет список
    }
  }
  const entry: CacheEntry<BatchListItem[]> = { key: sig, value: items };
  listCache.set(source, entry);
  return entry.value;
}

export function listBatches(): Promise<BatchListItem[]> {
  return listSource('batches');
}

export async function readBatch(slug: string): Promise<T5Batch | null> {
  if (!isSafeSlug(slug)) return null;
  const file = `${slug}.md`;
  try {
    const s = await statFile(path.join(BATCHES_DIR, file));
    return await cachedBatch('batches', slug, file, freshnessKey(s));
  } catch {
    return null;
  }
}

/* ── SPECIAL ORDERS: штучки вне цикла (заказы автора) ─────────────────── */

export function listSpecial(): Promise<BatchListItem[]> {
  return listSource('special');
}

export async function readSpecial(slug: string): Promise<T5Batch | null> {
  if (!isSafeSlug(slug)) return null;
  const file = `${slug}.md`;
  try {
    const s = await statFile(path.join(SPECIAL_DIR, file));
    return await cachedBatch('special', slug, file, freshnessKey(s));
  } catch {
    return null;
  }
}

/* ── вердикты ──────────────────────────────────────────────────────── */

let verdictsCache: CacheEntry<StoredVerdict[]> | null = null;

/** сигнатура папки вердиктов: readdir + stat каждого файла */
async function verdictsSig(): Promise<string> {
  let files: string[] = [];
  try {
    files = (await readdir(VERDICTS_DIR)).filter((f) => f.endsWith('.md')).sort();
  } catch {
    return ''; // папки может не быть — вердиктов нет
  }
  const stats: (FileStat | null)[] = await Promise.all(
    files.map((f) => statFile(path.join(VERDICTS_DIR, f)).catch(() => null))
  );
  const parts: string[] = [];
  for (let i = 0; i < files.length; i++) {
    const s = stats[i];
    parts.push(s ? `${files[i]}:${freshnessKey(s)}` : `${files[i]}:gone`);
  }
  return parts.join('|');
}

function verdictSlugFromFile(file: string): string {
  const m = file.match(/^(.+?)-verdict/u);
  return m ? m[1] : file.replace(/\.md$/u, '');
}

export async function listVerdicts(slug?: string): Promise<StoredVerdict[]> {
  const sig = await verdictsSig();
  if (verdictsCache === null || verdictsCache.key !== sig) {
    const out: StoredVerdict[] = [];
    try {
      const files = (await readdir(VERDICTS_DIR)).filter((f) => f.endsWith('.md')).sort();
      for (const file of files) {
        try {
          const text = await readFile(path.join(VERDICTS_DIR, file), 'utf8');
          out.push({
            file,
            slug: verdictSlugFromFile(file),
            createdAt: parseVerdictDate(text, file),
            text,
          });
        } catch {
          // пропускаем битые
        }
      }
    } catch {
      return [];
    }
    verdictsCache = { key: sig, value: out.sort((a, b) => a.file.localeCompare(b.file)) };
  }
  const all = verdictsCache.value;
  return slug ? all.filter((v) => v.slug === slug) : all;
}

function parseVerdictDate(text: string, file: string): string {
  const m = text.match(/\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}/u);
  if (m) return m[0].replace(' ', 'T');
  const fm = file.match(/(\d{8})-(\d{4})/u);
  if (fm) return `${fm[1].slice(0, 4)}-${fm[1].slice(4, 6)}-${fm[1].slice(6, 8)}T${fm[2].slice(0, 2)}:${fm[2].slice(2, 4)}`;
  return '';
}

export async function saveVerdict(slug: string, text: string): Promise<StoredVerdict | null> {
  if (!isSafeSlug(slug)) return null;
  const now = new Date();
  const pad = (n: number) => String(n).padStart(2, '0');
  const stamp = `${now.getFullYear()}${pad(now.getMonth() + 1)}${pad(now.getDate())}-${pad(now.getHours())}${pad(now.getMinutes())}`;
  const file = `${slug}-verdict-${stamp}.md`;
  const header = `# Вердикт ${slug} — ${now.toISOString()}\n# (источник: прилавок)\n\n`;
  const body = text.trim() + '\n';
  await mkdir(VERDICTS_DIR, { recursive: true });
  await writeFile(path.join(VERDICTS_DIR, file), header + body, 'utf8');
  // новый файл меняет сигнатуру папки — кэш пересоберётся сам
  return { file, slug, createdAt: now.toISOString(), text: header + body };
}

/* ── доки памяти (docs/ + specs/ + docs/ars/) ──────────────────────── */

const DOC_WHITELIST = [
  'README', 'LAWS', 'TASTE', 'RENDERER_FACTS', 'NICHE', 'LIVING-NOTES',
  'T5-1-BETA', 'ARS-NOVEAU', 'RENDER-TROUBLES', 'CONSILIUM',
  // личные активы автора из specs/ (main — полный кабинет; в friend-pass ветке файлы-заглушки)
  'OC-CANON', 'OC-BODY-ARCHIVE', 'GOLDEN-CORPUS', 'SPECIAL-ROSTER',
  // АРС · ПЛАНЕТЫ — сеансы конвейера (подпуть docs/ars/)
  'ARS-00', 'ARS-01', 'ARS-02', 'ARS-03', 'ARS-04', 'ARS-05',
] as const;
export type DocName = (typeof DOC_WHITELIST)[number];

/** имя дока → файл specs/ (отдаются verbatim в json-блоке) */
const SPEC_DOCS: Partial<Record<DocName, string>> = {
  'OC-CANON': 'specs/oc-canon.json',
  'OC-BODY-ARCHIVE': 'specs/oc-body-archive.json',
  'GOLDEN-CORPUS': 'specs/golden-corpus.json',
  'SPECIAL-ROSTER': 'specs/special-roster.json',
};

/** имя дока → файл внутри thread5/ по подпути (планеты АРС) */
const DOC_PATHS: Partial<Record<DocName, string>> = {
  'ARS-00': 'docs/ars/00-OVERVIEW.md',
  'ARS-01': 'docs/ars/01-SOL.md',
  'ARS-02': 'docs/ars/02-MERCURY.md',
  'ARS-03': 'docs/ars/03-VENUS.md',
  'ARS-04': 'docs/ars/04-EARTH.md',
  'ARS-05': 'docs/ars/05-FURNACE.md',
};

export function isDocName(name: string): name is DocName {
  return (DOC_WHITELIST as readonly string[]).includes(name);
}

export async function readDoc(name: string): Promise<string | null> {
  if (!isDocName(name)) return null;
  const docPath = DOC_PATHS[name as DocName];
  if (docPath) {
    try {
      return await readFile(path.join(T5_ROOT, docPath), 'utf8');
    } catch {
      return null;
    }
  }
  const specPath = SPEC_DOCS[name as DocName];
  if (specPath) {
    try {
      const json = await readFile(path.join(T5_ROOT, specPath), 'utf8');
      return `> verbatim из \`${specPath}\`\n\n\`\`\`json\n${json.trim()}\n\`\`\`\n`;
    } catch {
      return null;
    }
  }
  try {
    return await readFile(path.join(DOCS_DIR, `${name}.md`), 'utf8');
  } catch {
    try {
      return await readFile(path.join(T5_ROOT, `${name}.md`), 'utf8');
    } catch {
      return null;
    }
  }
}
