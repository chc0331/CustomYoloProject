import cv2

from dataset.canvas.component.ui_component_base import UIComponentBase, random_color, center_text


class TextComponent(UIComponentBase):
    def __init__(self):
        super().__init__(0, "Text")
        self.type_id = 2

    def draw(self, img):
        color = random_color()
        cv2.rectangle(img, (self.x, self.y), (self.x + self.w, self.y + self.h), color, -1)
        center_text(img, self.cls_name, self.x, self.y, self.w, self.h, font_scale=0.3)
