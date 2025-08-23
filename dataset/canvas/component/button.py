import cv2

from dataset.canvas.component.ui_component_base import UIComponentBase, random_color, center_text


class ButtonComponent(UIComponentBase):
    def __init__(self):
        super().__init__(1, "Button")
        self.type_id = 1


    def draw(self, img):
        color = random_color()
        side = min(self.w, self.h)
        cx = self.x + (self.w - side) // 2
        cy = self.y + (self.h - side) // 2
        radius = side // 2
        self.draw_rounded_rectangle(img, radius, color)
        center_text(img, self.cls_name, cx, cy, side, side, font_scale=0.3)


    def draw_rounded_rectangle(self, img, radius, color):
        """
        radius 적용된 사각형을 그려주는 함수
        img : 이미지
        x, y : 좌상단 좌표
        w, h : 너비, 높이
        radius : 모서리 둥글기
        color : (B, G, R)
        """
        x = self.x
        y = self.y
        w = self.w
        h = self.h
        # radius가 너무 크면 제한
        radius = min(radius, w // 2, h // 2)

        # 직사각형 본체
        cv2.rectangle(img, (x + radius, y), (x + w - radius, y + h), color, -1)
        cv2.rectangle(img, (x, y + radius), (x + w, y + h - radius), color, -1)

        # 모서리 원
        cv2.circle(img, (x + radius, y + radius), radius, color, -1)  # 좌상
        cv2.circle(img, (x + w - radius, y + radius), radius, color, -1)  # 우상
        cv2.circle(img, (x + radius, y + h - radius), radius, color, -1)  # 좌하
        cv2.circle(img, (x + w - radius, y + h - radius), radius, color, -1)
