from path_tree_generator.models.list_entries import ListEntry
from path_tree_generator.path_tree_generator import _PathTreeGenerator


def test_path_tree_dict(shared_datadir):
    ptg = _PathTreeGenerator(root_dir=shared_datadir)
    assert isinstance(ptg, _PathTreeGenerator)
    assert isinstance(ptg.get_tree(), list)


def test_path_tree_human_readable(shared_datadir):
    ptg = _PathTreeGenerator(root_dir=shared_datadir)
    assert isinstance(ptg, _PathTreeGenerator)
    assert isinstance(ptg.get_tree_human_readable(), list)


def test_path_tree_add_directory():
    pass


def test_path_tree_add_file():
    pass
