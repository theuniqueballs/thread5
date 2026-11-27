#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
THREAD 5 — ГИГИЕНА КОММИТОВ СПЕК (тикет #4, 2026-11-28): инструментальная
ловушка класса «full-file реформат в фичевом коммите».

Прецедент: волна 1в (492aa10) — specs/rating-techniques.json, полный дифф
7162 строки, дифф без пробелов (git show -w) — 67 строк: 7 100 строк
реформата отступов вмонтрованы в фичевый коммит. Ревью содержимого убито,
реверт фичи тянет реформат, blame обесценен. Ручная честность («я больше
не буду») — не ловушка; ловушка — числа.

Режимы:
    python3 tools/commit_hygiene.py              # последний коммит, тронувший specs/
    python3 tools/commit_hygiene.py --sha <hash> # конкретный коммит
    python3 tools/commit_hygiene.py --staged     # индекс (pre-commit): закешированное

Метод: полный stat (вставки+удаления по specs/*.json) против stat -w
(то же без пробельных изменений). Расхождение > CHURN_RATIO (5×) — WARN:
коммит несёт реформат, а не только контент. Отдельные вставки/удаления
после -w не штрафуются (контент обязан меняться); штраф — когда пробельный
шум кратно больше контента.

Выход: 0 = чисто · 1 = WARN (реформат-чурн) · 2 = битый вызов.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# тикет #4: расхождение >5× = WARN
CHURN_RATIO = 5.0
SPECS_PREFIX = "specs/"


def _git(*args: str, repo=None) -> str:
    proc = subprocess.run(
        ["git", "-C", str(repo or ROOT), *args],
        capture_output=True, text=True, timeout=60,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or f"git {' '.join(args)} → {proc.returncode}")
    return proc.stdout


def _numstat(diff_args: list[str], repo=None) -> dict[str, tuple[int, int]]:
    """Путь → (вставки, удаления) по specs/*.json; «-» (бинарник) → 0/0."""
    out = _git("diff", "--numstat", *diff_args, repo=repo)
    stats: dict[str, tuple[int, int]] = {}
    for line in out.splitlines():
        parts = line.split("\t")
        if len(parts) != 3:
            continue
        adds, dels, path = parts
        if not path.startswith(SPECS_PREFIX) or not path.endswith(".json"):
            continue
        a = int(adds) if adds.isdigit() else 0
        d = int(dels) if dels.isdigit() else 0
        if a or d:
            stats[path] = (a, d)
    return stats


def audit(specs_full: dict, specs_w: dict) -> list[str]:
    """Список WARN-строк: файлы, где пробельный чурн кратно больше контента."""
    warns = []
    for path, (full_a, full_d) in sorted(specs_full.items()):
        w_a, w_d = specs_w.get(path, (0, 0))
        full_total = full_a + full_d
        w_total = w_a + w_d
        if not full_total or not w_total:
            # нет контент-диффа — это format:-коммит (легален по закону №9,
            # отдельным коммитом с пометкой); ловим только смешение
            continue
        noise = full_total - w_total
        if noise / w_total > CHURN_RATIO:
            warns.append(
                f"{path}: дифф {full_total} строк, из них контент (git -w) "
                f"{w_total} — пробельный чурн ×{noise / w_total:.1f} > {CHURN_RATIO:g} "
                f"(тикет #4: реформат — отдельным коммитом «format:», "
                f"сериализация — tools/spec_io.py)"
            )
    return warns


def main() -> int:
    argv = sys.argv[1:]
    if argv[:1] in (["-h"], ["--help"]):
        print(__doc__)
        return 0
    if "--sha" in argv:
        i = argv.index("--sha")
        if i + 1 >= len(argv):
            print("commit_hygiene: --sha требует значение (hash)")
            return 2
        sha = argv[i + 1]
        base = f"{sha}^" if not sha.endswith("^") else sha
        specs_full = _numstat([base, sha])
        specs_w = _numstat(["-w", base, sha])
        label = sha
    elif "--staged" in argv:
        specs_full = _numstat(["--cached"])
        specs_w = _numstat(["--cached", "-w"])
        label = "индекс (staged)"
    else:
        # последний коммит, тронувший specs/ (приёмка тикета п.3)
        log = _git("log", "-1", "--format=%H", "--", SPECS_PREFIX).strip()
        if not log:
            print("commit_hygiene: коммитов, тронувших specs/, нет — чисто")
            return 0
        sha = log
        specs_full = _numstat([f"{sha}^", sha])
        specs_w = _numstat(["-w", f"{sha}^", sha])
        label = sha[:12]

    if not specs_full:
        print(f"commit_hygiene: {label} — specs/*.json не тронуты, чисто")
        return 0
    warns = audit(specs_full, specs_w)
    full_total = sum(a + d for a, d in specs_full.values())
    print(
        f"commit_hygiene: {label} · specs-дифф {full_total} строк"
        + (f" · WARN {len(warns)}" if warns else " · чисто")
    )
    if warns:
        for w in warns:
            print(f"  ⚠ {w}")
        return 1
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except RuntimeError as exc:
        print(f"commit_hygiene: git недоступен или репо битое — {exc}")
        sys.exit(2)
