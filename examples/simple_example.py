"""
This file is a simple example for using `PathTree`
and print different types of return values (to the terminal).
"""
import pathlib

from path_tree_generator import PathTree

if __name__ == '__main__':
    p = pathlib.Path('../tests/data')  # This works also as plain string and don't have to wrapped with pathlib.Path
    pt = PathTree(
        root_dir=p,
        relative_paths=True,
        paths_as_posix=False,
        read_stat=True,
    )

    print('### human-readable `str` of a directory tree (`PathTree`)')
    print(pt.human_readable())
    print('\n')

    print('### human-readable `list[str]` of a directory tree (`PathTree`)')
    print(pt.human_readable_list())
    print('\n')

    print('### `dict` representation of a directory tree (`PathTree`)')
    print(pt.dict())
    print('\n')

    print('### `json` representation of a directory tree (`PathTree`)')
    print(pt.json())
    print('\n')

    print('### `ListEntry` representation of a directory tree (`PathTree`)')
    print(pt.tree())
    print('\n')
