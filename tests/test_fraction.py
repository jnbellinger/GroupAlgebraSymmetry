''' Test suite for Fraction '''
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import unittest
from unittest.mock import patch
from Builder import Fraction as F

#class DefTest(unittest.TestCase):
class test_fraction(unittest.TestCase):
    #
    def test_fraction_init_nonint(self):
        with self.assertRaises(SystemExit) as cm:
            test_fraction_1 = F.Fraction(1.5, 4)
        try:
            self.assertNotEqual(cm.exception.code, 11)
            self.assertFalse(True, msg='Missed non-int argument')  # pragma: no cover  #pragma: no cover
        except:
            with self.assertRaises(SystemExit) as cm:
                test_fraction_2 = F.Fraction(1, 'x')
            try:
                self.assertNotEqual(cm.exception.code, 11)
                self.assertFalse(True, msg='Missed non-int argument')  #pragma: no cover
            except:
                self.assertTrue(True)
    def test_fraction_consistency(self):
        test_fraction_1 = F.Fraction(1,-4)
        if test_fraction_1.numerator != 1 or test_fraction_1.denominator != -4:
            self.assertFalse(True, msg='numerator and denominator do not match give 1, -4 ' + str(test_fraction_1))  #pragma: no cover
        else:
            self.assertTrue(True)
    #
    def test_fraction_init_zerodenom(self):
        with self.assertRaises(SystemExit) as cm:
            test_fraction_1 = F.Fraction(4, 0)
        if cm.exception.code == 12:
            self.assertTrue(True)
        else:
            self.assertFalse(True, msg='Missed 0 denominator')  #pragma: no cover
    #
    def test_fraction_print(self):
        test_fraction_1 = F.Fraction(-1, 10)
        expe = '(-1/10)'
        foun = test_fraction_1.__str__()
        if expe != foun:
            self.assertFalse(True, msg='Did not reproduce expected print ' +  str(expe) + ' ' + str(foun))  #pragma: no cover
        else:
            self.assertTrue(True)
    def test_fraction_repr(self):
        test_fraction_1 = F.Fraction(-1, 10)
        expe = '(-1/10)'
        foun = test_fraction_1.__repr__()
        if expe != foun:
            self.assertFalse(True, msg='Did not reproduce expected print ' + str(expe) + ' ' + str(foun))  #pragma: no cover
        else:
            self.assertTrue(True)
    #
    def test_fraction_isZero_true(self):
        test_fraction_1 = F.Fraction(0, 10)
        test_fraction_2 = F.Fraction(1, 10)
        if not test_fraction_1.isZero():
            self.assertFalse(True, msg='Did not find isZero when zero')  #pragma: no cover
        else:
            self.assertTrue(True)
    def test_fraction_iszero_false(self):
        test_fraction_2 = F.Fraction(1, 10)
        if test_fraction_2.isZero():
            self.assertFalse(True, msg='Found iszero when not zero')  #pragma: no cover
        else:
            self.assertTrue(True)
    #
    def test_fraction_equal_fraction(self):
        test_fraction_1 = F.Fraction(1, 3)
        test_fraction_2 = F.Fraction(2, 6)
        if not test_fraction_1 == test_fraction_2:
            self.assertFalse(True, msg='equal Fractions not found equal')  #pragma: no cover
        else:
            self.assertTrue(True)
    def test_fraction_equal_fraction_not_equal(self):
        test_fraction_1 = F.Fraction(1, 3)
        test_fraction_2 = F.Fraction(2, 7)
        if test_fraction_1 == test_fraction_2:
            self.assertFalse(True, msg='non-equal Fractions called equal')  #pragma: no cover
        else:
            self.assertTrue(True)
    def test_fraction_equal_fraction_bad(self):
        test_fraction_1 = F.Fraction(1, 3)
        test_fraction_2 = 7
        if test_fraction_1 == test_fraction_2:
            self.assertFalse(True, msg='Fraction called equal to non-Fraction')  #pragma: no cover
        else:
            self.assertTrue(True)
    #
    def test_fraction_mutemultiply_int(self):
        test_fraction = F.Fraction(1, 4)
        test_fraction.mutemultiply(4)
        if test_fraction.numerator != 4 or test_fraction.denominator != 4:
            self.assertFalse(True, msg='Fraction multiply by int failed, expect 4/4 ' + str(test_fraction))  #pragma: no cover
        else:
            self.assertTrue(True)
    def test_fraction_mutemultiply_int_bad(self):
        test_f = F.Fraction(1, 4)
        with self.assertRaises(SystemExit) as cm:
            test_f.mutemultiply('4')
        try:
            self.assertNotEqual(cm.exception.code, 14)
            self.assertFalse(True, msg='Missed non-int argument')  #pragma: no cover
        except:
            self.assertTrue(True)
    def test_fraction_mutemultiply_frac(self):
        test_1 = F.Fraction(1, 4)
        test_2 = F.Fraction(2, 3)
        test_1.mutemultiply(test_2)
        if test_1.numerator != 2 or test_1.denominator != 12:
            self.assertFalse(True, msg='Fraction multiplied by Fraction inconsistent ' + str(test_1))  #pragma: no cover
        else:
            self.assertTrue(True)
    #
    def test_fraction_muteadd_frac_compfrac(self):
        test_1 = F.Fraction(-1, 4)
        test_2 = F.Fraction(1, 2)
        test_1.muteadd(test_2)
        test_3 = F.Fraction(1, 4)
        if test_1 != test_3:
            self.assertFalse(True, msg='Fraction added to Fraction failed expect 2/8 ' + str(test_1))  #pragma: no cover
        else:
            self.assertTrue(True)
    def test_fraction_muteadd_frac(self):
        test_1 = F.Fraction(-1, 4)
        test_2 = F.Fraction(3, 4)
        test_1.muteadd(test_2)
        if test_1.numerator != 2 or test_1.denominator != 4:
            self.assertFalse(True, msg='Fraction added to Fraction failed expect 2/4 ' + str(test_1))  #pragma: no cover
        else:
            self.assertTrue(True)
    def test_fraction_muteadd_nonfrac(self):
        test_1 = F.Fraction(-1, 4)
        with self.assertRaises(SystemExit) as cm:
            test_1.muteadd(0)
        if cm.exception.code != 14:
            self.assertFalse(True, msg='Fractions add with Fractions') # pragma: no cover
        else:
            self.assertTrue(True)
    #
    def test_fraction_mutereplace(self):
        test_1 = F.Fraction(-1, 4)
        test_1.mutereplace(2, 5)
        test_2 = F.Fraction(2, 5)
        if test_1 != test_2:
            self.assertFalse(True, msg='Fraction replacement expected 2/5 got ' + str(test_1))  #pragma: no cover
        else:
            self.assertTrue(True)
    def test_fraction_mutereplace_zeroden(self):
        test_1 = F.Fraction(-1, 4)
        with self.assertRaises(SystemExit) as cm:
            test_1.mutereplace(2, 0)
        try:
            self.assertNotEqual(cm.exception.code, 15)
            self.assertFalse(True, msg='Fraction replacement with denominator 0 succeeded')  #pragma: no cover
        except:
            self.assertTrue(True)
    def test_fraction_mutereplace_nonfrac(self):
        test_1 = F.Fraction(-1, 4)
        with self.assertRaises(SystemExit) as cm:
            test_1.mutereplace('2', 0)
        try:
            self.assertNotEqual(cm.exception.code, 14)
            self.assertFalse(True, msg='Fraction replacement with non-int succeeded')  #pragma: no cover
        except:
            self.assertTrue(True)
    #
    def test_fraction_muteforcezero(self):
        test_1 = F.Fraction(100, 4)
        test_1.muteforceZero()
        if not test_1.isZero():
            self.assertFalse(True, msg='Fraction force to zero failed ' + str(test_1))  #pragma: no cover
        else:
            self.assertTrue(True)
    #
    def test_fraction_muteinvert(self):
        test_1 = F.Fraction(100, 4)
        test_1.muteinvert()
        test_2 = F.Fraction(4, 100)
        if test_1 != test_2:
            self.assertFalse(True, msg='Fraction invert failed, expected ' +  str(test_2) + ' got ' + str(test_1))  #pragma: no cover
        else:
            self.assertTrue(True)
    def test_fraction_muteinvert_zero(self):
        test_1 = F.Fraction(0, 4)
        with self.assertRaises(SystemExit) as cm:
            test_1.muteinvert()
        try:
            self.assertNotEqual(cm.exception.code, 16)
            self.assertFalse(True, msg='Fraction w/ 0 numerator inverted!')  #pragma: no cover
        except:
            self.assertTrue(True)
    #
    #
    #
    def test_fraction_multiply_int(self):
        test_fraction = F.Fraction(1, 4)
        test_2 = test_fraction.multiply(4)
        if test_2.numerator != 4 or test_2.denominator != 4:
            self.assertFalse(True, msg='Fraction multiply by int failed, expect 4/4 ' + str(test_2))  #pragma: no cover
        else:
            self.assertTrue(True)
    def test_fraction_multiply_int_bad(self):
        test_f = F.Fraction(1, 4)
        with self.assertRaises(SystemExit) as cm:
            test_g = test_f.multiply('4')
        try:
            self.assertNotEqual(cm.exception.code, 14)
            self.assertFalse(True, msg='Missed non-int argument')  #pragma: no cover
        except:
            self.assertTrue(True)
    def test_fraction_multiply_frac(self):
        test_1 = F.Fraction(1, 4)
        test_2 = F.Fraction(2, 3)
        test_p = test_1.multiply(test_2)
        if test_p.numerator != 2 or test_p.denominator != 12:
            self.assertFalse(True, msg='Fraction multiplied by Fraction inconsistent ' + str(test_p))  #pragma: no cover
        else:
            self.assertTrue(True)
    #
    def test_fraction_add_frac_compfrac(self):
        test_1 = F.Fraction(-1, 4)
        test_2 = F.Fraction(1, 2)
        test_a = test_1.add(test_2)
        test_3 = F.Fraction(1, 4)
        if test_a.numerator != 2 or test_a.denominator != 8:
            self.assertFalse(True, msg='Fraction added to Fraction failed expect 2/8 ' + str(test_a))  #pragma: no cover
        else:
            self.assertTrue(True)
    def test_fraction_add_frac(self):
        test_1 = F.Fraction(-1, 4)
        test_2 = F.Fraction(3, 4)
        test_a = test_1.add(test_2)
        if test_a.numerator != 2 or test_a.denominator != 4:
            self.assertFalse(True, msg='Fraction added to Fraction failed expect 2/4 ' + str(test_a))  #pragma: no cover
        else:
            self.assertTrue(True)
    def test_fraction_add_frac_badarg(self):
        test_1 = F.Fraction(-1, 4)
        with self.assertRaises(SystemExit) as cm:
            test_a = test_1.add('1')
        if cm.exception.code != 14:
            self.assertFalse(True, msg='Adding a string should not work') #pragma: no cover
        else:
            self.assertTrue(True)
    #
    def test_fraction_invert(self):
        test_1 = F.Fraction(100, 4)
        test_i = test_1.invert()
        test_2 = F.Fraction(4, 100)
        if test_i.numerator != 4 or test_i.denominator != 100:
            self.assertFalse(True, msg='Fraction invert failed, expected ' + str(test_2) + ' got ' + str(test_1))  #pragma: no cover
        else:
            self.assertTrue(True)
    def test_fraction_invertzero(self):
        test_1 = F.Fraction(0, 4)
        with self.assertRaises(SystemExit) as cm:
            test_i = test_1.invert()
        self.assertEqual(cm.exception.code, 16,  msg='Fraction w/ 0 numerator inverted!')  #pragma: no cover
    #
    def test_fraction_simplify1(self):
        test_f = F.Fraction(2, 4)
        self.assertEqual(str(test_f), '(1/2)', msg='Should have cancelled a factor of 2')
    def test_fraction_simplify2(self):
        test_f = F.Fraction(5, 1)
        self.assertEqual(str(test_f), '(5)', msg='Should have skipped the denominator of 1')
    def test_fraction_simplify3(self):
        test_f = F.Fraction(0, 1)
        self.assertEqual(str(test_f), '(0)', msg='Should have set to 0')
    def test_fraction_simplify4(self):
        test_f = F.Fraction(7, 7)
        self.assertEqual(str(test_f), '(1)', msg='Should have set to 1')
    def test_fraction_simplify5(self):
        test_f = F.Fraction(7, -7)
        self.assertEqual(str(test_f), '(-1)', msg='Should have set to -1')
    def test_fraction_simplify6(self):
        test_f = F.Fraction(2, -7)
        self.assertEqual(str(test_f), '(-2/7)', msg='Should have numerator negative')
    #
    def test_fraction_hash(self):
        # I wonder how portable this is...
        test_f = F.Fraction(2, -7)
        self.assertEqual(str(test_f.__hash__()), '118768521141512092', msg='This is what I get on ubuntu')

if __name__ == '__main__':
    unittest.main()  # pragma: no cover
