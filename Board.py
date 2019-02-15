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
        self.matrix_data[x1][y1] = card.get_first_cell()
        self.matrix_data[x2][y2] = card.get_second_cell()

        self.check_win(x1,y1,"DOT")


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
