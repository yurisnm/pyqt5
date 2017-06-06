import sys

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QWidget

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.central_widget = QWidget()
        self.cw_layout = QHBoxLayout()
        self.central_widget.setLayout(self.cw_layout)
        self.setCentralWidget(self.central_widget)

        self.line = LineEdit()
        self.kb = KeyBoard()

        self.cw_layout.addWidget(self.line)

        self.create_connections()

    def create_connections(self):
        self.line.signal_evoke_kb.connect(self.show_kb)

    def show_kb(self):
        if self.kb.isHidden():
            self.kb.show()
        else:
            self.kb.hide()


class LineEdit(QLineEdit):

    signal_evoke_kb = pyqtSignal()

    def __init__(self):
        super(LineEdit, self).__init__()

    def mousePressEvent(self, QMouseEvent):
        super(LineEdit, self).mousePressEvent(QMouseEvent)
        self.signal_evoke_kb.emit()

class KeyBoard(QWidget):

    def __init__(self):
        super(KeyBoard, self).__init__()
        self.layout = QHBoxLayout()
        for key in ['q','w','e','r','t','y']:
            self.layout.addWidget(QPushButton(key))
        self.setLayout(self.layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())