"""Страж CI-воркфлоу (SURGERY 2026-11-24: shell-smoke красная с рождения CI).

Прецеденты класса:
- 2026-11-20…23: «: » в имени шага ломало YAML всего ci.yml — Invalid
  workflow file на любом триггере (починено хирургией тройного вердикта;
  синтаксис после правки проверяется pyyaml вручную — AGENTS.md
  «Правки CI/workflows»);
- 2026-11-24: shell-smoke падала на всех прогонах CI — python-runtime-
  build.sh требует uv, которого в ubuntu-latest нет (web и pipeline
  при этом зелёные). Починено шагом astral-sh/setup-uv в ci.yml.

«YAML валиден» ≠ «джоба живая»: синтаксис проверяет pyyaml, а семантику
(триггер на main, имена шагов без «: », три джобы на месте) проверяет
этот тест — stdlib-only, CI ставит чистый python без зависимостей.
"""

import re
import unittest
from pathlib import Path

CI_YML = Path(__file__).resolve().parents[2] / ".github" / "workflows" / "ci.yml"
JOBS_REQUIRED = {"web", "pipeline", "shell-smoke"}


def push_branches(lines):
    """Ветки фильтра on.push.branches.

    None — фильтра нет (матчится любая ветка, включая main).
    list — перечисленные ветки.
    ValueError — on:/push: нет вообще (CI не триггерится ни на что).
    """
    in_on = False
    in_push = False
    for ln in lines:
        if re.match(r"^on:\s*$", ln):
            in_on = True
            continue
        if in_on and ln and not ln[0].isspace():
            break  # конец блока on: (следующий ключ верхнего уровня)
        if in_on and re.match(r"^  push:\s*$", ln):
            in_push = True
            continue
        if in_on and re.match(r"^  \S", ln):
            in_push = False  # соседний триггер (pull_request:)
        if in_push:
            m = re.match(r"^    branches:\s*(.*?)\s*$", ln)
            if m:
                raw = m.group(1)
                if raw.startswith("[") and raw.endswith("]"):
                    raw = raw[1:-1]
                if not raw:
                    return []
                return [b.strip().strip("'\"") for b in raw.split(",") if b.strip()]
    if not in_on:
        raise ValueError("ci.yml: блока on: нет — воркфлоу не триггерится")
    if not in_push:
        raise ValueError("ci.yml: триггера push: нет — прямые пуши не видят CI")
    return None


def step_name_violations(lines):
    """Имена шагов с «: » или хвостовым «:» — класс, ломавший YAML 2026-11-20.

    Кавычные имена пропускаются: name: "A: B" — валидный скаляр.
    """
    bad = []
    for n, ln in enumerate(lines, 1):
        m = re.match(r"^\s*-\s+name:\s*(.+?)\s*$", ln)
        if not m:
            continue
        val = m.group(1)
        if len(val) >= 2 and val[0] in "\"'" and val[-1] == val[0]:
            continue  # кавычный скаляр — двоеточия легальны
        if ": " in val or val.endswith(":"):
            bad.append((n, val))
    return bad


def job_ids(lines):
    """Джобы верхнего уровня в блоке jobs:."""
    in_jobs = False
    ids = []
    for ln in lines:
        if re.match(r"^jobs:\s*$", ln):
            in_jobs = True
            continue
        if in_jobs:
            m = re.match(r"^  ([A-Za-z0-9_-]+):\s*$", ln)
            if m:
                ids.append(m.group(1))
            elif ln and not ln[0].isspace():
                break
    return ids


class TestCIWorkflowLive(unittest.TestCase):
    """Инварианты живого .github/workflows/ci.yml."""

    def setUp(self):
        self.text = CI_YML.read_text(encoding="utf-8")
        self.lines = self.text.splitlines()

    def test_push_trigger_matches_main(self):
        branches = push_branches(self.lines)
        self.assertTrue(
            branches is None or "main" in branches,
            "push-триггер не матчит main: branches=%r — прямые пуши "
            "останутся без CI" % (branches,),
        )

    def test_step_names_no_stray_colon(self):
        violations = step_name_violations(self.lines)
        self.assertEqual(
            violations, [],
            "«: » в имени шага ломает YAML воркфлоу (Invalid workflow file, "
            "прецедент 2026-11-20): %r" % (violations,),
        )

    def test_jobs_present(self):
        missing = JOBS_REQUIRED - set(job_ids(self.lines))
        self.assertEqual(missing, set(), "потеряны джобы: %r" % (sorted(missing),))

    def test_no_tabs(self):
        self.assertNotIn(
            "\t", self.text, "таб в YAML запрещён (отступы — только пробелы)")


class TestCIWorkflowTamper(unittest.TestCase):
    """Тамперы: страж обязан ловить классы убийства CI."""

    def _branches_of(self, content):
        return push_branches(content.splitlines())

    def test_tamper_garbage_branch_filter(self):
        # мусор в фильтре веток: валидный YAML, но main не матчится
        content = "on:\n  push:\n    branches: ain]\n  pull_request:\n"
        self.assertNotIn("main", self._branches_of(content))

    def test_tamper_empty_branch_filter(self):
        content = "on:\n  push:\n    branches: []\n  pull_request:\n"
        self.assertEqual(self._branches_of(content), [])

    def test_tamper_colon_in_step_name(self):
        # прецедент 2026-11-20…23: двоеточие в имени шага
        content = "      - name: Гейты (P0-06: статус из индекса)\n"
        self.assertTrue(step_name_violations(content.splitlines()))

    def test_tamper_quoted_name_allowed(self):
        content = '      - name: "P0-06: статус из индекса"\n'
        self.assertEqual(step_name_violations(content.splitlines()), [])

    def test_tamper_missing_job(self):
        content = ("jobs:\n  web:\n    runs-on: ubuntu-latest\n"
                   "  pipeline:\n    runs-on: ubuntu-latest\n")
        self.assertTrue(JOBS_REQUIRED - set(job_ids(content.splitlines())))

    def test_missing_push_trigger_raises(self):
        content = "on:\n  pull_request:\n"
        with self.assertRaises(ValueError):
            push_branches(content.splitlines())


if __name__ == "__main__":
    unittest.main()
