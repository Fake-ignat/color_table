from PyQt5.QtWidgets import (QCheckBox, QHBoxLayout, QPushButton, QSizePolicy)

class MyHBox(QHBoxLayout):
    def __init__(self, parent, region, station_state):
        super().__init__()
        self.name = region
        self.checkBox = QCheckBox()
        self.checkBox.setTristate(True)
        self.addWidget(self.checkBox)
        btn = QPushButton(region)
        stations = parent.regions[region]
        btn.clicked.connect(lambda: parent.on_clicked(region, stations, station_state))
        btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.addWidget(btn)