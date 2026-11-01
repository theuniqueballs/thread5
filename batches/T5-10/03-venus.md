# T5-10 — 03 VENUS: свет, заявки, каналы, референсы

Вход: MERCURY ✅. Задача: перевести движок «БЫТ ЗАКЛИНАН» в промпт-право —
свет поведением, заявки в границе 60, палитры вне окна.

## Закон света v2 — исполнение (POS без приборов)

Все источники — среда/тело/предмет: солнце сквозь щель шторы (P05),
молодое утро двора (P04), пар и внутренний глоу полки (P08, P13),
сигил-глоу коврика (P12), лунное серебро сарая (P06), чужой закат и
споры (P03), кровь-луна и wisp (P24), core-orb (P16, P25), жар печи
(P29), отражённый фарами трамвай (P07). Приборных слов в POS — 0
(pos-floors чист; палитра-фрагменты с «lamp/lantern/candle/chandelier/
bulb» переписаны цветами без приборов: paper-cream, butter-gold,
amber-bright, lacquer-red, spark-gold, warm-dim). [INTENTIONAL] не
потребовался.

## Заявки (FAIL-режим claim-exists; граница 60)

| Слот | Тир | Канал | Лексема | Токен |
|---|---|---|---|---|
| P01 | R+ | r-geometry | covered nipples | ~53 |
| P02 | R+ | r-geometry | covered nipples | ~41 |
| P03 | R+ | contact-physics | see-through | ~55 |
| P05 | R+ | r-geometry | bare chest | ~53 |
| P09 | R+ | wet-sheer-delivery | covered nipples | ~52 |
| P13 | R+ | contact-physics | covered nipples | ~36 |
| P15 | R+ | r-geometry | boyshorts | ~45 |
| P17 | R+ | r-geometry | see-through | ~47 |
| P20 | R+ | wet-sheer-delivery | wet clothes + see-through | ~50 |
| P22 | R+ | contact-physics | bare breasts | ~43 |
| P23 | R+ | r-geometry | boyshorts | ~41 |
| P24 | R+ | r-geometry | panties | ~38 |
| P25 | R+ | wet-sheer-delivery | covered nipples | ~44 |
| P26 | R+ | handbra-open-palms | (перо-предплечье = handbra) | ~14 |
| P28 | R+ | contact-physics | covered nipples | ~40 |
| P31 | R+ | contact-physics | covered nipples | ~30 |
| P33 | R+ | wet-sheer-delivery | see-through + wet clothes | ~35 |

R-слоты (P06, P08, P10, P14, P18, P19, P21, P29, P30) — без заявок,
граница 75 не задета. M07 standing: каждая заявка — вещь с формой и
положением (рельеф, ткань, предмет).

## Каналы (реестр delivery-stats v0.8; все live)

r-geometry ×7 (P01, P02, P05, P15, P17, P23, P24) · contact-physics ×5
(P03, P13, P22, P28, P31) · wet-sheer-delivery ×4 (P09, P20, P25, P33) ·
handbra-open-palms ×1 (P26). Кандидаты ☠ 0/2; pantyline 0. Окно-агрегат
каналов — не запрет (прецедент T5-09: вращение по M13).

## Референсы темы (как живут в кадре, LAWS §6)

- Witch-быт: метла-транспорт (P07, P19), метла-работник (P06), котёл-
  память (P18), чайник-будильник (P08), гримуар-учебник (P15, P22),
  sigil-коврик (P12), лунная вода (P10), луна-бельё (P24).
- Modern life: трамвайная платформа (P07), рынок у моста (P11), почта
  и счета (P12), холодильник (P13), пылесос (P23), прачечная (P20),
  площадь-бускинг (P30), библиотека (P31), бассейн (P33).
- Никогда: IP-фразы и имена франшиз; «no man's sky» в POS отсутствует
  (gates v1.7.1).

## Уроки рендера, вшитые в POS (RENDERER_FACTS)

- Рельефы, не цвет: заявки через «reliefs» (P01, P02, P09, P13, P25,
  P28, P31) — цвет сосков мёртв (T5-05).
- Свет НА зоне заявки в каждом R+ (закон №21): cold crosswind (P01),
  pane sheen (P02), spore glow (P03), sun gap (P05), yard cold (P09),
  shelf glow (P13), fountain brass (P15), window glint (P17), boiler
  ring (P20), window glow (P22), hallway dim (P23), moon glow (P24),
  core-orb (P25), noon sun (P26), mirror ivory (P27), window light
  (P28), oven glow (P29), ember signs (P30), cyan edge (P31),
  door-crack (P32), dawn lane (P33).
- Канон-цвета волос — в первых ~10 токенах (урок Ana v1.7.3): P01/P02/
  P03 и все EXP-кандидаты.
- image-close — диверсификация (решение автора): image-close ×11 из 33,
  остальные — scene-close ×11, echo-close ×7, frame-close ×4.
