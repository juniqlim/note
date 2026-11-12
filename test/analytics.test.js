import { test } from 'node:test';
import assert from 'node:assert/strict';
import { renderHome } from '../site/render.js';

// juniq.im 의 모든 사이트는 같은 GA4 측정 ID 로 방문을 센다.
test('머리말에 구글 애널리틱스 태그가 있다', () => {
  const html = renderHome({ site: { title: 't', tagline: '' }, folders: [], notes: [] });

  assert.match(html, /<script async src="https:\/\/www\.googletagmanager\.com\/gtag\/js\?id=G-T12BGYGXSG"><\/script>/);
  assert.match(html, /gtag\('config','G-T12BGYGXSG'\)/);
});
