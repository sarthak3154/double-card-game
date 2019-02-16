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
    if rotation[0] == "VERTICAL":
        return Cell(rotation[3],rotation[4],x+1,y)
    else:
        return Cell(rotation[3],rotation[4],x,y+1)

def is_valid_card_input(cells):
    if cells[0] == None or cells[1] == None:
        return False
    x1 = cells[0].get_x_coordinate();
    x2 = cells[1].get_x_coordinate()
    y1 = cells[0].get_y_coordinate()
    y2 = cells[1].get_y_coordinate()
    if abs(x1 - x2) > 1 or abs(y1 - y2) > 1:
        return False
    if x1 != x2 and y1 != y2:
        return False
    return True
