class Move:
    """
    Represents a single chess move
    - Includes all information required to undo a move
    """
    def __init__(self, startSq, endSq, piece, pieceCaptured=None, promotionPiece=None, isCastle=False, isEnPassant=False, pieceMoved=False):
    
        self.startSq = startSq
        self.endSq = endSq

        self.piece = piece
        self.pieceCaptured = pieceCaptured
        self.promotionPiece = promotionPiece

        self.isCastle = isCastle
        self.isEnPassant = isEnPassant

        self.pieceMoved = pieceMoved

    def __repr__(self):
        return f"Move({self.startSq}->{self.endSq}, {self.piece.type})"