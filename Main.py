import sys

from gui.mainWindow import MainWindow
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)
    desktop = QApplication.desktop()
    window = MainWindow(desktop)
    window.show()
    sys.exit(app.exec_())
