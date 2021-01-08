# !/usr/bin/python3

import operator

from sudoku.format import *
from sudoku.reduce import *

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
