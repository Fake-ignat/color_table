from utils import get_regions
from gui.gui_helper import separator, create_okBox
from constants import STATION_LIST_DIR_RU as filename
from PyQt5.QtWidgets import (QCheckBox, QHBoxLayout, QVBoxLayout, QApplication, QWidget, QSizePolicy)

regions = get_regions(filename)
region_name = 'Пензенская область'
region = regions[region_name]

class StationChoice(QWidget):
    def __init__(self, region):
        super().__init__()
        self.region = region
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
        for station, id in self.region.items():
            vBox.addWidget(QCheckBox(station))
            if vBox.count() > 10:
                layout.addLayout(vBox)
                layout.addWidget(separator('V'))
                vBox = QVBoxLayout()
        layout.addLayout(vBox)
        return layout

import sys

app = QApplication(sys.argv)
choice = StationChoice(region)
choice.setWindowTitle(f'Метеостанции {region_name}')
choice.show()
sys.exit(app.exec_())
