import { test } from 'node:test';
import assert from 'node:assert/strict';
import { parseInline, parseBlocks } from '../site/md.js';
import { inlineToHtml, blocksToHtml } from '../site/render.js';

const ctx = { base: '', urlOf: () => null };

test('![글](주소) 는 그림이 된다', () => {
  const html = inlineToHtml(parseInline('![도표](https://x.com/a.png)', 'a.md'), ctx);
  assert.match(html, /<img src="https:\/\/x\.com\/a\.png" alt="도표"/);
});

// 링크가 아니라 그림이다. 앞의 ! 를 놓치면 주소만 적힌 링크가 나온다.
test('그림은 링크로 새지 않는다', () => {
  const html = inlineToHtml(parseInline('![도표](https://x.com/a.png)', 'a.md'), ctx);
  assert.doesNotMatch(html, /<a /);
});

// 옛 노트는 GitHub 웹에서 붙여넣은 <img> 를 그대로 갖고 있다.
// 파서가 모르면 태그가 글자로 새어 나온다.
test('한 줄짜리 <img> 태그는 그림으로 나간다', () => {
  const src = 'https://raw.githubusercontent.com/juniqlim/note/master/programming/x.png';
  const blocks = parseBlocks(`<img width="372" alt="스크린샷" src="${src}">`, 'a.md');
  const html = blocksToHtml(blocks, ctx);
  assert.match(html, new RegExp('<img src="' + src.replace(/[.]/g, '\\.') + '"'));
  assert.doesNotMatch(html, /&lt;img/);
});

test('그림 아닌 글은 그대로다', () => {
  const html = inlineToHtml(parseInline('[글](https://x.com/a)', 'a.md'), ctx);
  assert.match(html, /<a class="ext"/);
});
