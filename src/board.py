from piece import Piece
from constants import KNIGHT_OFFSETS, BISHOP_DIRECTIONS, ROOK_DIRECTIONS, QUEEN_DIRECTIONS, KING_OFFSETS

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

        piece = self.grid[startRow][startCol]
        piece.moved = True

        self.grid[endRow][endCol] = piece
        self.grid[startRow][startCol] = None

    def generateLegalMoves(self, piece, square):
        # Calls appropriate move generator function
        match piece.type:
            case 'P': return self.generatePawnMoves(piece, square)
            case 'N': return self.generateKnightMoves(piece, square)
            case 'B': return self.generateSlidingMoves(piece, square, BISHOP_DIRECTIONS)
            case 'R': return self.generateSlidingMoves(piece, square, ROOK_DIRECTIONS)
            case 'Q': return self.generateSlidingMoves(piece, square, QUEEN_DIRECTIONS)
            case 'K': return self.generateKingMoves(piece, square)

    def generatePawnMoves(self, piece, square):
        # Generates the list of legal pawn moves
        row, col = square
        moves = []

        if piece.colour == 'w':
            rowOffset = -1
        else:
            rowOffset = +1

        # Forward one square
        if self.inBounds(row + rowOffset, col):
            target = self.grid[row + rowOffset][col]
            if target is None:
                moves.append((row + rowOffset,col))
                
                # Forward two squares (only if pawn has not moved)
                if self.inBounds(row + (rowOffset * 2), col):
                    if not piece.moved:
                        target = self.grid[row + (rowOffset * 2)][col]
                        if target is None:
                            moves.append((row + rowOffset * 2, col))
       
        # Diagonal Captures
        for colOffset in (-1, 1):
            if self.inBounds(row + rowOffset, col + colOffset):
                target = self.grid[row + rowOffset][col + colOffset]
                if target and target.colour != piece.colour:
                    moves.append((row + rowOffset, col + colOffset))

        return moves

    def generateKnightMoves(self, piece, square):
        # Generates the list of legal Knight moves
        row, col = square
        moves = []

        for rowOffset, colOffset in KNIGHT_OFFSETS:
            if self.inBounds(row + rowOffset, col + colOffset):
                target = self.grid[row + rowOffset][col + colOffset]
                if target is None or target.colour != piece.colour:
                    moves.append((row + rowOffset, col + colOffset))

        return moves

    def generateSlidingMoves(self, piece, square, directions):
        # Generates the list of sliding moves given a list of directions
        row, col = square
        moves = []

        # Check for each direction the piece can slide
        for rowDir, colDir in directions:

            # Step to first square in this direction
            curRow = row + rowDir
            curCol = col + colDir

            # Keep moving until out of bounds/blocked
            while self.inBounds(curRow, curCol):
                target = self.grid[curRow][curCol]
                
                if target is None:
                    # Empty Square
                    moves.append((curRow, curCol))
                else:
                    # Opponent piece
                    if target.colour != piece.colour:
                        moves.append((curRow, curCol))
                    # Blocked by friendly piece
                    break
                
                # Step to the next square in this direction
                curRow += rowDir
                curCol += colDir

        return moves
    
    def generateKingMoves(self, piece, square):
        # Generate the list of legal King Moves
        row, col = square
        moves = []

        for rowOffset, colOffset in KING_OFFSETS:
            if self.inBounds(row + rowOffset, col + colOffset):
                target = self.grid[row + rowOffset][col + colOffset]
                if target is None or target.colour != piece.colour:
                    moves.append((row + rowOffset, col + colOffset))

        return moves


    def inBounds(self, row, col):
        # Checks if square is on the board
        return (0 <= row < 8) and (0 <= col < 8)