#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""T5-29: калибровочный аудит ratingTruth (В43) — таблица для постмортема.

Печатает по слотам: заявленный бейдж → состав-факт модели → вердикт автора
(ground truth: совпали P04/P11/P18/P27) → класс несоответствия.
Использует ЖИВУЮ модель gates.rating_implied (не копию — дрейф исключён).
"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))
import gates  # noqa: E402

GROUND_TRUTH_MATCH = {"P04", "P11", "P18", "P27"}

text, header, slots = gates.parse_batch(REPO / "batches" / "T5-29.md")
cfg = gates.GATES["ratingTruth"]

rows = []
for s in slots:
    if s.rating not in ("R+", "R", "PG-13"):
        continue
    implied = gates.rating_implied(s.pos, cfg)
    pos_l = (s.pos or "").lower()
    has_bare = any(t in pos_l for t in cfg["bareClaim"])
    has_read = any(t in pos_l for t in cfg["breastRead"])
    strap = any(t in pos_l for t in cfg["strapOnly"])
    hold = any(t in pos_l for t in cfg["handHold"])
    rtok = [
        k for k, toks in (cfg.get("rTokens") or {}).items()
        if any(t in pos_l for t in toks)
    ]
    ev = []
    if has_bare:
        ev.append("bareClaim")
    if has_read:
        ev.append("breastRead")
    if strap:
        ev.append("strapOnly")
    if hold:
        ev.append("handHold")
    ev += rtok
    if s.rating == implied:
        verdict = "СОВПАЛ"
    elif s.rating == "R+":
        verdict = "ЛОЖНЫЙ R+ (состав R)"
    elif s.rating == "R" and implied == "PG-13":
        verdict = "ДРЕЙФ R→PG-13"
    else:
        verdict = f"ДРЕЙФ PG-13→{implied}"
    author = "✓ автор" if s.sid in GROUND_TRUTH_MATCH else "✗ автор"
    ok = (s.sid in GROUND_TRUTH_MATCH) == (s.rating == implied)
    rows.append((s.sid, s.genre, s.rating, implied, verdict, author,
                 "OK" if ok else "!!! МОДЕЛЬ ≠ АВТОР", "+".join(ev) or "—"))

print(f"{'слот':<5}{'жанр':<10}{'бейдж':<6}{'состав':<7}"
      f"{'класс':<22}{'ground truth':<13}{'сходимость':<24}{'доказательства'}")
for r in rows:
    print(f"{r[0]:<5}{r[1]:<10}{r[2]:<6}{r[3]:<7}{r[4]:<22}{r[5]:<13}"
          f"{r[6]:<24}{r[7]}")

match_model = sum(1 for r in rows if r[2] == r[3])
match_author = len(GROUND_TRUTH_MATCH)
agree = sum(1 for r in rows if r[6] == "OK")
print()
print(f"модель: совпало {match_model}/33 · автор: {match_author}/33 · "
      f"сходимость модель↔автор: {agree}/33")
false_rplus = sum(1 for r in rows if r[4].startswith("ЛОЖНЫЙ"))
drift = sum(1 for r in rows if r[4].startswith("ДРЕЙФ"))
print(f"ложных R+: {false_rplus} · мягких дрейфов: {drift} · "
      f"помечено всего: {false_rplus + drift}")
