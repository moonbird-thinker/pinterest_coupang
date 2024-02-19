import os
import time
import requests
from datetime import date
from datetime import timedelta
from datetime import datetime
import random
from pprint import pprint as pp
import json
from pathlib import Path
import pandas as pd
import numpy as np
from tabulate import tabulate
from time import sleep

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


# ------------------------------------------------------------------------------------------------ START #
# 개인 입력 / 수정이 필요한 부분
# ------------------------------------------------------------------------------------------------ START #

ITEMSCOUT_CATEGORY_MAP_SHORTEN_INFO_PATH = 'itemscout_category_map_shorten_info.json'

ITEMSCOUT_CONVERSION_MAP_INFO_PATH = 'itemscout_conversion_info.json'

CATEGORY_MAP_INFO_CSV_FILE_PATH = 'category_map_info.csv'

# PAUSE_TIME = random.randint(1, 2)
PAUSE_TIME = 60

# ------------------------------------------------------------------------------------------------ END #


# ------------------------------------------------------------------------------------------------ START #
# 시스템 공통 입력 정보
# ------------------------------------------------------------------------------------------------ START #
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

# ------------------------------------------------------------------------------------------------ END #

def get_itemscout_categories_map_shorten_info():
    url = f'https://api.itemscout.io/api/category/categories_map_shorten'
    headers = {
        'User-Agent': random_user_agent,
    }
    response = requests.get(url, headers=headers)
    # pp(response.json())  # requests.models.Response > dict
    
    Path(ITEMSCOUT_CATEGORY_MAP_SHORTEN_INFO_PATH).touch(exist_ok=True)
    with open(ITEMSCOUT_CATEGORY_MAP_SHORTEN_INFO_PATH, "w", encoding="UTF-8") as output_file:
        json.dump(response.json(), output_file, ensure_ascii=False, indent=4, separators=(',', ': '))  # dic > _io.TextIOWrapper


def get_itemscout_conversion_map_info():
    url = f'https://api.itemscout.io/api/category/conversion_map'
    headers = {
        'User-Agent': random_user_agent,
    }
    response = requests.get(url, headers=headers)
    # pp(response.json())  # requests.models.Response > dict
    
    # here we create new xxx.json file with write mode using file i/o operation
    Path(ITEMSCOUT_CONVERSION_MAP_INFO_PATH).touch(exist_ok=True)
    with open(ITEMSCOUT_CONVERSION_MAP_INFO_PATH, "w", encoding="UTF-8") as output_file:
        json.dump(response.json(), output_file, ensure_ascii=False, indent=4, separators=(',', ': '))  # dic > _io.TextIOWrapper


def get_naverdatalab_cid_info():
    # File I/O Open function for read data from JSON File
    data = {} #Define Empty Dictionary Object
    try:
        with open(ITEMSCOUT_CONVERSION_MAP_INFO_PATH) as file_object:
            data = json.load(file_object)   # _io.TextIOWrapper > dic
    except ValueError:
        print("Bad JSON file format,  Change JSON File")
        
    # pp(data)
    # print([*data['data'].keys()])  # [*data['data']] 같은것
    return [*data['data'].keys()]  # list 로 반환
        

