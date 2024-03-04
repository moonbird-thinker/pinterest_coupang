import hmac
import hashlib
import requests
import json
from time import gmtime, strftime
from pprint import pprint as pp

REQUEST_METHOD = "POST"
DOMAIN = "https://api-gateway.coupang.com"
URL = "/v2/providers/affiliate_open_api/apis/openapi/v1/deeplink"

# Replace with your own ACCESS_KEY and SECRET_KEY
ACCESS_KEY = "50240aeb-73f0-4e51-bca6-e7bc304a4be6"
SECRET_KEY = "001519446892ffed3bd581b29064801695a5a78b"

REQUEST = { "coupangUrls": [
    "https://www.coupang.com/vp/products/7733016021?itemId=20784666491&vendorItemId=85248286801", 
    "https://www.coupang.com/vp/products/7187715866?itemId=18141121590&vendorItemId=85293329672"
]}


def generateHmac(method, url, secretKey, accessKey):
    path, *query = url.split("?")
    datetimeGMT = strftime('%y%m%d', gmtime()) + 'T' + strftime('%H%M%S', gmtime()) + 'Z'
    message = datetimeGMT + method + path + (query[0] if query else "")

    signature = hmac.new(bytes(secretKey, "utf-8"),
                         message.encode("utf-8"),
                         hashlib.sha256).hexdigest()

    return "CEA algorithm=HmacSHA256, access-key={}, signed-date={}, signature={}".format(accessKey, datetimeGMT, signature)


authorization = generateHmac(REQUEST_METHOD, URL, SECRET_KEY, ACCESS_KEY)
url = "{}{}".format(DOMAIN, URL)
response = requests.request(method=REQUEST_METHOD, url=url,
                            headers={
                                "Authorization": authorization,
                                "Content-Type": "application/json"
                            },
                            data=json.dumps(REQUEST)
                            )

pp(response.json())
res_info = response.json()

print(res_info['data'][0]['shortenUrl'])
print(res_info['data'][1]['shortenUrl'])