import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget

class Dialog(QDialog):

    def __init__(self):
        super(Dialog, self).__init__()

class MainWindow(QMainWindow):

    layout = None
    mw = None
    wid = None
    btn = None

    def __init__(self):
        super(MainWindow, self).__init__()
        self.init_ui()

    def init_ui(self):
        self.setFixedSize(500,500)
        self.layout = QVBoxLayout()
        self.btn = QPushButton("Replace")
        self.btn.clicked.connect(self.replace_widget)
        self.wid = Dialog()
        self.wid.setStyleSheet("background-color: green;")

        self.mw = QWidget()

        self.mw.setLayout(self.layout)
        self.setCentralWidget(self.mw)

        self.layout.addWidget(self.btn)
        self.layout.addWidget(self.wid)

    def replace_widget(self):

        self.layout.removeWidget(self.wid)
        self.wid.close()
        self.wid.hide()
        del self.wid
        self.wid = Dialog()
        self.wid.setStyleSheet("background-color: red;")
        self.layout.addWidget(self.wid)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())