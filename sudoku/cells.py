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
