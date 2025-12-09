class Move:
    """
    Represents a single chess move
    - Includes all information required to make/undo a move
    """
    def __init__(self, startSq, endSq, piece, pieceCaptured=None, prevPieceMoved=False, promotionType=None, isEnPassant=False, prevEnPassantSq=None, isCastle=False, kingSide=False):
    
        self.startSq = startSq
        self.endSq = endSq

        self.piece = piece
        self.pieceCaptured = pieceCaptured

        self.prevPieceMoved = prevPieceMoved

        self.promotionType = promotionType
        
        self.isEnPassant = isEnPassant
        self.prevEnPassantSq = prevEnPassantSq

        self.isCastle = isCastle
        self.kingSide = kingSide


    def __repr__(self):
        return f"Move({self.startSq}->{self.endSq}, {self.piece.type})"