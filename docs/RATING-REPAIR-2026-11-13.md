# RATING REPAIR — факт-оракул Yodayo вшит в конвейер

Дата: 2026-11-13 · Источник: аплоад автора «T5-YODAYO-RATING-REPAIR-MERGED»
(Cole/Grok merged, 2026-11-12, вербатим ниже) · Применено вместе с
docs/POSE-RAZBOR-2026-11-13.md и уроками В16/В22/В24 (вердикты T5-17/T5-19).

## Что применено машинно (scribe-маппинг гайда на реестры)

| Гайд | Куда легло | Версия |
|---|---|---|
| §1 коридоры A/B, fact ≠ label | specs/poses.json — поле `corridor` (A/B/A+B/SUPPORT/NICHE/UNKNOWN) на все 501 карт; honesty_rule | 1.12.0 |
| §2.1–2.3 фильтр поз | specs/poses.json — поле `rating_trust` (HIGH/MID/LOW/PENDING/UNKNOWN): HIGH-геометрия = LOW для высокого тира (§4.9); автор-пики и X1 = HIGH; X5 = PENDING до вердикта T5-20 | 1.12.0 |
| §2.4 Y-комбо | specs/camera.json — секция `y_cards` Y1–Y8 (паттерны, не эссе) + avoid-список «fake high tier» | 1.8.0 |
| §4 учёт badge ≠ fact, §5 один токен, §6 квоты, §7 EXP | specs/rating-recipes.json — `fact_label_policy`: fact aim 6–14, label ≈ fact, sheer ≤25% высокотирных, плоский eye-level cowboy без коридора ≤7/21 мейков (общий D4-кап 2026-11-05 НЕ возвращён), five_line отчёт | 1.10.0 |
| §12 чеклист писца → гейт | specs/gates.json + tools/gates.py — `corridorAudit` v1.10.0: R+ без `Corridor: A|B|A+B` = WARN (закон 8.6: WARN-старт, FAIL по вердикту); счётчик fact/label в квитанции | gates 1.10.0 |
| §3 VOLT 7 шагов, §8 SOL, §9 quality, §10 петля | specs/rating-recipes.json (`volt_order`, `one_token_rule`, `five_line_report`) + LIVING-NOTES 2026-11-13 | 1.10.0 |
| §11 «не делать» | Без изменений по существу: ARS без новых планет, флооры (anti-loli, IP-имена, X=0) не тронуты, канон-локи на месте | — |

Применено к сданному батчу ДО рендера (FURNACE не прогнан — правка бесплатна):
batches/T5-20.md — `Corridor:` в каждом R+; P01/P03 вшит коридор A (объект у груди);
P05, P07, P17, P19, P22, P24 понижены до честного R (нулевой коридор); HEAT
пересчитан R+×19 · R×12 · PG-13×2 (заодно исправлен ариф-баг «R+×26» при 25
бейджах). Гейты: PASS 0F, fact 19 = label 19, ложные бейджи 0.

## Сверка с оракулом автора (чат 2026-11-13, вербатим задачи)

Настоящий высокий тир обычно только если: (A) сильное раскрытие тела + грудь закрыта
объектом (руки/лента/ткань в руках), ИЛИ (B) сама поза+камера несут интим (низкий
ракурс, straddle, mid-action с одеждой). Мягкий see-through + cowboy + smile → чаще
R, иногда с ложным бейджем R+. Считать fact_R+ (в кадре есть A или B), не label_R+
(иконка/шапка). Гайд Cole/Grok этому оракулу подчинён полностью; расхождений нет.

---

## ВЕРБАТИМ ИСТОЧНИКА (аплоад автора, без правок)

# THREAD 5 — YODAYO RATING REPAIR (MERGED)
### Practical guide: poses · VOLT assembly · accounting · quotas
**Audience:** scribe / ARS · PixAI–Tsubaki / Yodayo rating behavior
**Tone:** technical · non-graphic · filter-safe wording
**Sources:** Stages 01–03 compressed and rephrased · 2026-11-12

---

## 0. Problem (plain)

On Yodayo, a slot labeled **R+** often does **not** read as R+ in the image.

What tends to land as a real high tier:
- strong **body exposure** with a clear **covering object** at the chest (hands, tape, held cloth), or
- a clearly **intimate pose + camera** (geometry and angle do the work).

What often stays **R** (sometimes with an R+ badge anyway):
- soft see-through fabric only,
- catalog standing pose + smile,
- rating only in the slot title.

**Goal:** increase *fact* high-tier frames, not badge count.
**Detail tags** (`absurdres`, `intricate details`) helped — keep them.

---

## 1. Two working corridors

| Corridor | Idea | Trust for high tier |
|---|---|---|
| **A · Cover object** | High exposure + chest covered by hands / tape / held cloth | High when explicit in tags |
| **B · Pose geometry** | Pose + camera angle carry intimacy (low angle, straddle, mid-action garment) | Mid–high |
| **A+B** | Both | Best for "super R+" EXP |
| **Neither** | Pretty scene only | Plan as **R** or PG-13 — do not label R+ |

