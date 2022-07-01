import json

import pytest

from path_tree_generator import PathTree
from path_tree_generator.models.list_entries import ListEntry


def test_path_tree_dict(shared_datadir):
    pt = PathTree(
        root_dir=shared_datadir,
        relative_paths=True,
        paths_as_posix=True,
    )

    data_file = (shared_datadir/'data.json')
    expected_dict = ListEntry.parse_file(data_file)

    assert pt.dict() == expected_dict.dict()
    assert pt.dict() == pt.get_dict()
    assert pt.get_dict() == expected_dict.dict()


def test_path_tree_json(shared_datadir):
    pt = PathTree(
        root_dir=shared_datadir,
        relative_paths=True,
        paths_as_posix=True,
    )

    data_file = (shared_datadir/'data.json')
    expected_json = json.load(data_file.open(encoding='utf-8'))

    tree_json = json.loads(pt.json(exclude_unset=True))
    assert tree_json == expected_json

    tree_get_json = json.loads(pt.get_json(exclude_unset=True))
    assert tree_get_json == tree_json
    assert tree_get_json == expected_json


@pytest.mark.parametrize(
    argnames='expected_hr_tree',
    argvalues=["""[data]
├── data.json
├── data.tree
├── [myDirectory-1]
│   ├── myFile.txt
│   └── [subdirectory]
│       └── green.gif
└── [myDirectory-2]
    ├── [subdirectory1]
    │   └── green.gif
    └── [subdirectory2]
        ├── myFile.txt
        └── myFile2.txt"""],
    ids=['human readable'],
)
def test_path_tree_human_readable(shared_datadir, expected_hr_tree):
    pt = PathTree(root_dir=shared_datadir)

    actual_data = pt.human_readable()
    assert actual_data == expected_hr_tree

    data_file = (shared_datadir/'data.tree')
    expected_data = data_file.open(encoding='utf-8').read()

    actual_data += '\n'  # append an empty line for getting rid of a line-break problem while testing
    assert actual_data == expected_data

    get_hr_data = pt.get_human_readable()
    assert get_hr_data == actual_data
    assert get_hr_data == expected_data


@pytest.mark.parametrize(
    argnames='expected_hr_tree',
    argvalues=[
        [
            '[data]',
            '├── data.json',
            '├── data.tree',
            '├── [myDirectory-1]',
            '│   ├── myFile.txt',
            '│   └── [subdirectory]',
            '│       └── green.gif',
            '└── [myDirectory-2]',
            '    ├── [subdirectory1]',
            '    │   └── green.gif',
            '    └── [subdirectory2]',
            '        ├── myFile.txt',
            '        └── myFile2.txt'
        ]
    ],
    ids=['human readable']
)
def test_path_tree_human_readable_list(shared_datadir, expected_hr_tree):
    pt = PathTree(root_dir=shared_datadir)

    actual_data = pt.human_readable_list()
    assert actual_data == expected_hr_tree

    data_file = (shared_datadir/'data.tree')
    expected_data = data_file.open(encoding='utf-8').read()

    actual_data.append('')  # append an empty line for getting rid of a line-break problem while testing
    assert '\n'.join(actual_data) == expected_data

    get_hr_list = pt.get_human_readable_list()
    assert get_hr_list == expected_hr_tree
    assert get_hr_list == actual_data
    assert '\n'.join(get_hr_list) == expected_data


@pytest.mark.parametrize('relative_paths', [True, False])
@pytest.mark.parametrize('paths_as_posix', [True, False])
def test_path_tree_dict_parameters(relative_paths, paths_as_posix):
    pt = PathTree(
        root_dir='/not/relevant/for/this/test',
        relative_paths=relative_paths,
        paths_as_posix=paths_as_posix,
    )
    assert isinstance(pt.dict(), dict)


@pytest.mark.parametrize('relative_paths', [True, False])
@pytest.mark.parametrize('paths_as_posix', [True, False])
def test_path_tree_json_parameters(relative_paths, paths_as_posix):
    pt = PathTree(
        root_dir='/not/relevant/for/this/test',
        relative_paths=relative_paths,
        paths_as_posix=paths_as_posix,
    )
    assert isinstance(pt.json(), str)


@pytest.mark.parametrize('relative_paths', [True, False])
@pytest.mark.parametrize('paths_as_posix', [True, False])
def test_path_tree_human_readable_parameters(relative_paths, paths_as_posix):
    pt = PathTree(
        root_dir='/not/relevant/for/this/test',
        relative_paths=relative_paths,
        paths_as_posix=paths_as_posix,
    )
    assert isinstance(pt.human_readable(), str)


@pytest.mark.parametrize('relative_paths', [True, False])
@pytest.mark.parametrize('paths_as_posix', [True, False])
def test_path_tree_human_readable_list_parameters(relative_paths, paths_as_posix):
    pt = PathTree(
        root_dir='/not/relevant/for/this/test',
        relative_paths=relative_paths,
        paths_as_posix=paths_as_posix,
    )
    assert isinstance(pt.human_readable_list(), list)
