from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import*

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from PyQt5.uic import loadUi

from PyQt5 import QtWidgets
from PyQt5 import QtCore
import json
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

import numpy as np

draw_path=True

class AdministratorScreen(QDialog):

    def __init__(self):
        super(AdministratorScreen, self).__init__()

        self.init_ui()
        self.scale = 1
        self.img_path = 'img\map_1.jpg'
        self.draw_path = True

        self.posts = [[-0.5, -0.5, "Маджахет"], [0.2, 0.8, "Сатурн"]] # [X, Y, ПОЗЫВНОЙ]
        self.pelengs = []                                         # [X, Y, ПЕЛЕНГ, ЧАСТОТА]

        self.fig, self.ax = plt.subplots(figsize=(5, 5))
        self.ax.set_facecolor((1.0, 0.47, 0.42))

        radial = FigureCanvas(self.fig)
        self.control_layer.addWidget(radial,0,0)
        self.plot_map()

        self.btn_clear.clicked.connect(self.clear_signals)

        self.btn_scale_50.clicked.connect(self.set_scale_1)
        self.btn_scale_100.clicked.connect(self.set_scale_2)
        self.btn_scale_200.clicked.connect(self.set_scale_4)

    def set_posts(self, posts):
        pass

    def set_peleng(self, pelengs):
        self.pelengs.append(pelengs)
        self.pelengs = [list(t) for t in set(tuple(sublist) for sublist in  self.pelengs)]
        # print(self.pelengs)
        self.plot_map()                

    def plot_map(self):
        self.ax.clear()
        self.ax.set_facecolor((1.0, 0.47, 0.42))

        img = Image.open(self.img_path)
        
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.set_frame_on(False)

        self.ax.imshow(img, extent=[-1, 1, -1, 1], aspect='auto')
        center_x, center_y = 0, 0
        coordinates_center_x, coordinates_center_y = 37*60 + 30, 55*60 + 50
        coord_dif_x, coord_dif_y = 1 * 60 * self.scale, 4 * 60 * self.scale
        self.ax.plot(center_x, center_y, 'r^', markersize=15, label="Center")
        self.ax.text(-1, -1, f"{center_x,}", fontsize=8, color='black', ha='left', va='bottom')
        self.ax.text(1, 1, f"{center_x,}", fontsize=8, color='black', ha='left', va='bottom')
        
        # НАШИ ПОСТЫ
        for post in self.posts: 
            x = float(post[0]) / self.scale
            y = float(post[1]) / self.scale
            
            if abs(x) > 1 or abs(y) > 1:
                factor = max(abs(x) + 0.1, abs(y) + 0.1)
                x /= factor
                y /= factor
            
            self.ax.plot(x, y, 'rs', markersize=10)  # ставим точку

            self.ax.text(x, y, f"({float(post[0]):.2f}, {float(post[1]):.2f})", fontsize=10, color='red', ha='left', va='bottom')
            self.ax.text(x, y+0.08, f"{post[2]}", fontsize=14, color='red', ha='left', va='bottom')
            # last_x, last_y = x, y
        
        # ПЕЛЕНГИ
        last_x, last_y = None, None
        
        for peleng in self.pelengs:
            # Высчитываем координаты относительно масштаба 
            x = float(peleng[0]) / self.scale
            y = float(peleng[1]) / self.scale
            
            # Проверяем что точно находится в границах отображаемой карты
            # Иначе рисуем на границе карты
            if abs(x) > 1 or abs(y) > 1:
                factor = max(abs(x) + 0.1, abs(y) + 0.1)
                x /= factor
                y /= factor
            
            self.ax.plot(x, y, 'bo', markersize=8)  # ставим точку

            # подписываем координаты
            self.ax.text(x, y, f"({float(peleng[0]):.2f}, {float(peleng[1]):.2f})", fontsize=10, color='blue', ha='left', va='bottom')
            last_x, last_y = x, y
        
            # Если поставлена галочка на отрисовку пеленга на карте
            if draw_path and last_x is not None:
                self.ax.plot([center_x, last_x], [center_y, last_y], 'b-', linewidth=0.5)
                self.ax.text((last_x - center_x)/2, (last_y-center_y)/2, f"{peleng[2]}°", 
                        fontsize=12, color='blue', ha='left', va='bottom')

        self.fig.canvas.draw()

    def change_draw_path(self):
        if self.draw_path == True:
            self.draw_path = False
        else:
            self.draw_path = True
        self.plot_map()

    def clear_signals(self):
        self.pelengs = []
        self.plot_map()

    def set_scale_1(self):
        self.scale = 1
        self.img_path = "img\map_1.jpg"
        self.plot_map()

    def set_scale_2(self):
        self.scale = 2
        self.img_path = "img\map_2.jpg"
        self.plot_map()

    def set_scale_4(self):
        self.scale = 4
        self.img_path = "img\map_4.jpg"
        self.plot_map()

    # # БАРДУШКО
    # Меняем масштаб карты (если нажата кнопка масштаба)
    # def change_scale(self):
    #     scale = scale_changed
    #     if scale == 1:
    #         image_path = "img/image_50000.jpg"
    #     elif scale == 2:
    #         image_path = "img/image_100000.jpg"
    #     else:
    #         image_path = "img/image_250000.jpg"
    
        # plot_xy_graph()

    def change_draw_path(self):
        global draw_path
        if draw_path == True:
            draw_path = False
        else:
            draw_path = True
        self.plot_map()

    def init_ui(self):
        loadUi('qt/administrator.ui', self)

        self.control_layer = self.Twidget
        self.control_layer = QGridLayout(self.control_layer)

        self.setWindowFlags(Qt.WindowStaysOnTopHint)
            

