#!/usr/bin/env python

# motor test program

import RPi.GPIO as GPIO # External module imports GPIO
import time # Library to slow or give a rest to the script
import sys # Library to access program arguments
import timeit
#from __future__ import print_function
#print(os.path.getsize(file_name)/1024+'KB / '+size+' KB downloaded!', end='\r')


# startup_message = "motortest.py running..."
# print("motortest.py running...")
# print("This program uses the MotorSystem and ControlSystem circuits.")
# print("Connect GPIO pin 16 to microswitch")
# print("Connect GPIO pin 18 to LED")
# print("Connect GPIO pin 12 to transistor gate")
# answer = input("[Y/N] to confirm / quit")
# if answer == 'n':
#     sys.exit()


GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.OUT) # LED pin 18 for feedback
GPIO.setup(18, GPIO.OUT) # Motor pin 12
msPin = 17
GPIO.setup(msPin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Microswitch pin 16 for feedback
motorpwm = GPIO.PWM(18,100)

print("Press CTRL+C to exit")
try:
    flag = True # Flag to prevent looping print statement
    motorpwm.start(0)
    cycle=input("How fast? (20-100)")
    motorpwm.ChangeDutyCycle(cycle)
    while 1:
        # The input() function will return either a True or False
        # indicating whether the pin is HIGH or LOW.
        if GPIO.input(msPin):  # button is released
            if flag:
                print("Button released")
                flag = False
        else:  # button is pressed:
            if not flag:
                print("Button pressed")
                time.sleep(0.01)
                flag = True

finally:
    motorpwm.stop()
    GPIO.cleanup()
