import json

from path_tree_generator import PathTree


def test_path_tree_dict(shared_datadir):
    pt = PathTree(root_dir=shared_datadir)
    data_file = (shared_datadir/'data.json')
    data = json.load(data_file.open(encoding='utf-8'))
    assert pt.dict() == data


def test_path_tree_human_readable(shared_datadir):
    pt = PathTree(root_dir=shared_datadir)
    data_file = (shared_datadir/'data.tree')
    data = data_file.open(encoding='utf-8').read()
    assert pt.human_readable() == data
