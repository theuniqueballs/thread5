#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
THREAD 5 — машинные гейты печи (контур 2 внешнего аудита 2026-10-28, 8.2.1–8.2.6).

Проверяет СОГЛАСОВАННОСТЬ текста батча и физику заявок. Не пишет промпты,
не заменяет вердикт автора (LAWS §9: единственный законодатель — вердикт).

Прогон:
    python3 tools/gates.py batches/T5-05.md
    python3 tools/gates.py batches/T5-05R.md --json specs/gate-receipts/2026-10-28-T5-05R.json
"""

import hashlib
import json
import re
import sys
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
            if p in ("R+", "R", "PG-13", "X"):
                self.rating = p
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


def claim_token(slot):
    for m in CLAIM_RE.finditer(slot.pos):
        prefix = slot.pos[: m.start()]
        return len(words(prefix)), m.group(0).lower()
    return None, None


def check_salience(slot, fails, warns):
    idx, sig = claim_token(slot)
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
    ab_pairs = ab_pairs_from_header(header)
    burned = load_burned()
    channels = load_channels()

    fails, warns = [], []
    slot_rows = []
    for s in slots:
        check_floors(s, fails)
        check_neg_linter(s, fails, warns)
        idx = check_salience(s, fails, warns)
        n = check_pos_budget(s, fails, warns)
        check_burn(s, burned, fails)
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
