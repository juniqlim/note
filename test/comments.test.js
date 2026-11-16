import { test } from 'node:test';
import assert from 'node:assert/strict';
import { renderNote } from '../site/render.js';

const note = { path: 'a.md', title: 'A', folder: 'programming', toc: [], blocks: [], links: [], backlinks: [], minutes: 1 };
const render = (site) => renderNote({ site, note, notes: [note], labelOf: () => 'p', base: '' });

// 댓글은 다른 저장소(juniqlim/comments)의 스크립트 하나로 붙는다.
test('댓글 스크립트가 정해져 있으면 노트 끝에 댓글 자리를 둔다', () => {
  const html = render({ title: 't', comments: 'https://x.dev/comments.js' });
  assert.match(html, /<div id="comments"><\/div>/);
  assert.match(html, /<script type="module" src="https:\/\/x\.dev\/comments\.js"><\/script>/);
});

test('정해져 있지 않으면 댓글이 없다', () => {
  assert.doesNotMatch(render({ title: 't' }), /id="comments"/);
});
