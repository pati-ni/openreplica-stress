import os
import signal
import signal
import sys
import time
from subprocess import Popen, PIPE


def kill_handler(signal, frame):
    global process
    process.kill()
    sys.exit(0)

def spawn_concoord(args):
    global process
    concoord_cmd = ['/home/students/cs091747/openreplica/openr-env/bin/concoord', 'replica'] + args
    process = Popen(concoord_cmd)



def init():
    #execfile('/home/students/cs091747/openreplica/openr-env/bin/activate_this.py')
    signal.signal(signal.SIGINT, kill_handler)
    signal.signal(signal.SIGTERM, kill_handler)

init()
print sys.argv
spawn_concoord(sys.argv[1:])

while True:
    print 'yo'
    time.sleep(2)
    process.communicate()