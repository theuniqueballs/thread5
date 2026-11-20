/**
 * THREAD 5 — нарезка пачки загрузки инбокса на короткие запросы.
 *
 * Приказ автора (2026-11-21): «инбокс наполняться порциями по 8 не хочет…
 * по две штуки, чтобы не перегружать». Урок 502: шлюз валит тяжёлые
 * multipart-пачки Bad Gateway'ем ДО того, как Next их увидит, — значит
 * режем на клиенте: максимум 2 файла И максимум 8 МБ на запрос, что
 * раньше кончится (тяжёлая одиночка летит одна).
 *
 * Чистая функция без React — живёт отдельно, тестируется в tests/unit.
 */

/** Максимум файлов в одном POST. */
export const UPLOAD_CHUNK = 2;
/** Максимум байтов в одном POST (2 файла по 6 МБ — ок, 2 по 9 МБ — уже нет). */
export const UPLOAD_CHUNK_BYTES = 8 * 1024 * 1024;

interface Chunkable {
  file: { size: number };
}

/** Порезать пачку на чанки: ≤UPLOAD_CHUNK файлов И ≤UPLOAD_CHUNK_BYTES байтов. */
export function buildUploadChunks<T extends Chunkable>(list: T[]): T[][] {
  const chunks: T[][] = [];
  let cur: T[] = [];
  let bytes = 0;
  for (const p of list) {
    const size = p.file.size;
    if (cur.length > 0 && (cur.length >= UPLOAD_CHUNK || bytes + size > UPLOAD_CHUNK_BYTES)) {
      chunks.push(cur);
      cur = [];
      bytes = 0;
    }
    cur.push(p);
    bytes += size;
  }
  if (cur.length > 0) chunks.push(cur);
  return chunks;
}
