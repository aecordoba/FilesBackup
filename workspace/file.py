# file.py
"""File class definition."""

class File:
    """Hold files data."""
    def __init__(self, filename, size, modiffication_time):
        self._filename = filename
        self._size = size
        self._modiffication_time = modiffication_time

    @property
    def filename(self):
        return self._filename

    @property
    def size(self):
        return self._size

    @property
    def modiffication_time(self):
        return self._modiffication_time
    
    def __repr__(self):
        return ('File: ' + f'{self.filename}\n' +
        f'\tsize: {self.size}\n' +
        f'\tlast modiffication: {self.modiffication_time}')

    def __str__(self):
        return ('File: ' + f'{self.filename} (size: {self.size}, last modiffication: {self.modiffication_time})')