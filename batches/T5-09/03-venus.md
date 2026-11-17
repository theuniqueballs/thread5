# T5-09 — 03 VENUS: законы света, заявки, каналы, референсы

Сеанс: VENUS (2026-10-31). Вход: MERCURY ✅ (маппинг ОС, каст 12/21,
кандидаты). Задача сеанса: перевести движок в промпт-право.

## Закон света v2 — исполнение (POS без приборов)

Все источники света батча — среда/тело/город, свет = поведение:
- город: неон-росчерки фасадов (P07, P21, P30), holo-проекция (P04,
  P08), браслетный свет лифта (P11, P24), свечение вендомата (P07),
  холодный рим шахты (P01), терминальное свечение (P02), кроссворк-
  зелёный (P23);
- тело/раса: ладонь саламандры (P06), огонь-перья (P16), core-orb
  слизня (P29), свечение тыквин изнутри (везде по теме), halo-holo
  (P12, P19), перья-гирлянды (P19), змейки-пьют-неон (P30);
- предмет: бирка-имя (P07), candy-cross (P15), свеча... — нет, свечей
  нет: carved pumpkin с внутренним свечением, фитиль отсутствует как
  класс (P06: no wick and no flame but her palm).
- [INTENTIONAL] не потребовался: приборов в POS нет вовсе (гейт
  pos-floors deviceWords — 0 срабатываний; P26 «lamp» пойман машиной на
  самопрогоне и вычищен до квитанции).

## Заявки (FAIL-режим claim-exists; граница 60 — закон аудита 8.2.2)

| Слот | Тир | Канал | Лексема заявки | Токен |
|---|---|---|---|---|
| P01 Sue | R+ | r-geometry | covered nipples | 60 |
| P02 Miyu | R+ | contact-physics | covered nipples | 53 |
| P03 Ash | R+ | x-coverage-block | bare breasts | 35 |
| P05 | R+ | contact-physics | covered nipples | 37 |
| P09 | R+ | wet-sheer-delivery | wet clothes (+covered nipples) | 37 |
| P11 | R+ | contact-physics | nipple | 40 |
| P13 | R+ | wet-sheer-delivery | wet clothes (+covered nipples) | 51 |
| P15 | R+ | handbra-open-palms | bare breasts | 35 |
| P16 | R+ | contact-physics | covered nipples | 52 |
| P18 | R+ | r-geometry | see-through (+covered nipples) | 40 |
| P20 | R+ | r-geometry | boyshorts | 43 |
| P24 | R+ | tape-only | tape cross | 53 |
| P25 Морра | R+ | contact-physics | covered nipples | 60 |
| P27 Куро | R+ | r-geometry | covered nipples | 50 |
| P28 Тэн | R+ | r-geometry | bare breasts | 54 |
| P30 Глаука | R+ | contact-physics | covered nipples | 58 |
| P31 Вель | R+ | r-geometry | covered nipples | 43 |
| R-слоты (P07, P08, P10, P14, P17, P19, P21, P23, P26, P32) | R | — | заявка ≤75, у всех есть | ✓ |

R-заявки: P07 wet clothes+covered nipples · P08 bare chest · P10/P14/
P19/P21/P23 covered nipples · P17 covered nipples (мокрый обёрт) ·
P26 covered nipples · P32 covered nipples (мокрый купальник).

## Каналы (реестр delivery-stats v0.8; все live)

- wet-sheer-delivery ×2: P09 (кислотный дождь на белом нейлоне), P13
  (плеск пунша картой).
- contact-physics ×5: P02 (руки-данные без веса), P05 (шнуровка
  работает сама), P11 (пальто проигрывает хвосту), P16 (жара шёлка
  прилипила), P25 (пар прилипил фартук).
- r-geometry ×6: P01 (вертикаль+кабель), P18 (мокрая простыня =
  геометрия тела), P20 (посадка и подол), P27 (разошедшийся шёлк),
  P28 (шёлковый крест), P31 (разрез от хвоста).
- handbra-open-palms ×1: P15 (ладони врозь держат уровень лотка).
- tape-only ×1: P24 (два креста — вся заявка).
- x-coverage-block ×1: P03 (bare state удвоен + блок покрытия в NEG).
- Кандидаты ☠: 0/2 (лимит не выбран — живых каналов достаточно).

## Референсы темы (как живут в кадре, LAWS §6)

- Night-City: мега-башни и шахты (P01, P11, P24), лобби с аквариумом
  (P17), вендоматы (P07), noodle-район за кадром, кислотный дождь и пар
  вентов (P09, P18, P23), неон-шрифты, гаснущие по одной букве (P21),
  holo-реклама и фасад-экраны (P04, P08), дроны-курьеры (P22).
- Halloween: carved pumpkins с внутренним свечением (P06, P10, P13,
  P17, P23), костюмы (медсестра P09, ангел P12, призрак P18, ведьма
  P05/P23, дэмон-маска P27), candy-экономика (P07, P15, P20, P22, P24),
  trick-or-treat как жест (P10, P21).
- Cyberware: data-cable от затылка (P01), терминальное стекло (P02),
  фантомные руки данных (P02) — без имплант-клише на телах героинь.
- Никогда: IP-имена, jack-o'-lantern, персонажи франшиз, свечи/фонари/
  факелы (закон света v2 + gates v1.3.1 ipNames).

## Уроки рендера, вшитые в POS (RENDERER_FACTS)

- Рельеф доставляется, цвет сосков сквозь ткань — мёртв (n=6 d=0):
  только reliefs, никаких цветных сосков сквозь ткань.
- R-заявки без edge-механики — самый стабильный канал: P07/P14/P17/
  P19/P21/P23/P26/P32 несут тир честной геометрией/состоянием ткани.
- Пантолайн-квота ≤2: не выбрана (0) — нижние заявки батча boyshorts
  (P20), не pantyline.
- Сигнал-пятно: wet/sheer только со светом НА зоне (P09 pink-cross
  glow, P13 string lights, P18 cold street glow, P17 tank glow).
