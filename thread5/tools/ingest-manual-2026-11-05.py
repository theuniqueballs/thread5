#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
INGEST — посылка Коула (Грок) «Composition Manual A–E» → реестры specs.
Разложение по решению писца (2026-11-05, вербатим живёт в
docs/COMPOSITION-MANUAL.md):
  Stage A → poses.json   (+manual_cards, +manual_family_quotas,
                          +h11_checklist, +t5_corpus_map)
  Stage B → camera.json  (+framing_ladder F1–F8, +grok_presets S/L/R,
                          +genre_camera_map, +camera_tier_effects,
                          +camera_top_errors, +batch_caps.cowboy_cap,
                          +anti_echo_law, +manual_map_note)
  Stage C → rating-techniques.json (+grok_packages α–κ, +anti_mono_quotas,
                          +mood_codes M-01…07, +implication_engines I-01…07)
  Stage D/E → docs only (молекулы/архив — вербатим в мануале).
Коды Коула (D/A/F/S/L/R/P13/M/I/Dx) — его словарь; местный — D#/CAM##
(camera.json). Конфликт B9 (камера в первых токенах) против местного
pos_language (кадровая строка последняя, рендер-проверено T5-11/12) —
писец не решает молча: вопрос автору (E11+1).
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = Path("/home/z/my-project/upload/T5-COMPOSITION-MANUAL-STAGE")
text = SRC.read_text(encoding="utf-8")
lines = text.splitlines()


def clean(s: str) -> str:
    s = s.strip()
    s = re.sub(r"\*\*(.+?)\*\*", r"\1", s)
    s = s.replace("`", "").replace("  ", " ").strip()
    return s


# ── Stage A: карточки поз ────────────────────────────────────────────────
def parse_stage_a():
    cards, quotas, corpus_map, checklist = [], [], [], []
    fam, fam_sub = None, None
    i = 0
    in_a10, in_a11, in_a12 = False, False, False
    while i < len(lines):
        ln = lines[i]
        m = re.match(r"^# (A\d)\. СЕМЬЯ «(.+?)»", ln)
        if m and not ln.startswith("###"):
            fam, fam_sub = m.group(1), clean(lines[i + 1]) if i + 1 < len(lines) and lines[i + 1].startswith("###") else ""
            i += 1
            continue
        if re.match(r"^# A10\.", ln):
            in_a10, in_a11, in_a12 = True, False, False
            i += 1
            continue
        if re.match(r"^# A11\.", ln):
            in_a10, in_a11, in_a12 = False, True, False
            i += 1
            continue
        if re.match(r"^# A12\.", ln):
            in_a10, in_a11, in_a12 = False, False, True
            i += 1
            continue
        if re.match(r"^# A13\.", ln):
            in_a10 = in_a11 = in_a12 = False
            i += 1
            continue
        m = re.match(r"^### (A\d-\d\d) · (.+)$", ln)
        if m:
            card = {"code": m.group(1), "name": clean(m.group(2)), "family": fam or (m.group(1)[:2]), "fields": {}}
            i += 1
            while i < len(lines) and lines[i].strip():
                b = re.match(r"^-\s+\*\*(.+?):\*\*\s+(.+)$", lines[i])
                if b:
                    card["fields"][clean(b.group(1))] = clean(b.group(2))
                i += 1
            cards.append(card)
            continue
        if in_a10 and ln.startswith("| A"):
            cells = [clean(c) for c in ln.split("|")[1:-1]]
            if len(cells) >= 4:
                quotas.append({"family": cells[0], "min": cells[1], "max": cells[2], "note": cells[3]})
        if in_a11 and ln.strip().startswith("- [ ]"):
            checklist.append(clean(ln.strip()[5:]))
        if in_a12 and ln.startswith("|"):
            cells = [clean(c) for c in ln.split("|")[1:-1]]
            if len(cells) == 2 and cells[0] not in ("Уже в корпусе", "---"):
                corpus_map.append({"in_corpus": cells[0], "family": cells[1]})
        i += 1
    return cards, quotas, checklist, corpus_map


