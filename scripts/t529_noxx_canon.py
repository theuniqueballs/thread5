#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""T5-29 вердикт, исполнение №1: NOXX → ОС-канон (canon 2.13.0 → 2.14.0).

Приказ автора (вердикт T5-29, 2026-11-22, вербатим): «особенно - 32 слот.
Забираем в ОС, даём ей имя - Noxx. Выдашь ей пакет ос-канона.»
Механика — прецедент Noir/Nier (T5-23, «десятая канонизация прямым приказом,
конверсия EXP-кандидата»): Noxx — одиннадцатая, ПЕРВАЯ из реестра
oc-candidates.json (пункт Д). Канон = PH-промпт автора VERBATIM.

Также: oc-candidates.json 1.1.0 → 1.2.0 (P32 promoted, прочие 8 — вердикт
«понравились, не забраны»), open-hypotheses.json — H-13 (кандидат-клетки).
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SPEC = ROOT / "specs"

PH_PROMPT = (
    "Masterpiece, best quality, absurdres, intricate details, eye-level close-up "
    "through clear vinyl, upper body, strap slipped off the shoulder's slope, 1girl, "
    "solo, depth-black hair in a ghost-layer shag, pale glowing face and silver-grey "
    "eyes, black skin with soft star-glow flecks, shadow girl, edges blurring into "
    "shade, human face, small high-set chest, slim waist, mid_strapslide, the tee's "
    "strap slipped off the shoulder's slope, the collarbone taking the strap's old "
    "line, the clear vinyl's gloss planes over everything, nothing underneath the "
    "negotiation but the light she argued in — the negotiated light is the claim, "
    "diplomacy-made, strap slipped off the shoulder's slope + the collarbone taking "
    "the strap's old line the vinyl raincoat's planes catching white points of "
    "corridor light, the mohair pushed to both elbows in a soft grey bundle, lace "
    "gloves at the wrist-line, her shadow already waiting at the wall, the strap's "
    "old line honest in the collarbone's hollow, the knot's ribs-claim flat and "
    "dark, the strap off the shoulder's slope, the collarbone holding its line, the "
    "corridor's threshold brackets long cold and hung with quiet, the aurora's "
    "seam-teal replacing whatever they once held, the wall holding her early shadow "
    "like a coat, Dusk Binding palette, dusk-bind-violet over corridor-stone, "
    "seam-light-teal at the edges, star-fleck-pale points; her colors: the dark "
    "that fits her."
)

VERDICT_QUOTE = (
    "особенно - 32 слот. Забираем в ОС, даём ей имя - Noxx. Выдашь ей пакет "
    "ос-канона."
)

