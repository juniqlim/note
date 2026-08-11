// 노트의 날짜는 git 이 안다. 파일명에 적어 둔 날짜는 그것을 손으로 되풀이한 것이었다.
//
// 입력은 `git log --format=%cs --name-status --reverse -M` 의 출력이다.
// 오래된 커밋이 먼저 오므로, 파일이 처음 나온 커밋이 쓴 날이고 마지막이 고친 날이다.
//
// 이름 변경(R)을 따라가는 것이 핵심이다. 폴더를 정리하며 옮긴 날을 쓴 날로 잡으면
// 2004년 글이 2026년에 쓴 것이 된다.
export function readHistory(log) {
  const dates = new Map();
  let date = '';

  const touch = (path) => {
    const seen = dates.get(path);
    if (seen) seen.updated = date;
    else dates.set(path, { created: date, updated: date });
  };

  for (const line of log.split('\n')) {
    if (!line.trim()) continue;
    if (/^\d{4}-\d{2}-\d{2}$/.test(line.trim())) { date = line.trim(); continue; }

    const [status, from, to] = line.split('\t');
    if (status.startsWith('R') && to) {
      // 옛 이름이 쌓아 온 이력을 새 이름이 물려받는다.
      const before = dates.get(from);
      dates.delete(from);
      dates.set(to, { created: before ? before.created : date, updated: date });
    } else if (from) {
      touch(from);
    }
  }
  return dates;
}
