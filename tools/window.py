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
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

from gates import parse_batch  # noqa: E402  (общий парсер слотов)

BATCH_DIR = ROOT / "batches"
BURNED = json.loads((ROOT / "specs/burned.json").read_text(encoding="utf-8"))


def delivered_batches():
    """Сданные батчи T5-*.md (без шаблона и отчётов), свежие первыми."""
    files = [
        p for p in BATCH_DIR.glob("T5-*.md")
        if not p.name.endswith(".gate-report.md")
    ]
    return sorted(files, key=lambda p: p.stat().st_mtime, reverse=True)


def collect(paths):
    """По батчу: заголовок + агрегаты. По системе: множества окна."""
    per_batch, agg = [], {
        "pose": set(), "palette": set(), "kinetics": set(),
        "carriers": set(), "channels": set(), "ratings": {},
    }
    for p in paths:
        _, _, slots = parse_batch(p)
        batch = {
            "file": p.name,
            "slots": len(slots),
            "pose": sorted({s.pose for s in slots if s.pose}),
            "palette": sorted({s.palette for s in slots if s.palette}),
            "kinetics": sorted({k for s in slots for k in s.kinetics}),
            "carriers": sorted({c for s in slots for c in s.carriers}),
            "channels": sorted({s.channel for s in slots if s.channel}),
            "ratings": {},
        }
        for s in slots:
            if s.rating:
                batch["ratings"][s.rating] = batch["ratings"].get(s.rating, 0) + 1
        for key in ("pose", "palette", "kinetics", "carriers", "channels"):
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
        "- Окно = последние сданные батчи: позы/палитры/кинетики окна НЕ",
        "  повторяются в новом батче (LAWS §7). Burn-актив не назначается",
        "  никогда, кроме ⚗ с явной гипотезой (law burned.json).",
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
        lines.append("")
    lines.append("## ЗАПРЕТ ОКНА (агрегат — не назначать)")
    lines.append(f"- позы ({len(agg['pose'])}): {', '.join(sorted(agg['pose'])) or '—'}")
    lines.append(f"- палитры ({len(agg['palette'])}): {', '.join(sorted(agg['palette'])) or '—'}")
    lines.append(f"- кинетики ({len(agg['kinetics'])}): {', '.join(sorted(agg['kinetics'])) or '—'}")
    lines.append(f"- носители ({len(agg['carriers'])}): {', '.join(sorted(agg['carriers'])) or '—'}")
    lines.append(f"- каналы ({len(agg['channels'])}): {', '.join(sorted(agg['channels'])) or '—'}")
    lines.append("")
    lines.append(f"## BURN-АКТИВ ({len(BURNED.get('entries', []))} кодов, specs/burned.json)")
    lines += burned_lines() or ["— реестр пуст"]
    return "\n".join(lines) + "\n"


def main():
    depth = 3
    out = None
    argv = sys.argv[1:]
    if "--depth" in argv:
        depth = int(argv[argv.index("--depth") + 1])
    if "--out" in argv:
        out = Path(argv[argv.index("--out") + 1])

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
