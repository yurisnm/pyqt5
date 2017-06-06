import random

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QRadioButton


class GameDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        layout = QGridLayout(self)

        lblWBS = QLabel("lblWBS")
        lblDialog = QLabel("lblDialog")
        btnOK = QPushButton("OK")
        layout.addWidget(btnOK, 5, 1)

        optGreen = QRadioButton()
        optYellow = QRadioButton()
        optRed = QRadioButton()
        lblGreen = QLabel("Green")
        lblYellow = QLabel("Yellow")
        lblRed = QLabel("Red")

        layout.addWidget(lblWBS, 0, 1)
        layout.addWidget(lblDialog, 1, 1)

        l = [optGreen, lblGreen, optYellow, lblYellow, optRed, lblRed]

        def randomOptions():

            for w in l:
                layout.removeWidget(w)

            rdmOpt = [2,3,4]
            random.shuffle(rdmOpt)

            for i in range(len(l)):
                layout.addWidget(l[i], rdmOpt[i//2], i % 2)

        randomOptions()
        btnOK.clicked.connect(randomOptions)
        self.setWindowTitle("PALCDMS")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gd = GameDialog()
    gd.show()
    sys.exit(app.exec_())