import numpy as np
from Cell import *

class Board(object):

    def __int__(self,w,h):
        self.w = w
        self.h = h
        self.matrix_data = np.empty((8, 12), dtype=object)

    def place_card(self,card):
        x1 = card.get_first_cell().get_x_coordinate()
        y1 = card.get_first_cell().get_y_coordinate()
        x2 = card.get_second_cell().get_x_coordinate()
        y2 = card.get_second_cell().get_y_coordinate()
        self.matrix_data[x1][y1] = card.get_first_cell()
        self.matrix_data[x2][y2] = card.second_cell()

    def get_cell_info(self,x,y):
        return self.matrix_data[x][y]
