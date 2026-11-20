/**
 * ECCHI-ORACLE ENGINE — каноническое ядро оракула (эра ORACLE-2, 2026-11-20).
 *
 * Чистый модуль: ноль node-импортов, ноль зависимостей — живёт и в прилавке
 * (браузер), и в API-роутах, и в oracle-service (bun build инлайнит его в
 * бандл — единый источник алгоритма для всего организма).
 *
 * Три слоя вплетения оракула в организм:
 *   1. ОЦЕНКА  — rateTextLite: экспресс-тираж слота без сервиса (зеркало
 *      полного движка oracle-service: те же словари, та же шкала);
 *   2. ЖАР     — batchHeat: метрика здоровья партии (R+-доля, баланс
 *      коридоров, свежесть карт, дрейф label↔fact, дубли каналов);
 *   3. ЖРЕБИЙ  — drawConstellation: детерминированный расклад карт на
 *      следующую партию (mulberry32, seed = номер партии). Тот же seed —
 *      тот же расклад в прилавке, в печи (tools/oracle.py, зеркало на
 *      python) и в сервисе. Паритет лочат золотые векторы
 *      tests/fixtures/oracle_vectors.json (оба тестовых набора читают его).
 *
 * Контракт зеркал (см. docs/ORACLE.md):
 *   - rateTextLite — упрощённое зеркало rateText из oracle-service
 *     (без LLM/vision, без x_risk_drivers; вердикт/коридор/классы совпадают
 *     на корпусе — векторные тесты держат);
 *   - drawConstellation — ЕДИНАЯ реализация: сервис и прилавок импортируют
 *     этот файл; python-зеркало в tools/oracle.py обязано давать побитово
 *     тот же результат (mulberry32 в беззнаковой 32-бит арифметике).
 */

/* ═══════════════════════════ 1. СЛОВАРИКИ ════════════════════════════ */
/* Зеркало сигнальных словарей oracle-service/index.ts (эра Y-STAMP 1.15.0).
 * Порядок слов не важен (матчинг по вхождению с границами слов), но состав
 * держим синхронным с сервисом: правка здесь = правка там = запись в
 * docs/ORACLE.md «реестр зеркал». Техническая лексика классификации. */

export const ENGINE_ERA = 'ORACLE-2 · 2026-11-20 · Y-STAMP 1.15.0 (В34/В35)';

const PG13 = ['sexy outfit', 'bikini', 'cleavage', 'thighs', 'off-shoulder', 'off shoulder', 'bare shoulders',
  'short shorts', 'miniskirt', 'micro skirt', 'midriff', 'crop top', 'zettai ryouiki', 'thighhighs',
  'thighhigh', 'stockings', 'bare back', 'backless', 'swimsuit', 'one-piece', 'pareo', 'sarong',
  'thigh gap', 'bare thighs', 'slit', 'high slit', 'sporty top', 'gym clothes'];

const R_SIG = ['lingerie', 'panties', 'panty shot', 'pantyshot', 'panties visible', 'upskirt', 'bra', 'underwear',
  'underwear only', 'erotic pose', 'microbikini', 'micro bikini', 'sling bikini', 'string bikini',
  'garter belt', 'thong', 'boyshorts', 'side-tie panties', 'bunny suit', 'towel only', 'apron only',
  'naked apron', 'buruma', 'bloomers', 'sarashi', 'fundoshi', 'camisole', 'nightgown', 'negligee',
  'bikini bridge', 'whale tail', 'pajama shorts', 'sleep shirt'];

const RPLUS_HARD = ['visible pantyline', 'pantyline', 'clothed nipples', 'covered nipples', 'taped nipples',
  'topless with tape', 'handbra', 'hand bra', 'hands covering chest', 'arms covering chest',
  'hands covering', 'arm bra', 'covering breasts with hands'];

const RPLUS_SOFT = ['cameltoe', 'camel toe', 'breast clinging', 'extreme fanservice', 'see-through',
  'see through', 'wet clothes', 'tight clothes', 'almost naked', 'breast pressing', 'clinging',
  'sheer panel', 'threadbare', 'nothing underneath', 'no bra', 'without underlayer', 'unlined',
  'braless', 'worn without a bra'];

const X_MARKERS = ['nipples exposed', 'nipples', 'areola', 'exposed breasts', 'bare breasts', 'nude',
  'topless bare', 'naked breasts', 'genitals', 'exposed genitals', 'vulva'];

