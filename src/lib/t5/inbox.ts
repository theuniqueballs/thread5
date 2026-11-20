/**
 * THREAD 5 — ИНБОКС финальных рендеров. Серверная либа (node, SDK).
 *
 * Поток по приказу автора (вердикт T5-16, 2026-11-08):
 *   1) автор закидывает итоговые рендеры кучкой — POST только пишет на диск
 *      (быстро, без vision-звонков: долгий запрос = HTML-таймаут шлюза = тухлый JSON);
 *   2) КАЖДОЕ изображение проходит X-фильтр-триаж ОТДЕЛЬНЫМИ ПОРЦИЯМИ
 *      (label-only, без описаний контента; fail-closed: любая ошибка триажа
 *      = карантин — «если считаешь такую хуйню, вероятнее всего заглохнешь»;
 *      fail-closed карантины от 429/сбоев можно перетриажнуть);
 *   3) некарантинные разбираются на артефакты/анатомию/камеру — писец ищет
 *      то, что автор не нашёл; журнал живёт на диске рядом с файлами.
 *
 * Хранение: <T5_ROOT>/inbox/ (gitignored) — meta.json + uploads/* + previews/*.
 * Файлы хранятся ДО явной очистки (DELETE ?all=1 / ?ids=) — писец видит их
 * между сессиями; после разбора пачка убирается кнопками, чтобы не копилась.
 *
 * Слот-маппинг (урок T5-17: пачка перепуталась слотами при закидке):
 *   - канонический тег «T5-18 P07» парсится из имени файла и/или задаётся
 *     пофайлово в UI;
 *   - файл на диске зовётся «T5-18__P07__<штамп>-<id>.webp» — папка читается
 *     по слотам подряд, без контент-матчинга;
 *   - meta.json хранится отсортированным (батч ↓, слот ↑).
 *
 * 2026-11-20: инбокс переехал за контентом (T5_ROOT — resolver store.ts);
 * все операции «прочитал→изменил→записал» сериализуются withMetaLock —
 * параллельные циклы триажа/анализа больше не затирают записи друг друга;
 * слоты — до P999 (парсер батчей давно трёхзначный).
 *
 * SDK: z-ai-web-dev-sdk ТОЛЬКО здесь (backend).
 */
import { promises as fs } from 'node:fs';
import path from 'node:path';
import { randomBytes } from 'node:crypto';
import { parseBatch } from '@/lib/t5/parse';
import { T5_ROOT } from '@/lib/t5/store';

const INBOX_DIR = path.join(T5_ROOT, 'inbox');
const UPLOADS_DIR = path.join(INBOX_DIR, 'uploads');
const PREVIEWS_DIR = path.join(INBOX_DIR, 'previews');
const META_PATH = path.join(INBOX_DIR, 'meta.json');

export type TriageLabel = 'sfw' | 'borderline' | 'x' | 'unknown';
export type InboxStatus = 'queued' | 'ok' | 'x' | 'analyzed' | 'error';

/** Факт-рейтинг кадра по гайду Коула (docs/RATING-REPAIR-2026-11-13.md):
 *  бейдж ≠ факт — считаем то, что ВИДНО в кадре, а не что заявлено в шапке. */
export type ColeRating = 'PG-13' | 'R' | 'R+';
/** Что несёт заряд R+: A — объект-прикрытие, B — геометрия позы+камеры. */
export type ColeCorridor = 'A' | 'B' | 'A+B';

export interface InboxIdentity {
  at: string;
  rating: ColeRating | null; // факт-рейтинг по Коу
  corridor: ColeCorridor | null; // коридор, который несёт заряд
  oneMinute: boolean | null; // one-minute test (гайд Коула §3): заряд живёт без окружения
  slot: string | null; // слот, определённый ЗРЕНИЕМ (когда тега не было)
  slotBatch: string | null; // в каком батче искали слот
  slotConfidence: 'high' | 'mid' | 'low' | null;
  note: string; // одно предложение: почему такой рейтинг
}

export interface InboxFinding {
  kind: string; // анатомия | руки | глаза | вид | камера | палитра | артефакт | композиция
  where: string;
  what: string;
}

export interface InboxItem {
  id: string;
  file: string; // имя файла внутри uploads/
  origName: string;
  size: number;
  mime: string;
  uploadedAt: string;
  tag: string | null; // каноническая метка автора, напр. «T5-16 P28»
  batch: string | null; // «T5-16» — вытащено из тега
  slot: string | null; // «P28» — вытащено из тега
  preview: string | null; // имя файла внутри previews/ (для тяжёлых оригиналов)
  status: InboxStatus;
  triage: { label: TriageLabel; reason: string; at: string };
  analysis: {
    at: string;
    severity: 'clean' | 'minor' | 'major';
    findings: InboxFinding[];
    note: string;
  } | null;
  /** Рейтинг по Коу + слот зрением (заказ автора 2026-11-21: «сам, по мануалу
   *  коула, и определял слот картинки, чтобы тебе потом было проще»). */
  identity: InboxIdentity | null;
  authorOverride: { label: 'sfw' | 'x'; at: string } | null;
}

