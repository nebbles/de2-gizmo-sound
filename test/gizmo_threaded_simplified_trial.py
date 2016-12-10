#!/usr/bin/env python

'''
gizmo.py is a release file for controlling the gizmo. Currently built for debigging the hardware, it will be expanded with use of both a 'giz-solenoid.py' and 'giz-motor.py'.

When fully integrated it will use threads to run both components of the Gizmo (motor and solenoid) in unison. Circuit diagram can be found in the documentation. Pin layout and wiring included in documentation.

Program currently supports 2 arguments.
- Pass 'loop' to program if you want to loop the file.
- Pass '<filename>' to program if a file other than 'tune.txt' needs to be used.

'''

## ----- Import libs ----- ##
import RPi.GPIO as GPIO # External module imports GPIO
import time # Library to slow or give a rest to the script
import timeit # Alternative timing library for platform specific timing
import sys # Library to access program arguments and call exits
import os # Library provides functionality to clear screen
import random
import datetime
import collections
import threading
from Queue import Queue

## ----- Pin definiton using Broadcom scheme ----- ##
solenoid1 = 23  # GPIO 16
solenoid2 = 24  # GPIO 18
solenoid3 = 4   # GPIO 07
solenoid4 = 17  # GPIO 11
motor1 = 18     # GPIO 12
led1 = 25       # GPIO 22
switch1 = 6    # GPIO 31
switch2 = 13    # GPIO 33