const CORRIDOR_A = ['hands covering chest', 'arms covering chest', 'handbra', 'hand bra', 'taped nipples',
  'topless with tape', 'towel mid-catch', 'towel caught', 'towel slipping', 'towel only', 'naked apron',
  'apron only', 'shirt as the only', 'worn as the only shirt', 'held to her chest', 'against her chest',
  'over her chest', 'covering her chest', 'at her chest', 'breast line', 'pressed flat against her own chest',
  'palm pressed flat', 'palm pressed', 'holding the dress front', 'holding the dress', 'book against',
  'cup against', 'bundled cloth', 'cloth hugged', 'tail wrapped', 'dress front pressed', 'pressed flat holding'];

const CORRIDOR_B = ['from below', 'low angle', 'slight from below', 'between knees', 'between her knees',
  'door gap', 'through the door', 'straddle', 'straddling', 'settle', 'kneel', 'kneel-back', 'mid-lift',
  'mid-catch', 'mid-pull', 'mid-turn', 'mid-action', 'waistband', 'hem lifted', 'hem pinned', 'hem tucked',
  'hem riding', 'lean back', 'leaning back', 'slipping strap', 'strap slip', 'slid off one shoulder',
  'sliding off one shoulder', 'mid-run', 'mid-step', 'pov'];

const LAYER2 = ['close-up', 'close up', 'cowboy shot', 'upper body', 'portrait', 'full body', 'wide shot',
  'from above', 'from the side', 'dutch angle', 'mirror', 'reflection', 'over shoulder', 'pov',
  'viewed from', 'insert', 'framing'];

const LAYER3 = ['looking at viewer', 'looking at the viewer', 'blush', 'smile', 'smiling', 'smirk', 'grin',
  'parted lips', 'half-closed eyes', 'half-lidded', 'looking back', 'looking away', 'looking down',
  'candid', 'embarrassed', 'surprised', 'teasing', 'gaze', 'eyes closed', 'sleepy', 'yawn', 'gasp'];

const LAYER4 = ['wet', 'soaked', 'steam', 'foam', 'waterline', 'tide-line', 'rain', 'sweat', 'glistening',
  'sheer', 'see-through', 'transparent', 'splashing', 'water at', 'emerging from'];

const DEAD_FABRICS = ['jeans', 'denim', 'leather', 'velvet', 'sweatpants', 'breeches', 'trousers', 'slacks',
  'vinyl', 'suede', 'wool coat', 'parka', 'flannel', 'suit'];

/** safety-флоры: слова, которых в POS быть не должно НИКОГДА (технический линт,
 *  зеркало FLOOR_LINT сервиса; здесь только FAIL-уровень — WARN-флоры живут в
 *  полном движке сервиса). */
const FLOOR_FAIL: { name: string; words: string[]; note: string }[] = [
  { name: 'genital_lock', words: ['exposed genitals', 'vulva', 'pubic hair'], note: 'Генитальный лок POS: слова никогда не пишутся в POS.' },
  { name: 'anti_loli', words: ['child', 'children', 'childish', 'chibi', 'young girl', 'immature body',
    'oversized head', 'loli', 'shota'], note: 'Anti-loli флор: возраст — формой тела; слова запрещены в POS.' },
  { name: 'milf_word', words: ['milf'], note: 'Слово milf запрещено в POS (N30).' },
  { name: 'muscle_law', words: ['muscular', 'ripped', 'six-pack', 'defined abs', 'bulging', 'bodybuilder'], note: 'Мускульный закон: тон soft/firm/toned-lite.' },
  { name: 'xxx_never', words: ['sex', 'sexual act', 'penis', 'cum', 'intercourse', 'половой акт'], note: 'XXX — никогда.' },
];

/* ═════════════════════════ 2. ОЦЕНКА (lite) ══════════════════════════ */

/** матчинг фраз с границами слов — то же поведение, что has() в сервисе */
function hasPhrases(text: string, phrases: string[]): string[] {
  const t = ` ${text.toLowerCase().replace(/[\n\r,;]+/g, ' ')} `;
  return phrases.filter((p) => {
    const needle = p.toLowerCase().replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    return new RegExp(`(^|[^a-zа-яё])${needle}([^a-zа-яё]|$)`, 'i').test(t);
  });
}

function hasAny(text: string, phrases: string[]): boolean {
  return hasPhrases(text, phrases).length > 0;
}

export type OracleTier = 'SFW' | 'PG-13' | 'R' | 'R+' | 'X';
export type OracleCorridor = 'A' | 'B' | 'A+B' | 'NONE';

export interface LiteVerdict {
  tier: OracleTier;
  /** триаж для инбокса: x | borderline | sfw */
  triage: 'x' | 'borderline' | 'sfw';
  corridor: OracleCorridor;
  exposureClasses: string[];
  /** стемы-сигналы по группам (для отладки и подсказок) */
  signals: { pg13: string[]; r: string[]; rplusHard: string[]; rplusSoft: string[]; x: string[] };
  floors: string[];
  warnings: string[];
  era: string;
}

