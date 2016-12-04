import time
import random
import sys
import os

print("show this for 3 seconds then clear screen")
os.system('clear')

offset = random.randint(0,1)

for i in xrange(0, 20+offset):
    if i % 2 == 0:
        sys.stdout.write("Heads")
    else:
        sys.stdout.write("Tails")
    time.sleep(0.1)
    sys.stdout.flush()
    sys.stdout.write("\r")
