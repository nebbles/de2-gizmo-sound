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

## -- IMPORT TUNE FROM FILE -- ##
infile = open("example.txt", "r") # Open data file -- "r" is for read
tune = [line.rstrip('\n') for line in infile]
infile.close() # Close the filehandle

# Pin definiton using Broadcom scheme
led1 = 17  # Broadcom pin 17 (P1 pin 11)
led2 = 27  # Broadcom pin 27 (P1 pin 13)
led3 = 22  # Broadcom pin 22 (P1 pin 15)

# Pin Setup:
GPIO.setmode(GPIO.BCM)  # Broadcom pin-numbering scheme
GPIO.setup(led1, GPIO.OUT)  # LED pin set as output
GPIO.setup(led2, GPIO.OUT)  # LED pin set as output
GPIO.setup(led3, GPIO.OUT)  # LED pin set as output

# tune = [[1,0,0],\
#         [1,1,0],\
#         [1,0,0],\
#         [1,1,1],\
#         [1,0,0],\
#         [1,1,0],\
#         [1,0,0],\
#         [1,1,1],\
#         [1,0,0],\
#         [1,1,0],\
#         [1,0,0],\
#         [1,1,1],\
#         [1,0,0],\
#         [1,1,0],\
#         [1,0,0],\
#         [1,1,1]]


print("LED Test Rig. Example file will play repetitively until exit. Press CTRL+C to exit")
t = 0.5
index = 0
loop = 1
try:
    while True:

        # if index == len(tune):
        #     index = 0

        print index
        hit1, hit2, hit3 = False, False, False

        notes = tune[index]
        print notes
        if notes[0] == '1':
            print 'hit1 true'
            hit1 = True
        if notes[1] == '1':
            print 'hit2 true'
            hit2 = True
        if notes[2] == '1':
            print 'hit3 true'
            hit3 = True

        if hit1:
            GPIO.output(led1, GPIO.HIGH)
        if hit2:
            GPIO.output(led2, GPIO.HIGH)
        if hit3:
            GPIO.output(led3, GPIO.HIGH)

        time.sleep(t)
        index += 1

        GPIO.output(led1, GPIO.LOW)
        GPIO.output(led2, GPIO.LOW)
        GPIO.output(led3, GPIO.LOW)





except KeyboardInterrupt:  # If CTRL+C is pressed, exit cleanly:
    print 'KeyboardInterrupt occured'

finally:
    GPIO.cleanup()  # cleanup all GPIO
