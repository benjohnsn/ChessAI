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
        # Returns piece at square
        row, col = square
        return self.grid[row][col]
    
    def makeMove(self, pieceSq, targetSq):
        # Moves piece to the target square
        startRow, startCol = pieceSq
        endRow, endCol = targetSq
        self.grid[endRow][endCol] = self.grid[startRow][startCol]
        self.grid[startRow][startCol] = None

    def generateLegalMoves(self, piece, square):
        # Calls appropriate move generator function
        match piece.type:
            case 'P': return self.generatePawnMoves(piece, square)
            case 'N': return self.generateKnightMoves(piece, square)
            case 'B': return self.generateBishopMoves(piece, square)
            case 'R': return self.generateRookMoves(piece, square)
            case 'Q': return self.generateQueenMoves(piece, square)
            case 'K': return self.generateKingMoves(piece, square)

    def generatePawnMoves(self, piece, square):
        # Generates the list of legal pawn moves
        row, col = square
        moves = []
        if piece.colour == 'w':
            direction = -1
        else:
            direction = +1

        # Forward one square
        if self.inBounds(row + direction, col):
            target = self.grid[row + direction][col]
            if target is None:
                moves.append((row + direction,col))
                
                # Forward two squares (only if pawn has not moved)
                if self.inBounds(row + (direction * 2), col):
                    if not piece.moved:
                        target = self.grid[row + (direction * 2)][col]
                        if target is None:
                            moves.append((row + direction * 2, col))
       
        # Diagonal Captures
        for offset in (-1, 1):
            if self.inBounds(row + direction, col + offset):
                target = self.grid[row + direction][col + offset]
                if target and target.colour != piece.colour:
                    moves.append((row + direction, col + offset))

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

    def inBounds(self, row, col):
        # Checks if square is on the board
        return (0 <= row < 8) and (0 <= col < 8)