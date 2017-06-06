import random
import sys

from PyQt5.QtChart import QCategoryAxis
from PyQt5.QtChart import QChart
from PyQt5.QtChart import QChartView
from PyQt5.QtChart import QLineSeries
from PyQt5.QtChart import QVXYModelMapper
from PyQt5.QtChart import QValueAxis
from PyQt5.QtCore import QAbstractItemModel, pyqtSlot
from PyQt5.QtCore import QModelIndex
from PyQt5.QtCore import QRect
from PyQt5.QtCore import QVariant
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QHeaderView
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QTableView
from PyQt5.QtWidgets import QWidget


class TableView(QTableView):

    def __init__(self):
        super(TableView, self).__init__()
        # self.clicked.connect(self.show_cell)
        self.setStyleSheet("""
            QTableView {

                background-color: #646464;
                padding: 4px;
                font-size: 8pt;
                border-style: none;
                border-bottom: 1px solid #fffff8;
                border-right: 1px solid #fffff8;
                selection-background-color: qlineargradient(x1: 0, y1: 0, x2: 0.5, y2: 0.5,
                                stop: 0 #FF92BB, stop: 1 white);
            }
        """)


    def show_cell(self, index):
        print("({},{}) = {}".format(index.row(),index.column(),self.model().get_data(index)))




class ItemModel(QAbstractItemModel):

    signal_update_models = pyqtSignal()

    def __init__(self):
        super(ItemModel, self).__init__()
        self.m_column_count = 4
        self.m_row_count = 9
        self.m_mapping = {}
        self.m_data = []
        self.fill_with_random_data()


    def fill_with_random_data(self):
        for r in range(self.m_row_count):
            data_vec = [None] * self.m_column_count

            for c in range(len(data_vec)):
                if (c%2)==0:
                    data_vec[c] = r*50+random.randint(0,100)%20
                else:
                    data_vec[c] = random.randint(0, 100) % 20
            self.m_data.append(data_vec)

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.m_data)

    def columnCount(self, parent=None, *args, **kwargs):
        return self.m_column_count

    def headerData(self, section, orientation, role=None):
        print(orientation)
        if role == Qt.DisplayRole:
            return QVariant()
        if orientation == Qt.Horizontal:
            if section%2==0:
                return "x"
            else:
                return "y"
        else:
            return "{}".format(section+1)

    def data(self, index, role=None):
        if role == Qt.DisplayRole:
            return self.m_data[index.row()][index.column()]
        elif role == Qt.EditRole:
            return self.m_data[index.row()][index.column()]
        elif role == Qt.BackgroundRole:
            for color, rect in self.m_mapping.items():
                if rect.contains(index.column(), index.row()):
                    return QColor(color)
        return QVariant()

    def setData(self, index, value, role=None):
        if index.isValid() and role == Qt.EditRole:
            self.m_data[index.row()][index.column()] = int(value)
            self.dataChanged.emit(index,index)
            self.signal_update_models.emit()
            return True
        return False

    def get_data(self, index):
        return self.m_data[index.row()][index.column()]

    def add_mapping(self, color, area):
        self.m_mapping[color] = area

    def flags(self, index):
        return Qt.ItemIsEditable | Qt.ItemIsEnabled
        # if (index.column() == 0):
        #     return Qt.ItemIsEditable | Qt.ItemIsEnabled
        # else:
        #     return Qt.ItemIsEnabled

    def index(self, row, column, parent=None, *args, **kwargs):
        if self.hasIndex(row,column,parent):
            return self.createIndex(row,column,self.m_data[row])
        return QModelIndex()

    def parent(self, index=None):
        return QModelIndex()



class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.init_ui()

    def init_ui(self):



        self.line_series = QLineSeries()
        self.chart = QChart()
        self.chart_view = QChartView(self.chart)
        self.chart_view.setMinimumSize(640,480)

        self.model = ItemModel()
        self.model.signal_update_models.connect(self.update_axes)

        self.table_view = TableView()

        self.table_view.setModel(self.model)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_view.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

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
                               QRect(0,0,2, self.model.rowCount()))

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

        self.grid = QGridLayout()
        self.grid.addWidget(self.table_view,0,0)
        self.grid.addWidget(self.chart_view,0,1)

        self.chart_view.setRenderHint(QPainter.Antialiasing)
        self.cw = QWidget()
        self.cw.setLayout(self.grid)
        self.setCentralWidget(self.cw)
        self.resize(400,300)

    @pyqtSlot()
    def update_axes(self):
        self.chart.removeSeries(self.line_series)
        self.chart.removeSeries(self.line_series2)
        self.chart.addSeries(self.line_series)
        self.chart.addSeries(self.line_series2)
        self.chart.createDefaultAxes()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())