import json
import os

from dataset.canvas.component.ui_component_base import CLASSES


class Node:
    def __init__(self, cls_id, xc, yc, w, h, depth, parent_id, comp_id, type_id):
        self.cls_id = cls_id
        self.xc = xc
        self.yc = yc
        self.w = w
        self.h = h
        self.depth = depth
        self.parent_id = parent_id
        self.comp_id = comp_id
        self.type_id = type_id
        self.children = []

    def to_dict(self):
        """dict로 직렬화 (json 저장 등 가능)"""
        return {
            "class_id": f"{self.cls_id}({CLASSES[self.cls_id]})",
            "x_center": self.xc,
            "y_center": self.yc,
            "width": self.w,
            "height": self.h,
            "depth": self.depth,
            "parent_id": self.parent_id,
            "component_id": self.comp_id,
            "type": self.type_id,
            "children": [child.to_dict() for child in self.children]
        }

    def __repr__(self):
        return (f"Node(class_id = {self.cls_id}({CLASSES[self.cls_id]}), "
                f"(x/y) = {self.xc}/{self.yc}, "
                f"(w/h) = {self.w}/{self.h}, "
                f"depth={self.depth}, "
                f"parent_id={self.parent_id}, "
                f"comp_id={self.comp_id}, "
                f"children={len(self.children)})")


def build_view_hierarchy(file_name):
    root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    file_path = os.path.join(root_path, "sample_dataset", "labels", file_name)
    labels = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:  # 빈 줄은 건너뜀
                labels.append(line)

    nodes = {}
    root = None

    # 1. 모든 라벨을 Node 객체로 생성
    for label in labels:
        # print("Label : {}".format(label))
        parts = label.strip().split()
        cls_id = int(parts[0])
        xc, yc, w, h = map(float, parts[1:5])
        depth = int(parts[5])
        parent_id = int(parts[6])
        comp_id = int(parts[7])
        type_id = int(parts[8])

        node = Node(cls_id, xc, yc, w, h, depth, parent_id, comp_id, type_id)
        # print("Node : {}".format(node))
        nodes[comp_id] = node

        if comp_id == 0:
            root = node

    # 2. 부모-자식 연결
    for comp_id, node in nodes.items():
        if node.comp_id != 0 and node.parent_id in nodes:
            parent = nodes[node.parent_id]
            parent.children.append(node)
    return root


# 실행 예시
if __name__ == "__main__":
    root_node = build_view_hierarchy("sample_0.txt")
    print("불러오는 파일:", root_node.to_dict())

    # JSON 파일로 저장
    with open("output.json", "w", encoding="utf-8") as f:
        json.dump(root_node.to_dict(), f, ensure_ascii=False, indent=4)
