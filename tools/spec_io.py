#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
THREAD 5 — ЕДИНЫЙ КАНОН СЕРИАЛИЗАЦИИ СПЕК (тикет #4, 2026-11-28).

Прецедент: волна 1в (492aa10) — дифф specs/rating-techniques.json 7162
строки, из них 67 контента (volt_run-блок); 7 100 строк — реформат отступов
всего файла, вмонтрованный в фичевый коммит. Ревью содержимого невозможно,
реверт фичи тянет реформат, blame спеки обесценен.

Закон (AGENTS «Запрещено», №9): спеки/JSON не реформатятся в фичевых
коммитах; смена форматирования — отдельный коммит «format:» с нулевым
контент-диффом (git show -w пуст). Этот модуль — исполнение второй половины
закона: все скрипты, пишущие specs/*.json, идут через dump_spec() —
один канон (ensure_ascii=False, trailing newline, LF), следующий дифф
спеки содержит только содержимое.

Формат-паспорт живых машинных файлов (indent): большинство реестров
печи — indent 1; ручные справочники (gates/closet/oc-canon/…) — indent 2.
Паспорт — данные, не разветвлённые конфиги: менять только format:-коммитом.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# один канон для всех писателей спек
ENSURE_ASCII = False
TRAILING_NEWLINE = True
INDENT_DEFAULT = 1

# формат-паспорт машинных specs-файлов (round-trip проверяется тестом
# test_spec_io на живом дереве): файл → indent. Файл вне паспорта пишется
# INDENT_DEFAULT; ручные справочники сюда не входят — их пишет человек.
SPEC_INDENT = {
    "specs/camera.json": 1,
    "specs/gate-registry.json": 1,
    "specs/palettes.json": 1,
    "specs/y-trust.json": 1,
    "specs/delivery-index.json": 1,
    "specs/delivery-stats.json": 1,
    "specs/dresser.json": 1,
    "specs/oc-candidates.json": 1,
    "specs/races.json": 1,
    "specs/furnace-ledger.json": 1,
    "specs/open-hypotheses.json": 1,
    "specs/pregarerobe/_ledger.json": 1,
    "specs/gate-receipts/*.json": 1,
    # тикет #6: gates.json — ручной справочник на indent 2; без паспорта
    # dump_spec без явного indent чуть не переформатировал его в 1 (класс
    # волны 1в / тикета #4 — пойман живым прогоном правки claimFact)
    "specs/gates.json": 2,
}


def dump_spec(path, data, indent: int | None = None) -> None:
    """Единственная легальная запись specs/*.json скриптами цеха.

    Канон: json.dumps(ensure_ascii=ENSURE_ASCII, indent=…, sort_keys=False)
    + trailing newline. indent = аргумент → паспорт файла → INDENT_DEFAULT.
    Выравнивание концов строк — LF (репо-канон, .gitattributes).
    """
    p = Path(path)
    if indent is None:
        rel = None
        try:
            rel = p.resolve().relative_to(ROOT).as_posix()
        except ValueError:
            rel = p.as_posix()
        indent = SPEC_INDENT.get(rel)
        if indent is None:
            import fnmatch
            for pat, ind in SPEC_INDENT.items():
                if "*" in pat and fnmatch.fnmatch(rel, pat):
                    indent = ind
                    break
        if indent is None:
            indent = INDENT_DEFAULT
    text = json.dumps(data, ensure_ascii=ENSURE_ASCII, indent=indent)
    if TRAILING_NEWLINE:
        text += "\n"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8", newline="\n")


def spec_roundtrip_ok(path) -> bool:
    """Файл уже лежит в каноне: повторная dump_spec не меняет ни байта.
    Гарантия «следующий дифф — только содержимое» (тикет #4, приёмка п.2)."""
    p = Path(path)
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return False
    rel = None
    try:
        rel = p.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        rel = p.as_posix()
    import fnmatch
    indent = SPEC_INDENT.get(rel)
    if indent is None:
        for pat, ind in SPEC_INDENT.items():
            if "*" in pat and fnmatch.fnmatch(rel, pat):
                indent = ind
                break
    if indent is None:
        indent = INDENT_DEFAULT
    canon = json.dumps(data, ensure_ascii=ENSURE_ASCII, indent=indent)
    if TRAILING_NEWLINE:
        canon += "\n"
    return p.read_text(encoding="utf-8") == canon
