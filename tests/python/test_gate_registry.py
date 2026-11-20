#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Юнит-тесты РЕЕСТРА ГЕЙТОВ (unittest, stdlib-only) — двойной аудит 2026-11-20,
P0-05 «объявленный гейт ≠ работающий» (живой прецедент: paletteSkin был
объявлен в gates.json v1.16.0, но отсутствовал в REQUIRED-списке валидатора).

Три страховки:

1. ИНВАРИАНТЫ РЕЕСТРА (быстрая, без subprocess): specs/gate-registry.json
   согласован с gates.json и tools/gates.py — каждая секция имеет живую
   impl-функцию, каждое поле квитанции собирается, множества секций
   совпадают с REQUIRED_GATES_KEYS валидатора.

2. ЗОЛОТОЙ ПРОГОН: gates.py на живом T5-27 → PASS 0F/2W, sha совпадает
   с квитанцией 2026-11-20-T5-27-v1.json. Если любой гейт молча
   отвалится или начнёт перекрывать норму — вердикт дрейфнет, тест упадёт.

3. ТАМПЕРЫ (гейты РЕАЛЬНО стреляют, а не декорированы):
   - изъятая hard-флора из NEG первого слота → FAIL с gate=floor;
   - изъятое вплетение Y-карты (пересказ вместо копипаст-юнита 1:1) →
     FAIL по yStamp (не вплетено / пересказ).

