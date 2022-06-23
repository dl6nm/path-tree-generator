import json

from path_tree_generator import PathTree


def test_path_tree(shared_datadir):
    pt = PathTree(
        root_dir=shared_datadir,
        dir_only=False
    )

    data_file = (shared_datadir/'data.json')
    data = json.load(data_file.open())

    assert pt.dict() == data
