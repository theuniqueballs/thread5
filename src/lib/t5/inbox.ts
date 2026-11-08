/**
 * THREAD 5 — ИНБОКС финальных рендеров. Серверная либа (node, SDK).
 *
 * Поток по приказу автора (вердикт T5-16, 2026-11-08):
 *   1) автор закидывает итоговые рендеры кучкой;
 *   2) КАЖДОЕ изображение проходит X-фильтр-триаж ДО всего остального
 *      (label-only, без описаний контента; fail-closed: любая ошибка триажа
 *      = карантин — «если считаешь такую хуйню, вероятнее всего заглохнешь»);
 *   3) некарантинные разбираются на артефакты/анатомию/камеру — писец ищет
 *      то, что автор не нашёл; журнал живёт на диске рядом с файлами.
 *
 * Хранение: thread5/inbox/ (gitignored) — meta.json + uploads/*.
 * SDK: z-ai-web-dev-sdk ТОЛЬКО здесь (backend).
 */
import { promises as fs } from 'node:fs';
import path from 'node:path';
import { randomBytes } from 'node:crypto';
import { parseBatch } from '@/lib/t5/parse';

const INBOX_DIR = path.join(process.cwd(), 'thread5', 'inbox');
const UPLOADS_DIR = path.join(INBOX_DIR, 'uploads');
const META_PATH = path.join(INBOX_DIR, 'meta.json');

export type TriageLabel = 'sfw' | 'borderline' | 'x' | 'unknown';
export type InboxStatus = 'queued' | 'ok' | 'x' | 'analyzed' | 'error';

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
  tag: string | null; // метка автора, напр. «T5-16 P28»
  status: InboxStatus;
  triage: { label: TriageLabel; reason: string; at: string };
  analysis: {
    at: string;
    severity: 'clean' | 'minor' | 'major';
    findings: InboxFinding[];
    note: string;
  } | null;
  authorOverride: { label: 'sfw' | 'x'; at: string } | null;
}

export const ALLOWED_EXT = ['png', 'jpg', 'jpeg', 'webp'] as const;
export const MAX_FILE_BYTES = 25 * 1024 * 1024;
export const MAX_BATCH_FILES = 40;

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
function extractJson<T>(raw: string | undefined): T | null {
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

/* ── мета-журнал ───────────────────────────────────────────────────────── */

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
  await fs.writeFile(META_PATH, JSON.stringify(items, null, 1), 'utf8');
}

/* ── X-фильтр-триаж: label-only, fail-closed ───────────────────────────── */

interface TriageOut { label: string; reason?: string }

