# MOTION-B07 - анимация B-07 · hover-луп + переход двухкадровки

> **v1.2 - фикс подачи (2026-11-23):** пресет «Probation» → «Найм»
> (контракт-пропс удалён из речи бота, корневой фикс v1.3 в BOT-DOC;
> визуал не тронут: бланк теперь стандартный бланк гильдии, промпт
> перехода валиден); банк: «пункт четвёртый» → «подчеркнула правило».
> **v1.1 - ремонт внешности (2026-11-21):** ран v2 «джага-джага» - луп
> «Плащ» переехал на «Пальто» (подол распахнутого пальто колышется -
> читается лучше глухого одеяния), банк дополнен жестом чокера. Переход
> «Probation» синхронизирован с ST-01 v1.1 (наклон через стойку) -
> движение то же, фигура теперь работает на кадр. (v1.2: пресет
> переименован в «Найм», промпт прежний.)
> **v1.0 - собран полным паком с рождения, под ЗАКОН БОБОВ** (вердикт
> автора 2026-11-04: ~2000 бобов ушли на один луп из-за перегруженного
> промпта на B-04). Один пресет = ОДНО движение (плюс максимум одно
> сопутствующее: дыхание). Камера стоит мёртво - push-in живёт в банке,
> по вердикту автора. Меньше движений = дешевле прогон = меньше плывуна.
> Для Sylvaine движения специально «стоечные»: медь, уши, пальто,
> кристалл - никакой сложной хореографии.
>
> **Переход двухкадровки (практика B-05/B-06 verbatim):** переход получил
> СВОЙ промпт - он связывает все три картинки воедино: SO-14 v2 (А) →
> ST-01 «Найм» (Б) → ST-02 «Уши» (Б2). Кадры Б - Image Editor-дельты
> поверх рендера SO-14 (IE-B07 v1.1). В img2video уходят ОБЕ картинки
> (старт + финиш): А+Б или А+Б2 - промпт «Найм» один на обе пары,
> нейронка достраивает промежуток сама. Луповые пресеты ниже - заставка
> из ОДНОГО кадра, сюжет перехода они не описывают.
>
> Как работает: готовый рендер + промпт отсюда уходят вместе в
> img2video-нейронку. На выходе - короткий почти-луп: на заставке при
> наведении мышки она слегка двигается. База и анти-морф-хвост вшиты
> в каждый пресет - скопировал → вставил → запустил. Кадр SO-14 остаётся
> статичным стоп-краном: луп делается ИЗ рендера, а не вместо него.
>
> **Ушной теллер в видео:** уши - фирменная физика B-07, но уши в
> видео-нейронках плывут так же, как жидкости: пресет «Уши» помечен
> рискованным, поплыло - откат на «Медь».

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

## PRESET · Найм (переход двухкадровки)
> Промпт-связка: сюжет перехода целиком - срыв на стойке → заметила
> единственного, кто не отвернулся (кадр Б: наклон через стойку, бланк
> гильдии протянут) → уши признались первыми (кадр Б2: уши падают, взгляд в
> сторону). Три коротких медленных шага - исключение из закона
> однодвижности: переход не луп, сюжет и есть движение. В img2video уходит
> пара А+Б или А+Б2, промпт тот же. Без «seamless loop» - переход не
> зациклен (нужен луп - добавь его из TAIL).
```
3d model, no 2d, subtle animation, she turns her head from the counter toward the viewer, her long ear tips flare red, she leans over the counter and holds out a paper folded in thirds toward the viewer with both hands, then her ears droop low as her gaze slides away, everything else stays still, no morphing, face stays consistent, no distortion, no camera shake
```

## PRESET · Медь (луп заставки, дефолт)
> Самый дешёвый: тёплое медное сияние зала едва колышется, она дышит.
> Всё остальное стоит на месте, камера мёртвая.
```
3d model, no 2d, subtle idle animation, the warm copper glow of the hall breathes softly, chest rises and falls with calm breathing, seamless loop, subtle motion only, everything else stays still, no morphing, face stays consistent, no distortion, no camera shake
```

## PRESET · Уши (сигнатура, риск)
> Одно движение: кончики очень длинных ушей подрагивают - теллер живёт
> даже в статике. Рискованно: уши в видео-нейронках плывут; поплыло -
> откат на «Медь». Глаза и рот НЕ двигаются.
```
3d model, no 2d, subtle idle animation, the tips of her very long ears twitch slightly, chest rises and falls with calm breathing, seamless loop, subtle motion only, everything else stays still, no morphing, face stays consistent, no distortion, no camera shake
```

