import sys
from PyQt5.QtCore import QPoint
from PyQt5.QtCore import QSize
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QStackedLayout
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget

from keyboard_full.KeyboardKey import KeyboardKey


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.text_edit = TextEdit(self)
        self.layout.addWidget(self.text_edit)
        self.kb = WKeyboard()
        self.kb.set_receiver(self.text_edit)

    def closeEvent(self, QCloseEvent):
        self.kb.close()
        super(MainWindow, self).closeEvent(QCloseEvent)

class TextEdit(QTextEdit):

    def __init__(self, parent):
        super(TextEdit, self).__init__()
        self.parent = parent

    def mousePressEvent(self, QMouseEvent):
        self.parent.kb.show()
        super(TextEdit, self).mousePressEvent(QMouseEvent)


class WKeyboard(QDialog):
    path = ":/Icons/assets_keyboard/"

    proportion = 1

    size = [700, 250]

    keyboard = []
    keyboard_keys = []
    keyboard_numbers_keys = []
    keyboard_symbols_keys = []
    keyboard_on = []
    keyboard_on_upper = []
    keyboard_off = []
    keyboard_off_upper = []

    keyboard_numbers = []
    keyboard_numbers_on = []
    keyboard_numbers_off = []

    keyboard_symbols = []
    keyboard_symbols_on = []
    keyboard_symbols_off = []

    h_row1 = None
    w_row1 = None
    h_row2 = None
    w_row2 = None
    h_row3 = None
    w_row3 = None
    h_row4 = None
    w_row4 = None
    v_container = None
    w_container = None

    h_row1_n = None
    w_row1_n = None
    h_row2_n = None
    w_row2_n = None
    h_row3_n = None
    w_row3_n = None
    h_row4_n = None
    w_row4_n = None
    v_container_n = None
    w_container_n = None

    h_row1_s = None
    w_row1_s = None
    h_row2_s = None
    w_row2_s = None
    h_row3_s = None
    w_row3_s = None
    h_row4_s = None
    w_row4_s = None
    v_container_s = None
    w_container_s = None

    __receiver = None

    oldPos = None
    selected = False

    button_caps_lock = None
    button_letters = None
    button_numbers = None
    button_symbols = None

    general_widget_letters = None
    general_widget_numbers = None
    general_widget_symbols = None
    general_container = None

    upper_case = False

    style_on = ""
    style_off = ""

    buttons_size = [44, 43]

    def __init__(self):
        super(WKeyboard, self).__init__()

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        # _size = [int(650*self.proportion), int(250*self.proportion)]
        self.oldPos = self.pos()
        self.selected = False

        self.upper_case = False

        self.keyboard = []
        self.keyboard_keys = []
        self.keyboard_on = []
        self.keyboard_on_upper = []
        self.keyboard_off = []
        self.keyboard_off_upper = []

        self.keyboard_numbers = []
        self.keyboard_numbers_on = []
        self.keyboard_numbers_off = []

        self.keyboard_symbols = []
        self.keyboard_symbols_on = []
        self.keyboard_symbols_off = []

        self.h_row1 = QHBoxLayout()
        self.w_row1 = QWidget()
        self.h_row2 = QHBoxLayout()
        self.w_row2 = QWidget()
        self.h_row3 = QHBoxLayout()
        self.w_row3 = QWidget()
        self.h_row4 = QHBoxLayout()
        self.w_row4 = QWidget()
        self.v_container = QVBoxLayout()
        self.w_container = QWidget()

        self.h_row1_n = QHBoxLayout()
        self.w_row1_n = QWidget()
        self.h_row2_n = QHBoxLayout()
        self.w_row2_n = QWidget()
        self.h_row3_n = QHBoxLayout()
        self.w_row3_n = QWidget()
        self.h_row4_n = QHBoxLayout()
        self.w_row4_n = QWidget()
        self.v_container_n = QVBoxLayout()
        self.w_container_n = QWidget()

        self.h_row1_s = QHBoxLayout()
        self.w_row1_s = QWidget()
        self.h_row2_s = QHBoxLayout()
        self.w_row2_s = QWidget()
        self.h_row3_s = QHBoxLayout()
        self.w_row3_s = QWidget()
        self.h_row4_s = QHBoxLayout()
        self.w_row4_s = QWidget()
        self.v_container_s = QVBoxLayout()
        self.w_container_s = QWidget()

        self.general_widget_letters = QWidget()
        self.general_widget_numbers = QWidget()
        self.general_widget_symbols = QWidget()
        self.general_container = QStackedLayout()

        self.button_caps_lock = QPushButton()
        self.button_caps_lock.setIcon(QIcon(self.path+'ic_capslock.png'))
        self.button_caps_lock.setIconSize(
            QSize(self.buttons_size[0], self.buttons_size[1]))
        self.button_caps_lock.pressed.connect(self.pressed_caps_lock)
        self.button_caps_lock.released.connect(self.released_caps_lock)

        self.button_letters = QPushButton("ABC")
        self.button_letters.pressed.connect(self.pressed_letters)
        self.button_letters.released.connect(self.released_letters)

        self.button_letters2 = QPushButton("ABC")
        self.button_letters2.pressed.connect(self.pressed_letters)
        self.button_letters2.released.connect(self.released_letters)

        self.button_letters3 = QPushButton("ABC")
        self.button_letters3.pressed.connect(self.pressed_letters)
        self.button_letters3.released.connect(self.released_letters)

        self.button_letters4 = QPushButton("ABC")
        self.button_letters4.pressed.connect(self.pressed_letters)
        self.button_letters4.released.connect(self.released_letters)

        self.button_numbers = QPushButton("&123")
        self.button_numbers.pressed.connect(self.pressed_numbers)
        self.button_numbers.released.connect(self.released_numbers)

        self.button_numbers2 = QPushButton("&123")
        self.button_numbers2.pressed.connect(self.pressed_numbers)
        self.button_numbers2.released.connect(self.released_numbers)

        self.button_numbers3 = QPushButton("&123")
        self.button_numbers3.pressed.connect(self.pressed_numbers)
        self.button_numbers3.released.connect(self.released_numbers)

        self.button_symbols = QPushButton("#+=")
        self.button_symbols.pressed.connect(self.pressed_symbols)
        self.button_symbols.released.connect(self.released_symbols)

        self.button_symbols2 = QPushButton("#+=")
        self.button_symbols2.pressed.connect(self.pressed_symbols)
        self.button_symbols2.released.connect(self.released_symbols)

        self.style_on = """
                    border:0px;
                    color: white;
                    background-color: rgb(0,187,255);
                """
        self.style_off = """
                   border: 0px;
                   border-color: white;
                   color: white;
                   background-color: rgb(37,43,52);
               """


        self.init_ui()

    def init_ui(self):
        self.set_up_keyboard_keys()
        self.set_up_keyboard_numbers_keys()
        self.set_up_keyboard_symbols_keys()
        self.set_up_keyboard_on()
        self.set_up_keyboard_off()
        self.set_up_keyboard()
        self.set_up_keyboard_numbers()
        self.set_up_keyboard_symbols()
        self.set_up_layout()
        self.set_up_layout_numbers()
        self.set_up_layout_symbols()

    def set_up_keyboard_keys(self):

        row_1 = [Qt.Key_Q, Qt.Key_W, Qt.Key_E, Qt.Key_R, Qt.Key_T, Qt.Key_Y,
                 Qt.Key_Y, Qt.Key_I, Qt.Key_O, Qt.Key_P, Qt.Key_Backspace]
        row_2 = [Qt.Key_A, Qt.Key_S, Qt.Key_D, Qt.Key_F, Qt.Key_G, Qt.Key_H,
                 Qt.Key_J, Qt.Key_K, Qt.Key_L, Qt.Key_Ccedilla, Qt.Key_Return]
        row_3 = [Qt.Key_Aring, Qt.Key_Z, Qt.Key_X, Qt.Key_C, Qt.Key_V,
                 Qt.Key_B, Qt.Key_N, Qt.Key_M, Qt.Key_Comma, Qt.Key_Period,
                 Qt.Key_Question, Qt.Key_Aring]
        row_4 = [Qt.Key_Aring, Qt.Key_Space,
                 Qt.Key_Left, Qt.Key_Right, Qt.Key_Aring]
        self.keyboard_keys = [row_1, row_2, row_3, row_4]

    def set_up_keyboard_numbers_keys(self):
        row_1 = [Qt.Key_1, Qt.Key_2, Qt.Key_3, Qt.Key_4, Qt.Key_5, Qt.Key_6,
                 Qt.Key_7, Qt.Key_8, Qt.Key_9, Qt.Key_0, Qt.Key_Backspace]

        row_2 = [Qt.Key_Minus, Qt.Key_Slash, Qt.Key_Colon, Qt.Key_Semicolon,
                 Qt.Key_ParenLeft, Qt.Key_ParenRight, Qt.Key_Dollar,
                 Qt.Key_Ampersand, Qt.Key_At, Qt.Key_Return]

        row_3 = [Qt.Key_Aring, Qt.Key_Period, Qt.Key_Comma, Qt.Key_Question,
                 Qt.Key_Exclam, Qt.Key_QuoteLeft, Qt.Key_QuoteDbl,
                 Qt.Key_Aring]

        row_4 = [Qt.Key_Aring, Qt.Key_Space, Qt.Key_Aring, Qt.Key_Aring]

        self.keyboard_numbers_keys = [row_1, row_2, row_3, row_4]

    def set_up_keyboard_symbols_keys(self):
        row_1 = [Qt.Key_BracketLeft, Qt.Key_BracketRight, Qt.Key_BraceLeft,
                 Qt.Key_BraceRight, Qt.Key_Aring, Qt.Key_Percent,
                 Qt.Key_Dead_Circumflex, Qt.Key_Asterisk, Qt.Key_Plus,
                 Qt.Key_Equal, Qt.Key_Backspace]

        row_2 = [Qt.Key_Underscore, Qt.Key_Backslash, Qt.Key_Aring,
                 Qt.Key_Dead_Tilde, Qt.Key_Less, Qt.Key_Greater,
                 Qt.Key_Aring, Qt.Key_Aring, Qt.Key_Aring, Qt.Key_Return]

        row_3 = [Qt.Key_Aring, Qt.Key_Period, Qt.Key_Comma, Qt.Key_Question,
                 Qt.Key_Exclam, Qt.Key_QuoteLeft, Qt.Key_QuoteDbl,
                 Qt.Key_Aring]

        row_4 = [Qt.Key_Aring, Qt.Key_Space, Qt.Key_Aring, Qt.Key_Aring]

        self.keyboard_symbols_keys = [row_1, row_2, row_3, row_4]

    def set_up_keyboard_on(self):
        row_1 = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'backspace']
        row_2 = ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'ç', 'Enter']
        row_3 = ['z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '?', 'A▲']
        row_4 = ['&123', ' ', '◄', '►', 'KB']
        self.keyboard_on = [row_1, row_2, row_3, row_4]

        row_1 = ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', 'backspace']
        row_2 = ['A', 'S', 'D', 'F', 'G', 'H', 'K', 'L', 'L', 'Ç', 'Enter']
        row_3 = ['Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', '?', 'A▲']
        row_4 = ['&123', ' ', '◄', '►', 'KB']
        self.keyboard_on_upper = [row_1, row_2, row_3, row_4]

        row_1 = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'backspace']
        row_2 = ['-', '/', ':', ';', '(', ')', '$', "&&", '@', 'Enter']
        row_3 = ['#+=', '.', ',', '?', '!', "'", '"', '#+=']
        row_4 = ['ABC', ' ', 'ABC', 'KB']
        self.keyboard_numbers_on = [row_1, row_2, row_3, row_4]

        row_1 = ['[', ']', '{', '}', '#', '%', '^', '*', '+', '=', 'backspace']
        row_2 = ['_', "\\", '|', '~', '<', '>', '§', "£", '¥', 'Enter']
        row_3 = ['&123', '.', ',', '?', '!', "'", '"', '&123']
        row_4 = ['ABC', ' ', 'ABC', 'KB']
        self.keyboard_symbols_on = [row_1, row_2, row_3, row_4]

    def set_up_keyboard_off(self):
        row_1 = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p',
                 'ic_backspace']
        row_2 = ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'ç', 'Enter']
        row_3 = ['A▲', 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '?', ]
        row_4 = ['&123', ' ', 'ic_arrow_left', 'ic_arrow_right', 'ic_keyboard']
        self.keyboard_off = [row_1, row_2, row_3, row_4]

        row_1 = ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P',
                 'ic_backspace']
        row_2 = ['A', 'S', 'D', 'F', 'G', 'H', 'K', 'L', 'L', 'Ç', 'Enter']
        row_3 = ['A▲', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', '?', ]
        row_4 = ['&123', ' ', 'ic_arrow_left', 'ic_arrow_right', 'ic_keyboard']
        self.keyboard_off_upper = [row_1, row_2, row_3, row_4]

        row_1 = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
                 'ic_backspace']
        row_2 = ['-', '/', ':', ';', '(', ')', '$', "&&", '@', 'Enter']
        row_3 = ['#+=', '.', ',', '?', '!', "'", '"', '#+=']
        row_4 = ['ABC', ' ', 'ABC', 'ic_keyboard']
        self.keyboard_numbers_off = [row_1, row_2, row_3, row_4]

        row_1 = ['[', ']', '{', '}', '#', '%', '^', '*', '+', '=',
                 'ic_backspace']
        row_2 = ['_', "\\", '|', '~', '<', '>', '§', "£", '¥', 'Enter']
        row_3 = ['&123', '.', ',', '?', '!', "'", '"', '&123']
        row_4 = ['ABC', ' ', 'ABC', 'ic_keyboard']
        self.keyboard_symbols_off = [row_1, row_2, row_3, row_4]

    def set_up_keyboard(self):

        self.keyboard = []

        normal_size = [int(50*self.proportion), int(50*self.proportion)]
        space_size = [int(350*self.proportion), int(50*self.proportion)]
        enter_size = [int(90*self.proportion), int(50*self.proportion)]
        backspace_size = [int(100*self.proportion), int(50*self.proportion)]

        _size = [int(50*self.proportion), int(50*self.proportion)]

        style = """
                    border: 0px;
                    border-color: white;
                    color: white;
                    background-color: rgb(37,43,52);
                """

        self.button_caps_lock.setFixedSize(normal_size[0],
                                           normal_size[1])
        self.button_caps_lock.setStyleSheet(style)

        self.button_numbers.setFixedSize(normal_size[0],
                                         normal_size[1])
        self.button_numbers.setStyleSheet(style)

        self.button_numbers2.setFixedSize(normal_size[0],
                                          normal_size[1])
        self.button_numbers2.setStyleSheet(style)

        self.button_numbers3.setFixedSize(normal_size[0],
                                          normal_size[1])
        self.button_numbers3.setStyleSheet(style)

        self.button_letters.setFixedSize(normal_size[0],
                                         normal_size[1])
        self.button_letters.setStyleSheet(style)

        self.button_letters2.setFixedSize(normal_size[0],
                                          normal_size[1])
        self.button_letters2.setStyleSheet(style)

        self.button_letters3.setFixedSize(normal_size[0],
                                          normal_size[1])
        self.button_letters3.setStyleSheet(style)

        self.button_letters4.setFixedSize(normal_size[0],
                                          normal_size[1])
        self.button_letters4.setStyleSheet(style)

        self.button_symbols.setFixedSize(normal_size[0],
                                         normal_size[1])
        self.button_symbols.setStyleSheet(style)

        self.button_symbols2.setFixedSize(normal_size[0],
                                          normal_size[1])
        self.button_symbols2.setStyleSheet(style)

        self.button_caps_lock.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_numbers.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_numbers2.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_letters.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_letters2.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_letters3.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_letters4.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_symbols.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_symbols2.setCursor(QCursor(Qt.PointingHandCursor))

        i, j = 0, 0
        for row in self.keyboard_on:
            row_n = []
            j = 0
            for key in row:
                if key == "backspace":
                    _size = backspace_size
                elif key == "Enter":
                    _size = enter_size
                elif key == " ":
                    _size = space_size
                else:
                    _size = normal_size
                if key == "A▲":
                    row_n.append(
                        self.button_caps_lock
                    )
                elif key == "&123":
                    row_n.append(
                        self.button_numbers
                    )
                else:
                    row_n.append(
                        KeyboardKey(
                            """
                                border-width: 5px;
                                border-radius: 5px;
                                border-color: white;
                                color: white;
                                background-color: rgb(37,43,52);
                            """,
                            self.keyboard_on[i][j], self.keyboard_off[i][j],
                            True,
                            _size,
                            self.__receiver,
                            self.keyboard_keys[i][j], self.keyboard_on[i][j]
                        )
                    )

                j += 1
            self.keyboard.append(row_n)
            i += 1

    def set_up_keyboard_numbers(self):

        self.keyboard_numbers = []

        normal_size = [int(50*self.proportion), int(50*self.proportion)]
        space_size = [int(350*self.proportion), int(50*self.proportion)]
        enter_size = [int(90*self.proportion), int(50*self.proportion)]
        backspace_size = [int(100*self.proportion), int(50*self.proportion)]

        _size = [int(50*self.proportion), int(50*self.proportion)]

        i, j = 0, 0
        for row in self.keyboard_numbers_on:
            row_n = []
            j = 0
            for key in row:
                if key == "backspace":
                    _size = backspace_size
                elif key == "Enter":
                    _size = enter_size
                elif key == " ":
                    _size = space_size
                elif key == "ABC":
                    _size = enter_size
                else:
                    _size = normal_size
                if key == "ABC" and j == 0:
                    row_n.append(
                        self.button_letters
                    )
                elif key == "ABC" and j == 2:
                    row_n.append(
                        self.button_letters2
                    )
                elif key == "#+=" and j == 0:
                    row_n.append(
                        self.button_symbols
                    )
                elif key == "#+=" and j == 7:
                    row_n.append(
                        self.button_symbols2
                    )
                else:
                    row_n.append(
                        KeyboardKey(
                            """
                                border-width: 5px;
                                border-color: white;
                                color: white;
                                background-color: rgb(37,43,52);
                            """,
                            self.keyboard_numbers_on[i][j],
                            self.keyboard_numbers_off[i][j],
                            True,
                            _size,
                            self.__receiver,
                            self.keyboard_numbers_keys[i][j],
                            self.keyboard_numbers_on[i][j]
                        )
                    )

                j += 1
            self.keyboard_numbers.append(row_n)
            i += 1

    def set_up_keyboard_symbols(self):

        self.keyboard_symbols = []

        normal_size = [int(50*self.proportion), int(50*self.proportion)]
        space_size = [int(350*self.proportion), int(50*self.proportion)]
        enter_size = [int(90*self.proportion), int(50*self.proportion)]
        backspace_size = [int(100*self.proportion), int(50*self.proportion)]

        _size = [int(50*self.proportion), int(50*self.proportion)]

        i, j = 0, 0
        for row in self.keyboard_symbols_on:
            row_n = []
            j = 0
            for key in row:
                if key == "backspace":
                    _size = backspace_size
                elif key == "Enter":
                    _size = enter_size
                elif key == " ":
                    _size = space_size
                elif key == "ABC":
                    _size = enter_size
                else:
                    _size = normal_size
                if key == "ABC" and j == 0:
                    row_n.append(
                        self.button_letters3
                    )
                elif key == "ABC" and j == 2:
                    row_n.append(
                        self.button_letters4
                    )
                elif key == "&123" and j == 0:
                    row_n.append(
                        self.button_numbers2
                    )
                elif key == "&123" and j == 7:
                    row_n.append(
                        self.button_numbers3
                    )
                else:
                    row_n.append(
                        KeyboardKey(
                            """
                                border-width: 5px;
                                border-color: white;
                                color: white;
                                background-color: rgb(37,43,52);
                            """,
                            self.keyboard_symbols_on[i][j],
                            self.keyboard_symbols_off[i][j],
                            True,
                            _size,
                            self.__receiver,
                            self.keyboard_symbols_keys[i][j],
                            self.keyboard_symbols_on[i][j]
                        )
                    )

                j += 1
            self.keyboard_symbols.append(row_n)
            i += 1

    def set_up_layout(self):
        self.setFixedSize(int(self.size[0] * self.proportion),
                          int(self.size[1] * self.proportion))

        self.v_container.setSpacing(0)
        self.v_container.setContentsMargins(1, 1, 1, 1)

        self.h_row1.setSpacing(2)
        self.h_row2.setSpacing(2)
        self.h_row3.setSpacing(2)
        self.h_row4.setSpacing(2)

        self.h_row1.setContentsMargins(int(40*self.proportion), 15, 0, 0)
        self.h_row2.setContentsMargins(int(50*self.proportion), 0, 0, 0)
        self.h_row3.setContentsMargins(int(75*self.proportion), 0, 0, 0)
        self.h_row4.setContentsMargins(int(90*self.proportion), 0, 0, 15)

        self.general_widget_letters.setLayout(self.v_container)
        self.general_container.addWidget(self.general_widget_letters)
        self.setLayout(self.general_container)
        self.v_container.addWidget(self.w_row1)
        self.v_container.addWidget(self.w_row2)
        self.v_container.addWidget(self.w_row3)
        self.v_container.addWidget(self.w_row4)
        self.w_row1.setLayout(self.h_row1)
        self.w_row2.setLayout(self.h_row2)
        self.w_row3.setLayout(self.h_row3)
        self.w_row4.setLayout(self.h_row4)

        style = """
            QWidget{
                background: rgb(25,30,25,50);
            }
            QPushButton{
                border-width: 5px;
                border-radius: 5px;
                color: white;
                background-color: rgb(0,187,255);
            }

        """
        self.w_row1.setStyleSheet(style)
        self.w_row2.setStyleSheet(style)
        self.w_row3.setStyleSheet(style)
        self.w_row4.setStyleSheet(style)

        for key in self.keyboard[0]:
            self.h_row1.addWidget(key)
        for key in self.keyboard[1]:
            self.h_row2.addWidget(key)
        for key in self.keyboard[2]:
            self.h_row3.addWidget(key)
        for key in self.keyboard[3]:
            self.h_row4.addWidget(key)

        self.h_row1.addStretch(-1)
        self.h_row2.addStretch(-1)
        self.h_row3.addStretch(-1)
        self.h_row4.addStretch(-1)

    def set_up_layout_numbers(self):
        self.setFixedSize(int(self.size[0] * self.proportion),
                          int(self.size[1] * self.proportion))

        self.v_container_n.setSpacing(0)
        self.v_container_n.setContentsMargins(1, 1, 1, 1)

        self.h_row1_n.setSpacing(2)
        self.h_row2_n.setSpacing(2)
        self.h_row3_n.setSpacing(2)
        self.h_row4_n.setSpacing(2)

        self.h_row1_n.setContentsMargins(int(20*self.proportion), 0, 0, 0)
        self.h_row2_n.setContentsMargins(int(25*self.proportion), 0, 0, 0)
        self.h_row3_n.setContentsMargins(int(23*self.proportion), 0, 0, 0)
        self.h_row4_n.setContentsMargins(int(5*self.proportion), 0, 0, 0)
        self.h_row1_n.setAlignment(Qt.AlignCenter)
        self.h_row2_n.setAlignment(Qt.AlignCenter)
        self.h_row3_n.setAlignment(Qt.AlignCenter)
        self.h_row4_n.setAlignment(Qt.AlignCenter)

        self.general_container.addWidget(self.general_widget_numbers)
        self.general_widget_numbers.setLayout(self.v_container_n)

        self.v_container_n.addWidget(self.w_row1_n)
        self.v_container_n.addWidget(self.w_row2_n)
        self.v_container_n.addWidget(self.w_row3_n)
        self.v_container_n.addWidget(self.w_row4_n)
        self.w_row1_n.setLayout(self.h_row1_n)
        self.w_row2_n.setLayout(self.h_row2_n)
        self.w_row3_n.setLayout(self.h_row3_n)
        self.w_row4_n.setLayout(self.h_row4_n)

        style = """
            QWidget{
                background: rgb(25,30,25,100);
            }
            QPushButton{
                border-width: 5px;
                border-radius: 5px;
                color: white;
                background-color: rgb(0,187,255);
            }

        """
        self.w_row1_n.setStyleSheet(style)
        self.w_row2_n.setStyleSheet(style)
        self.w_row3_n.setStyleSheet(style)
        self.w_row4_n.setStyleSheet(style)

        for key in self.keyboard_numbers[0]:
            self.h_row1_n.addWidget(key)
        for key in self.keyboard_numbers[1]:
            self.h_row2_n.addWidget(key)
        for key in self.keyboard_numbers[2]:
            self.h_row3_n.addWidget(key)
        for key in self.keyboard_numbers[3]:
            self.h_row4_n.addWidget(key)

    def set_up_layout_symbols(self):
        self.setFixedSize(int(self.size[0] * self.proportion),
                          int(self.size[1] * self.proportion))

        self.v_container_s.setSpacing(0)
        self.v_container_s.setContentsMargins(1, 1, 1, 1)

        self.h_row1_s.setSpacing(2)
        self.h_row2_s.setSpacing(2)
        self.h_row3_s.setSpacing(2)
        self.h_row4_s.setSpacing(2)

        self.h_row1_s.setContentsMargins(int(20*self.proportion), 0, 0, 0)
        self.h_row2_s.setContentsMargins(int(25*self.proportion), 0, 0, 0)
        self.h_row3_s.setContentsMargins(int(23*self.proportion), 0, 0, 0)
        self.h_row4_s.setContentsMargins(int(5*self.proportion), 0, 0, 0)
        self.h_row1_s.setAlignment(Qt.AlignCenter)
        self.h_row2_s.setAlignment(Qt.AlignCenter)
        self.h_row3_s.setAlignment(Qt.AlignCenter)
        self.h_row4_s.setAlignment(Qt.AlignCenter)

        self.general_container.addWidget(self.general_widget_symbols)
        self.general_widget_symbols.setLayout(self.v_container_s)

        self.v_container_s.addWidget(self.w_row1_s)
        self.v_container_s.addWidget(self.w_row2_s)
        self.v_container_s.addWidget(self.w_row3_s)
        self.v_container_s.addWidget(self.w_row4_s)
        self.w_row1_s.setLayout(self.h_row1_s)
        self.w_row2_s.setLayout(self.h_row2_s)
        self.w_row3_s.setLayout(self.h_row3_s)
        self.w_row4_s.setLayout(self.h_row4_s)

        style = """
            QWidget{
                background: rgb(25,30,25,100);
            }
            QPushButton{
                border-width: 5px;
                border-radius: 5px;
                color: white;
                background-color: rgb(0,187,255);
            }

        """
        self.w_row1_s.setStyleSheet(style)
        self.w_row2_s.setStyleSheet(style)
        self.w_row3_s.setStyleSheet(style)
        self.w_row4_s.setStyleSheet(style)

        for key in self.keyboard_symbols[0]:
            self.h_row1_s.addWidget(key)
        for key in self.keyboard_symbols[1]:
            self.h_row2_s.addWidget(key)
        for key in self.keyboard_symbols[2]:
            self.h_row3_s.addWidget(key)
        for key in self.keyboard_symbols[3]:
            self.h_row4_s.addWidget(key)

    def set_receiver(self, receiver):
        self.__receiver = receiver
        self.update_key_receivers()

    def update_key_receivers(self):
        for row in self.keyboard:
            for key in row:
                if isinstance(key, KeyboardKey):
                    key.set_receiver(self.__receiver)
        for row in self.keyboard_numbers:
            for key in row:
                if isinstance(key, KeyboardKey):
                    key.set_receiver(self.__receiver)
        for row in self.keyboard_symbols:
            for key in row:
                if isinstance(key, KeyboardKey):
                    key.set_receiver(self.__receiver)

    def pressed_caps_lock(self):
        self.button_caps_lock.setStyleSheet(self.style_on)

    def released_caps_lock(self):
        if self.upper_case:
            self.upper_case = False
        else:
            self.upper_case = True
        self.button_caps_lock.setStyleSheet(self.style_off)
        self.update_keyboard()

    def pressed_letters(self):
        self.button_letters.setStyleSheet(self.style_on)
        self.button_letters2.setStyleSheet(self.style_on)
        self.button_letters3.setStyleSheet(self.style_on)
        self.button_letters4.setStyleSheet(self.style_on)

    def released_letters(self):
        self.button_letters.setStyleSheet(self.style_off)
        self.button_letters2.setStyleSheet(self.style_off)
        self.button_letters3.setStyleSheet(self.style_off)
        self.button_letters4.setStyleSheet(self.style_off)
        self.general_container.setCurrentIndex(0)

    def pressed_numbers(self):
        self.button_numbers.setStyleSheet(self.style_on)
        self.button_numbers2.setStyleSheet(self.style_on)
        self.button_numbers3.setStyleSheet(self.style_on)

    def released_numbers(self):
        self.button_numbers.setStyleSheet(self.style_off)
        self.button_numbers2.setStyleSheet(self.style_off)
        self.button_numbers3.setStyleSheet(self.style_off)
        self.general_container.setCurrentIndex(1)

    def pressed_symbols(self):
        self.button_symbols.setStyleSheet(self.style_on)
        self.button_symbols2.setStyleSheet(self.style_on)

    def released_symbols(self):
        self.button_symbols.setStyleSheet(self.style_off)
        self.button_symbols2.setStyleSheet(self.style_off)
        self.general_container.setCurrentIndex(2)

    def update_keyboard(self):
        i, j = 0, 0
        for row in self.keyboard:
            j = 0
            for key in row:
                if isinstance(key, KeyboardKey):
                    if self.upper_case:
                        key.set_str_key(self.keyboard_on_upper[i][j])
                    else:
                        key.set_str_key(self.keyboard_on[i][j])
                j += 1
            i += 1

    def resizeEvent(self, event):
        super(WKeyboard, self).resizeEvent(event)

    def mousePressEvent(self, evt):
        self.selected = True
        self.oldPos = evt.globalPos()
        super(WKeyboard, self).mousePressEvent(evt)

    def mouseMoveEvent(self, evt):
        if self.selected:
            delta = QPoint(evt.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = evt.globalPos()

    def mouseReleaseEvent(self, event):
        self.selected = False
        super(WKeyboard, self).mouseReleaseEvent(event)

    def keyPressEvent(self, event):
        for row in self.keyboard:
            for key in row:
                if isinstance(key, KeyboardKey):
                    if key.get_key() == event.key():
                        key.key_pressed()
        for row in self.keyboard_numbers:
            for key in row:
                if isinstance(key, KeyboardKey):
                    if key.get_key() == event.key():
                        key.key_pressed()
        for row in self.keyboard_symbols:
            for key in row:
                if isinstance(key, KeyboardKey):
                    if key.get_key() == event.key():
                        key.key_pressed()

    def keyReleaseEvent(self, event):
        for row in self.keyboard:
            for key in row:
                if isinstance(key, KeyboardKey):
                    if key.get_key() == event.key():
                        key.key_released2()
        for row in self.keyboard_numbers:
            for key in row:
                if isinstance(key, KeyboardKey):
                    if key.get_key() == event.key():
                        key.key_released2()
        for row in self.keyboard_symbols:
            for key in row:
                if isinstance(key, KeyboardKey):
                    if key.get_key() == event.key():
                        key.key_released2()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec())

