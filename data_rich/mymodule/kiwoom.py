import time

from PyQt5.QAxContainer import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtTest import *
#
# from pykiwoom.kiwoom import *
#
# kiwoom = Kiwoom()

import datetime
# import FinanceDataReader as fdr


import sys
import os
import variable as v_

sys.path.append('C:/my_games/' + str(v_.game_folder) + '/' + str(v_.data_folder) + '/mymodule')

#
# from main_p import FirstTab

dir_path = "C:\\my_games\\" + str(v_.game_folder)
file_path = dir_path + "\\" + str(v_.data_folder) + "\\mymodule\\condition_stock.txt"
second_order_path = dir_path + "\\" + str(v_.data_folder) + "\\second_order\\second_order_stock.txt"

from errorCode import errors
from kiwoomType import *


class Kiwoom(QAxWidget):
    def __init__(self):
        super().__init__()
        print("키움 메서드", __name__)



        #######################################


    # 최초 초기화 부분
    def get_kiwoom_ready(self):
        self.realType = RealType()

        ####### event loop
        self.login_event_loop = None
        self.detail_account_info_event_loop = QEventLoop()
        self.calculator_event_loop = QEventLoop()

        ######### 스크린번호 모음
        self.screen_hoga_info = "10000"
        self.screen_my_info = "2000"
        self.screen_calculation_stock = "4000"
        self.screen_real_stock = "5000"  # 종목별로 할당할 스크린 번호
        self.screen_meme_stock = "6000"  # 종목별 할당할 주문용 스크린 번호
        self.screen_start_stop_real = "1000"
        self.screen_scan = "9000"
        #######변수모음
        self.account_num = None  # 계좌번호

        ######### 계좌 관련 변수
        self.use_money = 0
        self.use_money_percent = 0.5

        # 총 매입금액 및 총 수익
        self.total_buy_money_result = 0
        self.total_profit_loss_rate_result = 0

        self.buy_money = int(v_.one_mesoo_price)
        self.sell_money = int(v_.two_medo_price)
        print("self.buy_money, self.sell_money", self.buy_money, self.sell_money)

        ###### 변수 모음
        self.portfolio_stock_dict = {}
        self.account_stock_dict = {}
        self.not_account2_stock_dict = {}
        self.jango_dict = {}

        self.return_stock_dict = {}

        ####### 종목 분석용
        self.calcul_data = []
        self.result_minute_aver = {}

        ######### 조건 검색식 전용
        self.scan_list = []
        self.scan_list_result = []
        self.previous_data = {}
        # tr
        self.last_request_time = 0
        self.request_delay = 4
        # 실시간
        self.last_scan_time = 0
        self.scan_delay = 61
        # 세금
        # 매수매도세금
        # 실제 세금
        # self.meme_tax_price = 0.00015
        # 모의투자 세금
        self.meme_tax_price = 0.0035
        self.stock_tax_price = 0.0023

        #######로그인
        self.get_ocx_instance()
        self.event_slots()

        ##### 실시간
        self.real_event_slots()
        # 1은 tr, 2는 실시간
        self.data_type = 1
        self.started = 0

        ##### 매수 매도 중...
        self.buy_ing = []
        self.sell_ing = []

        # 로그인 관련
        self.signal_login_commConnect()

        ######계좌정보 가져오기
        self.get_account_info()
        self.detail_account_info()  # 예수금
        self.detail_account_mystock()  # 통장 내역(수익률 등 볼수 있음)
        self.not_concluded_account()  # 미체결 요청

        ########## 장시작 구분
        self.dynamicCall("SetRealReg(QString, QString, QString, QString)", self.screen_start_stop_real, '',
                         self.realType.REALTYPE['장시작시간']['장운영구분'], "0")

        ##### 조건식 다운
        self.GetConditionLoad()
        QTest.qWait(1000)
        self.GetConditionNameList()
        QTest.qWait(1000)

        # TR 5건 이하 - time.sleep없이 그냥 진행가능
        # TR 100건 이하 - time.sleep(0.2)를 추가하여 진행가능
        # TR 1000건 이하 - time.sleep(1.8)을 추가하여 진행가능
        # TR 1000건 초과 - 1시간 1000건 제약으로 time.sleep(3.6)을 추가하여 진행가능

        # # tr 1, 실시간 2
        # self.stock_start(self.data_type)

        ###############test 테스트$$$$$$$$$$$$$

        # 20일 이동평균선 계산
        # self.calculate_moving_average("035720", 20)

    # 실시간 스타트
    def get_kiwoom_start(self):
        # tr 1, 실시간 2
        if self.data_type == 1:
            self.started += 1
            print("tr 타입")
            ### 1번 Tr


            if self.started != 1:
                # 횟수제한
                self.wait_for_request_delay()
                self.detail_account_mystock()  # 총 매입금액, 총 수익
                self.last_request_time = time.time()

                result = len(self.portfolio_stock_dict)
                print("갱신전 관리 종목 갯수", result)

                self.read_code()  # 저장된 종목들 불러온다.
                self.screen_number_setting()  # 스크린 번호를 할당

                my_port_many = 0
                for code in self.portfolio_stock_dict.keys():
                    my_port_many += 1

                    # 10분봉 240 평균 구하기 결과는 ... result_minute_kiwoom_db 으로 리턴...
                    self.minute_kiwoom_db(code=code, tic=10)

                    self.getItemInfo(code)
                    QTest.qWait(300)

                print("내 종목 관리 갯수 : ", my_port_many)

        else:
            print("타입?", self.data_type)

        # self.jango_dict, self.account_stock_dict

        if len(self.account_stock_dict) > 0:
            # self.account_stock_dict의 모든 키와 값을 self.return_stock_dict에 추가
            for key, value in self.account_stock_dict.items():
                if key not in self.return_stock_dict:
                    self.return_stock_dict[key] = value
        if len(self.jango_dict) > 0:
            # self.jango_dict의 모든 키와 값을 self.return_stock_dict에 추가
            for key, value in self.jango_dict.items():
                if key not in self.return_stock_dict:
                    self.return_stock_dict[key] = value
        # if sCode in self.account_stock_dict.keys()

        return self.return_stock_dict, self.total_buy_money_result, self.total_profit_loss_rate_result

    # 로그인 부분
    def get_ocx_instance(self):
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")

    def event_slots(self):
        self.OnEventConnect.connect(self.login_slot)
        self.OnReceiveTrData.connect(self.trdata_slot)
        self.OnReceiveMsg.connect(self.msg_slot)

    def real_event_slots(self):
        #### 모두 실시간
        self.OnReceiveRealData.connect(self.realdata_slot)
        self.OnReceiveChejanData.connect(self.chejan_slot)  # 주문

        self.OnReceiveConditionVer.connect(self._handler_condition_load)    # 로컬에 사용자 조건식 저장 성공여부 응답 이벤트
        self.OnReceiveRealCondition.connect(self._handler_real_condition)   # 조건검색 실시간 편입, 이탈 종목 이벤트
        self.OnReceiveTrCondition.connect(self._handler_tr_condition)   # 조건검색 조회 응답


    def signal_login_commConnect(self):
        self.dynamicCall("CommConnect()")

        self.login_event_loop = QEventLoop()
        self.login_event_loop.exec_()

    def login_slot(self, errCode):
        print(errors(errCode))

        self.login_event_loop.exit()

    # 계좌번호 가져오기
    def get_account_info(self):
        account_list = self.dynamicCall("GetLogininfo(String)", "ACCNO")

        self.account_num = account_list.split(';')[0]

        print("나의 보유 계좌번호", self.account_num)

    def detail_account_info(self):
        print("예수금을 요청하는 부분")

        self.dynamicCall("SetInputValue(String, String)", "계좌번호", self.account_num)
        self.dynamicCall("SetInputValue(String, String)", "비밀번호", v_.mypw)
        self.dynamicCall("SetInputValue(String, String)", "비밀번호입력매체구분", "00")
        self.dynamicCall("SetInputValue(String, String)", "조회구분", "2")
        self.dynamicCall("CommRqData(String, String, int, String)", "예수금상세현황요청", "opw00001", "0", self.screen_my_info)

        self.detail_account_info_event_loop.exec_()

    def detail_account_mystock(self, sPrevNext="0"):
        print("계좌평가 잔고내역 요청하기 연속 조회 %s" % sPrevNext)

        self.dynamicCall("SetInputValue(String, String)", "계좌번호", self.account_num)
        self.dynamicCall("SetInputValue(String, String)", "비밀번호", v_.mypw)
        self.dynamicCall("SetInputValue(String, String)", "비밀번호입력매체구분", "00")
        self.dynamicCall("SetInputValue(String, String)", "조회구분", "2")
        self.dynamicCall("CommRqData(String, String, int, String)", "계좌평가잔고내역요청", "opw00018", sPrevNext, self.screen_my_info)


        self.detail_account_info_event_loop.exec_()


    def not_concluded_account(self, sPrevNext="0"):
        print("미체결 요청")

        self.dynamicCall("SetInputValue(QString, QString)", "계좌번호", self.account_num)
        self.dynamicCall("SetInputValue(QString, QString)", "체결구분", "1")
        self.dynamicCall("SetInputValue(QString, QString)", "매매구분", "0")
        self.dynamicCall("CommRqData(QString, QString, int, QString)", "실시간미체결요청", "opt10075", sPrevNext, self.screen_my_info)

        self.detail_account_info_event_loop.exec_()

    def cancel_screen_number(self, sScrNo):
        self.dynamicCall("DisconnectRealData(QString)", sScrNo)
        QTest.qWait(100)

    def trdata_slot(self, sScrNo, sRQName, sTrCode, sRecordName, sPrevNext):
        '''
        tr요청을 받는 구역이다! 슬롯이다!
        :param sScrNo: 스크린번호
        :param sRQName: 내가 요청했을 때 지은 이름
        :param sTrCode: 요청 id, tr코드
        :param sRecordName: 사용 안함
        :param sPrevNext: 다음 페이지가 있는지
        :return:
        '''

        if sRQName == "예수금상세현황요청":
            deposit = self.dynamicCall("GetCommData(String, String, int, String)", sTrCode, sRQName, 0, "예수금")
            print("예수금", int(deposit))

            self.use_money = int(deposit) * self.use_money_percent
            self.use_money = self.use_money / 4

            ok_deposit = self.dynamicCall("GetCommData(String, String, int, String)", sTrCode, sRQName, 0, "출금가능금액")
            print("출금가능금액", int(ok_deposit))

            self.detail_account_info_event_loop.exit()


        elif sRQName == "계좌평가잔고내역요청":
            total_buy_money = self.dynamicCall("GetCommData(String, String, int, String)", sTrCode, sRQName, 0, "총매입금액")
            self.total_buy_money_result = int(total_buy_money)


            print("총매입금액", self.total_buy_money_result)

            total_profit_loss_rate = self.dynamicCall("GetCommData(String, String, int, String)", sTrCode, sRQName, 0, "총수익률(%)")
            self.total_profit_loss_rate_result = float(total_profit_loss_rate)
            print("총수익률(%)", self.total_profit_loss_rate_result)

            rows = self.dynamicCall("GetRepeatCnt(QString, QString)", sTrCode, sRQName)


            cnt = 0
            for i in range(rows):
                code = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "종목번호")   # 종목번호 => 종목코드로 수정함
                code = code.strip()[1:]

                code_nm = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "종목명")
                stock_quantity = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "보유수량")
                buy_price = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "매입가")
                learn_rate = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "수익률(%)")
                current_price = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "현재가")
                tatal_chegual_price = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "매입금액")
                possible_quantity = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "매매가능수량")


                if code in self.account_stock_dict:
                    pass
                else:
                    self.account_stock_dict.update({code:{}})


                code_nm = code_nm.strip()
                stock_quantity = int(stock_quantity.strip())
                buy_price = int(buy_price.strip())
                learn_rate = float(learn_rate.strip())
                current_price = int(current_price.strip())
                tatal_chegual_price = int(tatal_chegual_price.strip())
                possible_quantity = int(possible_quantity.strip())

                self.account_stock_dict[code].update({"종목명": code_nm})
                self.account_stock_dict[code].update({"보유수량": stock_quantity})
                self.account_stock_dict[code].update({"매입가": buy_price})
                self.account_stock_dict[code].update({"수익률(%)": learn_rate})
                self.account_stock_dict[code].update({"현재가": current_price})
                self.account_stock_dict[code].update({"매입금액": tatal_chegual_price})
                self.account_stock_dict[code].update({"매매가능수량": possible_quantity})

                # print("계좌에 가지고 있는 종목 추가!!!!!!!!!!!", self.account_stock_dict)

                cnt += 1

            print("계좌에 가지고 있는 종목 %s" % self.account_stock_dict)
            print("계좌에 보유종목 카운트 %s" % cnt)

            if sPrevNext == "2":
                self.detail_account_mystock(sPrevNext="2")
            else:
                self.cancel_screen_number(sScrNo)
                self.detail_account_info_event_loop.exit()


        elif sRQName == "실시간미체결요청":

            rows = self.dynamicCall("GetRepeatCnt(QString, QString)", sTrCode, sRQName)


            for i in range(rows):
                print("실시간미체결요청", i)


                code = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "종목코드")
                code = code.strip()


                code_nm = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "종목명")
                code_nm = code_nm.strip()

                order_no = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "주문번호")
                order_no = order_no.strip()

                order_status = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "주문상태") # 접수, 확인, 체결
                order_status = order_status.strip()

                order_quantity = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "주문수량")
                order_quantity = int(order_quantity.strip())

                order_price = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "주문가격")
                order_price = int(order_price.strip())

                order_gubun = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "주문구분")  # -매도, +매수,
                order_gubun = order_gubun.strip().lstrip('+').lstrip('-')

                not_quantity = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "미체결수량")
                not_quantity = int(not_quantity.strip())

                ok_quantity = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "체결량")
                ok_quantity = int(ok_quantity.strip())

                print("실시간미체결요청 종목번호?x종목코드?", code, code_nm)








                if order_no in self.not_account2_stock_dict:
                    pass
                else:
                    self.not_account2_stock_dict[order_no] = {}

                self.not_account2_stock_dict[order_no].update({"종목코드": code})
                self.not_account2_stock_dict[order_no].update({"종목명": code_nm})
                self.not_account2_stock_dict[order_no].update({"주문번호": order_no})
                self.not_account2_stock_dict[order_no].update({"주문상태": order_status})
                self.not_account2_stock_dict[order_no].update({"주문수량": order_quantity})
                self.not_account2_stock_dict[order_no].update({"주문가격": order_price})
                self.not_account2_stock_dict[order_no].update({"주문구분": order_gubun})
                self.not_account2_stock_dict[order_no].update({"미체결수량": not_quantity})
                self.not_account2_stock_dict[order_no].update({"체결량": ok_quantity})

                print("미체결 종목 : %s " % self.not_account2_stock_dict[order_no])

            if sPrevNext == "2":
                self.not_concluded_account(2)
            else:
                # self.cancel_screen_number(sScrNo)
                self.detail_account_info_event_loop.exit()




        if sTrCode == "opt10001":
            if sRQName == "주식기본정보요청":

                # 주식체결 Tr

                # 횟수 제한 딜레이

                code = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "종목코드")
                code = code.strip()

                code_nm = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "종목명")
                code_nm = code_nm.strip()
                currentPrice = abs(int(self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "현재가")))
                print("주식기본정보요청", code, code_nm, currentPrice)

                ###########################지대로
                sCode = code

                # a = self.dynamicCall("GetCommRealData(QString, int)", sCode, self.realType.REALTYPE['주식체결']['체결시간'])  # HHMMSS
                b = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "현재가")   # +-0000
                b = abs(int(b))
                c = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "전일대비")  # +-0000
                c = abs(int(c))

                d = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "등락율")  # +-0000
                d = float(d)

                # e = self.dynamicCall("GetCommRealData(QString, int)", sCode, self.realType.REALTYPE['주식체결']['(최우선)매도호가'])  # +-0000
                # e = abs(int(e))

                # f = self.dynamicCall("GetCommRealData(QString, int)", sCode, self.realType.REALTYPE['주식체결']['(최우선)매수호가'])  # +-0000
                # f = abs(int(f))

                g = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "거래량")  # +-0000
                g = abs(int(g))

                # h = self.dynamicCall("GetCommRealData(QString, int)", sCode, self.realType.REALTYPE['주식체결']['누적거래량'])  # +-0000
                # h = abs(int(h))

                i = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "고가")  # +-0000
                i = abs(int(i))

                j = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "시가")  # +-0000
                j = abs(int(j))

                k = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "저가")  # +-0000
                k = abs(int(k))

                if sCode not in self.portfolio_stock_dict:
                    self.portfolio_stock_dict.update({sCode:{}})

                # self.portfolio_stock_dict[sCode].update({"체결시간": a})
                self.portfolio_stock_dict[sCode].update({"현재가": b})
                self.portfolio_stock_dict[sCode].update({"전일대비": c})
                self.portfolio_stock_dict[sCode].update({"등락율": d})
                # self.portfolio_stock_dict[sCode].update({"(최우선)매도호가": e})
                # self.portfolio_stock_dict[sCode].update({"(최우선)매수호가": f})
                self.portfolio_stock_dict[sCode].update({"거래량": g})
                # self.portfolio_stock_dict[sCode].update({"누적거래량": h})
                self.portfolio_stock_dict[sCode].update({"고가": i})
                self.portfolio_stock_dict[sCode].update({"시가": j})
                self.portfolio_stock_dict[sCode].update({"저가": k})

                print("내 포트폴리오에 상세 업데이트", sCode, self.portfolio_stock_dict[sCode])

                now = datetime.datetime.now()
                print("내 포트폴리오에 상세 업데이트 시간", now.strftime('%Y-%m-%d %H:%M:%S'))

                if g > 0:

                    # 계좌잔고평가내역에 있고 오늘 산 잔고에는 없을 경우
                    if sCode in self.account_stock_dict.keys() and sCode not in self.jango_dict.keys():
                        print("1")
                        # print("%s %s" % ("신규매도를 한다_1", sCode))
                        # 1: 신규매수, 2:신규매도, 3:매수취소, 4:매도취소, 5:매수정정, 6:매도정정

                        asd = self.account_stock_dict[sCode]

                        if int(asd['매매가능수량']) > 1:
                            first_meme_price = int(asd['매매가능수량']) / 2
                        else:
                            first_meme_price = asd['매매가능수량']

                        medo = b * asd['매매가능수량']
                        mesoo = asd['매입가'] * asd['매매가능수량']

                        meme_tax = (mesoo * self.meme_tax_price) + (medo * self.meme_tax_price) + (medo * self.stock_tax_price)



                        meme_rate = (medo - mesoo - meme_tax) / mesoo * 100
                        # meme_rate = (b / asd['매입가']) * 100 - 100


                        print("매도 매수 세금 수익률", medo, mesoo, meme_tax, meme_rate)

                        # 2차 매도인지 여부
                        second_meme = False
                        # result_sell_quantity = self.buy_money / 2
                        result_sell_quantity = self.sell_money
                        result_all_sell_quantity = int(asd['매매가능수량']) * int(asd['매입가'])
                        if result_all_sell_quantity > result_sell_quantity:
                            second_meme = True

                        code_nm = self.dynamicCall("GetMasterCodeName(QString)", sCode)

                        print("종목명, 수익률, 매매수량", code_nm, meme_rate, int(first_meme_price), asd['매입가'], b)

                        #################
                        if asd['매매가능수량'] > 0:

                            five_percent = True

                            if os.path.isfile(second_order_path) == True:
                                file = open(second_order_path, "r", encoding='utf-8-sig')

                                lines = file.readlines()

                                if len(lines) > 0:

                                    for i in range(len(lines)):
                                        if lines[i] != "":
                                            ls = lines[i].split("\t")

                                            if sCode == ls[0]:
                                                five_percent = False
                                                break
                            else:
                                file = open(second_order_path, "w", encoding='utf-8-sig')
                                file.write("")
                                file.close()

                            if five_percent == True and second_meme == True:

                                if (meme_rate > 5 or meme_rate < -5) and sCode not in self.sell_ing:

                                    wa = []
                                    wa.append(sCode)

                                    if len(wa) > 1:
                                        wa.clear()
                                        pass
                                    else:
                                        print("%s %s" % ("처음 신규매도를 한다_1_1", sCode))

                                        # 횟수 제한 딜레이
                                        self.wait_for_request_delay()
                                        # self.last_request_time = time.time()

                                        order_success = self.dynamicCall("SendOrder(QString, QString, QString, int, QString, int, int, QString, QString)", ["신규매도", self.portfolio_stock_dict[sCode]['주문용스크린번호'], self.account_num, 2, sCode, int(first_meme_price), 0, self.realType.SENDTYPE['거래구분']['시장가'], ""])

                                        self.last_request_time = time.time()

                                        if order_success == 0:
                                            print("매도주문 전달 성공", meme_rate)
                                            if sCode not in self.sell_ing:
                                                self.sell_ing.append(sCode)

                                            if sCode in self.account_stock_dict.keys() and asd['매매가능수량'] == 1:
                                                del self.account_stock_dict[sCode]

                                        else:
                                            print("매도주문 전달 실패")
                            else:
                                result_me = self.calculate_moving_average(sCode, 7)

                                print("int(result_me)", int(result_me))
                                print("계좌잔고평가내역에 있고 오늘 산 잔고에는 없을 경우 : 현재 가격(b)...", b)

                                if int(result_me) > int(b):  # 7일선 and 전량매도

                                    wa = []
                                    wa.append(sCode)

                                    if len(wa) > 1:
                                        wa.clear()
                                        pass
                                    else:
                                        print("%s %s" % ("7% 마지막 신규매도를 한다_1_2", sCode))

                                        # 횟수 제한 딜레이
                                        self.wait_for_request_delay()
                                        # self.last_request_time = time.time()

                                        order_success = self.dynamicCall("SendOrder(QString, QString, QString, int, QString, int, int, QString, QString)", ["신규매도", self.portfolio_stock_dict[sCode]['주문용스크린번호'], self.account_num, 2, sCode, asd['매매가능수량'], 0, self.realType.SENDTYPE['거래구분']['시장가'], ""])

                                        self.last_request_time = time.time()

                                        if order_success == 0:
                                            print("매도주문 전달 성공", meme_rate)

                                            if sCode not in self.sell_ing:
                                                self.sell_ing.append(sCode)

                                            if sCode in self.account_stock_dict.keys():
                                                del self.account_stock_dict[sCode]

                                        else:
                                            print("매도주문 전달 실패")
                                else:
                                    average_price = self.result_minute_kiwoom_db()
                                    print("10분봉 240 이평선에 팔기 240가격:", average_price)
                                    print("10분봉 240 이평선에 팔기 현재가격:", b)
                                    if sCode in average_price.keys() and int(average_price[sCode]["d_day_0_240"]) > int(b) or int(average_price[sCode]["d_day_0_37"]) > int(b) and int(average_price[sCode]["sto_fast"]) < 20:    # sto_fast

                                        wa = []
                                        wa.append(sCode)

                                        if len(wa) > 1:
                                            wa.clear()
                                            pass
                                        else:
                                            print("%s %s" % ("10분봉 240 마지막 신규매도를 한다_1_2", sCode))

                                            # 횟수 제한 딜레이
                                            self.wait_for_request_delay()

                                            order_success = self.dynamicCall(
                                                "SendOrder(QString, QString, QString, int, QString, int, int, QString, QString)",
                                                ["신규매도", self.portfolio_stock_dict[sCode]['주문용스크린번호'], self.account_num, 2,
                                                 sCode, asd['매매가능수량'], 0, self.realType.SENDTYPE['거래구분']['시장가'], ""])

                                            self.last_request_time = time.time()

                                            if order_success == 0:
                                                print("매도주문 전달 성공", meme_rate)

                                                if sCode not in self.sell_ing:
                                                    self.sell_ing.append(sCode)

                                                if sCode in self.account_stock_dict.keys():
                                                    del self.account_stock_dict[sCode]

                                            else:
                                                print("매도주문 전달 실패")


                        QTest.qWait(1000)


                        ##################
                    # 오늘 산 잔고에 있을 경우
                    elif sCode in self.jango_dict.keys():
                        print("2")

                        jd = self.jango_dict[sCode]

                        if int(jd['주문가능수량']) > 1:
                            first_meme_price = int(jd['주문가능수량']) / 2
                        else:
                            first_meme_price = jd['주문가능수량']

                        medo = b * jd['주문가능수량']
                        mesoo = jd['매입단가'] * jd['주문가능수량']

                        meme_tax = (mesoo * self.meme_tax_price) + (medo * self.meme_tax_price) + (medo * self.stock_tax_price)

                        meme_rate = (medo - mesoo - meme_tax) / mesoo * 100
                        # meme_rate = (b / jd['매입단가']) * 100 - 100

                        print("매도 매수 세금 수익률", medo, mesoo, meme_tax, meme_rate)

                        code_nm = self.dynamicCall("GetMasterCodeName(QString)", sCode)

                        # 2차 매도인지 여부
                        second_meme = False
                        result_sell_quantity = self.sell_money
                        result_all_sell_quantity = int(jd['주문가능수량']) * int(jd['매입단가'])
                        if result_all_sell_quantity > result_sell_quantity:
                            second_meme = True

                        print("종목명, 수익률, 매매수량", code_nm, meme_rate, int(first_meme_price), jd['매입단가'], b)

                        if jd['주문가능수량'] > 0:

                            five_percent = True

                            if os.path.isfile(second_order_path) == True:
                                file = open(second_order_path, "r", encoding='utf-8-sig')

                                lines = file.readlines()

                                if len(lines) > 0:

                                    for i in range(len(lines)):
                                        if lines[i] != "":
                                            ls = lines[i].split("\t")

                                            if sCode == ls[0]:
                                                five_percent = False
                                                break
                            else:
                                file = open(second_order_path, "w", encoding='utf-8-sig')
                                file.write("")
                                file.close()

                            if five_percent == True and second_meme == True:
                                if (meme_rate > 5 or meme_rate < -5) and sCode not in self.sell_ing:

                                    wa = []
                                    wa.append(sCode)

                                    if len(wa) > 1:
                                        wa.clear()
                                        pass
                                    else:
                                        print("%s %s" % ("처음 신규매도를 한다_2_1", sCode))

                                        # 횟수 제한 딜레이
                                        self.wait_for_request_delay()


                                        order_success = self.dynamicCall("SendOrder(QString, QString, QString, int, QString, int, int, QString, QString)", ["신규매도", self.portfolio_stock_dict[sCode]['주문용스크린번호'], self.account_num, 2, sCode, int(first_meme_price), 0, self.realType.SENDTYPE['거래구분']['시장가'], ""])

                                        self.last_request_time = time.time()

                                        if order_success == 0:
                                            print("매도주문 전달 성공", meme_rate)
                                            if sCode not in self.sell_ing:
                                                self.sell_ing.append(sCode)

                                            if sCode in self.account_stock_dict.keys() and jd['주문가능수량'] == 1:
                                                del self.account_stock_dict[sCode]

                                        else:
                                            print("매도주문 전달 실패")
                            else:
                                result_me = self.calculate_moving_average(sCode, 7)

                                print("int(result_me)", int(result_me))
                                print("오늘 산 잔고에 있을 경우 : 현재가격(b)...", b)

                                if int(result_me) > int(b): # 7일선 and 전량매도

                                    wa = []
                                    wa.append(sCode)

                                    if len(wa) > 1:
                                        wa.clear()
                                        pass
                                    else:
                                        print("%s %s" % ("7% 마지막 신규매도를 한다_2_2", sCode))

                                        # 횟수 제한 딜레이
                                        self.wait_for_request_delay()

                                        order_success = self.dynamicCall(
                                            "SendOrder(QString, QString, QString, int, QString, int, int, QString, QString)",
                                            ["신규매도", self.portfolio_stock_dict[sCode]['주문용스크린번호'], self.account_num, 2, sCode,
                                             jd['주문가능수량'], 0, self.realType.SENDTYPE['거래구분']['시장가'], ""])

                                        self.last_request_time = time.time()

                                        if order_success == 0:
                                            print("매도주문 전달 성공", meme_rate)
                                            if sCode not in self.sell_ing:
                                                self.sell_ing.append(sCode)


                                            if sCode in self.account_stock_dict.keys():
                                                del self.account_stock_dict[sCode]

                                        else:
                                            print("매도주문 전달 실패")
                                else:
                                    average_price = self.result_minute_kiwoom_db()
                                    print("10분봉 240 이평선에 팔기 240가격:", average_price)
                                    print("10분봉 240 이평선에 팔기 현재가격:", b)
                                    if sCode in average_price.keys() and int(average_price[sCode]["d_day_0_240"]) > int(b) or int(average_price[sCode]["d_day_0_37"]) > int(b) and int(average_price[sCode]["sto_fast"]) < 20:
                                        wa = []
                                        wa.append(sCode)

                                        if len(wa) > 1:
                                            wa.clear()
                                            pass
                                        else:
                                            print("%s %s" % ("10분봉 240 마지막 신규매도를 한다_2_2", sCode))

                                            # 횟수 제한 딜레이
                                            self.wait_for_request_delay()

                                            order_success = self.dynamicCall(
                                                "SendOrder(QString, QString, QString, int, QString, int, int, QString, QString)",
                                                ["신규매도", self.portfolio_stock_dict[sCode]['주문용스크린번호'], self.account_num, 2,
                                                 sCode,
                                                 jd['주문가능수량'], 0, self.realType.SENDTYPE['거래구분']['시장가'], ""])

                                            self.last_request_time = time.time()

                                            if order_success == 0:
                                                print("매도주문 전달 성공", meme_rate)
                                                if sCode not in self.sell_ing:
                                                    self.sell_ing.append(sCode)

                                                if sCode in self.account_stock_dict.keys():
                                                    del self.account_stock_dict[sCode]

                                            else:
                                                print("매도주문 전달 실패")

                        QTest.qWait(1000)

                    # 등락율이 1.0 % 이상이고 오늘 산 잔고에 없을 경우

                    # if sCode not in self.jango_dict.keys():

                    elif -1 < d < 5:

                        if sCode not in self.jango_dict:

                            print("3")

                            wa = []
                            wa.append(sCode)

                            if len(wa) > 1:
                                wa.clear()
                                pass
                            else:
                                print("3 : self.use_money", self.use_money)
                                # result = (self.use_money * 0.1) / b
                                result = self.buy_money / b

                                if result >= 1:

                                    quantity = int(result)
                                    # e => 현재가

                                    print("3 : quantity", quantity)

                                    if quantity > 0:

                                        print("3 : order_number", self.not_account2_stock_dict)

                                        already_stock = False

                                        if len(self.not_account2_stock_dict) != 0:

                                            for order_number in self.not_account2_stock_dict.keys():
                                                code = self.not_account2_stock_dict[order_number]['종목코드']
                                                if code == sCode:
                                                    already_stock = True
                                                    break

                                        print("3 : code : already_stock ?", already_stock, sCode)

                                        if already_stock == False:
                                            if sCode not in self.buy_ing:

                                                # 횟수 제한 딜레이


                                                code_nm = self.dynamicCall("GetMasterCodeName(QString)", sCode)

                                                print("%s %s %s" % ("신규매수를 한다_1_1", sCode, code_nm))


                                                print("quantityquantityquantity", quantity)

                                                self.wait_for_request_delay()
                                                order_success = self.dynamicCall("SendOrder(QString, QString, QString, int, QString, int, int, QString, QString)", ["시장가매수", self.portfolio_stock_dict[sCode]['주문용스크린번호'], self.account_num, 1, sCode, quantity, 0, self.realType.SENDTYPE['거래구분']['시장가'], ""])

                                                self.last_request_time = time.time()

                                                if order_success == 0:
                                                    print("매수주문 전달 성공", order_success)
                                                    self.buy_ing.append(sCode)
                                                else:
                                                    print("매수주문 전달 실패", order_success)

                                            else:

                                                # 횟수 제한 딜레이

                                                code_nm = self.dynamicCall("GetMasterCodeName(QString)", sCode)

                                                already_stock = False

                                                if len(self.not_account2_stock_dict) != 0:

                                                    for order_number in self.not_account2_stock_dict.keys():
                                                        code = self.not_account2_stock_dict[order_number]['종목코드']
                                                        if sCode in code:
                                                            already_stock = True
                                                            break
                                                if already_stock == False:

                                                    print("매수취소 대기에 없다.", sCode, code_nm, self.buy_ing)

                                                    # if sCode in self.buy_ing:
                                                    #     self.buy_ing.remove(sCode)

                                                elif already_stock == True:

                                                    print("이미 종목 매수 중이다.", sCode, code_nm, code, self.buy_ing)

                                                    if sCode not in self.buy_ing:
                                                        self.buy_ing.append(sCode)

                                        else:
                                            print("code 검색...이미 종목 있다!!!!!!!!!")
                        QTest.qWait(1000)
                    # else:
                    # ########################### 매수 중복중인거 해결부터 하기

                    if len(self.not_account2_stock_dict) > 0:

                        print("4")

                        not_meme_list = list(self.not_account2_stock_dict)

                        for order_num in not_meme_list:
                            code = self.not_account2_stock_dict[order_num]["종목코드"]
                            meme_price = self.not_account2_stock_dict[order_num]["주문가격"]
                            not_quantity = self.not_account2_stock_dict[order_num]["미체결수량"]
                            order_gubun = self.not_account2_stock_dict[order_num]["주문구분"]

                            if order_gubun == "매수" and not_quantity > 0 and b > meme_price:
                                wa = []
                                wa.append(code)

                                if len(wa) > 1:
                                    wa.clear()
                                    pass
                                else:
                                    print("%s %s" % ("매수취소 한다", code))

                                    # 횟수 제한 딜레이
                                    self.wait_for_request_delay()


                                    order_success = self.dynamicCall(
                                        "SendOrder(QString, QString, QString, int, QString, int, int, QString, QString)",
                                        ["매수취소", self.portfolio_stock_dict[code]['주문용스크린번호'], self.account_num, 3, code, 0, 0,
                                         self.realType.SENDTYPE['거래구분']['지정가'], order_num])

                                    self.last_request_time = time.time()

                                    if order_success == 0:
                                        if code in self.buy_ing:
                                            self.buy_ing.remove(code)
                                        print("매수취소 주문 전달 성공")
                                    else:
                                        print("매수취소 주문 전달 실패")
                            elif not_quantity == 0:
                                del self.not_account2_stock_dict[order_num]
                                if code in self.buy_ing:
                                    self.buy_ing.remove(code)
                                if code in self.sell_ing:
                                    self.sell_ing.remove(code)

                            elif order_gubun == "매도" and not_quantity > 0 and b < meme_price:

                                wa = []
                                wa.append(code)

                                if len(wa) > 1:
                                    wa.clear()
                                    pass
                                else:
                                    print("%s %s" % ("매도취소 한다", code))
                                    # 횟수 제한 딜레이
                                    self.wait_for_request_delay()

                                    order_success = self.dynamicCall("SendOrder(QString, QString, QString ,int, QString, int, int, QString, QString)", ["매도취소", self.portfolio_stock_dict[code]['주문용스크린번호'], self.account_num, 4, code, 0, 0, self.realType.SENDTYPE['거래구분']['지정가'], order_num])  # order_num 은 어떤 주문을 취소할 것인가.

                                    self.last_request_time = time.time()

                                    if order_success == 0:
                                        if code in self.sell_ing:
                                            self.sell_ing.remove(code)

                                        print("%s 매도취소 전달 성공" % code)  # 체결잔고에서  del을 했기 때문에 여기서 하지 않는다.

                                    else:
                                        print("%s 매도취소 전달 실패" % code)

                    ## 마지막 잠시 없애기

                    # for key, value in self.portfolio_stock_dict.copy().items():
                    #
                    #     if key == sCode:
                    #         print("실시간 제거 완료", sCode, self.portfolio_stock_dict[sCode]['스크린번호'])
                    #         self.dynamicCall("SetRealRemove(String, String)", self.portfolio_stock_dict[sCode]['스크린번호'], sCode)
                    #         self.cancel_screen_number(self.portfolio_stock_dict[sCode]['스크린번호'])
                    #         QTest.qWait(100)
                    #         break

                    ###################################
                else:
                    print("거래량 없다!!!")
                self.detail_account_info_event_loop.exit()
        #### 주식분봉차트조회
        if "주식분봉차트조회" == sRQName:
            print("분봉데이터 요청 ")
            code = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "종목코드")
            code = code.strip()
            print("%s 분봉데이터 요청" % code)

            cnt = self.dynamicCall("GetRepeatCnt(QString, QString)", sTrCode, sRQName)
            print("데이터 분봉수 %s" % cnt)

            # 한번 조회하면 600일치까지 일봉데이터를 받을 수 있다.
            for i in range(cnt):
                data = []

                current_price = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "현재가")
                value = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "거래량")
                start_price = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "시가")
                high_price = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "고가")
                low_price = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "저가")

                data.append("")
                data.append(current_price.strip().lstrip('+').lstrip('-'))  #.lstrip('+').lstrip('-')
                data.append(value.strip())
                data.append(start_price.strip().lstrip('+').lstrip('-'))
                data.append(high_price.strip().lstrip('+').lstrip('-'))
                data.append(low_price.strip().lstrip('+').lstrip('-'))
                data.append("")

                self.calcul_data.append(data.copy())

            if sPrevNext == "2" and cnt < 242:
                self.minute_kiwoom_db(code=code, sPrevNext=sPrevNext)
            else:

                print("총 분봉수 %s" % len(self.calcul_data))

                self.result_minute_aver = {}

                pass_success = False

                # 240일 이평선을 그릴 만큼의 데이터가 있는지 체크
                if self.calcul_data == None or len(self.calcul_data) < 240:
                    pass_success = False
                else:
                    # 240개 이상 되면은...
                    pass_success = True


                    if code in self.result_minute_aver:
                        pass
                    else:
                        # self.result_minute_aver({code: {}})
                        self.result_minute_aver[code] = {}
                        print("self.result_minute_aver", self.result_minute_aver)


                    # 먼저 10분봉 스토캐스틱 패스트 값 구하기

                    # Calculate Fast %K

                    print("현재가", self.calcul_data[0][1])
                    sto_now = int(self.calcul_data[0][1])

                    low_prices = []
                    high_prices = []

                    # 셋중 가장 큰수
                    for i in range(5):
                        high_prices.append(self.calcul_data[i][4])
                    # 셋중 가장 작은수
                    for i in range(5):
                        low_prices.append(self.calcul_data[i][5])

                    # max, min
                    sto_high = int(max(high_prices))
                    sto_low = int(min(low_prices))

                    fast_k = (sto_now - sto_low) / (sto_high - sto_low) * 100







                    ####아래는 10분봉 240평균값 구하기
                    print("self.calcul_data", self.calcul_data)

                    # 현재 240 이평
                    total_price = 0
                    for value in self.calcul_data[:240]:
                        total_price += int(value[1])
                    moving_average_price = total_price / 240
                    print("moving_average_price1", moving_average_price)
                    self.result_minute_aver[code].update({"d_day_0_240": moving_average_price})

                    # 현재 37 이평
                    total_price = 0
                    for value in self.calcul_data[:37]:
                        total_price += int(value[1])
                    moving_average_price = total_price / 37
                    print("moving_average_price_37", moving_average_price)
                    self.result_minute_aver[code].update({"d_day_0_37": moving_average_price})
                    # #
                    # total_price = 0
                    # for value in self.calcul_data[1:241]:
                    #
                    #     total_price += int(value[1])
                    #
                    # moving_average_price = total_price / 240
                    # self.result_minute_aver[code].update({"d_day_1_240": moving_average_price})
                    # print("moving_average_price2", moving_average_price)
                    #
                    # total_price = 0
                    # for value in self.calcul_data[2:242]:
                    #     total_price += int(value[1])
                    #
                    # moving_average_price = total_price / 240
                    # self.result_minute_aver[code].update({"d_day_2_240": moving_average_price})
                    # print("moving_average_price3", moving_average_price)

                    # 스토캐스틱 fast 값 넣기
                    self.result_minute_aver[code].update({"sto_fast": fast_k})
                    print("sto_fast", fast_k)



                if pass_success == True:
                    print("조건부 통과됨")

                elif pass_success == False:
                    print("조건부 통과 못함")

                # 10분봉
                self.last_request_time = time.time()

                self.calcul_data.clear()
                self.calculator_event_loop.exit()

        ######## 여긴 필요 없음....


        if "주식일봉차트조회" == sRQName:
            print("일봉데이터 요청 ")
            code = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "종목코드")
            code = code.strip()
            print("%s 일봉데이터 요청" % code)

            cnt = self.dynamicCall("GetRepeatCnt(QString, QString)", sTrCode, sRQName)
            print("데이터 일수 %s" % cnt)

            # 한번 조회하면 600일치까지 일봉데이터를 받을 수 있다.
            for i in range(cnt):
                data = []

                current_price = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "현재가")
                value = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "거래량")
                trading_value = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "거래대금")
                date = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "일자")
                start_price = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "시가")
                high_price = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "고가")
                low_price = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "저가")

                data.append("")
                data.append(current_price.strip())
                data.append(value.strip())
                data.append(trading_value.strip())
                data.append(date.strip())
                data.append(start_price.strip())
                data.append(high_price.strip())
                data.append(low_price.strip())
                data.append("")

                self.calcul_data.append(data.copy())


            if sPrevNext == "2":
                self.day_kiwoom_db(code=code, sPrevNext=sPrevNext)
            else:

                print("총 일수 %s" % len(self.calcul_data))

                pass_success = False

                # 120일 이평선을 그릴 만큼의 데이터가 있는지 체크
                if self.calcul_data == None or len(self.calcul_data) < 120:
                    pass_success = False
                else:
                    # 120일 이상 되면은...

                    total_price = 0
                    for value in self.calcul_data[:120]:
                        total_price += int(value[1])

                    moving_average_price = total_price / 120

                    # 오늘자 주가가 120일 이평선에 걸쳐있는지 확인
                    bottom_stock_price = False
                    check_price = None
                    if int(self.calcul_data[0][7]) <= moving_average_price and moving_average_price <= int(self.calcul_data[0][6]):
                        print("오늘 주가 120 이평선에 걸쳐 있는 것 확인")
                        bottom_stock_price = True
                        check_price = int(self.calcul_data[0][6])

                    # 과거 일봉들이 120일 이평선보다 밑에 있는지 확인,
                    # 그렇게 확인을 하다가 일봉이 120일 이평선보다 위에 있으면 계산 진행

                    prev_price = None   # 과거의 일봉 저가
                    if bottom_stock_price == True:

                        moving_average_price_prev = 0
                        price_top_moving = False

                        idx = 1
                        while True:

                            if len(self.calcul_data[idx:]) < 120:   # 120일치가 있는지 계속 확인
                                print("120일치가 없음!")
                                break

                            total_price = 0
                            for value in self.calcul_data[idx:120+idx]:
                                total_price += int(value[1])
                                moving_average_price_prev = total_price / 120

                            if moving_average_price_prev <= int(self.calcul_data[idx][6]) and idx <= 20:
                                print("20일 동안 주가가 120일 이평선과 같거나 위에 있으면 조건 통과 못함")
                                price_top_moving = False
                                break
                            elif int(self.calcul_data[idx][7]) > moving_average_price_prev and idx > 20:
                                print("120일 이평선 위에 있는 일봉 확인됨")
                                price_top_moving = True
                                prev_price = int(self.calcul_data[idx][7])
                                break
                            idx += 1

                        # 해당 부분 이평선이 가장 최근 일자의 이평선 가격보다 낮은지 확인
                        if price_top_moving == True:
                            if moving_average_price > moving_average_price_prev and check_price > prev_price:
                                print("포착된 이평선의 가격이 오늘자(최근일자) 이평선 가격보다 낮은 것 확인됨")
                                print("포착된 부분의 일봉 저가가 오늘자 일봉의 고가보다 낮은지 확인됨")
                                pass_success = True

                if pass_success == True:
                    print("조건부 통과됨")

                    # 횟수 제한 딜레이
                    code_nm = self.dynamicCall("GetMasterCodeName(QString)", code)

                    file= open(file_path, "a", encoding="utf8")
                    file.write("%s\t%s\t%s\n" % (code, code_nm, str(self.calcul_data[0][1])))
                    file.close()

                elif pass_success == False:
                    print("조건부 통과 못함")

                self.calcul_data.clear()
                self.calculator_event_loop.exit()





    def get_code_list_by_market(self, market_code):
        '''
        종목 코드들 반환
        :param market_code:
        :return:
        '''

        code_list = self.dynamicCall("GetCodeListByMarket(QStrin)", market_code)
        code_list = code_list.split(";")[:-1]

        return code_list


    ############종목 분석###########
    def calculator_fnc(self):
        '''
        종목 분석 실행용 함수(임시)
        :return:
        '''

        code_list = self.get_code_list_by_market("10")
        print("코스닥 갯수 %s" % len(code_list))

        for idx, code in enumerate(code_list):

            self.dynamicCall("DisconnectRealData(QString)", self.screen_calculation_stock)

            print("%s / %s : KOSDAQ Stock Code : %s is updating... " % (idx+1, len(code_list), code))

            self.day_kiwoom_db(code=code)

    def day_kiwoom_db(self, code=None, date=None, sPrevNext="0"):
        # 일봉 조회

        QTest.qWait((3600))

        self.dynamicCall("SetInputValue(QString, QString)", "종목코드", code)
        self.dynamicCall("SetInputValue(QString, QString)", "수정주가구분", "1")

        if date != None:
            self.dynamicCall("SetInputValue(QString, QString)", "기준일자", date)

        self.dynamicCall("CommRqData(QString, QString, int, QString)", "주식일봉차트조회", "opt10081", sPrevNext, self.screen_calculation_stock) # Tr서버로 전송 -Transaction

        self.calculator_event_loop.exec_()

    def minute_kiwoom_db(self, code=None, tic=None, sPrevNext="0"):
        # 분봉 조회
        print("주식분봉차트조회주식분봉차트조회주식분봉차트조회주식분봉차트조회주식분봉차트조회주식분봉차트조회주식분봉차트조회주식분봉차트조회주식분봉차트조회")
        self.dynamicCall("DisconnectRealData(QString)", self.screen_calculation_stock)

        self.dynamicCall("SetInputValue(QString, QString)", "종목코드", code)
        if tic != None:
            self.dynamicCall("SetInputValue(QString, QString)", "틱범위", tic)
        self.dynamicCall("SetInputValue(QString, QString)", "수정주가구분", "1")
        # 횟수 제한 딜레이
        self.wait_for_request_delay()

        self.dynamicCall("CommRqData(QString, QString, int, QString)", "주식분봉차트조회", "opt10080", sPrevNext,
                         self.screen_calculation_stock)  # Tr서버로 전송 -Transaction

        self.calculator_event_loop.exec_()

    def result_minute_kiwoom_db(self):
        # 분봉 조회
        return self.result_minute_aver





    ############종목 분석 여기까지###########


    # 매수법칙 계산 들어가면 됨

    def read_code(self):

        self.portfolio_stock_dict = {}

        if os.path.exists(file_path):
            file = open(file_path, "r", encoding='utf-8-sig')

            lines = file.readlines()
            for line in lines:
                if line != "":
                    ls = line.split("\t")

                    stock_code = ls[0]
                    stock_name = ls[1]
                    stock_price = int(ls[2].split("\n")[0])
                    stock_price = abs(stock_price)

                    self.portfolio_stock_dict.update({stock_code:{"종목명":stock_name, "현재가":stock_price}})
            file.close()

            print("read_code", self.portfolio_stock_dict)

        print("리스트가 잘 들어왔는지 보자.", self.scan_list_result)

        if int(self.data_type) == 1:

            # Tr

            for i in range(len(self.scan_list_result)):
                sCode = self.scan_list_result[i]

                c_name = self.dynamicCall("GetMasterCodeName(QString)", sCode)

                prev_price = self.dynamicCall("GetMasterLastPrice(QString)", sCode)
                prev_price = abs(int(prev_price))

                if sCode not in self.portfolio_stock_dict and prev_price < self.buy_money:

                    self.portfolio_stock_dict.update({sCode:{"종목명": c_name, "전일가": prev_price}})

                    print("c_name", c_name)
                    print("prev_price", prev_price)
        elif int(self.data_type) == 2:
            # 실시간

            for i in range(len(self.scan_list_result)):
                sCode = self.scan_list_result[i]

                if sCode not in self.portfolio_stock_dict:

                    self.portfolio_stock_dict.update({sCode:{}})

                    print("sCode", sCode)


        print("나의 포트폴리오...", len(self.portfolio_stock_dict), self.portfolio_stock_dict)


    def screen_number_setting(self):

        screen_overwrite = []

        # 계좌평가잔고내역에 있는 종목들
        for code in self.account_stock_dict.keys():
            if code not in screen_overwrite:
                screen_overwrite.append(code)

        # 미체결에 있는 종목들
        for order_number in self.not_account2_stock_dict.keys():
            code = self.not_account2_stock_dict[order_number]['종목코드']

            if code not in screen_overwrite:
                screen_overwrite.append(code)

        # 포트폴리오에 담겨 있는 종목들
        for code in self.portfolio_stock_dict.keys():
            if code not in screen_overwrite:
                screen_overwrite.append(code)

        # 스크린번호 할당
        cnt = 0
        for code in screen_overwrite:

            temp_screen = int(self.screen_real_stock)
            meme_screen = int(self.screen_meme_stock)


            if int(self.data_type) == 1:
                # Tr
                temp_screen += 1
                self.screen_real_stock = str(temp_screen)

                meme_screen += 1
                self.screen_meme_stock = str(meme_screen)
            elif int(self.data_type) == 2:
                # 실시간
                if (cnt % 50) == 0:
                    temp_screen += 1
                    self.screen_real_stock = str(temp_screen)

                if (cnt % 50) == 0:
                    meme_screen += 1
                    self.screen_meme_stock = str(meme_screen)


            if code in self.portfolio_stock_dict.keys():
                self.portfolio_stock_dict[code].update({"스크린번호": str(self.screen_real_stock)})
                self.portfolio_stock_dict[code].update({"주문용스크린번호": str(self.screen_meme_stock)})
            elif code not in self.portfolio_stock_dict.keys():
                self.portfolio_stock_dict.update({code: {"스크린번호": str(self.screen_real_stock), "주문용스크린번호": str(self.screen_meme_stock)}})

            cnt += 1

        print("종목수 : ", cnt)
        print("screen_number_setting", self.portfolio_stock_dict)


    def realdata_slot(self, sCode, sRealType, sRealData):


        if sRealType == "장시작시간":
            fid = self.realType.REALTYPE[sRealType]['장운영구분']
            value = self.dynamicCall("GetCommRealData(QString, int)", sCode, fid)

            print("???????! !!!!!!!!!!!!!!!!??????????", value)

            if value == '0':
                print("장 시작 전")
            elif value == '3':
                print("장 시작")
            elif value == '2':
                print("장 종료, 동시호가로 넘어감")
            elif value == '4':
                print("3시30분 장 종료")

                self.dynamicCall("SetRealRemove(String, String)", ["ALL", "ALL"])

                # for code in self.portfolio_stock_dict.keys():
                #     self.dynamicCall("SetRealRemove(String, String)", self.portfolio_stock_dict[code]['스크린번호'], code)

                QTest.qWait(5000)

                self.file_delete()
                # self.calculator_fnc()

                sys.exit()
            elif value == '8':
                print("장 마감")

                self.dynamicCall("SetRealRemove(String, String)", ["ALL", "ALL"])

                QTest.qWait(5000)

                self.file_delete()
                # self.calculator_fnc()

            elif value == '9':
                print("장종료-시간외종료")
            elif value == 'a':
                print("시간외종가매매시작")
            elif value == 'b':
                print("시간외종가매매종료")
            elif value == 'c':
                print("시간외단일가매매시작")
            elif value == 'd':
                print("시간외단일가매매종료")
            elif value == 's':
                print("선옵장마감전동시호가시작")
            elif value == 'e':
                print("선옵장마감전동시호가종료")

        elif sRealType == "주식체결" and int(self.data_type) == 2:
            # 주식체결 실시간
            a = self.dynamicCall("GetCommRealData(QString, int)", sCode, self.realType.REALTYPE[sRealType]['체결시간'])  # HHMMSS
            b = self.dynamicCall("GetCommRealData(QString, int)", sCode, self.realType.REALTYPE[sRealType]['현재가'])   # +-0000
            b = abs(int(b))

            c = self.dynamicCall("GetCommRealData(QString, int)", sCode, self.realType.REALTYPE[sRealType]['전일대비'])  # +-0000
            c = abs(int(c))

            d = self.dynamicCall("GetCommRealData(QString, int)", sCode, self.realType.REALTYPE[sRealType]['등락율'])  # +-0000
            d = float(d)

            e = self.dynamicCall("GetCommRealData(QString, int)", sCode, self.realType.REALTYPE[sRealType]['(최우선)매도호가'])  # +-0000
            e = abs(int(e))

            f = self.dynamicCall("GetCommRealData(QString, int)", sCode, self.realType.REALTYPE[sRealType]['(최우선)매수호가'])  # +-0000
            f = abs(int(f))

            g = self.dynamicCall("GetCommRealData(QString, int)", sCode, self.realType.REALTYPE[sRealType]['거래량'])  # +-0000
            g = abs(int(g))

            h = self.dynamicCall("GetCommRealData(QString, int)", sCode, self.realType.REALTYPE[sRealType]['누적거래량'])  # +-0000
            h = abs(int(h))

            i = self.dynamicCall("GetCommRealData(QString, int)", sCode, self.realType.REALTYPE[sRealType]['고가'])  # +-0000
            i = abs(int(i))

            j = self.dynamicCall("GetCommRealData(QString, int)", sCode, self.realType.REALTYPE[sRealType]['시가'])  # +-0000
            j = abs(int(j))

            k = self.dynamicCall("GetCommRealData(QString, int)", sCode, self.realType.REALTYPE[sRealType]['저가'])  # +-0000
            k = abs(int(k))

            if sCode not in self.portfolio_stock_dict:
                self.portfolio_stock_dict.update({sCode:{}})

            self.portfolio_stock_dict[sCode].update({"체결시간": a})
            self.portfolio_stock_dict[sCode].update({"현재가": b})
            self.portfolio_stock_dict[sCode].update({"전일대비": c})
            self.portfolio_stock_dict[sCode].update({"등락율": d})
            self.portfolio_stock_dict[sCode].update({"(최우선)매도호가": e})
            self.portfolio_stock_dict[sCode].update({"(최우선)매수호가": f})
            self.portfolio_stock_dict[sCode].update({"거래량": g})
            self.portfolio_stock_dict[sCode].update({"누적거래량": h})
            self.portfolio_stock_dict[sCode].update({"고가": i})
            self.portfolio_stock_dict[sCode].update({"시가": j})
            self.portfolio_stock_dict[sCode].update({"저가": k})

            print("내 포트폴리오에 상세 업데이트", sCode, self.portfolio_stock_dict[sCode])

            now = datetime.datetime.now()
            now_time_HMS = now.strftime("%H%M%S")
            print("내 포트폴리오에 상세 업데이트 시간", now.strftime('%Y-%m-%d %H:%M:%S'), now_time_HMS, a)

            delay_ = int(now_time_HMS) - int(a)
            print("시간 딜레이 발생", delay_)

            if str(now_time_HMS) != str(a) and delay_ > 200:
                print("시간 딜레이 크게 발생", delay_)

                self.dynamicCall("SetRealRemove(String, String)", ["ALL", "ALL"])

                self.real_stock_start(2)

            else:

                # 계좌잔고평가내역에 있고 오늘 산 잔고에는 없을 경우
                if sCode in self.account_stock_dict.keys() and sCode not in self.jango_dict.keys():
                    print("1")
                    # print("%s %s" % ("신규매도를 한다_1", sCode))
                    # 1: 신규매수, 2:신규매도, 3:매수취소, 4:매도취소, 5:매수정정, 6:매도정정

                    asd = self.account_stock_dict[sCode]

                    if int(asd['매매가능수량']) > 1:
                        first_meme_price = int(asd['매매가능수량']) / 2
                    else:
                        first_meme_price = asd['매매가능수량']

                    medo = b * asd['매매가능수량']
                    mesoo = asd['매입가'] * asd['매매가능수량']

                    meme_tax = (mesoo * self.meme_tax_price) + (medo * self.meme_tax_price) + (medo * self.stock_tax_price)

                    meme_rate = (medo - mesoo - meme_tax) / mesoo * 100
                    # meme_rate = (b / asd['매입가']) * 100 - 100

                    print("매도 매수 세금 수익률", medo, mesoo, meme_tax, meme_rate)

                    # 2차 매도인지 여부
                    second_meme = False
                    result_sell_quantity = self.sell_money
                    result_all_sell_quantity = int(asd['매매가능수량']) * int(asd['매입가'])
                    if result_all_sell_quantity > result_sell_quantity:
                        second_meme = True

                    # 횟수 제한 딜레이
                    code_nm = self.dynamicCall("GetMasterCodeName(QString)", sCode)

                    print("종목명, 수익률, 매매수량", code_nm, meme_rate, int(first_meme_price), asd['매입가'], b)

                    #################
                    if asd['매매가능수량'] > 0:

                        five_percent = True

                        if os.path.isfile(second_order_path) == True:
                            file = open(second_order_path, "r", encoding='utf-8-sig')

                            lines = file.readlines()

                            if len(lines) > 0:

                                for i in range(len(lines)):
                                    if lines[i] != "":
                                        ls = lines[i].split("\t")

                                        if sCode == ls[0]:
                                            five_percent = False
                                            break
                        else:
                            file = open(second_order_path, "w", encoding='utf-8-sig')
                            file.write("")
                            file.close()

                        if five_percent == True and second_meme == True:

                            if (meme_rate > 5 or meme_rate < -5) and sCode not in self.sell_ing:

                                wa = []
                                wa.append(sCode)

                                if len(wa) > 1:
                                    wa.clear()
                                    pass
                                else:
                                    print("%s %s" % ("처음 신규매도를 한다_1_1", sCode))

                                    # 횟수 제한 딜레이
                                    self.wait_for_request_delay()

                                    order_success = self.dynamicCall(
                                        "SendOrder(QString, QString, QString, int, QString, int, int, QString, QString)",
                                        ["신규매도", self.portfolio_stock_dict[sCode]['주문용스크린번호'], self.account_num, 2, sCode,
                                         int(first_meme_price), 0, self.realType.SENDTYPE['거래구분']['시장가'], ""])

                                    self.last_request_time = time.time()

                                    if order_success == 0:
                                        print("매도주문 전달 성공", meme_rate)
                                        if sCode not in self.sell_ing:
                                            self.sell_ing.append(sCode)

                                        if sCode in self.account_stock_dict.keys() and asd['매매가능수량'] == 1:
                                            del self.account_stock_dict[sCode]

                                    else:
                                        print("매도주문 전달 실패")
                        else:
                            result_me = self.calculate_moving_average(sCode, 7)

                            print("int(result_me)", int(result_me))
                            print("계좌잔고평가내역에 있고 오늘 산 잔고에는 없을 경우 : 현재가격(b)", b)

                            if int(result_me) > int(b):  # 7일선 and 전량매도

                                wa = []
                                wa.append(sCode)

                                if len(wa) > 1:
                                    wa.clear()
                                    pass
                                else:
                                    print("%s %s" % ("7% 마지막 신규매도를 한다_1_2", sCode))

                                    # 횟수 제한 딜레이
                                    self.wait_for_request_delay()

                                    order_success = self.dynamicCall(
                                        "SendOrder(QString, QString, QString, int, QString, int, int, QString, QString)",
                                        ["신규매도", self.portfolio_stock_dict[sCode]['주문용스크린번호'], self.account_num, 2, sCode,
                                         asd['매매가능수량'], 0, self.realType.SENDTYPE['거래구분']['시장가'], ""])

                                    self.last_request_time = time.time()

                                    if order_success == 0:
                                        print("매도주문 전달 성공", meme_rate)

                                        if sCode not in self.sell_ing:
                                            self.sell_ing.append(sCode)

                                        if sCode in self.account_stock_dict.keys():
                                            del self.account_stock_dict[sCode]

                                    else:
                                        print("매도주문 전달 실패")
                            else:
                                average_price = self.result_minute_kiwoom_db()
                                print("10분봉 240 이평선에 팔기 240가격:", average_price)
                                print("10분봉 240 이평선에 팔기 현재가격:", b)
                                if sCode in average_price.keys() and int(average_price[sCode]["d_day_0_240"]) > int(b) or int(average_price[sCode]["d_day_0_37"]) > int(b) and int(average_price[sCode]["sto_fast"]) < 20:
                                    wa = []
                                    wa.append(sCode)

                                    if len(wa) > 1:
                                        wa.clear()
                                        pass
                                    else:
                                        print("%s %s" % ("10분봉 240 마지막 신규매도를 한다_2_2", sCode))

                                        # 횟수 제한 딜레이
                                        self.wait_for_request_delay()

                                        order_success = self.dynamicCall(
                                            "SendOrder(QString, QString, QString, int, QString, int, int, QString, QString)",
                                            ["신규매도", self.portfolio_stock_dict[sCode]['주문용스크린번호'], self.account_num, 2,
                                             sCode,
                                             asd['매매가능수량'], 0, self.realType.SENDTYPE['거래구분']['시장가'], ""])

                                        self.last_request_time = time.time()

                                        if order_success == 0:
                                            print("매도주문 전달 성공", meme_rate)
                                            if sCode not in self.sell_ing:
                                                self.sell_ing.append(sCode)

                                            if sCode in self.account_stock_dict.keys():
                                                del self.account_stock_dict[sCode]

                                        else:
                                            print("매도주문 전달 실패")


                    ##################
                # 오늘 산 잔고에 있을 경우
                elif sCode in self.jango_dict.keys():
                    print("2")

                    jd = self.jango_dict[sCode]

                    if int(jd['주문가능수량']) > 1:
                        first_meme_price = int(jd['주문가능수량']) / 2
                    else:
                        first_meme_price = jd['주문가능수량']

                    medo = b * jd['주문가능수량']
                    mesoo = jd['매입단가'] * jd['주문가능수량']

                    meme_tax = (mesoo * self.meme_tax_price) + (medo * self.meme_tax_price) + (medo * self.stock_tax_price)



                    meme_rate = (medo - mesoo - meme_tax) / mesoo * 100
                    # meme_rate = (b / jd['매입단가']) * 100 - 100

                    print("매도 매수 세금 수익률", medo, mesoo, meme_tax, meme_rate)

                    code_nm = self.dynamicCall("GetMasterCodeName(QString)", sCode)

                    # 2차 매도인지 여부
                    second_meme = False
                    result_sell_quantity = self.sell_money
                    result_all_sell_quantity = int(jd['주문가능수량']) * int(jd['매입단가'])
                    if result_all_sell_quantity > result_sell_quantity:
                        second_meme = True

                    print("종목명, 수익률, 매매수량", code_nm, meme_rate, int(first_meme_price), jd['매입단가'], b)

                    if jd['주문가능수량'] > 0:

                        five_percent = True

                        if os.path.isfile(second_order_path) == True:
                            file = open(second_order_path, "r", encoding='utf-8-sig')

                            lines = file.readlines()

                            if len(lines) > 0:

                                for i in range(len(lines)):
                                    if lines[i] != "":
                                        ls = lines[i].split("\t")

                                        if sCode == ls[0]:
                                            five_percent = False
                                            break
                        else:
                            file = open(second_order_path, "w", encoding='utf-8-sig')
                            file.write("")
                            file.close()

                        if five_percent == True and second_meme == True:
                            if (meme_rate > 5 or meme_rate < -5) and sCode not in self.sell_ing:

                                wa = []
                                wa.append(sCode)

                                if len(wa) > 1:
                                    wa.clear()
                                    pass
                                else:
                                    print("%s %s" % ("처음 신규매도를 한다_2_1", sCode))

                                    # 횟수 제한 딜레이
                                    self.wait_for_request_delay()

                                    order_success = self.dynamicCall(
                                        "SendOrder(QString, QString, QString, int, QString, int, int, QString, QString)",
                                        ["신규매도", self.portfolio_stock_dict[sCode]['주문용스크린번호'], self.account_num, 2, sCode,
                                         int(first_meme_price), 0, self.realType.SENDTYPE['거래구분']['시장가'], ""])

                                    self.last_request_time = time.time()

                                    if order_success == 0:
                                        print("매도주문 전달 성공", meme_rate)
                                        if sCode not in self.sell_ing:
                                            self.sell_ing.append(sCode)

                                        if sCode in self.account_stock_dict.keys() and jd['주문가능수량'] == 1:
                                            del self.account_stock_dict[sCode]

                                    else:
                                        print("매도주문 전달 실패")
                        else:
                            result_me = self.calculate_moving_average(sCode, 7)

                            print("int(result_me)", int(result_me))
                            print("오늘 산 잔고에 있을 경우 : 현재가 (b)", b)

                            if int(result_me) > int(b):  # 7일선 and 전량매도

                                wa = []
                                wa.append(sCode)

                                if len(wa) > 1:
                                    wa.clear()
                                    pass
                                else:
                                    print("%s %s" % ("7% 마지막 신규매도를 한다_2_2", sCode))

                                    # 횟수 제한 딜레이
                                    self.wait_for_request_delay()

                                    order_success = self.dynamicCall(
                                        "SendOrder(QString, QString, QString, int, QString, int, int, QString, QString)",
                                        ["신규매도", self.portfolio_stock_dict[sCode]['주문용스크린번호'], self.account_num, 2, sCode,
                                         jd['주문가능수량'], 0, self.realType.SENDTYPE['거래구분']['시장가'], ""])

                                    self.last_request_time = time.time()

                                    if order_success == 0:
                                        print("매도주문 전달 성공", meme_rate)
                                        if sCode not in self.sell_ing:
                                            self.sell_ing.append(sCode)

                                        if sCode in self.account_stock_dict.keys():
                                            del self.account_stock_dict[sCode]

                                    else:
                                        print("매도주문 전달 실패")
                            else:
                                average_price = self.result_minute_kiwoom_db()
                                print("10분봉 240 이평선에 팔기 240가격:", average_price)
                                print("10분봉 240 이평선에 팔기 현재가격:", b)
                                if sCode in average_price.keys() and int(average_price[sCode]["d_day_0_240"]) > int(b) or int(average_price[sCode]["d_day_0_37"]) > int(b) and int(average_price[sCode]["sto_fast"]) < 20:
                                    wa = []
                                    wa.append(sCode)

                                    if len(wa) > 1:
                                        wa.clear()
                                        pass
                                    else:
                                        print("%s %s" % ("10분봉 240 마지막 신규매도를 한다_2_2", sCode))

                                        # 횟수 제한 딜레이
                                        self.wait_for_request_delay()

                                        order_success = self.dynamicCall(
                                            "SendOrder(QString, QString, QString, int, QString, int, int, QString, QString)",
                                            ["신규매도", self.portfolio_stock_dict[sCode]['주문용스크린번호'], self.account_num, 2,
                                             sCode,
                                             jd['주문가능수량'], 0, self.realType.SENDTYPE['거래구분']['시장가'], ""])

                                        self.last_request_time = time.time()

                                        if order_success == 0:
                                            print("매도주문 전달 성공", meme_rate)
                                            if sCode not in self.sell_ing:
                                                self.sell_ing.append(sCode)

                                            if sCode in self.account_stock_dict.keys():
                                                del self.account_stock_dict[sCode]

                                        else:
                                            print("매도주문 전달 실패")
                # 등락율이 1.0 % 이상이고 오늘 산 잔고에 없을 경우

                # if sCode not in self.jango_dict.keys():

                elif d > 1.0 and self.buy_money > b:

                    if sCode not in self.jango_dict:

                        print("3")

                        wa = []
                        wa.append(sCode)

                        if len(wa) > 1:
                            wa.clear()
                            pass
                        else:
                            print("3 : self.use_money", self.use_money)
                            # result = (self.use_money * 0.1) / b
                            result = self.buy_money / b

                            if result >= 1:

                                quantity = int(result)
                                # e => 현재가

                                print("3 : quantity", quantity)

                                if quantity > 0:

                                    print("3 : order_number", self.not_account2_stock_dict)

                                    already_stock = False

                                    if len(self.not_account2_stock_dict) != 0:

                                        for order_number in self.not_account2_stock_dict.keys():
                                            code = self.not_account2_stock_dict[order_number]['종목코드']
                                            if code == sCode:
                                                already_stock = True
                                                break

                                    print("3 : code : already_stock ?", already_stock, sCode)

                                    if already_stock == False:
                                        if sCode not in self.buy_ing:

                                            # 횟수 제한 딜레이
                                            self.wait_for_request_delay()

                                            code_nm = self.dynamicCall("GetMasterCodeName(QString)", sCode)

                                            print("%s %s %s" % ("신규매수를 한다_1_1", sCode, code_nm))

                                            print("quantityquantityquantity", quantity)

                                            order_success = self.dynamicCall(
                                                "SendOrder(QString, QString, QString, int, QString, int, int, QString, QString)",
                                                ["시장가매수", self.portfolio_stock_dict[sCode]['주문용스크린번호'], self.account_num, 1,
                                                 sCode, quantity, 0, self.realType.SENDTYPE['거래구분']['시장가'], ""])

                                            self.last_request_time = time.time()

                                            if order_success == 0:
                                                print("매수주문 전달 성공", order_success)
                                                self.buy_ing.append(sCode)
                                            else:
                                                print("매수주문 전달 실패", order_success)

                                        else:
                                            code_nm = self.dynamicCall("GetMasterCodeName(QString)", sCode)

                                            already_stock = False

                                            if len(self.not_account2_stock_dict) != 0:

                                                for order_number in self.not_account2_stock_dict.keys():
                                                    code = self.not_account2_stock_dict[order_number]['종목코드']
                                                    if sCode in code:
                                                        already_stock = True
                                                        break
                                            if already_stock == False:

                                                print("매수취소 대기에 없다.", sCode, code_nm, self.buy_ing)

                                                # if sCode in self.buy_ing:
                                                #     self.buy_ing.remove(sCode)

                                            elif already_stock == True:

                                                print("이미 종목 매수 중이다.", sCode, code_nm, code, self.buy_ing)

                                                if sCode not in self.buy_ing:
                                                    self.buy_ing.append(sCode)

                                    else:
                                        print("code 검색...이미 종목 있다!!!!!!!!!")
                # else:
                # ########################### 매수 중복중인거 해결부터 하기

                if len(self.not_account2_stock_dict) > 0:

                    print("4")

                    not_meme_list = list(self.not_account2_stock_dict)

                    for order_num in not_meme_list:
                        code = self.not_account2_stock_dict[order_num]["종목코드"]
                        meme_price = self.not_account2_stock_dict[order_num]["주문가격"]
                        not_quantity = self.not_account2_stock_dict[order_num]["미체결수량"]
                        order_gubun = self.not_account2_stock_dict[order_num]["주문구분"]

                        if order_gubun == "매수" and not_quantity > 0 and b > meme_price:
                            wa = []
                            wa.append(code)

                            if len(wa) > 1:
                                wa.clear()
                                pass
                            else:
                                print("%s %s" % ("매수취소 한다", code))

                                # 횟수 제한 딜레이
                                self.wait_for_request_delay()

                                order_success = self.dynamicCall(
                                    "SendOrder(QString, QString, QString, int, QString, int, int, QString, QString)",
                                    ["매수취소", self.portfolio_stock_dict[code]['주문용스크린번호'], self.account_num, 3, code, 0, 0,
                                     self.realType.SENDTYPE['거래구분']['지정가'], order_num])

                                self.last_request_time = time.time()

                                if order_success == 0:
                                    if code in self.buy_ing:
                                        self.buy_ing.remove(code)
                                    print("매수취소 주문 전달 성공")
                                else:
                                    print("매수취소 주문 전달 실패")
                        elif not_quantity == 0:
                            del self.not_account2_stock_dict[order_num]
                            if code in self.buy_ing:
                                self.buy_ing.remove(code)
                            if code in self.sell_ing:
                                self.sell_ing.remove(code)

                        elif order_gubun == "매도" and not_quantity > 0 and b < meme_price:

                            wa = []
                            wa.append(code)

                            if len(wa) > 1:
                                wa.clear()
                                pass
                            else:
                                print("%s %s" % ("매도취소 한다", code))
                                # 횟수 제한 딜레이
                                self.wait_for_request_delay()

                                order_success = self.dynamicCall(
                                    "SendOrder(QString, QString, QString ,int, QString, int, int, QString, QString)",
                                    ["매도취소", self.portfolio_stock_dict[code]['주문용스크린번호'], self.account_num, 4, code, 0, 0,
                                     self.realType.SENDTYPE['거래구분']['지정가'], order_num])  # order_num 은 어떤 주문을 취소할 것인가.

                                self.last_request_time = time.time()

                                if order_success == 0:
                                    if code in self.sell_ing:
                                        self.sell_ing.remove(code)

                                    print("%s 매도취소 전달 성공" % code)  # 체결잔고에서  del을 했기 때문에 여기서 하지 않는다.

                                else:
                                    print("%s 매도취소 전달 실패" % code)


                # ## 마지막 잠시 없애기
                #
                # for key, value in self.portfolio_stock_dict.copy().items():
                #
                #     if key == sCode:
                #         print("실시간 제거 완료", sCode, self.portfolio_stock_dict[sCode]['스크린번호'])
                #         self.dynamicCall("SetRealRemove(String, String)", self.portfolio_stock_dict[sCode]['스크린번호'], sCode)
                #         self.cancel_screen_number(self.portfolio_stock_dict[sCode]['스크린번호'])
                #         QTest.qWait(100)
                #         break



    def chejan_slot(self, sGubun, nItemCnt, sFidList):

        # QTest.qWait(1000)

        if int(sGubun) == 0:
            print("주문체결")
            account_num = self.dynamicCall("GetChejanData(int)", self.realType.REALTYPE['주문체결']['계좌번호'])
            sCode = self.dynamicCall("GetChejanData(int)", self.realType.REALTYPE['주문체결']['종목코드'])[1:]
            stock_name = self.dynamicCall("GetChejanData(int)", self.realType.REALTYPE['주문체결']['종목명'])
            stock_name = stock_name.strip()

            origin_order_number = self.dynamicCall("GetChejanData(int)", self.realType.REALTYPE['주문체결']['원주문번호'])
            order_number = self.dynamicCall("GetChejanData(int)", self.realType.REALTYPE['주문체결']['주문번호'])
            order_status = self.dynamicCall("GetChejanData(int)", self.realType.REALTYPE['주문체결']['주문상태'])   # 접수, 확인, 체결
            order_quan = self.dynamicCall("GetChejanData(int)", self.realType.REALTYPE['주문체결']['주문수량'])
            order_quan = int(order_quan)

            order_price = self.dynamicCall("GetChejanData(int)", self.realType.REALTYPE['주문체결']['주문가격'])
            order_price = int(order_price)

            not_chegual_quan = self.dynamicCall("GetChejanData(int)", self.realType.REALTYPE['주문체결']['미체결수량'])
            not_chegual_quan = int(not_chegual_quan)

            order_gubun = self.dynamicCall("GetChejanData(int)", self.realType.REALTYPE['주문체결']['주문구분'])    # -매도 +매수
            order_gubun = order_gubun.strip().lstrip('+').lstrip('-')

            chequal_time_str = self.dynamicCall("GetChejanData(int)", self.realType.REALTYPE['주문체결']['주문/체결시간'])

            chequal_price = self.dynamicCall("GetChejanData(int)", self.realType.REALTYPE['주문체결']['체결가'])   #deault : ''


            if chequal_price == '':
                chequal_price = 0
            else:
                chequal_price = int(chequal_price)

            chequal_quantity = self.dynamicCall("GetChejanData(int)", self.realType.REALTYPE['주문체결']['체결량'])   #deault : ''

            if chequal_quantity == '':
                chequal_quantity = 0
            else:
                chequal_quantity = int(chequal_quantity)

            current_price = self.dynamicCall("GetChejanData(int)", self.realType.REALTYPE['주문체결']['현재가'])
            current_price = abs(int(current_price))

            first_sell_price = self.dynamicCall("GetChejanData(int)", self.realType.REALTYPE['주문체결']['(최우선)매도호가'])
            first_sell_price = abs(int(first_sell_price))

            first_buy_price = self.dynamicCall("GetChejanData(int)", self.realType.REALTYPE['주문체결']['(최우선)매수호가'])
            first_buy_price = abs(int(first_buy_price))

            ##########새로 들어온 주분이면 주문번호 할당
            if order_number not in self.not_account2_stock_dict.keys():
                self.not_account2_stock_dict.update({order_number: {}})

            self.not_account2_stock_dict[order_number].update({"종목코드": sCode})
            self.not_account2_stock_dict[order_number].update({"주문번호": order_number})
            self.not_account2_stock_dict[order_number].update({"종목명": stock_name})
            self.not_account2_stock_dict[order_number].update({"주문상태": order_status})
            self.not_account2_stock_dict[order_number].update({"주문수량": order_quan})
            self.not_account2_stock_dict[order_number].update({"주문가격": order_price})
            self.not_account2_stock_dict[order_number].update({"미체결수량": not_chegual_quan})
            self.not_account2_stock_dict[order_number].update({"원주문번호": origin_order_number})
            self.not_account2_stock_dict[order_number].update({"주문구분": order_gubun})
            self.not_account2_stock_dict[order_number].update({"주문/체결시간": chequal_time_str})
            self.not_account2_stock_dict[order_number].update({"체결가": chequal_price})
            self.not_account2_stock_dict[order_number].update({"체결량": chequal_quantity})
            self.not_account2_stock_dict[order_number].update({"현재가": current_price})
            self.not_account2_stock_dict[order_number].update({"(최우선)매도호가": first_sell_price})
            self.not_account2_stock_dict[order_number].update({"(최우선)매수호가": first_buy_price})

            print("주문체결됨", stock_name, self.not_account2_stock_dict)

            if order_gubun == "매도":

                if os.path.isfile(second_order_path) == True:

                    file = open(second_order_path, "r", encoding='utf-8-sig')

                    lines = file.readlines()

                    print("주문체결됨 lines : ", lines)
                    print("self.buy_ing", self.buy_ing)
                    print("self.sell_ing", self.sell_ing)

                    file.close()

                    exist_code = False

                    for i in range(len(lines)):
                        if lines[i] != "":
                            ls = lines[i].split("\t")

                            if sCode == ls[0]:
                                exist_code = True

                    if exist_code == False:
                        print("second_order_path에 종목 정보 덮어쓰기", stock_name)
                        file = open(second_order_path, "a", encoding="utf8")
                        file.write("%s\t%s\t%s\n" % (sCode, stock_name, str(order_price)))
                        file.close()
                    else:
                        print("second_order_path에 종목 정보 삭제하기", stock_name)

                        if len(lines) > 0:

                            re_line = []

                            for i in range(len(lines)):
                                if lines[i] != "":
                                    ls = lines[i].split("\t")

                                    if sCode != ls[0]:
                                        stock_code = ls[0]
                                        stock_name = ls[1]
                                        stock_price = int(ls[2].split("\n")[0])
                                        stock_price = abs(stock_price)
                                        add_line = str(stock_code) + "\t" + str(stock_name) + "\t" + str(
                                            stock_price) + "\n"
                                        re_line.append(str(add_line))
                            print("re_linere_linere_line", len(re_line), re_line)

                            if len(re_line) > 0:

                                file = open(second_order_path, "w", encoding='utf-8-sig')
                                file.write(str(""))
                                file.close()

                                for i in range(len(re_line)):
                                    ls = lines[i].split("\t")
                                    stock_code = ls[0]
                                    stock_name = ls[1]
                                    stock_price = int(ls[2].split("\n")[0])

                                    file = open(second_order_path, "a", encoding='utf-8-sig')
                                    file.write("%s\t%s\t%s\n" % (stock_code, stock_name, str(stock_price)))
                                    file.close()
                        if sCode in self.buy_ing:
                            self.buy_ing.remove(sCode)
                        if sCode in self.sell_ing:
                            self.sell_ing.remove(sCode)

                else:
                    file = open(second_order_path, "w", encoding='utf-8-sig')
                    file.write("")
                    file.close()

        elif int(sGubun) == 1:
            print("잔고")

            account_num = self.dynamicCall("GetChejanData(int)", self.realType.REALTYPE['잔고']['계좌번호'])
            sCode = self.dynamicCall("GetChejanData(int)", self.realType.REALTYPE['잔고']['종목코드'])[1:]


            stock_name = self.dynamicCall("GetChejanData(int)", self.realType.REALTYPE['잔고']['종목명'])
            stock_name = stock_name.strip()

            current_price = self.dynamicCall("GetChejanData(int)", self.realType.REALTYPE['잔고']['현재가'])
            current_price = abs(int(current_price))

            stock_quan = self.dynamicCall("GetChejanData(int)", self.realType.REALTYPE['잔고']['보유수량'])
            stock_quan = int(stock_quan)

            like_quan = self.dynamicCall("GetChejanData(int)", self.realType.REALTYPE['잔고']['주문가능수량'])
            like_quan = int(like_quan)

            buy_price = self.dynamicCall("GetChejanData(int)", self.realType.REALTYPE['잔고']['매입단가'])
            buy_price = abs(int(buy_price))

            total_buy_price = self.dynamicCall("GetChejanData(int)", self.realType.REALTYPE['잔고']['총매입가'])
            total_buy_price = int(total_buy_price)

            meme_gubun = self.dynamicCall("GetChejanData(int)", self.realType.REALTYPE['잔고']['매도매수구분'])
            meme_gubun = self.realType.REALTYPE['매도수구분'][meme_gubun]

            first_sell_price = self.dynamicCall("GetChejanData(int)", self.realType.REALTYPE['잔고']['(최우선)매도호가'])
            first_sell_price = abs(int(first_sell_price))

            first_buy_price = self.dynamicCall("GetChejanData(int)", self.realType.REALTYPE['잔고']['(최우선)매수호가'])
            first_buy_price = abs(int(first_buy_price))

            if sCode not in self.jango_dict.keys():
                self.jango_dict.update({sCode: {}})

            self.jango_dict[sCode].update({"현재가": current_price})
            self.jango_dict[sCode].update({"종목코드": sCode})
            self.jango_dict[sCode].update({"종목명": stock_name})
            self.jango_dict[sCode].update({"보유수량": stock_quan})
            self.jango_dict[sCode].update({"주문가능수량": like_quan})
            self.jango_dict[sCode].update({"매입단가": buy_price})
            self.jango_dict[sCode].update({"총매입가": total_buy_price})
            self.jango_dict[sCode].update({"매도매수구분": meme_gubun})
            self.jango_dict[sCode].update({"(최우선)매도호가": first_sell_price})
            self.jango_dict[sCode].update({"(최우선)매수호가": first_buy_price})

            print("잔고 추가", self.jango_dict, stock_quan)

            if stock_quan == 0:

                del self.jango_dict[sCode]
                self.dynamicCall("SetRealRemove(QString, QString)", self.portfolio_stock_dict[sCode]['스크린번호'], sCode)

                if os.path.isfile(second_order_path) == True:
                    file = open(second_order_path, "r", encoding='utf-8-sig')

                    lines = file.readlines()

                    print("잔고확인 lines : ", lines)
                    print("self.buy_ing", self.buy_ing)
                    print("self.sell_ing", self.sell_ing)

                    file.close()
                else:
                    file = open(second_order_path, "w", encoding='utf-8-sig')
                    file.write("")
                    file.close()

                exist_code = False

                for i in range(len(lines)):
                    if lines[i] != "":
                        ls = lines[i].split("\t")

                        if sCode == ls[0]:
                            exist_code = True

                if exist_code == True:

                    if len(lines) > 0:

                        re_line = []

                        for i in range(len(lines)):
                            if lines[i] != "":
                                ls = lines[i].split("\t")

                                if sCode != ls[0]:
                                    stock_code = ls[0]
                                    stock_name = ls[1]
                                    stock_price = int(ls[2].split("\n")[0])
                                    stock_price = abs(stock_price)

                                    add_line = str(stock_code) + "\t" + str(stock_name) + "\t" + str(
                                        stock_price) + "\n"

                                    re_line.append(str(add_line))
                        if len(re_line) > 0:
                            file = open(second_order_path, "w", encoding='utf-8-sig')
                            file.write(str(""))
                            file.close()

                            for i in range(len(re_line)):
                                ls = lines[i].split("\t")
                                stock_code = ls[0]
                                stock_name = ls[1]
                                stock_price = int(ls[2].split("\n")[0])

                                file = open(second_order_path, "a", encoding='utf-8-sig')
                                file.write("%s\t%s\t%s\n" % (stock_code, stock_name, str(stock_price)))
                                file.close()

    def msg_slot(self, sScrNo, sRQName, sTrCode, msg):
        print("스크린: %s, 요청이름: %s, tr코드: %s --- %s" %(sScrNo, sRQName, sTrCode, msg))


    def file_delete(self):
        if os.path.isfile(file_path):
            os.remove(file_path)

