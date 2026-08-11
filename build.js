#!/usr/bin/env node
// md → docs/ 정적 사이트. 의존성 없음. 실행: node build.js
import { readFile, writeFile, mkdir, rm, cp } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { parseNote, blocksToText } from './site/md.js';
import { renderHome, renderChanges, renderNote, noteUrl } from './site/render.js';

const root = path.dirname(fileURLToPath(import.meta.url));
const out = path.join(root, 'docs');

const cfg = JSON.parse(await readFile(path.join(root, 'site.json'), 'utf8'));
const labelOf = (dir) => (cfg.folders.find((f) => f.dir === dir) || {}).label || dir;

// 이 저장소에는 아직 안 익은 글도 있다. site.json 의 notes 에 적은 것만 낸다.
// 적힌 순서가 곧 보이는 순서다. 이름이 틀리면 빌드가 멈춘다 — 조용히 빠지는 것보다 낫다.
const notes = [];
for (const p of cfg.notes) {
  const note = parseNote(p, await readFile(path.join(root, p), 'utf8'));
  note.slug = cfg.slugs[p] || note.meta.slug || '';
  note.text = blocksToText(note.blocks);
  notes.push(note);
}

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
