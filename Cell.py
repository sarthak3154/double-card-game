class Cell:

    def __init__(self,dot,color,x,y):
        self.dot = dot
        self.color = color
        self.x = x
        self.y = y

    def get_dot_type(self):
        return self.dot

    def get_color_type(self):
        return self.color

    def set_dot_type(self,dot):
        self.dot = dot

    def set_color_type(self,color):
        self.color = color
