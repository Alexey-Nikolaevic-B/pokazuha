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


class PelengScreen(QDialog):

    def __init__(self):
        super(PelengScreen, self).__init__()

        self.found = []

        self.init_ui()

        pelengs = [45, 54, 26, 100]

        self.theta_curcle = np.arange(0, 2*np.pi, 0.1)
        self.r_curcle = [0.1] * len(self.theta_curcle)

        # self.polar_ax = self.fig.add_axes(self.ax.get_position(), projection='polar', frameon=False)
        # self.polar_ax.set_theta_zero_location('N')

        self.fig, self.ax = plt.subplots(subplot_kw={'projection': 'polar'})
        self.fig.patch.set_facecolor((35/256, 38/256, 50/256))
        self.ax.set_facecolor('#232632')



  # Move radial labels away from
        
        radial = FigureCanvas(self.fig)
        self.control_layer.addWidget(radial,0,0)

        self.btn_clear.clicked.connect(self.clear)

        self.plot_()

    def clear(self): 
        self.found = []
        self.plot_()
        self.update_angles()


    def set_found(self, found):
        self.found.append(found)
        self.found = [list(t) for t in set(tuple(sublist) for sublist in  self.found)]
        
        self.update_angles()
        self.plot_()

    def update_angles(self):
        self.tableWidget.setRowCount(0)

        for i in range(len(self.found)):
            rowPosition = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rowPosition)
            self.tableWidget.setItem(rowPosition, 0, QTableWidgetItem(str(self.found[i][1])))
            self.tableWidget.setItem(rowPosition, 1, QTableWidgetItem(str(self.found[i][0])))

    def plot_(self):

        self.ax.clear()

        self.ax.tick_params(axis='x', colors='white')
        self.ax.tick_params(axis='y', colors='white')

        for element in self.found:
            r = np.arange(0.02, 1.01, 0.01)
            theta = [np.deg2rad(element[0])] * len(r)
            self.ax.plot(theta, r, 'k', linewidth=0.5, color='white')

        self.theta_curcle = np.arange(0, 2*np.pi, 0.1)
        self.r_curcle = [0.1] * len(self.theta_curcle)

        self.ax.plot(self.theta_curcle, self.r_curcle, 'k', linewidth=0.5, color='white')
        r_curcle = [0.03] * len(self.theta_curcle)
        self.ax.plot(self.theta_curcle, r_curcle, 'k', linewidth=4,)


        major_ticks = np.linspace(0, 2*np.pi, 24, endpoint=False)
        minor_ticks = np.linspace(0, 2*np.pi, 10, endpoint=False)

        self.ax.set_xticks(major_ticks, minor=False)
        self.ax.set_xticks(minor_ticks, minor=True)

        self.ax.set_rticks([])

        self.ax.set_rmax(1)
        self.ax.grid(False)

        self.ax.set_theta_zero_location("N")
        self.ax.set_theta_direction(-1)
        self.ax.set_rlabel_position(-22.5)
        

        self.fig.canvas.draw()


    def init_ui(self):
        loadUi('qt/peleng.ui', self)
        self.setWindowTitle("Круговая пеленговая панорам")

        self.control_layer = self.Twidget
        self.control_layer = QGridLayout(self.control_layer)   

        table = self.tableWidget
        table.setStyleSheet("background-color: rgb(255,255,255)")
        table.setRowCount(20)
        
        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

        delegate = AlignCenter(table)
        table.setItemDelegateForColumn(0, delegate)
        table.setItemDelegateForColumn(1, delegate) 


        style_btn = "QPushButton {color: rgb(0, 0, 0); background-color : rgb(200, 200, 200)} QPushButton::hover {background-color: rgb(255, 255, 255)}"

        self.btn_clear.setStyleSheet(style_btn)
        self.btn_usr.setStyleSheet(style_btn)
        self.btn_close.setStyleSheet(style_btn)
        self.btn_peleng.setStyleSheet(style_btn)

        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        self.setFixedWidth(800)
        self.setFixedHeight(570)


class AlignCenter(QtWidgets.QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(AlignCenter, self).initStyleOption(option, index)
        option.displayAlignment = QtCore.Qt.AlignCenter

