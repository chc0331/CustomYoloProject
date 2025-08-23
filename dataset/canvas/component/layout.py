import random
from cProfile import label

import cv2

from dataset.canvas.component.button import ButtonComponent
from dataset.canvas.component.icon import IconComponent
from dataset.canvas.component.text import TextComponent
from dataset.canvas.component.ui_component_base import clamp_rect, UIComponentBase, CLASSES, ui_label


# =========================
# 🔷 레이아웃 컴포넌트
# =========================
class LayoutComponent(UIComponentBase):
    def __init__(self, layout_cls, layout_name, img_size, max_depth, depth=0):
        super().__init__(layout_cls, layout_name)
        self.img_size = img_size
        self.max_depth = max_depth
        self.depth = depth
        self.type_id = 0
        self.children = []

    def draw(self, img):
        # Optional: draw layout boundary
        cv2.rectangle(img, (self.x, self.y), (self.x + self.w, self.y + self.h), (150, 150, 150), 1)

        # Split and recurse or place UI
        padded_x, padded_y, padded_w, padded_h = self.apply_padding(self.x, self.y, self.w, self.h)
        zones = self.split_zones(padded_x, padded_y, padded_w, padded_h)

        for zx, zy, zw, zh in zones:
            zx, zy, zw, zh = clamp_rect(zx, zy, zw, zh, self.img_size)

            if self.depth + 1 >= self.max_depth or random.random() < 0.4:
                comp = random.choice([TextComponent, ButtonComponent, IconComponent])()
                comp.depth = self.depth
                comp.parent_id = self.comp_id
                comp.comp_id = self.comp_id + 1
                comp.set_bbox(zx, zy, zw, zh)
                comp.draw(img)
                self.children.append(comp)
            else:
                layout_cls = random.randint(3, 7)
                layout_name = CLASSES[layout_cls]
                sublayout = LayoutComponent(layout_cls, layout_name, self.img_size, self.max_depth, self.depth + 1)
                sublayout.depth = self.depth + 1
                sublayout.parent_id = self.comp_id
                sublayout.comp_id = self.comp_id + 1
                sublayout.set_bbox(zx, zy, zw, zh)
                sublayout.draw(img)
                self.children.append(sublayout)

    def split_zones(self, x, y, w, h):
        if self.cls_idx == 3:  # Full
            return [(x, y, w, h)]
        elif self.cls_idx == 4:  # 1:1 Horizontal
            mid = w // 2
            return [(x, y, mid, h), (x + mid, y, w - mid, h)]
        elif self.cls_idx == 5:  # 1:2 Horizontal
            left = w // 3
            return [(x, y, left, h), (x + left, y, w - left, h)]
        elif self.cls_idx == 6:  # 1:1 Vertical
            mid = h // 2
            return [(x, y, w, mid), (x, y + mid, w, h - mid)]
        elif self.cls_idx == 7:  # 1:2 Vertical
            top = h // 3
            return [(x, y, w, top), (x, y + top, w, h - top)]
        return [(x, y, w, h)]

    def apply_padding(self, x, y, w, h):
        pad_h_pct = random.randint(0, 5)
        pad_v_pct = random.randint(0, 5)
        pad_x = int(round(w * pad_h_pct / 100))
        pad_y = int(round(h * pad_v_pct / 100))
        return clamp_rect(x + pad_x, y + pad_y, w - 2 * pad_x, h - 2 * pad_y, self.img_size)

    def label(self, img_size):
        labels = [ui_label(self.cls_idx, self.x, self.y, self.w, self.h, img_size,
                           self.depth, self.parent_id, self.comp_id, self.type_id)]
        print("Before Layout label : {}".format(labels))
        for child in self.children:
            child_label = [child.label(img_size)]
            print("Child label : {}".format(child_label))
            labels.extend(child_label)
        print("After Layout label : {}".format(labels))
        return labels
