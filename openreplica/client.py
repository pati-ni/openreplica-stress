import dns
import time
from zookeeper.client import ClientBase
import zookeeper.client as client
from concoord.proxy.lock import Lock
import sys

class OrBase(ClientBase):

    def __init__(self, id, proxy_class,  method, win, replica_addresses, *args):

        self.obj = proxy_class(replica_addresses)
        self.election_method = method
        self.win_method = win
        self.args = args
        ClientBase.__init__(self, id,logger_interval=6)


    @client.timer
    def benchmark(self):
        self.election_method(self.obj)
        self.win_method(self.obj)

    def run(self):
        while True:
            self.benchmark()


if __name__ == '__main__':
    test = OrBase(sys.argv[2], Lock, Lock.acquire, Lock.release, sys.argv[1])
    test.run()
