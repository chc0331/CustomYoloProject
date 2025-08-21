import torch

model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
image = ["C:/Users/admin/Downloads/test.jpg"]

results = model(image)

print(results.pandas().xyxy[0])