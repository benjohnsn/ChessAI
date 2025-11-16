import pygame
from board import Board
from gui import Gui
from constants import FPS, SQ_SIZE
class Game:
    """Main class
    - Tracks game state
    - Handles player inputs
    - Executes moves using board and updates turn
    - Draws board through Gui
    """
    def __init__(self):
        # Initialises pygame and objects
        pygame.init()
        self.running = True
        self.clock = pygame.time.Clock()
        self.gui = Gui()
        self.board = Board()
        self.turn = 'w'
        self.pieceSq = ()
        self.targetSq = ()
        self.legalMoves = []

    def run(self):
        # Main game loop: handles events, updates Gui and ticks clock
        while self.running:
            self.handleEvents()
            self.gui.draw(self.board, self.pieceSq, self.legalMoves)
            pygame.display.flip()
            self.clock.tick(FPS)

    def handleEvents(self):
        # Handles pygame events: quit, mouse click
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handleClick(pygame.mouse.get_pos())

    def handleClick(self, pos):
        # Handles player click
        square = self.getSquareFromPos(pos)
        piece = self.board.getPiece(square)

        # 1st click
        # - Must be a piece of the current player's colour (allows re-selection)
        # - Checks if piece is not None (None has no .colour attribute)
        if piece and piece.colour == self.turn:
            self.pieceSq = square
            self.legalMoves = self.board.generateLegalMoves(piece, square)
            return
        
        # 2nd click
        # - If no valid first click, return
        if not self.pieceSq:
            return
        
        # - Assign 2nd click because it must be empty/opponent square
        self.targetSq = square
        
        if self.targetSq in self.legalMoves:
            self.board.makeMove(self.pieceSq, self.targetSq)
            self.switchTurn()

            # Reset selected squares
            self.pieceSq = ()
            self.targetSq = ()
            self.legalMoves = []

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
