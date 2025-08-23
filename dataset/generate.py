import os

import cv2

from dataset.canvas.layout_canvas import LayoutCanvas


class DatasetGenerator:
    def __init__(self, base_path="../sample_dataset", dataset_count=5):
        self.dataset_count = dataset_count
        self.base_path = base_path
        # 경로 설정
        self.img_dir = os.path.join(base_path, "images")
        self.label_dir = os.path.join(base_path, "labels")
        os.makedirs(self.img_dir, exist_ok=True)
        os.makedirs(self.label_dir, exist_ok=True)

    # ----------------------------
    # 메인 생성 함수
    # ----------------------------
    def generate_dataset(self):
        for i in range(self.dataset_count):
            canvas = LayoutCanvas()
            img_path = os.path.join(self.img_dir, f"sample_{i}.png")
            label_path = os.path.join(self.label_dir, f"sample_{i}.txt")
            image, labels = canvas.draw()
            print("Finally label : {}".format(labels))
            cv2.imwrite(img_path, image)
            with open(label_path, "w") as f:
                f.write("\n".join(labels))
        print("✅ Synthetic dataset 생성 완료 (모든 컴포넌트 색상 고유)")


# ----------------------------
# 실행 예제
# ----------------------------
if __name__ == "__main__":
    generator = DatasetGenerator(dataset_count=5)
    generator.generate_dataset()
