from telnetlib import Telnet
from helper import *


class Device(object):
    def __init__(self, name):
        self.name = name
        self.url_ip, self.url_port = '', ''

    def __repr__(self):
        return type(self).__name__ + '(' + self.name + ')'

    def to_json(self):
        return self.__dict__

    def set_url(self, url):
        self.url_ip, self.url_port = str(url).strip('telnet://').split(':')
        return None

    def send_config(self, config):
        session = Telnet(self.url_ip, self.url_port)
        send_and_wait(session, '\r\n')
        result = send_and_wait(session, config)
        session.close()
        return result


class Router(Device):
    defaults = {
        'template': 'iol',
        'count': 1,
        'image': 'L2-ADVENTERPRISE-LATEST.bin',
        'ram': '256',
        'ethernet': '2',
        'serial': '0',
        'type': 'iol',
        'config': 'unconfigured'
    }

    def __init__(self, name, image=None):
        if image:
            Router.defaults['image'] = image
        for key, value in Router.defaults.items():
            setattr(self, key, value)
        super(Router, self).__init__(name)


class Switch(Device):
    defaults = {
        'template': 'iol',
        'count': 1,
        'image': 'L3-ADVENTERPRISEK9-LATEST.bin',
        'ram': '256',
        'ethernet': '2',
        'serial': '0',
        'type': 'iol',
        'config': 'unconfigured'
    }

    def __init__(self, name, image=None):
        if image:
            Switch.defaults['image'] = image
        for key, value in Switch.defaults.items():
            setattr(self, key, value)
        super(Switch, self).__init__(name)

