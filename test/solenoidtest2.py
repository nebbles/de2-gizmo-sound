#!/usr/bin/env python

'''
solenoid2.py is a test file for testing the frequency speed possible from the solenoid. Circuit diagram can be found in repository. Pins are set up as follows:

GPIO Pin    Purpose         Connected to
1           3.3v power      Top pin (C) of transistor (see CBE transistor pins - European)
6           GRND            Grnd of breadboard
11          Input port      Button press
16          Output port     Middle pin of transitor (open circuit for LED/Solenoid activation)

'''

import RPi.GPIO as GPIO # External module imports GPIO
import time # Library to slow or give a rest to the script
import timeit
import sys

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

def startup():
    print "This program uses the tests the speed of solenoid activation."
    print colour.darkcyan+colour.bold+"GPIO\tPurpose\t\tConnected to"+colour.end
    print colour.darkcyan+"1\t3.3v power\tTop pin (C) of transistor (see CBE transistor pins - European)\n6\tGRND\t\tGrnd of breadboard\n11\tInput port\tButton press\n16\tOutput port\tMiddle pin of transitor (open circuit for LED/Solenoid activation)"
    while True:
        answer = raw_input(colour.bold+"\n[C/Q] to confirm / quit: "+colour.end)
        answer = answer.lower()
        if answer == 'q':
            sys.exit()
        elif answer == 'c':
            break

# Pin definiton using Broadcom scheme
solenoidpin = 23  # LED/Solenoid -- Broadcom pin 23 (P1 pin 16)
butPin = 17  # BUTTON -- Broadcom pin 17 (P1 pin 11)

# Pin Setup:
GPIO.setmode(GPIO.BCM)  # Broadcom pin-numbering scheme
GPIO.setup(solenoidpin, GPIO.OUT)  # LED pin set as output
GPIO.setup(butPin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Button pin set as input w/ pull-up resistors

flag = True # Flag to prevent looping print statement

try:
    startup()
    print(colour.red+"\nPress button to activate solenoid. Press "+colour.bold+"CTRL+C"+colour.end+colour.red+" to exit."+colour.end)
    while True:
        # The input() function will return either a True or False
        # indicating whether the pin is HIGH or LOW.
        if GPIO.input(butPin):  # button is released
            GPIO.output(solenoidpin, GPIO.LOW)
            if flag:
                print("Button released")
                flag = False
        else:  # button is pressed:
            if not flag:
                print("Button pressed")
                flag = True
            #GPIO.output(solenoidpin, GPIO.HIGH)
            print("Going into rapid mode...")
            interval = input("Please choose an interval time (sec): ")
            print("Starting in 3")
            time.sleep(1)
            print("Starting in 2")
            time.sleep(1)
            print("Starting in 1")
            time.sleep(1)
            start_time = timeit.default_timer()

            for i in range(0,10):
                print i
                GPIO.output(solenoidpin, GPIO.HIGH)
                time.sleep(interval)
                GPIO.output(solenoidpin, GPIO.LOW)
                time.sleep(interval)

            elapsed_time = timeit.default_timer() - start_time
            print "elapsed time", elapsed_time

except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly
    print "\n"
finally:  # In any other exit circumstance, exit cleanly.
    GPIO.cleanup()
