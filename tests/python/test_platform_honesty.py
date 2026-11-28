#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Юнит-тесты ПЛАТФОРМЕННОЙ ЧЕСТНОСТИ БАТАРЕИ (тикет #1, внешний аудит
2026-11-27): на Windows-чекеуте (core.autocrlf=true) батарея была красной
сразу после чекаута — золотой T5-27 падал по sha (квитанция считала LF,
рабочий файл — CRLF), bun-тест ждал POSIX-литерал, тулзы крашились на
cp1251. Класс «объявлено ≠ исполнено», только по платформам: Linux-CI зелёный.

Страховки (соответствуют приёмке тикета):
  1. CRLF-чекаут золотого T5-27 → PASS 0F/2W, sha == запертой квитанции
     (sha-замок считает по LF-канону — gates.py нормализует \\r\\n → \\n;
     запертые квитанции НЕ пересчитываются, сравнение в одном каноне);
  2. .gitattributes жив и держит LF-канон текстовых семейств цеха
     (md/спеки/код), референсы автора (upload/) — без конвертации;
  3. tools-точки входа несут utf-8-reconfigure (cp1251-консоль не роняет
     печать ×/§/→ — ритуал «status в начало сеанса» жив на машине автора).

Прогон: python3 -m unittest discover -s tests/python -v
"""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO / "tools"))

GATES_PY = REPO / "tools" / "gates.py"
T5_27 = REPO / "batches" / "T5-27.md"
T5_27_RECEIPT = REPO / "specs" / "gate-receipts" / "2026-11-20-T5-27-v1.json"
GITATTR = REPO / ".gitattributes"


def _run_gates(path: Path) -> dict:
    out_json = Path(tempfile.mkdtemp(prefix="t5-platf-")) / "receipt.json"
    proc = subprocess.run(
        [sys.executable, str(GATES_PY), str(path), "--json", str(out_json)],
        capture_output=True, text=True, cwd=REPO, timeout=180,
    )
    receipt = json.loads(out_json.read_text(encoding="utf-8")) if out_json.exists() else {}
    receipt["_exit"] = proc.returncode
    return receipt


class TestCrlfGoldenRun(unittest.TestCase):
    """Воспроизведение Windows-чекаута: тот же T5-27, концы строк CRLF.

    Обе копии (CRLF и LF) — СИНТЕТИЧЕСКИЕ, из контента в памяти (аудит
    тикета #7, третье напоминание): чтение рабочего файла ассертило LF —
    на любом чекауте, материализованном до .gitattributes (у автора
    такой), тест падал без единого реального дрейфа. Теперь рабочий файл
    только читается и нормализуется в памяти (\\r\\n → \\n = LF-канон),
    варианты строк генерируются из него: тест платформо-независим.
    """

    def _canonical_bytes(self) -> bytes:
        """Контент эталона в LF-каноне — из рабочего файла, любой EOL."""
        data = T5_27.read_bytes()
        return data.replace(b"\r\n", b"\n")

    def _crlf_copy(self) -> Path:
        data = self._canonical_bytes()
        tmp = Path(tempfile.mkdtemp(prefix="t5-crlf-"))
        # полный CRLF-чекаут: батч и его папка (stories.md) — концы строк CRLF
        (tmp / "T5-27.md").write_bytes(data.replace(b"\n", b"\r\n"))
        cards_dir = tmp / "T5-27"
        cards_dir.mkdir()
        (cards_dir / "stories.md").write_bytes(
            (REPO / "batches" / "T5-27" / "stories.md").read_bytes().replace(b"\n", b"\r\n")
        )
        return tmp / "T5-27.md"

    def _lf_copy(self) -> Path:
        """Синтетическая LF-копия — двойной канон без ставки на рабочий файл."""
        data = self._canonical_bytes()
        tmp = Path(tempfile.mkdtemp(prefix="t5-lf-"))
        (tmp / "T5-27.md").write_bytes(data)
        cards_dir = tmp / "T5-27"
        cards_dir.mkdir()
        (cards_dir / "stories.md").write_bytes(
            (REPO / "batches" / "T5-27" / "stories.md").read_bytes()
        )
        return tmp / "T5-27.md"

    def test_crlf_checkout_passes_with_locked_sha(self):
        """CRLF-копия золотого T5-27: PASS · 0F/2W · sha == запертой квитанции.

        До фикса (тикет #1): sha сырых CRLF-байтов ≠ LF-канону квитанции —
        тест падал на чистом Windows-чекеуте без единого изменения контента.
        """
        receipt = _run_gates(self._crlf_copy())
        self.assertEqual(receipt.get("verdict"), "PASS",
                         f"CRLF-чекаут роняет золотой прогон: {receipt.get('_exit')}")
        self.assertEqual(len(receipt.get("fails", [])), 0)
        self.assertEqual(len(receipt.get("warns", [])), 2,
                         "WARN-счёт CRLF-копии дрейфнул — норма изменилась")
        ref = json.loads(T5_27_RECEIPT.read_text(encoding="utf-8"))
        self.assertEqual(receipt.get("sha256"), ref["sha256"],
                         "sha CRLF-копии ≠ запертой квитанции — sha-замок "
                         "считает не по LF-канону (тикет #1, регресс)")

    def test_lf_original_still_locked(self):
        """Регресс-страховка: LF-канон не сдвинулся (двойной канон).

        Гоняет СИНТЕТИЧЕСКУЮ LF-копию: на старом CRLF-чекеуте автора
        живой файл читался бы CRLF — gates.py нормализует sha, но тест
        не обязан зависеть от состояния рабочего дерева (тикет #7,
        п.5 остатка)."""
        receipt = _run_gates(self._lf_copy())
        ref = json.loads(T5_27_RECEIPT.read_text(encoding="utf-8"))
        self.assertEqual(receipt.get("sha256"), ref["sha256"])
        self.assertEqual(receipt.get("verdict"), "PASS")


class TestGitattributesLfCanon(unittest.TestCase):
    """.gitattributes: LF-канон текстовых семейств + замороженные референсы."""

    def test_gitattributes_exists(self):
        self.assertTrue(GITATTR.is_file(),
                        ".gitattributes отсутствует — Windows-чекеут получает "
                        "CRLF и роняет батарею (тикет #1, приёмка п.1)")

    def test_text_families_pinned_to_lf(self):
        text = GITATTR.read_text(encoding="utf-8")
        lines = text.splitlines()
        for pat in ("*.md", "*.json", "*.py"):
            hit = any(
                ln.startswith(pat) and "text" in ln and "eol=lf" in ln.replace(" ", "")
                for ln in lines
            )
            self.assertTrue(hit, f"«{pat} … text eol=lf» нет в .gitattributes")
        self.assertIn("* text=auto", text,
                      "«* text=auto» нет — нормализация на чекине не объявлена")

    def test_upload_references_frozen(self):
        text = GITATTR.read_text(encoding="utf-8")
        self.assertIn("upload/** -text", text,
                      "референсы автора (upload/) без «-text» — конвертация "
                      "концов строк тронет замороженные артефакты")


class TestUtf8Console(unittest.TestCase):
    """Тулзы несут utf-8-reconfigure: cp1251-консоль не роняет ритуал."""

    TOOLS = ("tools/gates.py", "tools/t5delivery.py", "tools/validate.py")

    def test_reconfigure_utf8_in_tool_entrypoints(self):
        for rel in self.TOOLS:
            src = (REPO / rel).read_text(encoding="utf-8")
            self.assertIn('reconfigure(encoding="utf-8"', src,
                          f"{rel}: нет sys.stdout.reconfigure(encoding='utf-8') — "
                          "печать ×/§/→ падает на cp1251 (тикет #1, приёмка п.4)")

    def test_delivery_status_runs_clean(self):
        """Ритуал «status в начало сеанса» жив и завершается нулём."""
        proc = subprocess.run(
            [sys.executable, str(REPO / "tools" / "t5delivery.py"), "status"],
            capture_output=True, text=True, cwd=REPO, timeout=60,
        )
        self.assertEqual(proc.returncode, 0,
                         f"t5delivery status падает: {proc.stderr[-300:]}")


if __name__ == "__main__":
    unittest.main()
