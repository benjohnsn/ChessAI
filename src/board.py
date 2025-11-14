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
        
    def getPiece(self, square):
        row, col = square
        return self.grid[row][col]
    
    def makeMove(self, pieceSq, targetSq):
        startRow, startCol = pieceSq
        endRow, endCol = targetSq
        self.grid[endRow][endCol] = self.grid[startRow][startCol]
        self.grid[startRow][startCol] = None
