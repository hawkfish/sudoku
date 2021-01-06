#!/usr/bin/python3

def readFixture(sdk):
    f = open(sdk, 'r')
    lines = f.readlines()
    f.close()
    return [ line.strip('\n') for line in lines]

def valuesFromDisplay(display):
    return [value-1 for value in display]
