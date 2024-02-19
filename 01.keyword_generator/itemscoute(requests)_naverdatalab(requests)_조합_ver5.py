# -*- coding: utf-8 -*-

# # 필요한 패키지들을 리스트에 저장합니다.
# import subprocess
# packages = [
#     "chromedriver-autoinstaller",
#     "openai",
#     "selenium",
#     "chardet",
#     "tabulate",
#     "emoji",
#     "requests",
#     "pyperclip",
#     "schedule",
#     "bs4"
#     "tqdm"
#     "requests"
# ]
#
# # 각 패키지를 설치합니다.
# for package in packages:
#     try:
#         # pip를 통해 패키지를 설치합니다.
#         subprocess.check_call(["C:\Users\ree31\AppData\Local\Programs\Python\Python311\python.exe -m pip", "install", package])
#         print(f"{package} installed successfully!")
#     except subprocess.CalledProcessError:
#         # 패키지 설치 실패 메시지 출력
#         print(f"Failed to install {package}.")
#     # 설치가 완료되었으면 코드블럭 아래에 설치 완료 메시지를 출력합니다.
#     print("\nAll packages installed successfully!")

import subprocess
from time import sleep
import datetime
import time
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import platform
import random
from tqdm import tqdm
from pprint import pprint as pp
from bs4 import BeautifulSoup
from datetime import timedelta
from urllib import parse
import pandas as pd
import os
from tabulate import tabulate
from itertools import product
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
import json
import ssl
import urllib3

osName = platform.system()  # window 인지 mac 인지 알아내기 위한

ssl._create_default_https_context = ssl._create_unverified_context

urllib3.disable_warnings()  # warning 메세지 안뜨게 하기

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

# [사용자 입력 정보]
# ======================================================================================================== START

# pause time 정보
PAUSE_TIME = 0.5
LOADING_WAIT_TIME = 3
LOGIN_WAIT_TIME = 180
GENERAL_REQUEST_WAIT_TIME = 0.3  # 일반적인 requests의 속도

# # fake-useragent / user-agent
# # https://domdom.tistory.com/329
# # ua = UserAgent(use_cache_server=True)
# ua = UserAgent(verify_ssl=False)
# user_agent = ua.random
# print(f'User-Agent : {user_agent}')
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15'
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15'
]
user_agent = random.choice(user_agents)
fixed_user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Whale/3.19.166.16 Safari/537.36'

csv_file_path = "info.csv"

# 추출하고자 하는 각 카테고리별 keyword 수 (네이버 max:500, 아이템스카우트 max: "아이템발굴"을 통한 500)
wanted_item_num = 500

ITEMSCOUT_CONVERSION_MAP_INFO_PATH = 'itemscout_conversion_info.json'

# [사용자 입력 정보]
# ======================================================================================================== END

# [시스템 공통 입력 정보]
# ======================================================================================================== START

# 데이터랩스 키워드 저장 리스트
datalab_info_keyword_lists = []

# 랜덤 생성 리스트
naver_cid_category_lists = []
naver_start_date_lists = []
naver_end_date_lists = []
naver_age_lists = []
naver_gender_list = []

##-------------------------------------------------------------------------------------------------------

# itemscout 에서 아이템들 대한 정보 리스트
keyword_id_lists = []  # keyword 아이디
rank_lists = []  # 랭킹
keyword_name_lists = []  # 키워드
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

# [시스템 공통 입력 정보]
# ======================================================================================================== END


def recursive_random_int_no_again(_count):
    if _count == 0:  # 카운트가 0이 되면 작동 종료
        print(random_number_list)
        return
    a = random.randint(1, 12)  # 아쉽지만 수동으로 _count 수를 넣어줌
    while a in random_number_list:
        a = random.randint(1, 12)  # 아쉽지만 수동으로 _count 수를 넣어줌
    random_number_list.append(a)
    _count -= 1  # 카운트를 - 1하고, 함수를 다시 호출 한다.
    recursive_random_int_no_again(_count)


