import unittest
from restunl.unetlab import *
from restunl.device import Router

UNETLAB_ADDRESS = '192.168.247.20'
USERNAME = 'admin'
PASSWORD = 'unl'
LAB_NAME = 'unittest_lab'
HOSTNAME = 'UNITT'
CONFIG = 'conf t \r\n hostname ' + HOSTNAME
VERIFY = 'show run | i hostname'


class UnlTests(unittest.TestCase):

    def setUp(self):
        self.unl = UnlServer(UNETLAB_ADDRESS)
        resp = self.unl.login(USERNAME, PASSWORD)
        self.assertEqual(200, resp.status_code)

    def tearDown(self):
        resp = self.unl.logout()
        self.assertEqual(200, resp.status_code)


class BasicUnlTests(UnlTests):

    def test_status(self):
        resp = self.unl.get_status()
        self.assertEqual(200, resp.status_code)

    def test_templates(self):
        resp = self.unl.get_templates()
        self.assertEqual(200, resp.status_code)

    def test_user_info(self):
        resp = self.unl.get_user_info()
        self.assertEqual(200, resp.status_code)


class BasicUnlLabTest(UnlTests):

    def test_create_lab(self):
        self.unl.delete_lab(LAB_NAME)
        resp = self.unl.create_lab(LAB_NAME).resp
        self.unl.delete_lab(LAB_NAME)
        self.assertEqual(200, resp.status_code)

    def test_delete_lab(self):
        self.unl.create_lab(LAB_NAME)
        resp = self.unl.delete_lab(LAB_NAME)
        self.assertEqual(200, resp.status_code)

    def test_get_nodes(self):
        lab = self.unl.create_lab(LAB_NAME)
        resp = lab.get_nodes()
        self.unl.delete_lab(LAB_NAME)
        self.assertEqual(200, resp.status_code)

    def test_create_node(self):
        lab = self.unl.create_lab(LAB_NAME)
        node = lab.create_node(Router('R1'))
        self.assertIn('telnet', node.url)

    def test_get_node(self):
        lab = self.unl.create_lab(LAB_NAME)
        device = Router('R1')
        lab.create_node(device)
        node = lab.get_node(Router('R1'))
        self.assertIn('telnet', node.url)

class AdvancedUnlNodeTest(UnlTests):

    def setUp(self):
        super(AdvancedUnlNodeTest, self).setUp()
        self.device_one = Router('R1')
        self.device_two = Router('R2')
        self.lab = self.unl.create_lab(LAB_NAME)
        self.node_one = self.lab.create_node(self.device_one)
        self.node_two = self.lab.create_node(self.device_two)

    def tearDown(self):
        self.unl.delete_lab(LAB_NAME)
        super(AdvancedUnlNodeTest, self).tearDown()

    def test_start_nodes(self):
        self.lab.stop_all_nodes()
        resp = self.lab.start_all_nodes()
        self.lab.stop_all_nodes()
        self.assertEqual(200, resp.status_code)

    def test_stop_nodes(self):
        self.lab.start_all_nodes()
        resp = self.lab.stop_all_nodes()
        self.assertEqual(200, resp.status_code)

    def test_delete_node(self):
        resp = self.lab.delete_node(self.node_one.id)
        self.assertEqual(200, resp.status_code)

    def test_del_all_nodes(self):
        self.lab.del_all_nodes()
        resp = self.lab.get_nodes()
        self.assertEqual(0, len(resp.json()['data']))

    def test_lab_cleanup(self):
        resp_1 = self.lab.stop_all_nodes()
        self.lab.del_all_nodes()
        resp_2 = self.lab.get_nodes()
        self.assertEqual(200, resp_1.status_code)
        self.assertEqual(0, len(resp_2.json()['data']))

    def test_connect_nodes(self):
        resp1, resp2 = self.node_one.connect_node('E0/0', self.node_two, 'E0/0')
        self.assertEqual(201, resp1.status_code)
        self.assertEqual(201, resp2.status_code)

    @unittest.skip("works but takes too long")
    def test_push_config(self):
        self.lab.start_all_nodes()
        self.node_one.configure(CONFIG)
        resp = self.node_one.configure(VERIFY)
        self.lab.start_all_nodes()
        self.assertIn(HOSTNAME, resp)

