def show_summary(
    camera_label,
    present_students,
    absent_students,
    checks_completed
):

    summary_text = ("Attendance Summary\n\n")

    summary_text += (
        f"✔ Present Students: "
        f"{len(present_students)}\n\n"
    )
    summary_text += "\n"

    summary_text += (
    f"✘ Absent Students: "
    f"{len(absent_students)}\n\n"
    )

    summary_text += "\n"
    summary_text += (
        f"Checks Completed : "
        f"{checks_completed}\n\n"
    )

    summary_text += (
        "Attendance Saved Successfully ✔"
    )

    camera_label.after(
        0,
        lambda: camera_label.configure(
            text=summary_text,
            image="",
            font=("Segoe UI", 18, "bold"),
            text_color="#EAEAEA",
            justify="left"
        )
    )

def start_attendance(camera_label):
    import os
    import random
    import pickle
    import time
    import shared_state
    import customtkinter as ctk
    from PIL import Image, ImageTk
    from datetime import datetime

    import cv2
    import face_recognition
    import numpy as np

    # =========================
    # PATHS
    # =========================
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATASET_PATH = os.path.join(BASE_DIR, 'dataset')
    ATTENDANCE_FILE = os.path.join(BASE_DIR, 'attendance.csv')

    # =========================
    # SETTINGS
    # =========================
    TOLERANCE = 0.45

    # Lecture settings
    lecture_duration = 1  # minutes( We can later change for an hour)
    number_of_checks = 3
    required_presence = 2

    # =========================
    # KNOWN FACE DATA
    # =========================
    known_encodings = []
    known_names = []

    # =========================
    # MARK ATTENDANCE FUNCTION
    # =========================
    def mark_attendance(name):

        today = datetime.now().strftime('%Y-%m-%d')
        existing_names = set()

        if os.path.exists(ATTENDANCE_FILE):

            with open(ATTENDANCE_FILE, 'r', encoding='utf-8') as f:

                lines = f.readlines()[1:]  # skip header

                for line in lines:

                    parts = line.strip().split(',')

                    if len(parts) >= 2 and parts[1].startswith(today):
                        existing_names.add(parts[0])

        if name not in existing_names:

            with open(ATTENDANCE_FILE, 'a', encoding='utf-8') as f:

                f.write(
                    f'{name},{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n'
                )

    # =========================
    # LOAD SAVED ENCODINGS
    # =========================
    print("\nLoading face encodings...")
    encodings_file = os.path.join(BASE_DIR, "encodings.pkl")
    
    if not os.path.exists(encodings_file):
        print("No encodings file found.")
        return

    with open(encodings_file, "rb") as f:
        data = pickle.load(f)
        known_encodings = data["encodings"]
        known_names = data["names"]

    print(
        f"Loaded {len(known_encodings)} encodings "
        f"for {len(set(known_names))} people."
    )

    # =========================
    # CREATE ATTENDANCE FILE
    # =========================
    if (
        not os.path.exists(ATTENDANCE_FILE)
        or os.path.getsize(ATTENDANCE_FILE) == 0
    ):

        with open(ATTENDANCE_FILE, 'w', encoding='utf-8') as f:
            f.write('Name,Timestamp\n')

    # =========================
    # RANDOM ATTENDANCE CHECKS
    # =========================
    random_checks = sorted(
        random.sample(
            range(20, lecture_duration * 60 - 20),
            number_of_checks
        )
    )

    print("\nRandom attendance checks scheduled at:\n")

    for sec in random_checks:
        mins = sec // 60
        secs = sec % 60
        print(f"{mins:02d}:{secs:02d}")

    # =========================
    # CAMERA
    # =========================
    cap = cv2.VideoCapture(1)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    print("\nStarting smart attendance system...")
    print("Press 'q' to quit.\n")

    # =========================
    # TRACKING VARIABLES
    # =========================
    start_time = time.time()
    completed_checks = set()
    detection_counts = {}
    recent_detections = {}
    frame_count = 0

    # =========================
    # MAIN LOOP
    # =========================
    try:

        while True:
            if not shared_state.attendance_running:
                break
            ret, frame = cap.read()

            if not ret or frame is None:
                print("Failed to grab frame.")
                break

            frame_count += 1

            current_elapsed = int(time.time() - start_time)

            # =========================
            # STOP AFTER LECTURE
            # =========================
            if current_elapsed >= lecture_duration * 60:
                print("\nLecture ended.\n")
                break

            # =========================
            # PROCESS EVERY 2ND FRAME
            # =========================
            if frame_count % 3!= 0:  # Process every 3rd frame for speed

                #cv2.imshow('Attendance System', frame)

                key = cv2.waitKey(1)
                if key == ord('q'):
                    break
                continue

            # =========================
            # CHECK IF RANDOM CHECK TIME
            # =========================
            perform_check = False

            for check_time in random_checks:

                if (
                    current_elapsed >= check_time
                    and check_time not in completed_checks
                ):

                    perform_check = True

                    completed_checks.add(check_time)

                    mins = current_elapsed // 60
                    secs = current_elapsed % 60

                    print(
                        f"\nAttendance Check Started "
                        f"at {mins:02d}:{secs:02d}\n"
                    )

            # =========================
            # FACE DETECTION
            # =========================
            # Resize frame for speed
            small_frame = cv2.resize(
                frame,
                (0, 0),
                fx=0.5,
                fy=0.5
            )

            #Convert Resized frame to RGB
            rgb_small = cv2.cvtColor(
                small_frame,
                cv2.COLOR_BGR2RGB
            )

            #Detect Faces
            face_locations = face_recognition.face_locations(
                rgb_small,
                model="hog"
            )

            face_encodings = face_recognition.face_encodings(
                rgb_small,
                face_locations
            )
            
            # =========================
            # FACE MATCHING
            # =========================
            for encoding, (top, right, bottom, left) in zip(
                face_encodings,
                face_locations
            ):
                #scale coordinates back
                top *= 2
                right *= 2
                bottom *= 2
                left *= 2

                name = "Unknown"

                matches = face_recognition.compare_faces(
                    known_encodings,
                    encoding,
                    tolerance=TOLERANCE
                )

                if True in matches:

                    distances = face_recognition.face_distance(
                        known_encodings,
                        encoding
                    )

                    match_index = np.argmin(distances)

                    if (
                        matches[match_index]
                        and distances[match_index] < TOLERANCE
                    ):

                        candidate = known_names[match_index]

                        # =========================
                        # STABLE DETECTION
                        # =========================
                        if candidate not in recent_detections:
                            recent_detections[candidate] = 0

                        recent_detections[candidate] += 1

                        # Must appear consistently
                        if recent_detections[candidate] >= 3:

                            name = candidate

                            # =========================
                            # RECORD ONLY DURING CHECK
                            # =========================
                            if perform_check:

                                if name not in detection_counts:
                                    detection_counts[name] = 0

                                detection_counts[name] += 1

                                print(
                                    f"{name} detected "
                                    f"({detection_counts[name]}/"
                                    f"{number_of_checks})"
                                )

                # =========================
                # DRAW FACE BOX
                # =========================
                color = (
                    (0, 255, 0)
                    if name != "Unknown"
                    else (0, 0, 255)
                )

                # ===== Professional Corner Face Box =====

                line_len = 25
                thickness = 3
                
                # Top-left
                cv2.line(frame,(left, top),(left + line_len, top),color,thickness)
                cv2.line(frame,(left, top),(left, top + line_len),color,thickness)

                # Top-right
                cv2.line(frame,(right, top),(right - line_len, top),color,thickness)
                cv2.line(frame,(right, top),(right, top + line_len),color,thickness)
                
                # Bottom-left
                cv2.line(frame,(left, bottom),(left + line_len, bottom),color,thickness)
                cv2.line(frame,(left, bottom),(left, bottom - line_len),color,thickness)
                
                # Bottom-right
                cv2.line(frame,(right, bottom),(right - line_len, bottom),color,thickness)
                cv2.line(frame,(right, bottom),(right, bottom - line_len),color,thickness)

                cv2.putText(
                    frame,
                    name,
                    (left + 5, top - 15),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.9,
                    color,
                    2
                )

            # =========================
            # DISPLAY TOP INFO BAR
            # =========================
            mins = current_elapsed // 60
            secs = current_elapsed % 60

            timer_text =f"Lecture Time: {mins:02d}:{secs:02d}"
               
            #Timer Text
            cv2.putText(
                frame,
                timer_text,
                (50, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 255),
                2,
                cv2.LINE_AA
            )
            
            
            # =========================
            # SHOW WINDOW
            # =========================
            # ===== Show Frame Inside Tkinter =====
            frame_height, frame_width = frame.shape[:2]
            max_width = 850
            max_height = 500

            scale = min(max_width / frame_width, max_height / frame_height)
            new_width = int(frame_width * scale)
            new_height = int(frame_height * scale)

            frame = cv2.resize(frame, (new_width, new_height))

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(rgb_frame)
            ctk_img = ctk.CTkImage(
                light_image=img,
                dark_image=img,
                size=(img.width, img.height)
            )
            camera_label.after(0, lambda: camera_label.configure(image=ctk_img, text=""))
            camera_label.image = ctk_img  # Keep reference to avoid garbage collection

            # =========================
            # EXIT
            # =========================
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # =========================
        # FINAL ATTENDANCE RESULT
        # =========================
        present_students = []
        absent_students = []

        print("\nFinal Attendance Results:\n")

        for student in set(known_names):

            count = detection_counts.get(student, 0)

            percentage = (
                count / number_of_checks
            ) * 100

            if count >= required_presence:
                present_students.append(student)
                mark_attendance(student)

                print(
                    f"{student}: PRESENT "
                    f"({count}/{number_of_checks} checks "
                    f"- {percentage:.0f}%)"
                )

            else:
                absent_students.append(student)
                print(
                    f"{student}: ABSENT "
                    f"({count}/{number_of_checks} checks "
                    f"- {percentage:.0f}%)"
                )

        show_summary(
            camera_label,
            present_students,
            absent_students,
            len(completed_checks)
        )

    finally:

        cap.release()

        cv2.destroyAllWindows()