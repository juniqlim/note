import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readHistory } from '../site/history.js';

// git log --format=%cs --name-status --reverse -M 의 출력. 오래된 커밋이 먼저 온다.
const LOG = `2022-09-26

A\tprogramming/a.md

2023-01-08

M\tprogramming/a.md
A\tprogramming/b.md

2026-07-19

M\tprogramming/b.md
`;

test('처음 나온 커밋이 쓴 날이다', () => {
  assert.equal(readHistory(LOG).get('programming/a.md').created, '2022-09-26');
});

test('마지막으로 나온 커밋이 고친 날이다', () => {
  assert.equal(readHistory(LOG).get('programming/a.md').updated, '2023-01-08');
});

test('한 번만 나온 노트는 쓴 날과 고친 날이 같다', () => {
  const h = readHistory('2026-07-19\n\nA\tprogramming/c.md\n').get('programming/c.md');
  assert.deepEqual(h, { created: '2026-07-19', updated: '2026-07-19' });
});

// 폴더를 정리하며 파일을 옮긴 날이 쓴 날로 둔갑하면 안 된다.
// ward/kent 문서 25편이 2026-07-15 에 옮겨졌을 뿐인데 그날 쓴 것처럼 보였다.
test('파일을 옮겨도 쓴 날은 원래 그대로다', () => {
  const log = `2004-01-05

A\tprogramming/ward-interview-clay.md

2026-07-15

R100\tprogramming/ward-interview-clay.md\tprogramming/ward/ward-interview-clay.md
`;
  const h = readHistory(log).get('programming/ward/ward-interview-clay.md');
  assert.deepEqual(h, { created: '2004-01-05', updated: '2026-07-15' });
});

test('옮기기 전 이름은 목록에 남지 않는다', () => {
  const log = `2004-01-05

A\told.md

2026-07-15

R100\told.md\tnew.md
`;
  assert.equal(readHistory(log).has('old.md'), false);
});

test('두 번 옮겨도 처음 쓴 날을 잃지 않는다', () => {
  const log = `2004-01-05

A\ta.md

2020-01-01

R100\ta.md\tb.md

2026-07-15

R100\tb.md\tc.md
`;
  assert.equal(readHistory(log).get('c.md').created, '2004-01-05');
});

test('빈 이력이면 아무것도 없다', () => {
  assert.equal(readHistory('').size, 0);
});
