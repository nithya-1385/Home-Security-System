import cv2
import numpy as np
import os

# Initialize recognizer and face detector
recognizer = cv2.face.LBPHFaceRecognizer_create()
facedetect = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

def prepare_training_data(data_folder):
    faces = []
    labels = []
    label_map = {}
    label_id = 0

    for person_name in os.listdir(data_folder):
        person_folder = os.path.join(data_folder, person_name)
        if not os.path.isdir(person_folder):
            continue
        
        label_map[label_id] = person_name
        
        for img_name in os.listdir(person_folder):
            img_path = os.path.join(person_folder, img_name)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            faces.append(img)
            labels.append(label_id)
        
        label_id += 1

    return faces, np.array(labels), label_map

faces, labels, label_map = prepare_training_data("dataset")
recognizer.train(faces, labels)

# Save the trained model and label map
recognizer.save("Trainer.yml")
np.save("label_map.npy", label_map)
print("Training completed!")
