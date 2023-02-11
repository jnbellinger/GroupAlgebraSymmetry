''' General routines '''
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
from Builder import Fraction as F
from Builder import Element as E
from Builder import Equation as Eq
from Builder import Equivalence
from Builder import Zero as Z
from Builder import Chain

#Table

class test_routines(unittest.TestCase):
    #
    def test_routine_list_size_ok(self):
        table = G.Table([0, 1, 2, 1, 2, 0, 2, 0, 1])
        maker = GenerateEquationsFromTable.GenerateEquationsFromTable(table)
        maker.generateEquationList()
        solver = SolveEquations.SolveEquations(maker.GiveSize(), maker.GiveEquations(), maker.GiveZeros())
        solver.ProcessEquationList()
        self.assertEqual(len(solver.GiveEquations()), 0, msg='Should have 0 independent equations')
    def test_routine_bad_arg(self):
        with self.assertRaises(SystemExit) as cm:
            table = GenerateEquationsFromTable.GenerateEquationsFromTable('table')
        self.assertEqual(cm.exception.code, 350, msg='SolveEquations wants a Table')
    def test_routine_find_key_max(self):
        table = G.Table([0, 1, 2, 1, 2, 0, 2, 0, 1])
        maker = GenerateEquationsFromTable.GenerateEquationsFromTable(table)
        maker.generateEquationList()
        solver = SolveEquations.SolveEquations(maker.GiveSize(), maker.GiveEquations(), maker.GiveZeros())
        solver.ProcessEquationList()
        #self.assertEqual(str(keylist), '[0={1_1}(2/1)+{2_2}(-1/1), 0={1_1}(1/1)+{2_2}(1/1), 0={2_2}(2/1)+{1_1}(-1/1)]', msg='Key list should have 3 Equations')
        self.assertIsNone(solver.getSameKey(), msg='Key list should be empty')
    #
    def test_routine_makechain_noteq(self):
        table = G.Table([0, 1, 2, 1, 2, 0, 2, 0, 1])
        maker = GenerateEquationsFromTable.GenerateEquationsFromTable(table)
        maker.generateEquationList()
        solver = SolveEquations.SolveEquations(maker.GiveSize(), maker.GiveEquations(), maker.GiveZeros())
        with self.assertRaises(SystemExit) as cm:
            table = solver.makeChain('list')
        self.assertEqual(cm.exception.code, 355, msg='SolveEquations:makeChain wants an Equation')
    def test_routine_makechain_wrongsize(self):
        table = G.Table([0, 1, 2, 1, 2, 0, 2, 0, 1])
        maker = GenerateEquationsFromTable.GenerateEquationsFromTable(table)
        maker.generateEquationList()
        solver = SolveEquations.SolveEquations(maker.GiveSize(), maker.GiveEquations(), maker.GiveZeros())
        n1 = N.Name(1, 3, 4)
        n2 = N.Name(3, 1, 4)
        n3 = N.Name(3, 3, 4)
        f1 = F.Fraction(1, 3)
        f2 = F.Fraction(2, 3)
        f3 = F.Fraction(4, 3)
        e1 = E.Element(n1, f1)
        e2 = E.Element(n2, f2)
        e3 = E.Element(n3, f3)
        eq1 = Eq.Equation([e1, e2, e3])
        answer = solver.makeChain(eq1)
        self.assertIsNone(answer, msg='Should fail, too many Elements')
    def test_routine_makechain_ok(self):
        table = G.Table([0, 1, 2, 1, 2, 0, 2, 0, 1])
        maker = GenerateEquationsFromTable.GenerateEquationsFromTable(table)
        maker.generateEquationList()
        solver = SolveEquations.SolveEquations(maker.GiveSize(), maker.GiveEquations(), maker.GiveZeros())
        n1 = N.Name(1, 3, 4)
        n2 = N.Name(3, 1, 4)
        f1 = F.Fraction(1, 3)
        f2 = F.Fraction(2, 3)
        e1 = E.Element(n1, f1)
        e2 = E.Element(n2, f2)
        eq1 = Eq.Equation([e1, e2])
        answer = solver.makeChain(eq1)
        banswer = isinstance(answer, Chain.Chain)
        self.assertTrue(answer, msg='Should be OK, 2 Elements')
    #
    def test_routine_6group_make(self):
        table = G.Table([ 0, 1, 2, 3, 4, 5, 1, 2, 0, 4, 5, 3, 2, 0, 1, 5, 3, 4, 3, 5, 4, 0, 2, 1, 4, 3, 5, 1, 0, 2, 5, 4, 3, 2, 1, 0])
        maker = GenerateEquationsFromTable.GenerateEquationsFromTable(table)
        maker.generateEquationList()
        solver = SolveEquations.SolveEquations(maker.GiveSize(), maker.GiveEquations(), maker.GiveZeros())
        solver.ProcessEquationList()
        solver.bulkInfo()
        #print('make', len(solver.ListOfEquivalences))
        bool1 = str(solver.ListOfEquivalences[0]) == '{1_5}(1)={1_4}(-1)+{1_3}(-1)'
        #bool1 = str(solver.ListOfEquations[0]) == '0={1_4}(1)+{1_5}(1)+{1_3}(1)'
        bool2 = str(solver.zeros) == '{0_0},{0_1},{0_2},{0_3},{0_4},{0_5},{1_0},{1_1},{1_2},{2_0},{2_1},{2_2},{3_0},{3_3},{4_0},{4_4},{5_0},{5_5}'
        #
        unac, total = solver.unaccounted()
        bool3 = unac == 0
        self.assertTrue(bool1 and bool2 and bool3, msg='Should have 1 Equation left and 18 zeros and nothing unaccounted for ' + str(bool1) + ' ' + str(bool2) + ' ' + str(bool3) + ' ' )
    #
    # I have to go through the headache of setting up fake versions of MakeEquations for each
    # of the routines in turn.  Painful.
    def test_routine_6group_turneq(self):
        table = G.Table([ 0, 1, 2, 3, 4, 5, 1, 2, 0, 4, 5, 3, 2, 0, 1, 5, 3, 4, 3, 5, 4, 0, 2, 1, 4, 3, 5, 1, 0, 2, 5, 4, 3, 2, 1, 0])
        maker = GenerateEquationsFromTable.GenerateEquationsFromTable(table)
        maker.generateEquationList()
        solver = SolveEquations.SolveEquations(maker.GiveSize(), maker.GiveEquations(), maker.GiveZeros())
        # NOW DO VERY BAD THINGS TO THIS
        eqq = Eq.Equation([E.Element(N.Name(1, 2, 6),F.Fraction(1,1)), E.Element(N.Name(1,3,6),F.Fraction(2,1)),E.Element(N.Name(1,4,6),F.Fraction(3,1))])
        eqr = Eq.Equation([E.Element(N.Name(2, 2, 6),F.Fraction(1,1)), E.Element(N.Name(2,3,6),F.Fraction(2,1)),E.Element(N.Name(2,4,6),F.Fraction(3,1))])
        solver.ListOfEquations.append(eqq)
        solver.ListOfEquations.append(eqr)
        solver.ProcessEquationList()
        # Changed the algorithm; intermediate stages different
        #solver.turnEquationsToEquivalence()
        #self.assertEqual(str(solver.ListOfEquivalences), '[{1_5}(1)={1_3}(-1/3), {1_4}(1)={1_3}(-2/3), {1_4}(1)={1_5}(-1)+{1_3}(-1)]', msg='Should have 3')
        #
        solver.reduceEquationsToEquivalences()
        self.assertEqual(str(solver.ListOfEquivalences), '[{1_3}(1)={1_5}(-3)]', msg='Only 1 left')
    def test_routine_6group_turneq_0(self):
        table = G.Table([ 0, 1, 2, 3, 4, 5, 1, 2, 0, 4, 5, 3, 2, 0, 1, 5, 3, 4, 3, 5, 4, 0, 2, 1, 4, 3, 5, 1, 0, 2, 5, 4, 3, 2, 1, 0])
        maker = GenerateEquationsFromTable.GenerateEquationsFromTable(table)
        maker.generateEquationList()
        solver = SolveEquations.SolveEquations(maker.GiveSize(), maker.GiveEquations(), maker.GiveZeros())
        solver.ProcessEquationList()
        # NOW DO VERY BAD THINGS TO THIS
        #solver.ListOfEquations.pop(0)
        with self.assertRaises(SystemExit) as cm:
            solver.turnEquationsToEquivalence()
        self.assertEqual(cm.exception.code, 358, msg='Should have failed, no Equations')
        #
    def test_routine_6group_make_2(self):
        table = G.Table([ 0, 1, 2, 3, 4, 5, 1, 2, 0, 4, 5, 3, 2, 0, 1, 5, 3, 4, 3, 5, 4, 0, 2, 1, 4, 3, 5, 1, 0, 2, 5, 4, 3, 2, 1, 0])
        maker = GenerateEquationsFromTable.GenerateEquationsFromTable(table)
        maker.generateEquationList()
        solver = SolveEquations.SolveEquations(maker.GiveSize(), maker.GiveEquations(), maker.GiveZeros())
        solver.ProcessEquationList()
        okzero = str(solver.zeros) == '{0_0},{0_1},{0_2},{0_3},{0_4},{0_5},{1_0},{1_1},{1_2},{2_0},{2_1},{2_2},{3_0},{3_3},{4_0},{4_4},{5_0},{5_5}'
        okch = str(solver.GiveChains()[0]) == '{1_5}(1)={2_5}(-1)={5_1}(1)={5_2}(-1)'
        eqstr = str(solver.GiveEquivalences()[0])
        okeq = ( ( eqstr == '{1_4}(1)={1_5}(-1)+{1_3}(-1)' ) or
                ( eqstr == '{1_4}(1)={1_3}(-1)+{1_5}(-1)' ) or
                (eqstr == '{1_5}(1)={1_4}(-1)+{1_3}(-1)' ) or
                (eqstr == '{1_5}(1)={1_3}(-1)+{1_4}(-1)' ) or
                (eqstr == '{1_3}(1)={1_5}(-1)+{1_4}(-1)' ) or
                (eqstr == '{1_3}(1)={1_4}(-1)+{1_5}(-1)' ))
        #okeq = str(solver.GiveEquivalences()[0]) == '{1_4}(1)={1_5}(-1)+{1_3}(-1)'
        self.assertTrue(okzero and okch and okeq, msg='Demand that the Equivalence, Chain, and Zeros be OK okzero, okch, okeq ' + str(okzero) + ' ' + str(okch) + ' ' + str(okeq))
    #
    def test_routine_6group_getchain(self):
        table = G.Table([ 0, 1, 2, 3, 4, 5, 1, 2, 0, 4, 5, 3, 2, 0, 1, 5, 3, 4, 3, 5, 4, 0, 2, 1, 4, 3, 5, 1, 0, 2, 5, 4, 3, 2, 1, 0])
        maker = GenerateEquationsFromTable.GenerateEquationsFromTable(table)
        maker.generateEquationList()
        solver = SolveEquations.SolveEquations(maker.GiveSize(), maker.GiveEquations(), maker.GiveZeros())
        solver.ProcessEquationList()
        cl = solver.GiveChains()
        self.assertEqual(len(cl), 4, msg='Should have 4 Chains, one cancelable by Equivalence')
    def test_routine_givekey(self):
        table = G.Table([ 0, 1, 2, 3, 4, 5, 1, 2, 0, 4, 5, 3, 2, 0, 1, 5, 3, 4, 3, 5, 4, 0, 2, 1, 4, 3, 5, 1, 0, 2, 5, 4, 3, 2, 1, 0])
        maker = GenerateEquationsFromTable.GenerateEquationsFromTable(table)
        maker.generateEquationList()
        solver = SolveEquations.SolveEquations(maker.GiveSize(), maker.GiveEquations(), maker.GiveZeros())
        solver.ProcessEquationList()
        keylist = solver.giveKeys()
        #self.assertEqual(str(keylist[0]), '{1_3}{1_4}{1_5}', msg='Should have gotten a list of Keys:  NOT sure this matters, algo changed')
        self.assertEqual(len(keylist), 0, msg='Not relevant anymore')
    #
    # Test the new doNextReduceEquationToEquivalence stuff
    def test_routine_donextreduce(self):
        table = G.Table([ 0, 1, 2, 3, 4, 5, 1, 2, 0, 4, 5, 3, 2, 0, 1, 5, 3, 4, 3, 5, 4, 0, 2, 1, 4, 3, 5, 1, 0, 2, 5, 4, 3, 2, 1, 0])
        maker = GenerateEquationsFromTable.GenerateEquationsFromTable(table)
        maker.generateEquationList()
        solver = SolveEquations.SolveEquations(maker.GiveSize(), maker.GiveEquations(), maker.GiveZeros())
        # OK, that was just the setup to make sure I had some handy framework.  Now wipe it and 
        # fill with new stuff.
        solver.zeros.zerolist.clear()
        solver.ListOfEquations.clear()
        solver.ListOfEquivalences.clear()
        solver.groupSize = 20
        names = []
        fracs = []
        elems = []
        for i in range(9):
            names.append(N.Name(i, 1, 20))
            fracs.append(F.Fraction(1,1))
            elems.append(E.Element(names[-1], fracs[-1]))
        for i in range(9):
            names.append(N.Name(i, 2, 20))
            elems.append(E.Element(names[i+9], fracs[i]))
        eq1 = Eq.Equation([copy.deepcopy(elems[0]), copy.deepcopy(elems[1]), copy.deepcopy(elems[2])])
        eq2 = Eq.Equation([copy.deepcopy(elems[3]), copy.deepcopy(elems[4]), copy.deepcopy(elems[2])])
        eq3 = Eq.Equation([copy.deepcopy(elems[5]), copy.deepcopy(elems[1]), copy.deepcopy(elems[3])])
        eq4 = Eq.Equation([copy.deepcopy(elems[6]), copy.deepcopy(elems[1]), copy.deepcopy(elems[3])])
        solver.ListOfEquations.append(eq1)
        solver.ListOfEquations.append(eq2)
        solver.ListOfEquations.append(eq3)
        solver.ListOfEquations.append(eq4)
        for i in range(7):
            solver.chainlist.append(Chain.Chain([copy.deepcopy(elems[i]), copy.deepcopy(elems[i+9]) ]))
        # In the end I expect 4 Equivalences:
        # elems[0] = elems[3] + elems[6] - elems[2]     {0_1}(1) = {3_1}(1) + {6_1}(1) + {2_1}(-1)
        # elems[4] = -elems[3] - elems[2]               {4_1}(1) = {3_1}(-1) + {2_1}(-1)
        # elems[5] = elems[6]                           {5_1}(1) = {6_1}(1)
        # elems[1] = -elems[3] - elems[6]               {1_1}(1) = {3_1}(-1) + {6_1}(-1)
        # After taking feedback into account:
        # First =>        {0_1}(1) = {3_1}(2) + {6_1}(1) + {4_1}(1)
        # Second =>       {2_1}(1) = {3_1}(-1) + {4_1}(-1)
        # Third =>        {5_1}(1) = {6_1}(1)
        # Fourth =>       {1_1}(1) = {6_1}(-1) + {3_1}(-1)
        #for entry in solver.GiveEquations():
        #    print('FFF', entry)
        #solver.turnEquationsToEquivalence()  # original
        solver.reduceEquationsToEquivalences()  # new
        #for entry in solver.GiveEquivalences():
        #    print('EEE', entry)
        self.assertEqual(str(solver.GiveEquivalences()[0]), '{0_1}(1)={3_1}(2)+{4_1}(1)+{6_1}(1)', msg='Equivalences w/ second algorithm')
    #
    def test_routine_reduceequiv_ok(self):
        table = G.Table([ 0, 1, 2, 3, 4, 5, 1, 2, 0, 4, 5, 3, 2, 0, 1, 5, 3, 4, 3, 5, 4, 0, 2, 1, 4, 3, 5, 1, 0, 2, 5, 4, 3, 2, 1, 0])
        maker = GenerateEquationsFromTable.GenerateEquationsFromTable(table)
        maker.generateEquationList()
        solver = SolveEquations.SolveEquations(maker.GiveSize(), maker.GiveEquations(), maker.GiveZeros())
        # OK, have framework, now hack it to be able to test the function
        n1 = N.Name(2, 3, 4)
        n2 = N.Name(2, 1, 4)
        n3 = N.Name(2, 2, 4)
        n4 = N.Name(2, 0, 4)
        n5 = N.Name(0, 3, 4)
        f1 = F.Fraction(1, 3)
        f2 = F.Fraction(2, 3)
        f3 = F.Fraction(3, 3)
        f4 = F.Fraction(4, 3)
        e1 = E.Element(n1, f1)
        e2 = E.Element(n2, f2)
        e3 = E.Element(n3, f3)
        e4 = E.Element(n4, f4)
        e5 = E.Element(n2, f4)
        eq1 = Eq.Equation([e1, e2, e3])
        eqv1 = Equivalence.Equivalence(eq1, e1)
        eqv2 = Equivalence.Equivalence(eq1, e2)
        solver.ListOfEquivalences.clear()
        solver.ListOfEquivalences.append(copy.deepcopy(eqv1))
        solver.reduceEquivalences(eqv2)
        self.assertEqual(len(solver.ListOfEquivalences), 0, msg='Duplicate should be gone')
    def test_routine_reduceequiv_diff(self):
        table = G.Table([ 0, 1, 2, 3, 4, 5, 1, 2, 0, 4, 5, 3, 2, 0, 1, 5, 3, 4, 3, 5, 4, 0, 2, 1, 4, 3, 5, 1, 0, 2, 5, 4, 3, 2, 1, 0])
        maker = GenerateEquationsFromTable.GenerateEquationsFromTable(table)
        maker.generateEquationList()
        solver = SolveEquations.SolveEquations(maker.GiveSize(), maker.GiveEquations(), maker.GiveZeros())
        # OK, have framework, now hack it to be able to test the function
        n1 = N.Name(2, 3, 4)
        n2 = N.Name(2, 1, 4)
        n3 = N.Name(2, 2, 4)
        n4 = N.Name(2, 0, 4)
        n5 = N.Name(0, 3, 4)
        f1 = F.Fraction(1, 3)
        f2 = F.Fraction(2, 3)
        f3 = F.Fraction(3, 3)
        f4 = F.Fraction(4, 3)
        e1 = E.Element(n1, f1)
        e2 = E.Element(n2, f2)
        e3 = E.Element(n3, f3)
        e4 = E.Element(n4, f4)
        e5 = E.Element(n5, f4)
        eq1 = Eq.Equation([e1, e2, e3])
        eq2 = Eq.Equation([e1, e5, e3])
        eqv1 = Equivalence.Equivalence(eq1, e1)
        eqv2 = Equivalence.Equivalence(eq2, e5)
        solver.ListOfEquivalences.clear()
        solver.ListOfEquivalences.append(copy.deepcopy(eqv1))
        solver.reduceEquivalences(eqv2)
        self.assertEqual(len(solver.ListOfEquivalences), 1, msg='Not a duplicate')
    def test_routine_reduceequiv_notok(self):
        table = G.Table([ 0, 1, 2, 3, 4, 5, 1, 2, 0, 4, 5, 3, 2, 0, 1, 5, 3, 4, 3, 5, 4, 0, 2, 1, 4, 3, 5, 1, 0, 2, 5, 4, 3, 2, 1, 0])
        maker = GenerateEquationsFromTable.GenerateEquationsFromTable(table)
        maker.generateEquationList()
        solver = SolveEquations.SolveEquations(maker.GiveSize(), maker.GiveEquations(), maker.GiveZeros())
        # OK, have framework, now hack it to be able to test the function
        n1 = N.Name(2, 3, 4)
        n2 = N.Name(2, 1, 4)
        n3 = N.Name(2, 2, 4)
        n4 = N.Name(2, 0, 4)
        n5 = N.Name(0, 3, 4)
        f1 = F.Fraction(1, 3)
        f2 = F.Fraction(2, 3)
        f3 = F.Fraction(3, 3)
        f4 = F.Fraction(4, 3)
        e1 = E.Element(n1, f1)
        e2 = E.Element(n2, f2)
        e3 = E.Element(n3, f3)
        e4 = E.Element(n4, f4)
        e5 = E.Element(n2, f4)
        eq1 = Eq.Equation([e1, e2, e3])
        eqv1 = Equivalence.Equivalence(eq1, e1)
        solver.ListOfEquivalences.clear()
        solver.ListOfEquivalences.append(copy.deepcopy(eqv1))
        with self.assertRaises(SystemExit) as cm:
            solver.reduceEquivalences(e5)
        self.assertEqual(cm.exception.code, 360, msg='Should have failed, not Equivalence')
