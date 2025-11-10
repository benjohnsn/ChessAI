import pygame
from board import Board
from gui import Gui
from constants import FPS, SQ_SIZE
class Game:
    # Main class
    # - Tracks game state
    # - Handles player inputs
    # - Executes moves on board and updates turn
    # - Draws board through Gui

    def __init__(self):
        # Initialises libraries and objects
        pygame.init()
        self.running = True
        self.clock = pygame.time.Clock()
        self.gui = Gui()
        self.board = Board()
        self.turn = 'w'
        self.playerClicks = []
        self.sqSelected = ()

    def run(self):
        # Main game loop: handles events, updates Gui and ticks clock
        while self.running:
            self.handleEvents()
            self.gui.draw(self.board, self.sqSelected)
            pygame.display.flip()
            self.clock.tick(FPS)

    def handleEvents(self):
        # Handles pygame events (quit, mouse click)
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handleClick(pygame.mouse.get_pos())

    def handleClick(self, pos):
        # Handles a player click on the board
        square = self.getSquareFromPos(pos)
        piece = self.board.getPiece(square)
        
        # Select your own piece (allows reselection)
        if piece is not None and piece.colour == self.turn:
            self.playerClicks = [square]
            self.sqSelected = square
            return
        
        # If piece already  selected, add target square, if it does not contain player piece
        if self.playerClicks:
            self.playerClicks.append(square)
        else:
            return
        
        # Check if move is legal and make piece
        if self.board.isLegalMove(self.playerClicks[0], self.playerClicks[1], self.turn):
            self.board.movePiece(self.playerClicks[0], self.playerClicks[1], self.turn)
            self.switchTurn()

        self.playerClicks = []
        self.sqSelected = ()

    def getSquareFromPos(self, pos):
        # Converts mouse position to board coordinates
        col = pos[0] // SQ_SIZE
        row = pos[1] // SQ_SIZE
        return (row, col)

    def switchTurn(self):
        if self.turn == 'w':
            self.turn = 'b'
        else:
             self.turn = 'w'
