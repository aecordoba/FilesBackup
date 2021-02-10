# file.py
"""File class definition."""
from pytz import timezone

class File:
    """Hold files data."""
    def __init__(self, filename, size, modification_time):
        self._filename = filename
        self._size = size
        self.modification_time = modification_time

    @property
    def filename(self):
        return self._filename

    @property
    def size(self):
        return self._size

    @property
    def modification_time(self):
        return self._modification_time
    
    @modification_time.setter
    def modification_time(self, modification_time):
        self._modification_time = (modification_time.replace(tzinfo=timezone('UTC'))).astimezone(timezone('America/Argentina/Buenos_Aires'))


    def __repr__(self):
        return ('File: ' + f'{self.filename}\n' +
        f'\tsize: {self.size}\n' +
        f'\tlast modification: {self.modification_time}')

    def __str__(self):
        return ('File: ' + f'{self.filename} (size: {self.size}, last modification: {self.modification_time})')