from PyQt5.QtWidgets import QCheckBox

from gui.station_choice import StationChoice
from logic.utils import load_data


class MonthsChoice(StationChoice):
    months = {'ЯНВАРЬ': 1, 'ФЕВРАЛЬ': 2, 'МАРТ': 3, 'АПРЕЛЬ': 4, 'МАЙ': 5, 'ИЮНЬ': 6,
              'ИЮЛЬ': 7, 'АВГУСТ': 8, 'СЕНТЯБРЬ': 9, 'ОКТЯБРЬ': 10, 'НОЯБРЬ': 11, 'ДЕКАБРЬ': 12}

    limit = 12
    small_col = 6
    big_col = 10

    def __init__(self, parent):
        super().__init__("Месяца", self.months, parent, 'month_names')

        self.setWindowTitle(f'Выбор месяца')
        self.move(50, 170)
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