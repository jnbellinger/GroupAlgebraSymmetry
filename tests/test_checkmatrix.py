''' Test the GenerateMatrix class '''
import os
import sys
import copy
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import unittest
from unittest.mock import patch
from Builder import CheckMatrixWithTable as Ch
from Builder import Group as G
from Builder import Matrix as M
from Builder import Name as N
from Builder import Fraction as F
from Builder import Element as E

class test_checkmatrix(unittest.TestCase):
    #
    def test_6group_badarg_1(self):
        with self.assertRaises(SystemExit) as cm:
            tester = Ch.CheckMatrixWithTable('table', [1,1,2])
        self.assertEqual(cm.exception.code, 990, 'First argument is not a Table')
    #
    def test_6group_badarg_2(self):
        table = G.Table([ 0, 1, 2, 3, 4, 5, 1, 2, 0, 4, 5, 3, 2, 0, 1, 5, 3, 4, 3, 5, 4, 0, 2, 1, 4, 3, 5, 1, 0, 2, 5, 4, 3, 2, 1, 0])
        with self.assertRaises(SystemExit) as cm:
            tester = Ch.CheckMatrixWithTable(table, '[1,1,2]')
        self.assertEqual(cm.exception.code, 991, 'Second argument is not a list')
    def test_6group_badarg_3(self):
        table = G.Table([ 0, 1, 2, 3, 4, 5, 1, 2, 0, 4, 5, 3, 2, 0, 1, 5, 3, 4, 3, 5, 4, 0, 2, 1, 4, 3, 5, 1, 0, 2, 5, 4, 3, 2, 1, 0])
        with self.assertRaises(SystemExit) as cm:
            tester = Ch.CheckMatrixWithTable(table, [1,1,2])
        self.assertEqual(cm.exception.code, 992, 'Second argument is not a list of Matrix')
    def test_6group_badarg_4(self):
        table = G.Table([ 0, 1, 2, 3, 4, 5, 1, 2, 0, 4, 5, 3, 2, 0, 1, 5, 3, 4, 3, 5, 4, 0, 2, 1, 4, 3, 5, 1, 0, 2, 5, 4, 3, 2, 1, 0])
        # Create 2 empty Matrix
        m1 = M.Matrix(5)
        m2 = M.Matrix(5)
        with self.assertRaises(SystemExit) as cm:
            tester = Ch.CheckMatrixWithTable(table, [m1, m2])
        self.assertEqual(cm.exception.code, 993, 'Second argument is not a list of Matrix of the right size')
    #
    def test_6group_ok_matrix(self):
        table = G.Table([ 0, 1, 2, 3, 4, 5, 1, 2, 0, 4, 5, 3, 2, 0, 1, 5, 3, 4, 3, 5, 4, 0, 2, 1, 4, 3, 5, 1, 0, 2, 5, 4, 3, 2, 1, 0])
        # Create 3 empty Matrix
        m1 = M.Matrix(6)
        m2 = M.Matrix(6)
        m3 = M.Matrix(6)
        # Now load them up
        m1.set(N.Name(1, 3, 6), F.Fraction(1, 1))
        m1.set(N.Name(1, 5, 6), F.Fraction(-1, 1))
        m1.set(N.Name(2, 3, 6), F.Fraction(-1, 1))
        m1.set(N.Name(2, 5, 6), F.Fraction(1, 1))
        m1.set(N.Name(3, 1, 6), F.Fraction(1, 1))
        m1.set(N.Name(3, 2, 6), F.Fraction(-1, 1))
        m1.set(N.Name(5, 1, 6), F.Fraction(-1, 1))
        m1.set(N.Name(5, 2, 6), F.Fraction(1, 1))
        #
        m2.set(N.Name(1, 4, 6), F.Fraction(1, 1))
        m2.set(N.Name(1, 5, 6), F.Fraction(-1, 1))
        m2.set(N.Name(2, 4, 6), F.Fraction(-1, 1))
        m2.set(N.Name(2, 5, 6), F.Fraction(1, 1))
        m2.set(N.Name(4, 1, 6), F.Fraction(1, 1))
        m2.set(N.Name(4, 2, 6), F.Fraction(-1, 1))
        m2.set(N.Name(5, 1, 6), F.Fraction(-1, 1))
        m2.set(N.Name(5, 2, 6), F.Fraction(1, 1))
        #
        m3.set(N.Name(3, 4, 6), F.Fraction(-1, 1))
        m3.set(N.Name(3, 5, 6), F.Fraction(1, 1))
        m3.set(N.Name(4, 3, 6), F.Fraction(1, 1))
        m3.set(N.Name(4, 5, 6), F.Fraction(-1, 1))
        m3.set(N.Name(5, 3, 6), F.Fraction(-1, 1))
        m3.set(N.Name(5, 4, 6), F.Fraction(1, 1))
        tester = Ch.CheckMatrixWithTable(table, [m1, m2, m3])
        self.assertTrue(tester.DriveChecks(), msg='Should be fine')
    def test_6group_not_ok_matrix(self):
        table = G.Table([ 0, 1, 2, 3, 4, 5, 1, 2, 0, 4, 5, 3, 2, 0, 1, 5, 3, 4, 3, 5, 4, 0, 2, 1, 4, 3, 5, 1, 0, 2, 5, 4, 3, 2, 1, 0])
        # Create 3 empty Matrix
        m1 = M.Matrix(6)
        m2 = M.Matrix(6)
        m3 = M.Matrix(6)
        # Now load them up
        m1.set(N.Name(1, 3, 6), F.Fraction(1, 1))
        m1.set(N.Name(1, 5, 6), F.Fraction(-1, 1))
        m1.set(N.Name(2, 3, 6), F.Fraction(-1, 1))
        m1.set(N.Name(2, 5, 6), F.Fraction(1, 1))
        m1.set(N.Name(3, 1, 6), F.Fraction(1, 1))
        m1.set(N.Name(3, 2, 6), F.Fraction(-1, 1))
        m1.set(N.Name(5, 1, 6), F.Fraction(-1, 1))
        m1.set(N.Name(5, 2, 6), F.Fraction(1, 1))
        #
        m2.set(N.Name(1, 4, 6), F.Fraction(1, 1))
        m2.set(N.Name(1, 5, 6), F.Fraction(-1, 1))
        m2.set(N.Name(2, 4, 6), F.Fraction(-1, 1))
        m2.set(N.Name(2, 5, 6), F.Fraction(1, 1))
        m2.set(N.Name(4, 1, 6), F.Fraction(1, 1))
        m2.set(N.Name(4, 2, 6), F.Fraction(-1, 1))
        m2.set(N.Name(5, 1, 6), F.Fraction(-1, 1))
        m2.set(N.Name(5, 2, 6), F.Fraction(1, 1))
        #
        m3.set(N.Name(3, 4, 6), F.Fraction(-1, 1))
        m3.set(N.Name(3, 5, 6), F.Fraction(1, 1))
        m3.set(N.Name(4, 3, 6), F.Fraction(1, 1))
        m3.set(N.Name(4, 5, 6), F.Fraction(-1, 1))
        m3.set(N.Name(5, 3, 6), F.Fraction(-1, 1))
        m3.set(N.Name(5, 5, 6), F.Fraction(1, 1)) # modified
        tester = Ch.CheckMatrixWithTable(table, [m1, m2, m3])
        self.assertFalse(tester.DriveChecks(), msg='Should fail on the third')
