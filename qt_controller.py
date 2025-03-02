from PyQt5 import QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal

import ui_main 
import ui_theory
import ui_perehvat
import ui_rabota

class QT_Controler(QObject):

    signal_goto_theory  = pyqtSignal()
    signal_goto_test    = pyqtSignal()
    signal_goto_main    = pyqtSignal()
    signal_goto_rabota  = pyqtSignal()
    signal_current_freq = pyqtSignal(float)

    def __init__(self):
        QObject.__init__(self)

        self.widget = QtWidgets.QStackedWidget()
        self.main   = ui_main.MainScreen()
        self.theory = ui_theory.TheoryScreen()
        self.rabota = ui_rabota.RabotaScreen()
        # self.perehvat = ui_perehvat.PerehvatScreen()
        
        self.signals()
        self.run()

    def signals(self):
        self.main.signal_goto_theory.connect(self.gotoTheoryScreen)
        self.main.signal_goto_rabota.connect(self.gotoRabotaScreen)

        self.theory.signal_goto_main.connect(self.gotoMainScreen)
        self.rabota.signal_goto_main.connect(self.gotoMainScreen)

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