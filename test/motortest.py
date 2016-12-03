#!/usr/bin/env python
import RPi.GPIO as GPIO # External module imports GPIO
import time # Library to slow or give a rest to the script
import sys # Library to access program arguments
import timeit
#from __future__ import print_function
#print(os.path.getsize(file_name)/1024+'KB / '+size+' KB downloaded!', end='\r')
print("motortest.py")

class colour:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.OUT) # Motor pin 12
    motorpwm = GPIO.PWM(18,100)
    return motorpwm

def startup():
    print "This program uses the MotorSystem circuit."
    print "Connect "+colour.BOLD+"GPIO pin 12"+colour.END+" to transistor gate for motor."
    while True:
        answer = raw_input("[Y/N] to confirm / quit: ")
        answer = answer.lower()
        if answer == 'n':
            sys.exit()
        elif answer == 'y':
            break

print colour.BOLD + 'Hello world' + colour.END
try:
    motorpwm = setup()
    startup()
    motorpwm.start(0)
    exit_words = ['exit', 'e', 'quit', 'q']
    print("\nYou can type any of the following to exit the program"), exit_words, "\n"

    while(1):
        cycle = raw_input("Set duty cycle (should be 20-100): ")
        if any(cycle in s for s in exit_words):
            sys.exit()
        elif cycle == 'help':
            print colour.BOLD+colour.GREEN"\nHELP: "+colour.END+colour.GREEN+"You can type any of the following to exit the program", exit_words
            print "To set duty cycle, input an integer from 0 to 100 incluseive.\n", colour.END
        else:
            try:
                cycle = int(cycle)
                if not (0 <= cycle <= 100): raise ValueError
                motorpwm.ChangeDutyCycle(cycle)
            except ValueError:
                print("Unable to change duty cycle: Input was not an integer (0 to 100 inclusive) or exit word.\n")

finally:
    motorpwm.stop()
    GPIO.cleanup()