// лимиты и правила очереди — из чистого модуля (клиент/сервер единый
// источник; см. upload-limits.ts — там же RETRIAGE_RE и needsTriageLike)
export { ALLOWED_EXT, MAX_FILE_BYTES, RETRIAGE_RE } from './upload-limits';
import { ALLOWED_EXT, MAX_FILE_BYTES, needsTriageLike } from './upload-limits';
/** Кап файлов на ОДИН запрос (2026-11-21): клиент режет пачки по 2 файла /
 *  ≤8 МБ (502 шлюза на тяжёлых multipart — Bad Gateway доходит до Next);
 *  4 = небольшой запас для ручного вызова API, легаси-«пачки по 8» теперь
 *  получают понятный 400 вместо таймаута шлюза. */
export const MAX_BATCH_FILES = 4;

/* ── слот-маппинг: из имени файла и свободного текста в канонический тег ── */

/** «P07», «p4», «..._P07.webp» → номер слота 1..999. */
const SLOT_P_RE = /(?:^|[^a-z0-9])P(\d{1,3})(?![a-z0-9])/iu;
/** «07 - name.webp», «04_name.png» → номер слота. */
const LEADING_NUM_RE = /^(\d{1,3})(?:[\s_.-]|$)/u;
/** «T5-18», «t5-07» → код батча. */
const BATCH_CODE_RE = /T5-(\d{1,3})/iu;

function pad2(n: number): string {
  return n < 10 ? `0${n}` : String(n);
}

/** Слот из имени файла: «P07.webp», «t5-18 p7.png», «07 - name.webp» → «P07». */
export function parseSlotFromName(name: string): string | null {
  const m = SLOT_P_RE.exec(name) ?? LEADING_NUM_RE.exec(name);
  if (!m) return null;
  const n = Number.parseInt(m[1], 10);
  if (!Number.isInteger(n) || n < 1 || n > 999) return null;
  return `P${pad2(n)}`;
}

/** Батч из имени файла: «T5-18_07.webp» → «T5-18». */
export function parseBatchFromName(name: string): string | null {
  const m = BATCH_CODE_RE.exec(name);
  if (!m) return null;
  return `T5-${m[1]}`;
}

export interface CanonicalTag {
  tag: string | null; // канонический вид: «T5-18 P07» / «P07» / «T5-18» / свободный текст
  batch: string | null;
  slot: string | null;
}

/** Свободный текст тега → канонический { tag, batch, slot }. */
export function normalizeTag(raw: string | null | undefined): CanonicalTag {
  const text = (raw ?? '').trim().slice(0, 40);
  if (!text) return { tag: null, batch: null, slot: null };
  const batchM = BATCH_CODE_RE.exec(text.toUpperCase());
  const batch = batchM ? `T5-${batchM[1]}` : null;
  const slotM = SLOT_P_RE.exec(text.toUpperCase());
  let slot: string | null = null;
  if (slotM) {
    const n = Number.parseInt(slotM[1], 10);
    if (Number.isInteger(n) && n >= 1 && n <= 999) slot = `P${pad2(n)}`;
  } else if (/^(?:СЛОТ\s*)?\d{1,3}$/iu.test(text)) {
    const n = Number.parseInt(text.replace(/\D+/gu, ''), 10);
    if (Number.isInteger(n) && n >= 1 && n <= 999) slot = `P${pad2(n)}`;
  }
  if (batch || slot) {
    return { tag: [batch, slot].filter(Boolean).join(' '), batch, slot };
  }
  return { tag: text, batch: null, slot: null }; // свободная метка без слота
}

/** Порядок карточек: батч ↓ (по номеру, не строке — T5-9 < T5-10), слот ↑, внутри — новее выше. */
function slotNum(item: Pick<InboxItem, 'slot'>): number {
  const m = /P(\d{1,3})/iu.exec(item.slot ?? '');
  return m ? Number.parseInt(m[1], 10) : 9999;
}

function batchNum(item: Pick<InboxItem, 'batch'>): number {
  const m = /T5-(\d{1,3})/iu.exec(item.batch ?? '');
  return m ? Number.parseInt(m[1], 10) : 0;
}

