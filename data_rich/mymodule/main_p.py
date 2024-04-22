# * QTabWidget 탭에 다양한 위젯 추가
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QFont, QColor     #아이콘
from PyQt5.QtCore import Qt, QThread
from PyQt5.QtWidgets import *

import sys
import datetime
import json

import variable as v_

sys.path.append('C:/my_games/' + str(v_.game_folder) + '/' + str(v_.data_folder) + '/mymodule')
import os
import time
import os.path
import re

# 패키지 다운 필요
import win32console, win32gui
from PyQt5.QtTest import *
# 나의 모듈
from kiwoom import Kiwoom
from ui import Ui_class
from test2 import TestCall


from massenger import line_monitor, line_to_me

from test_ import go_test


from server import game_start
import variable as v_

sys.setrecursionlimit(10 ** 7)
# pyqt5 관련###################################################
rowcount = 0
colcount = 0
thisRow = 0
thisCol = 0
table_datas = ""
#  onCollection= False
onCla = 'none'
onCharacter = 0
onDunjeon_1 = "none"
onDunjeon_1_level = 0
onDunjeon_2 = "none"
onDunjeon_2_level = 0
onDunjeon_3 = "none"
onDunjeon_3_level = 0
onDunjeon_3_step = 0

onHunt = "none"
onHunt2 = "none"
onHunt3 = "none"
onHunt4 = "none"
onMaul = "none"


version = v_.version_

# 기존 오토모드 관련##############################################


####################################################################################################################
# pytesseract.pytesseract.tesseract_cmd = R'E:\workspace\pythonProject\Tesseract-OCR\tesseract'


####################################################################################################################
####################################################################################################################
####################################################################################################################
#######pyqt5 관련####################################################################################################
####################################################################################################################
####################################################################################################################
####################################################################################################################
####################################################################################################################


class MyApp(QDialog):

    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMaximizeButtonHint | Qt.WindowMinimizeButtonHint)

        self.initUI()

    def initUI(self):

        tabs = QTabWidget()
        tabs.addTab(FirstTab(), '스케쥴')
        tabs.addTab(SecondTab(), '내 정보')
        tabs.addTab(ThirdTab(), '현재 컴퓨터 및 마우스 설정')

        # buttonbox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        # buttonbox.accepted.connect(self.accept)
        # buttonbox.rejected.connect(self.reject)

        vbox = QVBoxLayout()
        vbox.addWidget(tabs)
        # vbox.addWidget(buttonbox)

        self.setLayout(vbox)

        # self.rich_start1_ready()



        self.my_title()

        # 풀버젼
        # pyinstaller --hidden-import PyQt5 --hidden-import PyQt5.QtTest --hidden-import pandas --hidden-import pyserial --hidden-import requests --hidden-import chardet --add-data="C:\\my_games\\richproject\\data_rich;./data_rich" --add-data="C:\\my_games\\richproject\\mysettings;./mysettings" --name richproject -i="rich_project.ico" --add-data="rich_project.ico;./" --icon="rich_project.ico" main.py
        # 업데이트버젼
        # pyinstaller --hidden-import PyQt5 --hidden-import pyserial --hidden-import requests --hidden-import chardet --add-data="C:\\my_games\\richproject\\data_rich;./data_rich" --name richproject -i="rich_project.ico" --add-data="rich_project.ico;./" --icon="rich_project.ico" --paths "C:\Users\1_S_3\AppData\Local\Programs\Python\Python311\Lib\site-packages\cv2" main.py

        # self.setGeometry(1000 + 960 + 960, 300, 900, 600)
        self.setGeometry(20 + 960 + 960, 200, 900, 700)
        self.show()


        # 콘솔창 없애기
        # win32gui.ShowWindow(win32console.GetConsoleWindow(), 0)

        self.onetab = FirstTab()
        self.onetab.rich_start1_ready()

    def my_title(self):
        self.setWindowTitle(v_.this_game + "(ver " + version + ")")

