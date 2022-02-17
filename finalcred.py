from jugaad_trader import Zerodha
import time
import pandas as pd
import requests
import re
import datetime
from ks_api_client import ks_api



 
# Set access token loads the stored session.
# Name chosen to keep it compatible with kiteconnect.
## $ jtrader zerodha startsession 
# FT2891
# Zero@Kite
# 110425
#API manager details are these Username:SHIBHA11 Password: Algo@200@

#https://api.kite.trade/instruments - to get instrument token from zerodha
#to get instrument token from kotaksecurity
#https://preferred.kotaksecurities.com/security/production/TradeApiInstruments_FNO_02_02_2022.txt
#https://preferred.kotaksecurities.com/security/production/TradeApiInstruments_Cash_02_02_2022.txt
#https://tradeapi.kotaksecurities.com/devportal/apis - tradeapi
#https://sbx.kotaksecurities.com/devportal/apis - restapi
#https://github.com/osparamatrix/ks-orderapi-python - ksapi

#steps to create a new bot:- #https://www.youtube.com/watch?v=pZpDCfGCIZI
'''a. Create new bot and generate bot token - @botfather
   b. Open your bot with the help of username and type /start
   c. Use this URL to get chat ID
   d. use bot_token and chat_ID in python code.
'''

def execute_order():
    
    def get_message():
            telegram_auth_token = "5177017436:AAHHpFAsmeFnWhCEK3cMHBfssJmQdS1Ckhs"
            telegram_group_id = "getyourerroralert"

            msg = f"Error in placing order"

            def send_msg_on_telegram(message):
                telegram_api_url = f"https://api.telegram.org/bot{telegram_auth_token}/sendMessage?chat_id=@{telegram_group_id}&text={message}"
                tel_resp = requests.get(telegram_api_url)

                if tel_resp.status_code == 200:
                    print("Message has been sent on telegram")
                else:
                    print("Error:Could not send Message")

            send_msg_on_telegram(msg)

    def generate_session():
        generate_session.client = ks_api.KSTradeApi(access_token = "2e1c3c6c-6b63-3287-9dbf-6feb33912d3a", userid = "Shibha11", consumer_key = "d3nTiigogTcdpfgCAEff67dr_0Aa", ip = "127.0.0.1",app_id='gYqMAv2tyX0DR6lSiLeFQrdcsU8a')
        generate_session.client.login(password = "Algo@200@")
        generate_session.client.session_2fa(access_code = '9403')
    generate_session()

    url =  'https://tradeapi.kotaksecurities.com/apim/scripmaster/1.1/filename'
    headers = {'accept' : 'application/json', 'consumerKey' : 'd3nTiigogTcdpfgCAEff67dr_0Aa', 'Authorization':'Bearer 2e1c3c6c-6b63-3287-9dbf-6feb33912d3a'}
    res = requests.get(url,headers=headers).json()
    cashurl = res['Success']['cash']
    fnourl = res['Success']['fno']
    print(cashurl)
    print(fnourl)
    cashdf = pd.read_csv(cashurl,sep='|')
    fnodf = pd.read_csv(fnourl,sep='|')
    placed_orders = []
    count = 0
    while True:
        count+=1
        def get_zerodha_orders():
            kite = Zerodha()
            kite.set_access_token()
            get_zerodha_orders.orders = kite.orders()
            print("Number of orders: {} \n".format(len(get_zerodha_orders.orders)))
        try:
           get_zerodha_orders()
        except Exception as e:
            print("loop is ended")
            break

        if len(get_zerodha_orders.orders)==0:
           print("No orders")
        else:
           for order in range(len(get_zerodha_orders.orders)):
               print(get_zerodha_orders.orders[order])
               inst_name1 = re.findall("NIFTY",get_zerodha_orders.orders[order]["tradingsymbol"])
               inst_name2 = re.findall("BANKNIFTY",get_zerodha_orders.orders[order]["tradingsymbol"])
               if (inst_name1)or(inst_name2):
                  if get_zerodha_orders.orders[order]["status"] == 'OPEN':
                      if get_zerodha_orders.orders[order]["order_id"] not in placed_orders:

                                    def get_instrument_token(myorder):

                                        try:
                                            global instrumenttoken
                                            if myorder["tradingsymbol"] in cashdf['instrumentName']:
                                                instrument_index = cashdf.index[(cashdf['instrumentName'] == myorder["tradingsymbol"]) & (cashdf['exchange'] == 'NSE')].tolist()
                                                cashdf['instrumentToken'] = cashdf['instrumentToken'].astype(str)
                                                instrumenttoken = cashdf['instrumentToken'][instrument_index[0]]
                     
                                            else:
                                                trading_symbol = myorder["tradingsymbol"]

                                                x = re.findall("[A-Z]", trading_symbol)
                                                instrument_name = ''.join(x[:-2])
                                                option_type = ''.join(x[-2:])

                                                c = re.findall("[0-9]",trading_symbol)
                                                expirydate = ''.join(c[:5])
                                                exchange_price = ''.join(c[5:])
                                                a = expirydate[:2]
                                                y = '20'+a
                                                b = expirydate[2:3]
                                                d = expirydate[3:]
                                                v = datetime.datetime(int(y),int(b),int(d))
                                                expiry_date = v.strftime('%d%b%y').upper()
                                                instrument_index = fnodf.index[(fnodf.instrumentName == instrument_name ) & (fnodf.exchange == 'NSE') & (fnodf.optionType == option_type) & (fnodf.expiry == expiry_date) & (fnodf.strike == float(exchange_price))].tolist()
                                                fnodf['instrumentToken'] = fnodf['instrumentToken'].astype(str)
                                                instrumenttoken = fnodf['instrumentToken'][instrument_index[0]]
                                  

                                        except Exception as e:
                                            print("Error in placing order",e)
                                    get_instrument_token(get_zerodha_orders.orders[order])
                                            



                                    def place_kotak_orders(myorder):
                                        generate_session()
                                        if myorder["order_type"] == "LIMIT":
                                           myorder["order_type"] = "N"
                                        elif myorder["order_type"] == "MARKET":
                                            myorder["order_type"] = "O"
                                        else:
                                            myorder["order_type"] = "N"
                
                                        '''if orders[order]["validity"] == "DAY":
                                        orders[order]["validity"] == "GFD"'''
                                        '''print(myorder["order_type"])
                                        print(get_instrument_token.instrumenttoken)
                                        print(myorder["transaction_type"])
                                        print(myorder["quantity"])
                                        print(myorder["price"])
                                        print(myorder["disclosed_quantity"])
                                        print(myorder["variety"])
                                        print(myorder["tag"])'''
                                        
                                        try: 
                                            generate_session.client.place_order(order_type = myorder["order_type"], instrument_token = int(instrumenttoken),  \
                                            transaction_type = myorder["transaction_type"], quantity = myorder["quantity"], price = myorder["price"] ,\
                                            disclosed_quantity = myorder["disclosed_quantity"], trigger_price = myorder["trigger_price"],\
                                            validity = "GFD", variety = myorder["variety"].upper(), tag = str(myorder["tag"]))
                                            print("Success")
                                        except Exception as e:
                                            print("Error",e)
                                            get_message()
                                        
                                        placed_orders.append(myorder["order_id"])


                                    
                                    place_kotak_orders(get_zerodha_orders.orders[order])
                      else:
                        pass

                  else:
                     print("Status is not open")
               else:
                    print("Not BANKNIFTY or NIFTY")
        time.sleep(180)
    print(count)           
execute_order()

'''placed_by : FT2891
order_id : 220204001328402
exchange_order_id : 1000000046558162
parent_order_id : None
status : OPEN
status_message : None
status_message_raw : None
order_timestamp : 2022-02-04 10:28:27
exchange_update_timestamp : 2022-02-04 10:28:27
exchange_timestamp : 2022-02-04 10:28:27
variety : regular
exchange : NFO
tradingsymbol : NIFTY2221016000PE
instrument_token : 12628482
order_type : LIMIT
transaction_type : BUY
validity : DAY
product : MIS
quantity : 50
disclosed_quantity : 0
price : 0.15
trigger_price : 0
average_price : 0
filled_quantity : 0
pending_quantity : 50
cancelled_quantity : 0
market_protection : 0
meta : {}
tag : None
guid : 01XHEb4qOm0sNWP'''