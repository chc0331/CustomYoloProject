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


3. **데이터 셋 만들기**
-> 위 레이아웃 원칙을 준수하는 자동생성코드가 가능한가?
-> PNG 파일로 만들것.
-> 다른 UI 컴포넌트는 다른 색을 가질것.
-> Button / Icon은 Width/Height 1:1 비율로 만들어줘(레이아웃을 full로 채울때 작은 값 기준으로 설정해줘)

-> 데이터셋 정보
3-1. 레이아웃 GUI (png)
3-2. 레이아웃 정보 (라벨)
- Class index / int / 어떤 UI or Layout 컴포넌트인지
- X,Y 위치 / (x_center, y_center) / 중앙 좌표 (픽셀 -> 정규화)
- 크기 / (width, height) / 너비, 높이 (픽셀 -> 정규화)
- Depth / int / 레이아웃 중첩 수준
- Parent id / int / 상위 레이아웃 id
- Component id / int / 각 컴포넌트 별 고유 id
- Type id / int / Layout(0), UI(1), Text(2)

# class_id x_center y_center width height depth parent_id component_id type
# 1. cls_idx : int (버튼, 텍스트뷰 등 UI 클래스)
# 2. x_center y_center width height : float (정규화 좌표)
# 3. depth : int (중첩 레벨, 루트=0)
# 4. parent_id : int (상위 레이아웃 id, 최상위면 -1)
# 5. component_id : int (컴포넌트 고유 id)
# 6. type : int (Layout(0) 또는 UI(1) 또는 Text(2))
# 예시)
# 0(class_id), 0.45(x_center), 0.30(y_center), 0.20(width), 0.10(height), 1(depth) 1(parent_id), 101(component_id) UI (type)
# 7 0.500000 0.500000 1.000000 1.000000 0 -1 -1 0
# 4 0.500000 0.172852 0.921875 0.326172 1 -1 0 0
# 7 0.274414 0.172852 0.451172 0.298828 2 0 1 0
# 0 0.274414 0.081055 0.423828 0.091797 2 1 2 2
# 1 0.274414 0.218750 0.423828 0.183594 2 1 2 1
# 2 0.725586 0.172852 0.451172 0.298828 1 0 1 1
# 5 0.500000 0.663086 0.921875 0.654297 1 -1 0 0
# 4 0.210938 0.663086 0.289062 0.626953 2 0 1 0
# 2 0.145508 0.663086 0.130859 0.603516 2 1 2 1
# 1 0.276367 0.663086 0.130859 0.603516 2 1 2 1
# 7 0.644531 0.663086 0.578125 0.626953 2 0 1 0
# 0 0.644531 0.454102 0.531250 0.208984 2 1 2 2
# 1 0.644531 0.767578 0.531250 0.417969 2 1 2 1

# 방향
# 1) YOLO-style로 좌표/클래스 라벨 저장 (Detection 학습용)
# 2) JSON Tree로 계층 정보 저장 (Code Reconstruction 학습용)

4. **Yolo-lite 모델 직접 구현하기**
