#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Юнит-проверка yStackGate на живом батче T5-28 (applyFrom временно 0):
сколько слотов реально стакается (CL-код держит класс карты Y).
Логика-зеркало гейта: «—» = геометрия позы (skip), смежность COVER↔CLOTHED-TIGHT."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import gates  # noqa: E402

gates.GATES["yStack"]["applyFrom"] = 0

slots = gates.parse_batch(ROOT / "batches" / "T5-28.md")[2]
warns: list = []
st = gates.check_ystack(slots, warns, batch_no=28)

print(f"checked={st['checked']} stacked={st['stacked']} choked={st['choked']} "
      f"canon_without_codes={st['canon_without_codes']} geometry_only={st['geometry_only']}")
print(f"warns: {len(warns)}")
for sid, g, msg in warns:
    print(f"  [{sid}] {g}: {msg[:110]}")

closet = gates.load_closet_exposure()
ycards = gates.load_y_cards()
carries = {"COVER": {"COVER", "CLOTHED-TIGHT"}}
print("\nдетально (карта/класс → коды → держит?):")
for s in slots:
    if not s.y_card or s.y_card not in ycards or not s.gar_codes:
        continue
    exp = ((ycards[s.y_card].get("components") or {}).get("exposure") or {}).get("class")
    if not exp or exp == "—":
        print(f"  {s.sid} {s.y_card} [—]: геометрия позы несёт интим — стак не нужен")
        continue
    wanted = carries.get(exp, {exp})
    ok = [f"{c}:{'ДА' if wanted & set(closet.get(c, [])) else 'нет'}" for c in s.gar_codes]
    flag = "" if any(wanted & set(closet.get(c, [])) for c in s.gar_codes) else "  ← ДУШИТ"
    print(f"  {s.sid} {s.y_card} [{exp}]: {' '.join(ok)}{flag}")
