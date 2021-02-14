# coding: utf-8
from PyQt5.QtWidgets import (QHBoxLayout, QPushButton, QSizePolicy, QFrame, QSpinBox, QVBoxLayout, QLayout)
from PyQt5 import QtCore


class YearChoiceSpin(QSpinBox):
    def __init__(self, min_val, max_val, init_val, action):
        super().__init__()
        self.setMinimum(min_val)
        self.setMaximum(max_val)

        self.setValue(init_val)
        self.valueChanged.connect(action)


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


def create_ok_cancel_btnBox(ok_action=None, cancel_action=None):
    hBox = QHBoxLayout()
    hBox.setAlignment(QtCore.Qt.AlignHCenter)

    btns = {
        'OK': ok_action,
        'Отмена': cancel_action
    }

    for btn, action in btns.items():
        btn = QPushButton(btn)
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

def btn_set_click(name, action):
    btn = QPushButton(name)
    btn.clicked.connect(action)
    return btn


