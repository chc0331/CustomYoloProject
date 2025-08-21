# Yolo-lite implementation

1. **문제 정의**
-> 1-1. 모바일 위젯 GUI 이미지가 있을때 레이아웃 영역을 분류하는것.
-> 1-2. 모바일 위젯 GUI 이미지가 있을대 UI 컴포넌트를 분류하는것.
-> 1-3. 레이아웃 구현 원칙이 존재함.

2. **레이아웃 원칙**

2-1. Layout 컴포넌트 종류 : Full / 1to1Horizontal / 1to2Horizontal / 1to1Vertical / 1to2Vertical 
2-2. 1 depth 레이아웃은 TopLevelLayout 이라고 정의한다.
2-3. Layout 컴포넌트는 중첩이 가능하다. (여기서는 일단 1~3 depth로 정의한다.)
2-4. Layout 컴포넌트는 Layout 영역 기준으로 Padding 퍼센트 값을 가진다.(Horizontal : 0~5% / Vertical : 0~5%)
2-5. UI 컴포넌트 종류 :Text / Button / Icon 
2-6. UI 컴포넌트는 하나의 레이아웃 영역에 항상 full로 가득찬다. 
ex) 1to2Horizontal에서는 2개의 컴포넌트가 1 / 2영역에 각각 들어간다
2-7. UI 컴포넌트는 Width/Height를 바로 상위 뷰그룹 영역의 %값으로 적용된다.


3. **간단한 데이터 만들기**
-> 위 레이아웃 원칙을 준수하는 자동생성코드가 가능한가?
-> PNG 파일로 만들것.
-> 다른 UI 컴포넌트는 다른 색을 가질것.
-> Button / Icon은 Width/Height 1:1 비율로 만들어줘(레이아웃을 full로 채울때 작은 값 기준으로 설정해줘)
-> Text는 주어진 크기에 맞게 텍스트 내용이 들어간다. 

4. **Yolo-lite 모델 직접 구현하기**
