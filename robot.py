import RPi.GPIO as io
io.setmode(io.BCM)
import sys, os, tty, termios, time
from picamera import PiCamera
from time import sleep

camera = PiCamera()
camera.rotation = 180
camera.start_preview()
camera.annotate_text = "je suis un bg w/s: avancer-reculer +/-: vitesse a/d: visser-devisser  l: lights b: buzzer c: camera 1 or 2 p: photo x: exit "
#camera.brightness = 70
#camera.start_recording('/home/pi/video.h264')

# These two blocks of code configure the PWM settings for
# the two DC motors on the RC car. It defines the two GPIO
# pins used for the input, starts the PWM and sets the
# motors' speed to 0

pin_propulsion_ppm = 22
pin_propulsion_sens = 17
io.setup(pin_propulsion_ppm, io.OUT)
io.setup(pin_propulsion_sens, io.OUT)
propulsion = io.PWM(22,100)#pin, frequence
propulsion.start(0)#start pwm
propulsion.ChangeDutyCycle(0)

pin_drill_ppm = 24
pin_drill_sens = 25
io.setup(pin_drill_ppm, io.OUT)
io.setup(pin_drill_sens, io.OUT)
drill = io.PWM(24,100)
drill.start(0)
drill.ChangeDutyCycle(0)

# Defining the GPIO pins that will be used for the LEDs on
# the RC car and setting the output to false
io.setup(23, io.OUT)
io.output(23, False)

# Defining the GPIO pins that will be used for the Buzzer on
# the RC car and setting the output to false
io.setup(18, io.OUT)
io.output(18, False)

# Setting the PWM pins to false so the motors will not move
# until the user presses the first key
io.output(pin_propulsion_ppm, False)
io.output(pin_propulsion_sens, False)
io.output(pin_drill_ppm, False)
io.output(pin_drill_sens, False)

#global adavanceStatus
#adavanceStatus = False

# The getch method can determine which key has been pressed
# by the user on the keyboard by accessing the system files
# It will then return the pressed key as a variable
def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

# This section of code defines the methods used to determine
# whether a motor needs to spin forward or backwards. The
# different directions are acheived by setting one of the
# GPIO pins to true and the other to false. If the status of
# both pins match, the motor will not turn.

def motor1_forward():

    global advanceStatus
    advanceStatus = True 
    io.output(pin_propulsion_ppm, True)
    io.output(pin_propulsion_sens, False)
      
def motor1_reverse():

    global advanceStatus
    advanceStatus = False
    io.output(pin_propulsion_ppm, True)
    io.output(pin_propulsion_sens, True)
    
def motor2_forward():

    global advanceStatus2
    advanceStatus2 = True
    io.output(pin_drill_ppm, True)
    io.output(pin_drill_sens, True)
def motor2_reverse():
    
    global advanceStatus2
    advanceStatus2 = False
    io.output(pin_drill_ppm, True)
    io.output(pin_drill_sens, False)
    
        

# This method will toggle the lights on/off when the user
# presses a particular key. It will then change the status
# of the lights so it will know whether to turn them on or
# off when it is next called.
def toggleLights():

    global lightStatus

    if(lightStatus == False):
        io.output(23, True)
        lightStatus = True
    else:
        io.output(23, False)
        lightStatus = False

# This method will toggle the buzzer on/off when the user
# presses a particular key. It will then change the status
# of the buzzer so it will know whether to turn them on or
# off when it is next called.
def toggleBuzzer():

    global buzzerStatus

    if(buzzerStatus == False):
        io.output(18, True)
        buzzerStatus = True
    else:
        io.output(18, False)
        buzzerStatus = False

# This method will toggle the buzzer on/off when the user
# presses a particular key. It will then change the status
# of the buzzer so it will know whether to turn them on or
# off when it is next called.
def togglePhoto():

    global photoStatus

   # if(photoStatus == False):
    sleep(5)
    camera ('/home/pi/Desktop/image.jpg')
   # 	photoStatus = True
   # else:
    #    photoStatus = False


# This method allow to incremant the speed variable for the motor
def toggleVitesse(choix):
    global vitesseStatus
    global vitesseStatus2
	
    if(choix == "1"):
	if(vitesseStatus<98):
		vitesseStatus=vitesseStatus+3
	
    else:
	 if(vitesseStatus2<98):
                vitesseStatus2=vitesseStatus2+3


#fonction deceleration permet de realentir le moteur jusqu a  zero 
def toggleDeceleration(choix):

    global vitesseStatus
    global vitesseStatus2

    if(choix == "1"):
    	while (vitesseStatus != 0 ):
         vitesseStatus=vitesseStatus-3
	 propulsion.ChangeDutyCycle(vitesseStatus)
         sleep(0.05)        
    else:
        while (vitesseStatus2 != 0 ):
         vitesseStatus2=vitesseStatus2-3
         drill.ChangeDutyCycle(vitesseStatus2)
         sleep(0.05)
	
# Instructions for when the user has an interface
print("w/s: avancer-reculer")
print("a/d: devisser-visser")
print("+/-: vitesse = ")
print("l: lights")
print("b: buzzer")
print("c: camera 1 or 2")
print("p: prendre photo")
print("x: exit")


# Global variables for the status of the lights and steering
advanceStatus = False
advanceStatus2 = False
lightStatus = True
buzzerStatus = False
photoStatus = False
vitesseStatus =0
vitesseStatus2 =0

# Infinite loop that will not end until the user presses the
# exit key

	
# camera.annotate_text = "vitesse = 'vitesseStatus'"  
print("+/-: vitesse = ",vitesseStatus)
print("+/-: vitesse2 = ",vitesseStatus2)

# Keyboard character retrieval method is called and saved
# into variable
char = getch()

# The car will drive forward when the "w" key is pressed
if(char == "w"):
    toggleVitesse("1")
    if(advanceStatus == False):
	   toggleDeceleration("1")
    motor1_forward()

# The car will reverse when the "s" key is pressed
if(char == "s"):
    toggleVitesse("1")
    if(advanceStatus == True):
        toggleDeceleration("1")
    motor1_reverse()

# The drill will drive turn left  when the "a" key is pressed
if(char == "a"):
    toggleVitesse("2")
    if(advanceStatus2 == False):
            toggleDeceleration("2")
    motor2_forward()

# The drill will turn rigt when the "d" key is pressed
if(char == "d"):
    toggleVitesse("2")
    if(advanceStatus2 == True):
            toggleDeceleration("2")
    motor2_reverse()

# The "l" key will toggle the LEDs on/off
if(char == "l"):
    toggleLights()

# The "b" key will toggle the buzzer on/off
if(char == "b"):
    toggleBuzzer()

# The "b" key will toggle the buzzer on/off
if(char == "p"):
    togglePhoto()

# The "x" key will break the loop and exit the program

# At the end of each loop the acceleration motor will stop
# and wait for its next command
drill.ChangeDutyCycle(vitesseStatus2)
propulsion.ChangeDutyCycle(vitesseStatus)

# The keyboard character variable will be set to blank, ready
# to save the next key that is pressed
char = ""

# Program will cease all GPIO activity before terminating
io.cleanup()
