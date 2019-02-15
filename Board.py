import numpy as np
from Cell import *

class Board:

    def __init__(self, players):
        self.matrix_data = np.empty((8, 12), dtype=object)
        self.players = players
        self.placed_cards_count = 0
        self.winner = None

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
            self.check_win(x1, y1, "DOT")
            return True
        else:
            print('Invalid Move! Please input a valid position')
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

        if symbol == 'COLOR' and (patterns[0] in self.get_data_string(current_row) or \
                                  patterns[1] in self.get_data_string(current_row) or \
                                  patterns[0] in self.get_data_string(current_column) or \
                                  patterns[1] in self.get_data_string(current_column) or \
                                  patterns[0] in self.get_data_string(diagonal1) or \
                                  patterns[1] in self.get_data_string((diagonal1)) or \
                                  patterns[0] in self.get_data_string(diagonal2) or \
                                  patterns[1] in self.get_data_string((diagonal2))):
            return True
        elif symbol == 'DOT' and (patterns[2] in self.get_data_string(current_row) or \
                                  patterns[3] in self.get_data_string(current_row) or \
                                  patterns[2] in self.get_data_string(current_column) or \
                                  patterns[3] in self.get_data_string(current_column) or \
                                  patterns[2] in self.get_data_string(diagonal1) or \
                                  patterns[3] in self.get_data_string((diagonal1)) or \
                                  patterns[2] in self.get_data_string(diagonal2) or \
                                  patterns[3] in self.get_data_string((diagonal2))):
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
        move_success = self.place_card(final_card)
        if move_success:
            self.matrix_data[x1][y1] = None
            self.matrix_data[x2][y2] = None
            return True
        else:
            return False

    def get_placed_cards_count(self):
        return self.placed_cards_count

    def get_winner(self):
        return self.winner

    def is_move_legal(self, x1, y1, x2, y2):
        if y1 > 0 and (self.matrix_data[x1][y1-1] == None or self.matrix_data[x2][y1-1] == None):
                return False
        if x1 < 0 or x1 >= 7 or y1 < 0 or y2 >= 12:
            return False
        return True
