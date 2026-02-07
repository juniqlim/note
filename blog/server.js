const express = require("express");
const { marked } = require("marked");

const app = express();
const PORT = process.env.PORT || 3000;

// --- Configuration ---
const GITHUB_OWNER = process.env.GITHUB_OWNER || "juniqlim";
const GITHUB_REPO = process.env.GITHUB_REPO || "note";
const GITHUB_TOKEN = process.env.GITHUB_TOKEN || ""; // optional, for higher rate limits
const CACHE_TTL_MS = Number(process.env.CACHE_TTL_MS) || 10 * 60 * 1000; // 10 minutes

const CATEGORIES = [
  { id: "programming", label: "Programming", path: "programming" },
  { id: "investment", label: "Investment", path: "investment" },
];

// --- In-memory cache ---
const cache = {
  posts: null, // { data, fetchedAt }
  contents: new Map(), // path -> { data, fetchedAt }
};

function isFresh(entry) {
  return entry && Date.now() - entry.fetchedAt < CACHE_TTL_MS;
}

// --- GitHub API helpers ---
const API_BASE = "https://api.github.com";

function githubHeaders() {
  const h = { Accept: "application/vnd.github.v3+json", "User-Agent": "note-blog" };
  if (GITHUB_TOKEN) h.Authorization = `Bearer ${GITHUB_TOKEN}`;
  return h;
}

async function ghFetch(url) {
  const res = await fetch(url, { headers: githubHeaders() });
  if (!res.ok) throw new Error(`GitHub API ${res.status}: ${url}`);
  return res.json();
}

// Recursively list markdown files under a path
async function listMarkdownFiles(dirPath) {
  const url = `${API_BASE}/repos/${GITHUB_OWNER}/${GITHUB_REPO}/contents/${dirPath}`;
  const items = await ghFetch(url);
  const mdFiles = [];

  for (const item of items) {
    if (item.type === "file" && item.name.endsWith(".md")) {
      mdFiles.push(item);
    }
  }
  return mdFiles;
}

// Fetch raw markdown content
async function fetchFileContent(path) {
  if (isFresh(cache.contents.get(path))) {
    return cache.contents.get(path).data;
  }
  const url = `${API_BASE}/repos/${GITHUB_OWNER}/${GITHUB_REPO}/contents/${path}`;
  const data = await ghFetch(url);
  const content = Buffer.from(data.content, "base64").toString("utf-8");
  cache.contents.set(path, { data: content, fetchedAt: Date.now() });
  return content;
}

// --- Post parsing ---
function parsePostFromFile(item, categoryId) {
  const name = item.name.replace(/\.md$/, "");

  // Try to extract date from filename like "2023-03-15-title"
  const dateMatch = name.match(/^(\d{4}-\d{2}-\d{2})-(.+)$/);
  let date = null;
  let slug = name;
  let title = name;

  if (dateMatch) {
    date = dateMatch[1];
    slug = name;
    title = dateMatch[2].replace(/-/g, " ");
  } else {
    title = name.replace(/-/g, " ").replace(/_/g, " ");
  }

  // Capitalize first letter
  title = title.charAt(0).toUpperCase() + title.slice(1);

  return { slug, title, date, category: categoryId, path: item.path };
}

// --- Fetch all posts ---
async function getAllPosts() {
  if (isFresh(cache.posts)) return cache.posts.data;

  const allPosts = [];

  for (const cat of CATEGORIES) {
    try {
      const files = await listMarkdownFiles(cat.path);
      for (const f of files) {
        allPosts.push(parsePostFromFile(f, cat.id));
      }
    } catch (err) {
      console.error(`Failed to list ${cat.path}:`, err.message);
    }
  }

  // For investment, also scan subdirectories for .md files
  try {
    const investmentRoot = await ghFetch(
      `${API_BASE}/repos/${GITHUB_OWNER}/${GITHUB_REPO}/contents/investment`
    );
    for (const item of investmentRoot) {
      if (item.type === "dir") {
        try {
          const subFiles = await listMarkdownFiles(item.path);
          for (const f of subFiles) {
            allPosts.push(parsePostFromFile(f, "investment"));
          }
        } catch (err) {
          console.error(`Failed to list ${item.path}:`, err.message);
        }
      }
    }
  } catch (err) {
    console.error("Failed to scan investment subdirs:", err.message);
  }

  // Sort: dated posts first (newest), then undated alphabetically
  allPosts.sort((a, b) => {
    if (a.date && b.date) return b.date.localeCompare(a.date);
    if (a.date) return -1;
    if (b.date) return 1;
    return a.title.localeCompare(b.title);
  });

  cache.posts = { data: allPosts, fetchedAt: Date.now() };
  return allPosts;
}

