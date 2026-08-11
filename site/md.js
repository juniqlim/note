// md → AST 변환기. 이 repo의 md 관례에 맞춘 최소 파서.
// 지원: h1~h4, 단락(줄끝 두 칸 = 줄바꿈), ul/ol(2칸 들여쓰기 중첩), 인용,
//       코드펜스, 표, 수평선, **강조** *기울임* `코드` [링크](url), 프론트매터.

const REPO_BLOB = /^https?:\/\/github\.com\/[^/]+\/[^/]+\/blob\/[^/]+\/(.+)$/;

export function decodeEntities(s) {
  return s.replace(/&gt;/g, ">").replace(/&lt;/g, "<").replace(/&amp;/g, "&").replace(/&quot;/g, '"');
}

// raw: 원래 주소. 가리킨 노트가 여기 없을 때 그리로 내보내기 위해 남겨 둔다.
export function resolveHref(href, fromPath) {
  const m = href.match(REPO_BLOB);
  if (m) return { href: decodeURIComponent(m[1]), internal: true, raw: href };
  if (/^\.{0,2}\/?[^:]+\.md(#.*)?$/.test(href) && !/^https?:/.test(href)) {
    const dir = fromPath.split("/").slice(0, -1).join("/");
    const clean = href.replace(/^\.\//, "");
    return { href: clean.startsWith("/") ? clean.slice(1) : (dir ? dir + "/" + clean : clean), internal: true, raw: href };
  }
  return { href, internal: false, raw: href };
}

export function parseInline(text, fromPath) {
  const out = [];
  let rest = decodeEntities(text);
  const push = (node) => { if (node) out.push(node); };
  // 그림(!)이 링크보다 뒤에 있어도 된다. 정규식은 더 앞에서 시작하는 매치를 고른다.
  const re = /(\*\*([^*]+)\*\*)|(`([^`]+)`)|(\*([^*\n]+)\*)|(\[([^\]]*)\]\(([^)\s]+)\))|(https?:\/\/[^\s)<>"']+)|(!\[([^\]]*)\]\(([^)\s]+)\))/;
  while (rest.length) {
    const m = rest.match(re);
    if (!m) { push({ t: "text", v: rest }); break; }
    if (m.index > 0) push({ t: "text", v: rest.slice(0, m.index) });
    if (m[1]) push({ t: "strong", c: parseInline(m[2], fromPath) });
    else if (m[3]) push({ t: "code", v: m[4] });
    else if (m[5]) push({ t: "em", c: parseInline(m[6], fromPath) });
    else if (m[7]) {
      const r = resolveHref(m[9], fromPath);
      push({ t: "link", href: r.href, internal: r.internal, raw: r.raw, c: parseInline(m[8] || m[9], fromPath) });
    } else if (m[10]) {
      const r = resolveHref(m[10], fromPath);
      push({ t: "link", href: r.href, internal: r.internal, raw: r.raw, c: [{ t: "text", v: shortUrl(m[10]) }] });
    } else if (m[11]) {
      push({ t: "img", src: m[13], alt: m[12] });
    }
    rest = rest.slice(m.index + m[0].length);
  }
  return out;
}

function shortUrl(u) {
  return u.replace(/^https?:\/\//, "").replace(/\/$/, "");
}

export function slugify(text) {
  return text.trim().toLowerCase().replace(/[^\p{L}\p{N}]+/gu, "-").replace(/^-|-$/g, "");
}

function splitFrontmatter(src) {
  const lines = src.replace(/\r\n/g, "\n").split("\n");
  if (lines[0] !== "---") return { meta: {}, body: src.replace(/\r\n/g, "\n") };
  const end = lines.indexOf("---", 1);
  if (end < 0) return { meta: {}, body: src.replace(/\r\n/g, "\n") };
  const meta = {};
  lines.slice(1, end).forEach((l) => {
    const i = l.indexOf(":");
    if (i > 0) meta[l.slice(0, i).trim()] = l.slice(i + 1).trim();
  });
  return { meta, body: lines.slice(end + 1).join("\n") };
}

function parseListBlock(lines, ordered, fromPath) {
  const items = [];
  lines.forEach((raw) => {
    const indent = raw.match(/^\s*/)[0].replace(/\t/g, "  ").length;
    const text = raw.replace(/^\s*(?:[*-]|\d+\.)\s+/, "");
    const node = { inline: parseInline(text, fromPath), children: [] };
    if (indent >= 2 && items.length) {
      let parent = items[items.length - 1];
      while (indent >= 4 && parent.children.length) parent = parent.children[parent.children.length - 1];
      parent.children.push(node);
    } else items.push(node);
  });
  return { type: ordered ? "ol" : "ul", items };
}

export function parseBlocks(body, fromPath) {
  const lines = body.split("\n");
  const blocks = [];
  let i = 0;
  const isList = (l) => /^\s*(?:[*-]|\d+\.)\s+/.test(l);
  while (i < lines.length) {
    const line = lines[i];
    if (!line.trim()) { i++; continue; }
    let m;
    if ((m = line.match(/^```\s*(\S*)/))) {
      const lang = m[1] || "";
      const buf = [];
      i++;
      while (i < lines.length && !/^```/.test(lines[i])) buf.push(lines[i++]);
      i++;
      blocks.push({ type: "code", lang, code: buf.join("\n") });
      continue;
    }
    if ((m = line.match(/^(#{1,4})\s+(.*)$/))) {
      const text = m[2].replace(/\s*#*\s*$/, "");
      blocks.push({ type: "heading", level: m[1].length, text: decodeEntities(text), id: slugify(text), inline: parseInline(text, fromPath) });
      i++;
      continue;
    }
    if (/^(-{3,}|\*{3,}|_{3,})\s*$/.test(line)) { blocks.push({ type: "hr" }); i++; continue; }
    // 옛 노트는 GitHub 웹에서 붙여넣은 <img> 를 그대로 갖고 있다. 이것만은 알아본다.
    if (/^<img\s[^>]*>\s*$/i.test(line)) {
      blocks.push({
        type: "img",
        src: (line.match(/src="([^"]*)"/i) || [])[1] || "",
        alt: (line.match(/alt="([^"]*)"/i) || [])[1] || "",
      });
      i++;
      continue;
    }
    if (/^\s*\|.*\|\s*$/.test(line) && /^\s*\|?[\s:|-]+\|[\s:|-]*$/.test(lines[i + 1] || "")) {
      const cells = (l) => l.trim().replace(/^\||\|$/g, "").split("|").map((c) => parseInline(c.trim(), fromPath));
      const head = cells(line);
      i += 2;
      const rows = [];
      while (i < lines.length && /^\s*\|.*\|\s*$/.test(lines[i])) rows.push(cells(lines[i++]));
      blocks.push({ type: "table", head, rows });
      continue;
    }
    if (/^\s*>/.test(line)) {
      const buf = [];
      while (i < lines.length && /^\s*>/.test(lines[i])) buf.push(lines[i++].replace(/^\s*>\s?/, ""));
      blocks.push({ type: "quote", blocks: parseBlocks(buf.join("\n"), fromPath) });
      continue;
    }
    if (isList(line)) {
      const buf = [];
      const ordered = /^\s*\d+\.\s/.test(line);
      while (i < lines.length && (isList(lines[i]) || (lines[i].trim() && /^\s{2,}\S/.test(lines[i]) && !isList(lines[i]) && false))) buf.push(lines[i++]);
      blocks.push(parseListBlock(buf, ordered, fromPath));
      continue;
    }
    // 단락: 빈 줄/블록 시작 전까지. 줄 끝 두 칸 = 줄바꿈
    const buf = [];
    while (i < lines.length && lines[i].trim() && !isList(lines[i]) && !/^(#{1,4}\s|```|\s*>|\s*\||<img\s)/.test(lines[i]) && !/^(-{3,}|\*{3,})\s*$/.test(lines[i])) {
      buf.push(lines[i]);
      i++;
    }
    if (!buf.length) { i++; continue; }
    const inline = [];
    buf.forEach((l, idx) => {
      inline.push(...parseInline(l.replace(/\s+$/, ""), fromPath));
      if (idx < buf.length - 1) inline.push(/ {2}$/.test(l) ? { t: "br" } : { t: "text", v: " " });
    });
    blocks.push({ type: "p", inline });
  }
  return blocks;
}