/**
 * Экспресс-оценка POS-текста. Зеркало rateText из oracle-service: без
 * x_risk_drivers и WARN-флоров (это прерогатива полного движка), но вердикт
 * тира, коридор и классы раскрытия совпадают. Векторные тесты держат паритет.
 */
export function rateTextLite(text: string): LiteVerdict {
  const pg = hasPhrases(text, PG13);
  const r = hasPhrases(text, R_SIG);
  const rpHard = hasPhrases(text, RPLUS_HARD);
  const rpSoft = hasPhrases(text, RPLUS_SOFT);

  // X Cut: голые «nipples»/«areola» без смягчающего контекста (как в сервисе)
  const softened = /cloth(ed|ing)|covered|taped|through (her |the )?sweater/i.test(text);
  const bareNipple = X_MARKERS.filter((w) =>
    new RegExp(`(^|[^a-z])${w}([^a-z]|$)`, 'i').test(` ${text.toLowerCase()} `) &&
    !(w === 'nipples' && softened));

  const corridorA = hasPhrases(text, CORRIDOR_A);
  const corridorB = hasPhrases(text, CORRIDOR_B);
  const layer2 = hasPhrases(text, LAYER2);
  const layer3 = hasPhrases(text, LAYER3);
  const layer4 = hasPhrases(text, LAYER4);

  const exposure: string[] = [];
  if (rpHard.length || corridorA.length) exposure.push('COVER');
  if (corridorB.length) exposure.push('PROCESS');
  if (r.length) exposure.push('LINGERIE');
  if (hasAny(text, ['tight', 'clinging', 'fitted', 'taut'])) exposure.push('CLOTHED-TIGHT');
  if (hasAny(text, ['sheer', 'see-through', 'see through', 'transparent', 'wet'])) exposure.push('SHEER');

  const corridor: OracleCorridor =
    corridorA.length && corridorB.length ? 'A+B' : corridorA.length ? 'A' : corridorB.length ? 'B' : 'NONE';

  const layersEngaged = [
    Boolean(pg.length || r.length || rpHard.length),
    layer2.length > 0, layer3.length > 0, layer4.length > 0,
  ].filter(Boolean).length;

  let tier: OracleTier;
  if (bareNipple.length) tier = 'X';
  else if (rpHard.length >= 1 || rpSoft.length >= 2 ||
           (r.length + rpSoft.length >= 3 && layersEngaged >= 2 && corridor !== 'NONE')) tier = 'R+';
  else if (r.length >= 2 || (r.length >= 1 && (layer3.length || layer2.length))) tier = 'R';
  else if (pg.length >= 2 || (pg.length >= 1 && (layer3.length || layer2.length || layer4.length))) tier = 'PG-13';
  else if (pg.length + r.length + rpSoft.length >= 1) tier = 'PG-13';
  else tier = 'SFW';

  const warnings: string[] = [];
  const deadFabric = hasPhrases(text, DEAD_FABRICS);
  if (deadFabric.length && (exposure.includes('SHEER') || exposure.includes('CLOTHED-TIGHT')))
    warnings.push(`Мёртвая ткань (${deadFabric.join(', ')}) не несёт через-ткань заявку — сменить вещь или канал.`);
  if (tier === 'R+' && corridor === 'NONE')
    warnings.push('R+ без коридора: заявка не подтверждена физикой (В33) — план R/PG-13 или добрать коридор.');
  if (hasAny(text, ['sheer', 'see-through', 'see through']) &&
      !hasAny(text, ['nothing underneath', 'no bra', 'without underlayer', 'unlined', 'worn without a bra', 'braless']))
    warnings.push('Sheer без bare-under маркера: движок достроит подслой поверх NEG-лока. Добавь nothing underneath + подслой в NEG.');

  const floors = FLOOR_FAIL.flatMap((f) => {
    const hits = hasPhrases(text, f.words);
    return hits.length ? [`${f.name}: ${hits.join(', ')} — ${f.note}`] : [];
  });

  return {
    tier,
    triage: tier === 'X' ? 'x' : tier === 'R+' || tier === 'R' ? 'borderline' : 'sfw',
    corridor,
    exposureClasses: exposure,
    signals: { pg13: pg, r, rplusHard: rpHard, rplusSoft: rpSoft, x: bareNipple },
    floors,
    warnings,
    era: ENGINE_ERA,
  };
}

/* ═══════════════════════ 3. КАРТЫ И РОТАЦИЯ ══════════════════════════ */

