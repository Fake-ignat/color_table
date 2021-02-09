# coding: utf-8
from PyQt5.QtWidgets import (QHBoxLayout, QPushButton, QSizePolicy, QFrame)
from PyQt5 import QtCore
import ast


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


def copy_dict(origin_dict):
    string_origin = str(origin_dict)
    return ast.literal_eval(string_origin)
