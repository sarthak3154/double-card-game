from Board import Board

class Card(object):

    '''Sample class for initial commit'''

    DOT = ['BLACK','WHITE']

    COLOR = ['RED','WHITE']

    DIRECTION = ['HORIZONTAL' , 'VERTICAL']

    ROTATIONS = [[DIRECTION[0],DOT[0],COLOR[0],DOT[1],COLOR[1]],
                 [DIRECTION[1],DOT[0],COLOR[0],DOT[1],COLOR[1]],
                 [DIRECTION[0],DOT[1],COLOR[1],DOT[0],COLOR[0]],
                 [DIRECTION[1],DOT[1],COLOR[1],DOT[0],COLOR[0]],
                 [DIRECTION[0],DOT[1],COLOR[0],DOT[0],COLOR[1]],
                 [DIRECTION[1],DOT[1],COLOR[0],DOT[0],COLOR[1]],
                 [DIRECTION[0],DOT[0],COLOR[1],DOT[1],COLOR[0]],
                 [DIRECTION[1],DOT[0],COLOR[1],DOT[1],COLOR[0]]]

    # board = Board()
    # board.place_card(ROTATIONS[0], 0, 1)
    # c = board.get_cell_info(0,1)
    # print(c.get_dot_type())
    # print(board.matrix_data)
