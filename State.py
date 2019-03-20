import numpy as np

from Card import Card
from utils import get_orientation


class State:

    def __init__(self, current_level_state, new_card=None, pick_card=None):
        self.placed_cards_count = current_level_state.placed_cards_count
        self.last_card_placed = current_level_state.last_card_placed
        self.cards = current_level_state.cards.copy()
        if new_card is not None:
            if pick_card is not None:
                self.pick_card = pick_card
            self.current_level_matrix = current_level_state.current_level_matrix.copy()
            self.white_circle_coordinates = current_level_state.white_circle_coordinates.copy()
            self.red_circle_coordinates = current_level_state.red_circle_coordinates.copy()
            self.white_dot_coordinates = current_level_state.white_dot_coordinates.copy()
            self.red_dot_coordinates = current_level_state.red_dot_coordinates.copy()
            self.card = new_card
            self.place_new_card(new_card)
        else:
            self.current_level_matrix = current_level_state.matrix_data.copy()
            self.white_circle_coordinates = current_level_state.white_circle.copy()
            self.red_circle_coordinates = current_level_state.red_circle.copy()
            self.white_dot_coordinates = current_level_state.white_dot.copy()
            self.red_dot_coordinates = current_level_state.red_dot.copy()

    def place_new_card(self, card):
        x1 = card.get_first_cell().get_x_coordinate()
        y1 = card.get_first_cell().get_y_coordinate()
        x2 = card.get_second_cell().get_x_coordinate()
        y2 = card.get_second_cell().get_y_coordinate()
        move_state = self.is_move_legal(x1, y1, x2, y2)
        if move_state:
            self.current_level_matrix[x1][y1] = card.get_first_cell()
            self.current_level_matrix[x2][y2] = card.get_second_cell()
            self.placed_cards_count += 1
            self.last_card_placed = card
            self.cards[(x1, y1)] = (x2, y2)
            self.cards[(x2, y2)] = (x1, y1)
            self.add_coordinates_to_specific_list(card.get_first_cell(), (x1, y1))
            self.add_coordinates_to_specific_list(card.get_second_cell(), (x2, y2))
            return True
        else:
            return False

    def add_coordinates_to_specific_list(self, cell, coordinates):
        if cell.get_color_type() == 'WHITE_COLOR' and cell.get_dot_type() == 'WHITE_DOT':
            self.white_circle_coordinates.append(coordinates)
        if cell.get_color_type() == 'WHITE_COLOR' and cell.get_dot_type() == 'BLACK_DOT':
            self.white_dot_coordinates.append(coordinates)
        if cell.get_color_type() == 'RED_COLOR' and cell.get_dot_type() == 'WHITE_DOT':
            self.red_circle_coordinates.append(coordinates)
        if cell.get_color_type() == 'RED_COLOR' and cell.get_dot_type() == 'BLACK_DOT':
            self.red_dot_coordinates.append(coordinates)

    def get_heuristic_value(self):
        white_circle_value = 0
        white_dot_value = 0
        red_circle_value = 0
        red_dot_value = 0

        for (x, y) in self.white_circle_coordinates:
            white_circle_value = white_circle_value + int(str(x) + str((y + 1)))

        for (x, y) in self.white_dot_coordinates:
            white_dot_value = white_dot_value + int(str(x) + str((y + 1)))

        for (x, y) in self.red_circle_coordinates:
            red_circle_value = red_circle_value + int(str(x) + str((y + 1)))

        for (x, y) in self.red_dot_coordinates:
            red_dot_value = red_dot_value + int(str(x) + str((y + 1)))

        return round(white_circle_value + (3 * white_dot_value) - (2 * red_dot_value) - (1.5 * red_circle_value), 2)

    def find_color_count(self, start, end, x, y, color_type, direction, step=1):
        var_count = 0

        for i in range(start, end, step):
            x = x + i if direction == 1 or direction == 2 else x
            y = y + i if direction == 0 or direction == 2 else y
            if direction == 3 and step == 1:
                y = y + i
                x = x - i
            elif direction == 3 and step == -1:
                x = x + i
                y = y - i

            if 0 <= x < 12 and 8 > y >= 0:
                if self.current_level_matrix[x][y] is not None:
                    if self.current_level_matrix[x][y].get_color_type() == color_type:
                        var_count += 1
                    else:
                        break

        if var_count == 3:
            var_count += 2000
        elif var_count == 2:
            var_count += 100
        elif var_count == 1:
            var_count += 10

        return var_count

    def find_dot_count(self, start, end, x, y, dot_type, direction, step=1):
        var_count = 0

        for i in range(start, end, step):
            x = x + i if direction == 1 or direction == 2 else x
            y = y + i if direction == 0 or direction == 2 else y
            if direction == 3 and step == 1:
                y = y + i
                x = x - i
            elif direction == 3 and step == -1:
                x = x + i
                y = y - i

            if 0 <= x < 12 and 8 > y >= 0:
                if self.current_level_matrix[x][y] is not None:
                    if self.current_level_matrix[x][y].get_dot_type() == dot_type:
                        var_count -= 1
                    else:
                        break

        if var_count == -3:
            var_count -= 2000
        elif var_count == 2:
            var_count -= 100
        elif var_count == -1:
            var_count -= 10

        return var_count

    def get_first_informed_heuristic_value(self, parent_card_placed, type):
        first_cell = self.last_card_placed.get_first_cell()
        second_cell = self.last_card_placed.get_second_cell()
        x1 = first_cell.get_x_coordinate()
        y1 = first_cell.get_y_coordinate()
        x2 = second_cell.get_x_coordinate()
        y2 = second_cell.get_y_coordinate()

        parent_first_cell = parent_card_placed.get_first_cell()
        parent_second_cell = parent_card_placed.get_second_cell()
        opponent_type = 'DOTS' if type == 'COLOR' else 'COLOR'
        if self.check_win(parent_first_cell.x, parent_first_cell.y, type) or \
                self.check_win(parent_second_cell.x, parent_second_cell.y, type):
            return 3000 if type == 'COLOR' else -3000
        if self.check_win(parent_first_cell.x, parent_first_cell.y, opponent_type) or \
                self.check_win(parent_second_cell.x, parent_second_cell.y, opponent_type):
            return -3000 if type == 'COLOR' else 3000

        color_type_1 = self.current_level_matrix[x1][y1].get_color_type()
        color_type_2 = self.current_level_matrix[x2][y2].get_color_type()
        dot_type_1 = self.current_level_matrix[x1][y1].get_dot_type()
        dot_type_2 = self.current_level_matrix[x2][y2].get_dot_type()
        horizontal_count = self.find_color_count(1, 4, x1, y1, color_type_1, 0) + \
                               self.find_color_count(-1, -4, x1, y1, color_type_1, 0, -1) + \
                               self.find_color_count(1, 4, x2, y2, color_type_2, 0) + \
                               self.find_color_count(-1, -4, x2, y2, color_type_2, 0, -1) + \
                               self.find_dot_count(1, 4, x1, y1, dot_type_1, 0) + \
                               self.find_dot_count(-1, -4, x1, y1, dot_type_1, 0, -1) + \
                               self.find_dot_count(1, 4, x2, y2, dot_type_2, 0) + \
                               self.find_dot_count(-1, -4, x2, y2, dot_type_2, 0, -1)

        vertical_count = self.find_color_count(1, 4, x1, y1, color_type_1, 1) + \
                             self.find_color_count(-1, -4, x1, y1, color_type_1, 1, -1) + \
                             self.find_color_count(1, 4, x2, y2, color_type_2, 1) + \
                             self.find_color_count(-1, -4, x2, y2, color_type_2, 1, -1) + \
                             self.find_dot_count(1, 4, x1, y1, dot_type_1, 1) + \
                             self.find_dot_count(-1, -4, x1, y1, dot_type_1, 1, -1) + \
                             self.find_dot_count(1, 4, x2, y2, dot_type_2, 1) + \
                             self.find_dot_count(-1, -4, x2, y2, dot_type_2, 1, -1)

        diagonal_right_count = self.find_color_count(1, 4, x1, y1, color_type_1, 2) + \
                                   self.find_color_count(-1, -4, x1, y1, color_type_1, 2, -1) + \
                                   self.find_color_count(1, 4, x2, y2, color_type_2, 2) + \
                                   self.find_color_count(-1, -4, x2, y2, color_type_2, 2, -1) + \
                                   self.find_dot_count(1, 4, x1, y1, dot_type_1, 2) + \
                                   self.find_dot_count(-1, -4, x1, y1, dot_type_1, 2, -1) + \
                                   self.find_dot_count(1, 4, x2, y2, dot_type_2, 2) + \
                                   self.find_dot_count(-1, -4, x2, y2, dot_type_2, 2, -1)

        diagonal_left_count = self.find_color_count(1, 4, x1, y1, color_type_1, 3) + \
                                  self.find_color_count(-1, -4, x1, y1, color_type_1, 3, -1) + \
                                  self.find_color_count(1, 4, x2, y2, color_type_2, 3) + \
                                  self.find_color_count(-1, -4, x2, y2, color_type_2, 3, -1) + \
                                  self.find_dot_count(1, 4, x1, y1, dot_type_1, 3) + \
                                  self.find_dot_count(-1, -4, x1, y1, dot_type_1, 3, -1) + \
                                  self.find_dot_count(1, 4, x2, y2, dot_type_2, 3) + \
                                  self.find_dot_count(-1, -4, x2, y2, dot_type_2, 3, -1)

        return horizontal_count + vertical_count + diagonal_right_count + diagonal_left_count

    def generate_init_position_moves(self, position_tuple):
        x1, y1 = position_tuple
        valid_moves = []
        if self.is_move_legal(x1, y1, x1, y1 + 1):
            valid_moves.append([(x1, y1), (x1, y1 + 1)])
        if self.is_move_legal(x1, y1, x1 + 1, y1):
            valid_moves.append([(x1, y1), (x1 + 1, y1)])
        return valid_moves

    def get_max_fillable_row(self):
        BLANK_STATE = np.empty(np.size(self.current_level_matrix, 1), dtype=object)
        for i in range(np.size(self.current_level_matrix, 0)):
            if np.array_equal(self.current_level_matrix[i], BLANK_STATE):
                return i + 1
        return -1

    def get_valid_empty_positions_in_row(self, row):
        empty = []
        for j in range(np.size(self.current_level_matrix, 1)):
            if self.current_level_matrix[row][j] is None and (
                    row == 0 or self.current_level_matrix[row - 1][j] is not None):
                empty.append((row, j))
        return empty

    def get_placeable_available_positions(self):
        rows, cols = np.where(self.current_level_matrix == None)
        rows = np.unique(rows)
        max_fillable_row = self.get_max_fillable_row()
        available_positions = []
        for i in range(12 if max_fillable_row is -1 else max_fillable_row):
            if i in rows:
                empty_row_elements = self.get_valid_empty_positions_in_row(i)
                available_positions = available_positions + empty_row_elements
        return available_positions

    def check_pick_position_condition(self, x1, y1, x_max):
        return self.current_level_matrix[x1][y1] is not None and \
               (x1 == x_max or self.current_level_matrix[x1 + 1][y1] is None)

    def get_pickable_available_cards(self):
        x_max = np.size(self.current_level_matrix, 0) - 1
        current_x = x_max
        chosen_cards = []
        while current_x >= 0:
            row_card_pick_possible = False
            empty_cell_found = False
            for j in range(np.size(self.current_level_matrix, 1)):
                if self.current_level_matrix[current_x][j] is None:
                    empty_cell_found = True
                else:
                    x2, y2 = self.cards[(current_x, j)]
                    if (x2, y2) not in chosen_cards and (current_x, j) not in chosen_cards \
                            and self.is_recycler_move_legal(min(current_x, x2), min(j, y2), max(current_x, x2),
                                                            max(j, y2)) is True:
                        row_card_pick_possible = True
                        chosen_cards.append((min(current_x, x2), min(j, y2)))
            if row_card_pick_possible is False and empty_cell_found is False:
                return chosen_cards
            current_x -= 1
        return chosen_cards

    def get_card(self, rotations, position):
        x1, y1 = position
        x2, y2 = self.cards[position]
        first_cell = self.get_cell_info(x1, y1)
        second_cell = self.get_cell_info(x2, y2)
        cells = [first_cell, second_cell]
        card = Card(rotations[get_orientation(cells) - 1], y1, x1)
        return card

    def get_cell_info(self, x, y):
        return self.current_level_matrix[x][y]

    def remove_card(self, first_cell, second_cell):
        x1, y1 = first_cell
        x2, y2 = second_cell
        self.current_level_matrix[x1][y1] = None
        self.current_level_matrix[x2][y2] = None
        del self.cards[(x1, y1)]
        del self.cards[(x2, y2)]

    def is_move_legal(self, x1, y1, x2, y2):
        if x1 < 0 or x2 >= 12 or y1 < 0 or y2 >= 8:
            return False
        if self.current_level_matrix[x1][y1] is not None or self.current_level_matrix[x2][y2] is not None:
            return False
        if x1 > 0 and (self.current_level_matrix[x1 - 1][y1] is None or (
                y1 != y2 and self.current_level_matrix[x1 - 1][y2] is None)):
            return False
        return True

    def is_recycler_move_legal(self, x1, y1, x2, y2):
        last_card_x1 = self.last_card_placed.get_first_cell().get_x_coordinate()
        last_card_y1 = self.last_card_placed.get_first_cell().get_y_coordinate()
        last_card_x2 = self.last_card_placed.get_second_cell().get_x_coordinate()
        last_card_y2 = self.last_card_placed.get_second_cell().get_y_coordinate()
        if self.cards.get((x1, y1)) == None or self.cards.get((x2, y2)) == None \
                or self.cards[(x1, y1)] != (x2, y2) or self.cards[(x2, y2)] != (x1, y1):
            return False
        if (x1 == x2 and (self.get_cell_info(x1 + 1, y1) != None or self.get_cell_info(x1 + 1, y2) != None)) \
                or (x2 < 11 and self.get_cell_info(x2 + 1, y1) != None):
            return False
        if last_card_x1 != x1 or last_card_y1 != y1 or last_card_x2 != x2 or last_card_y2 != y2:
            return True
        return False

    def check_win(self, x, y, symbol):
        patterns = ["BLACK_DOT BLACK_DOT BLACK_DOT BLACK_DOT",
                    "WHITE_DOT WHITE_DOT WHITE_DOT WHITE_DOT",
                    "RED_COLOR RED_COLOR RED_COLOR RED_COLOR",
                    "WHITE_COLOR WHITE_COLOR WHITE_COLOR WHITE_COLOR"]
        current_row = self.current_level_matrix[:, y]
        current_column = self.current_level_matrix[x, :]
        diagonal1 = np.diagonal(self.current_level_matrix, y - x)
        diagonal2 = np.diagonal(np.fliplr(self.current_level_matrix), np.size(self.current_level_matrix, 1) - 1 - y - x)

        if symbol == 'DOTS' and (patterns[0] in get_data_string(current_row, symbol) or
                                 patterns[1] in get_data_string(current_row, symbol) or
                                 patterns[0] in get_data_string(current_column, symbol) or
                                 patterns[1] in get_data_string(current_column, symbol) or
                                 patterns[0] in get_data_string(diagonal1, symbol) or
                                 patterns[1] in get_data_string(diagonal1, symbol) or
                                 patterns[0] in get_data_string(diagonal2, symbol) or
                                 patterns[1] in get_data_string(diagonal2, symbol)):
            return True
        elif symbol == 'COLOR' and (patterns[2] in get_data_string(current_row, symbol) or
                                    patterns[3] in get_data_string(current_row, symbol) or
                                    patterns[2] in get_data_string(current_column, symbol) or
                                    patterns[3] in get_data_string(current_column, symbol) or
                                    patterns[2] in get_data_string(diagonal1, symbol) or
                                    patterns[3] in get_data_string(diagonal1, symbol) or
                                    patterns[2] in get_data_string(diagonal2, symbol) or
                                    patterns[3] in get_data_string(diagonal2, symbol)):
            return True
        else:
            return False


def get_data_string(direction, symbol):
    if symbol == "COLOR":
        return ' '.join(["None" if cell is None else cell.get_color_type() for cell in direction])
    else:
        return ' '.join(["None" if cell is None else cell.get_dot_type() for cell in direction])