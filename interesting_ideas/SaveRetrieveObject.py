import pickle

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.central_widget = QWidget()
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

        self.widget = Widget()


        self.btn_save = QPushButton("Save")
        self.btn_save.clicked.connect(self.save)
        self.btn_load = QPushButton("Load")
        self.btn_load.clicked.connect(self.load)

        self.layout.addWidget(self.widget)
        self.layout.addWidget(self.btn_save)
        self.layout.addWidget(self.btn_load)

    def save(self):
        with open("data.dat", 'wb') as f_out:
            pickle.dump(self.widget, f_out, protocol=pickle.HIGHEST_PROTOCOL)

    def load(self):
        with open('data.dat', 'rb') as f_in:
            widget = pickle.load(f_in)
            self.widget.name_line.setText(widget.name)


class Widget(QWidget):


    def __init__(self):
        super(Widget, self).__init__()
        self.name_line = QLineEdit()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.name_line)
        self.name_line.textChanged.connect(self.set_name)
        self.name = "default"
        self.name_line.setText(self.name)

    def set_name(self, name):
        self.name = name

    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, state):
        self.__dict__ = state


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())

