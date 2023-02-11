''' Test suite for Element '''
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Builder import Fraction as F
from Builder import Name as N
from Builder import Element as E
import unittest

class test_element(unittest.TestCase):
    #
    def test_element_init_and_print(self):
        nam1 = N.Name(1, 4, 6)
        fra1 = F.Fraction(1, 3)
        ele = E.Element(nam1, fra1)
        expe = '{1_4}(1/3)'
        foun = ele.__str__()
        self.assertEqual(expe, foun, msg='Expected ' + str(expe) + ' got ' +str(foun))
    #
    def test_element_repr(self):
        nam1 = N.Name(1, 4, 6)
        fra1 = F.Fraction(1, 3)
        ele = E.Element(nam1, fra1)
        expe = '{1_4}(1/3)'
        foun = ele.__repr__()
        self.assertEqual(expe, foun, msg='Expected ' + str(expe) + ' got ' + str(foun))
    #
    def test_element_init_badargs_fra(self):
        nam1 = N.Name(1, 4, 6)
        fra1 = F.Fraction(1, 3)
        with self.assertRaises(SystemExit) as cm:
            test_ele = E.Element(nam1, 4)
        self.assertEqual(cm.exception.code, 51, msg='Missed non-fraction second argument')
    def test_element_init_badargs_name(self):
        nam1 = N.Name(1, 4, 6)
        fra1 = F.Fraction(1, 3)
        with self.assertRaises(SystemExit) as cm:
            test_ele = E.Element('nam', fra1)
        self.assertEqual(cm.exception.code, 51, msg='Missed non-Name first argument')
    #
    def test_element_iszero_not(self):
        nam1 = N.Name(1, 4, 6)
        fra1 = F.Fraction(1, 3)
        ele1 = E.Element(nam1, fra1)
        self.assertFalse(ele1.isZero(), msg='Claimed zero when not ' + str(ele1))
    def test_element_iszero_is(self):
        nam1 = N.Name(1, 4, 6)
        fra1 = F.Fraction(0, 3)
        ele1 = E.Element(nam1, fra1)
        self.assertTrue(ele1.isZero(), msg='Claimed non-zero when it is ' + str(ele1))
    #
    def test_element_eq_is(self):
        nam1 = N.Name(1, 4, 6)
        fra1 = F.Fraction(1, 3)
        ele1 = E.Element(nam1, fra1)
        nam2 = N.Name(1, 4, 6)
        fra2 = F.Fraction(2, 6)
        ele2 = E.Element(nam2, fra2)
        self.assertTrue(ele1==ele2, msg='Claimed non-equal when they are ' + str(ele1) + ' ' + str(ele2))
    def test_element_eq_diff_frac(self):
        nam1 = N.Name(1, 4, 6)
        fra1 = F.Fraction(1, 3)
        ele1 = E.Element(nam1, fra1)
        nam2 = N.Name(1, 4, 6)
        fra2 = F.Fraction(1, 6)
        ele2 = E.Element(nam2, fra2)
        self.assertFalse(ele1==ele2, msg='Claimed equal when they are not ' + str(ele1) + ' ' + str(ele2))
    def test_element_eq_diff_name(self):
        nam1 = N.Name(1, 4, 6)
        fra1 = F.Fraction(1, 3)
        ele1 = E.Element(nam1, fra1)
        nam2 = N.Name(2, 4, 6)
        fra2 = F.Fraction(1, 3)
        ele2 = E.Element(nam2, fra2)
        self.assertFalse(ele1==ele2, msg='Claimed equal when they are not ' + str(ele1) + ' ' + str(ele2))
    #
    def test_element_eq_nonelem(self):
        nam1 = N.Name(1, 4, 6)
        fra1 = F.Fraction(1, 3)
        ele1 = E.Element(nam1, fra1)
        with self.assertRaises(SystemExit) as cm:
            if ele1 == '{1_4}(1/3)':
                print('x')  # pragma: no cover
        self.assertTrue(cm.exception.code == 53, msg='Failed to quit on bad comparison')
    #
    def test_element_mutemultiply_element(self):
        nam1 = N.Name(1, 4, 6)
        fra1 = F.Fraction(1, 3)
        ele1 = E.Element(nam1, fra1)
        nam2 = N.Name(1, 4, 6)
        fra2 = F.Fraction(3, 1)
        ele2 = E.Element(nam2, fra2)
        ele1.mutemultiply(ele2)
        k = ele1.name == nam1 and ele1.fraction.numerator == 3 and ele1.fraction.denominator == 3
        self.assertTrue(k, msg='Name or fraction is wrong with element, expect {1_4}{3/3} ' + str(ele1))
    def test_element_mutemultiply_fraction(self):
        nam1 = N.Name(1, 4, 6)
        fra1 = F.Fraction(1, 3)
        ele1 = E.Element(nam1, fra1)
        nam2 = N.Name(1, 4, 6)
        fra2 = F.Fraction(3, 1)
        ele1.mutemultiply(fra2)
        k = ele1.name == nam1 and ele1.fraction.numerator == 3 and ele1.fraction.denominator == 3
        self.assertTrue(k, msg='Name or fraction is wrong with element, expect {1_4}{3/3} ' + str(ele1))
    def test_element_mutemultiply_int(self):
        nam1 = N.Name(1, 4, 6)
        fra1 = F.Fraction(1, 3)
        ele1 = E.Element(nam1, fra1)
        ele1.mutemultiply(3)
        k = ele1.name == nam1 and ele1.fraction.numerator == 3 and ele1.fraction.denominator == 3
        self.assertTrue(k, msg='Name or fraction is wrong with element, expect {1_4}{3/3} ' + str(ele1))
    def test_element_mutemultiply_unknown(self):
        nam1 = N.Name(1, 4, 6)
        fra1 = F.Fraction(1, 3)
        ele1 = E.Element(nam1, fra1)
        with self.assertRaises(SystemExit) as cm:
            ele1.mutemultiply('d')
        self.assertEqual(cm.exception.code, 56, msg='Missed non-element/fraction argument')
    def test_element_mutemultiply_badname(self):
        nam1 = N.Name(1, 4, 6)
        fra1 = F.Fraction(1, 3)
        ele1 = E.Element(nam1, fra1)
        nam2 = N.Name(2, 4, 6)
        fra2 = F.Fraction(1, 3)
        ele2 = E.Element(nam2, fra2)
        with self.assertRaises(SystemExit) as cm:
            ele1.mutemultiply(ele2)
        self.assertEqual(cm.exception.code, 54, msg='Missed different element name')
    #
    def test_element_muteforceZero(self):
        nam1 = N.Name(1, 4, 6)
        fra1 = F.Fraction(1, 3)
        ele1 = E.Element(nam1, fra1)
        ele1.muteforceZero()
        self.assertTrue(ele1.isZero(), msg='Force zero failed ' + str(ele1))
    #
    def test_element_muteinvert(self):
        nam1 = N.Name(1, 4, 6)
        fra1 = F.Fraction(1, 3)
        ele1 = E.Element(nam1, fra1)
        ele1.muteinvert()
        k = ele1.fraction.numerator == 3 and ele1.fraction.denominator == 1
        self.assertTrue(k, msg='Invert failed ' + str(ele1))
    def test_element_muteinvert_bad(self):
        nam1 = N.Name(1, 4, 6)
        fra1 = F.Fraction(0, 3)
        ele1 = E.Element(nam1, fra1)
        with self.assertRaises(SystemExit) as cm:
            ele1.muteinvert()
        self.assertEqual(cm.exception.code, 16, msg='Inversion of 0 was not caught ' +  str(ele1))
    #
    def test_element_mutereplace_good(self):
        nam1 = N.Name(1, 4, 6)
        fra1 = F.Fraction(0, 3)
        ele1 = E.Element(nam1, fra1)
        fra2 = F.Fraction(1, 1)
        ele1.mutereplace(fra2)
        k = ele1.name == nam1 and ele1.fraction.numerator == 1 and ele1.fraction.denominator == 1
        self.assertTrue(k, msg='Failed to mutereplace, expect {1_4}(1/1) ' + str(ele1))
    def test_element_mutereplace_bad(self):
        nam1 = N.Name(1, 4, 6)
        fra1 = F.Fraction(0, 3)
        ele1 = E.Element(nam1, fra1)
        with self.assertRaises(SystemExit) as cm:
            ele1.mutereplace('1/2')
        self.assertEqual(cm.exception.code, 54, msg='mutereplace should not work with non-Fractions')

    def test_element_multiply_element(self):
        nam1 = N.Name(1, 4, 6)
        fra1 = F.Fraction(1, 3)
        ele1 = E.Element(nam1, fra1)
        nam2 = N.Name(1, 4, 6)
        fra2 = F.Fraction(3, 1)
        ele2 = E.Element(nam2, fra2)
        ele3 = ele1.multiply(ele2)
        k = ele3.name == nam1 and ele3.fraction.numerator == 3 and ele3.fraction.denominator == 3
        self.assertTrue(k, msg='Name or fraction is wrong with element, expect {1_4}{3/3} ' + str(ele3))
    def test_element_multiply_fraction(self):
        nam1 = N.Name(1, 4, 6)
        fra1 = F.Fraction(1, 3)
        ele1 = E.Element(nam1, fra1)
        nam2 = N.Name(1, 4, 6)
        fra2 = F.Fraction(3, 1)
        ele3 = ele1.multiply(fra2)
        k = ele3.name == nam1 and ele3.fraction.numerator == 3 and ele3.fraction.denominator == 3
        self.assertTrue(k, msg='Name or fraction is wrong with element, expect {1_4}{3/3} ' + str(ele3))
    def test_element_multiply_int(self):
        nam1 = N.Name(1, 4, 6)
        fra1 = F.Fraction(1, 3)
        ele1 = E.Element(nam1, fra1)
        ele3 = ele1.multiply(3)
        k = ele3.name == nam1 and ele3.fraction.numerator == 3 and ele3.fraction.denominator == 3
        self.assertTrue(k, msg='Name or fraction is wrong with element, expect {1_4}{3/3} ' + str(ele3))
    def test_element_multiply_unknown(self):
        nam1 = N.Name(1, 4, 6)
        fra1 = F.Fraction(1, 3)
        ele1 = E.Element(nam1, fra1)
        with self.assertRaises(SystemExit) as cm:
            ele2 = ele1.multiply('d')
        self.assertEqual(cm.exception.code, 54, msg='Missed non-element/fraction argument')
    def test_element_multiply_badname(self):
        nam1 = N.Name(1, 4, 6)
        fra1 = F.Fraction(1, 3)
        ele1 = E.Element(nam1, fra1)
        nam2 = N.Name(2, 4, 6)
        fra2 = F.Fraction(1, 3)
        ele2 = E.Element(nam2, fra2)
        with self.assertRaises(SystemExit) as cm:
            ele3 = ele1.multiply(ele2)
        self.assertEqual(cm.exception.code, 55, msg='Missed different element name')
    #
    def test_element_invert(self):
        nam1 = N.Name(1, 4, 6)
        fra1 = F.Fraction(1, 3)
        ele1 = E.Element(nam1, fra1)
        ele2 = ele1.invert()
        k = ele2.fraction.numerator == 3 and ele2.fraction.denominator == 1
        self.assertTrue(k, msg='Invert failed ' + str(ele2))
    def test_element_invert_bad(self):
        nam1 = N.Name(1, 4, 6)
        fra1 = F.Fraction(0, 3)
        ele1 = E.Element(nam1, fra1)
        with self.assertRaises(SystemExit) as cm:
            ele2 = ele1.invert()
        self.assertEqual(cm.exception.code, 16, msg='Inversion of 0 was not caught ' + str(ele1))
    #
    def test_element_muteadd_check_element(self):
        nam1 = N.Name(1, 4, 6)
        fra1 = F.Fraction(1, 3)
        ele1 = E.Element(nam1, fra1)
        nam2 = N.Name(1, 4, 6)
        fra2 = F.Fraction(1, 2)
        ele2 = E.Element(nam2, fra2)
        ele1.muteadd(ele2)
        k = ele1.name == nam1 and ele1.fraction.numerator == 5 and ele1.fraction.denominator == 6
        self.assertTrue(k, msg='Addition failed, expect {1,4}(5/6) ' + str(ele1))
    def test_element_muteadd_check_fraction(self):
        nam1 = N.Name(1, 4, 6)
        fra1 = F.Fraction(1, 3)
        ele1 = E.Element(nam1, fra1)
        fra2 = F.Fraction(1, 2)
        ele1.muteadd(fra2)
        k = ele1.name == nam1 and ele1.fraction.numerator == 5 and ele1.fraction.denominator == 6
        self.assertTrue(k, msg='Addition failed, expect {1,4}(5/6) ' + str(ele1))
    def test_element_muteadd_badtype(self):
        nam1 = N.Name(1, 4, 6)
        fra1 = F.Fraction(1, 3)
        ele1 = E.Element(nam1, fra1)
        with self.assertRaises(SystemExit) as cm:
            ele2 = ele1.muteadd('d')
        self.assertEqual(cm.exception.code, 57, msg='Bad type was not caught')
    def test_element_muteadd_badname(self):
        nam1 = N.Name(1, 4, 6)
        fra1 = F.Fraction(1, 3)
        ele1 = E.Element(nam1, fra1)
        nam2 = N.Name(2, 4, 6)
        fra2 = F.Fraction(1, 2)
        ele2 = E.Element(nam2, fra2)
        with self.assertRaises(SystemExit) as cm:
            ele1.muteadd(ele2)
        self.assertEqual(cm.exception.code, 58, msg='Name mismatch was not caught ' + str(ele1))
    #
    def test_element_add_check_element(self):
        nam1 = N.Name(1, 4, 6)
        fra1 = F.Fraction(1, 3)
        ele1 = E.Element(nam1, fra1)
        nam2 = N.Name(1, 4, 6)
        fra2 = F.Fraction(1, 2)
        ele2 = E.Element(nam2, fra2)
        ele3 = ele1.add(ele2)
        k = ele3.name == nam1 and ele3.fraction.numerator == 5 and ele3.fraction.denominator == 6
        self.assertTrue(k, msg='Addition failed, expect {1,4}(5/6) ' + str(ele3))
    def test_element_add_check_fraction(self):
        nam1 = N.Name(1, 4, 6)
        fra1 = F.Fraction(1, 3)
        ele1 = E.Element(nam1, fra1)
        fra2 = F.Fraction(1, 2)
        ele2 = ele1.add(fra2)
        k = ele2.name == nam1 and ele2.fraction.numerator == 5 and ele2.fraction.denominator == 6
        self.assertTrue(k, msg='Addition failed, expect {1,4}(5/6) ' + str(ele2))
    def test_element_add_badtype(self):
        nam1 = N.Name(1, 4, 6)
        fra1 = F.Fraction(1, 3)
        ele1 = E.Element(nam1, fra1)
        with self.assertRaises(SystemExit) as cm:
            ele2 = ele1.add('d')
        self.assertEqual(cm.exception.code, 54, msg='Bad type was not caught')
    def test_element_add_badname(self):
        nam1 = N.Name(1, 4, 6)
        fra1 = F.Fraction(1, 3)
        ele1 = E.Element(nam1, fra1)
        nam2 = N.Name(2, 4, 6)
        fra2 = F.Fraction(1, 2)
        ele2 = E.Element(nam2, fra2)
        with self.assertRaises(SystemExit) as cm:
            ele3 = ele1.add(ele2)
        self.assertEqual(cm.exception.code, 55, msg='Name mismatch was not caught ' + str(ele1))
    def test_element_hash(self):
        nam1 = N.Name(1, 4, 6)
        fra1 = F.Fraction(1, 3)
        ele1 = E.Element(nam1, fra1)
        self.assertEqual(str(hash(ele1)), '-3556319692878664532', msg='Hash is obscure')
    #
    def test_element_operatorVersion(self):
        nam1 = N.Name(0, 4, 6)
        fra1 = F.Fraction(1, 3)
        ele1 = E.Element(nam1, fra1)
        self.assertEqual(ele1.operatorVersion(), '(1/3)C4', msg='Should not have zeros')
    def test_element_operatorVersion_2(self):
        nam1 = N.Name(0, 4, 16)
        fra1 = F.Fraction(1, 3)
        ele1 = E.Element(nam1, fra1)
        self.assertEqual(ele1.operatorVersion(), '(1/3)C04', msg='Should have 1 zeros')
    def test_element_operatorVersion_badname(self):
        nam1 = N.Name(1, 4, 16)
        fra1 = F.Fraction(1, 3)
        ele1 = E.Element(nam1, fra1)
        with self.assertRaises(SystemExit) as cm:
            xx = ele1.operatorVersion()
        self.assertEqual(cm.exception.code, 56, msg='Should not have good Name')


# test_element_add(self, other):

if __name__ == '__main__':
    unittest.main()  # pragma: no cover
