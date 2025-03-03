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
import re
import random

class RabotaScreen(QDialog):
    
    signal_save_posts = pyqtSignal(list)
    signal_goto_main  = pyqtSignal()
    posts = []
    first_save = True

    def __init__(self):
        super(RabotaScreen, self).__init__()
        self.init_ui()

        self.btn_back.clicked.connect(self.goto_main)
        self.btn_save.clicked.connect(self.save)
        self.btn_clear.clicked.connect(self.clear)
        self.btn_add.clicked.connect(self.add_row)
        self.btn_remove.clicked.connect(self.deleteSelectedRow)


    def translate_coordinates(self, y, x):
        new_x = (38*60+13 - 37*60 - 30) / 60 
        new_y = (58*60+14 - 55*60 - 50) / 60 / 4

        # y_range = 38.30 - 36.30  # 200
        # x_range = 59.50 - 51.50  # 800
        
        # # Normalize the coordinates
        # new_y = (float(y) - 36.30) / y_range
        # new_x = (float(x) - 51.50) / x_range
        
        return (new_y, new_x)

    def deleteSelectedRow(self):
        if self.tableWidget.selectedIndexes():
            row = self.tableWidget.currentIndex().row()
        else:
            row = self.tableWidget.rowCount() - 1
        if row >= 0:
            self.tableWidget.removeRow(row)    

    def add_row(self):
        rowPosition = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rowPosition)

    def clear(self):
        self.tableWidget.setRowCount(0)
        self.posts = []
        self.first_save = True

    def goto_main(self):
        self.signal_save_posts.emit(self.posts)
        self.signal_goto_main.emit()

    def save(self):

        self.lbl_error.hide()

        if self.first_save:
            self.first_save = False
            self.tableWidget.insertRow(0)

        self.tableWidget.setItem(0, 0, QTableWidgetItem(self.lbl_name.text()))
        self.tableWidget.setItem(0, 1, QTableWidgetItem("0.5"))
        self.tableWidget.setItem(0, 2, QTableWidgetItem("0.5"))
        self.tableWidget.setItem(0, 3, QTableWidgetItem(self.lbl_adrr.text()))
        self.tableWidget.setItem(0, 4, QTableWidgetItem("МГц"))

        self.posts = []

        pattern_1 = re.compile(r'^(\d{2} \d{2})$')

        for i in range(1, self.tableWidget.rowCount()):
            name = ''
            x = ''
            y = ''

            name_cell = self.tableWidget.item(i,0)
            if  name_cell is not None and  name_cell.text() != '':
                name = self.tableWidget.item(i,0).text()
            
            name_x = self.tableWidget.item(i,1)
            if  name_x is not None and  name_x.text() != '':
                x = self.tableWidget.item(i,1).text()

            name_y = self.tableWidget.item(i,2)
            if  name_y is not None and  name_y.text() != '':
                y = self.tableWidget.item(i,2).text()
            
            y = y.replace(',', '.')
            x = x.replace(',', '.')

            y, x = self.translate_coordinates(y, x)
            
            # self.posts.append([x, y, name])
            # if not pattern_1.match(str(x)) or not pattern_1.match(str(y)) or x == '' or y == '':
            #     self.lbl_error.show()
            #     self.posts = []
            #     break

        self.w_progress.show()
        self.frame.hide()

        for x in range(100):
            self.pb_progressBar.setValue(x)

            if x == 10:
                self.lbl_progress.setText("Проверка аппаратных компонентов")
            elif x == 20:
                self.lbl_progress.setText("Проверка учётных данных")
            elif x == 30:
                self.lbl_progress.setText("Калибровка антенных систем")
            elif x == 40:
                self.lbl_progress.setText("Инициализация приёмников")
            elif x == 50:
                self.lbl_progress.setText("Синхронизация с ГЛОНАСС")
            elif x == 95:
                self.lbl_progress.setText("Переход в режим готовности")

            if x < 90: 
                time.sleep(x * random.random() / 1000)
            else:
                time.sleep(0.1)

        self.w_progress.hide()
        self.frame.show()

    def init_ui(self):
        loadUi('qt/rabota.ui', self)
        self.setWindowTitle("Работа")

        self.w_progress.hide()
        self.lbl_error.hide()

        style_btn = "QPushButton {color: rgb(0, 0, 0); background-color : rgb(200, 200, 200)} QPushButton::hover {background-color: rgb(255, 255, 255)}"

        self.btn_clear.setStyleSheet(style_btn)
        self.btn_save.setStyleSheet(style_btn)
        self.btn_add.setStyleSheet(style_btn)
        self.btn_remove.setStyleSheet(style_btn)

        table = self.tableWidget
        table.setStyleSheet("background-color: rgb(255,255,255)")
        table.setRowCount(0)
        
        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)

        delegate = AlignCenter(table)
        table.setItemDelegateForColumn(0, delegate)
        table.setItemDelegateForColumn(1, delegate)
        table.setItemDelegateForColumn(2, delegate)
        table.setItemDelegateForColumn(3, delegate)
        table.setItemDelegateForColumn(4, delegate)



class AlignCenter(QtWidgets.QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(AlignCenter, self).initStyleOption(option, index)
        option.displayAlignment = QtCore.Qt.AlignCenter



