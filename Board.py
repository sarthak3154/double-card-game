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
            return True
        else:
            print('Invalid Move! Please input a valid position')
            return False

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

    def get_cell_info(self, x, y):
        return self.matrix_data[x][y]

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
