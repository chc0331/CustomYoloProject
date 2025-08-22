import random

import cv2
import numpy as np

from dataset.canvas.component.layout import LayoutComponent
from dataset.canvas.component.ui_component_base import CLASSES


# =========================
# 🎨 LayoutCanvas
# =========================
class LayoutCanvas:

    def __init__(self, img_size=512, max_layout_depth=3):
        self.img_size = img_size
        self.max_layout_depth = max_layout_depth

    def draw(self):
        img = 255 * np.ones((self.img_size, self.img_size, 3), dtype=np.uint8)
        label_lines = []

        layout_cls = random.randint(3, 7)
        layout_name = CLASSES[layout_cls]
        layout = LayoutComponent(layout_cls, layout_name, self.img_size, self.max_layout_depth, depth=0)
        layout.set_bbox(0, 0, self.img_size, self.img_size)
        layout.draw(img)

        label_lines.extend(layout.label(self.img_size))
        return img, label_lines
