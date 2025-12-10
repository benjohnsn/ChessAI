import pygame
from constants import SIZE, CAPTION, DIMENSION, SQ_SIZE, LIGHT_COL, DARK_COL, SELECTION_HIGHLIGHT_COL, TARGET_HIGHLIGHT_COL

class Gui:
    """
    User interface for the chess game
    - Creates and manages pygame display
    - Loads and stores piece images
    - Draws chessboard and pieces
    - Highlights selected square and target squares
    """
    def __init__(self):
        # Initialises screen, loads piece images and board colours
        self.screen = pygame.display.set_mode(SIZE)
        pygame.display.set_caption(CAPTION)
        self.colours = [pygame.Color(LIGHT_COL), pygame.Color(DARK_COL), pygame.Color(SELECTION_HIGHLIGHT_COL), pygame.Color(TARGET_HIGHLIGHT_COL)]
        self.images = {}
        self.loadImages()


    def loadImages(self):
        # Loads piece images from folder and scales them to square size
        pieces = ['wP', 'wR', 'wN', 'wB', 'wQ', 'wK', 'bP', 'bR', 'bN', 'bB', 'bQ', 'bK']
        for piece in pieces:
            self.images[piece] = pygame.transform.scale(pygame.image.load("images/" + piece  + ".png"), (SQ_SIZE, SQ_SIZE))
    
    
    def draw(self, board, highlightSq, targetSqs):
        # Draws chess board
        for row in range(DIMENSION):
            for col in range(DIMENSION):
                rect = pygame.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
                colour = self.colours[(row + col) % 2]

                # Higlights Square
                if (row, col) == highlightSq:
                    colour = self.colours[2]
                
                # Highlights Target squares
                if (row, col) in targetSqs:
                    colour = self.colours[3]

                pygame.draw.rect(self.screen, colour, rect)

                # Draws Pieces onto correct square
                piece = board.grid[row][col]
                if piece is not None:
                    self.screen.blit(self.images[piece.colour + piece.type], rect)
