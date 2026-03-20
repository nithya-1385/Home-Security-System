import cv2
import serial
import numpy as np
import time

# Initialize serial communication with Arduino
arduino = serial.Serial('COM4', 9600, timeout=1)  # Replace 'COM3' with your port
time.sleep(2)  # Wait for Arduino to reset

# Load face recognition model and label mapqq
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("Trainer.yml")
label_map = np.load("label_map.npy", allow_pickle=True).item()

# Initialize webcam and face detector
video = cv2.VideoCapture(0)
facedetect = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

def send_command(cmd):
    arduino.write(cmd.encode())
    time.sleep(0.1)
    while arduino.in_waiting:
        print("Arduino:", arduino.readline().decode().strip())

while True:
    if arduino.in_waiting > 0:
        message = arduino.readline().decode().strip()
        print("Arduino:", message)

        if message == "MOTION":
            print("Motion detected, starting face recognition...")
            ret, frame = video.read()
            if not ret:
                continue

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = facedetect.detectMultiScale(gray, 1.3, 5)

            recognized = False
            for (x, y, w, h) in faces:
                face_roi = gray[y:y+h, x:x+w]
                label_id, confidence = recognizer.predict(face_roi)

                if confidence < 50:
                    name = label_map[label_id]
                    print(f"Recognized: {name} with confidence {confidence}")
                    recognized = True
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    cv2.putText(frame, name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                else:
                    print(f"Unknown face detected with confidence {confidence}")
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
                    cv2.putText(frame, "Unknown", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

            cv2.imshow("Face Recognition", frame)
            cv2.waitKey(1)

            if recognized:
                send_command('U')  # Send unlock command
            else:
                send_command('B')  # Send buzzer command

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
arduino.close()
