from PyQt5.QtCore import QSize
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QWidget

from charts.complete_charts.EChart import EChart


class TopBar(QWidget):

    btn_chart_line = None
    btn_chart_pie = None
    btn_chart_bar = None

    btn_close = None
    btn_confirm = None

    size_buttons = None

    signal_send_chart_selected = pyqtSignal(int)

    def __init__(self, parent):
        super(TopBar, self).__init__()
        self.setParent(parent)
        self.init_ui()

    def init_ui(self):

        self.__path = "resources/icons/assets_browser/"

        self.kb_active = True

        self.btn_chart_line = QPushButton("L")
        self.btn_chart_pie = QPushButton("P")
        self.btn_chart_bar = QPushButton("B")
        self.btn_kb = QPushButton()
        self.btn_close = QPushButton("x")
        self.btn_confirm = QPushButton("√")
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0,5,0,5)

        self.layout.setSpacing(2)



        self.style_buttons_off = """
            border-radius: 2px;
            background:rgb(37,43,52,220);
            color:white;
        """
        self.style_buttons_on = """
                    border-radius: 2px;
                    background: rgb(0,187,255);
                """
        self.size_buttons = 40

        self.btn_chart_line.setFixedSize(self.size_buttons, self.size_buttons)
        self.btn_chart_pie.setFixedSize(self.size_buttons, self.size_buttons)
        self.btn_chart_bar.setFixedSize(self.size_buttons, self.size_buttons)
        self.btn_kb.setFixedSize(self.size_buttons,self.size_buttons)
        self.btn_close.setFixedSize(20,20)
        self.btn_confirm.setFixedSize(20, 20)

        self.btn_chart_line.setStyleSheet(self.style_buttons_off)
        self.btn_chart_pie.setStyleSheet(self.style_buttons_off)
        self.btn_chart_bar.setStyleSheet(self.style_buttons_off)
        self.btn_kb.setStyleSheet(self.style_buttons_on)
        self.btn_close.setStyleSheet("""
            border-radius: 10px;
            background-color: red;
            color: white;
        """)
        self.btn_confirm.setStyleSheet("""
            border-radius: 10px;
            background-color: green;
            color: white;
        """)

        self.layout.addWidget(self.btn_chart_line)
        self.layout.addWidget(self.btn_chart_pie)
        # self.layout.addWidget(self.btn_chart_bar)
        self.layout.addStretch(-1)
        self.layout.addWidget(self.btn_kb)
        self.layout.addSpacing(5)
        self.layout.addWidget(self.btn_confirm)
        self.layout.addSpacing(5)
        self.layout.addWidget(self.btn_close)

        self.btn_chart_line.clicked.connect(self.btn_chart_line_clicked)
        self.btn_chart_pie.clicked.connect(self.btn_chart_pie_clicked)
        self.btn_chart_bar.clicked.connect(self.btn_chart_bar_clicked)
        self.btn_kb.clicked.connect(self.btn_kb_clicked)
        self.kb_icon = QIcon(self.__path + "ic_keyboard.png")
        self.btn_kb.setIcon(self.kb_icon)
        self.btn_kb.setIconSize(QSize(self.size_buttons, self.size_buttons))
        self.btn_confirm.clicked.connect(self.parent().confirm_chart)
        self.btn_close.clicked.connect(self.parent().hide)

        self.setStyleSheet("background: red;")


    def clear_all_button_selections(self):
        self.btn_chart_line.setStyleSheet(self.style_buttons_off)
        self.btn_chart_pie.setStyleSheet(self.style_buttons_off)
        self.btn_chart_bar.setStyleSheet(self.style_buttons_off)

    def btn_chart_line_clicked(self):
        self.clear_all_button_selections()
        self.btn_chart_line.setStyleSheet(self.style_buttons_on)
        self.signal_send_chart_selected.emit(EChart.LINE)

    def btn_chart_pie_clicked(self):
        self.clear_all_button_selections()
        self.btn_chart_pie.setStyleSheet(self.style_buttons_on)
        self.signal_send_chart_selected.emit(EChart.PIE)

    def btn_chart_bar_clicked(self):
        self.clear_all_button_selections()
        self.btn_chart_bar.setStyleSheet(self.style_buttons_on)
        self.signal_send_chart_selected.emit(EChart.BAR)

    def btn_kb_clicked(self):
        if not self.kb_active:
            self.btn_kb.setStyleSheet(self.style_buttons_on)
            self.kb_active = True
        else:
            self.btn_kb.setStyleSheet(self.style_buttons_off)
            # KEYBOARD.close()
            self.kb_active = False