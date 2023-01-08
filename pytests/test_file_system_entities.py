import pytest
from file_system.file_system_entities import FileSystemEntity, Root, Drive, Folder, byte, Text
from file_system.file_system_exceptions import IllegalFileSystemOperation, PathNotFound, PathAlreadyExists


def test_file_system_entity():
    """
    Test the getter/setters for the file system entity properties
    """

    entity = FileSystemEntity('drive', 'A', 'A')

    # test entity_type updates
    assert entity.entity_type == 'drive'

    entity.entity_type = 'folder'
    assert entity.entity_type == 'folder'

    with pytest.raises(IllegalFileSystemOperation):
        entity.entity_type = 'test'
    assert entity.entity_type == 'folder'

    # test name updates
    assert entity.name == 'A'

    entity.name = 'B'
    assert entity.name == 'B'

    # test path updates
    entity.name = 'A'
    assert entity.path == 'A'

    entity.path = 'B\\A'
    assert entity.path == 'B\\A'

    with pytest.raises(PathNotFound):
        entity.path = 'B\\C'
    assert entity.path == 'B\\A'

    # test size updates
    assert entity.size == 0

    entity.size = 10
    assert entity.size == 10


def test_root():
    """
    Test that a Root container can only contains drives with unique names
    """

    root = Root('root', 'root', '')

    drive = Drive('drive', 'A', 'A')

    root.add_child(drive)

    assert root.get_child('A') is drive

    folder = Folder('folder', 'stuff', 'stuff')

    with pytest.raises(IllegalFileSystemOperation):
        root.add_child(folder)

    assert 'stuff' not in root.get_names()

    dup_name_drive = Drive('drive', 'A', 'A')

    with pytest.raises(PathAlreadyExists):
        root.add_child(dup_name_drive)


def test_drive():
    """
    Test that a Drive container can only contains folders/bytes/text with unique names
    """

    drive = Drive('drive', 'A', 'A')

    folder = Folder('folder', 'stuff', 'A\\stuff')

    drive.add_child(folder)

    assert drive.get_child('stuff') is folder

    drive_test = Drive('drive', 'B', 'A\\B')

    with pytest.raises(IllegalFileSystemOperation):
        drive.add_child(drive_test)

    assert 'B' not in drive.get_names()

    dup_name_folder = Folder('folder', 'stuff', 'A\\stuff')

    with pytest.raises(PathAlreadyExists):
        drive.add_child(dup_name_folder)


def test_folder():
    """
    Test that a Folder container can only contains folders/bytes/text with unique names
    """

    drive = Drive('drive', 'A', 'A')

    folder = Folder('folder', 'stuff', 'A\\stuff')

    drive.add_child(folder)

    text = Text('text', 'list', 'A\\stuff\\list')
    text_dup = Text('text', 'list', 'A\\stuff\\list')

    folder.add_child(text)

    with pytest.raises(PathAlreadyExists):
        folder.add_child(text_dup)

    drive_test = Drive('drive', 'B', 'A\\stuff\\B')

    with pytest.raises(IllegalFileSystemOperation):
        folder.add_child(drive_test)


def test_byte():
    """
    Test that a byte container can only contains folders/bytes/text with unique names, and that any sizes
    passing through it are halved.
    """

    drive = Drive('drive', 'A', 'A')

    byte1 = byte('byte', 'stuff', 'A\\stuff')

    drive.add_child(byte1)

    text = Text('text', 'list', 'A\\stuff\\list')
    text_dup = Text('text', 'list', 'A\\stuff\\list')

    byte1.add_child(text)

    with pytest.raises(PathAlreadyExists):
        byte1.add_child(text_dup)

    drive_test = Drive('drive', 'B', 'A\\stuff\\B')

    print(drive_test.entity_type)

    with pytest.raises(IllegalFileSystemOperation):
        byte1.add_child(drive_test)


def test_text():
    """
    Test a Text entity and the getters/setter for the content property
    """

    drive = Drive('drive', 'A', 'A')

    text = Text('text', 'list', 'A\\list')

    drive.add_child(text)

    text.content = 'test'
    assert text.content == 'test'

