#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
THREAD 5 — вкус → план (директива роста автора 2026-11-01, идея 8).

Вердикт говорит «любимые слоты: P16, P20, P22» — и на этом связь
обрывалась. Скрипт читает вердикт-квитанции (структурированные
«Сработало»-строки LIVING-NOTES), сопоставляет с метаданными слотов
(жанр/кин/тир/палитра) и движками батчей (01-sol), агрегирует паттерны
вкуса и выдаёт ВКУС-БРИФ — раздел для брифа следующего батча.
TASTE.md перестаёт быть мёртвым архивом: это машинный вход SOL.

Уровень 1 (этот скрипт): метаданные вердикт-квитанций.
Уровень 2 (после пилота story-cards T5-10): ходы/свидетели/каналы из
карточек историй + разбор нелюбимого (вербатимы разнородны для машины).

Прогон:
    python3 tools/taste.py [--depth N] [--out path]
По умолчанию: последние 3 вердикт-секции, вывод в stdout.
"""

import json
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NOTES = ROOT / "docs/LIVING-NOTES.md"

GENRES = {"OC", "NICHE", "VOLT", "EXQUISITE", "EXP"}

LOVED_RE = re.compile(
    r"\*\*(?:Сработало|ПРОМОЦИЯ)[^\n]*?P(\d{2})[^\n]*?\*\*\s*\(([^)]*)\)"
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


def brief(depth=3, out_path=None):
    loved_all = parse_loved()
    batches = []
    for b, *_ in loved_all:
        if b not in batches:
            batches.append(b)
    recent = batches[:depth]
    loved = [(b, s, m) for b, s, m in loved_all if b in recent]

    if not loved:
        print("ВКУС-БРИФ: структурированных «Сработало»-квитанций не найдено")
        return 1

    engines = engines_for(recent)
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")

    lines = [
        "# ВКУС-БРИФ (tools/taste.py v1.0.0) — машинный вход SOL",
        "",
        f"- сгенерирован: {now}",
        f"- источник: docs/LIVING-NOTES.md (структурированные «Сработало»-квитанции)",
        f"- глубина: {depth} вердикт-секций ({', '.join(recent)}) · любимых слотов: {len(loved)}",
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
        "## Как пользоваться SOL",
        "",
        "- следующий движок ищи на пересечении паттернов выше и темы автора;",
        "- повтор любимого движка в лоб = износ (movesGate WARN, specs/moves-ledger.json) — вариация, не копия;",
        "- тиры не молоти в R+: любимые R/PG-13 держала история, не эротика;",
        "- уровень 2 (ходы/свидетели/каналы из карточек, разбор нелюбимого) — после пилота story-cards T5-10;",
        "- вердикты — единственный источник правды: секции без структурированных квитанций в статистику не попали.",
    ]

    text = "\n".join(lines) + "\n"
    if out_path:
        Path(out_path).write_text(text, encoding="utf-8")
        print(f"ВКУС-БРИФ: записан {out_path}")
    else:
        print(text)
    return 0


def main():
    depth = 3
    if "--depth" in sys.argv:
        depth = int(sys.argv[sys.argv.index("--depth") + 1])
    out_path = None
    if "--out" in sys.argv:
        out_path = sys.argv[sys.argv.index("--out") + 1]
    sys.exit(brief(depth=depth, out_path=out_path))


if __name__ == "__main__":
    main()
