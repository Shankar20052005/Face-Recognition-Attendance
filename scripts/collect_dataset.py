import cv2
import os

name = input("Enter your name: ")
save_path = f"../dataset/{name}"
os.makedirs(save_path, exist_ok=True)

cam = cv2.VideoCapture(0)
detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

count = 0
print("Starting to capture. Press 'q' to quit.")

while True:
    ret, frame = cam.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        count += 1
        face = frame[y:y + h, x:x + w]
        cv2.imwrite(f"{save_path}/{count}.jpg", face)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    cv2.imshow("Collecting Faces", frame)
    if cv2.waitKey(1) == ord('q') or count >= 50:
        break

cam.release()
cv2.destroyAllWindows()
print(f"Saved {count} images in {save_path}")
