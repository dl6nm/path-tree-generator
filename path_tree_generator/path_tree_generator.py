"""
Path Tree Generator
"""
import pathlib

from .models.list_entries import ListEntry, ListEntryType


class PathTree:
    def __init__(self, root_dir):
        self._generator = _PathTreeGenerator(root_dir=root_dir)

    def dict(self):
        return self._generator.get_tree()

    def human_readable(self):
        return """I'm a human readable path..."""


class _PathTreeGenerator:
    def __init__(self, root_dir: pathlib.Path):
        self._root_dir = root_dir
        self._tree_list: list[ListEntry] = []
        self._tree_built = False

    def get_tree(self) -> list[ListEntry]:
        if not self._tree_built:
            self._build_tree()
            self._tree_built = True
        return self._tree_list

    def _build_tree(self):
        if self._root_dir.is_dir():
            # self._root_dir.iterdir()
            children: list[ListEntry] = []
            for entry in self._root_dir.iterdir():
                children = self._add_entry(entry)
            self._tree_list.append(
                self._get_dir_entry(path=self._root_dir, children=children)
            )

        print(self._tree_list)

    def _get_dir_entry(self, path: pathlib.Path, children: list[ListEntry]):
        return ListEntry(
            entry_type=ListEntryType.dir,
            name=path.name,
            path=path,
            children=children
        )

    def _get_file_entry(self, path: pathlib.Path):
        return ListEntry(
            entry_type=ListEntryType.file,
            name=path.name,
            path=path,
        )
