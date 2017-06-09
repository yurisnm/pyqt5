import sys
from PyQt5.QtCore import QSize, pyqtSlot
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QInputDialog
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QTabBar
from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget


class MyWidget(QWidget):

    default_name = "New"

    def __init__(self):
        super(MyWidget, self).__init__()
        self.setStyleSheet("""
                    border-radius: 4px;
                    background:rgb(37,43,52,220);
                """)
        self.name = self.default_name




class TabBarPlus(QTabBar):
    """Tab bar that has a plus button floating to the right of the tabs."""

    plusClicked = pyqtSignal()

    def __init__(self, parent):
        super(TabBarPlus, self).__init__()
        self.setParent(parent)

        self.setStyleSheet(
        """
            QTabBar::tab {
                width: 80px;

            }

           QTabBar::tab:selected {
                font-family: Roboto;
                font-size: 18px;
                font: italic;
                color: rgb(0,0,0,255);

                background: rgb(234,234,234,255);
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;

                border:1px;
                border-color: rgb(197,197,199,255);
                border-top-style: solid;
                border-right-style: solid;
                border-left-style: solid;
                padding: 10px 50px 10px 24px;

           }

           QTabBar::tab:!selected{
                font-family: Roboto;
                font-size: 18px;
                font: italic;
                color: rgb(255,255,255,255);
                background: rgb(175,175,175,255);
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;

               border:1px;
                border-color: rgb(197,197,199,255);
                border-top-style: solid;
                border-right-style: solid;
                border-bottom-style: ;
                border-left-style: solid;
                padding: 10px 50px 10px 24px;
            }

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
            self.setTabText(idx, newName)

    def open_kb(self):
        print("open keyboard")



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

class WidgetTab(QTabWidget):

    layout = None
    def __init__(self):
        super(WidgetTab, self).__init__()
        self.setStyleSheet("""
            border-radius: 4px;
            background:rgb(37,43,52,220);
        """)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.setMinimumSize(800,400)
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

        self.add_tab()




    def add_tab(self):
        if self.count() >0:
            self.setTabsClosable(True)
        else:
            self.setTabsClosable(False)



        my_widget = MyWidget()


        self.addTab(my_widget,my_widget.name)

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

        super(WidgetTab, self).removeTab(p_int)


    @pyqtSlot()
    def update_axes(self):

        for s in self.series:
            self.chart.removeSeries(s)
            self.chart.addSeries(s)
        self.chart.createDefaultAxes()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    wt = WidgetTab()
    wt.show()
    sys.exit(app.exec_())