######################################################################################################

    # 조건 검색식

    def _handler_condition_load(self, ret, msg):    # 실시간
        print("handler condition load", ret, msg)

    def _handler_real_condition(self, code, type, cond_name, cond_index):   # 실시간
        print(" << 실시간 >>")
        print(cond_name, code, type)
        if code not in self.scan_list_result:
            if code != '':
                if type == 'I':
                    self.scan_list_result.append(code)
                    print("신규 편입")

        else:
            if type == "D":
                self.scan_list_result = list(set(self.scan_list_result))
                print("중복 제거")
        print("실시간 : ", self.scan_list_result)
        # self.read_code()

    def _handler_tr_condition(self, sScrNo, strCodeList, strConditionName, nIndex, nNext):   # 실시간
        print(" << tr >> ")
        # print("tr : ", sScrNo, strConditionName, nIndex, nNext)
        # print("tr : ", strCodeList)

        # 조건 검색식에 나온 모든 종목 담기
        result_list = strCodeList.split(';')
        for i in range(len(result_list)):
            if result_list[i] not in self.scan_list_result:
                if result_list[i] != '':
                    self.scan_list_result.append(result_list[i])

        print("최종 추출된 종목들", self.scan_list_result)

        ##### def read_code
        # self.read_code()
        # 우선 포트폴리오에 담자

        # for i in range(len(self.scan_list_result)):
        #     sCode = self.scan_list_result[i]
        #
        #     c_name = self.dynamicCall("GetMasterCodeName(QString)", sCode)
        #
        #     prev_price = self.dynamicCall("GetMasterLastPrice(QString)", sCode)
        #     prev_price = abs(int(prev_price))
        #
        #     if sCode not in self.portfolio_stock_dict and prev_price < self.buy_money:
        #         self.portfolio_stock_dict.update({sCode: {"종목명": c_name, "전일가": prev_price}})
        #
        #         print("c_name", c_name)
        #         print("prev_price", prev_price)

        self.detail_account_info_event_loop.exit()


    def GetConditionNameList(self):

        self.scan_list_result = []  # 검색식 종목 초기화

        condition_names_str = self.dynamicCall("GetConditionNameList()")

        self.condition_names_list = condition_names_str.split(';')
        self.condition_names_list.pop()

        for i in range(len(self.condition_names_list)):
            if 'day_danta' in self.condition_names_list[i]:
                self.scan_list.append(self.condition_names_list[i])
            if '이자보상비율' in self.condition_names_list[i]:
                self.scan_list.append(self.condition_names_list[i])
            if 'magic' in self.condition_names_list[i]:
                self.scan_list.append(self.condition_names_list[i])
            if 'taegg' in self.condition_names_list[i]:
                self.scan_list.append(self.condition_names_list[i])
            if 'dia' in self.condition_names_list[i]:
                self.scan_list.append(self.condition_names_list[i])
            if 'jiduk' in self.condition_names_list[i]:
                self.scan_list.append(self.condition_names_list[i])
        print("추출된 조건식", self.scan_list)

        for i in range(len(self.scan_list)):
            result = self.scan_list[i].split('^')
            self.send_condition(result[1], result[0])
            time.sleep(0.4)


    def send_condition(self, name, index):
        self.dynamicCall("SendCondition(QString, QString, int, int)", self.screen_scan, name, index, 1)
        # self.SendCondition(self.screen_scan, name, index, 1)
        self.detail_account_info_event_loop.exec_()
        # 최종 추출된 종목들
    ###가격 가져오기

    def getItemInfo(self, new_code):
        # 횟수제한
        self.wait_for_request_delay()

        self.dynamicCall("SetInputValue(QString, QString)", "종목코드", new_code)
        self.dynamicCall("CommRqData(QString, QString, int, QString)", "주식기본정보요청", "opt10001", 0, "100")

        self.last_request_time = time.time()

        self.detail_account_info_event_loop.exec_()

    ### 이동평균선 계산
    def calculate_moving_average(self, code, period):

        import requests
        import pandas as pd
        from ast import literal_eval

        try:

            try:
                # 네이버 금융 API를 통해 데이터 가져오기
                response = requests.get(
                    f"https://api.finance.naver.com/siseJson.naver?symbol={code}&requestType=0&count=50&timeframe=day")
                response_data = literal_eval(response.text.strip())

                # 응답 데이터를 DataFrame으로 변환
                price_data = pd.DataFrame(response_data[1:], columns=response_data[0])
                price_data.index = price_data["날짜"]
                price_data = price_data[["시가", "고가", "저가", "종가", "거래량"]]

                # print("price_data", price_data)

                # 이동평균 계산
                moving_average = price_data["종가"].rolling(window=period).mean()

                # , min_periods = 1

                # 결과 출력
                last_ma_value = moving_average.iloc[-1]

                pt = str(period) + "일 이동 평균 값 => " + str(last_ma_value)

                print("이평선 결과 :", pt)

                return last_ma_value

            except Exception as e:
                print("에러 발생:", e)

        except Exception as e:
            print(e)

    ### stochastic Fast 계산
    def calculate_stochastic_fast(self, code, period=5, smoothing=3):

        import requests
        import pandas as pd
        from ast import literal_eval

        try:
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

    def calculate_moving_price(self, code):

        import requests
        import pandas as pd
        from ast import literal_eval
        from datetime import datetime, timedelta

        # import pandas_datareader.data as web

        try:

            print("최근 3일간 저가 가격")
            # 네이버 금융 API를 통해 데이터 가져오기
            response = requests.get(
                f"https://api.finance.naver.com/siseJson.naver?symbol={code}&requestType=0&count=20&timeframe=day")
            response_data = literal_eval(response.text.strip())

            print("response_data", response_data)

            # 응답 데이터를 DataFrame으로 변환
            price_data = pd.DataFrame(response_data[1:], columns=response_data[0])
            price_data.index = price_data["날짜"]
            price_data = price_data[["시가", "고가", "저가", "종가", "거래량"]]

            # 최신 날짜부터 역순으로 저가 값을 추출하여 3개의 저가 값을 얻을 때까지 반복
            low_prices = []
            for idx, row in price_data[::-1].iterrows():
                low_price = row['저가']
                low_prices.append(low_price)
                if len(low_prices) >= 3:
                    break

            # 결과 출력
            print("최신 3일간 저가:", low_prices)

            # return last_ma_value

        except Exception as e:
            print("에러 발생:", e)

    #### 실시간 컨트롤

    def wait_for_request_delay(self):
        # 충분한 시간 간격을 두고 매수 주문 전송
        now_time = time.time()
        elapsed_time = now_time - self.last_request_time
        calcul_time = (self.request_delay - elapsed_time) * 1000
        print("wait_for_request_delay", now_time, self.last_request_time)
        if elapsed_time < self.request_delay:
            print("Tr 주문 전송을 위해 잠시 기다립니다.", calcul_time)

            QTest.qWait(calcul_time)

    def scan_wait_for_request_delay(self):
        # 충분한 시간 간격을 두고 조건 검색 하기

        jogun_scan = True

        now_time = time.time()
        elapsed_time = now_time - self.last_scan_time
        print("scan_wait_for_request_delay", now_time, self.last_scan_time)
        if elapsed_time < self.scan_delay:
            jogun_scan = False
            print("조건검색 전송을 위해 잠시 기다립니다.", elapsed_time)
            # time.sleep(self.scan_delay - elapsed_time)

        return jogun_scan
    ### 여긴 주문하는 부분분
    # def process_real_data(self, current_time, code, current_price):
    #     if code not in self.previous_data or self.previous_data[code] != current_time:
    #         self.previous_data[code] = current_time
    #         print(f"{current_time} - {code} 현재가: {current_price}")
    #
    #         # 데이터를 받은 시간과 현재 시간이 같은 경우에만 시장가 매수 주문 전송
    #         if self.is_same_time(current_time):
    #             self.send_market_buy_order(code)
    #
    # def is_same_time(self, current_time):
    #     return current_time == time.time()
    #
    # def send_market_buy_order(self, code):
    #     # 충분한 시간 간격을 두고 매수 주문 전송
    #     self.wait_for_request_delay()
    #
    #     account_number = "계좌번호"  # 매수할 계좌번호 입력
    #     quantity = 1  # 매수할 수량 입력
    #     self.kiwoom.dynamicCall("SendOrder(QString, QString, QString, int, QString, int, int, QString, QString)",
    #                             ["시장가매수", "0101", account_number, 1, code, quantity, 0, "", ""])
    #     print(f"{code} 시장가로 매수 주문이 전송되었습니다.")
    #     self.last_request_time = time.time()


    def real_stock_start(self, data_type):

        if int(data_type) == 2:
            ### 2번 실시간

            result = len(self.portfolio_stock_dict)
            print("갱신전 관리 종목 갯수", result)

            self.read_code()  # 저장된 종목들 불러온다.
            self.screen_number_setting()  # 스크린 번호를 할당

            QTest.qWait(5000)

            my_port_many = 0
            for code in self.portfolio_stock_dict.keys():
                my_port_many += 1
                screen_num = self.portfolio_stock_dict[code]['스크린번호']
                fids = self.realType.REALTYPE['주식체결']['체결시간']
                self.dynamicCall("SetRealReg(QString, QString, QString, QString)", screen_num, code, fids, "1")
                print("실시간 등록 코드: %s, 스크린번호: %s, fid번호: %s" % (code, screen_num, fids))
                QTest.qWait(300)

            print("내 종목 관리 갯수 : ", my_port_many)

    def test_time(self):
        now_time = time.time()
        print("test time : ", now_time)

        return now_time

    def test_time2(self):
        from main_p import FirstTab
        self.first_tab = FirstTab()
        self.first_tab.onActivated_test(1)