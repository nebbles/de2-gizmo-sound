#!/usr/bin/env python
import RPi.GPIO as GPIO # External module imports GPIO
import time # Library to slow or give a rest to the script
import sys # Library to access program arguments
import timeit
#from __future__ import print_function
#print(os.path.getsize(file_name)/1024+'KB / '+size+' KB downloaded!', end='\r')

print("motortest.py")

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.OUT) # Motor pin 12
    motorpwm = GPIO.PWM(18,100)
    return motorpwm

def startup():
    print("This program uses the MotorSystem circuit.")
    print("Connect GPIO pin 12 to transistor gate for motor")
    while True:
        answer = raw_input("[Y/N] to confirm / quit: ")
        answer = answer.lower()
        if answer == 'n':
            sys.exit()
        elif answer == 'y':
            break

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
        else:
            try:
                cycle = int(cycle)
                motorpwm.ChangeDutyCycle(cycle)
            except:
                print("Unable to change duty cycle: Input was not an integer or exit word.")

finally:
    motorpwm.stop()
    GPIO.cleanup()
