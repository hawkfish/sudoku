# !/usr/bin/python
import copy
import sys

def row(c):
    return int(c / 9)

def col(c):
    return c % 9


def box(c):
    return int(col(c) / 3) + 3 * int(row(c) / 3)
 
iRows = []
iCols = []
iBoxes = []
for c in range(0,9):
    iRows.append([])
    iCols.append([])
    iBoxes.append([])
    

for c in range(0,81):
    iRows[row(c)].append(c)
    iCols[col(c)].append(c)
    iBoxes[box(c)].append(c)

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
            cells.append( _boardIn[c] )
    return cells

_boardOut = '123456789'

def printBoard(board):
    for r in range(0,len(iRows)):
        line = ''
        for c in iRows[r]:
            if len(board.cells[c]) == 1:
                line += _boardOut[board.cells[c][0]]
            else:
                line += ' '
        print line

class ReduceError:
    pass
    
class Board:
    def __init__(self, cells):
        self.cells = cells
        self.total = 0
        self.shortest = None
        for c in range(0,len(self.cells)):
            self.total += len(cells[c])
            
        self.reduce()
        
    #   Find all the values used by a region
    def findRegionValues(self, region):
        values = [0 for v in range(0,9)]
        for c in region:
            if len(self.cells[c]) == 1:
                values[self.cells[c][0]] = 1
        return values
    
    #   Remove all illegal values from a cell by region
    def reduceCellByRegion(self, cell, region):
        if len(cell) == 1: return cell
        
        used = self.findRegionValues(region)
        reduced = []
        for value in cell:
            if not used[value]: reduced.append(value)
        
        if not len(reduced): raise ReduceError
        
        return reduced
    
    #   Remove all illegal values from a cell
    def reduceCell(self, c):
        old_len = len(self.cells[c])
        self.cells[c] = self.reduceCellByRegion(self.cells[c], iRows[row(c)])
        self.cells[c] = self.reduceCellByRegion(self.cells[c], iCols[col(c)])
        self.cells[c] = self.reduceCellByRegion(self.cells[c], iBoxes[box(c)])
        delta = old_len - len(self.cells[c])
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
        todo = 1
        while todo:
            todo = 0
            for c in range(0,len(self.cells)): todo += self.reduceCell(c)
            for r in iRows: todo += self.reduceRegion(r)
            for r in iCols: todo += self.reduceRegion(r)
            for r in iBoxes: todo += self.reduceRegion(r)

        self.shortest = 0
        min_len = 10
        for c in range(0,len(self.cells)):
            b_len = len(self.cells[c])
            if b_len == 1: continue
            if b_len >= min_len: continue
            min_len = b_len
            self.shortest = c

    def move(self):
        moves = []
        for n in self.cells[self.shortest]:
            cells = copy.deepcopy(self.cells)
            cells[self.shortest] = [n,]
            try:
                moves.append( Board(cells) )
            except:
                pass
        
        return moves

def compareBoards(lhs,rhs):
    diff = rhs.total - lhs.total
    if diff: return diff
    return len(rhs.cells[rhs.shortest]) - len(lhs.cells[lhs.shortest])
    


_searched = 0
_backtracks = 0

def search(board):
    global _searched
    _searched += 1
    if len(board.cells) == board.total:
        raise board
        
    print "Branch:"
    printBoard(board)

    moves = board.move()
    moves.sort(compareBoards)
    
    for m in moves:
        search(m)
        global _backtracks
        _backtracks += 1

def solve(board):
    try:
        search(board)
        print "No Solution"
    except Board, solution:
        print "Solution:"
        printBoard(solution)
    print "%d positions examined, %d backtracks" % (_searched, _backtracks,)

problem = sys.stdin.readlines()
problem = [ p[:-1] for p in problem]

solve(Board(parseCells(problem)))
