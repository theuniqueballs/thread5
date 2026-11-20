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

# кириллица в cp1251-пайпе (Windows-консоль) не должна ронять печать — как gates.py
try:
    sys.stdout.reconfigure(errors="replace")
    sys.stderr.reconfigure(errors="replace")
except (AttributeError, ValueError):
    pass

ROOT = REPO
DEFAULT_URL = "http://127.0.0.1:3031"
VECTORS_PATH = REPO / "tests" / "fixtures" / "oracle_vectors.json"

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
        })
    cards.sort(key=lambda c: card_num(c["id"]))
    return data.get("version", "—"), cards


def corpus_batches():
    """Партии корпуса: [(no, path)] по номеру; канонический парсер — gates."""
    out = []
    for p in (ROOT / "batches").glob("T5-*.md"):
        if p.name.endswith(".gate-report.md"):
            continue
        no = gates.batch_number(p)
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


def draw_constellation(batch_no, cards, usage, oc_target=3, main_target=21, exp_target=9, window_depth=3):
    """Побитовое зеркало drawConstellation (oracle-engine.ts). Порядок
    корзин, сортировок и rng-вызовов свято совпадает — иначе векторы падают."""
    # окно: последние window_depth партий прошлого
    past_nos = sorted({u["lastBatch"] for u in usage.values() if u["lastBatch"] and u["lastBatch"] < batch_no})
    window_nos = set(past_nos[-window_depth:] if window_depth > 0 else [])

    def in_window(cid):
        u = usage.get(cid)
        return bool(u and u["lastBatch"] in window_nos)

    usable = [c for c in cards
              if c["id"] and card_num(c["id"]) > 0 and c["pattern"].strip() and not in_window(c["id"])]
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
    draw = draw_constellation(batch_no, cards, usage,
                              oc_target=args.oc, main_target=args.main,
                              exp_target=args.exp, window_depth=args.depth)
    if args.md:
        print(f"## Жребий оракула — партия №{batch_no} (seed {draw['seed']})")
        print()
        print(f"Реестр: camera {version} · {len(cards)} карт · окно ротации: {args.depth} партий")
        print()
        for title, group in (("OC-тройка", draw["oc"]), ("Мейн-лента", draw["main"]), ("EXP-волна", draw["exp"])):
            print(f"### {title}")
            for c in group:
                print(f"- **{c['id']}** ({c['corridor']}, {c['exposureClass']}) — {c['reason']}")
            print()
        return 0
    print(f"=== ЖРЕБИЙ · T5-{batch_no} · seed {draw['seed']} · реестр camera {version} ===")
    print(f"окно съело: {draw['windowExcluded']} карт · пул иссяк на: {draw['shortfall']} слотах")
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

def main() -> int:
    parser = argparse.ArgumentParser(prog="oracle.py", description="ECCHI-ORACLE CLI печи (эра ORACLE-2)")
    parser.add_argument("--url", default=DEFAULT_URL, help=f"oracle-service URL (по умолчанию {DEFAULT_URL})")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("status", help="пульс сервиса")
    sub.add_parser("selftest", help="зеркало жребия против золотых векторов")

    p_window = sub.add_parser("window", help="окно ротации Y-карт")
    p_window.add_argument("--for", dest="for_batch", default="", help="номер партии (чьё прошлое смотрим)")
    p_window.add_argument("--depth", type=int, default=3, help="глубина окна (0 — выключить)")

    p_draw = sub.add_parser("draw", help="жребий карт на партию")
    p_draw.add_argument("--for", dest="for_batch", required=True, help="номер партии: T5-27")
    p_draw.add_argument("--oc", type=int, default=3)
    p_draw.add_argument("--main", type=int, default=21)
    p_draw.add_argument("--exp", type=int, default=9)
    p_draw.add_argument("--depth", type=int, default=3)
    p_draw.add_argument("--md", action="store_true", help="маркдауном (вставляется в бриф)")

    p_heat = sub.add_parser("heat", help="жар партии")
    p_heat.add_argument("batch", help="путь до батча (batches/T5-26.md)")
    p_heat.add_argument("--service", default=DEFAULT_URL, help="URL сервиса для честности label↔fact")
    p_heat.add_argument("--no-service", action="store_true", help="без сервиса (честность = нейтрально)")

    p_audit = sub.add_parser("audit", help="агрегированный аудит партии сервисом")
    p_audit.add_argument("batch", help="путь до батча")
    p_audit.add_argument("--url", default=DEFAULT_URL)

    args = parser.parse_args()
    if args.cmd == "status":
        return cmd_status(args)
    if args.cmd == "window":
        return cmd_window(args)
    if args.cmd == "draw":
        return cmd_draw(args)
    if args.cmd == "heat":
        return cmd_heat(args)
    if args.cmd == "audit":
        return cmd_audit(args)
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
