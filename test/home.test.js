import { test } from 'node:test';
import assert from 'node:assert/strict';
import { renderHome } from '../site/render.js';

// 이 사이트는 juniq.im 에서 온다. 온 길로 돌아갈 수 있어야 한다.
test('머리말에 홈으로 돌아가는 링크가 있다', () => {
  const html = renderHome({ site: { title: '나의 노트', tagline: '' }, folders: [], notes: [] });

  assert.match(html, /<a class="home" href="https:\/\/juniq\.im\/">← juniq<\/a>/);
});
