from piece import Piece

class Board:
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
        self.pieceSquare = ()
        self.targetSquare = ()
    
    def handleSquareClick(self, square, turn, highlightSq):
        piece = self.getPiece(square)
        if self.pieceSquare == ():
            if piece is not None and piece.colour == self.turn:
                self.pieceSquare = square
        else:
            if piece is not None and piece.colour == self.turn:
                self.pieceSquare = square
            else:
                self.targetSquare = square
        
        self.makeMove(piece, self.pieceSquare, self.targetSquare)


        return True
    
    def getPiece(self, square):
        row, col = square
        return self.grid[row][col]
    
    def makeMove(self, piece, start, target):
        startRow, startCol = start
        endRow, endCol = target
        self.grid[endRow][endCol] = piece
        self.grid[startRow][startCol] = None