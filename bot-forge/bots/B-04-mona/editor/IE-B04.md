# IE-B04 - IMAGE EDITOR STATE PACK · «Her date canceled (you live across the hall)» · v1.2 (эконом v3)

> **Назначение:** промпты для Image Editor - картинка персонажа живёт текущим
> состоянием чата. **База - канон-портрет L02 v0.4** (чёрное платье, туфли
> в руке, открытая бутылка, ирэдзуми-рукав слева, тёмно-винный пучок,
> янтарные глаза, тёплый янтарь коридора), НЕ аватар SO-11. Три
> типа секций: **ST** - состояние поверх базы (только дельта), **BG** - фон
> чата (полный промпт, «no humans»), **PP** - профильная PNG на белом фоне
> (full body).
>
> **v1.2 - кадр Б (вердикт автора 2026-11-04, механика Нико):** ST-01
> перепрофилирован в **«кадр Б»** двухкадрового перехода: полный кадр
> (канон-ран + действие), продолжает рендер SO-11 (кадр А). Порядок:
> рендер SO-11 → рендер ST-01 → motion-луп из А в Б. Остальные ST -
> дельты как раньше.
>
> **v1.1 - вайбик v0.4:** винный пучок, янтарные глаза, дракон пробивается
> в ST-02/ST-04, винный пучок и рукав в PP-01.
>
> **v1 - эконом v3 (вердикт B-01 v1.4):** состояний много = дорого по
> токенам. В пачке ровно **6 промптов**: 4 ST + 1 BG + 1 PP.
>
> **Правила дорожки:**
> 1. ST - ТОЛЬКО дельта: база (канон-ран L02 v0.4) не повторяется - она уже
>    на картинке. Исключение - ST-01 «кадр Б» (полный кадр).
> 2. Имя персонажа не входит.
> 3. Бюджет: ST ≤ 45 токенов · кадр Б ≤ 90 · BG ≤ 90 · PP ≤ 60. Только
>    физика (что видно).
> 4. Регистр **R+** - бельё/сползшая ткань/декольте - рабочая валюта
>    дорожки. Explicit-анатомия (соски, гениталии) - НИКОГДА; R18 - отдельной
>    ревизией.
> 5. Каждое состояние привязано к триггеру или уровню лестницы L03.
> 6. Канон-константа белья: **black lace + single champagne-gold bow** (цвет
>    платья + акцент канона). Не менять.
> 7. Ось шкалы - МОЛНИЯ ПЛАТЬЯ: насколько «случайно» расстёгнута. Молния
>    исправна всегда - исправна в её пользу.
> 8. Закон языка: промпты - EN only.

---

## Как применять

1. Определи доминирующее состояние сцены (триггер / уровень лестницы).
2. Копируй промпт кнопкой → Image Editor → примени к базовому портрету.
3. Шкала молнии накатывается по порядку (ST-02 → ST-03 → ST-04), конфликтные
   дельты не смешивать.
4. **Кадр Б (ST-01):** рендерится ОТДЕЛЬНОЙ статикой (не через Image Editor
   поверх базы), ПОСЛЕ рендера SO-11 и ДО сборки motion-лупа. Пара
   SO-11 (А) + ST-01 (Б) уходит в img2video как стартовый + конечный кадр.
5. Сброс к базе - заново открой базовый портрет в редакторе.
6. BG и PP - отдельные слоты: фон и профильная не смешиваются со ST.

---

## Шкала молнии - главная ось R+

```
коридор (база) → ST-01 кадр Б: стол на двоих → ST-02 молния наполовину → ST-03 бельё в проёме
```

---

## Состояния ST

### ST-01 · «Кадр Б» - стол на двоих (R+ · двухкадровый переход)
**Триггер:** лестница L2 - вино у неё, стол «случайно» на двоих, свеча
делает свою работу слишком хорошо.
**Кадр Б (v0.5):** НЕ дельта - ПОЛНЫЙ кадр, продолжает кадр А (рендер
SO-11): тот же свет/палитра/канон-ран, другое действие. Она уже внутри,
коридор позади - переход «сначала она в коридоре → потом ты уже за её
столом».

