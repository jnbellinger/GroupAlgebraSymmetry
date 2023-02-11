''' Test the CommuteBundle class '''
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
from Builder import CommuteBundle

#Table

class test_commutebundle(unittest.TestCase):

    def prepareequation(self):
        f1 = F.Fraction(1, 3)
        f2 = F.Fraction(2, 3)
        f3 = F.Fraction(3, 3)
        n1 = N.Name(3, 1, 4)
        n2 = N.Name(3, 2, 4)
        n3 = N.Name(3, 3, 4)
        e1 = E.Element(n1, f1)
        e2 = E.Element(n2, f2)
        e3 = E.Element(n3, f3)
        eq1 = Eq.Equation([e1, e2, e3])
        ch1 = Chain.Chain([e1, e2, e3])  # Not realistic, who cares
        return eq1, ch1
    #
    def test_commutebundle_sanity0(self):
        with self.assertRaises(SystemExit) as cm:
            cb = CommuteBundle.CommuteBundle(1, 0, 'noteq', [], Z.Zero([]))
        self.assertEqual(cm.exception.code, 340, msg='list of Equations is bad')
    def test_commutebundle_sanity1(self):
        with self.assertRaises(SystemExit) as cm:
            cb = CommuteBundle.CommuteBundle(1, 0, [], 'notch', Z.Zero([]))
        self.assertEqual(cm.exception.code, 340, msg='list of Chains is bad')
    def test_commutebundle_sanity2(self):
        with self.assertRaises(SystemExit) as cm:
            cb = CommuteBundle.CommuteBundle(1, 0, [], [], [])
        self.assertEqual(cm.exception.code, 340, msg='zero object is bad')
    def test_commutebundle_sanity3(self):
        eq1, ch1 = self.prepareequation()
        with self.assertRaises(SystemExit) as cm:
            cb = CommuteBundle.CommuteBundle(1, 0, [eq1], [ch1, eq1], Z.Zero([]))
        self.assertEqual(cm.exception.code, 342, msg='list of chains has non-chains')
    def test_commutebundle_sanity4(self):
        eq1, ch1 = self.prepareequation()
        with self.assertRaises(SystemExit) as cm:
            cb = CommuteBundle.CommuteBundle(1, 0, [eq1, ch1], [ch1], Z.Zero([]))
        self.assertEqual(cm.exception.code, 341, msg='list of Equations has non-Equation')
    def test_commutebundle_sanity5(self):
        eq1, ch1 = self.prepareequation()
        with self.assertRaises(SystemExit) as cm:
            cb = CommuteBundle.CommuteBundle(1, 0, [], [], Z.Zero([]))
        self.assertEqual(cm.exception.code, 343, msg='empty nothing to do')
