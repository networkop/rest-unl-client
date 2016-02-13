from restunl.unetlab import UnlServer
from restunl.device import Router
from restunl.helper import *
import time

LAB_NAME = 'test_1'
CONF_PATH = '..\\config\\'
IMAGE = 'L3-ADVENTERPRISEK9-LATEST.bin'
EXT_NET = {('R1', 'Ethernet0/3'): 'pnet1'}
TOPOLOGY = {('R1', 'Ethernet0/0'): ('R2', 'Ethernet0/0'),
            ('R2', 'Ethernet0/1'): ('R3', 'Ethernet0/0'),
            ('R1', 'Ethernet0/1'): ('R3', 'Ethernet0/1')}


def built_topo(lab, nodes, topo):
    for (a_name, a_intf), (b_name, b_intf) in topo.iteritems():
       if not a_name in nodes:
           nodes[a_name] = lab.create_node(Router(a_name, IMAGE))
           print("*** NODE {} CREATED".format(a_name))
       if not b_name in nodes:
           nodes[b_name] = lab.create_node(Router(b_name, IMAGE))
           print("*** NODE {} CREATED".format(b_name))
       node_a = nodes[a_name]
       node_b = nodes[b_name]
       node_a.connect_node(a_intf, node_b, b_intf)
       print("*** NODES {0} and {1} ARE CONNECTED".format(a_name, b_name))
    return None


def configure_nodes(nodes, path):
    import threading
    processes = []
    for node_name in nodes:
        conf = 'enable\r'
        conf += read_file('{0}{1}.txt'.format(path, node_name))
        conf += 'end\r write\r'
        process = threading.Thread(target=nodes[node_name].configure, args=(conf,))
        process.start()
        processes.append(process)
    [p.join() for p in processes]
    print("*** ALL NODES CONFIGURED")
    return None


def ext_connect(lab, nodes, rule):
    for (node_name, node_intf), pnet in rule.iteritems():
        ext_net = lab.create_net('cloud', net_type=pnet)
        nodes[node_name].connect_interface(node_intf, ext_net)
    return None


def app():
    unl = UnlServer('192.168.247.20')
    unl.login('admin', 'unl')
    print("*** CONNECTED TO UNL")
    lab = unl.create_lab(LAB_NAME)
    try:
        lab.cleanup()
        print("*** CREATED LAB")
        nodes = dict()
        built_topo(lab, nodes, TOPOLOGY)
        print("*** TOPOLOGY IS BUILT")
        ext_connect(lab, nodes, EXT_NET)
        print("*** CONNECTED TO HOST NETWORK")
        lab.start_all_nodes()
        print("*** NODES STARTED")
        configure_nodes(nodes, CONF_PATH)
        print("*** NODES CONFIGURED")
        raw_input('PRESS ANY KEY TO STOP THE LAB')
    except Exception as e:
        print("*** APP FAILED : {}".format(e))
    finally:
        print("*** CLEANING UP THE LAB")
        lab.cleanup()
        unl.delete_lab(LAB_NAME)

if __name__ == '__main__':
    app()
