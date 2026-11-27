#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
THREAD 5 — ORACLE CLI печи (эра ORACLE-2, 2026-11-20).

Нервная система конвейера из терминала: окно ротации, жар партии, жребий
карт на следующую партию, агрегированный аудит через сервис, пульс.

ЖРЕБИЙ — ПОБИТОВОЕ ЗЕРКАЛО канонического движка
(src/lib/t5/oracle-engine.ts, тот же алгоритм тянет прилавок и сервис):
mulberry32 в беззнаковой 32-бит арифметике + тот же порядок корзин и
rng-вызовов. Паритет лочат золотые векторы tests/fixtures/oracle_vectors.json
(`oracle.py selftest` проверяет зеркало против них; bun-тест
tests/unit/oracle.test.ts проверяет канон против них же).

Команды:
  status [--url URL]                    пульс сервиса (+ режимы органов)
  window [--for T5-NN] [--depth N]      окно ротации Y-карт по корпусу
  pool --for T5-NN [--depth N] [--ids]  активный пул Y (аудит Коула R5):
                                       сколько карт реально доступно жребию
  draw --for T5-NN [--oc N] [--main N] [--exp N] [--depth N] [--md]
                                       жребий карт на партию (детерминирован)
  heat BATCH.md [--service URL]        жар партии (R+/коридоры/свежесть/каналы;
                                       честность label↔fact — через сервис,
                                       без сервиса помечается как n/a)
  audit BATCH.md [--url URL]           агрегированный аудит слотов сервисом
  selftest                              зеркало жребия против золотых векторов

Выходы: 0 — ок; 1 — ошибка использования; 2 — сервис нужен, но недоступен;
3 — внутренний крах (с баннером, как gates.py).

