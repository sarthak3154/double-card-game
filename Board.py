import numpy as np
from Cell import Cell

class Board(object):

    matrix_data = np.empty((8,12), dtype=object)

    def __int__(self,w,h):
        self.w = w
        self.h = h

    def place_card(self,rotation, x, y):
        direction = rotation[0]
        self.matrix_data[x][y] = Cell(rotation[1],rotation[2],x,y)

        if direction == 'HORIZONTAL':
            self.matrix_data[x+1][y] = Cell(rotation[1],rotation[2],x+1,y)
        else:
            self.matrix_data[x][y+1] = Cell(rotation[1],rotation[2],x,y+1)


    def get_cell_info(self,x,y):
        return self.matrix_data[x][y]
