"""Страж инбокса: SDK-конфиг без token + СТОП автотриажа (заказ 2026-11-24).

Прецеденты класса:
- T5-19: 401 «missing X-Token header» карантинил пачку, пока конфиг SDK
  чинился на уровне окружения;
- 2026-11-24: то же самое повторилось — SDK берёт ПЕРВЫЙ конфиг с
  baseUrl && apiKey (cwd → home → /etc), даже если token в нём пуст;
  запрос уходит без заголовка X-Token → 401 → fail-closed карантин всего
  инбокса. Лечится в корне: self-check конфига ДО vision-звонка
  (sdk-config.ts) + красный баннер + блок автотриажа на клиенте;
- 2026-11-24: заказ автора — СТОП автотриажа в любой момент, чтобы снести
  инбокс и залить пачку по новой: СТОП-кнопка обрывает циклы, после
  ручного стопа автотриаж сам не перезапускается.

stdlib-only: тесты сверяют ЖИВЫЕ файлы (regex/позиции), а не копии логики.
"""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SDK_CONFIG = ROOT / "src" / "lib" / "t5" / "sdk-config.ts"
INBOX = ROOT / "src" / "lib" / "t5" / "inbox.ts"
INBOX_ROUTE = ROOT / "src" / "app" / "api" / "t5" / "inbox" / "route.ts"
INBOX_VIEW = ROOT / "src" / "components" / "t5" / "inbox-view.tsx"

RETRIAGE_RE = re.compile(r"fail-closed|429|too many|карантин", re.IGNORECASE)


def read(path: Path) -> str:
    if not path.exists():
        raise AssertionError(f"файл пропал: {path}")
    return path.read_text(encoding="utf-8")


class TestSdkConfigModule(unittest.TestCase):
    """sdk-config.ts: порядок поиска как у SDK, диагноз, секреты не текут."""

    def setUp(self):
        self.src = read(SDK_CONFIG)

    def test_экспортирует_контракт(self):
        for sym in (
            "export async function readSdkConfigState",
            "export class SdkConfigError",
            "export async function assertSdkVisionReady",
            "export interface SdkConfigState",
        ):
            self.assertIn(sym, self.src, f"нет {sym!r} в sdk-config.ts")

    def test_порядок_поиска_как_у_sdk(self):
        self.assertIn("path.join(process.cwd(), '.z-ai-config')", self.src)
        self.assertIn("os.homedir()", self.src)
        self.assertIn("'/etc/.z-ai-config'", self.src)
        # правило SDK: файл без baseUrl/apiKey конфигом не считается
        self.assertIn("nonEmptyString(cfg.baseUrl)", self.src)
        self.assertIn("nonEmptyString(cfg.apiKey)", self.src)

    def test_ok_равен_hasToken_а_не_наличию_файла(self):
        self.assertRegex(self.src, r"ok:\s*hasToken")
        self.assertRegex(self.src, r"found:\s*true")
        # ok считается от token, иначе диагноз врёт
        self.assertNotRegex(self.src, r"ok:\s*true")

    def test_секреты_не_текут_наружу(self):
        # значение token/apiKey не возвращается: нет ретёрна конфига целиком
        for forbidden in ("return cfg", "JSON.stringify(cfg)", "token: cfg", "apiKey: cfg", "...cfg"):
            self.assertNotIn(forbidden, self.src, f"риск утечки секрета: {forbidden!r} в sdk-config.ts")


