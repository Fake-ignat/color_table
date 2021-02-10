# coding: utf-8
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QApplication, QPushButton, QWidget

from gui.region_choice import RegionChoice
from state.state_holder import State_Holder


class GrandWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.holder = State_Holder()
        self.state = self.holder.get_state()

        self.ru_choice = RegionChoice('РФ', self)
        self.ru_choice.closing.connect(self.on_region_close)

        self.init_ui()
        self.resize(430, 280)
        self.setWindowTitle("Цветные таблицы")

    def init_ui(self):
        btn_ru_choice = QPushButton('Выбрать метеостанции РФ')
        btn_ru_choice.clicked.connect(self.choose_region_ru)

        btn_save = QPushButton('Save')
        btn_save.clicked.connect(self.save)

        hBox = QHBoxLayout()
        hBox.setAlignment(Qt.AlignHCenter)
        hBox.addWidget(btn_ru_choice)
        hBox.addWidget(btn_save)

        self.setLayout(hBox)

    def choose_region_ru(self):
            self.ru_choice.show()
            self.hide()

    def on_region_close(self):
        self.show()

    def save(self):
        self.holder.save_state()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GrandWindow()
    window.show()
    sys.exit(app.exec_())
