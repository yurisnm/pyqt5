# !/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QPoint
from PyQt5.QtCore import QRectF
from PyQt5.QtCore import QSize
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QBrush
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QPainterPath
from PyQt5.QtGui import QPen
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtWidgets import QGraphicsPathItem
from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtWidgets import QGraphicsTextItem
from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget

try:
    import Image
except ImportError:
    from PIL import Image
import pytesseract



import os, sys


class MainWindow(QMainWindow):
    _vLayout = None
    _mainWidget = None
    _drawWidget = None
    _btns_widget = None
    _tesseractWidget = None
    _layout_buttons = None
    _svs = None
    _btn_clear = None
    _btn_draw = None
    _btn_select = None
    _selected_option = 1

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self._mainWidget = QWidget()
        self._drawWidget = QWidget()
        self._btns_widget = QWidget()
        self._layout_buttons = QVBoxLayout()
        self._layout_draw = QHBoxLayout()
        self._drawWidget.setLayout(self._layout_draw)
        self._vLayout = QVBoxLayout()
        self._vLayout.setSpacing(2)
        self.setCentralWidget(self._mainWidget)
        self._mainWidget.setLayout(self._vLayout)
        self.configure_buttons()

        self._tesseractWidget = TesseractWidget()
        self._svs = ScreenViewScene()
        self._layout_draw.addWidget(self._btns_widget)
        self._layout_draw.addWidget(self._svs)


        self._vLayout.addWidget(self._drawWidget)
        self._vLayout.addWidget(self._tesseractWidget)
        self._svs.signal_send_image.connect(self.setImage)
        self._tesseractWidget.signal_send_text.connect(self._svs.switch_to_text)

    def configure_buttons(self):
        self._btn_select = QPushButton("Select")
        self._btn_draw = QPushButton("Draw")
        self._btn_clear = QPushButton("Clear")
        self._btn_select.clicked.connect(self.btn_select_clicked)
        self._btn_draw.clicked.connect(self.btn_draw_clicked)
        self._btn_clear.clicked.connect(self.btn_clear_clicked)
        self._layout_buttons.addWidget(self._btn_select)
        self._layout_buttons.addWidget(self._btn_draw)
        self._layout_buttons.addWidget(self._btn_clear)
        self._btns_widget.setLayout(self._layout_buttons)


    def btn_select_clicked(self):
        self._svs.selected_option = 0
        self._btn_select.setStyleSheet("background-color: blue")
        self._btn_draw.setStyleSheet("")
        self._btn_clear.setStyleSheet("")

    def btn_draw_clicked(self):
        self._svs.selected_option = 1
        self._btn_select.setStyleSheet("")
        self._btn_draw.setStyleSheet("background-color: blue")
        self._btn_clear.setStyleSheet("")

    def btn_clear_clicked(self):
        self._svs.clear()

    @pyqtSlot()
    def setImage(self):
        self._tesseractWidget.updateText()




class ScreenViewScene(QGraphicsView):

    signal_send_image = pyqtSignal()
    img = None
    painter = None
    item = None
    pos_text = None
    PIX = None
    pressing = False
    timer = None
    path = None
    selected_option = 1

    def __init__(self):
        QGraphicsView.__init__(self)
        self.setScene(GraphicsScene())
        self.setSceneRect(QRectF(self.viewport().rect()))
        self.PIX = QPixmap()
        self.timer = QTimer()
        self.timer.timeout.connect(self.proccessImage)
        self.path = QPainterPath()
        self.item = GraphicsPathItem()
        self.scene().addItem(self.item)


    def mousePressEvent(self, event):
        if self.selected_option == 1:
            self.timer.stop()
            self.pressing = True
            self._start = self.mapToScene(event.pos())
            self.path.moveTo(self._start)


    def mouseMoveEvent(self, event):
        if self.selected_option ==1:
            if self.pressing:
                self.end = self.mapToScene(event.pos())
                self.path.lineTo(self.end)
                self.item.setPath(self.path)
                self._start = self.end


    def mouseReleaseEvent(self, event):
        if self.selected_option == 1:
            self.timer.start(1000)
            self.pressing = False

    def proccessImage(self):
        gv = QGraphicsView()
        gv.setScene(GraphicsScene())
        gv.scene().addItem(self.item)

        self.PIX = QWidget.grab(gv)
        self.PIX.save("TEXT.png")
        self.signal_send_image.emit()
        self.timer.stop()


    @pyqtSlot(str)
    def switch_to_text(self, text):

        font = QFont()
        font.setPointSize(self.__height_to_point(self.PIX.height()))
        graphics_text_item = QGraphicsTextItem(text)
        graphics_text_item.setFlag(QGraphicsItem.ItemIsMovable)
        graphics_text_item.setFont(font)
        self.scene().addItem(graphics_text_item)
        graphics_text_item.setPos(
            QPoint(self.item.boundingRect().x(), self.item.boundingRect().y()))
        self.path = QPainterPath()
        self.item = GraphicsPathItem()
        self.scene().addItem(self.item)

    def clear(self):
        self.scene().clear()
        self.path = QPainterPath()
        self.item = GraphicsPathItem()
        self.item.setPath(self.path)
        self.scene().addItem(self.item)

    def __height_to_point(self, height):
        return height*0.6153846153846154

