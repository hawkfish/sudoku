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
    lines = formatCells(board._cells)
    print('\n'.join(lines))

