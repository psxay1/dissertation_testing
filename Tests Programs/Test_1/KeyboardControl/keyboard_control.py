from djitellopy import tello
import key_press as kp
import time
import cv2

kp.init()

drone = tello.Tello()
drone.connect()

global img
is_camera_on = False
is_camera_on

def get_keyboard_input():
	lr, fb, ud, yv = 0, 0, 0, 0
	speed = 50
	global is_camera_on

	if kp.get_key('LEFT'):
		lr = - speed
		print("*********************	" + "GO LEFT" + "	*********************")
	elif kp.get_key('RIGHT'):
		lr = speed
		print("*********************	" + "GO RIGHT" + "	*********************")

	if kp.get_key('UP'):
		fb = speed
		print("*********************	" + "GO FORWARD" + "	*********************")
	elif kp.get_key('DOWN'):
		fb = - speed
		print("*********************	" + "GO BACK" + "	*********************")

	if kp.get_key('w'):
		ud = speed
		print("*********************	" + "GO UP" + "	*********************")
	elif kp.get_key('s'):
		ud = - speed
		print("*********************	" + "GO DOWN" + "	*********************")

	if kp.get_key('a'):
		yv = speed
		print("*********************	" + "TURN LEFT" + "	*********************")
	elif kp.get_key('d'):
		print("*********************	" + "TURN RIGHT" + "	*********************")
		yv = - speed

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
		
	return [lr, fb, ud, yv]


while True:
	vals = get_keyboard_input()
	drone.send_rc_control(vals[0], vals[1], vals[2], vals[3])
	drone.streamon()
	img = drone.get_frame_read().frame
	cv2.imshow('Image', img)
	cv2.waitKey(1)
