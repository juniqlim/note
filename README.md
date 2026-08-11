# 나의 노트

저의 생각을 적은 노트입니다.
시간이 지나면서 제 생각이 바뀌는 것 처럼, 노트의 내용은 변경될 수 있습니다.

읽는 곳 — https://note.juniq.im

## 빌드

    node build.js        # → docs/

Node 18+ 만 필요하다. npm 패키지 없음.

## 구조

    site.json            사이트 제목 · 주제(폴더) · 낼 노트 목록 · slug
    programming/*.md     노트 원본. 여기 있는 것이 전부 나가지는 않는다
    ai-agent/*.md
    investment/*.md
    build.js             md 읽기 → 파싱 → docs/ 출력
    site/md.js           마크다운 파서 (프론트매터 · 표 · 중첩 리스트 · 백링크용 링크 수집)
    site/render.js       AST → HTML, 페이지 레이아웃
    site/style.css       스타일 (다크 기본 / 라이트 토글)
    site/app.js          테마 토글 + 클라이언트 검색
    test/                단위 테스트 — npm test
    docs/                배포물. Pages 로 올리므로 커밋한다

## 무엇을 내는가

여기에는 아직 안 익은 글도 있다. 그래서 폴더를 훑지 않고 `site.json` 의 `notes` 에
적은 것만 낸다. 적은 순서가 곧 보이는 순서다. 이름이 틀리면 빌드가 멈춘다 —
조용히 빠지면 왜 안 나오는지 알 수 없다.

## 쓰는 규칙

- `# 제목` 한 줄이 노트 제목. `# 제목 - 부제` 로 쓰면 뒤가 부제.
- `# 제목 (English Title)` 의 괄호는 원제로 따로 표시된다.
- H1 위에 URL 을 한 줄 두면 출처로 잡는다. "번역" 이라는 말이 있으면 번역 표시.
- 파일명 앞의 `YYYY-MM-DD-` 는 날짜로 쓰인다.
- 한글 파일명은 `site.json` 의 `slugs` 에 `"경로": "ascii-name"` 으로 URL 을 정해준다. 프론트매터 `slug:` 도 된다.
- 노트끼리 링크할 때 GitHub blob URL 을 그대로 붙여도 내부 링크로 바뀐다. `[글](../ai-agent/x.md)` 도 된다.
- 링크된 쪽 노트 하단에 백링크가 자동으로 생긴다.

프론트매터로 덮어쓸 수 있는 것: `summary` `subtitle` `date` `slug` `source` `translation` `sourceNote`

## 노트와 위키

둘은 역할이 다르고 사이트를 따로 둔다. 위키는 https://wiki.juniq.im 이다.

|  | 노트 | 위키 |
|---|---|---|
| 담는 것 | 글 한 편 | 개념 하나 |
| 이름 | 제목 문장 | 본문에서 부를 이름 |
| 날짜 | 쓴 날이 붙는다 | 없다. 계속 고친다 |
| 링크색 | 초록 | 파랑 |

노트에서는 `[[이름]]` 도 CamelCase 자동 링크도 쓰지 않는다. 그것은 위키의 문법이다.
