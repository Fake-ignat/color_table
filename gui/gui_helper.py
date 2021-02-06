from PyQt5.QtWidgets import (QHBoxLayout,QPushButton, QSizePolicy, QFrame)
from PyQt5 import QtCore


def create_okBox():
    hBox = QHBoxLayout()
    hBox.setAlignment(QtCore.Qt.AlignHCenter)
    for text in ('Ok', 'Cancel'):
        btn = QPushButton(text)
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