import sys

''' Simple immutable label/name, a combination of row and column '''

class Name:
    def __init__(self, row: int, column: int, size: int):
        if size < 1 or row < 0 or column < 0 or row >= size or column >= size:
            print('Name bad initialization', row, column, size)
            sys.exit(10)
        self.row = row
        self.column = column
        self.size = size
    #
    # Methods
    def __eq__(self, other):
        if not isinstance(other, Name):
            return False
        return (self.row == other.row and self.column == other.column and self.size == other.size)
    def __gt__(self, other):
        if not isinstance(other, Name):
            print('Name > comparison to non-Name')
            sys.exit(11)
        if self.size != other.size:
            print('Name > Name with different base')
            sys.exit(12)
        return (self.row * self.size + self.column > other.row * self.size + other.column)
    def __str__(self):
        return '{' + str(self.row) + '_' + str(self.column) + '}'
    def __repr__(self):
        return self.__str__()
    def __hash__(self):
        return hash((self.row, self.column, self.size))
