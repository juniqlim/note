import { test } from 'node:test';
import assert from 'node:assert/strict';
import { parseInline, resolveHref } from '../site/md.js';
import { inlineToHtml } from '../site/render.js';

// 이 사이트에 있는 노트만 아는 ctx.
const ctx = { base: '', urlOf: (p) => (p === 'programming/here.md' ? 'notes/programming/here.html' : null) };

test('GitHub blob 주소는 노트 경로로 풀린다', () => {
  const r = resolveHref('https://github.com/juniqlim/note/blob/master/programming/here.md', 'x.md');
  assert.equal(r.href, 'programming/here.md');
  assert.equal(r.internal, true);
});

test('원래 주소를 잃지 않는다', () => {
  const r = resolveHref('https://github.com/juniqlim/note/blob/master/programming/here.md', 'x.md');
  assert.equal(r.raw, 'https://github.com/juniqlim/note/blob/master/programming/here.md');
});

test('여기 있는 노트면 내부 링크가 된다', () => {
  const html = inlineToHtml(parseInline('[글](https://github.com/juniqlim/note/blob/master/programming/here.md)', 'x.md'), ctx);
  assert.match(html, /<a class="internal" href="notes\/programming\/here.html">글<\/a>/);
});

// 여기 없는 노트를 가리키는 것은 흔한 일이다. 링크를 없애면 독자는 원본으로 갈 길을 잃는다.
test('여기 없는 노트면 원래 주소로 나간다', () => {
  const html = inlineToHtml(parseInline('[글](https://github.com/juniqlim/note/blob/master/programming/gone.md)', 'x.md'), ctx);
  assert.match(html, /href="https:\/\/github.com\/juniqlim\/note\/blob\/master\/programming\/gone.md"/);
  assert.doesNotMatch(html, /class="dead"/);
});

// 상대경로는 이 저장소 안에서만 뜻이 통하므로 밖으로 내보낼 수 없다.
test('여기 없는 상대경로 링크는 글자로 남는다', () => {
  const html = inlineToHtml(parseInline('[글](../ai-agent/gone.md)', 'programming/x.md'), ctx);
  assert.match(html, /class="dead"/);
});

test('../ 는 상위 폴더로 풀린다', () => {
  const r = resolveHref('../alan/there.md', 'programming/ward/here.md');
  assert.equal(r.href, 'programming/alan/there.md');
});

// 목차처럼 같은 글 안의 제목으로 가는 링크는 새 창을 띄우면 안 된다.
test('# 링크는 같은 페이지 안에서 움직인다', () => {
  const html = inlineToHtml(parseInline('[문제](#1-문제-problem)', 'x.md'), ctx);
  assert.equal(html, '<a href="#1-문제-problem">문제</a>');
});
