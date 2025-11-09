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

    def movePiece(self, start, end, turn):
        startRow, startCol = start
        endRow, endCol = end
        piece = self.grid[startRow][startCol]
        target = self.grid[endRow][endCol]

        # Piece to move must be of correct colour
        if piece is None or piece.colour != turn:
            return False
        
        # Piece cannot move to a square occupied by its own colour
        if target is not None and target.colour == turn:
            return False
        
        # Move must be valid
        if not self.validMove():
            return False
        
        self.grid[endRow][endCol] = piece
        self.grid[startRow][startCol] = None

        return True
        
    def validMove(self):
        return True