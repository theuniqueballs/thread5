# MOTION-B03 — заставка B-03 · hover-луп обложки

> Как работает: готовый рендер SO-10 + промпт отсюда уходят вместе в
> img2video-нейронку. На выходе — короткий почти-луп: на заставке при
> наведении мышки она слегка двигается, елозит, делает что-то.
> База («3d model, no 2d») и анти-морф-хвост уже вшиты в каждый пресет —
> скопировал → вставил → запустил. В сборщике они подставляются сами.
> Кадр SO-10 остаётся статичным стоп-краном: луп делается ИЗ рендера,
> а не вместо него.

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

## PRESET · Порог (main)
> Ровно то, что происходит на рендере, но живьём: наклон головы за границу
> удобного, улыбка ползёт на зуб шире, один тяжёлый морг, сквозняк в волосах
> и ленте, зелёная кромка мигает едва заметно, тьма за спиной дышит,
> медленный наезд. Дефолт — с этого начинаем.
```
3d model, no 2d, subtle idle animation, she slowly tilts her head a few degrees to the side, past comfortable, smile slowly widens a little showing even white teeth, one slow heavy blink, void-black eyes never leave the viewer, long jet-black hair sways slightly in a warm night draft, thin pale-green ribbon drifts with her hair, chest rises and falls barely noticeably, faint pale-green porch glow flickers almost imperceptibly, pitch-black darkness behind her shifts very slightly, very slow gentle camera push-in, seamless loop, subtle motion only, everything else stays still, no morphing, face stays consistent, no distortion, no camera shake
```

## PRESET · Джага-джага (creep+)
> Жутче: замирает — потом голова уходит набок дальше нормы, улыбка
> растягивается шире, не моргает вовсе, подаётся ближе в проём и снова
> замирает. Зелёный пульсует раз за луп, тьма за спиной дышит.
```
3d model, no 2d, subtle idle animation, she stands unnaturally still, then her head slowly tilts far to the side, smile stretches a little too wide showing too many even white teeth, she never blinks, void-black pupils shrink tighter, she leans slightly closer into the doorway and freezes again, faint pale-green porch glow pulses once barely visible, the pitch-black darkness behind her seems to breathe, very slow gentle camera push-in, seamless loop, subtle motion only, everything else stays still, no morphing, face stays consistent, no distortion, no camera shake
```

## PRESET · Просто соседка (маскировка)
> Режим Pale Visitor: ничего аномального — просто живая девушка на пороге
> ночью. Один расслабленный морг, улыбка не меняется, зелёный стоит ровно.
> Для A/B: иногда нормальность продаёт лучше кринжа.
```
3d model, no 2d, subtle idle animation, she stands calmly in the doorway, calm natural idle sway, one relaxed friendly blink, soft smile stays the same, long jet-black hair drifts slightly in a warm night draft, chest rises and falls with calm breathing, faint pale-green porch glow stays steady, very slow gentle camera push-in, seamless loop, subtle motion only, everything else stays still, no morphing, face stays consistent, no distortion, no camera shake
```

## PRESET · Стоп-кран (риск)
> Лямка медленно сползает чуть ниже с голого плеча, взгляд не отрывается —
> джага-джага в движении. Рискованно: ткани в видео-нейронках плывут;
> поплыло — откатывайся на «Порог».
```
3d model, no 2d, subtle idle animation, she stands still looking at the viewer, thin white tank top strap slowly slides a little lower off her bare shoulder, soft smile stays calm, head tilts slightly to the side, long jet-black hair drifts in the warm night draft, faint pale-green porch glow flickers almost imperceptibly, very slow gentle camera push-in, seamless loop, subtle motion only, everything else stays still, no morphing, face stays consistent, no distortion, no camera shake
```

## BANK
- head slowly tilts to the side, a few degrees past comfortable | голова медленно клонится набок — за границу удобного
- head slowly returns to center | голова медленно возвращается прямо — замкнуть луп с наклоном
- smile slowly widens a little, showing more even white teeth | улыбка ползёт шире — зубов видно больше нормы
- smile softens back to a calm closed smile | улыбка спадает обратно к спокойной — замкнуть луп
- one slow heavy blink | один медленный тяжёлый морг
- she never blinks | не моргает вообще — весь луп
- void-black pupils shrink tighter | зрачки-точки сужаются ещё чуть
- she leans slightly closer into the doorway | подаётся чуть ближе в проём — и замирает
- chin lifts slightly, gaze stays on the viewer | подбородок чуть приподнимается, взгляд не отрывается
- thin white tank top strap slowly slides a little lower off her shoulder | лямка медленно сползает ниже с плеча — ткани плывут, тестируй
- long jet-black hair sways slightly in a warm night draft | волосы чуть колышутся от тёплого ночного сквозняка
- thin pale-green ribbon drifts with her hair | бледно-зелёная лента шевелится вместе с волосами
- chest rises and falls barely noticeably, calm breathing | грудь едва заметно дышит — спокойный вдох-выдох
- fingers slowly tap the door frame once, twice | пальцы медленно стучат по косяку: раз, второй — руки у нейронок плывут
- head rests lightly against the door frame | прислоняется головой к косяку, не отрывая взгляда
- faint pale-green porch glow flickers almost imperceptibly | зелёная лампочка крыльца мигает едва заметно
- faint pale-green porch glow stays steady | зелёная кромка стоит ровно — никакой пульсации
- pitch-black darkness behind her breathes and shifts slightly | темень за спиной дышит и чуть шевелится
- something barely moves inside the darkness behind her | в темноте за ней что-то едва движется — один раз за луп
- heat haze over dry asphalt shimmers softly | марево над сухим асфальтом дрожит
- very slow gentle camera push-in | очень медленный мягкий наезд камеры
- camera stays completely still | камера стоит мёртво — двигается только она
