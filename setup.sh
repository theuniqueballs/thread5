#!/usr/bin/env bash
# THREAD 5 — настройка свежего клона (ревизия 2026-11-01, 1.11b).
# Без этого шага pre-commit НЕ СУЩЕСТВУЕТ: клон коммитит без sha-замка
# молча. Запуск один раз после clone:
#   bash setup.sh
set -e
cd "$(dirname "$0")"

# python3 — единственная зависимость хука и гейтов (stdlib-only)
if ! command -v python3 >/dev/null 2>&1; then
  echo "✗ python3 не найден — гейты и sha-замок не работают без него"
  exit 1
fi

git config core.hooksPath .githooks
echo "✓ core.hooksPath = .githooks (sha-замок квитанций активен)"
# exec-бит хука мог потеряться (Windows-checkout / странная ФС): git молча
# пропускает неисполняемые хуки — перестраховываемся явным chmod
chmod +x .githooks/pre-commit 2>/dev/null || true
git config core.fileMode false
echo "✓ core.fileMode = false (mode-бит файловой системы не шумит в diff)"
python3 tools/validate.py
echo "✓ клон настроен: валидатор PASS, хук на месте"
echo "  инженерия: bun install && bun run test && bun run test:py (tests/README)"
