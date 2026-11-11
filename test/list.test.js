import { test } from 'node:test';
import assert from 'node:assert/strict';
import { parseBlocks } from '../site/md.js';
import { blocksToHtml } from '../site/render.js';

const ctx = { base: '', urlOf: () => null };
const html = (src) => blocksToHtml(parseBlocks(src, 'x.md'), ctx);

// 항목 아래 들여쓴 줄은 그 항목의 이어지는 글이다.
// 여기서 목록을 끊으면 항목마다 새 <ol> 이 되어 번호가 전부 1 이 된다.
test('번호 항목 아래 들여쓴 줄은 그 항목에 붙고 목록은 이어진다', () => {
  assert.equal(
    html('1. 코딩\n   실행되지 않으면 한 게 없다.\n2. 테스팅\n   끝났는지 알아야 한다.'),
    '<ol><li>코딩 실행되지 않으면 한 게 없다.</li><li>테스팅 끝났는지 알아야 한다.</li></ol>',
  );
});

test('이어지는 줄도 줄 끝 두 칸이면 줄바꿈이다', () => {
  assert.equal(html('1. 코딩  \n   설명\n2. 테스팅'), '<ol><li>코딩<br>설명</li><li>테스팅</li></ol>');
});

test('들여쓴 줄은 하위 항목에도 붙는다', () => {
  assert.equal(html('- 위\n  - 아래\n    이어짐'), '<ul><li>위<ul><li>아래 이어짐</li></ul></li></ul>');
});

test('들여쓰지 않은 줄은 목록 밖 단락이다', () => {
  assert.equal(html('1. 코딩\n밖이다'), '<ol><li>코딩</li></ol>\n<p>밖이다</p>');
});
