from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import*

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from PyQt5.uic import loadUi
import matplotlib.cbook as cbook
from PyQt5 import QtWidgets
from PyQt5 import QtCore
import json
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

import numpy as np
from mpl_interactions import ioff, panhandler, zoom_factory

draw_path=True

class AdministratorScreen(QDialog):

    def __init__(self):
        super(AdministratorScreen, self).__init__()

        self.pelengs = []
        self.control = []
        self.posts = []

        self.init_ui()
        self.scale = 1
        self.img_path = 'img\map_4.png'
        self.draw_path = True

        with plt.ioff():
            self.fig, self.ax = plt.subplots(figsize=(5, 5))
        self.fig.patch.set_facecolor((80/256, 80/256, 80/256))
        self.fig.subplots_adjust(wspace=0.1)
        self.fig.subplots_adjust(hspace=0.1)

        disconnect_zoom = zoom_factory(self.ax)
        pan_handler = panhandler(self.fig, button=1)

        radial = FigureCanvas(self.fig)
        self.control_layer.addWidget(radial,0,0)
        self.plot_map()

        # self.btn_clear.clicked.connect(self.clear_signals)

        # self.btn_scale_50.clicked.connect(self.set_scale_1)
        # self.btn_scale_100.clicked.connect(self.set_scale_2)
        # self.btn_scale_200.clicked.connect(self.set_scale_4)

    def set_control(self):
        with open("control.json", encoding='utf-8') as config_file:
            data = json.load(config_file)
        self.control = data['freq']
        self.control = list(map(int, self.control))

    def set_posts(self, posts):
        self.posts = posts

        self.plot_map()

    def set_peleng(self, pelengs):
        # self.pelengs = []
        self.pelengs.append(pelengs)
        self.pelengs = [list(t) for t in set(tuple(sublist) for sublist in self.pelengs)]

        for peleng in self.pelengs:
            if peleng[3] in self.control:
                peleng[4] = False
            else:
                peleng[4] = True
        self.plot_map()                

    def plot_map(self):
        self.ax.clear()

        img = Image.open(self.img_path)
        self.ax.set_facecolor((80/256, 80/256, 80/256))
        
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.set_frame_on(False)

        self.ax.imshow(img, extent=[0, 1, 0, 1], aspect='auto')
        center_x, center_y = 0.5, 0.5
        coord_cent_x, coord_cent_y = 55*60 + 50, 37*60 + 30
        coord_dif_x, coord_dif_y = 4 * 60, 1 * 60
        self.ax.plot(center_x, center_y, 'k^', markersize=15, label="Center")
        self.ax.text(0, 0, f"({(coord_cent_y-coord_dif_y*self.scale)//60}°{(coord_cent_y-coord_dif_y*self.scale)%60}'N, {(coord_cent_x-coord_dif_x*self.scale)//60}°{(coord_cent_x-coord_dif_x*self.scale)%60}'E)", fontsize=8, color='black', ha='left', va='bottom')
        self.ax.text(1, 1, f"({(coord_cent_y+coord_dif_y*self.scale)//60}°{(coord_cent_y+coord_dif_y*self.scale)%60}'N, {(coord_cent_x+coord_dif_x*self.scale)//60}°{(coord_cent_x+coord_dif_x*self.scale)%60}'E)", fontsize=8, color='black', ha='left', va='bottom')
        
        for post in self.posts:
            # Высчитываем координаты относительно масштаба 
            x = float(post[0]) / self.scale
            y = float(post[1]) / self.scale
            
            # Проверяем что точно находится в границах отображаемой карты
            # Иначе рисуем на границе карты
            if abs(x) > 1 or abs(y) > 1:
                factor = max(abs(x) + 0.1, abs(y) + 0.1)
                x /= factor
                y /= factor

            self.ax.text(x, y+0.04, f"{post[2]}", fontsize=14, color='black', ha='left', va='bottom')     

            self.ax.plot(x, y, 'ks', markersize=8)  # ставим точку
            # подписываем координаты
            self.ax.text(x, y, f"({int(coord_cent_y+coord_dif_y*float(post[1]))//60}°{int(coord_cent_y+coord_dif_y*float(post[1]))%60}'N,{int(coord_cent_x+coord_dif_x*float(post[0]))//60}°{int(coord_cent_x+coord_dif_x*float(post[0]))%60}'E)", fontsize=8, color='black', ha='left', va='bottom')


        for peleng in self.pelengs:
            x = float(peleng[0]) / self.scale
            y = float(peleng[1]) / self.scale
            
            if abs(x) > 1 or abs(y) > 1:
                factor = max(abs(x) + 0.1, abs(y) + 0.1)
                x /= factor
                y /= factor

            if x > 0 and y > 0:     
                if peleng[4]:
                    self.ax.plot(x, y, 'bo', markersize=12)
                    self.ax.text(x, y+0.04, f"{peleng[3]} МГц", fontsize=12, color='blue', ha='left', va='bottom')
                    self.ax.plot([center_x, x], [center_y, y], "b--", linewidth=2)
                else:
                    self.ax.plot(x, y, 'ro', markersize=12)
                    self.ax.text(x, y+0.04, f"{peleng[3]} МГц", fontsize=12, color='red', ha='left', va='bottom')
                    self.ax.plot([center_x, x], [center_y, y], "r--", linewidth=2)

            self.ax.text(x, y, f"({int(coord_cent_y+coord_dif_y*float(peleng[1]))//60}°{int(coord_cent_y+coord_dif_y*float(peleng[1]))%60}'N,{int(coord_cent_x+coord_dif_x*float(peleng[0]))//60}°{int(coord_cent_x+coord_dif_x*float(peleng[0]))%60}'E)", fontsize=8, color='black', ha='left', va='bottom')

        self.fig.canvas.draw()

    def clear_points(self):
        self.pelengs = []
        self.plot_map()

    def init_ui(self):
        loadUi('qt/administrator.ui', self)
        self.set_control()

        self.control_layer = self.Twidget
        self.control_layer = QGridLayout(self.control_layer)

        self.setWindowFlags(Qt.WindowStaysOnTopHint)
            