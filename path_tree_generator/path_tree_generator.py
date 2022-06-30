"""
Path Tree Generator
"""
import pathlib

from .models.list_entries import ListEntry, ListEntryType


class PathTree:
    def __init__(
            self,
            root_dir: str | pathlib.Path,
            relative_paths=True,
            wrap_with_root_dir=True,
    ):
        self.root_dir = root_dir
        if isinstance(root_dir, str):
            self.root_dir = pathlib.Path(root_dir)

        self._generator = _PathTreeGenerator(root_dir=self.root_dir)
        self._relative_paths = relative_paths
        self._wrap_with_root_dir = wrap_with_root_dir

    def dict(self):
        return self._generator.get_tree(
            relative_paths=self._relative_paths,
            wrap_with_root_dir=self._wrap_with_root_dir,
        ).dict()

    def json(self):
        tree = self._generator.get_tree(self._relative_paths, self._wrap_with_root_dir)
        return tree.json()

    def human_readable(self):
        return self._generator.get_tree_human_readable_list(
            relative_paths=self._relative_paths,
            root_dir_name_only=True,
        )


class _PathTreeGenerator:

    HR_DIR_PREFIX = "["
    HR_DIR_SUFFIX = "]"
    PIPE = "│"
    ELBOW = "└──"
    TEE = "├──"
    PIPE_PREFIX = "│   "
    SPACE_PREFIX = "    "

    def __init__(self, root_dir: pathlib.Path):
        self._root_dir = root_dir
        self._tree_list: list[ListEntry] = []
        self._tree_dict: dict[ListEntry] = {}
        self._tree_built = False
        self._hr_tree_list: list[str] = []
        self._hr_tree_built = False

    def get_tree(self, relative_paths=True, wrap_with_root_dir=True) -> ListEntry | list[ListEntry]:
        self._build_tree(self._root_dir, relative_paths=relative_paths)
        if wrap_with_root_dir:
            if relative_paths:
                path = self._root_dir.relative_to(self._root_dir)
            else:
                path = self._root_dir

            return ListEntry(
                entry_type=ListEntryType.dir,
                name=self._root_dir.name,
                path=path,
                children=self._tree_list,
            )
        return self._tree_list

    def _build_tree(self, path: pathlib.Path, relative_paths=True):
        if self._tree_built:
            return
        if relative_paths:
            entries = self._prepare_entries(
                path.relative_to(path.parent)
            )
        else:
            entries = self._prepare_entries(path)

        if entries:
            self._tree_list = entries

        self._tree_built = True

    def _prepare_entries(self, path: pathlib.Path) -> list[ListEntry] | None:
        entries: list[ListEntry] = []
        if path.is_dir():
            for entry in path.iterdir():
                if entry.is_dir():
                    entries.append(
                        self._get_dir_entry(entry)
                    )
                if entry.is_file():
                    entries.append(
                        self._get_file_entry(entry)
                    )
        if entries:
            return entries

    def _get_dir_entry(self, path: pathlib.Path):
        return ListEntry(
            entry_type=ListEntryType.dir,
            name=path.name,
            path=path,
            children=self._prepare_entries(path),
        )

    def _get_file_entry(self, path: pathlib.Path):
        return ListEntry(
            entry_type=ListEntryType.file,
            name=path.name,
            path=path,
        )

    def get_tree_human_readable_list(self, relative_paths=True, root_dir_name_only=True) -> list[str]:
        self._build_tree(self._root_dir, relative_paths=relative_paths)
        self._build_hr_tree(root_dir_name_only=root_dir_name_only)
        return self._hr_tree_list

    def _build_hr_tree(self, root_dir_name_only=True):
        if self._hr_tree_built:
            return
        self._hr_tree_head(root_dir_name_only=root_dir_name_only)
        self._hr_tree_body(self._tree_list)
        self._hr_tree_built = True

    def _hr_tree_head(self, root_dir_name_only=True):
        tree_head = self._root_dir.name if root_dir_name_only else self._root_dir
        self._hr_tree_list.append(
            f'{self.HR_DIR_PREFIX}{tree_head}{self.HR_DIR_SUFFIX}'
        )
        # self._hr_tree_list.append(self.PIPE)  # add additional space

    def _hr_tree_body(self, children, prefix=''):
        # entries = self._hr_prepare_entries(children)
        entries_count = len(children)
        for index, entry in enumerate(children):
            entry: ListEntry
            connector = self.ELBOW if index == entries_count - 1 else self.TEE
            if entry.entry_type == ListEntryType.dir:
                self._hr_add_directory(
                    entry, index, entries_count, prefix, connector
                )
            else:
                self._hr_add_file(entry, prefix, connector)

    def _hr_add_directory(
        self, entry: ListEntry, index, entries_count, prefix, connector
    ):
        self._hr_tree_list.append(
            f'{prefix}{connector} {self.HR_DIR_PREFIX}{entry.name}{self.HR_DIR_SUFFIX}'
        )

        if index != entries_count - 1:
            prefix += self.PIPE_PREFIX
        else:
            prefix += self.SPACE_PREFIX

        if entry.children is not None:
            self._hr_tree_body(
                children=entry.children,
                prefix=prefix,
            )
        # self._hr_tree_list.append(prefix.rstrip())

    def _hr_add_file(self, file, prefix, connector):
        self._hr_tree_list.append(f'{prefix}{connector} {file.name}')
