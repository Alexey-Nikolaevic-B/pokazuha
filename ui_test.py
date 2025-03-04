from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSignal
from PyQt5.uic import loadUi
from PyQt5 import QtGui, QtCore
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import*
import matplotlib.pyplot as plt
import re
import threading
import time
import json

from PyQt5.uic import loadUi
import json
from PIL import Image
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

import numpy as np

class TestScreen(QDialog):

    def __init__(self):
        super(TestScreen, self).__init__()
        
        self.test_path = " "
        self.cur_task = 0
        self.image  = ["empty", "img\map.jpg"]
        self.tasks  = ["Английский перевод 1914 года, H. RackhamOn the other hand, we denounce with righteous indignation and dislike men who are so beguiled and demoralized by the charms of pleasure of the moment, so blinded by desire, that they cannot foresee the pain and trouble that are bound to ensue; and equal blame belongs to those who fail in their duty through weakness of will, which is the same as saying through shrinking from toil and pain. These cases are perfectly simple and easy to distinguish. In a free hour, when our power of choice is untrammelled and when nothing prevents our being able to do what we like best, every pleasure is to be welcomed and every pain avoided. But in certain circumstances and owing to the claims of duty or the obligations of business it will frequently occur that pleasures have to be repudiated and annoyances accepted. The wise man therefore always holds in these matters to this principle of selection: he rejects pleasures to secure other greater pleasures, or else he endures pains to avoid worse pains", "Английский перевод 1914 года, H. RackhamOn the other hand, we denounce with righteous indignation and dislike men who are so beguiled and demoralized by the charms of pleasure of the moment, so blinded by desire, that they cannot foresee the pain and trouble that are bound to ensue; and equal blame belongs to those who fail in their duty through weakness of will, which is the same as saying through shrinking from toil and pain. These cases are perfectly simple and easy to distinguish. In a free hour, when our power of choice is untrammelled and when nothing prevents our being able to do what we like best, every pleasure is to be welcomed and every pain avoided. But in certain circumstances and owing to the claims of duty or the obligations of business it will frequently occur that pleasures have to be repudiated and annoyances accepted. The wise man therefore always holds in these matters to this principle of selection: he rejects pleasures to secure other greater pleasures, or else he endures pains to avoid worse pains"]
        self.checks = ["1", "2"]
        self.answers = [["1", "2", "1", "2"], ["1", "2"]]

        self.n = len(self.tasks)
        self.grades = [60, 80, 90]
        self.mark = 2
        self.correct = [0]*10
        
        self.init_ui()

        self.fig, self.ax = plt.subplots(figsize=(5, 5))
        self.fig.patch.set_facecolor((35/256, 38/256, 50/256))
        self.ax.set_facecolor((35/256, 38/256, 50/256))
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.set_frame_on(False)

        self.control_layer = self.pic_widget
        self.control_layer = QGridLayout(self.control_layer)

        radial = FigureCanvas(self.fig)
        self.control_layer.addWidget(radial,0,0)

        self.btn_backward.clicked.connect(lambda: self.update(0))
        self.btn_forward.clicked.connect(lambda: self.update(1))
        self.btn_end_test.clicked.connect(self.endTest)

        self.answ_1.clicked.connect(self.check)
        self.answ_2.clicked.connect(self.check)
        self.answ_3.clicked.connect(self.check)
        self.answ_4.clicked.connect(self.check)
        self.answ_5.clicked.connect(self.check)

    def set_path(self, path):
        self.test_path = path

        with open(self.test_path, encoding='utf-8') as config_file:
            data = json.load(config_file)
        self.image   = data['image']
        self.tasks   = data['tasks']
        self.checks  = data['checks']
        self.answers = data['answers']

        self.renew()

    def endTest(self):
        self.main_frame.hide()
        self.end_frame.show()

        i = self.correct.count(1)

        for i in range(len(self.butttons)):
            if self.butttons[i].isChecked():
                if str(i+1) == self.checks[self.cur_task]:
                    self.correct[self.cur_task] = 1


        i = self.correct.count(1)

        per = i / len(self.tasks) * 100
        self.mark = 2

        if per >= self.grades[2]:
            self.mark = 5
        elif per >= self.grades[1]:
            self.mark = 4
        elif per >= self.grades[0]:
            self.mark = 3

        if self.mark == 2:
            self.setStyleSheet('background-color: rgb(255, 71, 83)')
        if self.mark == 3:
            self.setStyleSheet('background-color: rgb(255, 142, 76)')
        if self.mark == 4:
            self.setStyleSheet('background-color: rgb(255, 230, 85)')
        if self.mark== 5:
            self.setStyleSheet('background-color: rgb(147, 181, 72)')

        # print(self.correct.count(1))

        self.lbl_mark.setText(str(self.mark))
        self.lbl_correct.setText(str(self.correct.count(1)) + " / " + str(len(self.correct)))

    def check(self):
        
        for i in range(len(self.butttons)):
            if self.butttons[i].isChecked():
                if str(i+1) == self.checks[self.cur_task]:
                    self.correct[self.cur_task] = 1

    def update(self, option):
        if (option == 0) and (self.cur_task > 0): 
            self.cur_task = self.cur_task - 1
        if (option == 1) and (self.cur_task < len(self.tasks)-1):
            self.cur_task = self.cur_task + 1

        self.btn_backward.setEnabled(True)
        self.btn_forward.setEnabled(True)
        self.btn_end_test.hide()

        if (self.cur_task < 1):
            self.btn_backward.setEnabled(False)
        if (self.cur_task == len(self.tasks)-1):
            self.btn_forward.setEnabled(False)
            self.btn_end_test.show()

        self.lbl_task.setText("Задание " + str(self.cur_task + 1))
        self.lbl_question.setText(self.tasks[self.cur_task])


        self.group.setExclusive(False)
        for i in range(len(self.butttons)):
            self.butttons[i].setChecked(False)
        self.group.setExclusive(True)


        # IMAGE
        if self.image[self.cur_task] == "empty":
            self.pic_widget.hide()
            pass
        else:
            img = Image.open(self.image[self.cur_task])
            self.ax.set_facecolor((35/256, 38/256, 50/256))

            self.ax.set_xticks([])
            self.ax.set_yticks([])
            self.ax.set_frame_on(False)

            self.ax.imshow(img, extent=[0, 1, 0, 1], aspect='auto')
            self.fig.canvas.draw()

            self.pic_widget.show()

        # QUESTION
            self.lbl_question.setText(self.tasks[self.cur_task])

        # CHECKS
        for i in range(5):
            self.butttons[i].hide()
            self.butttons[i].setChecked(False)

        for i in range(len(self.answers[self.cur_task])):
            self.butttons[i].setText(self.answers[self.cur_task][i])
            self.butttons[i].show()

    def renew(self): 
        self.cur_task = 0

        self.btn_forward.setEnabled(True)

        self.setStyleSheet('background-color: rgb(35,38,50)')
        
        self.btn_backward.setEnabled(False)
        self.btn_end_test.hide()

        self.answ_1.hide()
        self.answ_2.hide()
        self.answ_3.hide()
        self.answ_4.hide()
        self.answ_5.hide()

        self.end_frame.hide()

        self.main_frame.show()

        self.correct = [0]*len(self.tasks)

        # IMAGE
        if self.image[self.cur_task] == "empty":
            self.pic_widget.hide()
            pass
        else:
            img = Image.open(self.image[self.cur_task])
            self.ax.set_facecolor((35/256, 38/256, 50/256))

            self.ax.set_xticks([])
            self.ax.set_yticks([])
            self.ax.set_frame_on(False)

            self.ax.imshow(img, extent=[0, 1, 0, 1], aspect='equal')
            self.fig.canvas.draw()

            self.pic_widget.show()
            # image = self.lbl_image
            # pixmap = QtGui.QPixmap(self.image[self.cur_task])
            # pixmap = pixmap.scaled(500, 500)
            # image.setPixmap(pixmap)
            # image.setScaledContents(True)
            # image.show()

        # print(self.cur_task)
        # print(self.tasks[self.cur_task])
        # QUESTION
        self.lbl_question.setText(self.tasks[self.cur_task])

        # CHECKS
        for i in range(5):
            self.butttons[i].hide()

        for i in range(len(self.answers[self.cur_task])):
            self.butttons[i].setText(self.answers[self.cur_task][i])
            self.butttons[i].show()


    def init_ui(self):
        loadUi('qt/test.ui', self)
        self.setWindowTitle("Тестирование")

        self.btn_backward.hide()
        self.btn_backward.hide()

        self.group = QButtonGroup()
        self.group.addButton(self.answ_1)
        self.group.addButton(self.answ_2)
        self.group.addButton(self.answ_3)
        self.group.addButton(self.answ_4)
        self.group.addButton(self.answ_5)

        self.butttons = [self.answ_1, self.answ_2, self.answ_3, self.answ_4, self.answ_5]

        style_btn = "QPushButton {color: rgb(0, 0, 0); background-color : rgb(200, 200, 200)} QPushButton::hover {background-color: rgb(255, 255, 255)}"
        self.btn_backward.setStyleSheet(style_btn) 
        self.btn_forward.setStyleSheet(style_btn) 
        self.btn_end_test.setStyleSheet(style_btn)