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

import sys, os
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class RabotaScreen(QDialog):
    
    signal_save_posts = pyqtSignal(list)
    signal_goto_main  = pyqtSignal()
    signal_com_pod    = pyqtSignal(int)
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
        if y[3:5] == '00':
            new_y = 0
        else:
            new_y = int(y[0:2])

        if x[3:5] == '00':
            new_x = 0
        else:
            new_x = int(y[0:2])
            
        new_y = (int(y[0:2])*60+int(y[3:5]) - 36*60 - 30) / (60 * 2) 
        new_x = (int(x[0:2])*60+int(x[3:5]) - 51*60 - 50) / (60 * 8)
        
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
        self.tableWidget.setItem(0, 1, QTableWidgetItem("37.30"))
        self.tableWidget.setItem(0, 2, QTableWidgetItem("55.50"))
        self.tableWidget.setItem(0, 3, QTableWidgetItem(self.lbl_adrr.text()))
        self.tableWidget.setItem(0, 4, QTableWidgetItem("УКВ"))

        self.posts = []
        for i in range(1, self.tableWidget.rowCount()):
            name = ''
            x = ''
            y = ''

            name_cell = self.tableWidget.item(i,0)
            if  name_cell is not None and  name_cell.text() != '':
                name = self.tableWidget.item(i,0).text()
            
            name_y = self.tableWidget.item(i,1)
            if  name_y is not None and  name_y.text() != '':
                y = self.tableWidget.item(i,1).text()

            name_x = self.tableWidget.item(i,2)
            if  name_x is not None and  name_x.text() != '':
                x = self.tableWidget.item(i,2).text()

            if not ((str(x)[0:2].isdigit() and 
                     str(x)[0:2] != '00' and 
                     str(x)[3:5].isdigit())
                    and 
                    (str(y)[0:2].isdigit() and 
                     str(y)[0:2] != '00' and 
                     str(y)[3:5].isdigit()) 
                     and 
                    (len(x) == 5 and len(y) == 5)):
                self.lbl_error.show()
                self.posts = []
                break
            else:
                y_posts, x_posts = self.translate_coordinates(y, x)
                self.posts.append([x_posts, y_posts, name])

        for i in range(len(self.butttons)):
            if self.butttons[i].isChecked():
                self.signal_com_pod.emit(i)

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
                time.sleep(0.005)
            else:
                time.sleep(0.005)

        self.w_progress.hide()
        self.frame.show()

    def init_ui(self):
        loadUi(resource_path('qt/rabota.ui'), self)
        self.setWindowTitle("Работа")

        self.group = QButtonGroup()
        self.group.addButton(self.rb_com)
        self.group.addButton(self.rb_pod)

        self.butttons = [self.rb_com, self.rb_pod]

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



