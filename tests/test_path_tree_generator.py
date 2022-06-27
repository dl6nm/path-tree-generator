import pathlib

import pytest

from path_tree_generator.models.list_entries import ListEntry, ListEntryType
from path_tree_generator.path_tree_generator import _PathTreeGenerator


@pytest.mark.parametrize(
    argnames=['path', 'children', 'expected'],
    argvalues=[
        (
                pathlib.Path('/data'),
                None,
                {
                    'entry': ListEntry(
                        entry_type=ListEntryType.dir,
                        name='data',
                        path=pathlib.Path('/data'),
                        children=None,
                    ),
                    'length': 1,
                }
        )
    ],
    ids=['data'],
)
def test_ptg_add_directory(path, children, expected):
    tree_list = _PathTreeGenerator('test')
    tree_list._add_directory(path, children)

    list_entry = tree_list.get_tree()

    assert type(list_entry[0].entry_type) == ListEntryType
    assert list_entry[0].entry_type == ListEntryType.dir

    assert len(list_entry) == expected.get('length')
    assert list_entry[0] == expected.get('entry')


@pytest.mark.parametrize(
    argnames=['path', 'expected'],
    argvalues=[
        (
                pathlib.Path('/data/data.json'),
                {
                    'entry': ListEntry(
                        entry_type=ListEntryType.file,
                        name='data.json',
                        path=pathlib.Path('/data/data.json'),
                    ),
                    'length': 1,
                }
        )
    ],
    ids=['data.json'],
)
def test_ptg_add_file(path, expected):
    tree_list = _PathTreeGenerator('test')
    tree_list._add_file(path)

    list_entry = tree_list.get_tree()

    assert type(list_entry[0].entry_type) == ListEntryType
    assert list_entry[0].entry_type == ListEntryType.file

    assert len(list_entry) == expected.get('length')
    assert list_entry[0] == expected.get('entry')


def test_ptg_build_tree():
    assert False


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
