import cv2
import numpy as np

# Load trained model and label map
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("Trainer.yml")
label_map = np.load("label_map.npy", allow_pickle=True).item()

# Initialize webcam and face detector
video = cv2.VideoCapture(0)
facedetect = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

while True:
    ret, frame = video.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facedetect.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        face_roi = gray[y:y+h, x:x+w]
        label_id, confidence = recognizer.predict(face_roi)

        if confidence < 50:  # Recognized with high confidence
            name = label_map[label_id]
            color = (0, 255, 0)
            text = f"{name} ({int(confidence)}%)"
        else:  # Unknown face
            name = "Unknown"
            color = (0, 0, 255)
            text = "Unknown"

        # Draw rectangle and display name
        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
        cv2.putText(frame, text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

    cv2.imshow("Face Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
        break

video.release()
cv2.destroyAllWindows()