NOXX = {
    "name": "Noxx",
    "tarot": (
        "Two of Swords (assistant-assigned 2026-11-22, pending author veto) — "
        "ШЕСТАЯ младшая аркана канона. Два скрещённых клинка на весу, глаза не "
        "повязаны — она смотрит на обе стороны сразу: перемирие, которое держится "
        "сами. Свет не борется с тьмой — договаривается (the negotiated light)."
    ),
    "element": (
        "SEAM (assistant-assigned 2026-11-22, pending author veto) — шов света: "
        "seam-teal кромка, по которой тьма торгуется со светом; линия сияния, "
        "заменившая то, что раньше висело на кронштейнах порога. Не SHADOW (Lua) — "
        "Noxx несёт не стихию тени, а линию договора между светом и темнотой."
    ),
    "zodiac": (
        "Libra (assistant-assigned 2026-11-22; SHARED с Lyn и Una — третий "
        "носитель, flagged; pending author veto) — весы: дипломат по профессии и "
        "по знаку; равновесие, которое держится переговорами, а не силой."
    ),
    "birth": (
        "promoted from T5-29 P32 'shadow-strap-slide' (EXP · R45 Shadow-kin · R+ · "
        "Y9 · P268_DUSK_BINDING; вербатим вердикта T5-29 2026-11-22: «" + VERDICT_QUOTE + "») "
        "— одиннадцатая канонизация прямым приказом, конверсия EXP-кандидата; "
        "ПЕРВАЯ промоция из реестра oc-candidates.json (пункт Д, 1.1.0: пуля на "
        "продвижение сработала с первой боевой партии реестра)."
    ),
    "race": (
        "R45 Shadow-kin — её тень приходит раньше неё и остаётся на такт позже; "
        "чёрная кожа с мягкими искрами-звёздами (глубина, а не отсутствие), края "
        "размываются в сумрак; бледное светящееся лицо — единственная яркая точка "
        "в кадре; свет не борется с ней — договаривается сквозь прозрачность."
    ),
    "appearance_lock": (
        "ЛОК по канону VERBATIM PH-промпта автора (T5-29 P32, вердикт 2026-11-22, "
        "полный текст — поле ph_prompt_verbatim): depth-black hair in a ghost-layer "
        "shag, pale glowing face and silver-grey eyes, black skin with soft "
        "star-glow flecks, edges blurring into shade, human face, small high-set "
        "chest, slim waist; виниловый плащ просветом, мохер спущен к локтям мягким "
        "серым тюком, футболка узлом у рёбер, кружевные перчатки у линии запястий; "
        "её тень уже ждёт у стены."
    ),
    "ph_prompt_verbatim": PH_PROMPT,
    "hair": (
        "depth-black hair in a ghost-layer shag — призрачный слоистый шэг цвета "
        "глубокой черноты; фирменная стрижка-слои (ghost-layer), чёрная ось волос "
        "уникальна формой, не цветом."
    ),
    "eyes": (
        "silver-grey eyes — серебристо-серые на бледно светящемся лице; бледное "
        "светящееся лицо — единственное в каноне (яркая точка сумрака)."
    ),
    "skin": (
        "black skin with soft star-glow flecks — чёрная кожа с мягкими "
        "искрами-звёздами: глубина, а не отсутствие. Тёмная ось канона разведена "
        "трижды: Vae (obsidian + striking red), Noir (eclipse-dusk + umbral-purple), "
        "Noxx (star-fleck чёрный + silver-grey)."
    ),
    "body_type": (
        "BT-12 (Маленькая гордость), FAM-C (B2-B3): small high-set chest, slim "
        "waist (писцово по PH-промпту автора; pending автор-вето)"
    ),
    "signature_marks": [
        "edges blurring into shade — края тела размываются в сумрак: кромка-переговор между плотью и тенью",
        "её тень приходит раньше и уходит позже — эскорт у стены (her shadow already waiting at the wall)",
        "star-glow flecks на чёрной коже — созвездие, которое она носит собой",
    ],
    "emotional_register": (
        "diplomacy register — дипломатия света: свет не борется с ней и она не "
        "борется со светом; бретель легла на ключицу — линия принята обеими "
        "сторонами; тишина порога («long cold and hung with quiet»)."
    ),
    "anti_shield": (
        "bright daylight, harsh light, white room, shadow gone, vinyl opaque, "
        "star-flecks absent, glowing skin, red eyes, blue eyes, blonde hair, "
        "large breasts"
    ),
    "neg_additions": "vinyl opaque, shadow gone, star-flecks absent, harsh light",
    "collision_note": (
        "Noxx (depth-black ghost-layer shag · silver-grey · star-fleck чёрная кожа) "
        "vs Vae (obsidian + striking red) и Noir (eclipse-dusk + umbral-purple) — "
        "тёмная ось кожи разведена трижды: у Noxx звёздная пыль на черноте и "
        "серебряно-серый глаз; vs Lua (SHADOW) — элемент разведён: Noxx несёт SEAM "
        "(шов света), не стихию тени; бледное светящееся лицо — единственное в "
        "каноне, ни у кого больше лицо не светится."
    ),
    "canonical_garment": (
        "clear vinyl raincoat (gloss planes) + oversized mohair pushed to both "
        "elbows + slim cotton tee knotted at the ribs + lace elbow gloves — слои "
        "дипломатии: прозрачный винил делает её видимой, мохер — мягкий серый тюк "
        "у локтей, узел футболки держит линию рёбер (канон-рендер P32, Y9 strap "
        "slipped off the shoulder's slope)."
    ),
    "id": "noxx",
    "active": True,
    "render_receipts": [
        "T5-29 P32 'shadow-strap-slide' (EXP · R45 Shadow-kin · R+ · Y9 strap "
        "slipped off the shoulder's slope + the collarbone taking the strap's old "
        "line · P268_DUSK_BINDING; вердикт автора 2026-11-22: «" + VERDICT_QUOTE + "»)"
    ],
    "wardrobe_policy": (
        "signature: clear vinyl raincoat + mohair at elbows + knotted tee — винил "
        "просветом (SHEER-пара), мохер пучком у локтей, узел у рёбер; звёздная "
        "пыль кожи видима всегда, когда зона в кадре; канон-цвета VERBATIM: "
        "dusk-bind-violet over corridor-stone, seam-light-teal, star-fleck-pale "
        "(Dusk Binding, волна 13 «свет подземелья» — trial палитра подтверждена "
        "промоцией)."
    ),
    "signature_prompt_tokens": (
        "depth-black hair in a ghost-layer shag, pale glowing face and silver-grey "
        "eyes, black skin with soft star-glow flecks — VERBATIM в первых ~10 "
        "токенах тег-рана (hard-флор §2.4); призрачный шэг и звёздная пыль — "
        "ОТДЕЛЬНЫМИ клозами (урок В28 с рождения канона)"
    ),
}


