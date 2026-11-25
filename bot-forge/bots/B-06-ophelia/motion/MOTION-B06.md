# MOTION-B06 - анимация B-06 · hover-луп + переход двухкадровки

> **v1.0 - собран досрочно по требованию автора (2026-11-06), под ЗАКОН
> БОБОВ** (вердикт автора 2026-11-04: ~2000 бобов ушли на один луп из-за
> перегруженного промпта на B-04). Один пресет = ОДНО движение (плюс
> максимум одно сопутствующее: дыхание). Камера стоит мёртво - push-in
> живёт в банке, по вердикту автора. Меньше движений = дешевле прогон =
> меньше плывуна. Для Ophelia движения специально «домашние»: пламя,
> шар, гирлянда, слёзы - никакой сложной хореографии.
>
> **v1.0 - связка перехода (практика B-05 verbatim):** переход двухкадровки
> получил СВОЙ промпт - он связывает все три картинки воедино: SO-13 (А) →
> ST-01 «Рукав» (Б) → ST-02 «Пакет» (Б2). Кадры Б - Image Editor-дельты
> поверх рендера SO-13 (IE-B06 v1.0). В img2video уходят ОБЕ картинки
> (старт + финиш): А+Б или А+Б2 - промпт «Переход» один на обе пары,
> нейронка достраивает промежуток сама. Луповые пресеты ниже - заставка
> из ОДНОГО кадра, сюжет перехода они не описывают.
>
> Как работает: готовый рендер + промпт отсюда уходят вместе в
> img2video-нейронку. На выходе - короткий почти-луп: на заставке при
> наведении мышки она слегка двигается. База и анти-морф-хвост вшиты
> в каждый пресет - скопировал → вставил → запустил. Кадр SO-13 остаётся
> статичным стоп-краном: луп делается ИЗ рендера, а не вместо него.
>
> **PG-заметка:** слёзы - сигнатура бота, но жидкости в видео-нейронках
> плывут: пресет «Слеза» помечен как рискованный, поплыло - откат на
> «Свечи».

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

## PRESET · Гость (переход двухкадровки)
> Промпт-связка: сюжет перехода целиком - увидела гостя → слёзы пролились,
> рукав к глазу (кадр Б) → обе руки протягивают пакет (кадр Б2). Три
> коротких медленных шага - исключение из закона однодвижности: переход не
> луп, сюжет и есть движение. В img2video уходит пара А+Б или А+Б2, промпт
> тот же. Без «seamless loop» - переход не зациклен (нужен луп - добавь
> его из TAIL).
```
3d model, no 2d, subtle animation, she looks toward the viewer as tears well up and spill, she presses a black lace sleeve against one eye, then holds a paper goodie bag out toward the viewer with both hands, everything else stays still, no morphing, face stays consistent, no distortion, no camera shake
```

## PRESET · Свечи (луп заставки, дефолт)
> Самый дешёвый и самый «домашний»: пламя чёрных свечей подрагивает, она
> дышит. Всё остальное стоит на месте, камера мёртвая.
```
3d model, no 2d, subtle idle animation, the candle flames flicker gently, chest rises and falls with calm breathing, seamless loop, subtle motion only, everything else stays still, no morphing, face stays consistent, no distortion, no camera shake
```

## PRESET · Шар (сигнатура палитры)
> Одно движение: бледно-розовый шар среди чёрных чуть колышется -
> «пастельная контрабанда живёт». Глаза и улыбка НЕ двигаются.
```
3d model, no 2d, subtle idle animation, the pale pink balloon among the black ones sways slightly, chest rises and falls with calm breathing, seamless loop, subtle motion only, everything else stays still, no morphing, face stays consistent, no distortion, no camera shake
```

## PRESET · Гирлянда (декор-наполнитель)
> Одно движение: бумажная гирлянда колышется еле-еле. Дешёвый наполнитель,
> если пламя в конкретном рендере поплыло.
```
3d model, no 2d, subtle idle animation, the paper garland sways very slightly, chest rises and falls with calm breathing, seamless loop, subtle motion only, everything else stays still, no morphing, face stays consistent, no distortion, no camera shake
```

