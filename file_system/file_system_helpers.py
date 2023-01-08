
def path_parse(path):

    split_path = path.split('\\')
    split_path = [entity for entity in split_path if entity != '']

    return split_path


def print_recursive(entity):

    string = entity.path + ' ' + str(entity.size) + '\n'

    if entity.entity_type != 'text':
        for entity_name in entity.get_names():
            string += print_recursive(entity.get_child(entity_name))

    return string
