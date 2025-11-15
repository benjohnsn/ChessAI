import pygame
from board import Board
from gui import Gui
from constants import FPS, SQ_SIZE
class Game:
    # Main class
    # - Tracks game state
    # - Handles player inputs
    # - Executes moves using board and updates turn
    # - Draws board through Gui

    def __init__(self):
        # Initialises libraries and objects
        pygame.init()
        self.running = True
        self.clock = pygame.time.Clock()
        self.gui = Gui()
        self.board = Board()
        self.turn = 'w'
        self.pieceSq = ()
        self.targetSq = ()

    def run(self):
        # Main game loop: handles events, updates Gui and ticks clock
        while self.running:
            self.handleEvents()
            self.gui.draw(self.board)
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

        if not self.pieceSq:
            if piece is None:
                return
            if piece.colour != self.turn:
                return
            
            self.pieceSq = square
            return
            
        self.targetSq = square
        self.board.makeMove(self.pieceSq, self.targetSq)
        self.switchTurn()

    def getSquareFromPos(self, pos):
        # Converts mouse position to board coordinates
        col = pos[0] // SQ_SIZE
        row = pos[1] // SQ_SIZE
        return (row, col)

    def switchTurn(self):
        # Switches turns
        if self.turn == 'w':
            self.turn = 'b'
        else:
             self.turn = 'w'
