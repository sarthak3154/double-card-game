import numpy as np
from Cell import *

class Board:

    def __init__(self, players):
        self.matrix_data = np.empty((12, 8), dtype=object)
        self.players = players
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
            self.is_winner_found = self.check_win(x1, y1, self.current_player.get_play_choice())
            return True
        else:
            print('Invalid Move! Please input a valid move')
            return False

    def get_cell_info(self,x,y):
        return self.matrix_data[x][y]

    def check_win(self,x, y, symbol):
        patterns = ["BLACK_DOT BLACK_DOT BLACK_DOT BLACK_DOT",
                    "WHITE_DOT WHITE_DOT WHITE_DOT WHITE_DOT",
                    "RED_COLOR RED_COLOR RED_COLOR RED_COLOR",
                    "WHITE_COLOR WHITE_COLOR WHITE_COLOR WHITE_COLOR"]
        current_row = self.matrix_data[:,y]
        current_column = self.matrix_data[x,:]
        diagonal1 = np.diagonal(self.matrix_data)
        diagonal2 = np.diagonal(np.fliplr(self.matrix_data))

        if symbol == 'COLOR' and (patterns[0] in self.get_data_string(current_row,symbol) or \
                                  patterns[1] in self.get_data_string(current_row,symbol) or \
                                  patterns[0] in self.get_data_string(current_column,symbol) or \
                                  patterns[1] in self.get_data_string(current_column,symbol) or \
                                  patterns[0] in self.get_data_string(diagonal1,symbol) or \
                                  patterns[1] in self.get_data_string(diagonal1,symbol) or \
                                  patterns[0] in self.get_data_string(diagonal2,symbol) or \
                                  patterns[1] in self.get_data_string(diagonal2,symbol)):
            return True
        elif symbol == 'DOTS' and (patterns[2] in self.get_data_string(current_row,symbol) or \
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

    def move_card(self, first_cell, second_cell, final_card):
        x1 = first_cell.get_x_coordinate()
        y1 = first_cell.get_y_coordinate()
        x2 = second_cell.get_x_coordinate()
        y2 = second_cell.get_y_coordinate()
        if self.is_recycler_move_legal(x1, y1, x2, y2) is False:
            print('Illegal Move. Cannot pick the card last chosen by another player')
            return False
        move_success = self.place_card(final_card)
        if move_success:
            self.matrix_data[x1][y1] = None
            self.matrix_data[x2][y2] = None
            return True
        else:
            return False

    def get_placed_cards_count(self):
        return self.placed_cards_count

    def is_winner_found(self):
        return self.is_winner_found

    def set_current_player(self,current_player):
        self.current_player = current_player

    def get_current_player(self):
        return self.current_player.get_play_choice

    def is_move_legal(self, x1, y1, x2, y2):
        if y1 > 0 and (self.matrix_data[x1][y1-1] == None or self.matrix_data[x2][y1-1] == None):
            return False
        if x1 < 0 or x1 >= 7 or y1 < 0 or y2 >= 12:
            return False
        return True

    def is_recycler_move_legal(self, x1, y1, x2, y2):
        last_card_x1 = self.last_card_placed.get_first_cell().get_x_coordinate()
        last_card_y1 = self.last_card_placed.get_first_cell().get_y_coordinate()
        last_card_x2 = self.last_card_placed.get_second_cell().get_x_coordinate()
        last_card_y2 = self.last_card_placed.get_second_cell().get_y_coordinate()
        if last_card_x1 != x1 or last_card_y1 != y1 or last_card_x2 != x2 or last_card_y2 != y2:
            return True
        return False
