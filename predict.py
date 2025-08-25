import os
import random
from collections import Counter

import cv2
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from ultralytics import YOLO


def randomColor():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return r, g, b


def calculateBackgroundRectangle(text, cords_0, cords_1):
    text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)[0]
    text_width, text_height = text_size[0], text_size[1]
    bg_width = text_width + 10
    bg_height = text_height + 10
    bg_position = (cords_0, cords_1 + 2)
    return bg_position, bg_width, bg_height, text_height


def getColors(objects):
    colors = {}
    for obj, _ in objects.items():
        colors[obj] = randomColor()
    return colors


def predict():
    model = YOLO("./runs/detect/train7/weights/best.pt")
    # model.model.load_state_dict(torch.load('custom_model.pt'))
    # model.to('gpu')
    image_files = os.listdir("./sample_dataset/train/images")
    images = [image for image in image_files if image.split(".")[1] == "png"]

    selected_image = "./sample_dataset/train/images/" + images[1]
    img = Image.open(selected_image)
    img_np = np.array(img)  ## 행렬로 변환된 이미지
    # plt.imshow(img_np)  ## 행렬 이미지를 다시 이미지로 변경해 디스플레이
    # plt.show()  ## 이미지 인터프린터에 출력

    results = model.predict(selected_image)
    result = results[0]

    totalObject = len(result.boxes)
    object_counts = {}
    print("+", "-" * 60, "+", sep="")
    if (totalObject > 0):
        title = f"There are a total of {totalObject} objects in the selected image."
        print(f"|{title}", " " * (60 - len(title)), "|", sep="")
        print("+", "-" * 60, "+", sep="")
        class_names = [result.names[box.cls[0].item()] for box in result.boxes]
        object_counts = Counter(class_names)

        for obj, count in object_counts.items():
            text = obj + ": " + str(count)
            print(f"|{text}", " " * (58 - len(text)), "|")

            print("+", "-" * 60, "+", sep="")

        image = cv2.imread(selected_image)
    else:
        info = "There is no object in the selected image."
        print(f"|{info}", " " * (60 - len(info)), "|", sep="")
        print("+", "-" * 60, "+", sep="")

    image = cv2.imread(selected_image)
    colors = getColors(object_counts)

    for box in result.boxes:
        class_id = result.names[box.cls[0].item()]
        cords = box.xyxy[0].tolist()
        cords = [round(x) for x in cords]
        color = colors[class_id]

        cv2.rectangle(image, (cords[0], cords[1]), (cords[2], cords[3]), color, 2)

        bg_position, bg_width, bg_height, text_height = calculateBackgroundRectangle(class_id, cords[0], cords[1])
        cv2.rectangle(image, bg_position, (bg_position[0] + bg_width, bg_position[1] - bg_height), color, -1)

        imageCords = (cords[0] + 3, cords[1] - ((bg_height - text_height) // 2))
        cv2.putText(image, class_id, imageCords, cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    height, width, _ = image.shape
    plt.figure(figsize=(width / 100, height / 100), dpi=100)
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.show()


if __name__ == "__main__":
    predict()
