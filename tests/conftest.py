import json
import pathlib

import pytest


@pytest.fixture(scope='session', autouse=True)
def init_test():
    """ Initialize test setup """
    # Check if 'emptyDirectory' exists in tests/data, otherwise create it
    p = pathlib.Path().absolute()
    if p.parent.name == 'path-tree-generator':
        ed = p / 'data/emptyDirectory'
        if not ed.exists():
            ed.mkdir()


@pytest.fixture()
def example_data(shared_datadir, filename: str):
    """ Get json of a pytest-datadir file located in the test modules "test_{module_name}" folder """
    file = shared_datadir / filename
    if filename.endswith('json'):
        data = json.loads(file.read_bytes())
        if isinstance(data, dict):
            return dict(data)
        elif isinstance(data, list):
            return list(data)
    else:
        data = []
        with open(file, encoding='utf-8') as f:
            for line in f:
                data.append(line.rstrip())
        return data


@pytest.fixture()
def example_data_list(example_data, filename: str):
    return example_data


@pytest.fixture()
def example_data_string(example_data, filename: str):
    return '\n'.join(example_data).strip()
