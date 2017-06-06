import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QPushButton

import random

class Label(QLabel):

    def __init__(self):
        super(Label, self).__init__()

        self.letters = ['q','w','e','r','t','y']

        self.h_layout = QHBoxLayout()
        self.setLayout(self.h_layout)

        self.label = QLabel('Random letters: _')
        self.btn = QPushButton("Roll")
        self.btn.clicked.connect(self.change_label)

        self.h_layout.addWidget(self.label)

        self.h_layout.addWidget(self.btn)

    def change_label(self):
        self.label.setText(random.choice(self.letters))




if __name__=="__main__":
    app = QApplication(sys.argv)
    main_label = Label()
    main_label.show()
    sys.exit(app.exec_())

