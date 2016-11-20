#!/usr/bin/env python

'''
testrig.py is a test file for running the parsing script. It allows for testing and degbugging of the tune that is being passed to the final program by translating its commands into discrete LED blinks or sound snippets. Circuit diagram can be found in the documentation. Pins are set up as follows:

GPIO Pin    Purpose         Connected to
6           GRND            Grnd of breadboard
11          Output          LED 1
13          Output          LED 2
15          Output          LED 3

Program currently supports 2 arguments.
- Pass 'loop' to program if you want to loop the file.
- Pass '<filename>' to program if a file other than 'example.py' needs to be used.

'''

import RPi.GPIO as GPIO # External module imports GPIO
import time # Library to slow or give a rest to the script
import sys # Library to access program arguments
import timeit

start_time = timeit.default_timer()
elapsed = timeit.default_timer() - start_time

shouldLoop = False
args = sys.argv[1:]
timeinterval = 0.5
inputfile = "example.py"

if len(args) > 2:
    print "Program can only accept 2 arguments:"
    print "1: 'loop'"
    print "2: <filename>"
    sys.exit()

for arg in args:
    if arg == 'help':
        print "Program can accept 2 arguments:"
        print "1: 'loop'"
        print "2: <filename>"
        sys.exit()
    elif arg == 'loop':
        shouldLoop = True
    else:
        inputfile = arg

## -- IMPORT TUNE FROM FILE -- ##
infile = open("example.py", "r") # Open data file -- "r" is for read
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

# Start up feedback
print("LED Test Rig. Press CTRL+C to exit")
if shouldLoop:
    loopstatement = "Program will loop."
else:
    loopstatement = "Program will not loop and will exit upon completion."
print(loopstatement)
filestatement = "Tune being read from: " + inputfile


try:
    while shouldLoop:
        for index in range(0,len(tune)):
            start_time = timeit.default_timer()

            hit1, hit2, hit3 = False, False, False
            notes = tune[index]
            print index, " ", notes

            if notes[0] == '1': hit1 = True
            if notes[1] == '1': hit2 = True
            if notes[2] == '1': hit3 = True

            if hit1: GPIO.output(led1, GPIO.HIGH)
            if hit2: GPIO.output(led2, GPIO.HIGH)
            if hit3: GPIO.output(led3, GPIO.HIGH)

            elapsed = timeit.default_timer() - start_time
            print elapsed

            time.sleep(timeinterval)

            GPIO.output(led1, GPIO.LOW)
            GPIO.output(led2, GPIO.LOW)
            GPIO.output(led3, GPIO.LOW)


except KeyboardInterrupt:  # If CTRL+C is pressed, exit cleanly:
    print 'KeyboardInterrupt occured'

finally:
    GPIO.cleanup()  # cleanup all GPIO