Прогон: python3 -m unittest discover -s tests/python -v
"""

import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO / "tools"))

import gates  # noqa: E402

GATES_PY = REPO / "tools" / "gates.py"
REGISTRY = REPO / "specs" / "gate-registry.json"
T5_27 = REPO / "batches" / "T5-27.md"
T5_27_RECEIPT = REPO / "specs" / "gate-receipts" / "2026-11-20-T5-27-v1.json"


def run_gates(path: Path) -> dict:
    """Живой прогон gates.py на копии батча; квитанция --json пишется в
    TEMP-каталог (не в batches/ — тест не мусорит в репо)."""
    out_json = Path(tempfile.mkdtemp(prefix="t5-gatereg-receipt-")) / "receipt.json"
    proc = subprocess.run(
        [sys.executable, str(GATES_PY), str(path), "--json", str(out_json)],
        capture_output=True, text=True, cwd=REPO, timeout=180,
    )
    receipt = json.loads(out_json.read_text(encoding="utf-8")) if out_json.exists() else {}
    receipt["_exit"] = proc.returncode
    return receipt


class TestRegistryInvariants(unittest.TestCase):
    """Реестр ↔ gates.json ↔ gates.py: цепочка «объявлено → исполнено →
    доказано» не может разорваться молча."""

    def test_registry_loads_and_sections_match_required(self):
        reg = json.loads(REGISTRY.read_text(encoding="utf-8"))
        sections = [g["section"] for g in reg["gates"]]
        self.assertEqual(
            sorted(sections), sorted(gates.REQUIRED_BRIDGE) if hasattr(gates, "REQUIRED_BRIDGE") else sorted(sections)
        )
        # REQUIRED-список валидатора — единственный эталон (не дублируем:
        # читаем прямо из валидатора)
        vsrc = (REPO / "tools" / "validate.py").read_text(encoding="utf-8")
        m = re.search(r"REQUIRED_GATES_KEYS = \[(.*?)\]", vsrc, re.S)
        self.assertIsNotNone(m, "REQUIRED_GATES_KEYS не найден в validate.py")
        required = re.findall(r'"(\w+)"', m.group(1))
        self.assertEqual(
            sorted(sections), sorted(required),
            "секции реестра ≠ REQUIRED_GATES_KEYS валидатора — разрыв цепочки",
        )
        self.assertEqual(len(sections), len(set(sections)), "дубли секций в реестре")

    def test_every_impl_exists_in_gates_py(self):
        reg = json.loads(REGISTRY.read_text(encoding="utf-8"))
        src = GATES_PY.read_text(encoding="utf-8")
        for row in reg["gates"]:
            for fn in row.get("impl") or []:
                self.assertTrue(
                    re.search(rf"^def {re.escape(fn)}\(", src, re.M),
                    f"impl «{fn}» (секция {row['section']}) не существует в gates.py",
                )

    def test_every_receipt_field_is_built(self):
        reg = json.loads(REGISTRY.read_text(encoding="utf-8"))
        src = GATES_PY.read_text(encoding="utf-8")
        for row in reg["gates"]:
            rf = row.get("receiptField")
            if not rf:
                continue
            leaf = str(rf).split(".")[-1]
            self.assertIn(
                f'"{leaf}"', src,
                f"receiptField «{rf}» ({row['section']}) не собирается в квитанции",
            )

    def test_every_declared_section_exists_in_gates_json(self):
        reg = json.loads(REGISTRY.read_text(encoding="utf-8"))
        for row in reg["gates"]:
            self.assertIn(
                row["section"], gates.GATES,
                f"секция «{row['section']}» объявлена в реестре, но отсутствует в gates.json",
            )


class TestGoldenRun(unittest.TestCase):
    """Живой T5-27 под гейтами — вердикт и sha заперты: дрейф любого гейта
    (отвал или перекрытие нормы) меняет вердикт и роняет тест."""

    def test_t5_27_passes_with_locked_verdict(self):
        receipt = run_gates(T5_27)
        self.assertEqual(receipt.get("verdict"), "PASS", f"живой прогон T5-27: {receipt.get('_exit')}")
        self.assertEqual(len(receipt.get("fails", [])), 0)
        self.assertEqual(len(receipt.get("warns", [])), 2, "WARN-счёт T5-27 дрейфнул — норма изменилась")
        # sha живого батча == эталонной квитанции
        ref = json.loads(T5_27_RECEIPT.read_text(encoding="utf-8"))
        self.assertEqual(receipt.get("sha256"), ref["sha256"], "sha батча T5-27 изменился без новой квитанции")


class TestTamperDetection(unittest.TestCase):
    """Гейты стреляют: порча батча обязана заканчиваться FAIL, а не PASS."""

    def _tampered_copy(self, mutate) -> Path:
        text = T5_27.read_text(encoding="utf-8")
        new_text = mutate(text)
        self.assertNotEqual(text, new_text, "тампер не применился")
        tmp = tempfile.mkdtemp(prefix="t5-gatereg-")
        p = Path(tmp) / "T5-27.md"
        p.write_text(new_text, encoding="utf-8")
        return p

    def test_removed_hard_floor_fails(self):
        """Изъятие hard-флоры («loli») из NEG первого слота → FAIL gate=floor."""
        def drop_loli(text: str) -> str:
            return text.replace(", loli,", ",", 1)  # первый NEG (P01)

        receipt = run_gates(self._tampered_copy(drop_loli))
        self.assertEqual(receipt.get("verdict"), "FAIL", "изъятая hard-флора прошла гейты — floors молчат")
        floor_fails = [f for f in receipt.get("fails", []) if f.get("gate") == "floor"]
        self.assertTrue(floor_fails, f"FAIL есть, но не по gate=floor: {receipt.get('fails', [])[:3]}")

    def test_paraphrased_weave_fails(self):
        """Вплетение Y-карты заменено пересказом (не копипаст 1:1) → FAIL yStamp
        (В34/В35: «промпт не оставляется на произвол судьбы»)."""
        WEAVE = (
            "braced into the bookcase behind the viewer, both palms flat on the shelf-boards "
            "either side of the frame, the spine's weight leaning into the shelf's edge, "
            "one knee notched on the lower rail"
        )
        PARAPHRASE = (
            "leaning hard into the bookcase from behind the camera, both hands pressed flat "
            "on the shelves around the frame, her weight settling onto the shelf edge, "
            "one knee hooked on the lower rail"
        )

        def swap(text: str) -> str:
            self.assertIn(WEAVE, text, "вплетение Y443 не найдено в T5-27 — формат дрейфнул")
            return text.replace(WEAVE, PARAPHRASE)

        receipt = run_gates(self._tampered_copy(swap))
        self.assertEqual(receipt.get("verdict"), "FAIL", "пересказ вплетения прошёл гейты — yStamp молчит")
        ys = receipt.get("y_stamp") or {}
        self.assertTrue(
            ys.get("no_weave", 0) + ys.get("mismatch", 0) > 0,
            f"FAIL есть, но y_stamp не заметил подмены: {ys}",
        )


if __name__ == "__main__":
    unittest.main()
