# !/usr/bin/python3

import copy

from sudoku.board import *

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

