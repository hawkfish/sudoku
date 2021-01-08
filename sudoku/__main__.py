# !/usr/bin/python3

import argparse
import sys
from solver import *

def onMoved():
    finished = False

    def showBoard(board, label):
        print(label)
        print("-" * 11)
        printBoard(board)
        sys.stdout.write( '> ' )
        sys.stdout.flush()

        nonlocal finished
        cmd = sys.stdin.readline().strip()
        if cmd == 'q': sys.exit(0)
        if cmd == 'f': finished = True

    def showMoves(board, c, delta):
        if finished: return

        if c < 0:
            showBoard(board, "Branch:")
            return

        if not delta: return
        if len(board._cells[c]) != 1: return

        showBoard(board, f"Cell {row(c)+1}, {col(c)+1}:")

    return showMoves

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Solve a Sudoku problem read from stdin')
    parser.add_argument( 'files', metavar='file', type=str, nargs='*', help="Problem files to read and solve.")
    parser.add_argument('-k', '--king', action='store_true', help="Use King's move restrictions")
    parser.add_argument('-n', '--knight', action='store_true', help="Use Knight's move restrictions")
    parser.add_argument('-a', '--adjacent', action='store_true', help="Use adjacency restrictions")
    parser.add_argument('-i', '--interactive', action='store_true', help="Interactive mode")

    args = parser.parse_args()
    rules = [
        reduceRow,
        reduceCol,
        reduceBox,
    ]
    if args.king: rules.append(reduceKing)
    if args.knight: rules.append(reduceKnight)
    if args.adjacent: rules.append(reduceAdjacent)

    for filename in args.files:
        f = open(filename, 'r')
        problem = f.readlines()
        problem = [ p[:-1] for p in problem]
        f.close()

        solver = Solver()

        board = Board(parseCells(problem), rules)
        print("Problem:")
        print("-" * 11)
        printBoard(board)
        print()

        callback = None
        if args.interactive: callback = onMoved()

        solution = solver.solve(board, callback)
        if solution:
            print("Solution:")
            print("-" * 11)
            printBoard(solution)
            print()

        else:
            print("No Solution")

        print("%d positions examined, %d backtracks" % (solver._searched, solver._backtracks,))