export async function triageImage(mime: string, buf: Buffer): Promise<{ label: TriageLabel; reason: string }> {
  try {
    const raw = await visionJson({
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
    return {
      label: 'x',
      reason: `триаж упал (${String(err instanceof Error ? err.message : err).slice(0, 60)}) — карантин (fail-closed)`,
    };
  }
}

/* ── авто-разбор артефактов (некарь-антинные изображения) ──────────────── */

interface AnalysisOut {
  severity?: string;
  findings?: { kind?: string; where?: string; what?: string }[];
  note?: string;
}

const ANALYSIS_SYSTEM =
  'Ты — технический ревизор рендеров для конвейера аниме-промптов. Ты ищешь ТОЛЬКО дефекты ' +
  'изображения как картинки: сломанная анатомия (пальцы, конечности, сочленения), битые глаза/лицо, ' +
  'артефакты рендера (швы, лишние конечности, расплавленные предметы, случайный текст/водяные знаки), ' +
  'несобранная камера/ракурс (точка съёма не совпадает с заявленной), палитра/свет вне регистра, ' +
  'видовая нестыковка (заявленная анатомия вида не соблюдена). Не описывай сюжет и не оценивай ' +
  'привлекательность. Ответ — ТОЛЬКО JSON: {"severity":"clean|minor|major",' +
  '"findings":[{"kind":"анатомия|руки|глаза|вид|камера|палитра|артефакт|композиция","where":"где на картинке","what":"что сломано"}],"note":"итог одной фразой"}. ' +
  'Без находок: severity "clean", findings []. Не выдумывай дефекты, если их нет.';

/** POS/NEG контекст слота, если автор пометил файл как «T5-16 P28». */
async function slotContext(tag: string | null): Promise<string> {
  if (!tag) return '';
  const m = tag.match(/^(T5-\d+)\s*[-— ]?\s*(P\d{1,3})$/iu);
  if (!m) return '';
  try {
    const raw = await fs.readFile(path.join(process.cwd(), 'thread5', 'batches', `${m[1]}.md`), 'utf8');
    const batch = parseBatch(raw);
    const slot = batch.slots.find((s) => s.id.toLowerCase() === m[2].toLowerCase());
    if (!slot) return '';
    return [
      `Слот ${slot.id} (${slot.slug}) батча ${m[1]}; жанр ${slot.genre ?? '—'}, рейтинг ${slot.rating ?? '—'}.`,
      `POS: ${slot.pos.slice(0, 1200)}`,
      slot.neg ? `NEG: ${slot.neg.slice(0, 500)}` : '',
      'Сверяй картинку с этим промптом: несоблюдение заявленной камеры/вида/палитры — находка kind «камера»/«палитра».',
    ].filter(Boolean).join('\n');
  } catch {
    return '';
  }
}

export async function analyzeItem(item: InboxItem): Promise<InboxItem> {
  const context = await slotContext(item.tag);
  try {
    const buf = await fs.readFile(path.join(UPLOADS_DIR, item.file));
    const raw = await visionJson({
      messages: [{
        role: 'user',
        content: [
          {
            type: 'text',
            text: ANALYSIS_SYSTEM + (context ? `\n\nКОНТЕКСТ ПРОМПТА:\n${context}` : ''),
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
    item.status = 'analyzed';
  } catch (err) {
    item.analysis = {
      at: new Date().toISOString(),
      severity: 'minor',
      findings: [],
      note: `авто-разбор не удался: ${String(err instanceof Error ? err.message : err).slice(0, 120)}`,
    };
    item.status = 'error';
  }
  return item;
}

/* ── сохранение пачки файлов + немедленный триаж ───────────────────────── */

export interface SaveOutcome {
  item: InboxItem | null;
  error?: string;
  origName: string;
}

function safeExt(name: string): string | null {
  const ext = path.extname(name).slice(1).toLowerCase();
  return (ALLOWED_EXT as readonly string[]).includes(ext) ? ext : null;
}

export async function saveAndTriage(file: File, tag: string | null): Promise<SaveOutcome> {
  const ext = safeExt(file.name);
  if (!ext) return { item: null, error: 'не картинка (png/jpg/jpeg/webp)', origName: file.name };
  if (file.size > MAX_FILE_BYTES) return { item: null, error: 'больше 25 МБ', origName: file.name };
  const buf = Buffer.from(await file.arrayBuffer());
  if (buf.length === 0) return { item: null, error: 'пустой файл', origName: file.name };

  const id = randomBytes(6).toString('hex');
  const stamp = new Date().toISOString().replace(/[-:TZ.]/gu, '').slice(0, 14);
  const mime = ext === 'png' ? 'image/png' : ext === 'webp' ? 'image/webp' : 'image/jpeg';
  const fname = `${stamp}-${id}.${ext}`;
  await fs.mkdir(UPLOADS_DIR, { recursive: true });
  await fs.writeFile(path.join(UPLOADS_DIR, fname), buf);

  const triage = await triageImage(mime, buf);
  const item: InboxItem = {
    id,
    file: fname,
    origName: file.name.slice(0, 120),
    size: buf.length,
    mime,
    uploadedAt: new Date().toISOString(),
    tag,
    status: triage.label === 'x' ? 'x' : 'ok',
    triage: { label: triage.label, reason: triage.reason, at: new Date().toISOString() },
    analysis: null,
    authorOverride: null,
  };
  return { item, origName: file.name };
}

/* ── служебное ─────────────────────────────────────────────────────────── */

export function resolveUploadPath(file: string): string | null {
  if (!/^[\w.-]+$/u.test(file)) return null; // только имена внутри uploads/
  return path.join(UPLOADS_DIR, file);
}

export function effectiveLabel(item: InboxItem): TriageLabel {
  if (item.authorOverride) return item.authorOverride.label;
  return item.triage.label;
}
