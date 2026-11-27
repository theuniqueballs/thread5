#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ПРЕ-ГАРДЕРОБ (пункт Ж, dresser.json v1.4.0): свежие комбо одежды под
жребийные Y-карты ПЕРЕД батчем.

Закон (specs/dresser.json → pregarderobe):
  (1) жребий партии → список Y-карт → класс экспозиции каждой
  (2) матрица y_stack: полки-источники + канал-партнёр + gar_f
  (3) кубик по пересечению exposure∋класс ∩ fit∋категория сцены
  (4) 2–3 вещи с РАЗНЫХ полок + аксессуар (AC)
  (5) реестр наборов (_ledger.json): НАБОР в КУЛДАУНЕ — повтор запрещён
      3 сданные партии (зеркально окну ротации), затем набор СВОБОДЕН;
      вечного бана нет (вердикт автора 2026-11-23: «комбо не должны
      навсегда баниться, это тупость» — аудит Коула R8 «cooldown наборов,
      не eternal unique»)
  (6) запись specs/pregarderobe/<batch>.json

Использование:
  python3 tools/pregarment.py --for T5-29 --y Y442,Y316,Y237 \
      [--scene street,lounge,street,...] [--seed 42] [--dry]

Тест-горн (tools/testforge.py) импортирует roll_combo тем же кубиком.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SPEC = ROOT / "specs"
PG_DIR = SPEC / "pregarderobe"
LEDGER = PG_DIR / "_ledger.json"

import spec_io  # noqa: E402  (тикет #4: единый канон сериализации specs/*.json)

# Кулдаун набора: сколько СДАННЫХ партий подряд набор не может повториться
# (зеркально окну ротации LAWS §7). Вечный бан снят вердиктом автора
# 2026-11-23 («комбо не должны навсегда баниться, это тупость»),
# лечение по Коулу R8: «cooldown наборов, не eternal unique».
COOLDOWN_BATCHES = 3

BATCH_NUM_RE = re.compile(r"(?:T5|TB|SO)-(\d+)")

SCENES = ["swim", "lounge", "street", "active", "formal", "specialty", "intimates"]


def load_closet() -> dict:
    return json.loads((SPEC / "closet.json").read_text(encoding="utf-8"))


def load_matrix() -> dict:
    d = json.loads((SPEC / "dresser.json").read_text(encoding="utf-8"))
    return d["y_stack"]["matrix"]


def load_ledger() -> dict:
    if LEDGER.exists():
        led = json.loads(LEDGER.read_text(encoding="utf-8"))
    else:
        led = {"version": "1.0.0", "combos_used": {}}
    # миграция 1.0.0 → 1.1.0 (кулдаун вместо вечного бана): старые записи
    # остаются как есть — их «batch» несёт партию, кулдаун считается от неё
    led.setdefault("version", "1.0.0")
    led.setdefault("combos_used", {})
    led["policy"] = {
        "cooldown_batches": COOLDOWN_BATCHES,
        "law": "НАБОР в кулдауне 3 сданные партии (зеркально окну ротации), затем свободен; вечного бана нет (вердикт автора 2026-11-23, Коул R8)",
    }
    return led


def save_ledger(led: dict) -> None:
    PG_DIR.mkdir(parents=True, exist_ok=True)
    spec_io.dump_spec(LEDGER, led)  # тикет #4: единый канон сериализации


def combo_key(codes: list[str]) -> str:
    return hashlib.sha1("|".join(sorted(codes)).encode()).hexdigest()[:16]


def batch_no_of(label: str) -> int | None:
    """Номер партии из метки («T5-30» → 30; «test»/мусор → None)."""
    m = BATCH_NUM_RE.search(str(label or ""))
    return int(m.group(1)) if m else None


def combo_blocked(ledger: dict, key: str, batch_no: int | None) -> bool:
    """Кулдаун набора (вместо вечного бана, вердикт автора 2026-11-23).

    Набор заблокирован, если его последнее использование — внутри окна
    кулдауна (COOLDOWN_BATCHES партий до текущей). Записи без читаемого
    номера партии (мусорная метка) и вызов без номера партии (batch_no
    None — прямой вызов roll_combo без контекста партии) блокируются
    консервативно: свежесть важнее переброса, старший прецедент — кубик
    перебрасывает, а не возвращает катаное."""
    entry = (ledger.get("combos_used") or {}).get(key)
    if not entry:
        return False
    last_no = batch_no_of(entry.get("batch", ""))
    if last_no is None or batch_no is None:
        return True
    return 0 < batch_no - last_no <= COOLDOWN_BATCHES


