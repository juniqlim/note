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
    if (n.t === 'img') return imgToHtml(n);
    return '';
  }).join('');
}

// \uadf8\ub9bc\uc740 \uc6d0\ub798 \uc788\ub358 \uc790\ub9ac(raw.githubusercontent.com \ub4f1)\uc5d0\uc11c \uadf8\ub300\ub85c \uac00\uc838\uc628\ub2e4.
function imgToHtml(n) {
  return '<img src="' + attr(n.src) + '" alt="' + attr(n.alt || '') + '" loading="lazy">';
}

function itemsToHtml(list, ctx) {
  return list.map((it) => '<li>' + inlineToHtml(it.inline, ctx)
    + (it.children && it.children.length ? '<ul>' + itemsToHtml(it.children, ctx) + '</ul>' : '')
    + '</li>').join('');
}

export function blocksToHtml(blocks, ctx) {
  return blocks.map((b) => blockToHtml(b, ctx)).join('\n');
}

function blockToHtml(b, ctx) {
  switch (b.type) {
    case 'img': return '<p class="figure">' + imgToHtml(b) + '</p>';
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
      <a href="${base}index.html">노트</a>
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

// 다 보여주는 목록이다. 제목만 놓는다 — 요약까지 붙이면 길어져서 아무도 훑지 않는다.
export function renderHome({ site, folders, notes, base = '' }) {
  const groups = folders.map((f) => {
    const list = notes.filter((n) => n.folder === f.dir);
    if (!list.length) return '';
    // 부제까지 놓는다. "도메인 주도 설계" 가 둘이면 제목만으로는 고를 수 없다.
    const items = list.map((n) => `<a class="line" href="${attr(base + noteUrl(n))}">
        <span class="line-title">${esc(n.title)}${n.source && n.source.translation ? '<span class="badge">번역</span>' : ''}</span>
        ${n.subtitle ? '<span class="line-sub">' + esc(n.subtitle) + '</span>' : ''}
        <span class="mono dim">${esc(n.date || '')}</span>
      </a>`).join('');
    return `<section class="group">
      <div class="group-head"><h2>${esc(f.label)}</h2><span class="mono dim">${list.length}</span></div>
      <div class="lines">${items}</div>
    </section>`;
  }).join('');

  return shell({
    title: site.title, site, base, bodyClass: 'narrow',
    body: `<p class="tagline">${esc(site.tagline)}</p>
<p class="mono dim">${esc(site.repo)} · 노트 ${notes.length}편</p>
<div class="groups">${groups}</div>`,
  });
}

// 변경 목록이니 고친 날로 줄 세운다. 쓴 날은 목록이 맡는다.
export function renderChanges({ site, notes, labelOf, base = '' }) {
  const rows = notes.slice()
    .sort((a, b) => (b.updated || b.date || '').localeCompare(a.updated || a.date || ''))
    .map((n) => `<a class="change" href="${attr(base + noteUrl(n))}">
      <span class="mono dim">${esc(n.updated || n.date)}</span>
      <span class="change-title">${esc(n.title)}</span>
      <span class="mono dim">${esc(labelOf(n.folder))}</span>
    </a>`).join('');

  return shell({
    title: '최근 변경 · ' + site.title, site, base, bodyClass: 'narrow',
    body: `<h1>최근 변경</h1>
<p class="lede">git 커밋 이력에서 가져온 고친 날입니다.</p>
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

  const body = blocksToHtml(note.blocks, ctx);

  return shell({
    title: note.title + ' · ' + site.title, site, base, bodyClass: 'note-page',
    body: `<aside class="rail">
  <a class="mono back" href="${base}index.html">← ${esc(labelOf(note.folder))}</a>
  <span class="kicker">Contents</span>
  <nav class="toc">${toc}</nav>
  <div class="stats mono">
    <span>${esc((note.date ? '쓴 날 ' + note.date + ' · ' : '') + '읽기 ' + note.minutes + '분')}</span>
    ${note.updated && note.updated !== note.date ? '<span>고친 날 ' + esc(note.updated) + '</span>' : ''}
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
