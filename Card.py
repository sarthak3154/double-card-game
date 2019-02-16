from Board import Board
from Cell import *
from utils import *

class Card:

    def __init__(self,rotation, ycoordinate, xcoordinate):
        self.rotation = rotation
        self.first_cell = Cell(rotation[1] ,rotation[2],ycoordinate,xcoordinate)
        self.second_cell = get_second_cell(rotation, ycoordinate, xcoordinate)

    def get_first_cell(self):
        return self.first_cell

    def get_second_cell(self):
        return self.second_cell

    def get_rotation(self):
        return self.rotation