// 한쪽이 다른 쪽을 그대로 품고 있으면 같은 말이다. "나는 TDD 왜하는가." 와 "TDD 왜하는가?"
const echoes = (a, b) => {
  const bare = (s) => s.replace(/[\s.?!·,]/g, "");
  const [x, y] = [bare(a), bare(b)];
  return !!x && !!y && (x.includes(y) || y.includes(x));
};

// 노트 하나를 사이트가 쓰는 형태로 변환
export function parseNote(path, src) {
  const { meta, body } = splitFrontmatter(src);
  const lines = body.split("\n");
  const h1At = lines.findIndex((l) => /^#\s+/.test(l));
  const preamble = h1At > 0 ? lines.slice(0, h1At).filter((l) => l.trim()) : [];
  const rest = h1At >= 0 ? lines.slice(h1At + 1).join("\n") : body;
  const blocks = parseBlocks(rest, path);
  const firstIsH2 = blocks[0] && blocks[0].type === "heading" && blocks[0].level === 2;

  // 오래된 노트에는 H1 없이 ## 로 시작하는 것이 있다. 그것이 제목이다 —
  // 그냥 두면 파일명이 제목이 되어 목록에 ward-interview-clay 같은 것이 뜬다.
  let subtitle = meta.subtitle || "";
  let rawTitle;
  if (h1At >= 0) {
    rawTitle = lines[h1At].replace(/^#\s+/, "").trim();
    // 제목 아래 첫 ## 가 짧으면 부제로 올린다. 본문에서는 빼되,
    // 제목을 되풀이할 뿐이면 부제로 쓰지 않는다 — 목록에 같은 말이 두 번 나온다.
    if (!subtitle && firstIsH2 && blocks[0].text.length <= 40) {
      const lead = blocks.shift().text;
      subtitle = echoes(rawTitle, lead) ? "" : lead;
    }
  } else if (firstIsH2) {
    rawTitle = blocks.shift().text;
  } else {
    rawTitle = path.split("/").pop().replace(/\.md$/, "");
  }

  // 관례에서 벗어난 옛 노트는 파서가 알아맞히게 두지 않고 직접 적는다.
  if (meta.title) rawTitle = meta.title;

  // 제목: "한글 (English)" → 원제 분리 / " - 부제" → 부제 분리.
  // 하이픈이 여럿이면 어디서 갈라야 할지 알 수 없으니 통째로 제목이다.
  let title = rawTitle, titleOriginal = "";
  const dash = title.split(/\s+[-–—]\s+/);
  if (dash.length === 2) { title = dash[0].trim(); subtitle = subtitle || dash[1].trim(); }
  const paren = title.match(/^(.*?)\s*\(([^)]+)\)\s*$/);
  if (paren && /[A-Za-z]/.test(paren[2])) { title = paren[1].trim(); titleOriginal = paren[2].trim(); }

  // 출처: H1 위의 URL 줄 + 설명 줄 (또는 프론트매터 source/translation)
  let source = null;
  const preUrl = preamble.find((l) => /https?:\/\//.test(l));
  const preNote = preamble.filter((l) => !/^https?:\/\/\S+\s*$/.test(l.trim())).join(" ").trim();
  if (meta.source || meta.translation || preUrl) {
    const url = (meta.source || meta.translation || (preUrl || "").match(/https?:\/\/\S+/)[0]).trim();
    source = { url, label: shortUrl(url), note: meta.sourceNote || preNote, translation: /번역/.test(preNote + (meta.sourceNote || "")) || !!meta.translation };
  }

  const toc = blocks.filter((b) => b.type === "heading" && b.level >= 2 && b.level <= 3)
    .map((b) => ({ id: b.id, text: b.text, level: b.level }));
  const summary = meta.summary || autoSummary(blocks, title);
  const links = collectLinks(blocks).filter((l) => l.internal).map((l) => l.href);
  const chars = body.replace(/\s/g, "").length;
  const dateMatch = path.match(/(\d{4})-(\d{2})-(\d{2})/);

  return {
    path, meta, title, titleOriginal, subtitle, source, blocks, toc, summary, links,
    folder: path.split("/")[0],
    slug: path.split("/").pop().replace(/\.md$/, "").replace(/^\d{4}-\d{2}-\d{2}-/, ""),
    date: meta.date || (dateMatch ? dateMatch[0] : ""),
    updated: meta.updated || "",
    minutes: Math.max(1, Math.round(chars / 500)),
    words: chars,
  };
}

// 요약: 문장 끝(.!?…)을 만나거나 ~110자가 될 때까지 바로 다음 불롟/단락을 이어 붙인다.
function autoSummary(blocks, title) {
  const piece = (b) => {
    if (b.type === "p") return inlineToText(b.inline).trim();
    if (b.type === "ul" || b.type === "ol") return b.items.map((it) => inlineToText(it.inline).trim()).filter(Boolean).join(" · ");
    if (b.type === "quote") return blocksToText(b.blocks).replace(/\s+/g, " ").trim();
    return "";
  };
  const start = blocks.findIndex((b) => piece(b));
  if (start < 0) return "";
  let text = "";
  for (let i = start; i < blocks.length; i++) {
    const b = blocks[i];
    if (b.type === "heading" || b.type === "code" || b.type === "table") break;
    const p = piece(b);
    if (!p) continue;
    text = text ? text + " " + p : p;
    const done = text.split(/(?<=[.!?…])\s+/)[0].trim();
    if (/[.!?…]/.test(text) || text.length >= 110) { text = done.length >= 15 ? done : text; break; }
  }
  text = text.trim();
  if (title && text.replace(/[\s.]/g, "").startsWith(title.replace(/[\s.]/g, "")) && text.length < title.length + 6) return "";
  if (text.length <= 110) return text;
  const cut = text.slice(0, 110);
  const lastSpace = cut.lastIndexOf(" ");
  return (lastSpace > 60 ? cut.slice(0, lastSpace) : cut) + "…";
}

export function inlineToText(nodes) {
  return nodes.map((n) => (n.t === "text" ? n.v : n.t === "code" ? n.v : n.t === "br" ? " " : n.c ? inlineToText(n.c) : "")).join("");
}

export function blocksToText(blocks) {
  return blocks.map((b) => {
    if (b.type === "p" || b.type === "heading") return inlineToText(b.inline);
    if (b.type === "ul" || b.type === "ol") return b.items.map((it) => inlineToText(it.inline)).join(" ");
    if (b.type === "quote") return blocksToText(b.blocks);
    if (b.type === "code") return b.code;
    if (b.type === "table") return b.rows.map((r) => r.map(inlineToText).join(" ")).join(" ");
    return "";
  }).join("\n");
}

function collectLinks(blocks, acc = []) {
  const walkInline = (nodes) => nodes.forEach((n) => {
    if (n.t === "link") acc.push(n);
    if (n.c) walkInline(n.c);
  });
  blocks.forEach((b) => {
    if (b.inline) walkInline(b.inline);
    if (b.items) b.items.forEach((it) => { walkInline(it.inline); (it.children || []).forEach((c) => walkInline(c.inline)); });
    if (b.blocks) collectLinks(b.blocks, acc);
    if (b.head) { b.head.forEach(walkInline); b.rows.forEach((r) => r.forEach(walkInline)); }
  });
  return acc;
}