def candidates_for(class_: str, scene: str, closet: dict, matrix: dict) -> list[dict]:
    """Вещи-кандидаты: полки матрицы класса ∩ exposure∋класс ∩ fit∋категория.
    Пусто → фильтр сцены ослабляется (одежда-совместимость важнее сцены,
    зеркально закону y_stack «пустое пересечение → переброс»)."""
    row = matrix.get(class_)
    if row is None:
        return []
    out = []
    for shelf in row["shelves"]:
        sh = closet["shelves"].get(shelf)
        if not sh:
            continue
        for it in sh["items"]:
            if class_ in it.get("exposure", []) and scene in it.get("fit", []):
                out.append({**it, "shelf": shelf})
    if out:
        return out
    # ослабление: без сцены
    for shelf in row["shelves"]:
        sh = closet["shelves"].get(shelf)
        if not sh:
            continue
        for it in sh["items"]:
            if class_ in it.get("exposure", []):
                out.append({**it, "shelf": shelf})
    return out


def roll_combo(rng: random.Random, y_card: dict, scene: str, closet: dict,
               matrix: dict, ledger: dict, tries: int = 40,
               batch_no: int | None = None) -> dict:
    """Одно свежее комбо под Y-карту. Класс «—» → geometry_only (без стака).

    batch_no — номер партии, под которую катаем (кулдаун набора считается
    от него); None — прямой вызов без контекста партии: катаные наборы
    блокируются консервативно (прецедент кубика: переброс, не реюз)."""
    comp = y_card.get("components") or {}
    class_ = (comp.get("exposure") or {}).get("class", "—")
    base = {
        "y_card": y_card["id"],
        "class": class_,
        "corridor": y_card.get("corridor", "—"),
        "scene": scene,
    }
    if class_ not in matrix:
        return {**base, "geometry_only": True,
                "note": "класс «—»: геометрия позы несёт кадр, стак одежды не нужен (yStack skip)"}
    row = matrix[class_]
    cands = candidates_for(class_, scene, closet, matrix)
    if not cands:
        return {**base, "empty_crossing": True,
                "note": "пустое пересечение — карта перебрасывается (закон y_stack), не одежда"}
    acc_pool = [it for it in closet["shelves"].get("AC", {}).get("items", [])
                if class_ in it.get("exposure", [])]
    used = ledger["combos_used"]
    last_reason = ""
    for _ in range(tries):
        n_items = rng.choice([2, 2, 3])
        picked, shelves_used = [], set()
        pool = list(cands)
        rng.shuffle(pool)
        for it in pool:
            if len(picked) >= n_items:
                break
            if it["shelf"] in shelves_used:
                continue
            picked.append(it)
            shelves_used.add(it["shelf"])
        if len(picked) < 2:
            last_reason = "мало полок в пересечении"
            continue
        codes = [p["code"] for p in picked]
        if combo_blocked(ledger, combo_key(codes), batch_no):
            last_reason = "набор в кулдауне (последние 3 партии) — переброс"
            continue
        accessory = None
        if acc_pool and rng.random() < 0.6:
            accessory = rng.choice(acc_pool)["code"]
        return {
            **base,
            "channel": row["channel"],
            "gar_f": row["gar_f"],
            "codes": [{"code": p["code"], "name": p["name"], "pos": p["pos"],
                       "shelf": p["shelf"], "hook": p.get("hook", "")} for p in picked],
            "accessory": accessory,
            "combo_key": combo_key(codes + ([accessory] if accessory else [])),
        }
    # исчерпание свежих наборов — комбо с одной новой вещью (документируем)
    picked, shelves_used = [], set()
    pool = list(cands)
    rng.shuffle(pool)
    for it in pool:
        if len(picked) >= 2:
            break
        if it["shelf"] in shelves_used:
            continue
        picked.append(it)
        shelves_used.add(it["shelf"])
    codes = [p["code"] for p in picked]
    return {
        **base,
        "channel": row["channel"],
        "gar_f": row["gar_f"],
        "codes": [{"code": p["code"], "name": p["name"], "pos": p["pos"],
                   "shelf": p["shelf"], "hook": p.get("hook", "")} for p in picked],
        "accessory": None,
        "combo_key": combo_key(codes),
        "note": f"свежие наборы исчерпаны ({last_reason}) — комбо с минимальным пересечением, разрешено законом",
    }


