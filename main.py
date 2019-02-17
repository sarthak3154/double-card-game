import os

# from colored import fg, bg, attr
import numpy as np
from utils import *
from Board import *
from Card import *
from Cell import *
from Player import *
#from tabulate import tabulate

DOT = ['BLACK_DOT','WHITE_DOT']
COLOR = ['RED_COLOR','WHITE_COLOR']
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
    if len(mode) > 1 or (mode.isnumeric() and (int(mode) > 2 or int(mode) < 1)):
        print('Invalid Input! Choose from the default Play Modes.')
        return select_play_mode()

    return int(mode)


def assign_player_choices():
    choice = input('\nPlayer 1, what do you want to play with? (dots or color): \n')
    choice = choice.upper()
    players = [None for i in range(NUM_PLAYERS)]
    players[0] = Player(choice,'Player 1')
    players[1] = Player('COLOR' if choice == 'DOTS' else 'DOTS' , 'Player 2')
    return players


def perform_player_regular_move(board):
    move = input('Play your move: \n')
    moveInfo = move.split(' ')
    card = Card(ROTATIONS[int(moveInfo[1]) - 1], get_col_coordinate(moveInfo[2]), get_row_coordinate(moveInfo[3]))
    move_success = board.place_card(card)
    if move_success is False:
        return perform_player_regular_move(board)
    return True


def perform_player_recycling_move(board):
    move = input('Play your move: \n')
    moveInfo = move.split(' ')
    first_cell = board.get_cell_info(get_row_coordinate(moveInfo[1]), get_col_coordinate(moveInfo[0]))
    second_cell = board.get_cell_info(get_row_coordinate(moveInfo[3]), get_col_coordinate(moveInfo[2]))
    if is_valid_pick_card_input([first_cell, second_cell]) is False:
        print('Invalid Input Card. Please input a valid card to be moved')
        return perform_player_recycling_move(board)
    final_card = Card(ROTATIONS[int(moveInfo[4]) - 1], get_col_coordinate(moveInfo[5]), get_row_coordinate(moveInfo[6]))
    move_success = board.move_card(first_cell, second_cell, final_card)
    if move_success is False:
        return perform_player_recycling_move(board)
    return True


dt = np.dtype('U10')

def print_board(board):
    print_matrix = np.empty((12, 8), dtype=dt)
    # iteate over rows
    for i in range(np.size(board.matrix_data, 0)):
        # iterate over colums
        for j in range(np.size(board.matrix_data, 1)):
            if board.matrix_data[i][j] is not None:
                dot_type = board.matrix_data[i][j].get_dot_type()
                color_type = board.matrix_data[i][j].get_color_type()
                print_matrix[i][j] = ('RC' if color_type == COLOR[0] else 'WC') +\
                                 ('*' if dot_type == DOT[0] else 'o')

    #print(tabulate(np.flip(print_matrix, 0), headers, tablefmt="fancy_grid"))
    print(np.flip(print_matrix,0))

n = -1


def next_player():
    global n
    n+=1
    return n % NUM_PLAYERS


playMode = select_play_mode()

if playMode == 1:
    print('\nYou have chosen to play in Manual Mode!')
    players = assign_player_choices()
    board = Board(players)
    headers = [str(chr(64 + i + 1)) for i in range(np.size(board.matrix_data, 1))]
    print_board(board)

    while board.get_placed_cards_count() < 24 and board.is_winner_found is False:
        current_player = next_player()
        print('\nPlayer {0}, Your turn now...'.format(str(current_player + 1)))
        board.set_current_player(players[current_player])
        perform_player_regular_move(board)
        print_board(board)

    while board.is_winner_found is False and board.get_placed_cards_count() < 60:
        current_player = next_player()
        print('\nPlayer {0}, Your turn now for the recycling move...'.format(str(current_player + 1)))
        board.set_current_player(players[current_player])
        perform_player_recycling_move(board)
        print_board(board)

    if board.is_winner_found is True:
        print(str(board.get_current_player().get_player_name()) + " with play choice " + str(board.get_current_player().get_play_choice()) + " won the game ")
    else:
        print('Game draw!')