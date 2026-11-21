#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ТЕСТ-ГОРН (заказ автора 2026-11-21, пункты А/Б/Г/В):
«собирай варианты того что может быть сгенерировано (тестовые батчи-болванки),
собирай позитив и негатив, чтобы всё прогонять-прогонять-прогонять без конца
и края. Тестовые батчи могут не отображаться в основном пуле, они нужны
только тебе»

Цели, зашитые в инварианты:
  А — сходиться с предполагаемым рейтингом: каждый слот несёт predicted
      {tier, corridor, class, channel}; проверка — сигналы тира в POS
      (rating-recipes) и запрет верхних сигналов; факт (генерация+триаж)
      сверяется командой compare по inbox/meta.json.
  Б — полная осведомлённость: манифест слота перечисляет ВСЁ, из чего собран
      промпт (Y-карта, раса, clarifiers, типаж, метки, комбо пре-гардероба,
      палитра, кинетика, гиммик, oc_hook) — ни одной скрытой детали.
  В — тег-порядок: OPENER по регистрам raw-plus v2.3.0 (проверка tag_order).
  Г — ничего не забывается: coverage-ledger помнит использование каждого
      кода всех пулов; coverage — отчёт «что никогда не каталось».

Команды:
  python3 tools/testforge.py roll  --n 12 --seed 42
  python3 tools/testforge.py check  [--batch TB-...] | all
  python3 tools/testforge.py coverage
  python3 tools/testforge.py compare [--batch TB-...]

