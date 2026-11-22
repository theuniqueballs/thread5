#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
THREAD 5 — ЕДИНЫЙ МОДУЛЬ СДАЧИ ПАРТИЙ (delivery index).

Аудит 2026-11-20 (двойной: Коула/Grok §6.3 + внешний архитектурный P0-06):
«кто двигает окно — тот один модуль; остальные читают квитанцию». До этого
три инструмента держали по три своих копии «какие партии считать сданными»:
  gates.py::load_prev_y_usage / check_cross_batch  — glob T5-*.md по-своему
  window.py::delivered_batches                     — glob по-своему
  oracle.py::corpus_batches                        — glob по-своему
  CI: ls batches/T5-*.md | sort -V | tail -1       — четвёртая копия
Черновик T5-28, положенный в папку, молча лез в окно ротации, жребий и
гейты ДО сдачи. Теперь статус партии живёт в specs/delivery-index.json,
и все читают его отсюда.

Статусы:
  draft      — черновик: в окно/жребий/CI НЕ попадает
  ready      — собран, гейты пройдены, ждёт сдачи: в окно НЕ попадает
  delivered  — сдан: единственный статус, который видит окно ротации
  superseded — заменён реворком (T5-05R накрыл T5-05): окном не считается

Правило толерантности: файл без записи в индексе считается «delivered»
(исторические партии все сданы; индекс нужен, чтобы помечать НЕсданное).
Валидатор (проверка №12) требует явной записи для каждого T5-*.md —
нельзя молча положить черновик мимо индекса.

CLI:
    python3 tools/t5delivery.py latest      # путь свежайшей сданной (для CI)
    python3 tools/t5delivery.py status      # таблица статусов
    python3 tools/t5delivery.py validate    # 0/1 — индекс согласован с папкой
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX_PATH = ROOT / "specs" / "delivery-index.json"
BATCH_DIR = ROOT / "batches"

STATUSES = ("draft", "ready", "delivered", "superseded")
# партия считается сданной, только если статус явно «delivered» (или её нет
# в индексе вовсе — толерантный дефолт для легаси, см. докуиннг выше)
DELIVERED = "delivered"


def bnum(p):
    """Номер партии из имени файла («T5-09.md» → 9; нет кода → -1).
    Тот же смысл, что gates.batch_number / window.bnum — одна арифметика
    на все инструменты, чтобы номера нигде не разъехались."""
    m = re.search(r"T5-(\d+)", Path(p).name)
    return int(m.group(1)) if m else -1


def load_index():
    """{(stem без .md): статус}. Битый индекс — громкий отказ, не молчание.

    2026-11-23 (Коул §4/§11.3 «MODE counters»): в записи может жить поле
    mode (CLOCK/LAB/SURGERY/SPECIAL — из брифа партии; у старых партий
    его нет, история не переписывается). Статусная карта его игнорирует,
    для счётчика дисциплины есть mode_of()."""
    if not INDEX_PATH.exists():
        return {}
    try:
        raw = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    except Exception as e:
        raise SystemExit(f"t5delivery: specs/delivery-index.json не читается — {e}")
    out = {}
    for row in raw.get("batches", []):
        name, status = row.get("batch"), row.get("status")
        if not name or status not in STATUSES:
            raise SystemExit(
                f"t5delivery: битая запись индекса {row!r} — batch обязателен, "
                f"status ∈ {STATUSES}"
            )
        out[name] = status
    return out


MODES = ("CLOCK", "LAB", "SURGERY", "SPECIAL")


def mode_rows():
    """[(batch, mode)] записей с полем mode — от старых к новым.
    Битое значение mode — громкий отказ (мусор в индексе не молчит)."""
    if not INDEX_PATH.exists():
        return []
    raw = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    rows = []
    for row in raw.get("batches", []):
        if "mode" in row and row.get("batch"):
            if row["mode"] not in MODES:
                raise SystemExit(
                    f"t5delivery: битый mode в записи {row.get('batch')!r}: "
                    f"{row['mode']!r} ∈ {MODES}"
                )
            rows.append((row["batch"], row["mode"]))
    return rows


