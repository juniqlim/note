#!/usr/bin/env node
// md → docs/ 정적 사이트. 의존성 없음. 실행: node build.js
import { readFile, writeFile, mkdir, rm, cp, readdir } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { execFileSync } from 'node:child_process';
import { parseNote, blocksToText } from './site/md.js';
import { readHistory } from './site/history.js';
import { renderHome, renderChanges, renderNote, noteUrl } from './site/render.js';

const root = path.dirname(fileURLToPath(import.meta.url));
const out = path.join(root, 'docs');

const cfg = JSON.parse(await readFile(path.join(root, 'site.json'), 'utf8'));
const labelOf = (dir) => (cfg.folders.find((f) => f.dir === dir) || {}).label || dir;

// 쓴 날·고친 날은 git 이 안다. quotePath 를 끄지 않으면 한글 경로가 \xxx 로 나온다.
let history = new Map();
try {
  history = readHistory(execFileSync('git',
    ['-c', 'core.quotePath=false', 'log', '--format=%cs', '--name-status', '--reverse', '-M'],
    { cwd: root, encoding: 'utf8', maxBuffer: 64 * 1024 * 1024 }));
} catch {
  console.warn('git 이력을 읽지 못했다 — 날짜 없이 낸다.');
}

// folders 에 적은 폴더를 훑는다. 하위 폴더는 따라 들어가지 않는다 —
// kent/ ward/ 처럼 갈래로 삼을 것만 folders 에 따로 적어 라벨을 준다.
// 그래서 md 를 넣기만 하면 목록에 뜬다. 안 낼 것만 exclude 에 적는다.
const notes = [];
for (const f of cfg.folders) {
  const entries = await readdir(path.join(root, f.dir), { withFileTypes: true }).catch(() => []);
  for (const e of entries) {
    if (!e.isFile() || !e.name.endsWith('.md')) continue;
    const p = f.dir + '/' + e.name;
    if (cfg.exclude.includes(p)) continue;
    const note = parseNote(p, await readFile(path.join(root, p), 'utf8'));
    const when = history.get(p) || {};
    note.folder = f.dir;
    note.slug = cfg.slugs[p] || note.meta.slug || '';
    // 프론트매터에 적은 날이 있으면 그것이 먼저다 — 다른 곳에서 옮겨 온 글이 있다.
    note.date = note.meta.date || when.created || note.date;
    note.updated = when.updated || '';
    note.text = blocksToText(note.blocks);
    notes.push(note);
  }
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