Soft "outline under cloth" without a cover object and without hard geometry → plan **R**.

---

## 2. Pose library hygiene

### 2.1 Fields to add on each pose

```
id / name
corridor: A | B | A+B | SUPPORT | NICHE
rating_trust: HIGH | MID | LOW | UNKNOWN
camera_default: distance × angle
pool: VOLT | NICHE | EXQ | EXP
anti: what kills the read
```

### 2.2 Filter old poses

**LOW (do not aim high tier without a stronger combo)**
- straight standing, arms at sides, looking at viewer
- cowboy + soft smile + named lingerie only
- wet/sheer only, no cover object, no hard pose
- wide full-body with tiny face (fine for NICHE, not for high-tier VOLT)
- formal sit, hands in lap

**MID (usable if camera/exposure upgraded)**
- strap slip mid-catch
- hip-cock at door
- over-shoulder look
- shirt lift without cover object

**HIGH (core VOLT)**
- shirt mid-lift + tape (or equivalent cover)
- hands covering chest, otherwise open torso
- towel/cloth mid-catch at chest
- low / between-knees corridor + look down (clothed edge of frame)
- straddle / settle pose where hem geometry is the claim
- one-sided waistband process + low angle

**NICHE-only**
- world/object leads the silhouette — do not force high tier on these.

### 2.3 New poses — only if they pass one gate

- [ ] Cover object at chest under high exposure? → A
- [ ] Unmistakable intimate geometry or mid-action? → B
- [ ] Default camera not plain cowboy eye-level?
- [ ] Mid-action, not "already posed still"?

If all no → SUPPORT pool only.

### 2.4 Combo unit (minimum for high tier)

```
pose × camera × exposure × pov
```

Exposure classes: `COVER` | `PROCESS` | `LINGERIE` | `CLOTHED-TIGHT` | `SHEER`
SHEER alone is weak on this platform.

**Stable combo cards (copy patterns, not essays):**

| ID | Pattern | Corridor |
|---|---|---|
| Y1 | mid-lift garment + cover at chest + upper body + slight low angle | A+B |
| Y2 | hands as cover + upper body + slight low angle | A |
| Y3 | low camera between knees + look down + hem frames torso | B |
| Y4 | cloth/towel mid-catch at chest | A |
| Y5 | straddle/settle + hem pulled by pose + claim token | B |
| Y6 | waistband process + cowboy from below | B |
| Y7 | through door gap + adjusting cover/strap | B |
| Y8 | close insert on cover gesture → optional payoff shot | A |

**Avoid as "fake high tier":**
sheer + eye-level cowboy + smile · lingerie name + formal sit · rating word with no geometry.

---

## 3. VOLT assembly (one slot, seven steps)

**Rule:** first the **charge**, then who she is, then where she is, then beauty.

1. **Pick corridor** A / B / A+B — or stop and label R.
2. **Pick a combo** (Y-card or same axes). Do not invent "just standing."
3. **Write one claim line** you could point at with a finger
   (cover object / mid-lift / low corridor / process hem).
4. **POS order:**
   `quality (incl. absurdres, intricate details) → camera → body → claim → action → rest of clothes → environment → light → face`
5. **NL:** present continuous, mid-action, mention claim + gaze; world in one short line max.
6. **NEG:** mirror the goal (if cover required, block full chest exposure; keep bad-hands; block catalog standing).
7. **Honest header:** no corridor → write **R**, not R+.

**One-minute test:** cover the environment tags with your hand.
Is the top of the prompt still charged? If not, the theme ate VOLT.

**Theme rule:** in VOLT slots, theme objects come **after** claim.
One to three anchors — not a poem in the first tokens.

---

## 4. Accounting: badge ≠ fact

Track per batch:

| Counter | Meaning |
|---|---|
| `label_R+` | slots titled or badged R+ |
| `fact_R+` | slots where corridor A or B is visible in the image |

Optimize **fact_R+**.
Ask in verdict: *which numbers were real high tier, which were badge-only?*

---

## 5. Dresser / channel tokens

A header rating is not a channel.

Every **fact R+** aim needs **one** early channel token, for example:
- tape / crosses at chest
- hands covering chest
- mid-lift / sliding waistband / slipping strap
- low corridor geometry tags
- towel mid-catch

**One** hard channel — not four stacked.
If fabric is thin, lock underlayer in POS and negative the extra under-layer garment.

Dresser token without pose×camera combo ≈ noise.

---

## 6. Quotas (sane targets on ~33 slots)

| | Suggested |
|---|---|
| fact R+ aim | ~6–14 (not 26) |
| label R+ | stay close to fact |
| honest R | solid middle of the batch |
| sheer without cover | ≤ ~25% of high-tier aims |
| plain cowboy eye-level | cap on mains (~5–7 / 21) |

