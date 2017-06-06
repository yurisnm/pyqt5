

import sys

from PyQt5.QtChart import QChart
from PyQt5.QtChart import QChartView
from PyQt5.QtChart import QLineSeries
from PyQt5.QtChart import QVXYModelMapper
from PyQt5.QtCore import QRect, pyqtSlot
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtWidgets import QHeaderView
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget

from charts.LineChart import ItemModel, TableView


class GraphicsView(QGraphicsView):

    def __init__(self):
        super(GraphicsView, self).__init__()
        self.scene = GraphicsScene()
        self.setScene(self.scene)


class GraphicsScene(QGraphicsScene):

    def __init__(self):
        super(GraphicsScene, self).__init__()

        self.line_series = QLineSeries()
        self.chart = QChart()
        self.chart_view = QChartView(self.chart)
        self.chart_view.setMinimumSize(640, 480)

        self.model = ItemModel()
        self.model.signal_update_models.connect(self.update_axes)

        self.table_view = TableView()

        self.table_view.setModel(self.model)
        self.table_view.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)
        self.table_view.verticalHeader().setSectionResizeMode(
            QHeaderView.Stretch)

        self.chart.setAnimationOptions(QChart.AllAnimations)
        self.chart.setAnimationDuration(2000)

        self.line_series.setName("Line 1")

        self.mapper = QVXYModelMapper(self)
        self.mapper.setXColumn(0)
        self.mapper.setYColumn(1)
        self.mapper.setSeries(self.line_series)
        self.mapper.setModel(self.model)
        self.chart.addSeries(self.line_series)

        seriesColorHex = self.line_series.pen().color().name()
        self.model.add_mapping(seriesColorHex,
                               QRect(0, 0, 2, self.model.rowCount()))

        self.line_series2 = QLineSeries()
        self.line_series2.setName("Line 2")

        self.mapper2 = QVXYModelMapper(self)
        self.mapper2.setXColumn(2)
        self.mapper2.setYColumn(3)
        self.mapper2.setSeries(self.line_series2)
        self.mapper2.setModel(self.model)
        self.chart.addSeries(self.line_series2)

        seriesColorHex = self.line_series2.pen().color().name()
        self.model.add_mapping(seriesColorHex,
                               QRect(2, 0, 2, self.model.rowCount()))

        self.chart.createDefaultAxes()


        self.chart_view.setRenderHint(QPainter.Antialiasing)
        self.chart.resize(500,400)
        self.chart.setFlag(QGraphicsItem.ItemIsMovable)
        self.chart.setFlag(QGraphicsItem.ItemIsSelectable)
        self.addItem(self.chart)

    @pyqtSlot()
    def update_axes(self):
        self.chart.removeSeries(self.line_series)
        self.chart.removeSeries(self.line_series2)
        self.chart.addSeries(self.line_series)
        self.chart.addSeries(self.line_series2)
        self.chart.createDefaultAxes()

class MainWindow(QMainWindow):

    main_widget = None
    gv = None
    layout = None

    def __init__(self):
        super(MainWindow, self).__init__()
        self.main_widget = QWidget()
        self.gv = GraphicsView()
        self.layout = QVBoxLayout()
        self.main_widget.setLayout(self.layout)
        self.setCentralWidget(self.main_widget)
        self.layout.addWidget(self.gv)
        self.resize(800,500)


if __name__=="__main__":
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())