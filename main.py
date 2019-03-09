import os

# from colored import fg, bg, attr
import numpy as np
from utils import *
from Board import *
from Card import *
from Cell import *
from MiniMax import *
from AlphaBeta import *
from Player import *
from StateNode import *
from State import State
from random import randint

# from tabulate import tabulate

DOT = ['BLACK_DOT', 'WHITE_DOT']
COLOR = ['RED_COLOR', 'WHITE_COLOR']
DIRECTION = ['HORIZONTAL', 'VERTICAL']
ROTATIONS = [[DIRECTION[0], DOT[0], COLOR[0], DOT[1], COLOR[1]],
             [DIRECTION[1], DOT[1], COLOR[1], DOT[0], COLOR[0]],
             [DIRECTION[0], DOT[1], COLOR[1], DOT[0], COLOR[0]],
             [DIRECTION[1], DOT[0], COLOR[0], DOT[1], COLOR[1]],
             [DIRECTION[0], DOT[1], COLOR[0], DOT[0], COLOR[1]],
             [DIRECTION[1], DOT[0], COLOR[1], DOT[1], COLOR[0]],
             [DIRECTION[0], DOT[0], COLOR[1], DOT[1], COLOR[0]],
             [DIRECTION[1], DOT[1], COLOR[0], DOT[0], COLOR[1]]]

print('\n\t\t:::: Double Board Game ::::')
NUM_PLAYERS = 2


def select_play_mode():
    mode = input('\nSelect from the Play Modes: \n1. Human v Human\n2. Human v AI\n')
    if len(mode) > 1 or (mode.isnumeric() and (int(mode) > 2 or int(mode) < 1)):
        print('Invalid Input! Choose from the default Play Modes.')
        return select_play_mode()

    return int(mode)


def select_computer_turn():
    mode = input('\nWhich turn does Computer will take (First or second) ?\nNote: use 1 and 2 for your input\n')
    if len(mode) > 1 or (mode.isnumeric() and (int(mode) > 2 or int(mode) < 1)):
        print('Invalid Input! Choose 1 or 2')
        return select_computer_turn()

    return int(mode)


def alpha_beta_trace_input():
    active = input('\nDo you want to activate alpha-beta algorithm  ?\n 1. Yes  2. No \n')
    if len(active) > 1 or (active.isnumeric() and (int(active) > 2 or int(active) < 1)):
        print('Invalid Input! Choose 1 or 2')
        return alpha_beta_trace_input()

    trace = input('\nDo you want to generate trace file ?\n 1. Yes  2. No \n')
    if len(trace) > 1 or (trace.isnumeric() and (int(trace) > 2 or int(trace) < 1)):
        print('Invalid Input! Choose 1 or 2')
        return alpha_beta_trace_input()

    is_active = True if int(active) is 1 else False
    is_trace = True if int(trace) is 1 else False

    return is_active, is_trace


def assign_player_choices(play_mode='human'):
    choice = input('\nPlayer 1, what do you want to play with? (dots or color): \n')
    choice = choice.upper()
    players = [None for i in range(NUM_PLAYERS)]
    players[0] = Player(choice, 'Player 1')
    players[1] = Player('COLOR' if choice == 'DOTS' else 'DOTS', 'Player 2' if play_mode == 'human' else 'AI')
    return players


def assign_computer_choices():
    random_number = randint(1, 2)
    choice = 'DOTS' if random_number is 1 else 'COLOR'
    print('\nAI has choosen to play with ' + choice)
    players = [None for i in range(NUM_PLAYERS)]
    players[0] = Player(choice, 'AI')
    players[1] = Player('COLOR' if choice == 'DOTS' else 'DOTS', 'You')
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
    cells = [first_cell, second_cell]
    if is_valid_pick_card_input(cells) is False:
        print('Invalid Input Card. Please input a valid card to be moved')
        return perform_player_recycling_move(board)
    final_card = Card(ROTATIONS[int(moveInfo[4]) - 1], get_col_coordinate(moveInfo[5]), get_row_coordinate(moveInfo[6]))
    move_success = board.move_card(ROTATIONS[get_orientation(cells) - 1], first_cell, second_cell, final_card)
    if move_success is False:
        return perform_player_recycling_move(board)
    return True


def is_valid_place_card_move(pick_card, place_card):
    if (pick_card.first_cell.x == place_card.first_cell.x and pick_card.first_cell.y == place_card.first_cell.y
            and pick_card.second_cell.x == place_card.second_cell.x and
            pick_card.second_cell.y == place_card.second_cell.y):
        if pick_card.rotation == place_card.rotation:
            return False
    return True


