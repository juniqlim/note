import { test } from 'node:test';
import assert from 'node:assert/strict';
import { renderHome } from '../site/render.js';

// 검색 결과는 본문을 대신하지 않고 머리말 아래에 겹쳐 뜬다 — 읽던 자리를 잃지 않게.
test('검색 결과 패널은 고정 머리말 안에 있다', () => {
  const html = renderHome({ site: { title: '나의 노트', tagline: '' }, folders: [], notes: [] });

  const header = html.match(/<header[\s\S]*?<\/header>/)[0];
  assert.match(header, /<div id="search-results" hidden><\/div>/);
});
