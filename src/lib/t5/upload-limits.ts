/**
 * THREAD 5 — чистые правила инбокса: ЕДИНЫЙ источник для клиента и сервера.
 *
 * Живёт отдельно от inbox.ts намеренно: инбокс-либа тянет node:fs/sharp и
 * серверна целиком — прямой импорт её значений в клиентский компонент
 * втаскивает node:fs в браузерный бандл (живой краш 2026-11-21: Turbopack
 * «chunking context does not support external modules», прилавок лёг 500).
 * Типы едут свободно (стираются на компиляции), значения — только отсюда.
 *
 * 2026-11-21 (цикл 2): сюда же переехала логика очереди триажа — раньше
 * RETRIAGE_RE жил ОСОБЫМИ копиями в inbox.ts (сервер) и inbox-view.tsx
 * (клиент), и любое расхождение молча меняло поведение очереди. Теперь
 * оба берега импортируют один needsTriageLike — дрейф исключён.
 */

/** Разрешённые расширения картинок инбокса. */
export const ALLOWED_EXT = ['png', 'jpg', 'jpeg', 'webp'] as const;

/** Кап размера одного файла (25 МБ). */
export const MAX_FILE_BYTES = 25 * 1024 * 1024;

/** Минимальная форма элемента журнала, нужная правилам очереди. */
export interface TriageQueueItem {
  status: string;
  triage: { label: string; reason: string };
  authorOverride: { label: string; at: string } | null;
}

/** Почему карантин можно перетриажировать автоматически: сбой триажа
 *  (fail-closed) или удушение 429 — это НЕ вердикт, а аварию можно лечить.
 *  Важно: 1301-вердикт контент-фильтра СЮДА НЕ МАТЧИТСЯ (живой урок
 *  2026-11-21: 13 отказов крутились в цикле бесконечно). */
export const RETRIAGE_RE = /fail-closed|429|too many|карантин/iu;

/** Кому нужен триаж: новые (queued/unknown) и аварийные карантины
 *  (упавший/задушенный триаж) — пока автор не вынес свой вердикт.
 *  Единственный источник: серверный needsTriage и клиентский цикл
 *  инбокса считают очередь по ЭТОЙ функции. */
export function needsTriageLike(item: TriageQueueItem): boolean {
  if (item.status === 'queued' || item.triage.label === 'unknown') return true;
  return (
    !item.authorOverride &&
    item.triage.label === 'x' &&
    RETRIAGE_RE.test(item.triage.reason)
  );
}
