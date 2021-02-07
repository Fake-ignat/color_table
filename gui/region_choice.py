import sys
from utils import load_data
from gui.gui_helper import separator, create_ok_cancel_btnBox
from constants import STATION_LIST_DIR_RU as filename
from gui.station_choice import StationChoice
from PyQt5.QtWidgets import (QCheckBox, QHBoxLayout, QVBoxLayout, QPushButton, QWidget, QSizePolicy,
                             QApplication)
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QCloseEvent

class RegionChoice(QWidget):
    closing = pyqtSignal()


    def __init__(self):
        super().__init__()
        self.regions = load_data(filename)
        self.setWindowTitle('Метеостанции РФ: Субъекты')
        self.init_ui()
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
        for region in self.regions.keys():
            vBox.addLayout(self.create_regionBox(region))
            if vBox.count() >= 13:
                layout.addLayout(vBox)
                layout.addWidget(separator('V'))
                vBox = QVBoxLayout()
        layout.addLayout(vBox)
        return layout


    def create_regionBox(self, region):
        hBox = QHBoxLayout()
        hBox.addWidget(QCheckBox())
        btn = QPushButton(region)
        stations = self.regions[region]
        btn.clicked.connect(lambda: self.on_clicked(region, stations))
        btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        hBox.addWidget(btn)
        return hBox

    def closeEvent(self, event: QCloseEvent):
        self.closing.emit()
        return super().closeEvent(event)

    def on_clicked(self, name, stations):
        try:
            self.station_choice = StationChoice(name, stations)
            self.station_choice.closing.connect(self.on_close)
            self.station_choice.show()
            self.hide()
        except Exception as e:
            print(e)

    def on_btn_OK_clicked(self):
        pass

    def on_close(self, d):
        self.show()
        if len(d):
            print(d)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    choice = RegionChoice()
    choice.show()
    sys.exit(app.exec_())
