# !/usr/bin/python3

import copy
import operator
import sys

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

iRows = []
iCols = []
iBoxes = []
for c in range(9):
    iRows.append([])
    iCols.append([])
    iBoxes.append([])

for c in range(81):
    iRows[row(c)].append(c)
    iCols[col(c)].append(c)
    iBoxes[box(c)].append(c)

#   Map out the kings move cells for each cell
iKings = []
for c in range(81):
    king = []

    if hasLeft(c):
        l = leftOf(c)
        king.append(l)
        if hasAbove(l): king.append(aboveOf(l))
        if hasBelow(l): king.append(belowOf(l))

    if hasRight(c):
        r = rightOf(c)
        king.append(r)
        if hasAbove(r): king.append(aboveOf(r))
        if hasBelow(r): king.append(belowOf(r))

    if hasAbove(c): king.append(aboveOf(c))
    if hasBelow(c): king.append(belowOf(c))

    iKings.append(king)

#   Map out the knights move cells for each cell
iKnights = []
for c in range(81):
    knight = []

    if hasLeft(c, 2):
        l = leftOf(c, 2)
        if hasAbove(l): knight.append(aboveOf(l))
        if hasBelow(l): knight.append(belowOf(l))

    if hasRight(c, 2):
        r = rightOf(c, 2)
        if hasAbove(r): knight.append(aboveOf(r))
        if hasBelow(r): knight.append(belowOf(r))

    if hasAbove(c, 2):
        a = aboveOf(c, 2)
        if hasLeft(a): knight.append(leftOf(a))
        if hasRight(a): knight.append(rightOf(a))

    if hasBelow(c, 2):
        b = belowOf(c, 2)
        if hasLeft(b): knight.append(leftOf(b))
        if hasRight(b): knight.append(rightOf(b))

    iKnights.append(knight)

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
    lines = formatCells(board.cells)
    print('\n'.join(lines))

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
def reduceKing(cells, c):
    cells[c] = reduceCellByRegion(cells, c, iKings[c])
    return cells

#   Apply the knight's move reduction rule
def reduceKnight(cells, c):
    cells[c] = reduceCellByRegion(cells, c, iKnights[c])
    return cells

#   Apply the adjacency move reduction rule
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

rules = [
    reduceRow,
    reduceCol,
    reduceBox,
]

class Board:
    def __init__(self, cells):
        self.cells = cells
        self.total = 0
        self.shortest = None
        for c in range(0,len(self.cells)):
            self.total += len(cells[c])

    #   Remove all illegal values from a cell
    def reduceCell(self, c):
        old_lens = [ len(cell) for cell in self.cells ]
        for rule in rules:
            self.cells = rule(self.cells, c)
        new_lens = [ len(cell) for cell in self.cells ]
        delta = sum(map(operator.sub, old_lens, new_lens))
        self.total -= delta
        return delta

    #   Look for values that can only go one place in the region
    def reduceRegion(self, region):
        valueCells = [[] for i in range(0,9)]
        for c in region:
            for v in self.cells[c]:
                valueCells[v].append(c)

        delta = 0
        for v in range(0,len(valueCells)):
            if 0 == len(valueCells[v]): raise ReduceError
            if 1 == len(valueCells[v]):
                c = valueCells[v][0]
                delta += len(self.cells[c]) - 1
                self.cells[c] = [v,]

        self.total -= delta
        return delta

    def reduce(self):
        #   Reduce all the cells as far as possible
        #   until we can't make any more progress
        todo = 1
        while todo:
            todo = 0
            for c in range(0,len(self.cells)): todo += self.reduceCell(c)
            for r in iRows: todo += self.reduceRegion(r)
            for r in iCols: todo += self.reduceRegion(r)
            for r in iBoxes: todo += self.reduceRegion(r)

        #   Once we fail to reduce cells,
        #   find the cell with the shortest list
        #   of possibilities
        self.shortest = 0
        min_len = 10
        for c in range(0,len(self.cells)):
            b_len = len(self.cells[c])
            if b_len == 1: continue
            if b_len >= min_len: continue
            min_len = b_len
            self.shortest = c

    def enumerateBranches(self):
        branches = []
        for value in self.cells[self.shortest]:
            cells = copy.deepcopy(self.cells)
            cells[self.shortest] = [value,]
            try:
                branch = Board(cells)
                branch.reduce()
                branches.append(branch)
            except ReduceError:
                pass

        return branches

#   Prefer boards with shorter shortest branches
def branchKey(branch):
    return len(branch.cells[branch.shortest])

class Solver:

    def __init__(self):
        self._searched = 0
        self._backtracks = 0

    def search(self, board):
        self._searched += 1

        if len(board.cells) == board.total:
            return board

        branches = board.enumerateBranches()
        branches.sort(key=branchKey)

        #   Recurse on the branches until we have a solution
        for branch in branches:
            solution = self.search(branch)
            if solution: return solution
            self._backtracks += 1
        return None

    def solve(self, board):
        board.reduce()
        return self.search(board)

if __name__ == '__main__':
    problem = sys.stdin.readlines()
    problem = [ p[:-1] for p in problem]

    solver = Solver()

    board = Board(parseCells(problem))
    print("Problem:")
    print("-" * 11)
    printBoard(board)
    print()

    solution = solver.solve(board)
    if solution:
        print("Solution:")
        print("-" * 11)
        printBoard(solution)
        print()

    else:
        print("No Solution")

    print("%d positions examined, %d backtracks" % (solver._searched, solver._backtracks,))
