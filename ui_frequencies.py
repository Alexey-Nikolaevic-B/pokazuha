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

class FrequenciesScreen(QDialog):

    def __init__(self):
        super(FrequenciesScreen, self).__init__()
        self.init_ui()


    def set_control(self):
        self.t_control.setRowCount(0)

        with open("control.json", encoding='utf-8') as config_file:
            data = json.load(config_file)
        self.freq = data['freq']
        self.mod = data['mod']

        for i in range(len(self.freq)):
            rowPosition = self.t_control.rowCount()
            self.t_control.insertRow(rowPosition)
            self.t_control.setItem(rowPosition, 0, QTableWidgetItem(str(self.freq[i]) + "°"))
            self.t_control.setItem(rowPosition, 1, QTableWidgetItem(str(self.mod[i])))

    def init_ui(self):
        loadUi('qt/frequencies.ui', self)
        self.setWindowTitle("Частоты")

        self.set_control()

        table_zapret = self.t_zapret
        table_zapret.setStyleSheet("background-color: rgb(255,255,255)")
        table_zapret.setRowCount(20)
        
        header = table_zapret.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)

        delegate = AlignCenter(table_zapret)
        table_zapret.setItemDelegateForColumn(0, delegate)

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

class AlignCenter(QtWidgets.QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(AlignCenter, self).initStyleOption(option, index)
        option.displayAlignment = QtCore.Qt.AlignCenter

