import cv2

print("OpenCV version:", cv2.__version__)
print("LBPH Available:", hasattr(cv2.face, 'LBPHFaceRecognizer_create'))

import serial
import time
import os

# === SERIAL SETUP ===
try:
    arduino = serial.Serial('COM9', 9600, timeout=1)  # Change COM port if needed
    time.sleep(2)  # Wait for Arduino to initialize
    print("✅ Arduino connected on COM9")
except:
    print("❌ Error: Could not connect to Arduino. Check the COM port.")
    arduino = None

# === LOAD FACE RECOGNIZER ===
recognizer = cv2.face.LBPHFaceRecognizer_create()

if not os.path.exists("trainer.yml"):
    print("❌ Error: trainer.yml not found. Please run the training script first.")
    exit()

recognizer.read('trainer.yml')

# === LOAD FACE DETECTOR ===
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# === CAMERA SETUP ===
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("❌ Error: Could not access the webcam.")
    exit()

# === DEBOUNCE VARIABLES ===
last_status = None
last_sent_time = time.time()
DEBOUNCE_SECONDS = 2  # time gap between signals to Arduino

print("🎥 Starting camera... Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Error: Frame not captured.")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    for (x, y, w, h) in faces:
        face_roi = gray[y:y+h, x:x+w]
        id_, confidence = recognizer.predict(face_roi)

        # Lower confidence = better match
        if confidence < 60:
            label = f"User {id_} ({round(100 - confidence)}%)"
            status = 'U'  # Unlock
        else:
            label = "Unknown"
            status = 'L'  # Lock

        # Debounce to prevent serial flooding
        if status != last_status or (time.time() - last_sent_time) > DEBOUNCE_SECONDS:
            if arduino:
                arduino.write(status.encode())
            last_status = status
            last_sent_time = time.time()

        # Draw box and label
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, label, (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

    cv2.imshow("🔒 Face Lock System", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# === CLEANUP ===
cap.release()
cv2.destroyAllWindows()
if arduino:
    arduino.close()
print("✅ Program closed.")
