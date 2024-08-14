

import json
import time

import requests

url_oc      = "https://www.nseindia.com/option-chain"
url_bnf     = 'https://www.nseindia.com/api/option-chain-indices?symbol=BANKNIFTY'
url_nf      = 'https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY'
url_indices = "https://www.nseindia.com/api/allIndices"

# Headers
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
            'accept-language': 'en,gu;q=0.9,hi;q=0.8',
            'accept-encoding': 'gzip, deflate, br'}

sess = requests.Session()
cookies = dict()

# Local methods
def set_cookie():
    request = sess.get(url_oc, headers=headers, timeout=5)
    cookies = dict(request.cookies)
def get_data(url):
    set_cookie()
    response = sess.get(url, headers=headers, timeout=5, cookies=cookies)
    if(response.status_code==401):
        set_cookie()
        response = sess.get(url_nf, headers=headers, timeout=5, cookies=cookies)
    if(response.status_code==200):
        return response.text
    return ""

def filename(opdata) : return opdata["records"]["timestamp"].replace(":","_")
# def getdata(): return get_data(url_bnf)
name=""
for ch in range(1000):
    try:
        time.sleep(60)
        oidata=get_data(url_bnf)
        # filename(oidata)
        if (filename(json.loads(oidata)) != name):
            with open(f"optionchaindatabnf//{filename(json.loads(oidata))}_{ch}.txt", "w") as f:
                f.write(oidata)
                print("write done ")
        name = filename(json.loads(oidata))
        print(f"done ******* {ch} ")
    except Exception as e:
        print(str(e))


# with open("iotxtfiles/helo.txt", "w") as f:
#     f.write("qqq")

