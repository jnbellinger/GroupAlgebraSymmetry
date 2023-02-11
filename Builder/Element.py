import sys
import math
from Builder import Name
from Builder import Fraction

''' Name and Fraction.  Fraction part is mutable.  '''

class Element:
    def __init__(self, name, fraction):
        if not isinstance(name, Name.Name) or not isinstance(fraction, Fraction.Fraction):
            print('Element needs a Name and a Fraction', type(name), type(fraction))
            sys.exit(51)
        self.name = name
        self.fraction = fraction
    #
    def __str__(self):
        return self.name.__str__() + self.fraction.__str__()
    def __repr__(self):
        return self.__str__()
    #
    # Methods
    def isZero(self):
        return (self.fraction.numerator == 0)
    #
    def __eq__(self, other):
        if not isinstance(other, Element):
            print('Element __eq__ needs an Element')
            sys.exit(53)
        return (self.name == other.name and self.fraction == other.fraction)
    #
    #   Mutations of itself:
    # mutemultiply (by an integer, a pair of integers, or a Fraction) CHECK
    # muteadd (a pair of integers or a Fraction)  CHECK
    # mutereplace  (a pair of integers or a Fraction)  CHECK
    # muteforceZero CHECK
    # muteinvert CHECK
    #   Returns a different Element:
    # multiply (by an integer, a pair of integers, or a Fraction)
    # add (a pair of integers or a Fraction)
    # invert
    #
    def mutemultiply(self, other):
        if isinstance(other, Fraction.Fraction):
            self.fraction.mutemultiply(other)
        elif isinstance(other, Element):
            if self.name != other.name:
                print('Elements of different types cannot be multiplied', other)
                sys.exit(54)
            self.fraction.mutemultiply(other.fraction)
        elif isinstance(other, int):
            self.fraction.mutemultiply(other)
        else:
            print('Element does not know how to multiply', other)
            sys.exit(56)
    #
    def muteadd(self, other):
        if isinstance(other, Fraction.Fraction):
            self.fraction.muteadd(other)
        elif isinstance(other, Element):
            if self.name != other.name:
                print('Elements of different types cannot be added', other)
                sys.exit(58)
            self.fraction.muteadd(other.fraction)
        else:
            print('Element does not know how to add this', other)
            sys.exit(57)
    #
    def mutereplace(self, other):
        if not isinstance(other, Fraction.Fraction):
            print('Elements wants to replace its Fraction with a Fraction', other)
            sys.exit(54)
        self.fraction = other
    # Note that I don't see the point in replace Elements
    #
    def muteforceZero(self):
        self.fraction.numerator = 0
    #
    def muteinvert(self):
        self.fraction.muteinvert()
    #
    def multiply(self, other):
        if isinstance(other, Fraction.Fraction):
            return Element(self.name, self.fraction.multiply(other))
        elif isinstance(other, Element):
            if self.name != other.name:
                print('Element different types cannot be multiplied', other)
                sys.exit(55)
            return Element(self.name, self.fraction.multiply(other.fraction))
        elif isinstance(other, int):
            return Element(self.name, self.fraction.multiply(other))
        else:
            print('Element wants to be multiplied with a Fraction', other)
            sys.exit(54)
    #
    def add(self, other):
        if isinstance(other, Fraction.Fraction):
            return Element(self.name, self.fraction.add(other))
        elif isinstance(other, Element):
            if self.name != other.name:
                print('Element different types cannot be added', other)
                sys.exit(55)
            return Element(self.name, self.fraction.add(other.fraction))
        else:
            print('Element wants to be added with a Fraction or an Element', other)
            sys.exit(54)
    #
    def invert(self):
        return Element(self.name, self.fraction.invert())
    #
    def __hash__(self):
        return hash((self.name, self.fraction))
    #
    def operatorVersion(self):
        ''' This is only for Names of the type (0, n, N), which are used for
        equations involving operators (matrices) 
        It assumes that we have already checked for n<N '''
        if self.name.row != 0:
            print('Element has a Name inconsistent with an Operator', self.name)
            sys.exit(56)
        order = int(math.log10(self.name.size) + .0001) + 1
        return str(self.fraction) + 'C' + str(self.name.column).zfill(order)
