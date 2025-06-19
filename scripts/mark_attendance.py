import face_recognition
import cv2
import pickle
import os
import numpy as np
from datetime import datetime

# Load encodings
with open("../encodings/encodings.pickle", "rb") as f:
    data = pickle.load(f)

# Track who has been marked already
marked_names = set()

# Create attendance directory if it doesn't exist
os.makedirs("../attendance", exist_ok=True)
filename = f"../attendance/Attendance_{datetime.now().date()}.csv"

# Create the CSV file if it doesn't exist
if not os.path.isfile(filename):
    with open(filename, "w") as f:
        f.write("Name,Time\n")

# Start video
cam = cv2.VideoCapture(0)
print("[INFO] Starting webcam. Press 'q' to stop...")

while True:
    ret, frame = cam.read()
    if not ret:
        break

    # Resize for faster processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    # Detect faces and encodings
    boxes = face_recognition.face_locations(rgb_small)
    encodings = face_recognition.face_encodings(rgb_small, boxes)

    for encoding, face_loc in zip(encodings, boxes):
        matches = face_recognition.compare_faces(data["encodings"], encoding, tolerance=0.5)
        name = "Unknown"

        if True in matches:
            matched_idxs = [i for (i, b) in enumerate(matches) if b]
            counts = {}

            for i in matched_idxs:
                matched_name = data["names"][i]
                counts[matched_name] = counts.get(matched_name, 0) + 1

            name = max(counts, key=counts.get)

            if name not in marked_names:
                now = datetime.now().strftime("%H:%M:%S")
                with open(filename, "a") as f:
                    f.write(f"{name},{now}\n")
                marked_names.add(name)
                print(f"[LOG] Marked {name} as present at {now}")

        # Draw rectangle & name
        top, right, bottom, left = [v * 4 for v in face_loc]
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    cv2.imshow("Attendance", frame)
    if cv2.waitKey(1) == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
print(f"[INFO] Attendance saved to {filename}")
