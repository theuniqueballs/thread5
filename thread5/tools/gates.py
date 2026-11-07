#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
THREAD 5 — машинные гейты печи (аудит 2026-10-28, 8.2.1–8.2.6 + аудит 2026-10-31, рек. 1–4).

Проверяет СОГЛАСОВАННОСТЬ текста батча и физику заявок. Не пишет промпты,
не заменяет вердикт автора (LAWS §9: единственный законодатель — вердикт).

v1.2.0 (внешний аудит 2026-10-31, F1–F8): claim-exists, поиск заявки без
порядка слов, POS-флоры, реестровые коды, каст кинов, межбатчевый
копипаст, формат строки слота.
v1.3.0 (вердикт T5-08, 2026-10-31): claim-exists эскалирован до FAIL,
POS-бюджет снят (pos.unlimited). v1.4.0 (вердикт T5-09, 2026-11-01):
oc-class-floor — OC-промпты класса EXQUISITE не ниже (FAIL с T5-10).
v1.5.0 (директива автора 2026-11-01, рендер Hana для закрепления):
char-spec — POS каждого слота несёт идентичность ЯВНО (цвет волос /
цвет глаз / кожа / тело, specs/hair-eye-library.json + стемы gates.json);
пропущенный параметр = импровизация рендерера (урок T5-09 P26/P31:
POS без единого тега волос). FAIL с T5-10, исторические партии — WARN-эра;
⚗ НЕ освобождает (идентичность — не предмет эксперимента).
v1.6.0 (ревизия 2026-11-01, docs/THREAD5-REVIEW-2026-11-01.md, слой
«Сразу»): (1.1) NEG-линтер видит якорные стили «X gone / X intact /
X off / X on / X visible» — stem-сверка с POS, паразит без референса —
WARN, намеренный — [NEG-ANCHOR]; (1.2) контргейт header-contract —
отсутствующая декларация шапки (спред/EXP-оверлей/окно/каст/HEAT) =
WARN «проверка пропущена»: молчание шумит; (1.7) спред и каст фильтруют
OC по тегу/имени в скобках (is_oc_slot), не по жанру — миграция
ocClassGate на T5-10 не ломает подсчёты; (1.8) канон-вербатим ОС
(oc-canon.json) выведен из копипаст-WARN, исключения видны в квитанции
(canonExempt). Спеки валидируются tools/validate.py ДО гейтов (1.3);
pre-commit: untracked-квитанции блокируют коммит, special/SO-батчи под
замком, setup.sh ставит хук (1.11).
v1.7.0 (директива роста автора 2026-11-01, чат, «десять инициатив»):
(идея 2) header-contract несёт applyFrom на ключе — декларации
«ГИПОТЕЗА ДВИЖКА» и «ХОДЫ» обязательны с T5-10 (SO-кометы вне —
короткая орбита, движка нет); (идея 3) movesGate — декларация ходов
против specs/moves-ledger.json: M-id вне реестра / отставленный →
WARN, ход в 3 сданных батчах подряд → WARN «износ хода» (standing
не считает износ; отставка — только вердиктом); (идея 1) storyCardsGate —
батч ≥10 без batches/T5-NN/stories.md → WARN «бюджет мысли не
проверяем пост-фактум» (пилот story-cards T5-10).
v1.7.1 (заказ T5-10, чат автора 2026-11-01, вечер): IP-блок темы
расширен (no man's sky / hello games) по образцу T5-09; прямая
директива автора — слова witch/witches и тема-лексика ведьм НЕ БАНИТЬ
(никаких флоров/NEG на тему-слова). Данные-only изменение, гейты
не тронуты — дельта к v1.7.0 ожидается +0.

v1.8.0 (вердикт-директива автора 2026-11-03, «чистка негатива» + формат):
negHygiene — NEG v3 против «горохострелов»: изъятые классы (гениталии,
возраст-стек, solo-хвосты) в NEG ≥T5-12 — WARN; приборных юнитов >2 —
WARN (база держит candle/lamp); цветовые гарды волос — только canon-lock
ОС и ≤2 юнита; семантических гардов > negBase.perSlotGuardsMax — WARN
(«как на войну собрался»); условные гарды (2girls/see-through/wet
clothes) без референса в POS — WARN. formatGate — POS ≥4 семантических
строк (не башенка; строка ≤140 знаков), NEG ≤3 строк: пустые строки не
считаются, WARN с applyFrom 12. Исторические партии не переписываются.

Прогон:
    python3 tools/gates.py batches/T5-08.md \
        --json specs/gate-receipts/2026-10-30-T5-08-v12.json \
        --md batches/T5-08.gate-report.md
"""

import hashlib
import json
import os
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
        self.pos_lines = []
        self.neg_lines = []
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
            cur.pos_lines = [l for l in buf if l]
        elif cur is not None and mode == "neg":
            cur.neg = norm_ws(" ".join(buf))
            cur.neg_lines = [l for l in buf if l]
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


def is_oc_slot(s, oc_names=()):
    """Ревизия 2026-11-01, 1.7: OC опознаётся по тегу/имени в скобках, не по жанру.

    С T5-10 жанр OC-слотов становится EXQUISITE (ocClassGate) — жанровые
    фильтры спреда/каста иначе начнут считать бывшие OC-слоты мейнами.
    """
    tokens = {t.strip() for t in s.paren.split("·")}
    return "OC" in tokens or bool(tokens & {n for n in oc_names if n})


def removed_neg_classes():
    """negBase v3 (gates.json v1.8.0): классы, изъятые из NEG вердиктом
    2026-11-03 («Чистка негатива (частичная)»). Слова остаются флорами POS,
    но NEG их больше не несёт — гейт не должен требовать изъятое."""
    nb = GATES.get("negBase", {})
    out = set()
    for units in nb.get("removedClasses", {}).values():
        out.update(u.lower() for u in units)
    return out


def neg_v3_active(batch_no):
    nb = GATES.get("negBase", {})
    return batch_no >= int(nb.get("applyFrom", 10**9))


def check_floors(slot, fails, batch_no=-1):
    neg = slot.neg.lower()
    skip = removed_neg_classes() if neg_v3_active(batch_no) else set()
    for f in GATES["header"]["hardFloors"]:
        if f.lower() in skip:
            continue
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
        else:
            # Ревизия 2026-11-01, 1.1: якорные стили «X gone / X intact /
            # X off / X on / X visible» — раньше гейтом не видны вообще.
            # Stem-сверка X с POS: якорь без референса — паразит-NEG →
            # WARN; намеренный паразит — пометка [NEG-ANCHOR].
            cfg_a = GATES["neg"]
            mark = cfg_a.get("anchorMark", "[NEG-ANCHOR]")
            probe = re.sub(re.escape(mark), " ", unit, flags=re.I).strip().lower()
            am = re.match(
                r"^(.+?)\s+("
                + "|".join(cfg_a.get("anchorStyles", []))
                + r")$",
                probe,
            )
            if am:
                xstems = set()
                for tw in words(am.group(1)):
                    if tw in STOP or len(tw) < 3:
                        continue
                    xstems |= stem_variants(tw)
                marked = mark.lower() in slot.neg.lower()
                if not (xstems & pos_stems) and not marked:
                    warns.append(
                        (slot.sid, "neg-anchor",
                         f"якорь-юнит «{unit}» ({am.group(2)}) не ссылается ни на "
                         f"один элемент POS — паразит-NEG? намеренный якорь пометь "
                         f"{mark} (ревизия 2026-11-01, 1.1)")
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


def check_neg_hygiene(slot, fails, warns, batch_no=-1, oc_names=()):
    """v1.8.0 — NEG v3 против «горохострелов» (вердикт автора 2026-11-03).
    Изъятые классы / приборы >2 / цветовые гарды волос вне canon-lock ОС /
    гарды > perSlotGuardsMax / условные гарды без референса в POS → WARN."""
    cfg = GATES.get("negBase") or {}
    if not cfg or (0 <= batch_no < cfg.get("applyFrom", 10 ** 9)):
        return
    units = [norm_ws(u) for u in slot.neg.split(",") if norm_ws(u)]
    low = [u.lower() for u in units]
    low_set = set(low)

    for cls, lst in (cfg.get("removedClasses") or {}).items():
        for u in lst:
            if u.lower() in low_set:
                warns.append((slot.sid, "neg-hygiene",
                              f"«{u}» — класс «{cls}» изъят из NEG (negBase v3): "
                              f"никогда не рисовался бы и без нас"))

    base_set = {b.lower() for b in cfg.get("always", [])}
    cond_map = cfg.get("conditional") or {}
    semantic = 0
    for u, ul in zip(units, low):
        if ul in base_set:
            continue
        semantic += 1
        need = cond_map.get(u) or cond_map.get(ul)
        if need and not re.search(need, slot.pos, re.I):
            warns.append((slot.sid, "neg-hygiene",
                          f"гард «{u}» без референса в POS (нужен: {need}) — "
                          f"паразит-NEG (negBase v3, смежно закону №14)"))
    if semantic > cfg.get("perSlotGuardsMax", 4):
        warns.append((slot.sid, "neg-hygiene",
                      f"семантических гардов {semantic} > {cfg.get('perSlotGuardsMax', 4)} — "
                      f"NEG собрался на войну (вердикт 2026-11-03)"))

    dev_words = ("candle", "candles", "candelabra", "lamp", "bulb", "lightbulb",
                 "lantern", "torch", "chandelier", "brazier", "streetlight",
                 "floodlight", "spotlight")
    devs = [u for u in low if u in dev_words]
    if len(devs) > 2:
        warns.append((slot.sid, "neg-hygiene",
                      f"приборных юнитов {len(devs)} > 2 — база v3 держит только candle, lamp "
                      f"(закон света v2: POS без приборов)"))

    hc = [u for u in low if re.search(r"^(?:not\s+)?[a-z\-]+\s+hair$", u)]
    if hc and not is_oc_slot(slot, oc_names):
        warns.append((slot.sid, "neg-hygiene",
                      f"цветовые гарды волос ({', '.join(hc)}) — только canon-lock ОС; "
                      f"у рандомных девиц цвет пишет POS VERBATIM (negBase v3)"))
    elif len(hc) > 2:
        warns.append((slot.sid, "neg-hygiene",
                      f"цветов волос в NEG {len(hc)} > 2 — «несколько цветов волос» "
                      f"лишняя хуйня (вердикт 2026-11-03)"))


def check_format_gate(slot, warns, batch_no=-1):
    """v1.8.0 — формат-гейт «не башенка» (вердикт автора 2026-11-03):
    POS ≥ posMinLines семантических строк, NEG ≤ negMaxLines строк,
    строка ≤ maxLineChars. Пустые строки не считаются."""
    cfg = GATES.get("formatGate") or {}
    if not cfg or (0 <= batch_no < cfg.get("applyFrom", 10 ** 9)):
        return
    mx = cfg.get("maxLineChars", 140)
    pos_lines = [l for l in getattr(slot, "pos_lines", []) if l.strip()]
    if pos_lines:
        if len(pos_lines) < cfg.get("posMinLines", 4):
            warns.append((slot.sid, "format",
                          f"POS собран в {len(pos_lines)} строку(и) — башенка: разбросай "
                          f"по семантическим строкам (≥{cfg.get('posMinLines', 4)})"))
        for l in pos_lines:
            if len(l) > mx:
                warns.append((slot.sid, "format",
                              f"POS-строка {len(l)} знаков > {mx} — башенка, читается "
                              f"по вертикали, а не разом"))
    neg_lines = [l for l in getattr(slot, "neg_lines", []) if l.strip()]
    if neg_lines and len(neg_lines) > cfg.get("negMaxLines", 3):
        warns.append((slot.sid, "format",
                      f"NEG в {len(neg_lines)} строках > {cfg.get('negMaxLines', 3)} — "
                      f"лишние абзацы ни к чему (вердикт 2026-11-03)"))


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


def load_canon_grams():
    """Ревизия 2026-11-01, 1.8: n-граммы канон-вербатима ОС (oc-canon.json).

    Канон ОС повторяется от партии к партии по праву (ЛОКи внешности),
    это не копипаст: 6-граммы из текстовых полей ростера не шумят
    парными и межбатчевыми WARN. FAIL ≥3 слотов каноном не гасится.
    Исключения не молчат: счётчик canonExempt в квитанции.
    """
    rel = GATES["copypaste"].get("canonWhitelist")
    if not rel:
        return frozenset()
    try:
        data = json.loads((ROOT / rel).read_text(encoding="utf-8"))
    except Exception:
        return frozenset()
    n = GATES["copypaste"]["ngramWords"]
    grams = set()

    def collect(o):
        if isinstance(o, str):
            wl = words(o)
            for i in range(len(wl) - n + 1):
                grams.add(" ".join(wl[i: i + n]))
        elif isinstance(o, dict):
            for v in o.values():
                collect(v)
        elif isinstance(o, list):
            for v in o:
                collect(v)

    for oc in (data.get("ocs") or {}).values():
        collect(oc)
    return frozenset(grams)


def check_copypaste(slots, ab_pairs, fails, warns, canon_grams=frozenset()):
    gram_slots = {}
    for s in slots:
        wl = words(strip_boilerplate(s.pos))
        for i in range(len(wl) - GATES["copypaste"]["ngramWords"] + 1):
            g = " ".join(wl[i: i + GATES["copypaste"]["ngramWords"]])
            gram_slots.setdefault(g, set()).add(s.sid)
    fails_seen, warn_pairs, canon_exempt = set(), set(), []
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
            if g in canon_grams:
                canon_exempt.append({"gram": g, "slots": sorted(ids)})
                continue
            warn_pairs.add((tuple(sorted(ids)), g))
    for (a, b), g in sorted(warn_pairs)[:20]:
        warns.append((f"{a}+{b}", "copypaste", f"пара делит n-грамму: «{g}»"))
    return canon_exempt


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


def check_header(text, header, slots, fails, warns, oc_names=()):
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
        # Ревизия 2026-11-01, 1.7: фильтр по is_oc_slot, не по жанру —
        # с T5-10 жанр OC-слотов EXQUISITE и жанровый фильтр ложно считал
        # бы их мейнами.
        mains = [
            s for s in slots
            if s.genre != "EXP" and not is_oc_slot(s, oc_names)
        ]
        rplus = sum(1 for s in mains if s.rating == "R+")
        r = sum(1 for s in mains if s.rating == "R")
        if (rplus, r) != (int(spread.group(1)), int(spread.group(2))):
            warns.append(
                ("BATCH", "header",
                 f"спред шапки R+×{spread.group(1)}·R×{spread.group(2)} ≠ факт R+×{rplus}·R×{r}")
            )
    if GATES["header"]["windowStatement"] and "Окно" not in header:
        warns.append(("BATCH", "header", "в шапке нет заявления окна ротации"))


def check_header_contract(header, warns, batch_no=-1):
    """Ревизия 2026-11-01, 1.2: молчаливая пропускаемость — системный дефект.

    Почти каждая проверка шапки делала «if нет данных: return» — молча.
    Нет спреда → гейт молчит. Нет каста → молчит. Аудитовские находки
    (F5: каст 12 vs 14) ловили люди, потому что машине было «нечего
    сравнивать». Контргейт: обязательная декларация шапки отсутствует →
    WARN «декларация не найдена, проверка пропущена». Молчание шумит.

    v1.7.0 (директива роста 2026-11-01): ключ может нести applyFrom —
    для батчей с номером < applyFrom требование молчит (объявленная
    эра, урок F2 — не переписываем историю задним числом); SO-кометы
    (номер -1) вне prereg движка: короткая орбита, движка нет.
    """
    cfg = GATES.get("headerContract", {})
    if cfg.get("mode") != "warn":
        return
    for req in cfg.get("require", []):
        apply_from = req.get("applyFrom")
        if apply_from and (batch_no < 0 or batch_no < apply_from):
            # v1.7.0: объявленная эра (история не шумит); SO-кометы (-1) вне
            # prereg движка — короткая орбита, движка нет (OVERVIEW «КОМЕТА»)
            continue
        if not re.search(req["pattern"], header):
            warns.append(
                ("BATCH", "header-contract",
                 f"декларация не найдена: {req['label']} — проверка «{req['key']}» "
                 f"пропущена, шапка неполная (ревизия 2026-11-01, 1.2)")
            )


def load_moves_ledger():
    rel = (GATES.get("movesGate") or {}).get("ledger", "specs/moves-ledger.json")
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def check_moves_gate(header, warns, batch_no=-1):
    """Директива роста 2026-11-01, идея 3 («ходы должны умирать»)."""
    cfg = GATES.get("movesGate", {})
    m = re.search(r"^ХОДЫ.*$", header, re.M)
    if not m:
        return  # обязательность декларации — header-contract (с T5-10)
    block = m.group(0)
    declared = sorted(set(re.findall(r"\bM\d{2}\b", block)))
    try:
        ledger = load_moves_ledger()
    except Exception as e:
        warns.append(("BATCH", "moves",
                      f"реестр ходов не читается ({e}) — сверка молчит, молчание шумит"))
        return declared
    moves = {mv.get("id"): mv for mv in ledger.get("moves", [])}
    for mid in declared:
        mv = moves.get(mid)
        if mv is None:
            warns.append(("BATCH", "moves",
                          f"{mid} вне реестра ходов — ход рождается только вердиктом "
                          f"(ARS §6 / LAWS §9); сначала вердикт, потом применение"))
            continue
        if mv.get("retired"):
            warns.append(("BATCH", "moves",
                          f"{mid} в отставке ({mv.get('retired')}) — применение вне закона; "
                          f"вернуть ход может только вердикт"))
        if mv.get("standing") or not mv.get("applications"):
            continue
        nums = sorted({a["no"] for a in mv["applications"] if isinstance(a.get("no"), int)})
        if batch_no >= 1:
            # текущий батч считает своё применение из декларации шапки:
            # реестр обновляется только пост-верdict, ждать записи — значит
            # гейт молчал бы ровно на том батче, где износ уже случился
            streak = 1
            n = batch_no - 1
            while n in nums:
                streak += 1
                n -= 1
            if streak >= int(cfg.get("wearStreak", 3)):
                warns.append(("BATCH", "moves",
                              f"износ хода {mid} «{mv.get('name')}»: применён в {streak} "
                              f"сданных батчах подряд (порог {cfg.get('wearStreak')}) — "
                              f"та же смерть, только на уровне хода; лампа автору, "
                              f"отставка — только вердиктом"))
    return declared


def check_story_cards(batch_path, warns, batch_no=-1):
    """Директива роста 2026-11-01, идея 1 (story-cards, пилот T5-10)."""
    cfg = GATES.get("storyCardsGate", {})
    apply_from = int(cfg.get("applyFrom", 10))
    if batch_no >= 0 and batch_no < apply_from:
        return False
    p = Path(batch_path)
    if not p.is_absolute():
        p = ROOT / p
    cards = p.with_suffix("") / "stories.md"
    if not cards.exists():
        try:
            shown = Path(os.path.relpath(cards, ROOT))
        except ValueError:
            shown = cards
        warns.append(("BATCH", "story-cards",
                      f"{shown} не найден — карточки историй отсутствуют, "
                      f"бюджет мысли не проверяем пост-фактум (директива роста 2026-11-01, "
                      f"идея 1; пилот — мейн-пул)"))
        return False
    return True


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


def check_oc_class_floor(slots, fails, warns, batch_no=-1, oc_names=()):
    """Вердикт T5-09 (2026-11-01, прилавок): OC-промпты — класс EXQUISITE не ниже.

    «Единственное, я бы хотел чтобы ОС промпты были класса Exquisite, не
    меньше, чтобы они прорабатывались очень хорошо и были сильно более
    детализированные». Прямое решение автора в вердикте — FAIL сразу без
    WARN-эры (прецедент ecchi-ключа, T5-05); исторические партии
    (номер < applyFrom) не переписываются (урок F2).
    OC-слот опознаётся по тегу OC в скобках ИЛИ по имени канонной OC в
    скобках — с T5-10 класс EXQUISITE вытесняет OC-тег с первого места
    («(EXQUISITE · Sue · R+…)»). Вето автора — правкой applyFrom/mode.
    """
    cfg = GATES.get("ocClassGate", {})
    if cfg.get("mode") != "fail":
        return
    if cfg.get("applyFrom") and batch_no < cfg["applyFrom"]:
        return
    floor = cfg.get("floor", "EXQUISITE")
    for s in slots:
        if is_oc_slot(s, oc_names) and s.genre != floor:
            fails.append(
                (s.sid, "oc-class-floor",
                 f"OC-слот в классе «{s.genre}» — вердикт T5-09: класс {floor}, "
                 f"не меньше (ультра своего жанра: канон-проработка и детали)")
            )


def _char_spec_stems():
    """Словарь цветовых стемов char-spec: hair-eye-library + дополнения gates.json."""
    cfg = GATES["charSpecGate"]
    data = json.loads(
        (ROOT / cfg["hairEyeRegistry"]).read_text(encoding="utf-8")
    )
    hair = set(data.get("hair", [])) | set(cfg.get("hairColorStems", []))
    eyes = set(data.get("eyes", [])) | set(cfg.get("eyeColorStems", []))
    return hair, eyes


def _stem_alt(stems):
    return "|".join(
        re.escape(s) for s in sorted(stems, key=len, reverse=True)
    )


def _token_has_stem(token, stems):
    t = (token or "").lower()
    return any(s in t for s in stems)


def check_char_spec(slots, fails, warns, batch_no=-1):
    """Директива автора 2026-11-01 (рендер Hana для закрепления, чат):
    «ВЕЗДЕ должно быть указано ВСЁ о персонаже… палитра это епта не
    паннацея, всё надо указывать в позитиве, каждую рисуемую мелочь».

    Гейт char-spec: POS каждого слота несёт идентичность ЯВНО — цвет волос,
    цвет глаз, кожу, тело (список require в gates.json — вето автора правкой
    списка). Пропущенный параметр = импровизация рендерера: урок T5-09
    P26/P31 (EXP) — POS без единого тега волос, NEG запретил только
    blonde/silver/white, рендер вывел цвет из палитры P54_ART_DECO_PLATINUM
    (platinum-silver) → незаписанный блонд, закреплённый автором как канон
    Hana (oc-canon v2.5.0). E3-развязка hair-eye-library подтверждена
    законом: палитра — настроение/свет, hair/eye — идентичность.
    Исторические партии (номер < applyFrom) — WARN-эра, задним числом не
    переписываются (урок F2). ⚗-метка НЕ освобождает: идентичность — не
    предмет эксперимента (в отличие от заявки, check_salience).
    """
    cfg = GATES["charSpecGate"]
    require = set(cfg.get("require", []))
    if not require:
        return
    hair_stems, eye_stems = _char_spec_stems()
    hair_re = re.compile(
        rf"\b(?:{_stem_alt(hair_stems)})[a-z-]*\s+(?:[a-z-]+\s+){{0,2}}hair\b",
        re.I,
    )
    # причёска без слова hair: «choppy black bob», «a choppy black bob»
    hair_style_re = re.compile(
        rf"\b(?:{_stem_alt(hair_stems)})[a-z-]*\s+(?:[a-z-]+\s+){{0,2}}"
        rf"(?:{'|'.join(cfg.get('hairStyleWords', []))})\b",
        re.I,
    )
    eye_pre_re = re.compile(
        rf"\b(?:{_stem_alt(eye_stems)})[a-z-]*\s+(?:[a-z-]+\s+){{0,1}}eyes?\b",
        re.I,
    )
    # цвет ПОСЛЕ слова глаза: «left eye red, right eye blue», face-lock
    # «anime eyes (wine-red, mood)»
    eye_post_re = re.compile(r"\beyes?\b\s*(?:\()?\s*([a-z][a-z-]*)", re.I)
    skin_re = re.compile(r"\bskin\b", re.I)
    body_re = re.compile(
        r"\b(?:build|breasts|body|figure|bust|chest|hips|waist|thighs|fullness|hourglass)\b",
        re.I,
    )
    hair_alt = cfg.get("hairAlt", [])
    skin_alt = cfg.get("skinAlt", [])
    eye_exempt = cfg.get("eyeExempt", [])
    escalated = cfg["mode"] == "fail" and not (
        cfg.get("applyFrom") and batch_no < cfg["applyFrom"]
    )
    sink = fails if escalated else warns
    era = (
        f"FAIL с T5-{cfg.get('applyFrom', '?'):02d}"
        if escalated
        else f"WARN-эра: FAIL с T5-{cfg.get('applyFrom', '?'):02d}"
    )
    for s in slots:
        low = s.pos.lower()
        missing = []
        if "hairColor" in require and not (
            hair_re.search(s.pos)
            or hair_style_re.search(s.pos)
            or any(a in low for a in hair_alt)
        ):
            missing.append("цвет волос")
        if "eyeColor" in require:
            eye_ok = bool(eye_pre_re.search(s.pos)) or any(
                _token_has_stem(m.group(1), eye_stems)
                for m in eye_post_re.finditer(s.pos)
            )
            if not eye_ok and any(a in low for a in eye_exempt):
                eye_ok = True  # глаза не видны: вуаль/повязка
            if not eye_ok:
                missing.append("цвет глаз")
        if "skin" in require and not (
            skin_re.search(s.pos) or any(a in low for a in skin_alt)
        ):
            missing.append("кожа")
        if "body" in require and not body_re.search(s.pos):
            missing.append("тело")
        if missing:
            sink.append(
                (s.sid, "char-spec",
                 f"POS без {', '.join(missing)} — параметр не задан, рендерер "
                 f"импровизирует (F-016, директива «ВЕЗДЕ ВСЁ» 2026-11-01; {era})")
            )


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


def check_race_cast(header, slots, statuses, warns, oc_names=()):
    """Аудит 2026-10-31, §8: каст кинов против races.json и шапки."""
    cfg = GATES["raceCast"]
    # Ревизия 2026-11-01, 1.7: is_oc-фильтр вместо жанрового — миграция
    # ocClassGate (T5-10: жанр OC → EXQUISITE) не разваливает каст.
    mains = [
        s for s in slots
        if s.genre != "EXP" and not is_oc_slot(s, oc_names)
    ]
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


def check_cross_batch(batch_path, slots, warns, canon_grams=frozenset()):
    """Аудит 2026-10-31, F6/рек.4: 6-граммы против двух предыдущих партий.

    Ревизия 2026-11-01, 1.8: канон-вербатим ОС (oc-canon.json) не шумит —
    гасится с прозрачным счётчиком (возврат (shared, canonExempt)).
    """
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
        return [], []
    seen = {}
    for p in prevs:
        _, _, pslots = parse_batch(p)
        for g, ids in pos_grams(pslots).items():
            seen.setdefault(g, (p.name, ids))
    hits = []
    canon_exempt = []
    for g, ids in pos_grams(slots).items():
        if g in seen:
            if g in canon_grams:
                canon_exempt.append({"gram": g, "slotsHere": sorted(ids),
                                     "sourceBatch": seen[g][0]})
                continue
            hits.append((sorted(ids), g, seen[g][0], sorted(seen[g][1])))
    if hits:
        src = ", ".join(sorted({h[2] for h in hits}))
        warns.append(
            ("BATCH", "cross-copypaste",
             f"{len(hits)} общих {GATES['copypaste']['ngramWords']}-грамм с предыдущими партиями ({src}) — межбатчевый копипаст (аудит 2026-10-31, F6); детально в квитанции"))
    return [
        {"gram": g, "slotsHere": a, "sourceBatch": p, "slotsThere": b}
        for a, g, p, b in hits[: cfg["maxListed"]]
    ], canon_exempt[: cfg["maxListed"]]


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
    canon_grams = load_canon_grams()
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
        check_floors(s, fails, batch_no)
        check_neg_linter(s, fails, warns)
        check_neg_hygiene(s, fails, warns, batch_no, oc_names)
        check_format_gate(s, warns, batch_no)
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
    cp_canon_exempt = check_copypaste(slots, ab_pairs, fails, warns, canon_grams)
    check_channels(slots, channels, fails, warns)
    check_header(text, header, slots, fails, warns, oc_names)
    check_header_contract(header, warns, batch_no)
    moves_declared = check_moves_gate(header, warns, batch_no)
    story_cards_ok = check_story_cards(batch_path, warns, batch_no)
    check_pos_floors(slots, text, oc_names, warns)
    check_race_cast(header, slots, race_statuses, warns, oc_names)
    check_slot_format(slots, warns)
    check_oc_class_floor(slots, fails, warns, batch_no, oc_names)
    check_char_spec(slots, fails, warns, batch_no)
    cross_shared, cross_canon_exempt = check_cross_batch(
        batch_path, slots, warns, canon_grams
    )

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
        "crossBatchCanonExempt": cross_canon_exempt,
        "copypasteCanonExempt": cp_canon_exempt,
        "movesDeclared": moves_declared,
        "storyCards": story_cards_ok,
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
