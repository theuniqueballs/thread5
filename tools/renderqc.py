#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""renderqc.py — RENDER-QC конвейер (ПЛАН 5.5 T2.1, В56 «гейты мерили
бумагу»; вердикт T5-34: 15 ложных R+ из 17 при чистых гейтах).

Продукт-изация сеанса t534-render-qc (tools/out/t534-render-qc — 34
сырых VLM-ответа, привязка к слотам по канон-локам): инбокс-рендеры →
VLM-разбор → таблица «слот / заявка / канон-локи / тема-эхо» → автодрафт
rating_truth_delta в прилавок вердикта. Автор арбитрирует готовую
таблицу одним взглядом (В56: fact-слой обязателен до вердикта).

Уроки, вшитые в инструмент:
- T5-17/T5-33: пин по исключению не ставится — спорные файлы уходят
  строкой «unknown» автору, не карантином всего инбокса;
- 401-инцидент T5-33: VLM-шаг живёт отдельной командой (prompt/run),
  ретраи и «не разобрано» — честно, падение одного файла не роняет
  таблицу;
- claim ≠ fact: столбец truth остаётся пустым — тир решает автор
  (LAWS §9), машина даёт только канон-локи и эхо.

Команды:
  slots  --batch T5-34            словарь заявок: слот/тир/имя/канон-токены
  prompt --batch T5-34            канонический VLM-промпт (9 секций)
  table  --qc-dir tools/out/t534-render-qc --batch T5-34
                                  таблица table.md + дельта-драфт
                                  delta-draft.json (truth: null — автор)
  oc-fidelity [--out DIR]         дрифт-таблица канон-локов по девицам
                                  партия за партией (ПЛАН 5.5 T6.3)
