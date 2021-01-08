# !/usr/bin/python3

def row(c):
    return c // 9

def col(c):
    return c % 9

def box(c):
    return (col(c) // 3) + 3 * (row(c) // 3)

def hasLeft(c, n=1):
    return col(c) >= n

def leftOf(c, n=1):
    return c - n

def hasRight(c, n=1):
    return col(c) < 9-n

def rightOf(c, n=1):
    return c + n

def hasAbove(c, n=1):
    return row(c) >= n

def aboveOf(c, n=1):
    return c - 9 * n

def hasBelow(c, n=1):
    return row(c) < 9-n

def belowOf(c, n=1):
    return c + 9 * n

#   TODO: Refactor as format.py
from sudoku.regions import *

_boardIn = {
   '1': [0],
   '2': [1],
   '3': [2],
   '4': [3],
   '5': [4],
   '6': [5],
   '7': [6],
   '8': [7],
   '9': [8],
   ' ': [0,1,2,3,4,5,6,7,8],
   }

def parseCells(lines):
    cells = []
    for l in lines:
        for c in l:
            if c in _boardIn:
                cells.append( _boardIn[c] )
    return cells

_boardOut = '123456789'

def formatCells(cells):
    lines = []
    for r in range(len(iRows)):
        line = ''
        for c in iRows[r]:
            if len(cells[c]) == 1:
                line += _boardOut[cells[c][0]]
            else:
                line += ' '
        lines.append(line[:3] + '|' + line[3:6] + '|' + line[6:])
        if r in (2, 5,): lines += ['---+---+---']
    return lines

def printBoard(board):
    lines = formatCells(board._cells)
    print('\n'.join(lines))

