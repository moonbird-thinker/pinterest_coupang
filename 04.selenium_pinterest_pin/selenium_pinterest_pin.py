# -*- coding: utf-8 -*-

import subprocess
import datetime
import platform
import random
import time
from datetime import timedelta
from datetime import date, datetime, timedelta
from time import gmtime
from time import sleep
from time import strftime
import chromedriver_autoinstaller
import pyshorteners
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os.path
from bs4 import BeautifulSoup
import time
import requests
import re
import os
import json
import hashlib
import hmac
from time import gmtime, strftime
from pprint import pprint as pp
from urllib.parse import urljoin
from urllib import parse
from urllib.parse import urlparse
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tqdm import tqdm
from dateutil.relativedelta import relativedelta
from urllib.request import urlopen
from tabulate import tabulate
import pandas as pd
from pathlib import Path
import undetected_chromedriver as uc
import urllib3
from itertools import product
from PIL import Image
import pyperclip
import pyautogui

urllib3.disable_warnings()  # warnings 메시지를 띄우지 않기 위해

print(f'\n현재 마우스 포인트 위치: {pyautogui.position()}')

osName = platform.system()  # window 인지 mac 인지 알아내기 위한

C_END = "\033[0m"
C_BOLD = "\033[1m"
C_INVERSE = "\033[7m"
C_BLACK = "\033[30m"
C_RED = "\033[31m"
C_GREEN = "\033[32m"
C_YELLOW = "\033[33m"
C_BLUE = "\033[34m"
C_PURPLE = "\033[35m"
C_CYAN = "\033[36m"
C_WHITE = "\033[37m"
C_BGBLACK = "\033[40m"
C_BGRED = "\033[41m"
C_BGGREEN = "\033[42m"
C_BGYELLOW = "\033[43m"
C_BGBLUE = "\033[44m"
C_BGPURPLE = "\033[45m"
C_BGCYAN = "\033[46m"
C_BGWHITE = "\033[47m"

# [사용자 입력 정보] ======================================================================================================== START

# finterest_image가 임시 저장되어 있는 path
local_image_path = "Z:\\finterest_image\\"

# 워터마크 썸네일 사용할 것인지 아닌지
watermark = True

# 워터마크 썸네일 사용할 경우 워터마크 파일명
watermark_file_name = 'watermark.png'

# 키워드당 몇개의 PIN을 발행할 것인지? 10개까지~
pin_number_per_keyword = 3

# 쿠팡 파트너 API access key와 secret key, 현재 default로는 coupang API 로 링크를 생성하지 않고 AFCODE 기반으로 직접 링크를 만들고 있어 coupang API 로 단축 url 을 생성하고 싶을때 해당 값 세팅
coupang_access_key = ""  # access_key 를 입력하세요!
coupang_secret_key = ""  # secret_key 를 입력하세요!

# 링크 변환을 할 수 없는 경우를 위해 fake 쿠팡 링크를 만들어준다.
fake_coupang_link = 'https://link.coupang.com/a/3KS6f'  # 간편 링크를 통해 만든 본인 링크

# 쿠팡 파트너스 채널 아이디
CHANNELID = 'pinterest'

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15'
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15'
]
random_user_agent = random.choice(user_agents)
fixed_user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Whale/3.19.166.16 Safari/537.36'

# itemscout category 및 파라미터 선택
# 1차분류: 선택안함,
#        패션의류(1)(여성의류, 여성언더웨어/잠옷, 남성의류, 남성언더웨어/잠옷),
#        패션잡화(2)(양말, 여성신발, 남성신발, 신발용품, 여성가방, 남성가방, 여행용가방/소품, 지갑, 벨트, 모자, 장갑, 선글라스/안경태, 헤어액세서리, 패션소품, 시계, 순금, 주얼리),
#        화장품/미용(3)(스킨케어, 선케어, 클렌징, 마스크/팩, 베이스메이크업, 색조메이크업, 네일케어, 바디케어, 헤어케어, 헤어스타일링, 향수, 뷰티소품, 남성화장품),
#        디이털/가전(4)(학습기기, 게임기/타이틀, PC, PC액세서리, 노트북액세서리, 태블릿PC액세서리, 모니터주변기기, 주변기기, 멀티미디어장비, 저장장치, PC부품, 네트워크장비, 소프트웨어, 노트북, 태블릿PC, 모니터, 휴대폰, 휴대폰악세서리, 카메라/캠코더용품, 광학기기/용품, 영상가전, 음향가전, 이미용가전, 계절가전, 주방가전, 자동차기기),
#        가구/인테리어(5)(침실가구, 거실가구, 주방가구, 수납가구, 아동/주니어가구, 서재/사무용가구, 아웃도어가구, DIY자재/용품, 인테리어소품, 침구단품, 침구세트, 솜류, 카페트/러그, 커큰/블라인드, 수예, 홈데코),
#        출산/육아(6)(분유, 기저귀, 물티슈, 이유식, 아기간식, 수유용품, 유모차, 카시트, 외출용품, 목용용품, 스킨/바디용품, 위생/건강용품, 구강철결용품, 유아세제, 소독/살균용품, 안전용품, 유아가구, 이유식용품, 임부복, 임산부용품, 유아침구, 출산/돌기념품, 신생아의류, 유아동의류, 유아동잡화, 수영복/용품, 유아발육용품, 완구/매트, 인형, 교구, 유아동 주얼리, 유아동언더웨어/잠옷),
#        식품(7)(건강식품, 다이어트식품, 냉동/간편조리식품, 축산물, 반찬, 김치, 음료, 과자/베이커리, 유가공품, 수산물, 농산물, 밀키트, 가루/분말류, 라면/면류, 소스/드레싱, 식용유/오일, 장류, 잼/시럽, 제과/제빵재료, 조미료, 통조림/캔, 주류),
#        스포츠/레저(8)(마라톤용품, 당구용품, 기타스포츠용품, 등산, 캠핑, 골프, 헬스, 요가/필라테스, 인라인스케이트, 스케이트/보드/롤러, 오토바이/스쿠터, 축구, 야구, 농구, 배구, 탁구, 배드민턴, 테니스, 스쿼시, 족구, 볼링, 스킨스쿠버, 검도, 댄스, 권투, 보호용품, 수련용품, 스포츠액세서리, 자전거, 스키/보드, 낚시, 수영),
#        생활/건강(9)(화방용품, 자동차용품, 수집품, 관상어용품, 음반, DVD, 종교, 주방용품, 세탁용품, 건강측정용품, 건강관리용품, 당뇨관리용품, 의료용품, 실버용, 재활운동용품, 물리치료/저주파용품, 좌욕/좌훈용품, 냉온/찜질용품, 구강위생용품, 눈건강용품, 발건강용품, 안마용품, 수납/정리용품, 청소용품, 생활용춤, 원예/식물, 정원/원예용품, 블루레이, 반려동물, 악기, 욕실용품, 문구/사무용품, 공구),
#        여가/생활편의(10)(원데이클래스, 국내여행/체험, 해외여행, 렌터카, 생활편의, 예체능레슨, 자기계발/취미레슨, 홈케어서비스),
#        면세점(11)(화장품, 향수, 시계/기프트, 주얼리, 패션/잡화, 전자제품, 식품/건강),
#        도서(45830)(소설, 시/에세이, 인문, 가정/요리, 경제/경영, 자기계발, 사회/정치, 역사, 종교, 예술/대중문화, 국어/외국어, 자연/과학, 수험서/자격증, 여행, 컴퓨터/IT, 잡지, 청소년, 유아, 어린이, 만화, 외국도서, 건가/취미, 중학교참고서, 고등학교참고서, 초등학교참고서, 중고도서)
# 기간: 최근 30일, 과거선택(날짜선택) (duration 30d 또는 날짜 설정, duration: 2023-03,2023-04 3월부터 4월)
# 성별: 전체, 남성, 여성 (sample. 남성과 여성이면 f,m)
# 연령대: 10, 20, 30, 40, 50, 60 (sample. 20,60 이면 20대부터 60대까지)

# 아이템스카우트 정보 설정, 카테고리 (1차 분류만 있을때) - 랜덤 카테고리 말고 조합에 의한 카테고리선정으로 전체의 데이터를 기준으로 계속 돌게 만들어준다.
random_itemscout_category_lists = ['패션의류', '패션잡화', '화장품/미용', '디이털/가전', '가구/인테리어',
                                   '출산/육아', '식품', '스포츠/레저', '생활/건강', '여가/생활편의', '면세점', '도서']
random_itemscout_cid_lists = ['1', '2', '3', '4', '5',
                              '6', '7', '8', '9', '10', '11', '45830']
random_itemscout_age_lists = ['10,10', '20,20', '30,30', '40,40', '50,50', '60,60', '10,20', '10,30', '10,40',
                              '10,50', '10,60', '20,30', '20,40', '20,50', '20,60'
    , '30,40', '30,50', '30,60', '40,50', '40,60', '50,60']
random_itemscout_gender_lists = ['f,m', 'f', 'm']  # 전체, 여성, 남성

random_itemscout_input_info_list = list(
    product(random_itemscout_cid_lists, random_itemscout_age_lists, random_itemscout_gender_lists))
# print(random_itemscout_input_info_list)

# # datalab 정보 설정
# # 패션의류 50000000 패션잡화 50000001 화장품/미용 50000002 디지털가전 50000003 가구인테리어 50000004
# # 출산육아 50000005 식품 50000006 스포츠레저 50000007 생활건강 50000008 여가생활편의 50000009 면세점 50000010 도서 50005542
# random_naverdatalab_category_lists = ['패션의류', '패션잡화', '화장품/미용', '디지털가전', '가구인테리어', '출산육아', '식품', '스포츠레저', '생활건강', '여가생활편의', '면세점', '도서']
random_naverdatalab_cid_lists = ['50000000', '50000001', '50000002', '50000003', '50000004', '50000005',
                                 '50000006', '50000007', '50000008', '50000009', '50000010', '50005542']
