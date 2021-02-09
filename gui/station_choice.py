from gui.gui_helper import separator, create_ok_cancel_btnBox, copy_dict
from PyQt5.QtWidgets import (QCheckBox, QHBoxLayout, QVBoxLayout, QWidget)
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtCore import pyqtSignal


class StationChoice(QWidget):
    closing = pyqtSignal()
    default_state = {"stations": {}, "isChecked": 0}

    def __init__(self, name, stations, parent):
        super().__init__()
        self.parent = parent
        self.name = name
        self.stations = stations
        self.state = parent.state[name] \
            if name in parent.state \
            else copy_dict(self.default_state)

        self.init_ui()
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

        amount = len(self.stations)
        column_size = 5 if amount <= 50 else 10

        for station, id in self.stations.items():
            vBox.addWidget(QCheckBox(station))
            if vBox.count() >= column_size:
                layout.addLayout(vBox)
                layout.addWidget(separator('V'))
                vBox = QVBoxLayout()
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

    def clear_state(self):
        self.state = copy_dict(self.default_state)

    def render_checkBoxes(self):
        for checkBox in self.findChildren(QCheckBox):
            name = checkBox.text()
            if name in self.state['stations']:
                checkBox.setChecked(True)
            else:
                checkBox.setChecked(False)

    def update_state(self):
        checkBoxes = self.findChildren(QCheckBox)
        full_size = len(checkBoxes)

        for checkBox in checkBoxes:
            if checkBox.checkState():
                st_name = checkBox.text()
                id = self.stations[st_name]

                self.state['stations'][st_name] = id

            now_size = len(self.state['stations'])
            if now_size:
                self.state['isChecked'] = 2 if full_size == now_size else 1

    def modify_parent_state(self):
        if self.state['isChecked']:
            self.parent.state[self.name] = self.state
        else:
            if self.name in self.parent.state:
                self.parent.state.pop(self.name)



import sys

# app = QApplication(sys.argv)
# choice = StationChoice(region, stations)
# choice.show()
# sys.exit(app.exec_())
