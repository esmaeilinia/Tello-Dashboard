import Tkinter
import tellopy
import sys
from time import sleep
import cv2
import time
import traceback
import av
import numpy
import keyboard

root = Tkinter.Tk()
move_by = 20.0

def handler(event, sender, data, **args):
    drone = sender
    if event is drone.EVENT_FLIGHT_DATA:
        print data

drone = tellopy.Tello()
drone.subscribe(drone.EVENT_FLIGHT_DATA, handler)
drone.connect()
drone.wait_for_connection(60.0)

root.title("GUI Example")

# Functions
def increase_movement_speed():
	global move_by
	move_by  += 2.0
	# print "New speed : " + move_by

def decrease_movement_speed():
	global move_by
	if move_by <= 10.0:
		pass
	else:
		move_by -= 2.0
	# print "New speed : " + move_by

def take_off():
	print "Taking off"
	drone.takeoff()
	sleep(3)

def land():
	print "Landing"
	drone.land()
	sleep(3)
	drone.quit()
	sys.exit()

def go_up():
	print "Going Up"
	drone.up(move_by)
	sleep(3)

def go_down():
	print "Going Down"
	drone.down(move_by)
	sleep(3)

def go_left():
	print "Going Left"
	drone.left(move_by)
	sleep(3)
	drone.right(move_by/10)
	sleep(1)

def go_right():
	print "Going Right"
	drone.right(move_by)
	sleep(3)
	drone.left(move_by/10)
	sleep(1)

def go_forward():
	print "Going Forward"
	drone.forward(move_by)
	sleep(3)

def go_backward():
	print "Going Backward"
	drone.backward(move_by)
	sleep(3)

def flip_forward():
	print "Flipping Forward"
	drone.flip_forward()
	sleep(3)

def flip_backward():
	print "Flipping Backward"
	drone.flip_back()
	sleep(3)

def flip_left():
	print "Flipping Left"
	drone.flip_left()
	sleep(3)

def flip_right():
	print "Flipping Right"
	drone.flip_right()
	sleep(3)

def flip_forwardleft():
	print "Flipping Forwards Left"
	drone.flip_forwardleft()
	sleep(3)

def flip_backleft():
	print "Flipping Back Left"
	drone.flip_backleft()
	sleep(3)

def flip_forwardright():
	print "Flipping Forward Right"
	drone.flip_forwardright()
	sleep(3)

def flip_backright():
	print "Flipping Back Right"
	drone.flip_backright()
	sleep(3)

def rotate_clockwise():
	print "Rotating clockwise"
	drone.clockwise(move_by)
	sleep(3)

def rotate_counter_clockwise():
	print "Rotating counter clockwise"
	drone.counter_clockwise(move_by)

def get_video():
	try:
		retry = 3
		container = None
		while container is None and 0 < retry:
			retry -= 1
			try:
				container = av.open(drone.get_video_stream())
			except av.AVError as ave:
				print(ave)
				print('retry...')

		# skip first 300 frames
		frame_skip = 300
		t_end = time.time() + 60
		while time.time() < t_end:
			for frame in container.decode(video=0):
				if 0 < frame_skip:
					frame_skip = frame_skip - 1
					continue
				else:
					t_end = time.time() + 60
				start_time = time.time()
				image = cv2.cvtColor(numpy.array(frame.to_image()), cv2.COLOR_RGB2BGR)
				cv2.imshow('Original', image)
				# cv2.imshow('Canny', cv2.Canny(image, 100, 200))
				cv2.waitKey(1)
				if frame.time_base < 1.0/60:
					time_base = 1.0/60
				else:
					time_base = frame.time_base
				frame_skip = int((time.time() - start_time)/time_base)

				if keyboard.is_pressed('q'):
					print "*******************************"
					break


	except Exception as ex:
		exc_type, exc_value, exc_traceback = sys.exc_info()
		traceback.print_exception(exc_type, exc_value, exc_traceback)
		print(ex)
	finally:
		drone.quit()
		cv2.destroyAllWindows()



# GUI
lbl_op = Tkinter.Label(root, text="Flight Control")
lbl_op.pack()

# Get Video
btn_get_video = Tkinter.Button(root, text="Get Video", command=get_video)
btn_get_video.pack()

# Increase Speed
btn_increase_speed = Tkinter.Button(root, text="Increase", command=increase_movement_speed)
btn_increase_speed.pack()

# Increase Speed
btn_decrease_speed = Tkinter.Button(root, text="Decrease", command=decrease_movement_speed)
btn_decrease_speed.pack()

# Take off
btn_take_off = Tkinter.Button(root, text="TakeOff", command=take_off)
btn_take_off.pack()

# Land
btn_land = Tkinter.Button(root, text="Land", command=land)
btn_land.pack()

# Up
btn_go_up = Tkinter.Button(root, text="Go Up", command=go_up)
btn_go_up.pack()

# Down
btn_go_down = Tkinter.Button(root, text="Go Down", command=go_down)
btn_go_down.pack()

# Left
btn_go_left = Tkinter.Button(root, text="Go Left", command=go_left)
btn_go_left.pack()

# Right
btn_go_right = Tkinter.Button(root, text="Go Right", command=go_right)
btn_go_right.pack()

# Forward
btn_go_left = Tkinter.Button(root, text="Go forward", command=go_forward)
btn_go_left.pack()

# Backward
btn_go_right = Tkinter.Button(root, text="Go backward", command=go_backward)
btn_go_right.pack()

# Flip Forward
btn_flip_forward = Tkinter.Button(root, text="Flip Forward", command=flip_forward)
btn_flip_forward.pack()

# Flip Backward
btn_flip_backward = Tkinter.Button(root, text="Flip Backward", command=flip_backward)
btn_flip_backward.pack()

# Flip Left
btn_flip_left = Tkinter.Button(root, text="Flip Left", command=flip_left)
btn_flip_left.pack()

# Flip Right
btn_flip_right = Tkinter.Button(root, text="Flip Right", command=flip_right)
btn_flip_right.pack()

#Flip Forward Left
btn_flip_forwardleft = Tkinter.Button(root, text = "Flip Forwards Left", command=flip_forwardleft)
btn_flip_forwardleft.pack()

#Flip Back Left
btn_flip_backleft = Tkinter.Button(root, text = "Flip Backwards Left", command=flip_backleft)
btn_flip_backleft.pack()

#Flip Forward Right
btn_flip_forwardright = Tkinter.Button(root, text = "Flip Forwards Right", command=flip_forwardright)
btn_flip_forwardright.pack()

#Flip Back Right
btn_flip_backright = Tkinter.Button(root, text = "Flip Backwards Right", command=flip_backleft)
btn_flip_backright.pack()

root.mainloop()