import pathlib

import pytest

from path_tree_generator.models.list_entries import ListEntry, ListEntryType
from path_tree_generator.path_tree_generator import _PathTreeGenerator


@pytest.mark.parametrize(
    argnames=['path', 'expected_dir_entry'],
    argvalues=[
        (
                pathlib.Path('/data'),
                ListEntry(
                    entry_type=ListEntryType.dir,
                    name='data',
                    path=pathlib.Path('/data'),
                    children=None,
                ),
        )
    ],
    ids=['data'],
)
def test_ptg_add_directory(path, expected_dir_entry):
    tree_list = _PathTreeGenerator(pathlib.Path('test'))
    dir_entry = tree_list._get_dir_entry(path)

    assert type(dir_entry.entry_type) == ListEntryType
    assert dir_entry.entry_type == ListEntryType.dir
    assert dir_entry == expected_dir_entry


@pytest.mark.parametrize(
    argnames=['path', 'expected_file_entry'],
    argvalues=[
        (
                pathlib.Path('/data/data.json'),
                ListEntry(
                    entry_type=ListEntryType.file,
                    name='data.json',
                    path=pathlib.Path('/data/data.json'),
                ),
        )
    ],
    ids=['data.json'],
)
def test_ptg_add_file(path, expected_file_entry):
    tree_list = _PathTreeGenerator(pathlib.Path('test'))
    file_entry = tree_list._get_file_entry(path)

    assert type(file_entry.entry_type) == ListEntryType
    assert file_entry.entry_type == ListEntryType.file

    assert file_entry == expected_file_entry


@pytest.mark.parametrize(
    argnames='expected_tree',
    argvalues=[
        [
            ListEntry(
                entry_type=ListEntryType.file,
                name='data.json',
                path=pathlib.Path('data/data.json')
            ),
            ListEntry(
                entry_type=ListEntryType.file,
                name='data.tree',
                path=pathlib.Path('data/data.tree')
            ),
            ListEntry(
                entry_type=ListEntryType.dir,
                name='myDirectory-1',
                path=pathlib.Path('data/myDirectory-1'),
                children=[
                    ListEntry(
                        entry_type=ListEntryType.dir,
                        name='subdirectory',
                        path=pathlib.Path('data/myDirectory-1/subdirectory'),
                        children=[
                            ListEntry(
                                entry_type=ListEntryType.file,
                                name='green.gif',
                                path=pathlib.Path('data/myDirectory-1/subdirectory/green.gif')
                            )
                        ]
                    ),
                    ListEntry(
                        entry_type=ListEntryType.file,
                        name='myFile.txt',
                        path=pathlib.Path('data/myDirectory-1/myFile.txt')
                    )
                ]
            ),
            ListEntry(
                entry_type=ListEntryType.dir,
                name='myDirectory-2',
                path=pathlib.Path('data/myDirectory-2'),
                children=[
                    ListEntry(
                        entry_type=ListEntryType.dir,
                        name='subdirectory1',
                        path=pathlib.Path('data/myDirectory-2/subdirectory1'),
                        children=[
                            ListEntry(
                                entry_type=ListEntryType.file,
                                name='green.gif',
                                path=pathlib.Path('data/myDirectory-2/subdirectory1/green.gif')
                            )
                        ]
                    ),
                    ListEntry(
                        entry_type=ListEntryType.dir,
                        name='subdirectory2',
                        path=pathlib.Path('data/myDirectory-2/subdirectory2'),
                        children=[
                            ListEntry(
                                entry_type=ListEntryType.file,
                                name='myFile.txt',
                                path=pathlib.Path('data/myDirectory-2/subdirectory2/myFile.txt')
                            ),
                            ListEntry(
                                entry_type=ListEntryType.file,
                                name='myFile2.txt',
                                path=pathlib.Path('data/myDirectory-2/subdirectory2/myFile2.txt')
                            )
                        ]
                    )
                ]
            )
        ]
    ],
)
def test_ptg_build_tree(shared_datadir, expected_tree):
    root_dir = shared_datadir
    ptg = _PathTreeGenerator(root_dir=root_dir)

    print('\n', '#' * 100)
    print(f'root_dir: {root_dir}')
    print('#' * 100)

    assert ptg._tree_built is False
    ptg._build_tree(root_dir, relative_paths=True)
    assert ptg._tree_built is True
    assert ptg._tree_list == expected_tree


def test_ptg_get_tree(shared_datadir):
    ptg = _PathTreeGenerator(root_dir=shared_datadir)
    assert isinstance(ptg, _PathTreeGenerator)
    assert ptg._tree_built is False
    assert isinstance(ptg.get_tree(), list)
    assert ptg._tree_built is True


def test_ptg_human_readable(shared_datadir):
    ptg = _PathTreeGenerator(root_dir=shared_datadir)
    assert isinstance(ptg, _PathTreeGenerator)
    assert ptg._tree_built is False
    assert isinstance(ptg.get_tree_human_readable(), list)
    assert ptg._tree_built is True
