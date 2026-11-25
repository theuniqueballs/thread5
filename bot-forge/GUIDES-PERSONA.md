# Гайды: персона под Nephra и мелкие модели

> **Статус:** ресёрч 2026-11-06. Вопрос автора: «модели типа Nephra не особо
> воспринимают такой формат персоны - что в неё писать». Ниже выжимка из
> расширенных гайдов, без воды. Эм дэши не используются.

## 1. Что такое Nephra

- Семейство LLM платформы Moescape (Taven): Nephra 8B, 70B, 12B (v2).
  Основа - Meta Llama 3, финетун Sao10K по RP-датасетам (roleplay +
  instruction-style).
- Формат промпта: Llama-3-Instruct. Контекст: 8192 токенов.
- Рекомендованные настройки с карточки HF (yodayo-ai/nephra_v1.0):
  temperature 1.12, min-p 0.075, repetition penalty 1.1, стоп-строки
  "\n{{user}}", "<", "\`\`\`" - у модели бывают сломанные генерации.

## 2. Главный вывод: мелкой модели нужна менее подробная персона

- r/MoescapeAI_Official, тред Peersona: «Smaller models like Nephra/Elune
  will need less detailed personas, while bigger models like
  Ultra/Deepseek/Claude won't need those limitations». То есть ощущение
  автора верное: подробная персона бьёт по Nephra, а не по Claude.
- ParasiticRogue (Model-Tips-and-Tricks на HF): жёстко структурированные
  нестандартные форматы (W++ и родня) дают менее стабильное поведение -
  такого синтаксиса мало в тренировочных данных; простыня из вики - bloat,
  модель тонет в нерелевантном.
- Его рекомендация - JED+, гибрид: списки для конкретики (appearance,
  черты личности), проза для бэкграунда и речевых паттернов.
- Перспектива письма: от первого лица («I») - личный голос, чат 1-на-1;
  от третьего лица - повествование и групповые сцены; второе лицо («You
  are...») - хуже всех для персонажа.

## 3. Официальные бюджеты Moescape (docs.moescape.ai)

- persona: 500-700 токенов
- greeting: 20-80 токенов
- world scenario: 0-100 токенов (опционально)
- example dialogue: 0-100 токенов (опционально); страница Tips: держи
  scenario + ED суммарно до ~500 символов
- 1 токен ≈ 3-4 символа; счётчик: platform.openai.com/tokenizer
- Каждое поле съедает память: чем больше persona + greeting + ED, тем
  короче история чата. Мелкая модель с 8192 контекста чувствует это сразу.

## 4. Логика Scenario Box (официальный док)

Порядок: constraints → variables → statements.

- constraints: все негативы («{{char}} does not X», запреты говорить и
  действовать за {{user}}) - в начало бокса.
- variables: пулы активностей, NPC, условия IF/AND/OR - в середину.
- statements: факты сцены - в конец.
- Boolean реально работает: «{{char}} will do X IF {{user}} gives A AND
  pats them on the head».

## 5. Форматы persona (официальный док, один образец «Lisa»)

- W++ - 266 токенов: читаемый, но жрёт токены на пунктуацию.
- Boostyle - 169: экономно, но каша: без категорий модель путает, к чему
  относится черта.
- Bracketed List - 207: списки со скобками, компромисс.
- Plaintext - 364: как вики-статья; дорого, зато близко к тренировочным
  данным.
- Вывод дока: «правильного» формата нет; решают читаемость для автора и
  стабильность у конкретной модели.
- Свежий character sheet (Shy Dreams, фев 2026, Moescape): Name(""),
  Appearance("x" + "y" + ...), Relationship to {{user}}, Speech,
  Personality, Kinks, Likes/Dislikes/Loves/Hates. Наши 13 секций - тот же
  принцип: скобки как организаторы внимания. В комментах автор поста:
  скобки говорят модели «здесь пул инфы», модель знает, где искать цвет
  глаз или одежду.

## 6. Что это значит для FORGE (атрибутный формат v2)

- Наш формат - bracket-list с прозой внутри секций. Для Nephra проблема,
  похоже, не в скобках, а в длине значений: мелкая модель теряет нить в
  многострочных значениях.
- Апгрейд под мелкие модели (тест автора, не переписывать вслепую):
  - значения секций резать до фраз-тэгов; канон держат [Appearance] и
    [System note];
  - голос оставить прозой (JED+): [Voice] с сэмплом реплики,
    [Background] - 2-3 предложения;
  - [Thoughts] - под вопросом для Nephra: метакоманды «в самом конце
    каждого ответа» мелкая модель может терять; скипнуть секцию = удалить
    одной правкой (закон v2 это уже разрешает);
  - ED работает как few-shot: он задаёт длину и формат ответа; наши пары
    короткие - ок.
- Гритинги 20-80 токенов у нас нарушены сознательно (полные сцены) - это
  рычаг длины ответов: длинный G = длинные ответы. Если Nephra пишет
  простыни - резать greeting, не persona.
- **Живой тест формата запущен:** `bots/B-06-ophelia` - персона в формате
  v3 «проза-тэги» (эталон сравнения - атрибутный v2 у B-04/B-05). Тест
  изолирует одну переменную (формат), остальное - в нормах конвейера.
  Вердикт автора - в L10 OPS бота после живого прогона.

## 7. Ссылки

- Advanced Character Creator Guide:
  docs.moescape.ai/tavern-chatbot-guide/lorebook-hub/advanced-character-creator-guide
- Tips On How To Enhance Character:
  docs.moescape.ai/tavern-chatbot-guide/tips-on-how-to-enhance-character
- Карточка Nephra v1: huggingface.co/yodayo-ai/nephra_v1.0
- Model-Tips-and-Tricks (ParasiticRogue):
  huggingface.co/ParasiticRogue/Model-Tips-and-Tricks
- Character sheet Shy Dreams (фев 2026):
  moescape.ai/posts/93ec8775-8e02-4196-9bbb-d10a32712ab9
- Тред Peersona:
  reddit.com/r/MoescapeAI_Official/comments/1rvvapk/peersona
