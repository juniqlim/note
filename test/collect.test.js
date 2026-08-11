import { test } from 'node:test';
import assert from 'node:assert/strict';
import { matches, groupOf } from '../site/collect.js';

// 저장소에는 마음대로 올린다. 사이트에는 적은 것만 낸다.
// 적기를 잊으면 안 나갈 뿐이지만, 빼기를 잊으면 나가 버린다.
test('적은 파일만 낸다', () => {
  const rules = ['programming/why-tdd.md'];
  assert.equal(matches('programming/why-tdd.md', rules), true);
  assert.equal(matches('programming/안-익은-글.md', rules), false);
});

test('폴더를 적으면 그 안이 다 나간다', () => {
  const rules = ['programming/ward'];
  assert.equal(matches('programming/ward/ward-episodes.md', rules), true);
  assert.equal(matches('programming/ward/깊이/더.md', rules), true);
  assert.equal(matches('programming/why-tdd.md', rules), false);
});

// 이름이 같은 폴더가 종목마다 있다. 하나씩 적을 수 없다.
test('폴더 이름만으로도 고를 수 있다', () => {
  const rules = ['**/sources'];
  assert.equal(matches('investment/SOil/sources/x.md', rules), true);
  assert.equal(matches('investment/SOil/soil.md', rules), false);
});

test('아무것도 안 적으면 아무것도 안 나간다', () => {
  assert.equal(matches('programming/why-tdd.md', []), false);
});

// 깊은 폴더는 가장 가까운 갈래에 속한다. 종목마다 갈래를 만들면 섹션이 마흔 개가 된다.
const FOLDERS = [
  { dir: 'investment', label: '투자' },
  { dir: 'investment/warren', label: '투자 · 워런 버핏' },
  { dir: 'investment', label: '투자 · 기업 분석', deep: true },
];

test('가장 깊이 들어맞는 갈래가 이긴다', () => {
  assert.equal(groupOf('investment/warren/buffett-dcf.md', FOLDERS).label, '투자 · 워런 버핏');
});

test('바로 아래 파일은 얕은 갈래에 남는다', () => {
  assert.equal(groupOf('investment/투자판단모델.md', FOLDERS).label, '투자');
});

test('더 깊은 것은 훑는 갈래가 받는다', () => {
  assert.equal(groupOf('investment/netflix/netflix.md', FOLDERS).label, '투자 · 기업 분석');
  assert.equal(groupOf('investment/ai-agent/hynix/hynix.md', FOLDERS).label, '투자 · 기업 분석');
});

test('훑지 않는 갈래는 바로 아래 파일만 받는다', () => {
  const shallow = [{ dir: 'programming', label: '프로그래밍' }];
  assert.equal(groupOf('programming/why-tdd.md', shallow).label, '프로그래밍');
  assert.equal(groupOf('programming/kent/canon.md', shallow), null);
});
