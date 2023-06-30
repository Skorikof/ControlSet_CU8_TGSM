import sys
from model import Model
from view import AppWindow
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon


def main():
    app = QApplication(sys.argv)
    m = Model()
    win = AppWindow(m)
    # win.setWindowIcon(QIcon('icon.png')
    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
