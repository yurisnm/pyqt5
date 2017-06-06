import os
import sys

from PyQt5.QtCore import QObject
from PyQt5.QtCore import QProcess
from PyQt5.QtCore import QProcessEnvironment
from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget


os.environ["QT5DIR"] = "/home/epson/Qt/5.8/gcc_64"
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = "/home/epson/Qt/5.8/gcc_64/plugins/platforms"
os.environ["QT_PLUGIN_PATH"] = "/home/epson/Qt/5.8/gcc_64/plugins"
os.environ["QML_IMPORT_PATH"] = "/home/epson/Qt/5.8/gcc_64/qml"
os.environ["QML2_IMPORT_PATH"] = "/home/epson/Qt/5.8/gcc_64/qml"
os.environ["QT_VIRTUALKEYBOARD_LAYOUT_PATH"] = "/home/epson/Qt/5.8/Src/qtvirtualkeyboard/src/virtualkeyboard/content"
os.environ["QT_VIRTUALKEYBOARD_STYLE"] = "custom"

os.environ["QT_IM_MODULE"] = "qtvirtualkeyboard"

# for i in QProcessEnvironment.systemEnvironment().keys():
#     print(i,"#####",QProcessEnvironment.systemEnvironment().value(i))

class Worker(QObject):
  sendOutput = pyqtSignal(str)

  def __init__(self):
    super(Worker, self).__init__()
    self.process = QProcess()
    self.setupProcess()

  def __del__(self):
    self.process.terminate()
    if not self.process.waitForFinished(10000):
      self.process.kill()

  def setupProcess(self):
    self.process.setProcessChannelMode(QProcess.MergedChannels)
    self.process.readyReadStandardOutput.connect(self.readStdOutput)

    self._envgcc = QProcessEnvironment.systemEnvironment()
    self._envgcc.insert("QT5DIR", "/home/epson/Qt/5.8/gcc_64")
    self._envgcc.insert("QT_QPA_PLATFORM_PLUGIN_PATH",
                        "/home/epson/Qt/5.8/gcc_64/plugins/platforms")
    self._envgcc.insert("QT_PLUGIN_PATH", "/home/epson/Qt/5.8/gcc_64/plugins")
    self._envgcc.insert("QML_IMPORT_PATH", "/home/epson/Qt/5.8/gcc_64/qml")
    self._envgcc.insert("QML2_IMPORT_PATH", "/home/epson/Qt/5.8/gcc_64/qml")
    self._envgcc.insert("QT_VIRTUALKEYBOARD_LAYOUT_PATH",
                        "/home/epson/Qt/5.8/Src/qtvirtualkeyboard/src/virtualkeyboard/content")
    self._envgcc.insert("QT_VIRTUALKEYBOARD_STYLE", "custom")
    self._envgcc.insert("QT_IM_MODULE", "qtvirtualkeyboard")
    self.process.setProcessEnvironment(self._envgcc)
    self.process.start("/home/epson/INTERACT/interact-ii/examples/ProcessExample.py")

  @pyqtSlot()
  def readStdOutput(self):
    output = str(self.process.readAllStandardOutput())
    # Do some extra processing of the output here if required
    # ...
    self.sendOutput.emit(output)



class MyQProcess(QWidget):
  def __init__(self):
   super(QWidget, self).__init__()
   layout = QVBoxLayout()
   self.edit = QTextEdit()
   self.thread = QThread()

   self.setupConnections()

   self.edit.setWindowTitle("QTextEdit Standard Output Redirection")
   layout.addWidget(self.edit)
   self.setLayout(layout)
   self.show()

  def setupConnections(self):
    self.worker = Worker()
    self.thread.finished.connect(self.worker.deleteLater)
    self.worker.sendOutput.connect(self.showOutput)

    self.worker.moveToThread(self.thread)
    self.thread.start()

  def __del__(self):
    if self.thread.isRunning():
      self.thread.quit()
      # Do some extra checking if thread has finished or not here if you want to

  #Define Slot Here
  @pyqtSlot(str)
  def showOutput(self, output):
    #self.edit.clear()
    self.edit.append(output)


def main():
    app = QApplication(sys.argv)
    w   = MyQProcess()

    return app.exec_()

if __name__ == '__main__':
    main()