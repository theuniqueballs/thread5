/* Быстрая проверка трека 1: парсер видит 3-значные Y-карты и прилавок — корень. */
import { parseBatch } from '/home/z/my-project/thread5/src/lib/t5/parse';
import { resolveT5Root, batchKey, shelfOrder } from '/home/z/my-project/thread5/src/lib/t5/store';
import { readFileSync } from 'node:fs';
import { join } from 'node:path';

const root = resolveT5Root();
console.log('T5_ROOT =', root);

const raw = readFileSync(join(root, 'batches/T5-26.md'), 'utf8');
const batch = parseBatch(raw);
console.log('T5-26 slots:', batch.slots.length);
const ycards = batch.slots.map((s) => s.yCard).filter(Boolean);
console.log('Y-cards parsed:', ycards.length);
console.log('unique:', [...new Set(ycards)].sort((a, b) => batchKey(a) - batchKey(b)).join(', '));
const three = ycards.filter((y) => y && y.length > 3);
console.log('3-digit ids:', three.length, three.slice(0, 6).join(', '));
const truncated = ycards.filter((y) => y && !new Set(['Y109', 'Y127', 'Y179', 'Y227', 'Y361', 'Y445', 'Y450', 'Y488', 'Y496', 'Y498', 'Y513', 'Y514', 'Y515', 'Y516', 'Y517', 'Y518', 'Y519', 'Y520', 'Y521']).has(y));
console.log('unexpected ids (should be empty):', truncated.join(', '));

// естественный порядок
const names = ['T5-9.md', 'T5-10.md', 'T5-100.md', 'T5-11.md', 'T5-2.md'];
console.log('shelf order:', [...names].sort(shelfOrder).join(' < '));

// камера
const cam = JSON.parse(readFileSync(join(root, 'specs/camera.json'), 'utf8'));
const ids = new Set(cam.y_cards.cards.map((c: { id: string }) => c.id));
const missing = [...new Set(ycards)].filter((y) => y && !ids.has(y));
console.log('camera version:', cam.version, '· cards:', ids.size);
console.log('Y-cards missing from camera (should be empty):', missing.join(', '));
