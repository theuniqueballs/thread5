# IE-B03 — IMAGE EDITOR STATE PACK · «So.. Are you home alone?» · v2 (эконом v3)

> **Назначение:** промпты для Image Editor — картинка персонажа живёт текущим
> состоянием чата. **База — канон-портрет L02 v1.1** (танк-топ на пороге:
> сползшая лямка, серое кружево, лента; зелёная лампочка; БЕЗ дождя),
> НЕ аватар SO-10. Три типа секций: **ST** — состояние поверх базы (только
> дельта), **BG** — фон чата (полный промпт, «no humans»), **PP** —
> профильная PNG на белом фоне (full body).
>
> **v2 — ревизия по вердикту автора 2026-10-31:** дождь — лор-брейк
> (солнце жжёт землю днём, гости ходят ночью); вся пачка дерайнена;
> акцент — бледно-зелёный; бельё-константа и лента — pale-green.
>
> **v1 — эконом v3 (вердикт B-01 v1.4):** состояний много = дорого по
> токенам. В пачке ровно **6 промптов**: 4 ST + 1 BG + 1 PP.
>
> **Правила дорожки:**
> 1. ST — ТОЛЬКО дельта: база (канон-ран L02 v1.1) не повторяется — она уже
>    на картинке.
> 2. Имя персонажа не входит.
> 3. Бюджет: ST ≤ 45 токенов · BG ≤ 90 · PP ≤ 60. Только физика (что видно).
> 4. Регистр **R+** — бельё/сползшая ткань/декольте — рабочая валюта
>    дорожки. Explicit-анатомия (соски, гениталии) — НИКОГДА; R18 — отдельной
>    ревизией.
> 5. Каждое состояние привязано к триггеру или уровню лестницы L03.
> 6. Канон-константа белья: **grey lace + single pale-green bow** (цвет
>    ночи + акцент канона). Не менять. Лента в волосах — всегда.
> 7. Ось шкалы — не одежда, а ДОПУСК: от порога внутрь. Каждая ступень —
>    «на сколько её пустили».
> 8. Закон языка: промпты — EN only.

---

## Как применять

1. Определи доминирующее состояние сцены (триггер / уровень лестницы).
2. Копируй промпт кнопкой → Image Editor → примени к базовому портрету.
3. Шкала допуска накатывается по порядку (ST-01 → ST-02 → ST-03), конфликтные
   дельты не смешивать. ST-04 — отдельная ветка поверх базы.
4. Сброс к базе — заново открой базовый портрет в редакторе.
5. BG и PP — отдельные слоты: фон и профильная не смешиваются со ST.

---

## Шкала допуска — главная ось R+

```
порог (база) → ST-01 ступень крыльца → ST-02 твой футбол → ST-03 бельё, подоконник изнутри
```

---

## Состояния ST

### ST-01 · Ступень крыльца (R+)
**Триггер:** лестница L2–L3 — ночь длиннее ожидания, разговор не кончается;
ей разрешили сесть на ступеньке.

```
sitting on the doorstep step, knees pressed together, hands folded on her lap, tank top strap straightened, dust brushed from her feet, calm head tilt, unblinking patient eyes
```

### ST-02 · Одолженная футболка (R+)
**Триггер:** лестница L4 — юзер выдал сухое. Твоё на ней.

```
wearing an oversized grey t-shirt slipped off one shoulder, bare shoulder and collarbone, hem to mid-thigh, bare legs, polite soft smile, head tilted
```

### ST-03 · Бельё и подоконник (R+)
**Триггер:** лестница L5–L6 — визит декларирован. Канон-константа белья.
Она ВНУТРИ — сама ступень и есть эччи.

```
dressed only in grey lace lingerie with a single pale-green bow, sitting on the windowsill inside, foil pushed back from the window edge, hot dark night beyond the glass, knees pressed together, hands folded on her lap, soft wide smile, pale-green ribbon in her hair
```

### ST-04 · Глазок (PG)
**Триггер:** loss_of_control — она знает, что ты смотришь. Хоррор из физики.

```
extreme close-up through a peephole fisheye distortion, one huge void-black eye pressed to the lens, tight pinprick pupil, pale skin, soft smile with even white teeth, black hair strands falling across her face
```

---

## Фон чата BG (полный промпт, «no humans»)

### BG-01 · Порог изнутри (базовый фон)
**Триггер:** фон карточки по умолчанию. Низ кадра спокоен — под текст чата.

```
anime background, no humans, dark apartment hallway at night seen from inside, front door ajar with a door chain stretched across the gap, faint pale-green glow pooling on the doorstep, heat haze rising from dry asphalt outside, boarded window edges in deep shadow, calm empty bottom edge for chat text, masterpiece, best quality
```

---

## Профильная PNG PP (белый фон, full body)

### PP-01 · Бельё цвета ночи (профильная)
**Триггер:** вторая картинка профиля. Прикрывается не от стыда — из
вежливости: скрипт выучен верно, шов заметен.

```
plain pure-white background, full body, dressed only in grey lace lingerie with a single pale-green bow, one arm across her chest, other hand covering, legs pressed together, head tilted, polite soft smile, pale-green ribbon in her black hair
```

---

## Печь дорожки IE (v2, эконом v3)

- [ ] ровно 6 промптов: 4 ST + 1 BG + 1 PP (эконом токенов — вердикт v1.4)
- [ ] ST ≤ 45 · BG ≤ 90 · PP ≤ 60 токенов; ST не повторяют базу L02 v1.1
- [ ] имя персонажа отсутствует
- [ ] состояние привязано к триггеру / уровню лестницы L03
- [ ] регистр R+: бельё/сползшая ткань/декольте — да; соски/гениталии — никогда
- [ ] бельё = grey lace + pale-green bow (канон-константа); лента в волосах — всегда
- [ ] лор-лок v1.1: дождя нет — wet/rain в промптах отсутствуют; ночь печёная,
      акцент бледно-зелёный
- [ ] ось шкалы — допуск (порог → ступень → футболка → изнутри), не одежда
- [ ] BG — «no humans», низ кадра пуст под текст чата
- [ ] PP — белый фон, full body, прикрывается «из вежливости»
- [ ] кириллицы в промптах нет — EN only
