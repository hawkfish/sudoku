# !/usr/bin/python3

from sudoku.cells import *

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

#   Find all the values used by a region
def findRegionValues(cells, region):
    values = [0 for v in range(0,9)]
    for c in region:
        if len(cells[c]) == 1:
            values[cells[c][0]] = 1
    return values

