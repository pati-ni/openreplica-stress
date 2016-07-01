import zookeeper.client as client
import random
import sys
from subprocess import Popen, PIPE
from openreplica.client import OrBase

from concoord.proxy.multiElection import MultiElection

import time


def spawn_process(nodes, script, index, id):

    node = nodes[index %  len(nodes)]
    cmd = ['ssh', node, '-t', '-t', 'python', script, str(id)]
    process = Popen(cmd, stdin=PIPE)
    # process = Popen(cmd, stderr=PIPE, stdout=PIPE, stdin=PIPE)
    return process

class FeedBackMonitor:
    client_spawned = 0
    processes =[]

    def __init__(self, client_nodes='node_list', replica_nodes='replica_list'):
        self.clients = client.insert_client_nodes(client_nodes)
        self.client_seed = random.choice(range(len(self.clients)))
        print 'Clients instances', self.clients

    def launch_clients(self, clients, id):
        client_script = '/home/students/cs091747/openreplica/openreplica/client.py'
        for c in range(clients):
            self.processes.append(spawn_process(self.clients, client_script, self.client_seed + self.client_spawned, id))
            self.client_spawned += 1
            pass

    def __del__(self):
        for p in self.processes:
            p.terminate()


if __name__ == '__main__':

    total_elections = int(sys.argv[1])
    m = MultiElection('')

    cls = FeedBackMonitor()
    for _ in range(total_elections):
        index = m.create_new_lock()
        cls.launch_clients(1, index)

    while True:
        time.sleep(1)







