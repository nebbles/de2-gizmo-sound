#!/usr/bin/env python

# motor test program

import RPi.GPIO as GPIO # External module imports GPIO
import time # Library to slow or give a rest to the script
import sys # Library to access program arguments
import timeit
#from __future__ import print_function
#print(os.path.getsize(file_name)/1024+'KB / '+size+' KB downloaded!', end='\r')

try:
    def startup():
        startup_message = "motortest.py running..."
        print("motortest.py running...")
        print("This program uses the MotorSystem and ControlSystem circuits.")
        print("Connect GPIO pin 16 to microswitch")
        print("Connect GPIO pin 18 to LED")
        print("Connect GPIO pin 12 to transistor gate")
        answer = str(raw_input("[Y/N] to confirm / quit"))
        if answer == 'n':
            sys.exit()

    def setup():
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(23, GPIO.IN) # Microswitch pin 16 for feedback
        GPIO.setup(24, GPIO.OUT) # LED pin 18 for feedback
        GPIO.setup(18, GPIO.OUT) # Motor pin 12
        motorpwm = GPIO.PWM(18,100)
        return motorpwm

    startup()
    motorpwm = setup()
    motorpwm.start(0)
    while(1):
        cycle=input("How fast? (20-100)")
        motorpwm.ChangeDutyCycle(cycle)

except KeyboardInterrupt:
    motorpwm.stop()
    GPIO.cleanup()

finally:
    GPIO.cleanup()
