#!/bin/bash
# Дренаж триажа T5-28 (2026-11-21): CAP=1 на запрос (вторая итерация фикса 502).
# Лог — в inbox/drain-triage.log; guard 80 запросов, пауза 2с между.
API="http://localhost:3000/api/t5/inbox/triage"
LOG="/home/z/my-project/inbox/drain-triage.log"
: > "$LOG"
for i in $(seq 1 80); do
  out=$(curl -s -m 110 -X POST "$API" -H 'Content-Type: application/json' -d '{}' 2>&1)
  triaged=$(echo "$out" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('triaged',0))" 2>/dev/null || echo "ERR")
  remaining=$(echo "$out" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('remaining','?'))" 2>/dev/null || echo "?")
  echo "[$(date +%H:%M:%S)] #$i triaged=$triaged remaining=$remaining" >> "$LOG"
  if [ "$remaining" = "0" ] || [ "$triaged" = "0" ] || [ "$triaged" = "ERR" ]; then
    echo "[$(date +%H:%M:%S)] DRAIN_DONE (remaining=$remaining, triaged=$triaged)" >> "$LOG"
    break
  fi
  sleep 2
done
