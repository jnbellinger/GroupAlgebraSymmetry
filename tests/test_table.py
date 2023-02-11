''' Table and G '''
import os
import sys
import copy
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import unittest
from unittest.mock import patch
from Builder import Group as G

#Table
#   def __init__(self, ilist):
#    def G(self, i):
#    def _product(self, i, j):
#    def product(self, i, j):
#    def inverse(self, i):
#G
#    def __init__(self, other):
#    def index(self):
#    def __eq__(self, other):
#    def inRange(self, other):
#    def __str__(self):
#    def __repr__(self):

class test_table(unittest.TestCase):
    #
    def test_table_init_ok(self):
        table = G.Table([0, 1, 2, 1, 2, 0, 2, 0, 1])
        self.assertEqual(str(table), ' [0] [1] [2]\n [1] [2] [0]\n [2] [0] [1]\n', msg='String should be easy')
    def test_table_repr(self):
        table = G.Table([0, 1, 2, 1, 2, 0, 2, 0, 1])
        self.assertEqual(repr(table), ' [0] [1] [2]\n [1] [2] [0]\n [2] [0] [1]\n', msg='String repor should be easy')
    def test_table_bad_list(self):
        with self.assertRaises(SystemExit) as cm:
            table = G.Table('table')
        self.assertEqual(cm.exception.code, 200, msg='Table:init want a *list* of int')
    def test_table_bad_nonint_list(self):
        with self.assertRaises(SystemExit) as cm:
            table = G.Table([0, 1, 2, '3'])
        self.assertEqual(cm.exception.code, 201, msg='Table:init want a list of *int*')
    def test_table_bad_nonsquare_list(self):
        with self.assertRaises(SystemExit) as cm:
            table = G.Table([0, 1, 2, 3, 4])
        self.assertEqual(cm.exception.code, 202, msg='Table:init wants a square list of int')
    def test_table_bad_oob_list(self):
        with self.assertRaises(SystemExit) as cm:
            table = G.Table([0, 1, 2, 0])
        self.assertEqual(cm.exception.code, 203, msg='Table:init entry exceeds square root of list size -1')
    def test_table_bad_uneq_list(self):
        with self.assertRaises(SystemExit) as cm:
            table = G.Table([0, 1, 0, 0])
        self.assertEqual(cm.exception.code, 204, msg='Table:init list had unequal numbers of products')
    def test_table_bad_notonto_list(self):
        with self.assertRaises(SystemExit) as cm:
            table = G.Table([0, 2, 1,  1, 1, 2,  2, 0, 0])
        self.assertEqual(cm.exception.code, 205, msg='Table:init list had failure to map rows onto')
    def test_table_bad_col_notonto_list(self):
        with self.assertRaises(SystemExit) as cm:
            table = G.Table([0, 1, 2, 2, 1, 0, 1, 2, 0])
        self.assertEqual(cm.exception.code, 216, msg='Table:init list had failure to map columns onto')
    def test_table_bad_nonassoc(self):
        with self.assertRaises(SystemExit) as cm:
            table = G.Table([0, 1, 2, 3, 4, 1, 0, 3, 4, 2, 2, 3, 4, 1, 0, 3, 4, 0, 2, 1, 4, 2, 1, 0, 3])
        self.assertEqual(cm.exception.code, 217, msg='Table:init not associative')
    # internal routine test
    def test_table__product_ok(self):
        table = G.Table([0, 1, 2,  1, 2, 0,  2, 0, 1])
        self.assertEqual(table._product(1, 1), 2, msg='Should have given the right answer')
    def test_table__product_low(self):
        table = G.Table([0, 1, 2,  1, 2, 0,  2, 0, 1])
        with self.assertRaises(SystemExit) as cm:
            k = table._product(-1, 2)
        self.assertEqual(cm.exception.code, 215, msg='Table:init _product had value too low')
    def test_table__product_high(self):
        table = G.Table([0, 1, 2,  1, 2, 0,  2, 0, 1])
        with self.assertRaises(SystemExit) as cm:
            k = table._product(3, 2)
        self.assertEqual(cm.exception.code, 215, msg='Table:init _product had value too high')
    def test_table_G_ok(self):
        table = G.Table([0, 1, 2,  1, 2, 0,  2, 0, 1])
        expected = table.G(2)
        self.assertEqual(str(expected), '[2]', msg='Should have 2')
    def test_table_G_ok_2(self):
        table = G.Table([0, 1, 2,  1, 2, 0,  2, 0, 1])
        expected = table.G(2)
        self.assertTrue(isinstance(expected, G.G), msg='Should have a G')
    def test_table_G_bad_notint(self):
        table = G.Table([0, 1, 2,  1, 2, 0,  2, 0, 1])
        with self.assertRaises(SystemExit) as cm:
            k = table.G('[2]')
        self.assertEqual(cm.exception.code, 208, msg='Table:G should get int')
    def test_table_G_bad_lowint(self):
        table = G.Table([0, 1, 2,  1, 2, 0,  2, 0, 1])
        with self.assertRaises(SystemExit) as cm:
            k = table.G(-4)
        self.assertEqual(cm.exception.code, 209, msg='Table:G int too low')
    def test_table_G_bad_highint(self):
        table = G.Table([0, 1, 2,  1, 2, 0,  2, 0, 1])
        with self.assertRaises(SystemExit) as cm:
            k = table.G(4)
        self.assertEqual(cm.exception.code, 209, msg='Table:G int too high')
    #
    def test_table_product_ok(self):
        # also tests G == G
        table = G.Table([0, 1, 2,  1, 2, 0,  2, 0, 1])
        g1 = table.G(1)
        g2 = table.G(2)
        gx = table.product(g1, g1)
        self.assertEqual(gx, g2, msg='Table:product group product matches')
    def test_table_product_notgroup(self):
        table = G.Table([0, 1, 2,  1, 2, 0,  2, 0, 1])
        g1 = table.G(1)
        g2 = table.G(2)
        with self.assertRaises(SystemExit) as cm:
            gx = table.product(1, 1)
        self.assertEqual(cm.exception.code, 219, msg='Table:product wants G')
    def test_table_product_outofrange_high(self):
        table = G.Table([0, 1, 2,  1, 2, 0,  2, 0, 1])
        g1 = table.G(1)
        g2 = table.G(2)
        # DO BAD THING
        g2._index = 4
        with self.assertRaises(SystemExit) as cm:
            gx = table.product(g1, g2)
        self.assertEqual(cm.exception.code, 210, msg='Table:product wants G in range, too high')
    def test_table_product_outofrange_low(self):
        table = G.Table([0, 1, 2,  1, 2, 0,  2, 0, 1])
        g1 = table.G(1)
        g2 = table.G(2)
        # DO BAD THING
        g2._index = -4
        with self.assertRaises(SystemExit) as cm:
            gx = table.product(g1, g2)
        self.assertEqual(cm.exception.code, 210, msg='Table:product wants G in range, too low')
    def test_table_inverse_ok(self):
        table = G.Table([0, 1, 2,  1, 2, 0,  2, 0, 1])
        g1 = table.G(1)
        g2 = table.G(2)
        gx = table.inverse(g1)
        self.assertEqual(gx, g2, msg='Table:inverse should have given inverse')
    def test_table_inverse_notg(self):
        table = G.Table([0, 1, 2,  1, 2, 0,  2, 0, 1])
        with self.assertRaises(SystemExit) as cm:
            gx = table.inverse(1)
        self.assertEqual(cm.exception.code, 211, msg='Table:inverse wants G')
    def test_table_inverse_badg(self):
        table = G.Table([0, 1, 2,  1, 2, 0,  2, 0, 1])
        g1 = table.G(1)
        # DO BAD THING
        g1._index = -4
        with self.assertRaises(SystemExit) as cm:
            gx = table.inverse(g1)
        self.assertEqual(cm.exception.code, 212, msg='Table:inverse wants G in range')
    #
    #
    def test_table_g_init_bad(self):
        table = G.Table([0, 1, 2,  1, 2, 0,  2, 0, 1])
        g1 = table.G(1)
        with self.assertRaises(SystemExit) as cm:
            gx = G.G('1')
        self.assertEqual(cm.exception.code, 206, msg='G:init wants int')
    def test_table_g_eq_bad(self):
        table = G.Table([0, 1, 2,  1, 2, 0,  2, 0, 1])
        g1 = table.G(1)
        with self.assertRaises(SystemExit) as cm:
            bx = g1 == '[1]'
        self.assertEqual(cm.exception.code, 207, msg='G:== wants another G')
    def test_table_g_inrange_bad(self):
        table = G.Table([0, 1, 2,  1, 2, 0,  2, 0, 1])
        g1 = table.G(1)
        g2 = table.G(2)
        with self.assertRaises(SystemExit) as cm:
            bx = g1.inRange(g2)
        self.assertEqual(cm.exception.code, 213, msg='G:inRange wants an int to compare to')
    def test_table_g_repr(self):
        table = G.Table([0, 1, 2,  1, 2, 0,  2, 0, 1])
        g1 = table.G(1)
        self.assertEqual(repr(g1), '[1]', msg='Should be same as str')
    #
    def test_table_size(self):
        table = G.Table([0, 1, 2,  1, 2, 0,  2, 0, 1])
        self.assertEqual(table.size(), 3, msg='Should have been easy 3')
