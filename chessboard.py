from constant import *
from square import Square
from piece import *
from movetracker import MoveTracker
import copy
import os

class Chessboard:

    # initiating a chessboard object
    def __init__(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for c in range(COLUMNS)]
        self.last_play = None
        self._create()
        self._add_pieces('white')
        self._add_pieces('black')

    # creating the squares on the chessboard (8 by 8)
    def _create(self):
        for r in range(ROWS):
            for c in range(COLUMNS):
                self.squares[r][c] = Square(r, c)
                
    def move(self, piece, move):
        # keeping track of beginning and end moves
        start = move.start
        end = move.end
        self.squares[start.r][start.c].piece = None
        self.squares[end.r][end.c].piece = piece

        # cool pawn promotion
        if isinstance(piece, Pawn):
            if end.r == 0 or end.r == 7:
                self.squares[end.r][end.c].piece = Queen(piece.color)

        # castling - left and right
        if isinstance(piece, King):
            if self.castling_check(start, end):
                # taking the proper rook (left or right depending on whether it is queen or king castling)
                if (end.c - start.c < 0):
                    rook = piece.rook1
                else:
                    rook = piece.rook2

                # recursion by moving the rook on the last move added to moves (in the king possible moves)
                self.move(rook, rook.moves[-1]) 


        piece.moved = True

        piece.clear_moves()

        self.last_play = move

    # returning moves that are valid for the piece
    def valid_move(self, piece, move):
        return move in piece.moves

    # checking if castling is possible 
    def castling_check(self, start, end):
        return abs(start.c - end.c) == 2

    def game_check(self, piece, move):
        # creating a copy of board to see whether moving a piece would lead to a check
        piece_copy = copy.deepcopy(piece)
        board_copy = copy.deepcopy(self)
        board_copy.move(piece_copy, move)

        for r in range(ROWS):
            for c in range(COLUMNS):
                # checking through all squares that have opposing team pieces
                if board_copy.squares[r][c].has_opp_piece(piece.color):
                    current_piece = board_copy.squares[r][c].piece
                    board_copy.possible_moves(current_piece, r, c, bool=False)
                    for move in current_piece.moves:
                        # if it is possible that a piece can attack a king - means player is in check!
                        if isinstance(move.end.piece, King):
                            return True
                
        return False

    def _add_pieces(self, color):
        # add pieces in corresponding rows depending on team color
        if color == 'white':
            pawns_row = 6
            not_pawns_row = 7
        else:
            pawns_row = 1
            not_pawns_row = 0

        # places all the pawns on the board 
        for c in range(COLUMNS):
            self.squares[pawns_row][c] = Square(pawns_row, c, Pawn(color))

        # knights on the board
        self.squares[not_pawns_row][1] = Square(not_pawns_row, 1, Knight(color))
        self.squares[not_pawns_row][6] = Square(not_pawns_row, 6, Knight(color))

        # bishops on the board
        self.squares[not_pawns_row][2] = Square(not_pawns_row, 2, Bishop(color))
        self.squares[not_pawns_row][5] = Square(not_pawns_row, 5, Bishop(color))

        # rooks on the board
        self.squares[not_pawns_row][0] = Square(not_pawns_row, 0, Rook(color))
        self.squares[not_pawns_row][7] = Square(not_pawns_row, 7, Rook(color))


        # queen on the board
        self.squares[not_pawns_row][3] = Square(not_pawns_row, 3, Queen(color))

        # king on the board
        self.squares[not_pawns_row][4] = Square(not_pawns_row, 4, King(color))
    

    def possible_moves(self, piece, r, c, bool=True):
        
        # common function that covers the possible straight moves for pieces such as rooks, bishops, and queens
        def straight_moves(steps):
            # thinking of steps as possible moves (diagonals, edges, etc)
            for s in steps:
                row_step, column_step = s
                possible_r = r + row_step
                possible_c = c + column_step

                while True:
                    if Square.in_board(possible_r, possible_c):
                        # keeping track of possible moves and making squares accordingly
                        start = Square(r, c)
                        end_piece = self.squares[possible_r][possible_c].piece
                        end = Square(possible_r, possible_c, end_piece)

                        #creating the corresponding move
                        move = MoveTracker(start, end)
                        # if square is empty 
                        if self.squares[possible_r][possible_c].empty_check():
                            # looking for checks
                            if bool:
                               if not self.game_check(piece, move):
                                   piece.add_moves(move)
                            else:
                               piece.add_moves(move)


                        # if square has own color piece
                        elif self.squares[possible_r][possible_c].has_own_piece(piece.color):
                            break

                        # if square has opposite side piece -> then add move and then break loop (can't move past opp piece)
                        elif self.squares[possible_r][possible_c].has_opp_piece(piece.color):
                            # looking for game checks
                            if bool:
                               if not self.game_check(piece, move):
                                   piece.add_moves(move)
                            else:
                               piece.add_moves(move)

                            break

                        possible_r = possible_r + row_step
                        possible_c = possible_c + column_step
                    
                    else:
                        break


        if isinstance(piece, Pawn):
            if piece.moved:
                steps = 1
            else:
                steps = 2

            initial = r + piece.direction
            final = r + (piece.direction * (1 + steps))
            for move in range(initial, final, piece.direction):
                if Square.in_board(move):
                    if self.squares[move][c].empty_check():
                        # must make a new start and end move squares
                        # creating a new move!
                        start = Square(r, c)
                        end = Square(move, c)
                        move = MoveTracker(start, end)

                        # see if there are any potential checks - because if so, then should not be able to move
                        if bool:
                           if not self.game_check(piece, move):
                               piece.add_moves(move)
                        else:
                           piece.add_moves(move)

                    else: 
                        break
                else:
                    break

            # diagonal possible moves 
            # should be able to move diagonally if opposite color piece is in its diagonal
            move_row = r + piece.direction
            move_columns = [c-1, c+1]
            for col in move_columns:
                if Square.in_board(move_row, col):
                    if self.squares[move_row][col].has_opp_piece(piece.color):
                        start = Square(r, c)
                        end_piece = self.squares[move_row][col].piece
                        end = Square(move_row, col, end_piece)
                        move = MoveTracker(start, end)
                        
                        if bool:
                           if not self.game_check(piece, move):
                               piece.add_moves(move)
                        else:
                           piece.add_moves(move)



        elif isinstance(piece, Knight):
            # possible movements for a Knight (always L-shaped)
            moves = [(r-2, c-1), (r-2, c+1), (r-1, c-2), (r-1, c+2), (r+2, c+1), (r+2, c-1), (r+1, c+2), (r+1, c-2)]

            for m in moves:
                possible_r, possible_c = m

                if Square.in_board(possible_r, possible_c):
                    if self.squares[possible_r][possible_c].empty_or_opp(piece.color):
                        start = Square(r, c)
                        end_piece = self.squares[possible_r][possible_c].piece
                        end = Square(possible_r, possible_c, end_piece)

                        move = MoveTracker(start, end)

                        if bool:
                           if not self.game_check(piece, move):
                               piece.add_moves(move)
                           else: break
                        else:
                           piece.add_moves(move)


        elif isinstance(piece, Bishop):
            # possible moves for a bishop - all diagonals
            straight_moves([(1,1), (1,-1), (-1, 1), (-1,-1)]) #all diagonals

        elif isinstance(piece, Rook):
            # possible moves for a rook - all edges
            straight_moves([(1,0), (-1,0), (0,1), (0,-1)]) #all edges moves

        elif isinstance(piece, Queen):
            # possible moves for a queen - diagonals and edges
            straight_moves([(1,1), (1,-1), (-1, 1), (-1,-1), (1,0), (-1,0), (0,1), (0,-1)]) # combo of bishop and rook
        
        elif isinstance(piece, King):
            # possible moves for a king - move one in all directions (diagonals and edges)
            moves = [(r-1, c-1), (r-1, c+1), (r-1, c), (r+1, c-1), (r+1, c+1), (r+1, c), (r, c-1), (r, c+1)]

            for m in moves:
                possible_r, possible_c = m

                if Square.in_board(possible_r, possible_c):
                    if self.squares[possible_r][possible_c].empty_or_opp(piece.color):
                        start = Square(r, c)
                        end = Square(possible_r, possible_c)

                        move = MoveTracker(start, end)
                        piece.add_moves(move)

            # castling - only can castle if no pieces in between rook and king
            if not piece.moved:
                rook1 = self.squares[r][0].piece
                if isinstance(rook1, Rook):
                    if not rook1.moved:
                        for i in range(1,4):
                            if self.squares[r][i].has_piece():
                                break

                            if i == 3:
                                piece.rook1 = rook1

                                # moving rook to castling position
                                start = Square(r, 0)
                                end = Square(r, 3)
                                move_rook = MoveTracker(start, end)
                                rook1.add_moves(move_rook)

                                # moving king to castling position
                                start = Square(r, c)
                                end = Square(r, 2)
                                move_king = MoveTracker(start, end)
                                piece.add_moves(move_king)


                rook2 = self.squares[r][7].piece
                if isinstance(rook2, Rook):
                    if not rook2.moved:
                        for i in range(5,7): # checking if any pieces in between the rook and king
                            if self.squares[r][i].has_piece():
                                break

                            if i == 6:
                                piece.rook2 = rook2

                                # moving rook to castling position
                                start = Square(r, 7)
                                end = Square(r, 5)
                                move_rook = MoveTracker(start, end)
                                rook2.add_moves(move_rook)

                                # moving king to castling position
                                start = Square(r, c)
                                end = Square(r, 6)
                                move_king = MoveTracker(start, end)
                                piece.add_moves(move_king)