/** минимальная форма карты, нужная алгоритмам (прилавок мапит camera.json) */
export interface OracleCard {
  id: string;            // "Y513"
  corridor: string;      // "A" | "B" | "A+B" | "—"
  exposureClass: string; // "COVER" | "PROCESS" | "CLOTHED-TIGHT" | "—"
  pattern: string;       // вплетение (строка 3 POS, В34)
  /** поза-обёртка "PL###" — окно поз §7 исключает карты на позах окна (обкатка T5-27, проблема №1) */
  builtFrom?: string;
}

/** история использования карты по корпусу */
export interface CardUsage {
  id: string;
  usedCount: number;
  /** номер партии последнего использования (null — никогда) */
  lastBatch: number | null;
  /** имя файла последнего использования (для подсказок) */
  lastBatchFile: string | null;
}

export interface RotationWindow {
  /** глубина окна (сколько последних партий смотрим) */
  depth: number;
  /** партии в окне, по убыванию номера: [{no, file}] */
  batches: { no: number; file: string }[];
  /** Y-id → партия, где карта использована (в пределах окна) */
  usedInWindow: Record<string, string>;
}

/**
 * Окно ротации Y-карт по корпусу батчей. Зеркало load_prev_y_usage из
 * tools/gates.py v1.16.0: только партии С НОМЕРОМ МЕНЬШЕ `batchNo` (правка
 * старого батча не должна видеть «будущие» партии), окно = последние
 * `depth` партий по номеру. depth=0 — окно выключено.
 *
 * Слоты приходят распарсенными (parseBatch): прилавок читает корпус сам,
 * печь — своим парсером, сервису отдаёт клиент. Алгоритм один.
 */
export function buildRotationWindow(
  batches: { slug: string; slots: { yCard: string | null }[] }[],
  batchNo: number,
  depth: number,
): RotationWindow {
  const numbered = batches
    .map((b) => {
      const m = /^(?:T5)-(\d+)$/i.exec(b.slug.trim());
      return m ? { no: Number.parseInt(m[1], 10), file: `${b.slug}.md`, b } : null;
    })
    .filter((x): x is { no: number; file: string; b: { slug: string; slots: { yCard: string | null }[] } } => x !== null)
    .filter((x) => (batchNo <= 0 ? true : 0 < x.no && x.no < batchNo))
    .sort((a, b) => a.no - b.no);

  const windowBatches = depth > 0 ? numbered.slice(-depth) : [];
  const usedInWindow: Record<string, string> = {};
  for (const w of windowBatches) {
    for (const s of w.b.slots) {
      if (s.yCard && !(s.yCard in usedInWindow)) usedInWindow[s.yCard] = w.file;
    }
  }
  return {
    depth,
    batches: windowBatches.map((w) => ({ no: w.no, file: w.file })).reverse(),
    usedInWindow,
  };
}

/** карточка использования по корпусу (для свежести и подсказок «давненько») */
export function buildCardUsage(
  batches: { slug: string; slots: { yCard: string | null }[] }[],
  batchNo: number,
): Record<string, CardUsage> {
  const usage: Record<string, CardUsage> = {};
  const push = (id: string, file: string, no: number) => {
    const u = usage[id] ?? { id, usedCount: 0, lastBatch: null, lastBatchFile: null };
    u.usedCount += 1;
    if (u.lastBatch === null || no > u.lastBatch) { u.lastBatch = no; u.lastBatchFile = file; }
    usage[id] = u;
  };
  for (const b of batches) {
    const m = /^(?:T5)-(\d+)$/i.exec(b.slug.trim());
    if (!m) continue;
    const no = Number.parseInt(m[1], 10);
    if (batchNo > 0 && no >= batchNo) continue; // только прошлое
    for (const s of b.slots) if (s.yCard) push(s.yCard, `${b.slug}.md`, no);
  }
  return usage;
}

/* ═════════════════════════ 4. ЖАР ПАРТИИ ═════════════════════════════ */

/** окно ПОЗ ротации (§7): PL-коды слотов последних depth партий до batchNo —
 *  карты жребия, чьи built_from попадают в это множество, не раздаются
 *  (обкатка T5-27, проблема №1: Y-окно чисто, а поза карты — в бане) */
export function buildPoseWindow(
  batches: { slug: string; slots: { pose: string | null }[] }[],
  batchNo: number,
  depth: number,
): string[] {
  const numbered = batches
    .map((b) => {
      const m = /^(?:T5)-(\d+)$/i.exec(b.slug.trim());
      return m ? { no: Number.parseInt(m[1], 10), b } : null;
    })
    .filter((x): x is { no: number; b: { slug: string; slots: { pose: string | null }[] } } => x !== null)
    .filter((x) => (batchNo <= 0 ? true : 0 < x.no && x.no < batchNo))
    .sort((a, b) => a.no - b.no);
  const windowBatches = depth > 0 ? numbered.slice(-depth) : [];
  const poses = new Set<string>();
  for (const w of windowBatches) {
    for (const s of w.b.slots) if (s.pose) poses.add(s.pose);
  }
  return [...poses];
}