Fewer real hits beat a wall of false badges.

---

## 7. EXP "super high tier"

If the order says super R+ / hard experiment:
- every EXP slot must show corridor **A or B**
- channel token present
- combo id noted
- new faces → stable camera first; extreme angle is a second variable

Rating token without pose work = order not fulfilled (even if gates PASS).

---

## 8. SOL / theme depth (short)

Shallow theme is a **spine** problem, not a rating problem.

Need: AXIS · ANTI · PROMISE · theme object on CORE slots.
VOLT still orders: claim → theme object → rest.
If PROMISE fails on most mains, fix SOL — do not spam high-tier labels.

---

## 9. Quality tags

Keep batch-wide: `absurdres`, `intricate details`.

Optional on high-tier slots only: more detail on fingers / fabric tension / cover object.
Do not expect quality tags to promote a LOW pose.

---

## 10. After each batch (five lines)

```
1) fact R+ slot numbers:
2) badge-only numbers:
3) theme ate VOLT? (yes/no + numbers)
4) EXP: corridor present? hit/miss
5) one pose/combo trust update
```

Update pose `rating_trust` and archive dead camera combos.

---

## 11. Do not

- Treat platform badge as proof
- Stack many claim tokens
- Put environment before claim in VOLT
- Label R+ with neither corridor
- Expand ARS with a new "planet" for this
- Drop anti-floor safety tags / canon rules

---

## 12. One-page checklist (scribe)

```
[ ] Corridor A or B chosen?
[ ] Combo (pose × camera × exposure) set?
[ ] Claim line early in POS?
[ ] Camera in first ~15 tokens?
[ ] NL mid-action + gaze?
[ ] Theme after claim?
[ ] One dresser channel token?
[ ] Header tier honest?
[ ] absurdres / intricate details present?
[ ] fact vs label noted after render?
```

---

## 13. File map

| Part | Content |
|---|---|
| §1–2 | Corridors, pose filter, combos |
| §3 | VOLT seven-step build |
| §4–10 | Badge≠fact, dresser, quotas, EXP, SOL, quality, loop |
| §11–12 | Limits + checklist |

**End of merged repair guide.**
Use on the next batch; adjust trust from verdicts, not from hope.

— Cole / Grok · Yodayo Rating Repair · merged filter-safe edition

---

## 14. ЭТАЛОН R+ (урок В44, вердикт T5-31, 2026-11-25)

Ground truth — вербатим автора по рендеру T5-31:

> «Эталон того, что должно быть в рейтинге R+ - 28 слот. Вот это - R+. Поза,
> где ты между ногами девчонки, она в труселях смотрит на тебя снизу и ты
> видишь очертания её.. ну, ты понял - тоже R+. Всё остальное можешь считать
> как R и PG-13. Скажем, девушка в одежде для R, но в супер-эро позе - R+
> тоже. То, как в слоте 28 - это R+. Голенькая плюс-минус, частично голенькая,
> но с прикрытыми сосочками».

**R+ = минимум покрытия + честная голая линия + супер-эро регистр.** Три
легальные формы:

| Форма | Состав | Пример |
|---|---|---|
| 1. Частично голая | прикрытие ТОЛЬКО грудной линии (лента/листва/падший лиф), остальное голое | P28 T5-31: bare underneath a single silk ribbon |
| 2. Супер-эро поза | одежда для R, но поза/состояние ткани несут регистр | мокрая камсолька с проступающими намёками (P06 T5-31) |
| 3. Взгляд снизу | позиция «между ног» / она в труселях смотрит на камеру снизу, очертания читаются | вербатим автора |

Жёсткие следствия (В43 в силе — бейдж = состав):

- Крупный СТАТИЧНЫЙ объект, steadily прижатый к груди (декантер, сеть,
  полотенце-слой, поднос) = ПАНЕЛЬ → потолок R, каким бы «смелым» ни был
  замысел. Машина ratingTruth это ещё не различает (handHold-токены), глаз
  автора — да: сборка R+ пишется сразу под эталон, без надежды на гейт.
- Транзиентный лов на пол-скольжении (полотенце поймано НА ЛЕТУ, лоза срывает
  топ ДО КОНЦА) — R+ жив.
- X=0 не трогается: прикрытые соски = прикрытие формой (лента, листья,
  падший лиф, тёмнота), голота живёт отсутствием другой одежды +
  NEG-бронью (clothing under the wrap, bra, underwear).
- Эталон-слот P28 T5-31 заморожен; каждый R+ слот новых партий собирать ПОД
  него и спрашивать: «это дороже или дешевле P28 по прикрытию?» Дешевле — R.

Калибровка машины ratingTruth отложена до послотовых меток автора по рендеру
v2 (правило §9: один рендер закон не плодит — hard-правку словарей не делаем
до второго замера).

— запись хирургии «работа над ошибками» T5-31 · verdicts/T5-31.json · урок В44
