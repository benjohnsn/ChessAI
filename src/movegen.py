from move import Move
from constants import DIMENSION, KNIGHT_OFFSETS, BISHOP_DIRECTIONS, ROOK_DIRECTIONS, QUEEN_DIRECTIONS, KING_OFFSETS

class MoveGen:
    def __init__(self, board):
        self.board = board

    def generateLegalMoves(self, piece, square):
        # Generates the list of legal Moves
        pseudoLegalMoves = self.generatePseudoLegalMoves(piece, square)
        legalMoves = []

        for move in pseudoLegalMoves:
            self.board.makeMove(move, isTest=True)

            if not self.isKingInCheck(piece.colour):
                legalMoves.append(move)

            self.board.undoMove()

        return legalMoves


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

        rowOffset = -1 if piece.colour == 'w' else 1
            
        r = row + rowOffset
        c = col

        # Forward one square
        if self.inBounds(r, c):
            target = self.board.grid[r][c]
            if target is None:
                move = Move(square, (r, c), piece, target, piece.moved)
                moves.append(move)
                
                r2 = row + (rowOffset * 2)

                # Forward two squares (only if pawn has not moved)
                if self.inBounds(r2, c):
                    if not piece.moved:
                        target = self.board.grid[r2][c]
                        if target is None:
                            move = Move(square, (r2, c), piece, target, piece.moved)
                            moves.append(move)


        # Diagonal Captures
        for colOffset in (-1, 1):
            c = col + colOffset
            if self.inBounds(r, c):
                target = self.board.grid[r][c]
                if target and target.colour != piece.colour:
                    move = Move(square, (r, c), piece, target, piece.moved)
                    moves.append(move)
            if self.inBounds(row, c): 
                target = self.board.grid[row][c] 
                if target and target.colour != piece.colour and target.enPassantTarget == True: 
                    move = Move(square, (r, c), piece, target, piece.moved, isEnPassant=True) 
                    moves.append(move)

        return moves


    def generateKnightMoves(self, piece, square):
        # Generates the list of legal Knight moves
        row, col = square
        moves = []

        for rowOffset, colOffset in KNIGHT_OFFSETS:
            r = row + rowOffset
            c = col + colOffset
            if self.inBounds(r, c):
                target = self.board.grid[r][c]
                if target is None or target.colour != piece.colour:
                    move = Move(square, (r, c), piece, target, piece.moved)
                    moves.append(move)

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
                target = self.board.grid[r][c]
                
                if target is None:          # Empty Square
                    move = Move(square, (r, c), piece, target, piece.moved)
                    moves.append(move)
                else:
                    if target.colour != piece.colour:   # Opponent Piece
                        move = Move(square, (r, c), piece, target, piece.moved)
                        moves.append(move)
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
                target = self.board.grid[r][c]
                if target is None or target.colour != piece.colour:
                    move = Move(square, (r, c), piece, target, piece.moved)
                    moves.append(move)

        if piece.moved == False and not self.isKingInCheck(piece.colour):
            if piece.colour == 'w':

                cornerPiece = self.board.grid[7][7]
                if cornerPiece and cornerPiece.type == 'R' and cornerPiece.colour == piece.colour and cornerPiece.moved == False:
                    if self.board.grid[7][5] is None and self.board.grid[7][6] is None:
                        if not self.squareAttacked((7, 5), 'b') and not self.squareAttacked((7, 6), 'b'):
                            move = Move(square, (7, 6), piece, None, piece.moved, isCastle=True, kingSide=True)
                            moves.append(move)

                cornerPiece = self.board.grid[7][0]
                if cornerPiece and cornerPiece.type == 'R' and cornerPiece.colour == piece.colour and cornerPiece.moved == False:
                    if self.board.grid[7][3] is None and self.board.grid[7][2] is None and self.board.grid[7][1] is None:
                        if not self.squareAttacked((7, 3), 'b') and not self.squareAttacked((7, 2), 'b'):
                            move = Move(square, (7, 2), piece, None, piece.moved, isCastle=True)
                            moves.append(move)
            else:
                
                cornerPiece = self.board.grid[0][7]
                if cornerPiece and cornerPiece.type == 'R' and cornerPiece.colour == piece.colour and cornerPiece.moved == False:
                    if self.board.grid[0][5] is None and self.board.grid[0][6] is None:
                        if not self.squareAttacked((0, 5), 'w') and not self.squareAttacked((0, 6), 'w'):
                            move = Move(square, (0, 6), piece, None, piece.moved, isCastle=True, kingSide=True)
                            moves.append(move)

                cornerPiece = self.board.grid[0][0]
                if cornerPiece and cornerPiece.type == 'R' and cornerPiece.colour == piece.colour and cornerPiece.moved == False:
                    if self.board.grid[0][3] is None and self.board.grid[0][2] is None and self.board.grid[0][1] is None:
                        if not self.squareAttacked((0, 3), 'w') and not self.squareAttacked((0, 2), 'w'):
                            move = Move(square, (0, 2), piece, None, piece.moved, isCastle=True)
                            moves.append(move)

        return moves


    def inBounds(self, row, col):
        # Checks if square is on the board
        return (0 <= row < DIMENSION) and (0 <= col < DIMENSION)
    

    def isKingInCheck(self, colour):
        # Checks if the player's king is in check
        square = self.findKing(colour)
        enemy = 'b' if colour == 'w' else 'w'
        return self.squareAttacked(square, enemy)
            

    def findKing(self, colour):
    # Iterates through the board to find the player's king
        for row in range(DIMENSION):
            for col in range(DIMENSION):
                piece = self.board.grid[row][col]
                if piece and piece.type == 'K' and piece.colour == colour:
                    return (row, col)


    def squareAttacked(self, square, enemy):
        # Checks if a square is attacked by the enemy
        row, col = square

        # Pawn Attacks
        rowOffset = 1 if enemy == 'w' else -1    

        for colOffset in (-1, 1):
            r = row + rowOffset
            c = col + colOffset
            if self.inBounds(r, c):
                piece = self.board.grid[r][c]
                if piece and piece.colour == enemy and piece.type == 'P':
                    return True
        
        # Knight Attacks
        for rowOffset, colOffset in KNIGHT_OFFSETS:
            r = row + rowOffset
            c = col + colOffset
            if self.inBounds(r, c):
                piece = self.board.grid[r][c]
                if piece and piece.colour == enemy and piece.type == 'N':
                    return True

        # Rook and Queen Attacks (straight lines) 
        for rowDir, colDir in ROOK_DIRECTIONS:
            r = row + rowDir
            c = col + colDir

            while self.inBounds(r, c):
                piece = self.board.grid[r][c]

                if piece:
                    if piece.colour == enemy and (piece.type == 'R' or piece.type == 'Q'):
                        return True
                    break

                r += rowDir
                c += colDir

        # Bishop and Queen Attacks (diagonal lines)
        for rowDir, colDir in BISHOP_DIRECTIONS:
            r = row + rowDir
            c = col + colDir

            while self.inBounds(r, c):
                piece = self.board.grid[r][c]

                if piece:
                    if piece.colour == enemy and (piece.type == 'B' or piece.type == 'Q'):
                        return True
                    break

                r += rowDir
                c += colDir

        # King Attacks
        for rowOffset, colOffset in KING_OFFSETS:
            r = row + rowOffset
            c = col + colOffset
            if self.inBounds(r, c):
                piece = self.board.grid[r][c]
                if piece and piece.colour == enemy and piece.type == 'K':
                    return True
                
        return False