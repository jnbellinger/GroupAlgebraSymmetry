import sys

''' Two integers.  Mutable.  Usual fraction rules  NOTE: Not in reduced form '''

class Fraction:
    def __init__(self, numerator: int, denominator: int):
        if not isinstance(numerator, int) or not isinstance(denominator, int):
            print('Fraction needs two ints', numerator, denominator)
            sys.exit(11)
        if denominator == 0:
            print('Fraction cannot have 0 denominator')
            sys.exit(12)
        self.numerator = numerator
        self.denominator = denominator
    #
    def __str__(self):
        # massage to look nicer
        if self.denominator < 0:
            self.numerator = self.numerator * -1
            self.denominator = self.denominator * -1
        # Simplify some common fractions
        if self.numerator%2 == 0 and self.denominator%2 == 0:
            self.numerator = int(self.numerator/2)
            self.denominator = int(self.denominator/2)
        if self.numerator == 0:
            return '(0)'
        elif self.numerator == self.denominator:
            return '(1)'
        elif self.numerator == -self.denominator:
            return '(-1)'
        elif self.denominator == 1:
            return '(' + str(self.numerator) + ')'
        return '(' + str(self.numerator) + '/' + str(self.denominator) + ')'
    def __repr__(self):
        return self.__str__()
    #
    # Methods
    def isZero(self):
        return (self.numerator == 0)
    #
    def __eq__(self, other):
        if not isinstance(other, Fraction):
            return False
        return (self.numerator * other.denominator == self.denominator * other.numerator)
    #
    #   Mutations of itself:
    # mutemultiply (by an integer, a pair of integers, or a Fraction) NO:  only do another Fraction
    # muteadd (a pair of integers or a Fraction)  CHECK
    # mutereplace  (a pair of integers or a Fraction)  CHECK
    # muteforceZero CHECK
    # muteinvert CHECK
    #   Returns a different Fraction:
    # multiply (by an integer, a pair of integers, or a Fraction)
    # add (a pair of integers or a Fraction)
    # invert
    #
    #
    #def mutemultiply(self, numerator: int, denominator: int):
    #    if not isinstance(numerator, int) or not isinstance(denominator, int):
    #        print('Fraction wants to be multiplied by an int, pair of ints, or Fraction', numerator, denominator)
    #        sys.exit(14)
    #    if denominator == 0:
    #        print('Fraction cannot be scaled by 1/0', numerator, denominator)
    #        sys.exit(15)
    #    self.numerator = self.numerator * numerator
    #    self.denominator = self.denominator * denominator
    #
    def mutemultiply(self, other):
        if isinstance(other, Fraction):
            self.numerator = self.numerator * other.numerator
            self.denominator = self.denominator * other.denominator
        elif isinstance(other, int):
            self.numerator = self.numerator * other
        else:
            print('Fraction wants to be multiplied by an int, pair of ints, or Fraction', other)
            sys.exit(14)
    #
    #def muteadd(self, numerator: int, denominator: int):
    #    if not isinstance(numerator, int) or not isinstance(denominator, int):
    #        print('Fraction wants to add with a pair of ints', numerator, denominator)
    #        sys.exit(14)
    #    if denominator == 0:
    #        print('Fraction cannot be added with 1/0', numerator, denominator)
    #        sys.exit(15)
    #    if self.denominator == denominator:
    #        self.numerator = self.numerator + numerator
    #    else:
    #        self.numerator = self.numerator * denominator + self.denominator * numerator
    #        self.denominator = self.denominator * denominator
    #
    def muteadd(self, other):
        if not isinstance(other, Fraction):
            print('Fraction wants to be added with a Fraction', other)
            sys.exit(14)
        if self.denominator == other.denominator:
            self.numerator = self.numerator + other.numerator
        else:
            self.numerator = self.numerator * other.denominator + self.denominator * other.numerator
            self.denominator = self.denominator * other.denominator
    #
    def mutereplace(self, numerator: int, denominator: int):
        if not isinstance(numerator, int) or not isinstance(denominator, int):
            print('Fraction needs a pair of ints for a replacement', numerator, denominator)
            sys.exit(14)
        if denominator == 0:
            print('Fraction cannot be 1/0', numerator, denominator)
            sys.exit(15)
        self.numerator = numerator
        self.denominator = denominator
    #
    def muteforceZero(self):
        self.numerator = 0
    #
    def muteinvert(self):
        if self.numerator == 0:
            print('Fraction: 0 cannot be inverted')
            sys.exit(16)
        temp = self.numerator
        self.numerator = self.denominator
        self.denominator = temp
    #
    def multiply(self, other):
        if isinstance(other, Fraction):
            return Fraction(self.numerator * other.numerator, self.denominator * other.denominator)
        elif isinstance(other, int):
            return Fraction(self.numerator * other, self.denominator)
        else:
            print('Fraction wants to be multiplied with an int or Fraction', other)
            sys.exit(14)
    #
    #def add(self, numerator: int, denominator: int):
    #    if not isinstance(numerator, int) or not isinstance(denominator, int):
    #        print('Fraction add needs a pair of ints', numerator, denominator)
    #        sys.exit(14)
    #    if denominator == 0:
    #        print('Fraction add does not work with 1/0', numerator, denominator)
    #        sys.exit(15)
    #    if self.denominator == denominator:
    #        return Fraction(self.numerator + numerator, self.denominator)
    #    return Fraction(self.numerator * denominator + self.denominator * numerator, self.denominator * denominator)
    #
    def add(self, other):
        if not isinstance(other, Fraction):
            print('Fraction wants to be added with a Fraction', other)
            sys.exit(14)
        if self.denominator == other.denominator:
            return Fraction(self.numerator + other.numerator, self.denominator)
        return Fraction(self.numerator * other.denominator + self.denominator * other.numerator, self.denominator * other.denominator)
    #
    def invert(self):
        if self.numerator == 0:
            print('Fraction invert fails if = 0')
            sys.exit(16)
        return Fraction(self.denominator, self.numerator)
    #
    def __hash__(self):
        return hash((self.denominator, self.numerator))
