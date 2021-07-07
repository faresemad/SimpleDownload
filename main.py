from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
from sys import argv
from time import sleep
import pafy
import os
import humanize
import requests as r

ui, _ = loadUiType("index.ui")
# https://www.youtube.com/watch?v=2LI2WC5LSQc


class Mainwindow(QWidget, ui, QThread):
    def __init__(self, parent=None):
        super(Mainwindow, self).__init__(parent=parent)
        self.setupUi(self)
        self.selector()
        self.setStyleSheet(open('style.css').read())

    def selector(self):
        # لازم ياخد داتا
        self.pushButton_2.clicked.connect(self.locatePath)
        self.pushButton_2.clicked.connect(self.locatePath)

        self.pushButton.clicked.connect(self.startThread)
        self.linky.setPlaceholderText("Set Your URL")
        self.lineEdit.setPlaceholderText("Set Your Path")

    def vars(self):
        self.link = str(self.linky.text())

    def locatePath(self):
        save_place = QFileDialog.getExistingDirectory(
            self, "Select Download Directory")
        text = str(save_place)
        name = (text[0:].split(',')[0].replace("'", ''))
        self.lineEdit.setText(name)

    def getQuality(self, data):
        self.linky.editingFinished.connect(self.startThread)
        try:
            self.comboBox.addItem(data)
        except:
            pass

    def downUrl(self):
        save_location = self.lineEdit.text()
        quality = self.comboBox.currentIndex()
        self.linkk = str(self.linky.text())
        self.threadStart = get_link(link=self.linkk)
        self.threadStart.dd.connect(self.getQuality)
        self.threadStart.start()
        try:

            st[quality].download(
                filepath=save_location, callback=self.progrss, quiet=True, remux_audio=False)
            self.linky.setText("")
            self.lineEdit.setText("")
            self.comboBox.clear()
            self.progressBar.setValue(0)
        except:
            pass

    def startThread(self):
        self.linkk = str(self.linky.text())
        self.threadStart = get_link(link=self.linkk)
        self.threadStart.dd.connect(self.getQuality)
        self.threadStart.start()


class get_link(QThread):
    link = pyqtSignal(str)
    dd = pyqtSignal(str)

    # اكتب هنا المتغيرات
    def __init__(self, link):
        QThread.__init__(self)
        self.link = link

    def run(self):
        video = pafy.new(self.link)
        st = video.allstreams
        for s in st:
            size = humanize.naturalsize(s.get_filesize())
            data = f"{s.mediatype}  {s.extension}  {s.quality} {size}"
            self.dd.emit(data)

    def progrss(self, total, recvd, ratio, rate, eta):
        prectage = (recvd * 100) / total
        self.progressBar.setValue(prectage)


app = QApplication(argv)
myapp = Mainwindow()
myapp.show()
app.exec_()
