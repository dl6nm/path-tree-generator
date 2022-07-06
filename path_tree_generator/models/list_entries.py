import pathlib

from enum import Enum
from typing import Optional, Union
from os import stat_result

from pydantic import BaseModel


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
    size_bytes: Optional[int]
    stat: Optional[stat_result]
    children: Optional[list['ListEntry']]
