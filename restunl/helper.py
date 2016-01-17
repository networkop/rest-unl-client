import time
import re


def append_unl(name):
    return name + ".unl"


def get_obj_by_name(objects, name):
    for obj_id in objects:
        if objects[obj_id]["name"] == name:
            return objects[obj_id]
    return None


def get_intf_id(intf_name):
    x, y = re.findall('\d+', intf_name)
    return int(x) + (int(y) * 16)


def send_and_wait(session, text):
        session.read_very_eager()
        result = ''
        session.write(text)
        while not any(stop_char in result[-5:] for stop_char in ['>', '#']):
            session.write('\r\n')
            result += session.read_very_eager()
            time.sleep(0.1)
        return result


def read_file(filename):
    with open(filename) as f:
        return ''.join(f.readlines())


def wrap_conf(text):
    return '\r\n'.join(['enable',  text, 'end'])