Прогон: python3 tools/oracle.py <команда>
"""

from __future__ import annotations

import argparse
import json
import sys
import tempfile
from pathlib import Path
from urllib.error import URLError
from urllib.request import Request, urlopen

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))

import gates  # noqa: E402  (канонический парсер батчей печи)
import t5delivery  # noqa: E402  (единый индекс сдачи — аудит 2026-11-20 P0-06)
import spec_io  # noqa: E402  (тикет #4: единый канон сериализации specs/*.json)

# кириллица в cp1251-пайпе (Windows-консоль) не должна ронять печать — как gates.py
try:
    sys.stdout.reconfigure(errors="replace")
    sys.stderr.reconfigure(errors="replace")
except (AttributeError, ValueError):
    pass

ROOT = REPO
DEFAULT_URL = "http://127.0.0.1:3031"
VECTORS_PATH = REPO / "tests" / "fixtures" / "oracle_vectors.json"
TRUST_PATH = REPO / "specs" / "y-trust.json"
TRUST_CEILING = 80  # Коул §7.2: CLOCK — только HIGH+MID, потолок 60–80 карт

U32 = 0xFFFFFFFF


# ════════════════════════ mulberry32 (зеркало) ════════════════════════

def mulberry32(seed: int):
    """Побитовое зеркало mulberry32 из oracle-engine.ts (беззнаковый домен)."""
    a = seed & U32
    while True:
        a = (a + 0x6D2B79F5) & U32
        t = a
        t = (imul(t ^ (t >> 15), t | 1)) & U32
        t = (t ^ (t + imul(t ^ (t >> 7), t | 61))) & U32
        yield ((t ^ (t >> 14)) & U32) / 4294967296.0


def imul(a: int, b: int) -> int:
    """JS Math.imul: знаковое 32-бит умножение — но в беззнаковом домене
    биты те же, что у (a*b) & 0xFFFFFFFF, поэтому берём произведение."""
    return (a * b) & U32


# ════════════════════════ корпус и реестр ════════════════════════

def card_num(card_id: str) -> int:
    digits = "".join(ch for ch in card_id if ch.isdigit())
    return int(digits) if digits else -1


def load_camera():
    """Реестр карт: specs/camera.json (тот же файл, что читают прилавок/сервис)."""
    path = ROOT / "specs" / "camera.json"
    if not path.exists():
        return None, []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None, []
    cards = []
    for c in data.get("y_cards", {}).get("cards", []):
        comps = c.get("components") or {}
        exposure = comps.get("exposure") or {}
        cards.append({
            "id": c.get("id", ""),
            "corridor": c.get("corridor") or "—",
            "exposureClass": exposure.get("class") or "—",
            "pattern": comps.get("pose") or c.get("pattern") or "",
            "builtFrom": c.get("built_from") or "",
        })
    cards.sort(key=lambda c: card_num(c["id"]))
    return data.get("version", "—"), cards


def corpus_batches(batch_dir=None):
    """Партии корпуса: [(no, path)] по номеру; канонический парсер — gates.
    2026-11-21: «кто сдан» — t5delivery (индекс specs/delivery-index.json),
    не локальный glob: черновик/ready не попадают в корпус жребия (двойной
    аудит 2026-11-20, Коул §6.3 + P0-06). batch_dir — для тестов/векторов."""
    root = REPO / "batches" if batch_dir is None else Path(batch_dir)
    out = []
    for no, p in t5delivery.delivered_batches(batch_dir=root):
        if no and no > 0:
            out.append((no, p))
    out.sort(key=lambda x: x[0])
    return out


def build_usage(batch_no: int):
    """Карта → {usedCount, lastBatch, lastBatchFile} по корпусу ДО партии
    (зеркало buildCardUsage: только прошлое)."""
    usage: dict[str, dict] = {}

    def push(cid: str, no: int, fname: str):
        u = usage.setdefault(cid, {"id": cid, "usedCount": 0, "lastBatch": None, "lastBatchFile": None})
        u["usedCount"] += 1
        if u["lastBatch"] is None or no > u["lastBatch"]:
            u["lastBatch"] = no
            u["lastBatchFile"] = fname

    for no, path in corpus_batches():
        if batch_no > 0 and no >= batch_no:
            continue
        try:
            _, _, slots = gates.parse_batch(path)
        except Exception:
            continue
        for s in slots:
            if s.y_card:
                push(s.y_card, no, path.name)
    return usage


def build_window(batch_no: int, depth: int, corpus=None):
    """Окно ротации (зеркало buildRotationWindow gates.py v1.16.0):
    последние depth партий ДО batch_no по номеру. corpus — либо живой корпус
    (по умолчанию), либо синтетический [(no, path)] для тестов/векторов."""
    past = corpus if corpus is not None else corpus_batches()
    # корпус всегда сортируется по номеру партии: живой уже отсортирован,
    # синтетический (тесты/векторы) может приходить в любом порядке
    past = sorted(((no, p) for no, p in past if 0 < no < batch_no), key=lambda x: x[0])
    window = past[-depth:] if depth > 0 else []
    used: dict[str, str] = {}
    for no, path in window:
        try:
            _, _, slots = gates.parse_batch(path)
        except Exception:
            continue
        for s in slots:
            if s.y_card and s.y_card not in used:
                used[s.y_card] = path.name
    return {
        "depth": depth,
        "batches": [{"no": no, "file": p.name} for no, p in reversed(window)],
        "usedInWindow": used,
    }


# ════════════════════════ ЖРЕБИЙ (зеркало drawConstellation) ════════════════════════

def oc_rank(card, usage):
    u = usage.get(card["id"])
    cover = 1000 if card["exposureClass"] == "COVER" else 0
    fresh = 0 if u else 500
    rarity = max(0, 100 - u["usedCount"] * 10) if u else 0
    age = max(0, 60 - u["lastBatch"]) if (u and u["lastBatch"]) else 0
    return cover + fresh + rarity + age


def build_pose_window(batch_no: int, depth: int, corpus=None):
    """Окно ПОЗ ротации (§7, обкатка T5-27 проблема №1): PL-коды слотов
    последних depth партий до batch_no — карта жребия, чей built_from в этом
    множестве, не раздаётся (зеркало buildPoseWindow oracle-engine.ts)."""
    past = []
    for no, path in (corpus if corpus is not None else corpus_batches()):
        if 0 < no < batch_no:
            past.append((no, path))
    past.sort(key=lambda x: x[0])
    window = past[-depth:] if depth > 0 else []
    poses = set()
    for _no, path in window:
        try:
            _, _, slots = gates.parse_batch(path)
        except Exception:
            continue
        for s in slots:
            if s.pose:
                poses.add(s.pose)
    return sorted(poses)


def draw_constellation(batch_no, cards, usage, oc_target=3, main_target=21, exp_target=9, window_depth=3, window_poses=None):
    """Побитовое зеркало drawConstellation (oracle-engine.ts). Порядок
    корзин, сортировок и rng-вызовов свято совпадает — иначе векторы падают."""
    # окно: последние window_depth партий прошлого
    past_nos = sorted({u["lastBatch"] for u in usage.values() if u["lastBatch"] and u["lastBatch"] < batch_no})
    window_nos = set(past_nos[-window_depth:] if window_depth > 0 else [])

    def in_window(cid):
        u = usage.get(cid)
        return bool(u and u["lastBatch"] in window_nos)

    # обкатка T5-27, проблема №1: PL-окно поз — карта на позе окна не раздаётся
    pose_window = set(window_poses or [])

    def pose_banned(c):
        return bool(pose_window and c.get("builtFrom") and c["builtFrom"] in pose_window)

    usable = [c for c in cards
              if c["id"] and card_num(c["id"]) > 0 and c["pattern"].strip()
              and not in_window(c["id"]) and not pose_banned(c)]
    usable.sort(key=lambda c: card_num(c["id"]))
    pool_a = [c for c in usable if c["corridor"] in ("A", "A+B")]
    pool_b = [c for c in usable if c["corridor"] in ("B", "A+B")]
    pool_mid = [c for c in usable if c["corridor"] in ("—", "-", "")]
    oc_pool = sorted(pool_a, key=lambda c: oc_rank(c, usage), reverse=True)
    exp_pool = sorted([c for c in usable if c["id"] not in usage],
                      key=lambda c: card_num(c["id"]), reverse=True)

    seed = (batch_no * 2654435761) & U32
    if seed == 0:
        seed = 1
    rng = mulberry32(seed)

    drawn = set()
    shortfall = 0

    def take(pool):
        live = [c for c in pool if c["id"] not in drawn]
        if not live:
            return None
        r = next(rng)
        pick = live[int(r * len(live)) % len(live)]
        drawn.add(pick["id"])
        return pick

    oc, main, exp = [], [], []
    for _ in range(oc_target):
        pick = take(oc_pool)
        if pick is None:
            shortfall += 1
            continue
        u = usage.get(pick["id"])
        reason = (f"OC-жребий: карта не использована ни разу — «новенькая», коридор {pick['corridor']}, класс {pick['exposureClass']}"
                  if not u else
                  f"OC-жребий: коридор {pick['corridor']}, класс {pick['exposureClass']}; «давненько не была» — последний раз партия №{u['lastBatch']}")
        oc.append({**pick, "reason": reason})

    baskets = [pool_a, pool_b, pool_mid]
    for i in range(main_target):
        order = [baskets[i % 3], baskets[(i + 1) % 3], baskets[(i + 2) % 3]]
        pick = None
        for basket in order:
            pick = take(basket)
            if pick:
                break
        if pick is None:
            shortfall += 1
            continue
        u = usage.get(pick["id"])
        side = ("A+B" if pick["corridor"] == "A+B" else "B (геометрия)" if pick["corridor"] == "B"
                else "A (объект у груди)" if pick["corridor"] == "A" else "низкий тир")
        tail = f", последний выход — партия №{u['lastBatch']}" if u else ", ни разу"
        main.append({**pick, "reason": f"мейн {i + 1:02d}: корзина {side}; окно чисто{tail}"})

    for _ in range(exp_target):
        pick = take(exp_pool)
        if pick is None:
            shortfall += 1
            continue
        exp.append({**pick, "reason": f"EXP-жребий: новенькая карта (ни разу не создавали), номер {card_num(pick['id'])} — волна свежих"})

    return {
        "batchNo": batch_no,
        "seed": seed,
        "oc": oc,
        "main": main,
        "exp": exp,
        "windowExcluded": sum(1 for c in cards if in_window(c["id"])),
        "windowPosesExcluded": sum(1 for c in cards if pose_banned(c)),
        "shortfall": shortfall,
    }


# ════════════════════════ ЖАР (числовые компоненты) ════════════════════════

HEAT_WEIGHTS = {"rplus": 0.30, "corridor": 0.20, "freshness": 0.20, "honesty": 0.15, "channels": 0.15}


def batch_heat(path: Path, usage: dict, service_honesty: float | None):
    """Жар партии: числовое зеркало batchHeat (TS). Честность — два базиса
    (эра В34/В35): с сервисом — его аудит по всем слотам; без сервиса —
    ВПЛЕТЕНИЕ для слотов с Y-картой (паттерн карты 1:1 подстрокой —
    реестровое, прозо-устойчивое; урок замера T5-26: тег-словари на прозе
    давали ложный drift 33/33). Бескарточные слоты без сервиса не считаются
    честностью вовсе — словари lite живут только в TS."""
    _, _, slots = gates.parse_batch(path)
    _, camera_cards = load_camera()
    patterns = {c["id"]: c["pattern"].strip() for c in camera_cards if c["pattern"].strip()}
    weave_checked = 0
    weave_missing = 0
    for s in slots:
        if s.y_card and s.y_card in patterns:
            weave_checked += 1
            hay = " ".join(s.pos.split()).lower()
            needle = " ".join(patterns[s.y_card].split()).lower()
            if needle not in hay:
                weave_missing += 1
    rated = [s for s in slots if s.rating and s.rating != "—"]
    rplus = sum(1 for s in rated if s.rating == "R+")
    rplus_share = (rplus / len(rated)) if rated else 0.0

    corr: dict[str, int] = {}
    for s in slots:
        key = (s.corridor or "—").strip() or "—"
        corr[key] = corr.get(key, 0) + 1

    with_card = [s for s in slots if s.y_card]
    fresh = [s for s in with_card if s.y_card not in usage]
    batch_no = gates.batch_number(path)

    channels: dict[str, int] = {}
    for s in slots:
        if s.channel and s.channel.strip():
            c = s.channel.strip()
            channels[c] = channels.get(c, 0) + 1
    channel_dupes = sorted(([c, n] for c, n in channels.items() if n > 1), key=lambda x: -x[1])

    rplus_score = (0.0 if rplus_share <= 0 else
                   rplus_share / 0.30 * 0.70 if rplus_share < 0.30 else
                   1.0 if rplus_share <= 0.60 else
                   max(0.0, 1 - (rplus_share - 0.60) / 0.40))
    a_side = corr.get("A", 0)
    b_side = corr.get("B", 0)
    ab = corr.get("A+B", 0)
    corr_max = max(a_side + ab, b_side + ab, 1)
    corridor_score = min(a_side + ab, b_side + ab) / corr_max
    freshness_score = (len(fresh) / len(with_card)) if with_card else 0.5
    if service_honesty is not None:
        honesty_score = service_honesty
    elif weave_checked:
        # В34-базис без сервиса: только карточные слоты, по вплетению 1:1
        honesty_score = max(0.0, 1.0 - weave_missing / weave_checked)
    else:
        honesty_score = 1.0
    channel_total = sum(channels.values())
    channels_score = (len(channels) / channel_total) if channel_total else 1.0

    score = round(100 * (HEAT_WEIGHTS["rplus"] * rplus_score
                         + HEAT_WEIGHTS["corridor"] * corridor_score
                         + HEAT_WEIGHTS["freshness"] * freshness_score
                         + HEAT_WEIGHTS["honesty"] * honesty_score
                         + HEAT_WEIGHTS["channels"] * channels_score))
    label = "ГОРЯЧО" if score >= 75 else ("ТЁПЛЫЙ" if score >= 50 else "ХОЛОДНЫЙ")
    return {
        "path": str(path), "batch_no": batch_no, "slots": len(slots), "rated": len(rated),
        "rplus_share": round(rplus_share, 3), "corridor": corr,
        "cards": len(with_card), "fresh": len(fresh), "channels_total": channel_total,
        "channel_dupes": channel_dupes,
        "honesty": (f"{service_honesty:.2f} по сервису (все слоты)" if service_honesty is not None else
                    (f"{honesty_score:.2f} по вплетению В34 ({weave_checked - weave_missing}/{weave_checked} карточных слотов; бескарточные — только с сервисом)"
                     if weave_checked else "n/a (карточных слотов нет, сервис не поднят)")),
        "score": score, "label": label,
        "formula": "жар = 0.30·R+-доля + 0.20·баланс коридоров + 0.20·свежесть карт + 0.15·честность label + 0.15·уникальность каналов",
    }


# ════════════════════════ сервис ════════════════════════

def service_call(url: str, path_qs: str, payload: dict | None = None, timeout: float = 8.0):
    """POST/GET к oracle-service. Возвращает (status, json|текст)."""
    full = url.rstrip("/") + path_qs
    if payload is not None:
        req = Request(full, data=json.dumps(payload).encode("utf-8"),
                     headers={"Content-Type": "application/json"}, method="POST")
    else:
        req = Request(full, method="GET")
    with urlopen(req, timeout=timeout) as res:
        body = res.read().decode("utf-8")
    try:
        return res.status if hasattr(res, "status") else 200, json.loads(body)
    except json.JSONDecodeError:
        return 200, body


def honesty_from_service(url: str, path: Path) -> float | None:
    """Доля слотов без FAIL-вердикта по /batch — компонент честности жара."""
    _, _, slots = gates.parse_batch(path)
    payload = {"slots": [{"id": s.sid, "pos": s.pos, "badge": s.rating or "",
                          "corridor": s.corridor or "", "ycard": s.y_card or ""} for s in slots]}
    try:
        _, data = service_call(url, "/batch", payload, timeout=20.0)
    except (URLError, OSError, TimeoutError):
        return None
    if not isinstance(data, dict) or "slots_audited" not in data:
        return None
    audited = data["slots_audited"]
    if not audited:
        return None
    failed = data.get("failed_slots", 0)
    return max(0.0, 1.0 - failed / audited)


# ════════════════════════ команды ════════════════════════

def parse_for(raw: str) -> int:
    """«T5-27» / «t5-27» / «27» → 27. Раньше жрал все цифры строки («T5-27» → 527)
    и жребий сеялся не тем номером — печь и сервис расходились в раскладах."""
    cleaned = raw.strip().upper().removeprefix("T5").replace(" ", "")
    cleaned = cleaned.lstrip("-–—")
    digits = "".join(ch for ch in cleaned if ch.isdigit())
    return int(digits) if digits else 0


def cmd_status(args) -> int:
    try:
        _, data = service_call(args.url, "/health", timeout=2.0)
        print("СЕРВИС ЖИВ:", json.dumps(data, ensure_ascii=False, indent=1))
        return 0
    except (URLError, OSError, TimeoutError) as e:
        print(f"сервис {args.url} не отвечает ({e.__class__.__name__}) — печь на локальных алгоритмах;")
        print("жребий/окно/жар работают, честность label↔fact и LLM-мозг — только с сервисом")
        return 2


def cmd_window(args) -> int:
    batch_no = parse_for(args.for_batch) if args.for_batch else 0
    if batch_no <= 0:
        latest = corpus_batches()
        batch_no = (latest[-1][0] + 1) if latest else 27
        print(f"(--for не задан — смотрю прошлое следующей партии: T5-{batch_no})")
    window = build_window(batch_no, args.depth)
    print(f"=== ОКНО РОТАЦИИ · до T5-{batch_no} · глубина {window['depth']} ===")
    print("партии в окне:", ", ".join(b["file"].replace(".md", "") for b in window["batches"]) or "—")
    used = window["usedInWindow"]
    print(f"карт в окне: {len(used)}")
    for cid in sorted(used, key=card_num)[:60]:
        print(f"  {cid} — {used[cid]}")
    if len(used) > 60:
        print(f"  … и ещё {len(used) - 60}")
    print("закон: карта из окна НЕ раздаётся жребием (gates.py v1.16.0 — окно смотрит только назад)")
    return 0


def active_pool(cards, usage, batch_no, window_depth=3, window_poses=None):
    """Активный пул — ТОЧНОЕ зеркало фильтра usable из draw_constellation
    (аудит Коула R5: писец видит реальное пространство выбора жребия):
    карты с валидным id/паттерном, не в окне ротации, не на позе окна.
    Возвращает (usable, n_window, n_pose_banned)."""
    past_nos = sorted({u["lastBatch"] for u in usage.values() if u["lastBatch"] and u["lastBatch"] < batch_no})
    window_nos = set(past_nos[-window_depth:] if window_depth > 0 else set())

    def in_window(cid):
        u = usage.get(cid)
        return bool(u and u["lastBatch"] in window_nos)

    pose_window = set(window_poses or [])

    def pose_banned(c):
        return bool(pose_window and c.get("builtFrom") and c["builtFrom"] in pose_window)

    n_win = sum(1 for c in cards if in_window(c["id"]))
    n_pose = sum(1 for c in cards if pose_banned(c))
    usable = [c for c in cards
              if c["id"] and card_num(c["id"]) > 0 and c["pattern"].strip()
              and not in_window(c["id"]) and not pose_banned(c)]
    return usable, n_win, n_pose


# ════════════════════════ траст-слой Y (заказ автора 2026-11-23, Коул §7) ════════════════════════

def load_trust() -> dict:
    """Реестр доверия specs/y-trust.json (сгенерирован: oracle.py trust --rebuild).
    Пустой dict — слой не построен (жребий ходит как раньше, без потолка)."""
    if TRUST_PATH.exists():
        try:
            return json.loads(TRUST_PATH.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {}


def load_verdict_evidence():
    """JSON-вердикты (t5-verdict/1) → улики по Y-картам партии.

    Коул §7.1 «hit Y/PL → trust HIGH, miss → LOW»:
      hit    — слот в loved или подтверждённая гипотеза (hypothesis_hits);
      neutral— слот в ok_with_issues (не хит, не провал — улика не копится);
      miss   — катана в вердиктной партии мимо loved/ok (в т.ч. neutral-список).
    Соответствие слот → карта — канонический парсер печи (gates.parse_batch).

    v1.1.0 (ПЛАН 5.5 T2.3/1.4, волна 2): fact-слой — тир берётся и из
    rating_truth_delta, не только из loved: слот, чей ЗАЯВЛЕННЫЙ тир
    доехал до рендера (truth == declared), — hit-улика карте (kind
    fact_hit) даже если автор его не залюбил; заявка, развалившаяся на
    рендере (truth ≠ declared), — miss-улика (kind fact_drift). Loved
    остаётся сильнейшей уликой вкуса; fact — улика delivery карты."""
    hits: dict[str, list] = {}
    neutrals: dict[str, list] = {}
    misses: dict[str, list] = {}
    sources = []
    for vf in sorted((ROOT / "verdicts").glob("*.json")):
        try:
            d = json.loads(vf.read_text(encoding="utf-8"))
        except Exception:
            continue
        if d.get("schema") != "t5-verdict/1" or not d.get("batch"):
            continue
        bfile = ROOT / "batches" / f"{d['batch']}.md"
        if not bfile.exists():
            continue
        try:
            _, _, slots = gates.parse_batch(bfile)
        except Exception:
            continue
        by_sid = {s.sid: s for s in slots if s.y_card}
        loved = {e.get("slot") for e in (d.get("loved") or []) if e.get("slot")}
        ok = {e.get("slot") for e in (d.get("ok_with_issues") or []) if e.get("slot")}
        hyp = {e.get("slot") for e in (d.get("hypothesis_hits") or []) if e.get("slot")}
        delta = {r.get("slot"): r.get("truth") for r in (d.get("rating_truth_delta") or [])
                 if r.get("slot") and r.get("truth")}
        for sid, s in by_sid.items():
            truth = delta.get(sid)
            fact_ok = truth is not None and truth == s.rating
            fact_tag = ("fact_ok" if fact_ok else "fact_drift") if truth else None
            if sid in loved or sid in hyp or fact_ok:
                kind = ("loved" if sid in loved
                        else "hypothesis" if sid in hyp else "fact_hit")
                hits.setdefault(s.y_card, []).append(
                    {"batch": d["batch"], "slot": sid, "kind": kind,
                     **({"fact": fact_tag} if fact_tag else {})})
            elif sid in ok:
                neutrals.setdefault(s.y_card, []).append(
                    {"batch": d["batch"], "slot": sid, "kind": "ok_with_issues",
                     **({"fact": fact_tag} if fact_tag else {})})
            else:
                misses.setdefault(s.y_card, []).append(
                    {"batch": d["batch"], "slot": sid,
                     "kind": "fact_drift" if truth else "miss",
                     **({"fact": fact_tag} if fact_tag else {})})
        sources.append({"file": vf.name, "batch": d["batch"]})
    return hits, neutrals, misses, sources


def build_trust() -> dict:
    """Реестр доверия Y: HIGH (hit) / MID (нет данных или только ok) / LOW (miss).
    Hit сильнее miss: карта с хитом — HIGH независимо от старых промахов
    (искупление хитом; LOW сидит до новой попытки в LAB или хита)."""
    hits, neutrals, misses, sources = load_verdict_evidence()
    cards: dict[str, dict] = {}
    for cid in sorted(set(hits) | set(neutrals) | set(misses), key=card_num):
        h, m = len(hits.get(cid, [])), len(misses.get(cid, []))
        trust = "HIGH" if h else ("LOW" if m else "MID")
        ev = hits.get(cid, []) + neutrals.get(cid, []) + misses.get(cid, [])
        cards[cid] = {
            "trust": trust, "hits": h, "misses": m,
            "neutral": len(neutrals.get(cid, [])),
            # v1.1.0 (T2.3/1.4): fact-слой — доехал ли ЗАЯВЛЕННЫЙ тир до
            # рендера; тёплые на бумаге и холодные в пикселях видны в цифрах
            "fact_hits": sum(1 for e in ev if e.get("fact") == "fact_ok"),
            "fact_drifts": sum(1 for e in ev if e.get("fact") == "fact_drift"),
            "evidence": ev,
        }
    n = {t: sum(1 for c in cards.values() if c["trust"] == t) for t in ("HIGH", "MID", "LOW")}
    fact_h = sum(c["fact_hits"] for c in cards.values())
    fact_d = sum(c["fact_drifts"] for c in cards.values())
    return {
        "id": "y-trust",
        "name": "Траст-слой Y: HIGH/MID/LOW по hit/miss из JSON-вердиктов",
        "version": "1.1.0",
        "born": "2026-11-23",
        "born_from": ("Заказ автора 2026-11-23 «Сделай траст-слой Y» + аудит Коула/Grok "
                       "§7 «ACTIVE POOLS И TRUST — обязательный следующий шаг»: жребий честен, "
                       "но 400+ window-eligible карт — лотерея, а не выбор; CLOCK ходит по "
                       "узкому пулу HIGH+MID ≤ 80, LOW (промахи вердиктов) сидят до искупления. "
                       "v1.1.0 (2026-11-28, ПЛАН 5.5 T2.3/T1.4, волна 2): fact-слой — "
                       "тир берётся и из rating_truth_delta (truth == declared — fact_hit "
                       "улика карте, развалившаяся заявка — fact_drift miss); loved остаётся "
                       "сильнейшей уликой вкуса, fact — улика delivery"),
        "policy": {
            "HIGH": "хит в JSON-вердикте (loved, подтверждённая гипотеза или fact-хит: заявленный тир доехал до рендера) — первыми в пул CLOCK",
            "MID": "нет улик (не катана в вердиктных партиях) или только ok_with_issues — годна по умолчанию",
            "LOW": "катана в вердиктной партии мимо loved/ok — miss; сидит до хита или LAB-искупления",
            "ceiling": TRUST_CEILING,
            "draw": "CLOCK (жребий --trust): только HIGH+MID, потолок 80; порядок: HIGH → MID (никогда не катаны → реже всех → по номеру)",
            "note": "Коул §7.4: window-eligible (просто не в окне) — НЕ «активный пул»; в бриф/квитанцию печатаются active_trust_count и window_eligible_count",
            "regenerate": "python3 tools/oracle.py trust --rebuild (после каждого нового verdicts/*.json; валидатор — проверка №15)",
        },
        "sources": sources,
        "stats": {"high": n["HIGH"], "mid": n["MID"], "low": n["LOW"],
                  "judged_batches": len(sources),
                  "fact_hits": fact_h, "fact_drifts": fact_d},
        "cards": cards,
    }


def trust_pool(cards, usage, batch_no, window_depth=3, window_poses=None,
               trust_cards=None, ceiling=None):
    """Активный пул CLOCK (Коул §7.2): HIGH+MID ≤ потолка, LOW исключены.

    Строится ОТ window-eligible (окно/позы уже съедены): сначала HIGH
    (доказанные хиты), затем MID до потолка — никогда не катаны раньше,
    затем реже всех, затем по номеру карты (детерминизм без кубика)."""
    eligible, n_win, n_pose = active_pool(cards, usage, batch_no, window_depth, window_poses)
    if trust_cards is None:
        trust_cards = load_trust().get("cards") or {}
    if ceiling is None:
        ceiling = int((load_trust().get("policy") or {}).get("ceiling") or TRUST_CEILING)

    def level(c):
        return (trust_cards.get(c["id"]) or {}).get("trust", "MID")

    high = [c for c in eligible if level(c) == "HIGH"]
    mid = [c for c in eligible if level(c) == "MID"]
    low = [c for c in eligible if level(c) == "LOW"]

    def mid_priority(c):
        u = usage.get(c["id"]) or {}
        return (u.get("usedCount") or 0, card_num(c["id"]))

    mid.sort(key=mid_priority)
    pool = high + mid[: max(0, ceiling - len(high))]
    stats = {"high": len(high), "mid": len(mid), "low": len(low),
             "eligible": len(eligible), "window": n_win, "pose": n_pose,
             "ceiling": ceiling}
    return pool, stats


def cmd_trust(args) -> int:
    """Траст-слой Y: rebuild из verdicts/*.json или отчёт по реестру."""
    if args.rebuild:
        reg = build_trust()
        spec_io.dump_spec(TRUST_PATH, reg)  # тикет #4: единый канон сериализации
        st = reg["stats"]
        print(f"траст-слой Y собран: specs/y-trust.json ({reg['version']})")
        print(f"  партий с JSON-вердиктами: {st['judged_batches']} · HIGH {st['high']} · MID {st['mid']} · LOW {st['low']}")
        print(f"  вердиктные файлы: {', '.join(s['file'] for s in reg['sources']) or '—'}")
        return 0
    reg = load_trust()
    if not reg:
        print("specs/y-trust.json не построен — python3 tools/oracle.py trust --rebuild")
        return 1
    st = reg.get("stats") or {}
    print(f"=== ТРАСТ-СЛОЙ Y · y-trust {reg.get('version')} · Коул §7 ===")
    print(f"партий с JSON-вердиктами: {st.get('judged_batches', 0)} · HIGH {st.get('high', 0)} · MID {st.get('mid', 0)} · LOW {st.get('low', 0)}")
    for t in ("HIGH", "LOW"):
        ids = [cid for cid, c in (reg.get("cards") or {}).items() if c["trust"] == t]
        print(f"  {t}: {', '.join(ids) or '—'}")
    print(f"потолок CLOCK: {int((reg.get('policy') or {}).get('ceiling') or TRUST_CEILING)} карт (HIGH+MID; жребий --trust)")
    return 0


def cmd_pool(args) -> int:
    """Активный пул Y-карт для партии: сколько карт РЕАЛЬНО доступно
    жребию после окна ротации и запрета поз (аудит Коула R5 «лотерея из
    500»: писец не видел пространства выбора). Target — из
    specs/active-pools.json; пул < target = окно жрёт слишком много."""
    batch_no = parse_for(args.for_batch)
    if batch_no <= 0:
        print("нужен номер партии: --for T5-28")
        return 1
    version, cards = load_camera()
    if not cards:
        print("specs/camera.json не читается")
        return 3
    pools_spec = {}
    try:
        pools_spec = json.loads((ROOT / "specs/active-pools.json").read_text(encoding="utf-8"))
    except Exception:
        pass
    target = int((pools_spec.get("pools") or {}).get("y_cards", {}).get("target") or 60)

    usage = build_usage(batch_no)
    window_poses = build_pose_window(batch_no, args.depth)
    usable, n_win, n_pose = active_pool(cards, usage, batch_no, args.depth, window_poses)
    trust = load_trust()
    trust_cards = trust.get("cards") if trust.get("version") else None
    print(f"=== АКТИВНЫЙ ПУЛ Y · T5-{batch_no} · реестр camera {version} ===")
    print(f"всего карт: {len(cards)} · окно ротации ({args.depth} партий) съело: {n_win} · запрет поз съел: {n_pose}")
    # Коул §7.4 (траст-слой, 2026-11-23): «просто не в окне» — НЕ «активный
    # пул»; честное имя — window-eligible, активный пул CLOCK = HIGH+MID ≤ потолка
    print(f"window-eligible (не в окне, не под запретом поз): {len(usable)} карт")
    if trust_cards:
        pool, st = trust_pool(cards, usage, batch_no, args.depth, window_poses,
                              trust_cards=trust_cards)
        health = "ЗДОРОВ" if len(pool) >= target else f"ТУГО (пул ниже target {target} — сигнал SOL'у)"
        print(f"траст-слой (y-trust {trust.get('version')}): вне окна HIGH {st['high']} · MID {st['mid']} · LOW {st['low']} (LOW — вне жребия CLOCK)")
        print(f"АКТИВНЫЙ ПУЛ CLOCK (HIGH+MID, потолок {st['ceiling']}): {len(pool)} карт · {health}")
        if args.ids:
            print("карты CLOCK: " + " ".join(c["id"] for c in pool))
        print("квитанция в бриф: 'Активный пул Y (CLOCK, траст): " + str(len(pool)) + " из " + str(len(cards))
              + " (HIGH " + str(st["high"]) + " · MID " + str(len(pool) - st["high"])
              + " · LOW −" + str(st["low"]) + ", потолок " + str(st["ceiling"]) + ")"
              + " / window-eligible " + str(st["eligible"])
              + " — active_trust_count " + str(len(pool)) + ", window_eligible_count " + str(st["eligible"]) + "'")
    else:
        if usable and args.ids:
            print("карты: " + " ".join(c["id"] for c in usable))
        print("траст-слой Y не построен: python3 tools/oracle.py trust --rebuild (заказ автора 2026-11-23, Коул §7)")
        print("квитанция в бриф (без траста): 'window-eligible Y: " + str(len(usable)) + " из " + str(len(cards))
              + " (окно −" + str(n_win) + ", позы −" + str(n_pose) + ", target " + str(target) + ")'")
    print("long tail (весь реестр) — только режим LAB по приказу автора (specs/active-pools.json)")
    return 0


def cmd_draw(args) -> int:
    batch_no = parse_for(args.for_batch)
    if batch_no <= 0:
        print("нужен номер партии: --for T5-27 (жребий сеется номером — расклад воспроизводим)")
        return 1
    version, cards = load_camera()
    if not cards:
        print("specs/camera.json не читается — жребий бросается только по живому реестру")
        return 3
    usage = build_usage(batch_no)
    window_poses = build_pose_window(batch_no, args.depth)
    # траст-слой Y (заказ автора 2026-11-23, Коул §7): CLOCK-жребий ходит
    # только по HIGH+MID ≤ потолка; дефолт без --trust — прежняя механика
    # (окно/позы): паритет прилавок↔печь↔сервис и золотые вектора нетронуты
    trust = load_trust()
    trust_cards = trust.get("cards") if trust.get("version") else None
    trust_stats = None
    if args.trust:
        if not trust_cards:
            print("траст-слой Y не построен: python3 tools/oracle.py trust --rebuild")
            return 1
        pool, trust_stats = trust_pool(cards, usage, batch_no, args.depth,
                                       window_poses, trust_cards=trust_cards)
        keep = {c["id"] for c in pool}
        cards = [c for c in cards if c["id"] in keep]
    elif trust_cards:
        _pool, trust_stats = trust_pool(cards, usage, batch_no, args.depth,
                                        window_poses, trust_cards=trust_cards)
    draw = draw_constellation(batch_no, cards, usage,
                              oc_target=args.oc, main_target=args.main,
                              exp_target=args.exp, window_depth=args.depth,
                              window_poses=window_poses)
    if args.md:
        print(f"## Жребий оракула — партия №{batch_no} (seed {draw['seed']})")
        print()
        print(f"Реестр: camera {version} · {len(cards)} карт · окно ротации: {args.depth} партий")
        if trust_stats:
            at = trust_stats["high"] + min(trust_stats["mid"], max(0, trust_stats["ceiling"] - trust_stats["high"]))
            print(f"Траст: активный пул CLOCK {at} карт (HIGH {trust_stats['high']} · потолок {trust_stats['ceiling']}) · window-eligible {trust_stats['eligible']} · active_trust_count {at} / window_eligible_count {trust_stats['eligible']}")
        print()
        for title, group in (("OC-тройка", draw["oc"]), ("Мейн-лента", draw["main"]), ("EXP-волна", draw["exp"])):
            print(f"### {title}")
            for c in group:
                print(f"- **{c['id']}** ({c['corridor']}, {c['exposureClass']}) — {c['reason']}")
            print()
        return 0
    print(f"=== ЖРЕБИЙ · T5-{batch_no} · seed {draw['seed']} · реестр camera {version} ===")
    print(f"окно съело: {draw['windowExcluded']} карт · позы окна съели: {draw['windowPosesExcluded']} · пул иссяк на: {draw['shortfall']} слотах")
    if trust_stats:
        st = trust_stats
        at = st["high"] + min(st["mid"], max(0, st["ceiling"] - st["high"]))
        mode = ("траст-CLOCK (HIGH+MID ≤ потолка)" if args.trust
                else "без траст-фильтра (окно/позы; --trust — режим CLOCK)")
        print(f"траст: активный пул CLOCK {at} карт · window-eligible {st['eligible']} · LOW −{st['low']} · {mode}")
        print(f"active_trust_count {at} / window_eligible_count {st['eligible']} (в бриф, Коул §7.3)")
    for title, group in (("OC", draw["oc"]), ("МЕЙН", draw["main"]), ("EXP", draw["exp"])):
        ids = " ".join(c["id"] for c in group)
        print(f"{title} ({len(group)}): {ids}")
    for c in draw["oc"] + draw["exp"][:2]:
        print(f"  {c['id']}: {c['reason']}")
    print("детерминизм: тот же for + тот же корпус → тот же расклад (паритет с прилавком/сервисом — векторы)")
    return 0


def cmd_heat(args) -> int:
    path = Path(args.batch)
    if not path.is_absolute():
        path = ROOT / path
    if not path.exists():
        print(f"батч не найден: {path}")
        return 1
    batch_no = gates.batch_number(path)
    usage = build_usage(batch_no)
    service_honesty = None
    if not args.no_service:
        service_honesty = honesty_from_service(args.service, path)
    heat = batch_heat(path, usage, service_honesty)
    print(f"=== ЖАР · {path.name} (партия №{heat['batch_no']}) ===")
    print(f"слотов: {heat['slots']} · рейтинговых: {heat['rated']} · R+-доля: {round(heat['rplus_share'] * 100)}%")
    print("коридоры:", " · ".join(f"{k}×{v}" for k, v in sorted(heat["corridor"].items())))
    print(f"карты: {heat['cards']} (свежих {heat['fresh']}) · каналов: {heat['channels_total']}"
          + (f" · дубли: {heat['channel_dupes']}" if heat["channel_dupes"] else ""))
    print(f"честность label↔fact: {heat['honesty']}")
    print(f"ЖАР: {heat['score']}/100 — {heat['label']}")
    print(heat["formula"])
    return 0


def cmd_audit(args) -> int:
    path = Path(args.batch)
    if not path.is_absolute():
        path = ROOT / path
    if not path.exists():
        print(f"батч не найден: {path}")
        return 1
    _, _, slots = gates.parse_batch(path)
    if not slots:
        print("нулевая парсинг батча — гейты бы сказали FAIL (контракт gates.py main); аудит нечего гонять")
        return 1
    payload = {"slots": [{"id": s.sid, "pos": s.pos, "badge": s.rating or "",
                          "corridor": s.corridor or "", "ycard": s.y_card or ""} for s in slots]}
    try:
        _, data = service_call(args.url, "/batch", payload, timeout=60.0)
    except (URLError, OSError, TimeoutError) as e:
        print(f"сервис {args.url} недоступен ({e.__class__.__name__}) — аудит партии делает только он;")
        print("подними: cd mini-services/oracle-service && bun start")
        return 2
    if not isinstance(data, dict) or "verdict" not in data:
        print("сервис ответил не audits-форматом:", str(data)[:300])
        return 3
    print(f"=== АУДИТ ОРАКУЛА · {path.name} ===")
    print(f"вердикт: {data['verdict']} · слотов: {data['slots_audited']}")
    print(f"FAIL-чеков: {data['fail_checks']} · WARN-чеков: {data['warn_checks']} · слотов FAIL: {data['failed_slots']}")
    w = data.get("weave", {})
    print(f"вплетение 1:1: {w.get('weaved_1_to_1', '?')}/{w.get('with_cards', '?')} (мимо: {w.get('misses', '?')})")
    print("коридоры:", " · ".join(f"{k}×{v}" for k, v in sorted(data.get("corridor_histogram", {}).items())))
    bad = [s for s in data.get("slots", []) if s.get("verdict") == "FAIL"]
    for s in bad[:10]:
        fails = [c["name"] for c in s.get("checks", []) if c.get("status") == "FAIL"]
        print(f"  {s.get('id')}: {'; '.join(fails) or 'агрегат'}")
    if len(bad) > 10:
        print(f"  … и ещё {len(bad) - 10}")
    print("вердикт автора — единственный законодатель (LAWS §9): это аудит слотов, не приговор партии")
    return 0


def cmd_selftest(_args) -> int:
    """Зеркало против золотых векторов: mulberry32 + жребий + окно + жар."""
    if not VECTORS_PATH.exists():
        print(f"векторы не найдены: {VECTORS_PATH}")
        return 3
    vectors = json.loads(VECTORS_PATH.read_text(encoding="utf-8"))
    failures = []

    for seed_str, expected in vectors.get("mulberry32", {}).items():
        rng = mulberry32(int(seed_str))
        got = [round(next(rng), 15) for _ in range(len(expected))]
        want = [round(x, 15) for x in expected]
        if got != want:
            failures.append(f"mulberry32(seed={seed_str}): {got[:3]}… ≠ {want[:3]}…")

    fx = vectors.get("fixture", {})
    cards = fx.get("cards", [])
    usage = {u["id"]: u for u in fx.get("usage", []).values()} if isinstance(fx.get("usage"), dict) is False else fx.get("usage", {})
    # usage в фикстуре — dict id → usage
    for batch_str, expected in vectors.get("draws", {}).items():
        draw = draw_constellation(int(batch_str), cards, usage,
                                  oc_target=3, main_target=9, exp_target=4, window_depth=3)
        for key in ("oc", "main", "exp"):
            got_ids = [c["id"] for c in draw[key]]
            if got_ids != expected[key]:
                failures.append(f"draw({batch_str}).{key}: {got_ids} ≠ {expected[key]}")
        for key in ("seed", "windowExcluded", "shortfall"):
            if draw[key] != expected[key]:
                failures.append(f"draw({batch_str}).{key}: {draw[key]} ≠ {expected[key]}")

    if failures:
        print("САМТЕСТ ЗЕРКАЛА: FAIL")
        for f in failures:
            print("  -", f)
        print("зеркало разошлось с каноном: сверить порядок корзин/rng в draw_constellation")
        return 3
    print("САМТЕСТ ЗЕРКАЛА: PASS — mulberry32, жребий и окна побитово совпадают с каноном (oracle-engine.ts)")
    return 0


# ════════════════════════ main ════════════════════════

# ══════════════ калибровочный мост (аудит 5.3 §3.1, волна 1) ══════════════
# Решения автора №2/№3 (2026-11-25): после рендера — послотовые метки сразу,
# мост запускаем «как только, так сразу». Рейтинг — домен №1 по жалобам
# (T5-29: 17 ложных R+; T5-31: «много где», урок В44) — получает 2-батчевый
# цикл честности вместо «отложено навсегда». Схема t5-verdict/1 дополнена
# ОПЦИОНАЛЬНЫМ полем rating_truth_delta — taste.py читает только известные
# поля, валидатор №15 читает schema/batch, так что старые вердикты живы.

TIER_RANK = {"PG-13": 0, "R": 1, "R+": 2}


def find_latest_receipt(batch, receipts_dir=None):
    """Новейшая гейт-квитанция партии по (дата, версия) из ИМЕНИ файла.
    mtime не участвует (аудит 2026-10-31, F2) — та же дисциплина дат, что
    в t5delivery.receipt_dates; receipts_dir — для тестов."""
    d = Path(receipts_dir) if receipts_dir else REPO / "specs" / "gate-receipts"
    stem = Path(batch).name
    if stem.endswith(".md"):
        stem = stem[: -len(".md")]
    best_key, best_path = None, None
    for p in d.glob("*.json"):
        m = t5delivery.RECEIPT_RE.match(p.name)
        if m and m.group(2) == stem:
            key = (m.group(1), int(m.group(3) or 0))
            if best_key is None or key > best_key:
                best_key, best_path = key, p
    return best_path


def cmd_rating_delta(args) -> int:
    """КАЛИБРОВОЧНЫЙ МОСТ: машинный тир слота (slot_table новейшей квитанции)
    против послотовых меток автора (verdicts/T5-NN.json → rating_truth_delta).

    Схема t5-verdict/1, опциональное поле (заполняет автор после рендера
    одним взглядом — по СПОРНЫМ слотам, не по всем 33):
      "rating_truth_delta": [
        {"slot": "P07", "truth": "R+", "note": "почему"}
      ]                truth ∈ R+ / R / PG-13

    Инструмент — LAB-отчёт: НИЧЕГО не переписывает. Правка словарей
    ratingTruth (specs/gates.json) — только по слову автора «калибровка
    принята»; после правки перезапинить калибровку В43
    (tests/python/test_t529_lessons.py на живом T5-29)."""
    stem = Path(args.batch).name
    if stem.endswith(".md"):
        stem = stem[: -len(".md")]
    rec_path = (Path(args.receipt) if args.receipt
                else find_latest_receipt(stem))
    if rec_path is None or not rec_path.exists():
        print(f"rating-delta: квитанция партии {stem} не найдена — "
              f"сначала прогони гейты (tools/gates.py)")
        return 1
    try:
        rec = json.loads(rec_path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"rating-delta: квитанция {rec_path.name} не читается — {e}")
        return 1
    table = {r.get("id"): r for r in rec.get("slot_table") or [] if r.get("id")}
    if not table:
        print("rating-delta: в квитанции пуст slot_table — нечем калибровать")
        return 1
    vpath = (Path(args.verdict) if args.verdict
             else REPO / "verdicts" / f"{stem}.json")
    if not vpath.exists():
        print(f"rating-delta: вердикта нет (verdicts/{stem}.json) — метки "
              f"автора придут с рендером; сравнивать не с чем (это не FAIL)")
        return 0
    try:
        verdict = json.loads(vpath.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"rating-delta: вердикт {vpath.name} не читается — {e}")
        return 1
    marks = verdict.get("rating_truth_delta") or []
    if not marks:
        print(f"rating-delta: в вердикте {vpath.name} нет rating_truth_delta — "
              f"послотовых меток автора не было; сравнивать не с чем")
        print('  схема (опционально в t5-verdict/1): "rating_truth_delta": '
              '[{"slot": "P07", "truth": "R+", "note": "почему"}]')
        return 0

    agree, false_rplus, missed_rplus, drift, unknown, illegal = [], [], [], [], [], []
    for m in marks:
        slot, truth = str(m.get("slot", "")), str(m.get("truth", ""))
        row = table.get(slot)
        if row is None:
            unknown.append(slot)
            continue
        mach = row.get("rating") or ""
        if truth not in TIER_RANK or mach not in TIER_RANK:
            illegal.append((slot, mach, truth, m.get("note")))
            continue
        if mach == truth:
            agree.append(slot)
        elif mach == "R+":
            false_rplus.append((slot, mach, truth,
                                row.get("channel") or "—", m.get("note")))
        elif truth == "R+":
            missed_rplus.append((slot, mach, truth,
                                 row.get("channel") or "—", m.get("note")))
        else:
            drift.append((slot, mach, truth,
                          row.get("channel") or "—", m.get("note")))

    print(f"rating-delta {stem}: квитанция {rec_path.name} · "
          f"вердикт {vpath.name} (машинный тир = slot_table квитанции)")
    print(f"— меток автора {len(marks)} · сошлось {len(agree)} · "
          f"ложных R+ {len(false_rplus)} · пропущенных R+ {len(missed_rplus)} · "
          f"дрейф {len(drift)}"
          + (f" · слот не найден {unknown}" if unknown else "")
          + (f" · нелегальный тир {len(illegal)}" if illegal else ""))

    def _rows(title, rows):
        if not rows:
            return
        print(f"— {title}:")
        for slot, mach, truth, extra, note in rows:
            line = f"    {slot}: машина {mach} → автор {truth} ({extra})"
            if note:
                line += f" — {note}"
            print(line)

    _rows("ЛОЖНЫЕ R+ (машина завысила — словари пропускают)", false_rplus)
    _rows("ПРОПУЩЕННЫЕ R+ (машина занизила — словари не видят)", missed_rplus)
    _rows("ДРЕЙФ (R↔PG-13 и прочее)", drift)
    if illegal:
        print("— нелегальные метки (ожидаю truth ∈ R+/R/PG-13):")
        for slot, mach, truth, note in illegal:
            print(f"    {slot}: машина {mach} → автор {truth!r}"
                  + (f" — {note}" if note else ""))
    if false_rplus:
        chans = {}
        for _slot, _m, _t, ch, _n in false_rplus:
            chans[ch] = chans.get(ch, 0) + 1
        print("— где смотреть в словарях ratingTruth (gates.json): каналы "
              "ложных — " + ", ".join(
                  f"{c}×{n}" for c, n in sorted(chans.items(), key=lambda kv: -kv[1])))
    print("— LAB: словари не тронуты; правка по слову автора «калибровка "
          "принята», после — перезапинить калибровку В43 "
          "(tests/python/test_t529_lessons.py)")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(prog="oracle.py", description="ECCHI-ORACLE CLI печи (эра ORACLE-2)")
    parser.add_argument("--url", default=DEFAULT_URL, help=f"oracle-service URL (по умолчанию {DEFAULT_URL})")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("status", help="пульс сервиса")
    sub.add_parser("selftest", help="зеркало жребия против золотых векторов")

    p_window = sub.add_parser("window", help="окно ротации Y-карт")
    p_window.add_argument("--for", dest="for_batch", default="", help="номер партии (чьё прошлое смотрим)")
    p_window.add_argument("--depth", type=int, default=3, help="глубина окна (0 — выключить)")

    p_pool = sub.add_parser("pool", help="активный пул Y-карт (аудит Коула R5)")
    p_pool.add_argument("--for", dest="for_batch", required=True, help="номер партии: T5-28")
    p_pool.add_argument("--depth", type=int, default=3, help="глубина окна ротации")
    p_pool.add_argument("--ids", action="store_true", help="печатать id карт пула")

    p_draw = sub.add_parser("draw", help="жребий карт на партию")
    p_draw.add_argument("--for", dest="for_batch", required=True, help="номер партии: T5-27")
    p_draw.add_argument("--oc", type=int, default=3)
    p_draw.add_argument("--main", type=int, default=21)
    p_draw.add_argument("--exp", type=int, default=9)
    p_draw.add_argument("--depth", type=int, default=3)
    p_draw.add_argument("--md", action="store_true", help="маркдауном (вставляется в бриф)")
    p_draw.add_argument("--trust", action="store_true",
                        help="режим CLOCK: жребий только по траст-пулу HIGH+MID ≤ 80 (specs/y-trust.json, Коул §7; заказ автора 2026-11-23)")

    p_trust = sub.add_parser("trust", help="траст-слой Y: HIGH/MID/LOW из JSON-вердиктов (Коул §7)")
    p_trust.add_argument("--rebuild", action="store_true",
                         help="пересобрать specs/y-trust.json из verdicts/*.json")

    p_heat = sub.add_parser("heat", help="жар партии")
    p_heat.add_argument("batch", help="путь до батча (batches/T5-26.md)")
    p_heat.add_argument("--service", default=DEFAULT_URL, help="URL сервиса для честности label↔fact")
    p_heat.add_argument("--no-service", action="store_true", help="без сервиса (честность = нейтрально)")

    p_audit = sub.add_parser("audit", help="агрегированный аудит партии сервисом")
    p_audit.add_argument("batch", help="путь до батча")
    p_audit.add_argument("--url", default=DEFAULT_URL)

    p_delta = sub.add_parser(
        "rating-delta",
        help="калибровочный мост: машинный тир (квитанция) vs послотовые метки автора (rating_truth_delta) — LAB, ничего не правит")
    p_delta.add_argument("--batch", required=True, help="партия: T5-32 или batches/T5-32.md")
    p_delta.add_argument("--verdict", default="", help="путь к вердикту (по умолчанию verdicts/<партия>.json)")
    p_delta.add_argument("--receipt", default="", help="путь к квитанции (по умолчанию новейшая по имени)")

    args = parser.parse_args()
    if args.cmd == "status":
        return cmd_status(args)
    if args.cmd == "window":
        return cmd_window(args)
    if args.cmd == "pool":
        return cmd_pool(args)
    if args.cmd == "draw":
        return cmd_draw(args)
    if args.cmd == "trust":
        return cmd_trust(args)
    if args.cmd == "heat":
        return cmd_heat(args)
    if args.cmd == "audit":
        return cmd_audit(args)
    if args.cmd == "rating-delta":
        return cmd_rating_delta(args)
    if args.cmd == "selftest":
        return cmd_selftest(args)
    parser.error(f"неизвестная команда: {args.cmd}")
    return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(1)
    except BrokenPipeError:
        sys.exit(0)
    except Exception as e:  # краш = exit 3 + баннер, как gates.py
        print(f"ORACLE CLI: КРАШ — {e.__class__.__name__}: {e}", file=sys.stderr)
        print("это баг инструмента, не гейта: приложи вывод к issues", file=sys.stderr)
        sys.exit(3)
