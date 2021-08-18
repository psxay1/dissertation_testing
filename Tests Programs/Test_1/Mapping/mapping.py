import cv2
import math
import time
import numpy as np
import key_press as kp
from time import sleep
from djitellopy import tello

# ******************** PARAMETERS ********************

fSpeed = 117/10 # Forward speed in cm/sec (~15cm/sec)
aSpeed = 360/10 # Angular speed in degrees/sec (50 d/sec)
interval = 0.25

dInterval = fSpeed*interval
aInterval = aSpeed*interval

# ****************************************************

x, y = 500, 500
a = 0
yaw = 0

kp.init()

drone = tello.Tello()
drone.connect()

points = []

global img
is_camera_on = False


def get_keyboard_input():
	lr, fb, ud, yv = 0, 0, 0, 0
	speed = 15
	aspeed = 50
	d = 0
	global is_camera_on, yaw, x, y, a

	if kp.get_key('LEFT'):
		lr = - speed
		d = dInterval
		# a = - 180
		a = 180
		print("*********************	" + "GO LEFT" + "	*********************")

	elif kp.get_key('RIGHT'):
		lr = speed
		d = - dInterval
		# a = 180
		a = 0
		print("*********************	" + "GO RIGHT" + "	*********************")

	if kp.get_key('UP'):
		fb = speed
		d = dInterval
		# a = 270
		a = 90
		print("*********************	" + "GO FORWARD" + "	*********************")

	elif kp.get_key('DOWN'):
		fb = - speed
		d = - dInterval
		# a = - 90
		a = 270
		print("*********************	" + "GO BACK" + "	*********************")

	if kp.get_key('w'):
		ud = speed
		print("*********************	" + "GO UP" + "	*********************")

	elif kp.get_key('s'):
		ud = - speed
		print("*********************	" + "GO DOWN" + "	*********************")

	if kp.get_key('a'):
		yv = - aspeed
		yaw -= aInterval
		print("*********************	" + "TURN LEFT" + "	*********************")

	elif kp.get_key('d'):
		yv = aspeed
		yaw += aInterval
		print("*********************	" + "TURN RIGHT" + "	*********************")

	if kp.get_key('l'):
		drone.land()
		print("*********************	" + "LAND" + "	  *********************")
	if kp.get_key('t'):
		print("*********************	" + "TAKE OFF" + "	   *********************")
		drone.takeoff()
	if kp.get_key('b'):
		print("*********************	" + "Battery percentage: " + str(drone.get_battery()) + "%" + "	   *********************")
	if kp.get_key('c'):
		print("*********************	" + "SWITCH CAMERA ON/OFF" + "	   *********************")
		is_camera_on = not is_camera_on

	if kp.get_key('p'):
		print("*********************	" + "TAKE PHOTO" + "	   *********************")
		cv2.imwrite(f'../Resources/Images/{time.time()}.jpg', img)

	sleep(interval)
	a += yaw
	x += int(d * math.cos(math.radians(a)))
	y += int(d * math.sin(math.radians(a)))
		
	return [lr, fb, ud, yv, x, y]

def drawPoints(img, points):
	for point in points:
		cv2.circle(img, point, 5, (0, 0, 255), cv2.FILLED)

	cv2.circle(img, points[-1], 8, (0, 255, 0), cv2.FILLED)
	cv2.putText(img, f'({(points[-1][0] - 500)/100}, {(points[-1][1] - 500)/100})m', 
		(points[0][1] + 10, points[-1][1] + 30),
		cv2.FONT_HERSHEY_PLAIN, 1,
		(255,0, 255), 1)


while True:
	vals = get_keyboard_input()
	drone.send_rc_control(vals[0], vals[1], vals[2], vals[3])

	points.append((vals[4], vals[5]))
	img = np.zeros((1000, 1000, 3), np.uint8)
	drawPoints(img, points)
	cv2.imshow("Output", img)
	cv2.waitKey(1)
