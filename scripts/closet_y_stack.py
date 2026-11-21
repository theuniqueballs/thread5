#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CLOSET v1.1.0 — Y×CLOSET STACK, акт 1: exposure-поле каждому коду.

Заказ автора (2026-11-21, после вердикта T5-28): «У тебя есть комбо Y, но
одежда дрессера вообще не стакается с рейтингом. Даже если комбо крутое и
ёбнутое, неправильная одежда в неправильном состоянии скинет R+ комбо до
PG-13. Надо найти способ стакнуть момент Y и одежду, а как — это уже твоя
забота».

Механизм: у каждого кода CLOSET появляется поле exposure — список классов
экспозиции Y-карт (COVER | PROCESS | LINGERIE | CLOTHED-TIGHT | SHEER,
camera.json y_cards.law), которые вещь ДЕРЖИТ ЧЕСТНО по своей pos/hook-строке.
Сборка Y-first (y_assembly) сужает кубик Дрессера до кодов, совместимых с
классом карты; гейт yStack (gates.py) ловит душилки.

Классы присвоены вручную по pos/hook каждой вещи (dump /tmp/closet_dump.txt);
принципы:
  COVER        — вещь не мешает прикрытию ладонью/предметом: тонкая, сдвинутая,
                 открытая зона, либо сама объект-прикрытие (полотенце, лацканы);
  PROCESS      — вещь честно процессится: подол, бретель, узел, молния, пояс,
                 пуговицы, wrap — есть что поднимать/сдвигать/снимать;
  LINGERIE     — вещь сама кадр-бельё или домашний интимный регистр;
  CLOTHED-TIGHT— облегание читает форму: bumps/pantyline/cameltoe через ткань
                 (тёмная/честная ткань, clinging, compression, mirror-finish);
  SHEER        — просвет: шёлк/шифон/органза/тюль/кружево/сетка/прозрачный винил.

