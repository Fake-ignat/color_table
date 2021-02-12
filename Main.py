import sys

from gui.mainWindow import GrandWindow
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)
    desktop = QApplication.desktop()
    window = GrandWindow(desktop)
    window.show()
    sys.exit(app.exec_())
