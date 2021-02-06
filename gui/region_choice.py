import sys
from utils import get_regions
from gui.gui_helper import separator, create_okBox
from constants import STATION_LIST_DIR_RU as filename
from PyQt5.QtWidgets import (QCheckBox, QHBoxLayout, QVBoxLayout, QPushButton, QWidget, QSizePolicy)

class RegionChoice(QWidget):
    def __init__(self):
        super().__init__()
        self.regions = get_regions(filename)
        self.init_ui()
        self.move(200, 250)

    def init_ui(self):
        layout = QVBoxLayout()

        layout.addLayout(self.create_choiceBox())
        layout.addWidget(separator('H'))
        layout.addLayout(create_okBox())
        self.setLayout(layout)

    def create_choiceBox(self):
        layout = QHBoxLayout()
        vBox = QVBoxLayout()
        for region in self.regions.keys():
            vBox.addLayout(create_regionBox(region))
            if vBox.count() > 10:
                layout.addLayout(vBox)
                layout.addWidget(separator('V'))
                vBox = QVBoxLayout()
        layout.addLayout(vBox)
        return layout


def create_regionBox(region):
    hBox = QHBoxLayout()
    hBox.addWidget(QCheckBox())
    btn = QPushButton(region)
    btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    hBox.addWidget(btn)
    return hBox



