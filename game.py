import pygame

from constant import *
from chessboard import Chessboard
from drag import Drag

class Game:

    def __init__(self):
        self.board = Chessboard()
        self.drag = Drag()
        self.next_turn = 'white'

    # alternating brown and white pieces on the chessboard
    def background(self, screen):
        for r in range(ROWS):
            for c in range(COLUMNS):
                if (r + c) % 2 == 0:
                    color = 'white' 
                else:
                    color = (181, 101, 29) 

                rect = (c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)

                pygame.draw.rect(screen, color, rect)

    # loading all the icon pictures onto the chessboard
    def show_pieces(self, screen):
        for r in range(ROWS):
            for c in range(COLUMNS):
                if self.board.squares[r][c].has_piece():
                    piece = self.board.squares[r][c].piece

                    if piece is not self.drag.piece:
                        img = pygame.image.load(piece.image)
                        img_center = c * SQUARE_SIZE + SQUARE_SIZE // 2, r * SQUARE_SIZE + SQUARE_SIZE // 2
                        piece.image_rect = img.get_rect(center=img_center)
                        screen.blit(img, piece.image_rect)

    # highlighting the possible moves for a specific piece when clicked and dragged
    def show_moves(self, screen):
        if self.drag.dragcheck:
            piece = self.drag.piece

            for m in piece.moves:
                if (m.end.r + m.end.c) % 2 == 0:
                    color = '#FF6865'
                else:
                    color = '#FF3632'
                #drawing the rectangle with the corresponding color
                rect = (m.end.c * SQUARE_SIZE, m.end.r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)

                pygame.draw.rect(screen, color, rect)

    # requiring alternating turns in the chess game
    def next_player(self):
        if self.next_turn == 'black':
            self.next_turn = 'white'
        else:
            self.next_turn = 'black'

    # resetting the game completely
    def reset(self):
        self.__init__()
