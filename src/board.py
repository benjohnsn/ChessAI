from piece import Piece
from constants import DIMENSION, KNIGHT_OFFSETS, BISHOP_DIRECTIONS, ROOK_DIRECTIONS, QUEEN_DIRECTIONS, KING_OFFSETS

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

    def generatePseudoLegalMoves(self, piece, square):
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

        r = row + rowOffset
        c = col

        # Forward one square
        if self.inBounds(r, c):
            target = self.grid[r][c]
            if target is None:
                moves.append((r,c))
                
                r = row + (rowOffset * 2)

                # Forward two squares (only if pawn has not moved)
                if self.inBounds(r, c):
                    if not piece.moved:
                        target = self.grid[r][c]
                        if target is None:
                            moves.append((r, c))

        # Diagonal Captures
        for colOffset in (-1, 1):
            r = row + rowOffset
            c = col + colOffset
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
            r = row + rowOffset
            c = col + colOffset
            if self.inBounds(r, c):
                target = self.grid[r][c]
                if target is None or target.colour != piece.colour:
                    moves.append((r, c))

        return moves

    def generateSlidingMoves(self, piece, square, directions):
        # Generates the list of sliding moves given a list of directions
        row, col = square
        moves = []

        # Check for each direction the piece can slide
        for rowDir, colDir in directions:
            r = row + rowDir
            c = col + colDir

            # Keep moving until out of bounds/blocked
            while self.inBounds(r, c):
                target = self.grid[r][c]
                
                if target is None:          # Empty Square
                    moves.append((r, c))
                else:
                    if target.colour != piece.colour:   # Opponent Piece
                        moves.append((r, c))
                    break                               # Blocked by Friendly Piece
                
                # Step to the next square in this direction
                r += rowDir
                c += colDir

        return moves
    
    def generateKingMoves(self, piece, square):
        # Generate the list of legal King Moves
        row, col = square
        moves = []

        for rowOffset, colOffset in KING_OFFSETS:
            r = row + rowOffset
            c = col + colOffset
            if self.inBounds(r, c):
                target = self.grid[r][c]
                if target is None or target.colour != piece.colour:
                    moves.append((r, c))

        return moves

    def inBounds(self, row, col):
        # Checks if square is on the board
        return (0 <= row < DIMENSION) and (0 <= col < DIMENSION)
    
    def isKingInCheck(self, colour):
        # Checks if the player's king is in check
        kingRow, kingCol = self.findKing(colour)

        if colour == 'w':
            enemy = 'b'
        else:
            enemy = 'w'

        # Pawn Attacks
        if colour == 'w':
            rowOffset = -1
        else:
            rowOffset = +1

        for colOffset in (-1, 1):
            r = kingRow + rowOffset
            c = kingCol + colOffset
            if self.inBounds(r, c):
                piece = self.grid[r][c]
                if piece and piece.colour == enemy and piece.type == 'P':
                    return True
        
        # Knight Attacks
        for rowOffset, colOffset in KNIGHT_OFFSETS:
            r = kingRow + rowOffset
            c = kingCol + colOffset
            if self.inBounds(r, c):
                piece = self.grid[r][c]
                if piece and piece.colour == enemy and piece.type == 'N':
                    return True

        # Rook and Queen Attacks (straight lines) 
        for rowDir, colDir in ROOK_DIRECTIONS:
            r = kingRow + rowDir
            c = kingCol + colDir

            while self.inBounds(r, c):
                piece = self.grid[r][c]

                if piece:
                    if piece.colour == enemy and (piece.type == 'R' or piece.type == 'Q'):
                        return True
                    break

                r += rowDir
                c += colDir

        # Bishop and Queen Attacks (diagonal lines)
        for rowDir, colDir in BISHOP_DIRECTIONS:
            r = kingRow + rowDir
            c = kingCol + colDir

            while self.inBounds(r, c):
                piece = self.grid[r][c]

                if piece:
                    if piece.colour == enemy and (piece.type == 'B' or piece.type == 'Q'):
                        return True
                    break

                r += rowDir
                c += colDir
                
        return False

    def findKing(self, colour):
        # Iterates through the board to find the player's king
        for row in range(DIMENSION):
            for col in range(DIMENSION):
                piece = self.grid[row][col]
                if piece and piece.type == 'K' and piece.colour == colour:
                    return (row, col)
                