Хранилище: tests/test-corpus/TB-<дата>-<seed>.json — ВНЕ batches/, прилавок
болванок не видит (store.ts читает только batches/). Прогонять без конца и
края: каждый roll — новый сид.
"""
from __future__ import annotations

import argparse
import json
import random
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SPEC = ROOT / "specs"
CORPUS = ROOT / "tests" / "test-corpus"
sys.path.insert(0, str(ROOT / "tools"))
import pregarment as pg  # noqa: E402  (кубик пре-гардероба — тот же закон)

LINE_CAP = 200          # «не башенка»: физическая строка ≤200 знаков
CLAIM_TOKEN_CAP = 60    # закон салиенса
PRIMARY_TOKEN_WINDOW = 45  # основное — в первых ~40 токенах (+допуск)
SCENES = pg.SCENES

# чистые английские R+-сигналы по классу экспозиции (матрица y_stack несёт
# закон-строку с русским разбором — POS нужен рисуемый токен)
SIGNALS_RPLUS = {
    "COVER": "arms covering chest",
    "PROCESS": "half-off garment",
    "LINGERIE": "covered nipples",
    "CLOTHED-TIGHT": "clothed nipples",
    "SHEER": "see-through",
}

QUALITY = "masterpiece, best quality, absurdres, intricate details"
NEG_SAFETY = ["young girl, immature body, oversized head, loli, shota",
              "signature, watermark, artist name, logo, 1boy",
              "photorealistic, 3d face, realistic facial structure, bad anatomy, extra fingers, bad hands"]
NEG_ANTIWASH = "washed-out, faded colors, low contrast, flat colors, muddy colors, dull, overexposed, underexposed, pastel colors, muted colors, gray palette, pale colors, desaturated, white haze, milky fog, soft focus, hazy"

def load(name: str) -> dict:
    return json.loads((SPEC / name).read_text(encoding="utf-8"))

def wrap_lines(text: str, cap: int = LINE_CAP) -> list[str]:
    """Разбивка до cap знаков: по запятым (печь T5-28), сверхдлинные куски —
    по словам; склейка через пробел восстанавливает исходный текст 1:1
    (клеймо-паттерн не ломается)."""
    segs: list[tuple[str, str]] = []  # (sep_before, piece)
    for chunk in text.split(", "):
        if len(chunk) <= cap:
            segs.append((", " if segs else "", chunk))
        else:
            head = chunk
            while len(head) > cap:
                cut = head.rfind(" ", 1, cap)
                if cut <= 0:
                    cut = cap
                segs.append((" " if segs else "", head[:cut]))
                head = head[cut:].lstrip()
            if head:
                segs.append((" " if segs else "", head))
    out, cur = [], ""
    for sep, piece in segs:
        if cur and len(cur) + len(sep) + len(piece) > cap:
            out.append(cur + ("," if sep == ", " else ""))
            cur = piece
        else:
            cur = cur + sep + piece if cur else piece
    if cur:
        out.append(cur)
    return out

def fmt(x: str) -> str:
    return x.rstrip(" ,") + ("," if not x.rstrip().endswith(",") else "")


def cam_prose(cam_field: str, pools_cam: dict) -> str:
    """CAM-код → рисуемая проза (В34: обозначения в POS запрещены).
    CAM06_side → «side view»; голый код → sd из pools.cam; проза проходит как есть."""
    s = str(cam_field or "").strip()
    if not s:
        return "upper body three-quarter"
    m = re.match(r"CAM\d+[_ ](\w+)", s)
    if m:
        return f"{m.group(1).replace('_', ' ')} view"
    if re.match(r"CAM\d+$", s):
        for grp in ("base_axis_onotology_cam01_12", "aggressive_framing_cam13_18"):
            for it in pools_cam.get(grp, []):
                if it.get("id") == s:
                    return it.get("sd", s)
        return "upper body three-quarter"
    return s


def clean_pattern(pat: str) -> str:
    """Клеймо-паттерн без служебных хвостов: «… + CAM06_side» → чистая поза-физика
    (В34: камера доезжает прозой OPENER-кластера, не кодом)."""
    return re.sub(r"\s*\+?\s*CAM\d+\S*", "", str(pat or "")).strip(" ,")


def first_color(x) -> str:
    """accent1 бывает строкой/списком/вложенным списком — достаём первый цвет."""
    if isinstance(x, str):
        return x
    if isinstance(x, list) and x:
        return first_color(x[0])
    return "unnamed"

class Forge:
    def __init__(self) -> None:
        self.camera = load("camera.json")
        self.cards = {c["id"]: c for c in self.camera["y_cards"]["cards"]}
        self.closet = pg.load_closet()
        self.matrix = pg.load_matrix()
        self.channels = json.loads((SPEC / "dresser.json").read_text(encoding="utf-8"))["channels"]
        self.races = {r["id"]: r for r in load("races.json")["races"]
                      if not r["id"].startswith("BAN")}
        self.bodytypes = load("bodytypes.json")["types"]
        self.marks = load("marks.json")
        self.palettes = load("palettes.json")["palettes"]
        self.kinetics = load("pools.json")["sections"]["kinetics_k"]
        self.pools_cam = load("pools.json")["sections"]["cam"]
        self.he = load("hair-eye-library.json")
        self.recipes = load("rating-recipes.json")

    # ── кубики ────────────────────────────────────────────────────────
    def tier_pools(self) -> dict:
        """Стратификация как мейн-спред канона (7 R+ / 12 R / 2 PG-13 из 21):
        R+ = класс экспозиции + коридор A; R = класс + коридор ≠ A; PG-13 = класс «—»."""
        pools = {"R+": [], "R": [], "PG-13": []}
        for c in self.cards.values():
            cls = (c.get("components") or {}).get("exposure", {}).get("class", "—")
            if cls in ("COVER", "PROCESS", "LINGERIE", "CLOTHED-TIGHT", "SHEER"):
                pools["R+" if c.get("corridor") == "A" else "R"].append(c)
            else:
                pools["PG-13"].append(c)
        return pools

    def roll_y(self, rng: random.Random, tier: str, pools: dict) -> dict:
        pool = pools.get(tier) or pools["PG-13"]
        return rng.choice(pool)

    def roll_body(self, rng: random.Random) -> dict:
        return rng.choices(self.bodytypes, weights=[b["weight"] for b in self.bodytypes])[0]

    def roll_race(self, rng: random.Random) -> dict:
        ids = list(self.races)
        return self.races[rng.choice(ids)]

    def marks_for(self, rng: random.Random, race: dict, body: dict) -> tuple[list[dict], dict | None]:
        """0–3 метки (вес ~20/45/25/10) + oc_hook-кандидат (≤1, ~35% батча).
        Фильтры: kin_compat по skin_type + зона видима в кадре карты."""
        n = rng.choices([0, 1, 2, 3], weights=[20, 45, 25, 10])[0]
        skin = race.get("skin_type", "skin")
        cat_rules = self.marks["kin_compat_rules"]["category_matrix"]
        eye_ok = lambda m: True  # глаза живут на любой поверхности
        def ok(m: dict) -> bool:
            cat = m["category"]
            if cat == "eyes":
                return eye_ok(m)
            if skin in ("gel", "glass", "stone", "smoke"):
                return False
            if cat == "burn" and race["id"] in self.marks["kin_compat_rules"]["incompat_ids"]["fireproof"]:
                return False
            if cat in ("tattoo", "birthmark") and skin == "scales":
                return False
            return True
        pool = [m for m in self.marks["marks"] if not m["oc_hook"] and ok(m)]
        oc_pool = [m for m in self.marks["marks"] if m["oc_hook"] and ok(m)]
        picked, used_ids = [], set()
        while len(picked) < n and pool:
            m = rng.choice(pool)
            if m["id"] in used_ids:
                continue
            # пара к мягким типажам: серебро растяжек только на soft-рамке
            if m["id"] == "MK-F05" and body["axes"].get("frame") not in ("soft", "average"):
                continue
            picked.append(m)
            used_ids.add(m["id"])
        oc = None
        if oc_pool and rng.random() < 0.35:
            oc = rng.choice(oc_pool)
        return picked, oc

    def visible(self, mark: dict, card: dict) -> bool:
        """Зона метки видима в кадре Y-карты (approx-сверка по camera-строке)."""
        cam = str(((card.get("components") or {}).get("exposure") or {}).get("cover_object", "")) + \
              " " + str((card.get("components") or {}).get("camera", ""))
        cam_l = cam.lower()
        zmap = self.marks["visibility_pairs"]["zone_to_frame"]
        frames = zmap.get(mark["zone"], [])
        if not frames:
            return True
        # upper body / close-up / full body / back / profile — грубая рамка
        has = lambda *ws: any(w in cam_l for w in ws)
        frame_is_upper = has("upper body", "portrait", "close-up", "closeup")
        frame_is_full = has("full body", "full-body", "cowboy", "wide")
        frame_is_back = has("back", "behind")
        for f in frames:
            if f in ("close-up", "upper body", "portrait") and frame_is_upper:
                return True
            if f in ("full body", "waist-up profile", "upper body lean", "low angle") and (frame_is_full or frame_is_upper):
                return True
            if f in ("back", "profile") and (frame_is_back or has("three-quarter", "side")):
                return True
        return False

    # ── предикт рейтинга (А) ───────────────────────────────────────────
    @staticmethod
    def predict(card: dict, combo: dict) -> dict:
        cls = (card.get("components") or {}).get("exposure", {}).get("class", "—")
        corridor = card.get("corridor", "—")
        if cls == "—" or cls not in ("COVER", "PROCESS", "LINGERIE", "CLOTHED-TIGHT", "SHEER"):
            tier = "PG-13"       # В33: класс «—» не выносит R+
            why = "класс «—»: геометрия без экспозиции — заявки нет"
        elif corridor == "A":
            tier = "R+"
            why = "коридор A + класс экспозиции: объект-прикрытие/состояние несёт заряд"
        else:
            tier = "R"
            why = "коридор B: экспозиция заявлена, заряд геометрией слабее"
        return {"tier": tier, "corridor": corridor, "class": cls,
                "channel": combo.get("channel"), "why": why}

    # ── сигналы тира в POS (А) ─────────────────────────────────────────
    def tier_signals(self, pred: dict, combo: dict) -> list[str]:
        t = pred["tier"]
        if t == "R+":
            return [SIGNALS_RPLUS.get(pred["class"], "covered nipples")]
        rec = self.recipes["tiers"]["R" if t == "R" else "PG13"]
        return rec["signals"][:2]

    # ── сборка слота ───────────────────────────────────────────────────
    def roll_slot(self, rng: random.Random, idx: int, ledger: dict,
                  bt_used: dict, pal_used: dict, tier: str, pools: dict,
                  oc_hook_slot: int) -> dict:
        card = self.roll_y(rng, tier, pools)
        # типаж и палитра — с капами (≤3 на батч): переброс пока не найдём свободные
        for _ in range(30):
            body_try = self.roll_body(rng)
            pal_try = rng.choice(self.palettes)
            if (bt_used.get(body_try["id"], 0) < 3 and pal_used.get(pal_try["id"], 0) < 3):
                body, pal = body_try, pal_try
                break
        else:
            body, pal = body_try, pal_try
        bt_used[body["id"]] = bt_used.get(body["id"], 0) + 1
        pal_used[pal["id"]] = pal_used.get(pal["id"], 0) + 1
        race = self.roll_race(rng)
        scene = rng.choice(SCENES)
        combo = pg.roll_combo(rng, card, scene, self.closet, self.matrix, ledger)
        marks, _ = self.marks_for(rng, race, body)
        marks = [m for m in marks if self.visible(m, card)]
        # oc_hook — ≤1 на БАТЧ (закон marks.json): бандл ловит назначенный слот
        oc_hook = None
        if idx == oc_hook_slot:
            skin = race.get("skin_type", "skin")
            cat = None
            oc_pool = [m for m in self.marks["marks"] if m["oc_hook"]]
            for _ in range(12):
                m = rng.choice(oc_pool)
                if m["category"] == "eyes" or skin in ("skin", "mixed", "scales"):
                    cat = m
                    break
            oc_hook = cat
            if oc_hook and oc_hook["category"] != "eyes":
                marks = marks + [oc_hook]
        kin = rng.choice(self.kinetics)
        hair = rng.choice(self.he["hair"])
        base_eyes = rng.choice(self.he["eyes"])
        eye_mark = next((m for m in marks if m["category"] == "eyes"), None)
        if oc_hook and oc_hook["category"] == "eyes":
            eye_mark = oc_hook
        pred = self.predict(card, combo)
        signals = self.tier_signals(pred, combo)
        # комбо-вещи: геометрия-only карты без вещей — PG-13 сигнал из словаря
        if "codes" not in combo:
            signals = self.recipes["tiers"]["PG13"]["signals"][:2]
            pred["tier"] = "PG-13"
            pred["why"] = "нет стака одежды (геометрия/пустой кросс) — честный PG-13"

        # POS по регистрам raw-plus v2.3.0
        clar = ", ".join(race.get("clarifiers") or [])
        opener_parts = [
            QUALITY,
            f"{cam_prose((card.get('components') or {}).get('camera'), self.pools_cam)}, "
            f"{((card.get('components') or {}).get('pose') or card.get('pattern', '')).split(',')[0]}",
            "1girl, solo",
            f"{hair} hair, {base_eyes} eyes",
            clar,
            ", ".join(body["tags"]),
            kin["name"].lower().replace("_", " "),
        ]
        opener = ", ".join(p for p in opener_parts if p)
        if "codes" in combo:
            # claim-вещь — первый НЕ-аксессуар (аксессуар не заявка);
            # COVER-слот: заявка — само прикрытие (руки/скотч/объект карты)
            main_gar = next((c for c in combo["codes"] if c["shelf"] != "AC"),
                            combo["codes"][0])
            # claim = вещь (англ. pos) + состояние ткани каналом (state-теги
            # канала — англ.) + сигналы тира; gar_f — ЗАКОН для писца, в POS не идёт
            ch_states = []
            for ch_key, ch in self.channels.items():
                if ch_key in str(combo.get("channel", "")):
                    states = [s for s in ch.get("state", []) if "(" not in s]
                    if pred["tier"] != "R+":
                        # жёсткие R+-сигналы не едут в R-слот (сходство предикта А)
                        hard = set(self.recipes["tiers"]["RPLUS"]["signals"] +
                                   self.recipes["tiers"]["RPLUS"].get("signals_hard", []))
                        states = [s for s in states if s not in hard]
                    ch_states = states[:2]
                    break
            claim_noun = ("the cover" if (pred["class"] == "COVER" and pred["tier"] == "R+")
                          else f"the {main_gar['name'].lower()}")
            claim_core = (f"{main_gar['pos']}"
                          + (f", {', '.join(ch_states)}" if ch_states else "")
                          + ", nothing underneath"
                          + f", {'; '.join(signals)} — {claim_noun} is the claim, "
                          f"{card['id']}-made")
        else:
            claim_core = (f"{', '.join(signals)} — the frame is the claim, {card['id']}-made")
        weave = clean_pattern(card.get("pattern", ""))
        scene_bits = [m["pos"] for m in marks]
        if race.get("gimmick"):
            scene_bits.append(race["gimmick"])
        if oc_hook and oc_hook["category"] != "eyes":
            scene_bits.append(oc_hook["pos"])
        scene_bits.append(body["prose"])
        if race.get("light_hook"):
            scene_bits.append(race["light_hook"])
        scene_line = ", ".join(scene_bits)
        accent = first_color(pal.get("accent1") or pal.get("dominant"))
        pal_frag = pal.get("sd_fragment") or f"{pal['dominant'][0]} dominant, {pal.get('light_type', 'clean light')}"
        palette_line = (f"{pal_frag}, {accent} accent; her colors: {pal['name']}")
        eye_txt = eye_mark["pos"] if eye_mark else f"{base_eyes}"
        face_line = (f"stylized 2D anime face, anime eyes ({eye_txt}), small nose, small mouth, "
                     f"{hair} hair framing")

        pos_logical = [opener, claim_core, weave, scene_line, palette_line, face_line]
        pos_lines: list[str] = []
        for ln in pos_logical:
            pos_lines.extend(wrap_lines(ln + ","))

        # NEG по тиру
        tier_key = {"PG-13": "PG13", "R": "R", "R+": "RPLUS"}[pred["tier"]]
        counter = self.recipes["tiers"][tier_key].get("counter_neg", [])
        neg = list(NEG_SAFETY) + [NEG_ANTIWASH]
        if counter:
            neg.append(", ".join(counter[:6]))
        if pred["tier"] != "R+":
            neg.append("nude")

        slot = {
            "n": idx,
            "y_card": card["id"],
            "pattern_weaved": weave,
            "pattern_source": card.get("pattern", ""),
            "race": race["id"],
            "race_name": race["name"],
            "clarifiers": race.get("clarifiers", []),
            "gimmick": race.get("gimmick"),
            "bodytype": body["id"],
            "bodytype_tags": body["tags"],
            "marks": [m["id"] for m in marks],
            "oc_hook": {"mark": oc_hook["id"], "name": oc_hook["name"]} if oc_hook else None,
            "cl_codes": [c["code"] for c in combo.get("codes", [])],
            "gar_f": combo.get("gar_f"),
            "scene": scene,
            "palette": pal["id"],
            "kinetic": kin["id"],
            "hair": hair,
            "eyes": base_eyes if not eye_mark else "per eye-mark",
            "predicted": pred,
            "signals": signals,
            "pos": pos_lines,
            "neg": neg,
        }
        return slot


def roll(n: int, seed: int, out_path: Path | None) -> dict:
    forge = Forge()
    rng = random.Random(seed)
    ledger = pg.load_ledger()
    pools = forge.tier_pools()
    bt_used: dict = {}
    pal_used: dict = {}
    # мейн-спред канона: 7 R+ / 12 R / 2 PG-13 из 21
    tiers = (["R+"] * 7 + ["R"] * 12 + ["PG-13"] * 2)
    rng.shuffle(tiers)
    oc_hook_slot = rng.randrange(n) if rng.random() < 0.35 else -1
    slots = []
    for i in range(n):
        tier = tiers[i % len(tiers)]
        pool = pools.get(tier) or pools["PG-13"]
        if not pool:
            tier = "PG-13"
        slots.append(forge.roll_slot(rng, i + 1, ledger, bt_used, pal_used,
                                     tier, pools, oc_hook_slot))
    batch_id = f"TB-{datetime.now(timezone.utc).strftime('%Y%m%d')}-{seed}"
    doc = {
        "id": batch_id,
        "born": datetime.now(timezone.utc).isoformat(),
        "seed": seed,
        "n": n,
        "law": "тест-батч-болванка: не в batches/, прилавком не читается; цели А/Б/В/Г (testforge.py)",
        "slots": slots,
    }
    path = out_path or (CORPUS / f"{batch_id}.json")
    CORPUS.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"ролл {batch_id}: {n} слотов → {path}")
    tiers: dict = {}
    for s in slots:
        tiers[s["predicted"]["tier"]] = tiers.get(s["predicted"]["tier"], 0) + 1
    print(f"  предикт: {tiers}; типажей {len(set(s['bodytype'] for s in slots))}, "
          f"рас {len(set(s['race'] for s in slots))}, палитр {len(set(s['palette'] for s in slots))}")
    return doc


# ── check: инварианты ───────────────────────────────────────────────────
def check_batch(doc: dict, forge: Forge) -> list[str]:
    errs: list[str] = []
    b = doc["id"]
    oc_hooks = [s for s in doc["slots"] if s.get("oc_hook")]
    if len(oc_hooks) > 1:
        errs.append(f"{b}: ОС-сигнатурных меток >1 на батч ({len(oc_hooks)}) — закон marks.json")
    bt_count: dict = {}
    pal_count: dict = {}
    for s in doc["slots"]:
        sid = f"{b} P{s['n']:02d}"
        pos = s["pos"]
        text = " ".join(pos)
        # Б: манифест полон
        for f in ("y_card", "race", "bodytype", "palette", "predicted"):
            if not s.get(f):
                errs.append(f"{sid}: манифест неполон — нет {f}")
        # В: тег-порядок (OPENER = все строки до claim-строки, переноды не рвут регистры)
        opener_lines = []
        for l in pos:
            if "is the claim" in l:
                break
            opener_lines.append(l)
        opener = " ".join(opener_lines)
        if not opener.startswith("masterpiece, best quality"):
            errs.append(f"{sid}: OPENER не с квалити-тегов")
        toks = [t.strip() for t in opener.split(",")]
        try:
            i_girl = toks.index("1girl")
        except ValueError:
            errs.append(f"{sid}: нет 1girl в OPENER")
            i_girl = -1
        if i_girl != -1 and i_girl > 25:
            errs.append(f"{sid}: 1girl за пределами первичного окна ({i_girl}-й токен)")
        bt_first = next((i for i, t in enumerate(toks) if t in s["bodytype_tags"]), None)
        if bt_first is None:
            errs.append(f"{sid}: теги типажа {s['bodytype']} не в OPENER (закон тег-порядка)")
        elif bt_first > PRIMARY_TOKEN_WINDOW:
            errs.append(f"{sid}: типаж за первичным окном ({bt_first} токен)")
        if s["clarifiers"] and not all(cl in opener for cl in s["clarifiers"] if cl):
            errs.append(f"{sid}: кин-clarifiers не в OPENER целиком")
        # заявка ≤60 токенов
        claim_line = next((l for l in pos if "is the claim" in l), "")
        head = claim_line.split("—")[0] if claim_line else ""
        if len([t for t in head.split(",") if t.strip()]) > CLAIM_TOKEN_CAP:
            errs.append(f"{sid}: заявка длиннее {CLAIM_TOKEN_CAP} токенов")
        # клеймо 1:1
        if s["pattern_weaved"] and s["pattern_weaved"].rstrip(",") not in text.replace("\n", " "):
            # после переносов строк запятая может разбить паттерн — сверяем по словам
            joined = re.sub(r"\s+", " ", text)
            pat = re.sub(r"\s+", " ", s["pattern_weaved"])
            if pat not in joined:
                errs.append(f"{sid}: паттерн карты не вплетён 1:1 (строка 3)")
        # В34: служебных кодов в POS нет
        if re.search(r"CAM\d+", text):
            errs.append(f"{sid}: служебный CAM-код в POS (В34 — только проза)")
        # строки ≤200
        for i, l in enumerate(pos):
            if len(l) > LINE_CAP + 2:
                errs.append(f"{sid}: строка {i + 1} длиннее {LINE_CAP} ({len(l)})")
        # А: сигналы тира в POS
        for sig in s["signals"]:
            core = sig.split("(")[0].strip().lower()
            if core and core not in text.lower():
                errs.append(f"{sid}: сигнал тира «{sig}» не доехал в POS")
        # А: запрет верхних сигналов (PG-13/R не несут R+ hard)
        if s["predicted"]["tier"] != "R+":
            for bad in ("covered nipples", "handbra", "taped nipples", "topless with tape",
                        "cameltoe", "camel toe"):
                if bad in text.lower():
                    errs.append(f"{sid}: PG-13/R слот несёт R+ сигнал «{bad}»")
        # метки в SCENE + рейтинг-нейтральность
        marks_by_id = {m["id"]: m for m in forge.marks["marks"]}
        for mid in s["marks"]:
            m = marks_by_id.get(mid)
            if not m:
                errs.append(f"{sid}: неизвестная метка {mid}")
                continue
            if m["pos"] not in text:
                errs.append(f"{sid}: метка {mid} не в POS")
        if s.get("oc_hook"):
            m = marks_by_id.get(s["oc_hook"]["mark"])
            if m and m["pos"] not in text:
                errs.append(f"{sid}: oc_hook-метка {mid} не в POS")
        # yStack: вещь держит класс
        cls = s["predicted"]["class"]
        for code in s["cl_codes"]:
            item = None
            for shelf in forge.closet["shelves"].values():
                for it in shelf["items"]:
                    if it["code"] == code:
                        item = it
            if item and cls in ("COVER", "PROCESS", "LINGERIE", "CLOTHED-TIGHT", "SHEER"):
                if cls not in item.get("exposure", []):
                    errs.append(f"{sid}: {code} не держит класс {cls} (душилка)")
        # гиммик рисуем
        if s.get("gimmick") and s["gimmick"] not in text:
            errs.append(f"{sid}: гиммик кина не в SCENE-строке")
        # NEG: safety + анти-ваш всегда
        negtext = " ".join(s["neg"])
        if "loli" not in negtext or "washed-out" not in negtext:
            errs.append(f"{sid}: NEG без safety-префикса или анти-ваш")
        # капы
        bt_count[s["bodytype"]] = bt_count.get(s["bodytype"], 0) + 1
        pal_count[s["palette"]] = pal_count.get(s["palette"], 0) + 1
    for bt, c in bt_count.items():
        if c > 3:
            errs.append(f"{b}: типаж {bt} использован {c} раз (кап 3)")
    for pal, c in pal_count.items():
        if c > 3:
            errs.append(f"{b}: палитра {pal} использована {c} раз (кап 3)")
    return errs


def cmd_check(which: str) -> int:
    forge = Forge()
    files = sorted(CORPUS.glob("TB-*.json"))
    if which != "all":
        files = [f for f in files if f.stem == which] or files
    if not files:
        print("тест-корпус пуст — сначала roll")
        return 1
    total_errs = 0
    for f in files:
        doc = json.loads(f.read_text(encoding="utf-8"))
        errs = check_batch(doc, forge)
        status = "PASS" if not errs else f"FAIL ({len(errs)})"
        print(f"{doc['id']}: {status} — {len(doc['slots'])} слотов")
        for e in errs:
            print(f"  !! {e}")
        total_errs += len(errs)
    print(f"итог: {'PASS' if total_errs == 0 else f'FAIL — {total_errs} нарушений'} "
          f"({len(files)} тест-батчей)")
    return 0 if total_errs == 0 else 1


# ── coverage: ничего не забывается (Г) ──────────────────────────────────
def cmd_coverage() -> int:
    forge = Forge()
    led_path = CORPUS / "coverage-ledger.json"
    led = {"y_cards": {}, "races": {}, "bodytypes": {}, "marks": {}, "cl_codes": {},
           "palettes": {}, "updated": datetime.now(timezone.utc).isoformat()}
    if led_path.exists():
        led = json.loads(led_path.read_text(encoding="utf-8"))
    tb_files = sorted(CORPUS.glob("TB-*.json"))
    for f in tb_files:
        doc = json.loads(f.read_text(encoding="utf-8"))
        for s in doc["slots"]:
            for key, val in (("y_cards", s["y_card"]), ("races", s["race"]),
                             ("bodytypes", s["bodytype"]), ("palettes", s["palette"])):
                led[key][val] = led[key].get(val, 0) + 1
            for m in s["marks"]:
                led["marks"][m] = led["marks"].get(m, 0) + 1
            for c in s["cl_codes"]:
                led["cl_codes"][c] = led["cl_codes"].get(c, 0) + 1
    CORPUS.mkdir(parents=True, exist_ok=True)
    led_path.write_text(json.dumps(led, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    pools = {
        "y_cards": set(forge.cards),
        "races": set(forge.races),
        "bodytypes": {b["id"] for b in forge.bodytypes},
        "marks": {m["id"] for m in forge.marks["marks"]},
        "cl_codes": {i["code"] for sh in forge.closet["shelves"].values() for i in sh["items"]},
        "palettes": {p["id"] for p in forge.palettes},
    }
    print(f"покрытие пулов (тест-корпус: {len(tb_files)} батчей):")
    for k, full in pools.items():
        used = set(led[k])
        never = sorted(full - used, key=str)
        pct = round(100 * len(used) / len(full)) if full else 100
        print(f"  {k}: {len(used)}/{len(full)} ({pct}%) · никогда: "
              f"{', '.join(never[:8])}{'…' if len(never) > 8 else '' if never else '— всё катано'}")
    return 0


# ── compare: предикт ↔ факт (А) ────────────────────────────────────────
def cmd_compare(which: str, meta_path: Path | None = None,
                corpus_dir: Path | None = None,
                convergence_path: Path | None = None) -> int:
    meta_path = meta_path or (ROOT / "inbox" / "meta.json")
    corpus = corpus_dir or CORPUS
    if not meta_path.exists():
        print("inbox/meta.json нет — сгенируй и прогрузи тестовые кадры в инбокс (тег «TB-… P01»)")
        return 1
    items = json.loads(meta_path.read_text(encoding="utf-8"))
    if isinstance(items, dict):
        items = items.get("items", [])
    tb = [i for i in items if (i.get("tag") or "").upper().startswith("TB-")
          and i.get("identity")]
    if not tb:
        print("нет триажённых тест-кадров (нужен тег «TB-…» + identity после разбора)")
        return 1
    files = sorted(corpus.glob("TB-*.json"))
    preds = {}
    for f in files:
        doc = json.loads(f.read_text(encoding="utf-8"))
        for s in doc["slots"]:
            preds[(doc["id"].upper(), f"P{s['n']:02d}")] = s["predicted"]["tier"]
    rows, matched, misses = [], 0, []
    by_tier: dict = {}
    for i in tb:
        tag = (i["tag"] or "").upper()
        m = re.match(r"(TB-\S+)\s+P(\d+)", tag)
        if not m:
            continue
        key = (m.group(1), f"P{int(m.group(2)):02d}")
        if key not in preds:
            continue
        fact = i["identity"].get("rating")
        pred = preds[key]
        ok = fact == pred
        matched += int(ok)
        by_tier.setdefault(pred, {"n": 0, "ok": 0})
        by_tier[pred]["n"] += 1
        by_tier[pred]["ok"] += int(ok)
        if not ok:
            misses.append({"tag": i["tag"], "predicted": pred, "fact": fact,
                           "note": i["identity"].get("note", "")})
        rows.append({"tag": i["tag"], "predicted": pred, "fact": fact, "ok": ok})
    total = len(rows)
    out = {"updated": datetime.now(timezone.utc).isoformat(), "total": total,
           "matched": matched, "convergence": round(matched / total, 3) if total else None,
           "by_tier": by_tier, "misses": misses, "rows": rows}
    (convergence_path or CORPUS / "convergence.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"сходимость предикт↔факт: {matched}/{total}"
          f"{f' = {round(100 * matched / total)}%' if total else ''}")
    for t, v in sorted(by_tier.items()):
        print(f"  {t}: {v['ok']}/{v['n']}")
    for x in misses[:10]:
        print(f"  !! {x['tag']}: предикт {x['predicted']} / факт {x['fact']} — {x['note']}")
    print("отчёт: tests/test-corpus/convergence.json")
    return 0


def main() -> None:
    ap = argparse.ArgumentParser(description="тест-горн: батчи-болванки для бесконечных прогонов")
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("roll", help="ролл тест-батча")
    r.add_argument("--n", type=int, default=12)
    r.add_argument("--seed", type=int, default=None)
    c = sub.add_parser("check", help="инварианты тест-батчей")
    c.add_argument("--batch", default="all")
    sub.add_parser("coverage", help="аудит покрытия пулов (ничего не забывается)")
    cm = sub.add_parser("compare", help="сходимость предикт↔факт по inbox")
    cm.add_argument("--batch", default="all")
    a = ap.parse_args()
    if a.cmd == "roll":
        seed = a.seed if a.seed is not None else random.randrange(10**9)
        roll(a.n, seed, None)
        sys.exit(cmd_check("all") and 0 or 0)
    elif a.cmd == "check":
        sys.exit(cmd_check(a.batch))
    elif a.cmd == "coverage":
        sys.exit(cmd_coverage())
    elif a.cmd == "compare":
        sys.exit(cmd_compare(a.batch))


if __name__ == "__main__":
    main()
