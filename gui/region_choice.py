import sys

from logic.utils import load_data
from logic.constants import STATION_LIST_DIR_RU as filename

from gui.gui_helper import separator, create_ok_cancel_btnBox, value_from_state
from gui.myHBox import MyHBox
from gui.station_choice import StationChoice

from PyQt5.QtWidgets import (QHBoxLayout, QVBoxLayout,QWidget, QApplication)
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QCloseEvent
from logic.constants import WIDGET_STYLE

class RegionChoice(QWidget):
    closing = pyqtSignal()

    def __init__(self, name, parent):
        super().__init__()

        self.name = name
        self.parent = parent
        self.state = value_from_state(parent.state, name, {})
        self.regions = load_data(filename)

        self.setWindowTitle('Метеостанции РФ: Субъекты')
        self.init_ui()
        self.setStyleSheet(WIDGET_STYLE)
        self.render_checkBoxes()
        self.move(50, 250)
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
            vBox.addLayout(MyHBox(self, region))
            if vBox.count() >= 10:
                layout.addLayout(vBox)
                layout.addWidget(separator('V'))
                vBox = QVBoxLayout()
        layout.addLayout(vBox)
        return layout

    def closeEvent(self, event: QCloseEvent):
        self.closing.emit()
        return super().closeEvent(event)

    def on_station_choice_clicked(self, name, stations):
        try:
            self.station_choice = StationChoice(name, stations, self)
            self.station_choice.closing.connect(self.on_st_choice_close)
            self.station_choice.show()
            self.hide()
        except Exception as e:
            print(e)

    def on_btn_OK_clicked(self):
        self.modify_parent_state()
        self.close()

    def on_st_choice_close(self):
        self.render_checkBoxes()
        self.show()

    def render_checkBoxes(self):
        for hBoxes in self.findChildren(MyHBox):
            region = hBoxes.name
            if region in self.state:
                isChecked = self.state[region]["isChecked"]
                hBoxes.checkBox.setCheckState(isChecked)
            else:
                hBoxes.checkBox.setCheckState(0)

    def modify_parent_state(self):
        self.parent.state[self.name] = self.state
