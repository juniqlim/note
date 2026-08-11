// 어떤 md 를 어느 갈래로 낼지 정한다.

// 저장소에는 마음대로 올리고, 사이트에는 include 에 적은 것만 낸다.
// 적기를 잊으면 안 나갈 뿐이지만, 빼기를 잊으면 나가 버린다.
//
// 규칙은 세 가지로 쓴다.
//   programming/why-tdd.md   파일 하나
//   programming/ward         폴더 하나 — 그 안이 다 나간다
//   **/sources               이름이 같은 폴더가 여기저기 있을 때
export function matches(path, rules = []) {
  return rules.some((rule) => {
    if (rule.startsWith('**/')) {
      const name = rule.slice(3);
      return path.split('/').slice(0, -1).includes(name);
    }
    return path === rule || path.startsWith(rule + '/');
  });
}

// 갈래는 folders 에 적은 폴더다. 여럿에 걸리면 가장 깊은 것이 이긴다 —
// investment/warren 은 "투자" 가 아니라 "투자 · 워런 버핏" 이다.
//
// deep 이 없으면 바로 아래 파일만 받는다. 하위 폴더를 갈래로 삼고 싶을 때
// 그것을 folders 에 따로 적기 위해서다. deep 을 주면 아래를 다 훑는다 —
// 종목이 마흔 개면 갈래를 마흔 개 만들 수는 없다.
export function groupOf(path, folders = []) {
  let best = null;
  for (const f of folders) {
    if (!path.startsWith(f.dir + '/')) continue;
    const under = path.slice(f.dir.length + 1);
    if (!f.deep && under.includes('/')) continue;
    if (!best || f.dir.length > best.dir.length) best = f;
  }
  return best;
}
