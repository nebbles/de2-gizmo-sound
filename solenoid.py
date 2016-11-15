#!/usr/bin/env python


# External module imports GPIO
import RPi.GPIO as GPIO
# Library to slow or give a rest to the script
import time


# Pin definiton using Broadcom scheme
# Led
solenoidpin = 23  # Broadcom pin 23 (P1 pin 16)
# Button
butPin = 17  # Broadcom pin 17 (P1 pin 11)


# Pin Setup:
GPIO.setmode(GPIO.BCM)  # Broadcom pin-numbering scheme
GPIO.setup(solenoidpin, GPIO.OUT)  # LED pin set as output
# Button pin set as input w/ pull-up resistors
GPIO.setup(butPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)


print("Press button to activate solenoid. Press CTRL+C to exit")
try:
    while 1:
        # The input() function will return either a True or False
        # indicating whether the pin is HIGH or LOW.
        if GPIO.input(butPin):  # button is released
            GPIO.output(solenoidpin, GPIO.LOW)
        else:  # button is pressed:
            GPIO.output(solenoidpin, GPIO.HIGH)


except KeyboardInterrupt:  # If CTRL+C is pressed, exit cleanly:
    GPIO.cleanup()  # cleanup all GPIO
