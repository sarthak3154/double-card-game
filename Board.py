import numpy as np
from Cell import *

class Board:

    def __init__(self):
        self.matrix_data = np.empty((8, 12), dtype=object)

    def place_card(self,card):
        x1 = card.get_first_cell().get_x_coordinate()
        y1 = card.get_first_cell().get_y_coordinate()
        x2 = card.get_second_cell().get_x_coordinate()
        y2 = card.get_second_cell().get_y_coordinate()
        move_state = self.is_move_legal(x1, y1, x2, y2)
        if move_state == True:
            self.matrix_data[x1][y1] = card.get_first_cell()
            self.matrix_data[x2][y2] = card.second_cell()
            return True
        else:
            return False

    def get_cell_info(self,x,y):
        return self.matrix_data[x][y]

    def is_move_legal(self, x1, y1, x2, y2):
        if self.matrix_data[x1][y1-1] == None or self.matrix_data[x2][y1-1] == None:
            return False
        if x1 < 0 or x1 >= 7 or y1 < 0 or y2 >= 12:
            return False
        return True
