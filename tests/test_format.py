#!/usr/bin/python3

import unittest
from context import *

class TestFormat(unittest.TestCase):

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
