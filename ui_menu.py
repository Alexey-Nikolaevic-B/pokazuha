from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from PyQt5.QtCore import pyqtSignal

from PyQt5.uic import loadUi

class MenuScreen(QDialog):
    signal_lesson = pyqtSignal(int)

    def __init__(self):
        super(MenuScreen, self).__init__()
        self.init_ui()
        
        self.btn_prac.clicked.connect(lambda: self.choose_lesson(0))
        self.btn_control.clicked.connect(lambda: self.choose_lesson(1))
        self.btn_analysis.clicked.connect(lambda: self.choose_lesson(2))

    def choose_lesson(self, lesson):
        self.signal_lesson.emit(lesson)

    def init_ui(self):
        loadUi('qt/menu.ui', self)
        self.setFixedWidth(980)
        self.setFixedHeight(340)

        style_btn = "QPushButton {color: rgb(0, 0, 0); font: 20pt \"MS Shell Dlg 2\"; background-color : rgb(200, 200, 200)} QPushButton::hover {background-color: rgb(255, 255, 255)}"
        self.btn_prac.setStyleSheet(style_btn)
        self.btn_control.setStyleSheet(style_btn)
        self.btn_analysis.setStyleSheet(style_btn)