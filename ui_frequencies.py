from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import*
from PyQt5.uic import loadUi

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from PyQt5.uic import loadUi

from PyQt5 import QtWidgets
from PyQt5 import QtCore

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

import numpy as np
import json

import sys, os
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class FrequenciesScreen(QDialog):

    def __init__(self):
        super(FrequenciesScreen, self).__init__()
        self.init_ui()

        self.perehavat = []

    def set_peleng(self, perehavat):
        # self.pelengs = []
        self.perehavat.append(perehavat)
        self.perehavat = [list(t) for t in set(tuple(sublist) for sublist in self.perehavat)]

        # print(self.perehavat)
        # print(self.freq)

        self.t_zapret_2.setRowCount(self.zapret_n)

        for perehavat in self.perehavat:
            if not (str(int(perehavat[3])) in self.freq):
                rowPosition = self.t_zapret_2.rowCount()
                self.t_zapret_2.insertRow(rowPosition)
                self.t_zapret_2.setItem(rowPosition, 0, QTableWidgetItem(str(perehavat[3])))

    def set_perehvat(self):
        self.t_zapret_2.setRowCount(0)

        with open(resource_path("data/perehvat.json"), encoding='utf-8') as config_file:
            data = json.load(config_file)
        freq = data['freq']
        mod = data['mod']

        self.zapret_n = len(freq)

        for i in range(len(freq)):
            rowPosition = self.t_zapret_2.rowCount()
            self.t_zapret_2.insertRow(rowPosition)
            self.t_zapret_2.setItem(rowPosition, 0, QTableWidgetItem(str(freq[i])))
            self.t_zapret_2.setItem(rowPosition, 1, QTableWidgetItem(str(mod[i])))

    def set_control(self):
        self.t_control.setRowCount(0)

        with open(resource_path("data/control.json"), encoding='utf-8') as config_file:
            data = json.load(config_file)
        self.freq = data['freq']
        self.mod = data['mod']

        for i in range(len(self.freq)):
            rowPosition = self.t_control.rowCount()
            self.t_control.insertRow(rowPosition)
            self.t_control.setItem(rowPosition, 0, QTableWidgetItem(str(self.freq[i])))
            self.t_control.setItem(rowPosition, 1, QTableWidgetItem(str(self.mod[i])))

    def init_ui(self):
        loadUi(resource_path('qt/frequencies.ui'), self)
        self.setWindowTitle("Частоты")

        self.set_control()
        self.set_perehvat()

        table_zapret = self.t_zapret_2
        table_zapret.setStyleSheet("background-color: rgb(255,255,255)")
        
        header = table_zapret.horizontalHeader()
        # header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

        delegate = AlignCenter(table_zapret)
        table_zapret.setItemDelegateForColumn(0, delegate)
        table_zapret.setItemDelegateForColumn(1, delegate)

        table_control = self.t_control
        table_control.setStyleSheet("background-color: rgb(255,255,255)")
        # table_control.setRowCount(20)
        
        header = table_control.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

        delegate = AlignCenter(table_control)
        table_control.setItemDelegateForColumn(0, delegate)
        table_control.setItemDelegateForColumn(1, delegate) 
        
        style_btn = "QPushButton {color: rgb(0, 0, 0); background-color : rgb(200, 200, 200)} QPushButton::hover {background-color: rgb(255, 255, 255)}"

        self.btn_clear_1.setStyleSheet(style_btn)
        self.btn_clear_2.setStyleSheet(style_btn)

        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        delegate = AlignJustify(self.t_zapret_2)
        self.t_zapret_2.setItemDelegateForColumn(1, delegate)

class AlignJustify(QtWidgets.QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(AlignJustify, self).initStyleOption(option, index)
        option.displayAlignment = QtCore.Qt.AlignJustify

class AlignCenter(QtWidgets.QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(AlignCenter, self).initStyleOption(option, index)
        option.displayAlignment = QtCore.Qt.AlignCenter

