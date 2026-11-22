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
      сверяется командой compare по inbox/meta.json. С PROTO-2 (2026-11-22,
      протокол «пробы и ошибки» по вердикту T5-29): предикт — ЧЕСТНЫЙ ПО
      СОСТАВУ (gates.rating_implied, В43): POS собирается до тира, ретраи
      пока состав несёт таргет; predicted.tier ≡ rating_implied(POS).
  Б — полная осведомлённость: манифест слота перечисляет ВСЁ, из чего собран
      промпт (Y-карта, раса, clarifiers, типаж, метки, комбо пре-гардероба,
      палитра, кинетика, гиммик, oc_hook, ЖАНР) — ни одной скрытой детали.
  В — тег-порядок: OPENER по регистрам raw-plus v2.3.0 (проверка tag_order).
  Г — ничего не забывается: coverage-ledger помнит использование каждого
      кода всех пулов; coverage — отчёт «что никогда не каталось»; PROTO-2:
      ролл обновляет ledger сам, пролить невозможно.
  Д — СКЕЛЕТ-ЗАКОНЫ УРОКА T5-29 (PROTO-2, В39–В43): жанры VOLT/NICHE/
      EXQUISITE по Закону 24 (вольт-масса ≥ 13, ниша 5–8, EXQUISITE 1–4,
      бег жанра ≤ 3 — вперемешку); кины — опция (≤ 10/21, человек основа);
      EXP-клетки несут H-XX из specs/open-hypotheses.json (≤2 клеток на
      гипотезу, тема не кастует); NEG несёт hard-флор «candle, lamp»;
      карты вне окна последних 3 СДАННЫХ партий и без дублей; расы — только
      active/gold, вне канон-локов ОС, RF ≤ 2.

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

# ── PROTO-2: скелет-законы урока T5-29 (В39–В43) ─────────────────────
PROTO = 2               # версия протокола болванок (1 — до урока T5-29)
KIN_CAP = 10            # В40: кины — опция, ≤ 10 из 21 мейна (человек — основа)
RACE_RF = 2             # RF-кап расы в батче
VOLT_MIN, NICHE_MIN, NICHE_MAX = 13, 5, 8   # В39: вольт-ядро
EXQ_MIN, EXQ_MAX = 1, 4                            # В41: ультра в мейнах
GENRE_MAX_RUN = 3       # В39: вперемешку, не блоками
SCENE_CAP = 3           # ротация сцен (7 сцен × ≤3)
EXP_MAX_PER_HYP = 2     # В42: A/B-пара = одна переменная
WINDOW_DEPTH = 3        # окно ротации: последние 3 СДАННЫХ партии

# честные R+-сигналы по В43 (состав, не класс карты): транзиентный холд
# руками (handHold) или bare-line со стрэпами (strapOnly). Панельные
# «covered nipples» — R-потолок, в R+-слот не катятся (PROTO-1 причина №23)
SIGNALS_RPLUS_HONEST = {
    "COVER": "arms covering chest",                      # handHold
    "PROCESS": "hauling the garment with both fists",    # handHold
    "LINGERIE": "straps covering the chest's bare line",  # strapOnly
    "CLOTHED-TIGHT": "straps covering the chest's bare line",
    "SHEER": "arms covering chest",                      # руки сквозь просвет
}

QUALITY = "masterpiece, best quality, absurdres, intricate details"
NEG_SAFETY = ["young girl, immature body, oversized head, loli, shota",
              "signature, watermark, artist name, logo, 1boy, candle, lamp",
              "photorealistic, 3d face, realistic facial structure, bad anatomy, extra fingers, bad hands"]
