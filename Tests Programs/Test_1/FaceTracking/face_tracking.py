import cv2
import numpy as np
from djitellopy import tello

drone = tello.Tello()
drone.connect()

print("*********************	" + "Battery percentage: " + str(drone.get_battery()) + "%" + "	   *********************")

drone.streamon()
# drone.takeoff()
# drone.send_rc_control(0, 0, -10, 0)

width, height = 360, 240
fbRange = [6200, 6800]
pid = [0.4, 0.4, 0]
pError = 0

def find_face(img):
	face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades +'haarcascade_frontalface_default.xml')


	# face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
	imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(imgGray, 1.2, 8)

	face_centre_list = []
	face_area_list = []

	for (x, y, w, h) in faces:
		cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
		
		centre_x = x + (w // 2)
		centre_y = y + (h // 2)

		area = w * h
		
		cv2.circle(img, (centre_x, centre_y), 5, (0, 255, 0), cv2.FILLED)

		face_centre_list.append([centre_x, centre_y])
		face_area_list.append(area)

	if not face_area_list:
		# print("no faces here!!!")
		return img, [[0, 0], 0]
	else:
		i = face_area_list.index(max(face_area_list))
		return img, [face_centre_list[i], face_area_list[i]]

def track_face(drone, info, width, pid, pError):

	area = info[1]
	x, y = info[0]
	fb = 0

	error = x - width//2
	speed = pid[0] * error + pid[1] * (error - pError)
	speed = int(np.clip(speed, -100, 100))

	if area > fbRange[0] and area < fbRange[1]:
		fbSpeed = 0
		print("DO NOT MOVE!!!")
	elif area > fbRange[1]:
		fbSpeed = -20
	elif area<fbRange[0] and area != 0:
		fbSpeed = 20

	if x == 0:
		speed = 0
		error = 0

	print(speed, fb)

	# drone.send_rc_control(0, fb, 0, speed)
	return error


cap = cv2.VideoCapture(0)
while True:

	# _, camera_feed = cap.read()
	# camera_feed = cv2.resize(camera_feed, (width, height))
	# img, info = find_face(camera_feed)
	
	drone_feed = drone.get_frame_read().frame
	drone_feed = cv2.resize(drone_feed, (width, height))
	img, info = find_face(drone_feed)
	pError = track_face(drone, info, width, pid, pError)
	cv2.imshow("Output", img)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		drone.land()
		break