#!/usr/bin/env python

'''
testrig.py is a test file for running the parsing script. It allows for testing and degbugging of the tune that is being passed to the final program by translating its commands into discrete LED blinks or sound snippets. Circuit diagram can be found in the documentation. Pins are set up as follows:

GPIO Pin    Purpose         Connected to
6           GRND            Grnd of breadboard
11          Output          LED 1
13          Output          LED 2
15          Output          LED 3

'''

import RPi.GPIO as GPIO # External module imports GPIO
import time # Library to slow or give a rest to the script


# Pin definiton using Broadcom scheme
led1 = 17  # Broadcom pin 17 (P1 pin 11)
led2 = 27  # Broadcom pin 27 (P1 pin 13)
led3 = 22  # Broadcom pin 22 (P1 pin 15)

# Pin Setup:
GPIO.setmode(GPIO.BCM)  # Broadcom pin-numbering scheme
GPIO.setup(led1, GPIO.OUT)  # LED pin set as output
GPIO.setup(led2, GPIO.OUT)  # LED pin set as output
GPIO.setup(led3, GPIO.OUT)  # LED pin set as output

flag = True # Flag to prevent looping print statement

tune = [[1,0,0],\
        [1,1,0],\
        [1,0,0],\
        [1,1,1],\
        [1,0,0],\
        [1,1,0],\
        [1,0,0],\
        [1,1,1],\
        [1,0,0],\
        [1,1,0],\
        [1,0,0],\
        [1,1,1],\
        [1,0,0],\
        [1,1,0],\
        [1,0,0],\
        [1,1,1]]


print("Test LEDs one by one. Press CTRL+C to exit")
t = 0.5
index = 0
try:
    while 1:

        if index == 16:
            index = 0

        hit1, hit2, hit3 = False, False, False

        notes = tune[index]
        print notes
        if notes[0] == 1:
            hit1 = True
        if notes[1] == 1:
            hit2 = True
        if notes[2] == 1:
            hit3 = True

        if hit1:
            GPIO.output(led1, GPIO.HIGH)
        if hit2:
            GPIO.output(led2, GPIO.HIGH)
        if hit3:
            GPIO.output(led3, GPIO.HIGH)

        time.sleep(t)
        GPIO.output(led1, GPIO.LOW)
        GPIO.output(led2, GPIO.LOW)
        GPIO.output(led3, GPIO.LOW)





except KeyboardInterrupt:  # If CTRL+C is pressed, exit cleanly:
    print 'KeyboardInterrupt occured'

finally:
    GPIO.cleanup()  # cleanup all GPIO
