import json

import pytest

from path_tree_generator import PathTree
from path_tree_generator.models.list_entries import ListEntry


@pytest.mark.parametrize(
    argnames='filename',
    argvalues=['data.json'],
)
def test_path_tree_dict(shared_datadir, example_data, filename):
    pt = PathTree(
        root_dir=shared_datadir,
        relative_paths=True,
        paths_as_posix=True,
        read_stat=False,
    )
    expected_dict = ListEntry(**example_data)
    assert pt.dict() == expected_dict.dict()


def test_path_tree_json(shared_datadir):
    pt = PathTree(
        root_dir=shared_datadir,
        relative_paths=True,
        paths_as_posix=True,
        read_stat=False,
    )

    data_file = (shared_datadir/'data.json')
    expected_json = json.load(data_file.open(encoding='utf-8'))

    tree_json = json.loads(pt.json(exclude_unset=True))
    assert tree_json == expected_json


@pytest.mark.parametrize(
    argnames='filename',
    argvalues=['data.tree'],
    ids=['human readable'],
)
def test_path_tree_human_readable(shared_datadir, example_data_string, filename):
    pt = PathTree(root_dir=shared_datadir)
    actual_data = pt.human_readable()
    assert actual_data == example_data_string


@pytest.mark.parametrize(
    argnames='filename',
    argvalues=[
        'data.tree',
    ],
    ids=['human readable'],
)
def test_path_tree_human_readable_list(shared_datadir, example_data_list, filename):
    pt = PathTree(root_dir=shared_datadir)

    actual_data = pt.human_readable_list()
    assert actual_data == example_data_list

    data_file = (shared_datadir/'data.tree')
    expected_data = data_file.open(encoding='utf-8').read()

    # append an empty line to 'actual_data'
    # for getting rid of a line-break problem while testing
    actual_data.append('')
    assert '\n'.join(actual_data) == expected_data


@pytest.mark.parametrize('relative_paths', [True, False])
@pytest.mark.parametrize('paths_as_posix', [True, False])
@pytest.mark.parametrize('read_stat', [True, False])
def test_path_tree_dict_parameters(relative_paths, paths_as_posix, read_stat):
    pt = PathTree(
        root_dir='/not/relevant/for/this/test',
        relative_paths=relative_paths,
        paths_as_posix=paths_as_posix,
        read_stat=read_stat,
    )
    assert isinstance(pt.dict(), dict)


@pytest.mark.parametrize('relative_paths', [True, False])
@pytest.mark.parametrize('paths_as_posix', [True, False])
@pytest.mark.parametrize('read_stat', [True, False])
def test_path_tree_json_parameters(relative_paths, paths_as_posix, read_stat):
    pt = PathTree(
        root_dir='/not/relevant/for/this/test',
        relative_paths=relative_paths,
        paths_as_posix=paths_as_posix,
        read_stat=read_stat,
    )
    assert isinstance(pt.json(), str)


@pytest.mark.parametrize('relative_paths', [True, False])
@pytest.mark.parametrize('paths_as_posix', [True, False])
@pytest.mark.parametrize('read_stat', [True, False])
def test_path_tree_human_readable_parameters(relative_paths, paths_as_posix, read_stat):
    pt = PathTree(
        root_dir='/not/relevant/for/this/test',
        relative_paths=relative_paths,
        paths_as_posix=paths_as_posix,
        read_stat=read_stat,
    )
    assert isinstance(pt.human_readable(), str)


@pytest.mark.parametrize('relative_paths', [True, False])
@pytest.mark.parametrize('paths_as_posix', [True, False])
@pytest.mark.parametrize('read_stat', [True, False])
def test_path_tree_human_readable_list_parameters(relative_paths, paths_as_posix, read_stat):
    pt = PathTree(
        root_dir='/not/relevant/for/this/test',
        relative_paths=relative_paths,
        paths_as_posix=paths_as_posix,
        read_stat=read_stat,
    )
    assert isinstance(pt.human_readable_list(), list)


@pytest.mark.parametrize('relative_paths', [True, False])
@pytest.mark.parametrize('paths_as_posix', [True, False])
def test_path_tree_with_stat(shared_datadir, relative_paths, paths_as_posix):
    pt = PathTree(
        root_dir=shared_datadir,
        relative_paths=relative_paths,
        paths_as_posix=paths_as_posix,
        read_stat=True,
    )
    d = pt.dict()
    assert d.get('stat') is not None
    assert d.get('children')[0].get('stat') is not None


@pytest.mark.parametrize('relative_paths', [True, False])
@pytest.mark.parametrize('paths_as_posix', [True, False])
@pytest.mark.parametrize('read_stat', [True, False])
def test_path_tree_list_entry(shared_datadir, relative_paths, paths_as_posix, read_stat):
    pt = PathTree(
        root_dir=shared_datadir,
        relative_paths=relative_paths,
        paths_as_posix=paths_as_posix,
        read_stat=read_stat,
    )
    assert isinstance(pt.tree(), ListEntry)
