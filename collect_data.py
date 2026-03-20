import cv2
import os

# Initialize webcam and face detector
video = cv2.VideoCapture(0)
facedetect = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Create a folder for the person's images
name = input("Enter your name: ")
dataset_path = f"dataset/{name}"
os.makedirs(dataset_path, exist_ok=True)

print("Collecting images... Press 'q' to stop.")
count = 0

while True:
    ret, frame = video.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facedetect.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        count += 1
        face = gray[y:y+h, x:x+w]
        cv2.imwrite(f"{dataset_path}/{count}.jpg", face)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q') or count >= 100:
        break

video.release()
cv2.destroyAllWindows()
print(f"Images saved in {dataset_path}")
