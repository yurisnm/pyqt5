from PyQt5.QtCore import QCoreApplication
from PyQt5.QtCore import QEvent
from PyQt5.QtCore import QSize
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import QPushButton
# from resources.icons import global_resource_rc


class KeyboardKey(QPushButton):
    __path = "your_assets"

    __size = [30, 30]
    __style = ""
    __icon_on = ""
    __icon_off = ""
    __auto_repeat = True
    __receiver = None
    __key = None
    __str_key = None

    __upper_case = False

    def __init__(self, style, str_icon_on, str_icon_off, auto_repeat, size,
                 receiver, key, str_key):
        super(KeyboardKey, self).__init__()
        self.__size = size
        self.__style = style
        self.__icon_on = str_icon_on
        self.__icon_off = str_icon_off
        self.__auto_repeat = auto_repeat
        self.__receiver = receiver
        self.__key = key
        self.__str_key = str_key
        self.set_up_button(style, str_icon_on, str_icon_off, auto_repeat, size,
                           receiver, key, str_key)
        self.setCursor(QCursor(Qt.PointingHandCursor))

    def set_up_button(self, style, str_icon_on, str_icon_off, auto_repeat,
                      size, receiver, key, str_key):
        self.__size = size
        self.__style = style
        self.__icon_on = str_icon_on
        self.__icon_off = str_icon_off
        self.__auto_repeat = auto_repeat
        self.__receiver = receiver
        self.__key = key
        self.__str_key = str_key
        if str_key not in ['KB', 'A▲', '◄', '►', 'backspace']:
            self.setText(str_key)

        self.setFixedSize(size[0], size[1])
        self.setStyleSheet(style)
        self.setIconSize(QSize(size[0], size[1]))
        self.setIcon(QIcon(self.__path + str_icon_off + ".png"))
        self.setAutoRepeat(auto_repeat)
        # pix_map = QPixmap(self.__path + str_icon_off + ".png")
        # self.setMask(pix_map.mask())
        self.pressed.connect(self.key_pressed)
        self.released.connect(self.key_released)

    def set_receiver(self, receiver):
        self.__receiver = receiver

    def key_pressed(self):
        self.setStyleSheet("""
                            border-width: 5px;
                            border-radius: 5px;
                            color: white;
                            background-color: rgb(0, 187, 255);
                        """)

    def key_released(self):

        self.setStyleSheet(self.__style)
        if self.__str_key == "&&":
            self.__str_key = "&"
        event = QKeyEvent(QEvent.KeyPress, self.__key, Qt.NoModifier,
                          self.__str_key, False)
        QCoreApplication.postEvent(self.__receiver, event)

    def key_released2(self):
        self.setStyleSheet(self.__style)

    def set_str_key(self, key):
        self.__str_key = key
        if self.__str_key not in ['KB', 'A▲', '◄', '►', 'backspace']:
            self.setText(self.__str_key)

    def get_name(self):
        return self.__str_key

    def get_key(self):
        return self.__key

    def keyPressEvent(self, evt):
        event = QKeyEvent(QEvent.KeyPress, evt.key(), evt.modifiers(),
                          evt.text(), False)
        QCoreApplication.postEvent(self.__receiver, event)
        evt.ignore()

    def keyReleaseEvent(self, event):
        # super(KeyboardKey, self).keyReleaseEvent(event)
        event.ignore()
