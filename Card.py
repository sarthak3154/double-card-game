class Card:

    '''Sample class for initial commit'''

    ROTATION_NUMBERS = list(range(1,8))

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



