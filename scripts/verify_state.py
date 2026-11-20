#!/usr/bin/env python3
"""Проверка состояния двух деревьев (root vs thread5/) перед апгрейдом."""
import json
import os
import filecmp

ROOT = "/home/z/my-project/thread5"

print("=== ROOT specs versions ===")
for f in ["camera", "gates", "raw-plus", "poses", "palettes"]:
    p = os.path.join(ROOT, "specs", f + ".json")
    try:
        d = json.load(open(p, encoding="utf-8"))
        extra = ""
        if f == "camera":
            cards = d.get("y_cards", {}).get("cards", [])
            ids = [c.get("id", "") for c in cards]
            extra = f" | cards={len(cards)} | max={max(ids, key=lambda x: int(x[1:])) if ids else '-'}"
        print(f"  {f}: v{d.get('version')}{extra}")
    except Exception as e:
        print(f"  {f}: ERROR {e}")

print("=== NESTED thread5/specs versions ===")
for f in ["camera", "gates", "raw-plus", "poses", "palettes"]:
    p = os.path.join(ROOT, "thread5", "specs", f + ".json")
    try:
        d = json.load(open(p, encoding="utf-8"))
        extra = ""
        if f == "camera":
            cards = d.get("y_cards", {}).get("cards", [])
            ids = [c.get("id", "") for c in cards]
            extra = f" | cards={len(cards)} | max={max(ids, key=lambda x: int(x[1:])) if ids else '-'}"
        print(f"  {f}: v{d.get('version')}{extra}")
    except Exception as e:
        print(f"  {f}: ERROR {e}")


def tree_diff(a, b):
    diffs = []
    for dirpath, dirnames, filenames in os.walk(a):
        rel = os.path.relpath(dirpath, a)
        other_dir = os.path.join(b, rel) if rel != "." else b
        for name in filenames:
            pa = os.path.join(dirpath, name)
            pb = os.path.join(other_dir, name)
            if not os.path.exists(pb):
                diffs.append(f"ONLY-IN-ROOT: {os.path.relpath(pa, a)}")
            elif not filecmp.cmp(pa, pb, shallow=False):
                diffs.append(f"DIFFERS: {os.path.relpath(pa, a)}")
        if os.path.isdir(other_dir):
            for name in os.listdir(other_dir):
                pb = os.path.join(other_dir, name)
                if os.path.isfile(pb) and not os.path.exists(os.path.join(dirpath, name)):
                    diffs.append(f"ONLY-IN-NESTED: {os.path.relpath(pb, b)}")
    return diffs


for sub in ["batches", "specs", "verdicts", "docs", "special"]:
    a = os.path.join(ROOT, sub)
    b = os.path.join(ROOT, "thread5", sub)
    if not os.path.isdir(a) or not os.path.isdir(b):
        print(f"\n=== {sub}: MISSING DIR (root={os.path.isdir(a)}, nested={os.path.isdir(b)}) ===")
        continue
    d = tree_diff(a, b)
    print(f"\n=== {sub}: {len(d)} differences ===")
    for line in d[:12]:
        print(f"  {line}")
    if len(d) > 12:
        print(f"  … и ещё {len(d) - 12}")

for base in ["batches", "thread5/batches"]:
    p = os.path.join(ROOT, base)
    files = [f for f in os.listdir(p) if f.endswith(".md") and not f.endswith(".gate-report.md")]
    print(f"\n{base}: {len(files)} batch files")

print("\n=== git log nested tree (last 5) ===")
os.system("cd /home/z/my-project/thread5 && git log --oneline -5 -- thread5/ | cat")
print("\n=== git log root batches (last 3) ===")
os.system("cd /home/z/my-project/thread5 && git log --oneline -3 -- batches/ | cat")
