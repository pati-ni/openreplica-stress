execfile('/home/students/cs091747/openreplica/openr-env/bin/activate_this.py',
         dict(__file__='/home/students/cs091747/openreplica/openr-env/bin/activate_this.py'))
import dns
import time
from zookeeper.client import ClientBase
import zookeeper.client as client
from concoord.proxy.multiElection import MultiElection
import sys
import signal



class OrBase(ClientBase):

    def __init__(self, id, proxy_class,  method, win):

        self.obj = proxy_class('')
        self.election_method = method
        self.win_method = win
        self.id = id
        self.int_id = int(id)
        self.z_node = '/leader'+str(self.int_id)
        ClientBase.__init__(self, id)
        self.zk_log.ensure_path(self.z_node)
        self.running = True

    @client.timer
    def benchmark(self):
        self.election_method(self.obj, self.int_id)
        #self.win(id)
        self.win_method(self.obj, self.int_id)

    def run(self):
        while self.running:
            self.benchmark()

    @client.complete_task
    def win(self, id):
        pass


def kill_handler(signal):
    test.running = False
    time.sleep(1)
    sys.exit(0)


if __name__ == '__main__':
    print 'Start'
    signal.signal(signal.SIGINT, kill_handler)
    signal.signal(signal.SIGTERM, kill_handler)
    test = OrBase(sys.argv[1], MultiElection, MultiElection.acquire_lock, MultiElection.release_lock)
    test.run()
