import os
from Cell import *

def cls():
    clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')
    clear()

def getXCoordinate(xCellPosition):
    return ord(xCellPosition) % ord('A')

def getYCoordinate(yCellPosition):
    return int(yCellPosition) - 1

def get_second_cell(rotation,x,y):
    if rotation[0] == "HORIZONTAL":
        return Cell(rotation[1],rotation[2],x+1,y)
    else:
        return Cell(rotation[1],rotation[2],x,y+1)
