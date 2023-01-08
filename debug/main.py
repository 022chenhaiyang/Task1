from file_system.file_system import FileSystem


def main():
    """
    Demonstrates the FileSystem implementation.
    Executes methods and prints the file system structure after each operation.
    """

    print('\n##############')
    print('# File System')
    print('##############\n')

    print('Package in /file_system\n')

    print('Pytest suite in /tests\n')

    print('###################')
    print('# File System Demo')
    print('###################\n')

    print('1. Creating File System')
    file_system = FileSystem()

    print('2. Adding DriveA to Root')
    file_system.create('drive', 'DriveA', '')
    print('Current File System Structure: \n' + str(file_system))
    print()

    print('3. Adding DriveB to Root')
    file_system.create('drive', 'DriveB', '')
    print('Current File System Structure: \n' + str(file_system))
    print()

    print('4. Adding FolderA to DriveA')
    file_system.create('folder', 'FolderA', 'DriveA')
    print('Current File System Structure: \n' + str(file_system))
    print()

    print('5. Adding FolderB to DriveB')
    folder_b = file_system.create('folder', 'FolderB', 'DriveB')
    print('Current File System Structure: \n' + str(file_system))
    print()

    print('6. Adding FolderC to FolderB')
    file_system.create('folder', 'FolderC', 'DriveB\\FolderB')
    print('Current File System Structure: \n' + str(file_system))
    print()

    print('7. Adding ZipA to DriveA')
    zip_a = file_system.create('byte', 'byteA', 'DriveA')
    print('Current File System Structure: \n' + str(file_system))
    print()

    print('8. Adding TextA to FolderC')
    text_a = file_system.create('text', 'TextA', 'DriveB\\FolderB\\FolderC')
    print('Current File System Structure: \n' + str(file_system))
    print()

    print('9. Updating TextA Content with \'testabcd\'')
    file_system.wirteToFile(text_a.path, 'testabcd')
    print('Current File System Structure: \n' + str(file_system))
    print()

    print('10. Adding TextB to ZipA')
    text_b = file_system.create('text', 'TextB', 'DriveA\\ZipA')
    print('Current File System Structure: \n' + str(file_system))
    print()

    print('11. Updating TextB Content with \'testabcdtestabcd\'')
    file_system.wirteToFile(text_b.path, 'testabcdtestabcd')
    print('Current File System Structure: \n' + str(file_system))
    print()

    print('12. Move FolderB into ZipA')
    file_system.move(folder_b.path, zip_a.path)
    print('Current File System Structure: \n' + str(file_system))
    print()


if __name__ == '__main__':
    main()
