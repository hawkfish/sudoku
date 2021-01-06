#!/usr/bin/python3

import unittest
from context import *
from helpers import *

class TestSolver(unittest.TestCase):

    def test_search(self):
        setup = Solver()
        board = Board(parseCells(readFixture('2007-02-18.sdk')))
        board.reduce()

        solution = setup.search(board)
        self.assertIsNotNone(solution, "Didn't find solution")
        self.assertEqual(3, setup._searched)
        self.assertEqual(0, setup._backtracks)

if __name__ == '__main__':
    unittest.main()
