from file_system.file_system_helpers import path_parse, print_recursive
from file_system.file_system import FileSystem


def test_path_parse():
    """
    Test the path parser, which should remove leading/trailing \s and return a list of the path's entities
    """

    path = '\\A\\stuff\\list\\'

    parsed_path = path_parse(path)

    expected_results = ['A', 'stuff', 'list']

    assert parsed_path == expected_results


def test_print_recursive():
    """
    Test a helper function that recursively prints the contents of an entity
    """

    file_system = FileSystem()

    file_system.create('drive', 'A', '')
    file_system.create('folder', 'stuff', 'A')
    file_system.create('text', 'list', 'A\\stuff')
    file_system.create('folder', 'more_stuff', 'A')

    output_string = print_recursive(file_system._root)
    expected_string = ' 0\nA 0\nA\\stuff 0\nA\\stuff\\list 0\nA\\more_stuff 0\n'

    assert output_string == expected_string
