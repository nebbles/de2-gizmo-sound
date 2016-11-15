#!/usr/bin/env python

'''
solenoid.py is a test file for running the solenoid set up. Circuit diagram can be found in the same directory. Pins are set up as follows:

GPIO Pin    Purpose         Connected to
1           3.3v power      Top pin (C) of transistor (see CBE transistor pins - European)
6           GRND            Grnd of breadboard
11          Input port      Button press
16          Output port     Middle pin of transitor (open circuit for LED/Solenoid activation)

'''

import RPi.GPIO as GPIO # External module imports GPIO
import time # Library to slow or give a rest to the script


# Pin definiton using Broadcom scheme
solenoidpin = 23  # LED/Solenoid -- Broadcom pin 23 (P1 pin 16)
butPin = 17  # BUTTON -- Broadcom pin 17 (P1 pin 11)

# Pin Setup:
GPIO.setmode(GPIO.BCM)  # Broadcom pin-numbering scheme
GPIO.setup(solenoidpin, GPIO.OUT)  # LED pin set as output
GPIO.setup(butPin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Button pin set as input w/ pull-up resistors

flag = True # Flag to prevent looping print statement

print("Press button to activate solenoid. Press CTRL+C to exit")
try:
    while 1:
        # The input() function will return either a True or False
        # indicating whether the pin is HIGH or LOW.
        if GPIO.input(butPin):  # button is released
            GPIO.output(solenoidpin, GPIO.LOW)
            if flag:
                print("Button released")
                flag = False
        else:  # button is pressed:
            GPIO.output(solenoidpin, GPIO.HIGH)
            if not flag:
                print("Button pressed")
                flag = True


except KeyboardInterrupt:  # If CTRL+C is pressed, exit cleanly:
    GPIO.cleanup()  # cleanup all GPIO