def roll_batch(batch: str, y_ids: list[str], scenes: list[str] | None, seed: int,
               closet: dict | None = None, matrix: dict | None = None,
               dry: bool = False) -> dict:
    camera = json.loads((SPEC / "camera.json").read_text(encoding="utf-8"))
    cards = {c["id"]: c for c in camera["y_cards"]["cards"]}
    closet = closet or load_closet()
    matrix = matrix or load_matrix()
    ledger = load_ledger()
    rng = random.Random(seed)
    combos = []
    for i, yid in enumerate(y_ids):
        card = cards.get(yid)
        if card is None:
            sys.exit(f"нет Y-карты {yid} в camera.json")
        scene = scenes[i] if scenes and i < len(scenes) else SCENES[rng.randrange(len(SCENES))]
        combo = roll_combo(rng, card, scene, closet, matrix, ledger,
                           batch_no=batch_no_of(batch))
        combos.append(combo)
        if "combo_key" in combo and combo.get("combo_key") and not combo.get("note", "").startswith("свежие"):
            ledger["combos_used"][combo["combo_key"]] = {
                "batch": batch, "y_card": yid, "at": datetime.now(timezone.utc).isoformat()}
    out = {
        "batch": batch,
        "born": datetime.now(timezone.utc).isoformat(),
        "seed": seed,
        "law": "specs/dresser.json v1.4.0 → pregarerobe: свежие комбо под жребий, набор в кулдауне 3 сданные партии (зеркально окну ротации), затем свободен — вечного бана нет (вердикт автора 2026-11-23, Коул R8)",
        "combos": combos,
    }
    if not dry:
        PG_DIR.mkdir(parents=True, exist_ok=True)
        spec_io.dump_spec(PG_DIR / f"{batch}.json", out)  # тикет #4: канон
        save_ledger(ledger)
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description="пре-гардероб: свежие комбо под жребийные Y-карты")
    ap.add_argument("--for", dest="batch", required=True, help="метка партии (T5-29 / TB-...)")
    ap.add_argument("--y", required=True, help="Y-карты через запятую (жребий партии)")
    ap.add_argument("--scene", default="", help="категории сцены через запятую (по слотам; иначе кубик)")
    ap.add_argument("--seed", type=int, default=None, help="сид кубика (детерминизм)")
    ap.add_argument("--dry", action="store_true", help="не писать файлы, только печать")
    a = ap.parse_args()

    y_ids = [x.strip() for x in a.y.split(",") if x.strip()]
    scenes = [x.strip() for x in a.scene.split(",") if x.strip()] or None
    bad = [s for s in (scenes or []) if s not in SCENES]
    if bad:
        sys.exit(f"неизвестные категории сцены: {bad}; доступны {SCENES}")
    seed = a.seed if a.seed is not None else random.randrange(10**9)

    out = roll_batch(a.batch, y_ids, scenes, seed, dry=a.dry)
    stacked = [c for c in out["combos"] if "codes" in c]
    geo = [c for c in out["combos"] if c.get("geometry_only")]
    empty = [c for c in out["combos"] if c.get("empty_crossing")]
    print(f"пре-гардероб {a.batch}: {len(out['combos'])} карт — стак {len(stacked)} · "
          f"геометрия {len(geo)} · пустой кросс {len(empty)} · сид {seed}")
    for c in out["combos"]:
        if "codes" in c:
            codes = " + ".join(x["code"] for x in c["codes"])
            acc = f" + {c['accessory']}" if c.get("accessory") else ""
            print(f"  {c['y_card']} [{c['class']}/{c['scene']}] → {codes}{acc}")
        else:
            print(f"  {c['y_card']} [{c.get('class','—')}] → {c.get('note','')}")


if __name__ == "__main__":
    main()