def get_naver_datalab_shopping_insight(cid, start_date, end_date, age, gender):

    # naver 랜덤 생성 리스트
    global naver_cid_category_lists
    naver_cid_category_lists = []
    global naver_start_date_lists
    naver_start_date_lists = []
    global naver_end_date_lists
    naver_end_date_lists = []
    global naver_age_lists
    naver_age_lists = []
    global naver_gender_list
    naver_gender_list = []

    # 데이터랩스 키워드 저장 리스트
    global datalab_info_keyword_lists
    datalab_info_keyword_lists = []

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
        # pp(response.json())  # json -> dict
        items = response.json()
        # print(items['ranks'][0]['keyword'])
        # print(items['ranks'][1]['keyword'])
        # print(items['ranks'][2]['keyword'])

        for keyword_idx in range(0, len(items['ranks'])):
            naver_start_date_lists.append(start_date)
            naver_end_date_lists.append(end_date)
            naver_age_lists.append(age)
            naver_gender_list.append(gender)
            datalab_info_keyword_lists.append(items['ranks'][keyword_idx]['keyword'])

        print(f"({page_idx + 1})/({page_num}) ...")
        sleep(1)  # 꼭 0.5 초 delay를 줘야 한다. response 시간이 필요함

    print(f"\n키워드 리스트:")
    for idx, keyword in enumerate(datalab_info_keyword_lists):
        print(f"{idx + 1}. {keyword}")


def get_items_for_itemscout(cid, duration, ages, gender):

    # itemscout 랜덤 생성 리스트
    global itemscout_cid_category_lists
    itemscout_cid_category_lists = []
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

    response = requests.post(f'https://api.itemscout.io/api/category/{cid}/data', headers=headers, data=data, verify=False).json()
    # pp(response)

    for idx, item in enumerate(response['data']['data'].items()):
        if idx == wanted_item_num:
            break
        # print(f'{item}')
        # print(f"keywordID(keyword ID): {item[0]}")  # keyword 아이디
        # print(f"rank(랭킹): {item[1]['rank']}")  # 랭킹
        # print(f"keyword(키워드): {item[1]['keyword']}")  # 키워드
        # print(f"total(검색수): {item[1]['monthly']['total']}")  # 검색수
        # print(f"prdCnt(상품수): {item[1]['prdCnt']}")  # 상품수
        # try:
        #     print(f"{idx + 1}. ID {item[0]} | keyword {item[1]['keyword']} | 랭킹 {item[1]['rank']} | 검색수 {item[1]['monthly']['total']} | 상품수 {item[1]['prdCnt']}")
        # except:
        #     continue
        try:
            a = item[0]
            b = item[1]['keyword']
            c = item[1]['rank']
            d = item[1]['monthly']['total']
            e = item[1]['prdCnt']
        except:
            continue
        itemscout_duration_lists.append(duration)
        itemscout_age_lists.append(ages)
        itemscout_gender_list.append(gender)
        keyword_id_lists.append(item[0])
        rank_lists.append(item[1]['rank'])
        keyword_name_lists.append(item[1]['keyword'])
        no_of_search_total_lists.append(item[1]['monthly']['total'])
        prdCnt_lists.append(item[1]['prdCnt'])


