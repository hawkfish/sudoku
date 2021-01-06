#!/usr/bin/python3

import unittest
from context import *
from helpers import *

class TestRegions(unittest.TestCase):

    def test_findRowValues(self):
        setup = parseCells(readFixture('2007-02-18.sdk'))

        expected = [0, 0, 0, 1, 1, 1, 0, 0, 0]
        actual = findRegionValues(setup, iRows[0])
        self.assertEqual(expected, actual)

    def test_findColValues(self):
        setup = parseCells(readFixture('2007-02-18.sdk'))

        expected = [0, 0, 1, 0, 0, 0, 1, 1, 1]
        actual = findRegionValues(setup, iCols[5])
        self.assertEqual(expected, actual)

    def test_findBoxValues(self):
        setup = parseCells(readFixture('2007-02-18.sdk'))

        expected = [0, 1, 0, 1, 0, 1, 0, 1, 1]
        actual = findRegionValues(setup, iBoxes[2])
        self.assertEqual(expected, actual)

    def test_findKingValues(self):
        setup = parseCells(readFixture('2007-02-18.sdk'))

        expected = [0, 0, 0, 1, 0, 1, 0, 1, 1]
        actual = findRegionValues(setup, iKings[16])
        self.assertEqual(expected, actual)

    def test_findKnightValues(self):
        setup = parseCells(readFixture('2007-02-18.sdk'))

        expected = [0, 0, 0, 0, 0, 1, 0, 1, 0]
        actual = findRegionValues(setup, iKnights[15])
        self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()
