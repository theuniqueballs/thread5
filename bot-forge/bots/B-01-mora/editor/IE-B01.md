# IE-B01 — IMAGE EDITOR STATE PACK · «Death got laid off» · v3 (эконом)

> **Назначение:** промпты для Image Editor — картинка персонажа живёт текущим
> состоянием чата. **База — канон-портрет L02** (форма по стойке: жилет,
> рубашка, галстук), НЕ аватар SO-06. Три типа секций:
> **ST** — состояние поверх базы (только дельта),
> **BG** — фон чата (полный промпт, «no humans»),
> **PP** — профильная PNG на белом фоне (full body).
>
> **v3 — вердикт автора (v1.4):** состояний много = дорого по токенам.
> В пачке ровно **6 промптов**: 4 ST (шкала одежды 3 ступени + 1 характерное)
> + 1 BG + 1 PP.
>
> **Правила дорожки:**
> 1. ST — ТОЛЬКО дельта: база (канон-ран L02) не повторяется — она уже на
>    картинке.
> 2. Имя персонажа не входит.
> 3. Бюджет: ST ≤ 45 токенов · BG ≤ 90 · PP ≤ 60. Только физика (что видно).
> 4. Регистр **R+** — бельё/стыд/декольте — рабочая валюта дорожки.
>    Explicit-анатомия (соски, гениталии) — НИКОГДА; R18 — отдельной ревизией.
> 5. Каждое состояние привязано к триггеру или уровню лестницы L03.
> 6. Канон-константа белья: **ash-silver-grey lace + single deep-crimson
>    ribbon** (цвет её волос + красный акцент канона). Не менять.
> 7. Закон языка: промпты — EN only.

---

## Как применять

1. Определи доминирующее состояние сцены (триггер / уровень лестницы).
2. Копируй промпт кнопкой → Image Editor → примени к базовому портрету.
3. Шкала одежды накатывается по порядку (ST-01 → ST-02 → ST-03), конфликтные
   дельты не смешивать. ST-04 — отдельная ветка поверх базы.
4. Сброс к базе — заново открой базовый портрет в редакторе.
5. BG и PP — отдельные слоты: фон и профильная не смешиваются со ST.

---

## Шкала одежды — главная ось R+

```
одета (база) → ST-01 галстук/воротник → ST-02 рубашка с плеч → ST-03 бельё
```

---

## Состояния ST

### ST-01 · Галстук сдаётся (R+)
**Триггер:** вечер, лестница L2–L3 — «смена окончена», броня на первый ряд.

```
crimson necktie pulled loose hanging open, white shirt collar unbuttoned two buttons, soft cleavage in the shirt gap, tired after-shift slouch, relaxed shoulders
```

### ST-02 · Рубашка с плеч (R+)
**Триггер:** лестница L4 — она сама ослабила форму, но держит рукой.

```
white shirt slipped off both shoulders, held closed in front by one hand, black bra straps visible, bare shoulders and collarbones, faint blush, looking away
```

### ST-03 · Бельё цвета волос (R+)
**Триггер:** лестница L5–L6 — снятая броня. Канон-константа белья.

```
dressed only in ash-silver-grey lace lingerie with a single deep-crimson ribbon bow, arms crossed over her chest, face bright red from shame, eyes squeezed shut
```

### ST-04 · Зверь в шкафу (PG)
**Триггер:** loss_of_control — пылесос включили (C-15). Юмор из характера.

```
wide alarmed eyes with tiny pupils, back pressed against the kitchen counter, gripping the brass stamp in front of her chest like a shield, shoulders hunched
```

---

## Фон чата BG (полный промпт, «no humans»)

### BG-01 · Кухня после смены (базовый фон)
**Триггер:** фон карточки по умолчанию. Низ кадра спокоен — под текст чата.

```
anime background, no humans, midnight kitchen above a laundromat, milk-pale walls in blue shadow, open refrigerator door glowing warm gold across the floor tiles, a badge hanging from the fridge handle, a brass stamp lying beside a red-inked receipt on a dark oak table, folded suit vest on a chair back, thin steam from a kettle, calm empty bottom edge for chat text, masterpiece, best quality
```

---

## Профильная PNG PP (белый фон, full body)

### PP-01 · Бельё цвета волос (профильная)
**Триггер:** вторая картинка профиля. Красная как помидор, прикрывается.

```
plain pure-white background, full body, wearing only an ash-silver-grey lace bra and matching panties with a deep-crimson ribbon bow, arms crossed over her chest, one hand covering, legs pressed together, face bright red from shame, eyes shut
```

---

## Печь дорожки IE (v3)

- [ ] ровно 6 промптов: 4 ST + 1 BG + 1 PP (эконом токенов — вердикт v1.4)
- [ ] ST ≤ 45 · BG ≤ 90 · PP ≤ 60 токенов; ST не повторяют базу L02
- [ ] имя персонажа отсутствует
- [ ] состояние привязано к триггеру / уровню лестницы L03
- [ ] регистр R+: бельё/стыд/декольте — да; соски/гениталии — никогда
- [ ] бельё = ash-silver-grey lace + crimson ribbon (канон-константа)
- [ ] BG — «no humans», низ кадра пуст под текст чата
- [ ] PP — белый фон, full body, прикрывается
- [ ] кириллицы в промптах нет — EN only
