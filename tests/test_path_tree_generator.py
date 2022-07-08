import pathlib

import pytest

from path_tree_generator.models.list_entries import ListEntry, ListEntryStat, ListEntryType
from path_tree_generator.path_tree import _PathTreeGenerator


@pytest.mark.parametrize(
    argnames=['path', 'expected_dir_entry'],
    argvalues=[
        (
                pathlib.Path('/ptg_test_dir_not_available'),
                ListEntry(
                    entry_type=ListEntryType.dir,
                    name='ptg_test_dir_not_available',
                    path=pathlib.Path('/ptg_test_dir_not_available'),
                    children=None,
                ),
        )
    ],
    ids=['ptg_test_dir_not_available'],
)
def test_ptg_add_directory(path, expected_dir_entry):
    tree_list = _PathTreeGenerator(
        root_dir=pathlib.Path('test'),
        relative_paths=True,
        paths_as_posix=False,
        read_stat=False,
    )
    dir_entry = tree_list._get_dir_entry(path)

    assert type(dir_entry.entry_type) == ListEntryType
    assert dir_entry.entry_type == ListEntryType.dir
    assert dir_entry == expected_dir_entry


@pytest.mark.parametrize(
    argnames=['path', 'expected_file_entry'],
    argvalues=[
        (
                pathlib.Path('data.json'),
                ListEntry(
                    entry_type=ListEntryType.file,
                    name='data.json',
                    path=pathlib.Path('data.json'),
                ),
        )
    ],
    ids=['data.json'],
)
def test_ptg_add_file(path, expected_file_entry):
    tree_list = _PathTreeGenerator(
        root_dir=pathlib.Path('test'),
        relative_paths=True,
        paths_as_posix=False,
        read_stat=False,
    )
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
                name='data-with-stat.json',
                path=pathlib.Path('data-with-stat.json'),
            ),
            ListEntry(
                entry_type=ListEntryType.file,
                name='data.json',
                path=pathlib.Path('data.json'),
            ),
            ListEntry(
                entry_type=ListEntryType.file,
                name='data.tree',
                path=pathlib.Path('data.tree'),
            ),
            ListEntry(
                entry_type=ListEntryType.dir,
                name='myDirectory-1',
                path=pathlib.Path('myDirectory-1'),
                children=[
                    ListEntry(
                        entry_type=ListEntryType.file,
                        name='myFile.txt',
                        path=pathlib.Path('myDirectory-1/myFile.txt'),
                    ),
                    ListEntry(
                        entry_type=ListEntryType.dir,
                        name='subdirectory',
                        path=pathlib.Path('myDirectory-1/subdirectory'),
                        children=[
                            ListEntry(
                                entry_type=ListEntryType.file,
                                name='green.gif',
                                path=pathlib.Path('myDirectory-1/subdirectory/green.gif'),
                            )
                        ]
                    ),
                ],
            ),
            ListEntry(
                entry_type=ListEntryType.dir,
                name='myDirectory-2',
                path=pathlib.Path('myDirectory-2'),
                children=[
                    ListEntry(
                        entry_type=ListEntryType.dir,
                        name='subdirectory1',
                        path=pathlib.Path('myDirectory-2/subdirectory1'),
                        children=[
                            ListEntry(
                                entry_type=ListEntryType.file,
                                name='green.gif',
                                path=pathlib.Path('myDirectory-2/subdirectory1/green.gif'),
                            ),
                        ],
                    ),
                    ListEntry(
                        entry_type=ListEntryType.dir,
                        name='subdirectory2',
                        path=pathlib.Path('myDirectory-2/subdirectory2'),
                        children=[
                            ListEntry(
                                entry_type=ListEntryType.file,
                                name='myFile.txt',
                                path=pathlib.Path('myDirectory-2/subdirectory2/myFile.txt'),
                            ),
                            ListEntry(
                                entry_type=ListEntryType.file,
                                name='myFile2.txt',
                                path=pathlib.Path('myDirectory-2/subdirectory2/myFile2.txt'),
                            ),
                        ],
                    ),
                ],
            ),
        ],
    ],
)
def test_ptg_build_tree(shared_datadir, expected_tree):
    root_dir = shared_datadir
    ptg = _PathTreeGenerator(
        root_dir=root_dir,
        relative_paths=True,
        paths_as_posix=False,
        read_stat=False,
    )

    assert ptg._tree_built is False
    ptg._build_tree(root_dir)
    assert ptg._tree_built is True
    assert ptg._tree_list == expected_tree


