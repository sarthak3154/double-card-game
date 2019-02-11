import os
from utils import *
from Board import *
from Card import *
from Cell import *

print('\n\t\t:::: Double Board Game ::::')
NUM_PLAYERS = 2

def selectPlayMode():
    mode = input('\nSelect from the Play Modes: \n1. Human v Human\n2. Human v AI\n')
    if len(mode) > 1:
        print('Invalid Input! Choose from the default Play Modes.')
        return selectPlayMode()

    return int(mode)

def performPlayerMove(player, board):
    print('\nPlayer {0}, Your turn now...'.format(str(player + 1)))
    move = input('Play your move: ')
    moveInfo = move.split(' ')
    board.place_card(Card.ROTATIONS[int(moveInfo[1]) - 1],
        getXCoordinate(moveInfo[2]), getYCoordinate(moveInfo[3]))

n = -1
def nextPlayer():
    global n
    n+=1
    return n % NUM_PLAYERS

playMode = selectPlayMode()

if playMode == 1:
    print('\nYou have chosen to play in Manual Mode!')
    board = Board()
    isGameEnded = 0
    while isGameEnded is 0:
        performPlayerMove(nextPlayer(), board)
        isGameEnded = 1

    c = board.get_cell_info(0, 0)
    print(c.get_dot_type())
    print(board.matrix_data)
