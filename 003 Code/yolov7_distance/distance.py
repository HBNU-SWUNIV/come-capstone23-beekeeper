import time
import cv2
import torch
import numpy as np
import os

from numpy import random
from models.experimental import attempt_load
from utils.datasets import letterbox
from utils.general import check_img_size, check_requirements, non_max_suppression, scale_coords
from utils.plots import plot_one_box
from utils.torch_utils import select_device, time_synchronized
from sklearn.linear_model import LinearRegression

WEIGHTS = 'tinybest2.pt'
IMG_SIZE = 1280
DEVICE = 'cuda'
AUGMENT = False
CONF_THRES = 0.5
IOU_THRES = 0.45
CLASSES = None
AGNOSTIC_NMS = False

file_num = 0
while os.path.exists(f"coords_{file_num}.txt"):
    file_num += 1

f = open(f"coords_{file_num}.txt", "a")

print(torch.version.cuda)
print(torch.cuda.device_count())

# Webcam
cap = cv2.VideoCapture(0)

# Initialize
device = select_device(DEVICE)
half = device.type != 'cpu'  # half precision only supported on CUDA
print('device:', device)

# Load model
model = attempt_load(WEIGHTS, map_location=device)  # load FP32 model
stride = int(model.stride.max())  # model stride
imgsz = check_img_size(IMG_SIZE, s=stride)  # check img_size
if half:
    model.half()  # to FP16

# Get names and colors
names = model.module.names if hasattr(model, 'module') else model.names

if not names:
    raise ValueError("No classes found in the model. Please check the model.")

colors = [[random.randint(0, 255) for _ in range(3)] for _ in range(len(names))]

# Run inference
if device.type != 'cpu':
    model.to(device)
    model(torch.zeros(1, 3, imgsz, imgsz).to(device).type_as(next(model.parameters())))  # run once

# Define the focal length and known object width
focal_length_x = 1349.068  # 카메라 초점 거리 in pixels (x축 방향)
focal_length_y = 1355.048  # 카메라 초점 거리 in pixels (y축 방향)
known_width = 0.098  # 객체의 실제 폭

# Track the previous positions of each detected object
previous_positions = {}

def predict_future_positions(previous_positions, future_steps):
    model = LinearRegression()
    model.fit(np.arange(len(previous_positions)).reshape(-1, 1), np.array(previous_positions))

    future_positions = model.predict(np.arange(len(previous_positions), len(previous_positions) + future_steps).reshape(-1, 1))
    return future_positions


# Define a function to estimate distance from object size (assuming camera intrinsics are known)
def estimate_distance(bbox_width, focal_length_x, known_width):
    distance_x = (known_width * focal_length_x) / bbox_width
    return distance_x

# Detect function
# 기존 코드에서 불필요한 부분을 제거하고, 바운딩 박스에 distance 값만 출력하도록 수정

def detect(frame):
    img0 = frame

    img = letterbox(img0, imgsz, stride=stride)[0]

    img = img[:, :, ::-1].transpose(2, 0, 1) 
    img = np.ascontiguousarray(img)

    img = torch.from_numpy(img).to(device)
    img = img.half() if half else img.float()  
    img /= 255.0 
    if img.ndimension() == 3:
        img = img.unsqueeze(0)

    t0 = time_synchronized()
    pred = model(img, augment=AUGMENT)[0]

    pred = non_max_suppression(pred, CONF_THRES, IOU_THRES, classes=CLASSES, agnostic=AGNOSTIC_NMS)

    det = pred[0]

    if len(det):
        det[:, :4] = scale_coords(img.shape[2:], det[:, :4], img0.shape).round()

        for *xyxy, conf, cls in reversed(det):
            x1, y1, x2, y2 = [int(xyxy[i]) for i in range(4)]

            bbox_width = xyxy[2] - xyxy[0]
            distance = estimate_distance(bbox_width, focal_length_x, known_width)
            f.write(f'distance: {distance:.2f}m\n')

            cls = int(cls)
            if cls >= len(colors):
                raise ValueError(f"Detected class {cls} is out of bounds. Please check the model.")
            plot_one_box(xyxy, img0, color=colors[cls], line_thickness=3)
            
            # 바운딩 박스에 클래스명과 거리 표시
            class_name = names[int(cls)]  # 클래스명 추가
            text = f'{class_name}: {distance:.2f}m'
            cv2.putText(img0, text, (int(x1), int(y1) - 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, colors[int(cls)], 2)

            print(f'Inferencing and Processing Done. ({time.time() - t0:.3f}s)')
            print(f'{class_name}: {distance:.2f}m\n')

    return img0








# main
check_requirements(exclude=('pycocotools', 'thop'))
with torch.no_grad():
    frame_rate = 0
    start_time = time.time()
    while True:
        ret, frame = cap.read()
        result = detect(frame)
        
        # Calculate frame rate
        frame_rate += 1
        elapsed_time = time.time() - start_time
        if elapsed_time > 1:
            frame_rate = frame_rate / elapsed_time
            start_time = time.time()
            frame_rate_text = f'FPS: {frame_rate:.2f}'
            cv2.putText(result, frame_rate_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)
            frame_rate = 0
        
        cv2.imshow('pred_image', result)

        if cv2.waitKey(1) == ord('q'):
            break


