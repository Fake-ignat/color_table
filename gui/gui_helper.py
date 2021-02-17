# coding: utf-8
from PyQt5.QtWidgets import (QHBoxLayout, QPushButton, QSizePolicy, QFrame, QSpinBox,
                             QVBoxLayout, QLayout, QCheckBox)
from PyQt5 import QtCore
from constants import BTN_COLOR, SPIN_COLOR, CHECKED_COLOR, CB_COLOR


class YearChoiceSpin(QSpinBox):
    def __init__(self, min_val, max_val, init_val, action):
        super().__init__()
        self.setMinimum(min_val)
        self.setMaximum(max_val)
        self.setFixedSize(130, 30)

        self.setValue(init_val)
        self.valueChanged.connect(action)


        spin_color= f'background-color: {SPIN_COLOR}; font: bold 12pt/10pt arial;'
        self.setStyleSheet(spin_color)


class WdgtsHBox(QHBoxLayout):
    def __init__(self, *widgets):
        super().__init__()
        self.setAlignment(QtCore.Qt.AlignHCenter)
        for wdgt in widgets:
            self.addLayout(wdgt) \
                if isinstance(wdgt, QLayout) \
                else self.addWidget(wdgt)


class WdgtsVBox(QVBoxLayout):
    def __init__(self, *widgets):
        super().__init__()
        self.setAlignment(QtCore.Qt.AlignVCenter)
        for wdgt in widgets:
            self.addLayout(wdgt) \
                if isinstance(wdgt, QLayout) \
                else self.addWidget(wdgt)


class ChoiceCheckBox(QCheckBox):
    def __init__(self, name):
        super().__init__(name)
        self.setStyleSheet(self.get_style())
        self.stateChanged.connect(self.on_cb_changed)

    def on_cb_changed(self):
        color = CHECKED_COLOR if self.isChecked() else CB_COLOR
        self.setStyleSheet(self.get_style(color))

    def get_style(self, color=CB_COLOR):
        return f'background-color: {color};' \
               f'font: bold 10pt/6pt arial'


def create_ok_cancel_btnBox(ok_action=None, cancel_action=None):
    hBox = QHBoxLayout()
    hBox.setAlignment(QtCore.Qt.AlignHCenter)

    btns = {
        'OK': ok_action,
        'Отмена': cancel_action
    }

    for btn, action in btns.items():
        btn = QPushButton(btn)
        btn.setStyleSheet(f'background-color: {BTN_COLOR};'
                          f' font: bold 10pt/6pt arial')
        if action:
            btn.clicked.connect(action)
        btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        hBox.addWidget(btn)
    return hBox


def separator(orient='V'):
    line = QFrame()
    if orient == 'V':
        line.setFrameStyle(5)
    if orient == 'H':
        line.setFrameStyle(4)
    return line

def value_from_state(state, key, default_value):
    return state[key] \
        if key in state \
        else default_value

def btn_set_click(name, action, color=BTN_COLOR):
    btn = QPushButton(name)
    btn.clicked.connect(action)
    btn.setStyleSheet(f'color: black;'
                      f' background-color: {color};'
                      f'font: bold 10pt/6pt arial')
    return btn