random_naverdatalab_age_lists = ['10,20,30,40,50,60', '10', '20', '30', '40', '50',
                                 '60']  # 전체, 10대, 20대, 30대 40대, 50대, 60대이상
random_naverdatalab_gender_lists = ['f,m', 'f', 'm']  # 전체, 여성, 남성

random_naverdatalab_input_info_list = list(
    product(random_naverdatalab_cid_lists, random_naverdatalab_age_lists, random_naverdatalab_gender_lists))
# print(random_naverdatalab_input_info_list)

# 추출하고자 하는 각 카테고리별 keyword 수 (네이버 max:500, 아이템스카우트 max: "아이템발굴"을 통한 500)
wanted_item_num = 500

# 이미 검색된 키워드의 중복성 제거를위해 엑셀에 그 데이터들을 저장 후 리스트 비교를 함
keyword_list_csv_path = 'keyword_lists.csv'

# time 값 지정
LOADING_WAIT_TIME = 5
LONG_PAUSE_TIME = 3
PAUSE_TIME = 0.5
GENERAL_REQUEST_WAIT_TIME = 2
LOGIN_WAIT_TIME = 180  # 로그인시 기다리는 시간
NEXT_KEYWORD_SEARCH_TIME = 300  # random.randint(300, 500)  # 키워드와 키워드 사이의 sleep 간격
WRITE_PINTEREST_WAITTIME = 300  # random.randint(300, 500)  # random.randint(900, 1000)
NEXT_TRY_ISSUE_OCCURE = 500  # 해당 프로그램이 수행될때는 절전모드로의 진입이나 디스플레이 꺼짐등에 오동작하는 경우 또는 윈도우 창이
# 떠서 이미지 삽입 작업이 있을때나 제목등의 작성중일때는 컨트롤하는 경우 이슈 발생시 다음 대기시간까지의 sleep time")

# NEXT_KEYWORD_SEARCH_TIME = 300  # 키워드와 키워드 사이의 sleep 간격
# WRITE_PINTEREST_WAITTIME = 300  # random.randint(900, 1000)
# NEXT_TRY_ISSUE_OCCURE = 900  # 해당 프로그램이 수행될때는 절전모드로의 진입이나 디스플레이 꺼짐등에 오동작하는 경우 또는 윈도우 창이


# [사용자 입력 정보] ======================================================================================================== END

# [시스템 공통 입력 정보] ======================================================================================================== START

# partner product info
product_name_lists = []  # 상품명
product_discount_rate_lists = []  # 할인률과 원래가격
product_price_lists = []  # 상품가격
product_arrival_time_lists = []  # 도착예정시간
product_rating_star_lists = []  # star 평가: ex.3.5
product_review_lists = []  # 상품리뷰 수
product_link_lists = []  # 상품 구매 링크
product_image_lists = []  # 상품 이미지

product_short_url_lists = []  # 쿠팡 숏 링크 리스트

# itemscout 에서 아이템들 대한 정보 리스트
keyword_id_lists = []  # keyword 아이디
rank_lists = []  # 랭킹
no_of_search_total_lists = []  # 검색수
prdCnt_lists = []  # 상품수

# itemscout 에서 각 keyword 에 따른 전반적인 분석을 위한 리스트
competitionIntensity_lists = []  # 경쟁강도 수치
competitionIntensityDesc_lists = []  # 경쟁강도 등급
adClickRateTotal_lists = []  # 광고클릭률 수치
adClickRateTotalDesc_lists = []  # 광고클릭률 등급

# itemscout 에서 각 keyword 에 따른 블로그 카페 분석 리스트
blogCompetitionRatio_lists = []  # 블로그 경쟁강도 수치
blogCompetitionDesc_lists = []  # 블로그 경쟁강도 등급
cafeCompetitionRatio = []  # 카페 경쟁강도 수치
cafeCompetitionDesc_lists = []  # 카페 경쟁강도 등급

# itemscout 에서 각 keyword 에 따른 쿠팡 분석 리스트
coupangCompetitionRatio_lists = []  # 쿠팡 경쟁강도 수치
coupangCompetitionDesc_lists = []  # 쿠팡 경쟁강도 등급

# 랜덤 생성 리스트
itemscout_cid_category_lists = []
itemscout_duration_lists = []
itemscout_age_lists = []
itemscout_gender_list = []

# 랜덤 수 생성 이미 나온 랜덤 번호는 안나오도록 (겹치지 않는 카테고리를 선택하기 위해)
random_number_list = []

# 데이터랩스 & 아이템스카우트 키워드 저장 리스트
keyword_name_lists = []  # 키워드

# 상품이 pin_number_per_keyword 개가 안되거나 쿠팡 결과에 이상이 있을경우 대기 시간을 skip
# write 하는 과정에서 skip 되어 발행 대기 시간을 가지지 않게 하기 위해
check_next_wait_time = 1


# [시스템 공통 입력 정보] ======================================================================================================== END

def init_driver():
    # try :
    #     shutil.rmtree(r"C:\chrometemp")  #쿠키 / 캐쉬파일 삭제(캐쉬파일 삭제시 로그인 정보 사라짐)
    # except FileNotFoundError :
    #     pass

    if osName not in "Windows":
        try:
            subprocess.Popen([
                '/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9245 --user-data-dir="~/Desktop/crawling/chromeTemp45"'],
                shell=True, stdout=subprocess.PIPE)  # 디버거 크롬 구동
        except FileNotFoundError:
            subprocess.Popen([
                '/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9245 --user-data-dir="~/Desktop/crawling/chromeTemp45"'],
                shell=True, stdout=subprocess.PIPE)
    else:
        try:
            subprocess.Popen(r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9245 '
                             r'--user-data-dir="C:\chromeTemp45"')  # 디버거 크롬 구동
        except FileNotFoundError:
            subprocess.Popen(
                r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9245 '
                r'--user-data-dir="C:\chromeTemp45"')

    options = webdriver.ChromeOptions()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9245")

    # service = ChromeService(
    #     '/Users/xxx/.wdm/drivers/chromedriver/mac64/118.0.5993.70/chromedriver-mac-x64/chromedriver')  # for mac
    # service = ChromeService('C:\\Users\\ree31\\.wdm\\drivers\\chromedriver\\win64\\118.0.5993.71\\chromedriver.exe')
    # service = ChromeService('C:\\Users\\ree31\\.wdm\\drivers\\chromedriver\\win64\\119.0.6045.106\\chromedriver.exe')
    # service = ChromeService('C:\\Users\\ree31\\.wdm\\drivers\\chromedriver\\win64\\122.0.6261.95\\chromedriver-win32\\chromedriver.exe')
    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(LOADING_WAIT_TIME)
    return driver


def pinterest_login(driver):
    driver.get('https://www.pinterest.co.kr/')
    sleep(LOADING_WAIT_TIME)

    print(f'\n{C_BOLD}{C_RED}{C_BGBLACK}로그인 버튼을 눌러 로그인을 진행해 주세요주의: 3분안에 로그인을 완료해주세요!!!]{C_END}')
    pbar = tqdm(total=LOGIN_WAIT_TIME)
    for x in range(LOGIN_WAIT_TIME):
        sleep(1)
        try:
            try:
                driver.find_element(By.XPATH, "//div[contains(text(),'지난 30일 동안의 데이터 보기')]")
                break
            except:
                driver.find_element(By.XPATH, "//span[contains(text(),'만들기')]")
                break
        except:
            pass
        pbar.update(1)
    pbar.close()


def get_items_for_itemscout(cid, duration, ages, gender):
    # itemscout 랜덤 생성 리스트
    # global itemscout_cid_category_lists
    # itemscout_cid_category_lists = []
    global itemscout_duration_lists
    itemscout_duration_lists = []
    global itemscout_age_lists
    itemscout_age_lists = []
    global itemscout_gender_list
    itemscout_gender_list = []

    global keyword_id_lists
    keyword_id_lists = []  # keyword 아이디
    global rank_lists
    rank_lists = []  # 랭킹
    global keyword_name_lists
    keyword_name_lists = []  # 키워드
    global no_of_search_total_lists
    no_of_search_total_lists = []  # 검색수
    global prdCnt_lists
    prdCnt_lists = []  # 상품수

    headers = {
        'accept': 'application/json, text/plain, */*',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://itemscout.io',
        'referer': 'https://itemscout.io/',
        'user-agent': fixed_user_agent,
    }

    data = {
        'duration': parse.quote(duration, encoding="utf-8"),  # url encoding 후 넣어줌
        'genders': parse.quote(gender, encoding="utf-8"),
        'ages': parse.quote(ages, encoding="utf-8")
    }

    response = requests.post(f'https://api.itemscout.io/api/category/{cid}/data', headers=headers, data=data).json()
    # pp(response)

    temp_dict_lists = []
    for idx, item in enumerate(response['data']['data'].items()):
        if idx == wanted_item_num:
            break
        # print(f'{item}')
        # print(f"keywordID(keyword ID): {item[0]}")  # keyword 아이디
        # print(f"rank(랭킹): {item[1]['rank']}")  # 랭킹
        # print(f"keyword(키워드): {item[1]['keyword']}")  # 키워드
        # print(f"total(검색수): {item[1]['monthly']['total']}")  # 검색수
        # print(f"prdCnt(상품수): {item[1]['prdCnt']}")  # 상품수
        print(
            f"{idx + 1}. ID {item[0]} | keyword {item[1]['keyword']} | 랭킹 {item[1]['rank']} | 검색수 {item[1]['monthly']['total']} | 상품수 {item[1]['prdCnt']}")
        # itemscout_cid_category_lists.append(category)
        itemscout_duration_lists.append(duration)
        itemscout_age_lists.append(ages)
        itemscout_gender_list.append(gender)
        keyword_id_lists.append(item[0])
        rank_lists.append(item[1]['rank'])
        no_of_search_total_lists.append(item[1]['monthly']['total'])
        prdCnt_lists.append(item[1]['prdCnt'])

        keyword = item[1]['keyword']
        temp_dict = {'keyword': keyword, 'posted': 'X'}
        # keyword_name_lists.append(keyword)
        temp_dict_lists.append(temp_dict)

    itemscout_df = pd.DataFrame(temp_dict_lists, columns=['keyword', 'posted'])

    csv_path = f'{keyword_list_csv_path.replace(".csv", "_itemscout.csv")}'

    # print(tabulate(naverbook_df, headers='keys', tablefmt='grid'))
    if not os.path.exists(csv_path):
        itemscout_df.to_csv(csv_path, mode='w', sep=',', na_rep='NaN', encoding='utf-8-sig', index=False)
    else:
        itemscout_df.to_csv(csv_path, mode='a', sep=',', na_rep='NaN', encoding='utf-8-sig', index=False, header=False)

    print(f'\n{C_BOLD}{C_YELLOW}{C_BGBLACK}({csv_path})에서 중복된 행을 제거 시작{C_END}')
    data = pd.read_csv(csv_path)
    data = data.drop_duplicates(subset=['keyword'], keep="first")
    data.to_csv(csv_path, index=False, encoding="utf-8-sig")
    print(f'\n{C_BOLD}{C_YELLOW}{C_BGBLACK}중복된 검색 결과의 엑셀행을 제거 완료{C_END}\n')


