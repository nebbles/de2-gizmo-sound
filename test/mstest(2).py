#!/usr/bin/env python

# motor test program

import RPi.GPIO as GPIO # External module imports GPIO
import time # Library to slow or give a rest to the script
import sys # Library to access program arguments
import timeit
from datetime import datetime

#from __future__ import print_function
#print(os.path.getsize(file_name)/1024+'KB / '+size+' KB downloaded!', end='\r')

def startup():
    startup_message = "motortest.py running..."
    print("motortest.py running...")
    print("This program uses the MotorSystem and ControlSystem circuits.")
    print("Connect GPIO pin 16 to microswitch")
    print("Connect GPIO pin 18 to LED")
    print("Connect GPIO pin 12 to transistor gate")
    answer = input("[Y/N] to confirm / quit")
    if answer == 'n':
        sys.exit()


GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.OUT) # LED pin 18 for feedback
GPIO.setup(18, GPIO.OUT) # Motor pin 12
msPin = GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Microswitch pin 16 for feedback
motorpwm = GPIO.PWM(18,100)
return motorpwm

previoustime = datetime.now()

def calcrpm():
    global previoustime
    currenttime = datetime.now()
    x = currenttime - previoustime
    rpm = 60 / (4*x)
    previoustime = currenttime
    return rpm

try:
    #startup()
    motorpwm = setup()
    motorpwm.start(0)
    cycle=input("How fast? (20-100)")
    motorpwm.ChangeDutyCycle(cycle)

    while True:
        if not GPIO.input(msPin): # if ms pressed down
            print "triggered"
            rpm = calcrpm()
            print "RPM: ",rpm
            while True:
                if GPIO.input(msPin): # if ms is released
                    break

finally:
    motorpwm.stop()
    GPIO.cleanup()
