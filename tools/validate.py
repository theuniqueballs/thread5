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
 10. header-contract: applyFrom — int, паттерны компилируются (v1.7.0);
 11. PL-ссылки в batches/**/*.md существуют в poses.json (находка T5-16);
 12. delivery-index.json (двойной аудит 2026-11-20, P0-06): каждая партия
     T5-*.md имеет явный статус draft/ready/delivered/superseded/archived;
     записи без файла (кроме archived — файлы в archive/, аудит 5.3 волна 0)
     и файлы без записи — FAIL; окно/жребий/CI читают только
     delivered (tools/t5delivery.py — единственный модуль сдачи);
 13. gate-report.md ≡ новейшей JSON-квитанции той же партии (P0-04):
     версия гейтов / sha256 / вердикт / счётчики FAIL-WARN совпадают;
     отчёт — производная квитанции (gates.py --md-from-receipt);
 14. gate-registry.json (P0-05): каждая секция gates.json имеет живую
     impl-функцию в gates.py и поле в квитанции; множество секций ==
     REQUIRED-списку; прямые тесты считаются, долги без теста — видимый
     список, не молчание.
 15. y-trust.json свеж (не отстаёт от verdicts/*.json) — жребий CLOCK не
     ходит по протухшему доверию (Коул §7).
 16. жизненный цикл волн палитр (аудит 5.3, волна 1 — режим «пробуем»):
     trial-палитра «trial до вердикта T5-NN», после которой сдано ≥2 партий,
     а судьба волны не решена — печатается видимым списком (FAIL включится
     словом автора после разбора бэклога).

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

# тикет #1 (2026-11-28, платформенная честность): валидатор гоняется в
# pre-commit и вручную на каждой платформе — cp1251-консоль не роняет
# печать ×/§/→ (строки FAIL-причин несут их постоянно)
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass  # python < 3.7 или экзотика — работаем как работали

ROOT = Path(__file__).resolve().parent.parent
SPEC = ROOT / "specs"

CHANNEL_STATUSES = {"live", "dead", "rehab", "artifact", "candidate", "special"}
RACE_STATUSES = {"active", "gold", "banned", "quarantine"}
# 2026-11-20: догнано до gates.json v1.15.0 — секции, которые gates.py
# читает через GATES.get(...): отсутствующая секция = гейт МОЛЧА выключен,
# а валидатор печатал PASS (ровно та failure-мода, против которой он стоит)
# 2026-11-21 (двойной аудит, P0-05 «объявленный гейт ≠ работающий»):
# + paletteSkin — живой прецедент: секция была объявлена в v1.16.0, а
#   REQUIRED-список молчал — валидатор не заметил бы её исчезновение.
REQUIRED_GATES_KEYS = [
    "claim", "claimGate", "ocClassGate", "charSpecGate", "pos", "neg",
    "copypaste", "crossBatch", "channels", "registry", "posFloors",
    "raceCast", "burn", "header", "headerContract", "movesGate",
    "storyCardsGate",
    # эры 1.8.0–1.16.0
    "negBase", "formatGate", "corridorAudit", "claimPhysics", "yCards",
    "yStamp", "comboPose", "conceptFlag", "negDressGuards", "detailsGate",
    "paletteSkin",
    # эра 1.17.0 (дыра закрыта 2026-11-22: жил в gates.json без реестра)
    "yStack",
    # эра 1.18.0 — уроки T5-29 (В39–В43)
    "voltCore", "exquisiteMain", "expHypothesis", "ratingTruth",
    # эра 1.21.0 — урок T5-34 (В51)
    "ratingMass",
    # эра 1.23.0 — урок T5-34 (В55, ПЛАН 5.5 T6.2)
    "negCanonGuard",
    # эра 1.24.0 — урок T5-34 (В45, ПЛАН 5.5 T1.2)
    "voltRun",
    # эра 1.25.0 — урок T5-34 (В54, ПЛАН 5.5 T4.2)
    "themeEcho",
    # эра 1.26.0 — тикет #2 (К-1: «объявлено ≠ исполнено» исправлено)
    "k1Sense",
    # эра 1.27.0 — тикет #5 (В56: fact-слой заявки R+)
    "claimFact",
    # эра 1.29.0 — вердикт T5-35 (В57/В58: literal-ню-слой R+)
    "nudeTruth",
    # эра 1.30.0 — тикет #7 (В61: данбоору-носители R+)
    "carrierTruth",
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


def palette_selfbans(palettes):
    """№17 (тикет #3): палитра не запрещает собственную суть. Возвращает
    список (id, forbidden, причина) — кислотная семья (acid|lsd|neon в
    id/family) не может держать 'neon'/'vivid colors'/'saturated colors'
    в forbidden. Чистая функция — тест класса живёт в
    tests/python/test_palette_selfban.py (класс не вернётся в волну 19)."""
    out = []
    for p in palettes or []:
        pid = str(p.get("id") or "")
        fam = str(p.get("family") or "")
        acid_wave = re.search(r"acid|lsd|neon", (pid + " " + fam), re.I)
        if not acid_wave:
            continue  # оплаченный класс — суть волны, не любые цвета
        for f in p.get("forbidden") or []:
            fl = str(f).strip().lower()
            if fl in ("neon", "vivid colors", "saturated colors"):
                out.append((pid, f, "суть волны"))
                break
    return out


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

    # ── 12. delivery-index: каждая партия имеет статус, статусы легальны ──
    # (двойной аудит 2026-11-20, P0-06: черновик T5-NN.md без записи в индексе
    #  молча считался «сданным» — лез в окно ротации, жребий и CI; теперь
    #  specs/delivery-index.json — единственный источник, tools/t5delivery.py
    #  — единственный читатель для окна/жребия/гейтов/CI)
    DELIVERY_STATUSES = {"draft", "ready", "delivered", "superseded", "archived"}
    di = data.get("delivery-index.json")
    if di is None:
        fail("specs/delivery-index.json отсутствует — статус сдачи партий живёт мимо системы (проверка №12, аудит P0-06)")
    else:
        rows = di.get("batches") or []
        indexed = {}
        for row in rows:
            name, status = row.get("batch"), row.get("status")
            if not name or status not in DELIVERY_STATUSES:
                fail(f"delivery-index.json: битая запись {row!r} — batch обязателен, status ∈ {sorted(DELIVERY_STATUSES)}")
                continue
            # 2026-11-23 (Коул §4): mode в записи — из брифа партии; мусор
            # в mode не молчит (счётчик CLOCK-дисциплины читает его же)
            if "mode" in row and row["mode"] not in ("CLOCK", "LAB", "SURGERY", "SPECIAL"):
                fail(f"delivery-index.json: партия «{name}» — битый mode {row['mode']!r} ∈ CLOCK/LAB/SURGERY/SPECIAL (проверка №12)")
            if name in indexed:
                fail(f"delivery-index.json: партия «{name}» записана дважды")
            indexed[name] = status
        for md in (ROOT / "batches").glob("T5-*.md"):
            if md.name.endswith(".gate-report.md"):
                continue
            stem = md.name[: -len(".md")]
            if stem not in indexed:
                fail(f"delivery-index.json: нет записи для «{stem}» — впиши статус (draft/ready/delivered/superseded/archived), черновик без записи считается сданным (проверка №12)")
        for stem, st in indexed.items():
            if st == "archived":
                continue  # файлы живут в archive/ (T5-28, аудит 5.3 волна 0)
            if not (ROOT / "batches" / f"{stem}.md").exists():
                fail(f"delivery-index.json: запись «{stem}» без файла batches/{stem}.md")

    # ── 13. Markdown gate-report не отстаёт от JSON-квитанции ──────────
    # (двойной аудит 2026-11-20, P0-04: отчёт T5-27 показывал gates v1.15.0,
    #  а живая квитанция — v1.16.0 с paletteSkin; доказательство PASS
    #  показывало старую норму. Отчёт — ПРОИЗВОДНАЯ от квитанции: версия
    #  гейтов, sha, вердикт и счётчики обязаны совпадать с новейшей
    #  JSON-квитанцией той же партии)
    def _receipt_sort_key(p):
        # 2026-11-18-T5-24-v2-act2.json → (2026-11-18, 2); суффиксы после
        # -vN (act2/baseline/ystamp-*) легальны; диагностические без -vN
        # (ystamp-broken/synthetic, baseline) сортируются ниже нумерованных
        m = re.match(r"(\d{4}-\d{2}-\d{2})-(T5-\d+R?|SO-\d+)(?:-v(\d+))?(?:-[a-z0-9-]+)?\.json$", p.name)
        if not m:
            return None
        return (m.group(1), int(m.group(3) or 0))

    receipts_by_batch = {}
    for rp in (SPEC / "gate-receipts").glob("*.json"):
        try:
            rd = json.loads(rp.read_text(encoding="utf-8"))
        except Exception:
            continue
        b = rd.get("batch", "")
        receipts_by_batch.setdefault(b, []).append(rp)

    md_verdict_re = re.compile(r"Вердикт гейтов: \*\*(PASS|FAIL)\*\* \(FAIL (\d+) / WARN (\d+)\)")
    md_sha_re = re.compile(r"sha256: `([0-9a-f]{64})`")
    md_ver_re = re.compile(r"specs/gates\.json v([\d.]+)")
    for report_dir, pattern in ((ROOT / "batches", "T5-*.gate-report.md"), (ROOT / "special", "SO-*.gate-report.md")):
        if not report_dir.exists():
            continue
        for rep in report_dir.glob(pattern):
            stem = rep.name[: -len(".gate-report.md")]
            batch_key = f"{report_dir.name}/{stem}.md"
            candidates = receipts_by_batch.get(batch_key) or []
            if not candidates:
                continue  # до-квитанционная эра — нечем сверять
            keyed = [(k, p) for k, p in ((_receipt_sort_key(p), p) for p in candidates) if k]
            if not keyed:
                continue
            newest = max(keyed, key=lambda kp: kp[0])[1]
            rd = json.loads(newest.read_text(encoding="utf-8"))
            tool_ver = re.search(r"v([\d.]+)", str(rd.get("tool", "")))
            md_text = rep.read_text(encoding="utf-8")
            mv = md_verdict_re.search(md_text)
            ms = md_sha_re.search(md_text)
            mr = md_ver_re.search(md_text)
            if not (mv and ms and mr):
                fail(f"{rep.name}: не парсится шапка отчёта (вердикт/sha/версия) — формат сломан (проверка №13)")
                continue
            md_verdict, md_fails, md_warns = mv.group(1), int(mv.group(2)), int(mv.group(3))
            problems = []
            if mr.group(1) != (tool_ver.group(1) if tool_ver else None):
                problems.append(f"версия гейтов {mr.group(1)} ≠ квитанции {tool_ver.group(1) if tool_ver else '?'}")
            if ms.group(1) != rd.get("sha256"):
                problems.append(f"sha256 не совпадает с квитанцией")
            if md_verdict != rd.get("verdict") or md_fails != len(rd.get("fails", [])) or md_warns != len(rd.get("warns", [])):
                problems.append(
                    f"вердикт {md_verdict} {md_fails}F/{md_warns}W ≠ квитанции "
                    f"{rd.get('verdict')} {len(rd.get('fails', []))}F/{len(rd.get('warns', []))}W"
                )
            if problems:
                fail(f"{rep.name}: отстаёт от {newest.name} — {'; '.join(problems)}; перегенерируй: python3 tools/gates.py {batch_key} --md {report_dir.name}/{rep.name} (проверка №13, аудит P0-04)")

    # ── 14. gate registry: секция → impl → receiptField ─────────────────
    # (двойной аудит 2026-11-20, P0-05 «объявленный гейт ≠ работающий»:
    #  paletteSkin был объявлен в gates.json v1.16.0, но не было способа
    #  проверить, что за секцией стоит живой код и поле квитанции. Реестр
    #  specs/gate-registry.json — карта цепочки; валидатор сверяет её с
    #  реальностью: impl-функции существуют в gates.py, поля собираются
    #  в receipt, множество секций == обязательному списку)
    reg = data.get("gate-registry.json")
    if reg is None:
        fail("specs/gate-registry.json отсутствует — реестр «гейт → код → квитанция» обязателен (проверка №14, аудит P0-05)")
    else:
        try:
            gpy_src = (ROOT / "tools/gates.py").read_text(encoding="utf-8")
        except Exception as e:
            gpy_src = ""
            fail(f"tools/gates.py не читается — {e}")
        reg_sections = []
        tested, untested = [], []
        for row in reg.get("gates") or []:
            sec = row.get("section")
            if not sec:
                fail(f"gate-registry.json: запись без section — {row!r}")
                continue
            reg_sections.append(sec)
            impls = row.get("impl") or []
            if not impls:
                fail(f"gate-registry.json: секция «{sec}» без impl — кто её исполняет? (проверка №14)")
            for fn in impls:
                if gpy_src and not re.search(rf"^def {re.escape(str(fn))}\(", gpy_src, re.M):
                    fail(f"gate-registry.json: секция «{sec}» → impl «{fn}» не существует в tools/gates.py — гейт объявлен, но не исполняется (проверка №14, аудит P0-05)")
            rf = row.get("receiptField")
            if rf:
                leaf = str(rf).split(".")[-1]
                if gpy_src and f'"{leaf}"' not in gpy_src:
                    fail(f"gate-registry.json: секция «{sec}» → receiptField «{rf}» не собирается в квитанции gates.py — результат проверки не доезжает до доказательства (проверка №14)")
            if row.get("test"):
                tested.append(sec)
                tp = ROOT / str(row["test"])
                if not tp.exists():
                    fail(f"gate-registry.json: секция «{sec}» → тест {row['test']} не существует (проверка №14)")
            else:
                untested.append(sec)
        # множество секций == REQUIRED_GATES_KEYS == ключи gates.json
        missing_in_reg = [k for k in REQUIRED_GATES_KEYS if k not in reg_sections]
        extra_in_reg = [k for k in reg_sections if k not in REQUIRED_GATES_KEYS]
        if missing_in_reg:
            fail(f"gate-registry.json: секций нет в реестре {missing_in_reg} — объявлены в gates.json, но не отражены (проверка №14)")
        if extra_in_reg:
            fail(f"gate-registry.json: лишние секции {extra_in_reg} — нет в REQUIRED-списке валидатора (проверка №14)")
        if gates:
            gate_sections_missing = [k for k in REQUIRED_GATES_KEYS if k not in gates]
            if gate_sections_missing:
                fail(f"gates.json: нет секций {gate_sections_missing} — гейты на них молча выключены")
        print(
            f"gate-registry: {len(reg_sections)} секций · прямые тесты {len(tested)} · "
            f"без прямого теста {len(untested)} (долги видимы: {', '.join(untested) or '—'})"
        )

    # ── проверка №15: траст-слой Y (заказ автора 2026-11-23, Коул §7) ────
    # y-trust.json — сгенерированный реестр (oracle.py trust --rebuild):
    # после каждого нового verdicts/*.json он обязан быть перестроен, иначе
    # жребий CLOCK молча ходит по протухшему доверию.
    vjson = []
    if (ROOT / "verdicts").exists():
        for p in sorted((ROOT / "verdicts").glob("*.json")):
            try:
                if json.loads(p.read_text(encoding="utf-8")).get("schema") == "t5-verdict/1":
                    vjson.append(p)
            except Exception:
                continue
    ytrust = data.get("y-trust.json")
    if vjson and ytrust is None:
        fail("specs/y-trust.json отсутствует при живых JSON-вердиктах — построй траст-слой: "
             "python3 tools/oracle.py trust --rebuild (проверка №15, Коул §7)")
    elif ytrust is not None:
        src_files = [s.get("file") for s in (ytrust.get("sources") or [])]
        want = [p.name for p in vjson]
        if src_files != want:
            fail(f"y-trust.json отстаёт от verdicts/*.json (в реестре {src_files}, на диске {want}) — "
                 "перегенерируй: python3 tools/oracle.py trust --rebuild (проверка №15)")
        cards = ytrust.get("cards") or {}
        bad_trust = [cid for cid, c in cards.items() if c.get("trust") not in ("HIGH", "MID", "LOW")]
        if bad_trust:
            fail(f"y-trust.json: карты с неизвестным уровнем доверия {bad_trust} (проверка №15)")
        cam = data.get("camera.json") or {}
        cam_ids = {c.get("id") for c in ((cam.get("y_cards") or {}).get("cards") or [])}
        ghosts = [cid for cid in cards if cam_ids and cid not in cam_ids]
        if ghosts:
            fail(f"y-trust.json: карты не из camera.json {ghosts} (проверка №15)")
        st = ytrust.get("stats") or {}
        print(f"y-trust: {ytrust.get('version')} · партий {st.get('judged_batches', 0)} · "
              f"HIGH {st.get('high', 0)} · MID {st.get('mid', 0)} · LOW {st.get('low', 0)} · "
              f"потолок CLOCK {int((ytrust.get('policy') or {}).get('ceiling') or 0)}")

    # ── №16 (аудит 5.3, волна 1 — решение автора №4 «пробуем»): волны палитр
    # trial-палитра «trial до вердикта T5-NN»: после NN сдано ≥2 партий, а
    # судьба волны не решена (поле trial не снято) — правило промоции
    # (слово автора «волна принята» → trial снят = canon; непринятая волна
    # старше 2 партий не перекатывается). Режим «пробуем»: список виден
    # на каждом прогоне/pre-commit, FAIL включится словом автора после
    # разбора бэклога — машина не решает судьбу волн сама.
    pal = data.get("palettes.json")
    if pal and di is not None:
        delivered_nums = [
            int(re.match(r"T5-(\d+)R?$", s).group(1))
            for s, st in indexed.items()
            if st == "delivered" and re.match(r"T5-(\d+)R?$", s)
        ]
        newest_del = max(delivered_nums) if delivered_nums else None
        trial_re = re.compile(r"до вердикта (T5-\d+)")
        stale = []
        for p in pal.get("palettes") or []:
            tr = p.get("trial")
            if not tr or newest_del is None:
                continue
            m = trial_re.search(str(tr))
            if not m:
                continue
            if newest_del - int(m.group(1)[3:]) >= 2:
                stale.append((p.get("id"), str(tr)))
        waves = sorted({t.split()[-1] for _i, t in stale})
        if stale:
            print(
                f"волны (№16, WARN «пробуем»): trial-палитр {len(stale)} старше "
                f"2 партий от своего вердикта ({', '.join(waves)}) — реши судьбу "
                f"(canon → снять trial / снятие с ротации), правило промоции"
            )
        else:
            print("волны (№16): trial-протухших 0 — правило промоции соблюдено")

    # ── №17 (вердикт T5-34 §2.2, ПЛАН 5.5 T4.3; тикет #3): палитра не
    # запрещает собственную суть. Волна-18 «кислота» несла тему именами, а
    # содержимое гасила собственным forbidden («neon» в кислотной палитре =
    # класс ошибки: палитра запрещает то, чем она является). Решение автора
    # 2026-11-27 (тикет #3): «неон не виноват — тему хуёво раскрыл писец» —
    # 30 самозапретов lsd_wave_18 сняты (palettes 1.21.1), волна жива в
    # каноне; 'muddy colors'/'photo color' остались (защита палитры).
    # Проверка живёт дальше: класс «тематическая волна не наследует
    # forbidden из словаря мёртвой темы» не должен вернуться в волну 19 —
    # тест tests/python/test_palette_selfban.py тамперит кислотную палиту
    # с 'neon' и требует ловлю.
    if pal:
        self_ban = palette_selfbans(pal.get("palettes"))
        if self_ban:
            fams = sorted({str(p.get("family")) for p in pal.get("palettes") or []
                           if any(b[0] == p.get("id") for b in self_ban)})
            print(
                f"палитры (№17, WARN «пробую»): самозапретов {len(self_ban)} "
                f"({', '.join(fams)}) — палитра запрещает то, чем она является "
                "(вердикт T5-34 §2.2: тема живёт содержимым, не именем); "
                "судьба волны — решение автора (ПЛАН T4.4), FAIL включится "
                "словом; примеры: "
                + "; ".join(f"{b[0]} → {b[1]!r} ({b[2]})" for b in self_ban[:3])
            )
        else:
            print("палитры (№17): самозапретов 0 — суть волн не гасится")

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
