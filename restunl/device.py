class Device(object):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return type(self).__name__ + '(' + self.name + ')'

    def to_json(self):
        return self.__dict__


class Router(Device):
    defaults = {
        'template': 'iol',
        'count': 1,
        'image': 'L3-ADVENTERPRISEK9-M-15.4-1T.bin',
        'ram': '256',
        'ethernet': '2',
        'serial': '0',
        'type': 'iol',
        'config': 'unconfigured'
    }

    def __init__(self, name):
        for key, value in Router.defaults.items():
            setattr(self, key, value)
        super(Router, self).__init__(name)
