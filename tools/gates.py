#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
THREAD 5 — машинные гейты печи (аудит 2026-10-28, 8.2.1–8.2.6 + аудит 2026-10-31, рек. 1–4).

Проверяет СОГЛАСОВАННОСТЬ текста батча и физику заявок. Не пишет промпты,
не заменяет вердикт автора (LAWS §9: единственный законодатель — вердикт).

v1.2.0 (внешний аудит 2026-10-31, F1–F8): гейт «R+ без заявки» (claim-exists),
поиск заявки без порядка слов, POS-флоры (milf/приборы/имена OC/IP/титул темы),
реестровые коды (палитры/позы/кинетики/носители), каст кинов (12–14/21,
active/gold, RF≤2, карантин R30), межбатчевый копипаст (6-граммы против двух
предыдущих партий), формат строки слота (метки ⚗/☠ за скобкой); парсер терпит
метки внутри скобок.

Прогон:
    python3 tools/gates.py batches/T5-08.md \
        --json specs/gate-receipts/2026-10-30-T5-08-v12.json \
        --md batches/T5-08.gate-report.md
"""

import hashlib
import json
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GATES = json.loads((ROOT / "specs/gates.json").read_text(encoding="utf-8"))

SLOT_RE = re.compile(
    r"^P(\d{2})\s+—\s+(\S+)\s+\((.+?)\)\s*[⚗☠]?\s*$"
)
STOP = {
    "the", "a", "an", "of", "and", "or", "to", "in", "on", "at", "by",
    "for", "with", "her", "his", "its", "as", "is", "are",
}


def words(text):
    return re.findall(r"[A-Za-z0-9_']+", text.lower())


def norm_ws(text):
    return re.sub(r"\s+", " ", text).strip()


class Slot:
    def __init__(self, sid, slug, paren, header_line):
        self.sid = f"P{sid}"
        self.slug = slug
        self.paren = paren
        self.header_line = header_line
        self.genre = ""
        self.rating = ""
        self.pose = ""
        self.palette = ""
        self.kinetics = []
        self.carriers = []
        self.channel = None
        self.channel_mark = ""
        self.mark = "☠" if "☠" in header_line else ("⚗" if "⚗" in header_line else "")
        self.thesis = ""
        self.pos = ""
        self.neg = ""
        parts = [p.strip() for p in paren.split("·")]
        if parts:
            self.genre = parts[0]
        for p in parts:
            # аудит 2026-10-31, F3: метка внутри скобок («R+ ☠») не гасит тир
            p_clean = p.replace("☠", "").replace("⚗", "").strip()
            if p_clean in ("R+", "R", "PG-13", "X"):
                self.rating = p_clean
        m = re.search(r"\bPL\d+\b", paren)
        if m:
            self.pose = m.group(0)
        m = re.search(r"\bP\d{1,3}_[A-Z0-9_]+", paren)
        if m:
            self.palette = m.group(0)


def parse_batch(path):
    text = Path(path).read_text(encoding="utf-8")
    lines = text.splitlines()
    slots = []
    header_lines = []
    cur = None
    mode = None
    buf = []
    in_header_zone = True

    def flush_mode():
        nonlocal mode, buf
        if cur is not None and mode == "pos":
            cur.pos = norm_ws(" ".join(buf))
        elif cur is not None and mode == "neg":
            cur.neg = norm_ws(" ".join(buf))
        mode, buf = None, []

    for ln in lines:
        m = SLOT_RE.match(ln)
        if m and not ln.startswith((" ", "\t")):
            flush_mode()
            cur = Slot(m.group(1), m.group(2), m.group(3), ln)
            slots.append(cur)
            in_header_zone = False
            continue
        if ln.startswith("═"):
            flush_mode()
            continue
        if in_header_zone:
            header_lines.append(ln)
        if cur is None:
            continue
        sm = re.match(r"^Spine:\s*(.*)$", ln)
        if sm:
            flush_mode()
            cur.kinetics += re.findall(r"\bK\d{1,3}\b", sm.group(1))
            continue
        sm = re.match(r"^Stack:\s*(.*)$", ln)
        if sm:
            flush_mode()
            cur.carriers += re.findall(r"\bCR-[A-Z]\d+\b", sm.group(1))
            continue
        sm = re.match(r"^Channel:\s*(.*)$", ln)
        if sm:
            flush_mode()
            val = sm.group(1).strip()
            cur.channel = val.split()[0] if val else None
            cur.channel_mark = "☠" if "☠" in val else ""
            continue
        if re.match(r"^POS:\s*$", ln):
            flush_mode()
            mode, buf = "pos", []
            continue
        if re.match(r"^NEG:\s*$", ln):
            flush_mode()
            mode, buf = "neg", []
            continue
        tm = re.match(r"^THESIS:\s*(.*)$", ln)
        if tm:
            flush_mode()
            cur.thesis = tm.group(1).strip()
            continue
        if mode:
            buf.append(ln.strip())
    flush_mode()
    header = "\n".join(header_lines)
    return text, header, slots


def ab_pairs_from_header(header):
    return {
        frozenset((a, b))
        for a, b in re.findall(r"\((P\d{2})\s*,\s*(P\d{2})\)", header)
    }


def check_floors(slot, fails):
    neg = slot.neg.lower()
    for f in GATES["header"]["hardFloors"]:
        if f.lower() not in neg:
            fails.append((slot.sid, "floor", f"NEG нет hard-флоры: {f}"))
    for w in GATES["header"]["candleFloorWords"]:
        if w not in neg:
            fails.append((slot.sid, "floor", f"NEG нет candle/lamp-флоры: {w}"))
    for w in GATES["header"]["antiWash"]:
        if w.lower() not in neg:
            fails.append((slot.sid, "floor", f"NEG нет анти-ваша: {w}"))


def stem_variants(w):
    """Варианты слова для сверки POS↔NEG: snakes→{snakes,snake,snak}, joints→{joints,joint}."""
    v = {w}
    if w.endswith("ies") and len(w) > 4:
        v.add(w[:-3] + "y")
    if w.endswith("es") and len(w) > 3:
        v.add(w[:-2])
    if w.endswith("s") and not w.endswith("ss") and len(w) > 3:
        v.add(w[:-1])
    return v


def check_neg_linter(slot, fails, warns):
    if not slot.neg:
        fails.append((slot.sid, "neg", "NEG пуст"))
        return
    pos_stems = set()
    for w in words(slot.pos):
        pos_stems |= stem_variants(w)
    for unit in slot.neg.split(","):
        unit = norm_ws(unit)
        if not unit:
            continue
        uwords = words(unit)
        if len(uwords) > GATES["neg"]["unitMaxWords"]:
            warns.append(
                (slot.sid, "neg-unit",
                 f"юнит NEG из {len(uwords)} слов: «{unit}»")
            )
        m = re.match(GATES["neg"]["noClassPattern"], unit.lower())
        if m:
            hit = []
            for tw in words(m.group(2)):
                if tw in STOP or len(tw) < 3:
                    continue
                if stem_variants(tw) & pos_stems:
                    hit.append(tw)
            if hit:
                fails.append(
                    (slot.sid, "neg-no-class",
                     f"«{unit}» отрицает то, что заявлено в POS (→ {', '.join(hit)})")
                )
        low = unit.lower()
        if low == "nipples exposed" and re.search(
            r"covered nipples|clothed nipples|see-through|wet clothes|pantyline",
            slot.pos, re.I,
        ):
            fails.append(
                (slot.sid, "neg-self-shot",
                 "«nipples exposed» в NEG сквозь-ткань слота глушит заявку (каталог A3)")
            )


CLAIM_RE = re.compile(
    "|".join(re.escape(s) for s in sorted(
        GATES["claim"]["signal_lexemes"], key=len, reverse=True)),
    re.I,
)


# Поиск заявки БЕЗ порядка слов (аудит 2026-10-31, F1/P19: «forearms crossed
# over her bare breasts» против лексемы «crossed forearms over»).
MULTIWORD_CLAIMS = [
    s for s in GATES["claim"]["signal_lexemes"] if len(words(s)) > 1
]


def claim_token(slot):
    for m in CLAIM_RE.finditer(slot.pos):
        prefix = slot.pos[: m.start()]
        return len(words(prefix)), m.group(0).lower()
    wl = words(slot.pos)
    for lex in MULTIWORD_CLAIMS:
        lw = words(lex)
        if sum(1 for w in lw if w not in STOP) < 2:
            continue  # общие наборы («tape over») без порядка не маттим
        n = len(lw)
        for i in range(len(wl) - n + 1):
            if sorted(wl[i: i + n]) == sorted(lw):
                return i, f"{lex} (без порядка слов)"
    return None, None


def check_salience(slot, idx, sig, fails, warns):
    if idx is None:
        return idx
    if slot.mark:  # умышленный нарушитель (EXP-полигон, закон ⚗) — не гейтится
        return idx
    limit_key = "maxTokenRplus" if slot.rating == "R+" else "maxTokenR"
    limit = GATES["claim"][limit_key]
    hard = slot.rating == "R+"
    if idx > limit:
        msg = f"заявка «{sig}» на токене {idx} > {limit}"
        (fails if hard else warns).append(
            (slot.sid, "salience", msg + ("" if hard else " (R, WARN)"))
        )
    return idx


def check_pos_budget(slot, fails, warns):
    n = len(words(slot.pos))
    if GATES["pos"].get("unlimited"):
        # Вердикт T5-08 (2026-10-31): бюджет POS не ограничивается — решение
        # автора (ответ на F8 аудита). Число слов остаётся в отчёте.
        return n
    if n > GATES["pos"]["hardTokens"]:
        fails.append((slot.sid, "pos-budget", f"POS {n} слов > hard {GATES['pos']['hardTokens']}"))
    elif n > GATES["pos"]["targetTokens"]:
        warns.append((slot.sid, "pos-budget", f"POS {n} слов > цель {GATES['pos']['targetTokens']}"))
    return n


def strip_boilerplate(pos):
    out = pos
    for b in GATES["copypaste"]["boilerplateStrip"]:
        out = re.sub(re.escape(b), " ", out, flags=re.I)
    return out


def check_copypaste(slots, ab_pairs, fails, warns):
    gram_slots = {}
    for s in slots:
        wl = words(strip_boilerplate(s.pos))
        for i in range(len(wl) - GATES["copypaste"]["ngramWords"] + 1):
            g = " ".join(wl[i: i + GATES["copypaste"]["ngramWords"]])
            gram_slots.setdefault(g, set()).add(s.sid)
    fails_seen, warn_pairs = set(), set()
    for g, ids in gram_slots.items():
        if len(ids) >= GATES["copypaste"]["failSharedBySlots"]:
            key = ("FAIL", tuple(sorted(ids)), g)
            if key not in fails_seen:
                fails_seen.add(key)
                fails.append(
                    (",".join(sorted(ids)), "copypaste",
                     f"{len(ids)} слота делят n-грамму: «{g}»")
                )
        elif len(ids) == 2:
            pair = frozenset(ids)
            if pair in ab_pairs:
                continue
            warn_pairs.add((tuple(sorted(ids)), g))
    for (a, b), g in sorted(warn_pairs)[:20]:
        warns.append((f"{a}+{b}", "copypaste", f"пара делит n-грамму: «{g}»"))


def load_burned():
    data = json.loads((ROOT / "specs/burned.json").read_text(encoding="utf-8"))
    return {e["code"] for e in data["entries"]}


def load_channels():
    data = json.loads(
        (ROOT / GATES["channels"]["registry"]).read_text(encoding="utf-8")
    )
    return {c["id"]: c for c in data["channels"]}


def check_burn(slot, burned, fails):
    codes = [c for c in [slot.palette, slot.pose] if c] + slot.kinetics + slot.carriers
    for c in codes:
        if c in burned:
            fails.append(
                (slot.sid, "burn", f"{c} в burn-реестре (сгорел, в оборот нельзя)")
            )


def check_channels(slots, channels, fails, warns):
    quota = GATES["channels"]["candidateQuotaPerBatch"]
    cand_used, panty_used = [], []
    for s in slots:
        if not s.channel:
            if s.rating in ("R+", "X") and s.genre != "EXP":
                warns.append((s.sid, "channel", "R+ слот без аннотации Channel:"))
            continue
        ch = channels.get(s.channel)
        if ch is None:
            warns.append((s.sid, "channel", f"канал «{s.channel}» не в реестре"))
            continue
        status = ch["status"]
        if s.genre == "EXP" and GATES["channels"]["expOverlayExempt"]:
            continue
        if s.channel in GATES["channels"]["exempt"]:
            continue
        if s.rating in ("R+", "X"):
            if status in ("dead", "rehab", "artifact"):
                fails.append((s.sid, "channel", f"R+ на {status}-канале {s.channel}"))
            elif status == "candidate":
                if GATES["channels"]["candidateMark"] not in (s.channel_mark or ""):
                    warns.append(
                        (s.sid, "channel",
                         f"candidate-канал {s.channel} без пометки ☠")
                    )
                cand_used.append(s.sid)
                if s.channel == "pantyline-lower":
                    panty_used.append(s.sid)
    if len(cand_used) > quota:
        warns.append(
            ("BATCH", "channel-quota",
             f"candidate-каналы использованы {len(cand_used)}× ({','.join(cand_used)}) > {quota} — WARN волны 2, эскалация по KPI")
        )
    if len(panty_used) > 2:
        warns.append(
            ("BATCH", "pantyline-quota",
             f"pantyline {len(panty_used)}× ({','.join(panty_used)}) > 2 — WARN волны 2")
        )


def check_header(text, header, slots, fails, warns):
    if GATES["header"]["ecchiKeyForbidden"]:
        for s in slots:
            if "ecchi anime style" in s.pos.lower():
                fails.append(
                    (s.sid, "ecchi-key",
                     "«ecchi anime style» в POS — ключ снят вердиктом T5-05 (2026-10-28): «ничего не делает, я проверял»")
                )
    exp_decl = re.search(r"EXP-оверлей\s*\((\d+)", header)
    exp_fact = sum(1 for s in slots if s.genre == "EXP")
    if exp_decl and int(exp_decl.group(1)) != exp_fact:
        warns.append(
            ("BATCH", "header",
             f"шапка заявляет EXP {exp_decl.group(1)}, по факту {exp_fact}")
        )
    spread = re.search(r"R\+×(\d+)\s*·\s*R×(\d+)", header)
    if spread:
        mains = [s for s in slots if s.genre not in ("OC", "EXP")]
        rplus = sum(1 for s in mains if s.rating == "R+")
        r = sum(1 for s in mains if s.rating == "R")
        if (rplus, r) != (int(spread.group(1)), int(spread.group(2))):
            warns.append(
                ("BATCH", "header",
                 f"спред шапки R+×{spread.group(1)}·R×{spread.group(2)} ≠ факт R+×{rplus}·R×{r}")
            )
    if GATES["header"]["windowStatement"] and "Окно" not in header:
        warns.append(("BATCH", "header", "в шапке нет заявления окна ротации"))


def load_oc_names():
    data = json.loads(
        (ROOT / GATES["posFloors"]["ocNamesRegistry"]).read_text(encoding="utf-8")
    )
    return [k for k, v in data.get("ocs", {}).items() if v.get("active", True)]


def load_race_statuses():
    data = json.loads((ROOT / "specs/races.json").read_text(encoding="utf-8"))
    return {r["id"]: r.get("status", "?") for r in data.get("races", [])}


def load_registry_ids(rel, pattern):
    data = json.loads((ROOT / rel).read_text(encoding="utf-8"))
    ids = set()

    def walk(o):
        if isinstance(o, dict):
            v = o.get("id")
            if isinstance(v, str) and re.fullmatch(pattern, v):
                ids.add(v)
            for x in o.values():
                walk(x)
        elif isinstance(o, list):
            for x in o:
                walk(x)

    walk(data)
    return ids


def batch_title(text):
    m = re.search(r'Batch T5-\d+R?:\s*«(.+?)»', text)
    if not m:
        m = re.search(r'Batch T5-\d+R?:\s*"(.+?)"', text)
    return m.group(1) if m else None


def check_claim_exists(slot, idx, fails, warns, batch_no=-1):
    """Аудит 2026-10-31, F1/рек.1: R+/X слот без лексемы заявки в POS.

    v1.3.0 (вердикт T5-08, 2026-10-31): эскалация исполнена — FAIL;
    исторические партии (номер < applyFrom) остаются в WARN-эре:
    задним числом не переписываются (урок F2).
    """
    cfg = GATES["claimGate"]
    if slot.rating not in ("R+", "X") or slot.mark:
        return
    if idx is None:
        escalated = (
            cfg["mode"] == "fail"
            and not (cfg.get("applyFrom") and batch_no < cfg["applyFrom"])
        )
        if not escalated:
            msg = (
                f"{slot.rating} без лексемы заявки в POS — тир держится только "
                f"THESIS, рендерер прозу не видит (аудит 2026-10-31, F1; WARN-эра: эскалация с T5-{cfg.get('applyFrom', '?'):02d})"
            )
            warns.append((slot.sid, "claim-exists", msg))
        else:
            msg = (
                f"{slot.rating} без лексемы заявки в POS — тир держится только "
                f"THESIS, рендерер прозу не видит (аудит 2026-10-31, F1; FAIL с T5-{cfg.get('applyFrom', '?'):02d})"
            )
            fails.append((slot.sid, "claim-exists", msg))


def check_registry(slot, registries, warns):
    """Аудит 2026-10-31, F4/рек.3: коды слота против реестров specs/*.json."""
    pairs = [
        ("палитра", registries["palettes"], [slot.palette]),
        ("поза", registries["poses"], [slot.pose]),
        ("кинетика", registries["kinetics"], slot.kinetics),
        ("носитель", registries["carriers"], slot.carriers),
    ]
    for kind, (path, ids), codes in pairs:
        for c in codes:
            if c and c not in ids:
                warns.append(
                    (slot.sid, "registry",
                     f"{kind} {c} не в реестре {path} — опечатка кода? (аудит 2026-10-31, F4)")
                )


def check_pos_floors(slots, text, oc_names, warns):
    """Аудит 2026-10-31, §8: сторона POS, которую гейты v1.1 не видели."""
    cfg = GATES["posFloors"]
    title = batch_title(text)
    # имена-омонимы обычных слов (ash/doe/rue/sol/mab) матчатся только
    # с заглавной — «ash-brown hair» и «pale ash» не имя OC (v1.2.1 прогон)
    case_names = set(cfg.get("namesCaseSensitive", []))
    for s in slots:
        if re.search(r"\bmilf\b", s.pos, re.I):
            warns.append(
                (s.sid, "pos-floors",
                 "слово milf в POS — banned everywhere (policy writer_rules)"))
        if "[intentional]" not in s.pos.lower():
            for dw in cfg["deviceWords"]:
                if re.search(rf"\b{re.escape(dw)}\b", s.pos, re.I):
                    warns.append(
                        (s.sid, "pos-floors",
                         f"приборное слово «{dw}» в POS — закон света v2: свет поведением, прибор только по [INTENTIONAL] (T5-06)"))
        for nm in oc_names:
            if nm in case_names:
                hit = re.search(rf"\b{re.escape(nm)}\b", s.pos)
            else:
                hit = re.search(rf"\b{re.escape(nm)}\b", s.pos, re.I)
            if hit:
                warns.append(
                    (s.sid, "pos-floors",
                     f"имя OC «{nm}» в POS — имена OC никогда не в POS (LAWS §2.4)"))
        for ip in cfg["ipNames"]:
            if ip.lower() in s.pos.lower():
                warns.append(
                    (s.sid, "pos-floors",
                     f"IP-имя «{ip}» в POS (LAWS §6)"))
        if title and title.lower() in s.pos.lower():
            warns.append(
                (s.sid, "pos-floors",
                 f"титул темы «{title}» целиком в POS — тема живёт тегами по делу (LAWS §6)"))


def check_race_cast(header, slots, statuses, warns):
    """Аудит 2026-10-31, §8: каст кинов против races.json и шапки."""
    cfg = GATES["raceCast"]
    mains = [s for s in slots if s.genre not in ("OC", "EXP")]
    counts = Counter(
        c for s in mains for c in re.findall(r"\bR\d{2}\b", s.paren)
    )
    for c, n in sorted(counts.items()):
        st = statuses.get(c)
        if c in cfg["quarantine"]:
            warns.append(("BATCH", "race-cast",
                          f"{c} в карантине (races.json v2.3.0) — не назначать (в батче {n}×)"))
        elif st in (None, "?"):
            warns.append(("BATCH", "race-cast",
                          f"{c} не в реестре races.json"))
        elif st not in ("active", "gold"):
            warns.append(("BATCH", "race-cast",
                          f"{c} статус «{st}» — не назначать (в батче {n}×)"))
        if n > cfg["rfMax"]:
            warns.append(("BATCH", "race-cast",
                          f"{c} использован {n}× > RF {cfg['rfMax']}"))
    declared = re.search(r"каст\s+(\d{1,2})/(\d{1,2})", header)
    fact = sum(1 for s in mains if re.search(r"\bR\d{2}\b", s.paren))
    if declared and int(declared.group(1)) != fact:
        warns.append(
            ("BATCH", "race-cast",
             f"шапка заявляет каст {declared.group(1)}/{declared.group(2)}, по факту {fact} (аудит 2026-10-31, F5)"))
    if fact < cfg["min"] or fact > cfg["max"]:
        warns.append(
            ("BATCH", "race-cast",
             f"каст {fact}/{len(mains)} вне вилки {cfg['min']}–{cfg['max']} (policy v1.8)"))


def check_slot_format(slots, warns):
    """Аудит 2026-10-31, F3/рек.3: метки ⚗/☠ — только за закрывающей скобкой."""
    for s in slots:
        end = s.header_line.rfind(")")
        if end != -1 and any(ch in s.header_line[:end] for ch in "⚗☠"):
            warns.append(
                (s.sid, "slot-format",
                 "метка ⚗/☠ внутри скобок — конвенция: только за скобкой (F3)"))


def batch_number(path):
    m = re.search(r"T5-(\d+)", Path(path).name)
    return int(m.group(1)) if m else -1


def pos_grams(slots):
    grams = {}
    n = GATES["copypaste"]["ngramWords"]
    for s in slots:
        wl = words(strip_boilerplate(s.pos))
        for i in range(len(wl) - n + 1):
            g = " ".join(wl[i: i + n])
            grams.setdefault(g, set()).add(s.sid)
    return grams


def check_cross_batch(batch_path, slots, warns):
    """Аудит 2026-10-31, F6/рек.4: 6-граммы против двух предыдущих партий."""
    cfg = GATES["crossBatch"]
    num = batch_number(batch_path)
    prevs = sorted(
        (p for p in (ROOT / "batches").glob("T5-*.md")
         if not p.name.endswith(".gate-report.md")
         and p.resolve() != Path(batch_path).resolve()
         and 0 < batch_number(p) < num),
        key=lambda p: (batch_number(p), p.stat().st_mtime),
        reverse=True,
    )[: cfg["prevDepth"]]
    if not prevs:
        return []
    seen = {}
    for p in prevs:
        _, _, pslots = parse_batch(p)
        for g, ids in pos_grams(pslots).items():
            seen.setdefault(g, (p.name, ids))
    hits = []
    for g, ids in pos_grams(slots).items():
        if g in seen:
            hits.append((sorted(ids), g, seen[g][0], sorted(seen[g][1])))
    if hits:
        src = ", ".join(sorted({h[2] for h in hits}))
        warns.append(
            ("BATCH", "cross-copypaste",
             f"{len(hits)} общих {GATES['copypaste']['ngramWords']}-грамм с предыдущими партиями ({src}) — межбатчевый копипаст (аудит 2026-10-31, F6); детально в квитанции"))
    return [
        {"gram": g, "slotsHere": a, "sourceBatch": p, "slotsThere": b}
        for a, g, p, b in hits[: cfg["maxListed"]]
    ]


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    batch_path = Path(sys.argv[1])
    out_json = None
    if "--json" in sys.argv:
        out_json = Path(sys.argv[sys.argv.index("--json") + 1])
    out_md = None
    if "--md" in sys.argv:
        out_md = Path(sys.argv[sys.argv.index("--md") + 1])

    text, header, slots = parse_batch(batch_path)
    batch_no = batch_number(batch_path)
    ab_pairs = ab_pairs_from_header(header)
    burned = load_burned()
    channels = load_channels()
    oc_names = load_oc_names()
    race_statuses = load_race_statuses()
    reg_cfg = GATES["registry"]
    registries = {
        "palettes": (reg_cfg["palettes"],
                     load_registry_ids(reg_cfg["palettes"], r"P\d{1,3}_[A-Z0-9_]+")),
        "poses": (reg_cfg["poses"],
                  load_registry_ids(reg_cfg["poses"], r"PL\d+")),
        "kinetics": (reg_cfg["kinetics"],
                     load_registry_ids(reg_cfg["kinetics"], r"K\d{1,3}")),
        "carriers": (reg_cfg["carriers"],
                     load_registry_ids(reg_cfg["carriers"], r"CR-[A-Z]\d+")),
    }

    fails, warns = [], []
    slot_rows = []
    for s in slots:
        check_floors(s, fails)
        check_neg_linter(s, fails, warns)
        idx, sig = claim_token(s)
        check_salience(s, idx, sig, fails, warns)
        check_claim_exists(s, idx, fails, warns, batch_no)
        n = check_pos_budget(s, fails, warns)
        check_burn(s, burned, fails)
        check_registry(s, registries, warns)
        ch_status = ""
        if s.channel and s.channel in channels:
            ch_status = channels[s.channel]["status"]
        slot_rows.append({
            "id": s.sid, "slug": s.slug, "genre": s.genre, "rating": s.rating,
            "channel": s.channel or "", "channelStatus": ch_status,
            "claimToken": idx, "posWords": n,
        })
    check_copypaste(slots, ab_pairs, fails, warns)
    check_channels(slots, channels, fails, warns)
    check_header(text, header, slots, fails, warns)
    check_pos_floors(slots, text, oc_names, warns)
    check_race_cast(header, slots, race_statuses, warns)
    check_slot_format(slots, warns)
    cross_shared = check_cross_batch(batch_path, slots, warns)

    verdict = "FAIL" if fails else "PASS"
    sha = hashlib.sha256(batch_path.read_bytes()).hexdigest()
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")

    receipt = {
        "tool": "tools/gates.py (specs/gates.json v%s)" % GATES["version"],
        "batch": str(batch_path),
        "sha256": sha,
        "utc": now,
        "verdict": verdict,
        "slots": len(slots),
        "fails": [{"slot": a, "gate": b, "msg": c} for a, b, c in fails],
        "warns": [{"slot": a, "gate": b, "msg": c} for a, b, c in warns],
        "slot_table": slot_rows,
        "crossBatchShared": cross_shared,
    }
    print(f"=== ГЕЙТЫ {batch_path} ===")
    print(f"слотов: {len(slots)} · sha256: {sha[:12]}…")
    print(f"ВЕРДИКТ: {verdict} · FAIL: {len(fails)} · WARN: {len(warns)}")
    for a, b, c in fails:
        print(f"  FAIL [{a}] {b}: {c}")
    for a, b, c in warns:
        print(f"  WARN [{a}] {b}: {c}")

    if out_json:
        out_json.parent.mkdir(parents=True, exist_ok=True)
        out_json.write_text(
            json.dumps(receipt, ensure_ascii=False, indent=1), encoding="utf-8"
        )
        print(f"квитанция: {out_json}")

    if out_md:
        lines = [
            f"# Машинная квитанция печи — {batch_path.name}",
            "",
            f"- Вердикт гейтов: **{verdict}** (FAIL {len(fails)} / WARN {len(warns)})",
            f"- sha256: `{sha}`",
            f"- Прогон: {now} · specs/gates.json v{GATES['version']}",
            "",
            "| Слот | Слаг | Жанр | Тир | Канал | Статус | Заявка, токен | POS, слов |",
            "|---|---|---|---|---|---|---|---|",
        ]
        for r in slot_rows:
            lines.append(
                "| {id} | {slug} | {genre} | {rating} | {channel} | {channelStatus} | {claimToken} | {posWords} |".format(**r)
            )
        if fails:
            lines += ["", "## FAIL", ""]
            lines += [f"- **[{a}]** {b}: {c}" for a, b, c in fails]
        if warns:
            lines += ["", "## WARN", ""]
            lines += [f"- [{a}] {b}: {c}" for a, b, c in warns]
        out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"отчёт: {out_md}")

    sys.exit(0 if verdict == "PASS" else 1)


if __name__ == "__main__":
    main()
