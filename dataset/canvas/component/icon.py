import cv2

from dataset.canvas.component.ui_component_base import UIComponentBase, random_color, center_text


class IconComponent(UIComponentBase):
    def __init__(self):
        super().__init__(2, "Icon")
        self.type_id = 1


    def draw(self, img, depth, parent_id, allocator):
        super().draw(img, depth, parent_id, allocator)
        color = random_color()
        side = min(self.w, self.h)
        cx = self.x + (self.w - side) // 2
        cy = self.y + (self.h - side) // 2
        center = (cx + side // 2, cy + side // 2)
        radius = side // 2
        cv2.circle(img, center, radius, color, -1)
        center_text(img, self.cls_name, cx, cy, side, side, font_scale=0.3)