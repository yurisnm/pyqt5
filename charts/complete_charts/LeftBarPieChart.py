from PyQt5.QtChart import QChart
from PyQt5.QtChart import QPieSeries
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget



class LeftBarPieChart(QWidget):



    def __init__(self, parent):
        super(LeftBarPieChart, self).__init__()
        self.parent = parent
        self.setParent(parent)

        self.chart = None
        self.inputs = []
        self.layout = None
        self.layout_inp = None
        self.btn_add = None
        self.w_inp = None
        self.header = None

        self.init_ui()

    def init_ui(self):


        self.chart = QChart()
        self.chart.setTheme(QChart.ChartThemeBlueIcy)
        self.chart.setAnimationDuration(1000)
        self.chart.setAnimationOptions(QChart.AllAnimations)
        self.serie = QPieSeries()

        self.layout = QVBoxLayout()
        self.layout_inp = QVBoxLayout()
        self.w_inp = QWidget()
        self.w_inp.setStyleSheet("""
            .QWidget{
                background-color: transparent;
            }
        """)

        self.w_inp.setLayout(self.layout_inp)

        self.setLayout(self.layout)
        self.inputs.append(InputPieChart(self))

        self.btn_add = QPushButton("+")
        self.btn_remove = QPushButton("-")
        self.btn_add.clicked.connect(self.add_input)
        self.btn_remove.clicked.connect(self.remove_input)
        self.btn_add.setStyleSheet("""
            border: 0px;
            background: green;
            color: white;
        """)
        self.btn_remove.setStyleSheet("""
            border: 0px;
            background: red;
            color: white;
        """)
        self.header = HeaderPieChartInput()
        self.layout.addWidget(self.header)
        self.layout.addWidget(self.w_inp)
        self.layout.addStretch(-1)
        self.layout.addWidget(self.btn_remove)
        self.layout.addWidget(self.btn_add)
        self.layout_inp.addWidget(self.inputs[0])


        self.serie.append(self.inputs[0].name.text(),2)

        # self.slice.setExploded()
        # self.slice.setLabelVisible()
        # self.slice.setPen(QPen(Qt.darkGreen,2))
        # self.slice.setBrush(Qt.green)

        self.chart.addSeries(self.serie)
        self.chart.setTitle("Pie Chart")

    def add_input(self):
        if len(self.inputs)<10:
            self.inputs.append(InputPieChart(self))
            self.layout_inp.addWidget(self.inputs[-1])
            self.serie.append(self.inputs[-1].name.text(),
                              int(self.inputs[-1].value.text()))
            # for slice in self.serie.slices():
            #     slice.setBrush(Qt.green)

    def remove_input(self):
        if len(self.inputs)>=1:
            self.layout_inp.removeWidget(self.inputs[-1])
            self.inputs[-1].hide()
            self.inputs.remove(self.inputs[-1])
            self.slc = self.serie.slices()[-1]
            self.serie.remove(self.slc)

            # for slice in self.serie.slices():
            #     slice.setBrush(Qt.green)

    def input_changed(self, txt):
        if self.serie in self.chart.series():
            self.chart.removeSeries(self.serie)
            self.serie = QPieSeries()
            for inp in self.inputs:
                self.serie.append(inp.name.text(), int(inp.value.text()))
            self.chart.addSeries(self.serie)


class HeaderPieChartInput(QWidget):

    lbl_name = None
    lbl_value = None
    layout = None

    def __init__(self):
        super(HeaderPieChartInput, self).__init__()
        self.init_ui()

    def init_ui(self):
        stly = """
            color: white;
        """
        self.lbl_name = QLabel("Nome")
        self.lbl_name.setStyleSheet(stly)
        self.lbl_value = QLabel("Valor")
        self.lbl_value.setStyleSheet(stly)

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.lbl_name)
        self.layout.addStretch(-1)
        self.layout.addWidget(self.lbl_value)
        self.setLayout(self.layout)



class InputPieChart(QWidget):

    layout = None
    name = None
    value = None

    signal_send_name = pyqtSignal(str)
    signal_send_value = pyqtSignal(str)

    def __init__(self, parent):
        super(InputPieChart, self).__init__()
        self.parent = parent
        self.setParent(parent)
        self.init_ui()

    def init_ui(self):
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.name = NameValueInput(self.parent)
        self.name.textChanged.connect(self.parent.input_changed)
        self.name.setText("Novo")
        self.value = NameValueInput(self.parent)
        self.value.textChanged.connect(self.keep_valid)
        self.value.textChanged.connect(self.parent.input_changed)
        self.value.setText('0')
        self.value.setInputMask('9999999')
        self.value.setCursorPosition(0)
        self.layout.addWidget(self.name)
        self.layout.addWidget(self.value)
        self.setLayout(self.layout)

    def keep_valid(self,txt):
        if txt == "":
            self.value.setText("0")
            self.value.setCursorPosition(0)

class NameValueInput(QLineEdit):

    def __init__(self, parent):
        super(NameValueInput, self).__init__()
        self.parent = parent

    def mousePressEvent(self, QMouseEvent):
        super(NameValueInput, self).mousePressEvent(QMouseEvent)
        if self.parent.parent.w_type_charts.kb_active:
            pass
            # KEYBOARD.close()
            # KEYBOARD.open()
            # KEYBOARD.set_receiver(self)

    def mouseDoubleClickEvent(self, QMouseEvent):
        super(NameValueInput, self).mouseDoubleClickEvent(QMouseEvent)
        if self.parent.parent.w_type_charts.kb_active:
            pass
            # KEYBOARD.close()
            # KEYBOARD.open()
            # KEYBOARD.set_receiver(self)
