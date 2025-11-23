import pygame
from gui import Gui
from board import Board
from constants import FPS, SQ_SIZE
class Game:
    """
    Main class
    - Tracks game state
    - Handles player inputs
    - Draws board through Gui
    - Executes moves using board and updates turn
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
        self.targetSqs = []


    def run(self):
        # Main game loop: handles events, updates Gui and ticks clock
        while self.running:
            self.handleEvents()
            self.gui.draw(self.board, self.pieceSq, self.targetSqs)
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
            self.targetSqs = [move.endSq for move in self.legalMoves]
            return
        
        # 2nd click
        # - If no valid first click, return
        if not self.pieceSq:
            return
        
        # - Assign 2nd click because it must be empty/opponent square
        self.targetSq = square
        
        # - If click is in the list of legal moves, make the move
        for move in self.legalMoves: 
            if self.targetSq == move.endSq:

                self.checkPawnPromotion(move)

                self.board.makeMove(move)
                self.switchTurn()

                self.resetMoveData()
                return


    def getSquareFromPos(self, pos):
        # Converts mouse position to board coordinates
        col = pos[0] // SQ_SIZE
        row = pos[1] // SQ_SIZE
        return (row, col)
    

    def checkPawnPromotion(self, move):
        # Checks if the move is a pawn attempting to promote
        # Adds promotion type to the move

        # If no piece or not a pawn
        if move.piece.type != 'P':
            return

        if (move.piece.colour == 'w' and move.endSq[0] == 0) or (move.piece.colour == 'b' and move.endSq[0] == 7):
            while True:
                promotionType = input("Promotion! (Q, R, B, N): ").upper()
                if promotionType in ('Q', 'R', 'B', 'N'):
                    move.promotionType = promotionType
                    return
                else:
                    print("Invalid Piece")


    def switchTurn(self):
        # Switches turns
        self.turn = 'b' if self.turn == 'w' else 'w'

    def resetMoveData(self):
        # Reset selected squares
        self.pieceSq = ()
        self.targetSq = ()
        self.legalMoves = []
        self.targetSqs = []
