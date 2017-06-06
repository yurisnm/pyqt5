from PyQt5.QtChart import QBarCategoryAxis
from PyQt5.QtChart import QBarSeries
from PyQt5.QtChart import QBarSet
from PyQt5.QtChart import QChart
from PyQt5.QtCore import QSize
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QInputDialog
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QTabBar
from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget


## MAIN TAB WIDGET
class LeftBarBarChart(QTabWidget):

    chart = None
    tabs = []
    bar_sets = []
    inputs = []
    main_tab = None

    def __init__(self, parent):
        super(LeftBarBarChart, self).__init__()
        self.setParent(parent)
        self.setStyleSheet("""
            color: white;
            border-radius: 4px;
            background:rgb(37,43,52,220);
        """)
        self.init_ui()

    def init_ui(self):
        # Tab Bar
        self.tab_bar = TabBarPlus(self)
        self.setTabBar(self.tab_bar)
        # Properties
        # self.setMovable(True)
        # Signals
        self.tab_bar.plusClicked.connect(self.add_tab)
        self.tab_bar.tabMoved.connect(self.tab_bar.movePlusButton)
        self.tabCloseRequested.connect(self.removeTab)
        #######
        self.chart = QChart()
        self.serie = QBarSeries()
        self.chart.addSeries(self.serie)
        self.chart.setTitle("Bar Chart")

        self.main_tab = MainTab(self)
        self.addTab(self.main_tab , self.main_tab.name)

        self.chart.createDefaultAxes()

        self.chart.setAnimationDuration(2000)
        self.chart.setAnimationOptions(QChart.AllAnimations)



    def add_tab(self):
        if self.count() >= 0:
            self.setTabsClosable(True)
        else:
            self.setTabsClosable(False)

        tab = Tab(self, "New Tab", len(self.main_tab.all_inputs))
        self.tabs.append(tab)
        self.addTab(tab, tab.name)


    def removeTab(self, p_int):
        if self.count() > 1:
            super(LeftBarBarChart, self).removeTab(p_int)
            del self.tabs[p_int - 1]

        if self.count() >=2:
            self.setTabsClosable(True)
        else:
            self.setTabsClosable(False)

    def update_all_tabs(self, amount):
        for tab in self.tabs:
            tab.update_tab(amount)

    def update_axes(self):
        self.chart.removeSeries(self.serie)
        self.chart.addSeries(self.serie)
        self.chart.createDefaultAxes()


class MainTab(QWidget):

    layout = None
    layout_inputs = None
    btn_add_input = None
    btn_remove_input = None
    name = "Categoria"
    parent = None
    all_inputs = []

    def __init__(self, parent):
        super(MainTab, self).__init__()
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()

        self.btn_remove_input = QPushButton("-")
        self.btn_remove_input.setStyleSheet("""
                    background-color: red;
                    color: white;
                """)
        self.btn_remove_input.clicked.connect(self.remove_input)

        self.btn_add_input = QPushButton("+")
        self.btn_add_input.setStyleSheet("""
                           background-color: green;
                           color: white;
                       """)
        self.btn_add_input.clicked.connect(self.add_input)

        self.layout_inputs = QVBoxLayout()
        self.layout.addLayout(self.layout_inputs)
        self.layout.addStretch(-1)
        self.layout.addWidget(self.btn_remove_input)
        self.layout.addWidget(self.btn_add_input)

        self.setLayout(self.layout)

    def add_input(self):
        new_inp = MainInput()
        self.all_inputs.append(new_inp)
        self.layout_inputs.addWidget(new_inp)
        self.parent.update_all_tabs(len(self.all_inputs))

    def remove_input(self):
        if len(self.all_inputs)>1:
            self.layout_inputs.removeWidget(self.all_inputs[-1])
            self.all_inputs[-1].hide()
            self.all_inputs.remove(self.all_inputs[-1])
            self.parent.update_all_tabs(len(self.all_inputs))

    def input_changed(self, value):
        print(value)


class Tab(QWidget):

    layout_inputs = None
    name = "Novo"
    amount = 0
    inputs = []
    parent = None

    def __init__(self,parent, name, amount):
        super(Tab, self).__init__()
        self.name = name
        self.amount = amount
        self.parent = parent
        self.init_ui()


    def init_ui(self):
        self.layout_inputs = QVBoxLayout()
        self.setLayout(self.layout_inputs)
        for i in range(self.amount):
            value = QLineEdit()
            value.textChanged.connect(self.keep_valid)
            # value.textChanged.connect(self.parent.input_changed)
            value.setText('0')
            value.setInputMask('9999999')
            value.setCursorPosition(0)
            self.inputs.append(value)
            self.layout_inputs.addWidget(value)
        l = QVBoxLayout()
        l.addSpacing(1)
        l.addStretch(-1)
        self.layout_inputs.addLayout(l)

    def update_tab(self, amount):
        if amount>self.amount:
            for i in range(amount-self.amount):
                value = QLineEdit()
                value.textChanged.connect(self.keep_valid)
                # value.textChanged.connect(self.parent.input_changed)
                value.setText('0')
                value.setInputMask('9999999')
                value.setCursorPosition(0)
                self.inputs.append(value)
                self.layout_inputs.insertWidget(0,value)
        else:
            for i in range(amount,self.amount):

                self.layout_inputs.removeWidget(self.inputs[-1])
                self.inputs[-1].hide()
                self.inputs[-1].close()
                self.inputs.remove(self.inputs[-1])
        self.amount = amount

    def keep_valid(self,txt):
        if txt == "":
            self.value.setText("0")
            self.value.setCursorPosition(0)

class MainInput(QWidget):

    name = None
    value = None
    q_line_name = None
    q_line_value = None
    layout = None

    def __init__(self):
        super(MainInput, self).__init__()
        self.name = "Categoria"
        self.init_ui()

    def init_ui(self):
        self.layout = QHBoxLayout()
        self.q_line_name = QLineEdit()
        self.q_line_name.setText(self.name)
        self.layout.addWidget(self.q_line_name)
        self.setLayout(self.layout)

class Input(QWidget):

    name = None
    value = None
    q_line_name = None
    q_line_value = None
    layout = None

    def __init__(self, name, value):
        super(Input, self).__init__()
        self.name = name
        self.value = str(value)
        self.init_ui()

    def init_ui(self):
        self.layout = QHBoxLayout()
        self.q_line_name = QLineEdit()
        self.q_line_name.setText(self.name)
        self.q_line_value = QLineEdit()
        self.q_line_value.setText(self.value)
        self.layout.addWidget(self.q_line_name)
        self.layout.addWidget(self.q_line_value)
        self.setLayout(self.layout)



# TAB BAR
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
        if self.currentIndex() != 0:
            if event.button() != Qt.LeftButton:
                super(TabBarPlus, self).mouseDoubleClickEvent(event)

            idx = self.currentIndex()
            ok = True
            input_dialog = QInputDialog()

            newName, ok = QInputDialog.getText(self, 'Mudar nome',
                                            'Novo nome:')

            if ok:
                self.setTabText(idx, newName)


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

