
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor, QIcon, QBrush, QPen, QPainter, QTransform
from PyQt5.QtWidgets import QFrame, QDockWidget, QGridLayout, QPushButton, QComboBox, QLabel
import chess
from ChessEventManager import eventManager

class GameSettings(QDockWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_gui()


    def init_gui(self):
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.setMinimumSize(300, 80)
        self.setMaximumSize(300, 80)
        self.setWindowTitle("Player Settings")

        self.mainWidget = QFrame(self)
        self.mainWidget.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        self.mainLayout = QGridLayout()
        # self.mainLayout.setContentsMargins(5, 5, 5, 5)
        self.mainWidget.setLayout(self.mainLayout)
        
        whiteLabel = QLabel("White")
        whiteLabel.setAlignment(Qt.AlignHCenter)
        self.mainLayout.addWidget(whiteLabel, 0, 0)
        self.whiteComboBox = QComboBox()
        self.whiteComboBox.addItems(["Player", "Stockfish", "LeelaZero"])
        self.mainLayout.addWidget(self.whiteComboBox, 1, 0)

        vsLabel = QLabel("vs.")
        vsLabel.setAlignment(Qt.AlignHCenter)
        self.mainLayout.addWidget(vsLabel, 1, 1)

        blackLabel = QLabel("Black")
        blackLabel.setAlignment(Qt.AlignHCenter)
        self.mainLayout.addWidget(blackLabel, 0, 2)
        self.blackComboBox = QComboBox()
        self.blackComboBox.addItems(["Player", "Stockfish", "LeelaZero"])
        self.mainLayout.addWidget(self.blackComboBox, 1, 2)

        self.setWidget(self.mainWidget)

