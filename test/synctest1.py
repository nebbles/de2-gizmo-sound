#!/usr/bin/env python

import random
import time
import datetime
import collections
import threading
from Queue import Queue

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
