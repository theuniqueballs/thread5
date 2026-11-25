# MOTION-B05 - анимация B-05 · hover-луп + переход двухкадровки

> **v1.0 - собран с рождения под ЗАКОН БОБОВ** (вердикт автора 2026-11-04:
> ~2000 бобов ушли на один луп из-за перегруженного промпта на B-04). Один
> пресет = ОДНО движение (плюс максимум одно сопутствующее: дыхание). Камера
> стоит мёртво - push-in живёт в банке, по вердикту автора. Меньше движений =
> дешевле прогон = меньше плывуна. Для Agnes движения специально
> «медсестринские»: дыхание, пепел, кольца - никакой сложной хореографии.
>
> **v1.1 - связка перехода (вердикт автора):** переход двухкадровки получил
> СВОЙ промпт - он связывает все три картинки воедино: SO-12 (А) → ST-01
> «Шшш» (Б) → ST-02 «Вена» (Б2). Кадры Б - Image Editor-дельты поверх
> рендера SO-12 (IE-B05 v1.2). В img2video уходят ОБЕ картинки (старт +
> финиш): А+Б или А+Б2 - промпт «Переход» один на обе пары, нейронка
> достраивает промежуток сама. Луповые пресеты ниже - заставка из ОДНОГО
> кадра, сюжет перехода они не описывают.
>
> Как работает: готовый рендер + промпт отсюда уходят вместе в
> img2video-нейронку. На выходе - короткий почти-луп: на заставке при
> наведении мышки она слегка двигается. База и анти-морф-хвост вшиты в
> каждый пресет - скопировал → вставил → запустил. Кадр SO-12 остаётся
> статичным стоп-краном: луп делается ИЗ рендера, а не вместо него.

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

## PRESET · Тише (переход двухкадровки)
> Промпт-связка: сюжет перехода целиком - заметила взгляд → палец к губам
> (кадр Б) → взгляд в ладонь, свечение, кольца (кадр Б2). Три коротких
> медленных шага - исключение из закона однодвижности: переход не луп,
> сюжет и есть движение. В img2video уходит пара А+Б или А+Б2, промпт тот
> же. Без «seamless loop» - переход не зациклен (нужен луп - добавь его
> из TAIL).
```
3d model, no 2d, subtle animation, she lifts her face toward the viewer and raises one index finger to her lips in a shushing gesture, then lowers her gaze to her open palm as a faint red glow gathers above it, the iron rings on her staff spin up slowly, everything else stays still, no morphing, face stays consistent, no distortion, no camera shake
```

## PRESET · Пепел (луп заставки)
> Дефолт и самый дешёвый: пепел плывёт в сером свете, она дышит. Всё
> остальное стоит на месте, камера мёртвая.
```
3d model, no 2d, subtle idle animation, ash and dust drift slowly through the air, chest rises and falls with calm breathing, seamless loop, subtle motion only, everything else stays still, no morphing, face stays consistent, no distortion, no camera shake
```

## PRESET · Кольца (орудие-герой)
> Одно движение: кольца посоха медленно вращаются - «работа продолжается».
> Глаза и улыбка НЕ двигаются.
```
3d model, no 2d, subtle idle animation, the three iron rings on her staff rotate slowly, chest rises and falls with calm breathing, seamless loop, subtle motion only, everything else stays still, no morphing, face stays consistent, no distortion, no camera shake
```

## PRESET · Вена (кадр Б2-совместимый)
> Одно движение: багровое свечение пульсирует в раскрытой ладони. Стартует
> идеально от рендера ST-02 (IE-B05) - пара А→Б2 для перехода «шшш → чудо».
```
3d model, no 2d, subtle idle animation, a faint red glow pulses gently in her open palm, chest rises and falls with calm breathing, seamless loop, subtle motion only, everything else stays still, no morphing, face stays consistent, no distortion, no camera shake
```

## PRESET · Взгляд (ядро яндере)
> Одно движение: голова медленно наклоняется, живой глаз не отпускает
> зрителя. Немигающее слежение - её фирменная жуть.
```
3d model, no 2d, subtle idle animation, she slowly tilts her head, her single grey eye stays on the viewer, chest rises and falls with calm breathing, seamless loop, subtle motion only, everything else stays still, no morphing, face stays consistent, no distortion, no camera shake
```

## PRESET · Капля (сигнатура, риск)
> Одно движение: одна капля крови медленно падает с пальцев - «обряд не
> окончен». Рискованно: жидкости в видео-нейронках плывут; поплыло - откат
> на «Пепел».
```
3d model, no 2d, subtle idle animation, a single drop of blood falls slowly from her fingertips, chest rises and falls with calm breathing, seamless loop, subtle motion only, everything else stays still, no morphing, face stays consistent, no distortion, no camera shake
```

## BANK
> Банк - для сборки своего пресета из фраз (база + выбранные движения +
> хвост). Закон бобов: выбирай 1-2 движения, камера по умолчанию мёртвая
> (push-in - только по вердикту автора).
- ash and dust drift slowly through the air | пепел плывёт в сером свете - дешёвый наполнитель лупа
- chest rises and falls with calm breathing | грудь дышит спокойно - сопутствующее по умолчанию
- chest rises and falls a little deeper | дыхание чуть глубже - возбуждение проступает
- the three iron rings on her staff rotate slowly | кольца посоха медленно вращаются - «работа продолжается»
- the rings slow down as if the work is finished | кольца замедляются - обряд закончен, замкнуть луп
- a faint red glow pulses gently in her open palm | багровое свечение пульсирует в раскрытой ладони
- the red glow fades out slowly | свечение медленно гаснет - замкнуть луп
- a single drop of blood falls slowly from her fingertips | капля крови с пальцев - «обряд не окончен», тестируй
- she slowly tilts her head | голова медленно наклоняется - «слушает»
- her single grey eye stays on the viewer | живой глаз не отрывается от зрителя - немигающее слежение
- she blinks once, slowly | один медленный блинк - единственное движение лица
- loose hair strands sway gently | выбившиеся пряди колышутся
- the free end of her blindfold sways slightly | свободный кончик повязки чуть колышется
- her weight shifts slightly on her bare knees | вес чуть переносится на босых коленях
- she presses her hand flat against her own chest | ладонь на собственной груди - слушает своё сердце
- her smile widens a little, then settles | улыбка чуть шире и замирает - «нашла форму»
- her smile settles back to stillness | улыбка замирает на месте - замкнуть луп
- grimoire pages flutter slightly | страницы фолианта чуть шелестят (риск: бумага плывёт)
- the grimoire page she turned settles back | перевёрнутая страница возвращается - замкнуть луп
- she lifts the staff slightly and sets it back | посох чуть приподнимается и возвращается (риск: предметы плывут)
- very slow gentle camera push-in | очень медленный мягкий наезд камеры - только по вердикту автора
- camera stays completely still | камера стоит мёртво - двигается только она (дефолт)
- she lifts her face toward the viewer | поднимает лицо к зрителю - «заметила взгляд», старт перехода
- she raises one index finger to her lips in a shushing gesture | палец вертикально к губам - кадр Б «Шшш»
- her crooked smile widens a little | улыбка чуть шире - кадр Б
- she leans slightly closer to the viewer | подаётся чуть ближе к зрителю - стык с кадром Б (upper body)
- her gaze drops to her open palm | взгляд вниз на раскрытую ладонь - кадр Б2
- a faint red glow gathers above her open palm | багровое свечение собирается над ладонью - кадр Б2
- the iron rings on her staff spin up slowly | кольца посоха разгоняются - кадр Б2
