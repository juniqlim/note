import { test } from 'node:test';
import assert from 'node:assert/strict';
import { parseNote } from '../site/md.js';

// 오래된 노트에는 H1 없이 ## 로 시작하는 것이 있다.
// 그대로 두면 파일명이 제목이 되어 목록에 ward-interview-clay 같은 것이 뜬다.
test('H1 이 없으면 첫 ## 을 제목으로 쓴다', () => {
  const note = parseNote('programming/ward/ward-interview-clay.md', '## 진흙과 함께 일하기\n본문이다.');
  assert.equal(note.title, '진흙과 함께 일하기');
});

test('그 ## 은 본문에서 빠진다 — 제목이 두 번 나오면 안 된다', () => {
  const note = parseNote('a.md', '## 진흙과 함께 일하기\n본문이다.');
  assert.equal(note.blocks[0].type, 'p');
});

test('H1 이 있으면 그것이 제목이다', () => {
  const note = parseNote('a.md', '# 진짜 제목\n## 첫 소제목\n본문');
  assert.equal(note.title, '진짜 제목');
});

// 제목도 H1 도 없으면 파일명 말고는 쓸 것이 없다.
test('H1 도 ## 도 없으면 파일명을 쓴다', () => {
  assert.equal(parseNote('programming/why-tdd.md', '그냥 본문').title, 'why-tdd');
});

// "제목 - 부제" 관례는 하이픈이 하나일 때만 뜻이 통한다.
// 여럿이면 어디서 갈라야 할지 알 수 없으니 통째로 제목이다.
test('하이픈이 하나면 뒤가 부제다', () => {
  const note = parseNote('a.md', '# 에이전틱 코딩 좀 더 잘하기 - 새로 배운 것\n본문');
  assert.equal(note.title, '에이전틱 코딩 좀 더 잘하기');
  assert.equal(note.subtitle, '새로 배운 것');
});

test('하이픈이 여럿이면 가르지 않는다', () => {
  const note = parseNote('a.md', '# ESSENTIALS - Canon TDD - Kent Beck | Craft 2025\n본문');
  assert.equal(note.title, 'ESSENTIALS - Canon TDD - Kent Beck | Craft 2025');
});

// 관례에서 벗어난 옛 노트는 파서가 알아맞히게 두지 않고 직접 적는다.
test('프론트매터 title 이 무엇보다 앞선다', () => {
  const note = parseNote('a.md', '---\ntitle: 프로그램을 다듬기\n---\n# 다른 제목\n본문');
  assert.equal(note.title, '프로그램을 다듬기');
});

// "나는 TDD 왜하는가." 아래 첫 ## 이 "TDD 왜하는가?" 면 목록에 같은 말이 두 번 나온다.
test('제목을 되풀이하는 부제는 버린다', () => {
  const note = parseNote('a.md', '# 나는 TDD 왜하는가.\n## TDD 왜하는가?\n본문');
  assert.equal(note.subtitle, '');
});

test('다른 말을 하는 부제는 남긴다', () => {
  const note = parseNote('a.md', '# 뽀모도로 회고\n## 3년치를 돌아보며\n본문');
  assert.equal(note.subtitle, '3년치를 돌아보며');
});
