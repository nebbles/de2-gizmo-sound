#!/usr/bin/env python
import RPi.GPIO as GPIO # External module imports GPIO
import time # Library to slow or give a rest to the script
import sys # Library to access program arguments
import timeit
#from __future__ import print_function
#print(os.path.getsize(file_name)/1024+'KB / '+size+' KB downloaded!', end='\r')

print("motortest.py")

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.OUT) # Motor pin 12
    motorpwm = GPIO.PWM(18,100)
    return motorpwm

def startup():
    print("This program uses the MotorSystem circuit.")
    print("Connect GPIO pin 12 to transistor gate for motor")
    while True:
        answer = str(raw_input("[Y/N] to confirm / quit"))
        if answer == 'n':
            sys.exit()
        elif answer == 'y':
            break

try:
    motorpwm = setup()
    startup()
    motorpwm.start(0)
    while(1):
        cycle=input("Set PWM (should be 20-100): ")
        motorpwm.ChangeDutyCycle(cycle)

finally:
    motorpwm.stop()
    GPIO.cleanup()
