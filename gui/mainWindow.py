# coding: utf-8
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QApplication, QPushButton, QWidget, QVBoxLayout

from gui.region_choice import RegionChoice
from logic.TableLoader import TableLoader
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

        btn_save = QPushButton('Сохранить\nсписок станций RU')
        btn_save.clicked.connect(self.save)

        btn_load = QPushButton("Загрузить")
        btn_load.clicked.connect(self.on_loadBtn_clicked)

        hBox = QHBoxLayout()
        hBox.setAlignment(Qt.AlignHCenter)

        hBox_1 = QHBoxLayout()
        hBox_1.setAlignment(Qt.AlignHCenter)
        hBox_1.addWidget(btn_ru_choice)
        hBox_1.addWidget(btn_save)

        vBox = QVBoxLayout()
        vBox.setAlignment(Qt.AlignVCenter)
        vBox.addLayout(hBox_1)
        vBox.addWidget(btn_load)

        self.setLayout(vBox)

    def choose_region_ru(self):
        self.ru_choice.show()
        self.hide()

    def on_region_close(self):
        self.show()

    def save(self):
        self.holder.save_state()

    def on_loadBtn_clicked(self):
        tl = TableLoader()
        for name, st_id in self.holder.chosen_ids_RU():
            tl.load_all(name, st_id)
            tl.save_as_excel(name)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GrandWindow()
    window.show()
    sys.exit(app.exec_())
