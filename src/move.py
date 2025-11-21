class Move:
    """
    Represents a single chess move
    - Includes all information required to make/undo a move
    """
    def __init__(self, startSq, endSq, piece, pieceCaptured=None, pieceMoved=False, promotionType=None, isEnPassant=False, isCastle=False, kingSide=False):
    
        self.startSq = startSq
        self.endSq = endSq

        self.piece = piece
        self.pieceCaptured = pieceCaptured

        self.pieceMoved = pieceMoved

        self.promotionType = promotionType

        self.isEnPassant = isEnPassant

        self.isCastle = isCastle
        self.kingSide = kingSide


    def __repr__(self):
        return f"Move({self.startSq}->{self.endSq}, {self.piece.type})"