''' Test the GenerateMatrix class '''
import os
import sys
import copy
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import unittest
from unittest.mock import patch
from Builder import GenerateEquationsFromTable
from Builder import SolveEquations
from Builder import Group as G
from Builder import Name as N
from Builder import Matrix as M
from Builder import Fraction as F
from Builder import Element as E
from Builder import Equation as Eq
from Builder import Zero as Z
from Builder import Chain
from Builder import GenerateMatrix

#Table

class test_generatematrix(unittest.TestCase):
    
    def test_generatematrix_6group_getsums(self):
        table = G.Table([ 0, 1, 2, 3, 4, 5, 1, 2, 0, 4, 5, 3, 2, 0, 1, 5, 3, 4, 3, 5, 4, 0, 2, 1, 4, 3, 5, 1, 0, 2, 5, 4, 3, 2, 1, 0])
        maker = GenerateEquationsFromTable.GenerateEquationsFromTable(table)
        maker.generateEquationList()
        solver = SolveEquations.SolveEquations(maker.GiveSize(), maker.GiveEquations(), maker.GiveZeros())
        biglist, zerolist, keylist, answer, answer2 = solver.ProcessEquationList()
        generator = GenerateMatrix.GenerateMatrix(solver.GiveEquivalences(), solver.GiveChains())
        self.assertEqual(len(generator.FreeChainPointer), 3, msg='Should have 3 Chains left')
    def test_generatematrix_6group_getsums_commut(self):
        table = G.Table([ 0, 1, 2, 3, 4, 5, 1, 2, 0, 4, 5, 3, 2, 0, 1, 5, 3, 4, 3, 5, 4, 0, 2, 1, 4, 3, 5, 1, 0, 2, 5, 4, 3, 2, 1, 0])
        maker = GenerateEquationsFromTable.GenerateEquationsFromTable(table)
        maker.generateEquationList()
        solver = SolveEquations.SolveEquations(maker.GiveSize(), maker.GiveEquations(), maker.GiveZeros())
        biglist, zerolist, keylist, answer, answer2 = solver.ProcessEquationList()
        generator = GenerateMatrix.GenerateMatrix(solver.GiveEquivalences(), solver.GiveChains())
        generator.CommuteAndSolve()
    def test_generatematrix_badargs_list1(self):
        table = G.Table([ 0, 1, 2, 3, 4, 5, 1, 2, 0, 4, 5, 3, 2, 0, 1, 5, 3, 4, 3, 5, 4, 0, 2, 1, 4, 3, 5, 1, 0, 2, 5, 4, 3, 2, 1, 0])
        maker = GenerateEquationsFromTable.GenerateEquationsFromTable(table)
        maker.generateEquationList()
        solver = SolveEquations.SolveEquations(maker.GiveSize(), maker.GiveEquations(), maker.GiveZeros())
        with self.assertRaises(SystemExit) as cm:
            generator = GenerateMatrix.GenerateMatrix('equivalences', solver.GiveChains())
        self.assertEqual(cm.exception.code, 320, 'First argument is bad')
    def test_generatematrix_badargs_list2(self):
        table = G.Table([ 0, 1, 2, 3, 4, 5, 1, 2, 0, 4, 5, 3, 2, 0, 1, 5, 3, 4, 3, 5, 4, 0, 2, 1, 4, 3, 5, 1, 0, 2, 5, 4, 3, 2, 1, 0])
        maker = GenerateEquationsFromTable.GenerateEquationsFromTable(table)
        maker.generateEquationList()
        solver = SolveEquations.SolveEquations(maker.GiveSize(), maker.GiveEquations(), maker.GiveZeros())
        with self.assertRaises(SystemExit) as cm:
            generator = GenerateMatrix.GenerateMatrix(solver.GiveEquivalences(), 'chains')
        self.assertEqual(cm.exception.code, 320, 'Second argument is bad')
    def test_generatematrix_badargs_listnotequiv(self):
        table = G.Table([ 0, 1, 2, 3, 4, 5, 1, 2, 0, 4, 5, 3, 2, 0, 1, 5, 3, 4, 3, 5, 4, 0, 2, 1, 4, 3, 5, 1, 0, 2, 5, 4, 3, 2, 1, 0])
        maker = GenerateEquationsFromTable.GenerateEquationsFromTable(table)
        maker.generateEquationList()
        solver = SolveEquations.SolveEquations(maker.GiveSize(), maker.GiveEquations(), maker.GiveZeros())
        with self.assertRaises(SystemExit) as cm:
            generator = GenerateMatrix.GenerateMatrix([5, 3, 3], solver.GiveChains())
        self.assertEqual(cm.exception.code, 321, 'First list is not of Equivalences')
    def test_generatematrix_badargs_listnotchain(self):
        #table = G.Table([0, 1, 2,  1, 2, 0,  2, 0, 1])
        table = G.Table([ 0, 1, 2, 3, 4, 5, 1, 2, 0, 4, 5, 3, 2, 0, 1, 5, 3, 4, 3, 5, 4, 0, 2, 1, 4, 3, 5, 1, 0, 2, 5, 4, 3, 2, 1, 0])
        maker = GenerateEquationsFromTable.GenerateEquationsFromTable(table)
        maker.generateEquationList()
        solver = SolveEquations.SolveEquations(maker.GiveSize(), maker.GiveEquations(), maker.GiveZeros())
        solver.ProcessEquationList()
        with self.assertRaises(SystemExit) as cm:
            generator = GenerateMatrix.GenerateMatrix(solver.GiveEquivalences(), [5, 3, 3])
        self.assertEqual(cm.exception.code, 322, 'Second list is not of Chains')
    #
    def test_generatematrix_parse_01(self):
        table = G.Table([ 0, 1, 2, 3, 4, 5, 1, 2, 0, 4, 5, 3, 2, 0, 1, 5, 3, 4, 3, 5, 4, 0, 2, 1, 4, 3, 5, 1, 0, 2, 5, 4, 3, 2, 1, 0])
        maker = GenerateEquationsFromTable.GenerateEquationsFromTable(table)
        maker.generateEquationList()
        solver = SolveEquations.SolveEquations(maker.GiveSize(), maker.GiveEquations(), maker.GiveZeros())
        solver.ProcessEquationList()
        gg = GenerateMatrix.GenerateMatrix(solver.GiveEquivalences(), solver.GiveChains())
        gg.CommuteAndSolve()
        acontent = str(gg.commuteSolutionContents()[2])
        trial = (acontent == '[C1, C2] = (-1)C1 + (2)C0') or (acontent == '[C1, C2] = (2)C0 + (-1)C1')
        self.assertTrue(trial, msg='Expect 2 terms')
        #self.assertEqual(str(gg.commuteSolutionContents()[2]), '[C1, C2] = (-1)C1 + (2)C0', msg='Expect 2 terms')
    def test_generatematrix_parse_bad_02(self):
        with self.assertRaises(SystemExit) as cm:
            gg = GenerateMatrix.GenerateMatrix([], [])
        self.assertEqual(cm.exception.code, 320, 'Should bail on empty lists')