def get_naver_datalab_shopping_insight(cid, start_date, end_date, age, gender):
    sleep(PAUSE_TIME)

    REQUEST_METHOD = "POST"
    DOMAIN = "https://datalab.naver.com"
    URL = "/shoppingInsight/getCategoryKeywordRank.naver"
    # https://www.useragentstring.com/ 를 통해 user_agent 업데이트
    user_agent = fixed_user_agent
    referer = 'https://datalab.naver.com/'

    url = "{}{}".format(DOMAIN, URL)

    if wanted_item_num % 20 > 0:
        page_num = wanted_item_num // 20 + 1
        last_page_count = wanted_item_num % 20
    else:
        page_num = wanted_item_num // 20
        last_page_count = 20

    temp_dict_lists = []
    for page_idx in range(page_num):
        if page_num == page_idx + 1:
            page_count = last_page_count
        else:
            page_count = 20
        response = requests.request(method=REQUEST_METHOD, url=url,
                                    headers={
                                        'User-Agent': user_agent,
                                        'referer': referer
                                    },
                                    params={
                                        "cid": cid,
                                        "timeUnit": 'date',
                                        "startDate": start_date,
                                        "endDate": end_date,
                                        "age": age,
                                        "gender": gender,
                                        "device": '',
                                        "page": page_idx + 1,
                                        "count": page_count  # 페이지당 MAX가 20, 카테고리별 총 500개 아이템이라 25번의 루프가 필요
                                    })
        # pp(response.json())
        items = response.json()
        # print(items['ranks'][0]['keyword'])
        # print(items['ranks'][1]['keyword'])

        global keyword_name_lists
        for keyword_idx in range(len(items['ranks'])):
            keyword = items['ranks'][keyword_idx]['keyword']
            # print(f"{keyword_idx + 1}. {keyword}")
            temp_dict = {'keyword': keyword, 'posted': 'X'}
            keyword_name_lists.append(keyword)
            temp_dict_lists.append(temp_dict)

        print(f"({page_idx + 1})/({page_num}) ...")
        sleep(0.8)

    # print(keyword_name_lists)
    print(f"\n키워드 리스트:")
    for idx, keyword in enumerate(keyword_name_lists):
        print(f"{idx + 1}. {keyword}")

    naverlab_df = pd.DataFrame(temp_dict_lists, columns=['keyword', 'posted'])

    csv_path = f'{keyword_list_csv_path.replace(".csv", "_naverlab.csv")}'

    # print(tabulate(naverlab_df, headers='keys', tablefmt='grid'))
    if not os.path.exists(csv_path):
        naverlab_df.to_csv(csv_path, mode='w', sep=',', na_rep='NaN', encoding='utf-8-sig', index=False)
    else:
        naverlab_df.to_csv(csv_path, mode='a', sep=',', na_rep='NaN', encoding='utf-8-sig', index=False, header=False)

    print(f'\n{C_BOLD}{C_YELLOW}{C_BGBLACK}({csv_path})에서 중복된 행을 제거 시작{C_END}')
    data = pd.read_csv(csv_path)
    data = data.drop_duplicates(subset=['keyword'], keep="first")
    data.to_csv(csv_path, index=False, encoding="utf-8-sig")
    print(f'\n{C_BOLD}{C_YELLOW}{C_BGBLACK}중복된 검색 결과의 엑셀행을 제거 완료{C_END}\n')


def get_naver_shopping_book():
    global keyword_name_lists
    keyword_name_lists = []  # 키워드

    url = f"https://msearch.shopping.naver.com/book/home"  # the URL of the search result page

    header = {
        'User-Agent': fixed_user_agent
    }
    response = requests.get(url, headers=header)  # make a GET request to the URL
    soup = BeautifulSoup(response.text, "lxml")  # parse the HTML content with BeautifulSoup
    # print(soup)

    script_tag = soup.select_one('#__NEXT_DATA__')
    # pp(json.loads(script_tag.string))

    print(type(response), type(soup), type(script_tag), type(script_tag.string), type(json.loads(script_tag.string)))
    # "<class 'requests.models.Response'> <class 'bs4.BeautifulSoup'> <class 'bs4.element.Tag'> <class 'bs4.element.Script'> <class 'dict'>"

    data = json.loads(script_tag.string)
    # print(len(data["props"]["pageProps"]["dehydratedState"]["queries"][0]["state"]["data"]["pages"][0]["BookHome"]["data"]))
    # pp(data)

    book_info_path = "book_info.json"
    Path(book_info_path).touch(exist_ok=True)
    with open(book_info_path, "w") as output_file:
        json.dump(data, output_file)
        print(f'\n도서정보 저장을 위해 python 객체(dict)를 json.dump를 사용하여 json 파일로 쓰기\n')

    real_data = data["props"]["pageProps"]["dehydratedState"]["queries"][0]["state"]["data"]["pages"][0]["BookHome"][
        "data"]

    temp_dict_lists = []
    for idx_data in range(len(real_data)):
        print(f'대분류 : {real_data[idx_data]["template"]}({real_data[idx_data]["title"]})')  # 대분류
        # CAS-IMAGE-SINGLE(None)
        # CULTURE-TODAY-BOOK-NEW(#알라딘 X 네이버 책방)
        # CULTURE-LIST-3COL(지난주 소설 베스트셀러)
        # CULTURE-BOOK-EVENT(None)
        # CAS-IMAGE-EMPHASIS-EXTRA-CONTENT-3COL(온 가족이 함께 즐기는 도서 기획전)
        # CULTURE-SHOPPING-BOOK-BEST-SELLER-AUTO(베스트셀러 TOP20)
        # CULTURE-TAB(이번 주 화제의 신간)
        # CULTURE-TODAY-BOOK-NEW(#예스24 X 네이버 책방)
        # CULTURE-AUDIO-BOOK(None)
        # CULTURE-TODAY-BOOK-NEW(#서점 분야별 화제의 신간 )
        # CULTURE-TAB(우리 아이 쑥쑥, 유아동/청소년 인기 신간)
        # CULTURE-SHOPPING-BOOK-BEST-SELLER-AUTO(영유아/청소년 베스트셀러 TOP20)
        # CULTURE-TAB(믿고 읽는, 한국학교사서협회 추천 도서)
        # CULTURE-TODAY-BOOK(사전 예약 판매)
        # CULTURE-TAB(일상을 풍성하게, 취미/실용서 인기 신간)

        if real_data[idx_data][
            "template"] == 'CULTURE-SHOPPING-BOOK-BEST-SELLER-AUTO':  # 베스트셀러 TOP20 - 현재는 베스트셀러 TOP20만 가져오게 하였습니다.
            real_blocks = real_data[idx_data]["blocks"]
            for idx_block in range(len(real_blocks)):
                print(f'\n소분류 : {real_blocks[idx_block]["title"]}')  # 소분류
                real_materials = real_blocks[idx_block]["materials"]
                for idx_material in range(len(real_materials)):
                    print(
                        f'({real_materials[idx_material]["rank"]}). {real_materials[idx_material]["title"]} | {real_materials[idx_material]["url"]} | {real_materials[idx_material]["image"]["url"]} | {real_materials[idx_material]["author"]} | {real_materials[idx_material]["publisher"]}')

                    keyword = f'{real_materials[idx_material]["title"]} 책 도서'
                    temp_dict = {'keyword': keyword, 'posted': 'X'}
                    # keyword_name_lists.append(keyword)
                    temp_dict_lists.append(temp_dict)

    # # 소분류 마다 책이 다양하게 분포 되어있겠지만 책의 중복성이 있을 수 있음 따라서 리스트 키워드 중복성 제거
    # keyword_name_lists = list(set(keyword_name_lists))
    # # print(keyword_name_lists)

    naverbook_df = pd.DataFrame(temp_dict_lists, columns=['keyword', 'posted'])

    csv_path = f'{keyword_list_csv_path.replace(".csv", "_naverbook.csv")}'

    # print(tabulate(naverbook_df, headers='keys', tablefmt='grid'))
    if not os.path.exists(csv_path):
        naverbook_df.to_csv(csv_path, mode='w', sep=',', na_rep='NaN', encoding='utf-8-sig', index=False)
    else:
        naverbook_df.to_csv(csv_path, mode='a', sep=',', na_rep='NaN', encoding='utf-8-sig', index=False, header=False)

    print(f'\n{C_BOLD}{C_YELLOW}{C_BGBLACK}({csv_path})에서 중복된 행을 제거 시작{C_END}')
    data = pd.read_csv(csv_path)
    data = data.drop_duplicates(subset=['keyword'], keep="first")
    data.to_csv(csv_path, index=False, encoding="utf-8-sig")
    print(f'\n{C_BOLD}{C_YELLOW}{C_BGBLACK}중복된 검색 결과의 엑셀행을 제거 완료{C_END}\n')