# ── Stage B: пресеты S/L/R, жанры, тир, ошибки ───────────────────────────
def parse_stage_b():
    presets = {"S": [], "L": [], "R": []}
    genre_map, tier_effects, errors = [], [], []
    mode = None
    for ln in lines:
        if ln.startswith("# B5."):
            mode = "presets"
            continue
        if ln.startswith("# B6."):
            mode = None
        if ln.startswith("# B7."):
            mode = "genre"
            continue
        if ln.startswith("# B8."):
            mode = "tier"
            continue
        if ln.startswith("# B9."):
            mode = None
        if ln.startswith("# B10."):
            mode = "errors"
            continue
        if ln.startswith("# B11."):
            mode = None
        if not ln.strip():
            continue
        if mode == "presets" and ln.startswith("| **"):
            cells = [clean(c) for c in ln.split("|")[1:-1]]
            if len(cells) >= 4 and re.match(r"^[SLR]\d$", cells[0]):
                presets[cells[0][0]].append(
                    {"code": cells[0], "dxa": cells[1], "tags_core": cells[2],
                     "why": cells[3] if len(cells) < 5 else cells[3] + " · " + cells[4]}
                )
        elif mode == "genre" and ln.startswith("| **"):
            cells = [clean(c) for c in ln.split("|")[1:-1]]
            if len(cells) == 3:
                genre_map.append({"genre": cells[0], "priority": cells[1], "avoid": cells[2]})
        elif mode == "tier" and ln.startswith("| **"):
            cells = [clean(c) for c in ln.split("|")[1:-1]]
            if len(cells) == 3:
                tier_effects.append({"tier": cells[0], "boosters": cells[1], "killers": cells[2]})
        elif mode == "errors" and re.match(r"^\d+\.", ln.strip()):
            errors.append(clean(re.sub(r"^\d+\.\s*", "", ln.strip())))
    return presets, genre_map, tier_effects, errors


# ── Stage C: пакеты α–κ, M-коды, I-движки, анти-моно ─────────────────────
def parse_stage_c():
    packages, moods, engines, anti_mono = [], [], [], []
    i = 0
    mode = None
    while i < len(lines):
        ln = lines[i]
        if ln.startswith("# C4."):
            mode = "mood"
            i += 1
            continue
        if ln.startswith("# C5."):
            mode = "engines"
            i += 1
            continue
        if ln.startswith("# C6."):
            mode = "packages"
            i += 1
            continue
        if ln.startswith("# C7."):
            mode = "antimono"
            i += 1
            continue
        if re.match(r"^# C[89]\.", ln):
            mode = None
            i += 1
            continue
        m = re.match(r"^### Пакет (\S+) · (.+)$", ln)
        if m and mode == "packages":
            pkg = {"id": m.group(1), "name": clean(m.group(2)), "fields": {}}
            i += 1
            while i < len(lines) and lines[i].strip() and lines[i].startswith("- "):
                b = re.match(r"^-\s+(.+?):\s+(.+)$", lines[i])
                if b:
                    pkg["fields"][clean(b.group(1))] = clean(b.group(2))
                i += 1
            packages.append(pkg)
            continue
        if ln.startswith("| M-") and mode == "mood":
            cells = [clean(c) for c in ln.split("|")[1:-1]]
            if len(cells) == 4:
                moods.append({"id": cells[0], "technique": cells[1], "pos_nl": cells[2], "effect": cells[3]})
        if ln.startswith("| I-") and mode == "engines":
            cells = [clean(c) for c in ln.split("|")[1:-1]]
            if len(cells) == 4:
                engines.append({"id": cells[0], "engine": cells[1], "how": cells[2], "tier": cells[3]})
        if mode == "antimono" and ln.strip().startswith("- "):
            b = re.match(r"^-\s+(.+?)\s+([≤≥])\s+(\d+)%", ln.strip())
            if b:
                anti_mono.append({"channels": b.group(1), "op": b.group(2), "pct": int(b.group(3))})
        i += 1
    return packages, moods, engines, anti_mono


def dump(path: Path, data: dict, indent: int):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=indent) + "\n", encoding="utf-8")


