from piece import Piece
from move import Move
from movegen import MoveGen

class Board:
    """
    Represents the chess board
    - Stores and updates the board (move/undo) using history
    - Generates pseudo-legal moves for each piece
    - Filters for legal moves using check detection
    """
    def __init__(self):
        self.grid = [
            [Piece('b','R'), Piece('b','N'), Piece('b','B'), Piece('b','Q'), Piece('b','K'), Piece('b','B'), Piece('b','N'), Piece('b','R')],
            [Piece('b','P') for _ in range(8)],
            [None]*8,
            [None]*8,
            [None]*8,
            [None]*8,
            [Piece('w','P') for _ in range(8)],
            [Piece('w','R'), Piece('w','N'), Piece('w','B'), Piece('w','Q'), Piece('w','K'), Piece('w','B'), Piece('w','N'), Piece('w','R')]
        ]
        self.moveGen = MoveGen(self)
        self.history = []
        self.enPassantTargetSq = ()

    def getPiece(self, square):
        # Returns piece at square
        row, col = square
        return self.grid[row][col]
    
    def makeMove(self, move, isTest=False):
        # Executes a move object on the board and pushes it to history
        startRow, startCol = move.startSq
        endRow, endCol = move.endSq

        if not isTest and self.enPassantTargetSq:
            self.resetEnPassantTarget()

        self.grid[startRow][startCol] = None
        
        if move.promotionType:
            piece = Piece(move.piece.colour, move.promotionType)
            self.grid[endRow][endCol] = piece
        elif move.isEnPassant:
            capRow = endRow + (1 if move.piece.colour == 'w' else -1)
            self.grid[capRow][endCol] = None
            self.grid[endRow][endCol] = move.piece
        elif move.isCastle:
            self.grid[endRow][endCol] = move.piece
            if move.piece.colour == 'w':
                if move.kingSide == True:
                    self.grid[7][5] = self.grid[7][7]
                    self.grid[7][7] = None
                    self.grid[7][5].moved = True
                else:
                    self.grid[7][3] = self.grid[7][0]
                    self.grid[7][0] = None
                    self.grid[7][3].moved = True
            else:
                if move.kingSide == True:
                    self.grid[0][5] = self.grid[0][7]
                    self.grid[0][7] = None
                    self.grid[0][5].moved = True
                else:
                    self.grid[0][3] = self.grid[0][0]
                    self.grid[0][0] = None
                    self.grid[0][3].moved = True
        else:
            self.grid[endRow][endCol] = move.piece

        move.pieceMoved = move.piece.moved
        move.piece.moved = True

        if not isTest:
            self.setEnPassantTarget(move, startRow, endRow)

        self.history.append(move)

    
    def setEnPassantTarget(self, move, startRow, endRow):
        # Sets the enPassantTarget flag
        if move.piece.type == 'P':
            if abs(startRow - endRow) == 2:
                move.piece.enPassantTarget = True
                self.enPassantTargetSq = move.endSq


    def resetEnPassantTarget(self):
        # Resets the enPassantTarget Flag
        row, col = self.enPassantTargetSq
        piece = self.grid[row][col]

        if piece and piece.type == 'P':
            piece.enPassantTarget = False
        
        self.enPassantTargetSq = ()


    def undoMove(self):
        # Undoes a move using history
        move = self.history.pop()

        startRow, startCol = move.startSq
        endRow, endCol = move.endSq

        self.grid[startRow][startCol] = move.piece
        if move.isEnPassant:
            self.grid[endRow][endCol] = None
            capRow = endRow + (1 if move.piece.colour == 'w' else -1)
            self.grid[capRow][endCol] = move.pieceCaptured
        elif move.isCastle:
            self.grid[endRow][endCol] = None
            if move.piece.colour == 'w':
                if move.kingSide == True:
                    self.grid[7][7] = self.grid[7][5]
                    self.grid[7][5] = None
                    self.grid[7][7].moved = False
                else:
                    self.grid[7][0] = self.grid[7][3]
                    self.grid[7][3] = None
                    self.grid[7][0].moved = False
            else:
                if move.kingSide == True:
                    self.grid[0][7] = self.grid[0][5]
                    self.grid[0][5] = None
                    self.grid[0][7].moved = False
                else:
                    self.grid[0][0] = self.grid[0][3]
                    self.grid[0][3] = None
                    self.grid[0][0].moved = False
        else:
            self.grid[endRow][endCol] = move.pieceCaptured

        move.piece.moved = move.pieceMoved

    def generateLegalMoves(self, piece, square):
        return self.moveGen.generateLegalMoves(piece, square)