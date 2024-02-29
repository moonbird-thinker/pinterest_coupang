import random
from bs4 import BeautifulSoup
import requests
import re

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

# partner product info
product_name_lists = []  # 상품명
product_discount_rate_lists = []  # 할인률과 원래가격
product_price_lists = []  # 상품가격
product_arrival_time_lists = []  # 도착예정시간
product_rating_star_lists = []  # star 평가: ex.3.5
product_review_lists = []  # 상품리뷰 수
product_link_lists = []  # 상품 구매 링크
product_image_lists = []  # 상품 이미지

keyword = '미니로디니니트'

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

# print(len(all_search_product_lists))
# print(len(ad_search_product_lists))
# print(len(rank_product_lists))

if len(rank_product_lists) < 10:
    print('검색된 결과가 없거나 10개 이하입니다. 다시금 시도하세요')
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

for inner in rank_product_lists[:10]:
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