def main():
    cards, quotas, checklist, corpus_map = parse_stage_a()
    presets, genre_map, tier_effects, errors = parse_stage_b()
    packages, moods, engines, anti_mono = parse_stage_c()

    print(f"Stage A: карточек {len(cards)}, квот {len(quotas)}, чеклист {len(checklist)}, корпус-мап {len(corpus_map)}")
    print(f"Stage B: пресетов S{len(presets['S'])}/L{len(presets['L'])}/R{len(presets['R'])}, жанры {len(genre_map)}, тир {len(tier_effects)}, ошибок {len(errors)}")
    print(f"Stage C: пакетов {len(packages)}, M-кодов {len(moods)}, I-движков {len(engines)}, анти-моно {len(anti_mono)}")

    # ── poses.json ──
    pp = ROOT / "specs/poses.json"
    poses = json.loads(pp.read_text(encoding="utf-8"))
    assert poses["version"] == "1.0.0", poses["version"]
    poses["version"] = "1.1.0"
    poses["manual_addendum"] = {
        "born": "2026-11-05",
        "source": "посылка Коула (Грок) «Composition Manual» Stage A, вербатим: docs/COMPOSITION-MANUAL.md; ингест tools/ingest-manual-2026-11-05.py",
        "law": "карточки A1-01…A9-04 — КАНДИДАТЫ, не пул ротации: в poses[] не входят, окно/burn не жгут. При первом использовании в батче писец выдаёт PL-код (с PL241), карточка входит в окно как обычная поза. Тройка H-11 (вес+вещь+взгляд) и фаза H-12 обязательны для VOLT/EXP; семя автора (A1) только с камерой-коридором (A15/R1-класс), не с ковбоем-глаз-уровнем.",
        "corpus_note": "не дублировать живой корпус: маппинг A12 в t5_corpus_map (PL104 dance-break, T5-10 floor-slide/moon/bike/shadow, Nix reflection lag, M05 catch — уже живы)",
        "family_quotas": quotas,
        "h11_checklist": checklist,
        "t5_corpus_map": corpus_map,
        "cards": cards,
    }
    dump(pp, poses, 2)

    # ── camera.json ──
    cp = ROOT / "specs/camera.json"
    cam = json.loads(cp.read_text(encoding="utf-8"))
    assert cam["version"] == "1.0.0", cam["version"]
    cam["version"] = "1.1.0"
    cam["framing_ladder"] = {
        "F1": {"name": "центр-формал", "pos": "centered composition, symmetrical framing", "note": "икона/EXQUISITE/обложка; стерильно при формальной позе; ≤3/батч"},
        "F2": {"name": "трети", "pos": "rule of thirds composition", "note": "рабочая лошадка; воздух со стороны взгляда"},
        "F3": {"name": "срез тела", "pos": "cropped composition, frame cuts at the hips / at the forehead", "note": "R+ если срез по claim-зоне — мозг достраивает; genital NEG обязателен"},
        "F4": {"name": "негатив-простор", "pos": "lots of negative space, small figure", "note": "одиночество; NICHE-друг"},
        "F5": {"name": "кадр-в-кадре", "pos": "frame within frame (doorway, window, legs arch)", "note": "сильнейший анти-стерильный фрейм"},
        "F6": {"name": "воздух на взгляд", "pos": "lead room, looking room", "note": "обязателен при gaze off-frame, иначе «смотрит в стену»"},
        "F7": {"name": "грязный кадр", "pos": "out of focus foreground, blurry railing in front", "note": "свидетель ближе нас; риск: модель замылит всё"},
        "F8": {"name": "зеркальный сплит", "pos": "mirror reflection showing a second angle", "note": "R9-класс; риск двойной анатомии"},
    }
    cam["grok_presets"] = {
        "source": "Composition Manual Stage B5 (Cole/Grok, 2026-11-04); коды S/L/R — словарь Коула, теги-ядро переносимо",
        "stable": presets["S"],
        "live": presets["L"],
        "rcam": presets["R"],
        "law": "R-пресеты = R+ камерой без claim-токенов (H-10): коридор A1 + R1, POV-пол R3, замочная скважина R4; A1-поза + ковбой-глаз-уровень = убить семя (D11).",
    }
    cam["genre_camera_map"] = genre_map
    cam["camera_tier_effects"] = tier_effects
    cam["camera_top_errors"] = errors
    cam["anti_echo_law"] = "соседние слоты не делят одну клетку D×A и не держат одну семью поз + один вес + один gaze (анти-эхо, Manual A10/B6)."
    cam["batch_caps"]["cowboy_cap_D4"] = "≤5 на 21 мейн / ≤7 на 33 total (Manual B6, анти-ковбой вердикта T5-12)"
    cam["manual_map_note"] = (
        "словарь Коула ≠ местный: Cole-D1…D7 ≈ местные D1…D7 (у нас есть ещё D8-деталь); Cole-A01…A12 — своя нумерация углов, "
        "местные CAM-коды A01–A16 остаются рабочими (пример: Cole-A03 extreme-low ≈ местные A03-снизу/A15-нижняя-линия-взгляда; "
        "Cole-A08 back ≈ местный A07-со-спины). Ось F (фрейминг) — НОВАЯ, принята как F1–F8. Конфликт порядка: Cole-B9 требует "
        "камеру в первых 10–20 токенах POS, местный pos_language держит кадровую строку последней у face-блока (рендер-проверено "
        "T5-11/12) — не менять без вердикта автора (CONSILIUM 2026-11-05, вопрос №6)."
    )
    dump(cp, cam, 1)

    # ── rating-techniques.json ──
    rp = ROOT / "specs/rating-techniques.json"
    rt = json.loads(rp.read_text(encoding="utf-8"))
    assert rt["version"] == "1.1.0", rt["version"]
    rt["version"] = "1.2.0"
    rt["grok_packages"] = {
        "born": "2026-11-05",
        "source": "Composition Manual Stage C6 (Cole/Grok); вербатим: docs/COMPOSITION-MANUAL.md",
        "law": "R+ слот = ОДИН пакет + один hard-claim (G20); пакеты чередуются (ритм анти-моно D10), ζζζ никогда.",
        "packages": packages,
    }
    rt["anti_mono_quotas"] = {
        "source": "Manual C7, предложение CONSILIUM (анти-моно вердикта T5-12)",
        "note": "доли от всех R+ слотов батча; γ/δ/η/ι = 0 → снова моноканал «соски на ткани»",
        "quotas": anti_mono,
    }
    rt["mood_codes"] = moods
    rt["implication_engines"] = engines
    dump(rp, rt, 2)

    print("specs обновлены: poses.json → 1.1.0, camera.json → 1.1.0, rating-techniques.json → 1.2.0")
    return 0


if __name__ == "__main__":
    sys.exit(main())
