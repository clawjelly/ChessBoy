from PyQt5.QtCore import Qt, QRectF, QPointF, QSize
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtWidgets import QWidget, QGraphicsScene, QGraphicsItem, \
                            QGraphicsPixmapItem, QGraphicsDropShadowEffect, \
                            QStyleOptionGraphicsItem
import chess

from ChessEventManager import eventManager

piece_source = dict()

piece_source["P"] = "imgs//Pawn White.png"
piece_source["R"] = "imgs//Rook White.png"
piece_source["N"] = "imgs//Knight White.png"
piece_source["B"] = "imgs//Bishop White.png"
piece_source["Q"] = "imgs//Queen White.png"
piece_source["K"] = "imgs//King White.png"

piece_source["p"] = "imgs//Pawn Black.png"
piece_source["r"] = "imgs//Rook Black.png"
piece_source["n"] = "imgs//Knight Black.png"
piece_source["b"] = "imgs//Bishop Black.png"
piece_source["q"] = "imgs//Queen Black.png"
piece_source["k"] = "imgs//King Black.png"

square_size = 256

def square_to_pos(square: int):    
    return (square % 8 + .5)*square_size, (7.5-(square//8))*square_size

def pos_to_square(x: float, y: float) -> int:
    return int(x // square_size + (square_size*8 - y) // square_size * 8 )

class BoardGUI(QGraphicsScene):

    def __init__(self, *args, **kwargs):
        super().__init__()

        self.scale = 1.0
        self.init_graphics()
        self.pool = PiecesPool()
        eventManager.newPieceOnBoard += self.newPieceOnBoard

    def init_graphics(self):
        self.board = BoardGfx()
        self.addItem(self.board)

    def fit_to_window_scale(self, window_size: QSize, padding=100) -> float:
        size_base = min(window_size.width(), window_size.height())
        size_div = self.board.rect.bottomRight().x()
        return size_base/(size_div+padding)

    def setup_board(self, board:chess.Board) -> None:
        self.pool.clear_pieces()
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece!=None:
                pos=square_to_pos(square)
                self.add_piece(piece.symbol(), *pos)

    def newPieceOnBoard(self, piece):
        self.addItem(piece)

    def add_piece(self, pieceType: str, x: int, y: int):
        piece = self.pool.get_piece(pieceType)
        piece.setPos(x, y)


class BoardGfx(QGraphicsItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        # Setup squares
        self.square_source = dict()
        self.square_source[0] = "imgs//Field Light.png"
        self.square_source[1] = "imgs//Field Dark.png"
        self.rect = QRectF( QPointF(0, 0), QPointF(1, 1))
        for squareID in range(0, 64):
            square = SquareGfx()
            bw = ((squareID//8) % 2 + squareID % 2) % 2
            sqx = QPixmap(self.square_source[bw])
            square.setPixmap(sqx)
            x = sqx.width()*(squareID % 8)
            y = sqx.height()*(squareID//8)
            square.setPos(x, y)
            square.setParentItem(self)
        self.rect.setBottomRight(
            QPointF(x+sqx.width(), y+sqx.height()))
        self.square_size = sqx.width()
    
    def boundingRect(self) -> QRectF:
        return self.rect

    # def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget):
    #     painter.drawPixmap()

class SquareGfx(QGraphicsPixmapItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

class PieceGfx(QGraphicsPixmapItem):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.setAcceptedMouseButtons(Qt.LeftButton | Qt.RightButton)
        self.setAcceptHoverEvents(True)
        self.setTransformationMode(Qt.SmoothTransformation)
        self.type=""

    def set_piece(self, pieceType: str):
        self.type=pieceType
        self.setPixmap(QPixmap(piece_source[pieceType]))
        size = self.pixmap().size()
        self.setOffset(-size.width()/2, -size.height()/2)

    def mousePressEvent(self, event):
        self.old_pos = self.pos()
        self.old_square = pos_to_square(self.pos().x(), self.pos().y())
        self.setPos(event.scenePos())
        self.setGraphicsEffect(QGraphicsDropShadowEffect())
        self.setScale(1.1)
        self.setZValue(2)
        eventManager.onPieceLifted(self)

    def mouseMoveEvent(self, event):
        self.setPos(event.scenePos())

    def mouseReleaseEvent(self, event):
        self.setGraphicsEffect(None)
        self.setScale(1.0)
        self.setZValue(0)
        self.new_square = pos_to_square(self.pos().x(), self.pos().y())
        self.setPos(self.old_pos)
        if self.old_square != self.new_square:
            move = chess.Move.from_uci(
                chess.SQUARE_NAMES[self.old_square] + chess.SQUARE_NAMES[self.new_square])
            eventManager.onMoveTry(move)

class PiecesPool:
    """ Manages piece instances so we don't need to create them twice. """

    def __init__(self) -> None:
        self.pieces = dict()

        self.pieces["P"] = []
        self.pieces["R"] = []
        self.pieces["N"] = []
        self.pieces["B"] = []
        self.pieces["Q"] = []
        self.pieces["K"] = []

        self.pieces["p"] = []
        self.pieces["r"] = []
        self.pieces["n"] = []
        self.pieces["b"] = []
        self.pieces["q"] = []
        self.pieces["k"] = []

    def clear_pieces(self):
        for pieces in self.pieces.values():
            for piece in pieces:
                piece.setVisible(False)

    def get_piece(self, pieceType: str) -> PieceGfx:
        free_pieces = [ piece for piece in self.pieces[pieceType] if not piece.isVisible() ]
        if len(free_pieces)<1:
            piece = PieceGfx()
            piece.set_piece(pieceType)
            self.pieces[pieceType].append(piece)
            eventManager.newPieceOnBoard(piece)
            return piece
        else:
            piece = free_pieces[0]
            piece.setVisible(True)
            return piece

if __name__=="__main__":

    import sys
    from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsView

    app = QApplication([])
    window = QMainWindow()
    board = BoardGUI()
    gv = QGraphicsView(board)
    # gv.scale(.5, .5)

    board.add_piece("p", 300, 300)

    window.setCentralWidget(gv)
    window.setGeometry(300, 300, 1280, 720)
    window.show()
    sys.exit(app.exec())