def generate_states_from_position(parent_state_node, position_moves, recycler_parent_node=None, pick_card=None):
    current_state = parent_state_node.get_data() if recycler_parent_node is None else recycler_parent_node.get_data()
    move_state_nodes = []
    for move in position_moves:
        x1 = move[0][0]
        y1 = move[0][1]
        x2 = move[1][0]
        for i in range(4):
            card = Card(ROTATIONS[(2 * i) if x1 == x2 else (2 * i + 1)], y1, x1)
            if pick_card is None or (pick_card is not None and is_valid_place_card_move(pick_card, card)):
                state = State(current_state, card)
                state_node = StateNode(state)
                state_node.parent = parent_state_node if recycler_parent_node is None else recycler_parent_node
                move_state_nodes.append(state_node)
    return move_state_nodes


def get_children_states(current_state_node, recycler_parent_node=None, pick_card=None):
    current_state = current_state_node.get_data()
    available_positions = current_state.get_placeable_available_positions()
    move_state_nodes = []
    for position in available_positions:
        position_moves = current_state.generate_init_position_moves(position)
        # print(position_moves)
        move_state_nodes = move_state_nodes + generate_states_from_position(current_state_node, position_moves, recycler_parent_node, pick_card)
    return move_state_nodes


def perform_ai_regular_move(current_state, board, ai_choice, is_active, is_trace):
    root_state_node = StateNode(current_state)
    root_state_node.children = get_children_states(root_state_node)
    leaf_nodes = []
    for child_state_node in root_state_node.children:
        child_state_node.children = get_children_states(child_state_node)
        leaf_nodes = leaf_nodes + child_state_node.children

    count = 0
    for leaf in leaf_nodes:
        leaf.heuristic_value = leaf.get_data().get_heuristic_value()
        count = count + 1

    decision_state_node = None
    algo = None
    if is_active:
        algo = AlphaBeta(root_state_node, ai_choice)
        decision_state_node = algo.alpha_beta_algorithm()
    else:
        algo = MiniMax(root_state_node, ai_choice)
        decision_state_node = algo.minimax_algorithm()

    if is_trace:
        f = open("tracemm.txt", "a+")
        f.write(str(count) + "\n")
        f.close()
        algo.write_nodes_data_to_trace_file()

    board.place_card(decision_state_node.data.card)


def get_recycler_move_children_states(current_state_node):
    card_positions = current_state_node.data.get_pickable_available_cards()
    children_state_nodes = []

    for position in card_positions:
        pick_state = State(board)
        pick_card = pick_state.get_card(ROTATIONS, position)
        pick_state.remove_card(position, pick_state.cards[position])
        state_node = StateNode(pick_state)
        children_state_nodes = children_state_nodes + get_children_states(state_node, current_state_node, pick_card)

    return children_state_nodes


def perform_ai_recycling_move(current_state, board):
    root_state_node = StateNode(current_state)
    root_state_node.children = get_recycler_move_children_states(root_state_node)

    for child_state_node in root_state_node.children:
        child_state_node.children = get_recycler_move_children_states(child_state_node)

    algo = MiniMax(root_state_node, ai_choice)
    decision_state_node = algo.minimax_algorithm()
    board.place_card(decision_state_node.data.card)


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
                print_matrix[i][j] = ('RC' if color_type == COLOR[0] else 'WC') + \
                                     ('*' if dot_type == DOT[0] else 'o')

    # print(tabulate(np.flip(print_matrix, 0), headers, tablefmt="fancy_grid"))
    flipped_matrix = np.flip(print_matrix, 0)
    print('\n'.join(
        [''.join(['{:5}'.format(item if item is not '' else 'None') for item in row]) for row in flipped_matrix]))
    print(''.join('{:5}'.format(index) for index in headers))


n = -1


def next_player():
    global n
    n += 1
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
        print(str(board.get_current_player().get_player_name()) + " with play choice " + str(
            board.get_current_player().get_play_choice()) + " won the game ")
    else:
        print('Game draw!')

if playMode == 2:
    print('\nYou have chosen to play with Computer!')
    (is_active, is_trace) = alpha_beta_trace_input()
    turn = select_computer_turn()
    if turn is 1:
        players = assign_computer_choices()
        ai_choice = players[0].play_choice
    elif turn is 2:
        players = assign_player_choices('ai')
        ai_choice = players[1].play_choice

    board = Board(players)
    headers = [str(chr(64 + i + 1)) for i in range(np.size(board.matrix_data, 1))]
    print_board(board)

    while board.get_placed_cards_count() < 8 and board.is_winner_found is False:
        current_player = players[next_player()]
        print('\n{0}, Your turn now...'.format(str(current_player.get_player_name())))
        board.set_current_player(current_player)
        if current_player.get_player_name() == 'AI':
            current_state = State(board)
            perform_ai_regular_move(current_state, board, ai_choice, is_active, is_trace)
        else:
            perform_player_regular_move(board)
        print_board(board)

    current_state = State(board)
    perform_ai_recycling_move(current_state, board)
