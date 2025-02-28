from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import*

from PyQt5.uic import loadUi

from PyQt5 import QtWidgets
from PyQt5 import QtCore

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

import numpy as np

import time

class RabotaScreen(QDialog):

    def __init__(self):
        super(RabotaScreen, self).__init__()
        self.init_ui()

        self.btn_save.clicked.connect(self.progress)

    def progress(self):
        self.w_progress.show()
        self.frame.hide()

        for x in range(100):
            self.pb_progressBar.setValue(x)
            time.sleep(0.001)

        self.w_progress.hide()
        self.frame.show()

    def init_ui(self):
        loadUi('qt/rabota.ui', self)

        self.w_progress.hide()

        table = self.tableWidget
        table.setStyleSheet("background-color: rgb(255,255,255)")
        table.setRowCount(20)
        
        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

        delegate = AlignCenter(table)
        table.setItemDelegateForColumn(0, delegate)
        table.setItemDelegateForColumn(1, delegate)


class AlignCenter(QtWidgets.QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(AlignCenter, self).initStyleOption(option, index)
        option.displayAlignment = QtCore.Qt.AlignCenter



