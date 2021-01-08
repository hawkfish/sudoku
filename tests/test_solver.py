#!/usr/bin/python3

import unittest
from context import *
from helpers import *

class TestSolver(unittest.TestCase):

    def test_enumerateBranches(self):
        setup = Solver()

        board = Board(parseCells(readFixture('2007-02-18.sdk')))
        board.reduce()

        #   We need to traverse three branches to solve this
        actual = setup.enumerateBranches(board)
        self.assertEqual(1, len(actual))
        self.assertEqual(153, board._total)

        board = actual[0]
        actual = setup.enumerateBranches(board)
        self.assertEqual(1, len(actual))
        self.assertEqual(142, board._total)

        board = actual[0]
        actual = setup.enumerateBranches(board)
        self.assertEqual(1, len(actual))
        self.assertEqual(len(board._cells), board._total)

    def test_search(self):
        setup = Solver()

        board = Board(parseCells(readFixture('2007-02-18.sdk')))
        board.reduce()

        solution = setup.search(board)
        self.assertIsNotNone(solution, "Didn't find solution")
        self.assertEqual(3, setup._searched)
        self.assertEqual(0, setup._backtracks)

    def test_miracle(self):
        rules = [
            reduceRow,
            reduceCol,
            reduceBox,
            reduceKing,
            reduceKnight,
            reduceAdjacent,
        ]

        setup = Solver()
        board = Board(parseCells(readFixture('miracle.sdk')), rules)
        board.reduce()

        solution = setup.search(board)
        actual = formatCells(solution._cells)
        expected = [
            '483|726|159',
            '726|159|483',
            '159|483|726',
            '---+---+---',
            '837|261|594',
            '261|594|837',
            '594|837|261',
            '---+---+---',
            '372|615|948',
            '615|948|372',
            '948|372|615',
        ]
        self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()
