# T5-09 — 02 MERCURY: канон, каст, кандидаты

Сеанс: MERCURY (2026-10-31). Вход: SOL ✅ (движок «город наряжается
сам», HEAT, каналы). Приказ автора «изучи ОС_канон» исполнен: канон
поднят вербатимом из specs/oc-canon.json (canon_version 2.3.0), расы —
по specs/races.json (features + note + collision).

## ОС-БЛОК: маппинг тем (по канону и элементу; промпты ОС не следуют теме батча — вердикт T5-05)

### P01 — Sue · GhostRunner (R+)
- Канон VERBATIM: platinum-white hair in twin ponytails; soft purple
  right eye (left covered by the square white medical eyepatch); a
  small neck tattoo; pale ivory; slender narrow frame; soft
  natural-set breasts. Элемент VOID, IX — The Hermit.
- Прочтение темы: вертикаль-паркур и тишина бега — Hermit-бегун на
  служебной шахте дата-башни; клинок-спутник, кабель-поводок; повязка —
  её единственный «прибор», и тот канон. Свет: cold rim light шахты.
- Канал: r-geometry (live). Заявка: covered nipples (токен 60).
- Second chance: T5-07 «Сью, но с натяжечкой» — тема подобрана под её
  регистр (distant → runner's rationed silence).

### P02 — Miyu · Ghost in the Shell (R+) — дебют в Thread 5
- Канон VERBATIM: long straight black hair, hime cut, blunt bangs, long
  sidelocks; heterochromia — left eye red, right eye blue; warm light
  tan; slim elegant body; soft natural-set breasts; sharp triangular
  anime fangs. Элемент SPIRIT — призрак буквально; оболочка = термоптик.
- Прочтение темы: костюм мерцает между видимостью и невидимостью;
  отражение в стекле опаздывает на полсекунды (призрак); данные ложатся
  на плечи руками без веса. cap_per_batch:1 гетерохромии соблюдён
  (единственная в батче).
- NEG-особенность: из базового NEG удалены black hair / blue eyes /
  heterochromia (канон); добавлены matching eyes / single eye color.
- Канал: contact-physics (live). Заявка: covered nipples (токен 53).

### P03 — Ash · True Eve (R+) — дебют в Thread 5
- Канон VERBATIM: very long ivory-white hair; a thin white veil covering
  the whole face except the mouth (VEIL-REWRITE 2026-09-23: глаза не
  описываются и не видны — в POS НЕТ anime eyes); snow-pale; slender
  body; modest neat breasts. Элемент BONE, хранительница реликвий.
- Прочтение темы: «Ева до яблока» — первое утро, жилая теплица, первая
  трава по щиколотку, нагота без стыда; monastic garments сняты темой
  (канон: different outfit per prompt); вуаль дышит с каждым выдохом.
- NEG: блок покрытия канала x-coverage-block (covered breasts, bra, top
  on, cotton habit on) + eyes visible / mouth covered.
- Канал: x-coverage-block (live). Заявка: bare breasts (токен 35).

## Расовый каст мейнов: 12/21 (policy 12–14; RF ≤2 — все семьи разные)

R02 Elf (P21, moonlit-pale, ничего на ухе) · R07 Dragon-kin (P13,
крылья-фрагменты правят крой) · R08 Serpent-kin (P14, ход для хвоста) ·
R10 Deer-folk (P10, гирлянда-обмотка; БЕЗ лаванды и щёчных чешуй —
Doe-лок чист) · R13 Merfolk-adapt (P17, мокрый обёрт) · R18 Gargoyle-kin
(P08, тяжёлое плетение по камню) · R22 Flame-salamander (P06, шёлк
не-враг-огню; гребень — не key light, отказ от него) · R26 Bee-kin (P22,
полоса и простор) · R34 Phoenix-kin (P16, шарф-топ жару прощает) ·
R36 Tanuki-kin (P11, вытачка под хвост проиграла) · R38 Vampire-kin
(P24-EXQ, аристократичный регистр, не хоррор) · R39 Nephilim-kin (P19,
спина открыта — крылья правят кроем; трогательно, не величественно).
R30 Frog-kin — карантин, не назначен. Fox/drooping — Sol-лок, в батче
нет fox-семьи вовсе. Collision_table чиста.
Люди (9): P04, P05, P07, P09, P12, P15, P18, P20, P23.

## EXP-кандидаты (9; расы свежие, не из EXP T5-07/T5-08; ≥3 фишечки)

| # | Код-имя | Раса | Тир | Регистр-механизм гипотезы |
|---|---|---|---|---|
| P25 | Морра | R41 Witch-kin | R+ | кабинет-автомат считает варку сам, обгоняя помешивание |
| P26 | Уль | R11 Bat-kin | R | вниз головой — ожерелье из косточек считает сезоны |
| P27 | Куро | R24 Oni-kin | R+ | настоящие рога выигрывают у бумажной маски |
| P28 | Тэн | R35 Arachne-kin | R+ | шёлк-сам-обёрт: крест её собственной работы |
| P29 | Плюм | R25 Slime-girl | PG-13 | колпак держит форму, но форму держит воля |
| P30 | Глаука | R40 Medusa-kin | R+ | змейки пьют неон, две вежливых — в золотых колпачках |
| P31 | Вель | R37 Succubus-kin | R+ | гроссбух перелистывается сам до колонки должников |
| P32 | Марра | R23 Shark-kin | R | жабры считают глотки фонтанчика один за один |
| P33 | Пава | R31 Flower-kin | PG-13 | бутон раскрывается на минуту раньше сумерек |

Фишечки (метка + предмет + регистр) — в слотах батча; код-имена в
Гипотезах. Коко (T5-08) — единственный живой сигнал, в полку не
возвращается без приказа.

## Регистры третями формой тела

student 11 (P04, P07, P10, P12, P14, P19, P21, P22, P26, P29, P33) ·
young 11 (P01, P02, P05, P08, P11, P13, P15, P17, P18, P27, P28) ·
milf-form 11 (P03, P06, P09, P16, P20, P23, P24, P25, P30, P31, P32).
Регистр подачи в POS — строением (plush/settled/hourglass vs lithe/
slight/willowy), без слова «milf» (hard-флор).
