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
  3. delivery-stats.json: id каналов уникальны, статусы легальны,
     exempt-каналы существуют; пересечения с burn-реестром (1.15);
  4. races.json: id уникальны, статусы легальны, карантин gates.json
     согласован со статусами races.json (1.15);
  5. burned.json: коды уникальны; hair-eye-library.json / oc-canon.json —
     структура, на которой стоят гейты (1.3);
  6. docstring gates.py не отстаёт от версии gates.json (2.5);
  7. policy.json ↔ gates.json: решение по POS-бюджету одно, не три (2.1);
  8. pre-commit хук установлен: core.hooksPath=.githooks (1.11b) —
     свежий клон без setup.sh коммитит без замка молча.

Прогон:
    python3 tools/validate.py
Выход: 0 = PASS, 1 = FAIL (блокирует pre-commit и прогонку батчей).
"""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SPEC = ROOT / "specs"

CHANNEL_STATUSES = {"live", "dead", "rehab", "artifact", "candidate", "special"}
RACE_STATUSES = {"active", "gold", "banned", "quarantine"}
REQUIRED_GATES_KEYS = [
    "claim", "claimGate", "ocClassGate", "charSpecGate", "pos", "neg",
    "copypaste", "crossBatch", "channels", "registry", "posFloors",
    "raceCast", "burn", "header", "headerContract",
]

fails = []


def fail(msg):
    fails.append(msg)


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
        # файлы-реестры существуют
        refs = []
        cs = gates.get("charSpecGate") or {}
        if "hairEyeRegistry" in cs:
            refs.append(("charSpecGate.hairEyeRegistry", cs["hairEyeRegistry"]))
        pf = gates.get("posFloors") or {}
        if "ocNamesRegistry" in pf:
            refs.append(("posFloors.ocNamesRegistry", pf["ocNamesRegistry"]))
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

        # ── 8. хук установлен (1.11b) ───────────────────────────────────
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
