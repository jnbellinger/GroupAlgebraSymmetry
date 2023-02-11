''' Test suite for Name '''
import os
import sys
import copy
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import unittest
from unittest.mock import patch
from Builder import Name as N
from Builder import Key as K

#class DefTest(unittest.TestCase):
class test_key(unittest.TestCase):
    #
    def test_key_init_good_nodup(self):
        n1 = N.Name(1, 2, 4)
        n2 = N.Name(1, 3, 4)
        n3 = N.Name(3, 2, 4)
        key = K.Key([n1, n2, n3])
        a = key.namelist[0] == n1 and key.namelist[1] == n2 and key.namelist[2] == n3
        self.assertTrue(a, msg='Did not create the expected Key ' + str(key))
    #
    def test_key_init_good_dup(self):
        n1 = N.Name(1, 2, 4)
        n2 = N.Name(1, 3, 4)
        n3 = N.Name(3, 2, 4)
        n4 = N.Name(1, 3, 4)
        key = K.Key([n1, n2, n3, n4])
        a = key.namelist[0] == n1 and key.namelist[1] == n2 and key.namelist[2] == n3 and key.count() == 3
        self.assertTrue(a, msg='Key did not eliminate duplicates ' + str(key))
    def test_key_init_bad_notlist(self):
        n1 = N.Name(1, 2, 4)
        with self.assertRaises(SystemExit) as cm:
            key = K.Key(n1)
        self.assertEqual(cm.exception.code, 60, msg='Key needs a list (of Name)')
    def test_key_init_bad_empty(self):
        with self.assertRaises(SystemExit) as cm:
            key = K.Key([])
        self.assertEqual(cm.exception.code, 61, msg='Key needs a non-empty list (of Name)')
    def test_key_init_bad_notName(self):
        n1 = N.Name(1, 2, 4)
        with self.assertRaises(SystemExit) as cm:
            key = K.Key([n1, 4])
        self.assertEqual(cm.exception.code, 62, msg='Key needs a list of Name')
    def test_key_init_name_base_mismatch(self):
        n1 = N.Name(1, 2, 4)
        n2 = N.Name(1, 3, 5)
        with self.assertRaises(SystemExit) as cm:
            key = K.Key([n1, n2])
        self.assertEqual(cm.exception.code, 63, msg='Key Names do not have same base')
    #
    #
    def test_key_str(self):
        n1 = N.Name(1, 2, 4)
        n2 = N.Name(1, 3, 4)
        a = K.Key([n1, n2])
        expe = str(n1) + str(n2)
        foun = str(a)
        self.assertEqual(expe, foun, msg='Key __str__ mismatch ' + expe + ' ' +foun)
    def test_key_repr(self):
        n1 = N.Name(1, 2, 4)
        n2 = N.Name(1, 3, 4)
        a = K.Key([n1, n2])
        expe = repr(n1) + repr(n2)
        foun = repr(a)
        self.assertEqual(expe, foun, msg='Key __repr__ mismatch ' + expe + ' ' +foun)
    #
    #
    def test_key_equal(self):
        n1 = N.Name(1, 2, 4)
        n2 = N.Name(1, 3, 4)
        n3 = N.Name(1, 2, 4)
        n4 = N.Name(1, 3, 4)
        a = K.Key([n1, n2])
        b = K.Key([n4, n3])
        self.assertEqual(a, b, msg='Keys should be equal ' + str(a) + ' ' + str(b))
    #
    def test_key_not_equal(self):
        n1 = N.Name(1, 2, 4)
        n2 = N.Name(1, 3, 4)
        n3 = N.Name(1, 1, 4)
        n4 = N.Name(1, 3, 4)
        a = K.Key([n1, n2])
        b = K.Key([n4, n3])
        self.assertNotEqual(a, b, msg='Keys should not be equal ' + str(a) + ' ' + str(b))
    def test_key_equal_not_matching(self):
        n1 = N.Name(1, 2, 4)
        n2 = N.Name(1, 3, 4)
        n3 = N.Name(1, 2, 5)
        n4 = N.Name(1, 3, 5)
        a = K.Key([n1, n2])
        b = K.Key([n4, n3])
        self.assertNotEqual(a, b, msg='Key Names have different bases ' + str(a) + ' ' + str(b))
    def test_key_equal_not_length(self):
        n1 = N.Name(1, 2, 4)
        n2 = N.Name(1, 3, 4)
        n3 = N.Name(1, 2, 4)
        n4 = N.Name(1, 3, 4)
        n5 = N.Name(3, 3, 4)
        a = K.Key([n1, n2])
        b = K.Key([n4, n3, n5])
        self.assertNotEqual(a, b, msg='Keys are not same length, why equal? ' + str(a) + ' ' + str(b))
    def test_key_equal_not_key(self):
        n1 = N.Name(1, 2, 4)
        n2 = N.Name(1, 3, 4)
        a = K.Key([n1, n2])
        self.assertNotEqual(a, n1, msg='Key cannot be equal anything but another Key')
    #
    def test_key_overlap_good(self):
        n1 = N.Name(1, 2, 4)
        n2 = N.Name(1, 3, 4)
        n4 = N.Name(1, 3, 4)
        n5 = N.Name(3, 3, 4)
        a = K.Key([n1, n2])
        b = K.Key([n4, n5])
        over = a.overlap(b)
        c = K.Key([n2])
        self.assertEqual(over, c, msg='Key overlap bad, expect ' + str(c) + ', got ' + str(over))
    def test_key_overlap_none(self):
        n1 = N.Name(1, 2, 4)
        n2 = N.Name(1, 3, 4)
        n4 = N.Name(2, 1, 4)
        n5 = N.Name(3, 3, 4)
        a = K.Key([n1, n2])
        b = K.Key([n4, n5])
        over = a.overlap(b)
        self.assertIsNone(over, msg='Key expect no overlap? ' + str(over))
    def test_key_overlap_notkey(self):
        n1 = N.Name(1, 2, 4)
        n2 = N.Name(1, 3, 4)
        a = K.Key([n1, n2])
        with self.assertRaises(SystemExit) as cm:
            over = a.overlap(n1)
        self.assertEqual(cm.exception.code, 64, msg='Key overlaps only Key ')
    #
    def test_key_name_present_yes(self):
        n1 = N.Name(1, 2, 4)
        n2 = N.Name(1, 3, 4)
        n3 = N.Name(1, 3, 4)
        a = K.Key([n1, n2])
        self.assertTrue(a.present(n3), msg='Key ' + str(a) + ' should contain ' + str(n3))
    def test_key_name_present_no(self):
        n1 = N.Name(1, 2, 4)
        n2 = N.Name(1, 3, 4)
        n3 = N.Name(2, 3, 4)
        a = K.Key([n1, n2])
        self.assertFalse(a.present(n3), msg='Key ' + str(a) + ' does not contain ' + str(n3))
    def test_key_name_present_bad(self):
        n1 = N.Name(1, 2, 4)
        n2 = N.Name(1, 3, 4)
        n3 = N.Name(2, 3, 4)
        a = K.Key([n1, n2])
        with self.assertRaises(SystemExit) as cm:
            over = a.present('{2_3}')
        self.assertEqual(cm.exception.code, 65, msg='Key cannot search for non-Name')
    #
    def test_key_contents(self):
        n1 = N.Name(1, 2, 4)
        n2 = N.Name(1, 3, 4)
        n3 = N.Name(2, 3, 4)
        a = K.Key([n1, n2, n3])
        b = a.contents()
        c = [n1, n2, n3]
        self.assertEqual(c, b, msg='Two lists should be the same')
    def test_key_tuple(self):
        n1 = N.Name(1, 2, 4)
        n2 = N.Name(1, 3, 4)
        n3 = N.Name(2, 3, 4)
        a = K.Key([n1, n2, n3])
        b = a.tuple()
        self.assertEqual(str(b), '({1_2}, {1_3}, {2_3})', msg='Tuple should hold the list')




if __name__ == '__main__':
    unittest.main()    # pragma: no cover
