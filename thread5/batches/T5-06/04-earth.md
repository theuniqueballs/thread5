# T5-06 — 04 EARTH: заметка (закон света, 2026-10-28)

Поступок: авторский A/B по спавну приборов на рендерах T5-06. `bulb` в
POS P03 дала лампочку в кадре; `lamp` в NEG не спасла; авторская замена
POS на поведение («the light holding the beam line and her chest
bright») прибор убрала. Вывод: POS-слово прибора сильнее NEG-гарда.

## Сделано EARTH (поверх готового батча, без пересборки)

- POS вычищен от приборов: P03 (×1), P06 (×2), P14 (×2), P17 (×1),
  P19 (×3), P25/P26 (×1 каждая) — 10 вхождений `bulb` → поведение
  света по формуле направление → цвет → форма → на чём. Фразы:
  P03 «the light holding the beam line and her chest bright» (дословно
  авторская), P06 «the overhead light laying the seam line bright» +
  «the light on the seam and her chest line», P14 «the loft light on
  the tape crosses» + «the light on the tape and the silk line»,
  P17 «the warm light on the wet hem», P19 «the loft light catching
  the waistband line» + «ember-tip-orange accent on the loft glow» +
  «the light on the waistband and the rail», P25/P26 «the tent's
  morning glow through canvas».
- NEG-гард расширен во всех слотах: `bulb, lightbulb` после `lamp`
  (bulb в гарде отсутствовала — прошла мимо страховки).
- Закон внесён: `docs/ars/04-EARTH` § ЗАКОН СВЕТА (v2) — правило,
  формула, таблица замены, режим [INTENTIONAL]; чеклист EARTH дополнен.
- Факт амендирован: `RENDERER_FACTS.md` (гард = страховка, не лечение).
- План VENUS не тронут (понятия-источники в плане легальны; перевод в
  поведение — работа EARTH). В шапку 03-venus.md добавлена пометка о
  стыке и метке [INTENTIONAL]; опечатка «лампside» исправлена.

## Искоренение (предложение FURNACE)

Гейт-класс «приборы света в POS»: машинная проверка в gates.py по
списку bulb, lightbulb, lamp, lantern, candle, torch, chandelier,
brazier, headlamp, flashlight, sconce (+ биграммы «light fixture»,
«neon sign») на POS-строках; FAIL при попадании. Исключение — слоты с
меткой [INTENTIONAL] (список из плана VENUS). EARTH чинит текст,
FURNACE решает вопрос класса.

## Сомнения на рендер

- P25/P26: «morning glow through canvas» вместо «morning bulb» —
  проверить, что палатка читается освещённой СНАРУЖИ (контровой
  утренний), а не подвесным светом внутри.
- P19: акцент перенесён с лампы на «loft glow» — проверить, что
  ember-tip-orange читается в самом свечении, а не ищет предмет.
- P06: «overhead light» — проверить отсутствие спавна патрона/абажура
  сверху кадра (если спавн вернётся — заменить на «warm amber glow»).
