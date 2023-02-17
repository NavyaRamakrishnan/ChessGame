# videos and articles consumed to learn about pygame and chess designs
# https://www.youtube.com/watch?v=EnYui0e73Rs&list=PLBwF487qi8MGU81nDGaeNE1EnNEPYWKY_&index=1
# https://www.geeksforgeeks.org/design-a-chess-game/
# https://levelup.gitconnected.com/chess-python-ca4532c7f5a4
# https://www.youtube.com/watch?v=OpL0Gcfn4B4&t=1704s
# https://medium.com/codex/how-to-code-a-simple-chess-game-in-python-9a9cb584f57
# https://realpython.com/pygame-a-primer/

import pygame
import sys

from constant import *
from game import Game
from square import Square
from movetracker import MoveTracker

class Main:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
        pygame.display.set_caption("Chess")
        self.game = Game()

    def loop(self):

        screen = self.screen
        game = self.game
        drag = self.game.drag
        board = self.game.board

        while True:
            game.background(screen)
            game.show_moves(screen)
            game.show_pieces(screen)

            if drag.dragcheck:
                drag.update_screen(screen)

            for event in pygame.event.get():

                # event of clicking on the piece
                if event.type == pygame.MOUSEBUTTONDOWN:
                    drag.update_position(event.pos)
                    print(event.pos)

                    row_click = drag.y // SQUARE_SIZE # figures out which row you are clicking on 
                    column_click = drag.x // SQUARE_SIZE # figures out which column you are clicking on

                    print(drag.y, row_click) 
                    print(drag.x, column_click)

                    if board.squares[row_click][column_click].has_piece():
                        piece = board.squares[row_click][column_click].piece
                        # must check if color is valid too (next turn)
                        if piece.color == game.next_turn:
                            board.possible_moves(piece, row_click, column_click,)
                            drag.start_position(event.pos)
                            drag.drag(piece)
                            game.background(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen)

                # moving around mouse
                elif event.type == pygame.MOUSEMOTION:
                    if drag.dragcheck:
                        drag.update_position(event.pos)
                        game.background(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)
                        drag.update_screen(screen)

                # releasing mouse click
                elif event.type == pygame.MOUSEBUTTONUP:

                    if drag.dragcheck:
                        drag.update_position(event.pos)

                        row_final = drag.y // SQUARE_SIZE
                        column_final = drag.x // SQUARE_SIZE

                        start = Square(drag.start_row, drag.start_column)
                        end = Square(row_final, column_final)
                        move = MoveTracker(start, end)

                        if board.valid_move(drag.piece, move):
                            board.move(drag.piece, move)
                            game.background(screen)
                            game.show_pieces(screen)

                            # hand turn to next player
                            game.next_player()


                    drag.no_drag()

                # resetting game if space key is pressed
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        game.reset()
                        game = self.game
                        board = self.game.board
                        drag = self.game.drag

                # usual code added in for pygame applications
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()

main = Main()
main.loop()
