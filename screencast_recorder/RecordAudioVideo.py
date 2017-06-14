
import subprocess
from subprocess import check_output, PIPE

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget
from sounddevice import sleep

class Widget(QWidget):

    def __init__(self):
        super(Widget, self).__init__()
        self.command_v = "ffmpeg -thread_queue_size 512 -video_size 1920x1080 -framerate 25 -f x11grab -i :0.0+0,0 output.mkv"
        self.command_a = "ffmpeg -f alsa -i plughw:CARD=VX5500,DEV=0 output.mp3"

        self.btn_record = QPushButton("Record")
        self.btn_record.clicked.connect(self.record)
        self.btn_stop = QPushButton("Stop")
        self.btn_stop.clicked.connect(self.stop)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.btn_record)
        self.layout.addWidget(self.btn_stop)
        self.setLayout(self.layout)

    def record(self):
        self.record_v = subprocess.Popen(self.command_v.split(" "), stdout=PIPE,
                                    stdin=PIPE)
        self.record_a = subprocess.Popen(self.command_a.split(" "), stdout=PIPE,
                                    stdin=PIPE)

    def stop(self):
        self.record_v.communicate(b'q')
        self.record_a.communicate(b'q')
        self.command_concat = """ffmpeg -i output.mkv -i output.mp3 -c:v copy -c:a aac -strict experimental output_final.mkv"""
        subprocess.call(self.command_concat.split(" "))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget()
    widget.show()
    sys.exit(app.exec_())



