/**
 * THREAD 5 — доступ к памяти (файлы контент-корпуса).
 * Прилавок и API читают одни и те же файлы; никакого другого состояния нет.
 *
 * Раскладка (инженерный апгрейд 2026-11-20): контент живёт в КОРНЕ репо
 * (batches/ specs/ verdicts/ docs/ special/ — сюда указывают хук, гейты и
 * квитанции с 2026-11-17, коммит 49313c2). Дубль в thread5/ был заморожен
 * на эре T5-24 (camera.json 1.14.0, 37 карт) и удалён: прилавок читал
 * труп и не видел T5-25/T5-26, SO-07…10 и 3-значные Y-карты.
 *
 * Порядок разрешения T5_ROOT (старые раскладки продолжают работать):
 *   1. env T5_ROOT — явное указание (деплой standalone-сборки);
 *   2. cwd с batches/ — каноничная корневая раскладка;
 *   3. cwd/thread5 — легаси (app-репо + отдельный клон контента).
 *
 * Кэш: всё, что дорого читать+парсить, живёт в памяти процесса с
 * mtime-инвалидацией. Алгоритм один: stat файла → если mtime/size не
 * изменились — отдаём из кэша, иначе перечитываем и перепарсиваем.
 * Списки (listBatches/listSpecial) не читают файлы вовсе, пока сигнатура
 * набора (имя+mtime+size каждого файла) совпадает — только readdir + stat.
 */
import { existsSync } from 'node:fs';
import { readFile, readdir, stat, writeFile, mkdir } from 'node:fs/promises';
import path from 'node:path';
import { parseBatch, type T5Batch } from './parse';
import type { BatchListItem, StoredVerdict } from './types';

/** Где живёт контент-корпус (см. комментарий модуля). */
export function resolveT5Root(): string {
  const env = process.env.T5_ROOT;
  if (env && env.trim()) return path.resolve(env.trim());
  const cwd = process.cwd();
  if (existsSync(path.join(cwd, 'batches'))) return cwd; // каноничная раскладка
  return path.join(cwd, 'thread5'); // легаси: контент-клон рядом с app-репо
}

export const T5_ROOT = resolveT5Root();
export const BATCHES_DIR = path.join(T5_ROOT, 'batches');
export const VERDICTS_DIR = path.join(T5_ROOT, 'verdicts');
export const DOCS_DIR = path.join(T5_ROOT, 'docs');
export const SPECIAL_DIR = path.join(T5_ROOT, 'special');

const SLUG_RE = /^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$/u;

export function isSafeSlug(slug: string): boolean {
  return SLUG_RE.test(slug);
}

/**
 * Естественный порядок полки: «T5-9» < «T5-10» < «T5-100» (лексикографическая
 * сортировка ломается на разных разрядах номеров — инцидент прилавка).
 * Терпит хвост «.md» и суффикс R: работает и для слагов, и для имён файлов.
 */
const SHELF_NUM_RE = /^(T5|SO)-(\d+)(R)?(?=\.|$)/iu;

export function shelfOrder(a: string, b: string): number {
  const ma = SHELF_NUM_RE.exec(a);
  const mb = SHELF_NUM_RE.exec(b);
  if (ma && mb) {
    if (ma[1].toUpperCase() !== mb[1].toUpperCase()) return a.localeCompare(b);
    const na = Number.parseInt(ma[2], 10);
    const nb = Number.parseInt(mb[2], 10);
    if (na !== nb) return na - nb;
    if (!!ma[3] !== !!mb[3]) return ma[3] ? 1 : -1; // T5-05R после T5-05
  }
  return a.localeCompare(b);
}

/** числовой ключ батча для сортировок («T5-10» → 10; нет кода → -1) */
export function batchKey(slug: string | null | undefined): number {
  const m = SHELF_NUM_RE.exec((slug ?? '').trim());
  return m ? Number.parseInt(m[2], 10) : -1;
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
      .sort(shelfOrder); // естественный порядок: T5-9 < T5-10 < T5-100
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
  // секунды в штампе: два вердикта в одну минуту больше не затирают друг друга
  const stamp = `${now.getFullYear()}${pad(now.getMonth() + 1)}${pad(now.getDate())}-${pad(now.getHours())}${pad(now.getMinutes())}${pad(now.getSeconds())}`;
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
  'AGENTS', 'ARS-NOVEAU', 'RENDER-TROUBLES', 'CONSILIUM',
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

/* ── спеки (specs/*.json) с mtime-кэшем: Y-чип и будущие потребители ──── */

const SPEC_RE = /^specs\/[a-z0-9][a-z0-9.-]*\.json$/iu;
const specCache = new Map<string, CacheEntry<unknown>>();

/** JSON-спека из контент-корпуса с mtime-кэшем (camera.json — 521+ карт). */
export async function readSpecJson<T>(rel: string): Promise<T | null> {
  if (!SPEC_RE.test(rel)) return null; // только белый вид «specs/имя.json»
  const p = path.join(T5_ROOT, rel);
  try {
    const s = await statFile(p);
    const key = freshnessKey(s);
    const hit = specCache.get(rel);
    if (hit && hit.key === key) return hit.value as T;
    const value = JSON.parse(await readFile(p, 'utf8')) as T;
    specCache.set(rel, { key, value });
    return value;
  } catch {
    return null;
  }
}

/**
 * Индекс сдачи партий (specs/delivery-index.json) — единственный источник
 * статуса draft/ready/delivered/superseded (двойной аудит 2026-11-20,
 * Коул §6.3 «один модуль окна» + P0-06 «delivery index»). Жребий прилавка
 * фильтрует корпус как печь (tools/t5delivery.py): черновик в batches/
 * не считается «предыдущей партией» до сдачи. Партия без записи —
 * толерантный дефолт «delivered» (легаси-корпус, как в python-зеркале).
 */
export interface DeliveryIndexRow {
  batch?: string;
  status?: string;
}

export async function deliveryStatusMap(): Promise<Map<string, string> | null> {
  const idx = await readSpecJson<{ batches?: DeliveryIndexRow[] }>('specs/delivery-index.json');
  if (!idx?.batches?.length) return null;
  const map = new Map<string, string>();
  for (const row of idx.batches) {
    if (row?.batch) map.set(row.batch, row.status ?? 'delivered');
  }
  return map;
}

export function isDeliveredBatch(statusMap: Map<string, string> | null, slug: string): boolean {
  if (!statusMap) return true; // индекса нет — все партии сданы (легаси)
  return (statusMap.get(slug) ?? 'delivered') === 'delivered';
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
