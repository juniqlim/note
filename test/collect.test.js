import { test } from 'node:test';
import assert from 'node:assert/strict';
import { isExcluded, groupOf } from '../site/collect.js';

// 뺄 것이 폴더 하나면 그 안의 것을 다 적을 필요가 없다.
// investment/daily-news 204편을 한 줄로 뺀다.
test('폴더를 적으면 그 안의 것이 다 빠진다', () => {
  const rules = ['investment/daily-news'];
  assert.equal(isExcluded('investment/daily-news/2026-02-10.md', rules), true);
  assert.equal(isExcluded('investment/netflix/netflix.md', rules), false);
});

test('파일 하나만 적을 수도 있다', () => {
  const rules = ['programming/the-ai-cloud.md'];
  assert.equal(isExcluded('programming/the-ai-cloud.md', rules), true);
  assert.equal(isExcluded('programming/the-ai-cloud-2.md', rules), false);
});

// sources 든 report 든 이름이 같은 폴더가 종목마다 있다. 하나씩 적을 수 없다.
test('폴더 이름만으로도 뺄 수 있다', () => {
  const rules = ['**/sources'];
  assert.equal(isExcluded('investment/SOil/sources/x.md', rules), true);
  assert.equal(isExcluded('investment/SOil/soil.md', rules), false);
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
