#!/usr/bin/python3

import unittest
from sudoku import *

def readFixture(sdk):
    f = open(sdk, 'r')
    lines = f.readlines()
    f.close()
    return [ line.strip('\n') for line in lines]

def valuesFromDisplay(display):
    return [value-1 for value in display]

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

class TestRegions(unittest.TestCase):

    def test_findRowValues(self):
        setup = parseCells(readFixture('data/2007-02-18.sdk'))

        expected = [0, 0, 0, 1, 1, 1, 0, 0, 0]
        actual = findRegionValues(setup, iRows[0])
        self.assertEqual(expected, actual)

    def test_findColValues(self):
        setup = parseCells(readFixture('data/2007-02-18.sdk'))

        expected = [0, 0, 1, 0, 0, 0, 1, 1, 1]
        actual = findRegionValues(setup, iCols[5])
        self.assertEqual(expected, actual)

    def test_findBoxValues(self):
        setup = parseCells(readFixture('data/2007-02-18.sdk'))

        expected = [0, 1, 0, 1, 0, 1, 0, 1, 1]
        actual = findRegionValues(setup, iBoxes[2])
        self.assertEqual(expected, actual)

    def test_findKingValues(self):
        setup = parseCells(readFixture('data/2007-02-18.sdk'))

        expected = [0, 0, 0, 1, 0, 1, 0, 1, 1]
        actual = findRegionValues(setup, iKings[16])
        self.assertEqual(expected, actual)

    def test_findKnightValues(self):
        setup = parseCells(readFixture('data/2007-02-18.sdk'))

        expected = [0, 0, 0, 0, 0, 1, 0, 1, 0]
        actual = findRegionValues(setup, iKnights[15])
        self.assertEqual(expected, actual)

class TestReduce(unittest.TestCase):

    def test_reduceRow(self):
        setup = parseCells(readFixture('data/2007-02-18.sdk'))

        expected = valuesFromDisplay( [1, 2, 3, 7, 8, 9, ] )
        actual = reduceRow(setup, 7)[7]
        self.assertEqual(expected, actual)

    def test_reduceCol(self):
        setup = parseCells(readFixture('data/2007-02-18.sdk'))

        expected = valuesFromDisplay( [1, 2, 4, 8, 9, ] )
        actual = reduceCol(setup, 12)[12]
        self.assertEqual(expected, actual)

    def test_reduceBox(self):
        setup = parseCells(readFixture('data/2007-02-18.sdk'))

        expected = valuesFromDisplay( [1, 3, 5, 7, ] )
        actual = reduceBox(setup, 7)[7]
        self.assertEqual(expected, actual)

    def test_reduceKing(self):
        setup = parseCells(readFixture('data/2007-02-18.sdk'))

        expected = valuesFromDisplay( [1, 2, 3, 5, 8, ] )
        actual = reduceKing(setup, 55)[55]
        self.assertEqual(expected, actual)

    def test_reduceKnight(self):
        setup = parseCells(readFixture('data/2007-02-18.sdk'))

        expected = valuesFromDisplay( [2, 4, 5, 6, 7, ] )
        actual = reduceKnight(setup, 34)[34]
        self.assertEqual(expected, actual)

    def test_reduceAdjacent(self):
        setup = parseCells(readFixture('data/2007-02-18.sdk'))

        c = 40
        expected = valuesFromDisplay( [1, 2, 3, 4, 6, 8, 9, ] )
        actual = reduceAdjacent(setup, c)
        self.assertEqual(expected, actual[leftOf(c)])
        self.assertEqual(expected, actual[rightOf(c)])
        self.assertEqual(expected, actual[aboveOf(c)])
        self.assertEqual(expected, actual[belowOf(c)])

class TestBoard(unittest.TestCase):

    def assertCell(self, values, actual):
        expected = valuesFromDisplay( values )
        self.assertEqual(expected, actual)

    def test_reduceCell(self):
        setup = Board(parseCells(readFixture('data/2007-02-18.sdk')))

        self.assertEqual(5, setup.reduceCell(0))
        self.assertCell([1, 3, 8, 9, ], setup.cells[0] )

    def test_reduceRegion(self):
        setup = Board(parseCells(readFixture('data/2007-02-18.sdk')))

        #   After reducing all the cells, there are three
        #   regions that can be reduced
        for c in range(len(setup.cells)): setup.reduceCell(c)
        self.assertEqual(1, setup.reduceRegion(iRows[7]))
        self.assertEqual(1, setup.reduceRegion(iCols[2]))
        self.assertEqual(2, setup.reduceRegion(iBoxes[6]))
        self.assertCell([3,], setup.cells[8] )

    def test_reduce(self):
        setup = Board(parseCells(readFixture('data/2007-02-18.sdk')))
        setup.reduce()

        #   This board has a branch point in cell 5
        self.assertEqual(5, setup.shortest)
        self.assertEqual([0, 1, ], setup.cells[setup.shortest])

    def test_enumerateBranches(self):
        setup = Board(parseCells(readFixture('data/2007-02-18.sdk')))
        setup.reduce()

        #   We need to traverse three branches to solve this
        actual = setup.enumerateBranches()
        self.assertEqual(1, len(actual))
        self.assertEqual(153, setup.total)

        setup = actual[0]
        actual = setup.enumerateBranches()
        self.assertEqual(1, len(actual))
        self.assertEqual(142, setup.total)

        setup = actual[0]
        actual = setup.enumerateBranches()
        self.assertEqual(1, len(actual))
        self.assertEqual(len(setup.cells), setup.total)

class TestSolver(unittest.TestCase):

    def test_search(self):
        setup = Solver()
        board = Board(parseCells(readFixture('data/2007-02-18.sdk')))
        board.reduce()

        solution = setup.search(board)
        self.assertIsNotNone(solution, "Didn't find solution")
        self.assertEqual(3, setup._searched)
        self.assertEqual(0, setup._backtracks)

if __name__ == '__main__':
    unittest.main()
