#!/usr/bin/python3

import unittest
from context import *
from helpers import *

class TestBoard(unittest.TestCase):

    def assertCell(self, values, actual):
        expected = valuesFromDisplay( values )
        self.assertEqual(expected, actual)

    def test_reduceCell(self):
        setup = Board(parseCells(readFixture('2007-02-18.sdk')))

        self.assertEqual(5, setup.reduceCell(0))
        self.assertCell([1, 3, 8, 9, ], setup._cells[0] )

    def test_reduceRegion(self):
        setup = Board(parseCells(readFixture('2007-02-18.sdk')))

        #   After reducing all the cells, there are three
        #   regions that can be reduced
        for c in range(len(setup._cells)): setup.reduceCell(c)
        self.assertEqual(1, setup.reduceRegion(iRows[7]))
        self.assertEqual(1, setup.reduceRegion(iCols[2]))
        self.assertEqual(2, setup.reduceRegion(iBoxes[6]))
        self.assertCell([3,], setup._cells[8] )

    def test_reduce(self):
        setup = Board(parseCells(readFixture('2007-02-18.sdk')))
        setup.reduce()

        #   This board has a branch point in cell 5
        self.assertEqual(5, setup._shortest)
        self.assertEqual([0, 1, ], setup._cells[setup._shortest])

    def test_enumerateBranches(self):
        setup = Board(parseCells(readFixture('2007-02-18.sdk')))
        setup.reduce()

        #   We need to traverse three branches to solve this
        actual = setup.enumerateBranches()
        self.assertEqual(1, len(actual))
        self.assertEqual(153, setup._total)

        setup = actual[0]
        actual = setup.enumerateBranches()
        self.assertEqual(1, len(actual))
        self.assertEqual(142, setup._total)

        setup = actual[0]
        actual = setup.enumerateBranches()
        self.assertEqual(1, len(actual))
        self.assertEqual(len(setup._cells), setup._total)

if __name__ == '__main__':
    unittest.main()
