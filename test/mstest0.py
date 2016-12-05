#!/usr/bin/env python

# motor test program

import RPi.GPIO as GPIO # External module imports GPIO
import time # Library to slow or give a rest to the script
import sys # Library to access program arguments
import timeit
from datetime import datetime

GPIO.setmode(GPIO.BCM)
switch1 = 6    # GPIO 31
switch2 = 13    # GPIO 33
GPIO.setup(switch1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(switch2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
previoustime = datetime.now()

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
    rpm = 60 / (2*x)
    previoustime = currenttime
    return rpm

counter = 0
rpm = 0
print(colour.red+"Press "+colour.bold+"CTRL+C"+colour.end+colour.red+" to exit"+colour.end)
try:
    flag = True # Flag to prevent looping print statement
    while True:
        if GPIO.input(switch1) and not GPIO.input(switch2):  # button is released
            if flag:
                print("\nButton released")
                flag = False
        elif not GPIO.input(switch1) and GPIO.input(switch2):  # button is pressed:
            if not flag:
                counter += 1
                print("\nButton pressed")
                print("Counter: "+colour.yellow+str(counter)+colour.end)
                rpm = calcrpm()
                print "RPM: "+colour.green+str(rpm)+colour.end
                flag = True

except KeyboardInterrupt:
    print "\n"
finally:
    GPIO.cleanup()
