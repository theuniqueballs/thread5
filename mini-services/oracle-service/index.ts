/**
 * ECCHI-ORACLE service — inference endpoint for thread5.
 * Port: 3031 (fixed).
 *
 * Layers:
 *   1. Deterministic rule engine (this file) — tier scoring, corridor detection,
 *      claimPhysics audit, safety-floor linting. No GPU, no network.
 *   2. LLM oracle (z-ai-web-dev-sdk) — natural-language brain over the distilled
 *      system prompt (../ecchi-oracle/distill/system_prompt.txt).
 *   3. Vision (z-ai SDK createVision) — image -> structured technical description
 *      -> rule engine + optional LLM verdict.
 */
import ZAI from "z-ai-web-dev-sdk";
import { readFileSync, existsSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { join, dirname } from "node:path";

const HERE = dirname(fileURLToPath(import.meta.url));
// знание (ecchi-oracle/) ищем рядом с сервисом; фолбэк — старая раскладка пака
const PKG = [join(HERE, "..", "ecchi-oracle"), join(HERE, "..", "..", "ecchi-oracle")].find((p) =>
  existsSync(join(p, "taxonomy", "rating-marks.json")),
) || join(HERE, "..", "ecchi-oracle");
const PORT = 3031;

// ---------------------------------------------------------------- knowledge

const taxonomy = {
  ratingMarks: JSON.parse(readFileSync(join(PKG, "taxonomy", "rating-marks.json"), "utf-8")),
  corridors: JSON.parse(readFileSync(join(PKG, "taxonomy", "corridors.json"), "utf-8")),
  safety: JSON.parse(readFileSync(join(PKG, "taxonomy", "safety-floors.json"), "utf-8")),
  rendererFacts: JSON.parse(readFileSync(join(PKG, "taxonomy", "renderer-facts.json"), "utf-8")),
};
const distillPath = join(PKG, "distill", "system_prompt.txt");
const distillPrompt = existsSync(distillPath)
  ? readFileSync(distillPath, "utf-8")
  : "Ты — ECCHI-ORACLE, эксперт домена «эччи-приёмы манги и аниме» конвейера thread5.";

// Y-card registry (camera.json из чекаута thread5 при наличии; taxonomy fallback)
// в нашей раскладке (thread5/mini-services/oracle-service) ../.. = корень thread5/
const THREAD5_CANDIDATES = [join(HERE, "..", "..", "specs", "camera.json"), "/home/z/my-project/thread5/specs/camera.json"];
const GATES_CANDIDATES = [join(HERE, "..", "..", "specs", "gates.json"), "/home/z/my-project/thread5/specs/gates.json"];
let cameraCards: Record<string, { pattern?: string; corridor?: string; trust?: string; components?: Record<string, unknown> }> = {};
let cameraVersion: string | null = null;
for (const c of THREAD5_CANDIDATES) {
  if (existsSync(c)) {
    try {
      const cam = JSON.parse(readFileSync(c, "utf-8"));
      cameraVersion = cam.version || null;
      const raw = cam.y_cards?.cards || cam.y_cards || {};
      if (Array.isArray(raw)) for (const card of raw) if (card?.id) cameraCards[String(card.id)] = card;
      else if (raw && typeof raw === "object") cameraCards = raw;
      break;
    } catch { /* fallback below */ }
  }
}
if (!Object.keys(cameraCards).length) {
  const fallback = taxonomy.corridors.y_cards as Record<string, unknown>;
  for (const [k, v] of Object.entries(fallback)) if (k.startsWith("Y")) cameraCards[k] = v as typeof cameraCards[string];
}

// конфиг yStamp-гейта (gates.json) — сверяем той же конфигурацией, что tools/gates.py;
// фолбэк — константы 1.15.0 (В34/В35)
let yStampCfg: {
  bannedMarkers?: string[];
  minWeaveStems?: number;
  minExecStems?: number;
  rplus_banned_classes?: string[];
} = {};
for (const g of GATES_CANDIDATES) {
  if (existsSync(g)) {
    try {
      const gates = JSON.parse(readFileSync(g, "utf-8")) as { yStamp?: typeof yStampCfg };
      yStampCfg = gates.yStamp || {};
      break;
    } catch { /* фолбэк ниже */ }
  }
}
const BANNED_MARKERS: RegExp[] = (
  yStampCfg.bannedMarkers || ["Y-STAMP:", "«[^»]+»", "\\bCAM\\d{1,3}\\b", "\\bcorridor\\s+[AB+]\\b"]
).map((p) => new RegExp(p, "i"));

const SYS_SHORT =
  "Ты — ECCHI-ORACLE, компактная экспертная модель домена «эччи-приёмы манги и аниме» " +
  "конвейера thread5 (RAW+ батчи, Tsubaki.2 Pro → Yodayo). Технический тон, filter-safe wording. Рабочий потолок — R+.";

// ---------------------------------------------------------------- helpers

const has = (text: string, phrases: string[]) => {
  const t = ` ${text.toLowerCase().replace(/[\n\r,;]+/g, " ")} `;
  return phrases.filter((p) => {
    const needle = p.toLowerCase().replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    return new RegExp(`(^|[^a-zа-яё])${needle}([^a-zа-яё]|$)`, "i").test(t);
  });
};
const hasAny = (text: string, phrases: string[]) => has(text, phrases).length > 0;
const approxTokens = (text: string) => Math.ceil(text.trim().split(/\s+/).length * 1.35);

// ---------------------------------------------------------------- signal dictionaries

const PG13 = ["sexy outfit", "bikini", "cleavage", "thighs", "off-shoulder", "off shoulder", "bare shoulders",
  "short shorts", "miniskirt", "micro skirt", "midriff", "crop top", "zettai ryouiki", "thighhighs",
  "thighhigh", "stockings", "bare back", "backless", "swimsuit", "one-piece", "pareo", "sarong",
  "thigh gap", "bare thighs", "slit", "high slit", "sporty top", "gym clothes"];

const R = ["lingerie", "panties", "panty shot", "pantyshot", "panties visible", "upskirt", "bra", "underwear",
  "underwear only", "erotic pose", "microbikini", "micro bikini", "sling bikini", "string bikini",
  "garter belt", "thong", "boyshorts", "side-tie panties", "bunny suit", "towel only", "apron only",
  "naked apron", "buruma", "bloomers", "sarashi", "fundoshi", "camisole", "nightgown", "negligee",
  "bikini bridge", "whale tail", "pajama shorts", "sleep shirt"];

const RPLUS_HARD = ["visible pantyline", "pantyline", "clothed nipples", "covered nipples", "taped nipples",
  "topless with tape", "handbra", "hand bra", "hands covering chest", "arms covering chest",
  "hands covering", "arm bra", "covering breasts with hands"];

const RPLUS_SOFT = ["cameltoe", "camel toe", "breast clinging", "extreme fanservice", "see-through",
  "see through", "wet clothes", "tight clothes", "almost naked", "breast pressing", "clinging",
  "sheer panel", "threadbare", "nothing underneath", "no bra", "without underlayer", "unlined",
  "braless", "worn without a bra"];

const X_MARKERS = ["nipples exposed", "nipples", "areola", "exposed breasts", "bare breasts", "nude",
  "topless bare", "naked breasts", "genitals", "exposed genitals", "vulva"];

const CORRIDOR_A = ["hands covering chest", "arms covering chest", "handbra", "hand bra", "taped nipples",
  "topless with tape", "towel mid-catch", "towel caught", "towel slipping", "towel only", "naked apron",
  "apron only", "shirt as the only", "worn as the only shirt", "held to her chest", "against her chest",
  "over her chest", "covering her chest", "at her chest", "breast line", "pressed flat against her own chest",
  "palm pressed flat", "palm pressed", "holding the dress front", "holding the dress", "book against",
  "cup against", "bundled cloth", "cloth hugged", "tail wrapped", "dress front pressed", "pressed flat holding"];

const CORRIDOR_B = ["from below", "low angle", "slight from below", "between knees", "between her knees",
  "door gap", "through the door", "straddle", "straddling", "settle", "kneel", "kneel-back", "mid-lift",
  "mid-catch", "mid-pull", "mid-turn", "mid-action", "waistband", "hem lifted", "hem pinned", "hem tucked",
  "hem riding", "lean back", "leaning back", "slipping strap", "strap slip", "slid off one shoulder",
  "sliding off one shoulder", "mid-run", "mid-step", "pov"];

const LAYER2 = ["close-up", "close up", "cowboy shot", "upper body", "portrait", "full body", "wide shot",
  "from above", "from the side", "dutch angle", "mirror", "reflection", "over shoulder", "pov",
  "viewed from", "insert", "framing"];
const LAYER3 = ["looking at viewer", "looking at the viewer", "blush", "smile", "smiling", "smirk", "grin",
  "parted lips", "half-closed eyes", "half-lidded", "looking back", "looking away", "looking down",
  "candid", "embarrassed", "surprised", "teasing", "gaze", "eyes closed", "sleepy", "yawn", "gasp"];
const LAYER4 = ["wet", "soaked", "steam", "foam", "waterline", "tide-line", "rain", "sweat", "glistening",
  "sheer", "see-through", "transparent", "splashing", "water at", "emerging from"];
const CHANNEL_TOKENS = RPLUS_HARD.concat(["towel mid-catch", "waistband mid-pull", "mid-lift", "low corridor",
  "shirt mid-lift", "hem process", "strap slip", "palm pressed flat", "pressed flat holding", "holding the dress front"]);

const DEAD_FABRICS = ["jeans", "denim", "leather", "velvet", "sweatpants", "breeches", "trousers", "slacks",
  "vinyl", "suede", "wool coat", "parka", "flannel", "suit"];

const FLOOR_LINT = [
  { name: "genital_lock", words: ["exposed genitals", "vulva", "pubic hair"], level: "FAIL",
    note: "Генитальный лок POS: слова никогда не пишутся в POS." },
  { name: "anti_loli", words: ["child", "children", "childish", "chibi", "young girl", "immature body",
    "oversized head", "loli", "shota"], level: "FAIL",
    note: "Anti-loli флор: возраст — формой тела; слова запрещены в POS." },
  { name: "milf_word", words: ["milf"], level: "FAIL", note: "Слово milf запрещено в POS (N30)." },
  { name: "muscle_law", words: ["muscular", "ripped", "six-pack", "defined abs", "bulging", "bodybuilder"],
    level: "FAIL", note: "Мускульный закон: тон soft/firm/toned-lite." },
  { name: "camera_token", words: ["camera"], level: "WARN",
    note: "Токен «camera» рисует камеру предметом — кадр пишется «viewed from …»." },
  { name: "device_words", words: ["candle", "lamp", "lantern", "torch", "chandelier", "campfire"],
    level: "WARN", note: "Приборы света спавнятся предметами; свет — поведением." },
  { name: "xxx_never", words: ["sex", "sexual act", "penis", "cum", "intercourse", "половой акт"],
    level: "FAIL", note: "XXX — никогда: не пишется ни в POS, ни куда-либо." },
];

// ---------------------------------------------------------------- engine: rate

function rateText(text: string) {
  const tokens = approxTokens(text);
  const pg = has(text, PG13);
  const r = has(text, R);
  const rpHard = has(text, RPLUS_HARD);
  const rpSoft = has(text, RPLUS_SOFT);

  // X Cut: bare "nipples"/"areola" NOT softened by clothed/covered/taped context
  const softened = /cloth(ed|ing)|covered|taped|through (her |the )?sweater/i.test(text);
  const bareNipple = X_MARKERS.filter((w) =>
    new RegExp(`(^|[^a-z])${w}([^a-z]|$)`, "i").test(` ${text.toLowerCase()} `) &&
    !(["nipples"].includes(w) && softened));
  const xRiskDrivers = [];
  if (hasAny(text, ["wet", "soaked"]) && hasAny(text, ["white", "light", "sheer", "see-through", "see through", "thin"]))
    xRiskDrivers.push("wet + светлая/тонкая ткань");
  if (hasAny(text, ["nipples through clothing"])) xRiskDrivers.push("цветной сосок через ткань (nipples through clothing)");

  const corridorA = has(text, CORRIDOR_A);
  const corridorB = has(text, CORRIDOR_B);
  const layer2 = has(text, LAYER2);
  const layer3 = has(text, LAYER3);
  const layer4 = has(text, LAYER4);
  const deadFabric = has(text, DEAD_FABRICS);

  const exposure: string[] = [];
  if (rpHard.length || corridorA.length) exposure.push("COVER");
  if (corridorB.length) exposure.push("PROCESS");
  if (r.length) exposure.push("LINGERIE");
  if (hasAny(text, ["tight", "clinging", "fitted", "taut"])) exposure.push("CLOTHED-TIGHT");
  if (hasAny(text, ["sheer", "see-through", "see through", "transparent", "wet"])) exposure.push("SHEER");

  const corridor: "A" | "B" | "A+B" | "NONE" =
    corridorA.length && corridorB.length ? "A+B" : corridorA.length ? "A" : corridorB.length ? "B" : "NONE";

  const layersEngaged = [!!(pg.length || r.length || rpHard.length), layer2.length > 0,
    layer3.length > 0, layer4.length > 0].filter(Boolean).length;

  let tier: string;
  if (bareNipple.length) tier = "X";
  else if (rpHard.length >= 1 || rpSoft.length >= 2 ||
           (r.length + rpSoft.length >= 3 && layersEngaged >= 2 && corridor !== "NONE"))
    tier = "R+";
  else if (r.length >= 2 || (r.length >= 1 && (layer3.length || layer2.length))) tier = "R";
  else if (pg.length >= 2 || (pg.length >= 1 && (layer3.length || layer2.length || layer4.length))) tier = "PG-13";
  else if (pg.length + r.length + rpSoft.length >= 1) tier = "PG-13";
  else tier = "SFW";

  const triage = tier === "X" ? "x" : tier === "R+" ? "borderline" : tier === "R" ? "borderline" : "sfw";

  const warnings: string[] = [];
  for (const f of FLOOR_LINT) {
    const hits = has(text, f.words);
    if (hits.length) warnings.push(`[${f.level}] ${f.name}: ${hits.join(", ")} — ${f.note}`);
  }
  if (tier === "R+" && corridor === "NONE")
    warnings.push("[FAIL] R+ без коридора: бейдж самосертифицирован — ни A (объект у груди), ни B (геометрия поза+камера). План R/PG-13.");
  if (deadFabric.length && (exposure.includes("SHEER") || exposure.includes("CLOTHED-TIGHT")))
    warnings.push(`[WARN] Мёртвая ткань (${deadFabric.join(", ")}) не несёт через-ткань заявку — сменить вещь или канал.`);
  if (xRiskDrivers.length && tier !== "X")
    warnings.push(`[WARN] X-драйверы: ${xRiskDrivers.join("; ")} — свет НЕ на зоне / сухая тёмная ткань (закон №28) или one-piece.`);
  if (hasAny(text, ["sheer", "see-through", "see through"]) && !hasAny(text, ["nothing underneath", "no bra", "without underlayer", "unlined", "worn without a bra", "braless"]))
    warnings.push("[WARN] Sheer без bare-under маркера: движок достроит подслой поверх NEG-лока (T4-05 P07). Добавь nothing underneath + bra/camisole в NEG.");

  return {
    verdict: tier,
    triage,
    corridor,
    exposure_classes: exposure,
    layers_engaged: layersEngaged,
    signals: { pg13: pg, r, rplus_hard: rpHard, rplus_soft: rpSoft, x_markers: bareNipple },
    layers: { "1_что_видно": pg.length + r.length + rpHard.length, "2_как_показано": layer2.length,
      "3_зачем_показано": layer3.length, "4_что_дорисует": layer4.length },
    x_risk_drivers: xRiskDrivers,
    approx_tokens: tokens,
    warnings,
    law: "1 сигнал = PG-13/R · 3+ R-сигнала через 2+ слоя = R+ · X = один жёсткий факт (не сумма намёков)",
  };
}

// ---------------------------------------------------------------- engine: Y-STAMP

const STAMP_RE = /Y-STAMP:\s*(Y\d+)\s*«([^»]+)»\s*×\s*(.+?)(?:\s*×\s*(.+?))?\s*·\s*corridor\s*(A\+B|A|B|—)/i;

function stemsOf(pattern: string): string[] {
  return pattern.toLowerCase().split(/[^a-zа-яё0-9]+/).filter((w) => w.length >= 4);
}

const normWs = (s: string) => s.replace(/\s+/g, " ").trim();

function parseStampLine(text: string) {
  const m = text.match(STAMP_RE);
  if (!m) return null;
  return { card_id: m[1].toUpperCase(), stamp_class: m[2].trim(), pose: m[3].trim(), camera: (m[4] || "").trim(), corridor: m[5].trim() };
}

function yStampChecks(input: {
  pos: string;
  stamp?: string;                    // паспорт-метка (чип/метаданные) — в POS не живёт, только сверка с картой
  card_id?: string;
  badge?: string;
  declaredCorridor?: string;
}) {
  // v1.15.0 yStamp (вердикт автора 2026-11-19 по T5-25, В34 «и прочие обозначения
  // - не нужны, нужно только то, что за ними имеется в виду...» + В35): клеймо =
  // вплетённый смысл — строка 3 POS = паттерн карты копипастом 1:1, БЕЗ строки-метки
  // «Y-STAMP: ...» / «класс» / CAM-кодов / corridor-токена. Паспорт — метаданные
  // (Y-card в шапке, чип прилавка). Зеркало check_ystamp в tools/gates.py v1.15.0.
  const pos = input.pos || "";
  const posLines = pos.split("\n").map((l) => l.trim()).filter(Boolean);
  const checks: { name: string; status: "PASS" | "WARN" | "FAIL"; detail: string }[] = [];

  // (1) В34: служебные обозначения в POS запрещены — ловим без карты (метка без Y-card тоже нарушение)
  for (const l of posLines) {
    let hit: string | null = null;
    for (const bre of BANNED_MARKERS) {
      const m = bre.exec(l);
      if (m) { hit = m[0]; break; }
    }
    if (hit) {
      checks.push({ name: "В34: обозначения в POS", status: "FAIL",
        detail: `Служебное обозначение «${hit}» в строке «${l.slice(0, 72)}» — обозначения не рисуются: паттерн доезжает вплетением 1:1, камера — камерным кластером OPENER, коридор — физикой claim-строки, класс — рейтингом слота; паспорт — метаданные (LAWS §17, gates 1.15.0).` });
      break;
    }
  }

  const parsedMeta = parseStampLine(input.stamp || "");
  const cardId = input.card_id ? input.card_id.toUpperCase() : parsedMeta?.card_id || null;

  if (!cardId) {
    if (!checks.length)
      checks.push({ name: "Y-карта", status: "PASS", detail: "Слот без Y-карты — вплетение не требуется; обозначений в POS нет (В34 чист)." });
    return { checks, weaved: false, card: null, card_id: null as string | null, weave: null };
  }
  const card = cameraCards[cardId] || null;
  if (!card) {
    checks.push({ name: "Паспорт карты", status: "FAIL", detail: `Карта ${cardId} не найдена в реестре (camera.json ${cameraVersion ?? "fallback"}) — чужой/битый паспорт.` });
    return { checks, weaved: false, card: null, card_id: cardId, weave: null };
  }

  const cardPattern = String(card.components?.pose || card.pattern || "");
  const cardCorridor = String(card.corridor || card.components?.corridor || "");
  const cardClass = cardClassOf(card);
  const badge = (input.badge || "").toUpperCase().replace("RPLUS", "R+");

  if (!cardPattern.trim()) {
    checks.push({ name: "Паттерн карты", status: "FAIL", detail: `Карта ${cardId} без паттерна (components.pose пуст) — вплетать нечего, слот не может быть собран от этой карты.` });
    return { checks, weaved: false, card, card_id: cardId, weave: null };
  }

  // (2) вплетение: ПЕРВИЧНЫЙ детектор — копипаст-юнит 1:1 подстрокой (LAWS §17.2);
  // стемы — только диагностика пересказа (урок P28/Y320: короткие паттерны стем-порог ронял)
  const poseN = normWs(cardPattern).toLowerCase();
  let weaveIdx = -1;
  if (poseN) {
    for (let i = 0; i < posLines.length; i++) {
      if (normWs(posLines[i]).toLowerCase().includes(poseN)) { weaveIdx = i; break; }
    }
  }
  const patternStems = new Set(stemsOf(cardPattern));
  let bestHits = 0;
  for (const l of posLines) {
    const ws = new Set(stemsOf(l));
    let hits = 0;
    for (const s of patternStems) if (ws.has(s)) hits++;
    if (hits > bestHits) bestHits = hits;
  }
  const minWeave = yStampCfg.minWeaveStems ?? 4;
  if (weaveIdx >= 0) {
    checks.push({ name: "Вплетение 1:1", status: "PASS", detail: `Паттерн ${cardId} найден в POS копипаст-юнитом (строка ${weaveIdx + 1}).` });
    // (5) исполнение вне строки вплетения
    const body = posLines.filter((_, i) => i !== weaveIdx).join(" ");
    const bodyStems = new Set(stemsOf(body));
    const minExec = yStampCfg.minExecStems ?? 2;
    const executed = [...patternStems].filter((s) => bodyStems.has(s));
    if (executed.length < minExec)
      checks.push({ name: "Исполнение телом POS", status: "FAIL",
        detail: `Стемов паттерна вне строки вплетения: ${executed.length} (нужно ≥${minExec}) — паттерн живёт дважды: камерный кластер OPENER + строка 3 (LAWS §17.3).` });
    else
      checks.push({ name: "Исполнение телом POS", status: "PASS", detail: `Исполнено стемами: ${executed.slice(0, 4).join(", ")}.` });
  } else if (bestHits < minWeave) {
    checks.push({ name: "Вплетение 1:1", status: "FAIL",
      detail: `Паттерн карты ${cardId} не вплетён (стемов в лучшей строке: ${bestHits}, нужно ≥${minWeave}; копипаста 1:1 нет) — «не оставляй промпт на произвол судьбы» (В34); строка 3 = паттерн копипастом: «${normWs(cardPattern).slice(0, 70)}…»` });
  } else {
    checks.push({ name: "Вплетение 1:1", status: "FAIL",
      detail: `Вплетение ${cardId} пересказано — копипаст-юнит 1:1 из camera.json не найден подстрокой (LAWS §17.2); если вшита чужая карта — сверить поле Y-card.` });
  }

  // сверка паспорта-метки (если приложен как метаданные) с картой
  if (parsedMeta && cardClass && parsedMeta.stamp_class && parsedMeta.stamp_class !== cardClass)
    checks.push({ name: "Класс паспорта = карте", status: "FAIL", detail: `Метка «${parsedMeta.stamp_class}», карта ${cardId} = ${cardClass}. Класс печатается из карты, не выбирается.` });
  if (parsedMeta && cardCorridor && parsedMeta.corridor && parsedMeta.corridor !== cardCorridor)
    checks.push({ name: "Коридор паспорта = карте", status: "FAIL", detail: `Метка corridor ${parsedMeta.corridor}, карта ${cardId} = ${cardCorridor}.` });

  // (4) В33: R+/X от обёртки без класса
  const bannedClasses = yStampCfg.rplus_banned_classes || ["—"];
  if ((badge === "R+" || badge === "X") && cardClass && bannedClasses.includes(cardClass))
    checks.push({ name: "В33: класс «—» не выносит R+/X", status: "FAIL",
      detail: `Бейдж ${badge} при классе «${cardClass}» (карта ${cardId}): паспорт не самосертифицирует рейтинг (В33) — добрать факт печью или честно понизить тир.` });

  // (7) коридор карты vs поле слота — WARN
  const declaredCorridor = (input.declaredCorridor || "").toUpperCase();
  if (cardCorridor && declaredCorridor && declaredCorridor !== "NONE" && declaredCorridor !== cardCorridor.toUpperCase())
    checks.push({ name: "Коридор карты = полю Corridor:", status: "WARN", detail: `Поле слота ${declaredCorridor}, карта ${cardId} = ${cardCorridor} — сверить (В31: коридор обязан сходиться и физикой POS).` });

  return { checks, weaved: weaveIdx >= 0, card, card_id: cardId, weave: normWs(cardPattern) };
}

function cardClassOf(card: { pattern?: string; corridor?: string; trust?: string; components?: Record<string, unknown> }): string {
  const c = (card.components?.exposure as { class?: string } | undefined)?.class || (card as { class?: string }).class || "";
  if (c) return String(c);
  // обёртки акта 1: класс не задан — «—» по В27 ПУСТО (trust/corridor)
  const empty = card.corridor === "—" || /В27 ПУСТО/i.test(String(card.trust || ""));
  return empty ? "—" : "";
}

function printStamp(cardId: string) {
  const id = cardId.toUpperCase().replace(/^Y(?!\d)/, "Y");
  const card = cameraCards[id];
  if (!card) return null;
  const pattern = String(card.components?.pose || card.pattern || "");
  const corridor = String(card.corridor || card.components?.corridor || "—");
  const cls = cardClassOf(card) || "—";
  const camera = String(card.components?.camera || (card as { camera?: string }).camera || "");
  const meta = camera
    ? `Y-STAMP: ${id} «${cls}» × ${pattern} × ${camera} · corridor ${corridor}`
    : `Y-STAMP: ${id} «${cls}» × ${pattern} · corridor ${corridor}`;
  return {
    card_id: id,
    era: "gates 1.15.0 — В34/В35: клеймо = вплетённый смысл, метки в POS запрещены",
    // ЕДИНСТВЕННЫЙ текст клейма, легальный в POS (В34): паттерн карты копипастом 1:1
    weave: pattern,
    weave_rules: {
      position: "строка 3 POS: после claim-строки, до деталей (LAWS §17.1)",
      doctrine: "паттерн карты копипастом 1:1 с физикой ЦЕЛИКОМ (В35), без сжатия и пересказа",
      banned_in_pos: ["строка-метка Y-STAMP:", "«класс» в кавычках", "CAM-коды", "corridor-токен"],
      camera_note: "камера — отдельным камерным кластером OPENER (не меткой)",
      corridor_note: "коридор — физикой claim-строки (В31)",
    },
    // метаданные чипа/сверки — в POS НЕ печатается (В34)
    stamp_metadata: meta,
    class: cls, corridor, camera, pattern,
    trust: card.trust || null,
    built_from: (card as { built_from?: string }).built_from || null,
    В33_note: cls === "—" ? "Класс «—» (В27 ПУСТО): R+/X под этой картой = FAIL (В33). Для низких тиров — ок." : null,
    camera_version: cameraVersion,
  };
}

// ---------------------------------------------------------------- engine: triage v2 (АКТ 9)

const SLOT_PATTERNS: { type: string; re: RegExp }[] = [
  { type: "special", re: /\bSO-?\d\d\b/i },
  { type: "OC", re: /\bP0[1-3]\b/ },
  { type: "EXP", re: /\bP(2[5-9]|3[0-3])\b/ },
  { type: "main", re: /\bP(0[4-9]|1\d|2[0-4])\b/ },
];

function detectSlotType(fileTag?: string, fileName?: string): { type: string; from: string } {
  const hay = `${fileTag || ""} ${fileName || ""}`;
  for (const p of SLOT_PATTERNS) if (p.re.test(hay)) return { type: p.type, from: fileTag ? "file_tag" : "file_name" };
  return { type: "unknown", from: "no match — нужен тег файла (например «T5-18 P07»)" };
}

function factRating(engine: ReturnType<typeof rateText>, description: string) {
  // Шкала автора (2026-11-17): R+ — еле прикрытая; R — suggestive, купальники, бельё; PG-13 — всё остальное; Partial — частичные/полупрозрачные
  const tier = engine.verdict;
  const partial = hasAny(description, ["полупрозрач", "частично откры", "see through", "see-through", "sheer", "просвечив"]);
  if (tier === "X") return { fact: "X", rule: "X Cut: один жёсткий факт" };
  if (tier === "R+" && engine.corridor !== "NONE") return { fact: "R+", rule: "еле прикрытая + коридор подтверждён в кадре" };
  if (tier === "R+" && engine.corridor === "NONE") return { fact: partial ? "Partial" : "R", rule: "сигналы есть, коридора в кадре нет — еле прикрытой не вижу (В33)" };
  if (tier === "R") return { fact: partial ? "Partial" : "R", rule: "suggestive / купальники / бельё" };
  if (tier === "PG-13") return { fact: "PG-13", rule: "всё остальное" };
  return { fact: "SFW", rule: "ноль эччи-сигналов" };
}

function triageV2(input: {
  engine: ReturnType<typeof rateText>;
  description: string;
  fileTag?: string;
  fileName?: string;
  label?: string;
}) {
  const { fact, rule } = factRating(input.engine, input.description);
  const slot = detectSlotType(input.fileTag, input.fileName);
  const label = input.label ? input.label.toUpperCase().replace("RPLUS", "R+").replace("PG13", "PG-13") : null;
  const drift = label && fact !== "X" && label !== fact ? (label === "R+" && fact === "R+" ? null : `${label} ≠ fact ${fact}`) : null;
  return {
    x_verdict: input.engine.triage, // x | borderline | sfw
    slot_type: slot.type,
    slot_type_from: slot.from,
    fact_rating: fact,
    fact_rule: rule,
    label,
    drift,
    drift_note: drift ? (label === "R+" ? "В33: завышение — самосертификация (болезнь T5-23)." : label && (fact === "R+" || fact === "Partial") ? "В33: занижение — потеря HEAT-квоты, тоже пиздёж." : "В33: label ≠ fact — пометить, не молчать.") : null,
    patterns: [] as string[],
    law: "триаж выносит fact (что в кадре), label — только сверка; drift в обе стороны (В33)",
  };
}

function auditSlot(input: { badge?: string; corridor?: string; pos?: string; stamp?: string; card_id?: string }) {
  const pos = input.pos || "";
  const badge = (input.badge || "").toUpperCase().replace("RPLUS", "R+").replace("PG13", "PG-13");
  const declaredCorridor = (input.corridor || "NONE").toUpperCase();
  const scoring = rateText(pos);
  const checks: { name: string; status: "PASS" | "WARN" | "FAIL"; detail: string }[] = [];

  const exposure = scoring.exposure_classes;
  checks.push({
    name: "Класс раскрытия",
    status: exposure.length ? "PASS" : "FAIL",
    detail: exposure.length ? exposure.join(" · ") : "Ни COVER/PROCESS/LINGERIE/CLOTHED-TIGHT/SHEER в POS — раскрытия нет.",
  });

  const aOk = scoring.corridor === "A" || scoring.corridor === "A+B";
  const bOk = scoring.corridor === "B" || scoring.corridor === "A+B";
  if (declaredCorridor.includes("A"))
    checks.push({ name: "Коридор A (объект у груди)", status: aOk ? "PASS" : "FAIL",
      detail: aOk ? "Объект-прикрытие в тегах найден." : "Заявлен A, но объект-прикрытия (руки/тейп/ткань у груди) в POS нет — самосертификация." });
  if (declaredCorridor.includes("B"))
    checks.push({ name: "Коридор B (геометрия поза+камера)", status: bOk ? "PASS" : "FAIL",
      detail: bOk ? "Геометрия (ракурс/посадка/mid-action) в тегах найдена." : "Заявлена B, но тегов низкого ракурса/посадки/mid-action нет — самосертификация." });

  const channels = has(pos, CHANNEL_TOKENS);
  checks.push({
    name: "Канал-токен",
    status: channels.length === 1 ? "PASS" : channels.length === 0 ? "FAIL" : "WARN",
    detail: channels.length === 1 ? `Один канал: ${channels[0]}`
      : channels.length === 0 ? "Канала нет: рейтинг живёт только в шапке слота (fake high tier)."
      : `Стек каналов (${channels.length}): ${channels.join(", ")} — оставить один.`,
  });

  // claim salience: rough position of first channel among tokens
  let claimPos = -1;
  const lower = pos.toLowerCase();
  for (const c of CHANNEL_TOKENS) {
    const idx = lower.indexOf(c);
    if (idx >= 0 && (claimPos < 0 || idx < claimPos)) claimPos = idx;
  }
  const claimToken = claimPos >= 0 ? approxTokens(pos.slice(0, claimPos)) : null;
  if (claimToken !== null)
    checks.push({ name: "Салиенс заявки", status: claimToken <= 60 ? "PASS" : "WARN",
      detail: claimToken <= 60 ? `Заявка ~ на токене ${claimToken} (≤60 — ок).` : `Заявка на ~${claimToken}-м токене (>60) — переставить раньше (после камеры/тела).` });
  else
    checks.push({ name: "Салиенс заявки", status: "FAIL", detail: "Заявки в POS нет." });

  const lightOnZone = hasAny(pos, ["light on", "on her chest", "on her hands", "across her ribs", "rim", "backlight",
    "side light", "glow on", "light pooling", "on the zone"]);
  if (exposure.length)
    checks.push({ name: "Свет на зоне (CONTRAST)", status: lightOnZone ? "PASS" : "WARN",
      detail: lightOnZone ? "Свет прописан на зоне заявки." : "Свет НА зоне не назван — грань потеряет читаемость." });

  const fail = checks.filter((c) => c.status === "FAIL").length;
  const warn = checks.filter((c) => c.status === "WARN").length;
  const selfCertified = badge.includes("R+") && scoring.corridor === "NONE";

  // Y-STAMP checks (АКТ 2) — добавляются к основному аудиту
  const stampResult = yStampChecks({ pos, stamp: input.stamp, card_id: input.card_id, badge, declaredCorridor });
  if (stampResult.checks.length) checks.push(...stampResult.checks);
  const stampFail = stampResult.checks.filter((c) => c.status === "FAIL").length;
  const stampWarn = stampResult.checks.filter((c) => c.status === "WARN").length;

  const verdict = fail + stampFail === 0 && !selfCertified ? (warn + stampWarn ? "WARN" : "PASS") : "FAIL";
  return {
    verdict,
    badge,
    declared_corridor: declaredCorridor,
    detected_corridor: scoring.corridor,
    self_certified: selfCertified,
    В33_honesty: selfCertified
      ? "В33: бейдж R+ без коридора — пиздёж. Либо добрать факт (карта с физикой + коридор), либо честно понизить и написать «не получилось»."
      : null,
    stamp: stampResult.card_id
      ? { card_id: stampResult.card_id, weaved: stampResult.weaved, registry_version: cameraVersion, era: "1.15.0 В34/В35" }
      : null,
    checks,
    warnings: scoring.warnings,
    fixes: buildFixes(checks, selfCertified, scoring),
    one_minute_test: "Прикрой окружение рукой: верх промпта всё ещё заряжен телом/заявкой? Если заряжен темой/оружием/декором — тема съела VOLT.",
  };
}

function buildFixes(checks: { name: string; status: string; detail: string }[], selfCert: boolean, scoring: ReturnType<typeof rateText>): string[] {
  const fixes: string[] = [];
  if (selfCert) fixes.push("Понизить бейдж до честного R/PG-13 или перестроить слот по Y-карте (объект-прикрытие для A / низкий ракурс+процесс для B).");
  for (const c of checks) {
    if (c.status === "FAIL" && c.name === "Класс раскрытия") fixes.push("Добавить раскрытие: вещь с состоянием (thin light thing / wet / clinging), процесс (mid-lift, mid-catch) или объект-прикрытие.");
    if (c.status === "FAIL" && c.name === "Коридор A (объект у груди)") fixes.push("Коридор A: объект у груди — руки/тейпы/полотенце mid-catch/книга/чашка с контакт-геометрией.");
    if (c.status === "FAIL" && c.name === "Коридор B (геометрия поза+камера)") fixes.push("Коридор B: slight from below / посадка (straddle, kneel-back) / процесс с одеждой (waistband mid-pull, hem pinned).");
    if (c.status === "FAIL" && c.name === "Канал-токен") fixes.push("Вставить один ранний канал-токен: tape / hands covering chest / mid-lift / low corridor / towel mid-catch.");
  }
  if (scoring.warnings.some((w) => w.includes("sheer"))) fixes.push("bare-under маркер позитивом (nothing underneath) + подслой в NEG (bra, camisole, bandeau, undershirt).");
  if (scoring.warnings.some((w) => w.includes("Мёртвая ткань"))) fixes.push("Сменить вещь на живую ткань (тонкий трикотаж/хлопок/шёлк) или перевести заявку в процесс/объект-канал.");
  if (!fixes.length) fixes.push("Слот честный: держать NEG-зеркало (nipples, exposed breasts, catalog standing) и свет на зоне.");
  return fixes;
}

// ---------------------------------------------------------------- engine: volt skeleton

function voltSkeleton(scene: string, ycard: string, target: string) {
  const card = cameraCards[ycard.toUpperCase()] as { pattern?: string; corridor?: string; trust?: string; components?: { pose?: string } } | undefined;
  const cardPattern = card ? String(card.components?.pose || card.pattern || "") : "";
  const tier = target && /r\+/i.test(target) ? "R+" : "R";
  const lines = [
    "anime style, original character, 1girl, solo, absurdres, intricate details,",
    card && cardPattern ? `/* камера по ${ycard.toUpperCase()} */ cowboy shot / upper body — выбери D+A по карте: ${cardPattern}` : "cowboy shot, slight from below,",
    "young woman, [3-5 тегов формы тела],",
    card && cardPattern ? `/* ЗАЯВКА (по ${ycard.toUpperCase()}, коридор ${card.corridor}) */ ${cardPattern.split(" + ").slice(0, 2).join(" + ")}, nothing underneath,` : "/* ЗАЯВКА: одна строка, на которую можно указать пальцем */,",
    "/* действие: present continuous, mid-action */,",
    `/* сцена: ${scene || "…"} — ПОСЛЕ заявки, один-три якоря */,`,
    "/* свет НА зоне заявки (жёсткий боковой / контровой), приборов нет */,",
    "stylized 2D anime face, anime eyes ([цвет, состояние]), small nose, small mouth,",
    "masterpiece, best quality, anime artstyle",
  ];
  return {
    tier,
    ycard: ycard.toUpperCase(),
    corridor: card?.corridor || "—",
    trust: card?.trust || "—",
    pos_skeleton: lines.join("\n"),
    neg: [
      "young girl, immature body, oversized head, loli, shota,",
      "signature, watermark, 1boy, candle, lamp, bad hands, extra fingers,",
      tier === "R+" ? "nipples, exposed breasts, bra, catalog standing, washed-out, faded colors, low contrast" : "washed-out, faded colors, low contrast",
    ].join("\n"),
    header: `VOLT · ${tier} · Corridor: ${card?.corridor || "—"} · Combo: ${ycard.toUpperCase() || "—"} · Channel: (один)`,
    checklist: ["Заявка ≤ токена 60?", "Камера в первых 10-20 токенах?", "Тема — после заявки?", "Один канал?", "One-minute test?"],
    reminder: "POS ≤130 слов цель, 150 hard; заявка сразу после канона/тела; мир — одной строкой.",
  };
}

// ---------------------------------------------------------------- dataset index

function datasetIndex() {
  const statsPath = join(PKG, "dataset", "stats.json");
  const stats = existsSync(statsPath) ? JSON.parse(readFileSync(statsPath, "utf-8")) : null;
  const files = ["train.jsonl", "val.jsonl"];
  let total = 0;
  const samples: Record<string, unknown[]> = {};
  for (const f of files) {
    const p = join(PKG, "dataset", f);
    if (!existsSync(p)) continue;
    const lines = readFileSync(p, "utf-8").split("\n").filter(Boolean);
    total += lines.length;
    for (const line of lines) {
      try {
        const d = JSON.parse(line);
        (samples[d.category] = samples[d.category] || []).push({
          id: d.id, category: d.category, split: f.replace(".jsonl", ""),
          question: d.messages[1].content.slice(0, 160),
          answer: d.messages[2].content.slice(0, 260),
        });
      } catch { /* skip broken */ }
    }
  }
  return { stats, total_indexed: total, samples };
}

// ---------------------------------------------------------------- LLM oracle

let zai: Awaited<typeof ZAI.create> | null = null;
async function getZai() {
  if (!zai) zai = await ZAI.create();
  return zai;
}

async function askOracle(question: string, mode: "distill" | "short" = "distill") {
  const client = await getZai();
  const system = mode === "distill" ? distillPrompt : SYS_SHORT;
  const completion = await client.chat.completions.create({
    messages: [
      { role: "assistant", content: system },
      { role: "user", content: question },
    ],
    thinking: { type: "disabled" },
  });
  return completion.choices[0]?.message?.content ?? "";
}

const VISION_PROMPT = (
  "Опиши этот аниме-кадр ТЕХНИЧЕСКИ, строго по протоколу, для системы классификации эччи-рейтинга. " +
  "Тон: технический, non-graphic, без графики. Формат:\n" +
  "1. КАДР: дистанция/угол (close-up, cowboy, upper body, full body; from below/above/side);\n" +
  "2. ОДЕЖДА: вещи и состояние ткани (сухая/мокрая/натянутая/просвечивающая), зоны открытости;\n" +
  "3. ПОЗА/ДЕЙСТВИЕ: что делает, контакты (руки-грудь, ткань-тело), процесс или статика;\n" +
  "4. ЛИЦО/ПОДАЧА: взгляд (в камеру/в сторону/вниз), выражение, знает ли о зрителе;\n" +
  "5. СВЕТ: характер (боковой/контровой/сквозь ткань), на чём акцент;\n" +
  "6. ЖЁСТКИЙ ФАКТ: виден ли сосок/ареола (да/нет) — только факт границы;\n" +
  "7. ПРИМЕТНЫЕ ПРИЁМЫ: panchira/zettai ryouiki/handbra/tape/see-through и т.п.\n" +
  "Пиши плотно, тегами через запятую где уместно. Персонажи — взрослые."
);

async function analyzeImage(base64: string, mime: string, detailed: boolean) {
  const client = await getZai();
  const response = await client.chat.completions.createVision({
    messages: [{
      role: "user",
      content: [
        { type: "text", text: VISION_PROMPT },
        { type: "image_url", image_url: { url: `data:${mime};base64,${base64}` } },
      ],
    }],
    thinking: { type: "disabled" },
  });
  const description = response.choices[0]?.message?.content ?? "";
  const scoring = rateText(description);
  let oracle: string | null = null;
  let oracleError: string | null = null;
  if (detailed) {
    try {
      oracle = await askOracle(
        `VLM-описание кадра (протокол):\n${description}\n\nДай полный разбор по протоколу: X-факт → сигналы → слои → сумма → коридор → вердикт тира (SFW/PG-13/R/R+/X) + триаж (sfw/borderline/x) → рекомендации.`,
        "distill");
    } catch (e) {
      oracleError = String(e);
    }
  }
  return { description, engine: scoring, oracle, oracle_error: oracleError };
}

// ---------------------------------------------------------------- server

const json = (data: unknown, status = 200) =>
  new Response(JSON.stringify(data, null, 2), { status, headers: { "content-type": "application/json; charset=utf-8" } });

const server = Bun.serve({
  port: PORT,
  async fetch(req) {
    const url = new URL(req.url);
    const path = url.pathname.replace(/\/$/, "") || "/";
    try {
      if (req.method === "GET" && path === "/health")
        return json({ ok: true, service: "ecchi-oracle", port: PORT, layers: ["rule-engine", "llm", "vision"], era: "Y-STAMP v1.15.0 (В34/В35: вплетение 1:1, метки в POS запрещены)", camera_registry: cameraVersion || "taxonomy-fallback", cards_indexed: Object.keys(cameraCards).length });

      if (req.method === "GET" && path === "/taxonomy") {
        const marks = taxonomy.ratingMarks.marks;
        return json({
          scale: Object.keys(marks).map((k) => ({ mark: k, order: marks[k].order, name: marks[k].name_ru, signals: marks[k].signals?.slice(0, 8) })),
          corridors: { A: taxonomy.corridors.corridors.A.idea, B: taxonomy.corridors.corridors.B.idea, "A+B": taxonomy.corridors.corridors["A+B"].idea },
          y_cards: taxonomy.corridors.y_cards,
          y_stamp: {
            law: "клеймо = вплетённый смысл (В34): строка 3 POS = паттерн карты копипастом 1:1, БЕЗ метки/класса/CAM-кодов/corridor-токена (gates 1.15.0); паспорт — метаданные (Y-card в шапке, чип прилавка)",
            camera_registry: cameraVersion || "taxonomy-fallback",
            cards_indexed: Object.keys(cameraCards).length,
          },
          combo_doctrine: taxonomy.corridors.combo_doctrine.law,
          В33: taxonomy.ratingMarks.honesty_law_В33.name,
          triage_v2: taxonomy.ratingMarks.triage_v2.law,
          carrier_classes: taxonomy.rendererFacts.carrier_classes,
          safety: { xxx: taxonomy.safety.floors.xxx_never.rule, anti_loli: taxonomy.safety.floors.anti_loli.rule, x_cut: taxonomy.safety.floors.x_default_out.rule },
        });
      }

      if (req.method === "GET" && path === "/dataset")
        return json(datasetIndex());

      if (req.method === "POST" && path === "/rate") {
        const body = await req.json().catch(() => ({}));
        const text = String(body.text || "");
        if (!text.trim()) return json({ error: "text required" }, 400);
        return json(rateText(text));
      }

      if (req.method === "POST" && path === "/audit") {
        const body = await req.json().catch(() => ({}));
        if (!String(body.pos || "").trim()) return json({ error: "pos required" }, 400);
        return json(auditSlot(body));
      }

      if (path === "/ystamp" && (req.method === "GET" || req.method === "POST")) {
        const cardId = req.method === "GET" ? String(url.searchParams.get("card") || "") : String(((await req.json().catch(() => ({}))) as { card?: string }).card || "");
        if (!cardId.trim()) return json({ error: "card required (например ?card=Y29)", registry_version: cameraVersion, cards_indexed: Object.keys(cameraCards).length }, 400);
        const stamp = printStamp(cardId);
        if (!stamp) return json({ error: `карта ${cardId} не найдена в реестре camera.json`, registry_version: cameraVersion, cards_indexed: Object.keys(cameraCards).length }, 404);
        return json(stamp);
      }

      if (req.method === "POST" && path === "/triage") {
        // триаж v2 по текстовому описанию кадра (без vision) — для tools/
        const body = await req.json().catch(() => ({}));
        const text = String(body.description || body.text || "");
        if (!text.trim()) return json({ error: "description required" }, 400);
        const engine = rateText(text);
        return json({ description_engine: engine, triage_v2: triageV2({ engine, description: text, fileTag: body.file_tag, fileName: body.file_name, label: body.label }) });
      }

      if (req.method === "POST" && path === "/volt") {
        const body = await req.json().catch(() => ({}));
        return json(voltSkeleton(String(body.scene || ""), String(body.ycard || ""), String(body.target || "R+")));
      }

      if (req.method === "POST" && path === "/ask") {
        const body = await req.json().catch(() => ({}));
        const question = String(body.question || "");
        if (!question.trim()) return json({ error: "question required" }, 400);
        const mode = body.mode === "short" ? "short" : "distill";
        const answer = await askOracle(question, mode);
        return json({ question, answer, mode, system: mode === "distill" ? "distill/system_prompt.txt" : "short persona" });
      }

      if (req.method === "POST" && path === "/vision") {
        const body = await req.json().catch(() => ({}));
        const b64 = String(body.image_base64 || "");
        if (!b64) return json({ error: "image_base64 required" }, 400);
        const mime = String(body.mime || "image/jpeg");
        const detailed = body.detailed !== false;
        const result = await analyzeImage(b64, mime, detailed);
        // триаж v2 поверх описания (акт 9): X-фильтр → слот-тип → fact → drift
        const triage = triageV2({ engine: result.engine, description: result.description, fileTag: body.file_tag, fileName: body.file_name, label: body.label });
        return json({ ...result, triage_v2: triage });
      }

      return json({ error: "not found", routes: ["GET /health", "GET /taxonomy", "GET /dataset", "POST /rate", "POST /audit", "POST /volt", "POST /ask", "POST /vision", "POST /triage", "GET|POST /ystamp?card=Y29"] }, 404);
    } catch (e) {
      return json({ error: String(e) }, 500);
    }
  },
});

console.log(`[ecchi-oracle] listening on :${server.port}`);
console.log(`[ecchi-oracle] knowledge package: ${PKG}`);
