# Face-Recognition-Based-Smart-Lock-Using-OpenCV-Arduino
This project is a real-time smart lock system that uses face recognition for secure, contactless access. A webcam captures the user’s face, detects it using a Haar Cascade Classifier, and recognizes it with OpenCV’s LBPH algorithm.  If the face is authorized, a command is sent via serial communication to an Arduino,

# 🔒 Face Recognition Smart Lock System

This project is a real-time **smart lock system** that uses **face recognition** for secure and hands-free access. It combines **OpenCV** for face detection and recognition with **Arduino** to control a **servo motor** acting as the door lock.

---

## 🧠 How It Works

1. A **webcam** captures the user's face.
2. **Haar Cascade Classifier** detects the face in real-time.
3. **LBPH (Local Binary Patterns Histograms)** algorithm recognizes the user.
4. If the face is **authorized**, a signal is sent via **serial communication** to the **Arduino**.
5. The **Arduino** rotates a **servo motor** to unlock the door for 5 seconds.
6. If the face is **not recognized**, the door remains locked.

---

## 🗂 Project Structure

| File/Folder           | Description                                  |
|-----------------------|----------------------------------------------|
| `capture_faces.py`    | Captures face samples and saves them         |
| `train_model.py`      | Trains LBPH face recognizer and saves model  |
| `trainer.py`          | Real-time recognition and Arduino control    |
| `dataset/`            | Stores captured face images                  |
| `trainer.yml`         | Trained model file                           |
| `haarcascade_frontalface_default.xml` | Face detection XML file     |
| `Arduino Code (.ino)` | Controls the servo motor via serial input    |

---

## 🔧 Requirements

### Hardware:
- Arduino UNO (or compatible)
- Servo Motor (SG90 recommended)
- USB cable
- Webcam
- Jumper wires and breadboard (optional)

### Software:
- Python 3
- OpenCV (`opencv-contrib-python`)
- Arduino IDE

Install dependencies:

```bash
pip install opencv-contrib-python
