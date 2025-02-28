from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import*

from PyQt5.uic import loadUi

from PyQt5 import QtWidgets
from PyQt5 import QtCore

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

import numpy as np


class AdministratorScreen(QDialog):

    def __init__(self):
        super(AdministratorScreen, self).__init__()

        self.init_ui()

    # def plot_(self):


    #     self.control_layer.addWidget(radial,0,0)



    def init_ui(self):
        loadUi('qt/administrator.ui', self)

