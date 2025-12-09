class Piece:
    def __init__(self, colour, type):
        self.colour = colour
        self.type = type
        self.moved = False

    def __repr__(self):
        return f"{self.colour}{self.type}"