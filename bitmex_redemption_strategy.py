import bitmex, datetime, sys, warnings
warnings.filterwarnings("ignore")
BITMEX_API_KEY = '' #remplacer par vos clés API
BITMEX_API_SECRET = ''
STRATEGYS_LEVERAGE = 5 #le levier désiré sur la stratégie
def connect_bitmex():
    return bitmex.bitmex(test = False, api_key = BITMEX_API_KEY, api_secret = BITMEX_API_SECRET)
def get_user(bitmex_client):
    return bitmex_client.User.User_getMargin().result()
def get_wallet_balance(user_object):
    #Converting sats to $BTC
    return user_object[0]["walletBalance"] / 100000000
def get_ticker_info(bitmex_client, ticker_name):
    return bitmex_client.Trade.Trade_getBucketed(symbol = ticker_name, binSize="5m", partial = True, count = 1, reverse = True).result()
def get_nb_contracts_xbtusd(user_object, price_xbtusd):
    return get_wallet_balance(user_object) * price_xbtusd * STRATEGYS_LEVERAGE
def get_current_position(bitmex_client):
    open_positions = bitmex_client.Position.Position_get().result()
    try:
        open_position = open_positions[0][0]["currentQty"]
        return open_position
    except Exception as e:
        print(">> Unable to close a trade for [REDEMPTION STRATEGY], no position opened.")
        print(e)
        sys.exit(0)
def short():
    bitmex_client = connect_bitmex()
    user_object = get_user(bitmex_client)
    wallet_balance = get_wallet_balance(user_object)
ticker_info = get_ticker_info(bitmex_client, "XBTUSD")
    price_xbtusd = ticker_info[0][0]["close"]
contracts_ammount = get_nb_contracts_xbtusd(user_object, price_xbtusd)
try:
        bitmex_client.Order.Order_new(symbol="XBTUSD", ordType = 'Market', orderQty = - contracts_ammount).result()
        print(">> Date : %s , %s contracts opened on XBTUSD." % (datetime.datetime.now(), contracts_ammount))
    except Exception as e:
        print(">> Unable to close a trade for XBTUSD : bad bitmex api response.")
        print(e)
def stop_short():
bitmex_client = connect_bitmex()
    current_position = get_current_position(bitmex_client)
    try:
        bitmex_client.Order.Order_new(symbol="XBTUSD", ordType = 'Market', orderQty = - current_position).result()
        print(">> Date : %s , %s contracts closed on XBTUSD." % (datetime.datetime.now(), current_position))
    except Exception as e:
        print(">> Unable to close a trade for XBTUSD : bad bitmex api response.")
        print(e)
def long():
    bitmex_client = connect_bitmex()
    user_object = get_user(bitmex_client)
    wallet_balance = get_wallet_balance(user_object)
ticker_info = get_ticker_info(bitmex_client, "XBTUSD")
    price_xbtusd = ticker_info[0][0]["close"]
contracts_ammount = get_nb_contracts_xbtusd(user_object, price_xbtusd)
try:
        bitmex_client.Order.Order_new(symbol="XBTUSD", ordType = 'Market', orderQty = contracts_ammount).result()
        print(">> Date : %s , %s contracts opened on XBTUSD." % (datetime.datetime.now(), contracts_ammount))
    except Exception as e:
        print(">> Unable to open a trade for XBTUSD : bad bitmex api response.")
        print(e)
def stop_long():
bitmex_client = connect_bitmex()
    current_position = get_current_position(bitmex_client)
    try:
        bitmex_client.Order.Order_new(symbol="XBTUSD", ordType = 'Market', orderQty = - current_position).result()
        print(">> Date : %s , %s contracts closed on XBTUSD." % (datetime.datetime.now(), current_position))
    except Exception as e:
        print(">> Unable to close a trade for XBTUSD : bad bitmex api response.")
        print(e)
