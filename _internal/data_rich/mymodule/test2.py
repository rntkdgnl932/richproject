import sys
import os
import time
import requests
import datetime


from PyQt5.QAxContainer import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtTest import *

import variable as v_

sys.path.append('C:/my_games/' + str(v_.game_folder) + '/' + str(v_.data_folder) + '/mymodule')



dir_path = "C:\\my_games\\" + str(v_.game_folder)
file_path = dir_path + "\\" + str(v_.data_folder) + "\\mymodule\\condition_stock.txt"
second_order_path = dir_path + "\\" + str(v_.data_folder) + "\\mymodule\\second_order_stock.txt"


class TestCall(QAxWidget):
    def __init__(self):
        super().__init__()
        print("TestCallTestCallTestCall", __name__)

    def test_time(self):
        now = datetime.datetime.now()
        now_time_HMS = now.strftime("%H%M%S")
        print("test time : ", now_time_HMS)

        return now_time_HMS

    def test_time2(self):
        now = datetime.datetime.now()
        now_time_HMS = now.strftime("%H%M%S")
        print("test time 2 : ", now_time_HMS)

        return now_time_HMS