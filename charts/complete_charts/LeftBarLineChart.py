from PyQt5.QtChart import QChart
from PyQt5.QtChart import QChartView
from PyQt5.QtChart import QLineSeries
from PyQt5.QtChart import QVXYModelMapper
from PyQt5.QtCore import QRect
from PyQt5.QtCore import QSize
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QHeaderView
from PyQt5.QtWidgets import QInputDialog
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QTabBar
from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget

from charts.LineChart import TableView
from charts.complete_charts.Chart import Chart
from charts.complete_charts.ItemModelLineChart import ItemModelLineChart


class WTableLineChart(QWidget):



    def __init__(self, parent):
        super(WTableLineChart, self).__init__()
        self.parent = parent
        self.layout = None
        self.table = None
        self.btn_add_line = None
        self.btn_remove_line = None

        self.init_ui()
        self.setStyleSheet("""
                    border-radius: 4px;
                    background:rgb(37,43,52,220);
                """)

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.table = TableLineChart(self)
        self.setLayout(self.layout)
        self.layout.addWidget(self.table)

        self.btn_add_line = QPushButton("+")
        self.btn_add_line.setStyleSheet("""
        background-color: green;
        color: white;
        """)
        self.btn_remove_line = QPushButton("-")
        self.btn_remove_line.setStyleSheet("""
        background-color: red;
        color: white;
        """)
        self.layout.addWidget(self.btn_remove_line)
        self.layout.addWidget(self.btn_add_line)

    def create_connections(self):
        self.btn_add_line.clicked.connect(self.table.model().insertRows)
        self.btn_remove_line.clicked.connect(self.table.model().remove_row)


class TableLineChart(TableView):

    name = ""

    def __init__(self, parent):
        super(TableLineChart, self).__init__()
        self.parent = parent
        self.setStyleSheet("""
                    border-radius: 4px;
                    background:rgb(37,43,52,220);
                """)
        self.clicked.connect(self.show_cell)
        self.doubleClicked.connect(self.show_cell)


    def show_cell(self, index):
        if self.parent.parent.w_type_charts.kb_active:
            pass
            # KEYBOARD.close()
            # KEYBOARD.open()
            # KEYBOARD.set_receiver(self)
        # print("({},{}) = {}".format(index.row(),index.column(),self.model().get_data(index)))


class TabBarPlus(QTabBar):
    """Tab bar that has a plus button floating to the right of the tabs."""

    plusClicked = pyqtSignal()

    def __init__(self, parent):
        super(TabBarPlus, self).__init__()
        self.setParent(parent)
        self.setStyleSheet("""
            color: white;
            border-radius: 4px;
            background:rgb(37,43,52,220);
        """)
        # Plus Button
        self.plusButton = QPushButton("+")
        self.plusButton.setParent(self)
        self.plusButton.setMaximumSize(20, 20) # Small Fixed size
        self.plusButton.setMinimumSize(20, 20) # Small Fixed size
        self.plusButton.clicked.connect(self.plusClicked.emit)
        self.movePlusButton() # Move to the correct location
    # end Constructor

    def sizeHint(self):
        """Return the size of the TabBar with increased width for the plus button."""
        sizeHint = QTabBar.sizeHint(self)
        width = sizeHint.width()
        height = sizeHint.height()
        return QSize(width+25, height)
    # end tabSizeHint

    def resizeEvent(self, event):
        """Resize the widget and make sure the plus button is in the correct location."""
        super().resizeEvent(event)

        self.movePlusButton()
    # end resizeEvent

    def tabLayoutChange(self):
        """This virtual handler is called whenever the tab layout changes.
        If anything changes make sure the plus button is in the correct location.
        """
        super().tabLayoutChange()

        self.movePlusButton()
    # end tabLayoutChange

    def mouseDoubleClickEvent(self, event):
        if event.button() != Qt.LeftButton:
            super(TabBarPlus, self).mouseDoubleClickEvent(event)

        idx = self.currentIndex()
        ok = True
        self.input_dialog = QInputDialog()
        print(type(self.input_dialog.textEchoMode()))

        newName, ok = QInputDialog.getText(self, 'Mudar nome',
                                        'Novo nome:')

        if ok:
            self.parent().tables[idx].name = newName
            self.parent().series[idx].setName(newName)
            self.setTabText(idx, newName)

    def open_kb(self):
        print("open kb")
        # KEYBOARD.close()
        # KEYBOARD.open()
        # KEYBOARD.set_receiver(self.input_dialog)


    def movePlusButton(self):
        """Move the plus button to the correct location."""
        # Find the width of all of the tabs
        size = 0
        for i in range(self.count()):
            size += self.tabRect(i).width()

        # Set the plus button location in a visible area
        h = self.geometry().top()
        w = self.width()
        if size > w: # Show just to the left of the scroll buttons
            self.plusButton.move(w-54, h)
        else:
            self.plusButton.move(size, h)

    # end movePlusButton
