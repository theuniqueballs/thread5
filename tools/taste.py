#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
THREAD 5 — вкус → план (директива роста автора 2026-11-01, идея 8).

Вердикт говорит «любимые слоты: P16, P20, P22» — и на этом связь
обрывалась. Скрипт читает вербатимы вердиктов и выдаёт ВКУС-БРИФ —
раздел для брифа следующего батча. TASTE.md перестаёт быть мёртвым
архивом: это машинный вход SOL.

Уровень 0 (с 2026-11-21, двойной аудит P1-02): СТРУКТУРИРОВАННЫЕ
вердикты verdicts/T5-NN.json — канонический вход. Парсинг Markdown
(«Сработало»-строки LIVING-NOTES) — фолбэк для батчей без JSON: регексы
чувствительны к оформлению, поэтому новая эра пишет JSON, а LIVING-NOTES
остаётся человекочитаемой сводкой (источник — JSON, не наоборот).

Уровень 1: метаданные вердикт-квитанций (жанр/кин/тир/палитра).
Уровень 2 (после пилота story-cards T5-10): ходы/свидетели/каналы из
карточек историй + разбор нелюбимого.

Прогон:
    python3 tools/taste.py [--depth N] [--out path]
По умолчанию: последние 3 вердикта, вывод в stdout.
"""

import json
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NOTES = ROOT / "docs/LIVING-NOTES.md"
VERDICTS_DIR = ROOT / "verdicts"

GENRES = {"OC", "NICHE", "VOLT", "EXQUISITE", "EXP"}

LOVED_RE = re.compile(
    r"\*\*(?:Сработало|ПРОМОЦИЯ)[^\n]*?P(\d{2,3})\b[^\n]*?\*\*\s*\(([^)]*)\)"
)
SECTION_RE = re.compile(r"^##\s*Вердикт\s+(T5-\d+R?)", re.M)
ENGINE_RE = re.compile(r"##\s*Движок[^\n]*?:\s*(.+)$")


def parse_paren(paren):
    """Мета из скобки квитанции: «NICHE · gargoyle-kin R18 · R · P26_VOID_ECLIPSE»
    или прозой («кандидат «Коко», R27 Cow-kin R+ PL172») — многострочной тоже."""
    meta = {"genre": "", "kin": "", "rating": "", "palette": ""}
    pm = re.search(r"P\d{1,3}_[A-Z0-9_]+", paren)
    if pm:
        meta["palette"] = pm.group(0)
    km = re.search(r"\b([A-Za-z-]+-kin)\b", paren)
    if km:
        meta["kin"] = km.group(1)
    elif re.search(r"\bhuman\b", paren):
        meta["kin"] = "human"
    rm = re.search(r"(?<![A-Za-z0-9])(R\+|PG-13|R)(?![0-9A-Za-z])", paren)
    if rm:
        meta["rating"] = rm.group(1)
    for g in ("EXQUISITE", "NICHE", "VOLT", "OC", "EXP"):
        if re.search(rf"(?<![A-Za-z]){g}(?![a-z])", paren):
            meta["genre"] = g
            break
    return meta


def parse_loved():
    """[(batch, sid, meta_dict)] из структурированных квитанций."""
    text = NOTES.read_text(encoding="utf-8")
    sections = []
    for m in SECTION_RE.finditer(text):
        sections.append((m.start(), m.group(1)))
    out = []
    for i, (pos, batch) in enumerate(sections):
        end = sections[i + 1][0] if i + 1 < len(sections) else len(text)
        chunk = text[pos:end]
        for m in LOVED_RE.finditer(chunk):
            sid, paren = m.group(1), m.group(2)
            out.append((batch, f"P{sid}", parse_paren(paren)))
    return out


def parse_json_verdicts():
    """Уровень 0 (двойной аудит 2026-11-20, P1-02): вердикты в
    структурированной форме verdicts/T5-NN.json — канонический вход,
    не зависящий от оформления Markdown. Возвращает
    ([(batch, sid, meta)], {batch: {json-поля}}).

    Схема t5-verdict/1: loved[] со слотами и метой (genre/kin/rating/
    palette), overall, lessons (В-уроки), hypothesis_hits. Батч с JSON
    полностью заменяет свою Markdown-секцию (двойного счёта нет)."""
    loved, extra = [], {}
    if not VERDICTS_DIR.exists():
        return loved, extra
    for p in sorted(VERDICTS_DIR.glob("T5-*.json")):
        try:
            v = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue  # битый JSON — фолбэк на Markdown той же партии
        batch = v.get("batch") or p.stem
        rows = []
        for row in v.get("loved") or []:
            sid = row.get("slot")
            if not sid:
                continue
            meta = {
                "genre": row.get("genre") or "",
                "kin": row.get("kin") or "",
                "rating": row.get("rating") or "",
                "palette": row.get("palette") or "",
            }
            rows.append((batch, sid, meta))
        loved.extend(rows)
        extra[batch] = {
            "overall": (v.get("overall") or {}).get("score", ""),
            "file": p.name,
            "lessons": len(v.get("lessons") or []),
            "ok_with_issues": len(v.get("ok_with_issues") or []),
            "loved_count": len(rows),
        }
    return loved, extra


def engines_for(batches):
    """{batch: имя движка} из 01-sol артефактов."""
    out = {}
    for b in batches:
        sol = ROOT / "batches" / b / "01-sol.md"
        if not sol.exists():
            continue
        for ln in sol.read_text(encoding="utf-8").splitlines():
            em = ENGINE_RE.search(ln)
            if em:
                out[b] = em.group(1).strip().strip("*")
                break
    return out


def take_recent(batches, depth):
    """Последние `depth` вердикт-секций (2026-11-20: исправлена инверсия —
    раньше брались ПЕРВЫЕ секции LIVING-NOTES, т.е. самые старые вердикты,
    и свежайший вкус автора в бриф не попадал)."""
    if depth <= 0:
        return []
    return batches[-depth:]


def brief(depth=3, out_path=None):
    # уровень 0: структурированные JSON-вердикты — канон (P1-02);
    # Markdown «Сработало» — фолбэк для батчей без JSON (без двойного счёта:
    # батч с JSON исключается из MD-выборки целиком)
    json_loved, json_extra = parse_json_verdicts()
    json_batches = {b for b, *_ in json_loved} | set(json_extra)
    md_loved = [(b, s, m) for b, s, m in parse_loved() if b not in json_batches]
    loved_all = md_loved + json_loved

    batches = []
    for b, *_ in loved_all:
        if b not in batches:
            batches.append(b)
    recent = take_recent(batches, depth)
    loved = [(b, s, m) for b, s, m in loved_all if b in recent]

    if not loved:
        print("ВКУС-БРИФ: вердиктов не найдено (ни JSON, ни «Сработало»-квитанций)")
        return 1

    engines = engines_for(recent)
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")

    json_in_window = [b for b in recent if b in json_extra]
    src_line = (
        f"verdicts/*.json ({', '.join(json_in_window)})" if json_in_window else "—"
    )

    lines = [
        "# ВКУС-БРИФ (tools/taste.py v1.1.0) — машинный вход SOL",
        "",
        f"- сгенерирован: {now}",
        f"- источник-канон: verdicts/T5-NN.json (схема t5-verdict/1): {src_line}",
        f"- фолбэк: docs/LIVING-NOTES.md «Сработало»-квитанции (батчи без JSON)",
        f"- глубина: {depth} вердиктов ({', '.join(recent)}) · любимых слотов: {len(loved)}",
        "",
        "## Любимое автора — подтверждено вердиктами",
        "",
        "| Слот | Батч | Жанр | Кин | Тир | Палитра | Движок батча |",
        "|---|---|---|---|---|---|---|",
    ]
    for b, s, m in loved:
        lines.append(
            f"| {s} | {b} | {m['genre'] or '—'} | {m['kin'] or '—'} | "
            f"{m['rating'] or '—'} | {m['palette'] or '—'} | {engines.get(b, '—')} |"
        )

    def counter(field):
        c = Counter(m[field] for _, _, m in loved if m[field])
        return ", ".join(f"{k} ×{v}" for k, v in c.most_common()) or "—"

    eng_c = Counter(engines.get(b, "—") for b, _, _ in loved)
    eng_s = ", ".join(f"«{k}» ×{v}" for k, v in eng_c.most_common() if k != "—")

    lines += [
        "",
        "## Паттерны (что любит автор — данные, не вайб)",
        "",
        f"- жанры: {counter('genre')}",
        f"- кины: {counter('kin')}",
        f"- тиры: {counter('rating')} — низкий тир любим, когда история держит (VOLT-урок T5-06)",
        f"- палитры любимых слотов: {counter('palette')}",
        f"- движки любимых слотов: {eng_s}",
        "",
        "## Итоговые оценки партий (JSON-вердикты)",
        "",
    ]
    for b in recent:
        if b in json_extra:
            e = json_extra[b]
            lines.append(
                f"- {b}: {e['overall'] or '—'} · любимых {e['loved_count']} · "
                f"уроков {e['lessons']} · с-оговорками {e['ok_with_issues']} ({e['file']})"
            )
    lines += [
        "",
        "## Как пользоваться SOL",
        "",
        "- следующий движок ищи на пересечении паттернов выше и темы автора;",
        "- повтор любимого движка в лоб = износ (movesGate WARN, specs/moves-ledger.json) — вариация, не копия;",
        "- тиры не молоти в R+: любимые R/PG-13 держала история, не эротика;",
        "- уровень 2 (ходы/свидетели/каналы из карточек, разбор нелюбимого) — после пилота story-cards T5-10;",
        "- вердикты — единственный источник правды: новые партии пишутся в verdicts/T5-NN.json (JSON-канон), LIVING-NOTES — человекочитаемая сводка.",
    ]

    text = "\n".join(lines) + "\n"
    if out_path:
        Path(out_path).write_text(text, encoding="utf-8")
        print(f"ВКУС-БРИФ: записан {out_path}")
    else:
        print(text)
    return 0


def _arg_value(argv, flag, default=None, cast=str):
    """2026-11-20: значение флага без IndexError/ValueError."""
    if flag not in argv:
        return default
    i = argv.index(flag)
    if i + 1 >= len(argv) or argv[i + 1].startswith("--"):
        print(f"taste: флаг {flag} требует значение")
        sys.exit(2)
    try:
        return cast(argv[i + 1])
    except (TypeError, ValueError):
        print(f"taste: не поняла значение {flag}={argv[i + 1]!r}")
        sys.exit(2)


def main():
    argv = sys.argv[1:]
    depth = _arg_value(argv, "--depth", default=3, cast=int)
    out_path = _arg_value(argv, "--out", default=None, cast=str)
    sys.exit(brief(depth=depth, out_path=out_path))


if __name__ == "__main__":
    main()
