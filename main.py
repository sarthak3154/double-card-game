import os
from utils import *
from Board import *
from Card import *
from Cell import *

DOT = ['BLACK','WHITE']
COLOR = ['RED','WHITE']
DIRECTION = ['HORIZONTAL' , 'VERTICAL']
ROTATIONS = [[DIRECTION[0],DOT[0],COLOR[0],DOT[1],COLOR[1]],
             [DIRECTION[1],DOT[1],COLOR[1],DOT[0],COLOR[0]],
             [DIRECTION[0],DOT[1],COLOR[1],DOT[0],COLOR[0]],
             [DIRECTION[1],DOT[0],COLOR[0],DOT[1],COLOR[1]],
             [DIRECTION[0],DOT[1],COLOR[0],DOT[0],COLOR[1]],
             [DIRECTION[1],DOT[0],COLOR[1],DOT[1],COLOR[0]],
             [DIRECTION[0],DOT[0],COLOR[1],DOT[1],COLOR[0]],
             [DIRECTION[1],DOT[1],COLOR[0],DOT[0],COLOR[1]]]

print('\n\t\t:::: Double Board Game ::::')
NUM_PLAYERS = 2

def select_play_mode():
    mode = input('\nSelect from the Play Modes: \n1. Human v Human\n2. Human v AI\n')
    if len(mode) > 1:
        print('Invalid Input! Choose from the default Play Modes.')
        return select_play_mode()

    return int(mode)

def perform_player_move(player, board):
    print('\nPlayer {0}, Your turn now...'.format(str(player + 1)))
    move = input('Play your move: \n')
    moveInfo = move.split(' ')
    card = Card(ROTATIONS[int(moveInfo[1]) - 1],getXCoordinate(moveInfo[2]),getYCoordinate(moveInfo[3]))
    board.place_card(card)

n = -1
def nextPlayer():
    global n
    n+=1
    return n % NUM_PLAYERS

playMode = select_play_mode()

if playMode == 1:
    print('\nYou have chosen to play in Manual Mode!')
    board = Board()
    isGameEnded = 0
    while isGameEnded is 0:
        perform_player_move(nextPlayer(), board)
        print(board.matrix_data)
        isGameEnded = 1
