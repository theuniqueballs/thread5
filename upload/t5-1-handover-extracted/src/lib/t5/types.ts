/**
 * THREAD 5 — типы, которые живут по обе стороны API.
 * Файл клиентски-безопасный: никаких node-импортов.
 */

export interface BatchListItem {
  slug: string;
  file: string;
  theme: string | null;
  title: string;
  slotCount: number;
  expCount: number;
  ocCount: number;
  ratingSpread: Record<string, number>;
  verdictCount: number;
  mtime: string;
}

export interface StoredVerdict {
  file: string;
  slug: string;
  createdAt: string;
  text: string;
}

export type T5DocGroup = 'memory' | 'ars';

export interface T5DocMeta {
  name: string;
  title: string;
  hint: string;
  group: T5DocGroup;
}

/**
 * main = полный кабинет автора: крафт-доки + ЛИЧНОЕ (вкус, живой лист, OC-канон, корпус).
 * friend-pass: личные доки вычищены в самой ветке (файлы), а список там ужат — у друга
 * свой кабинет. Здесь (main) ничего не ужинаем.
 * Группы: 'memory' — доки памяти; 'ars' — АРС · ПЛАНЕТЫ (сеансы конвейера).
 */
export const T5_DOCS: T5DocMeta[] = [
  { name: 'LAWS', title: 'ЗАКОНЫ', hint: 'рабочий лист писца: флоры, формат, чеклист', group: 'memory' },
  { name: 'ARS-NOVEAU', title: 'ARS NOVEAU', hint: 'раскрытие темы: истории до тегов', group: 'memory' },
  { name: 'RENDER-TROUBLES', title: 'ТРАВМЫ РЕНДЕРА', hint: 'каталог проблем T4 → лечение', group: 'memory' },
  { name: 'RENDERER_FACTS', title: 'ФИЗИКА РЕНДЕРА', hint: 'что рисует и что мертво', group: 'memory' },
  { name: 'NICHE', title: 'НИША', hint: 'доктрина жанра чуда', group: 'memory' },
  { name: 'TASTE', title: 'ВКУС', hint: '28 законов вкуса автора', group: 'memory' },
  { name: 'LIVING-NOTES', title: 'ЖИВОЙ ЛИСТ', hint: 'квитанции вердиктов: решения автора', group: 'memory' },
  { name: 'OC-CANON', title: 'OC-КАНОН', hint: 'личный канон OC: тело, глаза, щиты', group: 'memory' },
  { name: 'SPECIAL-ROSTER', title: 'РОСТЕР ГОСТЕЙ', hint: 'чужие персонажи Special Orders: канон-раны под рукой', group: 'memory' },
  { name: 'OC-BODY-ARCHIVE', title: 'АРХИВ ТЕЛ', hint: 'личный архив тел OC', group: 'memory' },
  { name: 'GOLDEN-CORPUS', title: 'КОРПУС', hint: 'золотой корпус пар POS/NEG', group: 'memory' },
  { name: 'T5-1-BETA', title: '5.1 BETA', hint: 'проект нового формата: NL + аниме-теги + PH', group: 'memory' },
  { name: 'README', title: 'ПЕТЛЯ', hint: 'как работает тред', group: 'memory' },
  // ── АРС · ПЛАНЕТЫ: пять сеансов конвейера + карта системы ──
  { name: 'ARS-00', title: 'ОБЗОР СИСТЕМЫ', hint: 'карта ARS NOVEAU v2: планеты-сеансы конвейера', group: 'ars' },
  { name: 'ARS-01', title: '01 · SOL', hint: 'сеанс 1: ядро — идея, истории слотов, раскрытие темы', group: 'ars' },
  { name: 'ARS-02', title: '02 · MERCURY', hint: 'сеанс 2: спавн — каст, кости, дрессер', group: 'ars' },
  { name: 'ARS-03', title: '03 · VENUS', hint: 'сеанс 3: корпус сцены — RAW+ теги', group: 'ars' },
  { name: 'ARS-04', title: '04 · EARTH', hint: 'сеанс 4: сборка и полировка промптов', group: 'ars' },
  { name: 'ARS-05', title: '05 · FURNACE', hint: 'сеанс 5: ревью, негативы, блокнот ошибок', group: 'ars' },
];
