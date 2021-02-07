# coding: utf-8
import sys
from PyQt5.QtWidgets import QHBoxLayout, QApplication, QPushButton, QWidget
from PyQt5.QtCore import Qt
from state.state_holder import State_Holder
from gui.region_choice import RegionChoice


class GrandWindow(QWidget):
    state_holder = State_Holder

    def __init__(self):
        super().__init__()

        self.ru_choice = RegionChoice()
        self.ru_choice.closing.connect(self.on_close)

        self.init_ui()
        self.resize(430, 280)
        self.setWindowTitle("Цветные таблицы")

    def init_ui(self):
        btn_ru_choice = QPushButton('Выбрать метеостанции РФ')
        btn_ru_choice.clicked.connect(self.choose_station_ru)

        hBox = QHBoxLayout()
        hBox.setAlignment(Qt.AlignHCenter)
        hBox.addWidget(btn_ru_choice)

        self.setLayout(hBox)

    def choose_station_ru(self):
        try:
            self.ru_choice.show()
            self.hide()
        except Exception as e:
            print(e)

    def on_close(self):
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GrandWindow()
    window.show()
    sys.exit(app.exec_())
