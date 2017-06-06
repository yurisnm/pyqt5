from PyQt5.QtChart import QChart
from PyQt5.QtChart import QPieSeries
from PyQt5.QtWidgets import QGraphicsItem


class Chart(QChart):

    def __init__(self):
        super(Chart, self).__init__()
