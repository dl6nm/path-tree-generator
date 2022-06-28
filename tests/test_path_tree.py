import json

import pytest

from path_tree_generator import PathTree


def test_path_tree_dict(shared_datadir):
    pt = PathTree(root_dir=shared_datadir)
    data_file = (shared_datadir/'data.json')
    data = json.load(data_file.open(encoding='utf-8'))
    assert pt.dict() == data


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
def test_path_tree_human_readable(shared_datadir, expected_hr_tree):
    pt = PathTree(root_dir=shared_datadir)

    assert pt.human_readable() == expected_hr_tree

    data_file = (shared_datadir/'data.tree')
    expected_data = data_file.open(encoding='utf-8').read()

    actual_data = pt.human_readable()
    actual_data.append('')  # append an empty line for getting rid of a line-break problem while testing
    assert '\n'.join(actual_data) == expected_data
