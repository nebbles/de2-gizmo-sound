#!/usr/bin/env python

# Standardised set up
import RPi.GPIO as GPIO # External module imports GPIO
import time # Library to slow or give a rest to the script
import timeit # Alternative timing library for platform specific timing
import sys # Library to access program arguments and call exits
import os # Library provides functionality to clear screen
from datetime import datetime
import random

# Pin definiton using Broadcom scheme
solenoid1 = 23  # GPIO 16
solenoid2 = 24  # GPIO 18
solenoid3 = 4   # GPIO 07
solenoid4 = 17  # GPIO 11
motor1 = 18     # GPIO 12
led1 = 25       # GPIO 22
switch1 = 27    # GPIO 13
switch2 = 22    # GPIO 15

# Pin setup
GPIO.setmode(GPIO.BCM)  # Broadcom pin-numbering scheme
GPIO.setup(solenoid1, GPIO.OUT)  # set as I/O output
GPIO.setup(solenoid2, GPIO.OUT)  # set as I/O output
GPIO.setup(solenoid3, GPIO.OUT)  # set as I/O output
GPIO.setup(solenoid4, GPIO.OUT)  # set as I/O output
GPIO.setup(led1, GPIO.OUT)  # set as I/O output
GPIO.setup(motor1, GPIO.OUT) # set as I/O output
motor1pwm = GPIO.PWM(motor1,100) # set pwm on motor1 pin
GPIO.setup(switch1, GPIO.IN)
GPIO.setup(switch2, GPIO.IN)

class colour:
   purple = '\033[95m'
   cyan = '\033[96m'
   darkcyan = '\033[36m'
   blue = '\033[94m'
   green = '\033[92m'
   yellow = '\033[93m'
   red = '\033[91m'
   bold = '\033[1m'
   underline = '\033[4m'
   end = '\033[0m'

def calcrpm():
    global previoustime
    currenttime = datetime.now()
    x = currenttime - previoustime
    x = float(x.total_seconds())
    rpm = 60 / (4*x)
    previoustime = currenttime
    return rpm

counter = 0
rpm = 0
try:
    print(colour.red+"mstest1")
    print("This program combines the use of the motor and microswitch.")
    print("Use standardised pin layout."+colour.end)
    while True:
        answer = raw_input(colour.red+"\n[C/Q] to confirm / quit: "+colour.end)
        answer.lower()
        if answer == 'q':
            sys.exit()
        elif answer == 'c':
            break

    print(colour.red+"Press "+colour.bold+"CTRL+C"+colour.end+colour.red+" to exit"+colour.end)
    motor1pwm.start(0)
    while True:
        cycle = raw_input(colour.green+"Set duty cycle (should be 20-100): "+colour.end)
        try:
            cycle = int(cycle)
            if 0 <= cycle <= 100: break
        except:
            print(colour.yellow+"Input must be integer 0-100 inclusive.\n"+colour.end)
    motor1pwm.ChangeDutyCycle(cycle)
    while True:
        if not GPIO.input(switch1) and GPIO.input(switch2):  # button is pressed:
                counter += 1
                rpm = calcrpm()
                print("\nCounter: "+colour.yellow+str(counter)+colour.end+" RPM: "+colour.green+str(rpm)+colour.end)

except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly
    motor1pwm.stop()
    print "\n"
finally:  # In any other exit circumstance, exit cleanly.
    GPIO.cleanup()
