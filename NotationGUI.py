
from PyQt5.QtCore import Qt, QAbstractTableModel
from PyQt5.QtGui import QPalette, QColor, QIcon, QBrush, QPen, QPainter, QTransform
from PyQt5.QtWidgets import QFrame, QDockWidget, QLabel, QHBoxLayout, QVBoxLayout
import chess
from ChessEventManager import eventManager

# Tutorial from https://www.pythonguis.com/tutorials/qtableview-modelviews-numpy-pandas/

class NotationGUI(QDockWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.setMinimumSize(300, 500)
        self.setWindowTitle("Notation")
        eventManager.onMove += self.update
        eventManager.newGame += self.clear
        
        self.data = [["", "", ""]]

        self.centralWidget = QFrame()
        self.centralWidget.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        self.moveLayout = QVBoxLayout()
        self.moveLayout.setAlignment(Qt.AlignTop)
        self.centralWidget.setLayout(self.moveLayout)
        self.setWidget(self.centralWidget)

    def set_board(self, board:chess.Board) -> None:
        self.board = board
        # self.game = chess.pgn.Game.from_board(self.board)

    def line_count(self) -> int:
        mv = len(self.board.move_stack)
        return mv//2+mv%2

    def clear(self) -> None:
        pass

    def update(self, move: chess.Move, san: str, *args) -> None:

        # Do we need to add a new line?
        if self.moveLayout.count()<self.line_count():
        
            # create labels
            self.move_number_label = QLabel(f"<b>{self.line_count()}:</b>")
            self.white_move_label = QLabel()
            self.black_move_label = QLabel()

            # create line
            self.current_line = QHBoxLayout()
            self.current_line.addWidget(self.move_number_label)
            self.current_line.addWidget(self.white_move_label)
            self.current_line.addWidget(self.black_move_label)

            # add line to layout
            self.moveLayout.addLayout(self.current_line)
        
        if self.board.turn == chess.WHITE:
            # black played last
            # self.black_move_label.setText( move.uci() )
            self.black_move_label.setText(san)
        elif self.board.turn == chess.BLACK:
            # self.white_move_label.setText( move.uci() )               
            self.white_move_label.setText(san)


    def update_old(self, move: chess.Move, *args) -> None:
        m=0
        while m<len(self.board.move_stack):
            line = QHBoxLayout()
            self.moveLayout.addLayout(line)
            moveNumber = QLabel(f"<b>{m//2+1}:</b> ")
            # self.moveLayout.addWidget(moveNumber, m//2, 0, Qt.AlignTop)
            line.addWidget(moveNumber)
            whiteMove = QLabel(f"{self.board.move_stack[m].uci()}")
            # self.moveLayout.addWidget(whiteMove, m//2, 1, Qt.AlignTop)
            line.addWidget(whiteMove)
            if (m+1) < len(self.board.move_stack):
                blackMove = QLabel(f"{self.board.move_stack[m+1].uci()}")
                # self.moveLayout.addWidget(blackMove, m//2, 2, Qt.AlignTop)
                line.addWidget(blackMove)
            else:
                # self.moveLayout.addWidget(QLabel(""), m//2, 2, Qt.AlignTop)
                line.addWidget(QLabel(""))
            m+=2
