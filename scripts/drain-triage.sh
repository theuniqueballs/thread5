#!/bin/bash
# Дренаж очереди триажа инбокса: крутит /api/t5/inbox/triage, пока remaining > 0.
# Живой тест фикса 1301 (2026-11-21): старые fail-closed причины перетриажируются
# один раз, получают терминальный вердикт фильтра и выходят из очереди.
API="http://localhost:3000/api/t5/inbox/triage"
for i in $(seq 1 30); do
  out=$(curl -s -m 110 -X POST "$API" -H 'Content-Type: application/json' -d '{}')
  triaged=$(echo "$out" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('triaged',0))" 2>/dev/null || echo "?")
  remaining=$(echo "$out" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('remaining',0))" 2>/dev/null || echo "?")
  echo "[$i] triaged=$triaged remaining=$remaining"
  if [ "$remaining" = "0" ] || [ "$triaged" = "0" ]; then
    echo "QUEUE_DRAINED (remaining=$remaining)"
    break
  fi
  sleep 2
done
