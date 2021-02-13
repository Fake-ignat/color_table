# coding: utf-8
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QApplication, QPushButton, QWidget, QVBoxLayout

from gui.foreign_choice import ForeignChoice
from gui.region_choice import RegionChoice
from gui.months_choice import MonthsChoice

from logic.TableLoader import TableLoader
from state.state_holder import State_Holder


class GrandWindow(QWidget):

    def __init__(self, desktop):
        super().__init__()

        self.holder = State_Holder()
        self.desktop = desktop
        self.state = self.holder.get_state()

        self.ru_choice = RegionChoice('РФ', self)
        self.ru_choice.closing.connect(self.on_choice_close)

        self.kz_choice = ForeignChoice("Казахстан", self)
        self.kz_choice.closing.connect(self.on_choice_close)

        self.months_choice = MonthsChoice(self)
        self.months_choice.closing.connect(self.on_choice_close)

        self.init_ui()
        self.resize(430, 280)
        self.setWindowTitle("Цветные таблицы")

    def init_ui(self):
        btn_ru_choice = QPushButton('Метеостанции РФ')
        btn_ru_choice.clicked.connect(lambda x: self.choose(self.ru_choice))

        btn_kz_choice = QPushButton('Метеостанции РК')
        btn_kz_choice.clicked.connect(lambda x: self.choose(self.kz_choice))

        btn_save = QPushButton('Сохранить настройки')
        btn_save.clicked.connect(self.save)

        btn_months_choice = QPushButton('Выбрать месяца')
        btn_months_choice.clicked.connect(lambda x: self.choose(self.months_choice))

        btn_load = QPushButton("Загрузить")
        btn_load.clicked.connect(self.on_loadBtn_clicked)

        hBox = QHBoxLayout()
        hBox.setAlignment(Qt.AlignHCenter)

        hBox_1 = QHBoxLayout()
        hBox_1.setAlignment(Qt.AlignHCenter)
        hBox_1.addWidget(btn_ru_choice)
        hBox_1.addWidget(btn_kz_choice)
        hBox_1.addWidget(btn_months_choice)

        hBox_2 = QHBoxLayout()
        hBox_2.setAlignment(Qt.AlignHCenter)
        hBox_2.addWidget(btn_save)
        hBox_2.addWidget(btn_load)

        vBox = QVBoxLayout()
        vBox.setAlignment(Qt.AlignVCenter)
        vBox.addLayout(hBox_1)
        vBox.addLayout(hBox_2)

        self.setLayout(vBox)

    def choose(self, choice):
        choice.show()
        self.hide()

    def on_choice_close(self):
        self.show()

    def save(self):
        self.holder.save_state()

    def on_loadBtn_clicked(self):
        tl = TableLoader(self.holder)
        for name, st_id in self.holder.chosen_ids_RU():
            tl.load_all(name, st_id)
            tl.save_as_excel(name)
        for name, st_id in self.holder.chosen_ids_FOREIGN('Казахстан'):
            tl.load_all(name, st_id)
            tl.save_as_excel(name)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    desktop = QApplication.desktop()
    window = GrandWindow(desktop)
    window.show()
    sys.exit(app.exec_())