export interface HeatSlotDrift {
  slotId: string;
  label: string | null;
  fact: string;
  /** label ≠ fact по lite-движку (кандидат на проверку глазом, не приговор) */
  drift: string | null;
  /** чем считали факт: weave — реестровое вплетение В34 · lite — словари тег-эры */
  basis: 'weave' | 'lite' | '—';
}

export interface BatchHeat {
  slug: string;
  slotCount: number;
  ratedCount: number;
  ratingSpread: Record<string, number>;
  rplusShare: number;
  corridorHistogram: Record<string, number>;
  /** карты в слотах: всего/свежих (до этой партии не использованных)/в окне */
  cardsUsed: number;
  cardsFresh: number;
  cardsWindowClash: number;
  /** доля слотов с Y-картой */
  cardShare: number;
  drifts: HeatSlotDrift[];
  driftCount: number;
  channelDupes: { channel: string; count: number }[];
  /** жар 0..100 (эвристика, НЕ вердикт — вердикт выносит автор) */
  score: number;
  label: 'ГОРЯЧО' | 'ТЁПЛЫЙ' | 'ХОЛОДНЫЙ';
  formula: string;
}

const HEAT_WEIGHTS = { rplus: 0.3, corridor: 0.2, freshness: 0.2, honesty: 0.15, channels: 0.15 } as const;

/** нормализация для вплетенческой подстрочной сверки (как в ystamp) */
const normWsLower = (s: string) => s.replace(/\s+/gu, ' ').trim().toLowerCase();

/**
 * Жар-метрика партии: сколько конвейерного здоровья в батче. Эвристика для
 * прилавка и жребия — НЕ замена гейтам (те проверяют контракт слота) и НЕ
 * замена вердикту автора. Компоненты:
 *   rplus      — доля R+ в рейтинг-слотах против коридора плана [0.30..0.60];
 *   corridor   — баланс A/B (min/max);
 *   freshness  — доля свежих Y-карт (не использованных до партии);
 *   honesty    — ЧЕСТНОСТЬ ПО ДВУМ БАЗИСАМ (эра В34/В35):
 *                слот с Y-картой — фактом считается ВПЛЕТЕНИЕ (паттерн карты
 *                1:1 подстрокой в POS — реестровое, без словарей; прозу
 *                тег-словари не читают — урок замера T5-26: drift 33/33);
 *                слот без карты — lite-дрейф label↔fact (словари тег-эры,
 *                на прозе шумят — потому только для бескарточных);
 *   channels   — доля уникальных каналов доставки.
 */