```
1girl, solo, dark red hair pinned up in a loose chignon, two strands
escaping on purpose, amber eyes with faint smile lines, soft full mature
figure, elegant little black dress, one dress strap slipped off her bare
left shoulder, traditional japanese dragon and peony tattoo sleeve on her
left arm, champagne-gold drop earrings, dark red nail polish, sitting at
a small table set for two, wine glass raised, candlelight glow on her
skin, patient half-smile, warm honey-colored hallway light, upper body,
exquisite, masterpiece, best quality, absurdres, anime artstyle
```

### ST-02 · Молния наполовину (R+)
**Триггер:** лестница L3 - «помоги с молнией»; молния исправна, она просто
стоит спиной и ждёт, сколько это займёт.

```
dress zipper half open down the spine, bare back, black lace bra strap line, looking back over her shoulder, hair pinned up off her neck, the dragon head of her sleeve tattoo peeking past her shoulder blade, expectant eyes
```

### ST-03 · Бельё в проёме (R+)
**Триггер:** лестница L4-L5 - признание без слов; канон-константа белья.
Она в проёме СВОЕЙ двери - сама дверь и есть эччи.

```
dressed only in black lace lingerie with a single champagne-gold bow, standing in her open doorway, one shoulder against the frame, arms loosely crossed under her chest, bare feet, slow half-smile
```

### ST-04 · Третий бокал (R+)
**Триггер:** loss_of_control - маска съехала: реплики короче, дистанции
нет, вес ведёт корпус.

```
cheeks faintly flushed, chignon loose and messy, dress pooled off both shoulders at her elbows, black lace bra visible, the dragon and peony tattoo sleeve fully on display, wine glass loose in her fingers, slow crooked smile, swaying slightly
```

---

## Фон чата BG (полный промпт, «no humans»)

### BG-01 · Коридор на двоих (базовый фон)
**Триггер:** фон карточки по умолчанию. Низ кадра спокоен - под текст чата.

```
anime background, no humans, narrow apartment hallway at night facing two doors across from each other, warm honey-colored wall light, one door ajar with golden light spilling onto the carpet, high heels left by a shoe rack, open wine bottle on the floor by the wall, soft warm shadows, calm empty bottom edge for chat text, masterpiece, best quality
```

---

## Профильная PNG PP (белый фон, full body)

### PP-01 · Бельё и бокал (профильная)
**Триггер:** вторая картинка профиля. Прикрывается нарочито - скромность
как формальность: бокал в руке важнее руки.

```
plain pure-white background, full body, dressed only in black lace lingerie with a single champagne-gold bow, one arm draped over her chest, wine glass in the other hand, hip cocked, bare feet, amused half-smile, loose wine-dark chignon, traditional dragon and peony tattoo sleeve fully visible on her left arm
```

---

## Печь дорожки IE (v1.2, эконом v3)

- [ ] ровно 6 промптов: 4 ST + 1 BG + 1 PP (эконом токенов - вердикт v1.4)
- [ ] ST ≤ 45 · кадр Б ≤ 90 · BG ≤ 90 · PP ≤ 60 токенов; ST-02/03/04 не
      повторяют базу L02 v0.4
- [ ] ST-01 = кадр Б: полный кадр, канон-ран verbatim, продолжает кадр А
      (тот же свет/палитра/плечо слева); рендерится отдельно ДО сборки лупа
- [ ] имя персонажа отсутствует
- [ ] состояние привязано к триггеру / уровню лестницы L03
- [ ] регистр R+: бельё/сползшая ткань/декольте - да; соски/гениталии - никогда
- [ ] бельё = black lace + champagne-gold bow (канон-константа)
- [ ] ось шкалы - молния платья (стол на двоих → молния → бельё), не «стриптиз»
- [ ] ирэдзуми-рукав (слева) живёт во всех состояниях, где видно тело; дракон
      не переезжает на правую руку и на платье
- [ ] BG - «no humans», низ кадра пуст под текст чата
- [ ] PP - белый фон, full body, прикрывается «формально»
- [ ] em dash нет - только простой дефис
- [ ] кириллицы в промптах нет - EN only
