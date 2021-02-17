# coding: utf-8
from PyQt5.QtWidgets import (QCheckBox, QHBoxLayout, QPushButton, QSizePolicy)
from constants import BTN_COLOR, CHECKED_COLOR

class MyHBox(QHBoxLayout):
    def __init__(self, parent, region):
        super().__init__()
        self.parent = parent
        self.name = region
        self.stations = parent.regions[region]

        self.checkBox = QCheckBox()
        self.checkBox.setTristate(True)
        self.checkBox.clicked.connect(self.on_cb_clicked)
        self.checkBox.stateChanged.connect(self.on_cb_changed)
        self.addWidget(self.checkBox)

        self.btn = QPushButton(region)
        self.btn.setStyleSheet(f'background-color: {BTN_COLOR}; font: bold 10pt/6pt arial')
        self.btn.clicked.connect(lambda:
                            self.parent.on_station_choice_clicked(region, self.stations))
        self.btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.addWidget(self.btn)

    def on_cb_clicked(self):
        if self.checkBox.checkState():
            self.checkBox.setCheckState(2)
            self.check_all()

        else:
            self.uncheck_all()

    def check_all(self):
        self.parent.state[self.name] = {
            "stations": self.stations,
            "isChecked": 2
        }

    def uncheck_all(self):
        self.parent.state.pop(self.name)

    def on_cb_changed(self):
        color = CHECKED_COLOR if self.checkBox.isChecked() else BTN_COLOR
        self.btn.setStyleSheet(f'background-color: {color}; '
                               f'font: bold 10pt/6pt arial')
