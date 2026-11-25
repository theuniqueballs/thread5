# MOTION-B04 - заставка B-04 · hover-луп обложки

> **v1.2 - ЗАКОН БОБОВ (вердикт автора 2026-11-04: ~2000 бобов ушли на один
> луп из-за перегруженного промпта).** Один пресет = ОДНО движение (плюс
> максимум одно сопутствующее: дыхание, качание улики). Камера стоит
> мёртво - push-in и мигание света убраны из пресетов (живут в банке, по
> вердикту автора). Меньше движений = дешевле прогон = меньше плывуна.
>
> **v1.1 - пересобран под рендер v0.4** (ирэдзуми-рукав слева, тёмно-винные
> волосы, янтарные глаза): окно дракона живёт в каждом пресете, где видно
> плечо.
>
> **Двухкадровый переход (v0.5):** рендер SO-11 = кадр А; кадр Б - ST-01
> из IE-B04 (стол на двоих), рендерится отдельно. Порядок: кадр А → кадр Б
> → луп. При переходе в img2video уходят ОБЕ картинки (стартовая + конечная),
> промпт лупа остаётся однодвижным - переход-сюжет нейронка собирает сама
> (так случайно вышло на Нико - получилось мега круто, теперь это механика).
>
> Как работает: готовый рендер + промпт отсюда уходят вместе в
> img2video-нейронку. На выходе - короткий почти-луп: на заставке при
> наведении мышки она слегка двигается. База и анти-морф-хвост вшиты в
> каждый пресет - скопировал → вставил → запустил. Кадр SO-11 остаётся
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

## PRESET · Коридор (main)
> Дефолт и самый дешёвый: вес переносится с ноги на ногу, туфли качаются на
> пальцах. Всё остальное стоит на месте, камера мёртвая.
```
3d model, no 2d, subtle idle animation, her weight slowly shifts from one bare foot to the other, black stiletto heels swing gently in her fingers, chest rises and falls with calm breathing, seamless loop, subtle motion only, everything else stays still, no morphing, face stays consistent, no distortion, no camera shake
```

## PRESET · Дракон (вайбик-герой)
> Одно движение: плечо медленно подставляется янтарному свету - блик пробегает
> по золотой чешуе дракона. Глаза и улыбка НЕ двигаются - переход-сюжет
> (кадр А → кадр Б) делается отдельно из рендеров.
```
3d model, no 2d, subtle idle animation, she slowly tilts her bare left shoulder toward the warm light, gold scales of the dragon tattoo glint, chest rises and falls with calm breathing, seamless loop, subtle motion only, everything else stays still, no morphing, face stays consistent, no distortion, no camera shake
```

## PRESET · Голод (hunger+)
> Одно движение: взгляд медленно съезжает вниз по зрителю и возвращается.
> Это состояние L4 - держать редким.
```
3d model, no 2d, subtle idle animation, her eyes slowly travel down and back up to the viewer, chest rises and falls a little deeper, seamless loop, subtle motion only, everything else stays still, no morphing, face stays consistent, no distortion, no camera shake
```

## PRESET · Просто соседка (маскировка)
> Одно движение: ровный качающийся вес + один маленький кивок бутылкой.
> Нормальность продаёт подозрение лучше голода.
```
3d model, no 2d, subtle idle animation, calm natural idle sway, one small nod with the wine bottle like a greeting, chest rises and falls with calm breathing, seamless loop, subtle motion only, everything else stays still, no morphing, face stays consistent, no distortion, no camera shake
```

## PRESET · Стоп-кран (риск)
> Одно движение: обе бретонки медленно сползают к локтям, она НЕ поправляет -
> рукав дракона выходит целиком. Рискованно: ткани в видео-нейронках плывут;
> поплыло - откат на «Коридор».
```
3d model, no 2d, subtle idle animation, black dress straps slowly slide off both shoulders down to her elbows, she does not fix them, chest rises and falls with calm breathing, seamless loop, subtle motion only, everything else stays still, no morphing, face stays consistent, no distortion, no camera shake
```

## BANK
> Банк - для сборки своего пресета из фраз (база + выбранные движения +
> хвост). Закон бобов: выбирай 1-2 движения, камера по умолчанию мёртвая
> (push-in - только по вердикту автора).
- her weight slowly shifts from one bare foot to the other | вес медленно переносится с ноги на ногу - корпус живёт
- black stiletto heels swing gently in her fingers | туфли качаются на пальцах - улика «свидание кончилось»
- her smile assembles a half-second late, one corner first | улыбка собирается с опозданием - сначала один уголок
- her smile finishes forming, both corners level | улыбка догоняет - оба уголка на месте, замкнуть луп
- her eyes slowly travel down and back up to the viewer | взгляд медленно съезжает вниз и возвращается - аппетит без слов
- she bites her lower lip on the wine-stain side | прикус губы со стороны винного следа
- open wine bottle tilts slightly in her hand | бутылка чуть наклоняется - вино как третий участник
- one small nod with the wine bottle like a greeting | маленький кивок бутылкой - «привет, сосед»
- black dress strap slides a little lower off her left shoulder | бретонка сползает чуть ниже по ЛЕВОМУ плечу - ткани плывут, тестируй
- she pulls the strap back up with one finger | поправляет бретонку одним пальцем - шаг назад по лестнице
- loose hair strands sway softly in the hallway draft | выбившиеся пряди колышутся от сквозняка
- champagne-gold earrings catch the light | шампань-золото серёжек ловит свет
- gold on the dragon tattoo glints on her bare shoulder | золото на чешуе дракона бликует на голом плече
- light travels along the gold scales of the dragon tattoo | свет пробегает по золотой чешуе - дракон «оживает»
- she slowly tilts her bare left shoulder toward the warm light | плечо медленно подставляется янтарному свету - вайбик
- she notices the viewer watching and lifts her eyes to meet them | замечает взгляд и поднимает глаза - «знала, что смотришь»
- wine-dark hair strands drift slightly | винные пряди чуть колышутся
- warm honey hallway light flickers almost imperceptibly | янтарный свет коридора мигает едва заметно
- warm honey hallway light stays steady | свет стоит ровно - режим «просто соседка»
- chest rises and falls with calm breathing | грудь дышит спокойно
- chest rises and falls a little deeper | дыхание чуть глубже - голод проступает
- chin lifts slightly, gaze stays on the viewer | подбородок чуть вверх, взгляд не отрывается
- very slow gentle camera push-in | очень медленный мягкий наезд камеры - только по вердикту автора
- camera stays completely still | камера стоит мёртво - двигается только она (дефолт)
