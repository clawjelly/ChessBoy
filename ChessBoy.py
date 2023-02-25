# -------------------------------
# ChessBoy
# -------------------------------
# V 0.1

import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor, QIcon, QBrush, QPen, QPainter, QTransform
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, \
                            QVBoxLayout, QPushButton, \
                            QGraphicsScene, QGraphicsView, \
                            QMenuBar, QMenu, QAction, \
                            QDockWidget, QTextBrowser

from ChessEventManager import eventManager
from Preferences import Preferences
from BoardGUI import BoardGUI
from NotationGUI import NotationGUI
from GameSettings import GameSettings

import chess

from GameSettings import GameSettings
# import chess.engine
# import chess.svg

class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__()

        self.title = "Chessboy"
        self.width = 1920
        self.height = 1080
        self.iconName = "icons/ChessBoy.ico"
        self.setMinimumSize(800, 600)
        self.light_palette = QApplication.instance().palette()

        eventManager.onMoveTry += self.makeMoveEvent

        self.init_prefs()
        self.init_chess_board()
        self.init_gui()

        self.board_scene.setup_board(self.board)
        eventManager.newGame()

    # ---- Preferences

    def init_prefs(self):
        self.prefs = Preferences(self)

    def show_prefs(self):
        self.prefs.show()

    def set_dark_mode(self):
        app = QApplication.instance()
        app.setPalette(get_dark_mode())

    def set_light_mode(self):
        app = QApplication.instance()
        app.setPalette(self.light_palette)

    # --- Main GUI

    def init_gui(self):
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon(self.iconName))
        self.setGeometry(300, 300, self.width, self.height)

        self.init_menu_bar()
        self.init_board_gui()
        self.init_tool_bar()

        # docks
        self.init_player_settings_dock()
        self.init_notation_dock()

        self.show()

    def init_menu_bar(self):
        menuBar = self.menuBar()

        fileMenu = QMenu("&File", self)
        self.new_game_action = QAction("New Game", self)
        self.new_game_action.triggered.connect(self.new_game)
        fileMenu.addAction(self.new_game_action)
        menuBar.addMenu(fileMenu)

        editMenu = QMenu("&Edit", self)
        menuBar.addMenu(editMenu)
        self.dark_mode_action = QAction("Set Dark Mode", self)
        self.dark_mode_action.triggered.connect(self.set_dark_mode)
        editMenu.addAction(self.dark_mode_action)
        self.light_mode_action = QAction("Set Light Mode", self)
        self.light_mode_action.triggered.connect(self.set_light_mode)
        editMenu.addAction(self.light_mode_action)
        editMenu.addSeparator()
        self.show_prefs_action = QAction("Preferences", self)
        self.show_prefs_action.triggered.connect(self.show_prefs)
        editMenu.addAction(self.show_prefs_action)

        helpMenu = QMenu("&Help", self)
        self.show_about_action = QAction("About ChessBoy", self)
        helpMenu.addAction(self.show_about_action)
        menuBar.addMenu(helpMenu)

    def init_tool_bar(self):
        pass

    # ---- Board/BoardGUI

    def init_chess_board(self):
        self.board = chess.Board()

    def init_board_gui(self):
        # self.board_scene = QGraphicsScene()
        self.board_scene = BoardGUI()
        self.board_view = QGraphicsView(self.board_scene)
        self.board_view.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.board_view.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.board_view.setAcceptDrops(True)
        self.setCentralWidget(self.board_view)

    def init_player_settings_dock(self):
        self.player_settings_dock = GameSettings()
        self.player_settings_dock.resizeEvent = self.resizeEvent
        self.addDockWidget(Qt.RightDockWidgetArea, self.player_settings_dock)

    def init_notation_dock(self):
        self.notation_dock = NotationGUI()
        self.notation_dock.resizeEvent = self.resizeEvent
        self.addDockWidget(Qt.RightDockWidgetArea, self.notation_dock)
        self.notation_dock.set_board(self.board)

    def new_game(self):
        self.board.reset()
        self.board_scene.setup_board(self.board)
        eventManager.newGame()

    # --- Events

    def resizeEvent(self, event):
        scale = self.board_scene.fit_to_window_scale(self.board_view.size())
        transf = QTransform()
        transf.scale(scale, scale)
        self.board_view.setTransform(transf)

    def makeMoveEvent(self, move: chess.Move) -> None:
        # print(f"Chessboy: {move}")
        if move in self.board.legal_moves:
            san = self.board.san(move)
            self.board.push(move)
            self.board_scene.setup_board(self.board)
            eventManager.onMove(move, san)

def get_dark_mode():
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.black)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    return palette

if __name__=="__main__":
    app = QApplication([])
    app.setStyle("Fusion")
    window = MainWindow()
    sys.exit(app.exec())
