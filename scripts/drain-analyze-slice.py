#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Дренаж разбора инбокса порциями с бюджетом времени (процессы фона умирают
вместе с шеллом — крутим из bash-вызова напрямую, состояние в meta.json).

Каждый вызов: крутит POST /api/t5/inbox/analyze (CAP=1) пока remaining>0
или не выйдет бюджет (по умолчанию 480с). Прогресс — в stdout."""
import json
import sys
import time
import urllib.request

API = "http://localhost:3000/api/t5/inbox/analyze"
BUDGET = float(sys.argv[1]) if len(sys.argv) > 1 else 480.0

t0 = time.time()
done = 0
while time.time() - t0 < BUDGET:
    req = urllib.request.Request(
        API, data=json.dumps({"action": "analyze"}).encode(),
        headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=115) as r:
            d = json.loads(r.read().decode())
    except Exception as e:  # noqa: BLE001
        print(f"[{time.strftime('%H:%M:%S')}] error: {e}", flush=True)
        time.sleep(3)
        continue
    done += d.get("analyzed", 0)
    remaining = d.get("remaining", "?")
    print(f"[{time.strftime('%H:%M:%S')}] analyzed={d.get('analyzed')} "
          f"remaining={remaining} (total {done})", flush=True)
    if d.get("analyzed", 0) == 0 or remaining == 0:
        break
    time.sleep(2)
print(f"DRAIN_SLICE_DONE: done={done} remaining={remaining} "
      f"elapsed={time.time()-t0:.0f}s", flush=True)
