# Attendance and Face Recognition System

This program uses OpenCV and face_recognition libraries for face detection, recognition, and attendance tracking. The program loads images containing the faces of the people to be tracked. These images are then encoded using the face_recognition library to create an "encoding list". The program then opens the webcam and detects faces in the live video stream using face_recognition. If a face is found that matches one of the faces in the encoding list, the name associated with that face is displayed on the live video stream. A screenshot of the detected face is captured and saved in a folder called "screenshots_attend", and the name, time, and screenshot path are recorded in a CSV file called "attendance.csv". This program can be used to track attendance in schools, companies, and any place that requires keeping a record of attendance and check-ins.

## Requirements

- Python 3.5+
- OpenCV
- face_recognition

## Installation

1. Clone the repository or download the code file.
2. Install the required libraries using pip: `pip install opencv-python face_recognition`

## Usage

1. Add images of the faces you want to track to the `rawdata3` folder.
2. Run the program by executing `attendance.py`.
3. The live video stream from the webcam will be displayed. If a face is detected that matches one of the faces in `rawdata3`, the name associated with that face will be displayed on the video stream. A screenshot of the detected face will be saved in the `screenshots_attend` folder, and the name, time, and screenshot path will be recorded in `attendance.csv`.

Note: The program will create the `screenshots_attend` folder and `attendance.csv` file if they don't exist.
