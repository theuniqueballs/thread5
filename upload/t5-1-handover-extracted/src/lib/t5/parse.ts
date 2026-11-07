/**
 * THREAD 5 — парсер батча. Единственный источник правды формата.
 * Читает batches/*.md (RAW+ / данбуру-формат), отдаёт типизированную структуру
 * для прилавка и API. Чистая функция: никакой fs, никакой node — можно звать
 * откуда угодно.
 */

export interface T5Slot {
  id: string; // "P01"
  position: number; // 1
  slug: string; // "lua-storm-obsidian"
  rawMeta: string; // "OC · Sol · R+ · PL163 · P52_MEIJI_DUSK"
  genre: string | null; // "OC" | "NICHE" | "VOLT" | "EXQUISITE" | "EXP"
  experimental: boolean; // ⚗ в шапке
  character: string | null; // имя OC / раса ("Sol", "Cat-kin", "—")
  rating: string | null; // "PG-13" | "R" | "R+" | "X"
  pose: string | null; // "PL163"
  palette: string | null; // "P52_MEIJI_DUSK"
  expLetter: string | null; // "α" для EXP
  expHalf: string | null; // "A" | "B"
  thesis: string | null;
  canon: string | null;
  spine: string | null;
  stack: string | null; // "CR-W02 + CR-S17 + CR-E07 + CR-I16"
  stackIds: string[]; // ["CR-W02", ...]
  pos: string; // чистый текст тегов
  neg: string;
}

export interface T5Act {
  title: string; // "ACT I — DISCOVERY"
  slots: T5Slot[];
}

export interface T5Batch {
  slug: string; // "T5-01"
  title: string; // полный H1
  theme: string | null; // из кавычек H1
  format: string | null; // "(RAW+ / данбуру-формат)" из H1
  arc: string; // арка-проза между H1 и ТЕМА-СЛОВА
  themeWords: string[];
  movement: string | null; // ДВИЖОК (одноразовый)
  genreLegend: string | null; // ЖАНРЫ
  structure: string | null; // СТРУКТУРА
  protocol: string | null; // RENDER PROTOCOL
  acts: T5Act[];
  slots: T5Slot[]; // плоско, в порядке файла
  raw: string;
}

/** батч без полного текста: API отдаёт raw только по ?raw=1 */
export type T5BatchBody = Omit<T5Batch, 'raw'>;

