#!/usr/bin/python3

import os

def readFixture(sdk):
    f = open(os.path.join('tests', 'fixtures', sdk), 'r')
    lines = f.readlines()
    f.close()
    return [ line.strip('\n') for line in lines]

def valuesFromDisplay(display):
    return [value-1 for value in display]
