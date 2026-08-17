# 🎓 Smart Attendance System

A Python-based smart attendance management system that uses **facial recognition** and **computer vision** to automate student attendance.

The system captures student face data during registration, generates facial encodings, recognizes registered students through a webcam, performs multiple attendance checks during a lecture, and records the final attendance in a CSV file.

---

## ✨ Features

- 👤 **Student Registration**
  - Register students using webcam-based face capture.
  - Captures multiple face images for each student.

- 🧠 **Face Recognition**
  - Uses the `face-recognition` library for facial encoding and matching.
  - Uses OpenCV for real-time camera processing.

- 📷 **Real-Time Camera Recognition**
  - Displays the live camera feed directly inside the application dashboard.
  - Identifies recognized and unknown faces.

- 🎲 **Random Attendance Checks**
  - Performs multiple attendance checks at randomized points during a lecture.
  - Helps reduce the possibility of marking attendance based on a single camera check.

- 📊 **Attendance Threshold**
  - A student must be detected consistently across the configured checks to be marked present.

- 📝 **CSV Attendance Records**
  - Attendance is stored with the student's name and timestamp.
  - Duplicate attendance entries for the same day are prevented.

- 📈 **Dashboard Statistics**
  - Displays the number of registered students.
  - Displays the number of students marked present today.
  - Shows the current date and time.

- 📋 **Attendance Summary**
  - Displays present students, absent students, and completed attendance checks after a session.

- 🌙 **Modern Desktop Interface**
  - Built using CustomTkinter.
  - Dark-themed dashboard with dedicated controls and live camera preview.

---

## 🛠️ Technologies Used

| Technology       | Purpose                                   |
| ---------------- | ----------------------------------------- |
| Python           | Core programming language                 |
| OpenCV           | Camera access and image processing        |
| Face Recognition | Face encoding and recognition             |
| NumPy            | Numerical and image-processing operations |
| CustomTkinter    | Graphical user interface                  |
| Pillow           | Image handling                            |
| Pickle           | Storing facial encodings                  |
| CSV              | Attendance data storage                   |

---

## 🏗️ System Architecture

````text
                    ┌─────────────────────┐
                    │   Smart Attendance  │
                    │       System        │
                    └──────────┬──────────┘
                               │
              ┌────────────────┴────────────────┐
              │                                 │
       Student Registration              Attendance Session
              │                                 │
              ▼                                 ▼
       Capture Face Data                  Open Webcam
              │                                 │
              ▼                                 ▼
       Generate Encodings                Detect Faces
              │                                 │
              ▼                                 ▼
       Store Face Encodings              Compare Faces
                                                │
                                                ▼
                                      Random Attendance Checks
                                                │
                                                ▼
                                      Apply Presence Threshold
                                                │
                                                ▼
                                      Attendance Confirmation
                                                │
                                                ▼
                                      Save to attendance.csv

## 🔄 System Workflow

### 1. Student Registration

The user enters a student's name through the application.

The system then:

1. Opens the webcam.
2. Detects the student's face.
3. Captures multiple face images.
4. Stores the images inside the student's dataset folder.
5. Generates facial encodings.

---

### 2. Encoding Generation

The system processes the registered face images and generates numerical facial representations called **face encodings**.

These encodings are stored locally in:

```text
encodings.pkl
The recognition system uses these encodings for future face comparisons.

### 3. Attendance Session

When attendance starts:

Saved face encodings are loaded.
The webcam is initialized.
The lecture timer starts.
Multiple attendance checks are scheduled at randomized times.
Faces are detected from the camera feed.
Detected faces are compared with registered face encodings.
Stable detections are counted during attendance checks.
Students meeting the required presence threshold are marked present.


### 4. Attendance Storage

Confirmed attendance is stored in:

attendance.csv

Each record contains:

Name,Timestamp

The system prevents the same student from receiving multiple attendance entries on the same day.

## 📁 Project Structure
Smart-Attendance-System/
│
├── dataset/                # Local face dataset (not uploaded)
│
├── attendance.py           # Attendance and recognition logic
├── generate_encodings.py   # Generates facial encodings
├── main.py                 # Main GUI application
├── register.py             # Student registration
├── shared_state.py         # Shared application state
│
├── logo.png                # Application logo
├── requirements.txt        # Python dependencies
├── .gitignore              # Files excluded from Git
└── README.md               # Project documentation

## ⚙️ Installation
Prerequisites
Python 3.x
Webcam
Git
1. Clone the repository
git clone https://github.com/devrajbuilds/smart-attendance-system.git
cd smart-attendance-system
2. Create a virtual environment
python -m venv venv
3. Activate the virtual environment
Windows
venv\Scripts\activate
macOS / Linux
source venv/bin/activate
4. Install dependencies
pip install -r requirements.txt

## ▶️ Running the Application

Start the application using:

python main.py

The Smart Attendance System dashboard will open.

## 👤 Registering a Student
Click Register Student.
Enter the student's name.
Allow camera access.
Follow the capture instructions.
Capture the required face images.
The system processes the captured data for recognition.

## 📷 Starting Attendance
Ensure students have been registered.
Start the attendance session.
The system loads the saved face encodings.
The webcam begins monitoring the classroom.
Random attendance checks are performed.
Recognized students are counted across the checks.
Students satisfying the configured presence requirement are marked present.
🔐 Privacy & Data Handling

This repository does not contain real student face datasets, attendance records, or generated facial encoding data.

The following files/data are intentionally excluded from version control:

dataset/
attendance.csv
encodings.pkl
venv/

Real biometric data should be handled responsibly and only with appropriate consent and authorization.

## ⚠️ Current Limitations
The system currently uses a local webcam.
Face recognition performance can vary depending on lighting, camera quality, and face positioning.
The current implementation is designed primarily for local desktop use.
Attendance data is stored locally in CSV format.
Camera index may need to be changed depending on the connected webcam.

## 🚀 Future Enhancements

Potential improvements include:

🌐 Web-based administration dashboard
🗄️ Database integration using SQLite/MySQL
📱 Mobile or web access for attendance reports
📊 Advanced attendance analytics
📧 Automated attendance notifications
🔐 Role-based authentication
☁️ Secure cloud-based data storage
🎯 Improved recognition under different lighting conditions
🏫 Multi-class and multi-lecture support
📅 Automated daily/monthly attendance reports
🎯 Project Objective

The objective of this project is to develop a practical and automated attendance system that reduces manual attendance effort while using facial recognition and multiple verification checks to improve attendance reliability.

👨‍💻 Author

Devraj Builds

GitHub: @devrajbuilds

📜 License

This project is developed for educational and academic purposes.
````