def get_keyword_stats_for_itemscout():

    global competitionIntensity_lists
    competitionIntensity_lists = []  # 경쟁강도 수치
    global competitionIntensityDesc_lists
    competitionIntensityDesc_lists = []  # 경쟁강도 등급
    global adClickRateTotal_lists
    adClickRateTotal_lists = []  # 광고클릭률 수치
    global adClickRateTotalDesc_lists
    adClickRateTotalDesc_lists = []  # 광고클릭률 등급

    headers = {
        'accept': 'application/json, text/plain, */*',
        'origin': 'https://itemscout.io',
        'referer': 'https://itemscout.io/',
        'user-agent': fixed_user_agent,
    }

    for idx, keyword_id in enumerate(keyword_id_lists):
        response = requests.get(f'https://api.itemscout.io/api/v2/keyword/stats/{keyword_id}', headers=headers).json()
        # pp(response)
        # print(response['data']['competitionIntensity'])  # 경쟁강도 수치
        # print(response['data']['competitionIntensityDesc'])  # 경쟁강도 등급
        # print(response['data']['adClickRateStats']['adClickRateTotal'])  # 광고클릭률 수치
        # print(response['data']['adClickRateStats']['adClickRateTotalDesc'])  # 광고클릭률 등급
        # print(f"{idx + 1}. 경쟁강도({response['data']['competitionIntensityDesc']}) | 광고클릭률({response['data']['adClickRateStats']['adClickRateTotalDesc']})")
        competitionIntensity_lists.append(response['data']['competitionIntensity'])
        competitionIntensityDesc_lists.append(response['data']['competitionIntensityDesc'])
        adClickRateTotal_lists.append(response['data']['adClickRateStats']['adClickRateTotal'])
        adClickRateTotalDesc_lists.append(response['data']['adClickRateStats']['adClickRateTotalDesc'])
        sleep(GENERAL_REQUEST_WAIT_TIME)


def get_keyword_contents_competition_stats_for_itemscout():

    global blogCompetitionRatio_lists
    blogCompetitionRatio_lists = []  # 블로그 경쟁강도 수치
    global blogCompetitionDesc_lists
    blogCompetitionDesc_lists = []  # 블로그 경쟁강도 등급
    global cafeCompetitionRatio
    cafeCompetitionRatio = []  # 카페 경쟁강도 수치
    global cafeCompetitionDesc_lists
    cafeCompetitionDesc_lists = []  # 카페 경쟁강도 등급

    headers = {
        'accept': 'application/json, text/plain, */*',
        'origin': 'https://itemscout.io',
        'referer': 'https://itemscout.io/',
        'user-agent': fixed_user_agent,
    }

    for idx, keyword_id in enumerate(keyword_id_lists):
        response = requests.get(f'https://api.itemscout.io/api/v2/keyword/contents_competition_stats/{keyword_id}', headers=headers).json()
        # pp(response)
        # print(response['data']['blogCompetitionRatio'])  # 블로그 경쟁강도 수치
        # print(response['data']['blogCompetitionDesc'])  # 블로그 경쟁강도 등급
        # print(response['data']['cafeCompetitionRatio'])  # 카페 경쟁강도 수치
        # print(response['data']['cafeCompetitionDesc'])  # 카페 경쟁강도 등급
        # print(f"{idx + 1}. 블로그 경쟁강도({response['data']['blogCompetitionDesc']}) | 카페 경쟁강도({response['data']['cafeCompetitionDesc']})")
        blogCompetitionRatio_lists.append(response['data']['blogCompetitionRatio'])
        blogCompetitionDesc_lists.append(response['data']['blogCompetitionDesc'])
        cafeCompetitionRatio.append(response['data']['cafeCompetitionRatio'])
        cafeCompetitionDesc_lists.append(response['data']['cafeCompetitionDesc'])
        sleep(GENERAL_REQUEST_WAIT_TIME)


def get_keyword_coupang_stats_for_itemscout():

    global coupangCompetitionRatio_lists
    coupangCompetitionRatio_lists = []  # 쿠팡 경쟁강도 수치
    global coupangCompetitionDesc_lists
    coupangCompetitionDesc_lists = []  # 쿠팡 경쟁강도 등급

    headers = {
        'accept': 'application/json, text/plain, */*',
        'origin': 'https://itemscout.io',
        'referer': 'https://itemscout.io/',
        'user-agent': fixed_user_agent,
    }

    for idx, keyword_id in enumerate(keyword_id_lists):
        response = requests.get(f'https://api.itemscout.io/api/v2/keyword/coupang_stats/{keyword_id}', headers=headers).json()
        # pp(response)
        # print(response['data']['coupangCompetitionRatio'])  # 쿠팡 경쟁강도 수치
        # print(response['data']['coupangCompetitionDesc'])  # 쿠팡 경쟁강도 등급
        # print(f"{idx + 1}. 쿠팡 경쟁강도({response['data']['coupangCompetitionDesc']})")
        coupangCompetitionRatio_lists.append(response['data']['coupangCompetitionRatio'])
        coupangCompetitionDesc_lists.append(response['data']['coupangCompetitionDesc'])
        sleep(GENERAL_REQUEST_WAIT_TIME)


