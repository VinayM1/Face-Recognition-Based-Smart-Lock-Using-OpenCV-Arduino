import cv2
import os
import numpy as np

# Path to your dataset folder
dataset_path = "dataset"

# Create the LBPH face recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()

# Load the face cascade
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

def get_images_and_labels(path):
    image_paths = [os.path.join(path, f) for f in os.listdir(path) if f.endswith(".jpg")]
    face_samples = []
    ids = []

    for image_path in image_paths:
        # Load image in grayscale
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            print(f"Warning: Could not read image {image_path}")
            continue

        # Extract user ID from filename: User.{id}.{num}.jpg
        filename = os.path.basename(image_path)
        try:
            id_str = filename.split('.')[1]
            user_id = int(id_str)
        except:
            print(f"Warning: Could not extract user ID from filename {filename}")
            continue

        # Detect face in the image (optional, but recommended to confirm face region)
        faces = face_cascade.detectMultiScale(img)
        if len(faces) == 0:
            print(f"Warning: No face detected in {filename}")
            continue

        for (x, y, w, h) in faces:
            face_roi = img[y:y+h, x:x+w]
            face_samples.append(face_roi)
            ids.append(user_id)
            break  # Only use the first detected face

    return face_samples, ids

print("🔄 Training face recognizer. Please wait...")

faces, ids = get_images_and_labels(dataset_path)
if len(faces) == 0:
    print("❌ No faces found in dataset. Please capture faces first.")
    exit()

recognizer.train(faces, np.array(ids))

# Save the trained model
recognizer.write("trainer.yml")

print(f"✅ Training completed. {len(set(ids))} users trained, {len(faces)} face samples total.")
print("Trainer model saved as trainer.yml")
