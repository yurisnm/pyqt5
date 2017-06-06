
import sys

from PyQt5.QtChart import QChart
from PyQt5.QtChart import QChartView
from PyQt5.QtCore import QPoint, pyqtSlot
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QVBoxLayout

from charts.complete_charts.EChart import EChart
from charts.complete_charts.LeftBarBarChart import LeftBarBarChart
from charts.complete_charts.LeftBarLineChart import LeftBarLineChart
from charts.complete_charts.LeftBarPieChart import LeftBarPieChart
from charts.complete_charts.TopBar import TopBar


class MainChartWidget(QDialog):

    # w_type_charts = None
    # w_chart_line = None
    # w_chart_pie = None
    # w_chart_bar = None
    # w_chart = None
    #
    # v_layout_main = None
    # h_layout_middle = None
    #
    # selector = None

    signal_confirm_chart = pyqtSignal(QChart)

    def __init__(self):
        super(MainChartWidget, self).__init__()

        self.w_type_charts = None
        self.w_chart_line = None
        self.w_chart_pie = None
        self.w_chart_bar = None
        self.w_chart = None

        self.v_layout_main = None
        self.h_layout_middle = None

        self.selector = None
        self.init_ui()


    def init_ui(self):
        self.setFixedSize(700,600)
        self.assemble()
        self.set_styles()
        self.aux = QPoint(200,300)
        self.setWindowFlags(Qt.FramelessWindowHint)
        # self.setAttribute(Qt.WA_TranslucentBackground)

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()
        self._from_x = event.pos().x()
        self._from_y = event.pos().y()
        # self.start = event.pos()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)
        self.aux = QPoint(self.x() + delta.x(), self.y() + delta.y())
        self.move(self.aux)
        self.oldPos = event.globalPos()

        self._to_x = event.pos().x()
        self._to_y = event.pos().y()

        self.global_pos = event.globalPos()

        self._from_x = self._to_x
        self._from_y = self._to_y



    def set_styles(self):
        self.setStyleSheet("""
        MainChartWidget{
            border-radius: 4px;
            background:rgb(37,43,52,220);
            color: white;
        }
        QScrollArea{
                background-color:transparent;
                border-radius: 4px;
                border: 0px solid ;
                border-color: rgb(0,0,0,100)
            }

            QScrollBar:vertical{
                border:1px solid;
                border-color: rgb(197,197,199,100);
                width: 7px;
                margin: 0px 0px 0px 0px;
                background: rgb(234,234,234,100);

            }

            QScrollBar::handle:vertical  {
                background: rgba(14,65,148,100);
            }

            QScrollBar::add-line:vertical{
                height: 0px;
            }

            QScrollBar::sub-line:vertical{
                height: 0px;
            }
        """)




    def assemble(self):

        self.w_type_charts = TopBar(self)
        self.w_type_charts.signal_send_chart_selected.connect(self.set_chart_type)
        self.w_type_charts.setMinimumSize(650,50)
        self.w_type_charts.setMaximumHeight(50)

        self.w_chart_line = LeftBarLineChart(self)
        self.w_chart_line.setMinimumSize(200, 300)
        self.w_chart_line.setMaximumWidth(200)

        self.w_chart_pie = LeftBarPieChart(self)
        self.w_chart_pie.hide()
        self.w_chart_pie.setMinimumSize(200, 300)
        self.w_chart_pie.setMaximumWidth(200)

        self.w_chart_bar = LeftBarBarChart(self)
        self.w_chart_bar.hide()
        self.w_chart_bar.setMinimumSize(200, 300)
        self.w_chart_bar.setMaximumWidth(200)

        self.w_chart = QChartView()
        self.w_chart.setChart(self.w_chart_line.chart)
        self.w_chart.setMinimumSize(400,300)

        self.v_layout_main = QVBoxLayout()
        self.v_layout_main.setContentsMargins(20,20,20,20)
        self.h_layout_middle = QHBoxLayout()
        self.v_layout_main.addWidget(self.w_type_charts)
        self.v_layout_main.addLayout(self.h_layout_middle)
        self.h_layout_middle.addWidget(self.w_chart_line)
        self.h_layout_middle.addWidget(self.w_chart_pie)
        self.h_layout_middle.addWidget(self.w_chart_bar)
        self.h_layout_middle.addWidget(self.w_chart)

        self.setLayout(self.v_layout_main)
        self.w_type_charts.btn_chart_line_clicked()

    @pyqtSlot(int)
    def set_chart_type(self, type):
        self.w_chart_line.hide()
        self.w_chart_pie.hide()
        self.w_chart_bar.hide()
        self.selector = type
        if type == EChart.LINE:
            self.w_chart_line.show()
            self.w_chart.setChart(self.w_chart_line.chart)
        elif type == EChart.PIE:
            self.w_chart_pie.show()
            self.w_chart.setChart(self.w_chart_pie.chart)
        elif type == EChart.BAR:
            self.w_chart_bar.show()
            self.w_chart.setChart(self.w_chart_bar.chart)

    def confirm_chart(self):
        self.signal_confirm_chart.emit(self.w_chart.chart())
        # KEYBOARD.close()

    def hide(self):
        # KEYBOARD.close()
        super(MainChartWidget, self).hide()


# def resettable(f):
#     import copy
#
#     def __init_and_copy__(self, *args, **kwargs):
#         f(self, *args)
#         self.__original_dict__ = copy.deepcopy(self.__dict__)
#
#         def reset(o=self):
#             o.__dict__ = o.__original_dict__
#
#         self.reset = reset
#
#     return __init_and_copy__


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mcw = MainChartWidget()
    mcw.show()
    sys.exit(app.exec_())