#!/usr/bin/env node
// md → docs/ 정적 사이트. 의존성 없음. 실행: node build.js
import { readFile, writeFile, mkdir, rm, cp, readdir } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { execFileSync } from 'node:child_process';
import { parseNote, blocksToText } from './site/md.js';
import { readHistory } from './site/history.js';
import { isExcluded, groupOf } from './site/collect.js';
import { renderHome, renderChanges, renderNote, noteUrl } from './site/render.js';

const root = path.dirname(fileURLToPath(import.meta.url));
const out = path.join(root, 'docs');

const cfg = JSON.parse(await readFile(path.join(root, 'site.json'), 'utf8'));
const labelOf = (label) => label;

// 쓴 날·고친 날은 git 이 안다. quotePath 를 끄지 않으면 한글 경로가 \xxx 로 나온다.
let history = new Map();
try {
  history = readHistory(execFileSync('git',
    ['-c', 'core.quotePath=false', 'log', '--format=%cs', '--name-status', '--reverse', '-M'],
    { cwd: root, encoding: 'utf8', maxBuffer: 64 * 1024 * 1024 }));
} catch {
  console.warn('git 이력을 읽지 못했다 — 날짜 없이 낸다.');
}

// folders 에 적은 폴더가 갈래다. md 를 넣기만 하면 목록에 뜬다.
// 안 낼 것만 exclude 에 적는다. 자세한 규칙은 site/collect.js 에 있다.
const found = [];
const walk = async (dir) => {
  for (const e of await readdir(path.join(root, dir), { withFileTypes: true }).catch(() => [])) {
    if (e.isDirectory()) await walk(dir + '/' + e.name);
    else if (e.name.endsWith('.md')) found.push(dir + '/' + e.name);
  }
};
for (const top of [...new Set(cfg.folders.map((f) => f.dir.split('/')[0]))]) await walk(top);

const notes = [];
for (const p of found.map((f) => f.normalize('NFC')).sort()) {
  if (isExcluded(p, cfg.exclude)) continue;
  const group = groupOf(p, cfg.folders);
  if (!group) continue;
  const note = parseNote(p, await readFile(path.join(root, p), 'utf8'));
  const when = history.get(p) || {};
  note.folder = group.label;
  note.slug = cfg.slugs[p] || note.meta.slug || '';
  // 프론트매터에 적은 날이 있으면 그것이 먼저다 — 다른 곳에서 옮겨 온 글이 있다.
  note.date = note.meta.date || when.created || note.date;
  note.updated = when.updated || '';
  note.text = blocksToText(note.blocks);
  notes.push(note);
}
// 훑어 찾는 목록이다. 날짜순은 최근 변경이 맡는다.
notes.sort((a, b) => a.title.localeCompare(b.title, 'ko'));

// 백링크 — 여기 낸 노트끼리만 센다.
const back = new Map();
for (const n of notes) {
  for (const t of n.links) {
    if (!back.has(t)) back.set(t, []);
    if (!back.get(t).includes(n.path)) back.get(t).push(n.path);
  }
}
const known = new Set(notes.map((n) => n.path));
for (const n of notes) n.backlinks = (back.get(n.path) || []).filter((p) => known.has(p));

await rm(out, { recursive: true, force: true });
await mkdir(out, { recursive: true });

const write = async (rel, html) => {
  const dest = path.join(out, rel);
  await mkdir(path.dirname(dest), { recursive: true });
  await writeFile(dest, html, 'utf8');
};

await write('index.html', renderHome({ site: cfg.site, folders: cfg.folders, notes, base: '' }));
await write('changes.html', renderChanges({ site: cfg.site, notes, labelOf, base: '' }));

for (const note of notes) {
  const rel = decodeURIComponent(noteUrl(note));
  const base = '../'.repeat(rel.split('/').length - 1);
  await write(rel, renderNote({ site: cfg.site, note, notes, labelOf, base }));
}

// 검색 색인
await write('search.json', JSON.stringify(notes.map((n) => ({
  url: noteUrl(n),
  title: n.title,
  folder: labelOf(n.folder),
  summary: n.summary,
  text: n.text.replace(/\s+/g, ' ').slice(0, 4000),
}))));

await cp(path.join(root, 'site/style.css'), path.join(out, 'style.css'));
await cp(path.join(root, 'site/app.js'), path.join(out, 'app.js'));

// 빌드가 docs/를 지우므로 Pages 커스텀 도메인 표시를 매번 다시 쓴다.
if (cfg.site.domain) await writeFile(path.join(out, 'CNAME'), cfg.site.domain + '\n');

console.log('docs/ 생성 완료 — 노트 ' + notes.length + '편');
