from restunl.unetlab import UnlServer
from restunl.device import Router
from restunl.helper import *

LAB_NAME = 'test_1'
TOPOLOGY = {('R1', 'Ethernet0/0'): ('R2', 'Ethernet0/0'),
            ('R2', 'Ethernet0/1'): ('R3', 'Ethernet0/0'),
            ('R1', 'Ethernet0/1'): ('R3', 'Ethernet0/1'),
            ('R4', 'Ethernet0/0'): ('R1', 'Ethernet0/0')}


def app():
    try:
        unl = UnlServer('192.168.247.20')
        unl.login('admin', 'unl')
        print("*** CONNECTED TO UNL")
        lab = unl.create_lab(LAB_NAME)
        lab.cleanup()
        print("*** CREATED LAB")
        # Creating topology in UnetLab
        nodes = dict()
        for (a_name, a_intf), (b_name, b_intf) in TOPOLOGY.iteritems():
            # Create a mapping between a Node's name and an object
            if not a_name in nodes:
                nodes[a_name] = lab.create_node(Router(a_name))
                print("*** NODE {} CREATED".format(a_name))
            if not b_name in nodes:
                nodes[b_name] = lab.create_node(Router(b_name))
                print("*** NODE {} CREATED".format(b_name))
            # Extract Node objects using their names and connect them
            node_a = nodes[a_name]
            node_b = nodes[b_name]
            node_a.connect_node(a_intf, node_b, b_intf)
            print("*** NODES {0} and {1} ARE CONNECTED".format(a_name, b_name))
        print("*** TOPOLOGY IS BUILT")
        lab.start_all_nodes()
        print("*** NODES STARTED")
        # Reading and pushing configuration
        for node_name in nodes:
            conf = read_file('..\\config\\{}.txt'.format(node_name))
            nodes[node_name].configure(conf)
            print("*** NODE {} CONFIGURED".format(node_name))
        raw_input('PRESS ANY KEY TO STOP THE LAB')
    except Exception as e:
        print("*** APP FAILED : {}".format(e))
    finally:
        print("*** CLEANING UP THE LAB")
        lab.cleanup()
        unl.delete_lab(LAB_NAME)

if __name__ == '__main__':
    app()
