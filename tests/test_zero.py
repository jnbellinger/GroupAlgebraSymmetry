''' Test suite for Zero '''
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import unittest
from unittest.mock import patch
from Builder import Name as N
from Builder import Fraction as F
from Builder import Element as E
from Builder import Zero as Z
from Builder import Chain as C

#class DefTest(unittest.TestCase):
class test_zero(unittest.TestCase):
    #
    def test_zero_ok_size(self):
        n1 = N.Name(1, 3, 4)
        n2 = N.Name(3, 1, 4)
        n3 = N.Name(1, 3, 4)
        n4 = N.Name(3, 3, 4)
        f1 = F.Fraction(1, 3)
        f2 = F.Fraction(2, 3)
        f3 = F.Fraction(3, 3)
        f4 = F.Fraction(4, 3)
        z = Z.Zero([n1, n2, n3, n4])
        self.assertEqual(len(z.zerolist), 3, msg='Failed to create a 3-name Zero')
    def test_zero_ok_order(self):
        n1 = N.Name(1, 3, 4)
        n2 = N.Name(3, 1, 4)
        n3 = N.Name(1, 3, 4)
        n4 = N.Name(3, 3, 4)
        z = Z.Zero([n1, n2, n3])
        k = n1 == z.zerolist[0] and n2 == z.zerolist[1]
        self.assertTrue(k, msg='Names are in the wrong order ' + str(len(z.zerolist)))
    def test_zero_ok_size_elements(self):
        n1 = N.Name(1, 3, 4)
        n2 = N.Name(3, 1, 4)
        n3 = N.Name(1, 3, 4)
        n4 = N.Name(3, 3, 4)
        f1 = F.Fraction(1, 3)
        f2 = F.Fraction(2, 3)
        f3 = F.Fraction(3, 3)
        f4 = F.Fraction(4, 3)
        e1 = E.Element(n1, f1)
        e2 = E.Element(n2, f1)
        e3 = E.Element(n3, f1)
        e4 = E.Element(n4, f1)
        z = Z.Zero([e1, e2, e3, e4])
        self.assertEqual(len(z.zerolist), 3, msg='Failed to create a 3-element Zero')
    def test_zero_ok_order_elements(self):
        n1 = N.Name(1, 3, 4)
        n2 = N.Name(3, 1, 4)
        n3 = N.Name(1, 3, 4)
        n4 = N.Name(3, 3, 4)
        f1 = F.Fraction(1, 3)
        f2 = F.Fraction(2, 3)
        f3 = F.Fraction(3, 3)
        f4 = F.Fraction(4, 3)
        e1 = E.Element(n1, f1)
        e2 = E.Element(n2, f1)
        e3 = E.Element(n3, f1)
        e4 = E.Element(n4, f1)
        z = Z.Zero([e1, e2, e3, e4])
        k = n1 == z.zerolist[0] and n2 == z.zerolist[1] and n4 == z.zerolist[2]
        self.assertTrue(k, msg='Element Names are in the wrong order')
    def test_zero_ok_empty(self):
        z = Z.Zero([])
        self.assertEqual(len(z.zerolist), 0, msg='Zero should be empty')
    def test_zero_bad_nolist(self):
        n1 = N.Name(1, 3, 4)
        with self.assertRaises(SystemExit) as cm:
            z = Z.Zero(n1)
        self.assertEqual(cm.exception.code, 80, msg='Missed init w/o list failure')
    def test_zero_bad_noname(self):
        with self.assertRaises(SystemExit) as cm:
            z = Z.Zero(['{1_4}'])
        self.assertEqual(cm.exception.code, 81, msg='Missed init bad list failure')
    #
    def make_basic_one(self):
        n1 = N.Name(1, 3, 4)
        n2 = N.Name(3, 1, 4)
        n3 = N.Name(1, 3, 4)
        n4 = N.Name(3, 3, 4)
        f1 = F.Fraction(1, 3)
        f2 = F.Fraction(2, 3)
        f3 = F.Fraction(3, 3)
        f4 = F.Fraction(4, 3)
        e1 = E.Element(n1, f1)
        e2 = E.Element(n2, f1)
        e3 = E.Element(n3, f1)
        e4 = E.Element(n4, f1)
        return Z.Zero([e1, e2, e3, e4])
    #
    #
    def test_zero_add_name(self):
        z = self.make_basic_one()
        n5 = N.Name(2, 2, 4)
        z.add(n5)
        self.assertEqual(len(z.zerolist), 4, msg='Failed to add a unique Name')
    def test_zero_add_element(self):
        z = self.make_basic_one()
        n5 = N.Name(2, 2, 4)
        f5 = F.Fraction(1, 2)
        e5 = E.Element(n5, f5)
        z.add(e5)
        self.assertEqual(len(z.zerolist), 4, msg='Failed to add a unique Element')
    def test_zero_add_dups(self):
        z = self.make_basic_one()
        n5 = N.Name(2, 2, 4)
        f5 = F.Fraction(1, 2)
        e5 = E.Element(n5, f5)
        n6 = N.Name(2, 2, 4)
        z.add([e5, n6])
        self.assertEqual(len(z.zerolist), 4, msg='Failed to add a unique Element')
    def test_zero_add_badarg(self):
        z = self.make_basic_one()
        with self.assertRaises(SystemExit) as cm:
            z = z.add('{1_4}')
        self.assertEqual(cm.exception.code, 82, msg='Missed add bad arg failure')
    def test_zero_add_badlist(self):
        z = self.make_basic_one()
        n5 = N.Name(1, 1, 4)
        with self.assertRaises(SystemExit) as cm:
            z = z.add([n5, '{1_4}'])
        self.assertEqual(cm.exception.code, 81, msg='Missed add bad arg failure')
    def test_zero_add_chain(self):
        z = self.make_basic_one()
        nam = []
        fra = []
        ele = []
        for i in range(3):
            for j in range(3):
                nam.append(N.Name(i, j, 6))
                fra.append(F.Fraction(j+1, i+1))
                ele.append(E.Element(nam[-1], fra[-1]))
        nam = []
        fra = []
        ele = []
        for i in range(3):
            for j in range(3):
                nam.append(N.Name(i, j, 6))
                fra.append(F.Fraction(j+1, i+1))
                ele.append(E.Element(nam[-1], fra[-1]))
        ch1 = C.Chain(ele)
        with self.assertRaises(SystemExit) as cm:
            z.add(ch1)
        self.assertEqual(cm.exception.code, 12, msg='Failed to add Chain')
    #
    #
    def test_zero_present_name(self):
        z = self.make_basic_one()
        n5 = N.Name(1, 3, 4)
        self.assertTrue(z.present(n5), msg='Failed to find Name that was present')
    def test_zero_present_name_not(self):
        z = self.make_basic_one()
        n5 = N.Name(0, 3, 4)
        self.assertFalse(z.present(n5), msg='Found Name that was not present')
    def test_zero_present_name_notelement(self):
        z = self.make_basic_one()
        n5 = N.Name(0, 3, 4)
        e5 = E.Element(n5, F.Fraction(1, 3))
        self.assertFalse(z.present(e5), msg='Found Element that was not present')
    def test_zero_present_nonname(self):
        z = self.make_basic_one()
        with self.assertRaises(SystemExit) as cm:
            z.present('{1_3}')
        self.assertEqual(cm.exception.code, 83, msg='Missed invalid argument')
    #
    def test_zero_str(self):
        z = self.make_basic_one()
        self.assertEqual(str(z), '{1_3},{3_1},{3_3}', msg='String should be 3 elements, str')
    def test_zero_repr(self):
        z = self.make_basic_one()
        self.assertEqual(repr(z), '{1_3},{3_1},{3_3}', msg='String should be 3 elements, repr')
