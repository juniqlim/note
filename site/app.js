// 테마 토글 + 클라이언트 검색. 없어도 페이지는 읽힌다.
const html = document.documentElement;
const btn = document.getElementById('theme');
const setLabel = () => { if (btn) btn.textContent = html.dataset.theme === 'dark' ? '라이트' : '다크'; };
setLabel();
btn?.addEventListener('click', () => {
  const dark = html.dataset.theme === 'dark';
  if (dark) delete html.dataset.theme; else html.dataset.theme = 'dark';
  try { localStorage.setItem('theme', dark ? 'light' : 'dark'); } catch (e) {}
  setLabel();
});

const input = document.getElementById('q');
const panel = document.getElementById('search-results');
const page = document.getElementById('page');
if (input && panel && page) {
  const base = input.dataset.base || '';
  let index = null;
  const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

  const load = async () => {
    if (index) return index;
    index = await (await fetch(base + 'search.json')).json();
    return index;
  };

  const run = async (q) => {
    if (!q) { panel.hidden = true; page.hidden = false; return; }
    const list = await load();
    const lq = q.toLowerCase();
    const hits = list.map((n) => {
      const i = n.text.toLowerCase().indexOf(lq);
      const inTitle = n.title.toLowerCase().includes(lq);
      if (i < 0 && !inTitle) return null;
      const ex = i >= 0 ? '…' + n.text.slice(Math.max(0, i - 40), i + 90) + '…' : n.summary;
      return '<a class="hit" href="' + base + n.url + '"><span><span class="hit-title">' + esc(n.title)
        + '</span><span class="hit-folder">' + esc(n.folder) + '</span></span>'
        + '<span class="hit-ex">' + esc(ex || '') + '</span></a>';
    }).filter(Boolean);
    panel.innerHTML = '<p class="count">“' + esc(q) + '” — 노트 ' + hits.length + '건</p>' + hits.join('');
    panel.hidden = false;
    page.hidden = true;
  };

  let t;
  input.addEventListener('input', () => { clearTimeout(t); t = setTimeout(() => run(input.value.trim()), 120); });
  input.addEventListener('keydown', (e) => { if (e.key === 'Escape') { input.value = ''; run(''); } });
}
