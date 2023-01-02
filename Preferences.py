# -------------------------------
# Preferences
# -------------------------------

from collections import OrderedDict
import chess
import chess.engine
from PyQt5.QtWidgets import (QWidget, QDialog, QStackedLayout,
                             QFormLayout, QHBoxLayout, QVBoxLayout,
                             QListWidget, QComboBox, QLineEdit
                            )

class EngineSettings:
    """Defines everything necessary to communicate with an engine"""

    def __init__(self, _name = "", _filepath = "") -> None:
        self.name=_name
        self.filepath=_filepath

    def init_settings(self) -> QWidget:
        engine_settings_window = QWidget()
        engine_settings_layout = QFormLayout()
        engine_settings_window.setLayout(engine_settings_layout)

        self.name_widget = QLineEdit(self.name)
        engine_settings_layout.addRow("&Name:", self.name_widget)
        self.name_widget.textChanged.connect(lambda tx: self.name_widget.setText(tx))

        self.filepath_widget = QLineEdit(self.filepath)
        engine_settings_layout.addRow("&Filepath:", self.filepath_widget)
        self.filepath_widget.textChanged.connect(
            lambda tx: self.filepath_widget.setText(tx))

        return engine_settings_window

class Preferences(QDialog):
    
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.pages = OrderedDict()

        self.engines=[]
        self.engines.append(EngineSettings())
        self.engines[0].name = "Stockfish"
        self.engines[0].filepath = r"H:\Games\Chess\Engines\stockfish_15_win_x64_avx2\stockfish_15_x64_avx2.exe"

        self.load_prefs()
        self.init_dialog()

    def init_dialog(self):
        self.setWindowTitle("ChessBoy Preferences")
        self.setModal(True)
        self.setFixedSize(800, 600)

        self.setLayout(QHBoxLayout())

        # The selection side
        self.selection = QWidget()
        self.selection.setLayout(QVBoxLayout())
        self.selection_list = QListWidget()
        self.selection_list.currentRowChanged.connect(self.change_page)
        self.selection.layout().addWidget(self.selection_list)
        self.layout().addWidget(self.selection)

        # The settings side
        self.settings = QWidget()
        self.settings.setLayout(QStackedLayout())
        self.layout().addWidget(self.settings)

        self.init_pages()
        self.draw_pages()

    def init_pages(self):
        self.pages["Appearance"] = self.init_appearances()
        
        for engine in self.engines:
            self.pages[engine.name] = engine.init_settings()

    def init_appearances(self) -> QWidget:
        self.theme = QComboBox()
        self.theme.addItems(["Bright", "Dark"])

        appearances = QWidget()
        appearances.setLayout(QFormLayout())
        appearances.layout().addRow("&Theme:", self.theme)
        
        return appearances

    def draw_pages(self):
        self.selection_list.clear()
        list_id=0
        for page_name, page_widget in self.pages.items():
            print(f"Adding {page_name}")
            self.selection_list.insertItem(list_id, page_name)
            self.settings.layout().addWidget(page_widget)
            list_id+=1

    def add_settings_page(self, pid: int, widget: QWidget):
        self.selection_list

    def load_prefs(self):
        pass

    def change_page(self, index):
        self.settings.layout().setCurrentIndex(index)


    


