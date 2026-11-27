#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Юнит-тесты ГИГИЕНЫ КОММИТОВ СПЕК (тикет #4) — tools/commit_hygiene.py.

Инструментальная ловушка класса «full-file реформат в фичевом коммите»
(волна 1в: 7162 строки диффа на 67 контента). Метод: полный numstat по
specs/*.json против numstat -w; расхождение >5× — WARN. Тесты поднимают
временное git-репо и гоняют оба класса коммитов.

Прогон: python3 -m unittest discover -s tests/python -v
"""

import subprocess
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO / "tools"))

import commit_hygiene  # noqa: E402


def _git(cwd, *args):
    return subprocess.run(["git", "-C", str(cwd), *args],
                          capture_output=True, text=True, timeout=60)


class TmpRepo:
    """Мини-репо с specs/ для проверки audit() на живых числах numstat."""

    def __init__(self):
        import tempfile
        self.dir = Path(tempfile.mkdtemp(prefix="t5-hygiene-"))
        (self.dir / "specs").mkdir()
        _git(self.dir, "init", "-q")
        _git(self.dir, "config", "user.email", "t@t")
        _git(self.dir, "config", "user.name", "t")
        self._commit_base()

    def _commit_base(self):
        spec = {"version": "1.0.0", "palettes": [
            {"id": f"P{i}", "forbidden": ["muddy colors"]} for i in range(30)
        ]}
        (self.dir / "specs" / "palettes.json").write_text(
            json_dumps_ind2(spec), encoding="utf-8")
        _git(self.dir, "add", "-A")
        _git(self.dir, "commit", "-qm", "base")

    def commit_content_only(self):
        p = self.dir / "specs" / "palettes.json"
        text = p.read_text(encoding="utf-8")
        text = text.replace('"version": "1.0.0"', '"version": "1.0.1"')
        p.write_text(text, encoding="utf-8")
        _git(self.dir, "add", "-A")
        _git(self.dir, "commit", "-qm", "feat: content only")

    def commit_reformat_mix(self):
        """Класс волны 1в: 67 строк контента + full-file реформат отступов."""
        import json
        p = self.dir / "specs" / "palettes.json"
        data = json.loads(p.read_text(encoding="utf-8"))
        data["version"] = "1.1.0"          # немного контента
        data["palettes"][0]["forbidden"].append("neon")
        # реформат: весь файл пере-сериализуется другим indent
        p.write_text(json.dumps(data, ensure_ascii=False, indent=4) + "\n",
                     encoding="utf-8")
        _git(self.dir, "add", "-A")
        _git(self.dir, "commit", "-qm", "feat: mixed reformat")

    def numstats(self):
        sha = _git(self.dir, "log", "-1", "--format=%H").stdout.strip()
        full = commit_hygiene._numstat([f"{sha}^", sha], repo=self.dir)
        w = commit_hygiene._numstat(["-w", f"{sha}^", sha], repo=self.dir)
        return full, w


def json_dumps_ind2(data):
    import json
    return json.dumps(data, ensure_ascii=False, indent=2) + "\n"


class TestChurnAudit(unittest.TestCase):
    """audit(): числа решают, не ручная честность."""

    def test_content_only_clean(self):
        repo = TmpRepo()
        repo.commit_content_only()
        full, w = repo.numstats()
        warns = commit_hygiene.audit(full, w)
        self.assertEqual(warns, [], "контент-only коммит не штрафуется")

    def test_reformat_mix_caught(self):
        repo = TmpRepo()
        repo.commit_reformat_mix()
        full, w = repo.numstats()
        self.assertTrue(full, "дифф обязан быть непустым")
        warns = commit_hygiene.audit(full, w)
        self.assertEqual(len(warns), 1)
        self.assertIn("specs/palettes.json", warns[0])
        self.assertIn("format:", warns[0], "WARN обязан указать лечение")

    def test_pure_format_commit_not_fined(self):
        """Чистый format:-коммит (git -w пуст) легален — не штрафуется."""
        repo = TmpRepo()
        import json
        p = repo.dir / "specs" / "palettes.json"
        data = json.loads(p.read_text(encoding="utf-8"))
        p.write_text(json.dumps(data, ensure_ascii=False, indent=4) + "\n",
                     encoding="utf-8")
        _git(repo.dir, "add", "-A")
        _git(repo.dir, "commit", "-qm", "format: indent 2 → 4")
        full, w = repo.numstats()
        warns = commit_hygiene.audit(full, w)
        self.assertEqual(warns, [], "format:-коммит законен (закон №9)")


class TestLiveHistory(unittest.TestCase):
    """Живая история: последний specs-коммит репо чист по ловушке
    (волна 1е — 805 вставок без чурна; волне 1в лавочка закрыта)."""

    def test_last_specs_commit_clean(self):
        sha = commit_hygiene._git("log", "-1", "--format=%H", "--", "specs/").strip()
        if not sha:
            self.skipTest("нет specs-коммитов")
        full = commit_hygiene._numstat([f"{sha}^", sha])
        w = commit_hygiene._numstat(["-w", f"{sha}^", sha])
        warns = commit_hygiene.audit(full, w)
        self.assertEqual(warns, [], f"последний specs-коммит несёт чурн: {warns}")


if __name__ == "__main__":
    unittest.main()