class TestInboxGuard(unittest.TestCase):
    """inbox.ts: гвард ДО звонка, карантин-причина лечится RETRIAGE_RE."""

    def setUp(self):
        self.src = read(INBOX)

    def test_импорт_гварда(self):
        self.assertIn("import { SdkConfigError, assertSdkVisionReady } from './sdk-config';", self.src)

    def test_гвард_до_vision_звонка_в_триаже_и_разборе(self):
        self.assertEqual(self.src.count("await assertSdkVisionReady();"), 2, "гвард ровно в triageImage и analyzeItem")
        guard = self.src.index("await assertSdkVisionReady();")
        first_call = self.src.index("visionJsonRetry({")
        self.assertLess(guard, first_call, "гвард должен стоять ДО первого vision-звонка")

    def test_SdkConfigError_не_ретраится(self):
        passthrough = self.src.index("if (err instanceof SdkConfigError) throw err;")
        ladder = self.src.index("429|401|403|too many|token|unauthorized")
        self.assertLess(passthrough, ladder, "SdkConfigError должен выходить из лестницы до ретра-правил")

    def test_карантин_от_конфига_лечится_перетриажем(self):
        m = re.search(r"SDK-конфиг не готов \(.*\) — карантин \(fail-closed\)", self.src)
        self.assertIsNotNone(m, "нет карантин-причины для SdkConfigError в triageImage")
        self.assertRegex(m.group(0), RETRIAGE_RE, "причина обязана матчить RETRIAGE_RE — иначе после починки конфига карантин не перетриажится")

    def test_вердикт_1301_остаётся_неперетриаживаемым(self):
        # регресс урока 2026-11-21: вердикт фильтра НЕ матчит RETRIAGE_RE
        verdict = "контент-фильтр зрения отклонил кадр (1301) — вероятный X, вердикт фильтра (не сбой)"
        self.assertIn(verdict, self.src)
        self.assertIsNone(RETRIAGE_RE.search(verdict), "1301-вердикт вдруг стал перетриаживаемым")

    def test_разбор_отдельно_диагностирует_конфиг(self):
        self.assertIn("sdkCfgBroken", self.src)
        self.assertIn("авто-разбор недоступен: SDK-конфиг не готов", self.src)


class TestInboxRouteSdk(unittest.TestCase):
    """GET /api/t5/inbox отдаёт само-проверку конфига для баннера клиента."""

    def setUp(self):
        self.src = read(INBOX_ROUTE)

    def test_get_отдаёт_sdk_стейт(self):
        self.assertIn("import { readSdkConfigState } from '@/lib/t5/sdk-config';", self.src)
        self.assertIn("const sdk = await readSdkConfigState();", self.src)
        self.assertIn("NextResponse.json({ items, sdk })", self.src)


class TestStopSwitch(unittest.TestCase):
    """СТОП автотриажа в любой момент + баннер конфига на клиенте."""

    def setUp(self):
        self.src = read(INBOX_VIEW)

    def test_стоп_кнопка_обрывает_циклы(self):
        self.assertIn("OctagonX", self.src, "нет иконки СТОП-кнопки")
        self.assertRegex(self.src, r"onClick=\{stopLoops\}")
        stop = self.src.index("const stopLoops = useCallback")
        body = self.src[stop : self.src.index("}, []);", stop)]
        self.assertIn("manualStopRef.current = true;", body, "стоп обязан глушить автотриаж")
        self.assertIn("loopsAbort.current?.abort();", body, "стоп обязан обрывать активные циклы")

    def test_автотриаж_не_перезапускается_после_ручного_стопа(self):
        effect = self.src.index("if (loading || autoTriageRef.current || busy) return;")
        window = self.src[effect : effect + 400]
        self.assertIn("if (manualStopRef.current) return;", window, "автотриаж обязан молчать после ручного СТОПа")
        self.assertIn("if (sdkProblem) return;", window, "автотриаж обязан молчать при неготовом SDK-конфиге (иначе 401-пачка в карантин)")

    def test_явные_действия_снимают_ручной_стоп(self):
        # закинуть / прогнать триаж / перетриаж карантин / разобрать
        self.assertGreaterEqual(self.src.count("manualStopRef.current = false;"), 4)

    def test_красный_баннер_конфига(self):
        self.assertIn('role="alert"', self.src)
        self.assertIn("SDK-конфиг не готов", self.src)
        # клиент читает self-check из GET
        self.assertIn("data.sdk && !data.sdk.ok", self.src)

    def test_стоп_кнопка_видна_во_время_цикла(self):
        busy_banner = self.src.index("{busy && (")
        banner = self.src[busy_banner : self.src.index("{message && !busy", busy_banner)]
        self.assertIn("onClick={stopLoops}", banner, "СТОП обязан жить внутри рабочей полосы busy")
        self.assertIn("Стоп", banner)


if __name__ == "__main__":
    unittest.main()