def get_itemscout_category_map_info_to_csv():
    url = f'https://api.itemscout.io/api/category/0/subcategories'
    headers = {
        'User-Agent': random_user_agent,
    }
    response = requests.get(url, headers=headers)
    data_lv1 = response.json()
    # pp(data_lv1)
    
    category_list = []
    for i in range(len(data_lv1['data'])):
        sleep(PAUSE_TIME)
        # temp_dic = {}
        # print(f"\ndata_lv1 id : {data_lv1['data'][i]['id']}, name : {data_lv1['data'][i]['name']}")
        data_lv1_id = data_lv1['data'][i]['id']
        data_lv1_name = data_lv1['data'][i]['name']        

        url = f'https://api.itemscout.io/api/category/{data_lv1_id}/subcategories'
        headers = {
            'User-Agent': random_user_agent,
        }
        response = requests.get(url, headers=headers)
        data_lv2 = response.json()
        # pp(data_lv2)
        
        for j in range(len(data_lv2['data'])):
            # temp_dic = {}
            # print(f"data_lv2 id : {data_lv2['data'][j]['id']}, name : {data_lv2['data'][j]['name']}")
            data_lv2_id = data_lv2['data'][j]['id']
            data_lv2_name = data_lv2['data'][j]['name']  
            # temp_dic['cid1'] = data_lv1_id
            # temp_dic['name1'] = data_lv1_name
            # temp_dic['cid2'] = data_lv2_id
            # temp_dic['name2'] = data_lv2_name
            # category_list.append(temp_dic)
            
            url = f'https://api.itemscout.io/api/category/{data_lv2_id}/subcategories'
            headers = {
                'User-Agent': random_user_agent,
            }
            response = requests.get(url, headers=headers)
            data_lv3 = response.json()
            # pp(data_lv3)
            
            for k in range(len(data_lv3['data'])):
                # sleep(PAUSE_TIME)
                temp_dic = {}
                # print(f"data_lv3 id : {data_lv3['data'][k]['id']}, name : {data_lv3['data'][k]['name']}")
                data_lv3_id = data_lv3['data'][k]['id']
                data_lv3_name = data_lv3['data'][k]['name']
                temp_dic['cid1'] = data_lv1_id
                temp_dic['name1'] = data_lv1_name
                temp_dic['cid2'] = data_lv2_id
                temp_dic['name2'] = data_lv2_name
                temp_dic['cid3'] = data_lv3_id
                temp_dic['name3'] = data_lv3_name
                category_list.append(temp_dic)

                url = f'https://api.itemscout.io/api/category/{data_lv3_id}/subcategories'
                headers = {
                    'User-Agent': random_user_agent,
                }
                response = requests.get(url, headers=headers)
                data_lv4 = response.json()
                # pp(data_lv4)
                # print(len(data_lv4['data']))
                if len(data_lv4['data']) == 0:
                    continue
                else:
                    category_list.pop()  # 마지막 리스트 제거

                for p in range(len(data_lv4['data'])):
                    # sleep(PAUSE_TIME)
                    temp_dic = {}
                    # print(f"data_lv4 id : {data_lv4['data'][k]['id']}, name : {data_lv4['data'][k]['name']}")
                    data_lv4_id = data_lv4['data'][p]['id']
                    data_lv4_name = data_lv4['data'][p]['name']
                    temp_dic['cid1'] = data_lv1_id
                    temp_dic['name1'] = data_lv1_name
                    temp_dic['cid2'] = data_lv2_id
                    temp_dic['name2'] = data_lv2_name
                    temp_dic['cid3'] = data_lv3_id
                    temp_dic['name3'] = data_lv3_name
                    temp_dic['cid4'] = data_lv4_id
                    temp_dic['name4'] = data_lv4_name
                    category_list.append(temp_dic)

    df = pd.DataFrame(category_list)
    df = df.replace(np.nan, '')

    print(tabulate(df, headers='keys', tablefmt='grid'))
    if not os.path.exists(CATEGORY_MAP_INFO_CSV_FILE_PATH):
        df.to_csv(CATEGORY_MAP_INFO_CSV_FILE_PATH, mode='w', sep=',', na_rep='NaN', encoding='utf-8-sig', index=False)
    else:
        df.to_csv(CATEGORY_MAP_INFO_CSV_FILE_PATH, mode='a', sep=',', na_rep='NaN', encoding='utf-8-sig', index=False, header=False)

    # print(f'\n{C_BOLD}{C_YELLOW}{C_BGBLACK}중복된 검색 결과의 엑셀 ({CATEGORY_MAP_INFO_CSV_FILE_PATH}) 행을 제거 시작{C_END}')
    # data = pd.read_csv(CATEGORY_MAP_INFO_CSV_FILE_PATH)
    # data = data.drop_duplicates(subset=['keyword', 'title'], keep="first")
    # data.to_csv(CATEGORY_MAP_INFO_CSV_FILE_PATH, index=False, encoding="utf-8-sig")
    # print(f'\n{C_BOLD}{C_YELLOW}{C_BGBLACK}중복된 검색 결과의 엑셀행을 제거 완료{C_END}\n')


# main start
def main():
    try:
        print("\nSTART...")
        start_time = time.time()
        now = datetime.now()
        print("START TIME : ", now.strftime('%Y-%m-%d %H:%M:%S'))

        print(f"\n{C_BOLD}{C_YELLOW}{C_BGBLACK}[itemscout categorys map shorten 정보 가져오기 시작]{C_END}")
        get_itemscout_categories_map_shorten_info()
        print(f"\n{C_BOLD}{C_YELLOW}{C_BGBLACK}[itemscout categorys map shorten 정보 가져오기 완료]{C_END}")
        
        print(f"\n{C_BOLD}{C_YELLOW}{C_BGBLACK}[itemscout conversion map 정보 가져오기 시작]{C_END}")
        get_itemscout_conversion_map_info()
        print(f"\n{C_BOLD}{C_YELLOW}{C_BGBLACK}[itemscout conversion map 정보 가져오기 완료]{C_END}")
        
        print(f"\n{C_BOLD}{C_YELLOW}{C_BGBLACK}[itemscout conversion map 정보를 이용하여 네이버 cid 모두 가져오기 시작(return list)]{C_END}")
        get_naverdatalab_cid_info()
        print(f"\n{C_BOLD}{C_YELLOW}{C_BGBLACK}[itemscout conversion map 정보를 이용하여 네이버 cid 모두 가져오기 완료(return list)]{C_END}")
        
        print(f"\n{C_BOLD}{C_YELLOW}{C_BGBLACK}[itemscout categorys map 정보 엑셀 저장 시작]{C_END}")
        print(f'\n시간이 다소 소요 됩니다 추출중...')
        get_itemscout_category_map_info_to_csv()
        print(f"\n{C_BOLD}{C_YELLOW}{C_BGBLACK}[itemscout categorys map 정보 엑셀 저장 완료]{C_END}")

    finally:
        end_time = time.time()
        ctime = end_time - start_time
        time_list = str(timedelta(seconds=ctime)).split(".")
        print("\n실행시간 (시:분:초)", time_list)
        print("END...")
# main end


if __name__ == '__main__':
    main()


# 참고자료:
# https://guru99.com/ko/python-json.html?gpp&gpp_sid
