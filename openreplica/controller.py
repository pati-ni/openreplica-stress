from kazoo.client import KazooClient
from kazoo.retry import KazooRetry

from zookeeper.client import *
from monitor.controller import Service

from subprocess import Popen, PIPE

import logging
import os

openreplica_object ='concoord.object.multiElection.MultiElection'
#ssh node01 -t -t python /home/students/cs091747/openreplica/replicamanage.py -o concoord.object.lock.Lock -p 12000



class Controller(Service):
    connect_to_leader = True
    processes = {}
    alive = set()
    orQuorum = read_nodes(port=12000)
    leader = ''
    nameserver = set()

    def __init__(self):

        Service.__init__(self)
        self.zk.set('/leader', '')
        self.prepare()
        print self.orQuorum
        message = []
        print sorted(self.orQuorum.split(','))
        for node in sorted(self.orQuorum.split(',')):
            self.add_replica(node)
            self.alive.add(node)
            #message.append((time.time(), 0, node))


        # log_packet = {'hostname': self.hostname, 'node': 'add_replica', 'type': 'replica_management',
        #               'request_data': message}
        # self.queue.put(str(log_packet))

        print self.alive

        @self.zk.DataWatch('/leader')
        def quorum_change(data, stat):
            if data == '':
                print 'Leader data uninitialized'
                return True
            self.alive.add(data)
            self.leader = data
            print 'Updated Quorum', self.alive
            print 'Leader', self.leader
            return True

    def _find_leader(self):
        if self.leader == '':
            time.sleep(1)
            self._find_leader()


    def prepare(self):
        #cmd = ['~/openreplica/experiment-control.sh stop']
        #cmd = ['~/openreplica/experiment-control.sh start']

        for serverstring in self.orQuorum.split(','):
            node, port = serverstring.split(':')
            # print ' '.join(['ssh', node, 'killall -9 concoord'])
            p = Popen(['ssh', node, 'killall -9 concoord'])
            p.wait()

    def add_replica(self, nodestring):
        node,port = nodestring.split(':')
        devnull = open(os.devnull, 'wb')
        base_cmd = ['ssh', node, '-t','-t', '/home/students/cs091747/openreplica/openr-env/bin/concoord','replica']
        options = ['-o', openreplica_object, '-p',str(port)]
        if not node in self.nameserver:
            self.nameserver.add(node)
            options.append('-n')
            options.append('election.or')
        if self.alive:
            options.append('-b')
            alive = sorted(list(set(self.alive)))
            options.append(alive[0])


        cmd = base_cmd + options
        print ' '.join(cmd)
        # if nodestring in self.processes:
        #    self.processes[nodestring].terminate()
        # self.processes[nodestring] = Popen(cmd, stdin=devnull, stderr=devnull, stdout=devnull)
        self.processes[nodestring] = Popen(cmd, stdin=devnull)

    def kill_leader(self):
        if self.leader in self.processes:
            self.alive.remove(self.leader)
            node,port = self.leader.split(":")
            if node in self.nameserver:
                self.nameserver.remove(node)
            self.processes[self.leader].terminate()
            del self.processes[self.leader]
            print 'Alive', self.alive
            print 'Keys', self.processes.keys()
            self.leader = ''
            self._find_leader()
            #self.processes[self.leader].terminate()
        else:
            raise('Fatal: Can not find leader!!')



    def spawn_replica(self):
        if not self.alive:
            print 'no replicas to add'
            return "NULL"

        print 'Alive',self.alive
        print 'Keys', self.processes.keys()

        node,port = sorted(list(self.alive))[-1].split(':')
        for i in range(1,10):
            new_node = str(node+':'+str(int(port)+i))
            if new_node not in self.alive:
                break
        self.add_replica(new_node)
        self.alive.add(new_node)

        return node

    def quorum(self, show_leader):
        nodes = []
        for replica in self.alive:
            if replica == self.leader and show_leader:
                nodes.append(replica+' (leader)')
            else:
                nodes.append(replica)
        return nodes

    def __del__(self):
        for p in self.processes:
            p.terminate()


if __name__ == '__main__':
    # logging.basicConfig(level=logging.DEBUG)
    logging.basicConfig()
    c = Controller()
    c.run(host="0.0.0.0", port=19080)
