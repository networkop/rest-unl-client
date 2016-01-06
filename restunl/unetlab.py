from server import RestServer
from helper import *

REST_SCHEMA = {
    'login': '/auth/login',
    'logout': '/auth/logout',
    'status': '/status',
    'list_templates': '/list/templates/',
    'get_user_info': '/auth',
    'create_lab': '/labs',
    'create_node': '/labs/{lab_name}/nodes',
    'delete_lab': '/labs/{lab_name}',
    'get_all_nodes': '/labs/{lab_name}/nodes',
}


class UnlServer(RestServer):

    def __init__(self, address):
        super(UnlServer, self).__init__(address)

    def login(self, user, pwd):
        api_call = REST_SCHEMA['login']
        payload = {
            "username": user,
            "password": pwd
        }
        resp = self.add_object(api_call, data=payload)
        self.set_cookies(resp.cookies)
        return resp

    def logout(self):
        api_call = REST_SCHEMA['logout']
        resp = self.get_object(api_call)
        return resp

    def get_status(self):
        api_call = REST_SCHEMA['status']
        resp = self.get_object(api_call)
        return resp

    def get_templates(self):
        api_call = REST_SCHEMA['list_templates']
        resp = self.get_object(api_call)
        return resp

    def get_user_info(self):
        api_call = REST_SCHEMA['get_user_info']
        resp = self.get_object(api_call)
        return resp

    def create_lab(self, name):
        return UnlLab(self, name)

    def delete_lab(self, labname):
        api_call = REST_SCHEMA['delete_lab']
        api_url = api_call.format(api_call, lab_name=append_unl(labname))
        resp = self.del_object(api_url)
        return resp


class UnlLab(object):

    def __init__(self, unl, name):
        api_call = REST_SCHEMA['create_lab']
        payload = {
           "path": "/",
           "name": name,
           "version": "1"
        }
        self.name = name
        self.unl = unl
        self.resp = self.unl.add_object(api_call, data=payload)

    def create_node(self, device):
        return UnlNode(self, device)

    def get_nodes(self):
        api_call = REST_SCHEMA['get_all_nodes']
        api_url = api_call.format(api_call, lab_name=append_unl(self.name))
        resp = self.unl.get_object(api_url)
        return resp


class UnlNode(object):

    def __init__(self, lab, device):
        self.unl = lab.unl
        self.lab = lab
        self.device = device
        api_call = REST_SCHEMA['create_node']
        api_url = api_call.format(api_call, lab_name=append_unl(self.lab.name))
        payload = self.device.to_json()
        self.resp = self.unl.add_object(api_url, data=payload)