class ThirdTab(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        dir_path = "C:\\my_games"
        file_path = dir_path + "\\line\\line.txt"

        if os.path.isdir(dir_path) == False:
            os.makedirs(dir_path)
        isFile = False
        while isFile is False:
            if os.path.isfile(file_path) == True:
                isFile = True
                # 파일 읽기
                with open(file_path, "r", encoding='utf-8-sig') as file:
                    line = file.read()
                    line_ = line.split(":")
                    print('line', line)
            else:
                print('line 파일 없당')
                with open(file_path, "w", encoding='utf-8-sig') as file:
                    file.write("ccocco:메롱")

        file_path2 = dir_path + "\\mouse\\arduino.txt"

        isFile = False
        while isFile is False:
            if os.path.isfile(file_path2) == True:
                isFile = True
                # 파일 읽기
                with open(file_path2, "r", encoding='utf-8-sig') as file:
                    line2 = file.read()
                    v_.now_arduino = line2
                    print('line2', line2)
            else:
                print('line2 파일 없당')
                with open(file_path2, "w", encoding='utf-8-sig') as file:
                    file.write("on")

        dir_path2 = dir_path + "\\" + str(v_.game_folder) + "\\mysettings\\game_server"
        file_path3 = dir_path2 + "\\game_server.txt"

        isFile = False
        while isFile is False:
            if os.path.isdir(dir_path2) == True:
                if os.path.isfile(file_path3) == True:
                    isFile = True
                    # 파일 읽기
                    with open(file_path3, "r", encoding='utf-8-sig') as file:
                        line3 = file.read()
                        print('game server', line3)
                else:
                    print('game server 파일(line3) 없당')
                    with open(file_path3, "w", encoding='utf-8-sig') as file:
                        file.write("k0")
            else:
                os.makedirs(dir_path2)




        self.monitor = QGroupBox('My Cla Monitor & Arduino')

        self.own = QLabel("       현재 소유자 : " + line_[0] + "\n\n")
        self.computer = QLabel("       현재 컴퓨터 : " + line_[1] + " 컴퓨터\n\n")
        self.game_server = QLabel("       현재 게임서버 : " + line3 + "\n\n")
        self.mouse_arduino = QLabel("       현재 아두이노 활성화 상태 : " + line2 + "\n\n")

        self.own_in = QLineEdit(self)
        self.own_in.setText(line_[0])
        self.computer_in = QLineEdit(self)
        self.computer_in.setText(line_[1])
        self.game_server_in = QLineEdit(self)
        self.game_server_in.setText(line3)
        self.line_save = QPushButton("저장하기")
        self.line_save.clicked.connect(self.button_line_save)

        self.arduino_on = QPushButton("아두이노 on")
        self.arduino_on.clicked.connect(self.button_arduino_on)
        self.arduino_off = QPushButton("아두이노 off")
        self.arduino_off.clicked.connect(self.button_arduino_off)

        mo1_1 = QHBoxLayout()
        mo1_1.addWidget(self.own)

        mo1_2 = QHBoxLayout()
        mo1_2.addWidget(self.computer)

        mo1_5 = QHBoxLayout()
        mo1_5.addWidget(self.game_server)

        mo1_mouse = QHBoxLayout()
        mo1_mouse.addWidget(self.mouse_arduino)

        mo1_3 = QHBoxLayout()
        mo1_3.addStretch(1)
        mo1_3.addWidget(self.own_in)
        mo1_3.addWidget(self.computer_in)
        mo1_3.addWidget(self.game_server_in)
        mo1_3.addStretch(1)
        mo1_3.addWidget(self.line_save)
        mo1_3.addStretch(18)

        mo1_4 = QHBoxLayout()
        mo1_4.addWidget(self.arduino_on)
        mo1_4.addWidget(self.arduino_off)

        Mobox1 = QVBoxLayout()
        Mobox1.addStretch(1)
        Mobox1.addLayout(mo1_1)
        Mobox1.addLayout(mo1_2)
        Mobox1.addLayout(mo1_5)
        Mobox1.addLayout(mo1_mouse)
        Mobox1.addLayout(mo1_3)
        Mobox1.addStretch(3)
        Mobox1.addLayout(mo1_4)
        Mobox1.addStretch(3)

        self.monitor.setLayout(Mobox1)

        hbox_ = QHBoxLayout()
        hbox_.addWidget(self.monitor)

        Vbox_ = QVBoxLayout()
        Vbox_.addLayout(hbox_)

        self.setLayout(Vbox_)

    def button_line_save(self):
        own_ = self.own_in.text()  # line_edit text 값 가져오기
        computer_ = self.computer_in.text()
        game_server_ = self.game_server_in.text()
        print(own_)
        print(computer_)
        print(game_server_)

        self.own.setText("       현재 소유자 : " + own_ + "\n\n")
        self.computer.setText("       현재 컴퓨터 : " + computer_ + " 컴퓨터\n\n")
        self.game_server.setText("       현재 게임서버 : " + game_server_ + "\n\n")
        write_1 = own_ + ":" + computer_
        write_2 = game_server_
        dir_path = "C:\\my_games"
        file_path = dir_path + "\\line\\line.txt"
        file_path2 = dir_path + "\\" + str(v_.game_folder) + "\\mysettings\\game_server\\game_server.txt"

        with open(file_path, "w", encoding='utf-8-sig') as file:
            file.write(write_1)
        with open(file_path2, "w", encoding='utf-8-sig') as file:
            file.write(write_2)

    def button_arduino_on(self):
        print("arduino_on")
        file_path = "C:\\my_games\\mouse\\arduino.txt"
        with open(file_path, "w", encoding='utf-8-sig') as file:
            file.write("on")
        data = "on"
        self.mouse_arduino.setText("       현재 아두이노 활성화 상태 : " + data + "\n\n")
        v_.now_arduino = data



    def button_arduino_off(self):
        print("arduino_off")
        file_path = "C:\\my_games\\mouse\\arduino.txt"
        with open(file_path, "w", encoding='utf-8-sig') as file:
            file.write("off")
        data = "off"
        self.mouse_arduino.setText("       현재 아두이노 활성화 상태 : " + data + "\n\n")
        v_.now_arduino = data


class SecondTab(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        dir_path = "C:\\my_games\\" + str(v_.game_folder)
        file_path_one = dir_path + "\\mysettings\\idpw\\onecla.txt"
        file_path_two = dir_path + "\\mysettings\\idpw\\twocla.txt"
        if os.path.isfile(file_path_one) == True:
            # 파일 읽기
            with open(file_path_one, "r", encoding='utf-8-sig') as file:
                lines_one = file.read().splitlines()
                print('lines_one', lines_one)
                thismyid_one = lines_one[0]
                thismypw_one = lines_one[1]
                v_.mypw = thismypw_one
                thismyps_one = lines_one[2]
        else:
            print('one 파일 없당')
            thismyid_one = 'none'
            thismyps_one = 'none'

        if os.path.isfile(file_path_two) == True:
            # 파일 읽기
            with open(file_path_two, "r", encoding='utf-8-sig') as file:
                lines_two = file.read().splitlines()
                print('lines_two', lines_two)
                thismyid_two = lines_two[0]
                thismypw_two = lines_two[1]
                thismyps_two = lines_two[2]
        else:
            print('two 파일 없당')
            thismyid_two = 'none'
            thismyps_two = 'none'

        # 111

        self.com_group1 = QGroupBox('One Cla')
        self.one_cla_id = QLabel("       ID          ")
        self.one_cla_pw = QLabel("       PW        ")
        self.one_cla_ps = QLabel("       참고사항 ")

        self.one_cla_id_now = QLabel("       현재 내 아이디 : " + thismyid_one + "\n\n")
        self.one_cla_ps_now = QLabel("       무슨 참고 사항을 적었나요? " + thismyps_one)

        self.pushButton_login1 = QPushButton("로그인하기")
        self.pushButton_login1.clicked.connect(self.let_is_login_1)

        self.pushButton_left = QPushButton("좌로 정렬")
        self.pushButton_left.clicked.connect(self.win_left)

        # self.one_cla_id_in = QLineEdit()
        self.one_cla_id_in = QLineEdit(self)
        self.one_cla_id_in.setText(thismyid_one)
        self.one_cla_pw_in = QLineEdit(self)
        self.one_cla_pw_in.setText(thismypw_one)
        self.one_cla_ps_in = QLineEdit(self)
        self.one_cla_ps_in.setText(thismyps_one)
        self.pushButton_one = QPushButton("저장하기")
        self.pushButton_one.clicked.connect(self.button_event1)

        vbox1_1 = QHBoxLayout()
        vbox1_1.addWidget(self.one_cla_id_now)

        vbox1_2 = QHBoxLayout()
        vbox1_2.addWidget(self.one_cla_ps_now)

        vbox1_log = QHBoxLayout()
        vbox1_log.addStretch(5)
        vbox1_log.addWidget(self.pushButton_login1)
        vbox1_log.addStretch(5)

        vbox1_left = QHBoxLayout()
        vbox1_left.addStretch(15)
        vbox1_left.addWidget(self.pushButton_left)
        vbox1_left.addStretch(1)

        vbox1_3 = QHBoxLayout()
        vbox1_3.addWidget(self.one_cla_id)
        vbox1_3.addWidget(self.one_cla_id_in)

        vbox1_4 = QHBoxLayout()
        vbox1_4.addWidget(self.one_cla_pw)
        vbox1_4.addWidget(self.one_cla_pw_in)

        vbox1_5 = QHBoxLayout()
        vbox1_5.addWidget(self.one_cla_ps)
        vbox1_5.addWidget(self.one_cla_ps_in)

        vbox1_6 = QHBoxLayout()
        vbox1_6.addStretch(5)
        vbox1_6.addWidget(self.pushButton_one)

        Vbox1 = QVBoxLayout()
        Vbox1.addStretch(1)
        Vbox1.addLayout(vbox1_1)
        Vbox1.addLayout(vbox1_2)
        Vbox1.addStretch(1)
        Vbox1.addLayout(vbox1_log)
        Vbox1.addStretch(5)
        Vbox1.addLayout(vbox1_left)
        Vbox1.addStretch(3)
        Vbox1.addLayout(vbox1_3)
        Vbox1.addLayout(vbox1_4)
        Vbox1.addLayout(vbox1_5)
        Vbox1.addLayout(vbox1_6)
        Vbox1.addStretch(2)
        # maul_add = QPushButton('마을 의뢰 추가')
        # maul_add.clicked.connect(self.onActivated_maul_add)
        # vbox6.addWidget(maul_add)
        self.com_group1.setLayout(Vbox1)

        # 222
        self.com_group2 = QGroupBox('Two Cla')
        self.two_cla_id = QLabel("       ID          ")
        self.two_cla_pw = QLabel("       PW        ")
        self.two_cla_ps = QLabel("       참고사항 ")

        self.two_cla_id_now = QLabel("       현재 내 아이디 : " + thismyid_two + "\n\n")
        self.two_cla_ps_now = QLabel("       무슨 참고 사항을 적었나요? " + thismyps_two)

        self.pushButton_login2 = QPushButton("로그인하기")
        self.pushButton_login2.clicked.connect(self.let_is_login_2)

        self.pushButton_right = QPushButton("우로 정렬")
        self.pushButton_right.clicked.connect(self.win_right)

        self.two_cla_id_in = QLineEdit(self)
        self.two_cla_id_in.setText(thismyid_two)
        self.two_cla_pw_in = QLineEdit(self)
        self.two_cla_pw_in.setText(thismypw_two)
        self.two_cla_ps_in = QLineEdit(self)
        self.two_cla_ps_in.setText(thismyps_two)
        self.pushButton_two = QPushButton("저장하기")
        self.pushButton_two.clicked.connect(self.button_event2)

        vbox2_1 = QHBoxLayout()
        vbox2_1.addWidget(self.two_cla_id_now)

        vbox2_2 = QHBoxLayout()
        vbox2_2.addWidget(self.two_cla_ps_now)

        vbox2_log = QHBoxLayout()
        vbox2_log.addStretch(5)
        vbox2_log.addWidget(self.pushButton_login2)
        vbox2_log.addStretch(5)

        vbox2_right = QHBoxLayout()
        vbox2_right.addStretch(1)
        vbox2_right.addWidget(self.pushButton_right)
        vbox2_right.addStretch(15)

        vbox2_3 = QHBoxLayout()
        vbox2_3.addWidget(self.two_cla_id)
        vbox2_3.addWidget(self.two_cla_id_in)

        vbox2_4 = QHBoxLayout()
        vbox2_4.addWidget(self.two_cla_pw)
        vbox2_4.addWidget(self.two_cla_pw_in)

        vbox2_5 = QHBoxLayout()
        vbox2_5.addWidget(self.two_cla_ps)
        vbox2_5.addWidget(self.two_cla_ps_in)

        vbox2_6 = QHBoxLayout()
        vbox2_6.addStretch(5)
        vbox2_6.addWidget(self.pushButton_two)

        Vbox2 = QVBoxLayout()
        Vbox2.addStretch(1)
        Vbox2.addLayout(vbox2_1)
        Vbox2.addLayout(vbox2_2)
        Vbox2.addStretch(1)
        Vbox2.addLayout(vbox2_log)
        Vbox2.addStretch(5)
        Vbox2.addLayout(vbox2_right)
        Vbox2.addStretch(3)
        Vbox2.addLayout(vbox2_3)
        Vbox2.addLayout(vbox2_4)
        Vbox2.addLayout(vbox2_5)
        Vbox2.addLayout(vbox2_6)
        Vbox2.addStretch(2)
        # maul_add = QPushButton('마을 의뢰 추가')
        # maul_add.clicked.connect(self.onActivated_maul_add)
        # vbox6.addWidget(maul_add)
        self.com_group2.setLayout(Vbox2)

        ###
        hbox_ = QHBoxLayout()
        hbox_.addWidget(self.com_group2)

        Vbox_ = QVBoxLayout()
        Vbox_.addLayout(hbox_)

        ###
        hbox__ = QHBoxLayout()
        hbox__.addWidget(self.com_group1)
        hbox__.addLayout(Vbox_)

        ###
        vbox = QVBoxLayout()
        vbox.addLayout(hbox__)
        self.setLayout(vbox)

    def win_left(self):
        print("왼쪽으로 정렬 합니다.")

    def win_right(self):
        print("왼쪽으로 정렬 합니다.")

    def win_left_ex(self):
        print("왼쪽으로 정렬 합니다.")


    def win_right_ex(self):
        print("오른쪽으로 정렬 합니다.")


    def let_is_login_1(self):
        print("로그인1 버튼 입니다.")

    def let_is_login_2(self):
        print("로그인2 버튼 입니다.")

    def button_event1(self):
        one_cla_id_ = self.one_cla_id_in.text()  # line_edit text 값 가져오기
        one_cla_pw_ = self.one_cla_pw_in.text()
        one_cla_ps_ = self.one_cla_ps_in.text()
        print(one_cla_id_)
        print(one_cla_pw_)

        one_cla_id_result = "       현재 내 아이디 : " + one_cla_id_ + "\n\n"
        one_cla_ps_result = "       무슨 참고 사항을 적었나요? " + one_cla_ps_
        self.one_cla_id_now.setText(one_cla_id_result)
        self.one_cla_ps_now.setText(one_cla_ps_result)
        shcedule = one_cla_id_ + "\n" + one_cla_pw_ + "\n" + one_cla_ps_
        dir_path = "C:\\my_games\\" + str(v_.game_folder)
        file_path_one = dir_path + "\\mysettings\\idpw\\onecla.txt"
        file_path_two = dir_path + "\\mysettings\\idpw\\twocla.txt"
        with open(file_path_one, "w", encoding='utf-8-sig') as file:
            file.write(shcedule)

    def button_event2(self):
        two_cla_id_ = self.two_cla_id_in.text()  # line_edit text 값 가져오기
        two_cla_pw_ = self.two_cla_pw_in.text()
        two_cla_ps_ = self.two_cla_ps_in.text()
        print(two_cla_id_)
        print(two_cla_pw_)

        two_cla_id_result = "       현재 내 아이디 : " + two_cla_id_ + "\n\n"
        two_cla_ps_result = "       무슨 참고 사항을 적었나요? " + two_cla_ps_
        self.two_cla_id_now.setText(two_cla_id_result)
        self.two_cla_ps_now.setText(two_cla_ps_result)
        shcedule = two_cla_id_ + "\n" + two_cla_pw_ + "\n" + two_cla_ps_
        dir_path = "C:\\my_games\\" + str(v_.game_folder)
        file_path_one = dir_path + "\\mysettings\\idpw\\onecla.txt"
        file_path_two = dir_path + "\\mysettings\\idpw\\twocla.txt"
        with open(file_path_two, "w", encoding='utf-8-sig') as file:
            file.write(shcedule)


class FirstTab(QWidget):



    def __init__(self):
        super().__init__()
        self.initUI()
        self.set_rand_int()



    def initUI(self):
        global rowcount, colcount




        dir_path = "C:\\my_games\\" + str(v_.game_folder)
        file_path = dir_path + "\\mysettings\\myschedule\\schedule.txt"
        file_path3 = dir_path + "\\mysettings\\myschedule\\schedule2.txt"
        file_path5 = dir_path + "\\" + str(v_.data_folder) + "\\jadong\\jadong_force_list.txt"


        # def set
        self.tableWidget = QTableWidget()
        # self.tableWidget.setRowCount(len(lines))
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setSortingEnabled(True)
        # self.tableWidget.sortByColumn(1, Qt.DescendingOrder)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.verticalHeader().setVisible(False)  # 행번호 안나오게 하는 코드
        self.tableWidget.setHorizontalHeaderLabels(["종목", "종목코드", "보유수량", "현재매입금액", "매입가", "현재가", "수익률(%)"])

        self.label = QLabel('')

        # 스케쥴 변경 확인
        self.sche_add1 = QPushButton('부자되기', self)
        self.sche_add1.clicked.connect(self.rich_start1)

        # 테스트 버튼
        self.mytestin = QPushButton('테스뚜')
        self.mytestin.clicked.connect(self.mytestin_)
        self.perfect_pause = QPushButton('끄기')
        self.perfect_pause.clicked.connect(self.moonlight_stop_perfect)
        self.again_restart = QPushButton('업데이트')
        self.again_restart.clicked.connect(self.again_restart_game)

        # 스케쥴 선택 삭제
        self.sell_ = QPushButton('종목 매도')
        self.sell_.clicked.connect(self.sell_now)


        # 강제 노역(서브퀘스트 강제수행)

        self.force_sub = QGroupBox('매수중인 종목 갯수')

        self.my_stock_load = QLabel("현재 : " + str("로드 중") + "\n\n")

        test_box_ = QHBoxLayout()
        test_box_.addWidget(self.my_stock_load)

        self.force_sub.setLayout(test_box_)

        # self.onActivated_test(1)




        # 콜렉션 온오프(수집 온오프)
        self.onActivated_slelect_collection_toggle_read()

        self.collection_on_off = QGroupBox('수집 On/Off')
        print("dark_demention", v_.onCollection)
        if v_.onCollection == True:
            tgl_now = "On"
        else:
            tgl_now = "Off"
        self.now_toggle = QLabel("수집 : " + tgl_now + "\n")
        # 토글 버튼
        self.tgl = QCheckBox("On / Off")
        self.tgl.adjustSize()
        self.tgl.setChecked(v_.onCollection)
        self.tgl.toggled.connect(self.onActivated_slelect_collection_toggle)

        tgl33 = QHBoxLayout()
        tgl33.addWidget(self.now_toggle)

        collec_box = QVBoxLayout()
        collec_box.addLayout(tgl33)
        collec_box.addWidget(self.tgl)

        self.collection_on_off.setLayout(collec_box)






        # 캐릭터 아이디
        self.com_group3 = QGroupBox('클라 및 캐릭터 선택')
        cb_cla = QComboBox()
        list_cla = ['클라 선택', 'One', 'Two', 'Three', 'Four']
        cb_cla.addItems(list_cla)
        cb3 = QComboBox()
        list3 = ['캐릭터 선택', '1', '2', '3', '4', '5']
        cb3.addItems(list3)
        vbox3 = QVBoxLayout()
        vbox3.addWidget(cb_cla)
        vbox3.addWidget(cb3)
        character_ = QPushButton('캐릭터 선택')
        character_.clicked.connect(self.onActivated_character)
        self.com_group3.setLayout(vbox3)

        #self.one_cla_id_now = QLabel("       현재 내 아이디 : " + thismyid_one + "\n\n")

        # 일일퀘스트 요구 레벨(나의 레벨)
        read_level = '35'

        dir_path = "C:\\my_games\\" + str(v_.game_folder) + "\\mysettings\\my_level"
        one_file_path = dir_path + "\\one_character.txt"
        two_file_path = dir_path + "\\two_character.txt"

        isreadlevel = False
        while isreadlevel is False:
            if os.path.isdir(dir_path) == True:
                print('디렉토리 존재함')
                isreadlevel = True
                one_re_ = False
                two_re_ = False
                while one_re_ is False:
                    if os.path.isfile(one_file_path) == True:
                        one_re_ = True
                        with open(one_file_path, "r", encoding='utf-8-sig') as file:
                            one_read_level = file.read()
                    else:
                        with open(one_file_path, "w", encoding='utf-8-sig') as file:
                            file.write(read_level)
                while two_re_ is False:
                    if os.path.isfile(two_file_path) == True:
                        two_re_ = True
                        with open(two_file_path, "r", encoding='utf-8-sig') as file:
                            two_read_level = file.read()
                    else:
                        with open(two_file_path, "w", encoding='utf-8-sig') as file:
                            file.write(read_level)

            else:
                print('디렉토리 존재하지 않음')
                os.makedirs(dir_path)
                with open(one_file_path, "w", encoding='utf-8-sig') as file:
                    file.write(read_level)
                with open(two_file_path, "w", encoding='utf-8-sig') as file:
                    file.write(read_level)




        self.com_group3_level = QGroupBox('매수 및 매도 금액')
        self.one_require_level = QLabel("1차 매수 금액 : " + str(one_read_level))
        self.two_require_level = QLabel("2차 매도 금액 : " + str(two_read_level))
        self.require_level_in = QLineEdit(self)
        vbox_level = QVBoxLayout()
        vbox_level.addWidget(self.one_require_level)
        vbox_level.addWidget(self.two_require_level)
        vbox_level.addWidget(self.require_level_in)
        one_character_level = QPushButton('1차 매수금 저장')
        one_character_level.clicked.connect(self.onActivated_one_character_level)
        two_character_level = QPushButton('2차 매도금 저장')
        two_character_level.clicked.connect(self.onActivated_two_character_level)
        vbox_level.addWidget(one_character_level)
        vbox_level.addWidget(two_character_level)
        self.com_group3_level.setLayout(vbox_level)

        # 초기화 시간 수정
        #  onActivated_re_time 매수중인 종목
        self.com_group33 = QGroupBox('총 매입금액 및 총 수익')

        self.result_kiwoom_data_1 = "총 매입금액 : " + str("로드 중") + "\n\n"
        self.result_kiwoom_data_2 = "현재 총 수익 : " + str("로드 중") + "\n\n"

        self.my_stock_all_buy_money = QLabel(str("총 매입금액 : " + str("로드 중") + "\n\n"))
        self.my_stock_all_rate = QLabel(str("현재 총 수익 : " + str("로드 중") + "\n\n"))

        buy_box_ = QVBoxLayout()
        buy_box_.addWidget(self.my_stock_all_buy_money)
        buy_box_.addWidget(self.my_stock_all_rate)
        self.com_group33.setLayout(buy_box_)

        # 초기화 시간
        dir_path = "C:\\my_games\\" + str(v_.game_folder)
        file_path2 = dir_path + "\\mysettings\\refresh_time\\quest.txt"
        file_path13 = dir_path + "\\mysettings\\refresh_time\\refresh_time.txt"

        isRefresh = False
        while isRefresh is False:
            if os.path.isfile(file_path13) == True:
                with open(file_path13, "r", encoding='utf-8-sig') as file:
                    isRefresh = True
                    refresh_time = file.read()
                    print("refresh_time => ", refresh_time)
            else:
                with open(file_path13, "w", encoding='utf-8-sig') as file:
                    file.write(str(6))

        if os.path.isfile(file_path2) == True:
            # 파일 읽기
            with open(file_path2, "r", encoding='utf-8-sig') as file:
                lines2 = file.read().splitlines()
                day_ = lines2[0].split(":")
                re_time_ = str(day_[0]) + " => " + str(day_[1] + "시")
                print("최근 초기화 시간 : ", re_time_)
        else:
            re_time_ = "아직 모름..."

        self.com_group34 = QGroupBox('셋팅된 시간')
        # lbx = QBoxLayout(QBoxLayout.LeftToRight, parent=self)
        # self.com_group34.setLayout(lbx)
        self.my_refresh_time = QLabel("현재 초기화 시간 : " + str(refresh_time) + "\n\n" + "최근 초기화한 시간 : " + re_time_)
        # lbx.addWidget(self.my_refresh_time)

        self.pushButton_one = QPushButton("현재 내 상태 조회하기")
        self.pushButton_one.clicked.connect(self.mystatus_refresh)

        # vbox34 = QHBoxLayout()
        # vbox34.addWidget(self.my_refresh_time)
        #
        # Vbox3434 = QVBoxLayout()
        # Vbox3434.addLayout(vbox34)
        # Vbox3434.addWidget(self.pushButton_one)

        vbox34 = QHBoxLayout()
        vbox34.addWidget(self.my_refresh_time)

        Vbox3434 = QVBoxLayout()
        Vbox3434.addLayout(vbox34)
        Vbox3434.addWidget(self.pushButton_one)

        self.com_group34.setLayout(Vbox3434)

        # self.one_cla_id_now = QLabel("       현재 내 아이디 : " + thismyid_one + "\n\n")

        # 마을 의뢰
        self.com_group6 = QGroupBox('육성, 각종템받기, 거래소등록하기, 의뢰')
        cb6 = QComboBox()
        list6 = ['스케쥴 선택', '캐릭터바꾸기', '각종템받기', '버프와물약사기', '거래소등록', '튜토육성', '의뢰_세라보그', '의뢰_바란', '의뢰_국경지대', '의뢰_유로키나산맥']
        cb6.addItems(list6)
        vbox6 = QHBoxLayout()
        vbox6.addWidget(cb6)
        maul_add = QPushButton('육성 및 행동 추가')
        maul_add.clicked.connect(self.onActivated_maul_add)

        vbox6.addWidget(maul_add)
        self.com_group6.setLayout(vbox6)


        # 던전 종류
        self.dun_group_1 = QGroupBox('균열')
        dun_g1_name = QComboBox()
        # list4 = ['던전 선택', '일반_업보', '일반_지옥', '일반_죄악', '일반_저주', '특수_마족', '특수_아르카스', '파티_묘지']
        dun_g1_list = ['균열의 땅 선택', '홍염의신전', '얼음유적지', '마리아스의동굴']
        dun_g1_name.addItems(dun_g1_list)

        dun_g1_stair = QComboBox()
        dun_g1_stair_list = ['층', '1', '2', '3', '4', '5', '6', '7']
        dun_g1_stair.addItems(dun_g1_stair_list)

        # dun_g1_step = QComboBox()
        # dun_g1_step_list = ['lv', '1', '2', '3', '4', '5']
        # dun_g1_step.addItems(dun_g1_step_list)

        dun_box_1 = QHBoxLayout()
        dun_box_1.addWidget(dun_g1_name)
        dun_box_1.addWidget(dun_g1_stair)
        # dun_box_1.addWidget(dun_g1_step)

        dungeon_1 = QPushButton('균열 추가')
        dungeon_1.clicked.connect(self.onActivated_dunjeon_1_add)

        dun_box_1.addWidget(dungeon_1)
        self.dun_group_1.setLayout(dun_box_1)

        # 던전 종류
        self.dun_group_2 = QGroupBox('심연')
        dun_g2_name = QComboBox()
        # list4 = ['던전 선택', '일반_업보', '일반_지옥', '일반_죄악', '일반_저주', '특수_마족', '특수_아르카스', '파티_묘지']
        # dun_g2_list = ['던전 선택', '다크디멘젼', '레이드', '기간토마키아']
        dun_g2_list = ['뒤틀린 심연 선택', '뒤틀린심연']
        dun_g2_name.addItems(dun_g2_list)

        dun_g2_stair = QComboBox()
        dun_g2_stair_list = ['층', '1', '2']
        dun_g2_stair.addItems(dun_g2_stair_list)

        # dun_g2_step = QComboBox()
        # dun_g2_step_list = ['lv', '1', '2', '3']
        # dun_g2_step.addItems(dun_g2_step_list)

        dun_box_2 = QHBoxLayout()
        dun_box_2.addWidget(dun_g2_name)
        dun_box_2.addWidget(dun_g2_stair)
        # dun_box_2.addWidget(dun_g2_step)

        dungeon_2 = QPushButton('심연 추가')
        dungeon_2.clicked.connect(self.onActivated_dunjeon_2_add)

        dun_box_2.addWidget(dungeon_2)
        self.dun_group_2.setLayout(dun_box_2)

        # 던전 종류
        self.dun_group_3 = QGroupBox('월드')
        dun_g3_name = QComboBox()
        # list4 = ['던전 선택', '일반_업보', '일반_지옥', '일반_죄악', '일반_저주', '특수_마족', '특수_아르카스', '파티_묘지']
        # dun_g3_list = ['데이모스전장', '모리아기지', 'coming soon']
        dun_g3_list = ['월드 던전 선택', '스피렌의안뜰']
        dun_g3_name.addItems(dun_g3_list)

        dun_g3_stair = QComboBox()
        dun_g3_stair_list = ['층', '1', '2', '3', '4', '5', '6']
        dun_g3_stair.addItems(dun_g3_stair_list)

        dun_box_3 = QHBoxLayout()
        dun_box_3.addWidget(dun_g3_name)
        dun_box_3.addWidget(dun_g3_stair)

        dungeon_3 = QPushButton('월드 추가')
        dungeon_3.clicked.connect(self.onActivated_dunjeon_3_add)

        dun_box_3.addWidget(dungeon_3)
        self.dun_group_3.setLayout(dun_box_3)


        # 사냥터
        dir_path = "C:\\my_games\\" + str(v_.game_folder) + "\\" + str(v_.data_folder)
        file_path1 = dir_path + "\\jadong\\moon_serabog.txt"
        file_path2 = dir_path + "\\jadong\\moon_baran.txt"
        file_path3 = dir_path + "\\jadong\\moon_countryregion.txt"
        file_path4 = dir_path + "\\jadong\\moon_yourokina.txt"

        if os.path.isfile(file_path1) == True:
            with open(file_path1, "r", encoding='utf-8-sig') as file:
                read_serabog = file.read().splitlines()
                list5 = []
                for i in range(len(read_serabog)):
                    read_ready = read_serabog[i].split("_")
                    list5.append(read_ready[0])
                list5.insert(0, "< 세라보그 >")

            with open(file_path2, "r", encoding='utf-8-sig') as file:
                read_baran = file.read().splitlines()
                list55 = []
                for i in range(len(read_baran)):
                    read_2_ready = read_baran[i].split("_")
                    list55.append(read_2_ready[0])
                list55.insert(0, "< 바란 >")

            with open(file_path3, "r", encoding='utf-8-sig') as file:
                read_countryregioon = file.read().splitlines()
                list555 = []
                for i in range(len(read_countryregioon)):
                    read_2_ready = read_countryregioon[i].split("_")
                    list555.append(read_2_ready[0])
                list555.insert(0, "< 국경지대 >")

            with open(file_path4, "r", encoding='utf-8-sig') as file:
                read_yourokina = file.read().splitlines()
                list5555 = []
                for i in range(len(read_yourokina)):
                    read_2_ready = read_yourokina[i].split("_")
                    list5555.append(read_2_ready[0])
                list5555.insert(0, "< 유로키나산맥 >")

            # with open(file_path3, "r", encoding='utf-8-sig') as file:
            #     read_1 = file.read()
            #     read_1 = read_1.split(":")
            #     read_1 = "< 첼라노 >/" + read_1[1]
            #     read_1 = read_1.split("/")
            #     list555 = []
            #     for i in range(len(read_1)):
            #         list555.append(read_1[i])

        self.com_group5 = QGroupBox('자동사냥터')
        cb5 = QComboBox()
        #list5 = ['자동 사냥터 선택1', '사냥_콜리아 삼거리', '사냥_마른땅 벌목지', '사냥_실바인 진흙탕', '사냥_실바인 저수지']
        cb5.addItems(list5)
        jadong1 = QPushButton('세라보그 추가')
        jadong1.clicked.connect(self.onActivated_hunt_add)

        cb55 = QComboBox()
        #list55 = ['자동 사냥터 선택2', '사냥_콜리아 삼거리', '사냥_마른땅 벌목지', '사냥_실바인 진흙탕', '사냥_실바인 저수지']
        cb55.addItems(list55)
        jadong2 = QPushButton('바란 추가')
        jadong2.clicked.connect(self.onActivated_hunt_add_2)

        cb555 = QComboBox()
        #list555 = ['자동 사냥터 선택3', '사냥_콜리아 삼거리', '사냥_마른땅 벌목지', '사냥_실바인 진흙탕', '사냥_실바인 저수지']
        cb555.addItems(list555)
        jadong3 = QPushButton('국경지대 추가')
        jadong3.clicked.connect(self.onActivated_hunt_add_3)

        cb5555 = QComboBox()
        # list555 = ['자동 사냥터 선택3', '사냥_콜리아 삼거리', '사냥_마른땅 벌목지', '사냥_실바인 진흙탕', '사냥_실바인 저수지']
        cb5555.addItems(list5555)
        jadong4 = QPushButton('유로키나산맥 추가')
        jadong4.clicked.connect(self.onActivated_hunt_add_4)


        vbox5_1 = QHBoxLayout()
        vbox5_1.addWidget(cb5)
        vbox5_1.addWidget(jadong1)

        vbox5_2 = QHBoxLayout()
        vbox5_2.addWidget(cb55)
        vbox5_2.addWidget(jadong2)

        vbox5_3 = QHBoxLayout()
        vbox5_3.addWidget(cb555)
        vbox5_3.addWidget(jadong3)

        vbox5_4 = QHBoxLayout()
        vbox5_4.addWidget(cb5555)
        vbox5_4.addWidget(jadong4)

        lastbox = QVBoxLayout()
        lastbox.addLayout(vbox5_1)
        lastbox.addLayout(vbox5_2)
        lastbox.addLayout(vbox5_3)
        lastbox.addLayout(vbox5_4)


        self.com_group5.setLayout(lastbox)

        ###

        cb_cla.activated[str].connect(self.onActivated_cla)  # 요건 함수
        cb3.activated[str].connect(self.onActivated_character)  # 요건 함수
        # cb33.activated[str].connect(self.onActivated_time)  # 요건 함수
        #던전
        dun_g1_name.activated[str].connect(self.onActivated_dunjeon_1)  # 던전1 이름
        dun_g1_stair.activated[str].connect(self.onActivated_dunjeon_1_level)  # 던전1 층수
        # dun_g1_step.activated[str].connect(self.onActivated_dunjeon_1_step)  # 던전1 난이도

        dun_g2_name.activated[str].connect(self.onActivated_dunjeon_2)  # 던전2 이름
        dun_g2_stair.activated[str].connect(self.onActivated_dunjeon_2_level)  # 던전2 층수
        # dun_g2_step.activated[str].connect(self.onActivated_dunjeon_2_step)  # 던전2 난이도

        dun_g3_name.activated[str].connect(self.onActivated_dunjeon_3)  # 던전3 이름
        dun_g3_stair.activated[str].connect(self.onActivated_dunjeon_3_level)  # 던전3 층수
        # dun_g3_step.activated[str].connect(self.onActivated_dunjeon_3_step)  # 던전3 난이도

        cb5.activated[str].connect(self.onActivated_hunt)  # 요건 함수
        cb55.activated[str].connect(self.onActivated_hunt2)  # 요건 함수
        cb555.activated[str].connect(self.onActivated_hunt3)  # 요건 함수
        cb5555.activated[str].connect(self.onActivated_hunt4)  # 요건 함수
        cb6.activated[str].connect(self.onActivated_maul)  # 요건 함수

        # self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.cellClicked.connect(self.set_label)
        rowcount = self.tableWidget.rowCount()
        colcount = self.tableWidget.columnCount()

        # 레이아웃
        hbox1 = QHBoxLayout()
        # hbox1.addWidget(self.setItems)
        hbox1.addWidget(self.mytestin)
        hbox1.addWidget(self.perfect_pause)
        hbox1.addWidget(self.again_restart)
        hbox1.addWidget(self.sell_)

        go_cla_1 = QHBoxLayout()
        go_cla_1.addWidget(self.sche_add1)

        go_cla_end = QVBoxLayout()
        go_cla_end.addLayout(go_cla_1)

        hbox7 = QHBoxLayout()
        hbox7.addStretch(4)
        hbox7.addLayout(go_cla_end)
        hbox7.addStretch(4)
        hbox7.addLayout(hbox1)

        dun_1_hbox = QHBoxLayout()
        dun_1_hbox.addWidget(self.dun_group_1)

        dun_2_hbox = QHBoxLayout()
        dun_2_hbox.addWidget(self.dun_group_2)

        dun_3_hbox = QHBoxLayout()
        dun_3_hbox.addWidget(self.dun_group_3)

        hbox4 = QHBoxLayout()
        hbox4.addWidget(self.com_group5)


        hbox5 = QHBoxLayout()
        hbox5.addWidget(self.com_group6)

        hbox33 = QHBoxLayout()
        hbox33.addWidget(self.com_group33)

        first_box_1 = QHBoxLayout()
        first_box_1.addWidget(self.force_sub)

        first_box_2 = QHBoxLayout()
        first_box_2.addWidget(self.collection_on_off)

        first_vbox_1 = QVBoxLayout()
        first_vbox_1.addLayout(first_box_1)
        first_vbox_1.addLayout(first_box_2)

        Vbox33 = QVBoxLayout()
        Vbox33.addLayout(hbox33)
        Vbox33.addWidget(self.com_group34)


        CharacterAndLevel = QVBoxLayout()
        CharacterAndLevel.addWidget(self.com_group3)
        CharacterAndLevel.addWidget(self.com_group3_level)

        Vbox2 = QVBoxLayout()
        Vbox2.addLayout(hbox5)
        Vbox2.addLayout(dun_1_hbox)
        Vbox2.addLayout(dun_2_hbox)
        Vbox2.addLayout(dun_3_hbox)
        Vbox2.addLayout(hbox4)

        hbox2 = QHBoxLayout()
        hbox2.addLayout(first_vbox_1)
        hbox2.addLayout(Vbox33)
        # hbox2.addWidget(self.com_group34)
        hbox2.addLayout(CharacterAndLevel)
        hbox2.addLayout(Vbox2)

        vbox = QVBoxLayout()

        # self.tableWidget.resizeColumnsToContents()
        vbox.addWidget(self.tableWidget)
        vbox.addWidget(self.label)
        vbox.addLayout(hbox7)
        vbox.addLayout(hbox2)
        self.setLayout(vbox)


    def moonlight_stop_perfect(self):
        try:
            print("game_Playing(self): " + str(v_.game_folder) + "_stop")
            dir_path = "C:\\my_games\\load\\" + str(v_.game_folder)
            file_path = dir_path + "\\start.txt"
            # cla.txt
            cla_data = str(v_.now_cla) + "cla"
            file_path2 = dir_path + "\\" + cla_data + ".txt"
            with open(file_path, "w", encoding='utf-8-sig') as file:
                data = 'no'
                file.write(str(data))
                time.sleep(0.2)
            with open(file_path2, "w", encoding='utf-8-sig') as file:
                data = v_.now_cla
                file.write(str(data))
                time.sleep(0.2)
            # os.execl(sys.executable, sys.executable, *sys.argv)
            sys.exit()
        except Exception as e:
            print(e)
            return 0



    def again_restart_game(self):
        # change_ready_main = False
        # change_ready_step = False

        print("업데이트 후 재시작")
        # git pull 실행 부분
        # git_dir = '{https://github.com/rntkdgnl932/ncs.git}'
        # g = git.cmd.Git(git_dir)
        # g.pull()
        # Repo('여기 비워진것은 현재 실행되는 창의 위치란 뜻...현재 실행되는 창의 위치 기준...상대경로임...')
        dir_path = "C:\\my_games\\load\\" + str(v_.game_folder)
        file_path = dir_path + "\\start.txt"
        with open(file_path, "w", encoding='utf-8-sig') as file:
            data = 'no'
            file.write(str(data))

        # my_repo = git.Repo()
        # my_repo.remotes.origin.pull()
        # time.sleep(1)
        # 실행 후 재시작 부분
        os.execl(sys.executable, sys.executable, *sys.argv)

        # self.game.isCheck = True
        # self.game.start()
        # self.again_restart_background()

    def again_restart_background(self):

        print("game_Playing(self): again_restart_background")

        # self.BackGroundPotion_.potion_back_ = True
        # self.BackGroundPotion_.start()
        # time.sleep(1)

    def onActivated_test(self, data):
        print("data", data)


        self.testerrr = TestCall()
        testtt = self.testerrr.test_time()

        print("testtt", testtt)


        read = "현재 시간 : " + str(testtt) + "\n\n"
        print("read", read)
        self.my_refresh_time_test.setText(read)



    def onActivated_slelect_gold_read(self):
        dir_path = "C:\\my_games\\" + str(v_.game_folder)
        dir_gold = "C:\\my_games\\" + str(v_.game_folder) + "\\mysettings\\gold_force"
        file_path = dir_path + "\\mysettings\\gold_force\\limit_gold.txt"

        islimitgold = False
        while islimitgold is False:
            if os.path.isfile(file_path) == True:
                with open(file_path, "r", encoding='utf-8-sig') as file:
                    v_.onForceGold = file.read()
                    islimitgold = True
            else:
                if os.path.isdir(dir_gold) == False:
                    print('강제노역 시작 골드 디렉토리 존재하지 않음')
                    os.makedirs(dir_gold)
                with open(file_path, "w", encoding='utf-8-sig') as file:
                    file.write("50만")

        return v_.onForceGold

    def onActivated_slelect_gold(self, e):
        if e != 0 and e != '얼마이하':
            v_.onForceGold = e
            print('onForceGold : ', v_.onForceGold)
            dir_path = "C:\\my_games\\" + str(v_.game_folder)
            dir_gold = "C:\\my_games\\" + str(v_.game_folder) + "\\mysettings\\gold_force"
            file_path = dir_path + "\\mysettings\\gold_force\\limit_gold.txt"

            islimitgold = False
            while islimitgold is False:
                if os.path.isfile(file_path) == True:
                    with open(file_path, "w", encoding='utf-8-sig') as file:
                        file.write(e)
                        islimitgold = True
                else:
                    if os.path.isdir(dir_gold) == False:
                        print('강제노역 시작 골드 디렉토리 존재하지 않음')
                        os.makedirs(dir_gold)
                    with open(file_path, "w", encoding='utf-8-sig') as file:
                        file.write(e)
        else:
            print("금액을 선택해 주세요.")
        self.my_limit_gold.setText("골드 : " + str(e) + " 이하 강제노역 ㄱㄱ\n")
        self.onActivated_slelect_gold_read()


    def onActivated_slelect_collection_toggle_read(self):
        print('onCollection read', v_.onCollection)
        dir_path = "C:\\my_games\\" + str(v_.game_folder)
        dir_toggle = "C:\\my_games\\" + str(v_.game_folder) + "\\mysettings\\collection"
        file_path = dir_path + "\\mysettings\\collection\\collection_toggle.txt"

        isToggle = False
        while isToggle is False:
            if os.path.isfile(file_path) == True:
                with open(file_path, "r", encoding='utf-8-sig') as file:

                    read_tgl = file.read()
                    if read_tgl == "on":
                        isToggle = True
                        v_.onCollection = True
                    else:
                        isToggle = True
                        v_.onCollection = False
            else:
                if os.path.isdir(dir_toggle) == False:
                    print('토글 디렉토리 존재하지 않음')
                    os.makedirs(dir_toggle)
                with open(file_path, "w", encoding='utf-8-sig') as file:
                    file.write("off")
        return v_.onCollection

    def onActivated_slelect_collection_toggle(self, e):
        # global onCollection
        v_.onCollection = e
        print('onCollection change', v_.onCollection)
        dir_path = "C:\\my_games\\" + str(v_.game_folder)
        dir_toggle = "C:\\my_games\\" + str(v_.game_folder) + "\\mysettings\\collection"
        file_path = dir_path + "\\mysettings\\collection\\collection_toggle.txt"

        isToggle = False
        while isToggle is False:
            if os.path.isfile(file_path) == True:
                with open(file_path, "w", encoding='utf-8-sig') as file:
                    isToggle = True
                    if e == True:
                        file.write("on")
                    else:
                        file.write("off")
            else:
                if os.path.isdir(dir_toggle) == False:
                    print('토글 디렉토리 존재하지 않음')
                    os.makedirs(dir_toggle)
                with open(file_path, "w", encoding='utf-8-sig') as file:
                    file.write("off")
        if v_.onCollection == True:
            tgl_now = "On"
        else:
            tgl_now = "Off"
        self.now_toggle.setText("다크디멘션 : " + str(tgl_now) + "\n")
        self.tgl.setChecked(v_.onCollection)
        #self.set_rand_int()

    def onActivated_cla(self, text):
        global onCla
        if text != 0 and text != '클라 선택':
            onCla = text
            print('onCla', onCla)
        else:
            onCla = 'none'
            print("클라를 선택해 주세요.")
    def onActivated_character(self, text):
        global onCharacter
        if text != 0 and text != '캐릭터 선택':
            onCharacter = text
            print('onCharacter', onCharacter)
        else:
            onCharacter = 0
            print("캐릭터를 선택해 주세요.")

    def onActivated_one_character_level(self, text):
        character_level_ = self.require_level_in.text()  # line_edit text 값 가져오기
        print(character_level_)

        result_number_check = character_level_.isdigit()
        if result_number_check == True:
            character_level_result = "1차 매수 금액 : " + character_level_
            self.one_require_level.setText(character_level_result)
            dir_path = "C:\\my_games\\" + str(v_.game_folder)
            file_path = dir_path + "\\mysettings\\my_level\\one_character.txt"
            with open(file_path, "w", encoding='utf-8-sig') as file:
                file.write(character_level_)



        else:
            print("hi")



    def onActivated_two_character_level(self, text):
        character_level_ = self.require_level_in.text()  # line_edit text 값 가져오기
        print(character_level_)

        result_number_check = character_level_.isdigit()
        if result_number_check == True:
            character_level_result = "2차 매도 금액 : " + character_level_
            self.two_require_level.setText(character_level_result)
            dir_path = "C:\\my_games\\" + str(v_.game_folder)
            file_path = dir_path + "\\mysettings\\my_level\\two_character.txt"
            with open(file_path, "w", encoding='utf-8-sig') as file:
                file.write(character_level_)
        else:
            print("jkj")




    def onActivated_dunjeon_1(self, text):
        global onDunjeon_1
        if text != 0 and text != '균열의 땅 선택':
            onDunjeon_1 = text
            print('onDunjeon_1', onDunjeon_1)
        else:
            onDunjeon_1 = 'none'
            print("던전을 선택해 주세요.")

    def onActivated_dunjeon_1_level(self, text):
        global onDunjeon_1_level
        if text != 0 and text != '층':
            onDunjeon_1_level = text
            print('onDunjeon_1_level', onDunjeon_1_level)
        else:
            onDunjeon_1_level = 0
            print("던전 층수를 선택해 주세요.")



    def onActivated_dunjeon_2(self, text):
        global onDunjeon_2
        if text != 0 and text != '뒤틀린 심연 선택':
            onDunjeon_2 = text
            print('onDunjeon_2', onDunjeon_2)
        else:
            onDunjeon_2 = 'none'
            print("던전을 선택해 주세요.")

    def onActivated_dunjeon_2_level(self, text):
        global onDunjeon_2_level
        if text != 0 and text != '층':
            onDunjeon_2_level = text
            print('onDunjeon_2_level', onDunjeon_2_level)
        else:
            onDunjeon_2_level = 0
            print("던전 층수를 선택해 주세요.")


    def onActivated_dunjeon_3(self, text):
        global onDunjeon_3
        if text != 0 and text != '월드 던전 선택':
            onDunjeon_3 = text
            print('onDunjeon_3', onDunjeon_3)
        else:
            onDunjeon_3 = 'none'
            print("던전을 선택해 주세요.")

    def onActivated_dunjeon_3_level(self, text):
        global onDunjeon_3_level
        if text != 0 and text != '층':
            onDunjeon_3_level = text
            print('onDunjeon_3_level', onDunjeon_3_level)
        else:
            onDunjeon_3_level = 0
            print("던전 층수를 선택해 주세요.")

    # def onActivated_dunjeon_3_step(self, text):
    #     global onDunjeon_3_step
    #     if text != 0 and text != 'lv':
    #         onDunjeon_3_step = text
    #         print('onDunjeon_3_step', onDunjeon_3_step)
    #     else:
    #         onDunjeon_3_step = 0
    #         print("던전 난이도를 선택해 주세요.")

    def onActivated_hunt(self, text):
        global onHunt
        if text != 0 and text != '< 세라보그 >':
            onHunt = text
            print('onHunt', onHunt)
        else:
            onHunt = 'none'
            print("자동 사냥터를 선택해 주세요.")
    def onActivated_hunt2(self, text):
        global onHunt2
        if text != 0 and text != '< 바란 >':
            onHunt2 = text
            print('onHunt2', onHunt2)
        else:
            onHunt2 = 'none'
            print("자동 사냥터를 선택해 주세요.")
    def onActivated_hunt3(self, text):
        global onHunt3
        if text != 0 and text != '< 국경지대 >':
            onHunt3 = text
            print('onHunt3', onHunt3)
        else:
            onHunt3 = 'none'
            print("자동 사냥터를 선택해 주세요.")

    def onActivated_hunt4(self, text):
        global onHunt4
        if text != 0 and text != '< 유로키나산맥 >':
            onHunt4 = text
            print('onHunt4', onHunt4)
        else:
            onHunt4 = 'none'
            print("자동 사냥터를 선택해 주세요.")

    def onActivated_maul(self, text):
        global onMaul
        if text != 0 and text != '마을 의뢰 장소 선택':
            onMaul = text
            print('onMaul', onMaul)
        else:
            onMaul = 'none'
            print("마을 의뢰 장소를 선택해 주세요.")


    def onActivated_dunjeon_1_add(self):
        char_ = onCharacter
        dun_ = "던전/균열/" + str(onDunjeon_1) + "_" + str(onDunjeon_1_level)
            # print('char_', char_)
            # print('dun_', dun_)
            #
            # if onCla == "One" or onCla == "Two":
            #     data = "One:" + char_ + ":" + dun_ + ":대기중:" + "Two:" + char_ + ":" + dun_ + ":대기중\n"
            # elif onCla == "Three" or onCla == "Four":
            #     data = "Three:" + char_ + ":" + dun_ + ":대기중:" + "Four:" + char_ + ":" + dun_ + ":대기중\n"
            #
            #
            # print(data)
            # self.onActivated_dunjeon_add2(data)
    def onActivated_dunjeon_2_add(self):
        char_ = onCharacter
        dun_ = "던전/심연/" + str(onDunjeon_2) + "_" + str(onDunjeon_2_level)
        # if onCharacter == 0:
        #     pyautogui.alert(button='넵', text='캐릭터를 선택해 주시지예', title='뭐합니꺼')
        # elif onCla == 'none':
        #     pyautogui.alert(button='넵', text='몇 클라인지 선택해 주시지예', title='뭐합니꺼')
        # elif onDunjeon_2 == '던전 선택' or onDunjeon_2 == 'none' or onDunjeon_2_level == 0 or onDunjeon_2_level == "층":
        #     pyautogui.alert(button='넵', text='던전 및 층수를 선택해 주시지예', title='아 진짜 뭐합니꺼')
        # elif onCharacter != 0 and (onDunjeon_2 != '던전 선택' or onDunjeon_2 != 'none'):
        #     print('char_', char_)
        #     print('dun_', dun_)
        #
        #     if onCla == "One" or onCla == "Two":
        #         data = "One:" + char_ + ":" + dun_ + ":대기중:" + "Two:" + char_ + ":" + dun_ + ":대기중\n"
        #     elif onCla == "Three" or onCla == "Four":
        #         data = "Three:" + char_ + ":" + dun_ + ":대기중:" + "Four:" + char_ + ":" + dun_ + ":대기중\n"
        #
        #
        #     print(data)
        #     self.onActivated_dunjeon_add2(data)

    def onActivated_dunjeon_3_add(self):
        char_ = onCharacter
        dun_ = "던전/월드/" + str(onDunjeon_3) + "_" + str(onDunjeon_3_level)
        # if onCharacter == 0:
        #     pyautogui.alert(button='넵', text='캐릭터를 선택해 주시지예', title='뭐합니꺼')
        # elif onCla == 'none':
        #     pyautogui.alert(button='넵', text='몇 클라인지 선택해 주시지예', title='뭐합니꺼')
        # elif onDunjeon_3 == '던전 선택' or onDunjeon_3 == 'none' or onDunjeon_3_level == 0 or onDunjeon_3_level == "층":
        #     pyautogui.alert(button='넵', text='던전 및 층수를 선택해 주시지예', title='아 진짜 뭐합니꺼')
        # elif onCharacter != 0 and (onDunjeon_2 != '던전 선택' or onDunjeon_2 != 'none'):
        #     print('char_', char_)
        #     print('dun_', dun_)
        #
        #     if onCla == "One" or onCla == "Two":
        #         data = "One:" + char_ + ":" + dun_ + ":대기중:" + "Two:" + char_ + ":" + dun_ + ":대기중\n"
        #     elif onCla == "Three" or onCla == "Four":
        #         data = "Three:" + char_ + ":" + dun_ + ":대기중:" + "Four:" + char_ + ":" + dun_ + ":대기중\n"
        #
        #
        #     print(data)
        #     self.onActivated_dunjeon_add2(data)

    def onActivated_dunjeon_add2(self, data):
        global onCharacter, onDunjeon, rowcount, colcount
        print("rowcount", rowcount)
        print("colcount", colcount)
        self.table_load()

        print("data", data)
        # self.tableWidget.removeRow(5)
        self.tableWidget.insertRow(self.tableWidget.rowCount())
        row_add = self.tableWidget.rowCount() - 1
        data_ = re.sub("\n", "", data)
        datas = data_.split(":")
        # datas = dataed.replace("\n", "")
        print("datas", datas)
        print("datas", datas[0])
        print(len(datas))
        print(range(colcount))
        for i in range(len(datas)):
            self.tableWidget.setItem(row_add, i, QTableWidgetItem(datas[i]))
        self.mySchedule_add(data)
        rowcount = self.tableWidget.rowCount()

    def onActivated_hunt_add(self):
        global onCharacter, onHunt
        char_ = onCharacter
        # hun_ = onHunt
        hun_ = "사냥/serabog/" + onHunt
        # if onCharacter == 0:
        #     pyautogui.alert(button='넵', text='캐릭터를 선택해 주시지예', title='뭐합니꺼')
        # elif onHunt == '< 세라보그 >' or onHunt == 'none':
        #     pyautogui.alert(button='넵', text='던전을 선택해 주시지예', title='뭐합니꺼')
        # elif onCharacter != 0 and onHunt != '< 세라보그 >':
        #     print('char_', char_)
        #     print('dun_', hun_)
        #
        #     if onCla == "One" or onCla == "Two":
        #         data = "One:" + char_ + ":" + hun_ + ":대기중:" + "Two:" + char_ + ":" + hun_ + ":대기중\n"
        #     elif onCla == "Three" or onCla == "Four":
        #         data = "Three:" + char_ + ":" + hun_ + ":대기중:" + "Four:" + char_ + ":" + hun_ + ":대기중\n"
        #
        #
        #     print(data)
        #     self.onActivated_hunt_add2(data)
    def onActivated_hunt_add_2(self):
        global onCharacter, onHunt2
        char_ = onCharacter
        # hun_ = onHunt2
        hun_ = "사냥/baran/" + onHunt2
        # if onCharacter == 0:
        #     pyautogui.alert(button='넵', text='캐릭터를 선택해 주시지예', title='뭐합니꺼')
        # elif onHunt2 == '< 바란 >' or onHunt2 == 'none':
        #     pyautogui.alert(button='넵', text='던전을 선택해 주시지예', title='뭐합니꺼')
        # elif onCharacter != 0 and onHunt2 != '< 바란 >':
        #     print('char_', char_)
        #     print('dun_', hun_)
        #
        #     if onCla == "One" or onCla == "Two":
        #         data = "One:" + char_ + ":" + hun_ + ":대기중:" + "Two:" + char_ + ":" + hun_ + ":대기중\n"
        #     elif onCla == "Three" or onCla == "Four":
        #         data = "Three:" + char_ + ":" + hun_ + ":대기중:" + "Four:" + char_ + ":" + hun_ + ":대기중\n"
        #
        #
        #     print(data)
        #     self.onActivated_hunt_add2(data)
    def onActivated_hunt_add_3(self):
        global onCharacter, onHunt3
        char_ = onCharacter
        # # hun_ = "사냥_" + "첼라노_" + onHunt3
        # hun_ = "사냥/countryregioon/" + onHunt3
        # if onCharacter == 0:
        #     pyautogui.alert(button='넵', text='캐릭터를 선택해 주시지예', title='뭐합니꺼')
        # elif onHunt3 == '< 국경지대 >' or onHunt3 == 'none':
        #     pyautogui.alert(button='넵', text='던전을 선택해 주시지예', title='뭐합니꺼')
        # elif onCharacter != 0 and onHunt3 != '< 국경지대 >':
        #     print('char_', char_)
        #     print('dun_', hun_)
        #
        #     if onCla == "One" or onCla == "Two":
        #         data = "One:" + char_ + ":" + hun_ + ":대기중:" + "Two:" + char_ + ":" + hun_ + ":대기중\n"
        #     elif onCla == "Three" or onCla == "Four":
        #         data = "Three:" + char_ + ":" + hun_ + ":대기중:" + "Four:" + char_ + ":" + hun_ + ":대기중\n"
        #
        #
        #     print(data)
        #     self.onActivated_hunt_add2(data)

    def onActivated_hunt_add_4(self):
        global onCharacter, onHunt4
        char_ = onCharacter
        hun_ = "사냥/yourokina/" + onHunt4
        # if onCharacter == 0:
        #     pyautogui.alert(button='넵', text='캐릭터를 선택해 주시지예', title='뭐합니꺼')
        # elif onHunt4 == '< 유로키나산맥 >' or onHunt4 == 'none':
        #     pyautogui.alert(button='넵', text='던전을 선택해 주시지예', title='뭐합니꺼')
        # elif onCharacter != 0 and onHunt4 != '< 유로키나산맥 >':
        #     print('char_', char_)
        #     print('dun_', hun_)
        #
        #     if onCla == "One" or onCla == "Two":
        #         data = "One:" + char_ + ":" + hun_ + ":대기중:" + "Two:" + char_ + ":" + hun_ + ":대기중\n"
        #     elif onCla == "Three" or onCla == "Four":
        #         data = "Three:" + char_ + ":" + hun_ + ":대기중:" + "Four:" + char_ + ":" + hun_ + ":대기중\n"
        #
        #
        #     print(data)
        #     self.onActivated_hunt_add2(data)

    def onActivated_hunt_add2(self, data):
        global onCharacter, onDunjeon, rowcount, colcount
        print("rowcount", rowcount)
        print("colcount", colcount)
        self.table_load()

        print("data", data)
        # self.tableWidget.removeRow(5)
        self.tableWidget.insertRow(self.tableWidget.rowCount())
        row_add = self.tableWidget.rowCount() - 1
        data_ = re.sub("\n", "", data)
        datas = data_.split(":")
        # datas = dataed.replace("\n", "")
        print("datas", datas)
        print("datas", datas[0])
        print(len(datas))
        print(range(colcount))
        for i in range(len(datas)):
            self.tableWidget.setItem(row_add, i, QTableWidgetItem(datas[i]))
            self.tableWidget.item(row_add, i).setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.mySchedule_add(data)
        rowcount = self.tableWidget.rowCount()

    def onActivated_maul_add(self):
        global onCharacter, onMaul
        char_ = onCharacter
        maul_ = onMaul
        # if onCharacter == 0:
        #     pyautogui.alert(button='넵', text='캐릭터를 선택해 주시지예', title='뭐합니꺼')
        # elif onMaul == '마을 의뢰 장소 선택' or onMaul == 'none':
        #     pyautogui.alert(button='넵', text='마을 의뢰 장소를 선택해 주시지예', title='아 진짜 뭐합니꺼')
        # elif onCharacter != 0 and onMaul != '마을 의뢰 장소 선택':
        #     print('char_', char_)
        #     print('maul_', maul_)
        #     if onCla == "One" or onCla == "Two":
        #         data = "One:" + char_ + ":" + maul_ + ":대기중:" + "Two:" + char_ + ":" + maul_ + ":대기중\n"
        #     elif onCla == "Three" or onCla == "Four":
        #         data = "Three:" + char_ + ":" + maul_ + ":대기중:" + "Four:" + char_ + ":" + maul_ + ":대기중\n"
        #     print(data)
        #     self.onActivated_maul_add2(data)
        #     result = self.mySchedule_add(data)
        # if result == True:
        #     # self.set_rand_int()
        #     self.__init__()

    def onActivated_maul_add2(self, data):
        global onCharacter, onMaul, rowcount, colcount
        print("rowcount", rowcount)
        print("colcount", colcount)
        self.table_load()

        print("data", data)
        # self.tableWidget.removeRow(5)
        self.tableWidget.insertRow(self.tableWidget.rowCount())
        row_add = self.tableWidget.rowCount() - 1
        data_ = re.sub("\n", "", data)
        datas = data_.split(":")
        # datas = dataed.replace("\n", "")
        print("datas", datas)
        print("datas", datas[0])
        print(len(datas))
        print(range(colcount))
        for i in range(len(datas)):
            self.tableWidget.setItem(row_add, i, QTableWidgetItem(datas[i]))
        self.mySchedule_add(data)
        rowcount = self.tableWidget.rowCount()

    def mystatus_refresh(self):
        print("현재상태 초기화")
        # 초기화 시간
        dir_path = "C:\\my_games\\" + str(v_.game_folder)
        file_path2 = dir_path + "\\mysettings\\refresh_time\\quest.txt"
        file_path13 = dir_path + "\\mysettings\\refresh_time\\refresh_time.txt"

        isRefresh = False
        while isRefresh is False:
            if os.path.isfile(file_path13) == True:
                with open(file_path13, "r", encoding='utf-8-sig') as file:
                    refresh_time = file.read()
                    refresh_time_bool = refresh_time.isdigit()
                    if refresh_time_bool == True:
                        isRefresh = True
                        print("refresh_time", refresh_time)
                    else:
                        with open(file_path13, "w", encoding='utf-8-sig') as file:
                            file.write(str(4))
            else:
                with open(file_path13, "w", encoding='utf-8-sig') as file:
                    file.write(str(4))

        if os.path.isfile(file_path2) == True:
            # 파일 읽기
            with open(file_path2, "r", encoding='utf-8-sig') as file:
                lines2 = file.read().splitlines()
                day_ = lines2[0].split(":")
                re_time_ = str(day_[0]) + " => " + str(day_[1] + "시")
                print("최근 초기화 시간 : ", re_time_)
        else:
            re_time_ = "아직 모름..."
        self.my_refresh_time.setText("현재 초기화 시간 : " + str(refresh_time) + "\n\n" + "최근 초기화한 시간 : " + re_time_)
        self.set_rand_int()

    def set_rand_int(self):
        try:

            is_file = False

            dir_path = "C:\\my_games\\" + str(v_.game_folder)
            file_path = dir_path + "\\mysettings\\myschedule\\schedule.txt"
            file_path3 = dir_path + "\\mysettings\\myschedule\\schedule2.txt"
            rich_mystock_path_1 = dir_path + "\\mysettings\\myschedule\\result_kiwoom_data_1.txt"
            rich_mystock_path_2 = dir_path + "\\mysettings\\myschedule\\result_kiwoom_data_2.txt"

            if os.path.isfile(file_path) == True:
                # 파일 읽기
                with open(file_path, "r", encoding='utf-8-sig') as file:

                    # content = file.read()
                    lines = json.load(file)
                    if lines:
                        is_file = True
                        # lines = json.load(file)
            else:
                print('파일 없당')
                if os.path.isdir(dir_path) == True:
                    print('디렉토리 존재함')
                    with open(file_path, "r", encoding='utf-8-sig') as file:
                        # content = file.read()
                        lines = json.load(file)
                        if lines:
                            is_file = True
                            # lines = json.load(file)
                    # with open(file_path3, "r", encoding='utf-8-sig') as file:
                    #     shcedule = file.read().splitlines()
                    #     with open(file_path, "w", encoding='utf-8-sig') as file:
                    #         file.write(str(shcedule))
                    #         with open(file_path, "r", encoding='utf-8-sig') as file:
                    #             lines = file.read()
                else:
                    print('디렉토리 존재하지 않음')
                    os.makedirs(dir_path)
                    # with open(file_path3, "r", encoding='utf-8-sig') as file:
                    #     shcedule = json.load(file)
                    #     with open(file_path, "w", encoding='utf-8-sig') as file:
                    #         file.write(shcedule)
                    #     # with open(file_path, "w", encoding='utf-8-sig') as file:
                    #     #     json.dump(shcedule, file)
                    #         with open(file_path, "r", encoding='utf-8-sig') as file:
                    #             lines = json.load(file)


            # self.tableWidget.insertRow(self.tableWidget.rowCount(2))
            # "종목", "종목코드", "보유수량", "현재매입금액", "매입가", "현재가", "수익률(%)"
            self.tableWidget.setColumnWidth(0, 200)
            self.tableWidget.setColumnWidth(1, 100)
            self.tableWidget.setColumnWidth(2, 65)
            self.tableWidget.setColumnWidth(3, 150)
            self.tableWidget.setColumnWidth(4, 100)
            self.tableWidget.setColumnWidth(5, 100)
            self.tableWidget.setColumnWidth(6, 120)


            remove_ = self.tableWidget.rowCount()
            print("remove_", remove_)
            if remove_ > 0:
                for i in range(remove_):
                    self.tableWidget.removeRow(0)



            if is_file == True:

                num_rows = len(lines)  # 파일에서 읽은 데이터의 행 수를 가져옴

                print("num_rowsnum_rowsnum_rows", num_rows)

                result_stocks = "현재 : " + str(num_rows) + "\n\n"
                self.my_stock_load.setText(str(result_stocks))
                self.my_stock_load.repaint()
                print("내 보유종목 갯수", num_rows)

                # 파일읽기
                if os.path.isfile(rich_mystock_path_1) == True:
                    # 파일 읽기
                    with open(rich_mystock_path_1, "r", encoding='utf-8-sig') as file:
                        rich_mystock_read_1 = file.read()
                        self.my_stock_all_buy_money.setText(str(rich_mystock_read_1))
                        self.my_stock_all_buy_money.repaint()
                if os.path.isfile(rich_mystock_path_2) == True:
                    # 파일 읽기
                    with open(rich_mystock_path_2, "r", encoding='utf-8-sig') as file:
                        rich_mystock_read_2 = file.read()
                        self.my_stock_all_rate.setText(str(rich_mystock_read_2))
                        self.my_stock_all_rate.repaint()


                for row, (code, info) in enumerate(lines.items()):
                    self.tableWidget.insertRow(row)
                    self.tableWidget.setItem(row, 0, QTableWidgetItem(info.get('종목명', '')))
                    self.tableWidget.setItem(row, 1, QTableWidgetItem(code))

                    item_refresh = QTableWidgetItem()
                    item_refresh.setData(Qt.DisplayRole, int(info.get('보유수량', 0))) # 숫자로 설정 (정렬을 위해)
                    self.tableWidget.setItem(row, 2, item_refresh)

                    item_refresh = QTableWidgetItem()
                    item_refresh.setData(Qt.DisplayRole, int(info.get('매입금액', 0)))  # 숫자로 설정 (정렬을 위해)
                    self.tableWidget.setItem(row, 3, item_refresh)

                    item_refresh = QTableWidgetItem()
                    item_refresh.setData(Qt.DisplayRole, int(info.get('매입가', 0)))  # 숫자로 설정 (정렬을 위해)
                    self.tableWidget.setItem(row, 4, item_refresh)

                    item_refresh = QTableWidgetItem()
                    item_refresh.setData(Qt.DisplayRole, int(info.get('현재가', 0)))  # 숫자로 설정 (정렬을 위해)
                    self.tableWidget.setItem(row, 5, item_refresh)

                    item_refresh = QTableWidgetItem()
                    item_refresh.setData(Qt.DisplayRole, float(info.get('수익률(%)', 0)))  # 숫자로 설정 (정렬을 위해)
                    self.tableWidget.setItem(row, 6, item_refresh)

                # 제목 셀에 진한 글씨체 적용
                header_font = QFont()
                header_font.setBold(True)
                for i in range(self.tableWidget.columnCount()):
                    item = QTableWidgetItem(self.tableWidget.horizontalHeaderItem(i).text())
                    item.setFont(header_font)
                    self.tableWidget.setHorizontalHeaderItem(i, item)

                # 값 셀 가운데 정렬
                for i in range(self.tableWidget.rowCount()):
                    for j in range(self.tableWidget.columnCount()):
                        item = self.tableWidget.item(i, j)
                        if item is not None:
                            item.setTextAlignment(Qt.AlignCenter)
                # 수익률이 플러스일 때는 빨간색, 마이너스일 때는 파란색으로 표시
                for i in range(self.tableWidget.rowCount()):
                    profit_loss_item = self.tableWidget.item(i, 6)  # 수익률(%) 열에 해당하는 item
                    if profit_loss_item is not None:
                        profit_loss = float(profit_loss_item.text().replace('%', ''))
                        if profit_loss > 0:
                            profit_loss_item.setForeground(QColor('red'))
                        elif profit_loss < 0:
                            profit_loss_item.setForeground(QColor('blue'))

            else:
                self.tableWidget.setRowCount(1)
                self.tableWidget.setItem(0, 0, QTableWidgetItem("보유종목이 없습니다."))
                self.tableWidget.setSpan(0, 0, 1, 7)  # Merge cells for the message



        except Exception as e:
            print(e)
            return 0


    def set_label(self, row, column):
        global thisRow, thisCol
        item = self.tableWidget.item(row, column)
        value = item.text()
        col = str(row + 1)
        col_ = int(col)
        col2 = str(column + 1)
        col_2 = int(col2)
        thisRow = col_
        thisCol = col_2
        print("0열 데이타", col_)  # good
        print("Row", str(row + 1))
        print("Column", str(column + 1))
        print("value", str(value))
        label_str = 'Row: ' + str(row + 1) + ', Column: ' + str(column + 1) + ', Value: ' + str(value)
        self.label.setText(label_str)

    # 스케쥴 수정 및 추가
    def sche_load_(self):
        global table_datas
        try:
            rowcount = self.tableWidget.rowCount()
            print("schedule!!!")
            datas = ""
            if rowcount != 0:
                for i in range(0, rowcount):
                    for j in range(0, colcount):
                        data = self.tableWidget.item(i, j)
                        if data is not None:
                            if j + 1 == colcount:
                                datas += str(data.text()) + "\n"
                            else:
                                datas += str(data.text()) + ":"

                        else:
                            print("blank")
            # redata = ' '.join(datas).split()
            table_datas = datas
            return table_datas
        except Exception as e:
            print(e)
            return 0

    def table_load(self):
        global rowcount, colcount
        print("rowcount", rowcount)
        print("colcount", colcount)
        if rowcount != 0:
            for i in range(0, rowcount):
                for j in range(0, colcount):
                    data = self.tableWidget.item(i, j)
                    if data is not None:
                        if j + 1 == colcount:
                            item = QTableWidgetItem()
                            item.setText(str(data.text()))
                            # datas += str(data.text()) + "\n"
                            self.tableWidget.setItem(i, j, item)
                        else:
                            item = QTableWidgetItem()
                            item.setText(str(data.text()))
                            # datas += str(data.text()) + ":"
                            self.tableWidget.setItem(i, j, item)

                    else:
                        print("blank")



    def sell_now(self):
        global rowcount, colcount
        try:
            print("종목 매도")

        except Exception as e:
            print(e)
            return 0







    # def mySchedule_is(self):
    #     try:
    #         ##############다시 코딩
    #         dir_path = "C:\\my_games\\" + str(v_.game_folder)
    #         file_path = dir_path + "\\mysettings\\myschedule\\schedule.txt"
    #         if os.path.isfile(file_path) == True:
    #             # 파일 읽기
    #             with open(file_path, "r", encoding='utf-8-sig') as file:
    #                 lines = file.read()
    #
    #         remove_ = self.tableWidget.rowCount()
    #         print("remove_", remove_)
    #         for i in range(remove_ - 1):
    #             self.tableWidget.removeRow(0)
    #
    #         refresh_result = lines.split("\n")
    #         rowcount = self.tableWidget.rowCount()
    #         print("refresh_rowcount", self.tableWidget.rowCount())
    #         count_ = len(refresh_result) - rowcount - 1
    #         for i in range(count_):
    #             self.tableWidget.insertRow(self.tableWidget.rowCount())
    #         print("refresh_rowcount2", self.tableWidget.rowCount())
    #         self.tableWidget.clear
    #         self.set_rand_int()
    #         self.tableWidget.clear
    #     except Exception as e:
    #         print(e)
    #         return 0

    def mySchedule_add(self, data):
        try:
            schedule_add = False
            how_ = 'add'
            datas = str(data)
            result = self.mySchedule_change(how_, datas)
            print("added_", result)
            if result == True:
                schedule_add = True
                self.mystatus_refresh()
                print('스케쥴 추가 됨')

            return schedule_add
        except Exception as e:
            print(e)
            return 0

    def mySchedule_change(self, how_, datas):
        try:
            print("mySchedule_change")
            # ishow_ = False
            # dir_path = "C:\\my_games\\" + str(v_.game_folder)
            # file_path = dir_path + "\\mysettings\\myschedule\\schedule.txt"
            # file_path3 = dir_path + "\\mysettings\\myschedule\\schedule2.txt"
            # print(os.path.isfile(file_path))
            # print(os.path.isdir(dir_path))
            #
            # if os.path.isdir(dir_path) == True:
            #     print('디렉토리 존재')
            # else:
            #     os.makedirs(dir_path)
            #
            # print("how_", how_)
            # if how_ == "add":
            #     with open(file_path, "a", encoding='utf-8-sig') as file:
            #         print("add????", datas)
            #         file.write(datas)
            #         ishow_ = True
            #     # reset_schedule_ = ""
            #     # with open(file_path, "r", encoding='utf-8-sig') as file:
            #     #     lines = file.read().splitlines()
            #     #     lines = ' '.join(lines).split()
            #     #     print("lineslineslineslineslineslineslineslineslineslineslines", lines)
            #     #     for i in range(len(lines)):
            #     #         complete_ = lines[i].split(":")
            #     #         for j in range(len(complete_)):
            #     #             if j < 3:
            #     #                 reset_schedule_ += complete_[j] + ":"
            #     #             if j == 3:
            #     #                 reset_schedule_ += '대기중:'
            #     #             if 3 < j < 7:
            #     #                 reset_schedule_ += complete_[j] + ":"
            #     #             if j == 7:
            #     #                 reset_schedule_ += "대기중\n"
            #     #     print("reset_schedule_reset_schedule_reset_schedule_reset_schedule_reset_schedule_",
            #     #           reset_schedule_)
            #     #     with open(file_path3, "w", encoding='utf-8-sig') as file:
            #     #         file.write(reset_schedule_)
            #     ishow_ = True
            #     reset_schedule_ = ""
            #     with open(file_path, "r", encoding='utf-8-sig') as file:
            #         lines = file.read().splitlines()
            #         lines = ' '.join(lines).split()
            #
            #         isSchedule_ = False
            #         while isSchedule_ is False:
            #             if lines == [] or lines == "":
            #                 print("스케쥴이 비었다 : myQuest_play_check")
            #                 with open(file_path3, "r", encoding='utf-8-sig') as file:
            #                     schedule_ready = file.read()
            #                 with open(file_path, "w", encoding='utf-8-sig') as file:
            #                     file.write(schedule_ready)
            #                 with open(file_path, "r", encoding='utf-8-sig') as file:
            #                     lines = file.read().splitlines()
            #             else:
            #                 isSchedule_ = True
            #
            #         for i in range(len(lines)):
            #             complete_ = lines[i].split(":")
            #             for j in range(len(complete_)):
            #                 if j < 3:
            #                     reset_schedule_ += complete_[j] + ":"
            #                 if j == 3:
            #                     reset_schedule_ += '대기중:'
            #                 if 3 < j < 7:
            #                     reset_schedule_ += complete_[j] + ":"
            #                 if j == 7:
            #                     reset_schedule_ += "대기중\n"
            #
            #         print('reset_schedule_', reset_schedule_)
            #         # with open(file_path, "w", encoding='utf-8-sig') as file:
            #         #     file.write(reset_schedule_)
            #         with open(file_path3, "w", encoding='utf-8-sig') as file:
            #             file.write(reset_schedule_)
            #     self.set_rand_int()
            #
            # elif how_ == "modify":
            #     with open(file_path, "w", encoding='utf-8-sig') as file:
            #         file.write(datas)
            #
            #     # ishow_ = True
            #     # reset_schedule_ = ""
            #     # lines = datas
            #     # lines = lines.split('\n')
            #     # lines = ' '.join(lines).split()
            #     #
            #     #
            #     #
            #     # for i in range(len(lines)):
            #     #     complete_ = lines[i].split(":")
            #     #     for j in range(len(complete_)):
            #     #         if j < 3:
            #     #             reset_schedule_ += complete_[j] + ":"
            #     #         if j == 3:
            #     #             reset_schedule_ += '대기중:'
            #     #         if 3 < j < 7:
            #     #             reset_schedule_ += complete_[j] + ":"
            #     #         if j == 7:
            #     #
            #     #             reset_schedule_ += '대기중\n'
            #     #
            #     # print('reset_schedule_', reset_schedule_)
            #     # with open(file_path3, "w", encoding='utf-8-sig') as file:
            #     #     file.write(reset_schedule_)
            #     self.set_rand_int()
            #
            # return ishow_
        except Exception as e:
            print(e)
            return 0


    def rich_start1_ready(self):
        try:

            # self.sche_add1.setText("부자 되는 중")
            # self.sche_add1.setDisabled(True)
            #
            # self.kiwoom = Kiwoom()

            result_game = game_start()
            print("start?????????", result_game)
            if result_game == True:
                self.rich_start1()

            else:

                reply = QMessageBox.question(self, '주투홀', '시잘할까요?',
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                print("reply", reply)

                # 16384 => yes, 65536 => no

                if reply == QMessageBox.Yes:
                    print("yes", reply)
                else:
                    print("no", reply)

        except Exception as e:
            print(e)
            return 0

    def rich_start1(self):
        try:

            self.sche_add1.setText("부자 되는 중")
            self.sche_add1.setDisabled(True)

            dir_path = "C:\\my_games\\load\\" + str(v_.game_folder)
            file_path = dir_path + "\\start.txt"

            rich_dir_path = "C:\\my_games\\" + str(v_.game_folder)
            rich_file_path = rich_dir_path + "\\mysettings\\myschedule\\schedule.txt"

            rich_mystock_path_1 = rich_dir_path + "\\mysettings\\myschedule\\result_kiwoom_data_1.txt"
            rich_mystock_path_2 = rich_dir_path + "\\mysettings\\myschedule\\result_kiwoom_data_2.txt"

            with open(file_path, "w", encoding='utf-8-sig') as file:
                data = 'yes'
                file.write(str(data))

            self.kiwoom = Kiwoom()
            self.kiwoom.get_kiwoom_ready()

            ######################## 내 종목에서 second_order_stock.txt 안의 종목이 없으면 txt 내용 삭제 and 처음 잔고 확인시 금액 판별 후 txt에 넣기

            ## 실전테스트
            # code = "005930"
            #
            # self.kiwoom.calculate_biii(code=code)


            # self.kiwoom.minute_kiwoom_db(code=code, tic=10)
            # #
            # average_price = self.kiwoom.result_minute_kiwoom_db()
            # if code in average_price.keys():
            #     print("존재한다!!!!!!!!10분 240 평균값:", average_price)
            #     print("존재한다!!!!!!!!10분 240 평균값:", average_price[code]["d_day_0_240"])
            #
            # else:
            #     print("존재하지 않는다!!!!!!!!!!!!!!!", average_price)
            ## 실전 테스트 끝


            ### 실제로 시작

            moohanloop = True
            moohanloop_count = 0
            while moohanloop is True:
                moohanloop_count += 1

                now = datetime.datetime.now()
                now_time_HMS = now.strftime("%H%M%S")


                if 90000 < int(now_time_HMS) < 153000:
                    if moohanloop_count == 1:
                        print("주식 매매 중...", moohanloop_count, now_time_HMS)
                        result_kiwoom = self.kiwoom.get_kiwoom_start()
                        print("result_kiwoom, 횟수", result_kiwoom, moohanloop_count)

                        if not len(result_kiwoom[0]):
                            print("비어있따.")
                        else:
                            with open(rich_mystock_path_1, "w", encoding='utf-8-sig') as file:
                                result_kiwoom_data_1 = "총 매입금액 : " + str(result_kiwoom[1]) + "\n\n"
                                file.write(str(result_kiwoom_data_1))
                            with open(rich_mystock_path_2, "w", encoding='utf-8-sig') as file:
                                result_kiwoom_data_2 = "현재 총 수익 : " + str(result_kiwoom[2]) + "\n\n"
                                file.write(str(result_kiwoom_data_2))

                            with open(rich_file_path, "w", encoding='utf-8-sig') as file:
                                json.dump(result_kiwoom[0], file)
                            self.set_rand_int()

                    elif moohanloop_count == 2:
                        print("주식 매매 중...", moohanloop_count, now_time_HMS)
                        result_kiwoom = self.kiwoom.get_kiwoom_start()
                        print("result_kiwoom, 횟수", moohanloop_count, result_kiwoom)
                        if not len(result_kiwoom[0]):
                            print("비어있따.")
                        else:
                            with open(rich_mystock_path_1, "w", encoding='utf-8-sig') as file:
                                result_kiwoom_data_1 = "총 매입금액 : " + str(result_kiwoom[1]) + "\n\n"
                                file.write(str(result_kiwoom_data_1))
                            with open(rich_mystock_path_2, "w", encoding='utf-8-sig') as file:
                                result_kiwoom_data_2 = "현재 총 수익 : " + str(result_kiwoom[2]) + "\n\n"
                                file.write(str(result_kiwoom_data_2))

                            with open(rich_file_path, "w", encoding='utf-8-sig') as file:
                                json.dump(result_kiwoom[0], file)
                            self.set_rand_int()

                    elif (moohanloop_count % 50) == 0:
                        print("주식 매매 중...", moohanloop_count, now_time_HMS)
                        result_kiwoom = self.kiwoom.get_kiwoom_start()
                        print("result_kiwoom, 횟수", result_kiwoom, moohanloop_count)
                        if not len(result_kiwoom[0]):
                            print("비어있따.")
                        else:
                            with open(rich_mystock_path_1, "w", encoding='utf-8-sig') as file:
                                result_kiwoom_data_1 = "총 매입금액 : " + str(result_kiwoom[1]) + "\n\n"
                                file.write(str(result_kiwoom_data_1))
                            with open(rich_mystock_path_2, "w", encoding='utf-8-sig') as file:
                                result_kiwoom_data_2 = "현재 총 수익 : " + str(result_kiwoom[2]) + "\n\n"
                                file.write(str(result_kiwoom_data_2))

                            with open(rich_file_path, "w", encoding='utf-8-sig') as file:
                                json.dump(result_kiwoom[0], file)
                            self.set_rand_int()

                    if moohanloop_count != 1:
                        QTest.qWait(100)
                    else:
                        QTest.qWait(1000)
                    # QTest.qWait(100)


                else:
                    print("아직 시간 안됐다...", now_time_HMS)

                    for t in range(500):
                        now = datetime.datetime.now()
                        now_time_HMS = now.strftime("%H%M%S")

                        if 89000 < int(now_time_HMS) < 153000:
                            break
                        QTest.qWait(500)



                QTest.qWait(100)



#######################################################


        except Exception as e:
            print(e)
            return 0


    def hello2(self):
        print("hello!!!!!!!!!!")

    def mytestin_(self):
        try:

            print("testttttttttttt")

            # self.kiwoom = Kiwoom()
            # self.kiwoom.test_time2()

            # self.onActivated_test(1)
            # time.sleep(3)
            # self.onActivated_test2(1)
            # time.sleep(3)

            x = Test_check(self)
            # self.mytestin.setText("GootEvening")
            # self.mytestin.setDisabled(True)
            x.start()
            #
            # self.test = QApplication(sys.argv)
            #
            #
            # self.test.exec_()

        except Exception as e:
            print(e)
            return 0

    # def keyPressEvent(self, e):
    #     if e.key() == Qt.Key_Escape:
    #         self.close()
    #     elif e.key() == Qt.Key_F:
    #         self.showFullScreen()
    #     elif e.key() == Qt.Key_N:
    #         self.showNormal()


###########BackGround(백그라운드) 관련############################nowtest


class Test_check(QThread):

    # parent = MainWidget을 상속 받음.
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    def run(self):
        # self.parent.hello2()

        # cla = "one"



        print("여긴 테스트 모드(ver " + version + ")")
        # 매수중인 종목

        #

        go_test()





        # money_ = text_check_get(233, 48, 300, 65, cla)
        # # started_ = start_.split("\n")
        # print("money?", money_)
        # if len(money_) != 0:
        #     end_ = int_put_(money_)
        #     print("now_money?", end_)
        #     # for list in end_:
        #     #     try:
        #     #         if list == '레' or list == '벨':
        #     #             dunjeon_0_check = False
        #     #             isdungeon_ing = False
        #     #             print("공허 끝?", end_)
        #     #
        #     #     except:
        #     #         pass






        #
        # print(cv2.__file__)







# 실제 게임 플레이 부분 #################################################################
################################################
################################################


####################################################################################################################
####################################################################################################################
####################################################################################################################
####################################################################################################################
####################################################################################################################
####################################################################################################################
####################################################################################################################
####################################################################################################################
####################################################################################################################
def my_exception_hook(exctype, value, traceback):
    # Print the error and traceback

    print(exctype, value, traceback)
    # Call the normal Exception hook after
    sys.__excepthook__(exctype, value, traceback)
    # sys.exit(1)


# if __name__ == '__main__':
#     try:
#         app = QApplication(sys.argv)
#         ex = MyApp()
#
#         # Back up the reference to the exceptionhook
#         sys._excepthook = sys.excepthook
#
#         # Set the exception hook to our wrapping function
#         sys.excepthook = my_exception_hook
#
#         sys.exit(app.exec_())
#     except Exception as e:
#         print(e)
#         print("프로그램 꺼지기전 정지")
#         os.system("pause")
