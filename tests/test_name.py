''' Test suite for Name '''
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import unittest
from unittest.mock import patch
from Builder import Name as N

#class DefTest(unittest.TestCase):
class test_name(unittest.TestCase):
    #
    def test_name_init_row_negative(self):
        with self.assertRaises(SystemExit) as cm:
            test_name_neg_row = N.Name(-1, 3, 4)
        self.assertEqual(cm.exception.code, 10, msg='Missed negative row')
    def test_name_init_column_negative(self):
        with self.assertRaises(SystemExit) as cm:
            test_name_neg_col = N.Name(3, -1, 4)
        self.assertEqual(cm.exception.code, 10, msg='Missed negative column')
        #
    def test_name_init_row_toobig(self):
        with self.assertRaises(SystemExit) as cm:
            test_name_high_row = N.Name(4, 3, 4)
        self.assertEqual(cm.exception.code, 10, msg='Missed row too large')
    #
    def test_name_init_column_toobig(self):
        with self.assertRaises(SystemExit) as cm:
            test_name_high_col = N.Name(3, 4, 4)
        self.assertEqual(cm.exception.code, 10, msg='Missed column too large')
        #
    def test_name_equality(self):
        test_name_1 = N.Name(1, 2, 4)
        test_name_eq = N.Name(1, 2, 4)
        self.assertEqual(test_name_1, test_name_eq, msg='Should be equal')
    #
    def test_name_inequality_col(self):
        test_name_1 = N.Name(1, 2, 4)
        test_name_neq = N.Name(1, 3, 4)
        self.assertNotEqual(test_name_1, test_name_neq, msg='Different columns should not be equal')
    def test_name_inequality_row(self):
        test_name_1 = N.Name(1, 2, 4)
        test_name_neq = N.Name(2, 2, 4)
        self.assertNotEqual(test_name_1, test_name_neq, msg='Different rows should not be equal')
    def test_name_inequality_size(self):
        test_name_1 = N.Name(1, 2, 4)
        test_name_neq = N.Name(1, 2, 5)
        self.assertNotEqual(test_name_1, test_name_neq, msg='Different sizes should not be equal')
    def test_name_equality_wrong(self):
        test_name_1 = N.Name(1, 2, 4)
        self.assertNotEqual(test_name_1, '{1,2}', msg='Name compare only to Name')
    #
    def test_name_greater(self):
        test_name_1 = N.Name(1, 2, 4)
        test_name_2 = N.Name(0, 3, 4)
        self.assertGreater(test_name_1, test_name_2, msg='Should be greater')
    def test_name_greater_wrong(self):
        test_name_1 = N.Name(1, 2, 4)
        with self.assertRaises(SystemExit) as cm:
            if test_name_1 > '{1_2}':
                print('x')  # pragma: no cover
        self.assertEqual(cm.exception.code, 11, msg='Name compares only to Name')
    def test_name_greater_wrong_size(self):
        test_name_1 = N.Name(1, 2, 4)
        test_name_2 = N.Name(0, 3, 5)
        with self.assertRaises(SystemExit) as cm:
            if test_name_1 > test_name_2:
                print('x')  # pragma: no cover
        self.assertEqual(cm.exception.code, 12, msg='Name compares only to Name')
    def test_name_less(self):
        test_name_1 = N.Name(1, 2, 4)
        test_name_2 = N.Name(0, 3, 4)
        self.assertLess(test_name_2, test_name_1, msg='Should be less')
    #
    @patch('builtins.print')
    def test_name_print(self, mock_print):
        test_name_1 = N.Name(1, 3, 4)
        print(test_name_1)
        ex = '{1_3}'
        #mock_print.assert_called_with((ex))
        # something is screwed up with this.  It compares quote-less and
        # quote-stripped versions.
        exx = str(test_name_1)
        self.assertEqual(ex, exx, msg='Should be the same ' + ex + ' ' + exx)
    @patch('builtins.print')
    def test_name_repr(self, mock_print):
        test_name_1 = N.Name(1, 3, 4)
        foun = repr(test_name_1)
        #print(test_name_1)
        ex = '{1_3}'
        #mock_print.assert_called_with((ex))
        # something is screwed up with this.  It compares quote-less and
        # quote-stripped versions.
        self.assertEqual(ex, foun, msg='Should be the same ' + ex + ' ' + foun)
    def test_name_hash(self):
        test_name = N.Name(1, 3, 4)
        self.assertEqual(str(test_name.__hash__()), '-1070212610609621906', msg='I hope this hash is portable')

if __name__ == '__main__':
    unittest.main()  # pragma: no cover