def partner_coupang(keyword):
    global check_next_wait_time

    # target_url = 'https://www.coupang.com/np/search?component=&q=' + \
    #              str(keyword) + '&channel=user'  # URL

    # target_url = f'https://www.coupang.com/np/search?rocketAll=false&q={str(keyword)}&sorter=saleCountDesc'  # 판매량순

    target_url = f'https://www.coupang.com/np/search?component=&q={str(keyword)}&channel=user'  # 쿠팡 랭킹순

    headers = {'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6,zh;q=0.5',
               'User-Agent': random_user_agent,
               'Accept-Encoding': 'gzip'
               }

    res = requests.get(url=target_url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    all_search_product_lists = soup.select('li.search-product')  # 검색 상품 모두
    ad_search_product_lists = soup.select('li.search-product.search-product__ad-badge')  # 광고 상품만

    rank_product_lists = []
    for product in all_search_product_lists:
        if product not in ad_search_product_lists:
            rank_product_lists.append(product)

    if len(rank_product_lists) < pin_number_per_keyword:
        print(f'\n검색된 결과가 없거나 ({pin_number_per_keyword})개 미만입니다. 다시금 시도하세요')
        check_next_wait_time = 1
        sleep(1)
        return 0
    else:
        print('\n검색된 상품 수량 : ', len(rank_product_lists))

    # # Top 10개만 리스트에 담기 (사용되는 리스트 설명)
    # product_name_lists = []  # 상품명
    # product_discount_rate_lists = []  # 할인률과 원래가격
    # product_price_lists = []  # 상품가격
    # product_arrival_time_lists = []  # 도착예정시간
    # product_rating_star_lists = []  # star 평가: ex.3.5
    # product_review_lists = []  # 상품리뷰 수
    # product_link_lists = []  # 상품 구매 링크
    # product_image_lists = []  # 상품 이미지

    for inner in rank_product_lists[:pin_number_per_keyword]:
        product_name = inner.select_one('div > div.name')  # 상품명
        if product_name is not None:
            # print(product_name.text)
            product_name_lists.append(product_name.text)
        else:
            product_name_lists.append('No data')
        product_discount_rate = inner.select_one('div.price-wrap > div.price > span.price-info')  # 할인률과 원래가격
        if product_discount_rate is not None:
            # print(product_discount_rate.text.lstrip())
            product_discount_rate_lists.append(f'{product_discount_rate.text.lstrip()}원')
        else:
            product_discount_rate_lists.append('No data')
        product_price = inner.select_one('div.price-wrap > div.price > em > strong')  # 상품가격
        if product_price is not None:
            # print(product_price.text.replace(",", ""))
            product_price_lists.append(f"{product_price.text}원")
        else:
            product_price_lists.append('No data')
        product_arrival_time = inner.select_one('div.price-wrap > div.delivery > span.arrival-info')  # 도착예정시간
        if product_arrival_time is not None:
            # print(product_arrival_time.text)
            product_arrival_time_lists.append(product_arrival_time.text)
        else:
            product_arrival_time_lists.append('No data')
        product_rating_star = inner.select_one(
            'div.other-info > div.rating-star > span.star > em.rating')  # star 평가: ex.3.5
        if product_rating_star is not None:
            # print(product_rating_star.text)
            product_rating_star_lists.append(product_rating_star.text)
        else:
            product_rating_star_lists.append('No data')
        product_review = inner.select_one('div.other-info > div > span.rating-total-count')  # 상품리뷰 수
        if product_review is not None:
            # print(re.sub("[()]", "", product_review.text))
            product_review_lists.append(re.sub("[()]", "", product_review.text))
        else:
            product_review_lists.append('0')
        product_link = inner.select_one('a.search-product-link')  # 상품 구매 링크
        try:
            p_link = "https://www.coupang.com" + product_link['data-product-link']
        except:
            p_link = "https://www.coupang.com" + product_link['href']
        product_link_lists.append(p_link)

        product_image = inner.select_one('img.search-product-wrap-img')
        p_image = product_image.get('data-img-src')
        if p_image is None:
            p_image = product_image.get('src')
            if 'https:' in p_image:
                print("https: 문구를 포함하고 있습니다.")  # 예외처리 가끔 https: 가 포함되어져 오는 경우
                p_image = f'{p_image}'
            else:
                p_image = f'https:{p_image}'
            # print(p_image)
            product_image_lists.append(p_image)
        else:
            if 'https:' in p_image:
                p_image = f'{p_image}'
                print("https: 문구를 포함하고 있습니다.")
            else:
                p_image = f'https:{p_image}'
            # print(p_image)
            product_image_lists.append(p_image)

    # 출력
    count = 1
    for product_name, product_discount_rate, product_price, product_arrival_time, product_rating_star, product_review, product_link, product_image in zip \
                (product_name_lists, product_discount_rate_lists, product_price_lists, product_arrival_time_lists,
                 product_rating_star_lists,
                 product_review_lists, product_link_lists, product_image_lists):
        print(
            f'{count}. {product_name} | {product_discount_rate} | {product_price} | {product_arrival_time} | {product_rating_star} | {product_review} | \n{product_link} | \n{product_image}\n')
        count = count + 1

    # -----------------------------------------------------------------------
    # 쿠팡파트너스 API 를 사용한 링크 생성 방법
    # -----------------------------------------------------------------------

    REQUEST_METHOD = "POST"
    DOMAIN = "https://api-gateway.coupang.com"
    URL = "/v2/providers/affiliate_open_api/apis/openapi/v1/deeplink"

    # Replace with your own ACCESS_KEY and SECRET_KEY
    COUPANG_ACCESS_KEY = coupang_access_key
    COUPANG_SECRET_KEY = coupang_secret_key

    print('쿠팡 파트너스 API 한도(제한) 때문에 쿠팡 링크의 변환은 다소 시간이 걸릴 수 있습니다. 현재는 10초 간격으로 요청을 합니다.')
    for idx, i in enumerate(product_link_lists[:pin_number_per_keyword]):
        coupang_link = i  # 쿠팡링크
        REQUEST = {"coupangUrls": [coupang_link]}  # 해당 쿠팡링크 받기

        def generateHmac(method, url, api_secret_key, api_access_key):
            path, *query = url.split('?')
            os.environ['TZ'] = 'GMT+0'
            dt_datetime = strftime('%y%m%d', gmtime()) + 'T' + \
                          strftime('%H%M%S', gmtime()) + 'Z'  # GMT+0
            msg = dt_datetime + method + path + (query[0] if query else '')
            signature = hmac.new(bytes(api_secret_key, 'utf-8'),
                                 msg.encode('utf-8'), hashlib.sha256).hexdigest()

            return 'CEA algorithm=HmacSHA256, access-key={}, signed-date={}, signature={}'.format(api_access_key,
                                                                                                  dt_datetime,
                                                                                                  signature)

        authorization = generateHmac(
            REQUEST_METHOD, URL, COUPANG_SECRET_KEY, COUPANG_ACCESS_KEY)
        url = "{}{}".format(DOMAIN, URL)
        response = requests.request(method=REQUEST_METHOD, url=url,
                                    headers={
                                        "Authorization": authorization,
                                        "Content-Type": "application/json"
                                    },
                                    data=json.dumps(REQUEST)
                                    )

        # print(response.json())  #확인
        if idx != 0:
            time.sleep(5)  # 10초마다 한번씩 (쿠팡 제약 때문)
            # - 검색 API: 1시간당 10회
            # - 리포트 API: 1시간당 50회
            # - 모든 API: 1분당 100회
            # - 파트너스 웹의 링크생성 기능: 1분당 50회44

        text = response.json()
        # print(text)
        try:
            text_2 = text['data']
            print(f'{idx + 1}. {text_2}')
        except:
            # 없을시 가짜 리스트 생성
            text_2 = ['https://www.coupang.com/np/coupangglobal']
            # print('except(1) - 가짜 링크 생성')
        for i in text_2:
            try:
                product_short_url = i['shortenUrl']
            except:
                product_short_url = fake_coupang_link  # 가짜 링크 집어넣기
                # print('except(2) - 가짜 링크 생성')
            print(product_short_url)  # 확인
            product_short_url_lists.append(product_short_url)

    print("\n최종 쿠팡 파트너스 숏 링크가 생성 되었습니다.")  # 최종 확인

    if len(product_image_lists) < pin_number_per_keyword:
        check_next_wait_time = 1
        print('product_image_lists, out of range')
        return 0


def pinterest_write(driver, num, input_num, keyword, keyword_idx, age=None, gender=None):
    import pyautogui
    p = pyautogui.position()
    pyautogui.moveTo(p[0], p[1], 0.3)  # 화면잠김 방지를 위한 마우스 이동
    pyautogui.moveTo(p[0], p[1] + 30, 0.3)
    pyautogui.moveTo(p[0], p[1], 0.3)
    if input_num == '2':
        csv_path = f'{keyword_list_csv_path.replace(".csv", "_naverbook.csv")}'
    elif input_num == '3':
        csv_path = f'{keyword_list_csv_path.replace(".csv", "_naverlab.csv")}'
    else:
        csv_path = f'{keyword_list_csv_path.replace(".csv", "_itemscout.csv")}'

    if keyword_idx is not None:
        df = pd.read_csv(csv_path)

        if len(df) == 0:
            print(f'\n포스팅할 keyword가 존재하지 않습니다. ({csv_path}) 에 포스팅할 keyword가 존재해야 합니다.')
            return

    # 글 제목 구성
    if input_num == '3':  # 검색을 통한 발행이 아니라 datalab 에 의한 랜덤한 내용이라면,
        if gender == 'f,m':
            if age == '10,20,30,40,50,60':
                post_title = '[전연령][남녀] ' + product_name_lists[num][:69]
            else:
                post_title = '[' + str(age) + '대][남녀] ' + \
                             product_name_lists[num][:69]
        elif gender == 'f':
            if age == '10,20,30,40,50,60':
                post_title = '[전연령][여성] ' + product_name_lists[num][:69]
            else:
                post_title = '[' + str(age) + '대][여성] ' + \
                             product_name_lists[num][:69]
        else:
            if age == '10,20,30,40,50,60':
                post_title = '[전연령][남성] ' + product_name_lists[num][:69]
            else:
                post_title = '[' + str(age) + '대][남성] ' + \
                             product_name_lists[num][:69]
    elif input_num == '4':
        if gender == 'f,m':
            if age == '10,10':
                post_title = '[10대][남녀] ' + product_name_lists[num][:69]
            elif age == '20,20':
                post_title = '[20대][남녀] ' + product_name_lists[num][:69]
            elif age == '30,30':
                post_title = '[30대][남녀] ' + product_name_lists[num][:69]
            elif age == '40,40':
                post_title = '[40대][남녀] ' + product_name_lists[num][:69]
            elif age == '50,50':
                post_title = '[50대][남녀] ' + product_name_lists[num][:69]
            elif age == '60,60':
                post_title = '[60대][남녀] ' + product_name_lists[num][:69]
            else:
                post_title = f'[{str(age.split(",")[0])}~{str(age.split(",")[1])}대] ' + \
                             product_name_lists[num][:69]
        elif gender == 'f':
            if age == '10,10':
                post_title = '[10대][여성] ' + product_name_lists[num][:69]
            elif age == '20,20':
                post_title = '[20대][여성] ' + product_name_lists[num][:69]
            elif age == '30,30':
                post_title = '[30대][여성] ' + product_name_lists[num][:69]
            elif age == '40,40':
                post_title = '[40대][여성] ' + product_name_lists[num][:69]
            elif age == '50,50':
                post_title = '[50대][여성] ' + product_name_lists[num][:69]
            elif age == '60,60':
                post_title = '[60대][여성] ' + product_name_lists[num][:69]
            else:
                post_title = f'[{str(age.split(",")[0])}~{str(age.split(",")[1])}대][여성] ' + \
                             product_name_lists[num][:69]
        else:
            if age == '10,10':
                post_title = '[10대][남성] ' + product_name_lists[num][:69]
            elif age == '20,20':
                post_title = '[20대][남성] ' + product_name_lists[num][:69]
            elif age == '30,30':
                post_title = '[30대][남성] ' + product_name_lists[num][:69]
            elif age == '40,40':
                post_title = '[40대][남성] ' + product_name_lists[num][:69]
            elif age == '50,50':
                post_title = '[50대][남성] ' + product_name_lists[num][:69]
            elif age == '60,60':
                post_title = '[60대][남성] ' + product_name_lists[num][:69]
            else:
                post_title = f'[{str(age.split(",")[0])}~{str(age.split(",")[1])}대][남성] ' + \
                             product_name_lists[num][:69]
    else:  # 검색을 통한 발행 또는 네이버쇼핑 도서정보에 대한 내용이라면,
        post_title = product_name_lists[num][:69]

    if input_num == '2':
        title = f'[{keyword.replace(" 책 도서", "")}] 도서 추천 - {post_title}'  # 글의 제목
    else:
        title = f'[{keyword}] 추천 - {post_title}'  # 글의 제목

    # if input_num == '2':
    #     description = f'본 상품 키워드({keyword})는 네이버 쇼핑 도서 정보 데이터 조합으로 선정하고 있으며, 인기/추천 상품 리스트 TOP을 추천해 드리고 있습니다.'
    # elif input_num == '3' or input_num == '4':
    #     description = f'본 상품 키워드({keyword})는 네이버 데이터랩(naver datalab) 또는 아이템 스카우트(item scoute)의 데이터 조합으로 선정하고 있으며, 인기/추천 상품 리스트 TOP을 추천해 드리고 있습니다.'
    # else:
    #     description = f'본 상품 키워드({keyword})는 본인이 직접 검색을 통해 정한 키워드이며, 인기/추천 상품 리스트 TOP을 추천해 드리고 있습니다.'

    # 업로드에 사용할 이미지를 로컬에 저장
    print(f'\n(1) 업로드에 사용할 이미지를 로컬에 저장')
    # 이미지 저장할때 사이즈 키워서 저장 600x600 으론
    # image_url = 'https://thumbnail6.coupangcdn.com/thumbnails/remote/600x600ex/image/retail/images/1073670027066547-a36aed12-0f7d-450b-a759-b3b5f2afd513.jpg'
    image_url = product_image_lists[num].replace('230x230', '600x600')
    image_file_name = f'temp.png'
    with urlopen(image_url) as f:
        with open(local_image_path + image_file_name, 'wb') as h:
            img = f.read()  # 이미지 읽기
            h.write(img)  # 이미지 저장

    if watermark:
        # import autoit
        # 파일에 워터마크 넣음
        # 이미지 합치기 - https://blog.naver.com/PostView.naver?blogId=yh_park02&logNo=222493743987&parentCategoryNo=&categoryNo=53&viewDate=&isShowPopularPosts=true&from=search
        background_image = Image.open(local_image_path + image_file_name)
        foreground_image = Image.open(local_image_path + watermark_file_name)

        (back_img_h, back_img_w) = background_image.size
        print(background_image.size)
        print("back_img_h : ", back_img_h, "back_img_w : ", back_img_w)
        (fore_img_h, fore_img_w) = foreground_image.size
        print(foreground_image.size)
        print("fore_img_h : ", fore_img_h, "fore_img_w : ", fore_img_w)

        # 이미지 합성
        background_image.paste(foreground_image, (0, 0), foreground_image)
        # background_image.show()  # 합성한 이미지 몇 초 보여주기

        # 이미지 저장
        saves = local_image_path + image_file_name
        print(f"{saves}, {background_image}")
        background_image.save(saves)

    driver.get('https://www.pinterest.co.kr/pin-creation-tool/')
    # driver.refresh()
    sleep(LOADING_WAIT_TIME)

    # 내 텍스처 파일 업로드 및 window 파일 탐색창 처리(파일 선택)
    print(f'(2) 내 텍스처 파일 업로드 및 window 파일 탐색창 처리(파일 선택)')
    sleep(PAUSE_TIME)
    driver.find_element(By.XPATH,
                        '//*[@id="__PWS_ROOT__"]/div/div[1]/div/div[2]/div/div/div/div[2]/div[3]/div/div/div[3]/div/div/div[1]/div/div[1]/div').click()


    # ​​driver.find_element(By.XPATH, imgup).send_keys(save_path) # from 셀렉스
    
    # ------------------------------------------------
    # autoit 을 사용한 방법
    # ------------------------------------------------
    # sleep(2)
    # handle = "[CLASS:#32770; TITLE:열기]"  # Basic Window info 값 handle 변수에 저장
    # autoit.win_wait_active("열기", 3)  # 이름이 '열기'인 창이 나올 때까지 3초간 대기
    # img_path = local_image_path + image_file_name
    # sleep(3)
    # autoit.control_send(handle, "Edit1", img_path)  # 사진 클릭시 나오는 윈도우 창에서 파일이름(N)에 이미지 경로값 전달
    # sleep(1)
    # autoit.control_click(handle, "Button1")  # 사진 클릭시 나오는 윈도우 창에서 Button1 클릭
    # print(f'image uploading... ')
    # sleep(8)  # 이미지 업로드 시간이 필요

    # ------------------------------------------------
    # pyautogui 을 사용한 방법
    # ------------------------------------------------
    import pyautogui

    sleep(1)
    img_path = local_image_path + image_file_name
    pyperclip.copy(img_path)
    pyautogui.sleep(0.5)
    pyautogui.hotkey("ctrl", "v")  # 이건 딴데 클릭하면 안되는 단점
    pyautogui.sleep(0.5)
    pyautogui.press('enter')
    print(f'image uploading... ')
    sleep(10)  # 이미지 업로드 시간이 필요

    # ------------------------------------------------
    # pywinauto 을 사용한 방법
    # ------------------------------------------------
    # # 출처: https://inpa.tistory.com/entry/pywinauto-%E2%9A%A1-%EC%9C%88%EB%8F%84%EC%9A%B0-%ED%94%84%EB%A1%9C%EA%B7%B8%EB%9E%A8-%ED%85%8C%EC%8A%A4%ED%8A%B8-%EC%9E%90%EB%8F%99%ED%99%94-%EC%82%AC%EC%9A%A9%EB%B2%95
    # # https://freesugar.tistory.com/46
    # # https://ayoteralab.tistory.com/entry/python%EC%9D%84-%ED%86%B5%ED%95%9C-%EB%8B%A8%EC%88%9C-%EC%9E%91%EC%97%85-%EC%9E%90%EB%8F%99%ED%99%94-%EA%B5%AC%ED%98%84-RPA%EC%9D%98-%EC%8B%9C%EC%9E%91
    # from pywinauto import findwindows
    # from pywinauto import application
    #
    # procs = findwindows.find_elements()
    #
    # # pywinauto 는 윈도우 소프트웨어의 셀레니움이라 보시면 됨
    # # 테스트할 프로그램 이름 얻기
    # for proc in procs:
    #     print(f"{proc} / 프로세스 : {proc.process_id}")  # 열기 578664
    # sleep(2)
    #
    # # 테스트할 프로그램 실행 / 연결
    # # Application().start() : 프로그램 경로를 넣어서 실행
    # # Application().connect() : 이미 실행되고 있는 프로그램을 연결
    # # Application(backend="win32") : 메모장과 같은 old한 프로그램을 실행할때
    # # Application(backend="uia") : 최신 기술이 사용된 프로그램 (왠만한 요즘 프로그램들이 속함)
    #
    # # app = application.Application(backend='uia')
    # app = application.Application(backend='win32')
    # # app.connect(process=578664)
    # app.connect(title="열기")
    # # app.connect(title_re="열기")  # 정규식으로
    #
    # dig = app['열기']  # 변수에 열기 어플리케이션 객체를 할당
    # dig.print_control_identifiers()  # 열기의 컨트롤 요소를 트리로 모두 출력
    # # print(app.window(title_re="열기").print_control_identifiers())
    #
    # ctrl = dig['Edit']
    # dig.set_focus()
    # ctrl.click_input()
    # img_path = local_image_path + image_file_name
    # ctrl.type_keys(img_path)
    #
    # # 열기 버튼 클릭
    # try:
    #     dig.Button1.click()
    # except:
    #     print(Exception)
    #     exit()
    # print(f'image uploading... ')
    # sleep(8)  # 이미지 업로드 시간이 필요
    # ------------------------------------------------
    #
    # ------------------------------------------------

    # 제목 추가
    print(f'(3) 제목추가')
    ele = driver.find_element(By.ID, 'storyboard-selector-title')
    ele.send_keys(title)

    # 설명 추가
    print(f'(4) 설명추가')
    action = ActionChains(driver)
    action.key_down(Keys.TAB).perform()
    message = f'▶ 할인율과 원래가격: {product_discount_rate_lists[num]}\n' \
              f'▶ 가격: {product_price_lists[num]}\n' \
              f'▶ star 평가: {product_rating_star_lists[num]}\n' \
              f'▶ 리뷰수: {product_review_lists[num]}\n' \
              f'💦 본 상품 키워드({keyword})는 네이버 데이터랩(naver datalab)과 아이템 스카우트(item scoute)의 데이터 조합으로 선정(성별, 연령, 카테고리별)하고 있으며, 인기/추천 상품 리스트들을 추천해 드리고 있습니다.\n\n' \
              f'💦 자세한 내용을 살펴보시려면 링크를 통해 정보를 더 얻으세요.\n' \
              f'💦 파트너스 활동을 통해 일정액의 수수료를 제공받을 수 있습니다.'
    pyperclip.copy(message)
    action.key_down(Keys.CONTROL).send_keys('v').perform()
    sleep(PAUSE_TIME)

    # 링크 추가
    print(f'(5) 링크추가')
    driver.find_element(By.ID, 'WebsiteField').click()
    # message = 'https://link.coupang.com/re/AFFSDP?lptag=AF5108917&subid=wpmycafe24ree31206&pageKey=7643957281&traceid=V0-153&itemId=20319562019&vendorItemId=87405012680'
    message = product_short_url_lists[num]
    pyperclip.copy(message)
    action.key_down(Keys.CONTROL).send_keys('v').perform()
    sleep(PAUSE_TIME)

    # 보드선택
    print(f'(6) 보드선택')
    driver.find_element(By.XPATH, '//*[@id="__PWS_ROOT__"]/div/div[1]/div/div[2]/div/div/div/div[2]/div[3]/div/div/div[3]/div/div/div[2]/div/div/div[1]/div[3]/div/div[2]/div/div[2]/div/div/button').click()
    driver.find_element(By.XPATH, '//*[@id="__PWS_ROOT__"]/div/div[1]/div/div[2]/div/div/div/div[2]/div[3]/div/div/div[3]/div/div/div[2]/div/div/div[1]/div[3]/div/div[2]/div/div[2]/div/div[2]/div/div/div/div/div/div/div/div/div[2]/div[2]/div').click()
    sleep(PAUSE_TIME)

    # 게시
    print(f'(7) 게시... DONE')
    driver.find_element(By.XPATH,
                        '//*[@id="__PWS_ROOT__"]/div/div[1]/div/div[2]/div/div/div/div[2]/div[3]/div/div/div[2]/div[4]/div[2]/div').click()
    sleep(10)

    if keyword_idx is not None and num == pin_number_per_keyword - 1:
        print(
            f'\nexcel 에 해당 키워드({keyword})는 ({pin_number_per_keyword})개의 상품정보를 PIN 하여 해당 키워드는 완료됨을 표시하는 "O"로 표시 하겠습니다.')
        df["posted"].values[keyword_idx] = 'O'
        df.to_csv(csv_path, mode='w', sep=',', na_rep='NaN', encoding='utf-8-sig', index=False)
    else:
        print(f'\n키워드({keyword})를 사용하여 현재 ({num + 1})/({pin_number_per_keyword})개의 상품정보를 PIN 완료하였습니다.')


# main start
if __name__ == '__main__':
    try:
        print("\nSTART...")
        start_time = time.time()  # 시작 시간 체크
        now = datetime.now()
        print("START TIME : ", now.strftime('%Y-%m-%d %H:%M:%S'))

        print('\n' + C_BOLD + C_YELLOW + C_BGBLACK + '[크롬 드라이버 초기화 시작]', C_END)
        driver = init_driver()
        sleep(PAUSE_TIME)
        print('\n' + C_BOLD + C_YELLOW + C_BGBLACK + '[크롬 드라이버 초기화 완료]', C_END)

        print('\n' + C_BOLD + C_YELLOW + C_BGBLACK + '[핀터레스트 로그인 시작]', C_END)
        pinterest_login(driver)
        sleep(PAUSE_TIME)
        print('\n' + C_BOLD + C_YELLOW + C_BGBLACK + '[핀터레스트 로그인 완료]', C_END)
        driver.close()
        driver.quit()

        while True:
            # partner info
            product_name_lists = []  # 상품명
            product_discount_rate_lists = []  # 할인률과 원래가격
            product_price_lists = []  # 상품가격
            product_arrival_time_lists = []  # 도착예정시간
            product_rating_star_lists = []  # star 평가: ex.3.5
            product_review_lists = []  # 상품리뷰 수
            product_link_lists = []  # 상품 구매 링크
            product_image_lists = []  # 상품 이미지

            product_short_url_lists = []  # 쿠팡 숏 링크 리스트

            print('검색을 통해 파트너 url얻기 원하시면' + C_BOLD +
                  C_RED + '(1)' + C_END + '를 눌러주시고,')
            print('NAVER 도서에서 정보를 가져와 파트너 url을 얻기 원하신다면' +
                  C_BOLD + C_RED + '(2)' + C_END + '를 눌러주세요')
            print('NAVER 데이터랩스에서 추천하는 상품에 대한 파트너 url을 얻기 원하신다면' +
                  C_BOLD + C_RED + '(3)' + C_END + '를 눌러주세요')
            print('아이템스카우트에서 추천하는 상품에 대한 파트너 url을 얻기 원하신다면' +
                  C_BOLD + C_RED + '(4)' + C_END + '를 눌러주세요')
            print('프로그램을 종료하고 싶으면' + C_BOLD +
                  C_RED + '(q)' + C_END + '를 눌러주세요')
            input_num = input('원하는 번호를 입력하세요 : ')

            if input_num == 'q':
                break

            if input_num == '1':
                print('입력하신 키는 1 입니다...\n')
                sleep(2)
                query = input('검색 키워드를 입력하세요 : ')
                query = query.replace(' ', '+')

                # partner info
                product_name_lists = []  # 상품명
                product_discount_rate_lists = []  # 할인률과 원래가격
                product_price_lists = []  # 상품가격
                product_arrival_time_lists = []  # 도착예정시간
                product_rating_star_lists = []  # star 평가: ex.3.5
                product_review_lists = []  # 상품리뷰 수
                product_link_lists = []  # 상품 구매 링크
                product_image_lists = []  # 상품 이미지

                product_short_url_lists = []  # 쿠팡 숏 링크 리스트

                print('\n' + C_BOLD + C_YELLOW +
                      C_BGBLACK + '[파트너 링크 생성 시작]', C_END)
                ret = partner_coupang(query)
                if ret == 0:
                    continue
                print('\n' + C_BOLD + C_YELLOW +
                      C_BGBLACK + '[파트너 링크 생성 완료]', C_END)

                print('\n' + C_BOLD + C_YELLOW + C_BGBLACK +
                      f'[pinterest 자동 업로드 시작(keyword 당 ({pin_number_per_keyword})개의 상품)]', C_END)
                for idx in range(len(product_short_url_lists)):
                    print('\n' + C_BOLD + C_YELLOW + C_BGBLACK + '[크롬 드라이버 초기화 시작]', C_END)
                    driver = init_driver()
                    sleep(PAUSE_TIME)
                    print('\n' + C_BOLD + C_YELLOW + C_BGBLACK + '[크롬 드라이버 초기화 완료]', C_END)
                    pinterest_write(driver, idx, input_num, query, None, None, None)
                    sleep(5)
                    driver.close()
                    driver.quit()
                    if idx != len(product_short_url_lists) - 1:
                        now = datetime.now()
                        future_time = now + timedelta(seconds=WRITE_PINTEREST_WAITTIME)
                        print("\n현재 시간:", now.strftime("%Y-%m-%d %H:%M:%S"))
                        print(f"({WRITE_PINTEREST_WAITTIME})초 후의 다음 발행시간:", future_time.strftime("%Y-%m-%d %H:%M:%S"))
                        sleep(WRITE_PINTEREST_WAITTIME)
                print('\n' + C_BOLD + C_YELLOW + C_BGBLACK +
                      '[pinterest 자동 업로드 완료]', C_END)

            elif input_num == '2':
                print('입력하신 키는 2 입니다...\n')
                sleep(2)

                print('\n' + C_BOLD + C_YELLOW + C_BGBLACK + '[네이버 shopping 도서 정보 가져오기 시작(keyword 추출)]', C_END)
                # global datalab_info_keyword_lists
                keyword_name_lists = []
                get_naver_shopping_book()
                sleep(PAUSE_TIME)
                print('\n' + C_BOLD + C_YELLOW + C_BGBLACK + '[네이버 shopping 도서 정보 가져오기 완료(keyword 추출)]', C_END)

                keyword_df = pd.DataFrame()
                if not os.path.exists(f'{keyword_list_csv_path.replace(".csv", "_naverbook.csv")}'):
                    print(f'({keyword_list_csv_path.replace(".csv", "_naverbook.csv")}) csv 파일이 존재하지 않습니다.')
                else:
                    keyword_df = pd.read_csv(f'{keyword_list_csv_path.replace(".csv", "_naverbook.csv")}')

                for keyword_idx in range(0, len(keyword_df)):
                    keyword = keyword_df["keyword"].values[keyword_idx]
                    if keyword_df["posted"].values[keyword_idx] == 'O':
                        print(f'[SKIP] 해당 ({keyword_df["keyword"].values[keyword_idx]})은 이미 포스팅을 한 키워드입니다.')
                        continue

                    # partner info
                    product_name_lists = []  # 상품명
                    product_discount_rate_lists = []  # 할인률과 원래가격
                    product_price_lists = []  # 상품가격
                    product_arrival_time_lists = []  # 도착예정시간
                    product_rating_star_lists = []  # star 평가: ex.3.5
                    product_review_lists = []  # 상품리뷰 수
                    product_link_lists = []  # 상품 구매 링크
                    product_image_lists = []  # 상품 이미지

                    product_short_url_lists = []  # 쿠팡 숏 링크 리스트

                    if keyword_idx == 0 or check_next_wait_time == 1:
                        now = datetime.now()
                        future_time = now + timedelta(seconds=NEXT_KEYWORD_SEARCH_TIME)
                        print("\n현재 시간:", now.strftime("%Y-%m-%d %H:%M:%S"))
                        check_next_wait_time = 0
                        pass
                    else:
                        now = datetime.now()
                        future_time = now + timedelta(seconds=NEXT_KEYWORD_SEARCH_TIME)
                        print("\n현재 시간:", now.strftime("%Y-%m-%d %H:%M:%S"))
                        print(f"({NEXT_KEYWORD_SEARCH_TIME})초 후의 다음 발행시간:",
                              future_time.strftime("%Y-%m-%d %H:%M:%S"))
                        sleep(NEXT_KEYWORD_SEARCH_TIME)

                        check_next_wait_time = 0

                    print('\n' + C_BOLD + C_YELLOW +
                          C_BGBLACK + '[파트너 링크 생성 시작]', C_END)
                    print(
                        f'{C_BOLD}{C_YELLOW}{C_BGBLACK}파트너 검색 상품 : [{keyword_idx + 1}] {keyword} {C_END}')
                    ret = partner_coupang(keyword)
                    if ret == 0:
                        continue
                    print('\n' + C_BOLD + C_YELLOW +
                          C_BGBLACK + '[파트너 링크 생성 완료]', C_END)

                    print(
                        '\n' + C_BOLD + C_YELLOW + C_BGBLACK + f'[pinterest 자동 업로드 시작(keyword 당 ({pin_number_per_keyword})개의 상품)]',
                        C_END)
                    idx = 0
                    while True:
                        if idx == pin_number_per_keyword:
                            break
                        else:
                            print(f'\n키워드({keyword})를 사용하여 현재 ({idx + 1})/({pin_number_per_keyword})개의 상품정보를 PIN 시작합니다...')
                        try:
                            print('\n' + C_BOLD + C_YELLOW + C_BGBLACK + '[크롬 드라이버 초기화 시작]', C_END)
                            driver = init_driver()
                            sleep(PAUSE_TIME)
                            print('\n' + C_BOLD + C_YELLOW + C_BGBLACK + '[크롬 드라이버 초기화 완료]', C_END)
                            pinterest_write(driver, idx, input_num, keyword, keyword_idx, None, None)
                            sleep(5)
                            driver.close()
                            driver.quit()
                            if idx != len(product_short_url_lists) - 1:
                                now = datetime.now()
                                future_time = now + timedelta(seconds=WRITE_PINTEREST_WAITTIME)
                                print("\n현재 시간:", now.strftime("%Y-%m-%d %H:%M:%S"))
                                print(f"({WRITE_PINTEREST_WAITTIME})초 후의 다음 발행시간:",
                                      future_time.strftime("%Y-%m-%d %H:%M:%S"))
                                sleep(WRITE_PINTEREST_WAITTIME)
                            idx = idx + 1
                        except:
                            print("\nUNKNOW ERROR or CONNECTIONTIMEOUT ERROR")
                            print("[주의] 해당 프로그램이 수행될때는 절전모드로의 진입이나 디스플레이 꺼짐등에 오동작 할 수 있습니다.")
                            print("[주의] 윈도우 창이 떠서 이미지 삽입 작업이 있을때나 제목등의 작성중일때는 컨트롤하지 말아주세요.")
                            print("[주의] 초안이 50개가 넘어가 문제가 계속 발생할 수 있습니다. 초안을 삭제해 주세요")
                            print("[알람] 아래의 시간에 다시금 시도해 보겠습니다.")
                            driver.close()
                            driver.quit()
                            future_time = now + timedelta(seconds=NEXT_TRY_ISSUE_OCCURE)
                            print("\n현재 시간:", now.strftime("%Y-%m-%d %H:%M:%S"))
                            print(f"({NEXT_TRY_ISSUE_OCCURE})초 후에 다시 시작:",
                                  future_time.strftime("%Y-%m-%d %H:%M:%S"))
                            sleep(NEXT_TRY_ISSUE_OCCURE)
                            # pyautogui.moveTo(2939, 533, 2)  # 화면잠김 방지를 위한 마우스 이동
                            # pyautogui.moveTo(2624, 950, 2)
                            # pyautogui.moveTo(2939, 533, 2)
                    print('\n' + C_BOLD + C_YELLOW + C_BGBLACK +
                          '[pinterest 자동 업로드 완료]', C_END)

            elif input_num == '3':
                print('입력하신 키는 3 입니다...\n')
                sleep(2)

                today = date.today()
                before_one_month = today - timedelta(days=30)
                start_date = before_one_month
                # 어제 날짜: 오늘 - 1일
                yesterday = today - timedelta(days=1)
                end_date = yesterday

                count = 1
                for cid, age, gender in random_naverdatalab_input_info_list:
                    print('\n' + C_BOLD + C_YELLOW +
                          C_BGBLACK + 'count : ', count, C_END)
                    print(
                        f'{C_BOLD}{C_YELLOW}{C_BGBLACK}RANDOM info >>> cid {cid} | start_date {start_date} | endDate {end_date} | age {age} | gender {gender} {C_END}')

                    print('\n' + C_BOLD + C_YELLOW + C_BGBLACK + '[네이버 데이터랩스 정보 가져오기 시작(keyword 추출)]', C_END)
                    # global keyword_name_lists
                    keyword_name_lists = []
                    get_naver_datalab_shopping_insight(cid, start_date, end_date, age, gender)
                    sleep(PAUSE_TIME)
                    print('\n' + C_BOLD + C_YELLOW + C_BGBLACK + '[네이버 데이터랩스 정보 가져오기 완료(keyword 추출)]', C_END)

                    keyword_df = pd.DataFrame()
                    if not os.path.exists(f'{keyword_list_csv_path.replace(".csv", "_naverlab.csv")}'):
                        print(f'({keyword_list_csv_path.replace(".csv", "_naverlab.csv")}) csv 파일이 존재하지 않습니다.')
                    else:
                        keyword_df = pd.read_csv(f'{keyword_list_csv_path.replace(".csv", "_naverlab.csv")}')

                    for keyword_idx in range(0, len(keyword_df)):
                        keyword = keyword_df["keyword"].values[keyword_idx]
                        if keyword_df["posted"].values[keyword_idx] == 'O':
                            print(f'[SKIP] 해당 ({keyword_df["keyword"].values[keyword_idx]})은 이미 포스팅을 한 키워드입니다.')
                            continue

                        # partner info
                        product_name_lists = []  # 상품명
                        product_discount_rate_lists = []  # 할인률과 원래가격
                        product_price_lists = []  # 상품가격
                        product_arrival_time_lists = []  # 도착예정시간
                        product_rating_star_lists = []  # star 평가: ex.3.5
                        product_review_lists = []  # 상품리뷰 수
                        product_link_lists = []  # 상품 구매 링크
                        product_image_lists = []  # 상품 이미지

                        product_short_url_lists = []  # 쿠팡 숏 링크 리스트

                        if keyword_idx == 0 or check_next_wait_time == 1:
                            now = datetime.now()
                            future_time = now + timedelta(seconds=NEXT_KEYWORD_SEARCH_TIME)
                            print("\n현재 시간:", now.strftime("%Y-%m-%d %H:%M:%S"))
                            check_next_wait_time = 0
                            pass
                        else:
                            now = datetime.now()
                            future_time = now + timedelta(seconds=NEXT_KEYWORD_SEARCH_TIME)
                            print("\n현재 시간:", now.strftime("%Y-%m-%d %H:%M:%S"))
                            print(f"({NEXT_KEYWORD_SEARCH_TIME})초 후의 다음 발행시간:",
                                  future_time.strftime("%Y-%m-%d %H:%M:%S"))
                            sleep(NEXT_KEYWORD_SEARCH_TIME)

                            check_next_wait_time = 0

                        print('\n' + C_BOLD + C_YELLOW +
                              C_BGBLACK + '[파트너 링크 생성 시작]', C_END)
                        print(
                            f'{C_BOLD}{C_YELLOW}{C_BGBLACK}파트너 검색 상품 : [{keyword_idx + 1}] {keyword} {C_END}')
                        ret = partner_coupang(keyword)
                        if ret == 0:
                            continue
                        print('\n' + C_BOLD + C_YELLOW +
                              C_BGBLACK + '[파트너 링크 생성 완료]', C_END)

                        print('\n' + C_BOLD + C_YELLOW + C_BGBLACK +
                              f'[pinterest 자동 업로드 시작(keyword 당 ({pin_number_per_keyword})개의 상품)]', C_END)

                        try:
                            for idx in range(len(product_short_url_lists)):
                                if idx == pin_number_per_keyword:
                                    break
                                else:
                                    print(f'\n키워드({keyword})를 사용하여 현재 ({idx + 1})/({pin_number_per_keyword})개의 상품정보를 PIN 시작합니다...')
                                print('\n' + C_BOLD + C_YELLOW + C_BGBLACK + '[크롬 드라이버 초기화 시작]', C_END)
                                driver = init_driver()
                                sleep(PAUSE_TIME)
                                print('\n' + C_BOLD + C_YELLOW + C_BGBLACK + '[크롬 드라이버 초기화 완료]', C_END)
                                pinterest_write(driver, idx, input_num, keyword, keyword_idx, age, gender)
                                sleep(5)
                                driver.close()
                                driver.quit()
                                if idx != len(product_short_url_lists) - 1:
                                    now = datetime.now()
                                    future_time = now + timedelta(seconds=WRITE_PINTEREST_WAITTIME)
                                    print("\n현재 시간:", now.strftime("%Y-%m-%d %H:%M:%S"))
                                    print(f"({WRITE_PINTEREST_WAITTIME})초 후의 다음 발행시간:",
                                          future_time.strftime("%Y-%m-%d %H:%M:%S"))
                                    sleep(WRITE_PINTEREST_WAITTIME)
                        except:
                            print("\nUNKNOW ERROR or CONNECTIONTIMEOUT ERROR")
                            print("[주의] 해당 프로그램이 수행될때는 절전모드로의 진입이나 디스플레이 꺼짐등에 오동작 할 수 있습니다.")
                            print("[주의] 윈도우 창이 떠서 이미지 삽입 작업이 있을때나 제목등의 작성중일때는 컨트롤하지 말아주세요.")
                            print("[주의] 초안이 50개가 넘어가 문제가 계속 발생할 수 있습니다. 초안을 삭제해 주세요")
                            print("[알람] 아래의 시간에 다시금 시도해 보겠습니다.")
                            driver.close()
                            driver.quit()
                            future_time = now + timedelta(seconds=NEXT_TRY_ISSUE_OCCURE)
                            print("\n현재 시간:", now.strftime("%Y-%m-%d %H:%M:%S"))
                            print(f"({NEXT_TRY_ISSUE_OCCURE})초 후에 다시 시작:",
                                  future_time.strftime("%Y-%m-%d %H:%M:%S"))
                            sleep(NEXT_TRY_ISSUE_OCCURE)
                            # pyautogui.moveTo(2939, 533, 2)  # 화면잠김 방지를 위한 마우스 이동
                            # pyautogui.moveTo(2624, 950, 2)
                            # pyautogui.moveTo(2939, 533, 2)
                        print('\n' + C_BOLD + C_YELLOW + C_BGBLACK +
                              '[pinterest 자동 업로드 완료]', C_END)

                count = count + 1

            elif input_num == '4':
                print('입력하신 키는 4 입니다...\n')
                sleep(2)

                count = 1
                for cid, age, gender in random_itemscout_input_info_list:
                    print('\n' + C_BOLD + C_YELLOW +
                          C_BGBLACK + 'count : ', count, C_END)

                    # 아이템스카우트 기간
                    duration = '30d'  # (duration 30d 또는 날짜 설정, duration: 2023-03,2023-04 3월부터 4월)

                    print(
                        f'{C_BOLD}{C_YELLOW}{C_BGBLACK}RANDOM info >>> cid {cid} | duration {duration} | age {age} | gender {gender} {C_END}')

                    print(f'\n{C_BOLD}{C_YELLOW}{C_BGBLACK}[itemscout 에서 아이템들 리스트를 전체 받기 시작]{C_END}')
                    get_items_for_itemscout(cid, duration, age, gender)
                    sleep(PAUSE_TIME)
                    print(f'\n{C_BOLD}{C_YELLOW}{C_BGBLACK}[itemscout 에서 아이템들 리스트를 전체 받기 완료]{C_END}')

                    # count = 0  # 처음에는 대기 시간을 가지지 않도록 함
                    keyword_df = pd.DataFrame()
                    if not os.path.exists(f'{keyword_list_csv_path.replace(".csv", "_itemscout.csv")}'):
                        print(f'({keyword_list_csv_path.replace(".csv", "_itemscout.csv")}) csv 파일이 존재하지 않습니다.')
                    else:
                        keyword_df = pd.read_csv(f'{keyword_list_csv_path.replace(".csv", "_itemscout.csv")}')

                    # print("키워드 데이터 >>> ", keyword_name_lists)
                    for keyword_idx in range(0, len(keyword_df)):
                        keyword = keyword_df["keyword"].values[keyword_idx]
                        if keyword_df["posted"].values[keyword_idx] == 'O':
                            print(f'[SKIP] 해당 ({keyword_df["keyword"].values[keyword_idx]})은 이미 포스팅을 한 키워드입니다.')
                            continue

                        # partner info
                        product_name_lists = []  # 상품명
                        product_discount_rate_lists = []  # 할인률과 원래가격
                        product_price_lists = []  # 상품가격
                        product_arrival_time_lists = []  # 도착예정시간
                        product_rating_star_lists = []  # star 평가: ex.3.5
                        product_review_lists = []  # 상품리뷰 수
                        product_link_lists = []  # 상품 구매 링크
                        product_image_lists = []  # 상품 이미지

                        product_short_url_lists = []  # 쿠팡 숏 링크 리스트

                        if keyword_idx == 0 or check_next_wait_time == 1:
                            now = datetime.now()
                            future_time = now + timedelta(seconds=NEXT_KEYWORD_SEARCH_TIME)
                            print("\n현재 시간:", now.strftime("%Y-%m-%d %H:%M:%S"))
                            check_next_wait_time = 0
                            pass
                        else:
                            now = datetime.now()
                            future_time = now + timedelta(seconds=NEXT_KEYWORD_SEARCH_TIME)
                            print("\n현재 시간:", now.strftime("%Y-%m-%d %H:%M:%S"))
                            print(f"({NEXT_KEYWORD_SEARCH_TIME})초 후의 다음 발행시간:",
                                  future_time.strftime("%Y-%m-%d %H:%M:%S"))
                            sleep(NEXT_KEYWORD_SEARCH_TIME)

                            check_next_wait_time = 0

                        print('\n' + C_BOLD + C_YELLOW +
                              C_BGBLACK + '[파트너 링크 생성 시작]', C_END)
                        print(
                            f'{C_BOLD}{C_YELLOW}{C_BGBLACK}파트너 검색 상품 : [{keyword_idx + 1}] {keyword} {C_END}')
                        ret = partner_coupang(keyword)
                        if ret == 0:
                            continue
                        print('\n' + C_BOLD + C_YELLOW +
                              C_BGBLACK + '[파트너 링크 생성 완료]', C_END)

                        print('\n' + C_BOLD + C_YELLOW + C_BGBLACK +
                              f'[pinterest 자동 업로드 시작(keyword 당 ({pin_number_per_keyword})개의 상품)]', C_END)

                        try:
                            for idx in range(len(product_short_url_lists)):
                                if idx == pin_number_per_keyword:
                                    break
                                else:
                                    print(f'\n키워드({keyword})를 사용하여 현재 ({idx + 1})/({pin_number_per_keyword})개의 상품정보를 PIN 시작합니다...')
                                print('\n' + C_BOLD + C_YELLOW + C_BGBLACK + '[크롬 드라이버 초기화 시작]', C_END)
                                driver = init_driver()
                                sleep(PAUSE_TIME)
                                print('\n' + C_BOLD + C_YELLOW + C_BGBLACK + '[크롬 드라이버 초기화 완료]', C_END)
                                pinterest_write(driver, idx, input_num, keyword, keyword_idx, age, gender)
                                sleep(5)
                                driver.close()
                                driver.quit()
                                if idx != len(product_short_url_lists) - 1:
                                    now = datetime.now()
                                    future_time = now + timedelta(seconds=WRITE_PINTEREST_WAITTIME)
                                    print("\n현재 시간:", now.strftime("%Y-%m-%d %H:%M:%S"))
                                    print(f"({WRITE_PINTEREST_WAITTIME})초 후의 다음 발행시간:",
                                          future_time.strftime("%Y-%m-%d %H:%M:%S"))
                                    sleep(WRITE_PINTEREST_WAITTIME)
                                idx = idx + 1
                        except:
                            print("\nUNKNOW ERROR or CONNECTIONTIMEOUT ERROR")
                            print("[주의] 해당 프로그램이 수행될때는 절전모드로의 진입이나 디스플레이 꺼짐등에 오동작 할 수 있습니다.")
                            print("[주의] 윈도우 창이 떠서 이미지 삽입 작업이 있을때나 제목등의 작성중일때는 컨트롤하지 말아주세요.")
                            print("[주의] 초안이 50개가 넘어가 문제가 계속 발생할 수 있습니다. 초안을 삭제해 주세요")
                            print("[알람] 아래의 시간에 다시금 시도해 보겠습니다.")
                            driver.close()
                            driver.quit()
                            future_time = now + timedelta(seconds=NEXT_TRY_ISSUE_OCCURE)
                            print("\n현재 시간:", now.strftime("%Y-%m-%d %H:%M:%S"))
                            print(f"({NEXT_TRY_ISSUE_OCCURE})초 후에 다시 시작:",
                                  future_time.strftime("%Y-%m-%d %H:%M:%S"))
                            sleep(NEXT_TRY_ISSUE_OCCURE)
                            # pyautogui.moveTo(2939, 533, 2)  # 화면잠김 방지를 위한 마우스 이동
                            # pyautogui.moveTo(2624, 950, 2)
                            # pyautogui.moveTo(2939, 533, 2)
                        print('\n' + C_BOLD + C_YELLOW + C_BGBLACK +
                              '[pinterest 자동 업로드 완료]', C_END)

                count = count + 1

            else:
                print("잘못 입력 하였습니다. 1, 2, 3, 4, q 중에서 선택하시기 바랍니다.")
                continue

    finally:
        driver.close()  # 마지막 창을 닫기 위해서는 해당 주석 제거
        driver.quit()
        end_time = time.time()  # 종료 시간 체크
        ctime = end_time - start_time
        time_list = str(datetime.timedelta(seconds=ctime)).split(".")
        print("\n실행시간(초)", ctime)
        print("실행시간 (시:분:초)", time_list)
        print("\nEND...")
