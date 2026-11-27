#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Юнит-тесты ЕДИНОГО КАНОНА СЕРИАЛИЗАЦИИ СПЕК (тикет #4) — tools/spec_io.py.

Прецедент: волна 1в — дифф спеки 7162 строки при 67 строках контента.
Канон закрывает вторую половину класса: следующий дифф скриптной правки
спеки содержит только содержимое (round-trip живых машинных файлов
идемпотентен), а формат-паспорт не молчит о рассинхроне.

Прогон: python3 -m unittest discover -s tests/python -v
"""

import json
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO / "tools"))

import spec_io  # noqa: E402


class TestCanonConstants(unittest.TestCase):
    """Один канон для всех писателей (приёмка тикета п.2)."""

    def test_canon_is_single_source(self):
        self.assertIs(spec_io.ENSURE_ASCII, False, "ensure_ascii=False — канон")
        self.assertIs(spec_io.TRAILING_NEWLINE, True, "trailing newline — канон")
        self.assertEqual(spec_io.INDENT_DEFAULT, 1)

    def test_writers_use_spec_io(self):
        """Все скрипты, пишущие specs/*.json, идут через dump_spec — прямых
        json.dumps(...).write_text в писателях больше нет (класс закрыт
        инструментально, не обещанием)."""
        for tool, marker in (
            ("tools/oracle.py", "spec_io.dump_spec(TRUST_PATH"),
            ("tools/stamp_era.py", "spec_io.dump_spec(CAM"),
            ("tools/pregarment.py", "spec_io.dump_spec(LEDGER"),
            ("tools/gates.py", "spec_io.dump_spec(out_json"),
        ):
            src = (REPO / tool).read_text(encoding="utf-8")
            self.assertIn(marker, src, f"{tool} не пишет через spec_io.dump_spec")


class TestLiveRoundtrip(unittest.TestCase):
    """Живые машинные спеки уже лежат в каноне: повторная запись не меняет
    ни байта — следующий дифф содержит только содержимое."""

    MACHINE_SPECS = (
        "specs/camera.json",
        "specs/gate-registry.json",
        "specs/palettes.json",
        "specs/y-trust.json",
        "specs/delivery-index.json",
        "specs/dresser.json",
        "specs/oc-candidates.json",
        "specs/races.json",
    )

    def test_machine_specs_in_canon(self):
        bad = []
        for rel in self.MACHINE_SPECS:
            p = REPO / rel
            if not p.exists():
                continue
            if not spec_io.spec_roundtrip_ok(p):
                bad.append(rel)
        self.assertEqual(
            bad, [],
            f"спеки вне канона — следующий скриптный дифф потащит реформат: {bad}",
        )

    def test_dump_spec_idempotent_on_camera(self):
        p = REPO / "specs" / "camera.json"
        data = json.loads(p.read_text(encoding="utf-8"))
        import tempfile
        with tempfile.TemporaryDirectory(prefix="t5-specio-") as tmp:
            out = Path(tmp) / "camera.json"
            # запись во временную копию не строит rel-путь паспорта —
            # передаём indent явно, как паспорт живого файла
            spec_io.dump_spec(out, data, indent=1)
            self.assertEqual(
                out.read_text(encoding="utf-8"), p.read_text(encoding="utf-8"),
                "повторная сериализация camera.json изменила байты — канон дрейфует",
            )


if __name__ == "__main__":
    unittest.main()
