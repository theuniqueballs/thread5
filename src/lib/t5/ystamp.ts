/**
 * Y-STAMP — клеймо/паспорт слота (акт 2 вердикта T5-24, приказ Б;
 * LAWS §17, raw-plus 2.1.0, gates.json 1.14.0 yStampGate).
 *
 * Единый канонический формат с tools/gates.py v1.14.0:
 *   Y-STAMP: Y29 «COVER» × <поза карты 1:1> × <камера карты> · corridor A
 *
 * Клеймо печатается ТОЛЬКО из карты (specs/camera.json y_cards) — правка
 * промпта мимо карты запрещена: правишь карту — клеймо перерождает сам.
 * Печатаются рисуемые компоненты паспорта (класс экспозиции, поза, камера,
 * коридор); служебные поля карты (POV-read, профайлинг) в POS не печатаются
 * (закон непрозы: каждое слово рисуется).
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

/** Строка клейма из карты — копипаст-юнит 1:1, пересказ запрещён. */
export function buildYStampLine(card: YCardLike): string {
  const cls = card.components?.exposure?.class || '—';
  const pose = card.components?.pose || '';
  const camera = card.components?.camera || '';
  const corridor = card.corridor || '—';
  return `Y-STAMP: ${card.id} «${cls}» × ${pose} × ${camera} · corridor ${corridor}`;
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
