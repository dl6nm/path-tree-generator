import pathlib

from enum import Enum
from typing import Optional, Union

from pydantic import BaseModel


class ListEntryStat(BaseModel):
    size: Optional[int]  # total size, in bytes
    atime: Optional[float]  # time of last access
    ctime: Optional[float]  # time of last change
    mtime: Optional[float]  # time of last modification
    gid: Optional[int]  # group ID of owner
    mode: Optional[int]  # protection bits
    uid: Optional[int]  # user ID of owner


class ListEntryType(Enum):
    dir = 'dir'
    file = 'file'
    link = 'link'


class ListEntry(BaseModel):
    class Config:
        smart_union = True

    entry_type: ListEntryType
    name: str
    path: Union[str, pathlib.Path]
    stat: Optional[ListEntryStat]
    children: Optional[list['ListEntry']]
