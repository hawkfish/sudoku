#!/usr/bin/python3

import unittest
from context import *
from helpers import *

class TestReduce(unittest.TestCase):

    def test_reduceRow(self):
        setup = parseCells(readFixture('2007-02-18.sdk'))

        expected = valuesFromDisplay( [1, 2, 3, 7, 8, 9, ] )
        actual = reduceRow(setup, 7)[7]
        self.assertEqual(expected, actual)

    def test_reduceCol(self):
        setup = parseCells(readFixture('2007-02-18.sdk'))

        expected = valuesFromDisplay( [1, 2, 4, 8, 9, ] )
        actual = reduceCol(setup, 12)[12]
        self.assertEqual(expected, actual)

    def test_reduceBox(self):
        setup = parseCells(readFixture('2007-02-18.sdk'))

        expected = valuesFromDisplay( [1, 3, 5, 7, ] )
        actual = reduceBox(setup, 7)[7]
        self.assertEqual(expected, actual)

    def test_reduceKing(self):
        setup = parseCells(readFixture('2007-02-18.sdk'))

        expected = valuesFromDisplay( [1, 2, 3, 5, 8, ] )
        actual = reduceKing(setup, 55)[55]
        self.assertEqual(expected, actual)

    def test_reduceKnight(self):
        setup = parseCells(readFixture('2007-02-18.sdk'))

        expected = valuesFromDisplay( [2, 4, 5, 6, 7, ] )
        actual = reduceKnight(setup, 34)[34]
        self.assertEqual(expected, actual)

    def test_reduceAdjacent(self):
        setup = parseCells(readFixture('2007-02-18.sdk'))

        c = 40
        expected = valuesFromDisplay( [1, 2, 3, 4, 6, 8, 9, ] )
        actual = reduceAdjacent(setup, c)
        self.assertEqual(expected, actual[leftOf(c)])
        self.assertEqual(expected, actual[rightOf(c)])
        self.assertEqual(expected, actual[aboveOf(c)])
        self.assertEqual(expected, actual[belowOf(c)])

if __name__ == '__main__':
    unittest.main()
