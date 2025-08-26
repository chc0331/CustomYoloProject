import random

import cv2
import numpy as np

from dataset.canvas.component.ui_component_base import UIComponentBase, random_color, center_text, CompIdAllocator


class ButtonComponent(UIComponentBase):
    def __init__(self):
        super().__init__(1, "Button")
        self.type_id = 1

    def draw(self, img, depth, parent_id, allocator):
        super().draw(img, depth, parent_id, allocator)
        color = random_color()
        side = min(self.w, self.h)
        cx = self.x + (self.w - side) // 2
        cy = self.y + (self.h - side) // 2
        self.style = random.randint(1, 4)
        if self.style <= 2:
            radius = side // 2
            self.draw_rounded_rectangle(img, radius, color)
        elif self.style == 3:
            self.draw_filled(img)
        else:
            self.draw_outline(img)
        center_text(img, self.cls_name, cx, cy, side, side, font_scale=0.3)

    def draw_filled(self, img):
        color = random_color()
        cv2.rectangle(img, (self.x, self.y), (self.x + self.w, self.y + self.h), color, -1)

    def draw_outline(self, img):
        color = random_color()
        cv2.rectangle(img, (self.x, self.y), (self.x + self.w, self.y + self.h), color, 2)

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


if __name__ == "__main__":
    # 흰색 배경 생성
    img = np.ones((500, 500, 3), dtype=np.uint8) * 255

    # 버튼 생성 후 그림
    # btn = ButtonComponent(style="filled")
    # btn = ButtonComponent(style="rounded")
    btn = ButtonComponent()
    btn.set_bbox(150, 200, 200, 80)
    btn.draw(img, depth=0, parent_id=0, allocator=CompIdAllocator())

    # 결과 출력
    cv2.imshow("Button Demo", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