export function sortItems(items: InboxItem[]): InboxItem[] {
  return [...items].sort((a, b) => {
    const hasA = a.batch ? 1 : 0;
    const hasB = b.batch ? 1 : 0;
    if (hasA !== hasB) return hasA ? -1 : 1; // без тега — в конец
    const na = batchNum(a);
    const nb = batchNum(b);
    if (na !== nb) return nb - na; // T5-18 выше T5-17, T5-100 выше T5-99
    const sa = slotNum(a);
    const sb = slotNum(b);
    if (sa !== sb) return sa - sb;
    return (b.uploadedAt ?? '').localeCompare(a.uploadedAt ?? '');
  });
}

/* ── SDK: минимальная типизация createVision (без any) ─────────────────── */

interface VisionPartText { type: 'text'; text: string }
interface VisionPartImage { type: 'image_url'; image_url: { url: string } }
type VisionPart = VisionPartText | VisionPartImage;

interface VisionMessage { role: 'user' | 'assistant'; content: VisionPart[] }

interface VisionArgs {
  messages: VisionMessage[];
  thinking?: { type: 'disabled' | 'enabled' };
}

interface VisionResponse {
  choices?: { message?: { content?: string } }[];
}

interface VisionClient {
  chat: { completions: { createVision: (args: VisionArgs) => Promise<VisionResponse> } };
}

async function getVisionClient(): Promise<VisionClient> {
  const mod = (await import('z-ai-web-dev-sdk')) as unknown as {
    default: { create: () => Promise<unknown> };
  };
  const zai = await mod.default.create();
  return zai as VisionClient;
}

function dataUrl(mime: string, buf: Buffer): string {
  return `data:${mime};base64,${buf.toString('base64')}`;
}

