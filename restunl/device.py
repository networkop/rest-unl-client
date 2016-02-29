from telnetlib import Telnet
import time
import re


class UnetlabDeviceException(Exception):
    pass


class IOL(object):

    def __init__(self, name):
        self.name = name
        self.url_ip, self.url_port = '', ''
        self.intf_index = 0

    @staticmethod
    def get_intf_id(intf_name):
        x, y = re.findall('\d+', intf_name)
        return int(x) + (int(y) * 16)

    @staticmethod
    def send_and_wait(session, text):
        session.read_very_eager()
        result = ''
        session.write(text)
        while not any(stop_char in result[-5:] for stop_char in ['>', '#', 'no]:']):
            session.write('\r\n')
            result += session.read_very_eager()
            time.sleep(0.1)
        return result

    def get_next_intf(self):
        if self.intf_index > 64:
            raise UnetlabDeviceException('Too many interface configured')
        else:
            intf_module = self.intf_index / 4
            intf_number = self.intf_index % 4
        return 'Ethernet' + intf_module + '/' + intf_number

    def __repr__(self):
        return type(self).__name__ + '(' + self.name + ')'

    def to_json(self):
        return self.__dict__

    def set_url(self, url):
        self.url_ip, self.url_port = str(url).strip('telnet://').split(':')
        return None

    def send_config(self, config):
        session = Telnet(self.url_ip, self.url_port)
        result = self.send_and_wait(session, '\r\n')
        for line in config.splitlines():
            result = self.send_and_wait(session, line)
        session.close()
        return result


class Router(IOL):
    defaults = {
        'template': 'iol',
        'count': 1,
        'image': 'L2-ADVENTERPRISE-LATEST.bin',
        'ram': '256',
        'ethernet': '16',
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


class Switch(IOL):
    defaults = {
        'template': 'iol',
        'count': 1,
        'image': 'L3-ADVENTERPRISEK9-LATEST.bin',
        'ram': '256',
        'ethernet': '16',
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


def main():
    sw = Switch('sw', 'image')
    print sw.image
    print sw.ram


if __name__ == '__main__':
    main()
