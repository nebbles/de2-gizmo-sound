#!/usr/bin/env python

'''
This is a threadless release file for controlling the gizmo. It constitutes the simplified form of running the gizmo.

It can run both components of the Gizmo (motor and solenoid) in unison. Circuit diagram can be found in the documentation. Pin layout and wiring included in documentation.

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

def set_all_to_low():
    GPIO.output(solenoid1, GPIO.LOW)
    GPIO.output(solenoid2, GPIO.LOW)
    GPIO.output(solenoid3, GPIO.LOW)
    GPIO.output(solenoid4, GPIO.LOW)
    GPIO.output(led1, GPIO.LOW)
set_all_to_low()

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
default_pwm = 50
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

def activate_solenoids(notes):
    global line_number
    hit1, hit2, hit3, hit4 = False, False, False, False # set hits all to false
    if notes[1] == '1': hit1 = True
    if notes[2] == '1': hit2 = True
    if notes[3] == '1': hit3 = True
    if notes[4] == '1': hit4 = True

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

## ----- Begin program ----- ##
print "DE2 Gizmo Group Project"
print "Press CTRL+C to exit at any time.\n"
if not stopLoop:
    loopstatement = "Tune loop: enabled"
else:
    loopstatement = "Tune loop: disabled (will prompt on completion)"
print loopstatement
print "Tune being read from: " + inputfile

rpmHistory = History(capacity=4) # create an History object for rpm
rpmHistory.add(75) # add a default starting rpm so average can be calculated
average_rpm = rpmHistory.average_rpm() # get the average rpm
print len(tune),"len of tune"
try:
    while shouldLoop:
        motor1pwm.start(0)
        motor1pwm.ChangeDutyCycle(default_pwm) # set pwm at default_pwm

        counter = 0
        flag = True
        while line_number < len(tune):
            if GPIO.input(switch1) and not GPIO.input(switch2):  # button is released
                if flag:
                    flag = False
                    GPIO.output(led1, GPIO.LOW)

            elif not GPIO.input(switch1) and GPIO.input(switch2):  # button is pressed:
                if not flag:
                    flag = True
                    GPIO.output(led1, GPIO.HIGH)

                    # GET RPM, SAVE, CALCULATE AVERAGE

                    rpm = calcrpm() # get rpm
                    if 0<=rpm<=150: rpmHistory.add(rpm) # add rpm to History if it is realistically valid
                    average_rpm = rpmHistory.average_rpm() # get the average (over the last 4) of rpms

                    # PLAYS THE SOLENOIDS

                    if counter > 10: # wait for 10 brush strokes before starting
                        if tune[line_number][0] == '1': # current line should begin '1'

                            notes = tune[line_number]
                            print datetime.datetime.now(), line_number, notes
                            activate_solenoids(notes)

                            i = line_number + 1 # check ahead for other lines
                            try:
                                while tune[i][0] != '1': i += 1
                            except:
                                pass
                            number_of_lines_to_execute = i - line_number

                            if number_of_lines_to_execute > 1:
                                expected_time = ( 60 / (2*average_rpm) ) # calculate delay time to next trigger
                                sleep_time = (expected_time / number_of_lines_to_execute) * 0.5 # x = (delay_time / number_of_lines) * 0.9

                            for eachLine in range(0,number_of_lines_to_execute):
                                activate_solenoids(notes) # play first line
                                if number_of_lines_to_execute > 1:
                                    if eachLine > 0:
                                        new_sleep_time = sleep_time-0.1
                                        if new_sleep_time < 0: new_sleep_time = 0
                                        time.sleep(new_sleep_time) # delay by sleep_time
                                    else:
                                        time.sleep(sleep_time) # delay by sleep_time

                        else:
                            print "Sync error!"
                            raise KeyboardInterrupt

                    counter += 1
        motor1pwm.ChangeDutyCycle(0)
        motor1pwm.stop()
        raise KeyboardInterrupt


except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly
    print "\n"
finally:  # In any other exit circumstance, exit cleanly.
    set_all_to_low()
    motor1pwm.stop()
    time.sleep(0.2)
    GPIO.cleanup()
