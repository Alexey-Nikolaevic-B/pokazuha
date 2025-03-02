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

import time
import random

class RabotaScreen(QDialog):
    
    signal_goto_main = pyqtSignal()

    def __init__(self):
        super(RabotaScreen, self).__init__()
        self.init_ui()

        self.btn_back.clicked.connect(self.goto_main)
        self.btn_save.clicked.connect(self.progress)


    def goto_main(self):
        self.signal_goto_main.emit()

    def progress(self):

        self.tableWidget.insertRow(0)
        self.tableWidget.setItem(0, 0, QTableWidgetItem(self.lbl_name.text()))
        self.tableWidget.setItem(0, 1, QTableWidgetItem(f"{self.lbl_X.text()} ; {self.lbl_X.text()}"))
        self.tableWidget.setItem(0, 2, QTableWidgetItem(self.lbl_adrr.text()))
        self.tableWidget.setItem(0, 3, QTableWidgetItem("МГц"))

        self.w_progress.show()
        self.frame.hide()

        for x in range(100):
            self.pb_progressBar.setValue(x)
            if x < 90: 
                time.sleep(x * random.random() / 1000)
            else:
                time.sleep(0.1)

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
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)

        delegate = AlignCenter(table)
        table.setItemDelegateForColumn(0, delegate)
        table.setItemDelegateForColumn(1, delegate)
        table.setItemDelegateForColumn(1, delegate)
        table.setItemDelegateForColumn(2, delegate)


class AlignCenter(QtWidgets.QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(AlignCenter, self).initStyleOption(option, index)
        option.displayAlignment = QtCore.Qt.AlignCenter



