from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from PyQt5.uic import loadUi

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.animation import FuncAnimation

import matplotlib.pyplot as plt
import numpy as np
from scipy.fftpack import fft, fftfreq

class MenuScreen(QDialog):
    signal_goto_main   = pyqtSignal()

    def __init__(self):
        super(MenuScreen, self).__init__()
        self.init_ui()

    def init_ui(self):
        loadUi('qt/menu.ui', self)
        self.setWindowTitle("Теория")
        
        self.control_layer_4 = self.widget_4
        self.control_layer_4 = QGridLayout(self.control_layer_4)
        self.graph_1()
        self.graph_2()
        self.graph_3()
        self.graph_4()
        style_btn = "QPushButton {color: rgb(0, 0, 0); background-color : rgb(200, 200, 200)} QPushButton::hover {background-color: rgb(255, 255, 255)}"
        self.btn_back.setStyleSheet(style_btn)

        self.lbl_freq.setText(str(self.qs_carrier_freq.value()))
        self.lbl_m.setText(str((self.qs_coef_mod.value() / 100)))
        self.lbl_harm.setText(str(self.qs_hormonics.value()))