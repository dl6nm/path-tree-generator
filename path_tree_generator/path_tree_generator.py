"""
Path Tree Generator
"""
import pathlib

from .models.list_entries import ListEntry, ListEntryType


class PathTree:
    def __init__(self, root_dir: str | pathlib.Path):
        if isinstance(root_dir, str):
            root_dir = pathlib.Path(root_dir)
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
            self._build_tree(self._root_dir)
        return self._tree_list

    def _build_tree(self, path: pathlib.Path, relative_paths=True):
        relative_to = path if relative_paths else None
        self._tree_list = self._prepare_entries(path, relative_to.parent)
        self._tree_built = True

    def _prepare_entries(self, path: pathlib.Path, relative_to=None) -> list[ListEntry]:
        entries: list[ListEntry] = []
        if path.is_dir():
            for entry in path.iterdir():
                if entry.is_dir():
                    entries.append(
                        self._get_dir_entry(entry, relative_to)
                    )
                if entry.is_file():
                    entries.append(
                        self._get_file_entry(entry, relative_to)
                    )
        return entries

    def _get_dir_entry(self, path: pathlib.Path, relative_to=None):
        if relative_to not in [None, '']:
            path = path.relative_to(relative_to)
        return ListEntry(
            entry_type=ListEntryType.dir,
            name=path.name,
            path=path,
            children=self._build_tree(path),
        )

    def _get_file_entry(self, path: pathlib.Path, relative_to=None):
        if relative_to not in [None, '']:
            path = path.relative_to(relative_to)
        return ListEntry(
            entry_type=ListEntryType.file,
            name=path.name,
            path=path,
        )