class GraphicsPathItem(QGraphicsPathItem):

    pen = None
    path = None
    width = 20

    def __init__(self):
        super(GraphicsPathItem, self).__init__()
        self.init_ui()

    def init_ui(self):
        self.pen = QPen()
        self.pen.setWidth(self.width)
        self.pen.setJoinStyle(Qt.RoundJoin)
        self.pen.setCapStyle(Qt.RoundCap)
        self.setPen(self.pen)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)


class GraphicsScene(QGraphicsScene):
    def __init__(self):
        super(GraphicsScene, self).__init__()
        self.init_ui()

    def init_ui(self):
        self.setBackgroundBrush(QBrush(QColor(Qt.white)))

class TesseractWidget(QWidget):
    _path = ""
    _image = None
    _pixmap = None
    _line = None
    _v_layout = None
    _hWidget = None
    _hLayout = None
    _btnFile = None
    _fileDialog = None
    _lbl = None
    signal_send_text = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self._fileDialog = QFileDialog(self)
        self._v_layout = QVBoxLayout()
        self._v_layout.setSpacing(2)
        self.setLayout(self._v_layout)
        self._path = "TEXT.png"
        self._pixmap = QPixmap(self._path)
        self._btnFile = QPushButton("Open")
        self._hWidget = QWidget()
        self._hLayout = QHBoxLayout()
        self._hWidget.setLayout(self._hLayout)

        self._image = Image.open(self._path)
        self._line = QLineEdit()

        self._hLayout.addWidget(self._btnFile)
        self._hLayout.addWidget(self._line)
        size = QSize(160, 90)
        pix = self._pixmap.scaled(size, transformMode=Qt.SmoothTransformation)

        self._lbl = QLabel()
        self._lbl.setPixmap(pix)
        self._v_layout.addWidget(self._lbl)
        self._v_layout.addWidget(self._hWidget)
        self._btnFile.clicked.connect(self.openFilePressed)

        self._line.setText(pytesseract.image_to_string(Image.open('TEXT.png')))


    def openFilePressed(self):
        self._path = self._fileDialog.\
            getOpenFileName(self, "Image Files (*.png *.jpg)")
        if self._path[0] != "":
            self._pixmap = QPixmap(self._path[0])
            size = QSize(160, 90)
            pix = self._pixmap.scaled(size,
                                      transformMode=Qt.SmoothTransformation)
            self._lbl.setPixmap(pix)
            self._image = Image.open(self._path[0])
            text = pytesseract.image_to_string(self._image)
            self._line.setText(text)

    def updateText(self):

        self._pixmap = QPixmap('TEXT.png')
        size = QSize(160, 90)

        pix = self._pixmap.scaled(size,
                                  transformMode=Qt.SmoothTransformation)
        self._lbl.setPixmap(pix)
        self._image = Image.open('TEXT.png')
        text = pytesseract.image_to_string(self._image, lang='eng', config='-psm 8', )
        self._line.setText(text)
        self.signal_send_text.emit(text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())
