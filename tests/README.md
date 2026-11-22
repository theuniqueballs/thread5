# tests — тестовая территория thread5

## Прилавок (TypeScript, bun test)

```
bun run test          # tests/unit/*.test.ts — парсер, ystamp, инбокс, store
bun run typecheck     # tsc --noEmit
bun run lint          # eslint
```

Покрытие — регрессии живых инцидентов:

- `parse.test.ts` — 3-значные Y-карты (Y513/Y428: {1,2} резал id до Y51 и
  чип копировал ЧУЖОЕ вплетение), Corridor «A + B», P100+, ⚗ за скобкой,
  EXP-маркер с длинным тире, склейка POS-переносов;
- `ystamp.test.ts` — контракт В34: weave (легален в POS) vs stamp (метаданные);
- `inbox.test.ts` — слот-маппинг P999, порядок батчей по номеру, защита
  путей от «..», fail-closed перетриаж;
- `store.test.ts` — естественный порядок полки (T5-9 < T5-10 < T5-100),
  безопасность слагов, резолвер T5_ROOT.

## Печь (Python, unittest, stdlib-only)

```
bun run test:py       # = python3 -m unittest discover -s tests/python -v
```

- `test_gates.py` — SLOT_RE 2/3 цифры, окно ротации Y-карт смотрит НАЗАД,
  depth=0, нормализация Corridor, y_range из живого camera.json,
  story-cards exempt для SO;
- `test_window_taste.py` — порядок партии по номеру (mtime не врёт),
  take_recent (последние вердикт-секции, не первые).
- `test_ci_workflow.py` — страж CI: main в push-фильтре ci.yml, «: » в
  именах шагов (класс 2026-11-20, Invalid workflow file), джобы
  web/pipeline/shell-smoke на месте, тамперы.

## Сборки рантаймов (shell)

- `python-runtime-build.sh` — гоняет живой .zscripts/python-runtime-build.sh
  по трём сценариям (requirements.txt / pyproject.toml / node-only);
  требует `uv` на PATH (CI ставит через astral-sh/setup-uv);
- `python-runtime-container.sh` — требует локальный Docker + приватный
  runner-образ (внешний запуск, не CI).

CI: `.github/workflows/ci.yml` гоняет web + pipeline + shell-smoke на
каждый пуш/PR.