Выход: 0 = ок · 1 = аргументы · 3 = краш.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Канонические секции VLM-разбора (надмножество форматов t534: покрывает
# и CHARACTER/CLOTHING STATE, и HAIR/EYES/MARKERS/GARMENT)
SECTIONS = [
    "HAIR", "EYES", "MARKERS", "GARMENT", "POSE", "CAMERA", "SCENE",
    "RATING EVIDENCE", "THEME ECHO",
]
SECTION_RE = re.compile(r"^\d+\)\s*([A-Z][A-Z /-]{2,30}):\s*(.*)$", re.M)
PNUM_RE = re.compile(r"\bP(\d{1,3})\b")
RATING_RE = re.compile(r"\b(R\+|PG-13|R|X)\b")


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


# ── слоты партии: заявка + канон-токены ─────────────────────────────────

def canon_sources():
    """oc-canon + special-roster: имя → текст канона (для пина рендера)."""
    out = {}
    try:
        occ = load_json(ROOT / "specs/oc-canon.json").get("ocs", {})
        for name, o in occ.items():
            if not o.get("active", True):
                continue
            txt = " ".join(filter(None, [
                str(o.get("hair") or ""), str(o.get("eyes") or ""),
                str(o.get("skin") or ""),
                " ".join(str(m) for m in o.get("signature_marks") or [])]))
            if txt.strip():
                out[name] = txt
    except Exception:
        pass
    try:
        for g in load_json(ROOT / "specs/special-roster.json").get("guests", []):
            out[g["name"]] = str(g.get("canon_run") or "")
    except Exception:
        pass
    return out


def canon_tokens(text):
    stop = {"hair", "skin", "eyes", "eye", "body", "face", "with", "tied",
            "over", "left", "right", "very", "long", "small", "large",
            "black", "white", "red", "green", "blue", "blonde", "gold",
            "golden", "silver", "purple", "pink", "pale", "soft"}
    return {w[:5] for w in re.findall(r"[a-zA-Z']+", text.lower())
            if len(w) >= 5 and w.lower() not in stop}


def cmd_slots(batch):
    sys.path.insert(0, str(ROOT / "tools"))
    import gates
    _, _, slots = gates.parse_batch(str(ROOT / "batches" / f"{batch}.md"))
    srcs = canon_sources()
    oc_names = gates.load_oc_names()
    rows = []
    for s in slots:
        name = next((n for n in list(oc_names) + list(srcs)
                     if n in {t.strip() for t in s.paren.split("·")}), None)
        rows.append({
            "slot": s.sid, "claim": s.rating, "genre": s.genre,
            "name": name,
            "canon_tokens": sorted(canon_tokens(srcs.get(name, "")))
            if name else [],
        })
    print(json.dumps(rows, ensure_ascii=False, indent=1))
    return 0


# ── канонический VLM-промпт ─────────────────────────────────────────────

def cmd_prompt(batch):
    srcs = canon_sources()
    names = " / ".join(sorted(srcs)) or "—"
    print(f"""Ты — рендер-QC цеха THREAD 5. Разбери приложенный рендер партии
{batch} ПО СЕКЦИЯМ, ровно эти 9 заголовков, каждый с новой строки
«N) ЗАГОЛОВОК: …»:

1) HAIR: цвет/длина/причёка — дословно что видно.
2) EYES: цвет/форма/взгляд.
3) MARKERS: шрамы/тату/очки/протезы/маркеры канона.
4) GARMENT: ЧТО надето и В КАКОМ СОСТОЯНИИ (мокрое/смещено/натянуто).
5) POSE: геометрия тела — что ДЕЛАЮТ руки/ноги/корпус.
6) CAMERA: дистанция/угол/фокус.
7) SCENE: фон/свет/предметы.
8) RATING EVIDENCE: что в кадре несёт тир (носители: ткань/геометрия/
   камера) — БЕЗ присвоения тира, только факты пикселей.
9) THEME ECHO: есть ли в кадре аксиомы темы партии (свет/насыщение/
   мотив-предмет) — что именно.

Канон-локи для сверки (фамилии партии): {names}.
Не выдумывай того, чего не видно; «не видно» — честный ответ.""")


# ── таблица: разбор QC-JSON → слоты ────────────────────────────────────

def parse_qc_file(path):
    """VLM-ответ → {секции}; None если файл не похож на ответ."""
    try:
        j = load_json(path)
        content = j["choices"][0]["message"]["content"]
    except Exception:
        return None
    secs = {}
    for m in SECTION_RE.finditer(content):
        key = m.group(1).strip()
        secs.setdefault(key, m.group(2).strip())
    # хвост последней секции — до следующего заголовка не нужен: секции
    # короткие, первых строк достаточно для пина
    return secs or None


def pin_to_slot(secs, filename, slot_rows, srcs):
    """Пин файла к слоту: (1) P-номер в имени файла; (2) канон-локи.
    Урок T5-17/T5-33: спорный пин не ставится — ('unknown', причина)."""
    m = PNUM_RE.search(filename)
    if m:
        sid = f"P{int(m.group(1)):02d}"
        if any(r["slot"] == sid for r in slot_rows):
            return sid, "имя файла"
    body = " ".join(str(v) for v in secs.values())
    btoks = canon_tokens(body)
    best, best_n = None, 0
    for name, txt in srcs.items():
        n = len(canon_tokens(txt) & btoks)
        if n > best_n:
            best, best_n = name, n
    if best and best_n >= 3:
        cands = [r for r in slot_rows if r["name"] == best]
        if len(cands) == 1:
            return cands[0]["slot"], f"канон-локи {best} ({best_n} стемов)"
        if len(cands) > 1:
            return "unknown", f"канон {best} в нескольких слотах — автору"
    return "unknown", (f"слабый пин (лучший {best or '—'} {best_n} стемов)"
                       if best else "канон-локи не найдены")


def cmd_table(qc_dir, batch, out_dir=None):
    sys.path.insert(0, str(ROOT / "tools"))
    import gates
    batch_path = ROOT / "batches" / f"{batch}.md"
    _, _, slots = gates.parse_batch(str(batch_path))
    srcs = canon_sources()
    oc_names = gates.load_oc_names()
    slot_rows = []
    for s in slots:
        name = next((n for n in list(oc_names) + list(srcs)
                     if n in {t.strip() for t in s.paren.split("·")}), None)
        slot_rows.append({"slot": s.sid, "claim": s.rating,
                          "genre": s.genre, "name": name})
    by_sid = {r["slot"]: r for r in slot_rows}

    rows, unknown = [], []
    for f in sorted(Path(qc_dir).glob("*.json")):
        secs = parse_qc_file(f)
        if secs is None:
            unknown.append({"file": f.name, "slot": "unknown",
                            "pin_reason": "не VLM-ответ (манифест/битый)",
                            "claim": None, "canon_locks": [],
                            "theme_echo": False, "note": "", "truth": None})
            continue
        sid, why = pin_to_slot(secs, f.name, slot_rows, srcs)
        claim = by_sid.get(sid, {}).get("claim")
        # канон-локи: MARKERS/HAIR/EYES против канона имени слота
        canon_txt = srcs.get(by_sid.get(sid, {}).get("name") or "", "")
        ctoks = canon_tokens(canon_txt) if canon_txt else set()
        body = " ".join(str(secs.get(k, "")) for k in
                        ("MARKERS", "HAIR", "EYES", "CHARACTER"))
        hits = sorted(ctoks & canon_tokens(body)) if ctoks else []
        theme = secs.get("THEME ECHO") or secs.get("ACID/LSD THEME") or ""
        row = {
            "file": f.name, "slot": sid, "pin_reason": why,
            "claim": claim,
            "canon_locks": hits if sid != "unknown" else [],
            "theme_echo": bool(theme) and "not" not in theme.lower()[:40],
            "note": "; ".join(
                f"{k}: {str(secs.get(k, ''))[:90]}" for k in
                ("RATING EVIDENCE", "RATING VERDICT", "GARMENT") if k in secs
            )[:280],
            "truth": None,  # тир решает автор (LAWS §9) — машина не ставит
        }
        if sid == "unknown":
            unknown.append(row)
        else:
            rows.append(row)

    out = Path(out_dir) if out_dir else Path(qc_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "delta-draft.json").write_text(json.dumps(
        {"batch": batch, "source": str(qc_dir), "rows": rows,
         "unknown": unknown,
         "law": "truth: null — тир решает автор (LAWS §9); канон-локи и "
                "эхо — факты пикселей от VLM, дельта собирается вручную "
                "поверх этого драфта (renderqc не вердиктит)"},
        ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    lines = [f"# RENDER-QC — {batch} (источник: {qc_dir})", "",
             "| Файл | Слот | Пин | Заявка | Канон-локи | Эхо | Примечание |",
             "|---|---|---|---|---|---|---|"]
    for r in rows:
        lines.append(
            f"| {r['file']} | {r['slot']} | {r['pin_reason']} | "
            f"{r['claim'] or '—'} | {', '.join(r['canon_locks']) or '—'} | "
            f"{'✓' if r['theme_echo'] else '—'} | {r['note'][:80]} |")
    if unknown:
        lines += ["", "## Не припинены (урок T5-17/T5-33 — автору, не карантин)", ""]
        for u in unknown:
            lines.append(f"- {u['file']} — {u['pin_reason']}")
    (out / "table.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"RENDER-QC {batch}: строк {len(rows)} · неизвестных {len(unknown)} · "
          f"{out / 'table.md'} · {out / 'delta-draft.json'}")
    return 0


def cmd_oc_fidelity(out_dir=None):
    """6.3 (ПЛАН 5.5): OC-FIDELITY дрифт-таблица — канон-локи каждой канонной
    девицы на каждом рендере, партия за партией (источник — delta-draft.json
    всех RENDER-QC прогонов: tools/out/*/delta-draft.json). Боль (вердикт
    T5-34: OC-fidelity 1/3 — катка SO-19 потеряна, очки SO-20 в NEG):
    дрифт по девицам обязан быть виден трендом, а не «лучший/худший батч»;
    урок T5-17/T5-33 — спорные файлы (unknown) не карантинятся, просто не
    входят в таблицу."""
    sys.path.insert(0, str(ROOT / "tools"))
    import gates
    srcs = canon_sources()
    oc_names = gates.load_oc_names()
    per_oc: dict[str, dict] = {}
    parties = []
    for p in sorted(ROOT.glob("tools/out/*/delta-draft.json")):
        try:
            d = load_json(p)
        except Exception:
            continue
        batch = d.get("batch")
        if not batch or (ROOT / "batches" / f"{batch}.md").exists() is False:
            continue
        if batch in parties:
            continue
        parties.append(batch)
        try:
            _, _, slots = gates.parse_batch(str(ROOT / "batches" / f"{batch}.md"))
        except Exception:
            continue
        by_sid = {}
        for s in slots:
            name = next((n for n in list(oc_names) + list(srcs)
                         if n in {t.strip() for t in s.paren.split("·")}), None)
            if name:
                by_sid[s.sid] = name
        for r in d.get("rows") or []:
            sid = r.get("slot")
            name = by_sid.get(sid)
            if not name or name not in srcs:
                continue
            ctoks = canon_tokens(srcs.get(name, ""))
            hits = set(r.get("canon_locks") or [])
            rec = per_oc.setdefault(name, {
                "renders": 0, "hit_tokens": 0, "expected_tokens": 0,
                "missing": {}, "batches": []})
            rec["renders"] += 1
            rec["hit_tokens"] += len(hits & ctoks)
            rec["expected_tokens"] += len(ctoks)
            for tok in sorted(ctoks - hits):
                rec["missing"][tok] = rec["missing"].get(tok, 0) + 1
            if batch not in rec["batches"]:
                rec["batches"].append(batch)

    out = Path(out_dir) if out_dir else ROOT / "tools" / "out"
    out.mkdir(parents=True, exist_ok=True)
    lines = ["# OC-FIDELITY — дрифт канон-локов по девицам (партия за партией)", "",
             f"Источник: RENDER-QC дельта-драфты ({', '.join(parties) or '—'}). "
             "Спорные файлы (unknown) не входят — урок T5-17/T5-33.", "",
             "| Девица | Партий | Рендеров | Локи: доехало/ожидалось | Верность | Топ потерянных локов |",
             "|---|---|---|---|---|---|"]
    for name in sorted(per_oc, key=lambda n: -per_oc[n]["renders"]):
        r = per_oc[name]
        fid = (f"{r['hit_tokens'] / r['expected_tokens']:.0%}"
               if r["expected_tokens"] else "—")
        lost = ", ".join(f"{t}×{n}" for t, n in
                         sorted(r["missing"].items(), key=lambda kv: -kv[1])[:4]) or "—"
        lines.append(
            f"| {name} | {len(r['batches'])} | {r['renders']} | "
            f"{r['hit_tokens']}/{r['expected_tokens']} | {fid} | {lost} |")
    if not per_oc:
        lines.append("| — | — | — | — | — | RENDER-QC дельт ещё нет |")
    (out / "oc-fidelity.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    total_h = sum(r["hit_tokens"] for r in per_oc.values())
    total_e = sum(r["expected_tokens"] for r in per_oc.values())
    print(f"OC-FIDELITY: девиц {len(per_oc)} · партий {len(parties)} · "
          f"локов {total_h}/{total_e}"
          + (f" ({total_h / total_e:.0%})" if total_e else "")
          + f" · {out / 'oc-fidelity.md'}")
    return 0


def main():
    args = sys.argv[1:]
    try:
        if args and args[0] == "slots" and "--batch" in args:
            return cmd_slots(args[args.index("--batch") + 1])
        if args and args[0] == "prompt" and "--batch" in args:
            return cmd_prompt(args[args.index("--batch") + 1])
        if args and args[0] == "table" and "--qc-dir" in args and "--batch" in args:
            i = args.index("--qc-dir")
            b = args.index("--batch")
            out = (args[args.index("--out") + 1]
                   if "--out" in args else None)
            return cmd_table(args[i + 1], args[b + 1], out)
        if args and args[0] == "oc-fidelity":
            out = (args[args.index("--out") + 1]
                   if "--out" in args else None)
            return cmd_oc_fidelity(out)
    except Exception as e:  # краш инструмента — не FAIL батча
        print(f"RENDER-QC КРАШ: {e}", file=sys.stderr)
        return 3
    print(__doc__)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
