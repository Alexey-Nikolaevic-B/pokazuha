from PyQt5 import QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from PyQt5.uic import loadUi

import ui_main 
import ui_theory
import ui_perehvat
import ui_rabota
import ui_peleng

class QT_Controler(QObject):

    signal_goto_theory      = pyqtSignal()
    signal_goto_test        = pyqtSignal()
    signal_goto_main        = pyqtSignal()
    signal_goto_rabota      = pyqtSignal()
    signal_save_posts       = pyqtSignal(list)
    signal_com_pod          = pyqtSignal(int)

    def __init__(self):
        QObject.__init__(self)

        self.widget = QtWidgets.QStackedWidget()
        self.main   = ui_main.MainScreen()
        self.theory = ui_theory.TheoryScreen()
        self.rabota = ui_rabota.RabotaScreen()
        self.peleng = ui_peleng.PelengScreen()
        # self.perehvat = ui_perehvat.PerehvatScreen()
        
        self.signals()
        self.run()

    def signals(self):
        self.main.signal_goto_theory.connect(self.gotoTheoryScreen)
        self.main.signal_goto_rabota.connect(self.gotoRabotaScreen)
        self.rabota.signal_com_pod.connect(self.set_com_pod)

        self.theory.signal_goto_main.connect(self.gotoMainScreen)
        
        self.rabota.signal_goto_main.connect(self.gotoMainScreen)        
        self.rabota.signal_save_posts.connect(self.gotoMainScreen_posts)

    def set_com_pod(self, com_pod):
        self.status = com_pod
        self.signal_com_pod.emit(self.status)
        self.main.set_com_pod(self.status)

    def run(self):
        self.widget.addWidget(self.main)
        self.widget.show()

    def gotoRabotaScreen(self):
        self.widget.addWidget(self.rabota)
        self.widget.setCurrentIndex(self.widget.currentIndex()+1)

    def gotoTheoryScreen(self):
        self.widget.addWidget(self.theory)
        self.widget.setCurrentIndex(self.widget.currentIndex()+1)
        
    def gotoMainScreen(self):
        self.widget.addWidget(self.main)
        self.widget.setCurrentIndex(self.widget.currentIndex()+1)

    def gotoMainScreen_posts(self, data):
        self.posts = data
        self.signal_save_posts.emit(self.posts)

        self.main.set_posts(data)