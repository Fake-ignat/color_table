from gui.gui_helper import separator, create_ok_cancel_btnBox, value_from_state, ChoiceCheckBox
from PyQt5.QtWidgets import (QCheckBox, QHBoxLayout, QVBoxLayout, QWidget)
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtCore import pyqtSignal
from constants import WIDGET_STYLE
from copy import deepcopy


class StationChoice(QWidget):
    closing = pyqtSignal()

    limit = 50
    small_col = 12
    big_col = 25

    def __init__(self, name, base_data, parent, choice_key='stations'):
        super().__init__()
        self.parent = parent
        self.name = name
        self.base_data = base_data
        self.choice_key = choice_key

        self.state = value_from_state(
            state=parent.state,
            key=name,
            default_value=deepcopy(self.default_state()))

        self.init_ui()
        self.setStyleSheet(WIDGET_STYLE)
        self.render_checkBoxes()

        self.setWindowTitle(f'Метеостанции {self.name}')
        self.setMinimumWidth(470)
        self.move(200, 250)

    def init_ui(self):
        layout = QVBoxLayout()
        layout.addLayout(self.create_choiceBox())
        layout.addWidget(separator('H'))
        layout.addLayout(create_ok_cancel_btnBox(self.on_btn_OK_clicked, self.close))
        self.setLayout(layout)

    def create_choiceBox(self):
        layout = QHBoxLayout()
        vBox = QVBoxLayout()

        amount = len(self.base_data)
        column_size = self.small_col if amount <= self.limit else self.big_col
        try:
            for station, id in self.base_data.items():
                checkBox = ChoiceCheckBox(station)
                vBox.addWidget(checkBox)
                if vBox.count() >= column_size:
                    layout.addLayout(vBox)
                    layout.addWidget(separator('V'))
                    vBox = QVBoxLayout()
        except Exception as e:
            print(e)
        layout.addLayout(vBox)
        return layout

    def closeEvent(self, event: QCloseEvent):
        try:
            self.modify_parent_state()
            self.closing.emit()
            return super().closeEvent(event)
        except Exception as e:
            print("Station closeEvent",e)

    def on_btn_OK_clicked(self):
        self.clear_state()
        self.update_state()
        self.close()

    def default_state(self):
        return {self.choice_key: {}, "isChecked": 0}

    def clear_state(self):
        self.state = deepcopy(self.default_state())

    def render_checkBoxes(self):
        for checkBox in self.findChildren(QCheckBox):
            name = checkBox.text()
            if name in self.state[self.choice_key]:
                checkBox.setChecked(True)
            else:
                checkBox.setChecked(False)

    def update_state(self):
        checkBoxes = self.findChildren(QCheckBox)
        full_size = len(checkBoxes)

        for checkBox in checkBoxes:
            if checkBox.checkState():
                st_name = checkBox.text()
                value = self.base_data[st_name]

                self.state[self.choice_key][st_name] = value

            now_size = len(self.state[self.choice_key])
            if now_size:
                self.state['isChecked'] = 2 if full_size == now_size else 1

    def modify_parent_state(self):
        if self.state['isChecked']:
            self.parent.state[self.name] = self.state
        else:
            if self.name in self.parent.state:
                self.parent.state.pop(self.name)
