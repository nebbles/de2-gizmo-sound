#!/usr/bin/env python

# motor test program

import RPi.GPIO as GPIO # External module imports GPIO
import time # Library to slow or give a rest to the script
import sys # Library to access program arguments
import timeit
#from __future__ import print_function
#print(os.path.getsize(file_name)/1024+'KB / '+size+' KB downloaded!', end='\r')


GPIO.setmode(GPIO.BCM)
msPin = 17
GPIO.setup(msPin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Microswitch pin 16 for feedback

print("Press CTRL+C to exit")
try:
    flag = True # Flag to prevent looping print statement
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
                flag = True

finally:
    GPIO.cleanup()
