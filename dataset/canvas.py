import random

import cv2
import numpy as np


class LayoutCanvas:
    def __init__(self, img_size=512, max_layout_depth=3):
        self.img_size = img_size
        self.max_layout_depth = max_layout_depth

        # 클래스 정의
        self.classes = {
            0: "Text",
            1: "Button",
            2: "Icon",
            3: "FullLayout",
            4: "1to1Horizontal",
            5: "1to2Horizontal",
            6: "1to1Vertical",
            7: "1to2Vertical"
        }

    def clamp_rect(self, x, y, w, h):
        x = max(0, min(x, self.img_size - 1))
        y = max(0, min(y, self.img_size - 1))
        w = max(1, min(w, self.img_size - x))
        h = max(1, min(h, self.img_size - y))
        return x, y, w, h

    def add_label(self, label_lines, cls_idx, x, y, w, h):
        xc = (x + w / 2) / self.img_size
        yc = (y + h / 2) / self.img_size
        nw = w / self.img_size
        nh = h / self.img_size
        label_lines.append(f"{cls_idx} {xc:.6f} {yc:.6f} {nw:.6f} {nh:.6f}")

    def draw_text(self, img, text, x, y, color, scale=0.6, thickness=2):
        cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, scale, color, thickness, lineType=cv2.LINE_AA)

    def split_zones_by_layout(self, layout_cls, x, y, w, h):
        if layout_cls == 3:  # Full
            return [(x, y, w, h)]
        elif layout_cls == 4:  # 1:1 Horizontal
            mid = w // 2
            return [(x, y, mid, h), (x + mid, y, w - mid, h)]
        elif layout_cls == 5:  # 1:2 Horizontal
            left = w // 3
            return [(x, y, left, h), (x + left, y, w - left, h)]
        elif layout_cls == 6:  # 1:1 Vertical
            mid = h // 2
            return [(x, y, w, mid), (x, y + mid, w, h - mid)]
        elif layout_cls == 7:  # 1:2 Vertical
            top = h // 3
            return [(x, y, w, top), (x, y + top, w, h - top)]
        else:
            return [(x, y, w, h)]

    def apply_padding(self, x, y, w, h):
        pad_h_pct = random.randint(0, 5)
        pad_v_pct = random.randint(0, 5)
        pad_x = int(round(w * pad_h_pct / 100))
        pad_y = int(round(h * pad_v_pct / 100))
        xi = x + pad_x
        yi = y + pad_y
        wi = w - 2 * pad_x
        hi = h - 2 * pad_y
        xi, yi, wi, hi = self.clamp_rect(xi, yi, wi, hi)
        return xi, yi, wi, hi

    def random_color(self):
        color = tuple(random.randint(50, 220) for _ in range(3))
        return color

    def place_ui_component(self, img, label_lines, x, y, w, h, comp_cls=None):
        if comp_cls is None:
            comp_cls = random.randint(0, 2)

        color = self.random_color()

        # Button/Icon → 정사각형
        if comp_cls in [1, 2]:
            side = min(w, h)
            x_center = x + (w - side) // 2
            y_center = y + (h - side) // 2
            w = side
            h = side
            x = x_center
            y = y_center

        # 사각형 그리기
        if comp_cls in [1, 2]:
            # 원 그리기 (사각형 대신 원)
            center = (x + w // 2, y + h // 2)  # 중심 좌표
            radius = min(w, h) // 2  # 반지름 (너비/높이 중 작은 값 기준)
            cv2.circle(img, center, radius, color, -1)
        else:
            cv2.rectangle(img, (x, y), (x + w, y + h), color, -1)

        # 텍스트 가운데 정렬
        text = self.classes[comp_cls]
        font = cv2.FONT_HERSHEY_SIMPLEX
        thickness = 1
        scale = 0.3
        (text_w, text_h), baseline = cv2.getTextSize(text, font, scale, thickness)
        text_x = x + (w - text_w) // 2
        text_y = y + (h + text_h) // 2  # OpenCV는 y가 baseline 기준
        cv2.putText(img, text, (text_x, text_y), font, scale, (0, 0, 0), thickness, lineType=cv2.LINE_AA)

        # YOLO 라벨 추가
        self.add_label(label_lines, comp_cls, x, y, w, h)

    def make_layout(self, img, label_lines, x, y, w, h, depth):
        layout_cls = random.randint(3, 7)
        color = self.random_color()

        self.add_label(label_lines, layout_cls, x, y, w, h)
        title = self.classes[layout_cls]
        if depth == 0:
            title = f"TopLevelLayout-{title}"
        # self.draw_text(img, title, x + 5, y + 20, color, scale=0.3, thickness=1)

        xi, yi, wi, hi = self.apply_padding(x, y, w, h)
        zones = self.split_zones_by_layout(layout_cls, xi, yi, wi, hi)
        for zx, zy, zw, zh in zones:
            zx, zy, zw, zh = self.clamp_rect(zx, zy, zw, zh)
            cv2.rectangle(img, (zx, zy), (zx + zw, zy + zh), self.random_color(), 1)
            if depth + 1 >= self.max_layout_depth:
                self.place_ui_component(img, label_lines, zx, zy, zw, zh)
            else:
                if random.random() < 0.5:
                    self.make_layout(img, label_lines, zx, zy, zw, zh, depth + 1)
                else:
                    self.place_ui_component(img, label_lines, zx, zy, zw, zh)

    def draw(self):
        img = 255 * np.ones((self.img_size, self.img_size, 3), dtype=np.uint8)
        label_lines = []
        self.make_layout(img, label_lines, 0, 0, self.img_size, self.img_size, 0)
        return img, label_lines
