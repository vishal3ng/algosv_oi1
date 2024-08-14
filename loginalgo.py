import time
from datetime import datetime
from configparser import ConfigParser
import timestamp
from breeze_connect import BreezeConnect
import pandas as pd
import  logging
filename = "execution_algo_logs"
functionalData = ConfigParser()
functionalData.read("placement_data.ini")
logging.basicConfig(filename="execution_algo_logs.log", level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
### Data  ###
Stock_name = functionalData.get("equity", "stock_name")
Product = functionalData.get("equity", "product")
total_quantities = int(functionalData.get("equity", "total_quantities"))
slice_quantities = int(functionalData.get("equity", "slice_quantities"))
start_time = functionalData.get("equity", "start_time")
end_time = functionalData.get("equity", "end_time")
time_interval_inSec = float(functionalData.get("equity", "time_interval_inSec"))

### Key's ###
app_key = "44G6u9$66wy51895c501`7(8947D5652"
secret_key = "160CI3O0(9G54756437!+4e6vu3L612T"
session_token = "40880101"

def place_order():
    placeOrderResponce = (
        isec.place_order(Stock_name, "NSE", "cash", "Buy", "limit", "0", slice_quantities, lower_price, "Day", "0", "0", "0",
                         "Call", "0", "algo_sample", "Fresh", "0", "0", "0", "0"))
    logging.info(f"Order response {placeOrderResponce}")
    return placeOrderResponce["Success"]
def login_insta():
    isec = BreezeConnect(api_key=app_key)
    # Generate Session
    isec.generate_session(api_secret=secret_key,
                          session_token=session_token)
    return isec


isec = login_insta()

get_quotes = isec.get_quotes(Stock_name, "NSE", "0", "cash", "call")
lower_price = ((get_quotes['Success'][0])["lower_circuit"])
print(lower_price)
#
# def rangeAndQnt():
#     lower = total_quantities//slice_quantities
#     higher = total_quantities/slice_quantities
#     if higher > lower:
#         count = lower + 1
#     else:
#         count = lower
#     count
# # xxx=pd.DataFrame(iiii["Success"])
# for time_inter in range(2):
#     place_order()
#     time.sleep(time_interval_inSec)
#
#
# def place_order():
#     placeOrderResponse = (
#         isec.place_order(Stock_name, "NSE", "cash", "Buy", "limit", "0", slice_quantities, lower_price, "Day", "0", "0", "0",
#                          "Call", "0", "algo_sample", "Fresh", "0", "0", "0", "0"))
#     logging.info(f"Order response {placeOrderResponse}")
#     return placeOrderResponse["Success"]
isec.get_option_chain_quotes()
isec.get_historical_data_v2()