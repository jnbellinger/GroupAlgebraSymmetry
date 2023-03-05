''' routine to, given a Table, return a ListOfEquations '''
import sys
from Builder import Group as G
from Builder import Fraction as F
from Builder import Name as N
from Builder import Element as E
from Builder import Equation as Eq
from Builder import Zero as Z
from Builder import Matrix as M
# pylint: disable=invalid-name

class CheckMatrixWithTable:
    ''' Given a list of Matrix and a Cayley table, see if all of
    the Matrix satisfy the differential formula '''
    def __init__(self, cayleytable, listofmatrix):
        ''' Create, save copy of pointer to cayleytable '''
        # Sanity check
        if not isinstance(cayleytable, G.Table):
            print('CheckMatrixWithTable was not given a Table')
            sys.exit(990)
        self.groupSize = cayleytable.size()
        if not isinstance(listofmatrix, list):
            print('CheckMatrixWithTable was not given a list')
            sys.exit(991)
        for x in listofmatrix:
            if not isinstance(x, M.Matrix):
                print('CheckMatrixWithTable was not given a list of Matrix')
                sys.exit(992)
            if self.groupSize != x.size:
                print('CheckMatrixWithTable was given a list of Matrix with incompatible size')
                sys.exit(993)
        # These are pointers to elsewhere.  I do not intend to
        # modify the originals.
        self.table = cayleytable
        self.matrixlist = listofmatrix
    #
    def DriveChecks(self):
        ''' Run the checks for each matrix in turn.  I split out the
        detailed examination so that I can re-use this to check other
        unrelated matrices if I choose '''
        for matrix in self.matrixlist:
            if not self.CheckFormula(matrix):
                return False
        return True
    #
    #
    def CheckFormula(self, matrix):
        ''' This uses the fundamental formula to check the given matrix '''
        # \delta V_{i,tj^{-1}} + \delta V_{j,i^{-1}t} = \delta V_{ij,t}
        # \sum_i \delta V_{i,j} = \sum_j \delta V_{i,j} = 0
        g = []
        ginv = []
        for i in range(self.groupSize):
            g.append(self.table.G(i))
            ginv.append(self.table.inverse(g[-1]))
        #
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
                    e1 = matrix.get(a1.index(), a2.index())
                    e2 = matrix.get(b1.index(), b2.index())
                    e3 = matrix.get(c1.index(), c2.index())
                    e11 = e1.add(e2.add(e3.multiply(F.Fraction(-1, 1))))
                    if not e11.isZero():
                        return False
        return True
    #
