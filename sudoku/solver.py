# !/usr/bin/python3

import copy
import operator

from sudoku.cells import *

class ReduceError(BaseException):
    pass

#   Find all the values used by a region
def findRegionValues(cells, region):
    values = [0 for v in range(0,9)]
    for c in region:
        if len(cells[c]) == 1:
            values[cells[c][0]] = 1
    return values

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

_rules = [
    reduceRow,
    reduceCol,
    reduceBox,
]

class Board:
    def __init__(self, cells, rules = _rules):
        self._cells = cells
        self._rules = rules
        self._total = 0
        for c in range(0,len(self._cells)):
            self._total += len(cells[c])
        self._shortest = None

    #   Remove all illegal values from a cell
    def reduceCell(self, c, callback=None):
        old_lens = [ len(cell) for cell in self._cells ]
        for rule in self._rules:
            self._cells = rule(self._cells, c)
        new_lens = [ len(cell) for cell in self._cells ]
        delta = sum(map(operator.sub, old_lens, new_lens))
        self._total -= delta
        if callback: callback(self, c, delta)
        return delta

    #   Look for values that can only go one place in the region
    def reduceRegion(self, region, callback = None):
        valueCells = [[] for i in range(0,9)]
        for c in region:
            for v in self._cells[c]:
                valueCells[v].append(c)

        delta = 0
        for v in range(0,len(valueCells)):
            if 0 == len(valueCells[v]): raise ReduceError
            if 1 == len(valueCells[v]):
                c = valueCells[v][0]
                cellDelta = len(self._cells[c]) - 1
                delta += cellDelta
                self._cells[c] = [v,]
                if callback: callback(self, c, cellDelta)

        self._total -= delta
        return delta

    def reduce(self, callback = None):
        #   Reduce all the cells as far as possible
        #   until we can't make any more progress
        todo = 1
        while todo:
            todo = 0
            for c in range(0,len(self._cells)): todo += self.reduceCell(c, callback)
            for r in iRows: todo += self.reduceRegion(r, callback)
            for r in iCols: todo += self.reduceRegion(r, callback)
            for r in iBoxes: todo += self.reduceRegion(r, callback)

        #   Once we fail to reduce cells,
        #   find the cell with the shortest list
        #   of possibilities
        self._shortest = 0
        min_len = 10
        for c in range(0,len(self._cells)):
            b_len = len(self._cells[c])
            if b_len == 1: continue
            if b_len >= min_len: continue
            min_len = b_len
            self._shortest = c

#   Prefer boards with shorter shortest branches
def branchKey(branch):
    return len(branch._cells[branch._shortest])

class Solver:

    def __init__(self):
        self._searched = 0
        self._backtracks = 0

    def enumerateBranches(self, board, callback = None):
        branches = []
        for value in board._cells[board._shortest]:
            cells = copy.deepcopy(board._cells)
            cells[board._shortest] = [value,]
            try:
                branch = Board(cells, board._rules)
                branch.reduce(callback)
                branches.append(branch)
            except ReduceError:
                pass

        return branches

    def search(self, board, callback = None):
        self._searched += 1

        if len(board._cells) == board._total:
            return board

        branches = self.enumerateBranches(board, callback)
        branches.sort(key=branchKey)

        #   Recurse on the branches until we have a solution
        for branch in branches:
            if callback: callback(branch, -1, 0)
            solution = self.search(branch, callback)
            if solution: return solution
            self._backtracks += 1

        return None

    def solve(self, board, callback = None):
        board.reduce(callback)
        return self.search(board, callback)

