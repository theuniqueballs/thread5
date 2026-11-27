#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""stamp_era.py — era-сплит Y-карт (camera.json 1.23.0, ПЛАН 5.5 T3.1/T3.2).

Основание: вердикт T5-34 (В52 «старые Y = материал не слот») — 24 слота
партии собрались на старых 512 Y вербатимом («клеймо 1:1»), и процесс-
носители старой концепции рендером как эротика не читаются: 15 ложных R+
из 17. Era-сплит разводит концепции:

  era: legacy  — Y1–Y512 (старая концепция; определяется по combo-блоку
                 1.22.0 / диапазону id). Клеймо 1:1 ОТМЕНЕНО: карта
                 отдаёт скелет (поза / мех-группы / камерный кластер),
                 джус пишется заново (В52/В53: геометрия позы + состояние
                 вещи). Гейт yStamp eraGuard.
  era: modern  — Y513+ (волны «новеньких», юри-пара, носитель-комбо,
                 грань-X). Вплетение 1:1 обязательно, как было (В34/В35).

Перелейка (T3.3): карта, пересобранная в v2-концепцию (геометрия +
состояние вещи, паттерн переписан, combo-блок заново), переводится в
modern флагом --modern Y-id — реестр не растёт (закон реестровой диеты).

Режимы:
  python3 tools/stamp_era.py            # штамповать (идемпотентно)
  python3 tools/stamp_era.py --check    # проверить согласованность
  python3 tools/stamp_era.py --modern Y123 Y456   # перелейка → modern

Формат файла сохраняется (indent=1, ensure_ascii=False) — дифф чистый.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CAM = ROOT / "specs" / "camera.json"
LEGACY_MAX = 512  # старая 512-волна (combo-блок 1.22.0 — все, без пропусков)


def card_num(cid: str) -> int:
    try:
        return int(cid[1:])
    except ValueError:
        return -1


def stamp(data: dict, force_modern: set) -> tuple:
    """Ставит era каждой карте; возвращает (legacy, modern, изменённые id)."""
    cards = data.get("y_cards", {}).get("cards", [])
    legacy = modern = 0
    changed = []
    for card in cards:
        cid = card.get("id", "")
        n = card_num(cid)
        if cid in force_modern:
            era = "modern"
        elif 1 <= n <= LEGACY_MAX:
            era = "legacy"
        elif n > LEGACY_MAX:
            era = "modern"
        else:
            print(f"!! карта без числового id: {cid} — пропущена", file=sys.stderr)
            continue
        if era == "legacy":
            # слаженность: legacy обязан нести combo-блок разбора 1.22.0
            if not card.get("combo"):
                raise SystemExit(
                    f"ОТКАЗ: {cid} в диапазоне legacy (≤Y{LEGACY_MAX}), но без "
                    "combo-блока 1.22.0 — сплит по диапазону и по combo-блоку "
                    "расходятся; чини вручную, молчаливый пропуск запрещён")
        if card.get("era") != era:
            changed.append(cid)
        # era — сразу после id (паспорт концепции читается первым)
        fresh = {"id": cid}
        if era:
            fresh["era"] = era
        for k, v in card.items():
            if k in ("id", "era"):
                continue
            fresh[k] = v
        card.clear()
        card.update(fresh)
        if era == "legacy":
            legacy += 1
        else:
            modern += 1
    return legacy, modern, changed


def check(data: dict) -> int:
    """Согласованность: era ⇔ диапазон/combo, пропусков нет."""
    cards = data.get("y_cards", {}).get("cards", [])
    bad = []
    legacy = modern = 0
    for card in cards:
        cid = card.get("id", "")
        n = card_num(cid)
        era = card.get("era")
        if not era:
            bad.append(f"{cid}: нет поля era")
            continue
        if era not in ("legacy", "modern"):
            bad.append(f"{cid}: era={era} вне словаря")
        if era == "legacy" and not (1 <= n <= LEGACY_MAX and card.get("combo")):
            bad.append(f"{cid}: legacy вне диапазона/combo-блока")
        if era == "modern" and not n > LEGACY_MAX:
            bad.append(f"{cid}: modern вне диапазона Y{LEGACY_MAX}+ "
                       "(перелейка обязана идти через --modern осознанно)")
        if era == "legacy":
            legacy += 1
        else:
            modern += 1
    print(f"era-сплит: legacy {legacy} · modern {modern} · всего {len(cards)}")
    if bad:
        for b in bad:
            print(f"  !! {b}", file=sys.stderr)
        return 1
    print("ПРОВЕРКА ERA: PASS — сплит согласован (диапазон ⇄ combo ⇄ era)")
    return 0


def main() -> int:
    args = list(sys.argv[1:])
    do_check = "--check" in args
    force_modern = set()
    if "--modern" in args:
        rest = args[args.index("--modern") + 1:]
        force_modern = {a for a in rest if a.startswith("Y")}
    data = json.loads(CAM.read_text(encoding="utf-8"))
    if do_check:
        return check(data)
    legacy, modern, changed = stamp(data, force_modern)
    # тикет #4: сериализация спек — только через единый канон spec_io
    import spec_io
    spec_io.dump_spec(CAM, data)
    print(f"ERA-ШТАМП: legacy {legacy} · modern {modern} · перемечено {len(changed)}"
          + (f" → modern: {sorted(force_modern)}" if force_modern else ""))
    if changed:
        print("изменённые карты: " + ", ".join(changed[:20])
              + (" …" if len(changed) > 20 else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
