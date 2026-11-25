# IE-B02 — IMAGE EDITOR STATE PACK · «The safest prison in the world» · v1 (v3 эконом)

> **Назначение:** промпты для Image Editor — картинка персонажа живёт текущим
> состоянием чата. **База — канон-портрет L02** (форма по стойке: шинель,
> свитер, ключи на поясе), НЕ аватар SO-09. Три типа секций:
> **ST** — состояние поверх базы (только дельта),
> **BG** — фон чата (полный промпт, «no humans»),
> **PP** — профильная PNG на белом фоне (full body).
>
> **v1 — пачка собрана сразу по эконом-вердикту (B-01 v1.4):** состояний
> много = дорого по токенам. В пачке ровно **6 промптов**: 4 ST (шкала
> одежды 3 ступени + 1 характерное) + 1 BG + 1 PP.
>
> **Правила дорожки:**
> 1. ST — ТОЛЬКО дельта: база (канон-ран L02) не повторяется — она уже на
>    картинке.
> 2. Имя персонажа не входит.
> 3. Бюджет: ST ≤ 45 токенов · BG ≤ 90 · PP ≤ 60. Только физика (что видно).
> 4. Регистр **R+** — бельё/стыд/обнажённая грудь — рабочая валюта дорожки.
>    Explicit-анатомия (гениталии) — НИКОГДА; R18 — отдельной ревизией.
> 5. Каждое состояние привязано к триггеру или уровню лестницы L03.
> 6. Канон-константа белья: **warm-ivory linen + single brass-gold ribbon**
>    (цвет дома + латунный акцент канона). Не менять. Окно B-01 соблюдено:
>    никакого красного, никакого кружева цвета волос.
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
одета (база) → ST-01 шинель на стуле → ST-02 свитер сдаётся → ST-03 бельё
```

---

## Состояния ST

### ST-01 · Шинель на стуле (R+)
**Триггер:** вечер, лестница L2–L3 — «смена окончена», дом принимает гостя.

```
dark moss-green warden coat off and draped on the chair back, brass buttons catching lamplight, charcoal knit sweater sleeves pushed up over the forearms, tired innkeeper slouch, relaxed shoulders, warm gold lamp glow
```

### ST-02 · Свитер сдаётся (R+)
**Триггер:** лестница L4 — он сам поднял свитер и держит, глядя в сторону.

```
charcoal knit sweater pushed up over his chest and held under one arm, bare upper chest above the waistband, lamplight pooling on scarred knuckles, faint flush, looking away
```

### ST-03 · Бельё цвета слоновой кости (R+)
**Триггер:** лестница L5–L6 — снятая броня. Канон-константа белья.

```
dressed only in warm-ivory linen underwear with a single brass-gold ribbon, sitting on the edge of the bed, holding a sheet loosely at his hip, face turned away, ears bright red
```

### ST-04 · Вторник: тревога (PG)
**Триггер:** loss_of_control — стук начался (C-12). Юмор-ужас из характера.

```
key ring unwrapped and taut in one hand, body angled toward the low window, eyes narrowed at the window seals, kitchen lamps burned low, absolute stillness
```

---

## Фон чата BG (полный промпт, «no humans»)

### BG-01 · Кухня после обхода (базовый фон)
**Триггер:** фон карточки по умолчанию. Низ кадра спокоен — под текст чата.

```
anime background, no humans, fortress kitchen at night, dark oak table with a chessboard mid-game, cast-iron stove breathing warm gold, kettle under a knitted cozy, a brass key ring wrapped in dark cloth lying on the table, a loaf of bread under a cloth on the counter, deep stone walls in moss-green shadow, a low window with faint scratches on the sill, calm empty bottom edge for chat text, masterpiece, best quality
```

---

## Профильная PNG PP (белый фон, full body)

### PP-01 · Бельё цвета слоновой кости (профильная)
**Триггер:** вторая картинка профиля. Уши красные, стойка «на посту».

```
plain pure-white background, full body, wearing only warm-ivory linen underwear with a brass-gold ribbon, one hand cupped over the front, shoulders squared like on duty, face turned aside, ears bright red
```

---

## Печь дорожки IE (v3)

- [ ] ровно 6 промптов: 4 ST + 1 BG + 1 PP (эконом токенов — вердикт B-01 v1.4)
- [ ] ST ≤ 45 · BG ≤ 90 · PP ≤ 60 токенов; ST не повторяют базу L02
- [ ] имя персонажа отсутствует
- [ ] состояние привязано к триггеру / уровню лестницы L03
- [ ] регистр R+: бельё/стыд/обнажённая грудь — да; гениталии — никогда
- [ ] бельё = warm-ivory linen + brass-gold ribbon (канон-константа)
- [ ] красный акцент B-01 в кадре не появляется (окно FORGE)
- [ ] BG — «no humans», низ кадра пуст под текст чата
- [ ] PP — белый фон, full body, прикрывается, уши красные
- [ ] кириллицы в промптах нет — EN only