Полка получает агрегат carries (какие классы полка в целом несёт) — для
читаемости; per-код exposure — источник истины для стака и гейта.
"""
import json
import sys
from pathlib import Path

SPECS = Path(__file__).resolve().parent.parent / "specs" / "closet.json"

# код → классы экспозиции, которые вещь держит честно (см. докстринг)
EXPOSURE = {
    # DR — платья
    "CL-DR-01": ["SHEER", "CLOTHED-TIGHT", "PROCESS", "LINGERIE"],
    "CL-DR-02": ["CLOTHED-TIGHT", "PROCESS"],
    "CL-DR-03": ["CLOTHED-TIGHT", "PROCESS", "SHEER"],
    "CL-DR-04": ["PROCESS", "COVER"],
    "CL-DR-05": ["PROCESS", "COVER"],
    "CL-DR-06": ["PROCESS", "COVER"],
    "CL-DR-07": ["CLOTHED-TIGHT", "PROCESS", "COVER"],
    "CL-DR-08": ["CLOTHED-TIGHT", "PROCESS"],
    "CL-DR-09": ["PROCESS", "COVER"],
    "CL-DR-10": ["SHEER", "COVER", "PROCESS"],
    "CL-DR-11": ["COVER", "PROCESS"],
    "CL-DR-12": ["CLOTHED-TIGHT", "PROCESS", "COVER"],
    "CL-DR-13": ["LINGERIE", "PROCESS", "COVER"],
    "CL-DR-14": ["CLOTHED-TIGHT", "PROCESS"],
    # SK — юбки
    "CL-SK-01": ["PROCESS", "COVER"],
    "CL-SK-02": ["PROCESS", "COVER"],
    "CL-SK-03": ["PROCESS", "COVER"],
    "CL-SK-04": ["PROCESS", "COVER"],
    "CL-SK-05": ["PROCESS", "COVER"],
    "CL-SK-06": ["CLOTHED-TIGHT", "PROCESS"],
    "CL-SK-07": ["SHEER", "PROCESS"],
    "CL-SK-08": ["PROCESS", "COVER", "LINGERIE"],
    "CL-SK-09": ["PROCESS", "COVER"],
    "CL-SK-10": ["PROCESS", "COVER"],
    # TS — верх
    "CL-TS-01": ["PROCESS", "COVER"],
    "CL-TS-02": ["SHEER", "COVER", "PROCESS"],
    "CL-TS-03": ["CLOTHED-TIGHT", "PROCESS", "COVER"],
    "CL-TS-04": ["CLOTHED-TIGHT", "PROCESS", "COVER"],
    "CL-TS-05": ["CLOTHED-TIGHT", "COVER", "PROCESS"],
    "CL-TS-06": ["PROCESS", "COVER", "CLOTHED-TIGHT"],
    "CL-TS-07": ["PROCESS", "COVER"],
    "CL-TS-08": ["CLOTHED-TIGHT", "PROCESS"],
    "CL-TS-09": ["PROCESS", "COVER", "LINGERIE"],
    "CL-TS-10": ["LINGERIE", "PROCESS", "COVER"],
    "CL-TS-11": ["PROCESS", "COVER"],
    "CL-TS-12": ["SHEER", "PROCESS"],
    "CL-TS-13": ["CLOTHED-TIGHT", "PROCESS"],
    "CL-TS-14": ["CLOTHED-TIGHT", "PROCESS", "COVER"],
    # SW — вязаное
    "CL-SW-01": ["COVER", "PROCESS"],
    "CL-SW-02": ["PROCESS", "COVER"],
    "CL-SW-03": ["CLOTHED-TIGHT", "PROCESS"],
    "CL-SW-04": ["PROCESS", "COVER", "LINGERIE"],
    "CL-SW-05": ["COVER", "PROCESS", "CLOTHED-TIGHT"],
    "CL-SW-06": ["COVER", "PROCESS"],
    "CL-SW-07": ["COVER", "PROCESS"],
    "CL-SW-08": ["COVER", "PROCESS", "CLOTHED-TIGHT"],
    # BT — низ
    "CL-BT-01": ["PROCESS", "COVER", "CLOTHED-TIGHT"],
    "CL-BT-02": ["CLOTHED-TIGHT", "PROCESS"],
    "CL-BT-03": ["CLOTHED-TIGHT"],
    "CL-BT-04": ["PROCESS", "COVER"],
    "CL-BT-05": ["PROCESS", "LINGERIE", "COVER"],
    "CL-BT-06": ["COVER"],
    "CL-BT-07": ["CLOTHED-TIGHT", "COVER"],
    "CL-BT-08": ["CLOTHED-TIGHT"],
    "CL-BT-09": ["PROCESS", "COVER"],
    "CL-BT-10": ["LINGERIE", "PROCESS", "SHEER"],
    # UR — бельё
    "CL-UR-01": ["LINGERIE", "SHEER", "PROCESS"],
    "CL-UR-02": ["LINGERIE", "CLOTHED-TIGHT", "PROCESS"],
    "CL-UR-03": ["LINGERIE", "SHEER", "PROCESS"],
    "CL-UR-04": ["LINGERIE", "PROCESS"],
    "CL-UR-05": ["LINGERIE", "CLOTHED-TIGHT", "PROCESS"],
    "CL-UR-06": ["LINGERIE", "PROCESS", "CLOTHED-TIGHT"],
    "CL-UR-07": ["LINGERIE", "CLOTHED-TIGHT", "PROCESS"],
    "CL-UR-08": ["LINGERIE", "CLOTHED-TIGHT", "PROCESS"],
    "CL-UR-09": ["CLOTHED-TIGHT", "PROCESS", "LINGERIE"],
    "CL-UR-10": ["LINGERIE", "COVER", "PROCESS"],
    # HK — чулочно-носочное
    "CL-HK-01": ["SHEER", "LINGERIE"],
    "CL-HK-02": ["PROCESS", "LINGERIE"],
    "CL-HK-03": ["SHEER", "LINGERIE"],
    "CL-HK-04": ["PROCESS", "LINGERIE"],
    "CL-HK-05": ["PROCESS", "LINGERIE"],
    "CL-HK-06": ["SHEER", "PROCESS"],
    "CL-HK-07": ["SHEER", "LINGERIE", "PROCESS"],
    "CL-HK-08": ["LINGERIE"],
    # SM — купальники
    "CL-SM-01": ["LINGERIE", "PROCESS", "CLOTHED-TIGHT"],
    "CL-SM-02": ["LINGERIE", "PROCESS"],
    "CL-SM-03": ["LINGERIE", "PROCESS"],
    "CL-SM-04": ["LINGERIE", "CLOTHED-TIGHT"],
    "CL-SM-05": ["LINGERIE", "PROCESS"],
    "CL-SM-06": ["PROCESS", "CLOTHED-TIGHT", "COVER"],
    "CL-SM-07": ["PROCESS", "COVER", "CLOTHED-TIGHT"],
    "CL-SM-08": ["PROCESS", "CLOTHED-TIGHT"],
    "CL-SM-09": ["PROCESS", "LINGERIE", "COVER"],
    "CL-SM-10": ["PROCESS", "COVER", "LINGERIE"],
    # LG — дом и сон
    "CL-LG-01": ["LINGERIE", "PROCESS", "COVER"],
    "CL-LG-02": ["LINGERIE", "SHEER", "PROCESS"],
    "CL-LG-03": ["LINGERIE", "PROCESS", "COVER"],
    "CL-LG-04": ["LINGERIE", "PROCESS", "COVER"],
    "CL-LG-05": ["PROCESS", "COVER", "LINGERIE"],
    "CL-LG-06": ["SHEER", "LINGERIE", "PROCESS"],
    "CL-LG-07": ["LINGERIE", "PROCESS"],
    "CL-LG-08": ["LINGERIE", "PROCESS"],
    # OU — верхняя одежда
    "CL-OU-01": ["PROCESS", "COVER"],
    "CL-OU-02": ["SHEER", "PROCESS", "COVER"],
    "CL-OU-03": ["COVER", "PROCESS"],
    "CL-OU-04": ["PROCESS", "COVER"],
    "CL-OU-05": ["PROCESS", "COVER"],
    "CL-OU-06": ["PROCESS", "COVER"],
    "CL-OU-07": ["PROCESS", "COVER", "LINGERIE"],
    "CL-OU-08": ["COVER", "PROCESS", "LINGERIE"],
    # FX — формал и сцена
    "CL-FX-01": ["PROCESS", "COVER", "CLOTHED-TIGHT"],
    "CL-FX-02": ["CLOTHED-TIGHT", "PROCESS", "COVER"],
    "CL-FX-03": ["CLOTHED-TIGHT", "LINGERIE", "PROCESS"],
    "CL-FX-04": ["PROCESS", "COVER"],
    "CL-FX-05": ["PROCESS", "COVER"],
    "CL-FX-06": ["COVER", "PROCESS", "CLOTHED-TIGHT"],
    "CL-FX-07": ["PROCESS", "COVER", "CLOTHED-TIGHT"],
    "CL-FX-08": ["CLOTHED-TIGHT", "LINGERIE", "PROCESS"],
    # AC — аксессуары
    "CL-AC-01": ["LINGERIE", "COVER"],
    "CL-AC-02": ["LINGERIE", "COVER"],
    "CL-AC-03": ["COVER", "SHEER"],
    "CL-AC-04": ["COVER", "PROCESS", "LINGERIE"],
    "CL-AC-05": ["PROCESS"],
    "CL-AC-06": ["LINGERIE", "COVER"],
    "CL-AC-07": ["PROCESS"],
    "CL-AC-08": [],
    "CL-AC-09": ["PROCESS", "COVER"],
    "CL-AC-10": ["LINGERIE", "COVER"],
    # V — VAULT
    "CL-V-01": ["CLOTHED-TIGHT", "LINGERIE", "PROCESS"],
    "CL-V-02": ["CLOTHED-TIGHT", "LINGERIE"],
    "CL-V-03": ["CLOTHED-TIGHT", "LINGERIE"],
}

VALID = {"COVER", "PROCESS", "LINGERIE", "CLOTHED-TIGHT", "SHEER"}


def main() -> None:
    d = json.loads(SPECS.read_text(encoding="utf-8"))
    shelves = d["shelves"]

    # sanity: все коды спеки покрыты, лишних нет
    spec_codes = [it["code"] for v in shelves.values() for it in v["items"]]
    missing = [c for c in spec_codes if c not in EXPOSURE]
    extra = [c for c in EXPOSURE if c not in spec_codes]
    if missing or extra:
        print("FATAL missing:", missing, "extra:", extra)
        sys.exit(1)
    bad = {c: e for c, es in EXPOSURE.items() for e in es if e not in VALID}
    if bad:
        print("FATAL unknown classes:", bad)
        sys.exit(1)

    for shelf_id, shelf in shelves.items():
        for it in shelf["items"]:
            it["exposure"] = EXPOSURE[it["code"]]
        # агрегат полки — для читаемости (союз per-код полей)
        union: list[str] = []
        for it in shelf["items"]:
            for e in it["exposure"]:
                if e not in union:
                    union.append(e)
        shelf["carries"] = union

    d["version"] = "1.1.0"
    d["y_stack_born"] = (
        "2026-11-21, заказ автора (чат, после вердикта T5-28): «У тебя есть комбо Y, "
        "но одежда дрессера вообще не стакается с рейтингом. Даже если комбо крутое "
        "и ёбнутое, неправильная одежда в неправильном состоянии скинет R+ комбо до "
        "PG-13. Надо найти способ стакнуть момент Y и одежду, а как — это уже твоя "
        "забота». Поле exposure у каждого кода: какие классы экспозиции Y-карт "
        "(camera.json y_cards) вещь держит честно по своей pos/hook-строке. Сборка "
        "Y-first сужает кубик Дрессера до совместимых кодов (dresser.json v1.2.0 "
        "y_stack); гейт yStack (tools/gates.py) ловит душилки — вещь без класса "
        "карты в кадре душит экспозицию до PG-13."
    )

    SPECS.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("OK: exposure присвоен", len(EXPOSURE), "кодам; carries —", len(shelves), "полкам; version 1.1.0")


if __name__ == "__main__":
    main()
