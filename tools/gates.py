#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
THREAD 5 — машинные гейты печи (аудит 2026-10-28, 8.2.1–8.2.6 + аудит 2026-10-31, рек. 1–4).

Проверяет СОГЛАСОВАННОСТЬ текста батча и физику заявок. Не пишет промпты,
не заменяет вердикт автора (LAWS §9: единственный законодатель — вердикт).

v1.2.0 (внешний аудит 2026-10-31, F1–F8): claim-exists, поиск заявки без
порядка слов, POS-флоры, реестровые коды, каст кинов, межбатчевый
копипаст, формат строки слота.
v1.3.0 (вердикт T5-08, 2026-10-31): claim-exists эскалирован до FAIL,
POS-бюджет снят (pos.unlimited). v1.4.0 (вердикт T5-09, 2026-11-01):
oc-class-floor — OC-промпты класса EXQUISITE не ниже (FAIL с T5-10).
v1.5.0 (директива автора 2026-11-01, рендер Hana для закрепления):
char-spec — POS каждого слота несёт идентичность ЯВНО (цвет волос /
цвет глаз / кожа / тело, specs/hair-eye-library.json + стемы gates.json);
пропущенный параметр = импровизация рендерера (урок T5-09 P26/P31:
POS без единого тега волос). FAIL с T5-10, исторические партии — WARN-эра;
⚗ НЕ освобождает (идентичность — не предмет эксперимента).
v1.6.0 (ревизия 2026-11-01, docs/THREAD5-REVIEW-2026-11-01.md, слой
«Сразу»): (1.1) NEG-линтер видит якорные стили «X gone / X intact /
X off / X on / X visible» — stem-сверка с POS, паразит без референса —
WARN, намеренный — [NEG-ANCHOR]; (1.2) контргейт header-contract —
отсутствующая декларация шапки (спред/EXP-оверлей/окно/каст/HEAT) =
WARN «проверка пропущена»: молчание шумит; (1.7) спред и каст фильтруют
OC по тегу/имени в скобках (is_oc_slot), не по жанру — миграция
ocClassGate на T5-10 не ломает подсчёты; (1.8) канон-вербатим ОС
(oc-canon.json) выведен из копипаст-WARN, исключения видны в квитанции
(canonExempt). Спеки валидируются tools/validate.py ДО гейтов (1.3);
pre-commit: untracked-квитанции блокируют коммит, special/SO-батчи под
замком, setup.sh ставит хук (1.11).
v1.7.0 (директива роста автора 2026-11-01, чат, «десять инициатив»):
(идея 2) header-contract несёт applyFrom на ключе — декларации
«ГИПОТЕЗА ДВИЖКА» и «ХОДЫ» обязательны с T5-10 (SO-кометы вне —
короткая орбита, движка нет); (идея 3) movesGate — декларация ходов
против specs/moves-ledger.json: M-id вне реестра / отставленный →
WARN, ход в 3 сданных батчах подряд → WARN «износ хода» (standing
не считает износ; отставка — только вердиктом); (идея 1) storyCardsGate —
батч ≥10 без batches/T5-NN/stories.md → WARN «бюджет мысли не
проверяем пост-фактум» (пилот story-cards T5-10).
v1.7.1 (заказ T5-10, чат автора 2026-11-01, вечер): IP-блок темы
расширен (no man's sky / hello games) по образцу T5-09; прямая
директива автора — слова witch/witches и тема-лексика ведьм НЕ БАНИТЬ
(никаких флоров/NEG на тему-слова). Данные-only изменение, гейты
не тронуты — дельта к v1.7.0 ожидается +0.

v1.8.0 (вердикт-директива автора 2026-11-03, «чистка негатива» + формат):
negHygiene — NEG v3 против «горохострелов»: изъятые классы (гениталии,
возраст-стек, solo-хвосты) в NEG ≥T5-12 — WARN; приборных юнитов >2 —
WARN (база держит candle/lamp); цветовые гарды волос — только canon-lock
ОС и ≤2 юнита; семантических гардов > negBase.perSlotGuardsMax — WARN
(«как на войну собрался»); условные гарды (2girls/see-through/wet
clothes) без референса в POS — WARN. formatGate — POS ≥4 семантических
строк (не башенка; строка ≤140 знаков), NEG ≤3 строк: пустые строки не
считаются, WARN с applyFrom 12. Исторические партии не переписываются.

v1.9.0 (вердикт T5-13, чат автора 2026-11-05: «верни в негатив тег loli»):
negBase v3.1 — age-stack-кластер (young girl, immature body, oversized
head, loli, shota) возвращён в NEG всегда (safety-пол; изъятый в v3
класс удалён из removedClasses — WARN за его присутствие снят, absence
в NEG ≥T5-12 теперь проверяется как всегда-юниты). formatGate —
maxLineChars 140 → 200 (первая NEG-строка несёт safety-пол; закон
«башенки» не отменён: POS ≥4 строк, NEG ≤3 строк). Данные-only,
код не тронут — поведение меняют только gates.json.

v1.10.0 (rating-repair 2026-11-13, применён аплоад автора
v1.10.1 (T5-22 «COLD STOCK», 2026-11-14): IP-флор темы расширен (altered carbon / cortical stack / dhf / needlecast) — тема живёт правилами кадра; перегрев R+ с T5-22 = FAIL (8.6-эра).
«T5-YODAYO-RATING-REPAIR-MERGED», Cole/Grok §1/§4/§12, + razbor
2026-11-13 урок В24): corridorAudit — fact ≠ label. R+ бейдж легален
только при коридоре A|B|A+B, объявленном полем «Corridor:» в теле слота;
R+ без поля или с «Corridor: —» = ложный бейдж → WARN (закон 8.6:
новый аудит стартует в WARN; FAIL — по решению вердикта). Счётчик
fact_R+ (коридор A|B|A+B) идёт в квитанцию рядом с label_R+. applyFrom
20; R/PG-13 слоты поле могут не нести. Парсер слота читает Corridor:
аналогично Channel:.

v1.11.0 (вердикт T5-23, постмортем рейтинга): claimPhysics — коридор =
физика в POS, не поле. R+ с Corridor A/B обязан нести в POS токены
объекта-прикрытия (A), геометрии позы/камеры (B) и класс раскрытия;
нарушение = WARN «бейдж само-сертифицирован» (В31). applyFrom 24.
Словари токенов — specs/gates.json claimPhysics.

v1.12.0 (поручение автора 2026-11-16 «Y-позы вместо поз и положений камеры»
+ «разительно баффнуть промпт-составляющую» + уборка по T5-23):
(1) yCardGate — Y-first (camera.json 1.13.0 y_assembly): R+ слот обязан
нести Y-card; слот с картой обязан нести токены паттерна в POS
(stem-сверка с camera.json); дубль карты в батче — WARN; счётчики
y_cards идут в квитанцию. Парсер слота читает Y-card: и Y## в шапке.
(2) claimPhysics расширен на спред R (applyToR: R-бейдж без класса
раскрытия exposure_r — WARN; постмортем T5-23 п.5). (3) conceptFlag —
R+ слот с концептом-визиткой (поклон/реверанс/витрина/волна) без
физики заявки — WARN «концепт несовместим с тиром, флаг автору»
(постмортем §4.3). (4) negDressGuards — гарды одетости в R+-слотах
(кроме X-доставки) — WARN (постмортем §4.4). (5) detailsGate — В32
«детали — постоянный слой»: каждый мейн/EXP несёт ≥2 фишечки-ФОРМЫ в
POS — WARN (поручение автора T5-23: «больше деталей… серёжки,
татуировочки, узоры…»).

v1.14.0 (акт 2 вердикта T5-24, приказ Б «доктрину переписать так, чтобы
в промптах она железобетонно печаталась как клеймо и была мега-важной
его составляющей»): yStampGate — клеймо = паспорт слота. Слот с Y-картой
обязан печатать в POS строку-клеймо (строка 3 PROSE PLUS, после
claim-строки, до деталей): «Y-STAMP: Y{NN} «класс» × поза карты 1:1 ×
камера карты · corridor X». FAIL с T5-25: нет клейма / клеймо не той
карты / паттерн пересказан (копипаст-юнит 1:1) / класс «—» (обёртка
В27 ПУСТО) под R+ / клеймо не исполняется телом POS. WARN: окно ротации
карт (глубина 3), коридор клейма ≠ полю Corridor:, клеймо без карты в
шапке. Ретро --retro — старые партии показывают пробел WARN-ами, история
не переписывается. В33: клеймо не самосертифицирует рейтинг. Строка
клейма выведена из капа «башенки» (formatGate) и из n-грамм копипаста
(паспорт ≠ исполнение). Прогон с ретро: --retro

v1.15.0 (вердикт автора 2026-11-19 по T5-25, В34 «и прочие обозначения
- не нужны, нужно только то, что за ними имеется в виду. Ты не оставляешь
промпт на произвол судьбы.» + В35 «чем лучше ты описываешь комбо, тем
лучше модель понимает что ей надо нарисовать.»): yStamp перевёрнут —
клеймо = вплетённый смысл, метка-паспорт из POS изъята. FAIL с T5-25:
служебные обозначения в POS (строка-метка Y-STAMP:, «класс», CAM-коды,
corridor-токен); паттерн карты не вплетён (стемы < minWeaveStems в одной
строке); пересказ паттерна (копипаст-юнит 1:1 подстрокой); чужая карта;
класс «—» (обёртка В27 ПУСТО) под R+; исполнение отсутствует (стемы
паттерна вне вплетения < minExecStems). WARN: окно ротации (глубина 3),
corridor карты ≠ полю Corridor:. Exemption'ы эры 1.14.0 сняты
(stamp_exempt_* = false): вплетение — обычная проза POS (formatGate и
n-граммы действуют). Ретро: история ≤T5-24 не переписывается.

v1.17.0 (заказ автора 2026-11-21, после вердикта T5-28: «У тебя есть комбо
Y, но одежда дрессера вообще не стакается с рейтингом. Даже если комбо
крутое и ёбнутое, неправильная одежда в неправильном состоянии скинет R+
комбо до PG-13. Надо найти способ стакнуть момент Y и одежду, а как — это
уже твоя забота»): yStackGate — Y×CLOSET STACK. closet.json v1.1.0 даёт
каждому CL-коду поле exposure (классы экспозиции Y-карт, которые вещь
держит честно: COVER|PROCESS|LINGERIE|CLOTHED-TIGHT|SHEER); dresser.json
v1.2.0 — секцию y_stack (матрица класс → полки-источники ∩ канал-партнёр
∩ gar_f-состояние ∩ душилки; закон: Y-FIRST сужает кубик ДО броска,
пустое пересечение → переброс КАРТЫ, не одежды). Гейт: слот с Y-картой
обязан нести ≥1 CL-код с exposure∋класс карты — иначе WARN «одежда душит
экспозицию» (R+/R — «слот падает до PG-13»). Парсер слота собирает
CL-коды-ВЕЩИ из Gar-строки (код + « (»; канон-ССЫЛКИ без скобок — нет).
Слоты без CL-кодов (ОС-канон VERBATIM, PG-13-выдох) не трогаются.
Счётчики y_stack — в квитанцию. WARN с T5-29; FAIL — по вердикту автора
(прецедент yCardGate: WARN с T5-24).

v1.16.0 (инженерный апгрейд 2026-11-20, трек «гейты молча не выключаются»):
(1) нулевой слот-парсинг = FAIL — батч с дрейфнувшим форматом шапки
(перенос строки внутри скобок) раньше проходил послотовые проверки НОЛЬ
раз и молча давал PASS (живой пример: special/SO-06); (2) окно ротации
Y-карт смотрит НАЗАД по номеру партии (как cross-copypaste), а не на
глобально новейшие — правка старого батча не ловит фантомные «карта в
окне» от будущих партий; (3) поле Corridor: терпит «A + B»/дефисы и
печатает фактическое значение в диагностику (а не «—»); (4) слоты
P100+, расы R100+ и ходы M100+ парсятся (реестры растут); (5) диапазон
Y-множества в сообщениях — из живого camera.json (Y1–Y521), не из
реликтовой эры Y1–Y18; (6) CLI: краш = exit 3 с баннером (отличим от
FAIL), битые --json/--md = exit 2 без трейсбека, stdout не падает на
кириллице в cp1251-пайпе; (7) квитанция пишет batch-путь относительно
корня репо + mkdir для --md — sha-замок хука не слепнет от чужого CWD.

v1.18.0 (вердикт T5-29, 2026-11-22, уроки В39–В43: «сделай так, чтобы ты
никогда нахуй больше таких ошибок не повторял»): (В39) voltCore — вольт-ядро
мейнов по Закону 24 (вольт-масса ≥ 13, ниша 5–8) + перемешивание (бег жанра
≤ 3 слота, блоки-акты запрещены); (В40) raceCast policy v2.0 — человек основа,
кин опция: окно 0–10 вместо вилки 12–14; (В41) exquisiteMain — EXQUISITE в
мейн-массе 1–4 (не только на ОС-тейпе); (В42) expHypothesis — каждая EXP-
клетка несёт H-XX из specs/open-hypotheses.json («полка отдыхает» незаконна,
тема партии клетки не кастует); (В43) ratingTruth — рейтинг = что кадр несёт
составом: панель ткани на груди держит потолок R, R+ = транзиентный холд
объекта руками (единственная крышка) или bare-line со стрэпами; калибровка
на ground truth T5-29 — 33/33 (совпали P04/P11/P18/P27). Все пять — эра
applyFrom 30: FAIL с T5-30, T5-29 и старшие задним числом не бьются (--retro
показывает WARN-ами, прецедент yStamp/paletteSkin). Разбор:
docs/POSTMORTEM-T5-29.md.

v1.18.1 (горячий фикс по рендеру T5-31, 2026-11-25): negBase.always расширен
41-м юнитом — джанк-баны В24 (whistle/keychain/keyring/charm: свистки и
связки ключей спавнились из POS-реквизита, каталог RENDER-TROUBLES В24) +
цвет-гард приёма «проступающие сосочки» (areola/pink nipples — NEG закрывает
ЦВЕТ, слой жив, §14.1 RATING-REPAIR). perSlotGuardsMax не тронут (4): новые
юниты — boilerplate, не «война». T5-31: PASS 0F/0W (квитанция v3).

Прогон:
    python3 tools/gates.py batches/T5-08.md \
        --json specs/gate-receipts/2026-10-30-T5-08-v12.json \
        --md batches/T5-08.gate-report.md
    python3 tools/gates.py --md-from-receipt specs/gate-receipts/<json>
        # 2026-11-21 (двойной аудит, P0-04): отчёт — ПРОИЗВОДНАЯ квитанции;
        # перегенерация MD из JSON без перегона батча (версия гейтов/ша/
        # вердикт — ровно те, что зафикированы, проверка №13 валидатора)
Выход: 0 = PASS · 1 = FAIL · 2 = битый вызов · 3 = краш инструмента.
"""

import hashlib
import json
import os
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

# кириллица + ⚗/☠ в cp1251-пайпе (Windows-консоль) не должны ронять печать
try:
    sys.stdout.reconfigure(errors="replace")
    sys.stderr.reconfigure(errors="replace")
except Exception:
    pass  # python < 3.7 или экзотика — работаем как работали

ROOT = Path(__file__).resolve().parent.parent
GATES = json.loads((ROOT / "specs/gates.json").read_text(encoding="utf-8"))

# Единый индекс сдачи партий (двойной аудит 2026-11-20, Коул §6.3 + P0-06):
# «кто сдан» решает ОДИН модуль — окно/жребий/CI читают его, черновики и
# ready не попадают в историю ротации до сдачи. Импорт после ROOT: t5delivery
# самодостаточен, но держим порядок для читаемости трейсов.
sys.path.insert(0, str(Path(__file__).resolve().parent))
import t5delivery  # noqa: E402

SLOT_RE = re.compile(
    r"^P(\d{2,3})\s+—\s+(\S+)\s+\((.+?)\)\s*[⚗☠]?\s*$"
)
STOP = {
    "the", "a", "an", "of", "and", "or", "to", "in", "on", "at", "by",
    "for", "with", "her", "his", "its", "as", "is", "are",
}


def words(text):
    return re.findall(r"[A-Za-z0-9_']+", text.lower())


def norm_ws(text):
    return re.sub(r"\s+", " ", text).strip()


class Slot:
    def __init__(self, sid, slug, paren, header_line):
        self.sid = f"P{sid}"
        self.slug = slug
        self.paren = paren
        self.header_line = header_line
        self.genre = ""
        self.rating = ""
        self.pose = ""
        self.palette = ""
        self.kinetics = []
        self.carriers = []
        self.channel = None
        self.channel_mark = ""
        self.corridor = None  # v1.10.0 corridorAudit: A|B|A+B|— (fact ≠ label)
        self.y_card = None    # v1.12.0 Y-first: карта Y## из шапки или поля Y-card
        self.gar_codes = []   # v1.17.0 yStack: CL-коды-ВЕЩИ из Gar-строки (код + « (»)
        # v1.14.0 Y-STAMP (акт 2, приказ Б): строка клейма в POS
        self.stamp_line = None
        self.stamp_id = None
        self.stamp_class = None
        self.stamp_corridor = None
        self.mark = "☠" if "☠" in header_line else ("⚗" if "⚗" in header_line else "")
        self.thesis = ""
        self.pos = ""
        self.neg = ""
        self.pos_lines = []
        self.neg_lines = []
        self.body_lines = [header_line.strip()]  # v1.12.0: шапка+тело слота целиком
        parts = [p.strip() for p in paren.split("·")]
        if parts:
            self.genre = parts[0]
        for p in parts:
            # аудит 2026-10-31, F3: метка внутри скобок («R+ ☠») не гасит тир
            p_clean = p.replace("☠", "").replace("⚗", "").strip()
            if p_clean in ("R+", "R", "PG-13", "X"):
                self.rating = p_clean
        m = re.search(r"\bPL\d+\b", paren)
        if m:
            self.pose = m.group(0)
        m = re.search(r"\bP\d{1,3}_[A-Z0-9_]+", paren)
        if m:
            self.palette = m.group(0)
        # v1.12.0 Y-first: карта может стоять в шапке слота рядом с PL
        m = re.search(r"\bY\d{1,3}\b", paren)  # 1.13.0: серия до Y512 (акт 1)
        if m:
            self.y_card = m.group(0)


def parse_batch(path):
    text = Path(path).read_text(encoding="utf-8")
    lines = text.splitlines()
    slots = []
    header_lines = []
    cur = None
    mode = None
    buf = []
    in_header_zone = True

    def flush_mode():
        nonlocal mode, buf
        if cur is not None and mode == "pos":
            cur.pos = norm_ws(" ".join(buf))
            cur.pos_lines = [l for l in buf if l]
            # v1.14.0 Y-STAMP (акт 2, приказ Б): клеймо карты — строка в POS
            for l in cur.pos_lines:
                if l.startswith("Y-STAMP:"):
                    cur.stamp_line = norm_ws(l)
                    sm = re.match(
                        r"^Y-STAMP:\s*(Y\d{1,3})\s*«([^»]*)»\s*×\s*(.+?)"
                        r"\s*·\s*corridor\s*([AB+]+|—)\s*$",
                        l,
                        re.I,
                    )
                    if sm:
                        cur.stamp_id = sm.group(1)
                        cur.stamp_class = sm.group(2).strip()
                        cur.stamp_corridor = sm.group(4)
                    break
        elif cur is not None and mode == "neg":
            cur.neg = norm_ws(" ".join(buf))
            cur.neg_lines = [l for l in buf if l]
        mode, buf = None, []

    for ln in lines:
        m = SLOT_RE.match(ln)
        if m and not ln.startswith((" ", "\t")):
            flush_mode()
            cur = Slot(m.group(1), m.group(2), m.group(3), ln)
            slots.append(cur)
            in_header_zone = False
            continue
        if ln.startswith("═"):
            flush_mode()
            continue
        if in_header_zone:
            header_lines.append(ln)
        if cur is None:
            continue
        sm = re.match(r"^Spine:\s*(.*)$", ln)
        if sm:
            flush_mode()
            cur.kinetics += re.findall(r"\bK\d{1,3}\b", sm.group(1))
            continue
        # v1.17.0 yStack: вещи слота — только «CL-XX-NN (описание)»; коды-ССЫЛКИ
        # («канон-механика CL-TS-13: …») без скобок — не вещи, не собираем
        gm = re.match(r"^Gar:\s*(.*)$", ln)
        if gm:
            cur.gar_codes = re.findall(r"\b(CL-[A-Z]{1,3}-\d{2,3})\s*\(", gm.group(1))
        sm = re.match(r"^Stack:\s*(.*)$", ln)
        if sm:
            flush_mode()
            cur.carriers += re.findall(r"\bCR-[A-Z]\d+\b", sm.group(1))
            continue
        sm = re.match(r"^Channel:\s*(.*)$", ln)
        if sm:
            flush_mode()
            val = sm.group(1).strip()
            cur.channel = val.split()[0] if val else None
            cur.channel_mark = "☠" if "☠" in val else ""
            continue
        sm = re.match(r"^Corridor:\s*(A\s*\+\s*B|A\+B|A|B|—|–|-)\s*$", ln)  # v1.10.0; v1.16.0: «A + B»/дефисы терпим
        if sm:
            flush_mode()
            cur.corridor = norm_ws(sm.group(1).replace(" ", ""))
            if cur.corridor in ("—", "–", "-"):
                cur.corridor = "—"
            continue
        sm = re.match(r"^Y-card:\s*(Y\d{1,3})", ln)  # v1.12.0 Y-first; 1.13.0: до Y512
        if sm:
            flush_mode()
            cur.y_card = sm.group(1)
            continue
        if cur is not None:  # v1.12.0: тело слота целиком — для окна/fallback
            cur.body_lines.append(ln.strip())
        if re.match(r"^POS:\s*$", ln):
            flush_mode()
            mode, buf = "pos", []
            continue
        if re.match(r"^NEG:\s*$", ln):
            flush_mode()
            mode, buf = "neg", []
            continue
        tm = re.match(r"^THESIS:\s*(.*)$", ln)
        if tm:
            flush_mode()
            cur.thesis = tm.group(1).strip()
            continue
        if mode:
            buf.append(ln.strip())
    flush_mode()
    header = "\n".join(header_lines)
    return text, header, slots


def ab_pairs_from_header(header):
    return {
        frozenset((a, b))
        for a, b in re.findall(r"\((P\d{2,3})\s*,\s*(P\d{2,3})\)", header)
    }


def is_oc_slot(s, oc_names=()):
    """Ревизия 2026-11-01, 1.7: OC опознаётся по тегу/имени в скобках, не по жанру.

    С T5-10 жанр OC-слотов становится EXQUISITE (ocClassGate) — жанровые
    фильтры спреда/каста иначе начнут считать бывшие OC-слоты мейнами.
    """
    tokens = {t.strip() for t in s.paren.split("·")}
    return "OC" in tokens or bool(tokens & {n for n in oc_names if n})


def removed_neg_classes():
    """negBase v3 (gates.json v1.8.0): классы, изъятые из NEG вердиктом
    2026-11-03 («Чистка негатива (частичная)»). Слова остаются флорами POS,
    но NEG их больше не несёт — гейт не должен требовать изъятое."""
    nb = GATES.get("negBase", {})
    out = set()
    for units in nb.get("removedClasses", {}).values():
        out.update(u.lower() for u in units)
    return out


def neg_v3_active(batch_no):
    nb = GATES.get("negBase", {})
    return batch_no >= int(nb.get("applyFrom", 10**9))


def check_floors(slot, fails, batch_no=-1):
    neg = slot.neg.lower()
    skip = removed_neg_classes() if neg_v3_active(batch_no) else set()
    for f in GATES["header"]["hardFloors"]:
        if f.lower() in skip:
            continue
        if f.lower() not in neg:
            fails.append((slot.sid, "floor", f"NEG нет hard-флоры: {f}"))
    for w in GATES["header"]["candleFloorWords"]:
        if w not in neg:
            fails.append((slot.sid, "floor", f"NEG нет candle/lamp-флоры: {w}"))
    for w in GATES["header"]["antiWash"]:
        if w.lower() not in neg:
            fails.append((slot.sid, "floor", f"NEG нет анти-ваша: {w}"))


def stem_variants(w):
    """Варианты слова для сверки POS↔NEG: snakes→{snakes,snake,snak}, joints→{joints,joint}."""
    v = {w}
    if w.endswith("ies") and len(w) > 4:
        v.add(w[:-3] + "y")
    if w.endswith("es") and len(w) > 3:
        v.add(w[:-2])
    if w.endswith("s") and not w.endswith("ss") and len(w) > 3:
        v.add(w[:-1])
    return v


def check_neg_linter(slot, fails, warns):
    if not slot.neg:
        fails.append((slot.sid, "neg", "NEG пуст"))
        return
    pos_stems = set()
    for w in words(slot.pos):
        pos_stems |= stem_variants(w)
    for unit in slot.neg.split(","):
        unit = norm_ws(unit)
        if not unit:
            continue
        uwords = words(unit)
        if len(uwords) > GATES["neg"]["unitMaxWords"]:
            warns.append(
                (slot.sid, "neg-unit",
                 f"юнит NEG из {len(uwords)} слов: «{unit}»")
            )
        m = re.match(GATES["neg"]["noClassPattern"], unit.lower())
        if m:
            hit = []
            for tw in words(m.group(2)):
                if tw in STOP or len(tw) < 3:
                    continue
                if stem_variants(tw) & pos_stems:
                    hit.append(tw)
            if hit:
                fails.append(
                    (slot.sid, "neg-no-class",
                     f"«{unit}» отрицает то, что заявлено в POS (→ {', '.join(hit)})")
                )
        else:
            # Ревизия 2026-11-01, 1.1: якорные стили «X gone / X intact /
            # X off / X on / X visible» — раньше гейтом не видны вообще.
            # Stem-сверка X с POS: якорь без референса — паразит-NEG →
            # WARN; намеренный паразит — пометка [NEG-ANCHOR].
            cfg_a = GATES["neg"]
            mark = cfg_a.get("anchorMark", "[NEG-ANCHOR]")
            probe = re.sub(re.escape(mark), " ", unit, flags=re.I).strip().lower()
            am = re.match(
                r"^(.+?)\s+("
                + "|".join(cfg_a.get("anchorStyles", []))
                + r")$",
                probe,
            )
            if am:
                xstems = set()
                for tw in words(am.group(1)):
                    if tw in STOP or len(tw) < 3:
                        continue
                    xstems |= stem_variants(tw)
                marked = mark.lower() in slot.neg.lower()
                if not (xstems & pos_stems) and not marked:
                    warns.append(
                        (slot.sid, "neg-anchor",
                         f"якорь-юнит «{unit}» ({am.group(2)}) не ссылается ни на "
                         f"один элемент POS — паразит-NEG? намеренный якорь пометь "
                         f"{mark} (ревизия 2026-11-01, 1.1)")
                    )
        low = unit.lower()
        if low == "nipples exposed" and re.search(
            r"covered nipples|clothed nipples|see-through|wet clothes|pantyline",
            slot.pos, re.I,
        ):
            fails.append(
                (slot.sid, "neg-self-shot",
                 "«nipples exposed» в NEG сквозь-ткань слота глушит заявку (каталог A3)")
            )


def check_neg_hygiene(slot, fails, warns, batch_no=-1, oc_names=()):
    """v1.8.0 — NEG v3 против «горохострелов» (вердикт автора 2026-11-03).
    Изъятые классы / приборы >2 / цветовые гарды волос вне canon-lock ОС /
    гарды > perSlotGuardsMax / условные гарды без референса в POS → WARN."""
    cfg = GATES.get("negBase") or {}
    if not cfg or (0 <= batch_no < cfg.get("applyFrom", 10 ** 9)):
        return
    units = [norm_ws(u) for u in slot.neg.split(",") if norm_ws(u)]
    low = [u.lower() for u in units]
    low_set = set(low)

    for cls, lst in (cfg.get("removedClasses") or {}).items():
        for u in lst:
            if u.lower() in low_set:
                warns.append((slot.sid, "neg-hygiene",
                              f"«{u}» — класс «{cls}» изъят из NEG (negBase v3): "
                              f"никогда не рисовался бы и без нас"))

    base_set = {b.lower() for b in cfg.get("always", [])}
    cond_map = cfg.get("conditional") or {}
    semantic = 0
    for u, ul in zip(units, low):
        if ul in base_set:
            continue
        semantic += 1
        need = cond_map.get(u) or cond_map.get(ul)
        if need and not re.search(need, slot.pos, re.I):
            warns.append((slot.sid, "neg-hygiene",
                          f"гард «{u}» без референса в POS (нужен: {need}) — "
                          f"паразит-NEG (negBase v3, смежно закону №14)"))
    if semantic > cfg.get("perSlotGuardsMax", 4):
        warns.append((slot.sid, "neg-hygiene",
                      f"семантических гардов {semantic} > {cfg.get('perSlotGuardsMax', 4)} — "
                      f"NEG собрался на войну (вердикт 2026-11-03)"))

    dev_words = ("candle", "candles", "candelabra", "lamp", "bulb", "lightbulb",
                 "lantern", "torch", "chandelier", "brazier", "streetlight",
                 "floodlight", "spotlight")
    devs = [u for u in low if u in dev_words]
    if len(devs) > 2:
        warns.append((slot.sid, "neg-hygiene",
                      f"приборных юнитов {len(devs)} > 2 — база v3 держит только candle, lamp "
                      f"(закон света v2: POS без приборов)"))

    hc = [u for u in low if re.search(r"^(?:not\s+)?[a-z\-]+\s+hair$", u)]
    if hc and not is_oc_slot(slot, oc_names):
        warns.append((slot.sid, "neg-hygiene",
                      f"цветовые гарды волос ({', '.join(hc)}) — только canon-lock ОС; "
                      f"у рандомных девиц цвет пишет POS VERBATIM (negBase v3)"))
    elif len(hc) > 2:
        warns.append((slot.sid, "neg-hygiene",
                      f"цветов волос в NEG {len(hc)} > 2 — «несколько цветов волос» "
                      f"лишняя хуйня (вердикт 2026-11-03)"))


def check_format_gate(slot, warns, batch_no=-1):
    """v1.8.0 — формат-гейт «не башенка» (вердикт автора 2026-11-03):
    POS ≥ posMinLines семантических строк, NEG ≤ negMaxLines строк,
    строка ≤ maxLineChars. Пустые строки не считаются."""
    cfg = GATES.get("formatGate") or {}
    if not cfg or (0 <= batch_no < cfg.get("applyFrom", 10 ** 9)):
        return
    mx = cfg.get("maxLineChars", 140)
    # v1.14.0 yStamp: строка клейма выведена из капа «башенки» — её длину
    # задаёт карта (копипаст-юнит), а не дисциплина строк POS (LAWS §17.7)
    stamp_prefix = ((GATES.get("yStamp") or {}).get("linePrefix", "Y-STAMP")) + ":"
    stamp_exempt_fmt = bool(((GATES.get("yStamp") or {}).get(
        "stamp_exempt_format_gate", True)))
    pos_lines = [l for l in getattr(slot, "pos_lines", []) if l.strip()]
    if pos_lines:
        if len(pos_lines) < cfg.get("posMinLines", 4):
            warns.append((slot.sid, "format",
                          f"POS собран в {len(pos_lines)} строку(и) — башенка: разбросай "
                          f"по семантическим строкам (≥{cfg.get('posMinLines', 4)})"))
        for l in pos_lines:
            if len(l) > mx and not (stamp_exempt_fmt and l.startswith(stamp_prefix)):
                warns.append((slot.sid, "format",
                              f"POS-строка {len(l)} знаков > {mx} — башенка, читается "
                              f"по вертикали, а не разом"))
    neg_lines = [l for l in getattr(slot, "neg_lines", []) if l.strip()]
    if neg_lines and len(neg_lines) > cfg.get("negMaxLines", 3):
        warns.append((slot.sid, "format",
                      f"NEG в {len(neg_lines)} строках > {cfg.get('negMaxLines', 3)} — "
                      f"лишние абзацы ни к чему (вердикт 2026-11-03)"))


CLAIM_RE = re.compile(
    "|".join(re.escape(s) for s in sorted(
        GATES["claim"]["signal_lexemes"], key=len, reverse=True)),
    re.I,
)


# Поиск заявки БЕЗ порядка слов (аудит 2026-10-31, F1/P19: «forearms crossed
# over her bare breasts» против лексемы «crossed forearms over»).
MULTIWORD_CLAIMS = [
    s for s in GATES["claim"]["signal_lexemes"] if len(words(s)) > 1
]


def claim_token(slot):
    for m in CLAIM_RE.finditer(slot.pos):
        prefix = slot.pos[: m.start()]
        return len(words(prefix)), m.group(0).lower()
    wl = words(slot.pos)
    for lex in MULTIWORD_CLAIMS:
        lw = words(lex)
        if sum(1 for w in lw if w not in STOP) < 2:
            continue  # общие наборы («tape over») без порядка не маттим
        n = len(lw)
        for i in range(len(wl) - n + 1):
            if sorted(wl[i: i + n]) == sorted(lw):
                return i, f"{lex} (без порядка слов)"
    return None, None


def check_salience(slot, idx, sig, fails, warns):
    if idx is None:
        return idx
    if slot.mark:  # умышленный нарушитель (EXP-полигон, закон ⚗) — не гейтится
        return idx
    limit_key = "maxTokenRplus" if slot.rating == "R+" else "maxTokenR"
    limit = GATES["claim"][limit_key]
    hard = slot.rating == "R+"
    if idx > limit:
        msg = f"заявка «{sig}» на токене {idx} > {limit}"
        (fails if hard else warns).append(
            (slot.sid, "salience", msg + ("" if hard else " (R, WARN)"))
        )
    return idx


def check_pos_budget(slot, fails, warns):
    n = len(words(slot.pos))
    if GATES["pos"].get("unlimited"):
        # Вердикт T5-08 (2026-10-31): бюджет POS не ограничивается — решение
        # автора (ответ на F8 аудита). Число слов остаётся в отчёте.
        return n
    if n > GATES["pos"]["hardTokens"]:
        fails.append((slot.sid, "pos-budget", f"POS {n} слов > hard {GATES['pos']['hardTokens']}"))
    elif n > GATES["pos"]["targetTokens"]:
        warns.append((slot.sid, "pos-budget", f"POS {n} слов > цель {GATES['pos']['targetTokens']}"))
    return n


def strip_boilerplate(pos):
    out = pos
    for b in GATES["copypaste"]["boilerplateStrip"]:
        out = re.sub(re.escape(b), " ", out, flags=re.I)
    return out


def load_canon_grams():
    """Ревизия 2026-11-01, 1.8: n-граммы канон-вербатима ОС (oc-canon.json).

    Канон ОС повторяется от партии к партии по праву (ЛОКи внешности),
    это не копипаст: 6-граммы из текстовых полей ростера не шумят
    парными и межбатчевыми WARN. FAIL ≥3 слотов каноном не гасится.
    Исключения не молчат: счётчик canonExempt в квитанции.
    """
    rel = GATES["copypaste"].get("canonWhitelist")
    if not rel:
        return frozenset()
    try:
        data = json.loads((ROOT / rel).read_text(encoding="utf-8"))
    except Exception:
        return frozenset()
    n = GATES["copypaste"]["ngramWords"]
    grams = set()

    def collect(o):
        if isinstance(o, str):
            wl = words(o)
            for i in range(len(wl) - n + 1):
                grams.add(" ".join(wl[i: i + n]))
        elif isinstance(o, dict):
            for v in o.values():
                collect(v)
        elif isinstance(o, list):
            for v in o:
                collect(v)

    for oc in (data.get("ocs") or {}).values():
        collect(oc)
    return frozenset(grams)


def check_copypaste(slots, ab_pairs, fails, warns, canon_grams=frozenset()):
    gram_slots = {}
    for s in slots:
        wl = words(strip_boilerplate(pos_prose(s)))
        for i in range(len(wl) - GATES["copypaste"]["ngramWords"] + 1):
            g = " ".join(wl[i: i + GATES["copypaste"]["ngramWords"]])
            gram_slots.setdefault(g, set()).add(s.sid)
    fails_seen, warn_pairs, canon_exempt = set(), set(), []
    for g, ids in gram_slots.items():
        if len(ids) >= GATES["copypaste"]["failSharedBySlots"]:
            key = ("FAIL", tuple(sorted(ids)), g)
            if key not in fails_seen:
                fails_seen.add(key)
                fails.append(
                    (",".join(sorted(ids)), "copypaste",
                     f"{len(ids)} слота делят n-грамму: «{g}»")
                )
        elif len(ids) == 2:
            pair = frozenset(ids)
            if pair in ab_pairs:
                continue
            if g in canon_grams:
                canon_exempt.append({"gram": g, "slots": sorted(ids)})
                continue
            warn_pairs.add((tuple(sorted(ids)), g))
    for (a, b), g in sorted(warn_pairs)[:20]:
        warns.append((f"{a}+{b}", "copypaste", f"пара делит n-грамму: «{g}»"))
    return canon_exempt


def load_burned():
    data = json.loads((ROOT / "specs/burned.json").read_text(encoding="utf-8"))
    return {e["code"] for e in data["entries"]}


def load_channels():
    data = json.loads(
        (ROOT / GATES["channels"]["registry"]).read_text(encoding="utf-8")
    )
    return {c["id"]: c for c in data["channels"]}


def check_burn(slot, burned, fails):
    codes = [c for c in [slot.palette, slot.pose] if c] + slot.kinetics + slot.carriers
    for c in codes:
        if c in burned:
            fails.append(
                (slot.sid, "burn", f"{c} в burn-реестре (сгорел, в оборот нельзя)")
            )


def check_channels(slots, channels, fails, warns):
    quota = GATES["channels"]["candidateQuotaPerBatch"]
    cand_used, panty_used = [], []
    for s in slots:
        if not s.channel:
            if s.rating in ("R+", "X") and s.genre != "EXP":
                warns.append((s.sid, "channel", "R+ слот без аннотации Channel:"))
            continue
        ch = channels.get(s.channel)
        if ch is None:
            warns.append((s.sid, "channel", f"канал «{s.channel}» не в реестре"))
            continue
        status = ch["status"]
        if s.genre == "EXP" and GATES["channels"]["expOverlayExempt"]:
            continue
        if s.channel in GATES["channels"]["exempt"]:
            continue
        if s.rating in ("R+", "X"):
            if status in ("dead", "rehab", "artifact"):
                fails.append((s.sid, "channel", f"R+ на {status}-канале {s.channel}"))
            elif status == "candidate":
                if GATES["channels"]["candidateMark"] not in (s.channel_mark or ""):
                    warns.append(
                        (s.sid, "channel",
                         f"candidate-канал {s.channel} без пометки ☠")
                    )
                cand_used.append(s.sid)
                if s.channel == "pantyline-lower":
                    panty_used.append(s.sid)
    if len(cand_used) > quota:
        warns.append(
            ("BATCH", "channel-quota",
             f"candidate-каналы использованы {len(cand_used)}× ({','.join(cand_used)}) > {quota} — WARN волны 2, эскалация по KPI")
        )
    if len(panty_used) > 2:
        warns.append(
            ("BATCH", "pantyline-quota",
             f"pantyline {len(panty_used)}× ({','.join(panty_used)}) > 2 — WARN волны 2")
        )


def check_corridor(slots, warns, fails, batch_no=-1):
    """v1.10.0 corridorAudit (закон 8.6: WARN-старт). fact ≠ label:
    R+ бейдж легален только при коридоре A|B|A+B (Corridor: в теле слота).
    R+ без поля / с «—» = ложный бейдж — хуже честного R. Счётчик fact_R+
    возвращается для квитанции. applyFrom/mode — specs/gates.json.
    v1.13.0 В33 (автор 2026-11-17 «устрани пиздёж в рейтинге»: либо честно
    «не получилось», либо реальный тир): с failFrom ложный бейдж = FAIL,
    а не WARN-статистика."""
    cfg = GATES.get("corridorAudit")
    if not cfg or (0 <= batch_no < int(cfg.get("applyFrom", 10 ** 9))):
        return 0
    legal = set(cfg.get("corridors_legal", ["A", "B", "A+B"]))
    downgrade = cfg.get("corridor_downgrade", "—")
    fact = 0
    for s in slots:
        if s.rating not in ("R+", "X"):
            continue
        if s.corridor in legal:
            fact += 1
            continue
        why = "нет поля Corridor:" if s.corridor is None else f"Corridor: {s.corridor!r}"
        entry = (
            s.sid, "corridor",
            f"R+ без коридора A|B ({why}) — ложный бейдж хуже честного R: "
            f"вшить объект у груди (A) / камеру-интим (B) или писать R"
        )
        if batch_no >= int(cfg.get("failFrom", 10 ** 9)):
            fails.append(entry)  # В33: с failFrom ложный бейдж = FAIL
        else:
            warns.append(entry)
    return fact


def check_claimphysics(slots, warns, batch_no=-1):
    """v1.11.0 claimPhysics (В31; вердикт T5-23 + docs/RATING-POSTMORTEM-T5-23.md).
    Коридор = физика в POS, не поле. Поле «Corridor:» писал тот же писец, что и
    POS — самосертификация не считается (T5-23: 18 бейджей R+, триаж рендеров
    29 sfw / 4 borderline). R+ обязан нести в POS токены: (A) объект-прикрытие,
    (B) геометрия позы/камеры, плюс класс раскрытия. Нарушение → WARN
    «бейдж само-сертифицирован» (закон 8.6: WARN-старт, FAIL — по вердикту)."""
    cfg = GATES.get("claimPhysics")
    if not cfg or (0 <= batch_no < int(cfg.get("applyFrom", 10 ** 9))):
        return 0
    cover = [t.lower() for t in cfg.get("cover_a", [])]
    geom = [t.lower() for t in cfg.get("geometry_b", [])]
    expo = [t.lower() for t in cfg.get("exposure", [])]
    expo_r = [t.lower() for t in cfg.get("exposure_r", [])]
    caught = 0
    r_caught = 0
    for s in slots:
        if s.rating in ("R+", "X") and s.corridor and s.corridor != "—":
            pos = (s.pos or "").lower()
            corr = s.corridor.upper()
            miss = []
            if "A" in corr and not any(t in pos for t in cover):
                miss.append("нет объекта-прикрытия (коридор A)")
            if "B" in corr and not any(t in pos for t in geom):
                miss.append("нет геометрии позы/камеры (коридор B)")
            if not any(t in pos for t in expo):
                miss.append("нет класса раскрытия")
            if miss:
                caught += 1
                warns.append(
                    (s.sid, "claim-physics",
                     f"R+ бейдж само-сертифицирован ({'; '.join(miss)}) — поле Corridor "
                     f"не равно физике: вшить токен-объект/геометрию/раскрытие или "
                     f"писать честный R (В31, постмортем рейтинга T5-23)")
                )
        elif s.rating == "R" and cfg.get("applyToR"):
            # v1.12.0: словарь раскрытия на спред R (постмортем §5 — NICHE-мейны
            # с бейджем R за счёт «reading her breast shape» = PG-13 с бейджем)
            pos = (s.pos or "").lower()
            if not any(t in pos for t in expo_r):
                r_caught += 1
                warns.append(
                    (s.sid, "claim-physics-r",
                     "R-бейдж без класса раскрытия — тело не разоблачено ни одним "
                     "токеном (exposure_r): вшить состояние ткани/зону/процесс или "
                     "писать PG-13 (В31 на спред R, поручение автора 2026-11-16)")
                )
    return caught + r_caught


def load_closet_exposure():
    """v1.17.0 yStack: closet.json v1.1.0 — код → exposure-классы, которые
    вещь держит честно (Y×CLOSET STACK, заказ автора 2026-11-21)."""
    try:
        data = json.loads((ROOT / "specs" / "closet.json").read_text(encoding="utf-8"))
        return {
            it["code"]: list(it.get("exposure", []))
            for v in (data.get("shelves") or {}).values()
            for it in v.get("items", [])
        }
    except Exception:
        return {}


def load_y_cards():
    """v1.12.0 Y-first: карты из specs/camera.json y_cards (паттерн = pose+camera)."""
    try:
        data = json.loads((ROOT / "specs/camera.json").read_text(encoding="utf-8"))
        return {c["id"]: c for c in data.get("y_cards", {}).get("cards", [])}
    except Exception:
        return {}


def y_range(ycards):
    """v1.16.0: живой диапазон множества из camera.json («Y1–Y521»),
    а не зашитая строка реликтовой эры («Y1–Y18»)."""
    nums = sorted(int(k[1:]) for k in ycards if re.fullmatch(r"Y\d+", k))
    if not nums:
        return "Y∅ (camera.json не читается!)"
    return f"Y{nums[0]}–Y{nums[-1]}"


def _pattern_stems(card):
    """Отличительные стемы паттерна карты: pattern+camera, слова ≥5 символов без STOP."""
    comp = card.get("components") or {}
    src = " ".join([card.get("pattern", ""), comp.get("camera", "")])
    out = set()
    for w in words(src):
        w = w.strip("'")
        if len(w) >= 5 and w not in STOP and not w.isdigit():
            out.add(w[:5])
    return out


def check_ycards(slots, warns, batch_no=-1, ab_pairs=frozenset()):
    """v1.12.0 yCardGate (Y-first, поручение автора 2026-11-16 «Y-позы вместо поз
    и положений камеры»; база — вердикт T5-23: Y-комбо легальны в мейнах/ОС).
    (1) R+ слот без Y-card — WARN «сборка мимо Y-множества» (выход: карта Y1–Y18
    или PL-сборка с причиной в THESIS — PG-13/NICHE-выдох). (2) слот с картой:
    ≥minPatternStems стемов паттерна в POS (копипаст-юнит обязан доехать);
    (3) дубль карты в батче — WARN (кроме A/B-пар). Счётчики — в квитанцию."""
    cfg = GATES.get("yCards")
    if not cfg or (0 <= batch_no < int(cfg.get("applyFrom", 10 ** 9))):
        return {"used": [], "rplus_without": 0, "pattern_misses": 0, "duplicates": 0}
    ycards = load_y_cards()
    used, seen = [], Counter()
    rplus_without = 0
    pattern_misses = 0
    duplicates = 0
    for s in slots:
        if s.y_card:
            used.append(s.y_card)
            seen[s.y_card] += 1
            if s.y_card not in ycards:
                warns.append(
                    (s.sid, "y-card",
                     f"Y-card {s.y_card} не найдена в camera.json (множество {y_range(ycards)})")
                )
                continue
            stems = _pattern_stems(ycards[s.y_card])
            pos_stems = {w[:5] for w in words(s.pos) if len(w) >= 5}
            hits = len(stems & pos_stems)
            if hits < int(cfg.get("minPatternStems", 2)):
                pattern_misses += 1
                warns.append(
                    (s.sid, "y-card",
                     f"паттерн {s.y_card} не доехал в POS ({hits} стемов из "
                     f"≥{cfg.get('minPatternStems', 2)}) — карта копируется в POS "
                     "целиком (копипаст-юнит), не пересказывается")
                )
        elif s.rating == "R+" and cfg.get("rplusRequiresCard", True):
            rplus_without += 1
            warns.append(
                (s.sid, "y-card",
                 "R+ слот собран мимо Y-множества (нет Y-card) — Y-first: собрать "
                 f"по карте из camera.json ({y_range(ycards)}, y_assembly) или записать в THESIS "
                 "причину PL-сборки (PG-13/NICHE-выдох не считается)")
            )
    for yid, n in seen.items():
        if n > 1:
            # A/B-пара одной переменной — легальный дубль
            pair_slots = [s.sid for s in slots if s.y_card == yid]
            if len(pair_slots) == 2 and frozenset(pair_slots) in ab_pairs:
                continue
            duplicates += 1
            warns.append(
                ("BATCH", "y-card",
                 f"карта {yid} использована {n}× в батче — повтор паттерна читается "
                 f"копипастом; окно ротации Y-карт — 3 батча (y_assembly.window)")
            )
    return {"used": used, "rplus_without": rplus_without,
            "pattern_misses": pattern_misses, "duplicates": duplicates}


def load_combo_map():
    """v1.13.0 comboPose: составные позы poses.json (combo:true) -> их карты."""
    try:
        data = json.loads((ROOT / "specs/poses.json").read_text(encoding="utf-8"))
        return {
            p["id"]: p.get("card")
            for p in data.get("poses", []) if p.get("combo")
        }
    except Exception:
        return {}


def _card_pose_stems(card, minlen=5):
    """v1.14.0: стемы позы карты (components.pose) для проверки исполнения."""
    src = (card.get("components") or {}).get("pose", "") or ""
    out = set()
    for w in words(src):
        w = w.strip("'")
        if len(w) >= minlen and w not in STOP and not w.isdigit():
            out.add(w[:5])
    return out


def load_prev_y_usage(depth, exclude=None, batch_no=-1):
    """v1.14.0 yStamp: окно ротации карт — что использовано в последних
    `depth` сданных батчах ДО ТЕКУЩЕЙ партии (v1.16.0: фильтр по номеру,
    как в check_cross_batch — правка старого батча не должна видеть
    «будущие» партии как «предыдущие»). Возвращает {Y-id: имя батча}.
    2026-11-21: «кто сдан» — через t5delivery (индекс сдачи), не локальный
    glob: черновик T5-28 больше не считается «предыдущей партией»."""
    prevs = sorted(
        (p for _no, p in t5delivery.delivered_batches(batch_dir=ROOT / "batches")
         if (exclude is None or p.resolve() != Path(exclude).resolve())
         and (batch_no <= 0 or 0 < batch_number(p) < batch_no)),
        key=lambda p: (batch_number(p), p.stat().st_mtime),
    )
    used = {}
    # depth=0 — окно выключено (v1.16.0: раньше «-max(0, 0):» отдавало ВСЕ батчи)
    for p in (prevs[-depth:] if depth > 0 else []):
        try:
            _, _, pslots = parse_batch(p)
        except Exception:
            continue
        for s in pslots:
            if s.y_card:
                used.setdefault(s.y_card, p.name)
    return used


def check_ystack(slots, warns, batch_no=-1):
    """v1.17.0 yStackGate (Y×CLOSET STACK, заказ автора 2026-11-21 после вердикта
    T5-28: «У тебя есть комбо Y, но одежда дрессера вообще не стакается с
    рейтингом. Даже если комбо крутое и ёбнутое, неправильная одежда в
    неправильном состоянии скинет R+ комбо до PG-13»). Слот с Y-картой обязан
    нести хотя бы один CL-код, чьё exposure (closet.json v1.1.0) содержит класс
    экспозиции карты — иначе одежда душит сигнал: WARN «стак пуст». Слоты без
    CL-кодов (ОС-канон VERBATIM / PG-13-выдох) не трогаются: у канона своя
    механика прикрытия в Channel-строке. Душилка при живом носителе (носки
    под PROCESS-платьем и т.п.) — легальный слой-партнёр, не шумим."""
    cfg = GATES.get("yStack")
    if not cfg or (0 <= batch_no < int(cfg.get("applyFrom", 10 ** 9))):
        return {"checked": 0, "stacked": 0, "choked": 0, "canon_without_codes": 0,
                "geometry_only": 0}
    ycards = load_y_cards()
    closet_exp = load_closet_exposure()
    # смежность (v1.17.0): обтягивающая вещь не прячет геометрию прикрытия —
    # CLOTHED-TIGHT держит и COVER-карты (душат COVER только «объёмные
    # закрытые» — oversized/застёгнутые плотные слои без обоих классов);
    # обратное неверно: COVER-вещь (backless/кроп) не несёт bumps → CLOTHED-TIGHT-карту душит
    carries = {"COVER": {"COVER", "CLOTHED-TIGHT"}}
    st = {"checked": 0, "stacked": 0, "choked": 0, "canon_without_codes": 0,
          "geometry_only": 0}
    for s in slots:
        if not s.y_card or s.y_card not in ycards:
            continue  # карты нет / неизвестна — это территория yCardGate
        card = ycards[s.y_card]
        exposure_class = ((card.get("components") or {}).get("exposure") or {}).get("class")
        if not exposure_class or exposure_class == "—":
            # класс «—»: интим несёт ГЕОМЕТРИЯ позы (коридор B, «наследуется
            # от позы») — экспозиционного класса нет, одеждой не душится
            if s.gar_codes:
                st["geometry_only"] += 1
            continue
        if not s.gar_codes:
            if s.rating in ("R+", "R"):
                st["canon_without_codes"] += 1
            continue  # ОС-канон/PG-13 — не территория стака
        st["checked"] += 1
        wanted = carries.get(exposure_class, {exposure_class})
        known = [c for c in s.gar_codes if c in closet_exp]
        unknown = [c for c in s.gar_codes if c not in closet_exp]
        carriers = [c for c in known if wanted & set(closet_exp[c])]
        if unknown:
            warns.append((s.sid, "y-stack",
                          "CL-код(ы) %s не найдены в closet.json (шкаф v1.1.0+) — "
                          "стак не проверен, проверь код вручную" % ", ".join(unknown)))
        if carriers:
            st["stacked"] += 1
        else:
            st["choked"] += 1
            drop = " — R+/R сигнал не прочитается, слот падает до PG-13" if s.rating in ("R+", "R") else ""
            warns.append((s.sid, "y-stack",
                          "одежда душит экспозицию карты %s (%s): ни один CL-код "
                          "%s не держит класс (closet.json exposure) — переброс "
                          "вещи по матрице dresser.json y_stack%s"
                          % (s.y_card, exposure_class, ", ".join(s.gar_codes), drop)))
    return st


def check_ystamp(batch_path, slots, warns, fails, batch_no=-1, retro=False):
    """v1.15.0 yStamp (вердикт автора 2026-11-19 по T5-25, В34 «и прочие
    обозначения - не нужны, нужно только то, что за ними имеется в виду. Ты
    не оставляешь промпт на произвол судьбы.» + В35 «я генерил без PH и
    понял, что чем лучше ты описываешь комбо, тем лучше модель понимает что
    ей надо нарисовать.»). Клеймо = вплетённый смысл: слот с Y-картой несёт
    в POS строку 3 (после claim-строки, до деталей) = паттерн карты КОПИПАСТ
    1:1 с физикой — БЕЗ строки-метки «Y-STAMP: Y{NN} «класс» × ... · corridor
    X»: обозначения в POS запрещены, каждое доезжает только смыслом (камера —
    камерным кластером OPENER, коридор — физикой claim-строки, класс —
    рейтингом слота). Паспорт живёт в метаданных: поле Y-card в шапке, чип
    прилавка (печатается из camera.json по id).

    FAIL (с failFrom=applyFrom=25):
      (1) служебные обозначения в POS — строка-метка Y-STAMP:, «класс
          экспозиции», CAM-коды, corridor-токен (закон непрозы: метка не
          рисуется);
      (2) паттерн карты не вплетён (стемы паттерна в лучшей строке <
          minWeaveStems) — «промпт оставлен на произвол судьбы»;
      (3) вплетение пересказано / чужой карты (копипаст-юнит 1:1 не найден
          подстрокой);
      (4) R+/X собран от обёртки с классом «—» (В27 ПУСТО) — В33;
      (5) исполнение отсутствует (стемы паттерна вне строки вплетения <
          minExecStems) — вплетение вместо исполнения не считается.
    WARN: (6) карта в окне ротации (глубина windowDepth); (7) corridor
    карты ≠ полю Corridor: слота.

    Эры: партия < applyFrom без --retro молчит (объявленная эра, история
    не переписывается); с --retro все находки — WARN (ретро-демонстрация
    эпохи 1.14.0: метки-паспорта в POS были легальны до T5-25).
    В33-честность: паспорт не самосертифицирует рейтинг."""
    cfg = GATES.get("yStamp") or {}
    zero = {"mode": "silent", "with_card": 0, "weaved": 0, "no_weave": 0,
            "mismatch": 0, "banned": 0, "empty_class_rplus": 0,
            "not_executed": 0, "window_hits": 0, "corridor_warn": 0}
    if not cfg:
        return zero
    applied = 0 <= batch_no >= int(cfg.get("applyFrom", 10 ** 9))
    if not applied and not retro:
        return zero
    zero["mode"] = "FAIL" if applied else "RETRO-WARN"

    def emit(entry, fail_level):
        # FAIL только в живую эру и с failFrom; ретро и до-эра — WARN
        if applied and fail_level and batch_no >= int(cfg.get("failFrom", 10 ** 9)):
            fails.append(entry)
        else:
            warns.append(entry)

    ycards = load_y_cards()
    window_map = load_prev_y_usage(
        int(cfg.get("windowDepth", 3)), exclude=str(batch_path), batch_no=batch_no
    )
    banned_res = [re.compile(p) for p in cfg.get("bannedMarkers", [])]
    min_weave = int(cfg.get("minWeaveStems", 4))
    min_exec = int(cfg.get("minExecStems", 2))
    st = dict(zero)
    st["mode"] = zero["mode"]
    for s in slots:
        # (1) обозначения в POS — ловим независимо от карты (метка без
        # Y-card тоже нарушение)
        hit = None
        for l in s.pos_lines:
            for bre in banned_res:
                m = bre.search(l)
                if m:
                    hit = (l.strip()[:72], m.group(0))
                    break
            if hit:
                break
        if hit:
            st["banned"] += 1
            emit(
                (s.sid, "y-stamp",
                 f"служебное обозначение в POS («{hit[1]}» в строке "
                 f"«{hit[0]}») — В34: обозначения в промпте не нужны, нужно "
                 "только то, что за ними имеется в виду; смысл доезжает "
                 "прозой: паттерн — вплетением 1:1, камера — камерным "
                 "кластером OPENER, коридор — физикой claim-строки; паспорт "
                 "— метаданные (Y-card в шапке, чип прилавка), LAWS §17"),
                True,
            )
        if not s.y_card:
            continue
        card = ycards.get(s.y_card)
        if not card:
            # неизвестная карта уже поймана yCardGate — не дублируем
            continue
        st["with_card"] += 1
        comp = card.get("components") or {}
        pose = comp.get("pose", "") or ""
        cls = (comp.get("exposure") or {}).get("class", "—") or "—"
        corr = card.get("corridor", "—") or "—"
        pose_stems = _card_pose_stems(card)
        pose_n = norm_ws(pose).lower()
        # (2) вплетение: ПЕРВИЧНЫЙ детектор — копипаст-юнит 1:1 подстрокой
        # (LAWS §17.2); стемы — только диагностика «пересказа» (короткие
        # паттерны стем-порог ложно роняют — урок P28/Y320)
        weave_idx = -1
        if pose_n:
            for i, l in enumerate(s.pos_lines):
                if pose_n in norm_ws(l).lower():
                    weave_idx = i
                    break
        best_hits, best_idx = 0, -1
        for i, l in enumerate(s.pos_lines):
            hits = len(pose_stems & {w[:5] for w in words(l) if len(w) >= 5})
            if hits > best_hits:
                best_hits, best_idx = hits, i
        if weave_idx < 0 and best_hits < min_weave:
            st["no_weave"] += 1
            emit(
                (s.sid, "y-stamp",
                 f"паттерн карты {s.y_card} не вплетён в POS ({best_hits} "
                 f"стемов в лучшей строке, нужно ≥{min_weave}; копипаста 1:1 "
                 f"нет) — В34: не оставляй промпт на произвол судьбы; строка "
                 f"3 = паттерн карты копипастом 1:1 (LAWS §17.1; начало: "
                 f"«{norm_ws(pose)[:70]}…»)"),
                True,
            )
        elif weave_idx < 0:
            st["mismatch"] += 1
            emit(
                (s.sid, "y-stamp",
                 f"вплетение {s.y_card} пересказано — копипаст-юнит 1:1 из "
                 "camera.json не найден в POS подстрокой (LAWS §17.2); если "
                 "вшита чужая карта — сверить поле Y-card"),
                True,
            )
        else:
            st["weaved"] += 1
            # (5) исполнение вне строки вплетения
            body = " ".join(l for i, l in enumerate(s.pos_lines)
                            if i != weave_idx)
            body_stems = {w[:5] for w in words(body) if len(w) >= 5}
            hits = len(pose_stems & body_stems)
            if hits < min_exec:
                st["not_executed"] += 1
                emit(
                    (s.sid, "y-stamp",
                     f"вплетение {s.y_card} не исполняется телом POS ({hits} "
                     f"стемов паттерна вне вплетения, нужно ≥{min_exec}) — "
                     "паттерн живёт дважды: камерный кластер OPENER + строка 3 "
                     "(LAWS §17.3)"),
                    True,
                )
        # (4) В33: R+ от обёртки без класса
        if s.rating in ("R+", "X") and cls in cfg.get("rplus_banned_classes", ["—"]):
            st["empty_class_rplus"] += 1
            emit(
                (s.sid, "y-stamp",
                 f"{s.rating} собран от обёртки с классом «—» (В27 ПУСТО, "
                 f"{s.y_card}) — паспорт не самосертифицирует рейтинг (В33): "
                 "пересобрать печью или писать честный тир"),
                True,
            )
        # (6) окно ротации карт
        src_batch = window_map.get(s.y_card)
        if src_batch:
            st["window_hits"] += 1
            warns.append(
                (s.sid, "y-stamp",
                 f"карта {s.y_card} в окне ротации (использована в {src_batch}, "
                 f"окно {cfg.get('windowDepth', 3)} батчей, y_assembly.window) — "
                 "неизбежный повтор — ⚗ + объявление в чате")
            )
        # (7) corridor карты vs поле слота
        if s.corridor and corr not in ("—", "") and s.corridor != corr:
            st["corridor_warn"] += 1
            warns.append(
                (s.sid, "y-stamp",
                 f"исполнение объявило Corridor: {s.corridor}, карта "
                 f"{s.y_card} несёт corridor {corr} — свести (В31: коридор = "
                 "физика POS)")
            )
    return st


def check_combo_pose(slots, warns, batch_no=-1):
    """v1.13.0 comboPose (акт 1 вердикта T5-24, приказ автора А «всю составную
    позу — в доктрину комбо-Y»): составная поза (poses.json combo:true) обязана
    собираться в слоте от своей карты-обёртки (поле card, серия Y38+,
    camera.json 1.15.0). PL составной, а карта не в шапке / чужая карта = WARN
    (закон 8.6: WARN-старт, FAIL по вердикту). Карты-обёртки с меткой
    «В27 ПУСТО» в R+ не выходят до пересборки печью (В33-честность)."""
    cfg = GATES.get("comboPose")
    if not cfg or (0 <= batch_no < int(cfg.get("applyFrom", 10 ** 9))):
        return {"composite_used": 0, "without_card": 0, "mismatch": 0}
    cmap = load_combo_map()
    stats = {"composite_used": 0, "without_card": 0, "mismatch": 0}
    for s in slots:
        if not s.pose or s.pose not in cmap:
            continue
        stats["composite_used"] += 1
        card = cmap[s.pose]
        if not card or card in ("—", "indirect"):
            stats["without_card"] += 1
            warns.append(
                (s.sid, "combo-pose",
                 f"составная поза {s.pose} без карты-обёртки (poses.json "
                 f"card={card}) — акт 1: сборка от карты Y38+ (доктрина комбо-Y)")
            )
        elif not s.y_card:
            stats["without_card"] += 1
            warns.append(
                (s.sid, "combo-pose",
                 f"составная поза {s.pose} (карта {card}) — в шапке слота нет "
                 f"Y-card: сборка мимо комбо-доктрины (акт 1)")
            )
        elif s.y_card != card:
            stats["mismatch"] += 1
            warns.append(
                (s.sid, "combo-pose",
                 f"составная поза {s.pose} собрана от {s.y_card}, карта позы "
                 f"= {card} — привести к карте-обёртке или обновить built_from")
            )
    return stats


def check_concept_flag(slots, warns, batch_no=-1):
    """v1.12.0 conceptFlag (постмортем T5-23 §4.3 «концепт-инфляция»): концепт,
    структурно неспособный нести R+ (визитка/поклон/реверанс/витрина/приветствие),
    стопится на сборке и выносится автору с вариантами — молчаливый бейдж запрещён.
    Флаг поднимается, когда в POS есть концепт-лексема визитки (word-boundary),
    а физики заявки (physicsLexemes — свой жёсткий словарь; kinetics-теги вида
    mid_settle физикой не считаются) нет."""
    cfg = GATES.get("conceptFlag")
    if not cfg or (0 <= batch_no < int(cfg.get("applyFrom", 10 ** 9))):
        return 0
    visits = [t.lower() for t in cfg.get("visitLexemes", [])]
    phys = [t.lower() for t in cfg.get("physicsLexemes", [])]

    def lex_hit(tokens, text):
        return any(re.search(r"\b" + re.escape(t) + r"\b", text) for t in tokens)

    caught = 0
    for s in slots:
        if s.rating not in ("R+", "X"):
            continue
        pos = (s.pos or "").lower()
        is_visit = lex_hit(visits, pos)
        has_phys = lex_hit(phys, pos)
        if is_visit and not has_phys:
            caught += 1
            warns.append(
                (s.sid, "concept-flag",
                 "концепт-визитка в R+ (поклон/реверанс/витрина/приветствие) — "
                 "структурно не тянет тир (постмортем T5-23: ОС-интро P01–P03): "
                 "стоп сборки — флаг автору с вариантами (понижаем тир / вшиваем "
                 "физику Y-карты / меняем концепт)")
            )
    return caught


def check_neg_dress_guards(slots, warns, batch_no=-1):
    """v1.12.0 negDressGuards (постмортем T5-23 §4.4 «NEG-войны»): в R+-слоте
    гарды одетости добивают заявку до PG-13 (46–50 юнитов NEG при слабой
    эротике POS). X-доставка — исключение (LAWS §3: блок покрытия в NEG —
    инструмент доставки X). R+ с гардом одетости — WARN."""
    cfg = GATES.get("negDressGuards")
    if not cfg or (0 <= batch_no < int(cfg.get("applyFrom", 10 ** 9))):
        return 0
    guards = [t.lower() for t in cfg.get("units", [])]
    caught = 0
    for s in slots:
        if s.rating != "R+":
            continue
        neg = (s.neg or "").lower()
        hit = [g for g in guards if g in neg]
        if hit:
            caught += 1
            warns.append(
                (s.sid, "neg-dress",
                 f"гарды одетости в R+ NEG ({', '.join(hit)}) — добивают заявку "
                 f"(постмортем §4.4): NEG R+ — не война, гарды одетости запрещены, "
                 f"кроме X-доставки")
            )
    return caught


def check_details_layer(slots, warns, batch_no=-1, oc_names=()):
    """v1.12.0 detailsGate — В32 «детали — постоянный слой» (поручение автора,
    вердикт T5-23: «я бы хотел больше деталей… серёжки, татуировочки, узоры,
    может курительная трубка, повязка на глазу.. как в основной теме, так и в
    EXP»): каждый мейн и EXP-слот несёт ≥2 фишечки-ФОРМЫ (не слов) в POS.
    Меньше — риск-флаг на сборке. ОС — вне гейта: канон несёт гэг-стек ≥3."""
    cfg = GATES.get("detailsGate")
    if not cfg or (0 <= batch_no < int(cfg.get("applyFrom", 10 ** 9))):
        return
    tokens = [t.lower() for t in cfg.get("formTokens", [])]
    need = int(cfg.get("minPerSlot", 2))
    for s in slots:
        if s.genre == "OC" or is_oc_slot(s, oc_names):
            continue
        pos = (s.pos or "").lower()
        found = sorted({t for t in tokens if t in pos})
        if len(found) < need:
            warns.append(
                (s.sid, "details",
                 f"фишечек-ФОРМ {len(found)} < {need} (В32 «детали — постоянный слой»): "
                 f"вшить ≥{need} из словаря formTokens (тату/повязка/шрам/украшения/"
                 f"предмет-подпись) — деталь читается формой в первых 12 тегах")
            )


def check_palette_skin(slots, warns, batch_no=-1, retro=False):
    """v1.16.0 paletteSkin — В36 «палитра ≠ кожа» (вердикт T5-27: P01 Vae
    «Absolute Seduction» вышла на рендере с КРАСНОЙ кожей при каноне
    obsidian — строка палитры «blood-moon red deep over obsidian skin»
    отдала цветовой токен палитры модификатором кожи, token bleed).
    Паттерн: цвет → мост (over/on/onto/across…) → кожа в окне window
    токенов. Палитра красит ПРЕДМЕТ/СВЕТ, кожа держит канон-цвет вида.
    WARN с T5-28 (8.6: не ужесточать флоры из одного вердикта).
    --retro: старые партии показывают, что гейт поймал бы (метки эпохи,
    история не переписывается)."""
    cfg = GATES.get("paletteSkin")
    if not cfg:
        return 0
    if 0 <= batch_no < int(cfg.get("applyFrom", 10 ** 9)) and not retro:
        return 0
    colors = {c.lower() for c in cfg.get("color_words", [])}
    skins = {w.lower() for w in cfg.get("skin_words", [])}
    bridges = {b.lower() for b in cfg.get("bridges", [])}
    win = int(cfg.get("window", 5))
    caught = 0
    # свой токенайзер: дефисные составные — ОДИН токен («skin-spotlit» ≠
    # «skin» — кожа в сложном слове не модифицируется цветом палитры;
    # ловим ровно урок T5-27: «red … over obsidian skin», где skin стоит
    # отдельно и цвет реально перетекает; words() для гейта не трогаем —
    # он общий для остальных проверок)
    token_re = re.compile(r"[A-Za-z0-9_'-]+")
    for s in slots:
        toks = token_re.findall(norm_ws(s.pos or "").lower())
        for i, t in enumerate(toks):
            if t not in skins:
                continue
            # смотрим НАЗАД от слова кожи: цвет … мост … кожа
            span = toks[max(0, i - win):i]
            for bi in range(len(span) - 1, -1, -1):
                if span[bi] not in bridges:
                    continue
                color_hit = next((c for c in span[:bi] if c in colors), None)
                if color_hit:
                    caught += 1
                    warns.append(
                        (s.sid, "palette-skin",
                         f"цвет палитры «{color_hit}» перетёк в модификатор кожи "
                         f"(…{color_hit} … {span[bi]} … {t}): палитра красит "
                         f"предмет/свет, НЕ кожу — кожа держит канон-цвет вида "
                         f"(В36, урок T5-27 P01: red over obsidian skin = "
                         f"красная кожа на рендере)")
                    )
                break
    return caught


# ── v1.18.0: уроки T5-29 (В39–В43) ─────────────────────────────────────
# Вердикт 2026-11-22: «Но сделай так, чтобы ты никогда нахуй больше таких
# ошибок не повторял». Все пять проверок — applyFrom 30 (FAIL-эра с T5-30;
# T5-29 и старшие задним числом не бьются, квитанции заперты; --retro
# показывает пробелы WARN-ами, прецедент yStamp/paletteSkin).


def _mains(slots, oc_names=()):
    """Мейны = не-EXP и не-OC слоты (в порядке следования в батче)."""
    return [
        s for s in slots
        if s.genre != "EXP" and not is_oc_slot(s, oc_names)
    ]


def check_volt_core(slots, warns, fails, batch_no=-1, oc_names=(), retro=False):
    """v1.18.0 voltCore — В39 «вольт-ядро + перемешивание» (вердикт T5-29,
    пункты 2 и 4). Закон 24 / NICHE.md §В всегда требовал R+×14 · R×7 —
    дрейф T5-27/28/29 молча перевернул массу в 7/14, и ни один гейт этого
    не видел: жанровые токены читались, баланс — нет. Теперь: вольт-масса
    (VOLT + EXQUISITE) ≥ voltMin, ниша 5–8, бег одного класса ≤ maxRun —
    жанровые блоки-акты («АКТ I вольт, АКТ II ниша») запрещены."""
    cfg = GATES.get("voltCore")
    if not cfg:
        return {}
    if 0 <= batch_no < int(cfg.get("applyFrom", 10 ** 9)) and not retro:
        return {}
    hard = batch_no >= int(cfg.get("failFrom", 10 ** 9))
    mains = _mains(slots, oc_names)
    seq = []
    for s in mains:
        if s.genre in ("VOLT", "EXQUISITE"):
            seq.append("HOT")
        elif s.genre == "NICHE":
            seq.append("SPICE")
        else:
            seq.append("OTHER")
    volt = seq.count("HOT")
    niche = seq.count("SPICE")
    max_run, cur, prev = 0, 0, None
    for cls in seq:
        if cls in ("HOT", "SPICE"):
            cur = cur + 1 if cls == prev else 1
            max_run = max(max_run, cur)
        else:
            cur = 0
        prev = cls
    problems = []
    if volt < int(cfg.get("voltMin", 13)):
        problems.append(
            f"вольт-масса {volt} < {cfg.get('voltMin')} (Закон 24: R+×14 · R×7 — "
            f"вольт основа, ниша приправа)")
    if niche > int(cfg.get("nicheMax", 8)):
        problems.append(
            f"ниша {niche} > {cfg.get('nicheMax')} — перевес в NICHE (вердикт "
            f"T5-29, пункт 2)")
    if niche < int(cfg.get("nicheMin", 5)):
        problems.append(
            f"ниша {niche} < {cfg.get('nicheMin')} — чудо обязано присутствовать "
            f"(density floor, NICHE.md §5)")
    if max_run > int(cfg.get("maxRun", 3)):
        problems.append(
            f"жанровый бег {max_run} подряд > {cfg.get('maxRun')} — вольт и ниша "
            f"идут ВПЕРЕМЕШКУ, не блоками (вердикт T5-29, пункт 4)")
    if problems:
        entry = (
            "BATCH", "volt-core",
            "ВОЛЬТ-ЯДРО: " + "; ".join(problems) + " (В39, вердикт T5-29)")
        (fails if hard else warns).append(entry)
    return {
        "mains": len(mains), "volt": volt, "niche": niche,
        "other": seq.count("OTHER"), "max_run": max_run,
    }


def check_exquisite_main(slots, warns, fails, batch_no=-1, oc_names=(), retro=False):
    """v1.18.0 exquisiteMain — В41 «Exquisite в основной теме» (вердикт
    T5-29, пункт 5: «где Exquisite в основной теме»). Доктрина NICHE.md §Б
    всегда говорила «1–2 слота на батч, до 4» — T5-29 сдал ноль: ультра-
    регистр жил только на ОС-тейпе. Мейны без EXQUISITE не сдаются."""
    cfg = GATES.get("exquisiteMain")
    if not cfg:
        return {}
    if 0 <= batch_no < int(cfg.get("applyFrom", 10 ** 9)) and not retro:
        return {}
    hard = batch_no >= int(cfg.get("failFrom", 10 ** 9))
    mains = _mains(slots, oc_names)
    count = sum(1 for s in mains if s.genre == "EXQUISITE")
    if count < int(cfg.get("min", 1)):
        entry = (
            "BATCH", "exquisite-main",
            f"EXQUISITE в мейнах {count} < {cfg.get('min')} — ультра-регистр "
            f"живёт не только на ОС-тейпе: 1–4 слота в мейн-массе (В41, "
            f"вердикт T5-29, пункт 5)")
        (fails if hard else warns).append(entry)
    elif count > int(cfg.get("max", 4)):
        warns.append(
            ("BATCH", "exquisite-main",
             f"EXQUISITE в мейнах {count} > {cfg.get('max')} — ультра-регистр "
             f"теряет ультра-ность (доктрина: «до 4, когда тема богата»)"))
    return {"mains": len(mains), "exquisite": count}


def check_exp_hypothesis(slots, warns, fails, batch_no=-1, retro=False):
    """v1.18.0 expHypothesis — В42 «EXP проверяет штуки, не следует теме»
    (вердикт T5-29, пункт 6). LAWS §5 всегда требовал «тема-слова батча в
    EXP не входят» — T5-29 кастовал клетки в монстров-резидентов данжа.
    Зуб: каждая EXP-клетка несёт id H-XX из specs/open-hypotheses.json в
    строке «ТЕСТ (⚗ …)»; «полка отдыхает» незаконна — заказ на кандидатов
    исполняется КАК гипотезы (кандидат-механика = H-13)."""
    cfg = GATES.get("expHypothesis")
    if not cfg:
        return {}
    if 0 <= batch_no < int(cfg.get("applyFrom", 10 ** 9)) and not retro:
        return {}
    hard = batch_no >= int(cfg.get("failFrom", 10 ** 9))
    hyp_re = re.compile(str(cfg.get("hypIdRe", r"H-\d{2}")))
    exp = [s for s in slots if s.genre == "EXP"]
    per_hyp = {}
    without = []
    for s in exp:
        body = "\n".join(s.body_lines or [])
        ids = sorted(set(hyp_re.findall(body)))
        if not ids:
            without.append(s.sid)
            entry = (
                s.sid, "exp-hypothesis",
                "EXP-клетка без переменной из полки гипотез (нет H-XX в строке "
                "ТЕСТ) — EXP проверяет штуки, а не следует теме партии; "
                "«полка отдыхает» незаконна (В42, вердикт T5-29, пункт 6)")
            (fails if hard else warns).append(entry)
        for h in ids:
            per_hyp[h] = per_hyp.get(h, 0) + 1
    for h, n in sorted(per_hyp.items()):
        if n > int(cfg.get("maxPerHyp", 2)):
            warns.append(
                ("BATCH", "exp-hypothesis",
                 f"гипотеза {h} на {n} клетках > {cfg.get('maxPerHyp')} — "
                 f"A/B-пара несёт ОДНУ переменную, не три-четыре (LAWS §5)"))
    return {
        "cells": len(exp), "with_h": len(exp) - len(without),
        "without": without, "hyps_used": sorted(per_hyp),
    }


def rating_implied(pos, cfg):
    """v1.18.0 ratingTruth — модель состава: что кадр несёт по токенам POS.

    R+   : bareClaim («nothing underneath») И (strapOnly — линии, не панели
           ИЛИ (ни одной панели на груди И handHold — транзиентный холд
           объекта руками, как у P04 «both fists' haul of the towel»)).
    R    : bareClaim / breastRead (чтение формы через что угодно) / R-токены
           (мокрая кожа по рёбрам, tan lines, голая спина, интим-геометрия
           с партнёром, ноги-демонстрация).
    PG-13: всё остальное (мидрифф/плечи/бёдра сквозь ткань/слип бретели
           платья).
    Калибровка на ground truth T5-29: 33/33 (совпали P04/P11/P18/P27) —
    docs/POSTMORTEM-T5-29.md."""
    pos_l = (pos or "").lower()
    has_bare = any(t in pos_l for t in cfg.get("bareClaim", []))
    has_read = any(t in pos_l for t in cfg.get("breastRead", []))
    has_hold = any(t in pos_l for t in cfg.get("handHold", []))
    strap_only = any(t in pos_l for t in cfg.get("strapOnly", []))
    win = int(cfg.get("window", 100))
    panel_on = False
    for p in cfg.get("panels", []):
        for m in re.finditer(r"\b" + re.escape(p) + r"\b", pos_l):
            w0, w1 = max(0, m.start() - win), min(len(pos_l), m.end() + win)
            if not any(off in pos_l[w0:w1] for off in cfg.get("offMarkers", [])):
                panel_on = True
                break
        if panel_on:
            break
    r_evidence = any(
        t in pos_l
        for toks in (cfg.get("rTokens") or {}).values()
        for t in toks
    )
    if has_bare and (strap_only or (not panel_on and has_hold)):
        return "R+"
    if has_bare or has_read or r_evidence:
        return "R"
    return "PG-13"


def check_rating_truth(slots, warns, fails, batch_no=-1, retro=False):
    """v1.18.0 ratingTruth — В43 «рейтинг = что кадр несёт» (вердикт T5-29,
    пункт 7: «Несоответствие рейтингу… Делай отладку системы которая за это
    отвечает»). Предыдущая система (corridorAudit В33 + claimPhysics В31)
    проверяла только «R+ бейдж → есть заявка и прикрытие» — и проморгала
    инфляцию: 17 ложных R+ (заявка-строка есть, а состав несёт R: панель
    ткани на груди), 12 R↔PG-13 дрейфов. Модель rating_implied() сверяет
    бейдж с составом; ложный R+ = FAIL (наследие В33), мягкий дрейф = WARN.
    X-слоты вне модели (hard-флоры §2)."""
    cfg = GATES.get("ratingTruth")
    if not cfg:
        return {}
    if 0 <= batch_no < int(cfg.get("applyFrom", 10 ** 9)) and not retro:
        return {}
    hard = batch_no >= int(cfg.get("failFrom", 10 ** 9))
    stats = {
        "checked": 0, "implied_rplus": 0, "false_rplus": 0,
        "soft_drift": 0, "table": [],
    }
    for s in slots:
        if s.rating not in ("R+", "R", "PG-13"):
            continue
        implied = rating_implied(s.pos, cfg)
        stats["checked"] += 1
        stats["table"].append(
            {"slot": s.sid, "slug": s.slug, "declared": s.rating,
             "implied": implied})
        if implied == "R+":
            stats["implied_rplus"] += 1
        if s.rating == "R+" and implied != "R+":
            stats["false_rplus"] += 1
            entry = (
                s.sid, "rating-truth",
                f"ложный R+ бейдж: состав несёт {implied} — панель ткани на "
                f"груди держит потолок R; заявка-строка не делает слот R+. "
                f"R+-доказательство: транзиентный холд объекта руками "
                f"(единственная крышка, нижний слой снят) или bare-line со "
                f"стрэпами (В43, вердикт T5-29, пункт 7)")
            (fails if hard else warns).append(entry)
        elif s.rating == "R" and implied == "PG-13":
            stats["soft_drift"] += 1
            warns.append(
                (s.sid, "rating-truth",
                 "R-бейдж не подтверждён составом (мидрифф/плечи/бёдра сквозь "
                 "ткань): вшить R-токен (слип бельевой бретели / мокрая кожа "
                 "по рёбрам / tan lines / поле голой спины / интим-геометрия) "
                 "или писать честный PG-13 (В43)"))
        elif s.rating == "PG-13" and implied != "PG-13":
            stats["soft_drift"] += 1
            warns.append(
                (s.sid, "rating-truth",
                 f"PG-13-бейдж холоднее состава (несёт {implied}): либо убрать "
                 f"токен, либо поднять бейдж (В43)"))
        elif s.rating == "R" and implied == "R+":
            stats["soft_drift"] += 1
            warns.append(
                (s.sid, "rating-truth",
                 "состав горячее заявленного R (несёт R+-доказательство): "
                 "поднять бейдж или ослабить состав (В43)"))
    return stats


def check_header(text, header, slots, fails, warns, oc_names=()):
    if GATES["header"]["ecchiKeyForbidden"]:
        for s in slots:
            if "ecchi anime style" in s.pos.lower():
                fails.append(
                    (s.sid, "ecchi-key",
                     "«ecchi anime style» в POS — ключ снят вердиктом T5-05 (2026-10-28): «ничего не делает, я проверял»")
                )
    exp_decl = re.search(r"EXP-оверлей\s*\((\d+)", header)
    exp_fact = sum(1 for s in slots if s.genre == "EXP")
    if exp_decl and int(exp_decl.group(1)) != exp_fact:
        warns.append(
            ("BATCH", "header",
             f"шапка заявляет EXP {exp_decl.group(1)}, по факту {exp_fact}")
        )
    spread = re.search(r"R\+×(\d+)\s*·\s*R×(\d+)", header)
    if spread:
        # Ревизия 2026-11-01, 1.7: фильтр по is_oc_slot, не по жанру —
        # с T5-10 жанр OC-слотов EXQUISITE и жанровый фильтр ложно считал
        # бы их мейнами.
        mains = [
            s for s in slots
            if s.genre != "EXP" and not is_oc_slot(s, oc_names)
        ]
        rplus = sum(1 for s in mains if s.rating == "R+")
        r = sum(1 for s in mains if s.rating == "R")
        if (rplus, r) != (int(spread.group(1)), int(spread.group(2))):
            warns.append(
                ("BATCH", "header",
                 f"спред шапки R+×{spread.group(1)}·R×{spread.group(2)} ≠ факт R+×{rplus}·R×{r}")
            )
    if GATES["header"]["windowStatement"] and "Окно" not in header:
        warns.append(("BATCH", "header", "в шапке нет заявления окна ротации"))


def check_header_contract(header, warns, batch_no=-1):
    """Ревизия 2026-11-01, 1.2: молчаливая пропускаемость — системный дефект.

    Почти каждая проверка шапки делала «if нет данных: return» — молча.
    Нет спреда → гейт молчит. Нет каста → молчит. Аудитовские находки
    (F5: каст 12 vs 14) ловили люди, потому что машине было «нечего
    сравнивать». Контргейт: обязательная декларация шапки отсутствует →
    WARN «декларация не найдена, проверка пропущена». Молчание шумит.

    v1.7.0 (директива роста 2026-11-01): ключ может нести applyFrom —
    для батчей с номером < applyFrom требование молчит (объявленная
    эра, урок F2 — не переписываем историю задним числом); SO-кометы
    (номер -1) вне prereg движка: короткая орбита, движка нет.
    """
    cfg = GATES.get("headerContract", {})
    if cfg.get("mode") != "warn":
        return
    for req in cfg.get("require", []):
        apply_from = req.get("applyFrom")
        if apply_from and (batch_no < 0 or batch_no < apply_from):
            # v1.7.0: объявленная эра (история не шумит); SO-кометы (-1) вне
            # prereg движка — короткая орбита, движка нет (OVERVIEW «КОМЕТА»)
            continue
        if not re.search(req["pattern"], header):
            warns.append(
                ("BATCH", "header-contract",
                 f"декларация не найдена: {req['label']} — проверка «{req['key']}» "
                 f"пропущена, шапка неполная (ревизия 2026-11-01, 1.2)")
            )


def load_moves_ledger():
    rel = (GATES.get("movesGate") or {}).get("ledger", "specs/moves-ledger.json")
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def check_moves_gate(header, warns, batch_no=-1):
    """Директива роста 2026-11-01, идея 3 («ходы должны умирать»)."""
    cfg = GATES.get("movesGate", {})
    m = re.search(r"^ХОДЫ.*$", header, re.M)
    if not m:
        return  # обязательность декларации — header-contract (с T5-10)
    block = m.group(0)
    declared = sorted(set(re.findall(r"\bM\d{2,3}\b", block)))
    try:
        ledger = load_moves_ledger()
    except Exception as e:
        warns.append(("BATCH", "moves",
                      f"реестр ходов не читается ({e}) — сверка молчит, молчание шумит"))
        return declared
    moves = {mv.get("id"): mv for mv in ledger.get("moves", [])}
    for mid in declared:
        mv = moves.get(mid)
        if mv is None:
            warns.append(("BATCH", "moves",
                          f"{mid} вне реестра ходов — ход рождается только вердиктом "
                          f"(ARS §6 / LAWS §9); сначала вердикт, потом применение"))
            continue
        if mv.get("retired"):
            warns.append(("BATCH", "moves",
                          f"{mid} в отставке ({mv.get('retired')}) — применение вне закона; "
                          f"вернуть ход может только вердикт"))
        if mv.get("standing") or not mv.get("applications"):
            continue
        nums = sorted({a["no"] for a in mv["applications"] if isinstance(a.get("no"), int)})
        if batch_no >= 1:
            # текущий батч считает своё применение из декларации шапки:
            # реестр обновляется только пост-верdict, ждать записи — значит
            # гейт молчал бы ровно на том батче, где износ уже случился
            streak = 1
            n = batch_no - 1
            while n in nums:
                streak += 1
                n -= 1
            if streak >= int(cfg.get("wearStreak", 3)):
                warns.append(("BATCH", "moves",
                              f"износ хода {mid} «{mv.get('name')}»: применён в {streak} "
                              f"сданных батчах подряд (порог {cfg.get('wearStreak')}) — "
                              f"та же смерть, только на уровне хода; лампа автору, "
                              f"отставка — только вердиктом"))
    return declared


def check_story_cards(batch_path, warns, batch_no=-1):
    """Директива роста 2026-11-01, идея 1 (story-cards, пилот T5-10).
    v1.16.0: SO-кометы (batch_no < 0) не шумят — stories.md для заказов
    вне цикла никогда не существовал, WARN был постоянным фоном."""
    cfg = GATES.get("storyCardsGate", {})
    apply_from = int(cfg.get("applyFrom", 10))
    if batch_no < 0:
        return True  # SO вне цикла story-cards
    if batch_no < apply_from:
        return False
    p = Path(batch_path)
    if not p.is_absolute():
        p = ROOT / p
    cards = p.with_suffix("") / "stories.md"
    if not cards.exists():
        try:
            shown = Path(os.path.relpath(cards, ROOT))
        except ValueError:
            shown = cards
        warns.append(("BATCH", "story-cards",
                      f"{shown} не найден — карточки историй отсутствуют, "
                      f"бюджет мысли не проверяем пост-фактум (директива роста 2026-11-01, "
                      f"идея 1; пилот — мейн-пул)"))
        return False
    return True


def load_oc_names():
    data = json.loads(
        (ROOT / GATES["posFloors"]["ocNamesRegistry"]).read_text(encoding="utf-8")
    )
    return [k for k, v in data.get("ocs", {}).items() if v.get("active", True)]


def load_race_statuses():
    data = json.loads((ROOT / "specs/races.json").read_text(encoding="utf-8"))
    return {r["id"]: r.get("status", "?") for r in data.get("races", [])}


def load_registry_ids(rel, pattern):
    data = json.loads((ROOT / rel).read_text(encoding="utf-8"))
    ids = set()

    def walk(o):
        if isinstance(o, dict):
            v = o.get("id")
            if isinstance(v, str) and re.fullmatch(pattern, v):
                ids.add(v)
            for x in o.values():
                walk(x)
        elif isinstance(o, list):
            for x in o:
                walk(x)

    walk(data)
    return ids


def batch_title(text):
    m = re.search(r'Batch T5-\d+R?:\s*«(.+?)»', text)
    if not m:
        m = re.search(r'Batch T5-\d+R?:\s*"(.+?)"', text)
    return m.group(1) if m else None


def check_claim_exists(slot, idx, fails, warns, batch_no=-1):
    """Аудит 2026-10-31, F1/рек.1: R+/X слот без лексемы заявки в POS.

    v1.3.0 (вердикт T5-08, 2026-10-31): эскалация исполнена — FAIL;
    исторические партии (номер < applyFrom) остаются в WARN-эре:
    задним числом не переписываются (урок F2).
    """
    cfg = GATES["claimGate"]
    if slot.rating not in ("R+", "X") or slot.mark:
        return
    if idx is None:
        escalated = (
            cfg["mode"] == "fail"
            and not (cfg.get("applyFrom") and batch_no < cfg["applyFrom"])
        )
        if not escalated:
            msg = (
                f"{slot.rating} без лексемы заявки в POS — тир держится только "
                f"THESIS, рендерер прозу не видит (аудит 2026-10-31, F1; WARN-эра: эскалация с T5-{cfg.get('applyFrom', '?'):02d})"
            )
            warns.append((slot.sid, "claim-exists", msg))
        else:
            msg = (
                f"{slot.rating} без лексемы заявки в POS — тир держится только "
                f"THESIS, рендерер прозу не видит (аудит 2026-10-31, F1; FAIL с T5-{cfg.get('applyFrom', '?'):02d})"
            )
            fails.append((slot.sid, "claim-exists", msg))


def check_oc_class_floor(slots, fails, warns, batch_no=-1, oc_names=()):
    """Вердикт T5-09 (2026-11-01, прилавок): OC-промпты — класс EXQUISITE не ниже.

    «Единственное, я бы хотел чтобы ОС промпты были класса Exquisite, не
    меньше, чтобы они прорабатывались очень хорошо и были сильно более
    детализированные». Прямое решение автора в вердикте — FAIL сразу без
    WARN-эры (прецедент ecchi-ключа, T5-05); исторические партии
    (номер < applyFrom) не переписываются (урок F2).
    OC-слот опознаётся по тегу OC в скобках ИЛИ по имени канонной OC в
    скобках — с T5-10 класс EXQUISITE вытесняет OC-тег с первого места
    («(EXQUISITE · Sue · R+…)»). Вето автора — правкой applyFrom/mode.
    """
    cfg = GATES.get("ocClassGate", {})
    if cfg.get("mode") != "fail":
        return
    if cfg.get("applyFrom") and batch_no < cfg["applyFrom"]:
        return
    floor = cfg.get("floor", "EXQUISITE")
    for s in slots:
        if is_oc_slot(s, oc_names) and s.genre != floor:
            fails.append(
                (s.sid, "oc-class-floor",
                 f"OC-слот в классе «{s.genre}» — вердикт T5-09: класс {floor}, "
                 f"не меньше (ультра своего жанра: канон-проработка и детали)")
            )


def _char_spec_stems():
    """Словарь цветовых стемов char-spec: hair-eye-library + дополнения gates.json."""
    cfg = GATES["charSpecGate"]
    data = json.loads(
        (ROOT / cfg["hairEyeRegistry"]).read_text(encoding="utf-8")
    )
    hair = set(data.get("hair", [])) | set(cfg.get("hairColorStems", []))
    eyes = set(data.get("eyes", [])) | set(cfg.get("eyeColorStems", []))
    return hair, eyes


def _stem_alt(stems):
    return "|".join(
        re.escape(s) for s in sorted(stems, key=len, reverse=True)
    )


def _token_has_stem(token, stems):
    t = (token or "").lower()
    return any(s in t for s in stems)


def check_char_spec(slots, fails, warns, batch_no=-1):
    """Директива автора 2026-11-01 (рендер Hana для закрепления, чат):
    «ВЕЗДЕ должно быть указано ВСЁ о персонаже… палитра это епта не
    паннацея, всё надо указывать в позитиве, каждую рисуемую мелочь».

    Гейт char-spec: POS каждого слота несёт идентичность ЯВНО — цвет волос,
    цвет глаз, кожу, тело (список require в gates.json — вето автора правкой
    списка). Пропущенный параметр = импровизация рендерера: урок T5-09
    P26/P31 (EXP) — POS без единого тега волос, NEG запретил только
    blonde/silver/white, рендер вывел цвет из палитры P54_ART_DECO_PLATINUM
    (platinum-silver) → незаписанный блонд, закреплённый автором как канон
    Hana (oc-canon v2.5.0). E3-развязка hair-eye-library подтверждена
    законом: палитра — настроение/свет, hair/eye — идентичность.
    Исторические партии (номер < applyFrom) — WARN-эра, задним числом не
    переписываются (урок F2). ⚗-метка НЕ освобождает: идентичность — не
    предмет эксперимента (в отличие от заявки, check_salience).
    """
    cfg = GATES["charSpecGate"]
    require = set(cfg.get("require", []))
    if not require:
        return
    hair_stems, eye_stems = _char_spec_stems()
    hair_re = re.compile(
        rf"\b(?:{_stem_alt(hair_stems)})[a-z-]*\s+(?:[a-z-]+\s+){{0,2}}hair\b",
        re.I,
    )
    # причёска без слова hair: «choppy black bob», «a choppy black bob»
    hair_style_re = re.compile(
        rf"\b(?:{_stem_alt(hair_stems)})[a-z-]*\s+(?:[a-z-]+\s+){{0,2}}"
        rf"(?:{'|'.join(cfg.get('hairStyleWords', []))})\b",
        re.I,
    )
    eye_pre_re = re.compile(
        rf"\b(?:{_stem_alt(eye_stems)})[a-z-]*\s+(?:[a-z-]+\s+){{0,1}}eyes?\b",
        re.I,
    )
    # цвет ПОСЛЕ слова глаза: «left eye red, right eye blue», face-lock
    # «anime eyes (wine-red, mood)»
    eye_post_re = re.compile(r"\beyes?\b\s*(?:\()?\s*([a-z][a-z-]*)", re.I)
    skin_re = re.compile(r"\bskin\b", re.I)
    body_re = re.compile(
        r"\b(?:build|breasts|body|figure|bust|chest|hips|waist|thighs|fullness|hourglass)\b",
        re.I,
    )
    hair_alt = cfg.get("hairAlt", [])
    skin_alt = cfg.get("skinAlt", [])
    eye_exempt = cfg.get("eyeExempt", [])
    escalated = cfg["mode"] == "fail" and not (
        cfg.get("applyFrom") and batch_no < cfg["applyFrom"]
    )
    sink = fails if escalated else warns
    era = (
        f"FAIL с T5-{cfg.get('applyFrom', '?'):02d}"
        if escalated
        else f"WARN-эра: FAIL с T5-{cfg.get('applyFrom', '?'):02d}"
    )
    for s in slots:
        low = s.pos.lower()
        missing = []
        if "hairColor" in require and not (
            hair_re.search(s.pos)
            or hair_style_re.search(s.pos)
            or any(a in low for a in hair_alt)
        ):
            missing.append("цвет волос")
        if "eyeColor" in require:
            eye_ok = bool(eye_pre_re.search(s.pos)) or any(
                _token_has_stem(m.group(1), eye_stems)
                for m in eye_post_re.finditer(s.pos)
            )
            if not eye_ok and any(a in low for a in eye_exempt):
                eye_ok = True  # глаза не видны: вуаль/повязка
            if not eye_ok:
                missing.append("цвет глаз")
        if "skin" in require and not (
            skin_re.search(s.pos) or any(a in low for a in skin_alt)
        ):
            missing.append("кожа")
        if "body" in require and not body_re.search(s.pos):
            missing.append("тело")
        if missing:
            sink.append(
                (s.sid, "char-spec",
                 f"POS без {', '.join(missing)} — параметр не задан, рендерер "
                 f"импровизирует (F-016, директива «ВЕЗДЕ ВСЁ» 2026-11-01; {era})")
            )


def check_registry(slot, registries, warns):
    """Аудит 2026-10-31, F4/рек.3: коды слота против реестров specs/*.json."""
    pairs = [
        ("палитра", registries["palettes"], [slot.palette]),
        ("поза", registries["poses"], [slot.pose]),
        ("кинетика", registries["kinetics"], slot.kinetics),
        ("носитель", registries["carriers"], slot.carriers),
    ]
    for kind, (path, ids), codes in pairs:
        for c in codes:
            if c and c not in ids:
                warns.append(
                    (slot.sid, "registry",
                     f"{kind} {c} не в реестре {path} — опечатка кода? (аудит 2026-10-31, F4)")
                )


def check_pos_floors(slots, text, oc_names, warns):
    """Аудит 2026-10-31, §8: сторона POS, которую гейты v1.1 не видели."""
    cfg = GATES["posFloors"]
    title = batch_title(text)
    # имена-омонимы обычных слов (ash/doe/rue/sol/mab) матчатся только
    # с заглавной — «ash-brown hair» и «pale ash» не имя OC (v1.2.1 прогон)
    case_names = set(cfg.get("namesCaseSensitive", []))
    for s in slots:
        if re.search(r"\bmilf\b", s.pos, re.I):
            warns.append(
                (s.sid, "pos-floors",
                 "слово milf в POS — banned everywhere (policy writer_rules)"))
        if "[intentional]" not in s.pos.lower():
            for dw in cfg["deviceWords"]:
                if re.search(rf"\b{re.escape(dw)}\b", s.pos, re.I):
                    warns.append(
                        (s.sid, "pos-floors",
                         f"приборное слово «{dw}» в POS — закон света v2: свет поведением, прибор только по [INTENTIONAL] (T5-06)"))
        for nm in oc_names:
            if nm in case_names:
                hit = re.search(rf"\b{re.escape(nm)}\b", s.pos)
            else:
                hit = re.search(rf"\b{re.escape(nm)}\b", s.pos, re.I)
            if hit:
                warns.append(
                    (s.sid, "pos-floors",
                     f"имя OC «{nm}» в POS — имена OC никогда не в POS (LAWS §2.4)"))
        for ip in cfg["ipNames"]:
            if ip.lower() in s.pos.lower():
                warns.append(
                    (s.sid, "pos-floors",
                     f"IP-имя «{ip}» в POS (LAWS §6)"))
        if title and title.lower() in s.pos.lower():
            warns.append(
                (s.sid, "pos-floors",
                 f"титул темы «{title}» целиком в POS — тема живёт тегами по делу (LAWS §6)"))


def check_race_cast(header, slots, statuses, warns, fails, batch_no=-1, oc_names=(), retro=False):
    """Аудит 2026-10-31, §8: каст кинов против races.json и шапки.
    v1.18.0: policy v2.0 (В40, вердикт T5-29, пункт 3) — человек основа,
    кин опция: окно 0–10 вместо вилки 12–14; с failFrom — FAIL."""
    cfg = GATES["raceCast"]
    # Ревизия 2026-11-01, 1.7: is_oc-фильтр вместо жанрового — миграция
    # ocClassGate (T5-10: жанр OC → EXQUISITE) не разваливает каст.
    mains = [
        s for s in slots
        if s.genre != "EXP" and not is_oc_slot(s, oc_names)
    ]
    counts = Counter(
        c for s in mains for c in re.findall(r"\bR\d{2,3}\b", s.paren)
    )
    for c, n in sorted(counts.items()):
        st = statuses.get(c)
        if c in cfg["quarantine"]:
            warns.append(("BATCH", "race-cast",
                          f"{c} в карантине (races.json v2.3.0) — не назначать (в батче {n}×)"))
        elif st in (None, "?"):
            warns.append(("BATCH", "race-cast",
                          f"{c} не в реестре races.json"))
        elif st not in ("active", "gold"):
            warns.append(("BATCH", "race-cast",
                          f"{c} статус «{st}» — не назначать (в батче {n}×)"))
        if n > cfg["rfMax"]:
            warns.append(("BATCH", "race-cast",
                          f"{c} использован {n}× > RF {cfg['rfMax']}"))
    declared = re.search(r"каст\s+(\d{1,2})/(\d{1,2})", header)
    fact = sum(1 for s in mains if re.search(r"\bR\d{2,3}\b", s.paren))
    if declared and int(declared.group(1)) != fact:
        warns.append(
            ("BATCH", "race-cast",
             f"шапка заявляет каст {declared.group(1)}/{declared.group(2)}, по факту {fact} (аудит 2026-10-31, F5)"))
    # v1.18.0 raceCast policy v2.0 (В40, вердикт T5-29 п.3 «кины - опция,
    # а не основа»): человек — основа, кин — опция; окно 0–10 вместо вилки
    # 12–14. ЭРА ЧЕСТНА (прецедент yStack «задним числом не бьют — золотой
    # корпус цел»): до applyFrom свежие прогоны старых партий держат
    # ЛЕГАСИ-окно v1.8 и не дрейфуют от запертых квитанций; v2.0 включается
    # с эры 30 (FAIL с failFrom) и в --retro (видимая история).
    era = batch_no >= int(cfg.get("applyFrom", 10 ** 9))
    if era or retro:
        lo, hi = cfg["min"], cfg["max"]
        policy = (f"policy v2.0: человек — основа, кин — опция, "
                  f"В40 вердикта T5-29")
    else:
        lo, hi = 12, 14  # легаси-окно v1.8 (аудит 2026-10-31 §8)
        policy = "policy v1.8 (легаси-окно до эры В40)"
    if fact < lo or fact > hi:
        entry = (
            "BATCH", "race-cast",
            f"каст {fact}/{len(mains)} вне окна {lo}–{hi} ({policy})")
        if era and batch_no >= int(cfg.get("failFrom", 10 ** 9)):
            fails.append(entry)
        else:
            warns.append(entry)
    return {"kin": fact, "human": len(mains) - fact,
            "window": [lo, hi], "policy": "v2.0" if (era or retro) else "v1.8"}


def check_slot_format(slots, warns):
    """Аудит 2026-10-31, F3/рек.3: метки ⚗/☠ — только за закрывающей скобкой."""
    for s in slots:
        end = s.header_line.rfind(")")
        if end != -1 and any(ch in s.header_line[:end] for ch in "⚗☠"):
            warns.append(
                (s.sid, "slot-format",
                 "метка ⚗/☠ внутри скобок — конвенция: только за скобкой (F3)"))


def batch_number(path):
    m = re.search(r"T5-(\d+)", Path(path).name)
    return int(m.group(1)) if m else -1


def pos_prose(slot):
    """v1.14.0: POS без строк клейма — паспорт (Y-STAMP) не считается в
    n-граммах копипаста: считается исполнение, а не паспорт (LAWS §17.7)."""
    ys = GATES.get("yStamp") or {}
    prefix = ys.get("linePrefix", "Y-STAMP") + ":"
    exempt = bool(ys.get("stamp_exempt_ngrams", True))
    lines = [l for l in getattr(slot, "pos_lines", [])
             if l and not (exempt and l.startswith(prefix))]
    return " ".join(lines) if lines else slot.pos


def pos_grams(slots):
    grams = {}
    n = GATES["copypaste"]["ngramWords"]
    for s in slots:
        wl = words(strip_boilerplate(pos_prose(s)))
        for i in range(len(wl) - n + 1):
            g = " ".join(wl[i: i + n])
            grams.setdefault(g, set()).add(s.sid)
    return grams


def check_cross_batch(batch_path, slots, warns, canon_grams=frozenset()):
    """Аудит 2026-10-31, F6/рек.4: 6-граммы против двух предыдущих партий.

    Ревизия 2026-11-01, 1.8: канон-вербатим ОС (oc-canon.json) не шумит —
    гасится с прозрачным счётчиком (возврат (shared, canonExempt)).
    """
    cfg = GATES["crossBatch"]
    num = batch_number(batch_path)
    prevs = sorted(
        (p for _no, p in t5delivery.delivered_batches(batch_dir=ROOT / "batches")
         if p.resolve() != Path(batch_path).resolve()
         and 0 < batch_number(p) < num),
        key=lambda p: (batch_number(p), p.stat().st_mtime),
        reverse=True,
    )[: cfg["prevDepth"]]
    if not prevs:
        return [], []
    seen = {}
    for p in prevs:
        _, _, pslots = parse_batch(p)
        for g, ids in pos_grams(pslots).items():
            seen.setdefault(g, (p.name, ids))
    hits = []
    canon_exempt = []
    for g, ids in pos_grams(slots).items():
        if g in seen:
            if g in canon_grams:
                canon_exempt.append({"gram": g, "slotsHere": sorted(ids),
                                     "sourceBatch": seen[g][0]})
                continue
            hits.append((sorted(ids), g, seen[g][0], sorted(seen[g][1])))
    if hits:
        src = ", ".join(sorted({h[2] for h in hits}))
        warns.append(
            ("BATCH", "cross-copypaste",
             f"{len(hits)} общих {GATES['copypaste']['ngramWords']}-грамм с предыдущими партиями ({src}) — межбатчевый копипаст (аудит 2026-10-31, F6); детально в квитанции"))
    return [
        {"gram": g, "slotsHere": a, "sourceBatch": p, "slotsThere": b}
        for a, g, p, b in hits[: cfg["maxListed"]]
    ], canon_exempt[: cfg["maxListed"]]


def _argv_value(argv, flag):
    """v1.16.0: значение флага без IndexError — «--json» без значения = exit 2."""
    try:
        i = argv.index(flag)
    except ValueError:
        return None
    if i + 1 >= len(argv) or argv[i + 1].startswith("--"):
        print(f"gates: флаг {flag} требует значение (путь)")
        sys.exit(2)
    return argv[i + 1]


def report_md_from_receipt(receipt, batch_name):
    """2026-11-21 (двойной аудит, P0-04 «Markdown из JSON»): отчёт —
    ПРОИЗВОДНАЯ квитанции, не вторая независимая прогонка. Строит тот же
    --md-формат из JSON-квитанции: доказательство проверки не может
    показывать другую версию гейтов/вердикт, чем зафикировал JSON."""
    tool = str(receipt.get("tool", "tools/gates.py"))
    m = re.search(r"specs/gates\.json v([\d.]+)", tool)
    gver = m.group(1) if m else "?"
    fails = receipt.get("fails") or []
    warns = receipt.get("warns") or []
    verdict = receipt.get("verdict", "?")
    sha = receipt.get("sha256", "?")
    utc = receipt.get("utc", "?")
    lines = [
        f"# Машинная квитанция печи — {batch_name}",
        "",
        f"- Вердикт гейтов: **{verdict}** (FAIL {len(fails)} / WARN {len(warns)})",
        f"- sha256: `{sha}`",
        f"- Прогон: {utc} · specs/gates.json v{gver}",
        f"- Сгенерировано из JSON-квитанции (проверка №13 валидатора: MD ≡ JSON)",
        "",
        "| Слот | Слаг | Жанр | Тир | Канал | Статус | Заявка, токен | POS, слов |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for r in receipt.get("slot_table") or []:
        lines.append(
            "| {id} | {slug} | {genre} | {rating} | {channel} | {channelStatus} | {claimToken} | {posWords} |".format(**{**{
                "id": "", "slug": "", "genre": "", "rating": "", "channel": "",
                "channelStatus": "", "claimToken": "", "posWords": ""}, **r})
        )
    if fails:
        lines += ["", "## FAIL", ""]
        lines += [f"- **[{f.get('slot', '?')}]** {f.get('gate', '?')}: {f.get('msg', '')}" for f in fails]
    if warns:
        lines += ["", "## WARN", ""]
        lines += [f"- [{w.get('slot', '?')}] {w.get('gate', '?')}: {w.get('msg', '')}" for w in warns]
    return "\n".join(lines) + "\n"


def main():
    argv = sys.argv[1:]
    if len(argv) < 1 or argv[0] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0 if argv else 2)
    if argv[0] in ("-v", "--version"):
        print(f"tools/gates.py v1.18.0 · specs/gates.json v{GATES.get('version', '?')}")
        sys.exit(0)

    # 2026-11-21: отчёт ИЗ квитанции — MD не перегоняет батч заново (это
    # врало бы версией гейтов), а печатает зафикированное доказательство
    if argv[0] == "--md-from-receipt":
        if len(argv) < 2:
            print("gates: --md-from-receipt требует путь к JSON-квитанции")
            sys.exit(2)
        rp = Path(argv[1])
        if not rp.is_file():
            print(f"gates: квитанция не найдена: {rp}")
            sys.exit(2)
        receipt = json.loads(rp.read_text(encoding="utf-8"))
        batch_rel = str(receipt.get("batch", "")).strip()
        if not batch_rel:
            print("gates: в квитанции нет поля batch — не понимаю, чей отчёт")
            sys.exit(2)
        out = Path(argv[2]) if len(argv) > 2 and not argv[2].startswith("--") \
            else ROOT / (batch_rel.replace(".md", ".gate-report.md"))
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(report_md_from_receipt(receipt, Path(batch_rel).name), encoding="utf-8")
        print(f"отчёт из квитанции {rp.name}: {out}")
        sys.exit(0)

    batch_path = Path(argv[0])
    if not batch_path.is_file():
        print(f"gates: батч не найден: {batch_path}")
        sys.exit(2)
    out_json = None
    _j = _argv_value(argv, "--json")
    if _j is not None:
        out_json = Path(_j)
    out_md = None
    _m = _argv_value(argv, "--md")
    if _m is not None:
        out_md = Path(_m)

    text, header, slots = parse_batch(batch_path)
    batch_no = batch_number(batch_path)
    fails, warns = [], []
    if not slots:
        # v1.16.0: молчаливый PASS на нулевом парсинге — худший режим отказа
        # (все послотовые проверки исполнялись 0 раз; живой пример — SO-06,
        # шапка слота разорвана переносом строки внутри скобок)
        fails.append(("BATCH", "parse",
                      "0 слотов распарсено — формат шапки слота не совпал "
                      "(ожидается одна строка «P## — slug (мета)»); проверь "
                      "эм-тире, скобки и переносы строки (v1.16.0)"))
    ab_pairs = ab_pairs_from_header(header)
    burned = load_burned()
    channels = load_channels()
    oc_names = load_oc_names()
    race_statuses = load_race_statuses()
    canon_grams = load_canon_grams()
    reg_cfg = GATES["registry"]
    registries = {
        "palettes": (reg_cfg["palettes"],
                     load_registry_ids(reg_cfg["palettes"], r"P\d{1,3}_[A-Z0-9_]+")),
        "poses": (reg_cfg["poses"],
                  load_registry_ids(reg_cfg["poses"], r"PL\d+")),
        "kinetics": (reg_cfg["kinetics"],
                     load_registry_ids(reg_cfg["kinetics"], r"K\d{1,3}")),
        "carriers": (reg_cfg["carriers"],
                     load_registry_ids(reg_cfg["carriers"], r"CR-[A-Z]\d+")),
    }

    slot_rows = []  # fails/warns уже живут с нулевого guards-блока выше (v1.16.0)
    for s in slots:
        check_floors(s, fails, batch_no)
        check_neg_linter(s, fails, warns)
        check_neg_hygiene(s, fails, warns, batch_no, oc_names)
        check_format_gate(s, warns, batch_no)
        idx, sig = claim_token(s)
        check_salience(s, idx, sig, fails, warns)
        check_claim_exists(s, idx, fails, warns, batch_no)
        n = check_pos_budget(s, fails, warns)
        check_burn(s, burned, fails)
        check_registry(s, registries, warns)
        ch_status = ""
        if s.channel and s.channel in channels:
            ch_status = channels[s.channel]["status"]
        slot_rows.append({
            "id": s.sid, "slug": s.slug, "genre": s.genre, "rating": s.rating,
            "channel": s.channel or "", "channelStatus": ch_status,
            "corridor": s.corridor or "",
            "claimToken": idx or "—", "posWords": n,
        })
    cp_canon_exempt = check_copypaste(slots, ab_pairs, fails, warns, canon_grams)
    check_channels(slots, channels, fails, warns)
    fact_rplus = check_corridor(slots, warns, fails, batch_no)  # v1.10.0 corridorAudit; v1.13.0 В33 failFrom
    physics_caught = check_claimphysics(slots, warns, batch_no)  # v1.11.0 В31
    y_stats = check_ycards(slots, warns, batch_no, ab_pairs)  # v1.12.0 Y-first
    ystack_stats = check_ystack(slots, warns, batch_no)  # v1.17.0 Y×CLOSET STACK
    retro = "--retro" in sys.argv  # v1.14.0: ретро-режим новых гейтов (WARN)
    ystamp_stats = check_ystamp(batch_path, slots, warns, fails, batch_no, retro)  # v1.14.0 акт 2
    combo_stats = check_combo_pose(slots, warns, batch_no)  # v1.13.0 акт 1
    concept_caught = check_concept_flag(slots, warns, batch_no)  # v1.12.0
    dress_caught = check_neg_dress_guards(slots, warns, batch_no)  # v1.12.0
    check_details_layer(slots, warns, batch_no, oc_names)  # v1.12.0 В32
    palette_bleed = check_palette_skin(slots, warns, batch_no, retro)  # v1.16.0 В36
    check_header(text, header, slots, fails, warns, oc_names)
    check_header_contract(header, warns, batch_no)
    moves_declared = check_moves_gate(header, warns, batch_no)
    story_cards_ok = check_story_cards(batch_path, warns, batch_no)
    check_pos_floors(slots, text, oc_names, warns)
    race_stats = check_race_cast(header, slots, race_statuses, warns, fails, batch_no, oc_names, retro)  # v1.18.0: v2.0 + В40
    check_slot_format(slots, warns)
    check_oc_class_floor(slots, fails, warns, batch_no, oc_names)
    check_char_spec(slots, fails, warns, batch_no)
    # v1.18.0: уроки T5-29 (В39–В43) — FAIL-эра с T5-30, T5-29 и старше
    # задним числом не бьются (эра applyFrom 30); --retro показывает WARN-ами
    volt_stats = check_volt_core(slots, warns, fails, batch_no, oc_names, retro)  # В39
    exq_stats = check_exquisite_main(slots, warns, fails, batch_no, oc_names, retro)  # В41
    exp_hyp_stats = check_exp_hypothesis(slots, warns, fails, batch_no, retro)  # В42
    rating_stats = check_rating_truth(slots, warns, fails, batch_no, retro)  # В43
    cross_shared, cross_canon_exempt = check_cross_batch(
        batch_path, slots, warns, canon_grams
    )

    # v1.16.0: путь в квитанции — относительно корня репо: хук sha-замка
    # грепает "batch": "batches/..." и слепнет от абсолютных/чужих-CWD путей
    try:
        batch_rel = os.path.relpath(batch_path.resolve(), ROOT).replace(os.sep, "/")
    except ValueError:
        batch_rel = str(batch_path)
    verdict = "FAIL" if fails else "PASS"
    sha = hashlib.sha256(batch_path.read_bytes()).hexdigest()
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")

    receipt = {
        "tool": "tools/gates.py (specs/gates.json v%s)" % GATES["version"],
        "batch": batch_rel,
        "sha256": sha,
        "utc": now,
        "verdict": verdict,
        "slots": len(slots),
        "fails": [{"slot": a, "gate": b, "msg": c} for a, b, c in fails],
        "warns": [{"slot": a, "gate": b, "msg": c} for a, b, c in warns],
        "slot_table": slot_rows,
        "crossBatchShared": cross_shared,
        "crossBatchCanonExempt": cross_canon_exempt,
        "copypasteCanonExempt": cp_canon_exempt,
        "movesDeclared": moves_declared,
        "storyCards": story_cards_ok,
        "fact_label": {  # v1.10.0 corridorAudit: fact ≠ label
            "label_R+": sum(1 for s in slots if s.rating == "R+"),
            "fact_R+": fact_rplus,
        },
        "claim_physics": {  # v1.11.0 В31: самосертификация коридора
            "self_certified_Rplus": physics_caught,
        },
        "y_cards": {  # v1.12.0 Y-first: сборка слотов от Y-карт
            "used": y_stats["used"],
            "rplus_without_card": y_stats["rplus_without"],
            "pattern_misses": y_stats["pattern_misses"],
            "duplicates": y_stats["duplicates"],
        },
        "y_stack": {  # v1.17.0 Y×CLOSET STACK: одежда под класс карты
            "checked": ystack_stats["checked"],
            "stacked": ystack_stats["stacked"],
            "choked": ystack_stats["choked"],
            "canon_without_codes": ystack_stats["canon_without_codes"],
            "geometry_only": ystack_stats["geometry_only"],
        },
        "combo_pose": {  # v1.13.0 акт 1: составные позы — от карт-обёрток
            "composite_used": combo_stats["composite_used"],
            "without_card": combo_stats["without_card"],
            "card_mismatch": combo_stats["mismatch"],
        },
        "y_stamp": {  # v1.15.0 вердикт 2026-11-19: клеймо = вплетённый смысл
            "mode": ystamp_stats["mode"],
            "with_card": ystamp_stats["with_card"],
            "weaved": ystamp_stats["weaved"],
            "no_weave": ystamp_stats["no_weave"],
            "mismatch": ystamp_stats["mismatch"],
            "banned": ystamp_stats["banned"],
            "empty_class_rplus": ystamp_stats["empty_class_rplus"],
            "not_executed": ystamp_stats["not_executed"],
            "window_hits": ystamp_stats["window_hits"],
            "corridor_warn": ystamp_stats["corridor_warn"],
        },
        "buffs": {  # v1.12.0: квитанция баффа промпт-составляющей
            "concept_flagged": concept_caught,
            "neg_dress_guards": dress_caught,
        },
        "palette_skin": {  # v1.16.0 В36: палитра ≠ кожа (token bleed)
            "token_bleed": palette_bleed,
            "retro": bool(retro),
        },
        "race_cast": {  # v1.18.0 В40: кины — опция (policy v2.0, окно 0–10)
            "kin": race_stats["kin"], "human": race_stats["human"],
            "window": race_stats["window"],
            "policy": race_stats.get("policy", "v1.8"),
        },
        "volt_core": {  # v1.18.0 В39: вольт-ядро + перемешивание
            "mains": volt_stats.get("mains"),
            "volt": volt_stats.get("volt"),
            "niche": volt_stats.get("niche"),
            "max_run": volt_stats.get("max_run"),
            "retro": bool(retro),
        },
        "exquisite_main": {  # v1.18.0 В41: EXQUISITE в мейнах
            "mains": exq_stats.get("mains"),
            "exquisite": exq_stats.get("exquisite"),
            "retro": bool(retro),
        },
        "exp_hypothesis": {  # v1.18.0 В42: EXP = полка гипотез
            "cells": exp_hyp_stats.get("cells"),
            "with_h": exp_hyp_stats.get("with_h"),
            "without": exp_hyp_stats.get("without"),
            "hyps_used": exp_hyp_stats.get("hyps_used"),
            "retro": bool(retro),
        },
        "rating_truth": {  # v1.18.0 В43: рейтинг = состав, не заявка
            "checked": rating_stats.get("checked"),
            "implied_rplus": rating_stats.get("implied_rplus"),
            "false_rplus": rating_stats.get("false_rplus"),
            "soft_drift": rating_stats.get("soft_drift"),
            "retro": bool(retro),
        },
    }
    print(f"=== ГЕЙТЫ {batch_path} ===")
    print(f"слотов: {len(slots)} · sha256: {sha[:12]}…")
    print(f"ВЕРДИКТ: {verdict} · FAIL: {len(fails)} · WARN: {len(warns)}")
    if GATES.get("corridorAudit") and (batch_no >= int(GATES["corridorAudit"].get("applyFrom", 10 ** 9))):
        fl = receipt["fact_label"]
        # Фикс 2026-11-23 (внешний аудит, баг №3): «В33: FAIL» при живом
        # вердикте PASS выглядел противоречием — это МЕТКА ЭРЫ, не результат;
        # теперь печатается честно: «режим: FAIL-эра»
        honesty = (
            " · В33: режим FAIL-эра"
            if batch_no >= int(GATES["corridorAudit"].get("failFrom", 10 ** 9))
            else " · В33: WARN-старт"
        )
        print(
            f"fact/label: fact_R+ {fl['fact_R+']} · label_R+ {fl['label_R+']}"
            f" · ложные бейджи {fl['label_R+'] - fl['fact_R+']}{honesty}"
        )
    if GATES.get("comboPose") and (batch_no >= int(GATES["comboPose"].get("applyFrom", 10 ** 9))):
        cp = receipt["combo_pose"]
        print(
            f"comboPose: составных использовано {cp['composite_used']}"
            f" · без карты {cp['without_card']} · чужая карта {cp['card_mismatch']}"
        )
    if GATES.get("yCards") and (batch_no >= int(GATES["yCards"].get("applyFrom", 10 ** 9))):
        y = receipt["y_cards"]
        used_sorted = ", ".join(sorted(set(y["used"]), key=lambda x: int(x[1:]))) or "—"
        print(
            f"Y-first: карт {len(y['used'])} ({used_sorted}) · R+ без карты "
            f"{y['rplus_without_card']} · паттерн не доехал {y['pattern_misses']}"
            f" · дублей {y['duplicates']}"
        )
    if GATES.get("yStamp") and (
        batch_no >= int(GATES["yStamp"].get("applyFrom", 10 ** 9)) or retro
    ):
        ys = receipt["y_stamp"]
        # Фикс 2026-11-23 (внешний аудит, баг №3): «Y-STAMP [FAIL]» при PASS —
        # метка эры, не результат проверки; честная печать — «режим: FAIL-эра»
        era = ("FAIL-эра" if ys["mode"] == "FAIL"
               else "ретро-WARN" if ys["mode"] == "RETRO-WARN" else ys["mode"])
        print(
            f"Y-STAMP (режим: {era}): слотов с картой {ys['with_card']} · "
            f"вплетено 1:1 {ys['weaved']} · не вплетено {ys['no_weave']} · "
            f"пересказов {ys['mismatch']} · меток в POS {ys['banned']} · "
            f"R+ от «—» {ys['empty_class_rplus']} · "
            f"не исполнено телом POS {ys['not_executed']} · "
            f"в окне ротации {ys['window_hits']} · "
            f"corridor-разносов {ys['corridor_warn']}"
        )
    if GATES.get("paletteSkin") and (
        batch_no >= int(GATES["paletteSkin"].get("applyFrom", 10 ** 9)) or retro
    ):
        print(
            f"paletteSkin [В36]: перетёков цвета в кожу {receipt['palette_skin']['token_bleed']} "
            f"(палитра красит предмет/свет, кожа — канон вида)"
        )
    # v1.18.0: печать урока T5-29 только в его эре (или retro)
    if GATES.get("voltCore") and (
        batch_no >= int(GATES["voltCore"].get("applyFrom", 10 ** 9)) or retro
    ) and receipt["volt_core"].get("mains") is not None:
        vc = receipt["volt_core"]
        print(
            f"voltCore [В39]: мейнов {vc['mains']} · вольт-масса {vc['volt']} · "
            f"ниша {vc['niche']} · макс бег {vc['max_run']}"
        )
    if GATES.get("exquisiteMain") and (
        batch_no >= int(GATES["exquisiteMain"].get("applyFrom", 10 ** 9)) or retro
    ) and receipt["exquisite_main"].get("mains") is not None:
        em = receipt["exquisite_main"]
        print(f"exquisiteMain [В41]: EXQUISITE в мейнах {em['exquisite']}")
    if GATES.get("expHypothesis") and (
        batch_no >= int(GATES["expHypothesis"].get("applyFrom", 10 ** 9)) or retro
    ) and receipt["exp_hypothesis"].get("cells") is not None:
        eh = receipt["exp_hypothesis"]
        print(
            f"expHypothesis [В42]: клеток {eh['cells']} · с H-XX {eh['with_h']} · "
            f"без {len(eh['without'])} · полка: {', '.join(eh['hyps_used']) or '—'}"
        )
    if GATES.get("ratingTruth") and (
        batch_no >= int(GATES["ratingTruth"].get("applyFrom", 10 ** 9)) or retro
    ) and receipt["rating_truth"].get("checked") is not None:
        rt = receipt["rating_truth"]
        print(
            f"ratingTruth [В43]: проверено {rt['checked']} · ложных R+ "
            f"{rt['false_rplus']} · мягкий дрейф {rt['soft_drift']} · "
            f"состав-R+ {rt['implied_rplus']} (рейтинг = что кадр несёт)"
        )
    if receipt["race_cast"].get("kin") is not None:
        rc = receipt["race_cast"]
        print(
            f"raceCast [В40]: кин {rc['kin']} · human {rc['human']} · "
            f"окно {rc['policy']} {rc['window'][0]}–{rc['window'][1]}"
            + (" (человек — основа)" if rc.get("policy") == "v2.0" else "")
        )
    for a, b, c in fails:
        print(f"  FAIL [{a}] {b}: {c}")
    for a, b, c in warns:
        print(f"  WARN [{a}] {b}: {c}")

    if out_json:
        out_json.parent.mkdir(parents=True, exist_ok=True)
        out_json.write_text(
            json.dumps(receipt, ensure_ascii=False, indent=1), encoding="utf-8"
        )
        print(f"квитанция: {out_json}")

    if out_md:
        out_md.parent.mkdir(parents=True, exist_ok=True)  # v1.16.0: как у --json
        lines = [
            f"# Машинная квитанция печи — {batch_path.name}",
            "",
            f"- Вердикт гейтов: **{verdict}** (FAIL {len(fails)} / WARN {len(warns)})",
            f"- sha256: `{sha}`",
            f"- Прогон: {now} · specs/gates.json v{GATES['version']}",
            "",
            "| Слот | Слаг | Жанр | Тир | Канал | Статус | Заявка, токен | POS, слов |",
            "|---|---|---|---|---|---|---|---|",
        ]
        for r in slot_rows:
            lines.append(
                "| {id} | {slug} | {genre} | {rating} | {channel} | {channelStatus} | {claimToken} | {posWords} |".format(**r)
            )
        if fails:
            lines += ["", "## FAIL", ""]
            lines += [f"- **[{a}]** {b}: {c}" for a, b, c in fails]
        if warns:
            lines += ["", "## WARN", ""]
            lines += [f"- [{a}] {b}: {c}" for a, b, c in warns]
        out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"отчёт: {out_md}")

    sys.exit(0 if verdict == "PASS" else 1)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as exc:  # v1.16.0: краш ≠ FAIL — отделяем кодом 3
        import traceback
        traceback.print_exc()
        print()
        print(f"=== ГЕЙТЫ КРАШНУЛИСЬ: {exc!r} — это баг инструмента, не FAIL батча (exit 3) ===")
        sys.exit(3)