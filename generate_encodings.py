import os
import pickle
import face_recognition

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(BASE_DIR, "dataset")

known_encodings = []
known_names = []

print("Generating encodings...")

for person in os.listdir(DATASET_PATH):

    person_path = os.path.join(DATASET_PATH, person)

    if not os.path.isdir(person_path):
        continue

    for img_name in os.listdir(person_path):

        img_path = os.path.join(person_path, img_name)

        try:
            image = face_recognition.load_image_file(img_path)

            encodings = face_recognition.face_encodings(image)

            if encodings:
                known_encodings.append(encodings[0])
                known_names.append(person)

                print(f"Encoded: {person} -> {img_name}")

        except Exception as e:
            print(f"Error with {img_path}: {e}")

# Save encodings
encodings_file = os.path.join(BASE_DIR, "encodings.pkl")

with open(encodings_file, "wb") as f:

    pickle.dump({
        "encodings": known_encodings,
        "names": known_names
    }, f)

print("\nEncodings saved successfully!")