# coding: utf-8
from PyQt5.QtWidgets import (QCheckBox, QHBoxLayout, QPushButton, QSizePolicy)


class MyHBox(QHBoxLayout):
    def __init__(self, parent, region):
        super().__init__()
        self.parent = parent
        self.name = region
        self.stations = parent.regions[region]

        self.checkBox = QCheckBox()
        self.checkBox.setTristate(True)
        self.checkBox.clicked.connect(self.on_cb_clicked)
        self.addWidget(self.checkBox)

        btn = QPushButton(region)
        btn.clicked.connect(lambda:
                            self.parent.on_station_choice_clicked(region, self.stations))
        btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.addWidget(btn)

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