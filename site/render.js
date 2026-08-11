// AST → HTML 문자열. 스타일은 style.css 의 클래스가 담당한다.

const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const attr = (s) => esc(s).replace(/'/g, '&#39;');

// 노트 하나의 페이지 경로. notes.json 에서 slug 를 주면 그것을 쓴다 (한글 파일명 → ASCII URL).
export function noteUrl(note) {
  const dir = note.path.split('/').slice(0, -1).join('/');
  const name = note.slug || note.path.split('/').pop().replace(/\.md$/, '');
  return ['notes', ...dir.split('/'), name + '.html'].map(encodeURIComponent).join('/');
}

// 내부 링크는 md 경로 → 실제 페이지 경로로. 대상이 없으면 링크를 풀어 텍스트로 남긴다.
export function inlineToHtml(nodes, ctx) {
  return (nodes || []).map((n) => {
    if (n.t === 'text') return esc(n.v);
    if (n.t === 'br') return '<br>';
    if (n.t === 'strong') return '<strong>' + inlineToHtml(n.c, ctx) + '</strong>';
    if (n.t === 'em') return '<em>' + inlineToHtml(n.c, ctx) + '</em>';
    if (n.t === 'code') return '<code>' + esc(n.v) + '</code>';
    if (n.t === 'link') {
      const inner = inlineToHtml(n.c, ctx);
      if (n.internal) {
        const url = ctx.urlOf(n.href);
        if (url) return '<a class="internal" href="' + attr(ctx.base + url) + '">' + inner + '</a>';
        // 여기 없는 노트. 원래 주소가 있으면 그리로 보낸다 — 링크를 없애면 원본으로 갈 길이 끊긴다.
        if (n.raw && /^https?:/.test(n.raw)) {
          return '<a class="ext" href="' + attr(n.raw) + '" target="_blank" rel="noopener">' + inner + ' \u2197</a>';
        }
        return '<span class="dead">' + inner + '</span>';
      }
      return '<a class="ext" href="' + attr(n.href) + '" target="_blank" rel="noopener">' + inner + ' \u2197</a>';
    }
    return '';
  }).join('');
}

function itemsToHtml(list, ctx) {
  return list.map((it) => '<li>' + inlineToHtml(it.inline, ctx)
    + (it.children && it.children.length ? '<ul>' + itemsToHtml(it.children, ctx) + '</ul>' : '')
    + '</li>').join('');
}

function blockToHtml(b, ctx) {
  switch (b.type) {
    case 'heading': {
      const t = 'h' + Math.min(4, b.level);
      return '<' + t + ' id="' + attr(b.id) + '">' + inlineToHtml(b.inline, ctx) + '</' + t + '>';
    }
    case 'p': return '<p>' + inlineToHtml(b.inline, ctx) + '</p>';
    case 'ul': return '<ul>' + itemsToHtml(b.items, ctx) + '</ul>';
    case 'ol': return '<ol>' + itemsToHtml(b.items, ctx) + '</ol>';
    case 'quote': return '<blockquote>' + b.blocks.map((c) => blockToHtml(c, ctx)).join('') + '</blockquote>';
    case 'code': return '<pre><code>' + esc(b.code) + '</code></pre>';
    case 'hr': return '<hr>';
    case 'table': {
      const head = '<tr>' + b.head.map((c) => '<th>' + inlineToHtml(c, ctx) + '</th>').join('') + '</tr>';
      const rows = b.rows.map((r) => '<tr>' + r.map((c) => '<td>' + inlineToHtml(c, ctx) + '</td>').join('') + '</tr>').join('');
      return '<div class="scroll-x"><table><thead>' + head + '</thead><tbody>' + rows + '</tbody></table></div>';
    }
    default: return '';
  }
}

function shell({ title, site, base, body, bodyClass = '' }) {
  return `<!DOCTYPE html>
<html lang="ko" data-theme="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${esc(title)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@400;600&family=IBM+Plex+Mono:wght@400;500&family=Noto+Sans+KR:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="${base}style.css">
<script>try{if(localStorage.getItem('theme')==='light')delete document.documentElement.dataset.theme}catch(e){}</script>
</head>
<body class="${bodyClass}">
<header class="site-head">
  <div class="head-left">
    <a class="brand" href="${base}index.html">${esc(site.title)}</a>
    <nav>
      <a href="${base}index.html">주제</a>
      <a href="${base}changes.html">최근 변경</a>
      ${site.sibling ? `<a class="ext" href="${attr(site.sibling.url)}">${esc(site.sibling.label)} ↗</a>` : ''}
    </nav>
  </div>
  <div class="head-right">
    <input id="q" type="search" placeholder="검색 — 제목·본문" autocomplete="off" data-base="${base}">
    <button id="theme" type="button">라이트</button>
  </div>
</header>
<div id="search-results" hidden></div>
<main id="page">
${body}
</main>
<script src="${base}app.js" defer></script>
</body>
</html>
`;
}

export function renderHome({ site, folders, notes, base = '' }) {
  const groups = folders.map((f) => {
    const list = notes.filter((n) => n.folder === f.dir);
    if (!list.length) return '';
    const items = list.map((n) => `<a class="row" href="${attr(base + noteUrl(n))}">
        <span class="row-title">${esc(n.title)}${n.source && n.source.translation ? '<span class="badge">번역</span>' : ''}</span>
        ${n.summary ? '<span class="row-sum">' + esc(n.summary) + '</span>' : ''}
      </a>`).join('');
    return `<section class="group">
      <div class="group-head"><h2>${esc(f.label)}</h2><span class="mono dim">${esc(f.dir)} · ${list.length}</span></div>
      <div class="rows">${items}</div>
    </section>`;
  }).join('');

  return shell({
    title: site.title, site, base, bodyClass: 'narrow',
    body: `<p class="tagline">${esc(site.tagline)}</p>
<p class="mono dim">${esc(site.repo)} · 노트 ${notes.length}편</p>
<div class="groups">${groups}</div>`,
  });
}

export function renderChanges({ site, notes, labelOf, base = '' }) {
  const rows = notes.slice().sort((a, b) => (b.date || '').localeCompare(a.date || ''))
    .map((n) => `<a class="change" href="${attr(base + noteUrl(n))}">
      <span class="mono dim">${esc(n.date || '날짜 없음')}</span>
      <span class="change-title">${esc(n.title)}</span>
      <span class="mono dim">${esc(labelOf(n.folder))}</span>
    </a>`).join('');

  return shell({
    title: '최근 변경 · ' + site.title, site, base, bodyClass: 'narrow',
    body: `<h1>최근 변경</h1>
<p class="lede">파일명의 날짜 접두어를 씁니다. 실제 고침 이력은 git 커밋에서 채워야 합니다.</p>
<div class="changes">${rows}</div>`,
  });
}

export function renderNote({ site, note, notes, labelOf, base }) {
  const byPath = new Map(notes.map((n) => [n.path, n]));
  const ctx = { base, urlOf: (p) => (byPath.has(p) ? noteUrl(byPath.get(p)) : null) };

  const toc = note.toc.map((h) =>
    `<a class="toc-${h.level}" href="#${attr(h.id)}">${esc(h.text)}</a>`).join('');

  const source = note.source ? `<div class="source">
    <span class="kicker">${note.source.translation ? '번역' : '출처'}</span>
    ${note.source.note ? '<span class="source-note">' + esc(note.source.note) + '</span>' : ''}
    <a href="${attr(note.source.url)}" target="_blank" rel="noopener">${esc(note.source.label)} \u2197</a>
  </div>` : '';

  const backlinks = note.backlinks.length ? `<div class="backlinks">
    <span class="kicker">이 노트를 참조한 노트</span>
    ${note.backlinks.map((p) => '<a href="' + attr(base + noteUrl(byPath.get(p))) + '">' + esc(byPath.get(p).title) + '</a>').join('')}
  </div>` : '';

  const body = note.blocks.map((b) => blockToHtml(b, ctx)).join('\n');

  return shell({
    title: note.title + ' · ' + site.title, site, base, bodyClass: 'note-page',
    body: `<aside class="rail">
  <a class="mono back" href="${base}index.html">← ${esc(labelOf(note.folder))}</a>
  <span class="kicker">Contents</span>
  <nav class="toc">${toc}</nav>
  <div class="stats mono">
    <span>${esc((note.date ? note.date + ' · ' : '') + '읽기 ' + note.minutes + '분')}</span>
    <span>나가는 링크 ${note.links.length} · 백링크 ${note.backlinks.length}</span>
  </div>
</aside>
<article>
  <h1>${esc(note.title)}</h1>
  ${note.titleOriginal ? '<p class="orig mono">' + esc(note.titleOriginal) + '</p>' : ''}
  ${note.subtitle ? '<p class="subtitle">' + esc(note.subtitle) + '</p>' : ''}
  ${source}
  ${body}
  ${backlinks}
</article>`,
  });
}
