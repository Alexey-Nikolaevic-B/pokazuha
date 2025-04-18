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

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from PyQt5.uic import loadUi
import json
from PIL import Image
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np

import sys, os
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class TestScreen(QDialog):

    def __init__(self):
        super(TestScreen, self).__init__()
        
        self.test_path = " "
        self.cur_task = 0
        self.image  = ["empty", "img\map.jpg"]
        self.tasks  = ["..."]
        self.checks = ["1", "2"]
        self.answers = [["1", "2", "1", "2"], ["1", "2"]]
        self.selected_answers = []

        self.thread_counter = threading.Thread(target=self.counter, daemon=True)

        self.n = len(self.tasks)
        self.grades = [40, 80, 95]
        self.mark = 2
        self.correct = [0]*10
        self.test_sttarted = False
        
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

        self.answ_1.clicked.connect(self.check_singular)
        self.answ_2.clicked.connect(self.check_singular)
        self.answ_3.clicked.connect(self.check_singular)
        self.answ_4.clicked.connect(self.check_singular)
        self.answ_5.clicked.connect(self.check_singular)

        self.checkBox_1.clicked.connect(self.check_multiple)
        self.checkBox_2.clicked.connect(self.check_multiple)
        self.checkBox_3.clicked.connect(self.check_multiple)
        self.checkBox_4.clicked.connect(self.check_multiple)
        self.checkBox_5.clicked.connect(self.check_multiple)

        self.le_answ.textChanged.connect(self.check_text)

    def startTimer(self):
        if self.test_sttarted == False:
            self.thread_counter.start()
            self.test_sttarted = True

    def counter(self):
        while self.c >= 0:
            mins, secs = divmod(self.c, 60) 
            timer = '{:02d}:{:02d}'.format(mins, secs) 
            self.c = self.c - 1
            self.lbl_time.setText(str(timer))

            time.sleep(1)
        self.endTest()

    def set_path(self, path):
        self.test_path = path

        with open(resource_path(self.test_path), encoding='utf-8') as config_file:
            data = json.load(config_file)
        self.c       = data['time']
        self.image   = data['image']
        self.tasks   = data['tasks']
        self.checks  = data['checks']
        self.answers = data['answers']

        self.renew()

    def endTest(self):
        self.main_frame.hide()
        self.le_answ.hide()
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

    def check_text(self):
        if self.answers[self.cur_task][0] == "0":
            input = self.le_answ.text()
            if input in self.checks[self.cur_task]:
                self.correct[self.cur_task] = 1
            else:
                self.correct[self.cur_task] = 0

    def check_singular(self):
        
        for i in range(len(self.butttons)):
            if self.butttons[i].isChecked():
                if str(i+1) == self.checks[self.cur_task]:
                    self.correct[self.cur_task] = 1
                else:
                    self.correct[self.cur_task] = 0


    def check_multiple(self):
        self.selected_answers = []
        for i, checkbox in enumerate(self.buttons_check, start=1):
            if checkbox.isChecked():
                self.selected_answers.append(str(i))  # Convert to string to match your correct answers format
        
        # Check if the selected answers exactly match the correct answers
        if sorted(self.selected_answers) == sorted(self.checks[self.cur_task]):
            self.correct[self.cur_task] = 1
        else:
            self.correct[self.cur_task] = 0

    def update(self, option):
        if (option == 0) and (self.cur_task > 0): 
            self.cur_task = self.cur_task - 1
        if (option == 1) and (self.cur_task < len(self.tasks)-1):
            self.cur_task = self.cur_task + 1

        self.btn_backward.setEnabled(True)
        self.btn_forward.setEnabled(True)
        self.btn_end_test.hide()
        self.le_answ.hide()
        self.frame_3.hide()
        self.check_frame.hide()
        self.selected_answers = []
        
        for chech in self.buttons_check:
            chech.hide()


        input = self.le_answ.clear()

        if (self.cur_task < 1):
            self.btn_backward.setEnabled(False)
        if (self.cur_task == len(self.tasks)-1):
            self.btn_forward.setEnabled(False)
            self.btn_end_test.show()

        self.lbl_task.setText("Вопрос " + str(self.cur_task + 1))
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
            img = Image.open(resource_path(self.image[self.cur_task]))
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

        if self.answers[self.cur_task][0] == "0":
            self.le_answ.show()
            self.frame_3.hide()
        if self.answers[self.cur_task][0] == "1":
            self.frame_3.show()

            for i in range(len(self.answers[self.cur_task][1])):
                self.butttons[i].setText(self.answers[self.cur_task][1][i])
                self.butttons[i].show()

        if self.answers[self.cur_task][0] == "2":
            self.check_frame.show()

            for i in range(len(self.answers[self.cur_task][1])):
                self.buttons_check[i].setText(self.answers[self.cur_task][1][i])
                self.buttons_check[i].show()

    def renew(self):
        self.cur_task = 0

        self.btn_forward.setEnabled(True)

        self.setStyleSheet('background-color: rgb(35,38,50)')
        
        self.btn_backward.setEnabled(True)
        self.btn_end_test.hide()
        self.le_answ.hide()
        self.frame_3.hide()
        self.answ_1.hide()
        self.answ_2.hide()
        self.answ_3.hide()
        self.answ_4.hide()
        self.answ_5.hide()

        self.end_frame.hide()
        self.check_frame.hide()
        self.check_frame.hide()

        self.main_frame.show()

        self.correct = [0]*len(self.tasks)

        # IMAGE
        if self.image[self.cur_task] == "empty":
            self.pic_widget.hide()
            pass
        else:
            img = Image.open(resource_path(self.image[self.cur_task]))
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
                self.butttons[i].setChecked(False)

        if self.answers[self.cur_task][0] == "0":
            self.le_answ.show()
            self.frame_3.hide()
        if self.answers[self.cur_task][0] == "1":
            self.frame_3.show()

            for i in range(len(self.answers[self.cur_task][1])):
                self.butttons[i].setText(self.answers[self.cur_task][1][i])
                self.butttons[i].show()

        if self.answers[self.cur_task][0] == "2":
            self.check_frame.show()

            for i in range(len(self.answers[self.cur_task][1])):
                self.buttons_check[i].setText(self.answers[self.cur_task][1][i])
                self.buttons_check[i].show()


    def init_ui(self):
        loadUi(resource_path('qt/test.ui'), self)
        self.setWindowTitle("Тестирование")

        self.group = QButtonGroup()
        self.group.addButton(self.answ_1)
        self.group.addButton(self.answ_2)
        self.group.addButton(self.answ_3)
        self.group.addButton(self.answ_4)
        self.group.addButton(self.answ_5)

        self.butttons = [self.answ_1, self.answ_2, self.answ_3, self.answ_4, self.answ_5]

        self.group_check = QButtonGroup()
        self.group_check.setExclusive(False)
        self.group_check.addButton(self.checkBox_1)
        self.group_check.addButton(self.checkBox_2)
        self.group_check.addButton(self.checkBox_3)
        self.group_check.addButton(self.checkBox_4)
        self.group_check.addButton(self.checkBox_5)

        self.buttons_check = [self.checkBox_1, self.checkBox_2, self.checkBox_3, self.checkBox_4, self.checkBox_5]


        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        style_btn = "QPushButton {color: rgb(0, 0, 0);  background-color : rgb(200, 200, 200)} QPushButton::hover {background-color: rgb(255, 255, 255)}"
        self.btn_backward.setStyleSheet(style_btn) 
        self.btn_forward.setStyleSheet(style_btn) 
        self.btn_end_test.setStyleSheet(style_btn)