import sys
import os
import time
import datetime

import requests
# import http.client
import json
import pandas as pd

import variable as v_

sys.path.append('C:/my_games/' + str(v_.game_folder) + '/' + str(v_.data_folder) + '/mymodule')



dir_path = "C:\\my_games\\" + str(v_.game_folder)
file_path = dir_path + "\\" + str(v_.data_folder) + "\\mymodule\\condition_stock.txt"
second_order_path = dir_path + "\\" + str(v_.data_folder) + "\\mymodule\\second_order_stock.txt"


def go_test():
    import numpy as np
    import random


    print("test")
    cla = "one"

    plus = 0


    if cla == "one":
        plus = 0
    elif cla == "two":
        plus = 960
    elif cla == "three":
        plus = 960 * 2
    elif cla == "four":
        plus = 960 * 3

    print("hi hello")

    now = datetime.datetime.now()
    now_time = now.strftime("%H%M%S")
    print("내 포트폴리오에 상세 업데이트 시간", now.strftime('%Y-%m-%d %H:%M:%S'), now_time)

    code = "005930"  # 삼성전자
    period = 7  # 이동평균 기간

    conn = http.client.HTTPSConnection("api.finance.naver.com")
    payload = f"/siseJson.naver?symbol={code}&requestType=0&count=50&timeframe=day"
    conn.request("GET", payload)
    res = conn.getresponse()
    data = res.read().decode('utf-8')
    response_data = json.loads(data)

    price_data = pd.DataFrame(response_data[1:], columns=response_data[0])
    price_data.index = price_data["날짜"]
    price_data = price_data[["시가", "고가", "저가", "종가", "거래량"]]

    moving_average = price_data["종가"].rolling(window=period).mean()
    last_ma_value = moving_average.iloc[-1]

    pt = str(period) + "일 이동 평균 값 => " + str(last_ma_value)

    print("이평선 결과 :", pt)


    # if os.path.isfile(second_order_path) == True:
    #
    #     f = open(second_order_path, "r", encoding='utf-8-sig')
    #
    #     lines = f.readlines()
    #
    #     print("주문체결됨 lines : ", lines, len(lines))
    #
    #     f.close()
    #
    #     if len(lines) > 0:
    #
    #         re_line = []
    #
    #
    #         sCode = '003000'
    #
    #         for i in range(len(lines)):
    #             if lines[i] == "":
    #                 print("비어있다.")
    #
    #
    #             if lines[i] != "":
    #                 print("안 비었다.")
    #                 ls = lines[i].split("\t")
    #
    #                 print("sCode", sCode)
    #                 print("ls", ls)
    #
    #                 if sCode != ls[0]:
    #                     stock_code = ls[0]
    #                     print("stock_code", stock_code)
    #                     stock_name = ls[1]
    #                     print("stock_name", stock_name)
    #                     print("stock_price", ls[2])
    #                     stock_price = int(ls[2].split("\n")[0])
    #                     print("int(ls[2].split('\n')[0])", stock_price)
    #                     stock_price = abs(stock_price)
    #                     print("abs(stock_price)", stock_price)
    #
    #                     add_line = str(stock_code) + "\t" + str(stock_name) + "\t" + str(
    #                         stock_price) + "\n"
    #
    #                     print("add_line", add_line)
    #
    #                     re_line.append(str(add_line))
    #
    #                     print("re_line", re_line)
