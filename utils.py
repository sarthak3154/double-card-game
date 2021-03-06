import os
from Cell import *


def cls():
    clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')
    clear()


def get_row_coordinate(xCellPosition):
    return int(xCellPosition) - 1


def get_col_coordinate(yCellPosition):
    return ord(yCellPosition) % ord('A')


def get_second_cell(rotation,y,x):
    if rotation[0] == "VERTICAL":
        return Cell(rotation[3],rotation[4],y,x+1)
    else:
        return Cell(rotation[3],rotation[4],y+1,x)


def is_valid_pick_card_input(cells):
    if cells[0] == None or cells[1] == None:
        return False
    x1 = cells[0].get_x_coordinate()
    x2 = cells[1].get_x_coordinate()
    y1 = cells[0].get_y_coordinate()
    y2 = cells[1].get_y_coordinate()
    if abs(x1 - x2) > 1 or abs(y1 - y2) > 1:
        return False
    if x1 != x2 and y1 != y2:
        return False
    return True


def get_orientation(cells):
    x1 = cells[0].get_x_coordinate()
    x2 = cells[1].get_x_coordinate()
    y1 = cells[0].get_y_coordinate()
    y2 = cells[1].get_y_coordinate()
    dot_type_1 = cells[0].get_dot_type()
    dot_type_2 = cells[1].get_dot_type()
    color_type_1 = cells[0].get_color_type()
    color_type_2 = cells[1].get_color_type()

    if y2 - y1 > 0 and x2 - x1 is 0 and dot_type_1 is "BLACK_DOT" and color_type_1 is "RED_COLOR" and dot_type_2 is "WHITE_DOT" and color_type_2 is "WHITE_COLOR":
        return 1

    if y2 - y1 is 0 and x2 - x1 > 0 and dot_type_1 is "WHITE_DOT" and color_type_1 is "WHITE_COLOR" and dot_type_2 is "BLACK_DOT" and color_type_2 is "RED_COLOR":
        return 2

    if y2 - y1 > 0 and x2 - x1 is 0 and dot_type_1 is "WHITE_DOT" and color_type_1 is "WHITE_COLOR" and dot_type_2 is "BLACK_DOT" and color_type_2 is "RED_COLOR":
        return 3

    if y2 - y1 is 0 and x2 - x1 > 0 and dot_type_1 is "BLACK_DOT" and color_type_1 is "RED_COLOR" and dot_type_2 is "WHITE_DOT" and color_type_2 is "WHITE_COLOR":
        return 4

    if y2 - y1 > 0 and x2 - x1 is 0 and dot_type_1 is "WHITE_DOT" and color_type_1 is "RED_COLOR" and dot_type_2 is "BLACK_DOT" and color_type_2 is "WHITE_COLOR":
        return 5

    if y2 - y1 is 0 and x2 - x1 > 0 and dot_type_1 is "BLACK_DOT" and color_type_1 is "WHITE_COLOR" and dot_type_2 is "WHITE_DOT" and color_type_2 is "RED_COLOR":
        return 6

    if y2 - y1 > 0 and x2 - x1 is 0 and dot_type_1 is "BLACK_DOT" and color_type_1 is "WHITE_COLOR" and dot_type_2 is "WHITE_DOT" and color_type_2 is "RED_COLOR":
        return 7

    if y2 - y1 is 0 and x2 - x1 > 0 and dot_type_1 is "WHITE_DOT" and color_type_1 is "RED_COLOR" and dot_type_2 is "BLACK_DOT" and color_type_2 is "WHITE_COLOR":
        return 8