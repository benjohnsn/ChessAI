import pygame
from constants import SIZE, CAPTION, DIMENSION, SQ_SIZE, LIGHT_COL, DARK_COL, HIGHLIGHT_COL

class Gui:
    """User interface for the chess game
    - Creates and manages pygame display
    - Loads and store piece images
    - Draws chessboard and pieces
    """
    def __init__(self):
        # Initialises screen, loads piece images and board colours
        self.screen = pygame.display.set_mode(SIZE)
        pygame.display.set_caption(CAPTION)
        self.images = {}
        self.loadImages()
        self.colours = [pygame.Color(LIGHT_COL), pygame.Color(DARK_COL)]

    def loadImages(self):
        # Loads piece images from images folder and scales them to square size
        pieces = ['wP', 'wR', 'wN', 'wB', 'wQ', 'wK', 'bP', 'bR', 'bN', 'bB', 'bQ', 'bK']
        for piece in pieces:
            self.images[piece] = pygame.transform.scale(pygame.image.load("images/" + piece  + ".png"), (SQ_SIZE, SQ_SIZE))
    
    def draw(self, board, highlightSq):
        # Draws chess board
        for row in range(DIMENSION):
            for col in range(DIMENSION):
                displayRow = 7 - row
                rect = pygame.Rect(col * SQ_SIZE, displayRow * SQ_SIZE, SQ_SIZE, SQ_SIZE)
                colour = self.colours[(row + col) % 2]

                # Higlight Square
                if highlightSq == (row, col):
                    colour = pygame.Color(HIGHLIGHT_COL)
                pygame.draw.rect(self.screen, colour, rect)

                # Draws Pieces onto correct square
                piece = board.grid[row][col]
                if piece is not None:
                    self.screen.blit(self.images[piece.colour + piece.type], rect)
