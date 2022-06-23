import pathlib

import pytest

from path_tree_generator.models.listing import ListEntry, ListEntryType


def test_list_entry_type():
    assert len(ListEntryType) == 3
    assert ListEntryType.dir.value == 'dir'
    assert ListEntryType.file.value == 'file'
    assert ListEntryType.link.value == 'link'


@pytest.mark.parametrize(
    argnames=['_type', 'name', 'path', 'size_bytes'],
    argvalues=[
        ('dir', 'myDirectory', '/path/to/myDirectory', 0),
        ('dir', 'mySecondDirectory', '/path/to/mySecondDirectory', 0),
        ('file', 'my.log', '/path/to/my.log', 54321),
        ('file', 'my.pdf', '/path/to/my.pdf', 12345),
        ('file', 'mySecond.pdf', '/path/to/mySecond.pdf', None),
    ],
    ids=['myDirectory', 'mySecondDirectory', 'my.log', 'my.pdf', 'mySecond.pdf'],
)
def test_list_entry(_type, name, path, size_bytes):
    le = ListEntry(
        type=_type,
        name=name,
        path=path,
        size_bytes=size_bytes,
    )
    assert type(le.type) == ListEntryType
    assert le.type == ListEntryType(_type)

    assert le.type.name == _type
    assert le.name == name
    assert le.path == pathlib.Path(path)
    assert le.size_bytes == size_bytes


