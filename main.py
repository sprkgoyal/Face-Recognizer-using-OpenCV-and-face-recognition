# Rohit Goyal
# National Institute of Technology Silchar

import json
import requests
import numpy as np
from cv2 import cv2
import face_recognition
from datetime import datetime
from database import Database

# Create Lists of Known Encodings with respective names
encodings = []
scholars = []
student_database = Database()

all_students = student_database.get_returnable_data()
stay_timer = [0] * len(all_students)

# Load the Lists with respactive data
try:
	with open('encodings.json', 'r') as f:
		readfile = json.load(f)
		for k, v in readfile.items():
			for en in v:
				scholars.append(int(k))
				encodings.append(en)
except FileNotFoundError as err:
	print("Model is not trained! Train using 'create_encodings.py'")
	exit()

# Function to insert name, date and time when a new student apperas on Camera
def MarkAttendance(scholar = 0):
	global all_students
	if all_students[scholar-1][4] != 'P':
		stay_timer[scholar-1] += 1
		if stay_timer[scholar-1] >= 10:
			all_students[scholar-1][4] = 'P'
			all_students[scholar-1][3] = datetime.now().strftime("%H:%M:%S")

# Create a camera 
cam = cv2.VideoCapture(0)

faces = []
faceEncods = []
thisFrame = True

# either use default webcam OR
# I have used IP Webcam, you can search more about this on Google
# If you are using IP Webcam then uncomment below url and paste the same as on app
# use the same link of IPv4 appended with shot.jpg
# url = 'http://192.168.43.1:8080/shot.jpg'

# An Inifinite Loop where our camera works
while True:

	# Also uncomment below 3 lines to get frames from IP WebCam
	# frame_resp = requests.get(url)
	# frame_arr = np.array(bytearray(frame_resp.content), dtype=np.uint8)
	# frame = cv2.imdecode(frame_arr, -1)

	# If you are using IP Webcam then comment below
	ret, frame = cam.read()
	
	frame = cv2.flip(frame, 1)								# Fliping the frame sideways to nullify mirror mode
	
	if thisFrame:
		img = cv2.resize(frame, (0, 0), None, 0.25, 0.25)		# Decreaasing the size of image to decrease computation time
		img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)				# As face-detector works on RGB images
		faces = face_recognition.face_locations(img)				# Finding location of all faces in the frame
		faceEncods = face_recognition.face_encodings(img, faces)	# Finding the encoding of all the faces captured

	thisFrame = not thisFrame

	for faceEncod, face in zip(faceEncods, faces):
		y1, x2, y2, x1 = face									# Coordinates of face found
		y1 = 4*y1; y2 = 4*y2; x1 = 4*x1; x2 = 4*x2				# Scaling coordinates back to original as we compressed the image
		green_color = (50, 255, 10)
		cv2.rectangle(frame, (x1, y1), (x2, y2), green_color, 2)
		matches = face_recognition.compare_faces(encodings, faceEncod)		# Return a list of True/False where face-recognition predicts if face matches with known
		dists = face_recognition.face_distance(encodings, faceEncod)		# Return a list of distance where less the distance implies closer the face
		ind = np.argmin(dists)

		# if we found a face then we mark the attendance and put his/her name in the frame
		if matches[ind]:
			cv2.rectangle(frame, (x1-1, y2+25), (x2+1, y2), green_color, cv2.FILLED)
			scholar = scholars[ind]
			name = all_students[scholar-1][1]
			cv2.putText(frame, name, (x1, y2+18), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.1, (255, 255, 255), 2)
			MarkAttendance(scholar)

	# Showing the output in Camera Window
	cv2.imshow('Camera', frame)

	# Condition to stop Camera
	if cv2.waitKey(25) & 0xFF == ord('q') or cv2.getWindowProperty('Camera', cv2.WND_PROP_VISIBLE) < 1:
		break

# Release the camera and destroy all the windows after every thing is done
cam.release()
cv2.destroyAllWindows()

student_database.upload(all_students)
