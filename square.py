class Square:
    
    # initializing a square within the chessboard with corresponding row, column, and piece (default is none)
    def __init__(self, r, c, piece=None):
        self.r = r
        self.c = c
        self.piece = piece

    # checking whether the square has a piece
    def has_piece(self):
        return self.piece != None

    # checking whether the square is empty
    def empty_check(self):
        return not self.has_piece()

    # checking whether a square has the specific player's color (own team)
    def has_own_piece(self, color):
        return self.has_piece() and self.piece.color == color

    # checking whether a square has the opposite player's color (opposing team)
    def has_opp_piece(self, color):
        return self.has_piece() and self.piece.color != color

    # checking whether the square is either empty or has opposing team's piece
    def empty_or_opp(self, color):
        return self.empty_check() or self.has_opp_piece(color)

    # equals function made in order to compare two square objects
    def __eq__(self, other):
        return self.r == other.r and self.c == other.c

    # checking if coordinates are within the board
    @staticmethod
    def in_board(*positions):
        for p in positions:
            if p < 0 or p > 7:
                return False

        return True
