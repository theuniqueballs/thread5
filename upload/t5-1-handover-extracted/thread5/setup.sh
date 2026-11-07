#!/usr/bin/env bash
# THREAD 5 — настройка свежего клона (ревизия 2026-11-01, 1.11b).
# Без этого шага pre-commit НЕ СУЩЕСТВУЕТ: клон коммитит без sha-замка
# молча. Запуск один раз после clone:
#   bash setup.sh
set -e
cd "$(dirname "$0")"
git config core.hooksPath .githooks
echo "✓ core.hooksPath = .githooks (sha-замок квитанций активен)"
git config core.fileMode false
echo "✓ core.fileMode = false (mode-бит файловой системы не шумит в diff)"
python3 tools/validate.py
echo "✓ клон настроен: валидатор PASS, хук на месте"