export function batchHeat(
  batch: { slug: string; slots: { id: string; rating: string | null; corridor: string | null; channel: string | null; yCard: string | null; pos: string }[] },
  usage: Record<string, CardUsage>,
  cardsById?: Record<string, { pattern?: string; components?: { pose?: string } }>,
): BatchHeat {
  const slots = batch.slots;
  const spread: Record<string, number> = {};
  for (const s of slots) {
    const key = s.rating ?? '—';
    spread[key] = (spread[key] ?? 0) + 1;
  }
  const rated = slots.filter((s) => s.rating && s.rating !== '—');
  const rplus = rated.filter((s) => s.rating === 'R+').length;
  const rplusShare = rated.length ? rplus / rated.length : 0;

  const corr: Record<string, number> = {};
  for (const s of slots) {
    const key = (s.corridor ?? '—').trim() || '—';
    corr[key] = (corr[key] ?? 0) + 1;
  }

  const withCard = slots.filter((s) => s.yCard);
  const fresh = withCard.filter((s) => !usage[s.yCard as string]).length;
  // карты, использованные в последних 3 партиях ДО этого батча — «горячий хвост»
  const batchNo = Number.parseInt(/(\d+)$/u.exec(batch.slug)?.[1] ?? '0', 10);
  let windowClash = 0;
  if (batchNo > 0) {
    const recent = new Set<number>();
    for (const u of Object.values(usage)) {
      if (u.lastBatch !== null && u.lastBatch > batchNo - 4 && u.lastBatch < batchNo) recent.add(u.lastBatch);
    }
    for (const s of withCard) {
      const u = usage[s.yCard as string];
      if (u && u.lastBatch !== null && u.lastBatch > batchNo - 4 && u.lastBatch < batchNo) windowClash += 1;
    }
    void recent;
  }

  const drifts: HeatSlotDrift[] = [];
  for (const s of slots) {
    const card = s.yCard ? cardsById?.[s.yCard] : undefined;
    const pattern = card ? String(card.components?.pose || card.pattern || '') : '';
    if (card && pattern.trim()) {
      // В34-базис: факт = вплетение 1:1 (реестровое, прозо-устойчивое)
      const weaved = normWsLower(s.pos).includes(normWsLower(pattern));
      drifts.push({
        slotId: s.id,
        label: s.rating,
        fact: weaved ? 'weave 1:1' : 'weave missing',
        drift: weaved ? null : `вплетение ${s.yCard} не найдено в POS 1:1 (В34)`,
        basis: 'weave',
      });
    } else if (s.pos.trim() && s.rating && s.rating !== '—') {
      const lite = rateTextLite(s.pos);
      // юрисдикция словарей: ноль сигналов = прозаявка В35, которую тег-словари
      // эры 1.13 не читают (урок T5-26: 14/14 ложных дрейфов на мейнах).
      // Словари судят только тех, кого видят — вне юрисдикции не дрейф.
      const seen = lite.signals.pg13.length + lite.signals.r.length +
        lite.signals.rplusHard.length + lite.signals.rplusSoft.length;
      if (seen > 0) {
        const norm = (x: string) => x.replace('RPLUS', 'R+').toUpperCase();
        const drift = norm(s.rating) !== lite.tier ? `${norm(s.rating)} ≠ fact ${lite.tier}` : null;
        drifts.push({ slotId: s.id, label: s.rating, fact: lite.tier, drift, basis: 'lite' });
      } else {
        drifts.push({ slotId: s.id, label: s.rating, fact: 'проза вне словарей', drift: null, basis: '—' });
      }
    }
  }
  const driftCount = drifts.filter((d) => d.drift).length;
  // честность считается только по юрисдикционным слотам (weave + lite со сигналами)
  const jurisdiction = drifts.filter((d) => d.basis !== '—');
  const honestScoreBase = jurisdiction.length ? drifts.filter((d) => d.basis !== '—' && !d.drift).length / jurisdiction.length : 1;

  const channels: Record<string, number> = {};
  for (const s of slots) {
    const c = (s.channel ?? '').trim();
    if (c) channels[c] = (channels[c] ?? 0) + 1;
  }
  const channelDupes = Object.entries(channels)
    .filter(([, n]) => n > 1)
    .map(([channel, count]) => ({ channel, count }))
    .sort((a, b) => b.count - a.count);

  // компоненты 0..1
  const rplusScore = rplusShare <= 0 ? 0 : rplusShare < 0.3 ? rplusShare / 0.3 * 0.7 : rplusShare <= 0.6 ? 1 : Math.max(0, 1 - (rplusShare - 0.6) / 0.4);
  const aSide = corr['A'] ?? 0;
  const bSide = corr['B'] ?? 0;
  const ab = corr['A+B'] ?? 0;
  const corrMax = Math.max(aSide + ab, bSide + ab, 1);
  const corridorScore = Math.min(aSide + ab, bSide + ab) / corrMax;
  const freshnessScore = withCard.length ? fresh / withCard.length : 0.5; // без карт — нейтрально
  const honestyScore = honestScoreBase;
  const channelTotal = Object.values(channels).reduce((a, b) => a + b, 0);
  const channelsScore = channelTotal ? Object.keys(channels).length / channelTotal : 1;

  const score = Math.round(100 * (
    HEAT_WEIGHTS.rplus * rplusScore +
    HEAT_WEIGHTS.corridor * corridorScore +
    HEAT_WEIGHTS.freshness * freshnessScore +
    HEAT_WEIGHTS.honesty * honestyScore +
    HEAT_WEIGHTS.channels * channelsScore
  ));

  return {
    slug: batch.slug,
    slotCount: slots.length,
    ratedCount: rated.length,
    ratingSpread: spread,
    rplusShare: Number(rplusShare.toFixed(3)),
    corridorHistogram: corr,
    cardsUsed: withCard.length,
    cardsFresh: fresh,
    cardsWindowClash: windowClash,
    cardShare: slots.length ? Number((withCard.length / slots.length).toFixed(3)) : 0,
    drifts,
    driftCount,
    channelDupes,
    score,
    label: score >= 75 ? 'ГОРЯЧО' : score >= 50 ? 'ТЁПЛЫЙ' : 'ХОЛОДНЫЙ',
    formula: 'жар = 0.30·R+-доля + 0.20·баланс коридоров + 0.20·свежесть карт + 0.15·честность label + 0.15·уникальность каналов (эвристика, вердикт — автор)',
  };
}

/* ═════════════════════════ 5. ЖРЕБИЙ ОРАКУЛА ════════════════════════ */

