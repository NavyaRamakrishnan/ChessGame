import os

class Piece:

    # initializing a piece object
    def __init__(self, name, color, image=None, image_rect=None):
        self.name = name
        self.color = color
        self.image = image
        self.set_image()
        self.image_rect = image_rect
        self.moves = []
        self.moved = False

    # images/icons downloaded from online source
    def set_image(self, size=80):
        self.image = os.path.join(
            f'../icons/images/imgs-{size}px/{self.color}_{self.name}.png')

    # adding a move into the moves list for a piece
    def add_moves(self, move):
        self.moves.append(move)

    # clear all the moves for a piece
    def clear_moves(self):
        self.moves = []

class Pawn(Piece):

    # initializing a pawn subclass (direction depends on color of pawn)
    def __init__(self, color):
        if color == 'white':
            self.direction = -1
        else:
            self.direction = 1
        super().__init__('pawn', color)

class Knight(Piece):
    # initializing a knight subclass
    def __init__(self, color):
        super().__init__('knight', color)

class Bishop(Piece):
    # initializing a bishop subclass
    def __init__(self, color):
        super().__init__('bishop', color)

class Rook(Piece):
    # initializing a rook subclass
    def __init__(self, color):
        super().__init__('rook', color)

class Queen(Piece):
    # initializing a queen subclass
    def __init__(self, color):
        super().__init__('queen', color)

class King(Piece):
    # initializing a king subclass with two rook attributes (added in for castling)
    def __init__(self, color):
        self.rook1 = None
        self.rook2 = None
        super().__init__('king', color)
