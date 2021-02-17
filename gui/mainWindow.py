# coding: utf-8
import sys

from PyQt5.QtWidgets import QApplication, QWidget

from gui.foreign_choice import ForeignChoice
from gui.region_choice import RegionChoice
from gui.months_choice import MonthsChoice

from logic.TableLoader import TableLoader
from state.stateholder import StateHolder

from gui.gui_helper import value_from_state, btn_set_click, YearChoiceSpin, WdgtsHBox, WdgtsVBox
from constants import THIS_YEAR, WIDGET_STYLE


class MainWindow(QWidget):

    def __init__(self, desktop):
        super().__init__()

        self.holder = StateHolder()
        self.desktop = desktop
        self.state = self.holder.get_state()

        self.start_year = value_from_state(self.state, 'START_YEAR', 2010)
        self.end_year = value_from_state(self.state, 'END_YEAR', THIS_YEAR)

        self.ru_choice = RegionChoice('РФ', self)
        self.ru_choice.closing.connect(self.on_choice_close)

        self.kz_choice = ForeignChoice("Казахстан", self)
        self.kz_choice.closing.connect(self.on_choice_close)

        self.months_choice = MonthsChoice(self)
        self.months_choice.closing.connect(self.on_choice_close)

        self.init_ui()
        self.setStyleSheet(WIDGET_STYLE)
        self.resize(430, 280)
        self.setWindowTitle("Цветные таблицы")

    def init_ui(self):
        self.start_spin = self.start_year_choice()
        self.end_spin = self.end_year_choice()

        btn_ru_choice = btn_set_click('Метеостанции РФ', lambda x: self.choose(self.ru_choice))
        btn_kz_choice = btn_set_click('Метеостанции РК', lambda x: self.choose(self.kz_choice))
        btn_save = btn_set_click('Сохранить настройки', self.save)
        btn_months_choice = btn_set_click('Выбрать месяца', lambda x: self.choose(self.months_choice))
        btn_load = btn_set_click("Загрузить", self.on_loadBtn_clicked)

        hBox_1 = WdgtsHBox(self.start_spin, self.end_spin)
        hBox_2 = WdgtsHBox(btn_ru_choice, btn_kz_choice, btn_months_choice)
        # hBox_3 = WdgtsHBox(btn_save, btn_load)

        vBox = WdgtsVBox(hBox_1, hBox_2, btn_save, btn_load)

        self.setLayout(vBox)

    def choose(self, choice):
        choice.show()
        self.hide()

    def on_choice_close(self):
        self.show()

    def save(self):
        self.holder.save_state()

    def start_year_choice(self):
        start_spin = YearChoiceSpin(1985, THIS_YEAR, self.start_year,
                                    action=self.on_start_year_change)
        start_spin.setPrefix('C ')
        start_spin.setSuffix(' года')
        return start_spin

    def end_year_choice(self):
        end_spin = YearChoiceSpin(1985, THIS_YEAR, self.end_year,
                                  action=self.on_end_year_change)
        end_spin.setPrefix('по ')
        end_spin.setSuffix(' год')
        return end_spin

    def on_start_year_change(self):
        self.start_year = self.start_spin.value()
        self.valid_years()
        self.state['START_YEAR'] = self.start_year

    def on_end_year_change(self):
        self.end_year = self.end_spin.value()
        self.valid_years()
        self.state['END_YEAR'] = self.end_year

    def valid_years(self):
        if self.start_year > self.end_year:
            self.start_year, self.end_year = self.end_year, self.start_year
            self.start_spin.setValue(self.start_year)
            self.end_spin.setValue(self.end_year)

    def on_loadBtn_clicked(self):
        tl = TableLoader(self.holder)

        station_ids = self.holder.chosen_ids_RU()
        station_ids.extend(self.holder.chosen_ids_FOREIGN('Казахстан'))

        for name, st_id in station_ids:
            tl.load_all(name, st_id)
            tl.save_as_excel(name)





if __name__ == '__main__':
    app = QApplication(sys.argv)
    desktop = QApplication.desktop()
    window = MainWindow(desktop)
    window.show()
    sys.exit(app.exec_())
