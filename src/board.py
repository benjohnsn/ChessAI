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

    def generateLegalMoves(self, piece, square):
        match piece.type:
            case 'P': return self.generatePawnMoves(piece, square)
            case 'N': return self.generatePawnMoves(piece, square)
            case 'B': return self.generatePawnMoves(piece, square)
            case 'R': return self.generatePawnMoves(piece, square)
            case 'Q': return self.generatePawnMoves(piece, square)
            case 'K': return self.generatePawnMoves(piece, square)

    def generatePawnMoves(self, piece, square):
        row, col = square
        moves = []

        if piece.colour == 'w':
            direction = -1
        else:
            direction = +1

        target = self.grid[row + direction][col]
        if target is None:
            moves.append((row + direction,col))

        if not piece.moved:
            target = self.grid[row + (direction * 2)][col]
            if target is None:
                moves.append((row + direction * 2, col))

        

        return moves

    def generateKnightMoves(self, piece, square):
        pass
    def generateBishopMoves(self, piece, square):
        pass
    def generateRookMoves(self, piece, square):
        pass
    def generateQueenMoves(self, piece, square):
        pass
    def generateKingMoves(self, piece, square):
        pass