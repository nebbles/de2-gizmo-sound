#!/usr/bin/env python

# Standardised set up
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

# Pin definiton using Broadcom scheme
solenoid1 = 23  # GPIO 16
solenoid2 = 24  # GPIO 18
solenoid3 = 4   # GPIO 07
solenoid4 = 17  # GPIO 11
motor1 = 18     # GPIO 12
led1 = 25       # GPIO 22
switch1 = 6    # GPIO 31
switch2 = 13    # GPIO 33

# Pin setup
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

def solenoid(queue):
    while True:
        pass
        while not queue.qsize() == 0: # check if Q has item
            print "got item!"
            timestamp = queue.get() # dequeue item
            timenow = datetime.datetime.now()
            delay_dt = timestamp - timenow # get current time and subtract from prediction
            delay = delay_dt.total_seconds()
            if delay >= 0:
                time.sleep(float(delay)) # wait for delay
                print datetime.datetime.now(), "- Play solenoids!"# print an execution statement with timestamp

solenoidQueue = Queue() # create a Queue
solenoidThread = threading.Thread(target=solenoid,args=[solenoidQueue]) # create thread
solenoidThread.setDaemon = True # make thread a daemon thread
solenoidThread.start()
stampHistory = History()
opts = [1.8,1.9,1.95,2.0,2.05,2.1,2.2]

while True:
    timenow = datetime.datetime.now()
    print timenow, "- Brush!" # print brush stroke with time
    stampHistory.add(stamp=timenow) # add current time to History
    prediction = stampHistory.getprediction(fromtime=timenow) # get prediction for next hit
    # print ""
    print prediction, "- prediction"
    solenoidQueue.put(prediction) # add prediction to queue
    x = random.choice(opts) # get random x
    # print "sleep for", x # sleep for x
    time.sleep(x)
