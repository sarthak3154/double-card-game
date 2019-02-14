import os
from utils import *
from Board import *
from Card import *
from Cell import *
from Player import *

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

def assign_player_choices():
    choice = input('\nPlayer 1, what do you want to play with? (dots or color): ')
    choice = choice.lower()
    players = [None for i in range(NUM_PLAYERS)]
    players[0] = Player(choice)
    players[1] = Player('color' if choice == 'dots' else 'dots')
    return players

def perform_player_regular_move(board):
    move = input('Play your move: \n')
    moveInfo = move.split(' ')
    card = Card(ROTATIONS[int(moveInfo[1]) - 1], getXCoordinate(moveInfo[2]), getYCoordinate(moveInfo[3]))
    move_success = board.place_card(card)
    if move_success == False:
        return perform_player_regular_move(board)
    return True

def perform_player_recycling_move(board):
    move = input('Play your move: \n')
    moveInfo = move.split(' ')
    first_cell = board.get_cell_info(getXCoordinate(moveInfo[0]), getYCoordinate(moveInfo[1]))
    second_cell = board.get_cell_info(getXCoordinate(moveInfo[2]), getYCoordinate(moveInfo[3]))
    final_card = Card(ROTATIONS[int(moveInfo[4]) - 1], getXCoordinate(moveInfo[5]), getYCoordinate(moveInfo[6]))
    move_success = board.move_card(first_cell, second_cell, final_card)
    if move_success == False:
        return perform_player_recycling_move(board)
    return True

n = -1
def nextPlayer():
    global n
    n+=1
    return n % NUM_PLAYERS

playMode = select_play_mode()

if playMode == 1:
    print('\nYou have chosen to play in Manual Mode!')
    players = assign_player_choices()
    board = Board(players)
    while board.get_placed_cards_count() < 24 and board.get_winner() == None:
        print('\nPlayer {0}, Your turn now...'.format(str(nextPlayer() + 1)))
        perform_player_regular_move(board)

    while board.get_winner() == None:
        print('\nPlayer {0}, Your turn now for the recycling move...'.format(str(nextPlayer() + 1)))
        perform_player_recycling_move(board)

    if board.get_winner() != None:
        print(board.get_winner())
    else:
        print('Game draw!')