def excel_save(select_num):
    df = pd.DataFrame(None)

    global csv_file_path
    if select_num == 1:
        # print(f'\n{C_BOLD}{C_YELLOW}{C_BGBLACK}엑셀파일 (itemscout_{csv_file_path})에 저장 중입니다...{C_END}')
        file_path = f'itemscout_{csv_file_path}'
    else:
        # print(f'\n{C_BOLD}{C_YELLOW}{C_BGBLACK}엑셀파일 (naverdatalab_{csv_file_path})에 저장 중입니다...{C_END}')
        file_path = f'naverdatalab_{csv_file_path}'

    if select_num == 1:
        # df['카테고리'] = itemscout_cid_category_lists
        df['기간'] = itemscout_duration_lists
        df['나이'] = itemscout_age_lists
        df['성별'] = itemscout_gender_list
        df['키워드'] = keyword_name_lists
        df['keywordID'] = keyword_id_lists
        df['랭킹'] = rank_lists
        df['검색수'] = no_of_search_total_lists
        df['상품수'] = prdCnt_lists
        # df['경쟁강도등급'] = competitionIntensityDesc_lists
        # df['광고클릭률등급'] = adClickRateTotalDesc_lists
        # df['블로그경쟁강도등급'] = blogCompetitionDesc_lists
        # df['카페경쟁강도등급'] = cafeCompetitionDesc_lists
        # df['쿠팡경쟁강도등급'] = coupangCompetitionDesc_lists

        count = 1
        product_lists = []
        for x in range(len(keyword_name_lists)):
            temp_dict = {}
            # print(
            #     f"{count}. {itemscout_cid_category_lists[x]} | {itemscout_duration_lists[x]} | {itemscout_age_lists[x]} | {itemscout_gender_list[x]} "
            #     f"| {keyword_name_lists[x]} | {keyword_id_lists[x]} | {rank_lists[x]} | {no_of_search_total_lists[x]} | {prdCnt_lists} | {competitionIntensityDesc_lists} | "
            #     f"{adClickRateTotalDesc_lists} | {blogCompetitionDesc_lists} | {cafeCompetitionDesc_lists} | {coupangCompetitionDesc_lists}")
            # print(
            #     f"{count}. {itemscout_duration_lists[x]} | {itemscout_age_lists[x]} | {itemscout_gender_list[x]} "
            #     f"| {keyword_name_lists[x]} | {keyword_id_lists[x]} | {rank_lists[x]} | {no_of_search_total_lists[x]} | {prdCnt_lists}")
            # temp_dict['cid_category'] = f"{itemscout_cid_category_lists[x]}"
            temp_dict['duration'] = f"{itemscout_duration_lists[x]}"
            temp_dict['age'] = f"{itemscout_age_lists[x]}"
            temp_dict['gender'] = f"{itemscout_gender_list[x]}"
            temp_dict['keyword_name'] = f"{keyword_name_lists[x]}"
            temp_dict['keyword_id'] = f"{keyword_id_lists[x]}"
            temp_dict['rank'] = f"{rank_lists[x]}"
            temp_dict['no_of_search_total'] = f"{no_of_search_total_lists[x]}"
            temp_dict['prdCnt'] = f"{prdCnt_lists[x]}"
            # temp_dict['competitionIntensityDesc'] = f"{competitionIntensityDesc_lists[x]}"
            # temp_dict['adClickRateTotalDesc'] = f"{adClickRateTotalDesc_lists[x]}"
            # temp_dict['blogCompetitionDesc'] = f"{blogCompetitionDesc_lists[x]}"
            # temp_dict['cafeCompetitionDesc'] = f"{cafeCompetitionDesc_lists[x]}"
            # temp_dict['coupangCompetitionDesc'] = f"{coupangCompetitionDesc_lists[x]}"
            product_lists.append(temp_dict)
            count = count + 1

        # print(product_lists)
        # columns = ['cid_category', 'duration', 'age', 'gender', 'keyword_name', 'keyword_id', 'rank', 'no_of_search_total', 'prdCnt', 'competitionIntensityDesc', 'adClickRateTotalDesc', 'blogCompetitionDesc', 'cafeCompetitionDesc', 'coupangCompetitionDesc']
        columns = ['duration', 'age', 'gender', 'keyword_name', 'keyword_id', 'rank',
                   'no_of_search_total', 'prdCnt']
    else:
        print(len(datalab_info_keyword_lists))
        # df['카테고리'] = naver_cid_category_lists
        df['시작기간'] = naver_start_date_lists
        df['끝기간'] = naver_end_date_lists
        df['나이'] = naver_age_lists
        df['성별'] = naver_gender_list
        df['키워드'] = datalab_info_keyword_lists

        count = 1
        product_lists = []
        for x in range(len(datalab_info_keyword_lists)):
            temp_dict = {}
            # print(
            #     f"{count}. {naver_start_date_lists[x]} | {naver_end_date_lists[x]} | {naver_age_lists[x]} "
            #     f"| {naver_gender_list[x]} | {datalab_info_keyword_lists[x]}")
            # temp_dict['cid_category'] = f"{naver_cid_category_lists[x]}"
            temp_dict['start_date'] = f"{naver_start_date_lists[x]}"
            temp_dict['end_date'] = f"{naver_end_date_lists[x]}"
            temp_dict['age'] = f"{naver_age_lists[x]}"
            temp_dict['gender'] = f"{naver_gender_list[x]}"
            temp_dict['datalab_info_keyword'] = f"{datalab_info_keyword_lists[x]}"
            product_lists.append(temp_dict)
            count = count + 1

        # print(product_lists)
        columns = ['start_date', 'end_date', 'age', 'gender', 'datalab_info_keyword']

    df = pd.DataFrame(product_lists, columns=columns)

    # print(tabulate(df, headers='keys', tablefmt='grid'))
    if not os.path.exists(file_path):
        df.to_csv(file_path, mode='w', sep=',', na_rep='NaN', encoding='utf-8-sig', index=False)
    else:
        df.to_csv(file_path, mode='a', sep=',', na_rep='NaN', encoding='utf-8-sig', index=False, header=False)

    # print(f'\n{C_BOLD}{C_YELLOW}{C_BGBLACK}중복된 검색 결과의 엑셀 ({file_path}) 행을 제거 시작{C_END}')
    data = pd.read_csv(file_path)
    if select_num == 1:
        data = data.drop_duplicates(subset=['keyword_name'], keep="first")
    else:
        data = data.drop_duplicates(subset=['datalab_info_keyword'], keep="first")
    data.to_csv(file_path, index=False, encoding="utf-8-sig")
    # print(f'\n{C_BOLD}{C_YELLOW}{C_BGBLACK}중복된 검색 결과의 엑셀행을 제거 완료{C_END}\n')

    # print(f"### excel_save() - {datalab_info_keyword_lists}")

    # # openpyxl 3.0.7 | python 3.8
    # # 정해진 파일안에 계속 쌍이는 데이터
    # if not os.path.exists(file_path):
    #     with pd.ExcelWriter(file_path, mode='w', engine='openpyxl') as writer:
    #         df.to_excel(writer, sheet_name="Sheet1", index=False)
    # else:
    #     workbook = load_workbook(file_path)
    #     writer = pd.ExcelWriter(file_path, engine='openpyxl')
    #     writer.book = workbook
    #     writer.sheets = {ws.title: ws for ws in workbook.worksheets}
    #     df.to_excel(writer, startrow=writer.sheets['Sheet1'].max_row, index=False, header=False)
    #     writer.close()
    #
    # sleep(PAUSE_TIME)
    # print(f'\n{C_BOLD}{C_YELLOW}{C_BGBLACK}엑셀파일 ({file_path})에 저장 완료!!! {C_END}')
    #
    # print(f'\n{C_BOLD}{C_YELLOW}{C_BGBLACK}중복된 검색 결과의 엑셀 ({file_path}) 행을 제거 시작{C_END}')
    # data = pd.read_excel(file_path, sheet_name="Sheet1")
    # data = data.drop_duplicates(subset=['키워드'], keep="first")
    # data.to_excel(file_path, index=False)
    # print(f'\n{C_BOLD}{C_YELLOW}{C_BGBLACK}중복된 검색 결과의 엑셀행을 제거 완료{C_END}\n')
    #
    # df = pd.DataFrame(None)


