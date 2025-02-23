import cv2
import numpy as np
import serial
import time
import threading

# Known parameters (adjust as needed)
know_distance = 63.5 / 2 - 5  # Known distance when the reference image was taken (in cm)
know_width = 14.3             # Known width of the face (in cm)

# Colors for display
GREEN = (0, 255, 0)
RED = (0, 0, 255)
WHITE = (255, 255, 255)
fonts = cv2.FONT_HERSHEY_COMPLEX

# Initialize video capture
cap = cv2.VideoCapture(0)

# Load Haar Cascade for face detection
face_detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# Open serial port (adjust COM port if necessary)
arduino = serial.Serial(port="COM6", baudrate=9600, timeout=1)
time.sleep(2)  # Wait for Arduino to initialize

def send_data_to_arduino(data):
    # This function is used by the serial thread to send data
    try:
        arduino.write(data.encode())
        arduino.flush()
        print(f"Sent: {data.strip()}")
    except Exception as e:
        print("Serial write error:", e)

def focal_length(measured_distance, real_width, width_in_rf_image):
    focal_length_value = (width_in_rf_image * measured_distance) / real_width
    return focal_length_value

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
        return 0, 0

    x, y, w, h = faces[0]
    cv2.rectangle(image, (x, y), (x + w, y + h), GREEN, 1)
    face_width = w

    face_center_x = x + w / 2
    center_x = img_width / 2

    f_x = (img_width / 2) / np.tan(np.radians(67 / 2))
    angle_deg = np.degrees(np.arctan((face_center_x - center_x) / f_x))
    return face_width, angle_deg

# Read reference image to compute focal length
ref_image = cv2.imread("Ref_image2.jpg")
ref_image_face_width, _ = face_data(ref_image)
focal_length_found = focal_length(know_distance, know_width, ref_image_face_width)
print(f"Focal Length Found: {focal_length_found}")

# Global variable and lock for serial data to send
latest_data = None
data_lock = threading.Lock()

# Serial sender thread: sends the latest data every 0.25 seconds
def serial_sender():
    global latest_data
    while True:
        with data_lock:
            data_to_send = latest_data
            # Optionally clear latest_data after sending
            latest_data = None  
        if data_to_send is not None:
            send_data_to_arduino(data_to_send)
        time.sleep(0.1)  # Adjust sending rate as needed

# Start the serial sender thread (daemon so it exits when main thread does)
threading.Thread(target=serial_sender, daemon=True).start()

# Global variable to store previous angle (for rotation time calculation)
prev_angle = 0.0
angVel = 21.99  # Angular velocity in cm/s

while True:
    ret, frame = cap.read()
    if not ret:
        break

    face_width_in_frame, angle = face_data(frame)
    dist = 9999  # Default distance if no face detected

    if face_width_in_frame > 0:
        dist = distance_finder(focal_length_found, know_width, face_width_in_frame)
        rad = dist / np.cos(np.radians(angle))
        
        cv2.putText(frame, f"Rad = {round(rad,2)} CM", (50, 50), fonts, 1, RED, 2)
        cv2.putText(frame, f"Angle = {round(angle,2)} deg", (50, 100), fonts, 1, GREEN, 2)
        
        # Compute rotation time based on change in angle
        angle_diff_deg = angle - prev_angle
        angle_diff_rad = np.radians(angle_diff_deg)
        arc_length = angle_diff_rad * rad
        rotate_time = arc_length / angVel
        
        # Optionally, print these values for debugging
        print(f"Angle Diff: {angle_diff_deg:.2f} deg, Arc Length: {arc_length:.2f} cm, Rotate Time: {rotate_time:.2f} s")
        
        # Update previous angle
        prev_angle = angle
        
        # Prepare data to send via serial
        data = f"{angle},{rad}\n"
        with data_lock:
            latest_data = data

    if dist < 40:
        cv2.putText(frame, "You are too close to the screen", (30, 30), fonts, 1, RED, 1)
    cv2.imshow("frame", frame)
    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
