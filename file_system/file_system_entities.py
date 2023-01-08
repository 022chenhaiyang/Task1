from file_system.file_system_helpers import path_parse
from file_system.file_system_exceptions import IllegalFileSystemOperation, PathNotFound, PathAlreadyExists


class FileSystemEntity:
    """
    Represents an entity in our file system

    Every entity has the following properties:

    entity_type – The type of the entity ('root', 'drive', 'folder', 'zip', 'text').
    name - An alphanumeric string. Two entities with the same parent cannot have the same name.
    path – The concatenation of the names of the containing entities, from the drive down to and including the entity.
        The names are separated by ‘\’.
    size – an integer defined as follows:
        For a text file – it is the length of its content.
        For a drive or a folder, it is the sum of all sizes of the entities it contains.
        For a zip file, it is one half of the sum of all sizes of the entities it contains.
    """

    VALID_ENTITIES = ['root', 'drive', 'folder', 'zip', 'text']

    def __init__(self, entity_type, name, path):
        self._entity_type = entity_type
        self._name = name
        self._path = path
        self._size = 0  # all entities either empty container or content-less text at init

    @property
    def entity_type(self):
        return self._entity_type

    @entity_type.setter
    def entity_type(self, new_type):
        if new_type not in self.VALID_ENTITIES:
            raise IllegalFileSystemOperation(
                'Not a valid entity type, must be \'drive\', \'folder\', \'zip\', or \'text\''
            )
        else:
            self._entity_type = new_type

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        self._name = new_name

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, new_path):
        # cleanup leading/trailing \'s
        new_path = path_parse(new_path)
        path_name = new_path[-1]
        if self.name != path_name:
            raise PathNotFound('Name in path does not match file name')
        else:
            self._path = '\\'.join(new_path)

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, new_size):
        self._size = new_size


class Container(FileSystemEntity):
    """
    Containers may contain zero to many other entities.
    """

    def __init__(self, entity_type, name, path):
        FileSystemEntity.__init__(self, entity_type, name, path)
        self._children = {}

    def get_child(self, name):
        return self._children[name]

    def get_names(self):
        return self._children.keys()

    def delete_child(self, name):
        del self._children[name]

    @FileSystemEntity.path.setter
    def path(self, new_path):
        self._path = new_path

        # recursively update the children's paths,
        # base case is text's non-recursive path update
        # and containers with empty children sets.
        for child in self._children.keys():
            child_entity = self._children[child]
            child_entity.path = '{parent_path}\\{name}'.format(parent_path=new_path, name=child_entity.name)


class Root(Container):
    """
    The root of the file system where drives reside
    """

    VALID_ROOT_CHILDREN = ['drive']

    def __init__(self, entity_type, name, path):
        Container.__init__(self, entity_type, name, path)

    def add_child(self, child):
        if child.name in self._children.keys():
            raise PathAlreadyExists('An entity with that name already exists')
        elif child.entity_type not in self.VALID_ROOT_CHILDREN:
            raise IllegalFileSystemOperation('You cannot add a non-drive to the root')
        else:
            self._children[child.name] = child


class Drive(Container):
    """
    Represents a physical drive that exist only within the system's root
    """

    VALID_DRIVE_CHILDREN = ['folder', 'zip', 'text']

    def __init__(self, entity_type, name, path):
        Container.__init__(self, entity_type, name, path)

    def add_child(self, child):
        if child.name in self._children.keys():
            raise PathAlreadyExists('An entity with that name already exists')
        elif child.entity_type not in self.VALID_DRIVE_CHILDREN:
            raise IllegalFileSystemOperation('Entity is not valid for adding to a Drive')
        else:
            self._children[child.name] = child


class Folder(Container):
    """
    Represents a folder, which can be contained within drives, folders, and zips
    and can contain folders, zips, and text.
    """

    VALID_FOLDER_CHILDREN = ['folder', 'zip', 'text']

    def __init__(self, entity_type, name, path):
        Container.__init__(self, entity_type, name, path)

    def add_child(self, child):
        if child.name in self._children.keys():
            raise PathAlreadyExists('An entity with that name already exists')
        elif child.entity_type not in self.VALID_FOLDER_CHILDREN:
            raise IllegalFileSystemOperation('Entity is not valid for adding to a Folder')
        else:
            self._children[child.name] = child


class Zip(Container):
    """
    The same as a folder, but will only inherit half the size of its children
    """

    VALID_ZIP_CHILDREN = ['folder', 'zip', 'text']

    def __init__(self, entity_type, name, path):
        Container.__init__(self, entity_type, name, path)

    def add_child(self, child):
        if child.name in self._children.keys():
            raise PathAlreadyExists('An entity with that name already exists')
        elif child.entity_type not in self.VALID_ZIP_CHILDREN:
            raise IllegalFileSystemOperation('Entity is not valid for adding to a Zip')
        else:
            self._children[child.name] = child


class Text(FileSystemEntity):
    """
    A text file has a property called Content which is a string.
    """

    def __init__(self, entity_type, name, path):
        FileSystemEntity.__init__(self, entity_type, name, path)
        self._content = ''

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, new_content):
        self._content = new_content
