from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QCheckBox

from gui.station_choice import StationChoice
from constants import STATION_LIST_DIR_KZ as filename
from logic.utils import load_data


class ForeignChoice(StationChoice):
    closing = pyqtSignal()

    base_data = load_data(filename)
    limit = 50
    small_col = 12
    big_col = 24

    def __init__(self, name, parent):
        super().__init__(name, self.base_data, parent)

        self.setWindowTitle(f'Метеостанции {self.name}')
        self.move(50, 170)
        desk_width = parent.desktop.width()
        if desk_width > 1920:
            desk_width = desk_width // 2
        self.setFixedWidth(desk_width - 100)
        self.init_ui()

        self.render_checkBoxes()

    def default_state(self):
        return {self.choice_key: {}}

    def update_state(self):
        checkBoxes = self.findChildren(QCheckBox)

        for checkBox in checkBoxes:
            if checkBox.checkState():
                st_name = checkBox.text()
                value = self.base_data[st_name]

                self.state[self.choice_key][st_name] = value

    def modify_parent_state(self):
        self.parent.state[self.name] = self.state
