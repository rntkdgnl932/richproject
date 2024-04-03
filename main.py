# * QTabWidget 탭에 다양한 위젯 추가
import numpy as np
from PyQt5.QtWidgets import *
# from PyQt5.QtGui import QIcon, QFont       #아이콘
from PyQt5.QtCore import Qt, QThread
from PyQt5.QAxContainer import *
from PyQt5.QtWidgets import *

#
import os
import time
from datetime import datetime
import random
import os.path
from datetime import date, timedelta
import re

# print(cv2.__version__)
# import matplotlib.pyplot as plt

import numpy
# 패키지 다운 필요
# from pytesseract import image_to_string #

# import keyboard

# 패키지 다운 불필요
import webbrowser
import ctypes
import shutil
import sys


sys.path.append('C:/my_games/richproject/data_rich/mymodule')

# 나의 모듈 모두 표시해야함
# from function import imgs_set, imgs_set_, click_pos_2, random_int, text_check_get_3, int_put_, text_check_get, \
#     click_with_image, drag_pos, image_processing, get_region, click_pos_reg



from massenger import line_monitor

# from functools import partial

from test_ import go_test

import variable as v_
sys.path.append('C:/my_games/richproject/data_rich/mymodule')

sys.setrecursionlimit(10 ** 7)
# pyqt5 관련###################################################
rowcount = 0
colcount = 0
thisRow = 0
thisCol = 0
table_datas = ""
#  onCollection= False
onCharacter = 0
onRefresh_time = 0
onDunjeon = "none"
onDunjeon_level = 0
onHunt = "none"
onHunt2 = "none"
onHunt3 = "none"
onMaul = "none"

isgloballoop = False

# 기존 오토모드 관련###############################################


####################################################################################################################
# pytesseract.pytesseract.tesseract_cmd = R'E:\workspace\pythonProject\Tesseract-OCR\tesseract'
from PyQt5.QtWidgets import *
import sys

import main_p
from ui import *

sys.path.append('C:/my_games/' + str(v_.game_folder) + '/' + str(v_.data_folder) + '/mymodule')

import os.path

# if __name__ == '__main__':
#     try:
#         app = QApplication(sys.argv)
#         kiwoom.Kiwoom()
#         app.exec_()
#     except Exception as e:
#         print(e)
#         print("프로그램 꺼지기전 정지")
#         os.system("pause")

class Main():
    def __init__(self):
        print("시작합니다")

        self.app = QApplication(sys.argv)

        self.main_p = main_p.MyApp()

        self.app.exec_()

if __name__ == '__main__':
    try:
        Main()
    except Exception as e:
        print(e)
        print("프로그램 꺼지기전 정지")
        os.system("pause")

# if __name__ == '__main__':
#     try:
#         app = QApplication(sys.argv)
#         ex = main_p.MyApp()
#
#
#         # Back up the reference to the exceptionhook
#         sys._excepthook = sys.excepthook
#
#         # Set the exception hook to our wrapping function
#         sys.excepthook = main_p.my_exception_hook
#
#         sys.exit(app.exec_())
#     except Exception as e:
#         print(e)
#         print("프로그램 꺼지기전 정지")
#         os.system("pause")
