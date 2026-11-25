// Счётчик бюджетов публикуемых полей BOT-DOC (tok = cl100k_base, как на карточке Yodayo).
// Использование: bun bot-forge/tools/tokens.mjs <bot-doc.md>
// Проверяет: токены/символы полей, кириллицу в EN-полях, em dash, формат "речь" *действие*.

import { readFileSync } from "fs";
import { encodingForModel } from "js-tiktoken";

const enc = encodingForModel("gpt-4"); // cl100k_base

function fenceAfter(md, headingRe) {
  const idx = md.search(headingRe);
  if (idx < 0) return null;
  const rest = md.slice(idx);
  const start = rest.indexOf("```");
  if (start < 0) return null;
  const end = rest.indexOf("```", start + 3);
  if (end < 0) return null;
  return rest.slice(start + 3, end).replace(/^[a-z]*\n/, "").trim() || null;
}

function fenceFlat(md, headingRe) {
  const raw = fenceAfter(md, headingRe);
  if (raw === null) return null;
  return raw
    .split(/\n\s*\n/)
    .map((p) => p.replace(/\s*\n\s*/g, " ").trim())
    .join("\n\n")
    .trim();
}

function quoteAfter(md, headingRe) {
  const lines = md.split("\n");
  for (let i = 0; i < lines.length; i++) {
    if (!headingRe.test(lines[i])) continue;
    let j = i + 1;
    while (j < lines.length && lines[j].trim() === "") j++;
    const out = [];
    while (j < lines.length) {
      const line = lines[j];
      if (line.trimStart().startsWith(">")) out.push(line.replace(/^\s*>\s?/, ""));
      else if (line.trim() === "") out.push("");
      else break;
      j++;
    }
    while (out.length && out[out.length - 1].trim() === "") out.pop();
    const text = out.join("\n").trim();
    return text || null;
  }
  return null;
}

function brokenEmphasis(s) {
  const stars = (s.match(/\*/g) ?? []).length;
  if (stars % 2 !== 0) return true;
  for (const m of s.matchAll(/\*([^*]+)\*/g)) if (m[1].includes('"')) return true;
  return false;
}

const CYR = /[\u0400-\u04FF]/;
const DASH = /[—–]/;

const md = readFileSync(process.argv[2], "utf8");

const fields = {
  name: (md.match(/^name:\s*(.+)$/m) ?? [])[1] ?? null,
  nickname: (md.match(/^nickname:\s*([^#\n]+)/m) ?? [])[1]?.trim() ?? null,
  description: quoteAfter(md, /^### DESCRIPTION/m),
  persona: fenceFlat(md, /^### persona\b/m),
  world_scenario: fenceFlat(md, /^### world_scenario/m),
  creator_notes: fenceFlat(md, /^### CREATOR NOTES/m),
  G01: quoteAfter(md, /^### G-01\b/m),
  G02: quoteAfter(md, /^### G-02\b/m),
  G03: quoteAfter(md, /^### G-03\b/m),
  example_dialogue: fenceAfter(md, /^## L07 DIALOGUE/m),
  canon_appearance: fenceAfter(md, /^### canon\.appearance/m),
};

let fail = 0;
const failMsg = (k, msg) => {
  fail++;
  console.log(`  FAIL ${k}: ${msg}`);
};

for (const [k, v] of Object.entries(fields)) {
  if (!v) {
    console.log(`${k}: MISSING`);
    continue;
  }
  const tok = enc.encode(v).length;
  const ch = v.length;
  console.log(`${k}: ${tok} tok / ${ch} chars`);

  // законы
  if (k !== "name" && k !== "nickname") {
    if (CYR.test(v)) failMsg(k, "кириллица в EN-поле (закон языка v1.3)");
    if (DASH.test(v)) failMsg(k, "em/en dash в тексте (закон типографики)");
    if (brokenEmphasis(v)) failMsg(k, "реплика внутри звёздочек или порванные звёздочки (закон формата v1.4.2)");
  }
}

// бюджетные гейты
const p = fields.persona ? enc.encode(fields.persona).length : 0;
const s = fields.world_scenario ? enc.encode(fields.world_scenario).length : 0;
if (p && (p < 500 || p > 700)) failMsg("persona", `${p} tok вне 500-700`);
if (s && s > 100) failMsg("world_scenario", `${s} tok > 100`);
const d = fields.description?.length ?? 0;
if (d && d > 700) failMsg("description", `${d} chars > 700`);

// em dash во всём документе (закон типографики 2026-11-04)
if (DASH.test(md)) failMsg("document", "em/en dash где-то в документе");

console.log(fail === 0 ? "=== ALL GATES OK ===" : `=== GATES FAILED: ${fail} ===`);
