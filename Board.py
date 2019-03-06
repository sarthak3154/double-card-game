import numpy as np
from Cell import *


class Board:

    white_circle = []
    red_circle = []
    white_dot = []
    red_dot = []

    def __init__(self, players):
        self.matrix_data = np.empty((12, 8), dtype=object)
        self.players = players
        self.cards = {}
        self.placed_cards_count = 0
        self.last_card_placed = None
        self.current_player = None
        self.is_winner_found = False

    def place_card(self, card):
        x1 = card.get_first_cell().get_x_coordinate()
        y1 = card.get_first_cell().get_y_coordinate()
        x2 = card.get_second_cell().get_x_coordinate()
        y2 = card.get_second_cell().get_y_coordinate()
        move_state = self.is_move_legal(x1, y1, x2, y2)
        if move_state:
            self.matrix_data[x1][y1] = card.get_first_cell()
            self.matrix_data[x2][y2] = card.get_second_cell()
            self.placed_cards_count += 1
            self.last_card_placed = card
            self.add_coordinates_to_specific_list(card.get_first_cell(),(x1,y1))
            self.add_coordinates_to_specific_list(card.get_second_cell(),(x2, y2))
            self.cards[(x1, y1)] = (x2, y2)
            self.cards[(x2, y2)] = (x1, y1)
            self.is_winner_found = self.check_win(x1, y1, self.current_player.get_play_choice()) or \
                self.check_win(x2, y2, self.current_player.get_play_choice())
            return True
        else:
            print('Invalid Move! Please input a valid move')
            return False

    def get_cell_info(self,x,y):
        return self.matrix_data[x][y]

    def add_coordinates_to_specific_list(self,cell,coordinates):
        if cell.get_color_type() == 'WHITE_COLOR' and cell.get_dot_type() == 'WHITE_DOT':
            self.white_circle.append(coordinates)
        if cell.get_color_type() == 'WHITE_COLOR' and cell.get_dot_type() == 'BLACK_DOT':
            self.white_dot.append(coordinates)
        if cell.get_color_type() == 'RED_COLOR' and cell.get_dot_type() == 'WHITE_DOT':
            self.red_circle.append(coordinates)
        if cell.get_color_type() == 'RED_COLOR' and cell.get_dot_type() == 'BLACK_DOT':
            self.red_dot.append(coordinates)

    def check_win(self,x, y, symbol):
        patterns = ["BLACK_DOT BLACK_DOT BLACK_DOT BLACK_DOT",
                    "WHITE_DOT WHITE_DOT WHITE_DOT WHITE_DOT",
                    "RED_COLOR RED_COLOR RED_COLOR RED_COLOR",
                    "WHITE_COLOR WHITE_COLOR WHITE_COLOR WHITE_COLOR"]
        current_row = self.matrix_data[:,y]
        current_column = self.matrix_data[x,:]
        diagonal1 = np.diagonal(self.matrix_data,y-x)
        diagonal2 = np.diagonal(np.fliplr(self.matrix_data), np.size(self.matrix_data,1) - 1 - y - x)

        if symbol == 'DOTS' and (patterns[0] in self.get_data_string(current_row,symbol) or \
                                  patterns[1] in self.get_data_string(current_row,symbol) or \
                                  patterns[0] in self.get_data_string(current_column,symbol) or \
                                  patterns[1] in self.get_data_string(current_column,symbol) or \
                                  patterns[0] in self.get_data_string(diagonal1,symbol) or \
                                  patterns[1] in self.get_data_string(diagonal1,symbol) or \
                                  patterns[0] in self.get_data_string(diagonal2,symbol) or \
                                  patterns[1] in self.get_data_string(diagonal2,symbol)):
            return True
        elif symbol == 'COLOR' and (patterns[2] in self.get_data_string(current_row,symbol) or \
                                  patterns[3] in self.get_data_string(current_row,symbol) or \
                                  patterns[2] in self.get_data_string(current_column,symbol) or \
                                  patterns[3] in self.get_data_string(current_column,symbol) or \
                                  patterns[2] in self.get_data_string(diagonal1,symbol) or \
                                  patterns[3] in self.get_data_string(diagonal1,symbol) or \
                                  patterns[2] in self.get_data_string(diagonal2,symbol) or \
                                  patterns[3] in self.get_data_string(diagonal2,symbol)):
            return True
        else:
            return False

    def get_data_string(self, direction, symbol):
        if symbol == "COLOR":
            return ' '.join(["None" if cell is None else cell.get_color_type() for cell in direction])
        else:
            return ' '.join(["None" if cell is None else cell.get_dot_type() for cell in direction])

    def move_card(self, rotation, first_cell, second_cell, final_card):
        x1 = first_cell.get_x_coordinate()
        y1 = first_cell.get_y_coordinate()
        x2 = second_cell.get_x_coordinate()
        y2 = second_cell.get_y_coordinate()
        if self.is_recycler_move_legal(x1, y1, x2, y2) is False:
            return False
        if self.is_same_position_place_move_legal(rotation, x1, y1, x2, y2, final_card) is False:
            return False
        self.matrix_data[x1][y1] = None
        self.matrix_data[x2][y2] = None
        del self.cards[(x1, y1)]
        del self.cards[(x2, y2)]
        move_success = self.place_card(final_card)
        if move_success:
            return True
        else:
            self.matrix_data[x1][y1] = first_cell
            self.matrix_data[x2][y2] = second_cell
            self.cards[(x1, y1)] = (x2, y2)
            self.cards[(x2, y2)] = (x1, y1)
            return False

    def get_placed_cards_count(self):
        return self.placed_cards_count

    def is_winner_found(self):
        return self.is_winner_found

    def set_current_player(self,current_player):
        self.current_player = current_player

    def get_current_player(self):
        return self.current_player

    def is_move_legal(self, x1, y1, x2, y2):
        if self.matrix_data[x1][y1] is not None or self.matrix_data[x2][y2] is not None:
            return False
        if x1 > 0 and (self.matrix_data[x1-1][y1] is None or (y1 != y2 and self.matrix_data[x1-1][y2] is None)):
            return False
        if x1 < 0 or x2 >= 12 or y1 < 0 or y2 >= 8:
            return False
        return True

    def is_recycler_move_legal(self, x1, y1, x2, y2):
        last_card_x1 = self.last_card_placed.get_first_cell().get_x_coordinate()
        last_card_y1 = self.last_card_placed.get_first_cell().get_y_coordinate()
        last_card_x2 = self.last_card_placed.get_second_cell().get_x_coordinate()
        last_card_y2 = self.last_card_placed.get_second_cell().get_y_coordinate()
        if self.cards.get((x1, y1)) == None or self.cards.get((x2, y2)) == None \
                or self.cards[(x1, y1)] != (x2, y2) or self.cards[(x2, y2)] != (x1, y1):
            print('Illegal Move. This is not a card placed at the board')
            return False

        if (x1 == x2 and (self.get_cell_info(x1 + 1, y1) != None or self.get_cell_info(x1 + 1, y2) != None)) \
                or self.get_cell_info(x2 + 1, y1) != None:
            print('Illegal Move. Cannot pick this card. Pick any card from the top')
            return False

        if last_card_x1 != x1 or last_card_y1 != y1 or last_card_x2 != x2 or last_card_y2 != y2:
            return True

        print('Illegal Move. Cannot pick this card last chosen by another player')
        return False

    def is_same_position_place_move_legal(self, rotation, x1, y1, x2, y2, final_card):
        final_x1 = final_card.get_first_cell().get_x_coordinate()
        final_y1 = final_card.get_first_cell().get_y_coordinate()
        final_x2 = final_card.get_second_cell().get_x_coordinate()
        final_y2 = final_card.get_second_cell().get_y_coordinate()
        if final_x1 != x1 or final_y1 != y1 or final_x2 != x2 or final_y2 != y2 or rotation != final_card.get_rotation():
            return True

        print('Illegal Move. Same position placement attempt with same rotation')
        return False

    def get_max_fillable_row(self):
        BLANK_STATE = np.empty(np.size(self.matrix_data, 1), dtype=object)
        for i in range(np.size(self.matrix_data, 0)):
            if np.array_equal(self.matrix_data[i], BLANK_STATE):
                return i + 1
        return -1

    def get_valid_empty_positions_in_row(self, row):
        empty = []
        for j in range(np.size(self.matrix_data, 1)):
            if self.matrix_data[row][j] is None and (row == 0 or self.matrix_data[i-1][j] is not None):
                empty.append((row, j))
        return empty

    def get_placeable_available_positions(self):
        rows, cols = np.where(self.matrix_data == None)
        rows = np.unique(rows)
        max_fillable_row = self.get_max_fillable_row()
        available_positions = []
        for i in range(max_fillable_row):
            if i in rows:
                empty_row_elements = self.get_valid_empty_positions_in_row(i)
                available_positions = available_positions + empty_row_elements
        return available_positions
