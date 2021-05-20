# Rohit Goyal
# National Institute of Technology Silchar

import os
from cv2 import cv2
import json
import numpy as np
import face_recognition

# JSON does not support numpy array so we need to convert it into regular list
# A class method that converts numpy array to lists
class NumpyEncode(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, np.ndarray):
			return obj.tolist()
		return super().default(obj)

# Finding the paths of data
path = os.path.dirname(os.path.abspath('__file__'))
image_path = os.path.join(path, 'image')

# Dictonary to store all the known faces and ecnodings
encodings = {}

# Variables show progress
total_size = len(os.listdir(image_path))
cur_pos = 0

for root, dir, files in os.walk(image_path):
	lable = os.path.basename(root)
	print('[{}/{}] "{}"'.format(cur_pos, total_size, lable.replace('-', ' ').title()))			# Printing the progress
	cur_pos += 1
	for file in files:
		img_path = os.path.join(root, file)
		img = face_recognition.load_image_file(img_path)
		# img = cv2.resize(img, (0, 0), None, 0.25, 0.25)		# Compressing the image for faster computation
		img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)			# As face-detector works on RGB images
		faceEncods = face_recognition.face_encodings(img, model="cnn")	# Finding the encodings of all the faces captured in the image
		
		# If we found any face in the image, we save the encoding
		if len(faceEncods) > 0:
			if lable in encodings:
				encodings[lable].append(faceEncods[0])
			else:
				encodings[lable] = [faceEncods[0]]
		else:
			print('Face not detected in : "{}"'.format(img_path))

# Saving out encodigns in a file which we load in main program later
with open('encodings.json', 'w') as f:
	json.dump(encodings, f, cls=NumpyEncode)

# All encodings are complete
print('Encoding Complete')
