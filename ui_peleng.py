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

        self.fig, self.ax = plt.subplots(figsize=(5, 5))
        self.ax.set_facecolor((1.0, 0.47, 0.42))
        self.fig.patch.set_facecolor((35/256, 38/256, 50/256))
        self.ax.axis('off')  
        self.polar_ax = self.fig.add_axes(self.ax.get_position(), projection='polar', frameon=False)
        self.polar_ax.set_theta_zero_location('N')
        self.polar_ax.set_theta_direction(-1)

        rings = np.linspace(0.15, 1.0, 2)
        self.polar_ax.set_yticks(rings)
        self.polar_ax.tick_params(axis='x', colors='white')
        self.polar_ax.tick_params(axis='y', colors='white')

        yax = self.ax.axes.get_xaxis()
        yax = yax.set_visible(False)
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

        self.polar_ax.clear()
        self.polar_ax.set_theta_zero_location('N')
        self.polar_ax.set_theta_direction(-1)

        rings = np.linspace(0.15, 1.0, 2)
        self.polar_ax.set_yticks(rings)
        self.polar_ax.tick_params(axis='x', colors='white')
        self.polar_ax.tick_params(axis='y', colors='white')

        for peleng in self.found:
            bearing_angle = np.radians(peleng[0])
            self.polar_ax.plot([bearing_angle, bearing_angle], [0, 1], color='#FF2222', linewidth=4, zorder=1)

            angle_label = f"{int(np.degrees(bearing_angle))}°"
            self.polar_ax.annotate(angle_label, xy=(bearing_angle, 1.05), xytext=(bearing_angle, 1.1),
                            ha='center', va='bottom', fontsize=12, color='white', weight='bold',
                            bbox=dict(boxstyle='round,pad=0.1', fc='r', ec='none', alpha=0.7))
        

        self.fig.canvas.draw()


    def init_ui(self):
        loadUi('qt/peleng.ui', self)

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

