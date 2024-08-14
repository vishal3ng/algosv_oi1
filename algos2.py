import datetime


import json
import time
import sqlite3
import math
import pandas
import requests
import matplotlib.pyplot as plt

def create_db(tablename):
    print("table name is "+tablename)
    db_name = datetime.datetime.now().strftime("%d_%m_%Y")
    print("db name is "+db_name)
    db = sqlite3.connect(db_name)
    driver = db.cursor()
    driver.execute("CREATE TABLE IF NOT EXISTS "+tablename+"(TIME time,COI INT,nCOI INT,POI INT,nPOI INT,CVOL INT,PVOL INT)")
    return driver,db

oi_data=""
url_oc      = "https://www.nseindia.com/option-chain"
url_bnf     = 'https://www.nseindia.com/api/option-chain-indices?symbol=BANKNIFTY'
url_fnf     = 'https://www.nseindia.com/api/option-chain-indices?symbol=FINNIFTY'
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
    request = sess.get(url_oc, headers=headers, timeout=15)
    cookies = dict(request.cookies)
def get_data(url):
    set_cookie()
    response = sess.get(url, headers=headers, timeout=15, cookies=cookies)
    if(response.status_code==401):
        set_cookie()
        response = sess.get(url, headers=headers, timeout=15, cookies=cookies)
    if(response.status_code==200):
        return json.loads(response.text)
    return ""


def call_putOI_nearstr(opdata,rangestr=10,merge=2,nf_bnf=50):
    oidata = []
    calloi_sum = []
    putoi_sum = []
    ce_stricklist = []
    pe_stricklist = []
    strick=math.ceil((opdata["records"]["underlyingValue"])/nf_bnf)
    for ch in range(rangestr):
        ce_stricklist.append(int(strick+(ch-merge))*nf_bnf)
        pe_stricklist.append(int(strick-(ch-merge))*nf_bnf)
    print(ce_stricklist)
    print(pe_stricklist)
    for ch in range(len(ce_stricklist)):
        for allstr in range(90):
            if ce_stricklist[ch] == opdata["filtered"]["data"][allstr]["strikePrice"]:
                calloi_sum.append(opdata["filtered"]["data"][allstr]["CE"]["openInterest"])
            if pe_stricklist[ch] == opdata["filtered"]["data"][allstr]["strikePrice"]:
                putoi_sum.append(opdata["filtered"]["data"][allstr]["PE"]["openInterest"])
    return sum(calloi_sum),sum(putoi_sum)
def basic_oi():
    global oi_data
    opdata = (get_data(url_fnf))
    noi=call_putOI_nearstr(opdata)
    try:
        # noi = call_putOI_nearstr(opdata)
        time = opdata["records"]["timestamp"][12:]
        totalCeOI=opdata["filtered"]["CE"]["totOI"]
        totalPeOI=opdata["filtered"]["PE"]["totOI"]
        totalCeVol=opdata["filtered"]["CE"]["totVol"]
        totalPeVol=opdata["filtered"]["PE"]["totVol"]
        oi_data=[time,totalCeOI,noi[0],totalPeOI,noi[1],totalCeVol,totalPeVol]
        return oi_data
    except Exception:
        print("bank data from nse ")
        return oi_data
def row_time(opdata) : return opdata["records"]["timestamp"].replace(":","_")

def loadsampleoidata(tablename,data):
    driver=create_db(tablename)
    driver[0].execute("INSERT INTO "+tablename+" VALUES(?,?,?,?,?,?,?)",data)
    driver[1].commit()

for ch in range(1000):
    # try:
        time.sleep(10)
        print("now run "+str(ch))
        loadsampleoidata("simpleoi",basic_oi())

        driver = create_db("simpleoi")
        table = driver[0].execute("select * from simpleoi")
        sql = """select * from simpleoi"""

        data = pandas.read_sql(sql, driver[1])
        #pt 1
        plt.subplot(1, 2, 1)
        plt.plot(data.TIME, data.COI, label="up down",color='red')
        plt.plot(data.TIME, data.POI, label="up up",color='green')
        # plt.legend()
        plt.title("call vs put oi ***")
        #pt 2
        plt.subplot(1, 2, 2)
        plt.plot(data.TIME, data.nCOI, label="up down",color='red')
        plt.plot(data.TIME, data.nPOI, label="up up",color='green')

        plt.title("near call vs put")
        plt.show(block=False)
        plt.pause(10)
        print("after graph ")
        for x in table:
            print(x)
    # except Exception:
    #     print("fail to load a ")
