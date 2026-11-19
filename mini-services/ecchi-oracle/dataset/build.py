#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ECCHI-ORACLE dataset merge: seeds + generated parts -> train/val splits + stats."""
import json, random, collections, os, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
PARTS = ["seed-01.jsonl", "seed-02.jsonl", "seed-03.jsonl",
         "gen-a.jsonl", "gen-b.jsonl", "gen-c.jsonl", "gen-d.jsonl", "gen-e.jsonl"]
VAL_FRACTION = 0.09
SEED = 1337

def main():
    items, seen_hashes, dupes = [], set(), 0
    missing, broken = [], 0
    for part in PARTS:
        path = os.path.join(HERE, part)
        if not os.path.exists(path):
            print(f"!! missing part: {part}")
            missing.append(part)
            continue
        with open(path, encoding="utf-8") as fh:  # 2026-11-20: контекст-менеджер
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    d = json.loads(line)
                    key = hashlib.md5((d["messages"][1]["content"] + "|" + d["messages"][2]["content"][:200]).encode()).hexdigest()
                except (json.JSONDecodeError, KeyError, IndexError, TypeError):
                    # 2026-11-20: битая строка не должна валить всю сборку молча
                    broken += 1
                    continue
                if key in seen_hashes:
                    dupes += 1
                    continue
                seen_hashes.add(key)
                items.append(d)
    if missing:
        # 2026-11-20: явный отказ вместо «тихо построила датасет меньше»
        raise SystemExit(
            f"!! отсутствуют части датасета: {', '.join(missing)} — "
            f"запусти генераторы (gen_a.py…gen_e.py) рядом с build.py"
        )

    # global renumbering with source-prefixed ids kept
    random.seed(SEED)

    # stratified split by category
    by_cat = collections.defaultdict(list)
    for d in items:
        by_cat[d["category"]].append(d)

    train, val = [], []
    for cat in sorted(by_cat):
        bucket = by_cat[cat][:]
        random.shuffle(bucket)
        n_val = max(1, round(len(bucket) * VAL_FRACTION)) if len(bucket) >= 4 else 0
        val.extend(bucket[:n_val])
        train.extend(bucket[n_val:])
    random.shuffle(train)
    random.shuffle(val)

    with open(os.path.join(HERE, "train.jsonl"), "w", encoding="utf-8") as f:
        for d in train:
            f.write(json.dumps(d, ensure_ascii=False) + "\n")
    with open(os.path.join(HERE, "val.jsonl"), "w", encoding="utf-8") as f:
        for d in val:
            f.write(json.dumps(d, ensure_ascii=False) + "\n")

    stats = {
        "total": len(items),
        "train": len(train),
        "val": len(val),
        "dupes_removed": dupes,
        "broken_lines_skipped": broken,
        "by_category": {c: len(v) for c, v in sorted(by_cat.items())},
        "seed": SEED,
        "val_fraction": VAL_FRACTION,
        "system_prompt_len_chars": len(items[0]["messages"][0]["content"]) if items else 0,
    }
    with open(os.path.join(HERE, "stats.json"), "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
    print(json.dumps(stats, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
