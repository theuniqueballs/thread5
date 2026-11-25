# MOTION-B08 - анимация B-08 · hover-луп + переход двухкадровки · v1.2

> **v1.2 - синхрон под SO-15 v3 / ST-01·02 v3 (уши/волосы-фикс): тексты
> переходов не изменились - физика та же; база перехода - рендер SO-15 v3
> (кадр А), кадры Б - дельты IE-B08 v1.2. Остальное без изменений.
> v1.1 - хвост в пресетах чёрный (v2 канон), остальное без изменений.
> v1.0 - собран полным паком с рождения, под ЗАКОН БОБОВ** (вердикт
> автора 2026-11-04: ~2000 бобов ушли на один луп из-за перегруженного
> промпта на B-04). Один пресет = ОДНО движение (плюс максимум одно
> сопутствующее: дыхание). Камера стоит мёртво - push-in живёт в банке,
> по вердикту автора. Меньше движений = дешевле прогон = меньше плывуна.
> Для Sable движения «дворьиные»: хвост, уши, шарф, дыхание - никакой
> сложной хореографии.
>
> **Корневой закон B-07:** ни один пресет не описывает язык - только
> физику. Пропов в промптах нет.
>
> **Переход двухкадровки (практика B-05/B-06/B-07):** переход получил СВОЙ
> промпт - он связывает картинки воедино: SO-15 v3 (А) → ST-01 «Хвост» (Б)
> или → ST-02 «Оскал» (Б2). Кадры Б - Image Editor-дельты поверх рендера
> SO-15 v3 (IE-B08). В img2video уходят ОБЕ картинки (старт + финиш): А+Б -
> промпт «Хватка», А+Б2 - промпт «Оскал». Нейронка достраивает промежуток
> сама. Луповые пресеты ниже - заставка из ОДНОГО кадра, сюжет перехода
> они не описывают.
>
> Как работает: готовый рендер + промпт отсюда уходят вместе в
> img2video-нейронку. На выходе - короткий почти-луп: на заставке при
> наведении мышки она слегка двигается. База и анти-морф-хвост вшиты
> в каждый пресет - скопировал → вставил → запустил. Кадр SO-15 остаётся
> статичным стоп-краном: луп делается ИЗ рендера, а не вместо него.
>
> **Хвост и уши в видео:** фирменная физика B-08, но хвосты и уши в
> видео-нейронках плывут так же, как жидкости: пресеты «Хвост» и «Уши»
> помечены рискованными, поплыло - откат на «Дыхание».

## BASE
```
3d model, no 2d
```

## TAIL
```
seamless loop, subtle motion only, everything else stays still, no morphing, face stays consistent, no distortion, no camera shake
```

## NEG
```
morphing, warping, melting, face distortion, extra fingers, deformed hands, extra limbs, body rotation, walking, scene change, background change, zoom out, fast movement, jumping, text, watermark, logo, glitch
```

## PRESET · Хватка (переход двухкадровки, пара А+Б)
> Сюжет перехода: оскал на застукавшего → пауза между укусами → уши
> повернулись к зрителю → хвост признался первым (кадр Б). Один сюжет,
> три коротких медленных шага - исключение из закона однодвижности:
> переход не луп, сюжет и есть движение. Без «seamless loop» - переход
> не зациклен (нужен луп - добавь его из TAIL).
```
3d model, no 2d, subtle animation, she pauses mid-bite and lowers the sandwich, her wolf ears turn toward the viewer, her tail thumps against the floor twice, everything else stays still, no morphing, face stays consistent, no distortion, no camera shake
```

## PRESET · Оскал (переход двухкадровки, пара А+Б2)
> Сюжет перехода: застолье → встаёт на одно колено между зрителем и едой,
> уши прижаты, клыки голые (кадр Б2). Один сюжет, два шага. Без
> «seamless loop».
```
3d model, no 2d, subtle animation, she rises to one knee between the viewer and the food, her ears pin flat back, her fangs bare in a low snarl, everything else stays still, no morphing, face stays consistent, no distortion, no camera shake
```

