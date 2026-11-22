#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ПРОТОКОЛ 1 «ПРОБЫ И ОШИБОК» — детальный разбор тест-батча-пробы.

Батч: TB-20261122-20261122 (21 слот, seed 20261122, testforge до правок).
Сверка со ВСЕМИ системами правил: гейты 1.18.0 (В39–В43), LAWS §2/§5/§24–27,
NICHE, marks.json, raw-plus, hard-флоры. Печатает послотовую таблицу и
нумерованный список причин (нарушений) для сводки.
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))
import gates  # noqa: E402

TB = REPO / "tests" / "test-corpus" / "TB-20261122-20261122.json"
doc = json.loads(TB.read_text(encoding="utf-8"))
slots = doc["slots"]
races_reg = {r["id"]: r for r in json.loads(
    (REPO / "specs" / "races.json").read_text(encoding="utf-8"))["races"]}
rt_cfg = gates.GATES["ratingTruth"]
ps_cfg = gates.GATES.get("paletteSkin", {})

viol = []          # (номер, класс, слоты, суть)
def V(klass, sids, text):
    viol.append((klass, sids, text))

# ── послотовая таблица ──────────────────────────────────────────────────
print(f"{'N':<3}{'Y':<6}{'раса':<22}{'кин':<4}{'BT':<7}{'палитра':<10}"
      f"{'пред':<6}{'состав':<7}{'флаги'}")
implied_mismatch_rplus, implied_drift = [], []
per_slot_flags = {}
for s in slots:
    pos = " ".join(s["pos"])
    implied = gates.rating_implied(pos, rt_cfg)
    pred = s["predicted"]["tier"]
    flags = []
    if pred == "R+" and implied != "R+":
        flags.append(f"ЛОЖНЫЙ R+ (состав {implied})")
        implied_mismatch_rplus.append(s["n"])
    elif pred == "R" and implied == "PG-13":
        flags.append(f"ДРЕЙФ R→PG-13")
        implied_drift.append(s["n"])
    # В32: фишечки-ФОРМЫ
    fich = len(s["marks"]) + (1 if s.get("gimmick") else 0) + \
           (1 if s.get("oc_hook") else 0) + 1  # body prose всегда
    if fich < 2:
        flags.append(f"В32 фишечек {fich} < 2")
    # В36: палитра → кожа (color → bridge → skin в окне)
    skin_words = {w.lower() for w in ps_cfg.get("skin_words", [])}
    bridges = {b.lower() for b in ps_cfg.get("bridges", [])}
    colors = {c.lower() for c in ps_cfg.get("color_words", [])}
    toks = re.findall(r"[A-Za-z0-9_'-]+", pos.lower())
    bleed = False
    for i, t in enumerate(toks):
        if t in skin_words:
            w0 = max(0, i - 5)
            win = toks[w0:i]
            if any(c in win for c in colors) and any(b in win for b in bridges):
                bleed = True
    if bleed:
        flags.append("В36 палитра→кожа")
    # RF рас: повтор > 2 посчитаем на уровне батча
    race = races_reg.get(s["race"], {})
    is_kin = s["race"] != "R01"
    name = f"{s['race']} {race.get('name','')[:15]}"
    per_slot_flags[s["n"]] = flags
    print(f"{s['n']:<3}{s['y_card']:<6}{name:<22}{'кин' if is_kin else 'hum':<4}"
          f"{s['bodytype']:<7}{s['palette'][-8:]:<10}{pred:<6}{implied:<7}"
          f"{'; '.join(flags)}")

# ── причины (нарушения) ────────────────────────────────────────────────
kin_n = sum(1 for s in slots if s["race"] != "R01")
races_c = Counter(s["race"] for s in slots)
scenes_c = Counter(s["scene"] for s in slots)
hair_c = Counter(s["hair"] for s in slots)
genres = [s.get("genre") for s in slots]
exq = sum(1 for g in genres if g == "EXQUISITE")
exp_cells = [s for s in slots if s.get("exp") or s["predicted"].get("exp")]
neg_all = " ".join(" ".join(s["neg"]) for s in slots)

if kin_n > 10:
    V("В40 кин-основа", "весь батч",
      f"кинов {kin_n}/21 (окно policy v2.0 — 0–10, человек основа); "
      f"human {races_c.get('R01', 0)} — генератор не различает кин/human")
