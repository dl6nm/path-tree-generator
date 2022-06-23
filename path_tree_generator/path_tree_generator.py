"""
Path Tree Generator
"""


class PathTree:
    def __init__(self, root_dir):
        self._generator = _PathTreeGenerator(root_dir=root_dir)

    def dict(self):
        return {
            'foo': 'bar'
        }

    def human_readable(self):
        return """I'm a human readable path..."""


class _PathTreeGenerator:
    def __init__(self, root_dir):
        pass
