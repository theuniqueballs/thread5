#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
THREAD 5 — СТАНЦИЯ ОКНА (tool планетарного конвейера v2, docs/ars/).

Считает окно ротации один раз за батч: позы, палитры, кинетики, носители,
каналы последних N сданных батчей + актив burn-реестра. Квитанция станции
вписывается в бортовой журнал батча (batches/T5-NN/00-brief.md) и читается
SOL / MERCURY / VENUS — вместо ручного перечитывания батчей на каждом
сеансе (удобство против забывания, директива автора 2026-10-28).

Прогон:
    python3 tools/window.py                    # окно глубиной 3, в stdout
    python3 tools/window.py --depth 3 --out batches/T5-NN/window.md
    python3 tools/window.py --for T5-06 --out batches/T5-06/window.md
    # --for: окно ИМЕННО для названной партии (по номеру, не по mtime) —
    # добор пропущенных квитанций задним числом (аудит 2026-10-31, F2)
"""

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

from gates import parse_batch, load_oc_names, is_oc_slot  # noqa: E402  (общий парсер слотов)
import t5delivery  # noqa: E402  (единый индекс сдачи — аудит 2026-11-20 P0-06)

BATCH_DIR = ROOT / "batches"
BURNED = json.loads((ROOT / "specs/burned.json").read_text(encoding="utf-8"))


def bnum(p):
    """Номер партии из имени файла («T5-09.md» → 9; нет кода → -1)."""
    return t5delivery.bnum(p)


def delivered_batches():
    """Сданные батчи T5-*.md, свежие первыми.
    2026-11-20: сортировка по НОМЕРУ партии (mtime — только тай-брейк):
    mtime врёт после правок старых файлов (аудит 2026-10-31, F2).
    2026-11-21: единственный источник «кто сдан» — t5delivery (индекс
    specs/delivery-index.json: черновик/ready не лезут в окно; двойной
    аудит 2026-11-20, Коул §6.3 + P0-06)."""
    rows = t5delivery.delivered_batches(batch_dir=BATCH_DIR)
    return sorted(
        (p for _no, p in rows),
        key=lambda p: (bnum(p), p.stat().st_mtime),
        reverse=True,
    )


def _body_ycard(body_lines, y_body_re):
    """Карта из цитаты в теле слота (ретро-батчи до поля Y-card:).
    2026-11-20: без морского волчка — честный цикл, регекс один раз на строку."""
    for b in body_lines:
        m = y_body_re.search(b)
        if m:
            return m.group(0)[:-1].strip()
    return None


def collect(paths):
    """По батчу: заголовок + агрегаты. По системе: множества окна.
    2026-11-21 (аудит Коула R6 + вердикт T5-24 «дрифт и частая ротация
    одних OC»): собираем и OC-состав — машинное OC-окно вместо «как
    вспомнил» (is_oc_slot из gates — тот же детект, что у гейтов)."""
    oc_names = load_oc_names()
    per_batch, agg = [], {
        "pose": set(), "palette": set(), "kinetics": set(),
        "carriers": set(), "channels": set(), "ratings": {},
        "ycards": set(),  # v1.12.0 Y-first: окно Y-карт
        "ocs": set(),    # 2026-11-21: OC-окно (аудит Коула R6)
    }
    y_body_re = re.compile(r"\bY\d{1,3}\b\s*[«\"]")  # карта в теле слота; серия до Y521+
    for p in paths:
        _, _, slots = parse_batch(p)
        batch_ocs = set()
        for s in slots:
            if is_oc_slot(s, oc_names):
                tokens = {t.strip() for t in s.paren.split("·")}
                hit = next((n for n in tokens if n in oc_names), None)
                if hit:
                    batch_ocs.add(hit)
        batch = {
            "file": p.name,
            "slots": len(slots),
            "pose": sorted({s.pose for s in slots if s.pose}),
            "palette": sorted({s.palette for s in slots if s.palette}),
            "kinetics": sorted({k for s in slots for k in s.kinetics}),
            "carriers": sorted({c for s in slots for c in s.carriers}),
            "channels": sorted({s.channel for s in slots if s.channel}),
            "ratings": {},
            # v1.12.0: карта из шапки/поля Y-card: или из цитаты в теле (ретро-батчи)
            "ycards": sorted(
                {
                    y
                    for s in slots
                    for y in [s.y_card or _body_ycard(s.body_lines, y_body_re)]
                    if y
                }
            ),
            "ocs": sorted(batch_ocs),
        }
        for s in slots:
            if s.rating:
                batch["ratings"][s.rating] = batch["ratings"].get(s.rating, 0) + 1
        for key in ("pose", "palette", "kinetics", "carriers", "channels", "ycards", "ocs"):
            agg[key] |= set(batch[key])
        for r, n in batch["ratings"].items():
            agg["ratings"][r] = agg["ratings"].get(r, 0) + n
        per_batch.append(batch)
    return per_batch, agg


def burned_lines():
    out = []
    for e in BURNED.get("entries", []):
        out.append(
            f"- [{e.get('class','?')}] `{e.get('code','?')}` — {e.get('name','')}"
        )
    return out


def receipt_md(per_batch, agg, depth):
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    lines = [
        "# Квитанция СТАНЦИИ ОКНА",
        "",
        f"- Прогон: {now} · tools/window.py · глубина окна: {depth}",
        "- Окно = последние сданные батчи: позы/палитры/кинетики/Y-карты окна НЕ",
        "  повторяются в новом батче (LAWS §7, y_assembly.window). Burn-актив не",
        "  назначается никогда, кроме ⚗ с явной гипотезой (law burned.json).",
        "",
    ]
    for b in per_batch:
        r = " · ".join(f"{k}×{v}" for k, v in sorted(b["ratings"].items()))
        lines.append(f"## {b['file']} — {b['slots']} слотов ({r})")
        lines.append(f"- позы: {', '.join(b['pose']) or '—'}")
        lines.append(f"- палитры: {', '.join(b['palette']) or '—'}")
        lines.append(f"- кинетики: {', '.join(b['kinetics']) or '—'}")
        lines.append(f"- носители: {', '.join(b['carriers']) or '—'}")
        lines.append(f"- каналы: {', '.join(b['channels']) or '—'}")
        lines.append(f"- Y-карты (Y-first, camera.json): {', '.join(b['ycards']) or '—'}")
        lines.append(f"- OC-состав: {', '.join(b['ocs']) or '—'}")
        lines.append("")
    lines.append("## ЗАПРЕТ ОКНА (агрегат — не назначать)")
    lines.append(f"- позы ({len(agg['pose'])}): {', '.join(sorted(agg['pose'])) or '—'}")
    lines.append(f"- палитры ({len(agg['palette'])}): {', '.join(sorted(agg['palette'])) or '—'}")
    lines.append(f"- кинетики ({len(agg['kinetics'])}): {', '.join(sorted(agg['kinetics'])) or '—'}")
    lines.append(f"- носители ({len(agg['carriers'])}): {', '.join(sorted(agg['carriers'])) or '—'}")
    lines.append(f"- каналы ({len(agg['channels'])}): {', '.join(sorted(agg['channels'])) or '—'}")
    lines.append(f"- Y-карты ({len(agg['ycards'])}): {', '.join(sorted(agg['ycards'], key=lambda x: int(x[1:]))) or '—'}")
    lines.append("")
    lines.append("## OC-ОКНО (не назначать — дрифт/ротация одних, вердикт T5-24; аудит Коула R6)")
    lines.append(f"- OC последних {depth} партий: {', '.join(sorted(agg['ocs'])) or '—'}")
    lines.append("- ростер готовых: остальной актив oc-canon.json (ready к жребию, без окна)")
    lines.append("")
    lines.append(f"## BURN-АКТИВ ({len(BURNED.get('entries', []))} кодов, specs/burned.json)")
    lines += burned_lines() or ["— реестр пуст"]
    return "\n".join(lines) + "\n"


def _arg_value(argv, flag, default=None, cast=str):
    """2026-11-20: значение флага без IndexError/ValueError."""
    if flag not in argv:
        return default
    i = argv.index(flag)
    if i + 1 >= len(argv) or argv[i + 1].startswith("--"):
        print(f"window: флаг {flag} требует значение")
        sys.exit(2)
    try:
        return cast(argv[i + 1])
    except (TypeError, ValueError):
        print(f"window: не поняла значение {flag}={argv[i + 1]!r}")
        sys.exit(2)


def main():
    argv = sys.argv[1:]
    depth = _arg_value(argv, "--depth", default=3, cast=int)
    out = _arg_value(argv, "--out", default=None, cast=Path)

    for_target = _arg_value(argv, "--for", default=None, cast=str)
    if for_target is not None:
        # Окно для конкретной партии (аудит 2026-10-31, F2): предыдущие по
        # НОМЕРУ, не по mtime — mtime-порядок врёт после правок старых файлов.
        m = re.search(r"T5-(\d+)", for_target)
        if not m:
            print(f"--for: не понял партию «{for_target}»")
            sys.exit(2)
        tnum = int(m.group(1))

        paths = sorted(
            (p for p in delivered_batches() if 0 < bnum(p) < tnum),
            key=lambda p: (bnum(p), p.stat().st_mtime),
            reverse=True,
        )[:depth]
    else:
        paths = delivered_batches()[:depth]
    if not paths:
        print("нет сданных батчей — окно пустое")
        sys.exit(0)
    per_batch, agg = collect(paths)
    md = receipt_md(per_batch, agg, len(paths))
    print(md)
    if out:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(md, encoding="utf-8")
        print(f"квитанция станции: {out}")


if __name__ == "__main__":
    main()
