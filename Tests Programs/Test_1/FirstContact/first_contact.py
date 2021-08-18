from djitellopy import tello
from time import sleep

drone = tello.Tello()
drone.connect()
# temp = "This is the battery percentage: "
# battery_percentage = drone.get_battery()
# print(temp + str(battery_percentage))


drone.takeoff()

# drone.send_rc_control(30, 0, 0, 0)
sleep(2)
# drone.send_rc_control(0, -50, 0, 0)
# sleep(4)
drone.land()