import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime

path = r"C:\devolpment\rawdata3"
images = []
classNames = []
imagePaths = []
myList = os.listdir(path)
print(myList)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
    imagePaths.append(f'{path}/{cl}')  # Adding image paths to list
print(classNames)


def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList


encodeListKnown = findEncodings(images)
print('Encoding Complete')

cap = cv2.VideoCapture(0)

# Create the screenshots folder if it doesn't exist
if not os.path.exists('screenshots_attend'):
    os.makedirs('screenshots_attend')

# Create the attendance CSV file if it doesn't exist
if not os.path.exists('attendenc.csv'):
    with open('attendenc.csv', 'w') as f:
        f.write('Name,Time,Screenshot\n')

def markAttendance(name, screenshot_path):
    with open('attendenc.csv', 'r+') as f:
        lines = f.readlines()
        names = [line.split(',')[0] for line in lines]
        if name not in names:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.write(f'\n{name},{dtString},{screenshot_path}')  # Writing name, datetime, and screenshot path


while True:
    success, img = cap.read()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

            # Capture the frame where the face is detected
            now = datetime.now()
            dtString = now.strftime('%d-%m-%Y-%H-%M-%S')
            screenshot_path = f'screenshots_attend/{name}.png'
            cv2.imwrite(screenshot_path, img[y1:y2,
                                         x1:x2])  # Save the screenshot as a PNG file with the detected name and datetime as the file name

            markAttendance(name, screenshot_path)  # Pass the name and screenshot path as arguments to markAttendance()

    cv2.imshow('Webcam', img)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()