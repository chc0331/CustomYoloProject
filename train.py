import torch.cuda
from ultralytics import YOLO


def train():
    model = YOLO("model/yolov8m.pt")
    model.train(data="./dataset_custom.yaml", imgsz=640, batch=8, epochs=100, workers=1,
                device=0)
    torch.save(model.state_dict(), 'custom_model.pt')


if __name__ == "__main__":
    train()
