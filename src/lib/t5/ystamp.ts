/**
 * Y-STAMP — клеймо/паспорт слота (акт 2 вердикта T5-24, приказ Б; уточнение
 * автора 2026-11-19, В34 «не оставляй промпт на произвол судьбы»;
 * LAWS §17, raw-plus 2.2.0, gates.json 1.15.0 yStamp).
 *
 * В34: обозначения в POS ЗАПРЕЩЕНЫ — клеймо = вплетённый смысл. Чип копирует
 * ВПЛЕТЕНИЕ (паттерн карты 1:1 с физикой, без метки/класса/CAM-кодов/
 * corridor-токена) — то, что встает строкой 3 POS. Метка-паспорт
 * (buildYStampLine) — только метаданные чипа/сверки, в промпт не идет.
 * Печать ТОЛЬКО из карты (specs/camera.json y_cards): правка промпта мимо
 * карты запрещена — правишь карту, вплетение перерождает сам.
 */
export interface YCardComponents {
  exposure?: { class?: string; cover_object?: string; read?: string };
  pose?: string;
  pov?: string;
  camera?: string;
  profiling?: string;
}

export interface YCardLike {
  id: string;
  corridor?: string;
  built_from?: string;
  trust?: string;
  components?: YCardComponents;
}

/** Строка клейма-метки — ТОЛЬКО метаданные (В34: в POS не печатается). */
export function buildYStampLine(card: YCardLike): string {
  const cls = card.components?.exposure?.class || '—';
  const pose = card.components?.pose || '';
  const camera = card.components?.camera || '';
  const corridor = card.corridor || '—';
  return `Y-STAMP: ${card.id} «${cls}» × ${pose} × ${camera} · corridor ${corridor}`;
}

/**
 * Вплетение (COMBO-WEAVE, строка 3 POS) — паттерн карты копипастом 1:1,
 * БЕЗ обозначений (В34); физика карты целиком (В35). Единственный текст
 * клейма, легальный в POS.
 */
export function buildWeave(card: YCardLike): string {
  return card.components?.pose || '';
}

/**
 * Разбор строки клейма (сверка с картой — та же дисциплина, что в гейте;
 * поза и камера приходят одним телом — их сверка с картой идёт подстрокой,
 * как в tools/gates.py v1.14.0).
 */
export function parseYStampLine(
  line: string,
): { id: string; cls: string; body: string; corridor: string } | null {
  const m = line
    .trim()
    .match(/^Y-STAMP:\s*(Y\d{1,3})\s*«([^»]*)»\s*×\s*(.+?)\s*·\s*corridor\s*([AB+]+|—)\s*$/i);
  if (!m) return null;
  return { id: m[1], cls: m[2].trim(), body: m[3].trim(), corridor: m[4] };
}