@pytest.mark.parametrize('relative_paths', [True, False])
@pytest.mark.parametrize('paths_as_posix', [True, False])
def test_ptg_get_tree_with_root_dir(shared_datadir, relative_paths, paths_as_posix):
    ptg = _PathTreeGenerator(
        root_dir=shared_datadir,
        relative_paths=relative_paths,
        paths_as_posix=paths_as_posix,
        read_stat=False,
    )
    assert isinstance(ptg, _PathTreeGenerator)
    assert ptg._tree_built is False
    assert isinstance(ptg.get_tree(), ListEntry)
    assert isinstance(ptg.get_tree(), ListEntry)
    assert ptg._tree_built is True


@pytest.mark.parametrize('relative_paths', [True, False])
@pytest.mark.parametrize('paths_as_posix', [True, False])
def test_ptg_human_readable(shared_datadir, relative_paths, paths_as_posix):
    ptg = _PathTreeGenerator(
        root_dir=shared_datadir,
        relative_paths=relative_paths,
        paths_as_posix=paths_as_posix,
        read_stat=False,
    )
    assert isinstance(ptg, _PathTreeGenerator)
    assert ptg._tree_built is False
    assert isinstance(ptg.get_tree_human_readable(), str)
    assert ptg._tree_built is True


@pytest.mark.parametrize('relative_paths', [True, False])
@pytest.mark.parametrize('paths_as_posix', [True, False])
def test_ptg_human_readable_list(shared_datadir, relative_paths, paths_as_posix):
    ptg = _PathTreeGenerator(
        root_dir=shared_datadir,
        relative_paths=relative_paths,
        paths_as_posix=paths_as_posix,
        read_stat=False,
    )
    assert isinstance(ptg, _PathTreeGenerator)
    assert ptg._tree_built is False
    assert isinstance(ptg.get_tree_human_readable_list(), list)
    assert ptg._tree_built is True


@pytest.mark.parametrize(
    argnames='expected_hr_tree',
    argvalues=["""[data]
├── data-with-stat.json
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
    ids=['human readable']
)
def test_ptg_hr_tree(shared_datadir, expected_hr_tree):
    root_dir = shared_datadir
    ptg = _PathTreeGenerator(
        root_dir=root_dir,
        relative_paths=True,
        paths_as_posix=False,
        read_stat=False,
    )

    assert ptg._tree_built is False
    assert ptg.get_tree_human_readable(root_dir_name_only=True) == expected_hr_tree
    assert ptg._tree_built is True


@pytest.mark.parametrize(
    argnames='expected_hr_tree',
    argvalues=[
        [
            '[data]',
            '├── data-with-stat.json',
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
def test_ptg_hr_list_tree(shared_datadir, expected_hr_tree):
    root_dir = shared_datadir
    ptg = _PathTreeGenerator(
        root_dir=root_dir,
        relative_paths=True,
        paths_as_posix=False,
        read_stat=False,
    )

    assert ptg._tree_built is False
    assert ptg.get_tree_human_readable_list(root_dir_name_only=True) == expected_hr_tree
    assert ptg._tree_built is True


def test_ptg_build_tree_with_stat(shared_datadir):
    root_dir = shared_datadir
    ptg = _PathTreeGenerator(
        root_dir=root_dir,
        relative_paths=True,
        paths_as_posix=False,
        read_stat=True,
    )

    assert ptg._tree_built is False
    ptg._build_tree(root_dir)
    assert ptg._tree_built is True

    tl = ptg._tree_list
    for le in tl:
        assert isinstance(le, ListEntry)
        assert isinstance(le.stat, ListEntryStat)
        assert le.stat.size >= 0
        assert le.stat.ctime > 1640988000.0
