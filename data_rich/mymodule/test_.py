import sys
import os
import time
import datetime

import requests
# import http.client
import json
import pandas as pd
from ast import literal_eval

import variable as v_

sys.path.append('C:/my_games/' + str(v_.game_folder) + '/' + str(v_.data_folder) + '/mymodule')



dir_path = "C:\\my_games\\" + str(v_.game_folder)
file_path = dir_path + "\\" + str(v_.data_folder) + "\\mymodule\\condition_stock.txt"
second_order_path = dir_path + "\\" + str(v_.data_folder) + "\\mymodule\\second_order_stock.txt"


def go_test():
    from ast import literal_eval


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

    period = 9
    code = "005930"

    print("calculate_biii")
    # 네이버 금융 API를 통해 데이터 가져오기
    response = requests.get(
        f"https://api.finance.naver.com/siseJson.naver?symbol={code}&requestType=0&count=50&timeframe=day")
    response_data = literal_eval(response.text.strip())

    print("response_data", response_data)

    # 응답 데이터를 DataFrame으로 변환
    price_data = pd.DataFrame(response_data[1:], columns=response_data[0])
    price_data.index = price_data["날짜"]
    price_data = price_data[["시가", "고가", "저가", "종가", "거래량"]]

    close = price_data['종가']
    low = price_data['저가']
    high = price_data['고가']
    volume = price_data['거래량']  # 오타 수정

    # volume 데이터가 없는 경우를 처리
    if volume.empty:
        print("Volume 데이터가 없습니다.")
        return None

    # Bill 값 계산
    value1 = (close - low) ** 2 - (high - close) ** 2
    value2 = high - low
    bill = (value1 / value2) * volume
    bill_sum = bill.rolling(window=period).sum()

    # 결과 출력
    print("result biii:", bill_sum)

    # code = "005930"
    # period = 5
    # smoothing = 3
    #
    # print("calculate_stochastic_fast", code)
    # # 네이버 금융 API를 통해 데이터 가져오기
    # response = requests.get(
    #     f"https://api.finance.naver.com/siseJson.naver?symbol={code}&requestType=0&count=50&timeframe=day")
    # response_data = literal_eval(response.text.strip())
    #
    #
    # # 응답 데이터를 DataFrame으로 변환
    # price_data = pd.DataFrame(response_data[1:], columns=response_data[0])
    # price_data.index = price_data["날짜"]
    # price_data = price_data[["시가", "고가", "저가", "종가", "거래량"]]
    #
    #
    # #
    # # Calculate Fast %K
    # lowest_low = price_data['저가'].rolling(window=period).min()
    # highest_high = price_data['고가'].rolling(window=period).max()
    # fast_k = ((price_data['종가'] - lowest_low) / (highest_high - lowest_low)) * 100
    #
    # # Calculate Fast %D
    # fast_d = fast_k.rolling(window=smoothing).mean()
    #
    # # 결과 출력
    # print("Fast %K:", fast_k.iloc[-1])
    # print("Fast %D:", fast_d.iloc[-1])

    # # Calculate %K
    # lowest_low = price_data['저가'].rolling(window=period).min()
    # print("lowest_low", lowest_low)
    # highest_high = price_data['고가'].rolling(window=period).max()
    # print("highest_high", highest_high)
    # fast_k = ((price_data['종가'] - lowest_low) / (highest_high - lowest_low)) * 100
    # print("fast_k", fast_k)
    #
    # # Calculate %D
    # fast_d = fast_k.rolling(window=smoothing).mean()
    # print("fast_d", fast_d)





    # code = "005930"  # 삼성전자
    # period = 7  # 이동평균 기간
    #
    # conn = http.client.HTTPSConnection("api.finance.naver.com")
    # payload = f"/siseJson.naver?symbol={code}&requestType=0&count=50&timeframe=day"
    # conn.request("GET", payload)
    # res = conn.getresponse()
    # data = res.read().decode('utf-8')
    # response_data = json.loads(data)
    #
    # price_data = pd.DataFrame(response_data[1:], columns=response_data[0])
    # price_data.index = price_data["날짜"]
    # price_data = price_data[["시가", "고가", "저가", "종가", "거래량"]]
    #
    # moving_average = price_data["종가"].rolling(window=period).mean()
    # last_ma_value = moving_average.iloc[-1]
    #
    # pt = str(period) + "일 이동 평균 값 => " + str(last_ma_value)
    #
    # print("이평선 결과 :", pt)


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
def calculate_stochastic_fast(self, code, period=5, smoothing=3):

    import requests
    import pandas as pd
    from ast import literal_eval

    try:
        print("calculate_stochastic_fast", code)
        # 네이버 금융 API를 통해 데이터 가져오기
        response = requests.get(
            f"https://api.finance.naver.com/siseJson.naver?symbol={code}&requestType=0&count=50&timeframe=day")
        response_data = literal_eval(response.text.strip())

        # 응답 데이터를 DataFrame으로 변환
        price_data = pd.DataFrame(response_data[1:], columns=response_data[0])
        price_data.index = price_data["날짜"]
        price_data = price_data[["시가", "고가", "저가", "종가", "거래량"]]

        # Calculate %K
        lowest_low = price_data['저가'].rolling(window=period).min()
        highest_high = price_data['고가'].rolling(window=period).max()
        fast_k = ((price_data['종가'] - lowest_low) / (highest_high - lowest_low)) * 100

        # Calculate %D
        fast_d = fast_k.rolling(window=smoothing).mean()

        # 결과 출력

        print("결과 :", fast_k, fast_d)

        return fast_k, fast_d

    except Exception as e:
        print("에러 발생:", e)