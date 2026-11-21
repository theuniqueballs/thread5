#!/bin/bash
# Дренаж разбора T5-28 (2026-11-21): analyze CAP=1 — дефекты + факт-рейтинг по
# Коу + слот зрением. Лог — inbox/drain-analyze.log; guard 45 запросов, пауза 2с.
API="http://localhost:3000/api/t5/inbox/analyze"
LOG="/home/z/my-project/inbox/drain-analyze.log"
: > "$LOG"
for i in $(seq 1 45); do
  out=$(curl -s -m 110 -X POST "$API" -H 'Content-Type: application/json' -d '{"action":"analyze"}' 2>&1)
  analyzed=$(echo "$out" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('analyzed',0))" 2>/dev/null || echo "ERR")
  remaining=$(echo "$out" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('remaining','?'))" 2>/dev/null || echo "?")
  echo "[$(date +%H:%M:%S)] #$i analyzed=$analyzed remaining=$remaining" >> "$LOG"
  if [ "$remaining" = "0" ] || [ "$analyzed" = "0" ] || [ "$analyzed" = "ERR" ]; then
    echo "[$(date +%H:%M:%S)] DRAIN_DONE (remaining=$remaining, analyzed=$analyzed)" >> "$LOG"
    break
  fi
  sleep 2
done
