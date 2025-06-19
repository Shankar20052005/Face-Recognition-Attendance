import os
import cv2
import face_recognition
import pickle

dataset_dir = "../dataset"
encoding_file = "../encodings/encodings.pickle"

known_encodings = []
known_names = []

print("[INFO] Processing images...")

for person_name in os.listdir(dataset_dir):
    person_path = os.path.join(dataset_dir, person_name)

    if not os.path.isdir(person_path):
        continue

    for img_name in os.listdir(person_path):
        img_path = os.path.join(person_path, img_name)
        image = cv2.imread(img_path)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        boxes = face_recognition.face_locations(rgb, model="hog")
        encodings = face_recognition.face_encodings(rgb, boxes)

        for encoding in encodings:
            known_encodings.append(encoding)
            known_names.append(person_name)

print(f"[INFO] Encoded {len(known_encodings)} face(s).")

# Save encodings to file
data = {"encodings": known_encodings, "names": known_names}
with open(encoding_file, "wb") as f:
    pickle.dump(data, f)

print(f"[INFO] Encodings saved to {encoding_file}")
