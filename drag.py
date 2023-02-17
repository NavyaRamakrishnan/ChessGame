
import pygame

from constant import *

class Drag:

    # initializing a drag object that keeps track of the click and drag positions by the user
    def __init__(self):
        self.x = 0
        self.y = 0
        self.piece = None
        self.start_row = 0
        self.start_column = 0
        self.dragcheck = False

    # mouse - position represents a tuple of (x_coord, y_coord)
    def update_position(self, position):
        self.x, self.y = position

    # keeping track of where the mouse initially starts off
    def start_position(self, position):
        self.start_row =  position[1] // SQUARE_SIZE
        self.start_column = position[0] // SQUARE_SIZE

    # drag is set to true and piece is determined when dragging
    def drag(self, piece):
        self.piece = piece
        self.dragcheck = True

    # when piece is released, no longer being dragged
    def no_drag(self):
        self.piece = None
        self.dragcheck = False

    # making the piece follow the mouse when being dragged, constantly updating the screen
    def update_screen(self, screen):
        image = pygame.image.load(self.piece.image)
        image_center = self.x, self.y
        self.piece.image_rect = image.get_rect(center=image_center)
        screen.blit(image, self.piece.image_rect)