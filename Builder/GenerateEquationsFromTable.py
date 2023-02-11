''' routine to, given a Table, return a ListOfEquations '''
import sys
from Builder import Group as G
from Builder import Fraction as F
from Builder import Name as N
from Builder import Element as E
from Builder import Equation as Eq
from Builder import Zero as Z
# pylint: disable=invalid-name

class GenerateEquationsFromTable:
    ''' Generate the list of equations from the Cayley table '''
    def __init__(self, cayleytable):
        ''' Create, save copy of pointer to cayleytable '''
        if not isinstance(cayleytable, G.Table):
            print('GenerateEquationsFromTable was not given a Table')
            sys.exit(350)
        self.groupSize = cayleytable.size()
        self.table = cayleytable
        self.ListOfEquations = None # load this later
        self.zeros = None  # Load this later
    #
    #
    def generateEquationList(self):
        ''' Master generator '''
        # \delta V_{i,tj^{-1}} + \delta V_{j,i^{-1}t} = \delta V_{ij,t}
        # \sum_i \delta V_{i,j} = \sum_j \delta V_{i,j} = 0
        g = []
        ginv = []
        for i in range(self.groupSize):
            g.append(self.table.G(i))
            ginv.append(self.table.inverse(g[-1]))
        #
        self.ListOfEquations = []
        for i in range(self.groupSize):
            for j in range(self.groupSize):
                for t in range(self.groupSize):
                    #  X_{i,tj^{-1}} +  X_{j,i^{-1}t} -  X_{ij,t} = 0
                    a1 = g[i]
                    a2 = self.table.product(g[t], ginv[j])
                    b1 = g[j]
                    b2 = self.table.product(ginv[i], g[t])
                    c1 = self.table.product(g[i], g[j])
                    c2 = g[t]
                    e1 = E.Element(N.Name(a1.index(), a2.index(), self.groupSize), F.Fraction(1, 1))
                    e2 = E.Element(N.Name(b1.index(), b2.index(), self.groupSize), F.Fraction(1, 1))
                    e3 = E.Element(N.Name(c1.index(), c2.index(), self.groupSize), F.Fraction(-1, 1))
                    neweq = Eq.Equation([e1, e2, e3])
                    self.ListOfEquations.append(neweq)
        #
        # Some things are known to be zero already
        znames = []
        for i in range(self.groupSize):
            znames.append(N.Name(0, i, self.groupSize))
            znames.append(N.Name(i, 0, self.groupSize))
        self.zeros = Z.Zero(znames)
    #
    def GiveEquations(self):
        ''' Return the ListOfEquations:  OK if these are modified '''
        return self.ListOfEquations
    #
    def GiveSize(self):
        ''' Return the group size; should not be modified '''
        return self.groupSize
    #
    def GiveZeros(self):
        ''' Return the Zero object:  OK if this is modified '''
        return self.zeros
