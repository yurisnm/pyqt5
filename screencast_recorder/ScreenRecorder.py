import os
import shutil
import subprocess

from pathlib import Path
from subprocess import check_output, PIPE

import sys

from PyQt5.QtCore import QDir
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QWidget, QHBoxLayout, \
    QLabel

class Recorder(QWidget):

    img_path = "image00001.png"

    def __init__(self):
        super(Recorder, self).__init__()

        self.setWindowFlags(Qt.CustomizeWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.layout_outer = QVBoxLayout()
        self.widget_inner = QWidget()
        self.layout_inner = QVBoxLayout()
        self.layout_bar = QHBoxLayout()
        self.layout_timer = QHBoxLayout()
        self.layout_btns = QHBoxLayout()

        self.widget_inner.setLayout(self.layout_inner)
        self.layout_outer.addWidget(self.widget_inner)

        self.layout_inner.addLayout(self.layout_bar)
        self.layout_inner.addStretch(-1)
        self.layout_inner.addLayout(self.layout_timer)
        self.layout_inner.addLayout(self.layout_btns)

        self.setLayout(self.layout_outer)

        self.style = """
            .QWidget{
                background-color: #080f1c;
                border-radius: 10px;
            }
        """

        self.screencast_number = 0

        self.widget_inner.setStyleSheet(self.style)

        self.init_bar()
        self.init_timer()
        self.init_buttons()
        self.setFixedWidth(self.btn_size.width()*3+50)

        self.dir_name = "."


    def init_bar(self):
        self.btn_close = QPushButton("x")
        self.btn_close.clicked.connect(self.close_recorder)
        self.btn_close.setStyleSheet("""
            color: white;
            background-color: red;
            border: 0px;
            font-size: 12px;
            text-align: center;
            border-radius: 5px;
        """)
        self.btn_close.setFixedSize(QSize(30,18))

        self.btn_file = QPushButton("... /")
        self.btn_file.clicked.connect(self.choose_dir)
        self.btn_file.setStyleSheet("""
                    color: white;
                    background-color: gray;
                    border: 0px;
                    font-size: 10px;
                    text-align: center;
                    border-radius: 5px;
                """)
        self.btn_file.setFixedSize(QSize(210, 18))
        self.btn_file.setContentsMargins(0,0,0,0)

        self.layout_bar.addWidget(self.btn_file)
        self.layout_bar.addStretch(-1)
        self.layout_bar.addWidget(self.btn_close)

    def init_timer(self):
        self.interval_timer = 10
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time_elapsed)
        self.hours_elapsed = 0
        self.mins_elapsed = 0
        self.segs_elapsed = 0
        self.msegs_elapsed = 0
        self.lbl_time_elapsed = QLabel()
        self.update_timer_elapsed()

        self.lbl_time_elapsed.setFixedSize(QSize(100, 30))
        self.lbl_time_elapsed.setStyleSheet("""
            color: white;
            background-color: #080f1c;
        """)
        self.layout_timer.addWidget(self.lbl_time_elapsed)
        self.layout_timer.addStretch(-1)

    def init_buttons(self):

        self.btn_size = QSize(80, 30)

        self.btn_media_style = """
            QPushButton{
                background: #080f1c;
            }
            QPushButton::disabled{
                color: #999999
            }
            QPushButton::enabled{
                color: #4286f4;
            }
        """
        self.btn_record_style = """
            QPushButton{
                background: #080f1c;
            }
            QPushButton::disabled{
                color: #999999
            }
            QPushButton::enabled{
                color: red;
            }
        """

        self.btn_record = QPushButton("◉")
        self.btn_record.clicked.connect(self.record)
        self.btn_record.setStyleSheet(self.btn_record_style)
        self.btn_record.setFixedSize(self.btn_size)

        self.btn_resume = QPushButton("►")
        self.btn_resume.clicked.connect(self.resume)
        self.btn_resume.setStyleSheet(self.btn_media_style)
        self.btn_resume.setFixedSize(self.btn_size)

        self.btn_pause = QPushButton("||")
        self.btn_pause.clicked.connect(self.pause)
        self.btn_pause.setStyleSheet(self.btn_media_style)
        self.btn_pause.setFixedSize(self.btn_size)

        self.btn_stop = QPushButton("◼")
        self.btn_stop.clicked.connect(self.stop)
        self.btn_stop.setStyleSheet(self.btn_media_style)
        self.btn_stop.setFixedSize(self.btn_size)

        self.layout_btns.addWidget(self.btn_record)
        self.layout_btns.addWidget(self.btn_pause)
        self.layout_btns.addWidget(self.btn_resume)
        self.layout_btns.addWidget(self.btn_stop)
        self.layout_btns.addStretch(-1)
        self.btn_pause.hide()
        self.btn_resume.setDisabled(True)
        self.btn_stop.setDisabled(True)

    def record(self):
        self.timer.start(self.interval_timer)
        self.btn_record.setDisabled(True)
        self.btn_pause.show()
        self.btn_pause.setDisabled(False)
        self.btn_stop.show()
        self.btn_stop.setDisabled(False)
        self.btn_resume.hide()
        self.btn_resume.setDisabled(True)

        if not os.path.exists("video_temp"):
            os.makedirs("video_temp")
        # self.thread_recorder.start()
        # while Path("video_temp/output%05d.mkv"%self.count).is_file():
        #     self.count+=1
        self.count_temp = 0
        self.command = "ffmpeg -thread_queue_size 512 -video_size 1920x1080 -framerate 25 -f x11grab -i :0.0+0,0 video_temp/output%05d.mkv"%self.count_temp
        self.record_process = subprocess.Popen(self.command.split(" "), stdout=PIPE, stdin=PIPE)
        self.list_videos = open('video_temp/mylist.txt', 'w')
        self.list_videos.write("file 'output%05d.mkv'" % self.count_temp)
        self.list_videos.write('\n')
        self.paused = False


    def resume(self):
        self.timer.start(self.interval_timer)
        self.btn_resume.hide()
        self.btn_pause.show()
        self.btn_pause.setDisabled(False)
        self.btn_stop.show()
        self.btn_stop.setDisabled(False)
        while Path("video_temp/output%05d.mkv"%self.count_temp).is_file():
            self.count_temp+=1
        self.command = "ffmpeg -thread_queue_size 512 -video_size 1920x1080 -framerate 25 -f x11grab -i :0.0+0,0 video_temp/output%05d.mkv" % self.count_temp
        self.record_process = subprocess.Popen(self.command.split(" "),
                                               stdout=PIPE, stdin=PIPE)
        self.list_videos.write("file 'output%05d.mkv'" % self.count_temp)
        self.list_videos.write('\n')
        self.paused = False

    def pause(self):
        self.timer.stop()
        self.btn_pause.hide()
        self.btn_resume.show()
        self.btn_resume.setDisabled(False)
        # self.btn_stop.setDisabled(True)

        self.record_process.communicate(b'q')
        self.paused = True

    def stop(self):
        self.btn_pause.setDisabled(True)
        self.btn_pause.hide()
        self.btn_resume.setDisabled(True)
        self.btn_resume.show()
        self.btn_stop.setDisabled(True)
        self.btn_stop.show()
        self.btn_record.setDisabled(False)
        self.reset_timer()
        if not self.paused:
            self.record_process.communicate(b'q')
        self.list_videos.close()
        self.count = 0
        while Path("output%05d.mkv"%self.count).is_file():
            self.count+=1
        self.command = "ffmpeg -f concat -safe 0 -i video_temp/mylist.txt -c copy "+self.dir_name+"/output%05d.mkv"%self.count
        subprocess.call(self.command.split(" "))
        shutil.rmtree("video_temp")


        # command = ""
        # call(command.split(" "))
        # self.thread_recorder.terminate()
        # call(['ffmpeg', '-video_size', '1024x768', '-framerate', '25', '-f', 'x11grab', '-i', ':0.0+100,200', 'output.mp4'])
        # call(['ffmpeg', '-f', 'image2', '-r', '30', '-i', '/home/epson/INTERACT/interact-ii/examples/recorder/image%09d.png',
        #       '-vcodec', 'libx264', '-y', '/home/epson/INTERACT/interact-ii/examples/recorder/movie'+str(self.screencast_number)+'.mp4'])

        self.screencast_number+=1

    def get_pid(self, name):
        return check_output(["pidof",'-s', name])

    def update_time_elapsed(self):
        self.msegs_elapsed += 1
        if self.msegs_elapsed>=100:
            self.segs_elapsed += 1
            self.msegs_elapsed=0

        if self.segs_elapsed >= 60:
            self.mins_elapsed += 1
            self.segs_elapsed = 0
            self.msegs_elapsed = 0

        if self.mins_elapsed>=60:
            self.hours_elapsed += 1
            self.mins_elapsed = 0
            self.segs_elapsed = 0
            self.msegs_elapsed = 0
        self.update_timer_elapsed()

    def reset_timer(self):
        self.timer.stop()
        self.hours_elapsed = 0
        self.mins_elapsed = 0
        self.segs_elapsed = 0
        self.msegs_elapsed = 0
        self.update_timer_elapsed()

    def close_recorder(self):
        self.btn_record.show()
        self.btn_resume.show()
        self.btn_stop.show()
        self.btn_pause.hide()
        self.btn_record.setDisabled(False)
        self.btn_resume.setDisabled(True)
        self.btn_stop.setDisabled(True)
        self.reset_timer()
        self.close()

    def choose_dir(self):
        self.dir_name = QFileDialog.getExistingDirectory(self, 'Select Directory')

        if self.dir_name:
            self.btn_file.setText(self.dir_name)

    def update_timer_elapsed(self):
        self.lbl_time_elapsed.setText("%02d:%02d:%02d:%02d"%(
            self.hours_elapsed,
            self.mins_elapsed,
            self.segs_elapsed,
            self.msegs_elapsed
        ))

    def mousePressEvent(self, q_mouse_event):
        self.start = self.mapToGlobal(q_mouse_event.pos())
        self.pressing = True

    def mouseMoveEvent(self, q_mouse_event):
        if self.pressing:
            self.end = self.mapToGlobal(q_mouse_event.pos())
            self.delta = self.mapToGlobal(self.end-self.start)
            self.setGeometry(self.delta.x(),self.delta.y(),
                             self.width(),self.height())
            self.start = self.end

    def mouseReleaseEvent(self, q_mouse_event):
        self.pressing = False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    recorder = Recorder()
    recorder.show()
    sys.exit(app.exec())