## ----- Pin setup ----- ##
GPIO.setmode(GPIO.BCM)  # Broadcom pin-numbering scheme
GPIO.setup(solenoid1, GPIO.OUT)  # set as I/O output
GPIO.setup(solenoid2, GPIO.OUT)  # set as I/O output
GPIO.setup(solenoid3, GPIO.OUT)  # set as I/O output
GPIO.setup(solenoid4, GPIO.OUT)  # set as I/O output
GPIO.setup(led1, GPIO.OUT)  # set as I/O output
GPIO.setup(motor1, GPIO.OUT) # set as I/O output
motor1pwm = GPIO.PWM(motor1,100) # set pwm on motor1 pin
GPIO.setup(switch1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(switch2, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.output(solenoid1, GPIO.LOW)
GPIO.output(solenoid2, GPIO.LOW)
GPIO.output(solenoid3, GPIO.LOW)
GPIO.output(solenoid4, GPIO.LOW)
GPIO.output(led1, GPIO.LOW)

## ----- Set initial values ----- ##
shouldLoop = True # loop needs to be iniated at least one time
stopLoop = True # default behaviour is to stop loop after first iteration
args = sys.argv[1:]
inputfile = "tune.txt"
file_is_finished = False
line_number = 0
shouldExitThread = False

previoustime = datetime.datetime.now()
count_trigger = 0
# default_pwm = 55
default_pwm = 24.5
rpm = 0

## ----- Start up parsing ----- ##
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
        stopLoop = False
    else:
        inputfile = arg

## -- IMPORT TUNE FROM FILE -- ##
infile = open(inputfile, "r") # Open data file -- "r" is for read
tune = [line.rstrip('\n') for line in infile]
infile.close() # Close the filehandle

## ----- Classes and functions ----- ##

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

class History:
    def __init__(self, capacity=3):
        self.history = collections.deque([]) # Deque
        self.capacity = capacity

    def add(self, stamp):
        if len(self.history) == self.capacity: # check if list has 3 items
            self.history.popleft() # remove oldest
        self.history.append(stamp) # add stamp to list

    def clear(self):
        self.history.clear() # empty history deque

    def dump(self):
        print "capacity:", self.capacity
        print "number stored:", len(self.history)
        print "history:", list(self.history) # print history

    def average_rpm(self):
        avg_rpm = sum(self.history)/len(self.history)
        return avg_rpm

    def averageTimeDelta(self):
        datetimes = self.history
        if len(self.history) == 1: # if a average cannot be made return 0
            return datetime.timedelta(0)
        else:
            timedeltas = [datetimes[i]-datetimes[i-1] for i in range(1, len(datetimes))] # subtracting datetimes gives timedeltas
            average_timedelta = sum(timedeltas, datetime.timedelta(0)) / len(timedeltas) # giving datetime.timedelta(0) as the start value makes sum work on tds
            # print "avg_td",average_timedelta
            return average_timedelta

    def getprediction(self, fromtime):
        average_timedelta = self.averageTimeDelta() # get average delta
        prediction = fromtime + average_timedelta # add average delta to current time
        return prediction # return prediction as datetime

def calcrpm():
    global previoustime
    currenttime = datetime.datetime.now()
    x = currenttime - previoustime
    x = float(x.total_seconds())
    rpm = 60 / (2*x)
    previoustime = currenttime
    return rpm

def calcpwm(rpm, pwm, target=75):
    delta_rpm = abs(rpm-target) # find difference in rpm
    if rpm > target: # if rpm is greater than target then reduce
        new_pwm = pwm - delta_rpm/2 # change the pwm by the difference over two to tend towards perfect value
        if not 0 < new_pwm < 100:
            return pwm
        return new_pwm # reduce pwm
    elif rpm < target: # elif rpm is less than target then increase
        new_pwm = pwm + delta_rpm/2
        if not 0 < new_pwm < 100:
            return pwm
        return new_pwm # increase pwm
    else:
        return pwm

def solenoid():
    global line_number
    global file_is_finished
    while line_number < 10:
        if shouldExitThread: return

        # choose a delay time (about 0.4)
        delay_time = (60 / (2*average_rpm) ) - 0.1
        if delay_time < 0:
            delay_time = 0
        print delay_time, "delay_time"
        # delay by x
        time.sleep(delay_time)

        # play line
        notes = tune[line_number]
        print datetime.datetime.now(), line_number, notes

        hit1, hit2, hit3, hit4 = False, False, False, False # set hits all to false
        if notes[1] == '1':
            hit1 = True
            print "Hit solenoid1"
        if notes[2] == '1':
            hit2 = True
            print "Hit solenoid2"
        if notes[3] == '1':
            hit3 = True
            print "Hit solenoid3"
        if notes[4] == '1':
            hit4 = True
            print "Hit solenoid4"

        if hit1: GPIO.output(solenoid1, GPIO.HIGH)
        if hit2: GPIO.output(solenoid2, GPIO.HIGH)
        if hit3: GPIO.output(solenoid3, GPIO.HIGH)
        if hit4: GPIO.output(solenoid4, GPIO.HIGH)

        time.sleep(0.1)

        GPIO.output(solenoid1, GPIO.LOW)
        GPIO.output(solenoid2, GPIO.LOW)
        GPIO.output(solenoid3, GPIO.LOW)
        GPIO.output(solenoid4, GPIO.LOW)

        line_number += 1

    file_is_finished = True
    return

## ----- Begin program ----- ##
print "DE2 Gizmo Group Project"
print "Press CTRL+C to exit at any time.\n"
if not stopLoop:
    loopstatement = "Tune loop: enabled"
else:
    loopstatement = "Tune loop: disabled (will prompt on completion)"
print loopstatement
print "Tune being read from: " + inputfile

solenoidQueue = Queue() # create a Queue
solenoidThread = threading.Thread(target=solenoid) # create thread
solenoidThread.setDaemon = True # make thread a daemon thread
# stampHistory = History(capacity=3) # create a History object for tigger events
rpmHistory = History(capacity=4) # create an History object for rpm
rpmHistory.add(75) # add a default starting rpm so average can be calculated
average_rpm = rpmHistory.average_rpm() # get the average rpm
print len(tune),"len of tune"
try:
    while shouldLoop:
        motor1pwm.start(0)
        motor1pwm.ChangeDutyCycle(default_pwm) # set pwm at default_pwm
        current_pwm = default_pwm
        # for i in xrange(0, 4): # for first 10 trigger counts
        #     flag = True
        #     while True:
        #         if GPIO.input(switch1) and not GPIO.input(switch2):  # button is released
        #             if flag:
        #                 print("\nButton released")
        #                 flag = False
        #         elif not GPIO.input(switch1) and GPIO.input(switch2):  # button is pressed:
        #             if not flag:
        #                 flag = True
        #                 print("\nButton pressed")
        #                 print("Iteration: "+colour.yellow+str(i)+colour.end)
        #
        #                 print "tag 4"
        #                 rpm = calcrpm() # get rpm
        #                 if 0<=rpm<=150: rpmHistory.add(rpm)
        #                 average_rpm = rpmHistory.average_rpm()
        #                 print "RPM: "+colour.green+str(rpm)+colour.end
        #
        #                 current_pwm = calcpwm(rpm=average_rpm, pwm=current_pwm, target=75) # get new pwm
        #                 print "PWM DC: "+colour.red+str(current_pwm)+colour.end
        #                 motor1pwm.ChangeDutyCycle(current_pwm) # set pwm
        #
        #                 break
        solenoidThread.start() # start the thread (it will do nothing until item in queue)

        flag = True
        while not file_is_finished:
            if GPIO.input(switch1) and not GPIO.input(switch2):  # button is released
                if flag:
                    # print("\nButton released")
                    flag = False
                    GPIO.output(led1, GPIO.LOW)
            elif not GPIO.input(switch1) and GPIO.input(switch2):  # button is pressed:
                if not flag:
                    flag = True
                    GPIO.output(led1, GPIO.HIGH)

                    rpm = calcrpm() # get rpm
                    if 0<=rpm<=150: rpmHistory.add(rpm) # add rpm to History if it is realistically valid
                    average_rpm = rpmHistory.average_rpm() # get the average (over the last 4) of rpms

                    current_pwm = calcpwm(rpm=average_rpm, pwm=current_pwm, target=75) # get new pwm
                    # motor1pwm.ChangeDutyCycle(current_pwm) # set pwm
                    motor1pwm.ChangeDutyCycle(24.5) # set pwm

        if stopLoop:
            while True:
                prompt_for_loop = raw_input("Would you like to restart the tune [Y/N]? ")
                prompt_for_loop.lower()
                if prompt_for_loop == 'y' or prompt_for_loop == 'yes':
                    shouldLoop == True
                elif prompt_for_loop == 'n' or prompt_for_loop == 'no':
                    shouldLoop = False
                else:
                    print "Invalid answer to quesiton."
        if stopLoop == False:
            print "Looping back and restarting now..."
            file_is_finished = False
        #     line_number = 0


# except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly
#     print "\n"
finally:  # In any other exit circumstance, exit cleanly.
    print colour.yellow+"Waiting for solenoidThread to exit..."+colour.end
    shouldExitThread = True
    solenoidThread.join()
    print colour.green+colour.bold+"solenoidThread has exited safely"+colour.end
    motor1pwm.stop()
    time.sleep(0.2)
    GPIO.cleanup()
