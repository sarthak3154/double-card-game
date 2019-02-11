import os

def cls():
    clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')
    clear()

def getXCoordinate(xCellPosition):
    return ord(xCellPosition) % ord('A')

def getYCoordinate(yCellPosition):
    return int(yCellPosition) - 1
