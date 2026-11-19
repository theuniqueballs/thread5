# ECCHI-ORACLE — обучение (QLoRA)

## Что это

Файнтюн компактной чат-модели в эксперт домена «эччи-приёмы манги и аниме» на шкале рейтингов
конвейера thread5 (SFW → PG-13 → R → R+ | X — знание границы, XXX — отказ).
Датасет: 509 примеров (463 train / 46 val), 15 категорий (эпоха Y-STAMP) — см. `../dataset/stats.json`.

## Базовые модели

| Модель | Параметры | Заметки |
|---|---|---|
| **Qwen/Qwen2.5-1.5B-Instruct** (дефолт) | 1.5B | RU+EN, сильна с тегами, лучшая стартовая точка |
| Qwen/Qwen2.5-3B-Instruct | 3B | +качество аудитов, чуть дольше учить |
| meta-llama/Llama-3.2-3B-Instruct | 3B | альтернатива (нужен HF-токен, gated) |
| HuggingFaceTB/SmolLM2-1.7B-Instruct | 1.7B | лёгкая, слабее с русским |

## Быстрый старт (одна GPU ≥16 ГБ или Colab T4)

```bash
pip install -r requirements.txt

# 1) обучение (примерно 40-70 мин на T4 при 3 эпохах)
python train_lora.py

# 2) контроль качества: boundary-пробы (XXX/loli/X без приказа — должны дать отказ)
python eval_oracle.py --adapter ../checkpoints/oracle-1.5b/adapter

# 3) слияние адаптера в полные веса
python merge_export.py --adapter ../checkpoints/oracle-1.5b/adapter --out ../models/ecchi-oracle-1

# 4) инференс слитой модели (vLLM / transformers)
python eval_oracle.py --model ../models/ecchi-oracle-1
```

## Гиперпараметры (дефолты — уже рабочие)

- QLoRA: 4-bit NF4, double-quant, bf16 compute
- LoRA: r=16, alpha=32, dropout=0.05, все проекции (q/k/v/o/gate/up/down)
- lr=2e-4, cosine, warmup 3%, 3 эпохи, effective batch = 2×8 = 16
- max_seq_length 2048 (на T4 можно `--max-len 1536`)
- Сид 1337 — воспроизводимые сплиты (`dataset/build.py`, тот же сид)

## Файлы

- `train_lora.py` — обучение (SFTTrainer + chat template базовой модели)
- `merge_export.py` — слияние адаптера, экспорт полных весов
- `eval_oracle.py` — трёхслойная проверка: boundary-пробы → tier-вердикты → качественный дамп val
- `../dataset/build.py` — пересборка сплитов из частей (seed-01..03 + gen-a..d)

## Экспорт в GGUF / Ollama (локальный инференс thread5)

```bash
git clone --depth 1 https://github.com/ggerganov/llama.cpp && cd llama.cpp
pip install -r requirements.txt
# конвертация (bf16 -> f16 для совместимости):
python convert_hf_to_gguf.py /path/to/ecchi-oracle-1 --outfile ecchi-oracle-1-f16.gguf --outtype f16
./llama-quantize ecchi-oracle-1-f16.gguf ecchi-oracle-1-q4_k_m.gguf Q4_K_M
```

Ollama Modelfile:

```
FROM ecchi-oracle-1-q4_k_m.gguf
TEMPLATE """{{- range .Messages }}<|im_start|>{{ .Role }}
{{ .Content }}<|im_end|>
{{ end }}<|im_start|>assistant
"""
PARAMETER temperature 0.4
PARAMETER num_ctx 4096
```

```bash
ollama create ecchi-oracle -f Modelfile
ollama run ecchi-oracle
```

## Что проверять после обучения

1. Boundary-пробы (4/4 PASS): XXX-запросы и child-код — отказ с возвратом в R+.
2. Tier-вердикты: в classify/audit/vision ответах есть согласованная марка (PG-13/R/R+/X).
3. claimPhysics-логика: аудит FAIL ловит самосертификацию (нет класса раскрытия / объекта A / геометрии B).
4. Русский с английскими тегами — стиль выдержан.

Если boundary-пробы падают — поднять вес safety-категории (дублировать safety-примеры в train
или 4-я эпоха с lr 1e-4) и переобучить.