/**
 * mulberry32 — детерминированный PRNG. Вся арифметика в беззнаковом 32-бит
 * домене (JS: >>> 0 / Math.imul; python-зеркало: & 0xFFFFFFFF — биты
 * совпадают, что и лочат золотые векторы).
 */
export function mulberry32(seed: number): () => number {
  let a = seed >>> 0;
  return () => {
    a = (a + 0x6d2b79f5) | 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

/** числовой ключ карты («Y513» → 513; мусор → -1) */
export function cardNum(id: string): number {
  const m = /^Y(\d{1,4})$/i.exec(id.trim());
  return m ? Number.parseInt(m[1], 10) : -1;
}

export interface DrawCard {
  id: string;
  corridor: string;
  exposureClass: string;
  pattern: string;
  /** почему оракул вытянул именно её */
  reason: string;
}

export interface DrawResult {
  batchNo: number;
  seed: number;
  oc: DrawCard[];
  main: DrawCard[];
  exp: DrawCard[];
  /** сколько карт отсечено окном ротации */
  windowExcluded: number;
  /** сколько карт село на позы PL-окна (обкатка T5-27) */
  windowPosesExcluded: number;
  /** сколько карт не хватило (пул иссяк) — 0 = расклад полный */
  shortfall: number;
  determinism: string;
}

export interface DrawOptions {
  /** OC-карт (R+-способные, коридор A/A+B, класс COVER в приоритете) */
  ocTarget?: number;
  /** мейн-карт (баланс коридоров a/b/mid) */
  mainTarget?: number;
  /** EXP-карт (новенькие — никогда не использованные, старшие номера) */
  expTarget?: number;
  /** глубина окна ротации (по умолчанию 3, как y_assembly.window) */
  windowDepth?: number;
  /** PL-окно поз (LAWS §7): карты, чьи built_from-позы в окне, не раздаются.
   *  Обкатка T5-27, проблема №1: жребий вычёл только Y-окно, а Y81→PL63 и
   *  Y95→PL78 сели на позы-запреты. Пустой список/undefined = фильтр выключен
   *  (fixture-карты без builtFrom проходят насквозь — векторы не тронуты). */
  windowPoses?: string[];
}

/** сортировка карт по номеру — стабильная база для детерминизма */
function byNum(a: OracleCard, b: OracleCard): number {
  return cardNum(a.id) - cardNum(b.id);
}

/**
 * ЖРЕБИЙ ОРАКУЛА — детерминированный расклад карт на партию №batchNo.
 *
 * Правила (доктрина корпуса: RAW+ 24/33 слота = 3 OC + 21 мейн + EXP-оверлей;
 * «новенькие Y которых ещё не создавали» — заказ автора T5-26; «давненько не
 * было» — живой лист):
 *   - окно ротации: карты из последних `windowDepth` партий НЕ раздаются;
 *   - OC: коридор A/A+B, класс COVER в приоритете, свежесть решает порядок;
 *   - мейн: круглый обход корзин [a, b, mid] — баланс коридоров; A+B живёт
 *     в a и b одновременно; mid («—») — низкие тиры;
 *   - EXP: только никогда не использованные, старшие номера в приоритете;
 *   - rng тратится в ЖЁСТКОМ порядке: по одному вызову на слот, никаких
 *     rng-тайбрейков в сортировках — иначе зеркала разъедутся.
 *
 * Тот же (batchNo, cards, usage, окно) → тот же расклад. Всегда.
 */
export function drawConstellation(
  batchNo: number,
  cards: OracleCard[],
  usage: Record<string, CardUsage>,
  opts: DrawOptions = {},
): DrawResult {
  const ocTarget = Math.max(0, opts.ocTarget ?? 3);
  const mainTarget = Math.max(0, opts.mainTarget ?? 21);
  const expTarget = Math.max(0, opts.expTarget ?? 9);
  const windowDepth = Math.max(0, opts.windowDepth ?? 3);

  // окно: партии с номером < batchNo, последние windowDepth по номеру
  const windowNos = new Set<number>();
  if (windowDepth > 0 && batchNo > 0) {
    const past = new Set<number>();
    for (const u of Object.values(usage)) if (u.lastBatch !== null && u.lastBatch < batchNo) past.add(u.lastBatch);
    const sorted = [...past].sort((a, b) => a - b).slice(-windowDepth);
    for (const n of sorted) windowNos.add(n);
  }
  const inWindow = (id: string): boolean => {
    const u = usage[id];
    return Boolean(u && u.lastBatch !== null && windowNos.has(u.lastBatch));
  };

  // обкатка T5-27, проблема №1: PL-окно поз — карта на позе окна не раздаётся
  const poseWindow = new Set(opts.windowPoses ?? []);
  const poseBanned = (c: OracleCard): boolean =>
    poseWindow.size > 0 && Boolean(c.builtFrom) && poseWindow.has(c.builtFrom as string);

  const usable = cards
    .filter((c) => c.id && cardNum(c.id) > 0 && c.pattern.trim() && !inWindow(c.id) && !poseBanned(c))
    .sort(byNum);
  const poolA = usable.filter((c) => c.corridor === 'A' || c.corridor === 'A+B');
  const poolB = usable.filter((c) => c.corridor === 'B' || c.corridor === 'A+B');
  const poolMid = usable.filter((c) => c.corridor === '—' || c.corridor === '-' || !c.corridor.trim());

  // OC: A-сторона, COVER в приоритете, потом свежесть (никогда → старые → частые)
  const ocPool = [...poolA].sort((x, y) => ocRank(y, usage) - ocRank(x, usage));
  // EXP: никогда не использованные, старшие номера первыми (без rng-тайбрейков)
  const expPool = usable
    .filter((c) => !usage[c.id])
    .sort((x, y) => cardNum(y.id) - cardNum(x.id));

  const seed = ((batchNo * 2654435761) >>> 0) || 1; // Knuth multiplicative, batchNo=0 → 1
  const rng = mulberry32(seed);

  const drawn = new Set<string>();
  const shortfall = { n: 0 };
  const take = (pool: OracleCard[], reason: (c: OracleCard) => string): DrawCard | null => {
    const live = pool.filter((c) => !drawn.has(c.id));
    if (!live.length) return null;
    const pick = live[Math.floor(rng() * live.length) % live.length];
    drawn.add(pick.id);
    return { id: pick.id, corridor: pick.corridor, exposureClass: pick.exposureClass, pattern: pick.pattern, reason: reason(pick) };
  };

  const oc: DrawCard[] = [];
  for (let i = 0; i < ocTarget; i++) {
    const card = take(ocPool, (c) => {
      const u = usage[c.id];
      if (!u) return `OC-жребий: карта не использована ни разу — «новенькая», коридор ${c.corridor}, класс ${c.exposureClass}`;
      return `OC-жребий: коридор ${c.corridor}, класс ${c.exposureClass}; «давненько не была» — последний раз партия №${u.lastBatch}`;
    });
    if (!card) { shortfall.n += 1; continue; }
    oc.push(card);
  }

  const main: DrawCard[] = [];
  const baskets: OracleCard[][] = [poolA, poolB, poolMid];
  for (let i = 0; i < mainTarget; i++) {
    const order = [baskets[i % 3], baskets[(i + 1) % 3], baskets[(i + 2) % 3]]; // детерминированный обход
    let card: DrawCard | null = null;
    for (const basket of order) {
      card = take(basket, (c) => {
        const side = c.corridor === 'A+B' ? 'A+B' : c.corridor === 'B' ? 'B (геометрия)' : c.corridor === 'A' ? 'A (объект у груди)' : 'низкий тир';
        return `мейн ${String(i + 1).padStart(2, '0')}: корзина ${side}; окно чисто${usage[c.id] ? `, последний выход — партия №${usage[c.id].lastBatch}` : ', ни разу'}`;
      });
      if (card) break;
    }
    if (!card) { shortfall.n += 1; continue; }
    main.push(card);
  }

  const exp: DrawCard[] = [];
  for (let i = 0; i < expTarget; i++) {
    const card = take(expPool, (c) => `EXP-жребий: новенькая карта (ни разу не создавали), номер ${cardNum(c.id)} — волна свежих`);
    if (!card) { shortfall.n += 1; continue; }
    exp.push(card);
  }

  return {
    batchNo,
    seed,
    oc,
    main,
    exp,
    windowExcluded: cards.filter((c) => inWindow(c.id)).length,
    windowPosesExcluded: cards.filter((c) => poseBanned(c)).length,
    shortfall: shortfall.n,
    determinism: `seed = ${batchNo} × 2654435761 mod 2³² = ${seed}; тот же вход → тот же расклад (зеркала: прилавок/печь/сервис, векторы tests/fixtures/oracle_vectors.json)`,
  };
}

/** ранг OC-кандидатки: COVER-класс первее, свежее первее, реже используемые первее */
function ocRank(c: OracleCard, usage: Record<string, CardUsage>): number {
  const u = usage[c.id];
  const cover = c.exposureClass === 'COVER' ? 1000 : 0;
  const fresh = u ? 0 : 500;
  const rarity = u ? Math.max(0, 100 - u.usedCount * 10) : 0;
  const age = u?.lastBatch ? Math.max(0, 60 - u.lastBatch) : 0; // старее выход — выше ранг
  return cover + fresh + rarity + age;
}
