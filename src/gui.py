import pygame
from constants import SIZE, CAPTION, DIMENSION, SQ_SIZE, COL1, COL2, HIGHLIGHTCOL

class Gui:
    # User interface for the chess game
    # - Creates and manages pygame display
    # - loads and store piece images
    # - Draws chessboard and pieces

    def __init__(self):
        # Initialises screen and loads piece images
        self.screen = pygame.display.set_mode(SIZE)
        pygame.display.set_caption(CAPTION)
        self.images = {}
        self.loadimages()

    def loadimages(self):
        # Loads piece images from images folder and scales them to square size
        pieces = ['wP', 'wR', 'wN', 'wB', 'wQ', 'wK', 'bP', 'bR', 'bN', 'bB', 'bQ', 'bK']
        for piece in pieces:
            self.images[piece] = pygame.transform.scale(pygame.image.load("images/" + piece  + ".png"), (SQ_SIZE, SQ_SIZE))
    
    def draw(self, board, highlightSq):
        # Draws chess board and pieces onto the screen
        colours = [pygame.Color(COL1), pygame.Color(COL2)]
        for row in range(DIMENSION):
            for col in range(DIMENSION):
                rect = pygame.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
                colour = colours[(row + col) % 2]

                if highlightSq == (row, col):
                    colour = pygame.Color(HIGHLIGHTCOL)

                pygame.draw.rect(self.screen, colour, rect)
                piece = board.grid[row][col]
                if piece != None:
                    self.screen.blit(self.images[piece.colour + piece.type], rect)
       
        # Draw highlighted square
        # if highlightSq:
        #     row, col = highlightSq
        #     hrect = pygame.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        #     overlay = pygame.Surface((SQ_SIZE, SQ_SIZE), pygame.SRCALPHA)
        #     overlay.fill((255, 255, 0, 120))

        #     self.screen.blit(overlay, hrect)
