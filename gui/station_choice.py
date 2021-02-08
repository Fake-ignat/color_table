from gui.gui_helper import separator, create_ok_cancel_btnBox, pretty
from PyQt5.QtWidgets import (QCheckBox, QHBoxLayout, QVBoxLayout, QWidget)
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtCore import pyqtSignal


class StationChoice(QWidget):
    closing = pyqtSignal(dict)

    def __init__(self, name, stations, state):
        super().__init__()
        self.name = name
        self.stations = stations
        self.state = state

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
            self.closing.emit(self.send_state())
            return super().closeEvent(event)
        except Exception as e:
            print("Station closeEvent",e)

    def on_btn_OK_clicked(self):
        self.update_state()

    def clear_state(self):
        self.state = {
            "stations": {},
            "isChecked": 0
        }

    def render_checkBoxes(self):
        for checkBox in self.findChildren(QCheckBox):
            name = checkBox.text()
            if name in self.state['stations']:
                checkBox.setChecked(True)
            else:
                checkBox.setChecked(False)

    def update_state(self):
        self.clear_state()

        checkboxes = self.findChildren(QCheckBox)
        full_size = len(checkboxes)

        for checkBox in checkboxes:
            if checkBox.checkState():
                name = checkBox.text()
                id = self.stations[name]

                self.state['stations'][name] = id

            now_size = len(self.state['stations'])
            if now_size:
                self.state['isChecked'] = 2 if full_size == now_size else 1

    def send_state(self):
            return {self.name: self.state}



import sys

# app = QApplication(sys.argv)
# choice = StationChoice(region, stations)
# choice.show()
# sys.exit(app.exec_())
