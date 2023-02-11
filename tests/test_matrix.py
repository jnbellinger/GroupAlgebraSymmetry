''' Test suite for Matrix:  square matrices of Fractions '''
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import unittest
from unittest.mock import patch
from Builder import Name as N
from Builder import Fraction as F
from Builder import Matrix as M

class test_matrix(unittest.TestCase):
    #
    def test_matrix_init_blank(self):
        newmat = M.Matrix(2)
        self.assertEqual(str(newmat), '(0) (0) \n(0) (0) ', msg='Should have been 2x2')
    def test_matrix_init_nonint(self):
        with self.assertRaises(SystemExit) as cm:
            newmat = M.Matrix('2')
        self.assertEqual(cm.exception.code, 190, msg='Non-int size')
    def test_matrix_init_neg(self):
        with self.assertRaises(SystemExit) as cm:
            newmat = M.Matrix(-2)
        self.assertEqual(cm.exception.code, 191, msg='Negative size')
    def test_matrix_set_ok(self):
        newmat = M.Matrix(2)
        newmat.set(N.Name(0, 0, 2), F.Fraction(4, 1))
        self.assertEqual(str(newmat), '(4) (0) \n(0) (0) ', msg='Should have a non-zero')
    def test_matrix_set_frac_ok(self):
        newmat = M.Matrix(2)
        ff = F.Fraction(4, 1)
        newmat.set(N.Name(0, 0, 2), ff)
        ff.mutemultiply(F.Fraction(8, 1))
        self.assertEqual(str(newmat), '(4) (0) \n(0) (0) ', msg='Should not have changed')
    def test_matrix_set_badname_0(self):
        newmat = M.Matrix(2)
        with self.assertRaises(SystemExit) as cm:
            newmat.set('{1_2}', F.Fraction(4, 1))
        self.assertEqual(cm.exception.code, 192, msg='Should flag bad Name')
    def test_matrix_set_badfrac(self):
        newmat = M.Matrix(2)
        with self.assertRaises(SystemExit) as cm:
            newmat.set(N.Name(0, 0, 2), 4)
        self.assertEqual(cm.exception.code, 192, msg='Should flag bad Fraction')
    def test_matrix_set_badname(self):
        newmat = M.Matrix(2)
        with self.assertRaises(SystemExit) as cm:
            newmat.set(N.Name(0, 0, 3), F.Fraction(4, 1))
        self.assertEqual(cm.exception.code, 193, msg='Should flag bad Name size')
    #
    def test_matrix_get_ok(self):
        newmat = M.Matrix(2)
        ff = F.Fraction(4, 1)
        newmat.set(N.Name(0, 0, 2), F.Fraction(4, 1))
        self.assertEqual(ff, newmat.get(0, 0))
    def test_matrix_get_nonint(self):
        newmat = M.Matrix(2)
        ff = F.Fraction(4, 1)
        newmat.set(N.Name(0, 0, 2), F.Fraction(4, 1))
        with self.assertRaises(SystemExit) as cm:
            newmat.get(1, F.Fraction(4, 1))
        self.assertEqual(cm.exception.code, 194, msg='Wants ints, let one serve for both')
    def test_matrix_get_oob_high(self):
        newmat = M.Matrix(2)
        ff = F.Fraction(4, 1)
        newmat.set(N.Name(0, 0, 2), F.Fraction(4, 1))
        with self.assertRaises(SystemExit) as cm:
            newmat.get(1, 2)
        self.assertEqual(cm.exception.code, 195, msg='Out of bounds high')
    def test_matrix_get_oob_low(self):
        newmat = M.Matrix(2)
        ff = F.Fraction(4, 1)
        newmat.set(N.Name(0, 0, 2), F.Fraction(4, 1))
        with self.assertRaises(SystemExit) as cm:
            newmat.get(1, -2)
        self.assertEqual(cm.exception.code, 195, msg='Out of bounds low')
    #
    def test_matrix_add_ok(self):
        newmat = M.Matrix(2)
        newmat.set(N.Name(0, 0, 2), F.Fraction(4, 1))
        another = M.Matrix(2)
        another.set(N.Name(1, 1, 2), F.Fraction(1, 4))
        third = newmat.add(another)
        self.assertEqual(str(third), '(4) (0) \n(0) (1/4) ', msg='Should be diagonal')
    def test_matrix_add_scale_ok(self):
        newmat = M.Matrix(2)
        newmat.set(N.Name(0, 0, 2), F.Fraction(4, 1))
        another = M.Matrix(2)
        another.set(N.Name(1, 1, 2), F.Fraction(1, 4))
        ff = F.Fraction(4, 1)
        third = newmat.add(another, ff)
        self.assertEqual(str(third), '(4) (0) \n(0) (1) ', msg='Should be diagonal w/ higher')
    def test_matrix_add_nonmat(self):
        newmat = M.Matrix(2)
        with self.assertRaises(SystemExit) as cm:
            newmat.add('matrix')
        self.assertEqual(cm.exception.code, 196, msg='Not a Matrix to add')
    def test_matrix_add_wrong_mat_size(self):
        newmat = M.Matrix(2)
        second = M.Matrix(3)
        with self.assertRaises(SystemExit) as cm:
            newmat.add(second)
        self.assertEqual(cm.exception.code, 197, msg='Second Matrix wrong size')
    def test_matrix_add_arg_not_frac(self):
        newmat = M.Matrix(2)
        second = M.Matrix(2)
        with self.assertRaises(SystemExit) as cm:
            newmat.add(second, 2)
        self.assertEqual(cm.exception.code, 198, msg='2nd argument is not a Fraction')
    #
    def test_matrix_multiply_ok_matrix(self):
        newmat = M.Matrix(2)
        newmat.set(N.Name(0, 0, 2), F.Fraction(4, 1))
        newmat.set(N.Name(0, 1, 2), F.Fraction(3, 1))
        newmat.set(N.Name(1, 0, 2), F.Fraction(1, 1))
        newmat.set(N.Name(1, 1, 2), F.Fraction(2, 1))
        another = M.Matrix(2)
        another.set(N.Name(0, 0, 2), F.Fraction(1, 4))
        another.set(N.Name(1, 0, 2), F.Fraction(1, 4))
        another.set(N.Name(0, 1, 2), F.Fraction(1, 1))
        third = newmat.multiply(another)
        self.assertEqual(str(third), '(7/4) (4) \n(3/4) (1) ', msg='Multiply should be easy')
    def test_matrix_multiply_ok_frac(self):
        newmat = M.Matrix(2)
        newmat.set(N.Name(0, 0, 2), F.Fraction(4, 1))
        newmat.set(N.Name(0, 1, 2), F.Fraction(3, 1))
        newmat.set(N.Name(1, 0, 2), F.Fraction(1, 1))
        newmat.set(N.Name(1, 1, 2), F.Fraction(2, 1))
        second = newmat.multiply(F.Fraction(-1, 1))
        self.assertEqual(str(second), '(-4) (-3) \n(-1) (-2) ', msg='Simple scale')
    def test_matrix_multiply_badarg(self):
        newmat = M.Matrix(2)
        newmat.set(N.Name(0, 0, 2), F.Fraction(4, 1))
        newmat.set(N.Name(0, 1, 2), F.Fraction(3, 1))
        newmat.set(N.Name(1, 0, 2), F.Fraction(1, 1))
        newmat.set(N.Name(1, 1, 2), F.Fraction(2, 1))
        with self.assertRaises(SystemExit) as cm:
            second = newmat.multiply(3)
        self.assertEqual(cm.exception.code, 199, msg='2nd argument is not a Fraction or Matrix')
    def test_matrix_multiply_wrongsize(self):
        newmat = M.Matrix(2)
        second = M.Matrix(3)
        with self.assertRaises(SystemExit) as cm:
            third = newmat.multiply(second)
        self.assertEqual(cm.exception.code, 290, msg='Matrices must be same size')
    def test_matrix_repr(self):
        newmat = M.Matrix(2)
        newmat.set(N.Name(0, 0, 2), F.Fraction(4, 1))
        self.assertEqual(repr(newmat), '(4) (0) \n(0) (0) ', msg='Calls __str, should be same')
    #
    def test_matrix_equal(self):
        newmat = M.Matrix(2)
        newmat.set(N.Name(0, 0, 2), F.Fraction(4, 1))
        second = M.Matrix(2)
        second.set(N.Name(0, 0, 2), F.Fraction(4, 1))
        self.assertEqual(newmat, second, 'Both should be the same')
    def test_matrix_equal_not(self):
        newmat = M.Matrix(2)
        newmat.set(N.Name(0, 0, 2), F.Fraction(4, 1))
        second = M.Matrix(2)
        second.set(N.Name(1, 0, 2), F.Fraction(4, 1))
        self.assertNotEqual(newmat, second, 'Not the same')
    def test_matrix_equal_badarg(self):
        newmat = M.Matrix(2)
        newmat.set(N.Name(0, 0, 2), F.Fraction(4, 1))
        second = M.Matrix(3)
        with self.assertRaises(SystemExit) as cm:
            if newmat == 4:
                print('xc') # pragma: no cover
        self.assertEqual(cm.exception.code, 291, msg='Matrix can only equal a Matrix')
    def test_matrix_equal_wrongsize(self):
        newmat = M.Matrix(2)
        newmat.set(N.Name(0, 0, 2), F.Fraction(4, 1))
        second = M.Matrix(3)
        with self.assertRaises(SystemExit) as cm:
            if newmat == second:
                print('xc') # pragma: no cover
        self.assertEqual(cm.exception.code, 292, msg='Matrix can only equal a Matrix of the same size')

if __name__ == '__main__':
    unittest.main()  # pragma: no cover
