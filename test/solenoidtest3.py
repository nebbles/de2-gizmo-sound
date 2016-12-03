#!/usr/bin/env python

'''
solenoid3.py is a test file for running multiple solenoids simultaneously.
Circuit diagram can be found in repository. Pins are set up as follows
'''

import RPi.GPIO as GPIO # External module imports GPIO
import time # Library to slow or give a rest to the script
import timeit
import sys

# Pin definiton using Broadcom scheme
solenoid1 = 23  # GPIO 16
solenoid2 = 24  # GPIO 18
solenoid3 = 17  # GPIO 11
solenoid4 = 27  # GPIO 13
motor1 = 18     # GPIO 12
led1 = 4        # GPIO 07
switch1 = 22    # GPIO 15

# Pin setup
GPIO.setmode(GPIO.BCM)  # Broadcom pin-numbering scheme
GPIO.setup(solenoid1, GPIO.OUT)  # setup as I/O output
GPIO.setup(solenoid2, GPIO.OUT)  # setup as I/O output
GPIO.setup(solenoid3, GPIO.OUT)  # setup as I/O output
GPIO.setup(solenoid4, GPIO.OUT)  # setup as I/O output

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
    modes = ['file','debug']
    print colour.darkcyan+"This program uses the tests multiple solenoids."
    print "Modes available are: ", modes
    print modes[0],"- run the standard warmup file solenoidtest3.txt"
    print modes[1],"- run in debug mode where custom combinations can be played"+colour.end
    while True:
        answer = raw_input(colour.bold+"\nType in mode (or quit): "+colour.end)
        answer = answer.lower()
        if answer == 'q' or answer == 'quit':
            sys.exit()
        if answer == 'f' or answer == 'file':
            return 'file'
        elif answer == 'd' or answer == 'debug':
            return 'debug'

def playline(line, uptime=0.1):
    # line is string of 0,1
    if int(line[0]):
        print "play solenoid 1"
        GPIO.output(solenoid1, GPIO.HIGH)
    if int(line[1]):
        print "play solenoid 2"
        GPIO.output(solenoid2, GPIO.HIGH)
    if int(line[2]):
        print "play solenoid 3"
        GPIO.output(solenoid3, GPIO.HIGH)
    if int(line[3]):
        print "play solenoid 4"
        GPIO.output(solenoid4, GPIO.HIGH)
    print ""
    time.sleep(uptime)
    GPIO.output(solenoid1, GPIO.LOW)
    GPIO.output(solenoid2, GPIO.LOW)
    GPIO.output(solenoid3, GPIO.LOW)
    GPIO.output(solenoid4, GPIO.LOW)

def getinterval():
    interval = raw_input(colour.red+"Please input time between line execution: "+colour.end)
    interval = interval.lower()
    if interval == "":
        print colour.red+"Default interval of 0.5 seconds will be used."+colour.end
        interval = 0.5
        return interval
    elif interval == 'q' or interval == 'quit':
        sys.exit()
    else:
        try:
            interval = float(interval)
            if not (interval > 0): raise ValueError
            return interval
        except:
            print "Invalid interval time. Please use a float greater than 0."
            getinterval()

def gettune():
    infile = open("solenoidtest3.txt", "r") # Open data file -- "r" is for read
    tune = [line.rstrip('\n') for line in infile]
    infile.close() # Close the filehandle
    return tune

def filemode(tune):
    interval = getinterval()
    ut = interval/2
    for lineNumber in range(0,len(tune)):
        playline(tune[lineNumber], uptime=ut)
        time.sleep(interval)

    while True:
        decision = raw_input(colour.red+"File execution complete. Run again [Y/N]? "+colour.end)
        decision.lower()
        if decision == 'y' or decision == 'yes':
            filemode(tune)
        elif decision == 'n' or decision == 'no':
            sys.exit()

def stringcheck(string, defaultstring='1111'):
    if string == 'q' or string == 'quit':
        sys.exit()
    elif string == "":
        print colour.red+"Input is empty: using '"+colour.bold+defaultstring+colour.end+colour.red+"' as default"+colour.end
        playstring(defaultstring)
    elif string.strip('01'):
        print colour.yellow+"String must be binary (containing only 1 or 0)"+colour.end
        debugmode()
    elif not len(string) == 4:
        print colour.yellow+"Length of string is invalid: must be 4 binary digits (0/1)"+colour.end
        debugmode()
    else:
        playstring(string)

def playstring(string):
    playline(string)
    string2 = raw_input(colour.red+"\nPress enter to play line again or type new string: "+colour.end)
    stringcheck(string=string2, defaultstring=string)

def debugmode():
    print colour.red+"\nType in a 4 digit binary string correlating to which solenoids play."
    print colour.bold+"Example: "+colour.end+colour.red+"0100 plays solenoid 2"
    print colour.bold+"Example: "+colour.end+colour.red+"1010 plays solenoid 1 and 3"
    print colour.bold+"Default: "+colour.end+colour.red+"1111 all solenoids play"
    print ""
    string = raw_input("String: "+colour.end)
    stringcheck(string)

try:
    mode = startup()
    print(colour.red+"\nMode selected: "+colour.bold+mode+colour.end)

    # file mode
    if mode == 'file':
        tune = gettune()
        filemode(tune)
    # debug mode
    elif mode == 'debug':
        debugmode()

except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly
    print "\n"
finally:  # In any other exit circumstance, exit cleanly.
    GPIO.cleanup()
