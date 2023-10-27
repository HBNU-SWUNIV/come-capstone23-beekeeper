import cv2
import numpy as np
import time
from djitellopy import Tello

# Set points (center of the frame coordinates in pixels)
rifX, rifY = 960/2, 720/2

# PI constants
Kp_X, Ki_X = 0.1, 0.0
Kp_Y, Ki_Y = 0.2, 0.0

# Loop time
Tc = 0.05

# PI terms initialized
integral_X, error_X, previous_error_X = 0, 0, 0
integral_Y, error_Y, previous_error_Y = 0, 0, 0

centroX_pre, centroY_pre = rifX, rifY

# Load YOLOv4 model
yolo_net = cv2.dnn.readNet("yolov4.weights", "yolov4.cfg")  # Replace with your YOLOv4 weight and configuration files
layer_names = yolo_net.getUnconnectedOutLayersNames()

# Initialize YOLOv4 classes
yolo_classes = ["drone"]  # Replace with your specific drone class
yolo_colors = np.random.uniform(0, 255, size=(len(yolo_classes), 3))

# Initialize the drone
drone = Tello()
time.sleep(2.0)  # Waiting 2 seconds
print("Connecting...")
drone.connect()
print("BATTERY:")
print(drone.get_battery())
time.sleep(1.0)
print("Loading...")
drone.streamon()  # Start camera streaming
print("Takeoff...")
drone.takeoff()  # Drone takeoff

while True:
    start_time = time.time()
    frame = drone.get_frame_read().frame

    cv2.circle(frame, (int(rifX), int(rifY)), 10, (0, 0, 255), -1)

    h, w, channels = frame.shape
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

    yolo_net.setInput(blob)
    yolo_detections = yolo_net.forward(layer_names)

    selected_object = None
    max_confidence = 0.0

    for yolo_detection in yolo_detections:
        for yolo_obj in yolo_detection:
            scores = yolo_obj[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            
            if confidence > 0.6 and class_id == 0:  # Assuming class 0 is the drone
                center_x, center_y, width, height = (yolo_obj[0:4] * np.array([w, h, w, h])).astype(int)
                startX, startY = center_x - width // 2, center_y - height // 2
                endX, endY = startX + width, startY + height

                if confidence > max_confidence:
                    max_confidence = confidence
                    selected_object = yolo_obj

                label = "Drone: {:.2f}%".format(confidence * 100)
                cv2.rectangle(frame, (startX, startY), (endX, endY), yolo_colors[class_id], 2)

                centroX = (startX + endX) / 2
                centroY = (startY + endY) / 2
                centroX_pre = centroX
                centroY_pre = centroY

                cv2.circle(frame, (int(centroX), int(centroY)), 1, (0, 0, 255), 10)

                error_X = -(rifX - centroX)
                error_Y = rifY - centroY

                cv2.line(frame, (int(rifX), int(rifY)), (int(centroX), int(centroY)), (0, 255, 255), 5)

                y = startY - 15 if startY - 15 > 15 else startY + 15
                cv2.putText(frame, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, yolo_colors[class_id], 2)

                # PI controller
                integral_X = integral_X + error_X * Tc
                uX = Kp_X * error_X + Ki_X * integral_X
                previous_error_X = error_X

                integral_Y = integral_Y + error_Y * Tc
                uY = Kp_Y * error_Y + Ki_Y * integral_Y
                previous_error_Y = error_Y

                drone.send_rc_control(0, 0, round(uY), round(uX))

                # Exit the loop after processing the first detection
                break

    if selected_object is None:  # If no drone is recognized, use previous frame's center as reference
        centroX = centroX_pre
        centroY = centroY_pre
        cv2.circle(frame, (int(centroX), int(centroY)), 1, (0, 0, 255), 10)

        error_X = -(rifX - centroX)
        error_Y = rifY - centroY

        cv2.line(frame, (int(rifX), int(rifY)), (int(centroX), int(centroY)), (0, 255, 255), 5)

        integral_X = integral_X + error_X * Tc
        uX = Kp_X * error_X + Ki_X * integral_X
        previous_error_X = error_X

        integral_Y = integral_Y + error_Y * Tc
        uY = Kp_Y * error_Y + Ki_Y * integral_Y
        previous_error_Y = error_Y

        drone.send_rc_control(0, 0, round(uY), round(uX))

    cv2.imshow("Frame", frame)

    end_time = time.time()
    elapsed_time = end_time - start_time
    if Tc - elapsed_time > 0:
        time.sleep(Tc - elapsed_time)
    end_time_ = time.time()
    elapsed_time_ = end_time_ - start_time
    fps = 1 / elapsed_time_
    print("FPS:", fps)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

drone.streamoff()
cv2.destroyAllWindows()
drone.land()
print("Landing...")
print("BATTERY:")
print(drone.get_battery())
drone.end()
