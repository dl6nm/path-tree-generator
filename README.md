# path-tree-generator

Generate tree-like directory listings for humans and output them as `str`, `list[str]`, `dict` or `json`.

    from path_tree_generator import PathTree

    pt = PathTree('/my/path/to/generate')
    print(
        pt.human_readable()
    )

----------------------------------------------------------------------------------------------------

:warning: **This package is in Beta now and still under development!** :warning:

Keep in mind that classes, methods and their signatures 
might change anytime during development till the first official release 1.0.0.

The fist working version is released as **path-tree-generator v0.1.0** 
and contains the most base implementations.

Issues and suggestions can be tracked on [GitHub][issue-tracker].

----------------------------------------------------------------------------------------------------

## Table of Contents

- [Requirements](#requirements)
- [Usage](#usage)
  - [Installation](#installation)
  - [Example](#example)
    - [Human Readable Path Tree](#human-readable-path-tree)
    - [Path Tree `dict`](#path-tree-dict)
    - [Path Tree `json`](#path-tree-json)
- [Support](#support)
- [Contributing](#contributing)
- [License](#license)
- [Changelog](#changelog)
- [Known Issues](#known-issues)

## Requirements

[Python 3.10][python]+

`path-tree-generator` depends on the following packages:

- [Pydantic][pydantic] for data models and validation

## Usage

### Installation

    pip install path-tree-generator

### Examples

All example are using the same instance assigned to the variable `pt` as follows:

    from path_tree_generator import PathTree

    pt = PathTree('/my/path/to/generate')

#### Human Readable Path Tree

Using the `PathTree` instance `pt` from the [Examples](#examples) you can simply use one of the following method:

    pt.human_readable()
    pt.human_readable_list()

Both methods return a tree-like formatted recursive directory listing, either as string or as list of strings. 
Directories are wrapped in square brackets, files aren't.

`pt.human_readable()` returns the directory listing as plain _string_ (`str`) with line breaks.

    [data]
    ├── data-with-stat.json
    ├── data.json
    ├── data.tree
    ├── [myDirectory-1]
    │   ├── myFile.txt
    │   └── [subdirectory]
    │       └── green.gif
    └── [myDirectory-2]
        ├── [subdirectory1]
        │   └── green.gif
        └── [subdirectory2]
            ├── myFile.txt
            └── myFile2.txt

`pt.human_readable_list()` returns the directory listing as _list of strings_ (`list[str]`).
    
    [
        '[data]',
        '├── data-with-stat.json',
        '├── data.json',
        '├── data.tree',
        '├── [myDirectory-1]',
        '│   ├── myFile.txt',
        '│   └── [subdirectory]',
        '│       └── green.gif',
        '└── [myDirectory-2]',
        '    ├── [subdirectory1]',
        '    │   └── green.gif',
        '    └── [subdirectory2]',
        '        ├── myFile.txt',
        '        └── myFile2.txt'
    ]

#### Path Tree `dict`

You can also get a `dict` representation of a retrieved `PathTree`, having some additional information like 
the absolute or relative path of the file or directory and their stats like _size_, _ctime_, _mode_, _uid_ and so on.

Using the `PathTree` instance `pt` from the [Examples](#examples) you can simply use the following method:

    pt.dict()

The `dict` looks like as follows:

    {
        'entry_type': <ListEntryType.dir: 'dir'>, 
        'name': 'data', 
        'path': WindowsPath('.'), 
        'stat': {
            'size': 10834, 
            'atime': 1657198698.2257857, 
            'ctime': 1656593062.5510206, 
            'mtime': 1657177629.2652764, 
            'gid': 0, 
            'mode': 16895, 
            'uid': 0
        }, 
        'children': [
            {
                'entry_type': <ListEntryType.file: 'file'>, 
                'name': 'data-with-stat.json', 
                'path': WindowsPath('data-with-stat.json'), 
                'stat': {
                    'size': 5774, 
                    'atime': 1657198447.0669634, 
                    'ctime': 1657177197.231495, 
                    'mtime': 1657177629.2642767, 
                    'gid': 0, 
                    'mode': 33206, 
                    'uid': 0
                }, 
                'children': None
            },
            [...]
        ]
    }

#### Path Tree `json`

Last but not least you can get a `json` representation, with the same properties like the [Path Tree `dict`](#path-tree-dict).

Using the `PathTree` instance `pt` from the [Examples](#examples) you can simply use the following method:

    pt.json()

The `json` output looks like as follows:

    {
      "entry_type": "dir",
      "name": "data",
      "path": ".",
      "stat": {
        "size": 10834,
        "atime": 1657199261.7484741,
        "ctime": 1656593062.5510206,
        "mtime": 1657177629.2652764,
        "gid": 0,
        "mode": 16895,
        "uid": 0
      },
      "children": [
        {
          "entry_type": "file",
          "name": "data-with-stat.json",
          "path": "data-with-stat.json",
          "stat": {
            "size": 5774,
            "atime": 1657198447.0669634,
            "ctime": 1657177197.231495,
            "mtime": 1657177629.2642767,
            "gid": 0,
            "mode": 33206,
            "uid": 0
          },
          "children": null
        },
        [...]
      ]
    }

## Support

If you're opening [issues][issue-tracker], please mention the version that the issue relates to. 
Please further provide some sample code and also the expected output or behaviour. 

## Contributing

To contribute to this project, fork the repository, make your changes and create a pull request.

## License

This project is licensed under the terms of the MIT license.

## Changelog

All changes are documented on the [GitHub Releases][changelog] page.

## Known Issues

- Python version compatibility < v3.10 is not tested yet



[changelog]: https://github.com/dl6nm/path-tree-generator/releases
[issue-tracker]: https://github.com/dl6nm/path-tree-generator/issues
[pydantic]: https://pydantic-docs.helpmanual.io/
[python]: https://www.python.org/
