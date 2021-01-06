#!/usr/bin/python3

import unittest
from context import *

class TestCells(unittest.TestCase):

    def test_row0(self):
        for c in range(9):
            self.assertEqual(0, row(c))

    def test_row1(self):
        for c in range(9):
            self.assertEqual(1, row(c+9))

    def test_col0(self):
        for c in range(9):
            self.assertEqual(c, col(c))

    def test_col1(self):
        for c in range(9, 18):
            self.assertEqual(c-9, col(c))

    def test_box0(self):
        for c in range(3):
            self.assertEqual(0, box(c))

    def test_box4(self):
        for c in range(4*9 + 3, 4*9 + 6):
            self.assertEqual(4, box(c))

    def test_box8(self):
        for c in range(8*9 + 6, 8*9 + 9):
            self.assertEqual(8, box(c))

    def assert_hasLeft(self, n):
        for l in range(0,n):
            for c in range(l, 81, 9):
                self.assertFalse(hasLeft(c, n))

        for l in range(n,9):
            for c in range(l, 81, 9):
                self.assertTrue(hasLeft(c, n))

    def test_hasLeft(self):
        self.assert_hasLeft(1)
        self.assert_hasLeft(2)

    def test_leftOf(self):
        for c in range(81):
            if hasLeft(c):
                self.assertEqual(c-1, leftOf(c))

    def assert_hasRight(self, n):
        for r in range(0,9-n):
            for c in range(r, 81, 9):
                self.assertTrue(hasRight(c, n))

        for r in range(9-n,9):
            for c in range(r, 81, 9):
                self.assertFalse(hasRight(c, n))

    def test_hasRight(self):
        self.assert_hasRight(1)
        self.assert_hasRight(2)

    def test_rightOf(self):
        for c in range(81):
            if hasRight(c):
                self.assertEqual(c+1, rightOf(c))

    def assert_hasAbove(self, n):
        for a in range(0, n):
            for l in range(9):
                c = a * 9 + l
                self.assertFalse(hasAbove(c, n), ("%d: (%d, %d, %d)" % (c, a, l, n, )))

        for a in range(n, 9):
            for l in range(9):
                c = a * 9 + l
                self.assertTrue(hasAbove(c, n), ("%d: (%d, %d, %d)" % (c, a, l, n, )))

    def test_aboveOf(self):
        for n in range(1, 3):
            for c in range(81):
                if hasAbove(c, n):
                    self.assertEqual(c-9*n, aboveOf(c, n))

    def test_hasAbove(self):
        self.assert_hasAbove(1)
        self.assert_hasAbove(2)

    def assert_hasBelow(self, n):
        for b in range(0, n):
            for l in range(0, 9-n):
                c = b * 9 + l
                self.assertTrue(hasBelow(c, n), ("%d: (%d, %d, %d)" % (c, a, l, n, )))

        for b in range(9-n, 9):
            for l in range(9):
                c = b * 9 + l
                self.assertFalse(hasBelow(c, n), ("%d: (%d, %d, %d)" % (c, a, l, n, )))

    def test_hasBelow(self):
        self.assert_hasBelow(1)
        self.assert_hasBelow(2)

    def test_belowOf(self):
        for n in range(1, 3):
            for c in range(81):
                if hasBelow(c, n):
                    self.assertEqual(c+9*n, belowOf(c, n))

    def test_parseEmpty(self):
        setup = [ ' ' * 9 ] * 9
        expected = [ [v for v in range(9)] for c in range(81) ]
        actual = parseCells(setup)
        self.assertEqual(expected, actual)

    def test_parseFull(self):
        row = '123456789'
        setup = [ row[n:] + row[:n] for n in range(9)]
        expected = [ [ ( v + r) % 9 ] for v in range(9) for r in range(9) ]
        actual = parseCells(setup)
        self.assertEqual(expected, actual)

    def test_parseFormatted(self):
        row = '123456789'
        solid = [ row[n:] + row[:n] for n in range(9)]
        setup = [ row[:3] + '|' + row[3:6] + '|' + row[6:] for row in solid ]
        setup[6:6] = ['---+---+---']
        setup[3:3] = ['---+---+---']

        expected = [ [ ( v + r) % 9 ] for v in range(9) for r in range(9) ]
        actual = parseCells(setup)
        self.assertEqual(expected, actual)

        actual = formatCells(expected)
        self.assertEqual(setup, actual)

if __name__ == '__main__':
    unittest.main()
