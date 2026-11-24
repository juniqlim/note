# HotDraw의 CRC 기술 — 최초의 CRC 카드 (A CRC Description of HotDraw)
https://c2.com/doc/crc/draw.html
워드 커닝햄(Ward Cunningham)이 처음 쓴 CRC 카드를 소개한 글을 번역했습니다. 손글씨 카드는 읽기 쉽도록 내용을 글로 옮겨 적고 번역을 병기했습니다.

워드 커닝햄(Ward Cunningham), 1994

CRC 카드는 객체를 기술하는 방법이다. 프로그램에 쓰이는 클래스마다 그 클래스에 기대하는 책임(responsibilities)과 협력자(collaborators)를 인덱스 카드에 적는다. 여기 있는 것이 사상 최초로 만들어진 CRC 카드다. 몇 해 전 어느 이른 아침, 학생들에게 객체 설계의 감(feel)을 어떻게 전할지 고민하며 밤을 지새운 뒤에 쓴 것이다. 이 카드들은 나와 켄트 벡(Kent Beck)이 Smalltalk로 작성한 그림 편집기 HotDraw를 기술한다.

---

평소처럼 모델, 뷰, 컨트롤러(model, view and controller)부터 시작한다.

![Drawing](https://c2.com/doc/crc/d.gif)

| Drawing | |
|---|---|
| 도형(Figure)을 담는다. (Holds Figures.) | Figure |
| 갱신을 모아 두었다가, 요청이 오면 새로 그린다. (Accumulates updates, refreshes on demand.) | DrawingView<br>DrawingController |

![DrawingView](https://c2.com/doc/crc/dv.gif)

| DrawingView | |
|---|---|
| Drawing과, 선택된 도형들의 핸들(Handle) 집합을 담는다. (Holds Drawing and set of Handles for selected Figures.) | Drawing |
| 건드린 항목(핸들 또는 도형)을 찾는다. (Finds touched items (Handle or Figure).) | |

![DrawingController](https://c2.com/doc/crc/dc.gif)

| DrawingController | |
|---|---|
| 현재 도구(Tool)를 담는다. 그 도구에 마우스 이벤트를 보낸다. (Holds current Tool. Sends it mouse events.) | Drawing<br>DrawingView |
| 유휴 루프(idle loop)에서 Drawing을 새로 그린다. (Refreshes Drawing in idle loop.) | Tools |

---

Drawing은 Figure를 담는다. 여기 추상 클래스와 그것을 구체화한 것(refinements) 몇 가지가 있다. 구체화하면서 추가로 떠맡는 책임을 보여 주려고 이 특정한 종류의 Figure들을 골랐다.

![Figure](https://c2.com/doc/crc/f.gif)

| Figure | |
|---|---|
| 모든 도형은 의존 객체(dependents)를 가지며, 자신이 바뀔 때마다 그들에게 알린다. (All figures have dependents which they notify whenever they change.) | Drawing<br>Locator<br>GroupFigure |

![BoxFigure](https://c2.com/doc/crc/bf.gif)

| BoxFigure | |
|---|---|
| *(둥근 사각형 그림과 속성 이름)*<br>insideColor — 안쪽 색<br>borderRadius — 모서리 반지름<br>borderColor — 테두리 색<br>borderWidth — 테두리 두께 | TrackHandle |

![LineFigure](https://c2.com/doc/crc/lf.gif)

| LineFigure | |
|---|---|
| 두 끝점을 잇는다. 끝점은 Locator일 수 있다. (Connects two endpoints which may be Locators.) | TrackHandle<br>DisplayMedium<br>Locator |

![GroupFigure](https://c2.com/doc/crc/gf.gif)

| GroupFigure | |
|---|---|
| 도형을 더 담는다(Drawing에 들어 있지 않은 것). (Holds more Figures. (not in Drawing)) | Figures |
| 변환을 (구성원에게) 전달한다. (Forwards transformations.) | |
| 이미지를 캐시하고, 구성원이 갱신되면 캐시를 무효화한다. (Cache image, void on update of member.) | |

BoxFigure는 속성(attributes)으로 정의했다는 점에 주목하라. 속성이 책임보다 약하다는 것은 알았지만, 가끔 그림이 필요할 때 종이가 얼마나 융통성 있게 대처하는지 보여 주고 싶었다.

---

DrawingController는 Tool과 협력해서 변경을 만든다. 추상 클래스 Tool의 카드는 만들지 않았다. 기록할 필요가 있다고 느낀 책임이 하나도 없었기 때문이다. 클래스 이름 짓기 관례(naming conventions)가 그 존재를 암시한다.

![CreationTool](https://c2.com/doc/crc/ct.gif)

| CreationTool | |
|---|---|
| 클래스(도형의 종류)를 담는다. (Holds a class (kind of Figure).) | Drawing |
| 호출되면 (그 클래스의) 인스턴스를 Drawing에 추가한다. (Adds instances to Drawing when invoked.) | Figures (class) |

![SelectionTool](https://c2.com/doc/crc/st.gif)

| SelectionTool | |
|---|---|
| 도형을 선택한다(DrawingView에 핸들을 추가한다). (Selects Figures (adds Handles to DrawingView).) | DrawingController<br>DrawingView |
| 핸들을 호출한다. (Invokes Handles.) | Figures<br>Handles |

![ScrollTool](https://c2.com/doc/crc/sct.gif)

| ScrollTool | |
|---|---|
| 뷰의 창(window)을 조정한다. (Adjusts the View's window.) | DrawingView |

---

SelectionTool은 Figure와 Handle을 모두 건드리고 끌 수 있다. Tool과 Handle은 둘 다 Figure를 조작한다. 그래서 Handle은 멋진 작은 확장 단위(unit of extension)가 된다. Tool에게는 Figure처럼 보이고, Figure에게는 Tool처럼 보이기 때문이다.

![Handle](https://c2.com/doc/crc/h.gif)

| Handle | |
|---|---|
| 도형별 조정 기능으로 SelectionTool의 기능을 확장한다. (Extend the function of the SelectionTool with Figure specific adjustments.) | SelectionTool |
| 모든 핸들은 Locator를 가진다. (All have Locators.) | Locator |

![TrackHandle](https://c2.com/doc/crc/th.gif)

| TrackHandle | |
|---|---|
| 도형에 가해진 변환을 감지한다. (Sense a transformation to a figure.) | Figure |
| 같은 변환을 선택된 모든 것에 적용한다. (Apply same transformation to all selections.) | DrawingView |

---

마지막으로 Locator는 Point를 대신하는 것으로, 서로 관련된 도형 사이에 변경을 전파하는 방법을 안다. 예를 들어 Line이 BoxFigure의 모서리에 연결되어 있을 때 BoxFigure가 움직이면, 갱신 메시지가 Locator를 거쳐 Line으로 전파된다.

![Locator](https://c2.com/doc/crc/l.gif)

| Locator | |
|---|---|
| 도형의 한 지점(feature)의 위치를 캐시한다. (Caches the location of a feature of a Figure.) | Figures |
| 도형이 갱신되면 캐시를 무효화한다. (Voids cache when Figure updates.) | Point |
| Point처럼 쓸 수 있다. (Can be used as a Point.) | |

사실 HotDraw에는 Locator가 없었다. 대신 변경 전파를 처리하는 특수한 경우들(special cases)이 있었다. 카드를 그리다가 Locator라는 아이디어가 그냥 떠올랐다. 그 뒤로 HotDraw를 다시 구현할 때 Locator를 효과적으로 써 왔다.

---

이것이 원조 CRC 카드다. 카드를 쓰는 동안 나는 뭔가 좋은 것을 잡았다는 것을 알 수 있었다. 최근에 OOPSLA '94 팀과 객체 워크숍(Workshop on Teams & Objects)의 [입장문](crc-cards-oopsla94-teams-and-objects.md)에서 이 초기 경험을 돌아보았다. 관련 정보는 우리 [홈페이지](http://c2.com/)에서도 볼 수 있다.

Copyright 1994, Ward Cunningham. All Rights Reserved.
