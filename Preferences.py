# -------------------------------
# Preferences
# -------------------------------

import os, json
from dataclasses import dataclass, asdict
from collections import OrderedDict
import chess
import chess.engine
from PyQt5.QtWidgets import (QWidget, QDialog, QStackedLayout,
                             QFormLayout, QHBoxLayout, QVBoxLayout,
                             QListWidget, QComboBox, QLineEdit, QLabel,
                             QGroupBox, QPushButton, QAbstractItemView,
                             QMessageBox
                            )

@dataclass(order=True)
class EngineDef:
    """Defines everything necessary to communicate with an engine"""
    name: str
    filepath: str

    def init_settings_gui(self) -> QWidget:
        engine_settings_window = QWidget()
        engine_settings_layout = QFormLayout()
        engine_settings_window.setLayout(engine_settings_layout)

        name_widget = QLineEdit(self.name)
        engine_settings_layout.addRow("&Name:", name_widget)
        name_widget.textChanged.connect(
            lambda tx: name_widget.setText(tx))

        filepath_widget = QLineEdit(self.filepath)
        engine_settings_layout.addRow("&Filepath:", filepath_widget)
        filepath_widget.textChanged.connect(
            lambda tx: filepath_widget.setText(tx))

        return engine_settings_window

class EnginesSettings:

    def __init__(self, *args, **kwargs):
        self.engine_defs = []
        self.DEBUG_add_stockfish()

    def store_settings(self, filepath):
        settings = dict()
        settings["engines"] = dict()
        for engine in self.engine_defs:
            settings["engines"][engine.name] = asdict(engine)
        with open(filepath, "w") as settingsfile:
            json.dump(settings, settingsfile, indent=2)
    
    def restore_settings(self, filepath):
        if not os.path.exists(filepath):
            return
        with open(filepath) as settingsfile:
            settings = json.read(settingsfile)
        for enginedata in settings["engines"]:
            self.engine_defs.append(EngineDef(**enginedata))

    def DEBUG_add_stockfish(self):
        name = "Stockfish"
        filepath = r"H:\Games\Chess\Engines\stockfish_15_win_x64_avx2\stockfish_15_x64_avx2.exe"
        stockfish = EngineDef(name, filepath)
        self.engine_defs.append(stockfish)

    def init_settings_gui(self) -> QWidget:
        engine_settings_window = QWidget()

        engine_settings_layout = QFormLayout()
        engine_settings_window.setLayout(engine_settings_layout)

        engines_group = QGroupBox("Engines")
        engines_group_layout = QVBoxLayout()
        engines_group.setLayout(engines_group_layout)

        self.engine_list = QListWidget()
        self.engine_list.setSelectionMode(QAbstractItemView.SingleSelection)
        self.engine_list.addItems( [ engine.name for engine in self.engine_defs] )
        engines_group_layout.addWidget(self.engine_list)

        buttons_row = QWidget()
        buttons_row_layout = QHBoxLayout()
        buttons_row.setLayout(buttons_row_layout)
        bAdd = QPushButton("Add Engine")
        bAdd.released.connect(self.add_engine)
        buttons_row_layout.addWidget(bAdd)
        bRemove = QPushButton("Remove Engine")
        bRemove.released.connect(self.remove_engine)
        buttons_row_layout.addWidget(bRemove)

        engines_group_layout.addWidget(buttons_row)
        engine_settings_layout.addWidget(engines_group)

        return engine_settings_window
    
    def add_engine(self):
        print(self.engine_list.selectedItems())
    
    def remove_engine(self):
        if self.engine_list.selectedItems() == []:
            print("None selected")
            return
        msgBox = QMessageBox()
        msgBox.setText("This engine entry will be deleted.")
        msgBox.setInformativeText("Are you sure?")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msgBox.setDefaultButton(QMessageBox.Save)
        msgBox.setIcon(QMessageBox.Warning)
        if msgBox.exec_() != QMessageBox.Ok:
            return
        engine_name = self.engine_list.selectedItems()[0]
        print(f"Removing Engine {engine_name}")
        

class Preferences(QDialog):
    
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.pages = OrderedDict()
        self.engine_settings = EnginesSettings()

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
        
        self.pages["Engines"] = self.engine_settings.init_settings_gui()

        for engine in self.engine_settings.engine_defs:
            self.pages["  "+engine.name] = engine.init_settings_gui()

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
        self.engine_settings.restore_settings("settings/engines.json")

    def change_page(self, index):
        self.settings.layout().setCurrentIndex(index)
