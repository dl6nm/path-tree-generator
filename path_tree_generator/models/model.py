import pathlib

from enum import Enum
from typing import Optional

from pydantic import BaseModel


class ListEntryType(Enum):
    dir = 'dir'
    file = 'file'
    link = 'link'


class ListEntry(BaseModel):
    type: ListEntryType
    name: str
    path: pathlib.Path
    sizeBytes: int
    children: Optional[list['ListEntry']]
    # @todo: add permissions and attributes like mod, own, grp, ...
