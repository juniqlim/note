import { test } from 'node:test';
import assert from 'node:assert/strict';
import { parseInline } from '../site/md.js';
import { inlineToHtml } from '../site/render.js';

const ctx = { base: '', urlOf: () => null };

// 노트는 개념이 아니라 글 한 편이다. [[ ]] 로 서로를 부르지 않는다.
// 위키 문법을 그대로 두면 노트 본문의 대괄호가 엉뚱한 링크가 된다.
test('[[이름]] 은 링크가 아니라 글자로 남는다', () => {
  const html = inlineToHtml(parseInline('[[위키워드]] 를 적었다', 'x.md'), ctx);
  assert.equal(html, '[[위키워드]] 를 적었다');
});

// CamelCase 는 프로그래밍 노트에 흔하다. 링크로 잡으면 온 글이 링크가 된다.
test('CamelCase 는 링크가 되지 않는다', () => {
  const html = inlineToHtml(parseInline('TestCase 를 먼저 쓴다', 'x.md'), ctx);
  assert.equal(html, 'TestCase 를 먼저 쓴다');
});
