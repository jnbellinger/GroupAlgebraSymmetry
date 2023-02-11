''' class to manage a square Matrix of Fractions. I don't care about determinants '''
import sys
import copy
from Builder import Fraction as F
from Builder import Name as N

class Matrix:
    ''' Class to hold a square array of Fractions '''
    def __init__(self, size):
        ''' Create a zero-filled matrix of size size x size '''
        if not isinstance(size, int):
            print('Matrix:__init__ wants a postive *integer* size')
            sys.exit(190)
        if size <= 0:
            print('Matrix:__init__ wants a *postive* integer size')
            sys.exit(191)
        # Build it from lists
        self.size = size
        self.array = []
        temparray = []
        for i in range(size):
            temparray.append(F.Fraction(0, 1))
        for i in range(size):
            self.array.append(copy.deepcopy(temparray))
        # That's all
    #
    def set(self, name, fraction):
        ''' The argument order matters.  Reset the value in the given location '''
        if not isinstance(name, N.Name) or not isinstance(fraction, F.Fraction):
            print('Matrix:set wants a Name and a Fraction')
            sys.exit(192)
        # Assume nobody has monkeyed with the contents of Name!
        if name.size != self.size:
            print('Matrix:set was given an incompatible Name, sizes do not match')
            sys.exit(193)
        # Do a deep copy for safety's sake--otherwise I'll be chasing obscure bugs
        self.array[name.row][name.column] = copy.deepcopy(fraction)
    #
    def get(self, row, column):
        ''' Return the Fraction at this location '''
        if not isinstance(row, int) or not isinstance(column, int):
            print('Matrix:get needs to index its row and column by ints')
            sys.exit(194)
        if row < 0 or column < 0 or row >= self.size or column >= self.size:
            print('Matrix:get row or column is out of bounds', row, column)
            sys.exit(195)
        return self.array[row][column]
    #
    def add(self, other, fraction=F.Fraction(1, 1) ):
        ''' Add two Matrix together, with optional Fraction multiplying the second '''
        if not isinstance(other, Matrix):
            print('Matrix:add cannot add anything but another Matrix')
            sys.exit(196)
        if self.size != other.size:
            print('Matrix:add cannot add Matrix of a different size')
            sys.exit(197)
        if not isinstance(fraction, F.Fraction):
            print('Matrix:add wants the second argument to be a Fraction')
            sys.exit(198)
        # Sane
        newmat = Matrix(self.size)  # Always pretending I have infinite memory
        for row in range(self.size):
            for column in range(self.size):
                newf = self.array[row][column].add(fraction.multiply(other.array[row][column]))
                # Note that add and mutiply are non-mutating operations; they return Fraction
                newmat.array[row][column] = newf
        return newmat
    #
    # Multiply two, returning a new one
    def multiply(self, other):
        ''' Return the result of multiplying this by the other, whether this is Fraction
        or Matrix '''
        if not isinstance(other, F.Fraction) and not isinstance(other, Matrix):
            print('Matrix:multiply wants either a Fraction or a Matrix')
            sys.exit(199)
        if isinstance(other, F.Fraction):
            newmat = Matrix(self.size)
            for row in range(self.size):
                for column in range(self.size):
                    newmat.array[row][column] = self.array[row][column].multiply(other)
            return newmat
        #
        if self.size != other.size:
            print('Matrix:multiply wants the other Matrix to be the same size')
            sys.exit(290)
        newmat = Matrix(self.size)
        for row in range(self.size):
            for column in range(self.size):
                for k in range(self.size):
                    newmat.array[row][column].muteadd(self.array[row][k].multiply(other.array[k][column]))
        return newmat
    #
    def __str__(self):
        ''' Turn this into a string '''
        basestr = ''
        for row in range(self.size):
            for column in range(self.size):
                basestr = basestr + str(self.array[row][column]) + ' '
            if row != self.size - 1:
                basestr = basestr + '\n'
        return basestr
    def __repr__(self):
        return self.__str__()
    #
    def __eq__(self, other):
        ''' Are these two Matrix equal? '''
        if not isinstance(other, Matrix):
            print('Matrix:__eq wants another Matrix')
            sys.exit(291)
        if self.size != other.size:
            print('Matrix:__eq cannot compare Matrix of different size')
            sys.exit(292)
        for row in range(self.size):
            for column in range(self.size):
                if self.array[row][column] != other.array[row][column]:
                    return False
        return True