if implied_mismatch_rplus:
    V("В43 ложный R+", [f"P{n:02d}" for n in implied_mismatch_rplus],
      f"предикт по классу карты+коридору, состав POS по модели В43 несёт R — "
      f"{len(implied_mismatch_rplus)} слотов")
if implied_drift:
    V("В43 дрейф R→PG-13", [f"P{n:02d}" for n in implied_drift],
      f"R-слоты без R-доказательства составом ({len(implied_drift)} шт.)")
if all(g is None for g in genres):
    V("В39 жанры не моделируются", "весь батч",
      "в манифесте нет жанрового токена VOLT/NICHE/EXQUISITE — вольт-ядро, "
      "перемешивание и УЛЬТРА-регистр физически не проверяемы (hard-гейт "
      "«жанр в шапке» на болванках не исполняется)")
if exq == 0:
    V("В41 EXQUISITE=0", "весь батч",
      "ультра-регистр в болванках отсутствует: 1–4 EXQUISITE-мейна на батч — "
      "закон, ни одна болванка его не катает")
V("В42 EXP-клеток нет", "весь батч",
  "тест-горн не генерит EXP-клеток вовсе: полка гипотез (H-XX) не катается, "
  "протокол «EXP проверяет штуки» в прогонах не живёт")
V("§2 hard-флор NEG", "весь батч",
  "в NEG болванок нет «candle, lamp» — обязательный юнит света-закона v2 "
  "(реальные батчи несут в первой строке; болванки учат рендер без пола)")
rf_bad = {r: c for r, c in races_c.items() if c > 2}
if rf_bad:
    V("RF рас > 2", list(rf_bad),
      f"раса использована {rf_bad} раз — RF-кап 2 не enforcement в ролле")
# статусы: карантин/retired
bad_status = [(s["race"], races_reg.get(s["race"], {}).get("status"))
              for s in slots
              if races_reg.get(s["race"], {}).get("status") not in ("active", "gold")]
if bad_status:
    V("статусы рас не фильтруются", sorted({r for r, _ in bad_status}),
      f"ролл берёт любые не-BAN расы: {bad_status} — карантин R30 и прочие "
      f"статусы назначаются (races.json статусы игнорируются)")
scene_bad = {k: v for k, v in scenes_c.items() if v > 2}
if scene_bad:
    V("сцены без ротации", list(scene_bad),
      f"сцена-регистр скатывается в повтор: {scene_bad} — реестр пре-гардероба "
      f"требует разнообразия сцен")
hair_bad = {k: v for k, v in hair_c.items() if v > 1}
if hair_bad:
    V("причёски повторяются", f"{len(hair_bad)} цветов ×2",
      "салон-ротация (LAWS §15) на болванках не катается — hair-библиотека "
      "большая, повтор цвета в 21 слоте не нужен")
v32_bad = [n for n, f in per_slot_flags.items() if any("В32" in x for x in f)]
if v32_bad:
    V("В32 фишечки < 2", [f"P{n:02d}" for n in v32_bad],
      f"слоты без 2+ фишечек-ФОРМ ({len(v32_bad)} шт.) — метки 0 + кин без "
      f"гиммика/лайт-хука оставляют кадр пустым")
if "nude" in neg_all:
    V("NEG-дисциплина: «nude»", "R/PG-13 слоты",
      "генератор добавляет «nude» в NEG не-R+ слотов — юнита нет в реестре "
      "negBase (реальные батчи его не несут); негатив живёт по реестру, не по "
      "самодеятельности")
V("main-спред не enforcement", "код roll()",
  "tiers перемешиваются и назначаются, но предикт может молча понизить слот "
  "до PG-13 («нет стака одежды») — Закон 24 R+×14 · R×7 держится на честном "
  "слове, инвариант check не сверяет фактический спред")
V("сходимость А не измеряется", "весь батч",
  "compare требует триажа рендеров в инбоксе — для TB-кадров их нет, "
  "сходимость предикт↔факт с эпохи ЦИКЛА 4 не измерялась ни разу")
V("coverage не обновляется роллом", "процесс",
  "roll() пишет батч, но coverage-ledger обновляется отдельной командой — "
  "пролить легко: болванка катана, покрытие не залогировано")

print("\n=== ПРИЧИНЫ (нарушения) ===")
for i, (klass, sids, text) in enumerate(viol, 1):
    print(f"{i:>2}. [{klass}] {text}\n    слоты: {sids}")
print(f"\nИТОГО причин: {len(viol)}")