## PRESET · Блинк (тише всех)
> Одно движение: один медленный блинк - единственное движение лица.
> Самый безопасный пресет для крупных планов.
```
3d model, no 2d, subtle idle animation, she blinks once, slowly, chest rises and falls with calm breathing, seamless loop, subtle motion only, everything else stays still, no morphing, face stays consistent, no distortion, no camera shake
```

## PRESET · Слеза (сигнатура, риск)
> Одно движение: одна слеза медленно катится по щеке - «счастливые, они
> не считаются». Рискованно: жидкости в видео-нейронках плывут; поплыло -
> откат на «Свечи».
```
3d model, no 2d, subtle idle animation, a single tear rolls slowly down her cheek, chest rises and falls with calm breathing, seamless loop, subtle motion only, everything else stays still, no morphing, face stays consistent, no distortion, no camera shake
```

## PRESET · Хихи (настроение, ST-05-совместимый)
> Одно движение: плечи трясутся от смешка - смеётся сквозь слёзы.
> Стартует идеально от рендера ST-05 (IE-B06).
```
3d model, no 2d, subtle idle animation, her shoulders shake with a small giggle, chest rises and falls with calm breathing, seamless loop, subtle motion only, everything else stays still, no morphing, face stays consistent, no distortion, no camera shake
```

## BANK
> Банк - для сборки своего пресета из фраз (база + выбранные движения +
> хвост). Закон бобов: выбирай 1-2 движения, камера по умолчанию мёртвая
> (push-in - только по вердикту автора).
- the candle flames flicker gently | пламя свечей подрагивает - дефолт-наполнитель лупа
- the candle flames sway once and settle | пламя качнётся один раз и замрёт - замкнуть луп
- the pale pink balloon among the black ones sways slightly | розовый контрабандист колышется среди чёрных
- the paper garland sways very slightly | гирлянда колышется еле-еле - дешёвый наполнитель
- chest rises and falls with calm breathing | грудь дышит спокойно - сопутствующее по умолчанию
- chest rises and falls a little faster, like she is holding back tears | дыхание чуть чаще - слёзы на подходе
- a single tear rolls slowly down her cheek | слеза катится по щеке - сигнатура, тестируй
- a fresh tear track glistens and dries | дорожка слезы блестит и подсыхает - замкнуть луп
- she presses a black lace sleeve against one eye | рукав к одному глазу - кадр Б «Рукав»
- tears well up in her eyes | слёзы собираются в глазах - старт перехода
- both hands hold out a paper goodie bag toward the viewer | обе руки протягивают пакет - кадр Б2 «Пакет»
- she hugs the paper goodie bag a little tighter | прижимает пакет чуть крепче - «его собирали в октябре»
- her wobbly smile grows a little steadier | шатающаяся улыбка чуть укрепляется - «выбрала, кем быть»
- her wobbly smile settles back to stillness | улыбка замирает на месте - замкнуть луп
- she covers her mouth with a cardigan sleeve | рукав ко рту - «хихи»
- her shoulders shake with a small giggle | плечи трясутся от смешка - кадр-настроение ST-05
- she adjusts the crooked paper party hat with two fingers | поправляет кривую шляпу двумя пальцами (риск: руки плывут)
- she lifts her chin a little | подбородок чуть выше - гордость маленького победителя
- she leans slightly closer to the viewer | подаётся чуть ближе к зрителю - стык с кадрами Б (upper body)
- her glassy eyes brighten a little | стеклянные глаза чуть светлеют - надежда приехала
- she blinks once, slowly | один медленный блинк - самое безопасное движение лица
- long black hair strands sway gently | чёрные пряди колышутся - мягкий наполнитель
- her cardigan sleeves slip down over her hands | рукава сползают на пальцы - «лапы», стык с каноном
- the paper crown on the throne chair tilts a little | корона на трон-стуле чуть кренится (риск: бумага плывёт)
- very slow gentle camera push-in | очень медленный мягкий наезд камеры - только по вердикту автора
- camera stays completely still | камера стоит мёртво - двигается только она (дефолт)
- she looks toward the viewer | смотрит на зрителя - «увидела гостя», старт перехода
