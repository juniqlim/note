# 나의 노트

저의 생각을 적은 노트입니다.
시간이 지나면서 제 생각이 바뀌는 것 처럼, 노트의 내용은 변경될 수 있습니다.

읽는 곳 — https://note.juniq.im

## 올리는 법

**push 하면 끝이다.** GitHub Actions 가 빌드해서 배포한다 (`.github/workflows/pages.yml`).
테스트가 깨지면 배포하지 않는다.

손으로 확인하고 싶을 때만:

    node build.js        # → docs/ (저장소에 커밋하지 않는다)
    npm run serve        # 로컬에서 열어 본다

Node 18+ 만 필요하다. npm 패키지 없음.

## 구조

    site.json            사이트 제목 · 갈래(폴더) · 낼 노트 · slug
    programming/*.md     노트 원본
    ai-agent/*.md
    investment/*.md
    build.js             md 읽기 → 파싱 → docs/ 출력
    site/md.js           마크다운 파서 (프론트매터 · 표 · 중첩 리스트 · 그림 · 링크 수집)
    site/history.js      git 이력 → 쓴 날 · 고친 날
    site/collect.js      낼 것 고르기 · 갈래 정하기
    site/render.js       AST → HTML, 페이지 레이아웃
    site/style.css       스타일 (다크 기본 / 라이트 토글)
    site/app.js          테마 토글 + 클라이언트 검색
    test/                단위 테스트 — npm test
    docs/                빌드 결과물. Actions 가 만들어 배포한다 — 커밋하지 않는다

## 무엇을 내는가

**저장소에는 마음대로 올린다. 사이트에는 `include` 에 적은 것만 나간다.**
적기를 잊으면 안 나갈 뿐이지만, 빼기를 잊으면 나가 버린다.

    "include": [
      "programming/why-tdd.md",      파일 하나
      "programming/ward",            폴더 하나 — 그 안이 다 나간다
      "**/sources"                   이름이 같은 폴더가 여기저기 있을 때
    ]

`folders` 는 갈래(라벨)를 정한다. 한 파일이 여럿에 걸리면 가장 깊은 갈래가
이긴다 — `investment/warren` 은 "투자" 가 아니라 "투자 · 워런 버핏" 이다.
`deep: true` 를 주면 그 아래를 다 훑어 한 갈래로 받는다. 종목이 마흔 개일 때
갈래를 마흔 개 만들지 않으려고 있다.

## 날짜는 git 이 안다

쓴 날과 고친 날은 `git log` 에서 온다. 파일명 앞에 `YYYY-MM-DD-` 를 적던 것은
git 이 이미 아는 것을 손으로 되풀이한 것이었다 — 19편을 대조해 보니 모두 같았다.
새 노트에는 붙이지 않아도 된다.

이름 변경은 따라간다. 폴더를 정리하며 옮긴 날이 쓴 날로 둔갑하지 않는다.

## 쓰는 규칙

- `# 제목` 한 줄이 노트 제목. `# 제목 - 부제` 로 쓰면 뒤가 부제 (하이픈이 하나일 때만).
- `# 제목 (English Title)` 의 괄호는 원제로 따로 표시된다.
- H1 이 없으면 첫 `##` 이 제목이 된다.
- 제목 위나 바로 아래에 URL 을 한 줄 두면 출처로 잡는다. 뒤따르는 줄은 설명.
- 출처가 국외 사이트면 **번역**으로 표시된다. 참고만 한 글은 `translation: false` 로 끈다.
- 그림은 `![글](주소)`. 예전 노트가 갖고 있는 한 줄짜리 `<img>` 태그도 그대로 나간다.
- 한글 파일명은 `site.json` 의 `slugs` 에 `"경로": "ascii-name"` 으로 URL 을 정해준다. 프론트매터 `slug:` 도 된다.
- 노트끼리 링크할 때 GitHub blob URL 을 그대로 붙여도 내부 링크로 바뀐다. `[글](../ai-agent/x.md)` 도 된다.
- 링크된 쪽 노트 하단에 백링크가 자동으로 생긴다.

프론트매터로 덮어쓸 수 있는 것: `title` `subtitle` `summary` `date` `slug` `source` `translation` `sourceNote`

## 노트와 위키

둘은 역할이 다르고 사이트를 따로 둔다. 위키는 https://wiki.juniq.im 이다.

|  | 노트 | 위키 |
|---|---|---|
| 담는 것 | 글 한 편 | 개념 하나 |
| 이름 | 제목 문장 | 본문에서 부를 이름 |
| 날짜 | 쓴 날이 붙는다 | 없다. 계속 고친다 |
| 링크색 | 초록 | 파랑 |

노트에서는 `[[이름]]` 도 CamelCase 자동 링크도 쓰지 않는다. 그것은 위키의 문법이다.
