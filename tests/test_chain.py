''' Test suite for Chain '''
import os
import sys
import copy
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Builder import Fraction as F
from Builder import Name as N
from Builder import Element as E
from Builder import Chain as C
import unittest

class test_chain(unittest.TestCase):
    #
    def create_chain(self):
        nam = []
        fra = []
        ele = []
        for i in range(3):
            for j in range(3):
                nam.append(N.Name(i, j, 6))
                fra.append(F.Fraction(j+1, i+1))
                ele.append(E.Element(nam[-1], fra[-1]))
        return C.Chain(ele), nam, fra, ele
    #
    def create_extras(self):
        nam = []
        fra = []
        ele = []
        for i in range(3):
            for j in range(3):
                nam.append(N.Name(3 + i, 3 + j, 6))
                fra.append(F.Fraction(j+1, i+1))
                ele.append(E.Element(nam[-1], fra[-1]))
        return C.Chain(ele), nam, fra, ele
    def create_extras_over_in(self):
        nam = []
        fra = []
        ele = []
        for i in range(3):
            for j in range(3):
                nam.append(N.Name(1 + i, 1 + j, 6))
                fra.append(F.Fraction(j+1, i+1))
                ele.append(E.Element(nam[-1], fra[-1]))
        return C.Chain(ele), nam, fra, ele
    #
    def test_chain_init(self):
        # Also tests __str__
        ch1, nam, fra, ele = self.create_chain()
        self.assertEqual(str(ch1), '{0_0}(1)={0_1}(2)={0_2}(3)={1_0}(1/2)={1_1}(1)={1_2}(3/2)={2_0}(1/3)={2_1}(2/3)={2_2}(1)', msg='Did not insert all elements')
    def test_chain_init_nolist(self):
        nam = N.Name(1, 3, 5)
        fra = F.Fraction(3, 1)
        ele = E.Element(nam, fra)
        with self.assertRaises(SystemExit) as cm:
            ch1 = C.Chain(ele)
        self.assertEqual(cm.exception.code, 100, msg='Should have caught bad arg not list')
    def test_chain_init_noelelist(self):
        nam = N.Name(1, 3, 5)
        fra = F.Fraction(3, 1)
        ele = E.Element(nam, fra)
        with self.assertRaises(SystemExit) as cm:
            ch1 = C.Chain([nam])
        self.assertEqual(cm.exception.code, 101, msg='Should have caught list not Elements')
    def test_chain_init_withdups(self):
        nam = []
        fra = []
        ele = []
        for i in range(3):
            for j in range(3):
                nam.append(N.Name(i, j, 6))
                fra.append(F.Fraction(j+1, i+1))
                ele.append(E.Element(nam[-1], fra[-1]))
        elx = E.Element(N.Name(1, 1, 6), F.Fraction(5, 6))
        ele.append(elx)
        with self.assertRaises(SystemExit) as cm:
            ch1 = C.Chain(ele)
        self.assertEqual(cm.exception.code, 102, msg='Should have caught duplicate Element')
    #
    def test_chain_count(self):
        ch1, nam, fra, ele = self.create_chain()
        self.assertEqual(ch1.count(), 9, msg='Right number of Elements, but failed')
    def test_chain_key(self):
        ch1, nam, fra, ele = self.create_chain()
        self.assertEqual(str(ch1.Key()), '{0_0}{0_1}{0_2}{1_0}{1_1}{1_2}{2_0}{2_1}{2_2}', msg='Should have 9 keys')
    def test_chain_print_1(self):
        ch1, nam, fra, ele = self.create_chain()
        # DO BAD THINGS
        for i in range(8):
            ch1.chainlist.pop(-1)
        self.assertEqual(str(ch1), '{0_0}(1)', msg='Should have 1 key')
    def test_chain_print_0(self):
        ch1, nam, fra, ele = self.create_chain()
        # DO BAD THINGS
        for i in range(9):
            ch1.chainlist.pop(-1)
        self.assertEqual(str(ch1), ' 0 ', msg='Should have no key')
    #
    def test_chain_repr(self):
        ch1, nam, fra, ele = self.create_chain()
        self.assertEqual(repr(ch1), '{0_0}(1)={0_1}(2)={0_2}(3)={1_0}(1/2)={1_1}(1)={1_2}(3/2)={2_0}(1/3)={2_1}(2/3)={2_2}(1)', msg='Did not insert all elements')
    #
    def test_chain_countpresent(self):
        ch1, nam, fra, ele = self.create_chain()
        ele2 = []
        for i in range(9):
            ele2.append(E.Element(nam[i], fra[i]))
        self.assertEqual(ch1.countpresent(ele2), 9, msg='Should be 9, duplicate list')
    def test_chain_countpresent_1(self):
        ch1, nam, fra, ele = self.create_chain()
        ele2 = [ele[2]]
        self.assertEqual(ch1.countpresent(ele2), 1, msg='Should be 1 duplicate')
    def test_chain_countpresent_0(self):
        ch1, nam, fra, ele = self.create_chain()
        ele2 = [E.Element(N.Name(5, 5, 6), F.Fraction(1, 100))]
        self.assertEqual(ch1.countpresent(ele2), 0, msg='Should be 0 duplicate')
    def test_chain_countpresent_name(self):
        ch1, nam, fra, ele = self.create_chain()
        ele2 = []
        for i in range(9):
            ele2.append(nam[i])
        self.assertEqual(ch1.countpresent(ele2), 9, msg='Should be 9, duplicate list')
    def test_chain_countpresent_1_name(self):
        ch1, nam, fra, ele = self.create_chain()
        ele2 = [nam[2]]
        self.assertEqual(ch1.countpresent(ele2), 1, msg='Should be 1 duplicate')
    def test_chain_countpresent_0_name(self):
        ch1, nam, fra, ele = self.create_chain()
        ele2 = [N.Name(5, 5, 6)]
        self.assertEqual(ch1.countpresent(ele2), 0, msg='Should be 0 duplicate')
    def test_chain_countpresent_bad(self):
        ch1, nam, fra, ele = self.create_chain()
        ele2 = [fra[2]]
        with self.assertRaises(SystemExit) as cm:
            x = ch1.countpresent(ele2)
        self.assertEqual(cm.exception.code, 108, msg='Should have caught non-Element/Name in list')
    def test_chain_countpresent_element(self):
        ch1, nam, fra, ele = self.create_chain()
        self.assertEqual(ch1.countpresent(ele[2]), 1, msg='Should have one overlap')
    def test_chain_countpresent_name_a(self):
        ch1, nam, fra, ele = self.create_chain()
        self.assertEqual(ch1.countpresent(nam[2]), 1, msg='Should have one overlap')
    def test_chain_countpresent_name_b(self):
        ch1, nam, fra, ele = self.create_chain()
        ele2 = N.Name(5, 4, 6)
        self.assertEqual(ch1.countpresent(ele2), 0, msg='Should have 0 overlap')
    #
    def test_chain_countpresent_bad_single(self):
        ch1, nam, fra, ele = self.create_chain()
        with self.assertRaises(SystemExit) as cm:
            x = ch1.countpresent(fra[2])
        self.assertEqual(cm.exception.code, 107, msg='Should have caught non-Element/Name ')
    #
    def test_chain_add_two(self):
        ch1, nam, fra, ele = self.create_chain()
        ch2, nam2, fra2, ele2 = self.create_extras()
        ele0 = E.Element(nam[0], F.Fraction(2, 1))
        ch1.add([ele0, ele2[1]])
        self.assertEqual(str(ch1), '{0_0}(1)={0_1}(2)={0_2}(3)={1_0}(1/2)={1_1}(1)={1_2}(3/2)={2_0}(1/3)={2_1}(2/3)={2_2}(1)={3_4}(1)', msg='Failed to add an Element')
    #
    def test_chain_add_notlist(self):
        ch1, nam, fra, ele = self.create_chain()
        with self.assertRaises(SystemExit) as cm:
            ch1.add(ele[1])
        self.assertEqual(cm.exception.code, 103, msg='Only add *list* of Elements (or Chain)')
    def test_chain_add_list_notelement(self):
        ch1, nam, fra, ele = self.create_chain()
        with self.assertRaises(SystemExit) as cm:
            ch1.add(nam)
        self.assertEqual(cm.exception.code, 104, msg='Only add list of *Elements* (or Chain)')
    def test_chain_add_list_dupe_element(self):
        ch1, nam, fra, ele = self.create_chain()
        nam.append(N.Name(0, 0, 6))
        fra.append(F.Fraction(1, 1))
        ele.append(E.Element(nam[-1], fra[-1]))
        with self.assertRaises(SystemExit) as cm:
            ch1.add(ele)
        self.assertEqual(cm.exception.code, 105, msg='No duplicate *Elements* in list to add')
    def test_chain_add_list_nooverlap(self):
        ch1, nam, fra, ele = self.create_chain()
        ch2, nam2, fra2, ele2 = self.create_extras()
        with self.assertRaises(SystemExit) as cm:
            ch1.add(ele2)
        self.assertEqual(cm.exception.code, 106, msg='Only add overlapping list')
    def test_chain_add_list_2overlap_ok(self):
        ch1, nam, fra, ele = self.create_chain()
        ch2, nam2, fra2, ele2 = self.create_extras()
        ele3 = [copy.deepcopy(ele[2]), copy.deepcopy(ele[1]), copy.deepcopy(ele2[2])]
        ch1.add(ele3)
        self.assertEqual(ch1.count(), 10, msg='Did not add new element')
    def test_chain_add_list_2overlap_bad(self):
        ch1, nam, fra, ele = self.create_chain()
        ch2, nam2, fra2, ele2 = self.create_extras()
        elx = copy.deepcopy(ele[1])
        elx.fraction.mutemultiply(F.Fraction(1, 2))
        ele3 = [copy.deepcopy(ele[2]), elx, copy.deepcopy(ele2[2])]
        ch1.add(ele3)
        self.assertTrue(ch1.isZero(), msg='All zero now')
    def test_chain_add_list_2overlap_bad2(self):
        ch1, nam, fra, ele = self.create_chain()
        ch2, nam2, fra2, ele2 = self.create_extras()
        elx = copy.deepcopy(ele[1])
        elx.fraction.mutemultiply(F.Fraction(1, 2))
        ele3 = [copy.deepcopy(ele[2]), elx, copy.deepcopy(ele2[2])]
        ch1.add(ele3)
        self.assertEqual(ch1.count(), 10, msg='Did not add new element')
    def test_chain_add_chain_ok(self):
        ch1, nam, fra, ele = self.create_chain()
        ch2, nam2, fra2, ele2 = self.create_extras()
        elx = copy.deepcopy(ele[1])
        #elx.fraction.mutemultiply(F.Fraction(1, 2))
        ele3 = [copy.deepcopy(ele[2]), elx, copy.deepcopy(ele2[2])]
        ch2.add(ele3)
        ch1.add(ch2)
        self.assertEqual(ch1.count(), 18, msg='Did not add new chain')
    def test_chain_add_chain_notok(self):
        ch1, nam, fra, ele = self.create_chain()
        ch2, nam2, fra2, ele2 = self.create_extras()
        elx = copy.deepcopy(ele[1])
        elx.fraction.mutemultiply(F.Fraction(1, 2))
        ele3 = [copy.deepcopy(ele[2]), elx, copy.deepcopy(ele2[2])]
        ch2.add(ele3)
        ch1.add(ch2)
        self.assertEqual(ch1.count(), 10, msg='Should not add new chain')
    def test_chain_add_chain_zero(self):
        ch1, nam, fra, ele = self.create_chain()
        ch2, nam2, fra2, ele2 = self.create_extras()
        elx = copy.deepcopy(ele[1])
        #elx.fraction.mutemultiply(F.Fraction(1, 2))
        ele3 = [copy.deepcopy(ele[2]), elx, copy.deepcopy(ele2[2])]
        ch2.add(ele3)
        # DO BAD THING
        ch2.iszero = True
        ch1.add(ch2)
        self.assertEqual(ch1.count(), 9, msg='Should not add new chain')
    #
    def test_chain_setzero(self):
        ch1, nam, fra, ele = self.create_chain()
        origval = ch1.isZero()
        ch1.setZero()
        newval = ch1.isZero()
        self.assertTrue(((not origval) and newval), msg='Should have changed zero from False to True')
    #
    def test_chain_isusedup(self):
        ch1, nam, fra, ele = self.create_chain()
        origval = ch1.isUsedUp()
        ch1.setUsedUp()
        newval = ch1.isUsedUp()
        self.assertTrue(((not origval) and newval), msg='Should have changed used-up from False to True')
    #
    def test_chain_merge_nooverlap(self):
        ch1, nam, fra, ele = self.create_chain()
        ch2, nam2, fra2, ele2 = self.create_extras()
        answer = ch1.merge(ch2)
        self.assertEqual(answer, C.Chain.NOOP, msg='Should not merge, no overlap')
    def test_chain_merge_badarg(self):
        ch1, nam, fra, ele = self.create_chain()
        ch2, nam2, fra2, ele2 = self.create_extras()
        with self.assertRaises(SystemExit) as cm:
            ch1.merge(fra)
        self.assertEqual(cm.exception.code, 109, msg='Needs a Chain, why did it not fail?')
    def test_chain_merge_alreadyused(self):
        ch1, nam, fra, ele = self.create_chain()
        ch2, nam2, fra2, ele2 = self.create_extras()
        ch2.setUsedUp()
        answer = ch1.merge(ch2)
        self.assertEqual(answer, C.Chain.NOOP, msg='Other used up, should not merge')
    def test_chain_merge_selfalreadyused(self):
        ch1, nam, fra, ele = self.create_chain()
        ch2, nam2, fra2, ele2 = self.create_extras()
        ch1.setUsedUp()
        answer = ch1.merge(ch2)
        self.assertEqual(answer, C.Chain.NOOP, msg='Self used up, should not merge')
    #
    def test_chain_merge_overlap_incon_1(self):
        ch1, nam, fra, ele = self.create_chain()
        ch2, nam2, fra2, ele2 = self.create_extras_over_in()
        answer = ch1.merge(ch2)
        self.assertTrue(ch1.isZero() and ch2.isZero, msg='Should be inconsistent and zeroed!')
    def test_chain_merge_overlap_cons_one(self):
        ch1, nam, fra, ele = self.create_chain()
        ch2, nam2, fra2, ele2 = self.create_extras()
        ch2.add([ele2[2], ele[2]])
        answer = ch1.merge(ch2)
        self.assertEqual(answer, C.Chain.MERGED, msg='Should have merged, one overlap value')
    def test_chain_merge_overlap_cons_many_name(self):
        ch1, nam, fra, ele = self.create_chain()
        ch2, nam2, fra2, ele2 = self.create_chain()
        ch3, nam3, fra3, ele3 = self.create_extras()
        ch2.add([ele2[2], ele3[2]])
        answer = ch1.merge(ch2)
        self.assertEqual(str(ch1), '{0_0}(1)={0_1}(2)={0_2}(3)={1_0}(1/2)={1_1}(1)={1_2}(3/2)={2_0}(1/3)={2_1}(2/3)={2_2}(1)={3_5}(9/3)', msg='New term should have been added')
    def test_chain_merge_overlap_cons_many_answer(self):
        ch1, nam, fra, ele = self.create_chain()
        ch2, nam2, fra2, ele2 = self.create_chain()
        ch3, nam3, fra3, ele3 = self.create_extras()
        ch2.add([ele2[2], ele3[2]])
        answer = ch1.merge(ch2)
        self.assertTrue(answer == C.Chain.MERGED, msg='Should have merged, many overlap values')
    def test_chain_merge_overlap_incon_2(self):
        ch1, nam, fra, ele = self.create_chain()
        ch2, nam2, fra2, ele2 = self.create_chain()
        # DO BAD THING!
        ch2.chainlist[2].fraction.mutemultiply(F.Fraction(1, 2))
        old1 = ch1.isZero()
        old2 = ch2.isZero()
        answer = ch1.merge(ch2)
        new1 = ch1.isZero()
        new2 = ch2.isZero()
        check = answer == C.Chain.ZEROED
        self.assertTrue((not old1 and not old2) and new1 and new2 and check, msg='Chains should both have been zeroed')
    def test_chain_merge_overlap_cons_one_zero(self):
        ch1, nam, fra, ele = self.create_chain()
        ch2, nam2, fra2, ele2 = self.create_extras()
        ch2.add([ele2[2], ele[2]])
        # DO BAD THING!
        ch1.chainlist[2].fraction.muteforceZero()
        with self.assertRaises(SystemExit) as cm:
            answer = ch1.merge(ch2)
        self.assertEqual(cm.exception.code, 110, msg='Chain must not have a zero in it')
    def test_chain_merge_overlap_cons_one_zero_2(self):
        ch1, nam, fra, ele = self.create_chain()
        ch2, nam2, fra2, ele2 = self.create_extras()
        ch2.add([ele2[2], ele[2], ele[3]])
        # DO BAD THING!
        ch1.chainlist[2].fraction.muteforceZero()
        with self.assertRaises(SystemExit) as cm:
            answer = ch1.merge(ch2)
        self.assertEqual(cm.exception.code, 111, msg='Local Chain must not have a zero in it')
    #
    def test_chain_contents(self):
        ch1, nam, fra, ele = self.create_chain()
        self.assertEqual(ch1.contents(), ele, msg='Should be equal to what made it')
    #
    def test_chain_ok_neg(self):
        ele = [E.Element(N.Name(0, 2, 4), F.Fraction(-2, 1)), E.Element(N.Name(1, 2, 4), F.Fraction(-1, 1))]
        ele2 = [E.Element(N.Name(0, 2, 4), F.Fraction(1, 1)), E.Element(N.Name(1, 2, 4), F.Fraction(1, 2))]
        cha = C.Chain(ele)
        self.assertEqual(cha.contents(), ele2, msg='Should have scaled properly')
