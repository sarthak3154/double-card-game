
class State:

    def __init__(self, current_level_state, new_card):
        self.current_level_matrix = current_level_state.matrix_data.copy()
        self.white_circle_coordinates = current_level_state.white_circle
        self.red_circle_coordinates = current_level_state.red_circle
        self.white_dot_coordinates = current_level_state.white_dot
        self.red_dot_coordinates = current_level_state.red_dot
        self.card = new_card
        self.place_new_card(new_card)

    def place_new_card(self, card):
        x1 = card.get_first_cell().get_x_coordinate()
        y1 = card.get_first_cell().get_y_coordinate()
        x2 = card.get_second_cell().get_x_coordinate()
        y2 = card.get_second_cell().get_y_coordinate()
        move_state = self.is_move_legal(x1, y1, x2, y2)
        if move_state:
            self.current_level_matrix[x1][y1] = card.get_first_cell()
            self.current_level_matrix[x2][y2] = card.get_second_cell()
            self.add_coordinates_to_specific_list(card.get_first_cell(), (x1, y1))
            self.add_coordinates_to_specific_list(card.get_second_cell(), (x2, y2))
            return True
        else:
            return False

    def add_coordinates_to_specific_list(self,cell,coordinates):
        if cell.get_color_type() == 'WHITE_COLOR' and cell.get_dot_type() == 'WHITE_DOT':
            self.white_circle_coordinates.append(coordinates)
        if cell.get_color_type() == 'WHITE_COLOR' and cell.get_dot_type() == 'BLACK_DOT':
            self.white_dot_coordinates.append(coordinates)
        if cell.get_color_type() == 'RED_COLOR' and cell.get_dot_type() == 'WHITE_DOT':
            self.red_circle_coordinates.append(coordinates)
        if cell.get_color_type() == 'RED_COLOR' and cell.get_dot_type() == 'BLACK_DOT':
            self.red_dot_coordinates.append(coordinates)

    def get_heuristic_value(self):

        for (x,y) in self.white_circle_coordinates:
            print(x + "" + (y+1))
            white_circle_value = white_circle_value + int(x + "" + (y+1))

        for (x,y) in self.white_dot_coordinates:
            print(x + "" + (y + 1))
            white_dot_value = white_dot_value + int(x + "" + (y+1))

        for (x,y) in self.red_circle_coordinates:
            print(x + "" + (y + 1))
            red_circle_value = red_circle_value + int(x + "" + (y+1))

        for (x,y) in self.red_dot_coordinates:
            print(x + "" + (y + 1))
            red_dot_value = red_dot_value + int(x + "" + (y+1))

        return round(white_circle_value + (3*white_dot_value) - (2*red_dot_value) - (1.5*red_circle_value) , 2)

    def is_move_legal(self, x1, y1, x2, y2):
        if x1 < 0 or x2 >= 12 or y1 < 0 or y2 >= 8:
            return False
        if self.current_level_matrix[x1][y1] is not None or self.current_level_matrix[x2][y2] is not None:
            return False
        if x1 > 0 and (self.current_level_matrix[x1-1][y1] is None or (y1 != y2 and self.current_level_matrix[x1-1][y2] is None)):
            return False
        return True
