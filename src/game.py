import pygame
from gui import Gui
from board import Board
from constants import FPS, SQ_SIZE
class Game:
    """
    Main class
    - Tracks game state
    - Draws board through Gui
    - Handles player inputs
    - Executes moves using board and updates turn
    """
    def __init__(self):
        # Initialises pygame, objects and game data
        pygame.init()
        self.running = True
        self.gameEnd = False
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
            if self.gameEnd:
                pygame.time.delay(5000)
                self.running = False
            self.clock.tick(FPS)


    def handleEvents(self):
        # Handles pygame events: quit, mouse click
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handleClick(pygame.mouse.get_pos())


    def handleClick(self, pos):
        # Handles a player click
        square = self.getSquareFromPos(pos)
        piece = self.board.getPiece(square)

        # 1st click
        # - Must be a piece of the current player's colour (allows re-selection)
        # - Checks if piece is not None (None has no .colour attribute)
        if piece and piece.colour == self.turn:
            self.firstClick(square, piece)
            return
        
        # 2nd click
        # - If no valid first click, return
        if not self.pieceSq:
            return
        
        # - Assign 2nd click because it must be empty/opponent square
        self.targetSq = square

        self.makePlayerMove()


    def firstClick(self, square, piece):
        # 1st click
        self.pieceSq = square
        self.legalMoves = self.board.generateLegalMoves(piece, square)
        self.targetSqs = [move.endSq for move in self.legalMoves]


    def makePlayerMove(self):
        # - If click is in the list of legal moves, make the move
        for move in self.legalMoves: 
            if self.targetSq == move.endSq:

                self.checkPawnPromotion(move)
                self.board.makeMove(move)
                self.switchTurn()
                self.resetMoveData()
                self.gameEnd = self.checkGameEnd()
                return


    def getSquareFromPos(self, pos):
        # Converts mouse position to board coordinates
        col = pos[0] // SQ_SIZE
        row = pos[1] // SQ_SIZE
        return (row, col)


    def checkPawnPromotion(self, move):
        # Checks if the move is a pawn attempting to promote
        # Adds promotion type to the move

        # Check for pawn move
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


    def checkGameEnd(self):
        # Checks for Game end
        if self.board.generateAllLegalMoves(self.turn):
            return False
        
        if self.board.inCheck(self.turn):
            if self.turn == 'w':
                print("Checkmate: Black won!")
            else:
                print("Checkmate: White won!")
        else:
            print("Stalemate!")

        return True


    def resetMoveData(self):
        # Resets Move Data
        self.pieceSq = ()
        self.targetSq = ()
        self.legalMoves = []
        self.targetSqs = []
