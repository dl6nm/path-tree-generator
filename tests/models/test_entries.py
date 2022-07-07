import os
import pathlib

import pytest

from path_tree_generator.models.list_entries import ListEntry, ListEntryStat, ListEntryType


def test_list_entry_stat():
    stat = pathlib.Path('.').stat()
    les = ListEntryStat(
        size=stat.st_size,
        atime=stat.st_atime,
        ctime=stat.st_ctime,
        mtime=stat.st_mtime,
        gid=stat.st_gid,
        mode=stat.st_mode,
        uid=stat.st_uid,
    )
    assert isinstance(les.size, int)
    assert isinstance(les.atime, float)
    assert isinstance(les.ctime, float)
    assert isinstance(les.mtime, float)
    assert isinstance(les.gid, int)
    assert isinstance(les.mode, int)
    assert isinstance(les.uid, int)


def test_list_entry_type():
    assert len(ListEntryType) == 3
    assert ListEntryType.dir.value == 'dir'
    assert ListEntryType.file.value == 'file'
    assert ListEntryType.link.value == 'link'


@pytest.mark.parametrize(
    argnames=['_type', 'name', 'path', 'size'],
    argvalues=[
        ('dir', 'myDirectory', pathlib.Path('/path/to/myDirectory'), 0),
        ('dir', 'mySecondDirectory', pathlib.Path('/path/to/mySecondDirectory'), 0),
        ('file', 'my.log', pathlib.Path('/path/to/my.log'), 54321),
        ('file', 'my.pdf', pathlib.Path('/path/to/my.pdf'), 12345),
        ('file', 'mySecond.pdf', pathlib.Path('/path/to/mySecond.pdf'), None),
    ],
    ids=['myDirectory', 'mySecondDirectory', 'my.log', 'my.pdf', 'mySecond.pdf'],
)
def test_list_entry(_type, name, path, size):
    le = ListEntry(
        entry_type=_type,
        name=name,
        path=path,
        stat=ListEntryStat(size=size)
    )
    assert type(le.entry_type) == ListEntryType
    assert le.entry_type == ListEntryType(_type)

    assert le.entry_type.name == _type
    assert le.name == name
    assert le.path == pathlib.Path(path)
    assert le.stat.size == size


def test_list_entry_add_stat_result():
    file = pathlib.Path('')
    le = ListEntry(
        entry_type=ListEntryType.dir,
        name=file.name,
        path=file,
    )
    assert le.stat is None
    le.add_stat_result(file.stat())
    assert isinstance(le.stat, ListEntryStat)


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
                        entry_type=ListEntryType.dir,
                        name='mySubDir',
                        path='/path/to/directoryWithChildren/mySubDir',
                    ),
                    ListEntry(
                        entry_type=ListEntryType.file,
                        name='mySubDirFile.jpg',
                        path=pathlib.Path('/path/to/directoryWithChildren/mySubDirFile.jpg'),
                        stat=ListEntryStat(size=987654),
                    ),
                    ListEntry(
                        entry_type=ListEntryType.file,
                        name='mySubDirFile.jpg',
                        path='/path/to/directoryWithChildren/mySubDirFile.jpg',
                        stat=ListEntryStat(size=987654),
                    ),
                ],
                [
                    {
                        'entry_type': 'dir',
                        'name': 'mySubDir',
                        'path': pathlib.Path('/path/to/directoryWithChildren/mySubDir'),
                    },
                    {
                        'entry_type': 'dir',
                        'name': 'mySubDir',
                        'path': '/path/to/directoryWithChildren/mySubDir',
                    },
                    {
                        'entry_type': 'file',
                        'name': 'mySubDirFile.jpg',
                        'path': pathlib.Path('/path/to/directoryWithChildren/mySubDirFile.jpg'),
                        'stat': {
                            'size': 987654,
                        },
                    },
                    {
                        'entry_type': 'file',
                        'name': 'mySubDirFile.jpg',
                        'path': '/path/to/directoryWithChildren/mySubDirFile.jpg',
                        'stat': {
                            'size': 987654,
                        },
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


def test_list_entry_with_stat_type_check():
    file = pathlib.Path('')
    stat = file.stat()
    le = ListEntry(
        entry_type=ListEntryType.dir,
        name=file.name,
        path=file,
        stat=ListEntryStat(
            size=stat.st_size,
            atime=stat.st_atime,
            ctime=stat.st_ctime,
            mtime=stat.st_mtime,
            gid=stat.st_gid,
            mode=stat.st_mode,
            uid=stat.st_uid,
        ),
        children=None,
    )
    assert isinstance(le, ListEntry)
    assert isinstance(le.stat, ListEntryStat)
