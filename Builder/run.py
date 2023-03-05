import os
import sys
import copy
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Builder import GenerateEquationsFromTable
from Builder import SolveEquations
from Builder import Group as G
from Builder import Matrix as M
from Builder import Element as E
from Builder import Equation as Eq
from Builder import Zero as Z
from Builder import Chain
from Builder import GenerateMatrix
from Builder import CheckMatrixWithTable

DETAILS = False
# Read table
if len(sys.argv) < 2:
    print('python run.py NameOfFileWithFiniteGroupCayleyTable DETAILS')
    sys.exit(1)
try:
    filehandle = open(str(sys.argv[1]), 'r')
except:
    print('Cannot open', str(sys.argv[1]))
    sys.exit(1)
if len(sys.argv) == 3:  # I don't care what the second argument is; it invokes details
    DETAILS = True
#
tablearray = []
for line in filehandle:
    for word in line.rstrip().split():
        try:
            ix = int(word)
        except:
            print('The word', word, 'is not an integer')
            sys.exit(2)
        tablearray.append(ix)
filehandle.close()
table = G.Table(tablearray)
maker = GenerateEquationsFromTable.GenerateEquationsFromTable(table)
maker.generateEquationList()
if DETAILS:
    for eqn in maker.GiveEquations():
        print('OrigEq=', eqn)
    print('---------------------------')
    print(maker.GiveZeros())
    print('------------------------------------------------------')
solver = SolveEquations.SolveEquations(maker.GiveSize(), maker.GiveEquations(), maker.GiveZeros())
solver.ProcessEquationList()
if DETAILS:
    print('==========================')
    for eqn in solver.GiveEquations():
        print('NewEq=', eqn)
    print('==========================')
    for eqv in solver.GiveEquivalences():
        print('NewEqv=', eqv)
    print('==========================')
    print(solver.GiveZeros())
    print('==========================')
    for ch in solver.GiveChains():
        print('NewCh=', ch)
    print('==========================')
    xxx = solver.countInstancesOfChainInEquations()
    print(xxx)
    print('=====================================================')
matrixgenerator = GenerateMatrix.GenerateMatrix(solver.GiveEquivalences(), solver.GiveChains())
# matrixgenerator.MatrixList holds the list of differential matrices
# I should use the table object with this list to determine which of the Matrix
# objects satisfy the fundamental differential formula.  Just in case!
matrixtester = CheckMatrixWithTable.CheckMatrixWithTable(table, matrixgenerator.MatrixList)
if not matrixtester.DriveChecks():
    print('Some Matrix are not consistent with the fundamental equation')
if DETAILS:
    print('----')
    print(matrixgenerator.EquivChainPointer)
    print('----')
    print(matrixgenerator.FreeChainPointer)
    print('----')
matrixgenerator.CommuteAndSolve()
#
for entry in matrixgenerator.commuteSolutionContents():
    print(entry)
sys.exit(0)
