from turtle import distance
import cv2

know_distance = 30 #(que) What is this?
know_width = 14.3

#Colors
GREEN = (0,255,0)
RED = (0,0,255)
WHITE = (255, 255, 255)
fonts = cv2.FONT_HERSHEY_COMPLEX
cap = cv2.VideoCapture(0)

face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# focal length finder function
def focal_length(measured_distance, real_width, width_in_rf_image): # (que) How it got measured (measured_distance)!
    focal_length_value = (width_in_rf_image * measured_distance) / real_width
    return focal_length_value


# distance estimation function
def distance_finder(focal_length, real_face_width, face_width_in_frame):
    distance = (real_face_width * focal_length) / face_width_in_frame
    return distance

def face_data(image):
    face_width = 0
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray_image, 1.3, 5)
    for (x, y, h, w) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), GREEN, 1)
        face_width = w

    return face_width

# reading reference image from directory
ref_image = cv2.imread("Ref_image.jpg")

ref_image_face_width = face_data(ref_image)
focal_length_found = focal_length(know_distance, know_width, ref_image_face_width)
print(focal_length_found)
# cv2.imshow("ref_image", ref_image)

while True:
    _, frame = cap.read()

    face_width_in_frame = face_data(frame)
    dist = distance_finder(focal_length_found, know_width, face_width_in_frame)
    if face_width_in_frame != 0:
        # Drwaing Text on the screen
        cv2.putText(
            frame, f"Distance = {round(dist,2)} CM", (50, 50), fonts, 1, (WHITE), 2
        )

    if dist < 40: # (que) why 40?
        cv2.putText(
            frame, "You are too close to the screen", (30, 30), fonts, 1, (RED), 1
        )
    cv2.imshow("frame", frame)
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