/** Вытащить JSON-объект из ответа модели (терпит ```-заборы и мусор вокруг). */
function extractJson<T>(raw: string | null | undefined): T | null {
  if (!raw) return null;
  const cleaned = raw.replace(/```(?:json)?/giu, '').trim();
  const start = cleaned.indexOf('{');
  const end = cleaned.lastIndexOf('}');
  if (start < 0 || end <= start) return null;
  try {
    return JSON.parse(cleaned.slice(start, end + 1)) as T;
  } catch {
    return null;
  }
}

async function visionJson(args: VisionArgs): Promise<string | null> {
  const client = await getVisionClient();
  const res = await client.chat.completions.createVision({ ...args, thinking: { type: 'disabled' } });
  return res.choices?.[0]?.message?.content ?? null;
}

/**
 * visionJson с ретраем на 429 И 401/токен-сбои (урок T5-19: «missing X-Token
 * header» приходил пачкой, пока конфиг SDK чинился на уровне окружения —
 * такие карантины потом приходилось перетриаживать руками). Пауза между
 * попытками, чтобы пачка инбокса не рассыпалась в fail-closed карантин.
 */
function sleep(ms: number): Promise<void> {
  return new Promise((r) => setTimeout(r, ms));
}

async function visionJsonRetry(args: VisionArgs): Promise<string | null> {
  const waits = [0, 6000, 12000, 20000];
  let lastErr: unknown = null;
  for (const wait of waits) {
    if (wait > 0) await sleep(wait);
    try {
      return await visionJson(args);
    } catch (err) {
      lastErr = err;
      const msg = String(err instanceof Error ? err.message : err);
      // 429 — рейт-лимит; 401/403/token — временные сбои конфига шлюза
      if (!/429|401|403|too many|token|unauthorized/iu.test(msg)) throw err;
    }
  }
  throw lastErr instanceof Error ? lastErr : new Error(String(lastErr));
}

/* ── мета-журнал (атомарная запись: tmp → rename + мьютекс на RMW) ─────── */

export async function readMeta(): Promise<InboxItem[]> {
  try {
    const raw = await fs.readFile(META_PATH, 'utf8');
    const parsed: unknown = JSON.parse(raw);
    return Array.isArray(parsed) ? (parsed as InboxItem[]) : [];
  } catch {
    return [];
  }
}

export async function writeMeta(items: InboxItem[]): Promise<void> {
  await fs.mkdir(INBOX_DIR, { recursive: true });
  const tmp = `${META_PATH}.tmp`;
  await fs.writeFile(tmp, JSON.stringify(sortItems(items), null, 1), 'utf8');
  await fs.rename(tmp, META_PATH);
}

/**
 * Мьютекс read-modify-write журнала: триаж/анализ/загрузка ходят в meta.json
 * конкурентно (клиент крутит циклы; вкладка пережила перемонтирование) —
 * без сериализации поздний writeMeta затирает чужие записи (2026-11-20).
 */
let metaLockTail: Promise<unknown> = Promise.resolve();

export function withMetaLock<T>(fn: () => Promise<T>): Promise<T> {
  const run = metaLockTail.then(fn, fn);
  metaLockTail = run.then(
    () => undefined,
    () => undefined,
  );
  return run;
}

/* ── X-фильтр-триаж: label-only, fail-closed ───────────────────────────── */

interface TriageOut { label: string; reason?: string }

export async function triageImage(mime: string, buf: Buffer): Promise<{ label: TriageLabel; reason: string }> {
  try {
    const raw = await visionJsonRetry({
      messages: [{
        role: 'user',
        content: [
          {
            type: 'text',
            text:
              'You are a content moderation gate for an image-processing pipeline. ' +
              'Classify the image into exactly one label: ' +
              '"x" = explicit sexual content (visible genitals or sex acts, hard porn); ' +
              '"borderline" = strongly suggestive / heavy fanservice without explicit genitals; ' +
              '"sfw" = everything else. ' +
              'Reply with ONLY this JSON, no prose, no descriptions of the image, ' +
              'never describe body parts or acts: {"label":"sfw|borderline|x","reason":"<max 6 words, neutral>"}.',
          },
          { type: 'image_url', image_url: { url: dataUrl(mime, buf) } },
        ],
      }],
    });
    const parsed = extractJson<TriageOut>(raw);
    const label = parsed?.label;
    if (label === 'sfw' || label === 'borderline' || label === 'x') {
      return { label, reason: parsed?.reason?.slice(0, 80) ?? 'классифицировано триажем' };
    }
    // модель ответила мусором — fail-closed
    return { label: 'x', reason: 'триаж дал нечитаемый ответ — карантин (fail-closed)' };
  } catch (err) {
    const msg = String(err instanceof Error ? err.message : err);
    // 1301/contentFilter — ДЕТЕРМИНИРОВАННЫЙ отказ зрения: кадр слишком горяч
    // для moderation-gate. Это вердикт, а не сбой: ретраи жгут звонки впустую
    // и не дают очереди дренироваться (живой урок 2026-11-21: 13 отказов
    // крутились в цикле бесконечно). Тегаем X и НЕ перетриажируем авто-
    // матически — формулировка без слов-триггеров RETRIAGE_RE/needsTriage.
    if (/contentFilter|1301|unsafe|sensitive/iu.test(msg)) {
      return {
        label: 'x',
        reason: 'контент-фильтр зрения отклонил кадр (1301) — вероятный X, вердикт фильтра (не сбой)',
      };
    }
    return {
      label: 'x',
      reason: `триаж упал (${msg.slice(0, 60)}) — карантин (fail-closed)`,
    };
  }
}

/* ── рейтинг по Коу + слот зрением (заказ автора 2026-11-21) ───────────── */

/** Код последнего батча в batches/ (T5-XX с максимальным XX) — фолбэк,
 *  когда у файла нет ни тега, ни батч-хинта от UI. */
export async function latestBatchCode(): Promise<string | null> {
  try {
    const names = await fs.readdir(path.join(T5_ROOT, 'batches'));
    let best: number | null = null;
    for (const name of names) {
      const m = /^T5-(\d{1,3})\.md$/iu.exec(name);
      if (!m) continue;
      const n = Number.parseInt(m[1], 10);
      if (best === null || n > best) best = n;
    }
    return best === null ? null : `T5-${best}`;
  } catch {
    return null;
  }
}

/** Компактная строка-сигнатура слота для матчинга зрением: раса/персонаж +
 *  первые внешние токены POS (волосы/глаза/кожа стоят в POS рано). */
function slotSignature(pos: string): string {
  return pos.replace(/\s+/gu, ' ').trim().slice(0, 160);
}

/** Список слотов-кандидатов для одного батча: «P05 · персонаж R08 Serpent-kin ·
 *  R+ · сигнатура…». null — батч не читается/пуст. */
export async function slotCandidates(batch: string): Promise<string | null> {
  try {
    const raw = await fs.readFile(path.join(T5_ROOT, 'batches', `${batch}.md`), 'utf8');
    const parsed = parseBatch(raw);
    if (parsed.slots.length === 0) return null;
    return parsed.slots
      .map((s) =>
        `${s.id} · ${s.character ?? '—'} · ${s.rating ?? '—'} · ${slotSignature(s.pos)}`,
      )
      .join('\n');
  } catch {
    return null;
  }
}

/* ── авто-разбор артефактов (некарь-антинные изображения) ──────────────── */

interface AnalysisOut {
  severity?: string;
  findings?: { kind?: string; where?: string; what?: string }[];
  note?: string;
  rating?: string;
  corridor?: string;
  oneMinute?: boolean;
  slot?: string;
  slotConfidence?: string;
}

const ANALYSIS_SYSTEM =
  'Ты — технический ревизор рендеров для конвейера аниме-промптов. Ты ищешь ТОЛЬКО дефекты ' +
  'изображения как картинки: сломанная анатомия (пальцы, конечности, сочленения), битые глаза/лицо, ' +
  'артефакты рендера (швы, лишние конечности, расплавленные предметы, случайный текст/водяные знаки), ' +
  'несобранная камера/ракурс (точка съёма не совпадает с заявленной), палитра/свет вне регистра, ' +
  'видовая нестыковка (заявленная анатомия вида не соблюдена). Не описывай сюжет и не оценивай ' +
  'привлекательность. Не выдумывай дефекты, если их нет.';

/** Блок факт-рейтинга по гайду Коула (docs/RATING-REPAIR-2026-11-13.md):
 *  считаем ЧТО В КАДРЕ, а не что заявлено. Формулировки filter-safe. */
const COLE_RATING_BLOCK =
  '\n\nОтдельно оцени ФАКТ-рейтинг кадра по гайду Коула (бейдж ≠ факт):\n' +
  '- "R+" — в кадре есть коридор A (заметное раскрытие тела, но грудь закрыта объектом: руки/лента/ткань/скотч в руках или на груди) ' +
  'ИЛИ коридор B (интим несёт сама геометрия: низкий ракурс, посадка верхом, mid-action с одеждой, процесс снимания/сдвига); ' +
  'если есть и A, и B — коридор "A+B".\n' +
  '- "R" — лёгкий see-through/прозрачная ткань без объекта-прикрытия, каталог-поза с улыбкой, бельё без геометрии, заряд только в подписи.\n' +
  '- "PG-13" — просто красивая сцена без заявки на заряд.\n' +
  'one-minute test: прикрой мысленно окружение/фон — заряд остаётся в верхних токенах кадра (поза+камера+прикрытие)? ' +
  'Если заряд живёт только за счёт декораций — oneMinute=false.\n' +
  'Ответ строго по фактам кадра, без фантазии о том, «что имелось в виду».';

/** Блок матчинга слота зрением — только когда слот файла неизвестен. */
function slotMatchBlock(batch: string, candidates: string): string {
  return (
    `\n\nСлот файла НЕИЗВЕСТЕН. Матчинг зрением: ниже список слотов батча ${batch} ` +
    '(id · персонаж/раса · заявленный рейтинг · сигнатура POS). ' +
    'Найди ОДИН лучший кандидат по внешности (волосы/глаза/кожа/уши-хвост-рога/наряд) и позе; ' +
    'совпадение по 2+ стабильным признакам — high, по 1 расплывчатому — low; не уверен — confidence low.\n' +
    `КАНДИДАТЫ:\n${candidates}`
  );
}

function normalizeSlotId(v: unknown): string | null {
  const m = /P(\d{1,3})/iu.exec(String(v ?? ''));
  if (!m) return null;
  const n = Number.parseInt(m[1], 10);
  if (!Number.isInteger(n) || n < 1 || n > 999) return null;
  return `P${n < 10 ? `0${n}` : n}`;
}

function normalizeColeRating(v: unknown): ColeRating | null {
  const s = String(v ?? '').toUpperCase().replace(/[^A-Z0-9+-]/gu, '');
  if (s === 'R+') return 'R+';
  if (s === 'R') return 'R';
  if (s === 'PG13' || s === 'PG-13') return 'PG-13';
  return null;
}

function normalizeCorridor(v: unknown): ColeCorridor | null {
  const s = String(v ?? '').toUpperCase().replace(/[^AB+]/gu, '');
  if (s === 'A+B' || s === 'B+A' || s === 'AB' || s === 'BA') return 'A+B';
  if (s === 'A') return 'A';
  if (s === 'B') return 'B';
  return null;
}

/** POS/NEG контекст слота, если файл помечен каноническим тегом «T5-16 P28». */
async function slotContext(batch: string | null, slot: string | null): Promise<string> {
  if (!batch || !slot) return '';
  try {
    const raw = await fs.readFile(path.join(T5_ROOT, 'batches', `${batch}.md`), 'utf8');
    const parsed = parseBatch(raw);
    const s = parsed.slots.find((x) => x.id.toLowerCase() === slot.toLowerCase());
    if (!s) return '';
    return [
      `Слот ${s.id} (${s.slug}) батча ${batch}; жанр ${s.genre ?? '—'}, рейтинг ${s.rating ?? '—'}.`,
      `POS: ${s.pos.slice(0, 1200)}`,
      s.neg ? `NEG: ${s.neg.slice(0, 500)}` : '',
      'Сверяй картинку с этим промптом: несоблюдение заявленной камеры/вида/палитры — находка kind «камера»/«палитра».',
    ].filter(Boolean).join('\n');
  } catch {
    return '';
  }
}

/**
 * Разбор одного элемента: ОДИН vision-звонок = дефекты + факт-рейтинг по Коу
 * + слот зрением (если тега не было). batchHint — выбранный в UI батч;
 * фолбэи: тег файла → хинт UI → последний батч в batches/.
 */
export async function analyzeItem(item: InboxItem, batchHint?: string | null): Promise<InboxItem> {
  const norm = normalizeTag(item.tag);
  const batch = item.batch ?? norm.batch ?? (batchHint ? normalizeTag(batchHint).batch : null) ?? (await latestBatchCode());
  const slot = item.slot ?? norm.slot;
  const context = await slotContext(batch, slot);
  const needSlot = !slot && batch ? await slotCandidates(batch) : null;
  try {
    const buf = await fs.readFile(path.join(UPLOADS_DIR, item.file));
    const jsonShape =
      '{"severity":"clean|minor|major",' +
      '"findings":[{"kind":"анатомия|руки|глаза|вид|камера|палитра|артефакт|композиция","where":"где на картинке","what":"что сломано"}],' +
      '"rating":"PG-13|R|R+","corridor":"A|B|A+B|null","oneMinute":true|false,' +
      (needSlot ? '"slot":"P01..","slotConfidence":"high|mid|low",' : '') +
      '"note":"итог одной фразой"}';
    const raw = await visionJsonRetry({
      messages: [{
        role: 'user',
        content: [
          {
            type: 'text',
            text:
              ANALYSIS_SYSTEM +
              `\nОтвет — ТОЛЬКО JSON без прозы: ${jsonShape}` +
              COLE_RATING_BLOCK +
              (needSlot ? slotMatchBlock(batch ?? '', needSlot) : '') +
              (context ? `\n\nКОНТЕКСТ ПРОМПТА:\n${context}` : ''),
          },
          { type: 'image_url', image_url: { url: dataUrl(item.mime, buf) } },
        ],
      }],
    });
    const parsed = extractJson<AnalysisOut>(raw);
    if (!parsed) throw new Error('разбор дал нечитаемый JSON');
    const severity =
      parsed.severity === 'minor' || parsed.severity === 'major' || parsed.severity === 'clean'
        ? parsed.severity
        : 'minor';
    const findings = (parsed.findings ?? [])
      .slice(0, 12)
      .map((f) => ({
        kind: (f.kind ?? 'артефакт').slice(0, 24),
        where: (f.where ?? '—').slice(0, 120),
        what: (f.what ?? '—').slice(0, 240),
      }));
    item.analysis = {
      at: new Date().toISOString(),
      severity,
      findings,
      note: (parsed.note ?? '').slice(0, 300),
    };

    /* факт-рейтинг по Коу + слот зрением (заказ автора 2026-11-21) */
    const rating = normalizeColeRating(parsed.rating);
    const corridor = normalizeCorridor(parsed.corridor);
    const seenSlot = needSlot ? normalizeSlotId(parsed.slot) : null;
    const slotConfidence =
      parsed.slotConfidence === 'high' || parsed.slotConfidence === 'mid' || parsed.slotConfidence === 'low'
        ? parsed.slotConfidence
        : null;
    item.identity = {
      at: new Date().toISOString(),
      rating,
      corridor,
      oneMinute: typeof parsed.oneMinute === 'boolean' ? parsed.oneMinute : null,
      slot: seenSlot,
      slotBatch: needSlot ? batch : null,
      slotConfidence: needSlot ? slotConfidence : null,
      note: rating
        ? `${rating}${corridor ? ` · коридор ${corridor}` : ''} — по фактам кадра (гайд Коула)`
        : 'рейтинг не определился',
    };

    /* уверенный матч зрения заполняет пустой слот файла — ручные теги
     * автора неприкосновенны (приоритет: ручной тег > зрение) */
    if (seenSlot && (slotConfidence === 'high' || slotConfidence === 'mid') && !item.slot) {
      item.slot = seenSlot;
      item.batch = item.batch ?? batch;
      item.tag = [item.batch, seenSlot].filter(Boolean).join(' ') || item.tag;
    }

    item.status = 'analyzed';
  } catch (err) {
    const msg = String(err instanceof Error ? err.message : err);
    // 1301 — детерминированный отказ фильтра: ретраи бессмысленны, честно
    // говорим автору, что разбор недоступен (урок живого прогона 2026-11-21)
    const filterRefused = /contentFilter|1301|unsafe|sensitive/iu.test(msg);
    item.analysis = {
      at: new Date().toISOString(),
      severity: 'minor',
      findings: [],
      note: filterRefused
        ? 'контент-фильтр зрения отклонил кадр (1301) — авто-разбор недоступен, оцени глазами'
        : `авто-разбор не удался: ${msg.slice(0, 120)}`,
    };
    item.status = 'error';
  }
  return item;
}

/* ── сохранение пачки файлов (БЕЗ триажа — он отдельной порцией) ───────── */

export interface SaveOutcome {
  item: InboxItem | null;
  error?: string;
  origName: string;
}

function safeExt(name: string): string | null {
  const ext = path.extname(name).slice(1).toLowerCase();
  return (ALLOWED_EXT as readonly string[]).includes(ext) ? ext : null;
}

/** Магические байты: расширение может врать, содержимое — нет. */
function sniffMime(buf: Buffer): string | null {
  if (buf.length >= 8 && buf.subarray(0, 8).equals(Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]))) return 'image/png';
  if (buf.length >= 3 && buf[0] === 0xff && buf[1] === 0xd8 && buf[2] === 0xff) return 'image/jpeg';
  if (
    buf.length >= 12 &&
    buf.subarray(0, 4).toString('latin1') === 'RIFF' &&
    buf.subarray(8, 12).toString('latin1') === 'WEBP'
  )
    return 'image/webp';
  return null;
}

const PREVIEW_THRESHOLD = 512 * 1024; // тяжелее — делаем облегчённое превью
const PREVIEW_MAX_DIM = 1152;

/**
 * Превью через sharp: тяжёлые оригиналы (1–25 МБ webp/png) читаются нестабильно,
 * облегчённая копия 1152px q76 — стабильно и быстро. Падение превью не валит загрузку.
 */
async function makePreview(stem: string, mime: string, buf: Buffer): Promise<string | null> {
  if (buf.length <= PREVIEW_THRESHOLD) return null;
  try {
    const sharp = (await import('sharp')).default;
    const out = await sharp(buf, { failOn: 'none' })
      .rotate()
      .resize({ width: PREVIEW_MAX_DIM, height: PREVIEW_MAX_DIM, fit: 'inside', withoutEnlargement: true })
      .webp({ quality: 76 })
      .toBuffer();
    await fs.mkdir(PREVIEWS_DIR, { recursive: true });
    const name = `${stem}.webp`;
    await fs.writeFile(path.join(PREVIEWS_DIR, name), out);
    return name;
  } catch {
    return null;
  }
}

/** Быстрое сохранение: диск + мета со статусом queued. Никаких vision-звонков. */
export async function saveFile(file: File, tag: string | null): Promise<SaveOutcome> {
  const ext = safeExt(file.name);
  if (!ext) return { item: null, error: 'не картинка (png/jpg/jpeg/webp)', origName: file.name };
  if (file.size > MAX_FILE_BYTES) return { item: null, error: 'больше 25 МБ', origName: file.name };
  const buf = Buffer.from(await file.arrayBuffer());
  if (buf.length === 0) return { item: null, error: 'пустой файл', origName: file.name };
  const mime = sniffMime(buf);
  if (!mime) return { item: null, error: 'содержимое не png/jpg/webp (по магическим байтам)', origName: file.name };

  // канонический тег: явный из UI → иначе авто-парс из имени файла
  const explicit = normalizeTag(tag);
  const resolved = explicit.tag
    ? explicit
    : normalizeTag(
      [parseBatchFromName(file.name), parseSlotFromName(file.name)].filter(Boolean).join(' ') || null,
    );

  const id = randomBytes(6).toString('hex');
  const stamp = new Date().toISOString().replace(/[-:TZ.]/gu, '').slice(0, 14);
  const stem = `${stamp}-${id}`;
  // слот-имя файла: «T5-18__P07__20261109…-a1b2c3.webp» — папка читается по слотам
  const prefix = (resolved.tag ?? '').replace(/[^A-Za-z0-9-]+/gu, '_').replace(/^_+|_+$/gu, '');
  const fname = prefix ? `${prefix}__${stem}.${(mime.split('/')[1] ?? ext).replace('jpeg', 'jpg')}` : `${stem}.${(mime.split('/')[1] ?? ext).replace('jpeg', 'jpg')}`;
  await fs.mkdir(UPLOADS_DIR, { recursive: true });
  await fs.writeFile(path.join(UPLOADS_DIR, fname), buf);
  const preview = await makePreview(stem, mime, buf);

  const item: InboxItem = {
    id,
    file: fname,
    origName: file.name.slice(0, 120),
    size: buf.length,
    mime,
    uploadedAt: new Date().toISOString(),
    tag: resolved.tag,
    batch: resolved.batch,
    slot: resolved.slot,
    preview,
    status: 'queued',
    triage: { label: 'unknown', reason: 'в очереди на X-триаж', at: new Date().toISOString() },
    analysis: null,
    identity: null,
    authorOverride: null,
  };
  return { item, origName: file.name };
}

/* ── X-триаж отдельным проходом (порции по 2-3 файла, чтобы не таймаутить шлюз) ── */

/**
 * Кому нужен триаж: новые (queued/unknown) и fail-closed карантины
 * (упавший/задушенный 429 триаж) — пока автор не вынес свой вердикт.
 * Логика — в чистом модуле upload-limits.ts (needsTriageLike): её же
 * крутит клиентский цикл инбокса, дрейф двух берегов исключён.
 */
export function needsTriage(item: InboxItem): boolean {
  return needsTriageLike(item);
}

/** Триаж одного элемента (читает файл с диска, обновляет item in-place). */
export async function triageItem(item: InboxItem): Promise<InboxItem> {
  try {
    const buf = await fs.readFile(path.join(UPLOADS_DIR, item.file));
    const triage = await triageImage(item.mime, buf);
    item.triage = { label: triage.label, reason: triage.reason, at: new Date().toISOString() };
    // статус: карантин бьёт всё (fail-closed), но состоявшийся разбор
    // ('analyzed'/'error') перетриаж не топчет — иначе карточки выпадают
    // из фильтра «разобрано», хотя analysis/identity живы (живой урок 2026-11-21)
    const keep = item.status === 'analyzed' || item.status === 'error';
    item.status = triage.label === 'x' ? 'x' : keep ? item.status : 'ok';
  } catch (err) {
    item.triage = {
      label: 'x',
      reason: `триаж не удался (${String(err instanceof Error ? err.message : err).slice(0, 60)}) — карантин (fail-closed)`,
      at: new Date().toISOString(),
    };
    item.status = 'x';
  }
  return item;
}

/* ── очистка: после разбора пачку убираем, чтобы диск не пух ───────────── */

export interface DeleteReport {
  count: number;
  bytes: number;
  missing: number;
}

async function unlinkQuiet(dir: string, file: string | null | undefined): Promise<number> {
  if (!file) return 0;
  try {
    const st = await fs.stat(path.join(dir, file));
    await fs.unlink(path.join(dir, file));
    return st.size;
  } catch {
    return 0;
  }
}

/** Удалить конкретные id (файл + превью + запись журнала). */
export async function deleteItems(ids: string[]): Promise<DeleteReport> {
  const items = await readMeta();
  const wanted = new Set(ids);
  const victims = items.filter((i) => wanted.has(i.id));
  let bytes = 0;
  let missing = 0;
  for (const item of victims) {
    bytes += await unlinkQuiet(UPLOADS_DIR, item.file);
    const pBytes = await unlinkQuiet(PREVIEWS_DIR, item.preview);
    if (!item.preview && item.size > PREVIEW_THRESHOLD) missing += 1;
    bytes += pBytes;
  }
  const rest = items.filter((i) => !wanted.has(i.id));
  await writeMeta(rest);
  return { count: victims.length, bytes, missing };
}

/** Полная очистка инбокса (файлы + превью + журнал). */
export async function deleteAll(): Promise<DeleteReport> {
  const items = await readMeta();
  let bytes = 0;
  for (const item of items) {
    bytes += await unlinkQuiet(UPLOADS_DIR, item.file);
    bytes += await unlinkQuiet(PREVIEWS_DIR, item.preview);
  }
  // хвосты без журнала (ручные чистки и т.п.) тоже подметаем
  try {
    for (const f of await fs.readdir(UPLOADS_DIR)) bytes += await unlinkQuiet(UPLOADS_DIR, f);
    for (const f of await fs.readdir(PREVIEWS_DIR).catch(() => [] as string[])) bytes += await unlinkQuiet(PREVIEWS_DIR, f);
  } catch {
    /* нет папок — чистить нечего */
  }
  await writeMeta([]);
  return { count: items.length, bytes, missing: 0 };
}

/* ── служебное ─────────────────────────────────────────────────────────── */

export function resolveUploadPath(file: string): string | null {
  // только имена внутри uploads/: без «..», без разделителей, без скрытых
  if (!/^[\w][\w.-]*$/u.test(file) || file.includes('..')) return null;
  return path.join(UPLOADS_DIR, file);
}

export function resolvePreviewPath(file: string): string | null {
  if (!/^[\w][\w.-]*\.webp$/u.test(file) || file.includes('..')) return null;
  return path.join(PREVIEWS_DIR, file);
}

export function effectiveLabel(item: InboxItem): TriageLabel {
  if (item.authorOverride) return item.authorOverride.label;
  return item.triage.label;
}