def clock_streak():
    """Сколько CLOCK подряд от новейшей записи с mode (Коул §4: 2+ LAB
    подряд без приказа автора = нарушение CLOCK-дисциплины; счётчик —
    метрика здоровья №5/№6)."""
    streak = 0
    for _batch, mode in reversed(mode_rows()):
        if mode == "CLOCK":
            streak += 1
        else:
            break
    return streak


def batch_files(batch_dir=None):
    """Все файлы партий (без gate-report) — [(no, path)].
    batch_dir переопределяется вызывающими (окно/гейты патчат ROOT в
    тестах) — единая арифметика, разные корни."""
    root = Path(batch_dir) if batch_dir is not None else BATCH_DIR
    files = [
        p for p in root.glob("T5-*.md")
        if not p.name.endswith(".gate-report.md")
    ]
    return sorted(files, key=lambda p: (bnum(p), p.name))


def status_of(name_or_path):
    """Статус партии: индекс → толерантный дефолт «delivered»."""
    key = Path(name_or_path).name
    if key.endswith(".md"):
        key = key[: -len(".md")]
    return load_index().get(key, DELIVERED)


def delivered_batches(batch_dir=None):
    """[(no, path)] СДАННЫХ партий по номеру — единственный вход окна
    ротации, жребия и CI. mtime не участвует (аудит 2026-10-31, F2).
    batch_dir — опциональный корень (тесты окна/гейтов патчат ROOT)."""
    idx = load_index()
    return [
        (bnum(p), p)
        for p in batch_files(batch_dir)
        if idx.get(p.name[: -len(".md")], DELIVERED) == DELIVERED
    ]


def latest(batch_dir=None):
    """Путь свежайшей сданной партии (для CI: замена ls|sort|tail)."""
    rows = delivered_batches(batch_dir)
    return rows[-1][1] if rows else None


def _cmd(argv):
    if argv[:1] == ["latest"]:
        p = latest()
        if p is None:
            print("нет сданных партий")
            return 1
        print(p.relative_to(ROOT))
        return 0
    if argv[:1] == ["status"]:
        idx = load_index()
        modes = dict(mode_rows())
        rows = batch_files()
        counts = {s: 0 for s in STATUSES}
        for p in rows:
            counts[idx.get(p.name[: -len(".md")], DELIVERED)] += 1
        for p in rows:
            stem = p.name[: -len(".md")]
            mode = f" · {modes[stem]}" if stem in modes else ""
            print(f"{stem:<12} {idx.get(stem, DELIVERED + ' (нет записи)')}{mode}")
        streak = clock_streak()
        zone = ("зелёная зона (≥2 — цех в часах, Коул §13)" if streak >= 2
                else "меньше 2 — метрика здоровья хромает")
        print(f"— delivered {counts['delivered']} · draft {counts['draft']} · "
              f"ready {counts['ready']} · superseded {counts['superseded']}")
        print(f"— MODE-дисциплина: CLOCK подряд {streak} — {zone}")
        return 0
    if argv[:1] == ["validate"]:
        idx = load_index()
        problems = []
        for p in batch_files():
            stem = p.name[: -len(".md")]
            if stem not in idx:
                problems.append(f"нет записи: {stem} (впиши статус в specs/delivery-index.json)")
        for stem in idx:
            if not (BATCH_DIR / f"{stem}.md").exists():
                problems.append(f"запись без файла: {stem}.md не найден")
        if problems:
            print("delivery-index: FAIL")
            for x in problems:
                print(f"  ✗ {x}")
            return 1
        print(f"delivery-index: PASS ({len(idx)} партий)")
        return 0
    print(__doc__)
    return 0 if argv[:1] in (["-h"], ["--help"], []) else 2


if __name__ == "__main__":
    sys.exit(_cmd(sys.argv[1:]))
