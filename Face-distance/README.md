# Facedistance
📸💡 Face Distance Calculation between camera and person 💡📸

💻 This Python code leverages computer vision techniques and the OpenCV library to estimate the distance between a camera and a person's face in real-time. By using a known distance and width for calibration, the code calculates the focal length of the camera.

🔬 The code includes a focal length finder function that determines the focal length based on the known distance, known width, and the width of the face in a reference image.

📷 A distance estimation function is implemented to estimate the distance between the camera and the person's face using the calculated focal length, known face width, and the current face width in the frame.

🔍 The face_data function utilizes the Haar cascade classifier to detect faces in the image and returns the width of the detected face.

⚙️ The code captures video from the camera using OpenCV's VideoCapture function and continuously estimates the distance of the person's face within each frame.

📏 The calculated distance is displayed on the screen using OpenCV's putText function, and a warning message is shown if the person is too close to the screen.

🖥️ The program runs until the user presses the 'q' key, allowing for continuous real-time face distance estimation. Upon exiting, the video capture is released, and the windows are closed.

💡✨ Utilize this code to accurately estimate the distance between a camera and a person's face. It opens up possibilities for various applications, including human-computer interaction and augmented reality experiences.
