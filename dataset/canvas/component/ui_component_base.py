import random

import cv2

CLASSES = {
    0: "Text",
    1: "Button",
    2: "Icon",
    3: "FullLayout",
    4: "1to1Horizontal",
    5: "1to2Horizontal",
    6: "1to1Vertical",
    7: "1to2Vertical"
}


# =========================
# 🔷 공통 유틸 함수
# =========================
def clamp_rect(x, y, w, h, img_size):
    x = max(0, min(x, img_size - 1))
    y = max(0, min(y, img_size - 1))
    w = max(1, min(w, img_size - x))
    h = max(1, min(h, img_size - y))
    return x, y, w, h


def random_color():
    return tuple(random.randint(50, 220) for _ in range(3))


# 1. class_id : int (버튼, 텍스트뷰 등 UI 클래스)
# 2. x y w h : float (정규화 좌표)
# 3. depth : int (중첩 레벨, 루트=0)
# 4. parent_id : int (상위 레이아웃 id, 최상위면 -1)
# 5. component_id : int (컴포넌트 고유 id)
# 6. type : str (Layout 또는 UI)
def ui_label(cls_idx, x, y, w, h, img_size, depth, parent_id, comp_id, type_id):
    xc = (x + w / 2) / img_size
    yc = (y + h / 2) / img_size
    nw = w / img_size
    nh = h / img_size
    label_text = f"{cls_idx} {xc:.6f} {yc:.6f} {nw:.6f} {nh:.6f} {depth} {parent_id} {comp_id} {type_id}"
    # print("Label : {}".format(label_text))
    return label_text


def center_text(img, text, x, y, w, h, font_scale=0.3, thickness=1):
    font = cv2.FONT_HERSHEY_SIMPLEX
    (text_w, text_h), baseline = cv2.getTextSize(text, font, font_scale, thickness)
    text_x = x + (w - text_w) // 2
    text_y = y + (h + text_h) // 2
    cv2.putText(img, text, (text_x, text_y), font, font_scale, (0, 0, 0), thickness, lineType=cv2.LINE_AA)


class UIComponentBase:
    def __init__(self, cls_idx, cls_name):
        self.cls_idx = cls_idx
        self.cls_name = cls_name
        self.x = self.y = self.w = self.h = 0
        self.depth = 0
        self.parent_id = -1
        self.comp_id = -1
        self.type_id = 0

    def set_bbox(self, x, y, w, h):
        self.x, self.y, self.w, self.h = x, y, w, h

    def draw(self, img):
        raise NotImplementedError

    def label(self, img_size):
        return ui_label(self.cls_idx, self.x, self.y, self.w, self.h, img_size,
                        self.depth, self.parent_id, self.comp_id, self.type_id)