const SLOT_RE = /^P(\d{1,3})\s*[—–-]\s*(\S[^(]*?)\s*\((.+)\)\s*$/u;
const FIELD_RE = /^(THESIS|Canon|Spine|Stack|POS|NEG):(.*)$/u;
const ACT_TITLE_RE = /^(ACT\s+[IVX]+[^\n]*|EXP\s+OVERLAY[^\n]*)$/u;
const RATING_RE = /^(PG-13|R\+|R|X|XXX)$/u;
const POSE_RE = /^PL\d{1,3}$/u;
const PALETTE_RE = /^P\d{1,3}_.+$/u;
const GENRE_RE = /^(OC|NICHE|VOLT|EXQUISITE|EXP)$/u;

function isActDelimiter(line: string): boolean {
  const t = line.trim();
  return t.length >= 10 && /^═+$/u.test(t);
}

function isActTitle(lines: string[], i: number): boolean {
  const t = lines[i].trim();
  if (t.length === 0) return false;
  if (ACT_TITLE_RE.test(t)) return true;
  // общая форма: заголовок секции, зажатый между двумя разделителями ══
  // (покрывает OC BLOCK, ACT*, EXP OVERLAY и любые будущие секции)
  return isActDelimiter(lines[i - 1] ?? '') && isActDelimiter(lines[i + 1] ?? '');
}

interface SlotHeader {
  genre: string | null;
  experimental: boolean;
  character: string | null;
  rating: string | null;
  pose: string | null;
  palette: string | null;
}

export function parseSlotHeader(rawMeta: string): SlotHeader {
  const parts = rawMeta.split('·').map((p) => p.trim()).filter(Boolean);
  const experimental = parts.some((p) => p.includes('⚗'));
  let genre: string | null = null;
  let character: string | null = null;
  let rating: string | null = null;
  let pose: string | null = null;
  let palette: string | null = null;

  for (const part of parts) {
    const clean = part.replace(/⚗/gu, '').trim();
    if (genre === null && GENRE_RE.test(clean)) {
      genre = clean;
      continue;
    }
    if (rating === null && RATING_RE.test(clean)) {
      rating = clean;
      continue;
    }
    if (pose === null && POSE_RE.test(clean)) {
      pose = clean;
      continue;
    }
    if (palette === null && PALETTE_RE.test(clean)) {
      palette = clean;
      continue;
    }
    if (character === null && clean.length > 0 && clean !== '—') character = clean;
  }

  return { genre, experimental, character, rating, pose, palette };
}

function extractExpMarker(thesis: string | null): { letter: string | null; half: string | null } {
  if (!thesis) return { letter: null, half: null };
  const m = thesis.match(/^EXP\s+([α-ω])\s*[-–]\s*([AB])\b/u);
  if (!m) return { letter: null, half: null };
  return { letter: m[1], half: m[2] };
}

function parseStackIds(stack: string | null): string[] {
  if (!stack) return [];
  return stack.match(/CR-[A-Z]{1,2}\d{1,3}/gu) ?? [];
}

export function parseBatch(raw: string): T5Batch {
  const lines = raw.split(/\r?\n/);

  // H1
  let title = '';
  let slug = '';
  let theme: string | null = null;
  let format: string | null = null;
  const titleIdx = lines.findIndex((l) => l.startsWith('# '));
  if (titleIdx >= 0) {
    title = lines[titleIdx].replace(/^#\s+/, '').trim();
    const batchM = title.match(/Batch\s+([A-Za-z0-9._-]+)/u);
    if (batchM) slug = batchM[1];
    const themeM = title.match(/[«"]([^»"]+)[»"]/u);
    if (themeM) theme = themeM[1].trim();
    const fmtM = title.match(/—\s*(БАТЧ[^\n]*|\([^\n]*\))\s*$/u);
    if (fmtM) format = fmtM[1].trim();
  }

  // мета-строки шапки + арка
  let movement: string | null = null;
  let genreLegend: string | null = null;
  let structure: string | null = null;
  let protocol: string | null = null;
  let themeWords: string[] = [];
  const arcLines: string[] = [];

  let metaSeen = false;
  for (let i = titleIdx + 1; i < lines.length; i++) {
    const line = lines[i];
    if (isActDelimiter(line)) break;
    const t = line.trim();
    if (t.startsWith('ТЕМА-СЛОВА')) {
      themeWords = t
        .replace(/^ТЕМА-СЛОВА[^:]*:/u, '')
        .trim()
        .split(/[,;]\s*/u)
        .map((w) => w.trim())
        .filter(Boolean);
      metaSeen = true;
      continue;
    }
    if (t.startsWith('ДВИЖОК')) {
      movement = t.replace(/^ДВИЖОК[^:]*:/u, '').trim();
      metaSeen = true;
      continue;
    }
    if (t.startsWith('ЖАНРЫ')) {
      genreLegend = t.replace(/^ЖАНРЫ[^:]*:/u, '').trim();
      metaSeen = true;
      continue;
    }
    if (t.startsWith('СТРУКТУРА')) {
      structure = t.replace(/^СТРУКТУРА[^:]*:/u, '').trim();
      metaSeen = true;
      continue;
    }
    if (t.startsWith('RENDER PROTOCOL')) {
      protocol = t.replace(/^RENDER PROTOCOL[^:]*:/u, '').trim();
      metaSeen = true;
      continue;
    }
    // арка — проза до первой мета-строки
    if (!metaSeen && t.length > 0) arcLines.push(line);
  }
  const arc = arcLines.join('\n').trim();

  // слоты
  const slots: T5Slot[] = [];
  const acts: T5Act[] = [];
  let currentAct: T5Act | null = null;
  let current: T5Slot | null = null;
  let currentField: 'pos' | 'neg' | null = null;

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const t = line.trim();

    if (isActDelimiter(line)) {
      currentField = null;
      continue;
    }
    if (isActTitle(lines, i)) {
      currentField = null;
      currentAct = { title: t, slots: [] };
      acts.push(currentAct);
      continue;
    }

    const slotM = t.match(SLOT_RE);
    if (slotM) {
      currentField = null;
      const id = `P${slotM[1]}`;
      const header = parseSlotHeader(slotM[3].trim());
      current = {
        id,
        position: Number.parseInt(slotM[1], 10),
        slug: slotM[2].trim(),
        rawMeta: slotM[3].trim(),
        thesis: null,
        canon: null,
        spine: null,
        stack: null,
        stackIds: [],
        pos: '',
        neg: '',
        ...header,
        expLetter: null,
        expHalf: null,
      };
      slots.push(current);
      if (currentAct) currentAct.slots.push(current);
      continue;
    }

    if (!current) continue;

    const fieldM = t.match(FIELD_RE);
    if (fieldM) {
      const key = fieldM[1];
      const rest = fieldM[2].trim();
      currentField = null;
      if (key === 'THESIS') {
        // THESIS может быть многострочным
        let thesisText = rest;
        let j = i + 1;
        while (j < lines.length) {
          const rawLine = lines[j];
          const nt = rawLine.trim();
          if (nt === '') {
            let k = j + 1;
            while (k < lines.length && lines[k].trim() === '') k++;
            const ahead = (lines[k] ?? '').trim();
            if (FIELD_RE.test(ahead) || SLOT_RE.test(ahead) || isActTitle(lines, k) || isActDelimiter(lines[k] ?? '')) {
              j = k;
              break;
            }
            j = k;
            continue;
          }
          if (FIELD_RE.test(nt) || SLOT_RE.test(nt) || isActTitle(lines, j) || isActDelimiter(rawLine)) break;
          thesisText += `\n${nt}`;
          j++;
        }
        i = j - 1;
        current.thesis = thesisText.trim() || null;
        const exp = extractExpMarker(current.thesis);
        current.expLetter = exp.letter;
        current.expHalf = exp.half;
        continue;
      }
      if (key === 'Canon') {
        current.canon = rest || null;
        continue;
      }
      if (key === 'Spine') {
        current.spine = rest || null;
        continue;
      }
      if (key === 'Stack') {
        current.stack = rest || null;
        current.stackIds = parseStackIds(current.stack);
        continue;
      }
      if (key === 'POS') {
        currentField = 'pos';
        continue;
      }
      if (key === 'NEG') {
        currentField = 'neg';
        continue;
      }
    }

    if (currentField && t.length > 0) {
      if (currentField === 'pos') current.pos += (current.pos ? '\n' : '') + t;
      else current.neg += (current.neg ? '\n' : '') + t;
    }
  }

  return { slug, title, theme, format, arc, themeWords, movement, genreLegend, structure, protocol, acts, slots, raw };
}
