import pathlib

from enum import Enum
from typing import Optional, Union

from pydantic import BaseModel


class ListEntryStat(BaseModel):
    size: Optional[int]


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