# end class MyClass

class LeftBarLineChart(QTabWidget):

    layout = None
    chart = None

    tables = []
    models = []
    series = []

    default_name = None

    def __init__(self, parent):
        super(LeftBarLineChart, self).__init__()
        self.parent = parent
        self.setParent(parent)
        self.setStyleSheet("""
            border-radius: 4px;
            background:rgb(37,43,52,220);
        """)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.default_name = "Novo"
        self.init_ui()

    def init_ui(self):

        # Tab Bar
        self.tab = TabBarPlus(self)
        self.setTabBar(self.tab)

        # Properties
        # self.setMovable(True)
        # Signals
        self.tab.plusClicked.connect(self.add_tab)
        self.tab.tabMoved.connect(self.tab.movePlusButton)
        self.tabCloseRequested.connect(self.removeTab)

        #######
        self.chart = Chart()

        self.add_tab()

        self.chart.createDefaultAxes()

        self.chart.setAnimationDuration(2000)
        self.chart.setAnimationOptions(QChart.AllAnimations)


    def add_tab(self):
        if self.count() >0:
            self.setTabsClosable(True)
        else:
            self.setTabsClosable(False)


        model = ItemModelLineChart(self.parent)
        self.models.append(model)

        w_table_view = WTableLineChart(self.parent)
        w_table_view.table.name = self.default_name
        w_table_view.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)
        w_table_view.table.verticalHeader().setSectionResizeMode(
            QHeaderView.Stretch)
        w_table_view.table.setModel(model)
        w_table_view.create_connections()
        self.tables.append(w_table_view.table)


        line_series = QLineSeries()
        line_series.setName(w_table_view.table.name)
        self.series.append(line_series)

        mapper = QVXYModelMapper(self)
        mapper.setXColumn(0)
        mapper.setYColumn(1)
        mapper.setSeries(line_series)
        mapper.setModel(model)

        self.chart.addSeries(line_series)

        seriesColorHex = line_series.pen().color().name()
        model.add_mapping(seriesColorHex,
                               QRect(0, 0, 2, model.rowCount()))

        model.signal_update_models.connect(self.update_axes)

        self.addTab(w_table_view,w_table_view.table.name)

    def removeTab(self, p_int):
        if self.count() > 1:
            self.setTabsClosable(True)
        else:
            self.setTabsClosable(False)

        try:
            self.chart.removeSeries(self.series[p_int])
            self.tables.remove(self.tables[p_int])
            self.models.remove(self.models[p_int])
            self.series.remove(self.series[p_int])
        except:
            pass

        super(LeftBarLineChart, self).removeTab(p_int)


    @pyqtSlot()
    def update_axes(self):

        for s in self.series:
            self.chart.removeSeries(s)
            self.chart.addSeries(s)
        self.chart.createDefaultAxes()
