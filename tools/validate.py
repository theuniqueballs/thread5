#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
THREAD 5 — валидатор спек (ревизия 2026-11-01, docs/THREAD5-REVIEW-2026-11-01.md,
1.3 + 1.15 + 2.1 + 2.5 + 1.11b).

Прогоняется ДО gates.py (и в pre-commit): specs/*.json правятся руками и
никем не валидировались — одна опечатка в ключе конфига, битый JSON,
переименованный статус, и гейт МОЛЧА выключается: прогон показывает PASS,
потому что проверки просто нет. Молчание должно шуметь.

Проверяет:
  1. каждый specs/*.json парсится (1.3);
  2. gates.json: обязательные секции на месте, файлы-реестры существуют (1.3);
     2026-11-20: список секций догнан до v1.15.0 (negBase…detailsGate) и
     ВСЕ конфиг-регексы компилируются (не только headerContract) — битый
     паттерн раньше ронял гейт в трейсбек на самом прогоне;
  3. delivery-stats.json: id каналов уникальны, статусы легальны,
     exempt-каналы существуют; пересечения с burn-реестром (1.15);
  4. races.json: id уникальны, статусы легальны, карантин gates.json
     согласован со статусами races.json (1.15);
  5. burned.json: коды уникальны; hair-eye-library.json / oc-canon.json —
     структура, на которой стоят гейты (1.3); camera.json — y_cards непуст
     и формат id валиден (2026-11-20: пустой реестр ослеплял yStamp);
  6. docstring gates.py не отстаёт от версии gates.json (2.5);
  7. policy.json ↔ gates.json: решение по POS-бюджету одно, не три (2.1);
  8. pre-commit хук установлен: core.hooksPath=.githooks (1.11b) —
     свежий клон без setup.sh коммитит без замка молча.
     2026-11-20: флаг --ci (или env T5_VALIDATE_CI=1) пропускает проверку
     хука — в CI/артефактах хука нет и не должно быть;
  9. moves-ledger.json: структура реестра ходов (директива роста
     2026-11-01, идея 3): id M## уникальны, retired/standing легальны,
     applications числятся, отставка только вердиктом, триггер-индекс
     указывает только на известные ходы (v1.7.0);
 10. header-contract: applyFrom — int, паттерны компилируются (v1.7.0).

Прогон:
    python3 tools/validate.py           # рабочая станция (хук проверяется)
    python3 tools/validate.py --ci      # CI/артефакт (без проверки хука)
Выход: 0 = PASS, 1 = FAIL (блокирует pre-commit и прогонку батчей).
"""

import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SPEC = ROOT / "specs"

CHANNEL_STATUSES = {"live", "dead", "rehab", "artifact", "candidate", "special"}
RACE_STATUSES = {"active", "gold", "banned", "quarantine"}
# 2026-11-20: догнано до gates.json v1.15.0 — секции, которые gates.py
# читает через GATES.get(...): отсутствующая секция = гейт МОЛЧА выключен,
# а валидатор печатал PASS (ровно та failure-мода, против которой он стоит)
REQUIRED_GATES_KEYS = [
    "claim", "claimGate", "ocClassGate", "charSpecGate", "pos", "neg",
    "copypaste", "crossBatch", "channels", "registry", "posFloors",
    "raceCast", "burn", "header", "headerContract", "movesGate",
    "storyCardsGate",
    # эры 1.8.0–1.15.0
    "negBase", "formatGate", "corridorAudit", "claimPhysics", "yCards",
    "yStamp", "comboPose", "conceptFlag", "negDressGuards", "detailsGate",
]

# режим CI: без проверки хука (в раннере хука нет — проверка №8 не про него)
CI_MODE = "--ci" in sys.argv or os.environ.get("T5_VALIDATE_CI") == "1"

fails = []


def fail(msg):
    fails.append(msg)


def _walk_regexes(node, path="gates.json"):
    """2026-11-20: рекурсивно ищем строки-паттерны в ключах-регексах
    (pattern, bannedMarkers, noClassPattern, stem-списки не трогаем) и
    проверяем, что каждый компилируется — битый паттерн роняет gates.py
    в трейсбек на живом прогоне вместо валидации на коммите."""
    RE_KEYS = {"pattern", "bannedMarkers", "noClassPattern"}
    if isinstance(node, dict):
        for k, v in node.items():
            if k in RE_KEYS:
                patterns = v if isinstance(v, list) else [v]
                for p in patterns:
                    if isinstance(p, str):
                        try:
                            re.compile(p)
                        except re.error as e:
                            fail(f"{path} → {k}: паттерн {p!r} не компилируется — {e}")
            else:
                _walk_regexes(v, f"{path}.{k}")
    elif isinstance(node, list):
        for i, v in enumerate(node):
            _walk_regexes(v, f"{path}[{i}]")


def main():
    # ── 1. все specs/*.json парсятся ─────────────────────────────────────
    spec_files = sorted(SPEC.glob("*.json"))
    data = {}
    for p in spec_files:
        try:
            data[p.name] = json.loads(p.read_text(encoding="utf-8"))
        except Exception as e:
            fail(f"specs/{p.name}: JSON не парсится — {e}")
    print(f"JSON парсится: {len(data)}/{len(spec_files)}")

    gates = data.get("gates.json")
    if gates is None:
        fail("specs/gates.json не читается — гейты слепы")
    else:
        # ── 2. обязательные секции gates.json ────────────────────────────
        for k in REQUIRED_GATES_KEYS:
            if k not in gates:
                fail(f"gates.json: нет секции «{k}» — гейты на ней молча выключены")
        # 2026-11-20: все конфиг-регексы компилируются (см. _walk_regexes)
        _walk_regexes(gates)
        # файлы-реестры существуют
        refs = []
        cs = gates.get("charSpecGate") or {}
        if "hairEyeRegistry" in cs:
            refs.append(("charSpecGate.hairEyeRegistry", cs["hairEyeRegistry"]))
        pf = gates.get("posFloors") or {}
        if "ocNamesRegistry" in pf:
            refs.append(("posFloors.ocNamesRegistry", pf["ocNamesRegistry"]))
        mg = gates.get("movesGate") or {}
        if "ledger" in mg:
            refs.append(("movesGate.ledger", mg["ledger"]))
        ch = gates.get("channels") or {}
        if "registry" in ch:
            refs.append(("channels.registry", ch["registry"]))
        if "burnRegistry" in ch:
            refs.append(("channels.burnRegistry", ch["burnRegistry"]))
        reg = gates.get("registry") or {}
        for k in ("palettes", "poses", "kinetics", "carriers"):
            if k in reg:
                refs.append((f"registry.{k}", reg[k]))
        cp = gates.get("copypaste") or {}
        if "canonWhitelist" in cp:
            refs.append(("copypaste.canonWhitelist", cp["canonWhitelist"]))
        for label, rel in refs:
            if not (ROOT / rel).exists():
                fail(f"gates.json → {label}: файла «{rel}» нет — гейты упадут или промолчат")

        # ── 6. docstring gates.py не отстаёт (2.5) ──────────────────────
        try:
            gpy = (ROOT / "tools/gates.py").read_text(encoding="utf-8")
            ver = str(gates.get("version", ""))
            if ver and f"v{ver}" not in gpy:
                fail(f"gates.py docstring: нет «v{ver}» — версии дрейфуют (ревизия 2.5)")
        except Exception as e:
            fail(f"tools/gates.py не читается — {e}")

        # ── 7. policy ↔ gates: POS-бюджет (2.1) ─────────────────────────
        pol = data.get("policy.json")
        if pol:
            law = pol.get("law") or {}
            unlimited = (gates.get("pos") or {}).get("unlimited")
            pt = law.get("posTargetTokens", "?")
            ph = law.get("posHardTokens", "?")
            if unlimited and not (pt is None and ph is None):
                fail(
                    f"POS-бюджет: gates.pos.unlimited=true, а policy law несёт "
                    f"{pt}/{ph} — три источника правды (ревизия 2.1: исправить policy/LAWS)"
                )
            if not unlimited and pt is None:
                fail("POS-бюджет: gates.pos.unlimited=false, а policy law posTargetTokens=null — рассинхрон")

        # ── 8. хук установлен (1.11b); CI-режим пропускает (2026-11-20) ──
        if not CI_MODE:
            try:
                hp = subprocess.run(
                    ["git", "config", "core.hooksPath"],
                    capture_output=True, text=True, cwd=ROOT,
                ).stdout.strip()
            except Exception:
                hp = ""
            if hp != ".githooks":
                fail(
                    f"pre-commit хук не стоит (core.hooksPath={hp!r}) — свежий клон "
                    f"коммитит без sha-замка молча; запусти: bash setup.sh (ревизия 1.11)"
                )

    # ── 3. каналы (delivery-stats.json) ──────────────────────────────────
    ds = data.get("delivery-stats.json")
    chs = []
    if ds:
        chs = ds.get("channels") or []
        ids = [c.get("id") for c in chs]
        dupes = sorted({i for i in ids if ids.count(i) > 1})
        if dupes:
            fail(f"delivery-stats.json: дубликаты каналов {dupes}")
        for c in chs:
            if c.get("status") not in CHANNEL_STATUSES:
                fail(
                    f"delivery-stats.json: канал {c.get('id')!r} статус "
                    f"{c.get('status')!r} вне легального набора {sorted(CHANNEL_STATUSES)}"
                )
        if gates:
            for exempt in (gates.get("channels") or {}).get("exempt", []):
                if exempt not in ids:
                    fail(f"gates.json channels.exempt → «{exempt}» не существует в delivery-stats.json")

    # ── burn-реестр: коды уникальны; пересечения с каналами (1.15) ──────
    burned = data.get("burned.json")
    if burned:
        entries = burned.get("entries") or []
        codes = [e.get("code") for e in entries]
        dupes = sorted({c for c in codes if codes.count(c) > 1})
        if dupes:
            fail(f"burned.json: дубликаты кодов {dupes}")
        if ds:
            bset = set(codes)
            for c in chs:
                if c.get("id") in bset:
                    fail(
                        f"delivery-stats.json: канал «{c.get('id')}» одновременно "
                        f"в burn-реестре со статусом {c.get('status')!r} — сожжённое не живёт (ревизия 1.15)"
                    )

    # ── 4. расы (races.json) ─────────────────────────────────────────────
    races = data.get("races.json")
    if races:
        rl = races.get("races") or []
        rids = [r.get("id") for r in rl]
        dupes = sorted({i for i in rids if rids.count(i) > 1})
        if dupes:
            fail(f"races.json: дубликаты id {dupes}")
        for r in rl:
            if r.get("status") not in RACE_STATUSES:
                fail(
                    f"races.json: {r.get('id')!r} статус {r.get('status')!r} "
                    f"вне легального набора {sorted(RACE_STATUSES)}"
                )
        if gates:
            for q in (gates.get("raceCast") or {}).get("quarantine", []):
                row = next((r for r in rl if r.get("id") == q), None)
                if row is None:
                    fail(f"gates.json raceCast.quarantine: «{q}» нет в races.json")
                elif row.get("status") not in ("quarantine", "banned"):
                    fail(
                        f"gates.json raceCast.quarantine: «{q}» в races.json статус "
                        f"{row.get('status')!r} — карантин должен быть согласован со статусом расы"
                    )

    # ── 5. структуры, на которых стоят гейты ────────────────────────────
    cam = data.get("camera.json")
    if cam:
        # 2026-11-20: пустой/битый y_cards ослеплял yStamp молча (карты «не
        # найдены», проверки вплетения пропускались) — теперь это FAIL валидатора
        cards = (cam.get("y_cards") or {}).get("cards") or []
        if not cards:
            fail("camera.json: y_cards.cards пуст — yCardGate/yStamp слепнут (проверь структуру)")
        bad_ids = [c.get("id") for c in cards if not (isinstance(c.get("id"), str) and re.fullmatch(r"Y\d{1,3}", c["id"]))]
        if bad_ids:
            fail(f"camera.json: id карт вне формата Y{{NNN}} — {bad_ids[:5]}")
    he = data.get("hair-eye-library.json")
    if he:
        for k in ("hair", "eyes"):
            v = he.get(k)
            if not isinstance(v, list) or not v or not all(isinstance(x, str) and x for x in v):
                fail(f"hair-eye-library.json: «{k}» — пустой/битый список, char-spec ослепнет")
    occ = data.get("oc-canon.json")
    if occ:
        ocs = occ.get("ocs") or {}
        if not ocs:
            fail("oc-canon.json: ростер пуст — имена/канон-гейты ослепнут")
        for k, o in ocs.items():
            if not isinstance(o, dict) or not o.get("name"):
                fail(f"oc-canon.json: «{k}» без поля name — гейты имени ослепнут")

    # ── 9. moves-ledger.json (директива роста 2026-11-01, идея 3) ──────
    ml = data.get("moves-ledger.json")
    if ml:
        rules = ml.get("rules") or {}
        if not rules.get("retireOnlyByVerdict"):
            fail(
                "moves-ledger.json: rules.retireOnlyByVerdict не выставлен — "
                "машина не имеет права отставлять ходы (LAWS §9)"
            )
        ws = rules.get("wearWarnStreak")
        if not isinstance(ws, int) or ws < 2:
            fail(f"moves-ledger.json: wearWarnStreak={ws!r} — нужен int ≥ 2")
        if gates:
            gw = (gates.get("movesGate") or {}).get("wearStreak")
            if gw is not None and gw != ws:
                fail(
                    f"wearWarnStreak: moves-ledger.json={ws}, gates.json={gw} — "
                    "два источника правды по порогу износа"
                )
        moves = ml.get("moves") or []
        mids = [m.get("id") for m in moves]
        dupes = sorted({i for i in mids if mids.count(i) > 1})
        if dupes:
            fail(f"moves-ledger.json: дубликаты id ходов {dupes}")
        for m in moves:
            mid = m.get("id", "?")
            if not (isinstance(mid, str) and re.fullmatch(r"M\d{2,3}", mid)):
                fail(f"moves-ledger.json: id «{mid}» вне формата M##(##)")
            if not m.get("name") or not isinstance(m.get("triggers"), list):
                fail(f"moves-ledger.json: {mid} без name/triggers — триггер-закон ослепнет")
            if not isinstance(m.get("standing"), bool):
                fail(f"moves-ledger.json: {mid} без standing (bool) — movesGate не отличит ход-закон от приёма")
            if m.get("retired") is not None and not isinstance(m.get("retired"), str):
                fail(f"moves-ledger.json: {mid} retired должен быть null или строкой-вердиктом")
            if not isinstance(m.get("applications"), list):
                fail(f"moves-ledger.json: {mid} без applications — счёт износа молчит")
        ti = ml.get("triggerIndex") or {}
        for key, ids in ti.items():
            if not isinstance(ids, list) or not ids:
                fail(f"moves-ledger.json: triggerIndex[«{key}»] пуст — закон триггера не зависит от памяти")
            for i in ids:
                if i not in mids:
                    fail(f"moves-ledger.json: triggerIndex[«{key}»] указывает на неизвестный ход «{i}»")

    # ── 10. header-contract: applyFrom int, паттерны компилируются ──────
    if gates:
        for req in (gates.get("headerContract") or {}).get("require", []):
            af = req.get("applyFrom")
            if af is not None and not isinstance(af, int):
                fail(f"headerContract.{req.get('key')}: applyFrom={af!r} — нужен int или отсутствие")
            try:
                re.compile(req.get("pattern", ""))
            except re.error as e:
                fail(f"headerContract.{req.get('key')}: pattern не компилируется — {e}")

    # ── 11. pose-references: PL-ссылки в батчах существуют в poses.json ──
    # (находка T5-16: stories.md/00-brief ссылались на PL349–PL357 — кастом-карты,
    #  а X1-семья живёт на PL358–PL366; сданный JSON был прав, карточки — нет.
    #  Битая PL-ссылка молча уезжает в промпт-доки и ломает ротацию/учёт first-use.)
    try:
        import glob as _glob
        _poses_path = SPEC / "poses.json"
        if _poses_path.exists():
            _pose_ids = {p.get("id") for p in json.loads(_poses_path.read_text(encoding="utf-8")).get("poses", [])}
            _pl_re = re.compile(r"\bPL\d{2,4}\b")
            for _md_s in sorted(_glob.glob(str(ROOT / "batches" / "**" / "*.md"), recursive=True)):
                _md = Path(_md_s)
                _text = _md.read_text(encoding="utf-8")
                for _pl in sorted(set(_pl_re.findall(_text))):
                    if _pl not in _pose_ids:
                        fail(f"{_md.relative_to(ROOT)}: PL-ссылка «{_pl}» не существует в poses.json — битый ID (проверка №11)")
    except FileNotFoundError:
        pass  # poses.json отсутствует — поймано проверкой №1

    # ── вердикт ──────────────────────────────────────────────────────────
    if fails:
        print("ВАЛИДАТОР: FAIL")
        for f in fails:
            print(f"  ✗ {f}")
        sys.exit(1)
    print("ВАЛИДАТОР: PASS — спеки согласованы, молчание гейтов исключено")
    sys.exit(0)


if __name__ == "__main__":
    main()
