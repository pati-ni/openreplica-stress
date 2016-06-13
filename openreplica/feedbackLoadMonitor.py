import zookeeper.client as client
import random
import subprocess
from openreplica.client import OrBase

def spawn_process(nodes,script,opts,index,name):
    node = nodes[index%len(nodes)]
    cmd = ['screen','-dmS',name,'ssh', node, script]
    if len(opts[0])!=1:
        for opt,val in opts:
            cmd.append(opt)
            cmd.append(str(val))
    else:
        cmd.append(opts)

    print ' '.join(cmd)
    subprocess.call(cmd)
    return node

class FeedBackMonitor:
    replica_spawned = 0
    client_spawned = 0
    ports = {}
    connections={}
    def __init__(self, client_nodes='node_list', replica_nodes='replica_list'):
        self.clients = client.insert_client_nodes(client_nodes)
        self.replicas = client.insert_client_nodes(replica_nodes)

        self.replica_seed = random.choice(range(len(self.replicas)))
        self.client_seed = random.choice(range(len(self.clients)))

        print 'Replicas instances',self.replicas
        print 'Clients instances', self.clients



    def launch_replicas(self,replicas,id='test',nameservers=0,domain_name=None, obj='concoord.object.lock.Lock'):
        print 'Starting group', id
        replica_script = '/home/students/cs091747/openreplica/start.sh'
        self.connections[id]=[]
        port = 14000 + random.choice(range(100))
        self.ports[id] = port
        bootstrap_node = self.replicas[self.replica_seed]
        base_options = [('-o',obj),('-p',port),('-a','0.0.0.0')]

        for r in range(replicas):
            opts = base_options[:]
            if nameservers > 0 and not domain_name is None:
                opts = opts + [('-n',domain_name)]
                nameservers -= 1
            if r != 0:
                opts = opts + [('-b',bootstrap_node + ':' + str(port))]

            selected_node = spawn_process(self.replicas,replica_script,opts,self.replica_seed+self.replica_spawned, 'test')
            self.connections[id].append(selected_node+':'+str(port))
            self.replica_spawned += 1

    def launch_clients(self, clients,id='test'):
        connection_string = ','.join(self.connections[id])
        client_script = '/home/students/cs091747/openreplica/client.sh'
        for c in range(clients):
            spawn_process(self.clients, client_script, connection_string, self.client_seed + self.client_spawned, 'test'+str(c))
            self.client_spawned +=1
            pass



if __name__ == '__main__':
    cls = FeedBackMonitor()
    for i in range(1):
        id = 'test'+str(i)
        cls.launch_replicas(4, id=id)
        cls.launch_clients(1, id=id)










