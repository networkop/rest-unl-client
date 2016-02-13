
def append_unl(name):
    return name + ".unl"


def get_obj_by_name(objects, name):
    for obj_id in objects:
        if objects[obj_id]["name"] == name:
            return objects[obj_id]
    return None


def read_file(filename):
    with open(filename) as f:
        return ''.join(f.readlines())
