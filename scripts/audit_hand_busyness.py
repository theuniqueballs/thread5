#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Аудит занятости рук в Y-картах (пересмотр по вердикту T5-28, P04:
«лицом к зрителю + руки прижаты к стене за ней» — пересмотреть хуйню с
занятостью рук).

Ищем карты с ПОВЕРХНОСТНЫМ КОНТАКТОМ рук (palms flat on / leaning on /
braced / pressed against / on the ground…) и проверяем, несут ли они
ОРИЕНТАЦИОННЫЙ ЯКОРЬ: куда повёрнуто тело относительно камеры и поверхности
(facing away / profile / cheek to / shoulder toward the lens / back to
camera / toward the lens). Контакт без якоря = риск «фокус-разворота»:
рендерер разворачивает лицо к камере, руки остаются на поверхности — за
спиной. Это и есть бессмылица P04 (Y237)."""
import json
import re
from pathlib import Path

SPECS = Path(__file__).resolve().parent.parent / "specs" / "camera.json"

CONTACT_RE = re.compile(
    r"palms? (?:flat|pressed|planted)[^,;.]*?(?:on|against|to)\b"
    r"|lean(?:ing|ed)? back on\b"
    r"|braced (?:over|against|on)\b"
    r"|palms? (?:on|against)\b"
    r"|hands? (?:flat|pressed|planted)\b"
    r"|forehead to\b"
    r"|weight (?:on|given to|forward on)\b"
    r"|leaning (?:on|into|against)\b",
    re.IGNORECASE,
)

# позитивные ориентационные якоря (рисуют ГЕОМЕТРИЮ, а не NEG-запрет)
ANCHOR_RE = re.compile(
    r"facing away|faced? (?:away|to the wall)|profile\b|in profile"
    r"|cheek to\b|forehead to\b|shoulder (?:toward|to) the (?:lens|camera)"
    r"|back to the (?:lens|camera|viewer)|away from the (?:lens|camera)"
    r"|toward the wall|against the (?:wall|surface|window)"
    r"|over the viewer|toward the lens|into the (?:wall|lens|surface)"
    r"|to the plaster|leaning (?:in|into)\b|toward the camera",
    re.IGNORECASE,
)


def main() -> None:
    d = json.loads(SPECS.read_text(encoding="utf-8"))
    cards = d["y_cards"]["cards"]
    risky, anchored, no_contact = [], 0, 0
    for c in cards:
        comp = c.get("components") or {}
        text = " ".join(
            str(comp.get(k, "")) for k in ("pose", "pov", "camera", "exposure")
        )
        if not CONTACT_RE.search(text):
            no_contact += 1
            continue
        if ANCHOR_RE.search(text):
            anchored += 1
        else:
            risky.append(c)

    print(f"всего карт: {len(cards)}")
    print(f"  поверхностный контакт: {anchored + len(risky)}")
    print(f"    с ориентационным якорём: {anchored}")
    print(f"    БЕЗ якоря (риск фокус-разворота): {len(risky)}")
    print(f"  без контакта: {no_contact}")
    print()
    for c in risky:
        comp = c["components"]
        print(f"{c['id']}: {comp.get('pose', '')[:130]}")
        print(f"      cam: {comp.get('camera', '')[:60]} | pov: {comp.get('pov', '')[:60]}")


if __name__ == "__main__":
    main()