// --- Markdown rendering ---
marked.setOptions({ gfm: true, breaks: true });

function renderMarkdown(md) {
  return marked.parse(md);
}

// --- HTML templates ---
function layoutHtml(title, body) {
  return `<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${escapeHtml(title)}</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      line-height: 1.7;
      color: #333;
      max-width: 780px;
      margin: 0 auto;
      padding: 2rem 1.5rem;
      background: #fafafa;
    }
    header { margin-bottom: 2rem; padding-bottom: 1rem; border-bottom: 2px solid #eee; }
    header h1 a { color: #111; text-decoration: none; font-size: 1.5rem; }
    nav { margin-top: 0.5rem; }
    nav a {
      color: #555; text-decoration: none; margin-right: 1rem;
      font-size: 0.9rem; padding: 0.2rem 0.5rem; border-radius: 4px;
    }
    nav a:hover, nav a.active { background: #333; color: #fff; }
    .post-list { list-style: none; }
    .post-list li {
      padding: 0.8rem 0; border-bottom: 1px solid #eee;
      display: flex; align-items: baseline; gap: 1rem;
    }
    .post-list .date { color: #999; font-size: 0.85rem; white-space: nowrap; font-variant-numeric: tabular-nums; }
    .post-list a { color: #111; text-decoration: none; font-weight: 500; }
    .post-list a:hover { text-decoration: underline; }
    .post-list .category-tag {
      font-size: 0.7rem; color: #777; background: #eee;
      padding: 0.1rem 0.4rem; border-radius: 3px;
    }
    article { margin-top: 1rem; }
    article h1 { font-size: 1.8rem; margin-bottom: 0.5rem; }
    article .meta { color: #999; font-size: 0.85rem; margin-bottom: 2rem; }
    article .content { font-size: 1rem; }
    article .content h1, article .content h2, article .content h3 { margin: 1.5rem 0 0.5rem; }
    article .content h1 { font-size: 1.5rem; }
    article .content h2 { font-size: 1.3rem; }
    article .content p { margin-bottom: 1rem; }
    article .content pre {
      background: #1e1e1e; color: #d4d4d4;
      padding: 1rem; border-radius: 6px; overflow-x: auto;
      margin-bottom: 1rem; font-size: 0.9rem;
    }
    article .content code {
      background: #eee; padding: 0.15rem 0.4rem; border-radius: 3px; font-size: 0.9em;
    }
    article .content pre code { background: none; padding: 0; }
    article .content blockquote {
      border-left: 3px solid #ccc; padding-left: 1rem; color: #666; margin-bottom: 1rem;
    }
    article .content table { border-collapse: collapse; width: 100%; margin-bottom: 1rem; }
    article .content th, article .content td {
      border: 1px solid #ddd; padding: 0.5rem 0.75rem; text-align: left; font-size: 0.9rem;
    }
    article .content th { background: #f5f5f5; }
    article .content img { max-width: 100%; height: auto; border-radius: 4px; }
    article .content a { color: #0066cc; }
    article .content ul, article .content ol { margin-bottom: 1rem; padding-left: 1.5rem; }
    article .content li { margin-bottom: 0.3rem; }
    .back { display: inline-block; margin-bottom: 1.5rem; color: #555; text-decoration: none; font-size: 0.9rem; }
    .back:hover { color: #111; }
    .error { text-align: center; margin-top: 3rem; color: #999; }
    footer { margin-top: 3rem; padding-top: 1rem; border-top: 1px solid #eee; color: #aaa; font-size: 0.8rem; }
  </style>
</head>
<body>
  <header>
    <h1><a href="/">Notes</a></h1>
    <nav>
      <a href="/" id="nav-all">All</a>
      <a href="/category/programming" id="nav-programming">Programming</a>
      <a href="/category/investment" id="nav-investment">Investment</a>
    </nav>
  </header>
  ${body}
  <footer>Powered by GitHub API &middot; <a href="https://github.com/${GITHUB_OWNER}/${GITHUB_REPO}">Source</a></footer>
</body>
</html>`;
}

