import pathlib

import pytest

from path_tree_generator.models.list_entries import ListEntry, ListEntryType


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
        entry_type=_type,
        name=name,
        path=path,
        size_bytes=size_bytes,
    )
    assert type(le.entry_type) == ListEntryType
    assert le.entry_type == ListEntryType(_type)

    assert le.entry_type.name == _type
    assert le.name == name
    assert le.path == pathlib.Path(path)
    assert le.size_bytes == size_bytes


@pytest.mark.parametrize(
    argnames=['children', 'expected_values'],
    argvalues=[
        (
                [
                    ListEntry(
                        entry_type=ListEntryType.dir,
                        name='mySubDir',
                        path=pathlib.Path('/path/to/directoryWithChildren/mySubDir'),
                    ),
                    ListEntry(
                        entry_type=ListEntryType.file,
                        name='mySubDirFile.jpg',
                        path=pathlib.Path('/path/to/directoryWithChildren/mySubDirFile.jpg'),
                        size_bytes=987654,
                    ),
                ],
                [
                    {
                        'entry_type': 'dir',
                        'name': 'mySubDir',
                        'path': '/path/to/directoryWithChildren/mySubDir',
                    },
                    {
                        'entry_type': 'file',
                        'name': 'mySubDirFile.jpg',
                        'path': '/path/to/directoryWithChildren/mySubDirFile.jpg',
                        'size_bytes': 987654,
                    },
                ],
        ),
    ],
    ids=['children'],
)
def test_list_entry_with_children(children: list[ListEntry], expected_values: dict):
    le = ListEntry(
        entry_type=ListEntryType.dir,
        name='directoryWithChildren',
        path=pathlib.Path('/path/to/directoryWithChildren'),
        children=children,
    )
    for idx, child in enumerate(le.children):
        cle_expected = ListEntry(**expected_values[idx])
        assert type(child) == ListEntry
        assert child == cle_expected
