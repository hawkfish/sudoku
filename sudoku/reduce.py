# !/usr/bin/python3

from sudoku.cells import *
from sudoku.regions import *

class ReduceError(BaseException):
    pass

#   Remove all used values from a cell
def reduceCellByValues(cell, used):
    reduced = []
    for value in cell:
        if not used[value]: reduced.append(value)

    if not len(reduced): raise ReduceError

    return reduced

#   Remove all illegal values from a cell by region
def reduceCellByRegion(cells, c, region):
    cell = cells[c]
    if len(cell) == 1: return cell

    return reduceCellByValues(cell, findRegionValues(cells, region))

#   Apply the row reduction rule
def reduceRow(cells, c):
    cells[c] = reduceCellByRegion(cells, c, iRows[row(c)])
    return cells

#   Apply the column reduction rule
def reduceCol(cells, c):
    cells[c] = reduceCellByRegion(cells, c, iCols[col(c)])
    return cells

#   Apply the box reduction rule
def reduceBox(cells, c):
    cells[c] = reduceCellByRegion(cells, c, iBoxes[box(c)])
    return cells

#   Apply the king's move reduction rule
#   Any two cells separated by a king's move cannot contain the same digit
def reduceKing(cells, c):
    cells[c] = reduceCellByRegion(cells, c, iKings[c])
    return cells

#   Apply the knight's move reduction rule
#   Any two  cells separated by a knight's move cannot contain the same digit
def reduceKnight(cells, c):
    cells[c] = reduceCellByRegion(cells, c, iKnights[c])
    return cells

#   Apply the adjacency move reduction rule:
#   Any two orthogonally adjacent cells cannot contain consecutive digits
def reduceAdjacent(cells, c):
    cell = cells[c]
    if len(cell) == 1:
        value = cell[0]
        used = [0 for v in range(9)]
        if value > 0: used[value-1] = 1
        if value < 8: used[value+1] = 1

        if hasLeft(c):
            l = leftOf(c)
            cells[l] = reduceCellByValues(cells[l], used)

        if hasRight(c):
            r = rightOf(c)
            cells[r] = reduceCellByValues(cells[r], used)

        if hasAbove(c):
            a = aboveOf(c)
            cells[a] = reduceCellByValues(cells[a], used)

        if hasBelow(c):
            b = belowOf(c)
            cells[b] = reduceCellByValues(cells[b], used)

    return cells
