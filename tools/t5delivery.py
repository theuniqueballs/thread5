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
  archived   — файлы в archive/ (прецедент T5-28, 2026-11-25): в конвейере
               не участвует; batches/*.md для записи не требуется

Страж призраков (аудит 5.3 §3.3, волна 0 — решения автора 1–3):
  status печатает ALARM и не молчит, когда жизненный цикл залип:
  (1) ready старше 3 дней (класс T5-28: номер занят, окно/жребий не видят);
  (2) delivered без JSON-вердикта старше 2 дней (класс T5-30, AUDIT-5.4 §1.1:
      вердикт существовал в чате, но формально не существовал нигде);
  (3) hotfix-KPI — сколько квитанций партии датированы ПОЗЖЕ дня вердикта,
      либо в день вердикта при наличии квитанции ДО него: единственная
      честная мера пре-рендерной слепоты (T5-31 ×2: хирургия v2 + горячий
      фикс v3 ПОСЛЕ «муха не еблась» v1).

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

# тикет #1 (2026-11-28, платформенная честность): статус сдачи — первый
# прогон всякого сеанса (AGENTS «Начало сеанса»), обязан жить на Windows:
# cp1251-консоль не роняет печать ×/§/→ на UnicodeEncodeError
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass  # python < 3.7 или экзотика — работаем как работали

ROOT = Path(__file__).resolve().parent.parent
INDEX_PATH = ROOT / "specs" / "delivery-index.json"
BATCH_DIR = ROOT / "batches"

STATUSES = ("draft", "ready", "delivered", "superseded", "archived")
# партия считается сданной, только если статус явно «delivered» (или её нет
# в индексе вовсе — толерантный дефолт для легаси, см. докуиннг выше)
DELIVERED = "delivered"

# ── страж призраков (аудит 5.3, волна 0) ─────────────────────────────
# даты берутся ТОЛЬКО из имён квитанций (specs/gate-receipts/Дата-T5-NN*.json)
# и поля date JSON-вердиктов — mtime не участвует (аудит 2026-10-31, F2)
RECEIPT_RE = re.compile(
    r"^(\d{4}-\d{2}-\d{2})-(T5-\d+R?)(?:-v(\d+))?(?:-[a-z0-9-]+)?\.json$")
# первый JSON-вердикт — T5-27 (LIVING-NOTES: «с 2026-11-21 вердикты
# переходят на JSON-канон»); партии раньше этого номера не алармятся за
# отсутствие вердикта — их вердикты живут в LIVING-NOTES-архивах (MD-эра)
JSON_CANON_FROM = 27
READY_STALE_DAYS = 3    # класс T5-28 (аудит 5.3 §2.1)
VERDICT_STALE_DAYS = 2  # класс T5-30 (AUDIT-5.4 §1.1)


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


def raw_rows():
    """Сырые записи индекса (с note/mode) — для печати archived-пометок.
    Битый индекс громко отказывает — та же дисциплина, что load_index."""
    if not INDEX_PATH.exists():
        return []
    raw = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    rows = raw.get("batches", [])
    for row in rows:
        if not row.get("batch") or row.get("status") not in STATUSES:
            raise SystemExit(
                f"t5delivery: битая запись индекса {row!r} — batch обязателен, "
                f"status ∈ {STATUSES}"
            )
    return rows


def _stem(name):
    """«T5-31» / «batches/T5-31.md» → «T5-31» — один способ нормализации."""
    s = Path(name).name
    return s[: -len(".md")] if s.endswith(".md") else s


def receipt_dates(batch, receipts_dir=None):
    """[(дата 'YYYY-MM-DD', версия vN или 0)] квитанций партии — из ИМЁН
    файлов гейт-квитанций, сортировка по (дата, версия). Диагностические
    без -vN (baseline/ystamp-*) — версия 0. mtime не участвует
    (аудит 2026-10-31, F2); receipts_dir — для тестов."""
    d = Path(receipts_dir) if receipts_dir else ROOT / "specs" / "gate-receipts"
    stem = _stem(batch)
    out = []
    for p in d.glob("*.json"):
        m = RECEIPT_RE.match(p.name)
        if m and m.group(2) == stem:
            out.append((m.group(1), int(m.group(3) or 0)))
    return sorted(out)


def verdict_date(batch, verdicts_dir=None):
    """Дата вердикта партии (verdicts/T5-NN.json, схема t5-verdict/1, поле
    date) или None — честное «недостаточно данных», не ноль."""
    d = Path(verdicts_dir) if verdicts_dir else ROOT / "verdicts"
    p = d / f"{_stem(batch)}.json"
    if not p.exists():
        return None
    try:
        v = json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None
    if v.get("schema") != "t5-verdict/1":
        return None
    return v.get("date") or None


def days_between(date_str, today_str):
    """Целые дни между датами ISO «YYYY-MM-DD» (today − date)."""
    from datetime import date as _d
    return (_d.fromisoformat(today_str) - _d.fromisoformat(date_str)).days


def ghost_alarms(now=None, index_rows=None, receipts_dir=None, verdicts_dir=None):
    """[строки ALARM] — призраки жизненного цикла (аудит 5.3 §3.3).
    (1) ready старше READY_STALE_DAYS дней по новейшей квитанции;
    (2) delivered (эра JSON-канона, ≥ T5-27) без verdicts/*.json старше
        VERDICT_STALE_DAYS дней.
    Все параметры инъекционны — тесты не трогают рабочее дерево.
    Пустая квитанционная эра (до 2026-10-28) не алармит — нечем мерить."""
    today = now or date_today()
    idx = (dict(index_rows) if index_rows is not None else load_index())
    alarms = []
    for stem, status in idx.items():
        rows = receipt_dates(stem, receipts_dir)
        if not rows:
            continue  # до-квитанционная эра — честно нечем мерить
        newest = rows[-1][0]  # [(дата, версия)] → новейшая дата
        age = days_between(newest, today)
        if status == "ready" and age > READY_STALE_DAYS:
            alarms.append(
                f"ПРИЗРАК ready: {stem} — квитанция {newest} ({age} дн назад), "
                f"окно/жребий его не видят; реши судьбу (рендер/архив/суперсид)")
        if (status == "delivered" and age > VERDICT_STALE_DAYS
                and bnum(stem) >= JSON_CANON_FROM
                and verdict_date(stem, verdicts_dir) is None):
            alarms.append(
                f"ВЕРДИКТ-ПРИЗРАК: {stem} — новейшая квитанция {newest} "
                f"({age} дн), JSON-вердикта нет (класс T5-30, AUDIT-5.4 §1.1); "
                f"запиши verdicts/{stem}.json")
    return alarms


def hotfix_kpi(index_rows=None, receipts_dir=None, verdicts_dir=None):
    """[(партия, N)] — после-вердиктные квитанции партии: датированные
    ПОЗЖЕ дня вердикта рендера, либо в день вердикта при наличии квитанции
    ДО него (иначе квитанция дня — обычный сборочный прогон, не хотфикс;
    прецедент T5-29: сборка и вердикт в один день без правок после).
    Единственная честная мера пре-рендерной слепоты конвейера (аудит 5.3
    §2.1: T5-31 ×2 — хирургия v2 + горячий фикс v3 после «муха не еблась»
    v1). Партии без JSON-вердикта НЕ считаются — «недостаточно данных»,
    не ноль."""
    idx = (dict(index_rows) if index_rows is not None else load_index())
    out = []
    for stem, status in idx.items():
        if status != DELIVERED:
            continue
        vd = verdict_date(stem, verdicts_dir)
        if not vd:
            continue
        rows = receipt_dates(stem, receipts_dir)
        had_before = any(d < vd for d, _v in rows)
        n = sum(1 for d, _v in rows if d > vd or (d == vd and had_before))
        if n:
            out.append((stem, n))
    return out


def date_today():
    """Сегодня ISO — отдельная функция, чтобы тесты патчили одну точку."""
    from datetime import date as _d
    return _d.today().isoformat()


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
              f"ready {counts['ready']} · superseded {counts['superseded']} · "
              f"archived {counts['archived']}")
        print(f"— MODE-дисциплина: CLOCK подряд {streak} — {zone}")
        for stem, row in ((r.get("batch"), r) for r in raw_rows()
                          if r.get("status") == "archived"):
            note = (row.get("note") or "").split("; ")[0]
            print(f"— архив: {stem} — файлы в archive/ ({note[:80]}…)")
        alarms = ghost_alarms()
        if alarms:
            print("— ПРИЗРАКИ (жизненный цикл залип, аудит 5.3):")
            for a in alarms:
                print(f"  ⚠ {a}")
        else:
            print("— призраки: 0 (жизненный цикл не залип)")
        kpi = hotfix_kpi()
        total = sum(n for _, n in kpi)
        detail = ", ".join(f"{s} ×{n}" for s, n in kpi) or "—"
        print(f"— hotfix-KPI (квитанции после вердикта рендера): {detail} · "
              f"сумма {total} — пре-рендерная слепота (аудит 5.3 §2.1; "
              f"партии без JSON-вердикта не считаются)")
        return 0
    if argv[:1] == ["validate"]:
        idx = load_index()
        problems = []
        for p in batch_files():
            stem = p.name[: -len(".md")]
            if stem not in idx:
                problems.append(f"нет записи: {stem} (впиши статус в specs/delivery-index.json)")
        for stem, status in idx.items():
            if status == "archived":
                continue  # файлы живут в archive/ (T5-28, аудит 5.3 волна 0)
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
