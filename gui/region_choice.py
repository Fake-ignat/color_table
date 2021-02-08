import sys

from utils import load_data
from constants import STATION_LIST_DIR_RU as filename

from gui.gui_helper import separator, create_ok_cancel_btnBox
from gui.myHBox import MyHBox
from gui.station_choice import StationChoice

from PyQt5.QtWidgets import (QHBoxLayout, QVBoxLayout,QWidget, QApplication)
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QCloseEvent

class RegionChoice(QWidget):
    closing = pyqtSignal()

    def __init__(self, state):
        super().__init__()
        self.state = state
        self.setWindowTitle('Метеостанции РФ: Субъекты')
        self.regions = load_data(filename)
        self.init_ui()
        self.render_checkBoxes()
        self.move(200, 250)
        self.station_choice = None

    def init_ui(self):
        layout = QVBoxLayout()
        layout.addLayout(self.create_choiceBox())
        layout.addWidget(separator('H'))
        layout.addLayout(create_ok_cancel_btnBox(self.on_btn_OK_clicked, self.close))
        self.setLayout(layout)

    def create_choiceBox(self):
        layout = QHBoxLayout()
        vBox = QVBoxLayout()
        for region in self.regions:
            st_state = self.state[region] \
                if region in self.state \
                else dict(stations={}, isChecked=0)
            vBox.addLayout(MyHBox(self, region, st_state))
            if vBox.count() >= 13:
                layout.addLayout(vBox)
                layout.addWidget(separator('V'))
                vBox = QVBoxLayout()
        layout.addLayout(vBox)
        return layout

    def closeEvent(self, event: QCloseEvent):
        self.closing.emit()
        return super().closeEvent(event)

    def on_clicked(self, name, stations, small_state):
        try:
            self.station_choice = StationChoice(name, stations, small_state)
            self.station_choice.closing.connect(self.on_close)
            self.station_choice.show()
            self.hide()
        except Exception as e:
            print(e)

    def on_btn_OK_clicked(self):
        pass

    def on_close(self, data):
        self.show()
        try:
            self.update_state(data)
        except Exception as e:
            print(e)

    def update_state(self, new_data):
        for name, v in new_data.items():
            if v["isChecked"]:
                self.state = {**self.state, **new_data}
            else:
                self.state.pop(name)


        self.render_checkBoxes()

    def render_checkBoxes(self):
        for hBoxes in self.findChildren(MyHBox):
            region = hBoxes.name
            if region in self.state:
                isChecked = self.state[region]["isChecked"]
                hBoxes.checkBox.setCheckState(isChecked)
            else:
                hBoxes.checkBox.setCheckState(0)

test_state = {
    'Смоленская область': dict(stations={
        'Гагарин': '27507',
        'Рославль': '26882',
        'Рудня': '26675',
        'Смоленск': '26781'},
        isChecked=1),
    'Мордовия': dict(stations={
        'Саранск': '27760',
        'Темников': '27752',
        'Торбеево': '27758'},
        isChecked=1)}

if __name__ == '__main__':
    app = QApplication(sys.argv)
    choice = RegionChoice(test_state)
    choice.show()
    sys.exit(app.exec_())
