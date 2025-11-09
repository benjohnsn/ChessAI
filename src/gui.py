import pygame
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
    
    def draw(self, board):
        self.colours = [pygame.Color(COL1), pygame.Color(COL2)]
        for row in range(DIMENSION):
            for col in range(DIMENSION):
                rect = pygame.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
                pygame.draw.rect(self.screen, self.colours[(row + col) % 2], rect)
                piece = board.grid[row][col]
                if piece != None:
                    rect = pygame.Rect(col *SQ_SIZE, row *SQ_SIZE, SQ_SIZE, SQ_SIZE)
                    self.screen(self.images[piece], rect)