from copy import deepcopy

from PyQt5.QtWidgets import  QHBoxLayout, QVBoxLayout, QCheckBox

from gui.gui_helper import separator
from gui.station_choice import StationChoice
from logic.constants import STATION_LIST_DIR_KZ as filename
from logic.utils import load_data


class ForeignChoice(StationChoice):

    stations = load_data(filename)

    def __init__(self, name, parent):
        super().__init__(name, self.stations, parent)
        self.name = name
        self.parent = parent
        self.state = parent.state[name] \
            if name in parent.state \
            else deepcopy(self.default_state)

        self.setWindowTitle(f'Метеостанции {self.name}')
        self.move(50, 170)
        self.setFixedWidth(parent.desktop.width()//2 - 100)
        self.init_ui()

        self.render_checkBoxes()

    def create_choiceBox(self):
        layout = QHBoxLayout()
        vBox = QVBoxLayout()

        amount = len(self.stations)
        column_size = 12 if amount <= 50 else 25

        for station, id in self.stations.items():
            vBox.addWidget(QCheckBox(station))
            if vBox.count() >= column_size:
                layout.addLayout(vBox)
                layout.addWidget(separator('V'))
                vBox = QVBoxLayout()
        layout.addLayout(vBox)
        layout.setContentsMargins(0, 0, 0, 0)
        return layout