def main():
    # ── 1. oc-canon.json: Noxx + реестры + заметка + версия ──────────────
    canon_p = SPEC / "oc-canon.json"
    canon = json.loads(canon_p.read_text(encoding="utf-8"))
    assert "Noxx" not in canon["ocs"], "Noxx уже в каноне"
    canon["ocs"]["Noxx"] = NOXX
    canon["canon_version"] = "2.14.0"
    canon["registries"]["tarot"] += (
        "\nNoxx — Two of Swords (assistant-assigned 2026-11-22, вето открыто; "
        "шестая младшая аркана — скрещённые клинки на весу, перемирие, которое "
        "держится само: свет договаривается, не побеждает)."
    )
    canon["registries"]["element"] += (
        "\nNoxx — SEAM (assistant-assigned 2026-11-22, вето открыто; шов света: "
        "seam-teal кромка договора между светом и темнотой; НЕ SHADOW — стихия "
        "тени занята Lua)."
    )
    canon["registries"]["zodiac"] += (
        "\nNoxx — Libra (assistant-assigned 2026-11-22; SHARED с Lyn и Una — "
        "третий носитель, flagged; вето открыто)."
    )
    canon["notes"].append(
        "2026-11-22 v2.14.0 — NOXX PROMOTED from T5-29 P32 'shadow-strap-slide' "
        "(вердикт: «особенно - 32 слот. Забираем в ОС, даём ей имя - Noxx. Выдашь "
        "ей пакет ос-канона.»); R45 Shadow-kin, BT-12/FAM-C pending veto; Two of "
        "Swords / SEAM / Libra (SHARED Lyn+Una, flagged) assistant-assigned; канон "
        "= PH-промпт автора VERBATIM (винил-просвет, дипломатия света, Dusk "
        "Binding); первая промоция из oc-candidates.json (пункт Д) — с первой "
        "боевой партии реестра."
    )
    canon["note_on_status"] = canon["note_on_status"].replace(
        "ACTIVE: 27", "ACTIVE: 28"
    ).replace(
        "Nier и Noir с промоции 2026-11-15;",
        "Nier и Noir с промоции 2026-11-15; Noxx с промоции 2026-11-22 (T5-29, из oc-candidates);",
    )
    canon_p.write_text(
        json.dumps(canon, ensure_ascii=False, indent=1) + "\n", encoding="utf-8"
    )
    print(f"oc-canon.json → 2.14.0: Noxx добавлена, ACTIVE 28, реестры обновлены")

    # ── 2. oc-candidates.json: P32 promoted, прочие — вердикт ───────────
    cand_p = SPEC / "oc-candidates.json"
    cand = json.loads(cand_p.read_text(encoding="utf-8"))
    promoted = 0
    passed = 0
    for c in cand["candidates"]:
        if c["slot"] == "P32":
            c["status"] = "promoted"
            c["promoted_to"] = "oc-canon.json → Noxx (canon 2.14.0, 2026-11-22)"
            c["note"] += " — ЗАБРАНА вердиктом T5-29"
            promoted += 1
        else:
            c["status"] = "passed"
            c["note"] += " — вердикт T5-29: EXP понравились почти все, не забрана"
            passed += 1
    cand["stats"] = {"promoted": promoted, "passed": passed, "pending": 0}
    cand["version"] = "1.2.0"
    cand["changelog"]["1.2.0"] = (
        "2026-11-22: вердикт T5-29 — ПЕРВАЯ ПРОМОЦИЯ: P32 (R45 Shadow-kin) → "
        "oc-canon 2.14.0, имя Noxx, пакет ОС-канона по прямому приказу («Выдашь "
        "ей пакет ос-канона»); остальные 8 — passed с пометкой «понравились, не "
        "забраны» (история вкуса: EXP-клетки зашли, мейн-тема — нет)"
    )
    cand_p.write_text(
        json.dumps(cand, ensure_ascii=False, indent=1) + "\n", encoding="utf-8"
    )
    print(f"oc-candidates.json → 1.2.0: P32 promoted (Noxx), {passed} passed")

    # ── 3. open-hypotheses.json: H-13 кандидат-клетки ────────────────────
    hyp_p = SPEC / "open-hypotheses.json"
    hyp = json.loads(hyp_p.read_text(encoding="utf-8"))
    ids = [h["id"] for h in hyp["hypotheses"]]
    if "H-13" not in ids:
        hyp["hypotheses"].append({
            "id": "H-13",
            "title": "Кандидат-клетки: бандл (раса-гиммик × типаж × палитра × комбо у потолка) находит забираемых персонажей",
            "born": "2026-11-22",
            "source": "Заказ автора (пункт Д, oc-candidates.json 1.1.0) + вердикт T5-29: EXP-клетки «понравились почти все», P32 забрана в ОС прямым приказом (Noxx, canon 2.14.0) — первое подтверждение с первой боевой партии",
            "status": "open",
            "note": "EXP-клетка-кандидат обязана нести ЭТУ гипотезу (id в строке ТЕСТ) — «полка отдыхает» незаконна с T5-30 (В42): мощность EXP идёт на проверку переменных, тема партии клетки не кастует",
        })
        hyp["version"] = "1.2.0"
        if isinstance(hyp.get("changelog"), dict):
            hyp["changelog"]["1.2.0"] = (
                "2026-11-22: H-13 — кандидат-клетки как проверяемая гипотеза "
                "(вердикт T5-29, урок В42: EXP проверяет штуки, не следует теме)"
            )
        hyp_p.write_text(
            json.dumps(hyp, ensure_ascii=False, indent=1) + "\n", encoding="utf-8"
        )
        print("open-hypotheses.json → 1.2.0: H-13 зарегистрирована")
    else:
        print("open-hypotheses.json: H-13 уже есть")

    print("OK: Noxx в каноне, кандидаты сведены, полка пополнена")


if __name__ == "__main__":
    main()