def get_naverdatalab_cid_info():
    # File I/O Open function for read data from JSON File
    data = {}  # Define Empty Dictionary Object
    try:
        with open(ITEMSCOUT_CONVERSION_MAP_INFO_PATH) as file_object:
            data = json.load(file_object)  # _io.TextIOWrapper > dic
    except ValueError:
        print("Bad JSON file format,  Change JSON File")

    # pp(data)
    return [*data['data'].keys()]  # list 로 반환


def get_itemscout_cid_info():
    # File I/O Open function for read data from JSON File
    data = {}  # Define Empty Dictionary Object
    try:
        with open(ITEMSCOUT_CONVERSION_MAP_INFO_PATH) as file_object:
            data = json.load(file_object)  # _io.TextIOWrapper > dic
    except ValueError:
        print("Bad JSON file format,  Change JSON File")

    # pp(data)
    return [*data['data'].values()]  # list 로 반환


# main start
def main():
    try:
        start_time = time.time()  # 시작 시간 체크
        now = datetime.datetime.now()
        print("START TIME : ", now.strftime('%Y-%m-%d %H:%M:%S'))
        print("\nSTART...")

        print('\n' + C_BOLD + C_YELLOW + C_BGBLACK + '[네이버데이터랩 cid json 파일에서 읽어와 random input 값만들기 시작]', C_END)
        random_naverdatalab_cid_lists = get_naverdatalab_cid_info()
        # random_naverdatalab_cid_lists = ['50000000', '50000001', '50000002', '50000003', '50000004', '50000005',
        #                                 '50000006', '50000007', '50000008', '50000009', '50000010', '50005542']
        random_naverdatalab_age_lists = ['10,20,30,40,50,60', '10', '20', '30', '40', '50',
                                         '60']  # 전체, 10대, 20대, 30대 40대, 50대, 60대이상
        random_naverdatalab_gender_lists = ['f,m', 'f', 'm']  # 전체, 여성, 남성

        random_naverdatalab_input_info_list = list(
            product(random_naverdatalab_cid_lists, random_naverdatalab_age_lists, random_naverdatalab_gender_lists))
        print('\n' + C_BOLD + C_YELLOW + C_BGBLACK + f'[네이버데이터랩 cid json 파일에서 읽어와 random input 값만들기 완료... 총 ({len(random_naverdatalab_input_info_list)})개의 조합]', C_END)

        print('\n' + C_BOLD + C_YELLOW + C_BGBLACK + '[아이템스카우트 cid json 파일에서 읽어와 random input 값만들기 시작]', C_END)
        random_itemscout_cid_lists = get_itemscout_cid_info()
        # 아이템스카우트 정보 설정, 카테고리 (1차 분류만 있을때) - 랜덤 카테고리 말고 조합에 의한 카테고리선정으로 전체의 데이터를 기준으로 계속 돌게 만들어준다.
        # random_itemscout_category_lists = ['패션의류', '패션잡화', '화장품/미용', '디이털/가전', '가구/인테리어',
        #                                 '출산/육아', '식품', '스포츠/레저', '생활/건강', '여가/생활편의', '면세점', '도서']
        # random_itemscout_cid_lists = ['1', '2', '3', '4', '5',
        #                             '6', '7', '8', '9', '10', '11', '45830']
        random_itemscout_age_lists = ['10,10', '20,20', '30,30', '40,40', '50,50', '60,60', '10,20', '10,30', '10,40',
                                      '10,50', '10,60', '20,30', '20,40', '20,50', '20,60'
            , '30,40', '30,50', '30,60', '40,50', '40,60', '50,60']
        random_itemscout_gender_lists = ['f,m', 'f', 'm']  # 전체, 여성, 남성
        random_itemscout_input_info_list = list(
            product(random_itemscout_cid_lists, random_itemscout_age_lists, random_itemscout_gender_lists))
        print('\n' + C_BOLD + C_YELLOW + C_BGBLACK + f'[아이템스카우트 cid json 파일에서 읽어와 random input 값만들기 완료... 총 ({len(random_itemscout_input_info_list)})개의 조합 - ({len(random_itemscout_input_info_list[15638:])})]', C_END)

        while True:
            # while 문으로 계속적인 질문을 처리하는 구조

            # # naver 랜덤 생성 리스트
            # global naver_cid_category_lists
            # naver_cid_category_lists = []
            # global naver_start_date_lists
            # naver_start_date_lists = []
            # global naver_end_date_lists
            # naver_end_date_lists = []
            # global naver_age_lists
            # naver_age_lists = []
            # global naver_gender_list
            # naver_gender_list = []
            #
            # # 데이터랩스 키워드 저장 리스트
            # global datalab_info_keyword_lists
            # datalab_info_keyword_lists = []

            global random_number_list

            print('\n아이템 스카우트에서 상품키워드를 추출 하고자 하면' + C_BOLD +
                  C_RED + ' (1)' + C_END + '번을 입력해 주시고,')
            print('네이버 데이터랩스에서 상품키워드를 추출 하고자 하면' + C_BOLD +
                  C_RED + ' (2)' + C_END + '번을 입력해 주시고,')
            print('프로그램을 종료하고 싶으면' + C_BOLD +
                  C_RED + ' (q)' + C_END + '를 입력해 주세요')

            input_num = input('원하는 번호를 입력하세요 : ')
            # input_num = '2'  # 만약에 네이버데이터랩에서 무조건 상품을 추천받기를 워하면 이 부분을 주석해제하고 바로위에 있는 코드를 주석

            if input_num == 'q':
                print('입력하신 키는 q 입니다...프로그램을 종료합니다. bye...\n')
                sleep(3)
                break

            if input_num == '1':
                print('입력하신 키는 1 입니다...\n')
                sleep(2)

                count = 1
                # for cid, age, gender in random_itemscout_input_info_list:
                # for rnd_num in range(len(random_itemscout_input_info_list)):
                for rnd_num in range(len(random_itemscout_input_info_list[40671:])):  # 적절한 수준에서 키워드 뽑으시기 바랍니다. 해당 숫자는 숫자에 해당하는 카테고리 수까지 만큼 키워드를 생산할 것이다 라는 의미
                    cid, age, gender = random.choice(random_itemscout_input_info_list)
                    print('\n' + C_BOLD + C_YELLOW +
                          C_BGBLACK + 'count : ', count, C_END)

                    # 아이템스카우트 기간
                    duration = '30d'  # (duration 30d 또는 날짜 설정, duration: 2023-03,2023-04 3월부터 4월)

                    # print(f'{C_BOLD}{C_YELLOW}{C_BGBLACK}RANDOM info >>> cid {cid} | duration {duration} | age {age} | gender {gender} {C_END}')

                    # print(f'\n{C_BOLD}{C_YELLOW}{C_BGBLACK}[itemscout 에서 아이템들 리스트를 전체 받기 시작]{C_END}')
                    get_items_for_itemscout(cid, duration, age, gender)
                    sleep(PAUSE_TIME)
                    # print(f'\n{C_BOLD}{C_YELLOW}{C_BGBLACK}[itemscout 에서 아이템들 리스트를 전체 받기 완료]{C_END}')

                    # print(f'\n{C_BOLD}{C_YELLOW}{C_BGBLACK}[itemscout 에서 각 keyword 에 따른 전반적인 분석 시작]{C_END}')
                    # get_keyword_stats_for_itemscout()
                    # sleep(PAUSE_TIME)
                    # print(f'\n{C_BOLD}{C_YELLOW}{C_BGBLACK}[itemscout 에서 각 keyword 에 따른 전반적인 분석 완료]{C_END}')
                    #
                    # print(f'\n{C_BOLD}{C_YELLOW}{C_BGBLACK}[itemscout 에서 각 keyword 에 따른 블로그 카페 분석 시작]{C_END}')
                    # get_keyword_contents_competition_stats_for_itemscout()
                    # sleep(PAUSE_TIME)
                    # print(f'\n{C_BOLD}{C_YELLOW}{C_BGBLACK}[itemscout 에서 각 keyword 에 따른 블로그 카페 분석 완료]{C_END}')
                    #
                    # print(f'\n{C_BOLD}{C_YELLOW}{C_BGBLACK}[itemscout 에서 각 keyword 에 따른 쿠팡 분석 시작]{C_END}')
                    # get_keyword_coupang_stats_for_itemscout()
                    # sleep(PAUSE_TIME)
                    # print(f'\n{C_BOLD}{C_YELLOW}{C_BGBLACK}[itemscout 에서 각 keyword 에 따른 쿠팡 분석 완료]{C_END}')

                    # 엑셀 파일에 저장
                    excel_save(1)
                    count = count + 1

            if input_num == '2':
                print('입력하신 키는 2 입니다...\n')
                sleep(2)

                today = datetime.date.today()
                before_one_month = today - timedelta(days=30)
                start_date = before_one_month
                # 어제 날짜: 오늘 - 1일
                yesterday = today - timedelta(days=1)
                end_date = yesterday

                count = 1
                # for cid, age, gender in random_naverdatalab_input_info_list:
                for rnd_num in range(len(random_naverdatalab_input_info_list)):
                    cid, age, gender = random.choice(random_naverdatalab_input_info_list)
                    print('\n' + C_BOLD + C_YELLOW + C_BGBLACK + 'count : ', count, C_END)

                    # print(f'{C_BOLD}{C_YELLOW}{C_BGBLACK}RANDOM info >>> cid {cid} | start_date {start_date} | endDate {end_date} | age {age} | gender {gender} {C_END}')

                    print('\n' + C_BOLD + C_YELLOW + C_BGBLACK + '[네이버 데이터랩스 정보 가져오기 시작(keyword 추출)]', C_END)
                    # global datalab_info_keyword_lists
                    # datalab_info_keyword_lists = []
                    get_naver_datalab_shopping_insight(cid, start_date, end_date, age, gender)
                    sleep(PAUSE_TIME)
                    print('\n' + C_BOLD + C_YELLOW + C_BGBLACK + '[네이버 데이터랩스 정보 가져오기 완료(keyword 추출)]', C_END)

                    # # 엑셀 파일에 저장
                    excel_save(2)
                    count = count + 1

    finally:
        end_time = time.time()  # 종료 시간 체크
        ctime = end_time - start_time
        time_list = str(datetime.timedelta(seconds=ctime)).split(".")
        print("실행시간 (시:분:초)", time_list)
        now = datetime.datetime.now()
        print("END TIME : ", now.strftime('%Y-%m-%d %H:%M:%S'))
        print("\nEND...")
# main end


if __name__ == '__main__':
    main()