function escapeHtml(str) {
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function postListHtml(posts, activeCategory) {
  if (posts.length === 0) {
    return `<div class="error"><p>No posts found.</p></div>`;
  }
  const items = posts
    .map((p) => {
      const dateStr = p.date || "";
      const catLabel = CATEGORIES.find((c) => c.id === p.category)?.label || p.category;
      return `<li>
        <span class="date">${escapeHtml(dateStr)}</span>
        <a href="/post/${encodeURIComponent(p.path)}">${escapeHtml(p.title)}</a>
        <span class="category-tag">${escapeHtml(catLabel)}</span>
      </li>`;
    })
    .join("\n");

  const title = activeCategory
    ? CATEGORIES.find((c) => c.id === activeCategory)?.label || activeCategory
    : "All Posts";

  return layoutHtml(title, `<ul class="post-list">${items}</ul>`);
}

function postDetailHtml(post, htmlContent) {
  const catLabel = CATEGORIES.find((c) => c.id === post.category)?.label || post.category;
  const body = `
    <a class="back" href="/">&larr; Back</a>
    <article>
      <h1>${escapeHtml(post.title)}</h1>
      <div class="meta">${post.date ? escapeHtml(post.date) + " &middot; " : ""}${escapeHtml(catLabel)}</div>
      <div class="content">${htmlContent}</div>
    </article>`;
  return layoutHtml(post.title, body);
}

// --- Routes ---
app.get("/", async (req, res) => {
  try {
    const posts = await getAllPosts();
    res.send(postListHtml(posts, null));
  } catch (err) {
    console.error(err);
    res.status(500).send(layoutHtml("Error", `<div class="error"><p>Failed to load posts.</p><pre>${escapeHtml(err.message)}</pre></div>`));
  }
});

app.get("/category/:id", async (req, res) => {
  try {
    const posts = await getAllPosts();
    const filtered = posts.filter((p) => p.category === req.params.id);
    res.send(postListHtml(filtered, req.params.id));
  } catch (err) {
    console.error(err);
    res.status(500).send(layoutHtml("Error", `<div class="error"><p>Failed to load posts.</p></div>`));
  }
});

app.get("/post/*", async (req, res) => {
  try {
    const filePath = decodeURIComponent(req.params[0]);
    const posts = await getAllPosts();
    const post = posts.find((p) => p.path === filePath);

    if (!post) {
      return res.status(404).send(layoutHtml("Not Found", `<div class="error"><p>Post not found.</p></div>`));
    }

    const md = await fetchFileContent(post.path);
    const html = renderMarkdown(md);
    res.send(postDetailHtml(post, html));
  } catch (err) {
    console.error(err);
    res.status(500).send(layoutHtml("Error", `<div class="error"><p>Failed to load post.</p><pre>${escapeHtml(err.message)}</pre></div>`));
  }
});

// Force cache refresh
app.post("/api/refresh", (req, res) => {
  cache.posts = null;
  cache.contents.clear();
  res.json({ ok: true, message: "Cache cleared" });
});

app.listen(PORT, () => {
  console.log(`Blog server running at http://localhost:${PORT}`);
  console.log(`GitHub: ${GITHUB_OWNER}/${GITHUB_REPO}`);
  console.log(`Cache TTL: ${CACHE_TTL_MS / 1000}s`);
});
