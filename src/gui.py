import pygame
import board
from constants import HEIGHT, WIDTH, DIMENSION, SQ_SIZE, COL1, COL2

class Gui:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Chess")
        self.images = {}
        self.loadimages()

    def loadimages(self):
        pieces = ['wP', 'wR', 'wN', 'wB', 'wQ', 'wK', 'bP', 'bR', 'bN', 'bB', 'bQ', 'bK']
        for piece in pieces:
            self.images[piece] = pygame.image.load("images/" + piece  + ".png"), (SQ_SIZE, SQ_SIZE)
    
    def draw(self):
        self.screen.fill(COL1)
        self.colours = [pygame.Color(COL1), pygame.Color(COL2)]
        for self.row in range(DIMENSION):
            for self.col in range(DIMENSION):
                pygame.draw.rect(self.screen, self.colours[((self.row + self.col) % 2)], pygame.Rect(self.col * SQ_SIZE, self.row * SQ_SIZE, SQ_SIZE, SQ_SIZE))

