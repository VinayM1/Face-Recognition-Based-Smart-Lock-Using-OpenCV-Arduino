import cv2
import os

# ====== LOAD CASCADE SAFELY ======
def load_cascade():
    # Try OpenCV's built-in data path first
    opencv_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    if os.path.exists(opencv_path):
        cascade = cv2.CascadeClassifier(opencv_path)
        if not cascade.empty():
            print(f"✅ Loaded cascade from OpenCV directory: {opencv_path}")
            return cascade
    
    # Try other possible locations
    paths_to_try = [
        "haarcascade_frontalface_default.xml",  # Current directory
        r"D:\FaceRecognition_Lock\haarcascade_frontalface_default.xml",  # Your project path
        r"D:\Face Recognition_Lock\haarcascade_frontalface_default.xml"  # Alternative path
    ]
    
    for path in paths_to_try:
        if os.path.exists(path):
            cascade = cv2.CascadeClassifier(path)
            if not cascade.empty():
                print(f"✅ Loaded cascade from: {path}")
                return cascade
    
    print("❌ Error: Could not load face cascade.")
    print("Please ensure haarcascade_frontalface_default.xml exists in one of these locations:")
    print(f"- {opencv_path}")
    for path in paths_to_try:
        print(f"- {path}")
    exit()

face_cascade = load_cascade()

# ====== SETUP FOR FACE CAPTURE ======
cam = cv2.VideoCapture(0)
user_id = input("Enter numeric user ID: ")

dataset_dir = "dataset"
os.makedirs(dataset_dir, exist_ok=True)
sample_count = 0

while True:
    ret, frame = cam.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        sample_count += 1
        face_img = gray[y:y+h, x:x+w]
        file_path = f"{dataset_dir}/User.{user_id}.{sample_count}.jpg"
        cv2.imwrite(file_path, face_img)

        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        cv2.putText(frame, f"Samples: {sample_count}", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    cv2.imshow('Capturing Faces - Press Q to quit', frame)

    if cv2.waitKey(1) & 0xFF == ord('q') or sample_count >= 50:
        break

cam.release()
cv2.destroyAllWindows()
print(f"✅ Saved {sample_count} face samples for User ID {user_id}")