# PROTO-2: «candle, lamp» — hard-флор света v2 (LAWS §2) обязателен в NEG;
# «nude» убран — юнит вне реестра negBase (PROTO-1 причина №13)
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
        # ── PROTO-2: законы урока T5-29 ────────────────────────────
        # В43: предикт — по составу POS (модель печи), не по классу карты
        import gates as gates_mod
        self.rating_cfg = gates_mod.GATES["ratingTruth"]
        self.rating_implied = gates_mod.rating_implied
        # канон-локи: расы действующих ОС не катятся пулом (LAWS §21.4)
        canon = load("oc-canon.json")
        self.canon_races: set[str] = set()
        for oc in canon["ocs"].values():
            m = re.match(r"(R\d{2})", str(oc.get("race", "")))
            if m and oc.get("active", True):
                self.canon_races.add(m.group(1))
        # окно ротации: Y-карты последних WINDOW_DEPTH СДАННЫХ партий (t5delivery)
        self.window_cards: set[str] = set()
        try:
            import t5delivery
            for p in t5delivery.delivered_batches()[-WINDOW_DEPTH:]:
                self.window_cards |= set(
                    re.findall(r"\bY\d{1,3}\b",
                               Path(p).read_text(encoding="utf-8")))
        except Exception:
            pass  # окно пусто — болванкам разрешено всё (гейт окна — на бою)
        # полка гипотез для EXP-клеток (В42)
        self.hyp_shelf = [h["id"] for h in load("open-hypotheses.json")["hypotheses"]]

    # ── кубики ────────────────────────────────────────────────────────
    def tier_pools(self) -> dict:
        """Стратификация как мейн-спред канона (R+×14 · R×7 из 21 — Закон 24,
        восстановлен вердиктом T5-29 В39): R+ = класс экспозиции + коридор A;
        R = класс + коридор ≠ A; PG-13 = класс «—» (только EXP-клетки).
        PROTO-2: карты окна последних СДАННЫХ партий исключены (причина №8)."""
        pools = {"R+": [], "R": [], "PG-13": []}
        for cid, c in self.cards.items():
            if cid in self.window_cards:
                continue
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

    def roll_race(self, rng: random.Random, kin_used: int = 0,
                  rf_used: dict | None = None,
                  kin_cap: int = KIN_CAP) -> dict:
        """PROTO-2 (В40 + причины №7/№15/№16): человек — основа, кин — опция.
        Статусы active/gold только; канон-локи действующих ОС исключены
        (LAWS §21.4); RF ≤ 2 (R01 — основа, вне RF); kin_cap — только мейны
        (EXP-клетки-кандидаты — отдельная статья)."""
        rf_used = rf_used if rf_used is not None else {}
        human = self.races.get("R01")
        if human is None or kin_used >= kin_cap:
            return human
        pool = [
            r for rid, r in self.races.items()
            if rid != "R01"
            and r.get("status") in ("active", "gold")
            and rid not in self.canon_races
            and rf_used.get(rid, 0) < RACE_RF
        ]
        if not pool:
            return human
        picked = rng.choice(pool)
        rf_used[picked["id"]] = rf_used.get(picked["id"], 0) + 1
        return picked

    def genre_plan(self, rng: random.Random, n: int) -> list[str]:
        """PROTO-2 (В39/В41): жанровый скелет Закона 24 с перемешиванием.
        NICHE×7 (5–8) + вольт-масса ≥ 13 (VOLT + EXQUISITE 1–4), бег ≤ 3.
        NICHE ⇒ тир R, VOLT/EXQUISITE ⇒ тир R+ (вольт — жанр плоти R+/X,
        ниша — чудо R: связка канона, LAWS §5)."""
        if n >= VOLT_MIN + NICHE_MIN:          # вольт-ядро помещается целиком
            niche = min(NICHE_MAX, max(NICHE_MIN, min(7, n - VOLT_MIN)))
        elif n >= NICHE_MIN:                    # средний ролл: ниша без ядра
            niche = NICHE_MIN
        else:                                   # малый ролл: вольт без ниши
            niche = 0
        volt_n = n - niche
        exq = rng.randint(EXQ_MIN, min(EXQ_MAX, max(EXQ_MIN, volt_n - 1))) \
            if volt_n > EXQ_MIN else 0
        plan = (["NICHE"] * niche + ["EXQUISITE"] * exq
                + ["VOLT"] * (volt_n - exq))
        # перемешивание с бегом ≤ GENRE_MAX_RUN — только когда мешать чем
        # (моно-жанровый малый ролл законом бега не душится: смешивать нечем)
        if niche > 0 and volt_n > 0:
            for _ in range(200):
                rng.shuffle(plan)
                run, cur, prev = 0, 0, None
                for g in plan:
                    cur = cur + 1 if g == prev else 1
                    run = max(run, cur)
                    prev = g
                if run <= GENRE_MAX_RUN:
                    break
        return plan

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
        """PROTO-2: СТАРТОВЫЙ предикт по карте (тир-пул); итоговый тир
        назначается ЧЕСТНО ПО СОСТАВУ в roll_slot (rating_implied, В43) —
        предсказывает то, что проверяет печь, а не класс карты."""
        cls = (card.get("components") or {}).get("exposure", {}).get("class", "—")
        corridor = card.get("corridor", "—")
        if cls == "—" or cls not in ("COVER", "PROCESS", "LINGERIE", "CLOTHED-TIGHT", "SHEER"):
            tier = "PG-13"       # В33: класс «—» не выносит R+
            why = "класс «—»: геометрия без экспозиции — заявки нет"
        elif corridor == "A":
            tier = "R+"
            why = "коридор A + класс экспозиции (старт; итог — по составу POS)"
        else:
            tier = "R"
            why = "коридор B: экспозиция заявлена, заряд геометрией слабее (старт)"
        return {"tier": tier, "corridor": corridor, "class": cls,
                "channel": combo.get("channel"), "why": why}

    # ── сигналы тира в POS (А) ─────────────────────────────────────────
    def tier_signals(self, pred: dict, combo: dict) -> list[str]:
        """PROTO-2: R+-сигналы — ТОЛЬКО честные по В43 (холд руками/bare-line
        со стрэпами); панельные «covered nipples» = R-потолок (причина №23)."""
        t = pred["tier"]
        if t == "R+":
            return [SIGNALS_RPLUS_HONEST.get(pred["class"], "arms covering chest")]
        rec = self.recipes["tiers"]["R" if t == "R" else "PG13"]
        return rec["signals"][:2]

    # ── сборка слота ───────────────────────────────────────────────────
    def roll_slot(self, rng: random.Random, idx: int, ledger: dict,
                  bt_used: dict, pal_used: dict, tier: str, pools: dict,
                  oc_hook_slot: int, genre: str = "VOLT",
                  used: dict | None = None) -> dict:
        """PROTO-2: слот с жанром и ЧЕСТНЫМ ПО СОСТАВУ ти ром (В43).
        used — батч-пулы уникальности: cards (без дублей), hair (без
        повторов, пока пул жив), scene (cap SCENE_CAP), race_rf + kin_used
        (В40), exp_hyp (В42: ≤2 клеток на гипотезу)."""
        used = used if used is not None else {}
        used.setdefault("cards", set())
        used.setdefault("hair", set())
        used.setdefault("scene", {})
        used.setdefault("race_rf", {})
        used.setdefault("kin", 0)
        used.setdefault("exp_hyp", {})
        total_hint = used.get("total_hint", 0)

        def scene_cap() -> int:
            """Динамический кап: слоты/сцены — ротация без удушения
            (21/7 → 3; 30/7 → 5)."""
            return max(SCENE_CAP, -(-total_hint // len(SCENES))) if total_hint else SCENE_CAP

        def pick_card(t: str):
            pool = [c for c in (pools.get(t) or pools["PG-13"])
                    if c["id"] not in used["cards"]]
            if not pool:
                pool = [c for c in (pools.get(t) or pools["PG-13"])]
            return rng.choice(pool)

        def pick_hair() -> str:
            fresh = [h for h in self.he["hair"] if h not in used["hair"]]
            pick = rng.choice(fresh if fresh else self.he["hair"])
            used["hair"].add(pick)
            return pick

        def pick_scene() -> str:
            # T5-30 (2026-11-22): после 20 попыток берём НАИМЕНЕЕ загруженную
            # сцену, а не случайную — рост пулов (палитры 269→278) сдвинул rng-
            # последовательность и вскрыл флейк: «любая сцена» рвала кап, когда
            # математика ещё позволяла его держать (N слотов ≤ N_сцен × кап)
            cap = scene_cap()
            for _ in range(20):
                s = rng.choice(SCENES)
                if used["scene"].get(s, 0) < cap:
                    used["scene"][s] = used["scene"].get(s, 0) + 1
                    return s
            s = min(SCENES, key=lambda x: (used["scene"].get(x, 0), x))
            used["scene"][s] = used["scene"].get(s, 0) + 1
            return s

        # ── попытки: состав обязан нести таргет-тир (В43) ────────────
        best = None
        for attempt in range(12):
            # PROTO-2: EXP-клетки — клетки-кандидаты, кин-кап только на
            # мейнах (В40 говорит про 21 мейн; T5-29 EXP — все кины)
            kin_cap_here = KIN_CAP if genre != "EXP" else 10 ** 9
            card = pick_card(tier if tier != "PG-13" else "PG-13")
            for _ in range(30):
                body_try = self.roll_body(rng)
                pal_try = rng.choice(self.palettes)
                if (bt_used.get(body_try["id"], 0) < 3
                        and pal_used.get(pal_try["id"], 0) < 3):
                    body, pal = body_try, pal_try
                    break
            else:
                body, pal = body_try, pal_try
            race = self.roll_race(rng, used["kin"], used["race_rf"],
                                  kin_cap=kin_cap_here)
            if race["id"] != "R01":
                used["kin"] += 1
            # R01 не пишет в race_rf: человек — основа, не «раса с капом»
            scene = pick_scene()
            combo = pg.roll_combo(rng, card, scene, self.closet, self.matrix, ledger)
            marks, _ = self.marks_for(rng, race, body)
            marks = [m for m in marks if self.visible(m, card)]
            # В32: фишечки ≥ 2 — гарант: у human без гиммика/лайт-хука
            # дожимаем метку (фолбэк — eye-метка: глаза всегда в кадре,
            # kin-compat на любой поверхности)
            fich = len(marks) + (1 if race.get("gimmick") else 0) + 1
            if fich < 2:
                extra, _ = self.marks_for(rng, race, body)
                extra = [m for m in extra if self.visible(m, card)
                         and m["id"] not in {x["id"] for x in marks}]
                if not extra:
                    eye_pool = [m for m in self.marks["marks"]
                                if m["category"] == "eyes" and not m.get("oc_hook")]
                    extra = [rng.choice(eye_pool)] if eye_pool else []
                if extra:
                    marks.append(extra[0])
            oc_hook = None
            if idx == oc_hook_slot and genre != "EXP":
                skin = race.get("skin_type", "skin")
                oc_pool = [m for m in self.marks["marks"] if m["oc_hook"]]
                for _ in range(12):
                    m = rng.choice(oc_pool)
                    if m["category"] == "eyes" or skin in ("skin", "mixed", "scales"):
                        oc_hook = m
                        break
                if oc_hook and oc_hook["category"] != "eyes":
                    marks = marks + [oc_hook]
            kin = rng.choice(self.kinetics)
            hair = pick_hair()
            base_eyes = rng.choice(self.he["eyes"])
            eye_mark = next((m for m in marks if m["category"] == "eyes"), None)
            if oc_hook and oc_hook["category"] == "eyes":
                eye_mark = oc_hook
            pred = self.predict(card, combo)
            signals = self.tier_signals(pred, combo)
            if "codes" not in combo:
                signals = self.recipes["tiers"]["PG13"]["signals"][:2]

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
                main_gar = next((c for c in combo["codes"] if c["shelf"] != "AC"),
                                combo["codes"][0])
                ch_states = []
                for ch_key, ch in self.channels.items():
                    if ch_key in str(combo.get("channel", "")):
                        states = [s for s in ch.get("state", []) if "(" not in s]
                        if pred["tier"] != "R+":
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

            # В43: итоговый тир — по составу; не совпал → запасные сигналы,
            # потом переброс карты (следующая попытка)
            implied = self.rating_implied(" ".join(pos_lines), self.rating_cfg)
            if implied == tier:
                used["cards"].add(card["id"])
                bt_used[body["id"]] = bt_used.get(body["id"], 0) + 1
                pal_used[pal["id"]] = pal_used.get(pal["id"], 0) + 1
                pred["tier"] = tier
                pred["why"] = f"честно по составу (В43, попытка {attempt + 1}): {pred['why']}"
                break
            if implied != tier and attempt >= 6:
                # запасной ход: honest-сигнал второго типа поверх заявки
                alt = ("straps covering the chest's bare line"
                       if tier == "R+" and "straps" not in " ".join(signals)
                       else "arms covering chest" if tier == "R+" else None)
                if alt and "codes" in combo:
                    claim_core = claim_core.replace(
                        f"{'; '.join(signals)}", f"{'; '.join(signals)}; {alt}", 1)
                    pos_lines = []
                    for ln in [opener, claim_core, weave, scene_line, palette_line, face_line]:
                        pos_lines.extend(wrap_lines(ln + ","))
                    implied2 = self.rating_implied(" ".join(pos_lines), self.rating_cfg)
                    if implied2 == tier:
                        used["cards"].add(card["id"])
                        bt_used[body["id"]] = bt_used.get(body["id"], 0) + 1
                        pal_used[pal["id"]] = pal_used.get(pal["id"], 0) + 1
                        pred["tier"] = tier
                        pred["why"] = f"честно по составу (В43, alt-сигнал, попытка {attempt + 1})"
                        implied = implied2
                        break
            best = {"card": card, "body": body, "pal": pal, "race": race,
                    "combo": combo, "marks": marks, "oc_hook": oc_hook,
                    "kin": kin, "hair": hair, "eyes": base_eyes,
                    "pred": pred, "signals": signals, "pos": pos_lines,
                    "implied": implied, "scene": scene, "weave": weave,
                    "eye_mark": eye_mark}
            # PROTO-2: неудачная попытка ОТКАТЫВАЕТ пулы уникальности
            # (ретраи не должны жрать сцены/причёски/расы — рана №1 ролла 777)
            used["scene"][scene] = used["scene"].get(scene, 0) - 1
            used["hair"].discard(hair)
            if race["id"] != "R01":
                used["kin"] -= 1
                used["race_rf"][race["id"]] = used["race_rf"].get(race["id"], 0) - 1
        else:
            # 12 попыток не сошлись: берём лучшее, тир честно понижен —
            # спред сломается, check это поймает (закон на бою важнее тишины)
            assert best is not None
            card, body, pal = best["card"], best["body"], best["pal"]
            race, combo, marks = best["race"], best["combo"], best["marks"]
            oc_hook, kin, hair, base_eyes = (best["oc_hook"], best["kin"],
                                             best["hair"], best["eyes"])
            pred, signals, pos_lines = best["pred"], best["signals"], best["pos"]
            scene, weave = best["scene"], best["weave"]
            eye_mark = best["eye_mark"]
            used["cards"].add(card["id"])
            bt_used[body["id"]] = bt_used.get(body["id"], 0) + 1
            pal_used[pal["id"]] = pal_used.get(pal["id"], 0) + 1
            pred["tier"] = best["implied"]
            pred["why"] = ("12 попыток не сошлись — честный дрейф по составу "
                           "(В43; check обязан это поймать)")
            # пулы best-попытки жили с откатом — возвращаем их в игру:
            # слот реально занимает сцену/расу/причёску из best
            used["scene"][scene] = used["scene"].get(scene, 0) + 1
            used["hair"].add(hair)
            if race["id"] != "R01":
                used["kin"] += 1
                used["race_rf"][race["id"]] = used["race_rf"].get(race["id"], 0) + 1

        # NEG по тиру (PROTO-2: без «nude», candle/lamp в safety-строке)
        tier_key = {"PG-13": "PG13", "R": "R", "R+": "RPLUS"}[pred["tier"]]
        counter = self.recipes["tiers"][tier_key].get("counter_neg", [])
        neg = list(NEG_SAFETY) + [NEG_ANTIWASH]
        if counter:
            neg.append(", ".join(counter[:6]))

        slot = {
            "n": idx,
            "genre": genre,
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

    # ── EXP-клетка (В42: полка гипотез, не тема) ───────────────────────
    def roll_exp(self, rng: random.Random, idx: int, ledger: dict,
                 bt_used: dict, pal_used: dict, pools: dict,
                 used: dict) -> dict:
        """PROTO-2 (В42): EXP-клетка = ОДНА переменная из полки гипотез
        (specs/open-hypotheses.json, H-XX в test_line); тема партии клетки
        не кастует; oc_hook в EXP запрещён; предикт честный по составу."""
        used.setdefault("exp_hyp", {})
        # PROTO-2 (рана №4 ролла 777): приоритет — НЕЗАНЯТЫЕ гипотезы,
        # не начатые: полка из 13 не должна двоиться раньше времени
        counts = used["exp_hyp"]
        free = [h for h in self.hyp_shelf if counts.get(h, 0) == 0]
        half = [h for h in self.hyp_shelf if 0 < counts.get(h, 0) < EXP_MAX_PER_HYP]
        hyp = rng.choice(free or half or self.hyp_shelf)
        used["exp_hyp"][hyp] = used["exp_hyp"].get(hyp, 0) + 1
        # клетка катает любую карту вне окна и вне дублей: тир честный по составу
        slot = self.roll_slot(rng, idx, ledger, bt_used, pal_used,
                              "R+", pools, oc_hook_slot=-1, genre="EXP",
                              used=used)
        slot["exp"] = True
        slot["hypothesis"] = hyp
        slot["test_line"] = f"ТЕСТ (⚗ {hyp}: одна переменная, тема батча клетку не кастует)"
        return slot


def roll(n: int, seed: int, out_path: Path | None, n_exp: int = 9) -> dict:
    """PROTO-2: мейн-скелет по Законам 24/В39–В41 (жанры с перемешиванием,
    кин-кап, EXQUISITE 1–4) + EXP-клетки с H-XX (В42); предикт честный по
    составу (В43); coverage обновляется роллом сам (цель Г)."""
    forge = Forge()
    rng = random.Random(seed)
    ledger = pg.load_ledger()
    pools = forge.tier_pools()
    bt_used: dict = {}
    pal_used: dict = {}
    # total_hint — динамический кап сцен (слоты/сцены); + уникальность карт
    used: dict = {"total_hint": n + n_exp}
    # В39/В41: жанровый план (NICHE⇒R, VOLT/EXQUISITE⇒R+) с бегом ≤ 3
    plan = forge.genre_plan(rng, n)
    tiers = ["R+" if g in ("VOLT", "EXQUISITE") else "R" for g in plan]
    oc_hook_slot = rng.randrange(n) if rng.random() < 0.35 else -1
    slots = []
    for i in range(n):
        slots.append(forge.roll_slot(rng, i + 1, ledger, bt_used, pal_used,
                                     tiers[i], pools, oc_hook_slot,
                                     genre=plan[i], used=used))
    # В42: EXP-оверлей — клетки гипотез, тема батча их не кастует
    for j in range(n_exp):
        slots.append(forge.roll_exp(rng, n + j + 1, ledger, bt_used,
                                    pal_used, pools, used))
    batch_id = f"TB-{datetime.now(timezone.utc).strftime('%Y%m%d')}-{seed}"
    doc = {
        "id": batch_id,
        "born": datetime.now(timezone.utc).isoformat(),
        "seed": seed,
        "proto": PROTO,
        "n": n,
        "n_exp": n_exp,
        "law": ("тест-батч-болванка PROTO-2: не в batches/, прилавком не читается; "
                "цели А/Б/В/Г/Д (testforge.py): жанровый скелет Закона 24 с "
                "перемешиванием (В39), кин-кап (В40), EXQUISITE в мейнах (В41), "
                "EXP-клетки H-XX (В42), предикт честен по составу В43"),
        "slots": slots,
    }
    path = out_path or (CORPUS / f"{batch_id}.json")
    CORPUS.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"ролл {batch_id}: {n} мейн + {n_exp} EXP → {path}")
    tiers_stat: dict = {}
    genres_stat: dict = {}
    for s in slots:
        tiers_stat[s["predicted"]["tier"]] = tiers_stat.get(s["predicted"]["tier"], 0) + 1
        genres_stat[s["genre"]] = genres_stat.get(s["genre"], 0) + 1
    kin_n = sum(1 for s in slots if s["genre"] != "EXP" and s["race"] != "R01")
    print(f"  предикт: {tiers_stat} · жанры: {genres_stat} · кин-каст {kin_n}/{n}; "
          f"типажей {len(set(s['bodytype'] for s in slots))}, "
          f"рас {len(set(s['race'] for s in slots))}, "
          f"палитр {len(set(s['palette'] for s in slots))}")
    cmd_coverage()  # цель Г: ролл сам обновляет покрытие — пролить невозможно
    return doc


# ── check: инварианты ───────────────────────────────────────────────────
def check_batch(doc: dict, forge: Forge) -> list[str]:
    """PROTO-2: инварианты целей А–Д. Болванки proto 1 (до урока T5-29) —
    SKIP: история не переписывается, законы новых эр назад не бьют
    (прецедент квитанций печи); их вывод помечен era-skip."""
    b = doc["id"]
    if int(doc.get("proto", 1)) < PROTO:
        return []  # era-skip (cmd_check печатает пометку)
    errs: list[str] = []
    oc_hooks = [s for s in doc["slots"] if s.get("oc_hook")]
    if len(oc_hooks) > 1:
        errs.append(f"{b}: ОС-сигнатурных меток >1 на батч ({len(oc_hooks)}) — закон marks.json")
    mains = [s for s in doc["slots"] if s.get("genre") != "EXP"]
    exps = [s for s in doc["slots"] if s.get("genre") == "EXP"]
    # ── Д: скелет-законы урока T5-29 ────────────────────────────────
    genres = [s.get("genre") for s in mains]
    if any(g not in ("VOLT", "NICHE", "EXQUISITE") for g in genres):
        errs.append(f"{b}: мейн без жанрового токена VOLT/NICHE/EXQUISITE — "
                    f"hard-гейт жанров (NICHE.md §Б) исполняется и на болванках")
    volt = sum(1 for g in genres if g in ("VOLT", "EXQUISITE"))
    niche = sum(1 for g in genres if g == "NICHE")
    exq = sum(1 for g in genres if g == "EXQUISITE")
    if len(mains) >= VOLT_MIN + NICHE_MIN:
        if volt < VOLT_MIN:
            errs.append(f"{b}: вольт-масса {volt} < {VOLT_MIN} — Закон 24 (В39)")
        if not (NICHE_MIN <= niche <= NICHE_MAX):
            errs.append(f"{b}: ниша {niche} вне {NICHE_MIN}–{NICHE_MAX} (В39)")
        if not (EXQ_MIN <= exq <= EXQ_MAX):
            errs.append(f"{b}: EXQUISITE в мейнах {exq} вне {EXQ_MIN}–{EXQ_MAX} (В41)")
    run, cur, prev = 0, 0, None
    for g in genres:
        cur = cur + 1 if g == prev else 1
        run = max(run, cur)
        prev = g
    # бег душится только когда мешать чем: моно-жанровый малый ролл
    # (n < вольт-ядро + ниша) законом бега не бьётся — смешивать нечем
    if (run > GENRE_MAX_RUN and niche > 0 and volt > 0
            and len(mains) >= VOLT_MIN + NICHE_MIN):
        errs.append(f"{b}: жанровый бег {run} > {GENRE_MAX_RUN} — вперемешку, не блоками (В39)")
    kin_n = sum(1 for s in mains if s["race"] != "R01")
    if len(mains) >= 15 and kin_n > KIN_CAP:
        errs.append(f"{b}: кин {kin_n}/{len(mains)} > {KIN_CAP} — кины опция, "
                    f"человек основа (В40)")
    # канон-локи ОС не катятся пулом (LAWS §21.4)
    for s in doc["slots"]:
        if s["race"] in forge.canon_races:
            errs.append(f"{b} P{s['n']:02d}: раса {s['race']} — канон-лок "
                        f"действующей ОС (LAWS §21.4)")
    # окно ротации + дубли карт
    if forge.window_cards:
        win_hit = sorted({s["y_card"] for s in doc["slots"]}
                         & forge.window_cards, key=lambda x: int(x[1:]))
        if win_hit:
            errs.append(f"{b}: карты бьют по окну последних {WINDOW_DEPTH} сданных: "
                        f"{win_hit}")
    seen_cards: dict = {}
    for s in doc["slots"]:
        if s["y_card"] in seen_cards:
            errs.append(f"{b}: Y-карта {s['y_card']} в двух слотах "
                        f"(P{seen_cards[s['y_card']]:02d}, P{s['n']:02d}) — дубль")
        seen_cards[s["y_card"]] = s["n"]
    # EXP-клетки: H-XX из полки, ≤2 клеток/гипотеза, oc_hook запрещён
    hyp_ids = set(forge.hyp_shelf)
    hyp_count: dict = {}
    for s in exps:
        h = s.get("hypothesis")
        if not h or h not in hyp_ids:
            errs.append(f"{b} P{s['n']:02d}: EXP-клетка без валидного H-XX "
                        f"из полки гипотез (В42)")
        else:
            hyp_count[h] = hyp_count.get(h, 0) + 1
        if s.get("oc_hook"):
            errs.append(f"{b} P{s['n']:02d}: oc_hook в EXP-клетке (В42: кандидат "
                        f"≠ тест, LAWS §5 «один EXP-слот = одна роль»)")
    for h, c in hyp_count.items():
        if c > EXP_MAX_PER_HYP:
            errs.append(f"{b}: гипотеза {h} на {c} клетках > {EXP_MAX_PER_HYP} "
                        f"(A/B-пара = одна переменная)")
    # спред мейнов = фактический предикт (не на честном слове)
    rplus = sum(1 for s in mains if s["predicted"]["tier"] == "R+")
    if len(mains) >= VOLT_MIN + NICHE_MIN and (rplus, len(mains) - rplus) != (len(mains) - niche, niche):
        # вольт-масса обязана быть R+, ниша — R (связка канона)
        bad = [f"P{s['n']:02d}" for s in mains
               if (s.get("genre") in ("VOLT", "EXQUISITE")) != (s["predicted"]["tier"] == "R+")]
        if bad:
            errs.append(f"{b}: жанр↔тир рассинхрон (вольт⇒R+, ниша⇒R): {bad}")
    # RF рас ≤ 2 (R01 — человек-основа, вне RF: кап душит основу — рана №2)
    race_c: dict = {}
    for s in doc["slots"]:
        if s["race"] != "R01":
            race_c[s["race"]] = race_c.get(s["race"], 0) + 1
    for r, c in race_c.items():
        if c > RACE_RF:
            errs.append(f"{b}: раса {r} использована {c}× > RF {RACE_RF}")
    # сцены: динамический кап (слоты/сцены) — ротация без удушения
    scene_cap = max(SCENE_CAP, -(-len(doc["slots"]) // len(SCENES)))
    scene_c: dict = {}
    for s in doc["slots"]:
        scene_c[s["scene"]] = scene_c.get(s["scene"], 0) + 1
    for sc, c in scene_c.items():
        if c > scene_cap:
            errs.append(f"{b}: сцена {sc} использована {c}× > кап {scene_cap}")
    # причёски без повторов (пока пул жив)
    if len(doc["slots"]) <= len(forge.he["hair"]):
        hair_c = {}
        for s in doc["slots"]:
            hair_c[s["hair"]] = hair_c.get(s["hair"], 0) + 1
        for h, c in hair_c.items():
            if c > 1:
                errs.append(f"{b}: причёска {h} ×{c} — салон-ротация (LAWS §15)")

    bt_count: dict = {}
    pal_count: dict = {}
    for s in doc["slots"]:
        sid = f"{b} P{s['n']:02d}"
        pos = s["pos"]
        text = " ".join(pos)
        # Б: манифест полон
        for f in ("y_card", "race", "bodytype", "palette", "predicted", "genre"):
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
        # ── А/В43: предикт ≡ состав POS (цель А честная) ─────────────
        implied = forge.rating_implied(text, forge.rating_cfg)
        if implied != s["predicted"]["tier"]:
            errs.append(f"{sid}: предикт {s['predicted']['tier']} ≠ состав "
                        f"{implied} (В43: болванка обязана предсказывать то, "
                        f"что проверяет печь)")
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
                # PROTO-2: фикшен stale-переменной (причина №19) — метка
                # берётся из oc_hook, а не из последнего mid цикла меток
                errs.append(f"{sid}: oc_hook-метка {s['oc_hook']['mark']} не в POS")
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
        # NEG: safety + анти-ваш + hard-флор света (§2) + без самодеятельности
        negtext = " ".join(s["neg"])
        if "loli" not in negtext or "washed-out" not in negtext:
            errs.append(f"{sid}: NEG без safety-префикса или анти-ваш")
        if "candle" not in negtext or "lamp" not in negtext:
            errs.append(f"{sid}: NEG без «candle, lamp» — hard-флор света v2 (LAWS §2)")
        if "nude" in negtext:
            errs.append(f"{sid}: «nude» в NEG — юнит вне реестра negBase (дисциплина v3)")
        # В32: ≥2 фишечки-ФОРМЫ
        fich = len(s["marks"]) + (1 if s.get("gimmick") else 0) + \
               (1 if s.get("oc_hook") else 0) + 1
        if fich < 2 and s.get("genre") != "EXP":
            errs.append(f"{sid}: фишечек-ФОРМ {fich} < 2 (В32)")
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
        # PROTO-2 (причина №20): несуществующее имя — ЯВНАЯ ошибка,
        # не молчаливый фолбэк на весь корпус
        sel = [f for f in files if f.stem == which]
        if not sel:
            print(f"testforge: батч «{which}» не найден в {CORPUS} "
                  f"(доступны: {', '.join(f.stem for f in files) or '—'})")
            return 2
        files = sel
    if not files:
        print("тест-корпус пуст — сначала roll")
        return 1
    total_errs = 0
    for f in files:
        doc = json.loads(f.read_text(encoding="utf-8"))
        if int(doc.get("proto", 1)) < PROTO:
            # PROTO-2: болванки до урока T5-29 — законы новых эр назад не
            # бьют; история видна и помечена, не молчит
            print(f"{doc['id']}: SKIP (proto {doc.get('proto', 1)} < {PROTO} — "
                  f"эра-скип, законы В39–В43 не оглядываются назад) — "
                  f"{len(doc['slots'])} слотов")
            continue
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
def cmd_coverage(corpus_dir: Path | None = None) -> int:
    """Аудит покрытия пулов. Фикс 2026-11-23 (внешний аудит, баг №1):
    ledger ПЕРЕСЧИТЫВАЕТСЯ С НУЛЯ по корпусу — раньше старый файл
    дочитывался и счётчики копились (+288 за прогон), а тест грязнил
    боевой ledger. Пересчёт идемпотентен: файл не переписывается, если
    данные не изменились (no-rewrite-if-equal — git-шум исключён);
    corpus_dir — временный каталог для тестов."""
    forge = Forge()
    corpus = CORPUS if corpus_dir is None else Path(corpus_dir)
    led_path = corpus / "coverage-ledger.json"
    led = {"y_cards": {}, "races": {}, "bodytypes": {}, "marks": {}, "cl_codes": {},
           "palettes": {}, "updated": datetime.now(timezone.utc).isoformat()}
    tb_files = sorted(corpus.glob("TB-*.json"))
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
    # no-rewrite-if-equal: счётчики не изменились — файл не трогаем
    same = False
    if led_path.exists():
        try:
            old = json.loads(led_path.read_text(encoding="utf-8"))
            same = all((old.get(k) or {}) == led[k] for k in
                       ("y_cards", "races", "bodytypes", "marks", "cl_codes", "palettes"))
            if same:
                led = old
        except Exception:
            same = False
    if not same:
        corpus.mkdir(parents=True, exist_ok=True)
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
    r.add_argument("--n", type=int, default=21)
    r.add_argument("--seed", type=int, default=None)
    r.add_argument("--exp", type=int, default=9,
                   help="EXP-клеток с H-XX (В42; 0 — только мейн)")
    c = sub.add_parser("check", help="инварианты тест-батчей")
    c.add_argument("--batch", default="all")
    sub.add_parser("coverage", help="аудит покрытия пулов (ничего не забывается)")
    cm = sub.add_parser("compare", help="сходимость предикт↔факт по inbox")
    cm.add_argument("--batch", default="all")
    a = ap.parse_args()
    if a.cmd == "roll":
        seed = a.seed if a.seed is not None else random.randrange(10**9)
        roll(a.n, seed, None, n_exp=a.exp)
        # PROTO-2 (причина №18): exit-код честный — FAIL чека роняет ролл,
        # «and 0 or 0» больше не глотает нарушения
        sys.exit(cmd_check("all"))
    elif a.cmd == "check":
        sys.exit(cmd_check(a.batch))
    elif a.cmd == "coverage":
        sys.exit(cmd_coverage())
    elif a.cmd == "compare":
        sys.exit(cmd_compare(a.batch))


if __name__ == "__main__":
    main()
