import random

from PyQt5.QtCore import QAbstractItemModel
from PyQt5.QtCore import QModelIndex
from PyQt5.QtCore import QRect
from PyQt5.QtCore import QVariant
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QMouseEvent


class ItemModelLineChart(QAbstractItemModel):

    signal_update_models = pyqtSignal()

    def __init__(self, parent):
        super(ItemModelLineChart, self).__init__()
        self.parent = parent
        self.m_column_count = 2
        self.m_row_count = 0
        self.m_mapping = {}
        self.m_data = []
        # self.fill_with_random_data()

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
        self.color = color
        self.area = area
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

    def insertRows(self):
        self.beginInsertRows(QModelIndex(), self.m_row_count, self.m_row_count)

        self.m_data.append([0,0])
        self.m_row_count += 1
        self.add_mapping(self.color, QRect(0, 0, 2, self.rowCount()))
        self.endInsertRows()
        return True

    def removeRows(self):
        self.beginRemoveRows(QModelIndex(), self.m_row_count, self.m_row_count)
        self.m_data.pop()
        self.m_row_count -= 1
        self.endRemoveRows()

        return True

    def add_row(self):
        self.insertRows()

    def remove_row(self):
        if self.m_row_count>0:
            self.m_row_count -= 1
            self.removeRows()


