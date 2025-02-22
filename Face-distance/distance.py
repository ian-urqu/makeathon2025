from turtle import distance
import cv2
import numpy as np
import serial
import time

know_distance = 66  # (que) What is this?
know_width = 14.3

# Colors
GREEN = (0, 255, 0)
RED = (0, 0, 255)
WHITE = (255, 255, 255)
fonts = cv2.FONT_HERSHEY_COMPLEX
cap = cv2.VideoCapture(0)

face_detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

def send_data_to_arduino(angle, distance):
    # Format the data as "angle,distance" (e.g., "45,10")
    data = f"{angle},{distance}\n"
    arduino.write(data.encode())  # Send the data to Arduino
    print(f"Sent: {data.strip()}")

# focal length finder function
def focal_length(
    measured_distance, real_width, width_in_rf_image
):  # (que) How it got measured (measured_distance)!
    focal_length_value = (width_in_rf_image * measured_distance) / real_width
    return focal_length_value


# distance estimation function
def distance_finder(focal_length, real_face_width, face_width_in_frame):
    distance = (real_face_width * focal_length) / face_width_in_frame
    return distance


def face_data(image):
    face_width = 0
    angle_deg = 0
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    img_height, img_width, _ = image.shape

    faces = face_detector.detectMultiScale(gray_image, 1.3, 5)
    if len(faces) == 0:
        # No face found – return zero or None so downstream code can ignore
        return 0, 0

    # If faces were found, pick one (see below if you want only the largest face)
    x, y, w, h = faces[0]
    cv2.rectangle(image, (x, y), (x + w, y + h), GREEN, 1)
    face_width = w  # now correct usage of "w" as width

    face_center_x = x + w / 2
    face_center_y = y + h / 2

    center_x = img_width / 2
    center_y = img_height / 2

    # Using your known FOV or derived focal length for horizontal angle
    f_x = (img_width / 2) / np.tan(np.radians(67 / 2))
    angle_deg = np.degrees(np.arctan((face_center_x - center_x) / f_x))

    return face_width, angle_deg


# reading reference image from directory
ref_image = cv2.imread("Refimg3.jpg")

ref_image_face_width, _ = face_data(ref_image)
focal_length_found = focal_length(know_distance, know_width, ref_image_face_width)
print(focal_length_found)
# cv2.imshow("ref_image", ref_image)

arduino = serial.Serial(port="COM6", baudrate=9600, timeout=1)
time.sleep(2)  # Wait for the Arduino to initialize
while True:
    ret, frame = cap.read()

    face_width_in_frame, angle = face_data(frame)

    if face_width_in_frame > 0:
        # Drwaing Text on the screen
        dist = distance_finder(focal_length_found, know_width, face_width_in_frame)
        rad = dist/np.cos(np.radians(angle))
        cv2.putText(
            frame, f"Rad = {round(rad,2)} CM", (50, 50), fonts, 1, (RED), 2
        )
        cv2.putText(
            frame, f"Angle = {round(angle,2)} degrees", (50, 100), fonts, 1, (GREEN), 2
        )
        send_data_to_arduino(angle, rad)



    if dist < 40:  # (que) why 40?
        cv2.putText(
            frame, "You are too close to the screen", (30, 30), fonts, 1, (RED), 1
        )
    cv2.imshow("frame", frame)
    if cv2.waitKey(1) == ord("q"):
        break
cap.release()
cv2.destroyAllWindows()