## PRESET · Пальто (декор-наполнитель)
> Одно движение: подол распахнутого тёмно-синего пальто колышется
> еле-еле. Дешёвый наполнитель, если уши в конкретном рендере поплыли.
```
3d model, no 2d, subtle idle animation, the hem of her long open coat sways very slightly, chest rises and falls with calm breathing, seamless loop, subtle motion only, everything else stays still, no morphing, face stays consistent, no distortion, no camera shake
```

## PRESET · Кристалл (орудие-герой)
> Одно движение: фиолетовый кристалл посоха мерно пульсирует - «смены
> караулит». Стартует идеально от кадров с посохом в сгибе руки.
```
3d model, no 2d, subtle idle animation, the violet crystal of her staff pulses gently, chest rises and falls with calm breathing, seamless loop, subtle motion only, everything else stays still, no morphing, face stays consistent, no distortion, no camera shake
```

## PRESET · Блинк (тише всех)
> Одно движение: один медленный блинк - единственное движение лица.
> Самый безопасный пресет для крупных планов.
```
3d model, no 2d, subtle idle animation, she blinks once, slowly, chest rises and falls with calm breathing, seamless loop, subtle motion only, everything else stays still, no morphing, face stays consistent, no distortion, no camera shake
```

## PRESET · Гримуар (настроение, ST-07-совместимый)
> Одно движение: она прижимает гримуар чуть крепче во сне. Стартует
> идеально от рендера ST-07 (IE-B07).
```
3d model, no 2d, subtle idle animation, she hugs her grimoire a little tighter in her sleep, chest rises and falls with calm breathing, seamless loop, subtle motion only, everything else stays still, no morphing, face stays consistent, no distortion, no camera shake
```

## BANK
> Банк - для сборки своего пресета из фраз (база + выбранные движения +
> хвост). Закон бобов: выбирай 1-2 движения, камера по умолчанию мёртвая
> (push-in - только по вердикту автора).
- the warm copper glow of the hall breathes softly | медь зала дышит - дефолт-наполнитель лупа
- the tips of her very long ears twitch slightly | кончики ушей подрагивают - теллер, сигнатура, тестируй
- her long ears flare red and settle | уши вспыхивают красным и затихают - «поймала похвалу»
- her long ears droop low and stay there | уши падают и остаются - «рот соврал, уши признались»
- the hem of her long open coat sways very slightly | подол распахнутого пальто колышется - дешёвый наполнитель
- she touches her ribbon choker lightly | трогает ленту-чокер - «собраться», джага-деталь v2
- chest rises and falls with calm breathing | грудь дышит спокойно - сопутствующее по умолчанию
- chest rises and falls a little faster, like mid-rant | дыхание чаще - середина срыва на стойке
- the violet crystal of her staff pulses gently | кристалл посоха мерно пульсирует - «смены караулит»
- the crystal flare brightens once, then dims | кристалл вспыхивает раз и гаснет - замкнуть луп
- the three wooden charms sway on her belt | три брелока качаются на поясе (риск: предметы плывут)
- the charms settle back against her hip | брелока ложатся обратно на бедро - замкнуть луп
- she turns her head from the counter toward the viewer | разворачивает голову от стойки к зрителю - старт перехода
- she holds out a paper folded in thirds toward the viewer | протягивает бланк гильдии обеими руками - кадр Б
- she taps one finger on the counter, twice | стучит пальцем по стойке дважды - «подчеркнула правило» (риск: руки)
- she adjusts her ponytail with one hand | поправляет хвост одной рукой - «собраться»
- her chin lifts a little higher | подбородок чуть выше - «гордость вместо страха»
- her violet eyes narrow slightly, then soften | фиолетовые глаза сужаются и теплеют - «оценила и не призналась»
- she blinks once, slowly | один медленный блинк - самое безопасное движение лица
- she hugs her grimoire a little tighter in her sleep | прижимает гримуар во сне - утечка доверия, кадр ST-07
- her fingers tighten around the staff shaft | пальцы сжимаются на посохе - «белая хватка»
- her shoulders settle down an inch | плечи опускаются на дюйм - «первый вечер без боя»
- a page of her grimoire turns by itself | страница гримуара листается сама (риск: бумага плывёт)
- very slow gentle camera push-in | очень медленный мягкий наезд камеры - только по вердикту автора
- camera stays completely still | камера стоит мёртво - двигается только она (дефолт)
