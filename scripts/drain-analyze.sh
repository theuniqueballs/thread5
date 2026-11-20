#!/bin/bash
# Фоновый дренаж очереди разбора инбокса: дефекты + Коул + слот зрением.
# Пишет прогресс в scripts/analyze-drain.log. Пауза 3с между запросами —
# не дразним vision-API (урок 429-шторма 2026-11-21).
API="http://localhost:3000/api/t5/inbox/analyze"
LOG="/home/z/my-project/scripts/analyze-drain.log"
: > "$LOG"
for i in $(seq 1 40); do
  out=$(curl -s -m 115 -X POST "$API" -H 'Content-Type: application/json' -d '{"action":"analyze"}')
  analyzed=$(echo "$out" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('analyzed',0))" 2>/dev/null || echo "ERR")
  remaining=$(echo "$out" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('remaining',0))" 2>/dev/null || echo "ERR")
  echo "[$(date +%H:%M:%S)] analyzed=$analyzed remaining=$remaining" >> "$LOG"
  if [ "$remaining" = "0" ] || [ "$analyzed" = "0" ]; then
    echo "ANALYZE_DRAINED remaining=$remaining" >> "$LOG"
    break
  fi
  sleep 3
done
