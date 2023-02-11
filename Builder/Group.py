''' Individual Group element G  and Cayley table Table '''
import sys
import copy
import math

class Table:
    ''' Cayley table for the group '''
    def __init__(self, ilist):
        ''' Initialize from a list of integers. '''
        # Argument sanity
        if not isinstance(ilist, list):
            print('Table:init wants a *list* of integers')
            sys.exit(200)
        for i in ilist:
            if not isinstance(i, int):
                print('Table:init wants a list of *integers*')
                sys.exit(201)
        #
        length = len(ilist)
        sqsize = int(math.sqrt(length) + .01)
        if length != sqsize*sqsize:
            print('Table:init size is not a square integer')
            sys.exit(202)
        self._size = sqsize
        #
        array = [0 for i in range(self._size)]
        # initial sanity check
        for i in ilist:
            if i < 0 or i >= self._size:
                print('Table:init array has elements out of bounds', self._size)
                sys.exit(203)
            array[i]+=1
        for i in array:
            if i != array[0]:
                print('Table:init array does not have equal numbers of products')
                sys.exit(204)
        #
        self.itable = copy.deepcopy(ilist)
        #
        # Now do sanity checks on the contents!
        # Does each row or column map ONTO the list?
        r = [*range(self._size)]
        for row in range(self._size):
            trial = []
            for col in range(self._size):
                trial.append(self._product(row, col))
            trial.sort()
            if trial != r:
                print('Table:init array does not map a row onto all values', row)
                sys.exit(205)
        for col in range(self._size):
            trial = []
            for row in range(self._size):
                trial.append(self._product(row, col))
            trial.sort()
            if trial != r:
                print('Table:init array does not map a row onto all values', col)
                sys.exit(216)
        # OK, maps are ONTO.  Now collect inverses
        self._inverses = []
        for row in range(self._size):
            for col in range(self._size):
                if self.itable[row*self._size + col] == 0:
                    self._inverses.append(col)
                    break
        # Now check associativity.  BFI.  There are smarter ways, but for the kind of groups
        # we'll probably be dealing with this won't hurt
        for i in range(self._size):
            for j in range(self._size):
                for k in range(self._size):
                    if self._product(i, self._product(j, k)) != self._product(self._product(i, j), k):
                        print('Table:init array does not define an associative product')
                        sys.exit(217)
        # ok, looks good
    #
    # Equality isn't particularly useful.  Nor anything that mutates the array
    def G(self, i):
        ''' Return a group element object given an integer.  Object, keep things separate and clean '''
        if not isinstance(i, int):
            print('Table:G needs an int')
            sys.exit(208)
        if i < 0 or i >= self._size:
            print('Table:G int is out of bounds', i)
            sys.exit(209)
        return G(i)
    #
    def _product(self, i, j):
        ''' Return the group product of elements indexed i and j.  Internal use '''
        if i < 0 or j < 0 or i >= self._size or j >= self._size:
            print('Table:_product given group elements out of bounds')
            sys.exit(215)
        return self.itable[i*self._size + j]
    def product(self, i, j):
        ''' Return the group product of elements i, j, which are type G '''
        if not isinstance(i, G) or not isinstance(j, G):
            print('Table:product wants group elements G')
            sys.exit(219)
        ii = i.index()
        jj = j.index()
        if not i.inRange(self._size) or not j.inRange(self._size):
            print('Table:product given group elements out of bounds', i, j)
            sys.exit(210)
        return G(self._product(ii, jj))
    #
    def inverse(self, i):
        ''' Return the group element G that is the inverse of the argument '''
        if not isinstance(i, G):
            print('Table:inverse wants a group element G to return an inverse of ')
            sys.exit(211)
        if not i.inRange(self._size):
            print('Table:inverse index is out of range', i)
            sys.exit(212)
        return G(self._inverses[i.index()])
    #
    def __str__(self):
        ''' Turn table into a string '''
        base = ''
        for row in range(self._size):
            for col in range(self._size):
                base = base + ' [' + str(self.itable[row*self._size + col]) + ']'
            base = base + '\n'
        return base
    def __repr__(self):
        ''' representation '''
        return self.__str__()
    def size(self):
        ''' How big is the group? '''
        return self._size



###############################

class G:
    ''' Class to make sure integers do not get mixed up with group elements,
    even though they are counted with integers 0 .. N-1 '''
    def __init__(self, other):
        ''' Initialize from an integer index to the group element '''
        if not isinstance(other, int):
            print('G:init wants an int (index)')
            sys.exit(206)
        # Assume the range has already been checked!
        self._index = other
    #
    def index(self):
        ''' Return the internal index 0 .. N-1 '''
        return self._index
    #
    def __eq__(self, other):
        ''' Check if these are equal.  Only bother with the index '''
        if not isinstance(other, G):
            print('G:== wants to compare with a G')
            sys.exit(207)
        return self._index == other.index()
    #
    def inRange(self, other):
        ''' Is this in range? '''
        if not isinstance(other, int):
            print('G:inRange wants an integer')
            sys.exit(213)
        return (self._index >= 0 and self._index < other)
    #
    def __str__(self):
        ''' convert to string '''
        return '[' + str(self._index) + ']'
    def __repr__(self):
        return self.__str__()
