from os import name
import pickle


def register_face(name):
    import pickle
    import numpy as np
    import cv2
    import face_recognition
    import os

    # ===== Validate Name =====
    if not name or name.strip() == "":
        print("Invalid name.")
        return

    name = name.strip()

    # ===== Create Dataset Folder =====
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    dataset_path = os.path.join(BASE_DIR, "dataset", name)
    os.makedirs(dataset_path, exist_ok=True)

    # ===== Start Camera =====
    cap = cv2.VideoCapture(1)

    if not cap.isOpened():
        print("Camera not accessible.")
        return

    count = 0
    max_images = 15

    print("Press 's' to capture image | Press 'q' to quit")

    try:
        while True:
            ret, frame = cap.read()

            if not ret or frame is None:
                print("Camera read error.")
                break

            # Convert to RGB for face detection
            rgb = frame[:, :, ::-1]

            faces = face_recognition.face_locations(rgb)

            # Draw rectangle around face
            for (top, right, bottom, left) in faces:
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

            cv2.putText(
                frame,
                f"Images Captured: {count}/{max_images}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2,
            )

            cv2.imshow("Register Face", frame)

            key = cv2.waitKey(1) & 0xFF

            # ===== Capture Image =====
            if key == ord('s') and len(faces) > 0:
                top, right, bottom, left = faces[0]
                face = frame[top:bottom, left:right]

                img_path = os.path.join(dataset_path, f"{count}.jpg")
                cv2.imwrite(img_path, face)

                print(f"Saved image {count}")
                count += 1

            # ===== Exit Conditions =====
            if key == ord('q') or count >= max_images:
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()

    encodings_file = os.path.join(BASE_DIR, "encodings.pkl")
    known_encodings = []
    known_names = []
    # Load existing encodings if file exists
    if os.path.exists(encodings_file):
        with open(encodings_file, "rb") as f:
            data = pickle.load(f)
            known_encodings = data["encodings"]
            known_names = data["names"]
            
    # Process newly captured images
    for img_name in os.listdir(dataset_path):
        img_path = os.path.join(dataset_path, img_name)

    try:
        image = face_recognition.load_image_file(img_path)

        encodings = face_recognition.face_encodings(image)

        if encodings:
            known_encodings.append(encodings[0])
            known_names.append(name)

    except Exception as e:
        print(f"Encoding error: {e}")
        
    # Save updated encodings
    with open(encodings_file, "wb") as f:
        pickle.dump({
            "encodings": known_encodings,
            "names": known_names
        }, f)
    
    print(f"Registration completed for {name}")