## PRESET · Дыхание (луп заставки, дефолт)
> Самый дешёвый и самый безопасный: грудь дышит, всё остальное стоит.
```
3d model, no 2d, subtle idle animation, chest rises and falls with calm breathing, seamless loop, subtle motion only, everything else stays still, no morphing, face stays consistent, no distortion, no camera shake
```

## PRESET · Хвост (сигнатура, риск)
> Одно движение: чёрный хвост стучит по полу дважды - тело против всех
> зубов. Рискованно: хвосты плывут; поплыло - откат на «Дыхание».
> Рот и глаза НЕ двигаются.
```
3d model, no 2d, subtle idle animation, her fluffy black tail thumps against the floor twice, chest rises and falls with calm breathing, seamless loop, subtle motion only, everything else stays still, no morphing, face stays consistent, no distortion, no camera shake
```

## PRESET · Уши (сигнатура, риск)
> Одно движение: кончики волчьих ушей подрагивают - ловят застукавшего
> раньше лица. Рискованно: уши плывут; поплыло - откат на «Дыхание».
```
3d model, no 2d, subtle idle animation, the tips of her wolf ears twitch slightly, chest rises and falls with calm breathing, seamless loop, subtle motion only, everything else stays still, no morphing, face stays consistent, no distortion, no camera shake
```

## PRESET · Шарф (декор-наполнитель)
> Одно движение: концы тёмно-красного шарфа колышутся еле-еле. Дешёвый
> наполнитель, если хвост и уши в конкретном рендере поплыли.
```
3d model, no 2d, subtle idle animation, the loose ends of her dark red scarf sway very slightly, chest rises and falls with calm breathing, seamless loop, subtle motion only, everything else stays still, no morphing, face stays consistent, no distortion, no camera shake
```

## PRESET · Блинк (тише всех)
> Одно движение: один медленный блинк - единственное движение лица.
> Самый безопасный пресет для крупных планов.
```
3d model, no 2d, subtle idle animation, she blinks once, slowly, chest rises and falls with calm breathing, seamless loop, subtle motion only, everything else stays still, no morphing, face stays consistent, no distortion, no camera shake
```

## BANK
> Банк - для сборки своего пресета из фраз (база + выбранные движения +
> хвост). Закон бобов: выбирай 1-2 движения, камера по умолчанию мёртвая
> (push-in - только по вердикту автора).
- chest rises and falls with calm breathing | грудь дышит спокойно - сопутствующее по умолчанию
- chest rises and falls a little faster, like after a run | дыхание чаще - «догнала и жрёт»
- her fluffy black tail thumps against the floor twice | хвост стучит по полу дважды - «хвост против всех зубов» (риск)
- her tail stops mid-wag, caught by itself | хвост замирает посреди движения - «поймала себя» (риск)
- her tail curls tighter around her own legs | хвост обвивает ноги туже - «не отпущу» (риск)
- the tips of her wolf ears twitch slightly | кончики ушей подрагивают - «поймала раньше лица» (риск)
- her ears pin flat back and hold | уши прижимаются и остаются - «злость включилась» (риск)
- her ears turn toward the viewer | уши поворачиваются к зрителю - «застукали, слышит» (риск)
- the loose ends of her dark red scarf sway very slightly | концы шарфа колышутся - дешёвый наполнитель
- she lowers the sandwich and holds it still | опускает бутерброд и замирает - старт перехода «Хватка»
- she wipes her mouth with the back of her wrist | вытирает рот тыльной стороной запястья - «жор окончен» (риск: руки)
- her fangs bare once, then hide | клыки блеснут раз и спрячутся - «предупредила» (риск: рот)
- she cracks her neck once to one side | хрустит шеей один раз в бок - «разминка дворняги» (риск: шея)
- she blinks once, slowly | один медленный блинк - самое безопасное движение лица
- her flat pupils narrow slightly | плоские зрачки сужаются чуть-чуть - «прикинула выходы» (риск: глаза)
- her shoulders settle down an inch | плечи опускаются на дюйм - «первый вечер без цепей»
- she pulls the scarf knot a little tighter | подтягивает узел шарфа - «собраться» (риск: руки)
- very slow gentle camera push-in | очень медленный мягкий наезд камеры - только по вердикту автора
- camera stays completely still | камера стоит мёртво - двигается только она (дефолт)
