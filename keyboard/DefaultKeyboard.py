import os
import sys


from PyQt5.QtCore import QProcess
from PyQt5.QtCore import QProcessEnvironment
from PyQt5.QtQuick import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget

# os.environ["QT5DIR"] = "/home/epson/Qt/5.8/gcc_64"
# os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = "/home/epson/Qt/5.8/gcc_64/plugins/platforms"
# os.environ["QT_PLUGIN_PATH"] = "/home/epson/Qt/5.8/gcc_64/plugins"
# os.environ["QML_IMPORT_PATH"] = "/home/epson/Qt/5.8/gcc_64/qml"
# os.environ["QML2_IMPORT_PATH"] = "/home/epson/Qt/5.8/gcc_64/qml"
#
# # os.environ["QT_VIRTUALKEYBOARD_LAYOUT_PATH"] = "/home/epson/Qt/5.8/Src/qtvirtualkeyboard/src/virtualkeyboard/content/layouts/"
# # os.environ["QT_VIRTUALKEYBOARD_STYLE"] = "/home/epson/Qt/5.8/Src/qtvirtualkeyboard/src/virtualkeyboard/content/styles"
# os.environ["QT_IM_MODULE"] = "qtvirtualkeyboard"

os.environ["QT5DIR"] = "/home/epson/Qt/5.8/gcc_64"
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = "home/epson/Qt/5.8/gcc_64/plugins/platforms"
os.environ["QT_PLUGIN_PATH"] = "/home/epson/Qt/5.8/gcc_64/plugins"
os.environ["QML_IMPORT_PATH"] = "/home/epson/Qt/5.8/gcc_64/qml"
os.environ["QML2_IMPORT_PATH"] = "/home/epson/Qt/5.8/gcc_64/qml"
os.environ["QT_IM_MODULE"] = "qtvirtualkeyboard"

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.line_edit = None

        # Procesos
        self.build_process = QProcess(self)
        if not sys.platform.startswith('linux'):
            self._envgcc = QProcessEnvironment.systemEnvironment()
            self._envgcc.insert("QT5DIR", "/home/epson/Qt/5.8/gcc_64")
            self._envgcc.insert("QT_QPA_PLATFORM_PLUGIN_PATH", "/home/epson/Qt/5.8/gcc_64/plugins/platforms")
            self._envgcc.insert("QT_PLUGIN_PATH", "/home/epson/Qt/5.8/gcc_64/plugins")
            self._envgcc.insert("QML_IMPORT_PATH", "/home/epson/Qt/5.8/gcc_64/qml")
            self._envgcc.insert("QML2_IMPORT_PATH", "/home/epson/Qt/5.8/gcc_64/qml")
            self._envgcc.insert("QT_VIRTUALKEYBOARD_LAYOUT_PATH", "/home/epson/INTERACT/interact-ii/basic-b2qt.qml")
            self._envgcc.insert("QT_VIRTUALKEYBOARD_STYLE", "/home/epson/INTERACT/interact-ii/basic-b2qt.qml")
            self._envgcc.insert("QT_IM_MODULE", "qtvirtualkeyboard")
            self.build_process.setProcessEnvironment(self._envgcc)
        self.execution_process = QProcess(self)


        self.init_ui()

    def init_ui(self):
        self.line_edit = QLineEdit()
        self.line_edit2 = QLineEdit()
        self.layout = QVBoxLayout()
        self.main_widget = QWidget()
        self.main_widget.setLayout(self.layout)
        self.layout.addWidget(self.line_edit)
        self.layout.addWidget(self.line_edit2)
        self.setCentralWidget(self.main_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())